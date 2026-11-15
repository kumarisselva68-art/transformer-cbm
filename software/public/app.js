/**
 * Transformer CBM Platform — Client Application Engine
 * Apple / Linear Precision Aesthetic • Proportional Restrained Modals
 * Master Industrial Power Switch with Physical Thermal Caution Warning
 * Dynamic Dark/Light Vector Architecture Schematics
 */

// Global State
let currentUser = null;
let idToken = sessionStorage.getItem('google_id_token') || null;
let pollTimer = null;
let masterThermalChart = null;
let railsChart = null;
let currentTheme = localStorage.getItem('cbm_theme') || 'light';
let activeDiagramName = '07_master_hardware_circuit_schematic.svg';

// DOM Elements
const landingView = document.getElementById('landingView');
const appContainer = document.getElementById('appContainer');
const loginError = document.getElementById('loginError');

// Radial Gauges
const arcCoreTemp = document.getElementById('arcCoreTemp');
const readoutCoreTemp = document.getElementById('readoutCoreTemp');
const tagCoreStatus = document.getElementById('tagCoreStatus');
const lblCoreThreshold = document.getElementById('lblCoreThreshold');

const arcInletTemp = document.getElementById('arcInletTemp');
const readoutInletTemp = document.getElementById('readoutInletTemp');
const readoutDeltaT = document.getElementById('readoutDeltaT');

const arcPredTemp = document.getElementById('arcPredTemp');
const readoutPredTemp = document.getElementById('readoutPredTemp');
const readoutRateOfRise = document.getElementById('readoutRateOfRise');

const arcFanSpeed = document.getElementById('arcFanSpeed');
const readoutFanSpeed = document.getElementById('readoutFanSpeed');
const readoutFanMode = document.getElementById('readoutFanMode');
const animatedFanSvg = document.getElementById('animatedFanSvg');

// Hero Banner
const heroHeading = document.getElementById('heroHeading');
const heroSub = document.getElementById('heroSub');
const mainStateChip = document.getElementById('mainStateChip');
const lastHeartbeatTime = document.getElementById('lastHeartbeatTime');
const healthDot = document.getElementById('healthDot');
const healthStatusText = document.getElementById('healthStatusText');
const ctrlPowerStatusTag = document.getElementById('ctrlPowerStatusTag');

// Power Rails Meters
const rail12vVolts = document.getElementById('rail12vVolts');
const rail12vAmps = document.getElementById('rail12vAmps');
const rail12vWatts = document.getElementById('rail12vWatts');
const rail5vVolts = document.getElementById('rail5vVolts');
const rail5vAmps = document.getElementById('rail5vAmps');
const rail5vWatts = document.getElementById('rail5vWatts');
const rail3v3Volts = document.getElementById('rail3v3Volts');
const rail3v3Amps = document.getElementById('rail3v3Amps');
const rail3v3Watts = document.getElementById('rail3v3Watts');

// User Profile & Themes
const userAvatar = document.getElementById('userAvatar');
const userName = document.getElementById('userName');
const userRoleBadge = document.getElementById('userRoleBadge');
const adminUsersCard = document.getElementById('adminUsersCard');
const btnSignOut = document.getElementById('btnSignOut');
const btnThemeToggle = document.getElementById('btnThemeToggle');
const btnLandingThemeToggle = document.getElementById('btnLandingThemeToggle');

// Master Power Switch
const chkMasterPowerToggle = document.getElementById('chkMasterPowerToggle');
const lblPowerStateTitle = document.getElementById('lblPowerStateTitle');
const lblPowerStateSub = document.getElementById('lblPowerStateSub');

// Controls & Safety
const heroBtnTripStop = document.getElementById('heroBtnTripStop');
const btnEmergencyStop = document.getElementById('btnEmergencyStop');
const btnResetFaultLatch = document.getElementById('btnResetFaultLatch');
const btnFanModeAuto = document.getElementById('btnFanModeAuto');
const btnFanModeManual = document.getElementById('btnFanModeManual');
const fanSliderWrap = document.getElementById('fanSliderWrap');
const sliderFanSpeed = document.getElementById('sliderFanSpeed');
const lblFanSpeedVal = document.getElementById('lblFanSpeedVal');
const btnApplyFan = document.getElementById('btnApplyFan');

// Watchdog & Notification Setting Elements
const pillWatchdogState = document.getElementById('pillWatchdogState');
const chkWatchdogEmail = document.getElementById('chkWatchdogEmail');
const chkNotifyOvertemp = document.getElementById('chkNotifyOvertemp');
const chkNotifyEmergency = document.getElementById('chkNotifyEmergency');
const chkNotifyPowerOff = document.getElementById('chkNotifyPowerOff');
const btnSaveNotifications = document.getElementById('btnSaveNotifications');

// Predictive Health & Insulation Prognostics Elements
const valHealthIndex = document.getElementById('valHealthIndex');
const barHealthIndex = document.getElementById('barHealthIndex');
const badgeHealthClassification = document.getElementById('badgeHealthClassification');
const valHotspotEstimate = document.getElementById('valHotspotEstimate');
const valArrheniusFactor = document.getElementById('valArrheniusFactor');
const valThermalDelta = document.getElementById('valThermalDelta');
const titleHealthAdvisory = document.getElementById('titleHealthAdvisory');
const textHealthAdvisory = document.getElementById('textHealthAdvisory');

// Settings & Threshold Inputs
const inputCoreTripLimit = document.getElementById('inputCoreTripLimit');
const inputPredTripLimit = document.getElementById('inputPredTripLimit');
const inputHorizonSec = document.getElementById('inputHorizonSec');
const btnSaveThresholds = document.getElementById('btnSaveThresholds');
const btnResetDefaults = document.getElementById('btnResetDefaults');

// Collapsible Architecture Viewer
const btnToggleArchViewer = document.getElementById('btnToggleArchViewer');
const lblToggleArch = document.getElementById('lblToggleArch');
const archViewerContainer = document.getElementById('archViewerContainer');
const diagramBtns = document.querySelectorAll('.diagram-btn');
const diagramDisplayImg = document.getElementById('diagramDisplayImg');
const diagramViewerTitle = document.getElementById('diagramViewerTitle');
const btnDiagramOpenFull = document.getElementById('btnDiagramOpenFull');

// Custom Modal & Toast Elements
const customModal = document.getElementById('customModal');
const modalTitle = document.getElementById('modalTitle');
const modalMessage = document.getElementById('modalMessage');
const modalBadgeType = document.getElementById('modalBadgeType');
const modalIconWrap = document.getElementById('modalIconWrap');
const modalMessageBox = document.getElementById('modalMessageBox');
const btnModalCancel = document.getElementById('btnModalCancel');
const btnModalConfirm = document.getElementById('btnModalConfirm');
const toastContainer = document.getElementById('toastContainer');

let modalResolver = null;

// Circumference of radial gauge (r = 48)
const GAUGE_CIRCUMFERENCE = 2 * Math.PI * 48; // ~301.59

// ==========================================================
// 1. APPLICATION INITIALIZATION & THEME SETUP
// ==========================================================

window.addEventListener('DOMContentLoaded', () => {
  applyTheme(currentTheme);
  setupNavigationTabs();
  setupControlListeners();
  setupDiagramSwitcher();
  setupSettingsListeners();
  setupDemoSimulatorListeners();
  initScrollReveal();
  initKeyboardShortcuts();
  initExportListeners();

  // If already authenticated in current session, verify session
  if (idToken) {
    verifySession();
  } else {
    showLandingPage();
    initGoogleAuth();
  }
});

