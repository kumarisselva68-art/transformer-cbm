/**
 * Brevo Transactional Email Service Integration
 * High-precision, minimalist transactional incident dispatch
 * Designed in Apple/Linear-inspired dark industrial aesthetic
 */

export async function sendBrevoAlert(env, { subject, title, incidentType, details, metrics = {} }) {
  const apiKey = env.BREVO_API_KEY;
  const rawRecipients = env.ALERT_RECIPIENT_EMAIL || env.ALLOWED_EMAILS || 'kumarisselva68@gmail.com,yogarathinam26@gmail.com';
  const senderEmail = env.BREVO_SENDER_EMAIL || 'alerts@transformer-cbm.internal';

  if (!apiKey || apiKey === 'YOUR_BREVO_API_KEY') {
    console.warn('[BREVO_EMAIL_SKIPPED] Brevo API Key not configured in environment secrets.');
    return { success: false, reason: 'API_KEY_NOT_CONFIGURED' };
  }

  // Parse comma-separated recipient addresses
  const recipients = rawRecipients
    .split(',')
    .map(e => e.trim())
    .filter(e => e.length > 0 && e.includes('@'))
    .map(email => ({ email }));

  if (recipients.length === 0) {
    recipients.push({ email: 'kumarisselva68@gmail.com' });
  }

  const timestampIso = new Date().toUTCString();
  const deviceId = metrics.deviceId || 'TMS-ESP32 Rev 3.0';
  const coreTemp = metrics.t_core != null ? `${Number(metrics.t_core).toFixed(1)} °C` : 'N/A';
  const inletTemp = metrics.t_inlet != null ? `${Number(metrics.t_inlet).toFixed(1)} °C` : 'N/A';
  const predTemp = metrics.t_predicted != null ? `${Number(metrics.t_predicted).toFixed(1)} °C` : 'N/A';
  const psonState = metrics.pson_active ? 'ENERGIZED [ACTIVE]' : 'DE-ENERGIZED [SAFE SHUTDOWN]';
  const dashboardUrl = 'https://transformer-cbm.kumarisselva68.workers.dev';

  const htmlContent = `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Transformer CBM Alert</title>
      <style>
        body {
          margin: 0;
          padding: 32px 16px;
          background-color: #000000;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
          color: #f4f4f5;
          -webkit-font-smoothing: antialiased;
        }
        .wrapper {
          max-width: 580px;
          margin: 0 auto;
          background-color: #09090b;
          border: 1px solid #27272a;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 12px 32px rgba(0, 0, 0, 0.8);
        }
        .amber-bar {
          height: 4px;
          background: linear-gradient(90deg, #f59e0b 0%, #fbbf24 100%);
          width: 100%;
        }
        .header {
          padding: 24px 28px 16px 28px;
          border-bottom: 1px solid #18181b;
        }
        .brand-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 12px;
        }
        .brand-title {
          font-size: 13px;
          font-weight: 800;
          letter-spacing: 0.8px;
          text-transform: uppercase;
          color: #f59e0b;
        }
        .badge {
          display: inline-block;
          font-size: 11px;
          font-weight: 700;
          letter-spacing: 0.5px;
          text-transform: uppercase;
          padding: 3px 8px;
          border-radius: 6px;
          background-color: rgba(245, 158, 11, 0.15);
          color: #fbbf24;
          border: 1px solid rgba(245, 158, 11, 0.3);
        }
        .title {
          font-size: 18px;
          font-weight: 700;
          color: #ffffff;
          margin: 0;
          line-height: 1.35;
        }
        .content {
          padding: 24px 28px;
        }
        .description {
          font-size: 14px;
          color: #a1a1aa;
          line-height: 1.6;
          margin-top: 0;
          margin-bottom: 20px;
        }
        .table-wrap {
          border: 1px solid #27272a;
          border-radius: 10px;
          overflow: hidden;
          margin-bottom: 24px;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          font-size: 13px;
        }
        tr:not(:last-child) td {
          border-bottom: 1px solid #18181b;
        }
        td {
          padding: 10px 14px;
        }
        td.label {
          color: #71717a;
          font-weight: 600;
          width: 42%;
        }
        td.val {
          color: #f4f4f5;
          font-weight: 600;
          font-family: 'JetBrains Mono', Consolas, Menlo, monospace;
          text-align: right;
        }
        .action-row {
          text-align: center;
          margin: 28px 0 12px 0;
        }
        .btn {
          display: inline-block;
          background-color: #f59e0b;
          color: #000000 !important;
          font-weight: 700;
          font-size: 13px;
          letter-spacing: 0.2px;
          padding: 11px 24px;
          border-radius: 8px;
          text-decoration: none;
          box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }
        .footer {
          padding: 20px 28px;
          background-color: #040405;
          border-top: 1px solid #18181b;
          text-align: center;
          font-size: 11px;
          color: #52525b;
          line-height: 1.5;
        }
      </style>
    </head>
    <body>
      <div class="wrapper">
        <div class="amber-bar"></div>
        <div class="header">
          <div class="brand-row">
            <span class="brand-title">Transformer Condition Monitoring</span>
            <span class="badge">${incidentType}</span>
          </div>
          <h1 class="title">${title}</h1>
        </div>
        <div class="content">
          <p class="description">${details}</p>

          <div class="table-wrap">
            <table>
              <tr><td class="label">Hardware Unit</td><td class="val">${deviceId}</td></tr>
              <tr><td class="label">Core Temp (T1)</td><td class="val">${coreTemp}</td></tr>
              <tr><td class="label">Inlet Temp (T2)</td><td class="val">${inletTemp}</td></tr>
              <tr><td class="label">Projected Temp (+30s)</td><td class="val">${predTemp}</td></tr>
              <tr><td class="label">Transformer Rails</td><td class="val">${psonState}</td></tr>
              <tr><td class="label">Event Timestamp</td><td class="val">${timestampIso}</td></tr>
            </table>
          </div>

          <div class="action-row">
            <a href="${dashboardUrl}" class="btn" target="_blank">Open Supervisory Console</a>
          </div>
        </div>
        <div class="footer">
          Autonomous Supervisory Watchdog • Rajalakshmi Institute of Technology (ECE)<br>
          Automated Transactional Dispatch via Brevo &amp; Cloudflare Edge
        </div>
      </div>
    </body>
    </html>
  `;

  // Clean subject line without alarmist spam flags
  const formattedSubject = subject.startsWith('[ALERT]') ? subject.replace('[ALERT]', '').trim() : subject;
  const cleanSubject = `Transformer CBM Notice: ${formattedSubject}`;

  try {
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'api-key': apiKey,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        sender: { name: 'Transformer CBM Monitor', email: senderEmail },
        to: recipients,
        subject: cleanSubject,
        htmlContent
      })
    });

    if (!res.ok) {
      const err = await res.text();
      console.error('[BREVO_API_ERROR]', err);
      return { success: false, error: err };
    }

    const data = await res.json();
    return { success: true, messageId: data.messageId };
  } catch (err) {
    console.error('[BREVO_FETCH_ERROR]', err);
    return { success: false, error: err.message };
  }
}
