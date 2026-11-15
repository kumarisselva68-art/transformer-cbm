/**
 * Google OAuth 2.0 Identity Verification & Authorization Engine
 * Cloudflare Edge Worker Native Implementation
 */

// Cache Google Public Keys / Token verification responses for 5 minutes
const tokenCache = new Map();

/**
 * Verify Google ID Token (JWT) and check authorization against whitelist
 * @param {string} idToken - The Google JWT credential string
 * @param {object} env - Cloudflare Worker environment bindings
 * @param {object} db - D1 Database binding
 * @returns {Promise<{authorized: boolean, user?: object, error?: string}>}
 */
export async function verifyGoogleTokenAndAuthorize(idToken, env, db) {
  if (!idToken) {
    return { authorized: false, error: 'Missing authentication token' };
  }

  // Developer Bypass for automated unit tests and local testing
  if (env.ENVIRONMENT === 'development' && idToken === 'dev-admin-token') {
    return {
      authorized: true,
      user: {
        email: 'admin@gmail.com',
        name: 'Local Dev Administrator',
        role: 'ADMIN'
      }
    };
  }

  // Check in-memory Worker cache
  const cached = tokenCache.get(idToken);
  if (cached && cached.expiresAt > Date.now()) {
    return authorizeUserEmail(cached.payload, env, db);
  }

  try {
    // Validate with Google OAuth2 Tokeninfo Endpoint
    const googleRes = await fetch(`https://oauth2.googleapis.com/tokeninfo?id_token=${encodeURIComponent(idToken)}`);
    if (!googleRes.ok) {
      const errText = await googleRes.text();
      return { authorized: false, error: `Invalid Google Token: ${errText}` };
    }

    const payload = await googleRes.json();

    // Verify Audience (Matches our Google Client ID if configured)
    if (env.GOOGLE_CLIENT_ID && env.GOOGLE_CLIENT_ID !== 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com') {
      if (payload.aud !== env.GOOGLE_CLIENT_ID) {
        return { authorized: false, error: 'Google Client ID mismatch (Audience unauthorized)' };
      }
    }

    // Verify Issuer
    if (payload.iss !== 'accounts.google.com' && payload.iss !== 'https://accounts.google.com') {
      return { authorized: false, error: 'Invalid Google token issuer' };
    }

    // Verify Expiration
    const nowSec = Math.floor(Date.now() / 1000);
    if (payload.exp && parseInt(payload.exp, 10) < nowSec) {
      return { authorized: false, error: 'Google Token has expired' };
    }

    // Cache valid payload (expires 60s before token expiration)
    const ttlMs = Math.max(10, (parseInt(payload.exp, 10) - nowSec - 60)) * 1000;
    tokenCache.set(idToken, {
      payload,
      expiresAt: Date.now() + Math.min(ttlMs, 300000)
    });

    return await authorizeUserEmail(payload, env, db);
  } catch (err) {
    return { authorized: false, error: `Token validation error: ${err.message}` };
  }
}

/**
 * Check if the verified Google user email is authorized in D1 or environment variable
 */
async function authorizeUserEmail(payload, env, db) {
  const email = (payload.email || '').toLowerCase().trim();
  if (!email) {
    return { authorized: false, error: 'Google profile does not contain a verified email' };
  }

  // 1. Check D1 Database authorized_users table
  if (db) {
    try {
      const row = await db.prepare(
        'SELECT email, name, role FROM authorized_users WHERE LOWER(email) = ?'
      ).bind(email).first();

      if (row) {
        return {
          authorized: true,
          user: {
            email: row.email,
            name: row.name || payload.name || email,
            role: row.role || 'VIEWER',
            picture: payload.picture
          }
        };
      }
    } catch (err) {
      console.error('[AUTH_DB_ERROR]', err);
    }
  }

  // 2. Check fallback environment ALLOWED_EMAILS list
  const allowedList = (env.ALLOWED_EMAILS || '')
    .split(',')
    .map(e => e.trim().toLowerCase())
    .filter(Boolean);

  if (allowedList.includes(email)) {
    return {
      authorized: true,
      user: {
        email,
        name: payload.name || email,
        role: 'ADMIN',
        picture: payload.picture
      }
    };
  }

  return {
    authorized: false,
    error: `Access denied. Email '${email}' is not in the authorized personnel list.`
  };
}
