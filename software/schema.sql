-- ============================================================
-- Transformer CBM Cloud Database Schema (Cloudflare D1 SQLite)
-- ============================================================

-- 1. Real-time & Historical Telemetry Storage
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    t_core REAL NOT NULL,
    t_inlet REAL NOT NULL,
    t_predicted REAL NOT NULL,
    rate_of_rise REAL NOT NULL,
    v_12v REAL DEFAULT 12.0,
    i_12v REAL DEFAULT 0.0,
    v_5v REAL DEFAULT 5.0,
    i_5v REAL DEFAULT 0.0,
    v_3v3 REAL DEFAULT 3.3,
    i_3v3 REAL DEFAULT 0.0,
    pson_active INTEGER NOT NULL DEFAULT 1,
    fault_code INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_telemetry_created ON telemetry(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_telemetry_device ON telemetry(device_id, created_at DESC);

-- 2. Bidirectional Remote Command Queue
CREATE TABLE IF NOT EXISTS commands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    command_type TEXT NOT NULL CHECK(command_type IN ('POWER_ON', 'POWER_OFF', 'RESET_FAULT', 'SET_FAN')),
    payload TEXT DEFAULT '{}',
    status TEXT NOT NULL DEFAULT 'PENDING' CHECK(status IN ('PENDING', 'EXECUTED', 'CANCELLED', 'EXPIRED')),
    issued_by TEXT NOT NULL,
    issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    executed_at DATETIME
);

CREATE INDEX IF NOT EXISTS idx_commands_status ON commands(device_id, status);

-- 3. Incident Audit & Diagnostic Alert History
CREATE TABLE IF NOT EXISTS incident_alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    details TEXT NOT NULL,
    t_core REAL,
    email_dispatched INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_incident_created ON incident_alerts(created_at DESC);

-- 4. Authorized User Whitelist (Google OAuth 2.0 Access Control)
CREATE TABLE IF NOT EXISTS authorized_users (
    email TEXT PRIMARY KEY,
    name TEXT,
    role TEXT NOT NULL DEFAULT 'VIEWER' CHECK(role IN ('ADMIN', 'OPERATOR', 'VIEWER')),
    added_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 5. System Configuration & Watchdog Email Controls
CREATE TABLE IF NOT EXISTS system_settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT OR IGNORE INTO system_settings (key, value) VALUES ('watchdog_email_enabled', '0');

-- Seed Initial Administrators & Baseline Data
INSERT OR IGNORE INTO authorized_users (email, name, role) 
VALUES ('kumarisselva68@gmail.com', 'Kumar Selva (Admin)', 'ADMIN');

INSERT OR IGNORE INTO authorized_users (email, name, role) 
VALUES ('yogarathinam26@gmail.com', 'Yogarathinam (Admin)', 'ADMIN');

INSERT INTO telemetry (device_id, t_core, t_inlet, t_predicted, rate_of_rise, v_12v, i_12v, v_5v, i_5v, v_3v3, i_3v3, pson_active, fault_code)
VALUES ('TRANSFORMER_01', 34.5, 27.2, 35.1, 0.02, 12.04, 2.15, 5.01, 0.85, 3.31, 0.42, 1, 0);
