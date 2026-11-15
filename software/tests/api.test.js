/**
 * Automated Test Suite for Transformer CBM Cloud Edge Worker
 * Validates Routing, Device Authentication, Role Permissions, and Database Operations
 */

import { test, describe, before, beforeEach } from 'node:test';
import assert from 'node:assert/strict';
import worker from '../src/worker.js';

// In-Memory SQLite Mock for Testing D1 API without external network
class MockD1Database {
  constructor() {
    this.telemetryRows = [];
    this.commands = [];
    this.alerts = [];
    this.users = [
      { email: 'admin@gmail.com', name: 'System Administrator', role: 'ADMIN', added_at: new Date().toISOString() }
    ];
    this.settings = {};
  }

  prepare(sql) {
    const db = this;
    const boundArgs = [];

    return {
      bind(...args) {
        boundArgs.push(...args);
        return this;
      },
      async run() {
        const cleanSql = sql.trim().toUpperCase();
        if (cleanSql.startsWith('INSERT INTO TELEMETRY')) {
          const row = {
            id: db.telemetryRows.length + 1,
            device_id: boundArgs[0],
            t_core: boundArgs[1],
            t_inlet: boundArgs[2],
            t_predicted: boundArgs[3],
            rate_of_rise: boundArgs[4],
            v_12v: boundArgs[5],
            i_12v: boundArgs[6],
            v_5v: boundArgs[7],
            i_5v: boundArgs[8],
            v_3v3: boundArgs[9],
            i_3v3: boundArgs[10],
            pson_active: boundArgs[11],
            fault_code: boundArgs[12],
            created_at: new Date().toISOString()
          };
          db.telemetryRows.push(row);
          return { success: true };
        }
        if (cleanSql.startsWith('INSERT INTO COMMANDS')) {
          const cmd = {
            id: db.commands.length + 1,
            device_id: boundArgs[0],
            command_type: boundArgs[1],
            payload: boundArgs[2],
            status: 'PENDING',
            issued_by: boundArgs[3],
            issued_at: new Date().toISOString()
          };
          db.commands.push(cmd);
          return { success: true };
        }
        if (cleanSql.startsWith('UPDATE COMMANDS')) {
          // Cancel previous pending commands or mark executed
          if (cleanSql.includes("SET STATUS = 'CANCELLED'")) {
            db.commands.forEach(c => {
              if (c.device_id === boundArgs[0] && c.status === 'PENDING') c.status = 'CANCELLED';
            });
          } else if (cleanSql.includes("SET STATUS = 'EXECUTED'")) {
            const cmd = db.commands.find(c => c.id === boundArgs[0]);
            if (cmd) {
              cmd.status = 'EXECUTED';
              cmd.executed_at = new Date().toISOString();
            }
          }
          return { success: true };
        }
        if (cleanSql.startsWith('INSERT INTO INCIDENT_ALERTS')) {
          db.alerts.push({
            id: db.alerts.length + 1,
            device_id: boundArgs[0],
            incident_type: boundArgs[1],
            details: boundArgs[2],
            t_core: boundArgs[3],
            email_dispatched: boundArgs[4],
            created_at: new Date().toISOString()
          });
          return { success: true };
        }
        if (cleanSql.startsWith('INSERT INTO AUTHORIZED_USERS')) {
          db.users.push({
            email: boundArgs[0],
            name: boundArgs[1],
            role: boundArgs[2],
            added_at: new Date().toISOString()
          });
          return { success: true };
        }
        if (cleanSql.startsWith('DELETE FROM AUTHORIZED_USERS')) {
          db.users = db.users.filter(u => u.email.toLowerCase() !== boundArgs[0].toLowerCase());
          return { success: true };
        }
        if (cleanSql.startsWith('INSERT INTO SYSTEM_SETTINGS')) {
          db.settings[boundArgs[0]] = String(boundArgs[1]);
          return { success: true };
        }
        return { success: true };
      },
      async first() {
        const cleanSql = sql.trim().toUpperCase();
        if (cleanSql.includes('FROM SYSTEM_SETTINGS')) {
          const val = db.settings[boundArgs[0]];
          return val !== undefined ? { value: val } : null;
        }
        if (cleanSql.includes('FROM TELEMETRY')) {
          return db.telemetryRows[db.telemetryRows.length - 1] || null;
        }
        if (cleanSql.includes('FROM COMMANDS') && cleanSql.includes("STATUS = 'PENDING'")) {
          return db.commands.find(c => c.device_id === boundArgs[0] && c.status === 'PENDING') || null;
        }
        if (cleanSql.includes('FROM AUTHORIZED_USERS')) {
          return db.users.find(u => u.email.toLowerCase() === boundArgs[0].toLowerCase()) || null;
        }
        return null;
      },
      async all() {
        const cleanSql = sql.trim().toUpperCase();
        if (cleanSql.includes('FROM TELEMETRY')) {
          return { results: [...db.telemetryRows] };
        }
        if (cleanSql.includes('FROM INCIDENT_ALERTS')) {
          return { results: [...db.alerts] };
        }
        if (cleanSql.includes('FROM AUTHORIZED_USERS')) {
          return { results: [...db.users] };
        }
        return { results: [] };
      }
    };
  }
}

