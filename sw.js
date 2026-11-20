// Cache-first for video segments (they never change), network-first for everything else.
const CACHE = "route-guide-v1";
const MAX_SEGMENTS = 400; // roughly 25 minutes of 1080p, about 400 MB

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", e => e.waitUntil(
  caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim())
));

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  if (url.pathname.endsWith(".ts")) e.respondWith(segment(e.request));
});

async function segment(req) {
  const cache = await caches.open(CACHE);
  const hit = await cache.match(req);
  if (hit) return hit;
  const res = await fetch(req);
  if (res.ok) {
    cache.put(req, res.clone()).then(trim).catch(() => {});
  }
  return res;
}

async function trim() {
  const cache = await caches.open(CACHE);
  const keys = await cache.keys();
  for (let i = 0; i < keys.length - MAX_SEGMENTS; i++) await cache.delete(keys[i]);
}