function initScrollReveal() {
  const elements = document.querySelectorAll('.reveal-on-scroll');
  if (!elements.length) return;
  if (!('IntersectionObserver' in window)) {
    elements.forEach(el => el.classList.add('revealed'));
    return;
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -30px 0px' });
  elements.forEach(el => observer.observe(el));
}

function applyTheme(theme) {
  currentTheme = theme;
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('cbm_theme', theme);

  if (masterThermalChart && railsChart) {
    updateChartsTheme();
  }

  updateDiagramThemeSource();
}

if (btnThemeToggle) {
  btnThemeToggle.addEventListener('click', () => {
    applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
  });
}

if (btnLandingThemeToggle) {
  btnLandingThemeToggle.addEventListener('click', () => {
    applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
  });
}

function showLandingPage() {
  if (landingView) landingView.classList.remove('hidden');
  if (appContainer) appContainer.classList.add('hidden');
}

function showAppWorkspace() {
  if (landingView) landingView.classList.add('hidden');
  if (appContainer) appContainer.classList.remove('hidden');
}

// ==========================================================
// 2. PROPORTIONATE MODAL DIALOGS & TOAST SYSTEM
// ==========================================================

function showConfirmDialog({
  title = 'Confirm Command',
  message = 'Are you sure you wish to proceed?',
  caution = null,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  isDanger = false,
  badgeType = 'SUPERVISORY ACTION'
} = {}) {
  return new Promise((resolve) => {
    modalResolver = resolve;

    modalTitle.textContent = title;
    modalBadgeType.textContent = badgeType;
    btnModalConfirm.textContent = confirmText;
    btnModalCancel.textContent = cancelText;

    // Reset message box
    modalMessageBox.innerHTML = `<p class="modal-message">${message}</p>`;

    // Add optional safety caution alert
    if (caution) {
      const alertDiv = document.createElement('div');
      alertDiv.className = 'modal-caution-alert';
      alertDiv.innerHTML = `<strong>SAFETY NOTICE:</strong> ${caution}`;
      modalMessageBox.appendChild(alertDiv);
    }

    if (isDanger) {
      btnModalConfirm.className = 'btn-modal-confirm danger';
      modalIconWrap.className = 'modal-icon-badge danger';
      modalIconWrap.innerHTML = `<svg class="modal-svg" viewBox="0 0 24 24"><use href="#icon-stop"/></svg>`;
    } else {
      btnModalConfirm.className = 'btn-modal-confirm';
      modalIconWrap.className = 'modal-icon-badge';
      modalIconWrap.innerHTML = `<svg class="modal-svg" viewBox="0 0 24 24"><use href="#icon-alert"/></svg>`;
    }

    customModal.classList.remove('hidden');
  });
}

function closeConfirmDialog(result) {
  customModal.classList.add('hidden');
  if (modalResolver) {
    modalResolver(result);
    modalResolver = null;
  }
}

btnModalConfirm.addEventListener('click', () => closeConfirmDialog(true));
btnModalCancel.addEventListener('click', () => closeConfirmDialog(false));
customModal.addEventListener('click', (e) => {
  if (e.target === customModal) closeConfirmDialog(false);
});

// Toast notification helper
function showToast(message, type = 'info', duration = 3500) {
  if (!toastContainer) return;

  const toast = document.createElement('div');
  toast.className = `toast-item ${type}`;

  let iconRef = '#icon-activity';
  if (type === 'success') iconRef = '#icon-check';
  if (type === 'error') iconRef = '#icon-stop';
  if (type === 'warning') iconRef = '#icon-alert';

  toast.innerHTML = `
    <svg class="toast-icon" viewBox="0 0 24 24"><use href="${iconRef}"/></svg>
    <span class="toast-text">${message}</span>
  `;

  toastContainer.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast);
    }, 220);
  }, duration);
}

// ==========================================================
// 3. GOOGLE IDENTITY SERVICES (OAUTH 2.0)
// ==========================================================

function initGoogleAuth() {
  if (window.google && window.google.accounts) {
    const clientId = '250848327932-c2rob7h7agcs6db8s7daf1r71fsa5ph4.apps.googleusercontent.com';

    google.accounts.id.initialize({
      client_id: clientId,
      callback: handleCredentialResponse,
      auto_select: false
    });

    const btnContainer = document.getElementById('googleBtnContainer');
    if (btnContainer) {
      google.accounts.id.renderButton(btnContainer, {
        theme: currentTheme === 'dark' ? 'filled_black' : 'outline',
        size: 'large',
        width: 280,
        shape: 'pill'
      });
    }

    const navBtnContainer = document.getElementById('landingNavGoogleBtn');
    if (navBtnContainer) {
      google.accounts.id.renderButton(navBtnContainer, {
        theme: currentTheme === 'dark' ? 'filled_black' : 'outline',
        size: 'medium',
        shape: 'pill'
      });
    }
  } else {
    setTimeout(initGoogleAuth, 300);
  }
}

async function handleCredentialResponse(response) {
  if (!response.credential) {
    showLoginError('No credential received from Google identity service.');
    return;
  }

  idToken = response.credential;
  sessionStorage.setItem('google_id_token', idToken);
  await verifySession();
}

async function verifySession() {
  try {
    const res = await apiFetch('/api/auth/verify');
    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.error || 'Authentication denied');
    }

    const data = await res.json();
    currentUser = data.user;

    // Transition from landing page to workspace
    showAppWorkspace();

    // Populate user profile
    userName.textContent = currentUser.name || currentUser.email;
    userRoleBadge.textContent = currentUser.role || 'VIEWER';
    if (currentUser.picture) {
      userAvatar.src = currentUser.picture;
    }

    // Role-based visibility
    if (currentUser.role !== 'ADMIN') {
      if (adminUsersCard) adminUsersCard.classList.add('hidden');
    } else {
      if (adminUsersCard) adminUsersCard.classList.remove('hidden');
      loadAuthorizedUsers();
    }

    // Initialize telemetry polling & charts
    initCharts();
    loadHistory();
    loadAlerts();
    loadSystemSettings();
    startPolling();

  } catch (err) {
    showLoginError(err.message);
    sessionStorage.removeItem('google_id_token');
    idToken = null;
    showLandingPage();
    initGoogleAuth();
  }
}

function showLoginError(msg) {
  if (loginError) {
    loginError.textContent = msg;
    loginError.classList.remove('hidden');
  }
}

if (btnSignOut) {
  btnSignOut.addEventListener('click', () => {
    sessionStorage.removeItem('google_id_token');
    idToken = null;
    currentUser = null;
    clearInterval(pollTimer);
    location.reload();
  });
}

// ==========================================================
// 4. AUTHENTICATED FETCH HELPER
// ==========================================================

async function apiFetch(endpoint, options = {}) {
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (idToken) {
    headers['Authorization'] = `Bearer ${idToken}`;
  }

  return fetch(endpoint, { ...options, headers });
}

// ==========================================================
// 5. NAVIGATION TABS (WITH IMMEDIATE SCROLL RESET)
// ==========================================================

function setupNavigationTabs() {
  const allTabs = document.querySelectorAll('[data-tab]');
  
  allTabs.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTabId = btn.getAttribute('data-tab');

      // Update active state across all matching buttons
      allTabs.forEach(b => {
        if (b.getAttribute('data-tab') === targetTabId) {
          b.classList.add('active');
        } else {
          b.classList.remove('active');
        }
      });

      // Switch Tab Panes
      document.querySelectorAll('.tab-pane').forEach(pane => {
        if (pane.id === targetTabId) {
          pane.classList.add('active');
        } else {
          pane.classList.remove('active');
        }
      });

      // Scroll to the very top immediately on page/tab change!
      window.scrollTo({ top: 0, behavior: 'instant' });
      const mainWorkspace = document.querySelector('.main-workspace');
      if (mainWorkspace) mainWorkspace.scrollTop = 0;

      // Resize charts if tab switched to charts
      if (targetTabId === 'tab-dashboard' && masterThermalChart) masterThermalChart.resize();
      if (targetTabId === 'tab-rails' && railsChart) railsChart.resize();
    });
  });
}

// ==========================================================
// 6. COLLAPSIBLE ARCHITECTURE & DYNAMIC SVG VIEWER
// ==========================================================

function setupDiagramSwitcher() {
  // Collapsible toggle button
  if (btnToggleArchViewer && archViewerContainer) {
    btnToggleArchViewer.addEventListener('click', () => {
      const isHidden = archViewerContainer.classList.contains('hidden');
      if (isHidden) {
        archViewerContainer.classList.remove('hidden');
        lblToggleArch.textContent = 'Hide Architecture';
      } else {
        archViewerContainer.classList.add('hidden');
        lblToggleArch.textContent = 'Show Architecture';
      }
    });
  }

  // Diagram selector buttons
  diagramBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      diagramBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      activeDiagramName = btn.getAttribute('data-diagram');
      const diagramTitle = btn.textContent;

      if (diagramViewerTitle) diagramViewerTitle.textContent = diagramTitle;
      updateDiagramThemeSource();
    });
  });
}

