# REST API Specification: Transformer CBM Cloud Ecosystem

Base URL (Local): `http://localhost:8787`  
Base URL (Production): `https://transformer-cbm-backend.<your-subdomain>.workers.dev`

---

## 1. Public Endpoints

### `GET /api/health`
Returns system health, server timestamp, and active environment.

* **Headers:** None
* **Response (200 OK):**
```json
{
  "status": "healthy",
  "service": "Transformer CBM Edge API",
  "timestamp": "2026-11-12T12:00:00.000Z",
  "environment": "production"
}
```

---

## 2. Hardware Ingestion Endpoints (ESP32)

### `POST /api/telemetry`
Transmits sensor readings, rail voltages, and operating states from the ESP32. Returns any pending remote commands.

* **Headers:**
  * `X-Device-Key: <SECRET_KEY>` (Required)
  * `Content-Type: application/json`
* **Request Body:**
```json
{
  "device_id": "TRANSFORMER_01",
  "t_core": 38.5,
  "t_inlet": 27.2,
  "t_predicted": 40.1,
  "rate_of_rise": 0.05,
  "v_12v": 12.04,
  "i_12v": 2.85,
  "v_5v": 5.01,
  "i_5v": 0.85,
  "v_3v3": 3.31,
  "i_3v3": 0.42,
  "pson_active": 1,
  "fault_code": 0
}
```
* **Response (200 OK):**
```json
{
  "status": "acknowledged",
  "server_time": 1794484800000,
  "pending_command": "POWER_ON",
  "command_payload": {}
}
```
*(If no command is pending, `pending_command` returns `"NONE"`).*

* **Error Responses:**
  * `401 Unauthorized`: Invalid or missing `X-Device-Key`.

---

## 3. Protected Dashboard Endpoints (Google OAuth 2.0)

All protected endpoints require the Google ID Token passed in the `Authorization` header:
`Authorization: Bearer <GOOGLE_ID_TOKEN>`

### `GET /api/auth/verify`
Verifies the current Google credential, checks authorization against the database whitelist, and returns the user's role.

* **Response (200 OK):**
```json
{
  "status": "authenticated",
  "user": {
    "email": "engineer@gmail.com",
    "name": "Jane Doe",
    "role": "ADMIN",
    "picture": "https://lh3.googleusercontent.com/..."
  }
}
```
* **Error Response (403 Forbidden):**
```json
{
  "error": "Access denied. Email 'stranger@gmail.com' is not in the authorized personnel list."
}
```

---

### `GET /api/telemetry/latest?device_id=TRANSFORMER_01`
Retrieves the most recent telemetry frame recorded by the ESP32.

* **Response (200 OK):**
```json
{
  "status": "ok",
  "data": {
    "id": 1420,
    "device_id": "TRANSFORMER_01",
    "t_core": 38.5,
    "t_inlet": 27.2,
    "t_predicted": 40.1,
    "rate_of_rise": 0.05,
    "v_12v": 12.04,
    "i_12v": 2.85,
    "pson_active": 1,
    "fault_code": 0,
    "created_at": "2026-11-12 12:00:10"
  }
}
```

---

### `GET /api/telemetry/history?device_id=TRANSFORMER_01&limit=60`
Retrieves historical telemetry frames for rendering the live Chart.js graphs.

* **Parameters:** `limit` (Integer, default 60, max 300)
* **Response (200 OK):**
```json
{
  "status": "ok",
  "data": [
    { "id": 1400, "t_core": 37.1, "t_inlet": 27.0, "t_predicted": 37.5, "created_at": "..." },
    { "id": 1401, "t_core": 37.3, "t_inlet": 27.0, "t_predicted": 37.8, "created_at": "..." }
  ]
}
```

---

### `POST /api/control/power`
Queues a remote **Turn ON** or **Turn OFF** supervisory command for the ESP32.

* **Required Role:** `OPERATOR` or `ADMIN`
* **Request Body:**
```json
{
  "device_id": "TRANSFORMER_01",
  "state": "ON"
}
```
*(State can be `"ON"` or `"OFF"`).*

* **Response (200 OK):**
```json
{
  "status": "queued",
  "command": "POWER_ON",
  "device_id": "TRANSFORMER_01",
  "issued_by": "engineer@gmail.com",
  "timestamp": "2026-11-12T12:05:00.000Z"
}
```

---

### `GET /api/alerts?device_id=TRANSFORMER_01`
Fetches recent safety trips, communication losses, and supervisory actions.

* **Response (200 OK):**
```json
{
  "status": "ok",
  "data": [
    {
      "id": 12,
      "device_id": "TRANSFORMER_01",
      "incident_type": "CRITICAL_THERMAL_TRIP",
      "details": "Core Temperature Trip (65.2 °C >= 65.0 °C)",
      "t_core": 65.2,
      "email_dispatched": 1,
      "created_at": "2026-11-12 11:45:00"
    }
  ]
}
```

---

### `GET /api/users` & `POST /api/users` & `DELETE /api/users`
User whitelist management for team access control. (Restricted to `ADMIN` role).
