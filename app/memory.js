const DB_NAME = 'universe_memory';
const DB_VERSION = 2;

const STORE_DEFINITIONS = {
  observer_profile: {
    options: { keyPath: 'id' },
    indexes: [
      ['updatedAt', 'updatedAt'],
      ['name', 'name'],
    ],
  },
  system_events: {
    options: { keyPath: 'id', autoIncrement: true },
    indexes: [
      ['eventType', 'eventType'],
      ['moduleId', 'moduleId'],
      ['createdAt', 'createdAt'],
    ],
  },
  dream_entries: {
    options: { keyPath: 'id', autoIncrement: true },
    indexes: [
      ['createdAt', 'createdAt'],
      ['tag', 'tag', { multiEntry: true }],
    ],
  },
  intelligence_notes: {
    options: { keyPath: 'id', autoIncrement: true },
    indexes: [
      ['subject', 'subject'],
      ['createdAt', 'createdAt'],
    ],
  },
  counseling_records: {
    options: { keyPath: 'id', autoIncrement: true },
    indexes: [
      ['observerId', 'observerId'],
      ['createdAt', 'createdAt'],
    ],
  },
  module_state: {
    options: { keyPath: 'id', autoIncrement: true },
    indexes: [
      ['moduleId', 'moduleId'],
      ['updatedAt', 'updatedAt'],
      ['stateType', 'stateType'],
    ],
  },
};

let dbPromise;

function ensureIndexedDb() {
  if (!globalThis.indexedDB) {
    throw new Error('IndexedDB is not available in this environment.');
  }
}

function createStoreIfMissing(db, storeName, definition) {
  if (db.objectStoreNames.contains(storeName)) {
    return;
  }

  const objectStore = db.createObjectStore(storeName, definition.options);
  for (const [indexName, keyPath, options] of definition.indexes) {
    objectStore.createIndex(indexName, keyPath, options);
  }
}

function applyVersion1Schema(db) {
  for (const [storeName, definition] of Object.entries(STORE_DEFINITIONS)) {
    createStoreIfMissing(db, storeName, definition);
  }
}

function applyVersion2Schema(db, tx) {
  // Ensure base stores exist in case of fresh install directly at version 2.
  applyVersion1Schema(db);

  // Add index to quickly query snapshots by recency.
  if (db.objectStoreNames.contains('module_state')) {
    const stateStore = tx.objectStore('module_state');
    if (!stateStore.indexNames.contains('isSnapshot')) {
      stateStore.createIndex('isSnapshot', 'isSnapshot');
    }
  }
}

const MIGRATIONS = {
  1: applyVersion1Schema,
  2: applyVersion2Schema,
};

export function initializeMemory() {
  ensureIndexedDb();

  if (!dbPromise) {
    dbPromise = new Promise((resolve, reject) => {
      const openRequest = indexedDB.open(DB_NAME, DB_VERSION);

      openRequest.onerror = () => reject(openRequest.error);
      openRequest.onblocked = () => {
        console.warn('Universe memory upgrade is blocked by another tab.');
      };

      openRequest.onupgradeneeded = (event) => {
        const db = openRequest.result;
        const tx = openRequest.transaction;
        const fromVersion = event.oldVersion;

        for (let version = fromVersion + 1; version <= DB_VERSION; version += 1) {
          const migration = MIGRATIONS[version];
          if (migration) {
            migration(db, tx);
          }
        }
      };

      openRequest.onsuccess = () => resolve(openRequest.result);
    });
  }

  return dbPromise;
}

function completeRequest(request) {
  return new Promise((resolve, reject) => {
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

function completeTransaction(tx) {
  return new Promise((resolve, reject) => {
    tx.oncomplete = () => resolve();
    tx.onerror = () => reject(tx.error);
    tx.onabort = () => reject(tx.error || new Error('Transaction aborted.'));
  });
}

async function withStore(storeName, mode, callback) {
  const db = await initializeMemory();

  if (!db.objectStoreNames.contains(storeName)) {
    throw new Error(`Unknown store: ${storeName}`);
  }

  const tx = db.transaction(storeName, mode);
  const store = tx.objectStore(storeName);
  const result = await callback(store, tx);
  await completeTransaction(tx);
  return result;
}

function normalizeRecord(value) {
  const now = new Date().toISOString();
  return {
    ...value,
    updatedAt: value?.updatedAt ?? now,
    createdAt: value?.createdAt ?? now,
  };
}

export async function putRecord(store, value) {
  if (!value || typeof value !== 'object') {
    throw new Error('putRecord requires a plain object value.');
  }

  const record = normalizeRecord(value);

  return withStore(store, 'readwrite', async (objectStore) => {
    const request = objectStore.put(record);
    return completeRequest(request);
  });
}

function applyQueryRange(indexOrStore, queryOptions = {}) {
  const { range, only, lowerBound, upperBound, lowerOpen = false, upperOpen = false } = queryOptions;

  if (range) {
    return range;
  }

  if (only !== undefined) {
    return IDBKeyRange.only(only);
  }

  if (lowerBound !== undefined && upperBound !== undefined) {
    return IDBKeyRange.bound(lowerBound, upperBound, lowerOpen, upperOpen);
  }

  if (lowerBound !== undefined) {
    return IDBKeyRange.lowerBound(lowerBound, lowerOpen);
  }

  if (upperBound !== undefined) {
    return IDBKeyRange.upperBound(upperBound, upperOpen);
  }

  return undefined;
}

export async function listRecords(store, queryOptions = {}) {
  const {
    index,
    direction = 'next',
    limit = Infinity,
    offset = 0,
  } = queryOptions;

  return withStore(store, 'readonly', (objectStore) => new Promise((resolve, reject) => {
    const source = index ? objectStore.index(index) : objectStore;
    const keyRange = applyQueryRange(source, queryOptions);
    const results = [];
    let skipped = 0;

    const request = source.openCursor(keyRange, direction);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => {
      const cursor = request.result;
      if (!cursor || results.length >= limit) {
        resolve(results);
        return;
      }

      if (skipped < offset) {
        skipped += 1;
        cursor.continue();
        return;
      }

      results.push(cursor.value);
      cursor.continue();
    };
  }));
}

export async function getLatestState() {
  const snapshots = await listRecords('module_state', {
    index: 'updatedAt',
    direction: 'prev',
    limit: 1,
  });

  return snapshots[0] ?? null;
}

export async function saveSystemSnapshot(snapshot) {
  const normalizedSnapshot = normalizeRecord({
    ...snapshot,
    isSnapshot: true,
    stateType: snapshot?.stateType ?? 'system_snapshot',
  });

  const [stateId] = await Promise.all([
    putRecord('module_state', normalizedSnapshot),
    putRecord('system_events', {
      eventType: 'system_snapshot_saved',
      moduleId: snapshot?.moduleId ?? 'system',
      payload: snapshot,
      createdAt: normalizedSnapshot.createdAt,
    }),
  ]);

  return stateId;
}

export const MEMORY_STORES = Object.freeze(Object.keys(STORE_DEFINITIONS));
