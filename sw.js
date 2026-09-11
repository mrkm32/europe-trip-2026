// Service Worker for Europe Alps Odyssey 2026
// Enables 100% Offline Access across Alpine valleys, trains, and mountain passes
const CACHE_NAME = 'europe-alps-2026-v12';

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
  './documents/guides_support/On_Trip_Support_Overview_IBTO.pdf',
  './documents/trains/shared/00_Munich_to_Salzburg_Train_Tickets_Shared.pdf',
  './documents/trains/shared/Innsbruck_to_Bolzano_Train_Details.png',
  './documents/trains/shared/Salzburg_to_Innsbruck_WESTbahn_Tickets_Shared.pdf',
  './documents/trains/rowe/01_Innsbruck_to_Bolzano_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/01_Innsbruck_to_Bolzano_Train_Tickets_Matthews.pdf',
  './documents/rental_car/Car_Rental_Confirmation_Rowe.pdf',
  './documents/rental_car/Car_Rental_Voucher_Rowe.pdf',
  './documents/rental_car/IBTO_Driving_in_Italy_Ebook.pdf',
  './documents/lodging/Hotel_Rezia_Confirmation_Rowe.pdf',
  './documents/lodging/Hotel_Rezia_Confirmation_Matthews.pdf',
  './documents/tours_excursions/Dolomites_Cable_Car_Prices_Schedule_Boe.pdf',
  './documents/tours_excursions/Dolomites_La_Crusc_Lift_Prices.png',
  './documents/lodging/BB_Fortuny_Arrival_Map.pdf',
  './documents/lodging/BB_Fortuny_Confirmation_Rowe.pdf',
  './documents/lodging/BB_Fortuny_Confirmation_Matthews.pdf',
  './documents/tours_excursions/Venice_Tours_Payment_Rowe.pdf',
  './documents/tours_excursions/Venice_Tours_Payment_Matthews.pdf',
  './documents/tours_excursions/Salzburg_Sound_of_Music_Hallstatt_Tour_Viator.pdf',
  './documents/trains/matthews/02_Venice_SL_to_Mestre_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/02_Venice_SL_to_Mestre_Train_Tickets_Rowe.pdf',
  './documents/trains/rowe/03_Venice_Mestre_to_Tirano_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/03_Venice_Mestre_to_Tirano_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe.pdf',
  './documents/trains/matthews/04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews.pdf',
  './documents/lodging/Hotel_Arte_St_Moritz_Confirmation_Rowe.pdf',
  './documents/lodging/Hotel_Arte_St_Moritz_Confirmation_Matthews.pdf',
  './documents/trains/rowe/05_St_Moritz_to_Chur_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/05_St_Moritz_to_Chur_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/06_Chur_to_Andermatt_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/06_Chur_to_Andermatt_Train_Tickets_Matthews.pdf',
  './documents/trains/rowe/07_Andermatt_to_Zermatt_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/07_Andermatt_to_Zermatt_Train_Tickets_Matthews.pdf',
  './documents/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Rowe.pdf',
  './documents/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Matthews.pdf',
  './documents/trains/shared/Zermatt_to_Gornergrat_Train_Schedule.pdf',
  './documents/trains/rowe/08_Zermatt_to_Geneva_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/08_Zermatt_to_Geneva_Train_Tickets_Matthews.pdf',
  './documents/lodging/The_New_Midi_Geneva_Confirmation_Rowe.pdf',
  './documents/lodging/The_New_Midi_Geneva_Confirmation_Matthews.pdf',
  './documents/trains/rowe/09_Geneva_to_Airport_Train_Tickets_Rowe.pdf',
  './documents/trains/matthews/09_Geneva_to_Airport_Train_Tickets_Matthews.pdf',
  './documents/rendered/guides_support/On_Trip_Support_Overview_IBTO/page-1.png',
  './documents/rendered/guides_support/On_Trip_Support_Overview_IBTO/page-2.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-1.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-2.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-3.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-4.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-5.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-6.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-7.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-8.png',
  './documents/rendered/lodging/BB_Fortuny_Arrival_Map/page-9.png',
  './documents/rendered/lodging/BB_Fortuny_Confirmation_Matthews/page-1.png',
  './documents/rendered/lodging/BB_Fortuny_Confirmation_Matthews/page-2.png',
  './documents/rendered/lodging/BB_Fortuny_Confirmation_Rowe/page-1.png',
  './documents/rendered/lodging/BB_Fortuny_Confirmation_Rowe/page-2.png',
  './documents/rendered/lodging/Hotel_Arte_St_Moritz_Confirmation_Matthews/page-1.png',
  './documents/rendered/lodging/Hotel_Arte_St_Moritz_Confirmation_Matthews/page-2.png',
  './documents/rendered/lodging/Hotel_Arte_St_Moritz_Confirmation_Rowe/page-1.png',
  './documents/rendered/lodging/Hotel_Arte_St_Moritz_Confirmation_Rowe/page-2.png',
  './documents/rendered/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Matthews/page-1.png',
  './documents/rendered/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Matthews/page-2.png',
  './documents/rendered/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Rowe/page-1.png',
  './documents/rendered/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Rowe/page-2.png',
  './documents/rendered/lodging/Hotel_Rezia_Confirmation_Matthews/page-1.png',
  './documents/rendered/lodging/Hotel_Rezia_Confirmation_Matthews/page-2.png',
  './documents/rendered/lodging/Hotel_Rezia_Confirmation_Matthews/page-3.png',
  './documents/rendered/lodging/Hotel_Rezia_Confirmation_Matthews/page-4.png',
  './documents/rendered/lodging/Hotel_Rezia_Confirmation_Rowe/page-1.png',
  './documents/rendered/lodging/Hotel_Rezia_Confirmation_Rowe/page-2.png',
  './documents/rendered/lodging/Hotel_Rezia_Confirmation_Rowe/page-3.png',
  './documents/rendered/lodging/Hotel_Rezia_Confirmation_Rowe/page-4.png',
  './documents/rendered/lodging/The_New_Midi_Geneva_Confirmation_Matthews/page-1.png',
  './documents/rendered/lodging/The_New_Midi_Geneva_Confirmation_Matthews/page-2.png',
  './documents/rendered/lodging/The_New_Midi_Geneva_Confirmation_Rowe/page-1.png',
  './documents/rendered/lodging/The_New_Midi_Geneva_Confirmation_Rowe/page-2.png',
  './documents/rendered/rental_car/Car_Rental_Confirmation_Rowe/page-1.png',
  './documents/rendered/rental_car/Car_Rental_Confirmation_Rowe/page-2.png',
  './documents/rendered/rental_car/Car_Rental_Confirmation_Rowe/page-3.png',
  './documents/rendered/rental_car/Car_Rental_Voucher_Rowe/page-1.png',
  './documents/rendered/rental_car/Car_Rental_Voucher_Rowe/page-2.png',
  './documents/rendered/rental_car/Car_Rental_Voucher_Rowe/page-3.png',
  './documents/rendered/rental_car/Car_Rental_Voucher_Rowe/page-4.png',
  './documents/rendered/rental_car/Car_Rental_Voucher_Rowe/page-5.png',
  './documents/rendered/rental_car/Car_Rental_Voucher_Rowe/page-6.png',
  './documents/rendered/rental_car/Car_Rental_Voucher_Rowe/page-7.png',
  './documents/rendered/rental_car/Car_Rental_Voucher_Rowe/page-8.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-1.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-10.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-11.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-12.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-13.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-14.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-15.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-16.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-17.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-18.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-19.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-2.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-20.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-21.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-22.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-23.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-24.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-25.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-26.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-27.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-28.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-3.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-4.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-5.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-6.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-7.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-8.png',
  './documents/rendered/rental_car/IBTO_Driving_in_Italy_Ebook/page-9.png',
  './documents/rendered/tours_excursions/Dolomites_Cable_Car_Prices_Schedule_Boe/page-1.png',
  './documents/rendered/tours_excursions/Salzburg_Sound_of_Music_Hallstatt_Tour_Viator/page-1.png',
  './documents/rendered/tours_excursions/Salzburg_Sound_of_Music_Hallstatt_Tour_Viator/page-2.png',
  './documents/rendered/tours_excursions/Salzburg_Sound_of_Music_Hallstatt_Tour_Viator/page-3.png',
  './documents/rendered/tours_excursions/Venice_Tours_Payment_Matthews/page-1.png',
  './documents/rendered/tours_excursions/Venice_Tours_Payment_Matthews/page-2.png',
  './documents/rendered/tours_excursions/Venice_Tours_Payment_Matthews/page-3.png',
  './documents/rendered/tours_excursions/Venice_Tours_Payment_Matthews/page-4.png',
  './documents/rendered/tours_excursions/Venice_Tours_Payment_Rowe/page-1.png',
  './documents/rendered/tours_excursions/Venice_Tours_Payment_Rowe/page-2.png',
  './documents/rendered/tours_excursions/Venice_Tours_Payment_Rowe/page-3.png',
  './documents/rendered/tours_excursions/Venice_Tours_Payment_Rowe/page-4.png',
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

// Install: Cache essential application assets & pre-rendered ticket pages
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(
        PRECACHE_URLS.map((url) =>
          cache.add(url).catch((err) => {
            console.warn('Pre-caching non-fatal asset warning:', url, err);
          })
        )
      );
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

// Fetch: Cache-First for documents/rendered/, Network-First with Cache Fallback for everything else
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = event.request.url;

  // Cache-first strategy for rendered ticket pages & documents (instant offline performance)
  if (url.includes('/documents/rendered/') || url.includes('/documents/')) {
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
          return caches.match(event.request);
        });
      })
    );
    return;
  }

  // Network-First with Cache Fallback for app shell & dynamic data
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