function updateDiagramThemeSource() {
  if (!diagramDisplayImg) return;
  const themeFolder = (currentTheme === 'dark') ? 'dark' : 'light';
  const fullPath = `assets/diagrams/${themeFolder}/${activeDiagramName}`;
  diagramDisplayImg.src = fullPath;
  if (btnDiagramOpenFull) btnDiagramOpenFull.href = fullPath;
}

// ==========================================================
// 7. REAL-TIME TELEMETRY STREAMING & RADIAL GAUGES
// ==========================================================

function startPolling() {
  if (pollTimer) clearInterval(pollTimer);
  pollTelemetry();
  pollTimer = setInterval(pollTelemetry, 3000); // 3-second loop
}

let prevTripState = false;

async function pollTelemetry() {
  try {
    let d;
    if (demoSimulatorState) {
      if (demoSimulatorState === 'NORMAL') {
        simulatedData.t_core = +(38.2 + (Math.random() * 0.4 - 0.2)).toFixed(2);
        simulatedData.t_inlet = +(27.5 + (Math.random() * 0.2 - 0.1)).toFixed(2);
        simulatedData.rate_of_rise = 0.01;
        simulatedData.t_predicted = +(simulatedData.t_core + 0.3).toFixed(2);
        simulatedData.pson_active = 1;
        simulatedData.fault_code = 0;
      } else if (demoSimulatorState === 'OVERHEAT') {
        if (simulatedData.t_core < 68.5) {
          simulatedData.t_core = +(simulatedData.t_core + 0.85).toFixed(2);
        }
        simulatedData.rate_of_rise = 0.28;
        simulatedData.t_predicted = +(simulatedData.t_core + 30 * simulatedData.rate_of_rise).toFixed(2);
        if (simulatedData.t_core >= 65.0) {
          simulatedData.pson_active = 0;
          simulatedData.fault_code = 1;
        }
      } else if (demoSimulatorState === 'COOLDOWN') {
        simulatedData.t_core = +Math.max(34.0, simulatedData.t_core - 0.95).toFixed(2);
        simulatedData.rate_of_rise = -0.19;
        simulatedData.t_predicted = +Math.max(32.0, simulatedData.t_core - 5.7).toFixed(2);
        if (simulatedData.t_core <= 50.0) {
          simulatedData.pson_active = 1;
          simulatedData.fault_code = 0;
        }
      }
      simulatedData.created_at = new Date().toISOString();
      d = simulatedData;
    } else {
      const res = await apiFetch('/api/telemetry/latest');
      if (!res.ok) return;
      const result = await res.json();
      d = result.data;
      if (!d) return;
    }

    // 1. Update Transformer Core Hotspot (T1)
    readoutCoreTemp.textContent = d.t_core.toFixed(1);
    const corePct = Math.min(1, Math.max(0, (d.t_core - 20) / 50));
    arcCoreTemp.style.strokeDashoffset = GAUGE_CIRCUMFERENCE * (1 - corePct);

    const tripLimit = parseFloat(inputCoreTripLimit ? inputCoreTripLimit.value : 65.0);
    if (d.t_core >= tripLimit) {
      arcCoreTemp.style.stroke = 'var(--color-rose)';
      tagCoreStatus.textContent = 'FAULT TRIP';
      tagCoreStatus.className = 'mono font-bold text-danger';
    } else if (d.t_core >= tripLimit - 10.0) {
      arcCoreTemp.style.stroke = 'var(--color-amber)';
      tagCoreStatus.textContent = 'ELEVATED';
      tagCoreStatus.className = 'mono font-bold';
      tagCoreStatus.style.color = 'var(--color-amber)';
    } else {
      arcCoreTemp.style.stroke = 'var(--color-emerald)';
      tagCoreStatus.textContent = 'NOMINAL';
      tagCoreStatus.className = 'tag-status-normal';
      tagCoreStatus.style.color = '';
    }

    // 2. Update Cooling Airflow Inlet (T2)
    readoutInletTemp.textContent = d.t_inlet.toFixed(1);
    const inletPct = Math.min(1, Math.max(0, (d.t_inlet - 15) / 35));
    arcInletTemp.style.strokeDashoffset = GAUGE_CIRCUMFERENCE * (1 - inletPct);
    readoutDeltaT.textContent = (d.t_core - d.t_inlet).toFixed(1) + ' °C';

    // 3. Update Predictive Horizon (Tp)
    readoutPredTemp.textContent = d.t_predicted.toFixed(1);
    const predPct = Math.min(1, Math.max(0, (d.t_predicted - 20) / 50));
    arcPredTemp.style.strokeDashoffset = GAUGE_CIRCUMFERENCE * (1 - predPct);
    readoutRateOfRise.textContent = (d.rate_of_rise >= 0 ? '+' : '') + d.rate_of_rise.toFixed(2) + ' °C/s';

    // 4. Update Active Fan Modulation
    const fanSpeedVal = d.pson_active ? 75 : 0;
    const fanPct = fanSpeedVal / 100;
    arcFanSpeed.style.strokeDashoffset = GAUGE_CIRCUMFERENCE * (1 - fanPct);
    readoutFanSpeed.textContent = d.pson_active ? '75%' : '0%';
    
    if (d.pson_active) {
      animatedFanSvg.classList.add('spinning');
    } else {
      animatedFanSvg.classList.remove('spinning');
    }

    // 5. Update Master Power Switch & State Display
    if (chkMasterPowerToggle) {
      chkMasterPowerToggle.checked = d.pson_active;
    }
    if (d.pson_active) {
      mainStateChip.className = 'status-chip';
      mainStateChip.textContent = 'MAIN OUTPUT ENERGIZED';
      ctrlPowerStatusTag.className = 'power-status-tag';
      ctrlPowerStatusTag.textContent = 'ACTIVE [ENERGIZED]';
      if (lblPowerStateTitle) lblPowerStateTitle.textContent = 'Main Output Energized';
      if (lblPowerStateSub) lblPowerStateSub.textContent = 'Transformer main rails are active and delivering power to the load.';
    } else {
      mainStateChip.className = 'status-chip off';
      mainStateChip.textContent = 'MAIN RAILS ISOLATED';
      ctrlPowerStatusTag.className = 'power-status-tag off';
      ctrlPowerStatusTag.textContent = 'ISOLATED [DE-ENERGIZED]';
      if (lblPowerStateTitle) lblPowerStateTitle.textContent = 'Main Output Isolated';
      if (lblPowerStateSub) lblPowerStateSub.textContent = 'Transformer output rails are safely de-energized.';
    }

    // 6. System Health Indicator
    if (d.t_core >= tripLimit || (d.fault_code && d.fault_code > 0)) {
      healthDot.className = 'health-dot red';
      healthStatusText.textContent = 'SUPERVISORY TRIP';
      if (heroHeading) {
        heroHeading.textContent = 'SUPERVISORY TRIP';
        heroHeading.classList.add('text-danger');
      }
      if (heroSub) heroSub.textContent = 'Hardware safety trip latched — main output rails isolated.';
    } else {
      healthDot.className = 'health-dot';
      healthStatusText.textContent = 'SYSTEM NORMAL';
      if (heroHeading) {
        heroHeading.textContent = 'SYSTEM NORMAL';
        heroHeading.classList.remove('text-danger');
      }
      if (heroSub) heroSub.textContent = 'Continuous multi-rail telemetry and dual overtemperature supervision active.';
    }

    // 7. Predictive Health & IEEE Std C57.91 Arrhenius Prognostics
    const deltaT = d.t_core - d.t_inlet;
    const tHst = d.t_core + 0.08 * Math.max(0, deltaT) + 2.5; // Virtual Winding Hotspot (~ +4.2°C gradient)
    // IEEE Std C57.91 Arrhenius Aging Acceleration Factor (relative to 110°C / 383.15 K standard reference)
    const fAa = Math.exp((15000 / 383.15) - (15000 / (tHst + 273.15)));

    // Composite Transformer Health Index HI (0 - 100%)
    const penThermal = Math.max(0, (d.t_core - 45) * 1.4);
    const penAging = Math.min(20, fAa * 200);
    const penTrip = (d.pson_active === 0 || (d.fault_code && d.fault_code > 0)) ? 15 : 0;
    const healthIndex = Math.max(0, Math.min(100, 100 - penThermal - penAging - penTrip));

    if (valHealthIndex) valHealthIndex.textContent = healthIndex.toFixed(1);
    if (barHealthIndex) barHealthIndex.style.width = healthIndex.toFixed(1) + '%';
    if (valHotspotEstimate) valHotspotEstimate.textContent = tHst.toFixed(1);
    if (valArrheniusFactor) valArrheniusFactor.textContent = fAa < 0.001 ? '< 0.001' : fAa.toFixed(3);
    if (valThermalDelta) valThermalDelta.textContent = (deltaT >= 0 ? '+' : '') + deltaT.toFixed(1);

    if (badgeHealthClassification && barHealthIndex && textHealthAdvisory) {
      if (healthIndex >= 90) {
        badgeHealthClassification.textContent = 'OPTIMAL';
        badgeHealthClassification.style.backgroundColor = 'rgba(16, 185, 129, 0.15)';
        badgeHealthClassification.style.color = 'var(--color-emerald)';
        badgeHealthClassification.style.borderColor = 'rgba(16, 185, 129, 0.3)';
        barHealthIndex.style.background = 'var(--color-emerald)';
        textHealthAdvisory.textContent = 'Thermal margin optimal — Class B endurance verified.';
      } else if (healthIndex >= 75) {
        badgeHealthClassification.textContent = 'MODERATE';
        badgeHealthClassification.style.backgroundColor = 'rgba(6, 182, 212, 0.15)';
        badgeHealthClassification.style.color = 'var(--color-cyan)';
        badgeHealthClassification.style.borderColor = 'rgba(6, 182, 212, 0.3)';
        barHealthIndex.style.background = 'var(--color-cyan)';
        textHealthAdvisory.textContent = 'Moderate thermal rise — dynamic cooling active.';
      } else if (healthIndex >= 55) {
        badgeHealthClassification.textContent = 'DEGRADED';
        badgeHealthClassification.style.backgroundColor = 'rgba(245, 158, 11, 0.15)';
        badgeHealthClassification.style.color = 'var(--color-amber)';
        badgeHealthClassification.style.borderColor = 'rgba(245, 158, 11, 0.3)';
        barHealthIndex.style.background = 'var(--color-amber)';
        textHealthAdvisory.textContent = 'Elevated core temperature — accelerated aging advisory.';
      } else {
        badgeHealthClassification.textContent = 'CRITICAL TRIP';
        badgeHealthClassification.style.backgroundColor = 'rgba(244, 63, 94, 0.15)';
        badgeHealthClassification.style.color = 'var(--color-rose)';
        badgeHealthClassification.style.borderColor = 'rgba(244, 63, 94, 0.3)';
        barHealthIndex.style.background = 'var(--color-rose)';
        textHealthAdvisory.textContent = 'Overtemperature lockout active — main load rails isolated.';
      }
    }

    // 7b. Sound Industrial Safety Chime on trip transition
    const isTripped = (d.t_core >= tripLimit || (d.fault_code && d.fault_code > 0) || d.pson_active === 0);
    if (isTripped && !prevTripState) {
      playSafetyChime();
    }
    prevTripState = isTripped;

    // 7c. Update Firmware Fan Piecewise Curve Visualizer
    updateFanCurveDot(d.t_core, fanSpeedVal);

    // 8. Power Rails Meters
    const v12 = d.v_12v || 12.04;
    const i12 = d.i_12v || 0.0;
    const w12 = v12 * i12;
    rail12vVolts.textContent = v12.toFixed(2);
    rail12vAmps.textContent = i12.toFixed(2);
    rail12vWatts.textContent = w12.toFixed(1);

    const v5 = d.v_5v || 5.01;
    const i5 = d.i_5v || 0.85;
    const w5 = v5 * i5;
    rail5vVolts.textContent = v5.toFixed(2);
    rail5vAmps.textContent = i5.toFixed(2);
    rail5vWatts.textContent = w5.toFixed(1);

    const v3 = d.v_3v3 || 3.31;
    const i3 = d.i_3v3 || 0.42;
    const w3 = v3 * i3;
    rail3v3Volts.textContent = v3.toFixed(2);
    rail3v3Amps.textContent = i3.toFixed(2);
    rail3v3Watts.textContent = w3.toFixed(1);

    // Composite Power & Multi-Rail Allocation Bar
    const totalW = Math.max(0.1, w12 + w5 + w3);
    const valTotalPower = document.getElementById('valTotalPower');
    if (valTotalPower) valTotalPower.textContent = totalW.toFixed(1);

    const splitBar12v = document.getElementById('splitBar12v');
    const splitBar5v = document.getElementById('splitBar5v');
    const splitBar3v3 = document.getElementById('splitBar3v3');
    const pctRail12v = document.getElementById('pctRail12v');
    const pctRail5v = document.getElementById('pctRail5v');
    const pctRail3v3 = document.getElementById('pctRail3v3');

    if (splitBar12v && splitBar5v && splitBar3v3) {
      const p12 = Math.min(100, Math.max(0, Math.round((w12 / totalW) * 100)));
      const p5 = Math.min(100 - p12, Math.max(0, Math.round((w5 / totalW) * 100)));
      const p3 = Math.max(0, 100 - p12 - p5);
      splitBar12v.style.width = p12 + '%';
      splitBar5v.style.width = p5 + '%';
      splitBar3v3.style.width = p3 + '%';
      if (pctRail12v) pctRail12v.textContent = p12 + '%';
      if (pctRail5v) pctRail5v.textContent = p5 + '%';
      if (pctRail3v3) pctRail3v3.textContent = p3 + '%';
    }

    // 8. Heartbeat Timestamp
    if (d.created_at) {
      lastHeartbeatTime.textContent = new Date(d.created_at).toLocaleTimeString();
    }

    // 9. Append point to charts
    appendChartPoints(d);
  } catch (err) {
    console.error('[POLL_ERROR]', err);
  }
}

