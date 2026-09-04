// Service Worker for Europe Alps Odyssey 2026
// Enables 100% Offline Access across Alpine valleys, trains, and mountain passes
const CACHE_NAME = 'europe-alps-2026-v4';

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
  "./documents/guides_support/On_Trip_Support_Overview_IBTO.pdf",
  "./documents/trains/shared/Innsbruck_to_Bolzano_Train_Details.png",
  "./documents/trains/rowe/01_Innsbruck_to_Bolzano_Train_Tickets_Rowe.pdf",
  "./documents/trains/matthews/01_Innsbruck_to_Bolzano_Train_Tickets_Matthews.pdf",
  "./documents/rental_car/Car_Rental_Confirmation_Rowe.pdf",
  "./documents/rental_car/Car_Rental_Voucher_Rowe.pdf",
  "./documents/rental_car/IBTO_Driving_in_Italy_Ebook.pdf",
  "./documents/lodging/Hotel_Rezia_Confirmation_Rowe.pdf",
  "./documents/lodging/Hotel_Rezia_Confirmation_Matthews.pdf",
  "./documents/tours_excursions/Dolomites_Cable_Car_Prices_Schedule_Boe.pdf",
  "./documents/tours_excursions/Dolomites_La_Crusc_Lift_Prices.png",
  "./documents/lodging/BB_Fortuny_Arrival_Map.pdf",
  "./documents/lodging/BB_Fortuny_Confirmation_Rowe.pdf",
  "./documents/lodging/BB_Fortuny_Confirmation_Matthews.pdf",
  "./documents/tours_excursions/Venice_Tours_Payment_Rowe.pdf",
  "./documents/tours_excursions/Venice_Tours_Payment_Matthews.pdf",
  "./documents/trains/matthews/02_Venice_SL_to_Mestre_Train_Tickets_Matthews.pdf",
  "./documents/trains/rowe/02_Venice_SL_to_Mestre_Train_Tickets_Rowe.pdf",
  "./documents/trains/rowe/03_Venice_Mestre_to_Tirano_Train_Tickets_Rowe.pdf",
  "./documents/trains/matthews/03_Venice_Mestre_to_Tirano_Train_Tickets_Matthews.pdf",
  "./documents/trains/rowe/04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe.pdf",
  "./documents/trains/matthews/04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews.pdf",
  "./documents/lodging/Hotel_Arte_St_Moritz_Confirmation_Rowe.pdf",
  "./documents/lodging/Hotel_Arte_St_Moritz_Confirmation_Matthews.pdf",
  "./documents/trains/rowe/05_St_Moritz_to_Chur_Train_Tickets_Rowe.pdf",
  "./documents/trains/matthews/05_St_Moritz_to_Chur_Train_Tickets_Matthews.pdf",
  "./documents/trains/rowe/06_Chur_to_Andermatt_Train_Tickets_Rowe.pdf",
  "./documents/trains/matthews/06_Chur_to_Andermatt_Train_Tickets_Matthews.pdf",
  "./documents/trains/rowe/07_Andermatt_to_Zermatt_Train_Tickets_Rowe.pdf",
  "./documents/trains/matthews/07_Andermatt_to_Zermatt_Train_Tickets_Matthews.pdf",
  "./documents/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Rowe.pdf",
  "./documents/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Matthews.pdf",
  "./documents/trains/shared/Zermatt_to_Gornergrat_Train_Schedule.pdf",
  "./documents/trains/rowe/08_Zermatt_to_Geneva_Train_Tickets_Rowe.pdf",
  "./documents/trains/matthews/08_Zermatt_to_Geneva_Train_Tickets_Matthews.pdf",
  "./documents/lodging/The_New_Midi_Geneva_Confirmation_Rowe.pdf",
  "./documents/lodging/The_New_Midi_Geneva_Confirmation_Matthews.pdf",
  "./documents/trains/rowe/09_Geneva_to_Airport_Train_Tickets_Rowe.pdf",
  "./documents/trains/matthews/09_Geneva_to_Airport_Train_Tickets_Matthews.pdf",
];

// Install: Cache essential application assets immediately
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS).catch((err) => {
        console.warn('Pre-caching non-fatal asset warning:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate: Purge older cache versions
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

// Fetch: Network-First with Cache Fallback
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });
      })
  );
});
