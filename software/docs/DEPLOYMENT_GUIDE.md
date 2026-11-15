# Production Deployment Guide: Transformer CBM Cloud Ecosystem

This guide provides a turnkey walkthrough to deploy your Cloudflare Worker, D1 Database, and Real-Time Dashboard to production.

---

## Step 1: Cloudflare Account Preparation

1. **Sign up or log in** at [dash.cloudflare.com](https://dash.cloudflare.com/). (Free account).
2. **Find your Account ID:**
   * In the Cloudflare dashboard, click on **Workers & Pages** in the left sidebar.
   * Look on the right-hand panel under **Account ID** and copy your 32-character ID.
3. **Generate an API Token:**
   * Go to **My Profile** (top-right avatar) $\rightarrow$ **API Tokens** $\rightarrow$ **Create Token**.
   * Choose the **"Edit Cloudflare Workers"** template, or create a Custom Token with:
     * `Account` | `Workers Scripts` | `Edit`
     * `Account` | `D1` | `Edit`
     * `Account` | `Pages` | `Edit`
   * Click **Continue to summary** $\rightarrow$ **Create Token**, and copy the token.
4. **Authenticate Wrangler CLI locally:**
   ```bash
   npx wrangler login
   ```
   *(Or set `export CLOUDFLARE_API_TOKEN="your_token"` / PowerShell `$env:CLOUDFLARE_API_TOKEN="your_token"`).*

---

## Step 2: Create Cloudflare D1 Database

In your `software` directory:

1. **Create the D1 database instance:**
   ```bash
   npx wrangler d1 create transformer-cbm-db
   ```
   *Wrangler will print output like:*
   ```toml
   [[d1_databases]]
   binding = "DB"
   database_name = "transformer-cbm-db"
   database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
   ```
2. **Update `wrangler.toml`:**
   Copy the `database_id` value from the output and paste it into `software/wrangler.toml` replacing `"transformer-cbm-db-id"`.

3. **Initialize the Database Schema:**
   ```bash
   npx wrangler d1 execute transformer-cbm-db --remote --file=./schema.sql
   ```
   This creates the `telemetry`, `commands`, `incident_alerts`, and `authorized_users` tables.

---

## Step 3: Configure Google OAuth 2.0 Web Client ID

To allow Google Sign-In on your dashboard:

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project (e.g., `Transformer-CBM-Portal`).
3. Navigate to **APIs & Services** $\rightarrow$ **OAuth consent screen**:
   * User Type: **External** $\rightarrow$ Create.
   * Fill in App Name: `Transformer CBM Portal` and your email.
   * Click Save and Continue through Scopes and Test Users.
4. Navigate to **Credentials** $\rightarrow$ **Create Credentials** $\rightarrow$ **OAuth client ID**:
   * Application type: **Web application**.
   * Name: `Transformer CBM Dashboard`.
   * **Authorized JavaScript origins:**
     * `http://localhost:8787` (for local development)
     * `https://transformer-cbm-backend.<your-subdomain>.workers.dev` (your production URL)
5. Copy your **Client ID** (looks like `xxxxxxxxxxxx-xxxxxxxxxxxxxxxx.apps.googleusercontent.com`).
6. Paste your Client ID into:
   * `software/wrangler.toml` (`GOOGLE_CLIENT_ID = "..."`)
   * `software/public/app.js` (`const clientId = '...'`)

---

## Step 4: Configure Email Alerts (Brevo)

*(Optional, recommended for live email alerts on trips)*

1. Sign up for a free account at [brevo.com](https://www.brevo.com/) (300 free emails/day).
2. Go to **SMTP & API** $\rightarrow$ **API Keys** $\rightarrow$ **Generate a new API key**.
3. Set the key securely as a Cloudflare Worker secret:
   ```bash
   npx wrangler secret put BREVO_API_KEY
   ```
   *Paste your Brevo API key when prompted.*
4. Set recipient email in `wrangler.toml`:
   ```toml
   ALERT_RECIPIENT_EMAIL = "your-email@gmail.com"
   ```

---

## Step 5: Deploy to Production

Deploy the Worker and the frontend dashboard assets:

```bash
npx wrangler deploy
```

Wrangler will output your live URL:
`https://transformer-cbm-backend.<your-subdomain>.workers.dev`

Open this URL in any browser. You will see the Google Sign-In prompt. Once signed in with an authorized email, the real-time telemetry dashboard will activate!