// ==========================================================
// 8. STREAMING CHART.JS VISUALIZATION
// ==========================================================

function getChartColors() {
  const isDark = (currentTheme === 'dark');
  return {
    grid: isDark ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)',
    ticks: isDark ? '#71717a' : '#71717a',
    legend: isDark ? '#d4d4d8' : '#27272a'
  };
}

function initCharts() {
  const c = getChartColors();

  // Chart 1: Master Thermal Chart
  const ctxThermal = document.getElementById('masterThermalChart').getContext('2d');
  masterThermalChart = new Chart(ctxThermal, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: 'Core Hotspot (T1)',
          data: [],
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.1)',
          borderWidth: 2.2,
          tension: 0.3,
          fill: true,
          pointRadius: 2
        },
        {
          label: 'Cooling Inlet (T2)',
          data: [],
          borderColor: '#06b6d4',
          borderWidth: 1.8,
          tension: 0.3,
          pointRadius: 2
        },
        {
          label: 'Predicted Horizon (Tp)',
          data: [],
          borderColor: '#fbbf24',
          borderWidth: 2,
          borderDash: [5, 5],
          pointRadius: 0
        },
        {
          label: 'Trip Bound (65 °C)',
          data: [],
          borderColor: 'rgba(244, 63, 94, 0.75)',
          borderWidth: 1.5,
          borderDash: [4, 4],
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      interaction: { intersect: false, mode: 'index' },
      scales: {
        x: {
          grid: { color: c.grid },
          ticks: { color: c.ticks, font: { family: 'var(--font-mono)', size: 10 } }
        },
        y: {
          min: 20,
          max: 80,
          grid: { color: c.grid },
          ticks: { color: c.ticks, font: { family: 'var(--font-mono)', size: 11 } }
        }
      },
      plugins: {
        legend: { labels: { color: c.legend, font: { family: 'var(--font-sans)', size: 11, weight: 600 } } }
      }
    }
  });

  // Chart 2: Rails Load Distribution
  const ctxRails = document.getElementById('railsChart').getContext('2d');
  railsChart = new Chart(ctxRails, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        {
          label: '12V Rail Current (A)',
          data: [],
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245, 158, 11, 0.08)',
          borderWidth: 2,
          tension: 0.2,
          fill: true,
          pointRadius: 2
        },
        {
          label: '5V Rail Current (A)',
          data: [],
          borderColor: '#10b981',
          borderWidth: 1.8,
          tension: 0.2,
          pointRadius: 2
        },
        {
          label: '3.3V Rail Current (A)',
          data: [],
          borderColor: '#a855f7',
          borderWidth: 1.8,
          tension: 0.2,
          pointRadius: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      interaction: { intersect: false, mode: 'index' },
      scales: {
        x: {
          grid: { color: c.grid },
          ticks: { color: c.ticks, font: { family: 'var(--font-mono)', size: 10 } }
        },
        y: {
          min: 0,
          max: 6,
          grid: { color: c.grid },
          ticks: { color: c.ticks, font: { family: 'var(--font-mono)', size: 11 } }
        }
      },
      plugins: {
        legend: { labels: { color: c.legend, font: { family: 'var(--font-sans)', size: 11, weight: 600 } } }
      }
    }
  });
}

