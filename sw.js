const APP_VERSION = 'homehub-core-v1.0.0';
const PRECACHE = `precache-${APP_VERSION}`;
const RUNTIME = `runtime-${APP_VERSION}`;

const APP_SHELL_ASSETS = [
  '/',
  '/index.html',
  '/manifest.webmanifest',
  '/sw.js'
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(PRECACHE);
    const failures = [];

    await Promise.all(APP_SHELL_ASSETS.map(async (asset) => {
      try {
        const response = await fetch(asset, { cache: 'no-store' });
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        await cache.put(asset, response.clone());
      } catch (error) {
        failures.push({ asset, reason: error.message });
      }
    }));

    if (failures.length > 0) {
      const details = failures
        .map(({ asset, reason }) => `${asset} (${reason})`)
        .join(', ');
      throw new Error(`Service worker precache failed: ${details}`);
    }

    self.skipWaiting();
  })());
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter((key) => key !== PRECACHE && key !== RUNTIME)
        .map((key) => caches.delete(key))
    );

    await self.clients.claim();

    const clients = await self.clients.matchAll({ includeUncontrolled: true, type: 'window' });
    clients.forEach((client) => {
      client.postMessage({
        type: 'SW_UPDATED',
        version: APP_VERSION,
        message: 'HomeHub Core is updated and ready.'
      });
    });
  })());
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') {
    return;
  }

  const requestUrl = new URL(request.url);

  if (request.mode === 'navigate') {
    event.respondWith((async () => {
      try {
        const networkResponse = await fetch(request);
        const runtimeCache = await caches.open(RUNTIME);
        runtimeCache.put(request, networkResponse.clone());
        return networkResponse;
      } catch {
        const cachedIndex = await caches.match('/index.html');
        if (cachedIndex) {
          return cachedIndex;
        }
        return new Response('Offline', {
          status: 503,
          headers: { 'Content-Type': 'text/plain' }
        });
      }
    })());
    return;
  }

  const isSameOrigin = requestUrl.origin === self.location.origin;
  const isAppShellAsset = isSameOrigin && APP_SHELL_ASSETS.includes(requestUrl.pathname);

  if (isAppShellAsset) {
    event.respondWith((async () => {
      const cached = await caches.match(request);
      if (cached) {
        return cached;
      }
      const response = await fetch(request);
      const cache = await caches.open(PRECACHE);
      cache.put(request, response.clone());
      return response;
    })());
    return;
  }

  event.respondWith((async () => {
    const runtimeCache = await caches.open(RUNTIME);
    try {
      const networkResponse = await fetch(request);
      runtimeCache.put(request, networkResponse.clone());
      return networkResponse;
    } catch {
      const cached = await runtimeCache.match(request);
      if (cached) {
        return cached;
      }
      return fetch(request);
    }
  })());
});
