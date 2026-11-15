/**
 * Transformer Condition Monitoring & Predictive Thermal Management
 * Cloudflare Edge Worker Architecture (API, Authentication, Cron Watchdog)
 */

import { verifyGoogleTokenAndAuthorize } from './auth.js';
import { DB } from './db.js';
import { sendBrevoAlert } from './email.js';

// Response Helpers
function jsonResponse(data, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Device-Key',
      ...extraHeaders
    }
  });
}

function corsOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Device-Key'
    }
  });
}

export default {
  /**
   * Main HTTP Request Router
   */
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return corsOptions();
    }

    try {
      // ----------------------------------------------------
      // 1. PUBLIC HEALTH CHECK
      // ----------------------------------------------------
      if (path === '/api/health') {
        return jsonResponse({
          status: 'healthy',
          service: 'Transformer CBM Edge API',
          timestamp: new Date().toISOString(),
          environment: env.ENVIRONMENT || 'development'
        });
      }

      // ----------------------------------------------------
      // 2. HARDWARE INGESTION ENDPOINT (ESP32 -> CLOUDFLARE)
      // ----------------------------------------------------
      if (path === '/api/telemetry' && request.method === 'POST') {
        const deviceKey = request.headers.get('X-Device-Key') || request.headers.get('x-device-key');
        const expectedKey = env.DEVICE_KEY || 'cbm_esp32_sec_key_2026';

        if (!deviceKey || deviceKey !== expectedKey) {
          return jsonResponse({ error: 'Unauthorized: Invalid X-Device-Key' }, 401);
        }

        const payload = await request.json();
        
        // Save telemetry frame to D1
        await DB.insertTelemetry(env.DB, payload);

        // Check for critical thermal fault
        const isCoreTrip = (payload.t_core >= 65.0);
        const isPredictiveTrip = (payload.t_predicted >= 70.0);
        const hasFault = (payload.fault_code && payload.fault_code > 0) || isCoreTrip || isPredictiveTrip;

        if (hasFault) {
          const faultReason = isCoreTrip 
            ? `Critical Core Temperature Trip (${payload.t_core.toFixed(1)} °C ≥ 65.0 °C)`
            : isPredictiveTrip 
              ? `Predictive Thermal Extrapolation Trip (${payload.t_predicted.toFixed(1)} °C ≥ 70.0 °C)`
              : `System Supervisory Trip (Code ${payload.fault_code})`;

          // Check if an alert was already dispatched recently to prevent email spam (15-minute cooldown)
          const recentAlert = await env.DB.prepare(`
            SELECT id, created_at FROM incident_alerts 
            WHERE device_id = ? AND incident_type = 'CRITICAL_THERMAL_TRIP' AND email_dispatched = 1
            ORDER BY id DESC LIMIT 1
          `).bind(payload.device_id || 'TRANSFORMER_01').first();

          const shouldSendEmail = !recentAlert || 
            (Date.now() - new Date(recentAlert.created_at).getTime() > 15 * 60 * 1000);

          // Check dynamic setting for overtemperature notification
          const overtempSetting = await DB.getSetting(env.DB, 'notify_overtemp_email', '1');
          const dispatchEmail = (overtempSetting === '1') && shouldSendEmail;

          // Record alert in database
          ctx.waitUntil(DB.recordAlert(
            env.DB, 
            payload.device_id || 'TRANSFORMER_01', 
            'CRITICAL_THERMAL_TRIP', 
            faultReason, 
            payload.t_core, 
            dispatchEmail ? 1 : 0
          ));

          // Trigger Brevo email alert asynchronously with deduplication
          if (dispatchEmail) {
            ctx.waitUntil(sendBrevoAlert(env, {
              subject: `CRITICAL TRIP: Transformer Core at ${payload.t_core.toFixed(1)} °C`,
              title: 'Automatic Supervisory Protection Trip Activated',
              incidentType: 'THERMAL_OVERTEMP_FAULT',
              details: `The supervisory safety algorithm tripped the main power rail (PS_ON# CUT). Reason: ${faultReason}`,
              metrics: payload
            }));
          }
        }

        // Check and pop pending remote commands (e.g. POWER_ON or POWER_OFF)
        const pendingCommand = await DB.fetchAndPopPendingCommand(env.DB, payload.device_id || 'TRANSFORMER_01');

        return jsonResponse({
          status: 'acknowledged',
          server_time: Date.now(),
          pending_command: pendingCommand ? pendingCommand.command_type : 'NONE',
          command_payload: pendingCommand ? JSON.parse(pendingCommand.payload || '{}') : {}
        });
      }

      // ----------------------------------------------------
      // AUTHENTICATION GUARD FOR PROTECTED DASHBOARD ROUTES
      // ----------------------------------------------------
      if (path.startsWith('/api/')) {
        const authHeader = request.headers.get('Authorization') || '';
        const token = authHeader.replace(/^Bearer\s+/i, '').trim();

        const authResult = await verifyGoogleTokenAndAuthorize(token, env, env.DB);
        if (!authResult.authorized) {
          return jsonResponse({ error: authResult.error || 'Unauthorized Google Account' }, 403);
        }

        const user = authResult.user;

        // Route: Verify Current User Session
        if (path === '/api/auth/verify') {
          return jsonResponse({ status: 'authenticated', user });
        }

        // Route: Get Latest Telemetry
        if (path === '/api/telemetry/latest' && request.method === 'GET') {
          const deviceId = url.searchParams.get('device_id') || 'TRANSFORMER_01';
          const latest = await DB.getLatestTelemetry(env.DB, deviceId);
          return jsonResponse({ status: 'ok', data: latest || null });
        }

        // Route: Get Telemetry History for Charts
        if (path === '/api/telemetry/history' && request.method === 'GET') {
          const deviceId = url.searchParams.get('device_id') || 'TRANSFORMER_01';
          const limit = Math.min(parseInt(url.searchParams.get('limit') || '60', 10), 300);
          const history = await DB.getHistory(env.DB, deviceId, limit);
          return jsonResponse({ status: 'ok', data: history });
        }

        // Route: Remote Power Control (Turn ON / Turn OFF)
        if (path === '/api/control/power' && request.method === 'POST') {
          if (user.role !== 'ADMIN' && user.role !== 'OPERATOR') {
            return jsonResponse({ error: 'Permission denied: Operator or Admin role required' }, 403);
          }

          const body = await request.json();
          const targetState = (body.state || '').toUpperCase(); // 'ON' or 'OFF'
          const deviceId = body.device_id || 'TRANSFORMER_01';

          if (targetState !== 'ON' && targetState !== 'OFF') {
            return jsonResponse({ error: "Invalid state. Must be 'ON' or 'OFF'" }, 400);
          }

          const commandType = (targetState === 'ON') ? 'POWER_ON' : 'POWER_OFF';
          await DB.queueCommand(env.DB, deviceId, commandType, { requested_by: user.email }, user.email);

          // Audit record
          ctx.waitUntil(DB.recordAlert(
            env.DB,
            deviceId,
            `REMOTE_${commandType}`,
            `Remote ${commandType} command queued by user ${user.email} (${user.role})`
          ));

          // If turning OFF, dispatch Brevo notification if enabled
          if (targetState === 'OFF') {
            const notifyPowerOff = await DB.getSetting(env.DB, 'notify_power_off_email', '1');
            if (notifyPowerOff === '1') {
              const latest = await DB.getLatestTelemetry(env.DB, deviceId);
              ctx.waitUntil(sendBrevoAlert(env, {
                subject: 'TRANSFORMER DE-ENERGIZED: Remote Turn OFF Executed',
                title: 'Main Output Disconnected Remotely',
                incidentType: 'REMOTE_POWER_OFF',
                details: `The main transformer power output rails were de-energized via remote supervisory command by ${user.email} (${user.role}).<br><br><strong>SAFETY NOTICE:</strong> Do not touch the transformer core or internal power circuitry immediately. Cores retain residual heat and secondary filter capacitors hold stored energy charges for several minutes after de-energizing.`,
                metrics: {
                  deviceId,
                  t_core: latest ? latest.t_core : null,
                  t_inlet: latest ? latest.t_inlet : null,
                  t_predicted: latest ? latest.t_predicted : null,
                  pson_active: 0
                }
              }));
            }
          }

          return jsonResponse({
            status: 'queued',
            command: commandType,
            device_id: deviceId,
            issued_by: user.email,
            timestamp: new Date().toISOString()
          });
        }

        // Route: Fan Speed Modulation Control (Auto vs Manual PWM)
        if (path === '/api/control/fan' && request.method === 'POST') {
          if (user.role !== 'ADMIN' && user.role !== 'OPERATOR') {
            return jsonResponse({ error: 'Permission denied: Operator or Admin role required' }, 403);
          }

          const body = await request.json();
          const mode = (body.mode || 'AUTO').toUpperCase(); // 'AUTO' or 'MANUAL'
          const speed = Math.max(0, Math.min(100, parseInt(body.speed ?? 50, 10)));
          const deviceId = body.device_id || 'TRANSFORMER_01';

          await DB.queueCommand(env.DB, deviceId, 'SET_FAN', { mode, speed }, user.email);

          ctx.waitUntil(DB.recordAlert(
            env.DB,
            deviceId,
            'FAN_MODULATION_UPDATE',
            `Fan set to ${mode} mode (${speed}%) by ${user.email}`
          ));

          return jsonResponse({
            status: 'queued',
            command: 'SET_FAN',
            mode,
            speed,
            device_id: deviceId,
            issued_by: user.email
          });
        }

        // Route: Emergency Cutoff (Instant Trip)
        if (path === '/api/control/emergency-stop' && request.method === 'POST') {
          if (user.role !== 'ADMIN' && user.role !== 'OPERATOR') {
            return jsonResponse({ error: 'Permission denied: Operator or Admin role required' }, 403);
          }

          const body = await request.json().catch(() => ({}));
          const deviceId = body.device_id || 'TRANSFORMER_01';

          await DB.queueCommand(env.DB, deviceId, 'POWER_OFF', { emergency: true }, user.email);

          ctx.waitUntil(DB.recordAlert(
            env.DB,
            deviceId,
            'EMERGENCY_STOP_TRIP',
            `EMERGENCY MANUAL CUTOFF ACTIVATED by ${user.email} (${user.role})`
          ));

          // Check if emergency notification is enabled
          const notifyEmergency = await DB.getSetting(env.DB, 'notify_emergency_email', '1');
          if (notifyEmergency === '1') {
            const latest = await DB.getLatestTelemetry(env.DB, deviceId);
            ctx.waitUntil(sendBrevoAlert(env, {
              subject: 'CRITICAL EMERGENCY CUTOFF: Immediate Power Rails Cut',
              title: 'Manual Emergency Override Executed',
              incidentType: 'EMERGENCY_MANUAL_CUTOFF',
              details: `An immediate emergency shutdown of all transformer output rails was manually triggered by ${user.email} (${user.role}). Hardware PS_ON# has been severed immediately.<br><br><strong>SAFETY NOTICE:</strong> Do not touch transformer internal components or windings. Allow adequate cooldown and discharge period before physical hardware inspection.`,
              metrics: {
                deviceId,
                t_core: latest ? latest.t_core : null,
                t_inlet: latest ? latest.t_inlet : null,
                t_predicted: latest ? latest.t_predicted : null,
                pson_active: 0
              }
            }));
          }

          return jsonResponse({
            status: 'emergency_cutoff_queued',
            command: 'POWER_OFF',
            device_id: deviceId,
            issued_by: user.email,
            timestamp: new Date().toISOString()
          });
        }

        // Route: Reset Fault Latch
        if (path === '/api/control/reset' && request.method === 'POST') {
          if (user.role !== 'ADMIN') {
            return jsonResponse({ error: 'Permission denied: Administrator role required to reset fault latches' }, 403);
          }

          const body = await request.json().catch(() => ({}));
          const deviceId = body.device_id || 'TRANSFORMER_01';

          await DB.queueCommand(env.DB, deviceId, 'RESET_FAULT', {}, user.email);

          ctx.waitUntil(DB.recordAlert(
            env.DB,
            deviceId,
            'SUPERVISORY_FAULT_RESET',
            `Fault lockout reset dispatched by Administrator ${user.email}`
          ));

          return jsonResponse({
            status: 'queued',
            command: 'RESET_FAULT',
            device_id: deviceId,
            issued_by: user.email
          });
        }

        // Route: Get Incident Alerts Log
        if (path === '/api/alerts' && request.method === 'GET') {
          const deviceId = url.searchParams.get('device_id') || 'TRANSFORMER_01';
          const alerts = await DB.getRecentAlerts(env.DB, deviceId, 50);
          return jsonResponse({ status: 'ok', data: alerts });
        }

        // Route: List Authorized Users (Admin Only)
        if (path === '/api/users' && request.method === 'GET') {
          if (user.role !== 'ADMIN') {
            return jsonResponse({ error: 'Admin permission required' }, 403);
          }
          const users = await DB.listUsers(env.DB);
          return jsonResponse({ status: 'ok', data: users });
        }

        // Route: Whitelist User (Admin Only)
        if (path === '/api/users' && request.method === 'POST') {
          if (user.role !== 'ADMIN') {
            return jsonResponse({ error: 'Admin permission required' }, 403);
          }
          const body = await request.json();
          if (!body.email) {
            return jsonResponse({ error: 'Email is required' }, 400);
          }
          await DB.addUser(env.DB, body.email, body.name || body.email, body.role || 'VIEWER');
          return jsonResponse({ status: 'user_added', email: body.email });
        }

        // Route: Remove User (Admin Only)
        if (path === '/api/users' && request.method === 'DELETE') {
          if (user.role !== 'ADMIN') {
            return jsonResponse({ error: 'Admin permission required' }, 403);
          }
          const body = await request.json();
          if (!body.email) {
            return jsonResponse({ error: 'Email is required' }, 400);
          }
          await DB.removeUser(env.DB, body.email);
          return jsonResponse({ status: 'user_removed', email: body.email });
        }

        // Route: Get Dynamic System Settings
        if (path === '/api/settings' && request.method === 'GET') {
          const watchdogVal = await DB.getSetting(env.DB, 'watchdog_email_enabled', '0');
          const overtempVal = await DB.getSetting(env.DB, 'notify_overtemp_email', '1');
          const emergencyVal = await DB.getSetting(env.DB, 'notify_emergency_email', '1');
          const powerOffVal = await DB.getSetting(env.DB, 'notify_power_off_email', '1');
          const coreTripVal = await DB.getSetting(env.DB, 'core_trip_limit', '65.0');
          const predTripVal = await DB.getSetting(env.DB, 'pred_trip_limit', '70.0');
          const horizonVal = await DB.getSetting(env.DB, 'horizon_sec', '30');

          return jsonResponse({
            status: 'ok',
            settings: {
              watchdog_email_enabled: watchdogVal === '1',
              notify_overtemp_email: overtempVal === '1',
              notify_emergency_email: emergencyVal === '1',
              notify_power_off_email: powerOffVal === '1',
              core_trip_limit: parseFloat(coreTripVal) || 65.0,
              pred_trip_limit: parseFloat(predTripVal) || 70.0,
              horizon_sec: parseInt(horizonVal, 10) || 30
            }
          });
        }

        // Route: Update Dynamic System Settings (Admin Only)
        if (path === '/api/settings' && request.method === 'POST') {
          if (user.role !== 'ADMIN') {
            return jsonResponse({ error: 'Admin permission required' }, 403);
          }
          const body = await request.json();

          if (typeof body.watchdog_email_enabled !== 'undefined') {
            await DB.setSetting(env.DB, 'watchdog_email_enabled', body.watchdog_email_enabled ? '1' : '0');
          }
          if (typeof body.notify_overtemp_email !== 'undefined') {
            await DB.setSetting(env.DB, 'notify_overtemp_email', body.notify_overtemp_email ? '1' : '0');
          }
          if (typeof body.notify_emergency_email !== 'undefined') {
            await DB.setSetting(env.DB, 'notify_emergency_email', body.notify_emergency_email ? '1' : '0');
          }
          if (typeof body.notify_power_off_email !== 'undefined') {
            await DB.setSetting(env.DB, 'notify_power_off_email', body.notify_power_off_email ? '1' : '0');
          }
          if (typeof body.core_trip_limit !== 'undefined') {
            await DB.setSetting(env.DB, 'core_trip_limit', String(body.core_trip_limit));
          }
          if (typeof body.pred_trip_limit !== 'undefined') {
            await DB.setSetting(env.DB, 'pred_trip_limit', String(body.pred_trip_limit));
          }
          if (typeof body.horizon_sec !== 'undefined') {
            await DB.setSetting(env.DB, 'horizon_sec', String(body.horizon_sec));
          }

          ctx.waitUntil(DB.recordAlert(
            env.DB,
            'TRANSFORMER_01',
            'SETTINGS_UPDATED',
            `System notification and safety threshold settings updated by ${user.email}`
          ));

          return jsonResponse({ status: 'settings_updated' });
        }

        return jsonResponse({ error: 'API route not found' }, 404);
      }

      // ----------------------------------------------------
      // 3. STATIC DASHBOARD ASSETS (Cloudflare Pages/Worker Assets)
      // ----------------------------------------------------
      if (env.ASSETS) {
        return await env.ASSETS.fetch(request);
      }

      return new Response('Transformer CBM API Active. Static frontend binding not loaded.', { status: 200 });
    } catch (err) {
      console.error('[UNCAUGHT_WORKER_ERROR]', err);
      return jsonResponse({ error: 'Internal Server Error', details: err.message }, 500);
    }
  },

  /**
   * Autonomous Cron Trigger (Fires every 60 seconds)
   * Audits ESP32 Heartbeat and Dispatches Communication Loss Alert
   */
  async scheduled(event, env, ctx) {
    console.log('[CRON_AUDIT] Auditing ESP32 Heartbeat at', new Date().toISOString());

    try {
      // Dynamic database-backed setting (defaults to false until explicitly armed in dashboard)
      const settingVal = await DB.getSetting(env.DB, 'watchdog_email_enabled', '0');
      if (settingVal !== '1') {
        console.log('[CRON_AUDIT] Watchdog email alerts currently paused in dashboard settings.');
        return;
      }

      const latest = await DB.getLatestTelemetry(env.DB, 'TRANSFORMER_01');
      if (!latest || !latest.created_at) {
        console.warn('[CRON_AUDIT] No telemetry records found in database.');
        return;
      }

      // Check time elapsed since last ESP32 ping
      const lastPingTime = new Date(latest.created_at).getTime();
      const elapsedSeconds = Math.floor((Date.now() - lastPingTime) / 1000);

      // If silent > 120 seconds, declare COMMUNICATION_LOSS
      if (elapsedSeconds > 120) {
        // Anti-Spam Deduplication: Check if an email was already sent in the last 6 hours
        const lastCommAlert = await env.DB.prepare(`
          SELECT id, created_at, email_dispatched FROM incident_alerts
          WHERE device_id = ? AND incident_type = 'COMMUNICATION_LOSS' AND email_dispatched = 1
          ORDER BY id DESC LIMIT 1
        `).bind('TRANSFORMER_01').first();

        const cooldownMs = 6 * 60 * 60 * 1000; // 6-hour alert cooldown
        const alreadyNotifiedRecently = lastCommAlert && 
          (Date.now() - new Date(lastCommAlert.created_at).getTime() < cooldownMs);

        if (alreadyNotifiedRecently) {
          const minutesAgo = Math.round((Date.now() - new Date(lastCommAlert.created_at).getTime()) / 60000);
          console.log(`[CRON_AUDIT] Communication loss email suppressed. Already notified ${minutesAgo} mins ago.`);
          return;
        }

        console.error(`[COMMUNICATION_LOSS] ESP32 silent for ${elapsedSeconds}s! Dispatching 1 notification...`);

        // Record incident in database with email_dispatched = 1
        await DB.recordAlert(
          env.DB,
          'TRANSFORMER_01',
          'COMMUNICATION_LOSS',
          `ESP32 telemetry stream silent for ${elapsedSeconds} seconds (> 120s threshold). Possible Wi-Fi drop or SMPS power loss.`,
          null,
          1
        );

        // Dispatch single email notification
        await sendBrevoAlert(env, {
          subject: `COMMUNICATION LOSS: ESP32 Hardware Unreachable (${elapsedSeconds}s silent)`,
          title: 'Remote Hardware Heartbeat Timeout',
          incidentType: 'COMMUNICATION_LOSS',
          details: `The supervisory watchdog detected that the ESP32 controller has stopped transmitting telemetry for ${elapsedSeconds} seconds. Check local facility power and Wi-Fi gateway. Next notification will be suppressed for 6 hours.`,
          metrics: {
            deviceId: 'TRANSFORMER_01',
            t_core: latest.t_core,
            t_inlet: latest.t_inlet,
            t_predicted: latest.t_predicted,
            pson_active: latest.pson_active
          }
        });
      } else {
        console.log(`[CRON_AUDIT] ESP32 healthy. Last ping was ${elapsedSeconds}s ago.`);
      }
    } catch (err) {
      console.error('[CRON_AUDIT_ERROR]', err);
    }
  }
};