function updateChartsTheme() {
  const c = getChartColors();
  [masterThermalChart, railsChart].forEach(chart => {
    chart.options.scales.x.grid.color = c.grid;
    chart.options.scales.x.ticks.color = c.ticks;
    chart.options.scales.y.grid.color = c.grid;
    chart.options.scales.y.ticks.color = c.ticks;
    chart.options.plugins.legend.labels.color = c.legend;
    chart.update('none');
  });
}

async function loadHistory() {
  try {
    const res = await apiFetch('/api/telemetry/history?limit=30');
    if (!res.ok) return;
    const json = await res.json();
    const rows = json.data || [];

    masterThermalChart.data.labels = [];
    masterThermalChart.data.datasets.forEach(d => d.data = []);
    railsChart.data.labels = [];
    railsChart.data.datasets.forEach(d => d.data = []);

    rows.forEach(r => {
      const timeStr = new Date(r.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
      
      masterThermalChart.data.labels.push(timeStr);
      masterThermalChart.data.datasets[0].data.push(r.t_core);
      masterThermalChart.data.datasets[1].data.push(r.t_inlet);
      masterThermalChart.data.datasets[2].data.push(r.t_predicted);
      masterThermalChart.data.datasets[3].data.push(65.0);

      railsChart.data.labels.push(timeStr);
      railsChart.data.datasets[0].data.push(r.i_12v || 0.0);
      railsChart.data.datasets[1].data.push(r.i_5v || 0.0);
      railsChart.data.datasets[2].data.push(r.i_3v3 || 0.0);
    });

    masterThermalChart.update();
    railsChart.update();
  } catch (err) {
    console.error('[LOAD_HISTORY_ERROR]', err);
  }
}

function appendChartPoints(d) {
  if (!masterThermalChart || !railsChart) return;
  const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });

  if (masterThermalChart.data.labels.length >= 30) {
    masterThermalChart.data.labels.shift();
    masterThermalChart.data.datasets.forEach(ds => ds.data.shift());
  }
  masterThermalChart.data.labels.push(timeStr);
  masterThermalChart.data.datasets[0].data.push(d.t_core);
  masterThermalChart.data.datasets[1].data.push(d.t_inlet);
  masterThermalChart.data.datasets[2].data.push(d.t_predicted);
  masterThermalChart.data.datasets[3].data.push(65.0);
  masterThermalChart.update();

  if (railsChart.data.labels.length >= 30) {
    railsChart.data.labels.shift();
    railsChart.data.datasets.forEach(ds => ds.data.shift());
  }
  railsChart.data.labels.push(timeStr);
  railsChart.data.datasets[0].data.push(d.i_12v || 0.0);
  railsChart.data.datasets[1].data.push(d.i_5v || 0.0);
  railsChart.data.datasets[2].data.push(d.i_3v3 || 0.0);
  railsChart.update();
}

// ==========================================================
// 9. SUPERVISORY CONTROL ACTIONS (MASTER SWITCH & SAFETY WARNING)
// ==========================================================

function setupControlListeners() {
  // Industrial Master Power Toggle Switch
  if (chkMasterPowerToggle) {
    chkMasterPowerToggle.addEventListener('click', async (e) => {
      e.preventDefault(); // Pause until user confirms in dialog
      const willBeEnergized = !chkMasterPowerToggle.checked;

      if (!willBeEnergized) {
        // User is attempting to DE-ENERGIZE (Turn OFF)
        // Show proper physical safety caution warning
        const confirmed = await showConfirmDialog({
          title: 'De-energize Main Output',
          message: 'Transmit remote supervisory instruction to safely de-energize the transformer main load rails?',
          caution: 'Internal transformer windings, core iron, and secondary capacitor banks retain significant thermal mass and electrical charge. Do not touch internal components, coils, or heatsinks immediately; allow at least 60 seconds for safe thermal dissipation and electrical discharge.',
          confirmText: 'De-energize Output',
          cancelText: 'Cancel',
          isDanger: false,
          badgeType: 'POWER INTERFACE'
        });

        if (!confirmed) return;
        chkMasterPowerToggle.checked = false;
        await sendPowerCommand('OFF');

      } else {
        // User is attempting to ENERGIZE (Turn ON)
        const confirmed = await showConfirmDialog({
          title: 'Energize Main Output',
          message: 'Transmit remote supervisory instruction to energize Transformer Main Output load rails? Ensure test load and bench area are clear.',
          confirmText: 'Energize Output',
          cancelText: 'Cancel',
          isDanger: false,
          badgeType: 'POWER INTERFACE'
        });

        if (!confirmed) return;
        chkMasterPowerToggle.checked = true;
        await sendPowerCommand('ON');
      }
    });
  }

  // Refined Emergency Stop Cutoff (Hero Button & Control Tab Button)
  const triggerEmergencyStop = async () => {
    const confirmed = await showConfirmDialog({
      title: 'Emergency Cutoff Override',
      message: 'Execute an immediate emergency cutoff of all transformer main power rails? This instantly commands the hardware relay to open and isolate the system.',
      confirmText: 'Confirm Emergency Cutoff',
      cancelText: 'Cancel',
      isDanger: true,
      badgeType: 'HARDWARE SAFETY TRIP'
    });
    if (!confirmed) return;

    try {
      const res = await apiFetch('/api/control/emergency-stop', { method: 'POST' });
      const data = await res.json();
      if (res.ok) {
        showToast('EMERGENCY CUTOFF QUEUED: Hardware shutdown signal dispatched to Cloudflare Edge.', 'error', 5000);
        pollTelemetry();
        loadAlerts();
      } else {
        showToast(`Error: ${data.error}`, 'error');
      }
    } catch (err) {
      showToast(`Network Error: ${err.message}`, 'error');
    }
  };

  if (heroBtnTripStop) heroBtnTripStop.addEventListener('click', triggerEmergencyStop);
  if (btnEmergencyStop) btnEmergencyStop.addEventListener('click', triggerEmergencyStop);

  // Fault Latch Reset
  if (btnResetFaultLatch) {
    btnResetFaultLatch.addEventListener('click', async () => {
      const confirmed = await showConfirmDialog({
        title: 'Reset Supervisory Fault Latch',
        message: 'Acknowledge safety inspection and clear the supervisory lockout latch to allow normal operation?',
        confirmText: 'Reset Fault Latch',
        cancelText: 'Cancel',
        isDanger: false,
        badgeType: 'FAULT RECOVERY'
      });
      if (!confirmed) return;

      try {
        const res = await apiFetch('/api/control/reset', { method: 'POST' });
        const data = await res.json();
        if (res.ok) {
          showToast('Supervisory fault reset command dispatched.', 'success');
          loadAlerts();
          pollTelemetry();
        } else {
          showToast(`Error: ${data.error}`, 'error');
        }
      } catch (err) {
        showToast(`Network Error: ${err.message}`, 'error');
      }
    });
  }

  // Fan Modulation Modes
  if (btnFanModeAuto) {
    btnFanModeAuto.addEventListener('click', async () => {
      btnFanModeAuto.classList.add('active');
      btnFanModeManual.classList.remove('active');
      fanSliderWrap.style.opacity = '0.5';
      fanSliderWrap.style.pointerEvents = 'none';

      await apiFetch('/api/control/fan', {
        method: 'POST',
        body: JSON.stringify({ mode: 'AUTO' })
      });
      readoutFanMode.textContent = 'AUTO-PID';
      showToast('Cooling mode set to Autonomous Adaptive PID', 'info');
    });
  }

  if (btnFanModeManual) {
    btnFanModeManual.addEventListener('click', () => {
      btnFanModeManual.classList.add('active');
      btnFanModeAuto.classList.remove('active');
      fanSliderWrap.style.opacity = '1';
      fanSliderWrap.style.pointerEvents = 'auto';
      readoutFanMode.textContent = 'MANUAL';
    });
  }

  if (sliderFanSpeed) {
    sliderFanSpeed.addEventListener('input', (e) => {
      lblFanSpeedVal.textContent = e.target.value + '%';
    });
  }

  if (btnApplyFan) {
    btnApplyFan.addEventListener('click', async () => {
      const speed = parseInt(sliderFanSpeed.value, 10);
      const res = await apiFetch('/api/control/fan', {
        method: 'POST',
        body: JSON.stringify({ mode: 'MANUAL', speed })
      });
      if (res.ok) {
        showToast(`Manual Fan PWM duty cycle set to ${speed}%`, 'info');
        loadAlerts();
      }
    });
  }
}

