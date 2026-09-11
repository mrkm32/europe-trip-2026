// Service Worker for Europe Alps Odyssey 2026
// Enables 100% Offline Access across Alpine valleys, trains, and mountain passes
const CACHE_NAME = 'europe-alps-2026-v14';

const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './apple-touch-icon.png',
  './icon-192.png',
  './icon-512.png',
  './hero.jpg',
  './alps_map.jpg',
  'https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js',
  './documents/trains/shared/00_Munich_to_Salzburg_Train_Tickets_Shared.pdf',
  './documents/trains/shared/Innsbruck_to_Bolzano_Train_Details.png',
  './documents/trains/shared/Salzburg_to_Innsbruck_WESTbahn_Tickets_Shared.pdf',
  './documents/trains/rowe/01_Innsbruck_to_Bolzano_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/01_Innsbruck_to_Bolzano_Train_Tickets_Matthews.pdf',
  './documents/trains/matthews/02_Venice_SL_to_Mestre_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/02_Venice_SL_to_Mestre_Train_Tickets_Rowe.pdf',
  './documents/trains/rowe/03_Venice_Mestre_to_Tirano_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/03_Venice_Mestre_to_Tirano_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe.pdf',
  './documents/trains/matthews/04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews.pdf',
  './documents/trains/rowe/05_St_Moritz_to_Chur_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/05_St_Moritz_to_Chur_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/06_Chur_to_Andermatt_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/06_Chur_to_Andermatt_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/07_Andermatt_to_Zermatt_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/07_Andermatt_to_Zermatt_Train_Tickets_Matthews.pdf',
  './documents/trains/shared/Zermatt_to_Gornergrat_Train_Schedule.pdf',
  './documents/trains/rowe/08_Zermatt_to_Geneva_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/08_Zermatt_to_Geneva_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/09_Geneva_to_Airport_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/09_Geneva_to_Airport_Train_Tickets_Matthews.pdf',
  './documents/rendered/trains/matthews/01_Innsbruck_to_Bolzano_Train_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/01_Innsbruck_to_Bolzano_Train_Tickets_Matthews/page-2.png',
  './documents/rendered/trains/matthews/01_Innsbruck_to_Bolzano_Train_Tickets_Matthews/page-3.png',
  './documents/rendered/trains/matthews/02_Venice_SL_to_Mestre_Train_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/03_Venice_Mestre_to_Tirano_Train_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews/page-2.png',
  './documents/rendered/trains/matthews/04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews/page-3.png',
  './documents/rendered/trains/matthews/04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews/page-4.png',
  './documents/rendered/trains/matthews/05_St_Moritz_to_Chur_Train_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/05_St_Moritz_to_Chur_Train_Tickets_Matthews/page-2.png',
  './documents/rendered/trains/matthews/06_Chur_to_Andermatt_Train_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/06_Chur_to_Andermatt_Train_Tickets_Matthews/page-2.png',
  './documents/rendered/trains/matthews/07_Andermatt_to_Zermatt_Train_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/07_Andermatt_to_Zermatt_Train_Tickets_Matthews/page-2.png',
  './documents/rendered/trains/matthews/08_Zermatt_to_Geneva_Train_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/08_Zermatt_to_Geneva_Train_Tickets_Matthews/page-2.png',
  './documents/rendered/trains/matthews/09_Geneva_to_Airport_Train_Tickets_Matthews/page-1.png',
  './documents/rendered/trains/matthews/09_Geneva_to_Airport_Train_Tickets_Matthews/page-2.png',
  './documents/rendered/trains/rowe/01_Innsbruck_to_Bolzano_Train_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/01_Innsbruck_to_Bolzano_Train_Tickets_Rowe/page-2.png',
  './documents/rendered/trains/rowe/01_Innsbruck_to_Bolzano_Train_Tickets_Rowe/page-3.png',
  './documents/rendered/trains/rowe/02_Venice_SL_to_Mestre_Train_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/03_Venice_Mestre_to_Tirano_Train_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe/page-2.png',
  './documents/rendered/trains/rowe/04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe/page-3.png',
  './documents/rendered/trains/rowe/04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe/page-4.png',
  './documents/rendered/trains/rowe/05_St_Moritz_to_Chur_Train_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/05_St_Moritz_to_Chur_Train_Tickets_Rowe/page-2.png',
  './documents/rendered/trains/rowe/05_St_Moritz_to_Chur_Train_Tickets_Rowe/page-3.png',
  './documents/rendered/trains/rowe/06_Chur_to_Andermatt_Train_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/06_Chur_to_Andermatt_Train_Tickets_Rowe/page-2.png',
  './documents/rendered/trains/rowe/07_Andermatt_to_Zermatt_Train_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/07_Andermatt_to_Zermatt_Train_Tickets_Rowe/page-2.png',
  './documents/rendered/trains/rowe/07_Andermatt_to_Zermatt_Train_Tickets_Rowe/page-3.png',
  './documents/rendered/trains/rowe/08_Zermatt_to_Geneva_Train_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/08_Zermatt_to_Geneva_Train_Tickets_Rowe/page-2.png',
  './documents/rendered/trains/rowe/09_Geneva_to_Airport_Train_Tickets_Rowe/page-1.png',
  './documents/rendered/trains/rowe/09_Geneva_to_Airport_Train_Tickets_Rowe/page-2.png',
  './documents/rendered/trains/shared/00_Munich_to_Salzburg_Train_Tickets_Shared/page-1.png',
  './documents/rendered/trains/shared/Salzburg_to_Innsbruck_WESTbahn_Tickets_Shared/page-1.png',
  './documents/rendered/trains/shared/Salzburg_to_Innsbruck_WESTbahn_Tickets_Shared/page-2.png',
  './documents/rendered/trains/shared/Salzburg_to_Innsbruck_WESTbahn_Tickets_Shared/page-3.png',
  './documents/rendered/trains/shared/Salzburg_to_Innsbruck_WESTbahn_Tickets_Shared/page-4.png',
  './documents/rendered/trains/shared/Zermatt_to_Gornergrat_Train_Schedule/page-1.png'
];

// Install: Cache essential application assets & pre-rendered train ticket pages
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(
        PRECACHE_URLS.map((url) =>
          cache.add(url).catch((err) => {
            console.warn('Pre-caching asset:', url, err);
          })
        )
      );
    }).then(() => self.skipWaiting())
  );
});

// Activate: Purge older cache versions immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Cache-First for instant offline performance, Network Fallback with automatic caching
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      if (cachedResponse) {
        return cachedResponse;
      }
      return fetch(event.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      }).catch(() => {
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
        return caches.match(event.request);
      });
    })
  );
});
