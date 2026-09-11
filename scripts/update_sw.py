import json
import glob

CACHE_NAME = 'europe-alps-2026-v13'

with open("documents/catalog.json", "r") as f:
    catalog = json.load(f)

# Precache all train tickets (rendered pages) so they are 100% available offline
train_pngs = sorted(glob.glob("documents/rendered/trains/**/*.png", recursive=True))

precache_set = [
    './',
    './index.html',
    './manifest.json',
    './apple-touch-icon.png',
    './icon-192.png',
    './icon-512.png',
    './hero.jpg',
    './alps_map.jpg',
    'https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js'
]

# Add all train ticket PDFs
for item in catalog:
    if item.get("category") == "Train Tickets":
        p = f"./{item['path']}"
        if p not in precache_set:
            precache_set.append(p)

# Add all train ticket rendered PNGs
for png in train_pngs:
    p = f"./{png}"
    if p not in precache_set:
        precache_set.append(p)

precache_lines = ",\n".join([f"  '{url}'" for url in precache_set])

sw_content = f"""// Service Worker for Europe Alps Odyssey 2026
// Enables 100% Offline Access across Alpine valleys, trains, and mountain passes
const CACHE_NAME = '{CACHE_NAME}';

const PRECACHE_URLS = [
{precache_lines}
];

// Install: Cache essential application assets & pre-rendered train ticket pages
self.addEventListener('install', (event) => {{
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {{
      return Promise.allSettled(
        PRECACHE_URLS.map((url) =>
          cache.add(url).catch((err) => {{
            console.warn('Pre-caching asset:', url, err);
          }})
        )
      );
    }}).then(() => self.skipWaiting())
  );
}});

// Activate: Purge older cache versions immediately
self.addEventListener('activate', (event) => {{
  event.waitUntil(
    caches.keys().then((keys) => {{
      return Promise.all(
        keys.map((key) => {{
          if (key !== CACHE_NAME) {{
            return caches.delete(key);
          }}
        }})
      );
    }}).then(() => self.clients.claim())
  );
}});

// Fetch: Cache-First for instant offline performance, Network Fallback with automatic caching
self.addEventListener('fetch', (event) => {{
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {{
      if (cachedResponse) {{
        return cachedResponse;
      }}
      return fetch(event.request).then((networkResponse) => {{
        if (networkResponse && networkResponse.status === 200) {{
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {{
            cache.put(event.request, responseClone);
          }});
        }}
        return networkResponse;
      }}).catch(() => {{
        if (event.request.mode === 'navigate') {{
          return caches.match('./index.html');
        }}
        return caches.match(event.request);
      }});
    }})
  );
}});
"""

with open("sw.js", "w", encoding="utf-8") as f:
    f.write(sw_content)

print(f"Updated sw.js with {len(precache_set)} precache assets on cache {CACHE_NAME}!")