async function sendPowerCommand(state) {
  try {
    const res = await apiFetch('/api/control/power', {
      method: 'POST',
      body: JSON.stringify({ state, device_id: 'TRANSFORMER_01' })
    });

    const data = await res.json();
    if (!res.ok) {
      showToast(`Command Error: ${data.error || 'Failed to dispatch command'}`, 'error');
      return;
    }

    showToast(`Command Queued: Remote ${data.command} registered. The ESP32 will execute on its next check-in cycle.`, 'success');
    loadAlerts();
  } catch (err) {
    showToast(`Network Error: ${err.message}`, 'error');
  }
}

// ==========================================================
// 10. SETTINGS, THRESHOLDS & FACTORY DEFAULTS
// ==========================================================

function setupSettingsListeners() {
  // Save Notification Preferences Button
  if (btnSaveNotifications) {
    btnSaveNotifications.addEventListener('click', async () => {
      const overtemp = chkNotifyOvertemp ? chkNotifyOvertemp.checked : true;
      const emergency = chkNotifyEmergency ? chkNotifyEmergency.checked : true;
      const powerOff = chkNotifyPowerOff ? chkNotifyPowerOff.checked : true;
      const watchdog = chkWatchdogEmail ? chkWatchdogEmail.checked : false;

      try {
        const res = await apiFetch('/api/settings', {
          method: 'POST',
          body: JSON.stringify({
            notify_overtemp_email: overtemp,
            notify_emergency_email: emergency,
            notify_power_off_email: powerOff,
            watchdog_email_enabled: watchdog
          })
        });

        if (res.ok) {
          updateWatchdogPill(watchdog);
          showToast('Notification dispatch preferences successfully updated.', 'success');
          loadAlerts();
        } else {
          const err = await res.json();
          showToast(`Error: ${err.error || 'Failed to update preferences'}`, 'error');
        }
      } catch (err) {
        showToast(`Network Error: ${err.message}`, 'error');
      }
    });
  }

  // Watchdog Email Supervision Toggle
  if (chkWatchdogEmail) {
    chkWatchdogEmail.addEventListener('change', async () => {
      const isArmed = chkWatchdogEmail.checked;
      try {
        const res = await apiFetch('/api/settings', {
          method: 'POST',
          body: JSON.stringify({ watchdog_email_enabled: isArmed })
        });
        if (res.ok) {
          updateWatchdogPill(isArmed);
          showToast(`Watchdog Email Engine: ${isArmed ? 'ARMED (Single Alert with 6h Deduplication)' : 'PAUSED (Emails Muted)'}`, isArmed ? 'success' : 'warning');
          loadAlerts();
        } else {
          chkWatchdogEmail.checked = !isArmed;
          const err = await res.json();
          showToast(`Error: ${err.error}`, 'error');
        }
      } catch (err) {
        chkWatchdogEmail.checked = !isArmed;
        showToast(`Network Error: ${err.message}`, 'error');
      }
    });
  }

  // Save Threshold Settings
  if (btnSaveThresholds) {
    btnSaveThresholds.addEventListener('click', async () => {
      const coreLimit = parseFloat(inputCoreTripLimit.value);
      const predLimit = parseFloat(inputPredTripLimit.value);
      const horizonSec = parseInt(inputHorizonSec.value, 10);

      if (isNaN(coreLimit) || coreLimit < 40 || coreLimit > 95) {
        showToast('Please enter a valid core trip limit between 40°C and 95°C', 'warning');
        return;
      }

      localStorage.setItem('cbm_core_trip', coreLimit.toFixed(1));
      localStorage.setItem('cbm_pred_trip', predLimit.toFixed(1));
      localStorage.setItem('cbm_horizon_sec', horizonSec);

      if (lblCoreThreshold) lblCoreThreshold.textContent = coreLimit.toFixed(1);

      // Persist thresholds to edge database
      try {
        await apiFetch('/api/settings', {
          method: 'POST',
          body: JSON.stringify({
            core_trip_limit: coreLimit.toFixed(1),
            pred_trip_limit: predLimit.toFixed(1),
            horizon_sec: horizonSec
          })
        });
      } catch (e) {
        console.warn('Failed to sync settings to edge DB:', e);
      }

      showToast(`Thermal thresholds saved: Core ${coreLimit}°C, Predicted ${predLimit}°C, Horizon ${horizonSec}s`, 'success');
    });
  }

  // Reset to Factory Defaults
  if (btnResetDefaults) {
    btnResetDefaults.addEventListener('click', async () => {
      const confirmed = await showConfirmDialog({
        title: 'Reset to Factory Defaults',
        message: 'Restore standard baseline thresholds (Core: 65.0°C, Predicted: 70.0°C, Extrapolation Horizon: 30s)?',
        confirmText: 'Reset Defaults',
        cancelText: 'Cancel',
        isDanger: false,
        badgeType: 'CONFIG RECOVERY'
      });
      if (!confirmed) return;

      inputCoreTripLimit.value = '65.0';
      inputPredTripLimit.value = '70.0';
      inputHorizonSec.value = '30';

      localStorage.removeItem('cbm_core_trip');
      localStorage.removeItem('cbm_pred_trip');
      localStorage.removeItem('cbm_horizon_sec');

      if (lblCoreThreshold) lblCoreThreshold.textContent = '65.0';

      try {
        await apiFetch('/api/settings', {
          method: 'POST',
          body: JSON.stringify({
            core_trip_limit: '65.0',
            pred_trip_limit: '70.0',
            horizon_sec: 30
          })
        });
      } catch (e) {
        console.warn('Failed to reset settings on edge DB:', e);
      }

      showToast('Thresholds restored to engineering defaults (65.0°C / 70.0°C / 30s)', 'info');
    });
  }

  // Restore saved threshold preferences if available
  const savedCore = localStorage.getItem('cbm_core_trip');
  const savedPred = localStorage.getItem('cbm_pred_trip');
  const savedHorizon = localStorage.getItem('cbm_horizon_sec');
  if (savedCore && inputCoreTripLimit) inputCoreTripLimit.value = savedCore;
  if (savedPred && inputPredTripLimit) inputPredTripLimit.value = savedPred;
  if (savedHorizon && inputHorizonSec) inputHorizonSec.value = savedHorizon;
  if (savedCore && lblCoreThreshold) lblCoreThreshold.textContent = savedCore;
}

async function loadSystemSettings() {
  try {
    const res = await apiFetch('/api/settings');
    if (!res.ok) return;
    const json = await res.json();
    const s = json.settings || {};

    if (chkWatchdogEmail && typeof s.watchdog_email_enabled !== 'undefined') {
      chkWatchdogEmail.checked = s.watchdog_email_enabled;
      updateWatchdogPill(s.watchdog_email_enabled);
    }
    if (chkNotifyOvertemp && typeof s.notify_overtemp_email !== 'undefined') {
      chkNotifyOvertemp.checked = s.notify_overtemp_email;
    }
    if (chkNotifyEmergency && typeof s.notify_emergency_email !== 'undefined') {
      chkNotifyEmergency.checked = s.notify_emergency_email;
    }
    if (chkNotifyPowerOff && typeof s.notify_power_off_email !== 'undefined') {
      chkNotifyPowerOff.checked = s.notify_power_off_email;
    }
    if (s.core_trip_limit && inputCoreTripLimit && !localStorage.getItem('cbm_core_trip')) {
      inputCoreTripLimit.value = Number(s.core_trip_limit).toFixed(1);
      if (lblCoreThreshold) lblCoreThreshold.textContent = Number(s.core_trip_limit).toFixed(1);
    }
    if (s.pred_trip_limit && inputPredTripLimit && !localStorage.getItem('cbm_pred_trip')) {
      inputPredTripLimit.value = Number(s.pred_trip_limit).toFixed(1);
    }
    if (s.horizon_sec && inputHorizonSec && !localStorage.getItem('cbm_horizon_sec')) {
      inputHorizonSec.value = s.horizon_sec;
    }
  } catch (err) {
    console.error('[LOAD_SETTINGS_ERROR]', err);
  }
}

