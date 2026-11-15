/**
 * Cloudflare D1 Database Access Layer
 * Condition Monitoring Telemetry, Commands, and User Administration
 */

export const DB = {
  /**
   * Insert new telemetry snapshot from ESP32
   */
  async insertTelemetry(db, data) {
    const query = `
      INSERT INTO telemetry (
        device_id, t_core, t_inlet, t_predicted, rate_of_rise,
        v_12v, i_12v, v_5v, i_5v, v_3v3, i_3v3,
        pson_active, fault_code
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `;
    return await db.prepare(query).bind(
      data.device_id || 'TRANSFORMER_01',
      data.t_core ?? 0.0,
      data.t_inlet ?? 0.0,
      data.t_predicted ?? 0.0,
      data.rate_of_rise ?? 0.0,
      data.v_12v ?? 0.0,
      data.i_12v ?? 0.0,
      data.v_5v ?? 0.0,
      data.i_5v ?? 0.0,
      data.v_3v3 ?? 0.0,
      data.i_3v3 ?? 0.0,
      data.pson_active ? 1 : 0,
      data.fault_code ?? 0
    ).run();
  },

  /**
   * Get latest state of a monitored transformer
   */
  async getLatestTelemetry(db, deviceId = 'TRANSFORMER_01') {
    return await db.prepare(`
      SELECT * FROM telemetry 
      WHERE device_id = ? 
      ORDER BY id DESC 
      LIMIT 1
    `).bind(deviceId).first();
  },

  /**
   * Get historical telemetry frames for live charts (default last 100 points)
   */
  async getHistory(db, deviceId = 'TRANSFORMER_01', limit = 100) {
    const results = await db.prepare(`
      SELECT * FROM (
        SELECT id, device_id, t_core, t_inlet, t_predicted, rate_of_rise,
               v_12v, i_12v, v_5v, i_5v, v_3v3, i_3v3, pson_active, fault_code, created_at
        FROM telemetry
        WHERE device_id = ?
        ORDER BY id DESC
        LIMIT ?
      ) ORDER BY id ASC
    `).bind(deviceId, limit).all();

    return results.results || [];
  },

  /**
   * Queue a remote command (POWER_ON, POWER_OFF, RESET_FAULT)
   */
  async queueCommand(db, deviceId, commandType, payload = {}, issuedBy = 'SYSTEM') {
    // Invalidate existing pending commands of the same type to avoid duplicates
    await db.prepare(`
      UPDATE commands 
      SET status = 'CANCELLED' 
      WHERE device_id = ? AND status = 'PENDING'
    `).bind(deviceId).run();

    return await db.prepare(`
      INSERT INTO commands (device_id, command_type, payload, status, issued_by)
      VALUES (?, ?, ?, 'PENDING', ?)
    `).bind(deviceId, commandType, JSON.stringify(payload), issuedBy).run();
  },

  /**
   * Atomically fetch and mark pending command as EXECUTED when ESP32 polls
   */
  async fetchAndPopPendingCommand(db, deviceId = 'TRANSFORMER_01') {
    const pending = await db.prepare(`
      SELECT * FROM commands 
      WHERE device_id = ? AND status = 'PENDING'
      ORDER BY id ASC 
      LIMIT 1
    `).bind(deviceId).first();

    if (pending) {
      await db.prepare(`
        UPDATE commands 
        SET status = 'EXECUTED', executed_at = CURRENT_TIMESTAMP 
        WHERE id = ?
      `).bind(pending.id).run();
      return pending;
    }

    return null;
  },

  /**
   * Record incident alert (over-temp, power loss, comm loss)
   */
  async recordAlert(db, deviceId, incidentType, details, tCore = null, emailSent = 0) {
    return await db.prepare(`
      INSERT INTO incident_alerts (device_id, incident_type, details, t_core, email_dispatched)
      VALUES (?, ?, ?, ?, ?)
    `).bind(deviceId, incidentType, details, tCore, emailSent ? 1 : 0).run();
  },

  /**
   * List recent incident alerts
   */
  async getRecentAlerts(db, deviceId = 'TRANSFORMER_01', limit = 20) {
    const results = await db.prepare(`
      SELECT * FROM incident_alerts 
      WHERE device_id = ? 
      ORDER BY id DESC 
      LIMIT ?
    `).bind(deviceId, limit).all();
    return results.results || [];
  },

  /**
   * User Whitelist Management
   */
  async listUsers(db) {
    const results = await db.prepare(`SELECT email, name, role, added_at FROM authorized_users ORDER BY added_at ASC`).all();
    return results.results || [];
  },

  async addUser(db, email, name, role = 'VIEWER') {
    return await db.prepare(`
      INSERT INTO authorized_users (email, name, role)
      VALUES (?, ?, ?)
      ON CONFLICT(email) DO UPDATE SET name = excluded.name, role = excluded.role
    `).bind(email.toLowerCase().trim(), name, role).run();
  },

  async removeUser(db, email) {
    return await db.prepare(`DELETE FROM authorized_users WHERE LOWER(email) = ?`).bind(email.toLowerCase().trim()).run();
  },

  /**
   * System Dynamic Settings (Watchdog Email Alerts, Thresholds)
   */
  async getSetting(db, key, defaultValue = null) {
    const row = await db.prepare(`SELECT value FROM system_settings WHERE key = ?`).bind(key).first();
    return row ? row.value : defaultValue;
  },

  async setSetting(db, key, value) {
    return await db.prepare(`
      INSERT INTO system_settings (key, value, updated_at)
      VALUES (?, ?, CURRENT_TIMESTAMP)
      ON CONFLICT(key) DO UPDATE SET value = excluded.value, updated_at = CURRENT_TIMESTAMP
    `).bind(key, String(value)).run();
  }
};