describe('Transformer CBM Cloud Worker Tests', () => {
  let mockEnv;
  let mockCtx;

  beforeEach(() => {
    mockEnv = {
      ENVIRONMENT: 'development',
      DEVICE_KEY: 'test-device-secret-key',
      ALLOWED_EMAILS: 'admin@gmail.com',
      DB: new MockD1Database()
    };
    mockCtx = {
      waitUntil: (promise) => promise
    };
  });

  test('GET /api/health returns healthy status', async () => {
    const req = new Request('http://localhost/api/health');
    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.status, 'healthy');
  });

  test('POST /api/telemetry rejects without valid X-Device-Key', async () => {
    const req = new Request('http://localhost/api/telemetry', {
      method: 'POST',
      headers: { 'X-Device-Key': 'wrong-key', 'Content-Type': 'application/json' },
      body: JSON.stringify({ t_core: 35.0, t_inlet: 28.0 })
    });
    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 401);
  });

  test('POST /api/telemetry successfully accepts telemetry and saves to D1', async () => {
    const payload = {
      device_id: 'TRANSFORMER_01',
      t_core: 38.5,
      t_inlet: 27.2,
      t_predicted: 40.1,
      rate_of_rise: 0.05,
      v_12v: 12.02,
      i_12v: 3.4,
      pson_active: 1
    };

    const req = new Request('http://localhost/api/telemetry', {
      method: 'POST',
      headers: { 'X-Device-Key': 'test-device-secret-key', 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.status, 'acknowledged');
    assert.equal(body.pending_command, 'NONE');

    // Verify persisted in DB
    const latest = await mockEnv.DB.prepare('SELECT * FROM telemetry WHERE device_id = ?').bind('TRANSFORMER_01').first();
    assert.ok(latest);
    assert.equal(latest.t_core, 38.5);
  });

  test('Protected routes reject unauthenticated requests', async () => {
    const req = new Request('http://localhost/api/telemetry/latest');
    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 403);
  });

  test('Protected routes accept valid Dev Token and return data', async () => {
    // Insert initial telemetry row
    await mockEnv.DB.prepare('INSERT INTO telemetry').bind(
      'TRANSFORMER_01', 42.0, 28.0, 43.5, 0.04, 12.0, 2.5, 5.0, 0.5, 3.3, 0.2, 1, 0
    ).run();

    const req = new Request('http://localhost/api/telemetry/latest?device_id=TRANSFORMER_01', {
      headers: { 'Authorization': 'Bearer dev-admin-token' }
    });

    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.status, 'ok');
    assert.equal(body.data.t_core, 42.0);
  });

  test('POST /api/control/power queues remote Turn OFF command', async () => {
    const req = new Request('http://localhost/api/control/power', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer dev-admin-token',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ state: 'OFF', device_id: 'TRANSFORMER_01' })
    });

    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.command, 'POWER_OFF');
    assert.equal(body.status, 'queued');

    // Now test that the next ESP32 telemetry POST receives this pending command
    const espReq = new Request('http://localhost/api/telemetry', {
      method: 'POST',
      headers: { 'X-Device-Key': 'test-device-secret-key', 'Content-Type': 'application/json' },
      body: JSON.stringify({ device_id: 'TRANSFORMER_01', t_core: 38.0, t_inlet: 28.0, pson_active: 1 })
    });

    const espRes = await worker.fetch(espReq, mockEnv, mockCtx);
    assert.equal(espRes.status, 200);
    const espBody = await espRes.json();
    assert.equal(espBody.pending_command, 'POWER_OFF');
  });

  test('POST /api/control/power queues remote Turn ON command', async () => {
    const req = new Request('http://localhost/api/control/power', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer dev-admin-token',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ state: 'ON', device_id: 'TRANSFORMER_01' })
    });

    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.command, 'POWER_ON');
    assert.equal(body.status, 'queued');
  });

  test('POST /api/control/emergency-stop triggers emergency power cutoff', async () => {
    const req = new Request('http://localhost/api/control/emergency-stop', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer dev-admin-token',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ device_id: 'TRANSFORMER_01' })
    });

    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 200);
    const body = await res.json();
    assert.equal(body.status, 'emergency_cutoff_queued');
    assert.equal(body.command, 'POWER_OFF');
  });

  test('GET and POST /api/settings manages multi-event notifications and thresholds', async () => {
    // 1. Initial GET
    const getReq = new Request('http://localhost/api/settings', {
      method: 'GET',
      headers: { 'Authorization': 'Bearer dev-admin-token' }
    });
    const getRes = await worker.fetch(getReq, mockEnv, mockCtx);
    assert.equal(getRes.status, 200);
    const getJson = await getRes.json();
    assert.equal(getJson.status, 'ok');
    assert.equal(typeof getJson.settings.notify_overtemp_email, 'boolean');
    assert.equal(typeof getJson.settings.notify_emergency_email, 'boolean');
    assert.equal(typeof getJson.settings.notify_power_off_email, 'boolean');
    assert.equal(typeof getJson.settings.watchdog_email_enabled, 'boolean');

    // 2. POST updates
    const postReq = new Request('http://localhost/api/settings', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer dev-admin-token',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        notify_overtemp_email: false,
        notify_emergency_email: true,
        notify_power_off_email: false,
        watchdog_email_enabled: true,
        core_trip_limit: 68.5
      })
    });
    const postRes = await worker.fetch(postReq, mockEnv, mockCtx);
    assert.equal(postRes.status, 200);
    const postJson = await postRes.json();
    assert.equal(postJson.status, 'settings_updated');

    // 3. Verify updated settings
    const verifyRes = await worker.fetch(getReq, mockEnv, mockCtx);
    const verifyJson = await verifyRes.json();
    assert.equal(verifyJson.settings.notify_overtemp_email, false);
    assert.equal(verifyJson.settings.notify_emergency_email, true);
    assert.equal(verifyJson.settings.notify_power_off_email, false);
    assert.equal(verifyJson.settings.watchdog_email_enabled, true);
    assert.equal(verifyJson.settings.core_trip_limit, 68.5);
  });
});