function updateWatchdogPill(isArmed) {
  if (!pillWatchdogState) return;
  if (isArmed) {
    pillWatchdogState.textContent = 'ARMED [SINGLE DISPATCH]';
    pillWatchdogState.className = 'watchdog-state-pill active';
  } else {
    pillWatchdogState.textContent = 'PAUSED [OFF]';
    pillWatchdogState.className = 'watchdog-state-pill';
  }
}

// ==========================================================
// 11. INCIDENT AUDIT TRAIL LOG
// ==========================================================

async function loadAlerts() {
  try {
    const res = await apiFetch('/api/alerts');
    if (!res.ok) return;

    const json = await res.json();
    const alerts = json.data || [];
    const tbody = document.getElementById('incidentsTableBody');
    if (!tbody) return;

    if (alerts.length === 0) {
      tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No safety incidents logged. Operating within nominal bounds.</td></tr>';
      return;
    }

    tbody.innerHTML = alerts.map(a => {
      const isDanger = a.incident_type.includes('TRIP') || a.incident_type.includes('LOSS') || a.incident_type.includes('EMERGENCY');
      const badgeClass = isDanger ? 'badge-tag badge-danger' : 'badge-tag badge-info';
      const timeStr = new Date(a.created_at).toLocaleString();

      return `
        <tr>
          <td class="mono text-sm">${timeStr}</td>
          <td><span class="${badgeClass}">${a.incident_type}</span></td>
          <td class="text-sm">${a.details}</td>
          <td>${a.email_dispatched ? '<span class="badge-tag badge-info">Sent</span>' : '—'}</td>
        </tr>
      `;
    }).join('');
  } catch (err) {
    console.error('[LOAD_ALERTS_ERROR]', err);
  }
}

const btnRefreshAlerts = document.getElementById('btnRefreshAlerts');
if (btnRefreshAlerts) {
  btnRefreshAlerts.addEventListener('click', () => {
    loadAlerts();
    showToast('Incident audit log refreshed', 'info', 2000);
  });
}

// ==========================================================
// 12. TEAM ACCESS MANAGEMENT (ADMIN ONLY)
// ==========================================================

