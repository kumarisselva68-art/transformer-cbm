/**
 * Quick Brevo Email Delivery Test
 */
async function testBrevo() {
  const apiKey = process.env.BREVO_API_KEY || 'xkeysib-REDACTED-USE-ENV-SECRET';
  const recipient = 'kumarisselva68@gmail.com';

  const res = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: {
      'api-key': apiKey,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    body: JSON.stringify({
      sender: { name: 'Transformer CBM System', email: recipient },
      to: [{ email: recipient, name: 'Selva Kumari' }],
      subject: '[VERIFIED] Transformer CBM Supervisory Alert System Active',
      htmlContent: `
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; background: #000000; color: #ffffff; padding: 24px; border-radius: 12px; border: 1px solid #27272a;">
          <h2 style="color: #10b981; margin: 0 0 10px 0;">⚡ Transformer CBM Alert Engine Online</h2>
          <p style="color: #a1a1aa; line-height: 1.5;">
            Your Brevo Transactional Email Service and Cloudflare Worker Watchdog are fully configured and verified.
          </p>
          <div style="margin: 20px 0; padding: 14px; background: #111115; border-radius: 8px; border: 1px solid #1e1e24;">
            <p style="margin: 0; font-size: 14px; color: #38bdf8;"><strong>Status:</strong> Autonomous Edge Watchdog Armed</p>
            <p style="margin: 4px 0 0 0; font-size: 14px; color: #a1a1aa;"><strong>Alert Trigger:</strong> Automatic on T_core ≥ 65.0°C or Silence > 120s</p>
          </div>
          <p style="font-size: 13px; color: #71717a;">
            Live Dashboard: <a style="color: #3b82f6;" href="https://transformer-cbm.kumarisselva68.workers.dev">https://transformer-cbm.kumarisselva68.workers.dev</a>
          </p>
        </div>
      `
    })
  });

  const result = await res.json();
  console.log('BREVO DELIVERY RESPONSE:', result);
}

testBrevo();
