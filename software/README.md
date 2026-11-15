# Transformer Condition-Based Monitoring (CBM) Cloud Ecosystem

Production-grade Cloudflare Edge Worker backend, Serverless SQLite (D1) database, Google OAuth 2.0 Identity Management, and High-Performance Real-Time Web Dashboard for the **Transformer CBM & Predictive Thermal Management System (TMS-ESP32 Rev 3.0)**.

---

## 🌟 Key Architecture Capabilities

1. **Zero-Maintenance Edge Runtime:** Runs globally across 300+ edge locations on Cloudflare Workers with < 30ms latency.
2. **Serverless Database (Cloudflare D1):** High-speed SQL storage handling 100,000 writes/day and 5M reads/day for $0 without requiring a credit card.
3. **Google OAuth 2.0 Security:** Pure Google Identity Services authentication with role-based access control (Admin, Operator, Viewer) and an email whitelist guard.
4. **Remote Master Power Control:** Bidirectional **Remote Turn ON** and **Remote Turn OFF** for the ATX SMPS (`PS_ON#`), reinforced by local hardware thermal interlocks.
5. **Real-Time Dual-Series Graphs:** Interactive Chart.js streaming core temperature ($T_{core}$), inlet temperature ($T_{inlet}$), and mathematical trend extrapolation ($T_{pred}$) every 3 seconds.
6. **Autonomous Cron Watchdog:** Independent 60-second heartbeat supervisor that declares `COMMUNICATION_LOSS` and triggers Brevo email alerts if the ESP32 hardware drops offline.

---

## 📂 Project Structure

```
software/
├── src/
│   ├── worker.js              # Cloudflare Worker API router & Cron watchdog
│   ├── auth.js                # Google OAuth 2.0 token verification & email whitelist
│   ├── db.js                  # D1 SQLite query layer (telemetry, commands, alerts)
│   └── email.js               # Brevo transactional email dispatcher
├── public/                    # High-Speed Real-Time Dashboard (SPA)
│   ├── index.html             # Industrial theme portal with Google Sign-In
│   ├── app.js                 # Chart.js live rendering & remote supervisory control
│   └── styles.css             # High-tech dark/slate industrial UI
├── tests/
│   ├── api.test.js            # Automated edge API unit test suite
│   └── mock_esp32_simulator.js# Interactive ESP32 hardware simulator
├── docs/
│   ├── API_SPECIFICATION.md   # Complete REST API reference
│   ├── DEPLOYMENT_GUIDE.md    # Turnkey production deployment guide
│   └── ESP32_INTEGRATION.md   # Hardware firmware integration manual
├── schema.sql                 # D1 database SQL migration schema
├── wrangler.toml              # Cloudflare configuration file
└── package.json               # Scripts and dependencies
```

---

## 🚀 Quickstart & Local Development

### 1. Prerequisites
* Node.js v18+ (Node v24 detected)
* npm v9+

### 2. Run Local Automated Tests
```bash
npm test
```
All 7 unit tests validate authentication, D1 queries, telemetry ingestion, and remote command piggybacking.

### 3. Start Local Edge Development Server
```bash
npm run dev
```
Starts the local Cloudflare Worker at `http://localhost:8787` serving both the REST API and the live web dashboard.

### 4. Run the ESP32 Hardware Simulator
In a separate terminal:
```bash
npm run simulate
```
This simulator generates continuous sensor data ($T_{core}, T_{inlet}, T_{pred}, V_{12V}, I_{12V}$), sends telemetry via HTTPS POST, and executes inbound remote `POWER_ON` / `POWER_OFF` commands in real time.

---

## 🌐 Production Deployment

Deploying to Cloudflare requires just 3 steps once you have your Cloudflare API token:

```bash
# 1. Create the D1 Database
npx wrangler d1 create transformer-cbm-db

# 2. Apply the SQL Schema
npx wrangler d1 execute transformer-cbm-db --remote --file=./schema.sql

# 3. Deploy Worker and Dashboard
npx wrangler deploy
```

See [`docs/DEPLOYMENT_GUIDE.md`](docs/DEPLOYMENT_GUIDE.md) for full walkthrough including Google OAuth and Brevo setup.