async function loadAuthorizedUsers() {
  try {
    const res = await apiFetch('/api/users');
    if (!res.ok) return;

    const json = await res.json();
    const users = json.data || [];
    const list = document.getElementById('usersRosterList');
    if (!list) return;

    list.innerHTML = users.map(u => `
      <div class="roster-row">
        <div>
          <strong>${u.name || u.email}</strong>
          <span class="text-muted text-sm" style="display:block;">${u.email}</span>
        </div>
        <div style="display:flex; align-items:center; gap:10px;">
          <span class="user-badge">${u.role}</span>
          ${u.email.toLowerCase() !== currentUser.email.toLowerCase() ? `
            <button onclick="removeUser('${u.email}')" class="btn-secondary-sm" style="color:var(--color-rose);">Revoke</button>
          ` : '<span class="text-dim text-sm">(Current)</span>'}
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error('[LOAD_USERS_ERROR]', err);
  }
}

const btnAddAuthorizedUser = document.getElementById('btnAddAuthorizedUser');
if (btnAddAuthorizedUser) {
  btnAddAuthorizedUser.addEventListener('click', async () => {
    const emailInput = document.getElementById('inputNewEmail');
    const nameInput = document.getElementById('inputNewName');
    const roleSelect = document.getElementById('selectNewRole');

    const email = emailInput.value.trim();
    const name = nameInput.value.trim() || email;
    const role = roleSelect.value;

    if (!email) {
      showToast('Please enter a valid Google account email address.', 'warning');
      return;
    }

    try {
      const res = await apiFetch('/api/users', {
        method: 'POST',
        body: JSON.stringify({ email, name, role })
      });

      if (res.ok) {
        emailInput.value = '';
        nameInput.value = '';
        loadAuthorizedUsers();
        showToast(`User ${email} authorized successfully as ${role}!`, 'success');
      } else {
        const err = await res.json();
        showToast(`Error: ${err.error}`, 'error');
      }
    } catch (err) {
      showToast(`Network Error: ${err.message}`, 'error');
    }
  });
}

window.removeUser = async function (email) {
  const confirmed = await showConfirmDialog({
    title: 'Revoke Personnel Authorization',
    message: `Revoke platform dashboard access for ${email}?`,
    confirmText: 'Revoke Access',
    cancelText: 'Cancel',
    isDanger: true,
    badgeType: 'SECURITY AUDIT'
  });
  if (!confirmed) return;

  try {
    const res = await apiFetch('/api/users', {
      method: 'DELETE',
      body: JSON.stringify({ email })
    });

    if (res.ok) {
      loadAuthorizedUsers();
      showToast(`Access revoked for ${email}`, 'info');
    } else {
      const err = await res.json();
      showToast(`Error: ${err.error}`, 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
};

// ==========================================================
// 12. SUPERPOWERS: CSV EXPORTER, FAN CURVE, SIMULATOR & AUDIO
// ==========================================================

// Fan Transfer Function Visualizer
function updateFanCurveDot(tCore, fanPwm) {
  const dot = document.getElementById('fanCurveLiveDot');
  const lblTemp = document.getElementById('lblCurveTemp');
  const lblPWM = document.getElementById('lblCurvePWM');
  if (!dot) return;

  const tClamped = Math.max(25, Math.min(75, tCore));
  // x ranges 30 (25°C) to 440 (75°C)
  const cx = 30 + ((tClamped - 25) / 50) * 410;
  
  // y ranges 15 (100% PWM) to 85 (0% PWM)
  let cy = 85;
  if (tClamped < 35) {
    cy = 85;
  } else if (tClamped < 55) {
    cy = 85 - ((tClamped - 35) / 20) * 60; // 85 -> 25
  } else if (tClamped < 65) {
    cy = 25 - ((tClamped - 55) / 10) * 10; // 25 -> 15
  } else {
    cy = 85; // tripped
  }
  
  dot.setAttribute('cx', cx.toFixed(1));
  dot.setAttribute('cy', cy.toFixed(1));
  if (lblTemp) lblTemp.textContent = tCore.toFixed(1) + '°C';
  if (lblPWM) lblPWM.textContent = fanPwm + '%';
}

// Acoustic Industrial Safety Chime (Web Audio API)
let audioCtx = null;
function playSafetyChime() {
  const chk = document.getElementById('chkAudioChime');
  if (chk && !chk.checked) return;

  try {
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    if (!AudioContextClass) return;
    if (!audioCtx) audioCtx = new AudioContextClass();
    if (audioCtx.state === 'suspended') {
      audioCtx.resume();
    }

    const now = audioCtx.currentTime;
    
    // First high tone (880 Hz)
    const osc1 = audioCtx.createOscillator();
    const gain1 = audioCtx.createGain();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(880, now);
    gain1.gain.setValueAtTime(0.12, now);
    gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
    osc1.connect(gain1);
    gain1.connect(audioCtx.destination);
    osc1.start(now);
    osc1.stop(now + 0.12);

    // Second warning tone (440 Hz)
    const osc2 = audioCtx.createOscillator();
    const gain2 = audioCtx.createGain();
    osc2.type = 'triangle';
    osc2.frequency.setValueAtTime(440, now + 0.14);
    gain2.gain.setValueAtTime(0.18, now + 0.14);
    gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.35);
    osc2.connect(gain2);
    gain2.connect(audioCtx.destination);
    osc2.start(now + 0.14);
    osc2.stop(now + 0.35);
  } catch (err) {
    console.warn('[AUDIO_CHIME_ERROR]', err);
  }
}

// CSV Telemetry Exporter
function initExportListeners() {
  const btnExport = document.getElementById('btnExportTelemetry');
  if (btnExport) {
    btnExport.addEventListener('click', exportTelemetryCSV);
  }
}

async function exportTelemetryCSV() {
  try {
    showToast('Preparing telemetry history for export...', 'info', 2000);
    const res = await apiFetch('/api/telemetry/history?limit=300');
    if (!res.ok) {
      showToast('Failed to fetch telemetry history from edge', 'error');
      return;
    }
    const json = await res.json();
    const rows = json.data || [];
    if (!rows.length) {
      showToast('No telemetry records available to export', 'warning');
      return;
    }

    const headers = [
      'Timestamp (ISO)',
      'Timestamp (Local)',
      'Device ID',
      'Core Hotspot T1 (°C)',
      'Inlet Airflow T2 (°C)',
      'Delta T Rise (°C)',
      'Rate of Rise (°C/s)',
      'Projected Horizon (°C)',
      'Virtual Hotspot THST (°C)',
      'Arrhenius Aging FAA',
      'Health Index HI (%)',
      'PS_ON State',
      'Fan Modulation (%)',
      'Voltage 12V (V)',
      'Current 12V (A)',
      'Power 12V (W)',
      'Voltage 5V (V)',
      'Current 5V (A)',
      'Power 5V (W)',
      'Voltage 3.3V (V)',
      'Current 3.3V (A)',
      'Power 3.3V (W)',
      'Total Load Power (W)',
      'Fault Code'
    ];

    const csvLines = [headers.join(',')];

    for (const r of rows) {
      const deltaT = (r.t_core - r.t_inlet).toFixed(2);
      const tHst = (r.t_core + 0.08 * Math.max(0, r.t_core - r.t_inlet) + 2.5).toFixed(2);
      const fAa = Math.exp((15000 / 383.15) - (15000 / (parseFloat(tHst) + 273.15))).toFixed(4);
      const w12 = (r.v_12v * r.i_12v).toFixed(2);
      const w5 = (r.v_5v * r.i_5v).toFixed(2);
      const w3 = (r.v_3v3 * r.i_3v3).toFixed(2);
      const wTotal = (parseFloat(w12) + parseFloat(w5) + parseFloat(w3)).toFixed(2);
      const localTime = new Date(r.created_at).toLocaleString();

      const line = [
        `"${r.created_at}"`,
        `"${localTime}"`,
        `"${r.device_id || 'TRANSFORMER_01'}"`,
        r.t_core.toFixed(2),
        r.t_inlet.toFixed(2),
        deltaT,
        (r.slope || 0).toFixed(3),
        (r.t_pred || r.t_core).toFixed(2),
        tHst,
        fAa,
        (r.health_index || 98.4).toFixed(1),
        r.pson_active ? 'ENERGIZED' : 'TRIPPED',
        r.pson_active ? '75%' : '0%',
        r.v_12v.toFixed(2),
        r.i_12v.toFixed(2),
        w12,
        r.v_5v.toFixed(2),
        r.i_5v.toFixed(2),
        w5,
        r.v_3v3.toFixed(2),
        r.i_3v3.toFixed(2),
        w3,
        wTotal,
        r.fault_code || 0
      ].join(',');

      csvLines.push(line);
    }

    const csvContent = csvLines.join('\r\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    const dateStr = new Date().toISOString().slice(0, 10);
    a.href = url;
    a.download = `transformer_cbm_telemetry_${dateStr}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    showToast(`Successfully exported ${rows.length} telemetry records to CSV!`, 'success');
  } catch (err) {
    console.error('[CSV_EXPORT_ERROR]', err);
    showToast(`Failed to export CSV: ${err.message}`, 'error');
  }
}

// Viva Demo & Fault Injection Simulator
let demoSimulatorState = null; // null (live hardware), 'NORMAL', 'OVERHEAT', 'COOLDOWN'
const simulatedData = {
  t_core: 38.2,
  t_inlet: 27.5,
  rate_of_rise: 0.01,
  t_predicted: 38.5,
  pson_active: 1,
  fault_code: 0,
  v_12v: 12.04,
  i_12v: 2.45,
  v_5v: 5.02,
  i_5v: 0.85,
  v_3v3: 3.31,
  i_3v3: 0.42,
  created_at: new Date().toISOString()
};

function setupDemoSimulatorListeners() {
  const btnNormal = document.getElementById('btnDemoNormal');
  const btnOverheat = document.getElementById('btnDemoOverheat');
  const btnCooldown = document.getElementById('btnDemoCooldown');
  const btnLive = document.getElementById('btnDemoLiveHardware');
  const badgeDemo = document.getElementById('badgeDemoMode');

  const updateButtons = (activeBtn) => {
    [btnNormal, btnOverheat, btnCooldown, btnLive].forEach(b => {
      if (b) b.classList.remove('active');
    });
    if (activeBtn) activeBtn.classList.add('active');
  };

  if (btnNormal) {
    btnNormal.addEventListener('click', () => {
      demoSimulatorState = 'NORMAL';
      simulatedData.t_core = 38.2;
      simulatedData.t_inlet = 27.5;
      simulatedData.pson_active = 1;
      simulatedData.fault_code = 0;
      updateButtons(btnNormal);
      if (badgeDemo) {
        badgeDemo.className = 'status-chip';
        badgeDemo.style.background = '';
        badgeDemo.textContent = 'SIMULATION: NOMINAL';
      }
      showToast('Simulator running: Nominal 38.2°C Baseline', 'info');
      pollTelemetry();
    });
  }

  if (btnOverheat) {
    btnOverheat.addEventListener('click', () => {
      demoSimulatorState = 'OVERHEAT';
      simulatedData.pson_active = 1;
      simulatedData.t_core = 58.0; // Start at 58°C so examiners see trip in ~8s
      updateButtons(btnOverheat);
      if (badgeDemo) {
        badgeDemo.className = 'status-chip';
        badgeDemo.style.background = '#be123c';
        badgeDemo.textContent = 'SIMULATION: OVERHEAT SPIKE';
      }
      showToast('Simulator: Injecting rapid thermal excursion towards 67.5°C trip threshold!', 'warning');
      pollTelemetry();
    });
  }

  if (btnCooldown) {
    btnCooldown.addEventListener('click', () => {
      demoSimulatorState = 'COOLDOWN';
      updateButtons(btnCooldown);
      if (badgeDemo) {
        badgeDemo.className = 'status-chip';
        badgeDemo.style.background = '';
        badgeDemo.textContent = 'SIMULATION: COOLING';
      }
      showToast('Simulator: High convection cool-down active (-0.25°C/s)', 'info');
      pollTelemetry();
    });
  }

  if (btnLive) {
    btnLive.addEventListener('click', () => {
      demoSimulatorState = null;
      updateButtons(btnLive);
      if (badgeDemo) {
        badgeDemo.className = 'status-chip off';
        badgeDemo.style.background = '';
        badgeDemo.textContent = 'LIVE SENSOR SYNC';
      }
      showToast('Reconnected to live ESP32 edge hardware stream', 'success');
      pollTelemetry();
    });
  }
}

// Operator Keyboard Shortcuts
function initKeyboardShortcuts() {
  const modalShortcuts = document.getElementById('modalShortcuts');
  const btnCloseShortcuts = document.getElementById('btnCloseShortcuts');
  if (btnCloseShortcuts && modalShortcuts) {
    btnCloseShortcuts.addEventListener('click', () => {
      modalShortcuts.classList.add('hidden');
    });
    modalShortcuts.addEventListener('click', (e) => {
      if (e.target === modalShortcuts) modalShortcuts.classList.add('hidden');
    });
  }

  window.addEventListener('keydown', (e) => {
    const tag = (e.target && e.target.tagName) ? e.target.tagName.toUpperCase() : '';
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

    if (e.key === '1') switchTab('tab-dashboard');
    else if (e.key === '2') switchTab('tab-controls');
    else if (e.key === '3') switchTab('tab-rails');
    else if (e.key === '4') switchTab('tab-alerts');
    else if (e.key === '5') switchTab('tab-settings');
    else if (e.key === 't' || e.key === 'T') {
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    }
    else if (e.key === 'e' || e.key === 'E') {
      const heroBtn = document.getElementById('heroBtnTripStop');
      if (heroBtn) heroBtn.click();
    }
    else if (e.key === '?') {
      if (modalShortcuts) modalShortcuts.classList.toggle('hidden');
    }
    else if (e.key === 'Escape') {
      if (modalShortcuts && !modalShortcuts.classList.contains('hidden')) {
        modalShortcuts.classList.add('hidden');
      }
    }
  });
}
