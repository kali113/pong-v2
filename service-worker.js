// Service Worker for Pong AI v2
// Caches Python runtime and dependencies for faster subsequent loads

const CACHE_NAME = 'pong-ai-v2-cache-v1';
const RUNTIME_CACHE = 'pong-runtime-cache-v1';

// Resources to cache immediately on install
const PRECACHE_URLS = [
    '/pong-v2/',
    '/pong-v2/index.html',
    '/pong-v2/game/',
    '/pong-v2/game/index.html',
    '/pong-v2/game/favicon.png'
];

// Large runtime files to cache after first load
const RUNTIME_URLS = [
    'https://pygame-web.github.io/archives/0.9/pythons.js',
    'https://pygame-web.github.io/archives/0.9/cpython312/main.js',
    'https://pygame-web.github.io/archives/0.9/cpython312/main.data',
    'https://pygame-web.github.io/archives/0.9/cpython312/main.wasm'
];

// Install event - cache essential files
self.addEventListener('install', (event) => {
    console.log('[ServiceWorker] Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('[ServiceWorker] Precaching app shell');
            return cache.addAll(PRECACHE_URLS);
        })
    );
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('[ServiceWorker] Activating...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
                        console.log('[ServiceWorker] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    return self.clients.claim();
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    
    // Skip chrome-extension and other non-http requests
    if (!url.protocol.startsWith('http')) {
        return;
    }

    // Strategy: Cache First for Python runtime files (they're large and static)
    if (url.hostname === 'pygame-web.github.io') {
        event.respondWith(
            caches.open(RUNTIME_CACHE).then((cache) => {
                return cache.match(event.request).then((response) => {
                    if (response) {
                        console.log('[ServiceWorker] Serving from cache:', url.pathname);
                        return response;
                    }
                    
                    console.log('[ServiceWorker] Fetching and caching:', url.pathname);
                    return fetch(event.request).then((networkResponse) => {
                        // Cache successful responses
                        if (networkResponse && networkResponse.status === 200) {
                            cache.put(event.request, networkResponse.clone());
                        }
                        return networkResponse;
                    });
                });
            })
        );
        return;
    }

    // Strategy: Network First for APK and game files (they may update)
    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // Cache successful responses
                if (response && response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, responseClone);
                    });
                }
                return response;
            })
            .catch(() => {
                // Fallback to cache if network fails
                return caches.match(event.request);
            })
    );
});

// Background sync for future PWA features
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-game-state') {
        console.log('[ServiceWorker] Background sync triggered');
        // Future: Sync multiplayer game state
    }
});

// Push notifications for future features
self.addEventListener('push', (event) => {
    const options = {
        body: event.data ? event.data.text() : 'New update available!',
        icon: '/pong-v2/game/favicon.png',
        badge: '/pong-v2/game/favicon.png'
    };
    
    event.waitUntil(
        self.registration.showNotification('Pong AI v2', options)
    );
});
