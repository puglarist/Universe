const DB_NAME = 'universe-observer';
const DB_VERSION = 1;
const STORE_NAME = 'identity';
const PROFILE_KEY = 'observer-profile';

const elements = {
  identitySummary: document.getElementById('identitySummary'),
  observerIdValue: document.getElementById('observerIdValue'),
  lastSeenValue: document.getElementById('lastSeenValue'),
  resumeValue: document.getElementById('resumeValue'),
  menuToggle: document.getElementById('menuToggle'),
  menuPanel: document.getElementById('menuPanel'),
  form: document.getElementById('preferencesForm'),
  displayName: document.getElementById('displayName'),
  preferredModule: document.getElementById('preferredModule'),
  compactMode: document.getElementById('compactMode'),
  highContrast: document.getElementById('highContrast'),
  showHints: document.getElementById('showHints'),
  statusText: document.getElementById('statusText')
};

let db;
let identityState;

function openDb() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onupgradeneeded = () => {
      const upgradeDb = request.result;
      if (!upgradeDb.objectStoreNames.contains(STORE_NAME)) {
        upgradeDb.createObjectStore(STORE_NAME, { keyPath: 'id' });
      }
    };

    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

function readProfile() {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readonly');
    const store = tx.objectStore(STORE_NAME);
    const request = store.get(PROFILE_KEY);
    request.onsuccess = () => resolve(request.result?.value ?? null);
    request.onerror = () => reject(request.error);
  });
}

function writeProfile(profile) {
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE_NAME, 'readwrite');
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
    const store = tx.objectStore(STORE_NAME);
    store.put({ id: PROFILE_KEY, value: profile });
  });
}

function stableObserverId() {
  if (crypto.randomUUID) {
    return `observer-${crypto.randomUUID()}`;
  }

  const bytes = new Uint8Array(16);
  crypto.getRandomValues(bytes);
  return `observer-${Array.from(bytes, (b) => b.toString(16).padStart(2, '0')).join('')}`;
}

function defaultProfile(nowIso) {
  return {
    observerId: stableObserverId(),
    displayName: 'Observer',
    lastSeenAt: nowIso,
    appResumeAt: nowIso,
    preferences: {
      preferredModule: 'navigation',
      ui: {
        compactMode: false,
        highContrast: false,
        showHints: true
      }
    }
  };
}

function formatDate(iso) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short'
  }).format(new Date(iso));
}

function applyUiPreferences() {
  document.body.classList.toggle('compact', identityState.preferences.ui.compactMode);
  document.body.classList.toggle('high-contrast', identityState.preferences.ui.highContrast);
}

function renderProfile() {
  applyUiPreferences();
  elements.identitySummary.textContent = `${identityState.displayName} (${identityState.observerId}) • Preferred module: ${identityState.preferences.preferredModule}`;
  elements.observerIdValue.textContent = identityState.observerId;
  elements.lastSeenValue.textContent = formatDate(identityState.lastSeenAt);
  elements.resumeValue.textContent = formatDate(identityState.appResumeAt);

  elements.displayName.value = identityState.displayName;
  elements.preferredModule.value = identityState.preferences.preferredModule;
  elements.compactMode.checked = identityState.preferences.ui.compactMode;
  elements.highContrast.checked = identityState.preferences.ui.highContrast;
  elements.showHints.checked = identityState.preferences.ui.showHints;
}

async function persistAndRender(statusMessage) {
  await writeProfile(identityState);
  renderProfile();
  elements.statusText.textContent = statusMessage;
  setTimeout(() => {
    if (elements.statusText.textContent === statusMessage) {
      elements.statusText.textContent = '';
    }
  }, 1500);
}

function bindEvents() {
  elements.menuToggle.addEventListener('click', () => {
    const isHidden = elements.menuPanel.hidden;
    elements.menuPanel.hidden = !isHidden;
    elements.menuToggle.setAttribute('aria-expanded', String(isHidden));
  });

  elements.form.addEventListener('input', async () => {
    identityState.displayName = elements.displayName.value.trim() || 'Observer';
    identityState.preferences.preferredModule = elements.preferredModule.value;
    identityState.preferences.ui.compactMode = elements.compactMode.checked;
    identityState.preferences.ui.highContrast = elements.highContrast.checked;
    identityState.preferences.ui.showHints = elements.showHints.checked;
    await persistAndRender('Preferences saved');
  });
}

async function initialize() {
  db = await openDb();
  const nowIso = new Date().toISOString();
  const stored = await readProfile();

  if (!stored) {
    identityState = defaultProfile(nowIso);
  } else {
    identityState = {
      ...stored,
      appResumeAt: nowIso,
      lastSeenAt: nowIso,
      preferences: {
        ...stored.preferences,
        ui: {
          compactMode: false,
          highContrast: false,
          showHints: true,
          ...stored.preferences?.ui
        }
      }
    };
  }

  await writeProfile(identityState);
  renderProfile();
  bindEvents();
}

initialize().catch((error) => {
  console.error(error);
  elements.identitySummary.textContent = 'Unable to initialize observer profile.';
});
