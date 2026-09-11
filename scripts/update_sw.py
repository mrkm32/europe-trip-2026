import json
import glob

CACHE_NAME = 'europe-alps-2026-v12'

with open("documents/catalog.json", "r") as f:
    catalog = json.load(f)

rendered_pngs = sorted(glob.glob("documents/rendered/**/*.png", recursive=True))

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

for item in catalog:
    p = f"./{item['path']}"
    if p not in precache_set:
        precache_set.append(p)

for png in rendered_pngs:
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

// Install: Cache essential application assets & pre-rendered ticket pages
self.addEventListener('install', (event) => {{
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {{
      return Promise.allSettled(
        PRECACHE_URLS.map((url) =>
          cache.add(url).catch((err) => {{
            console.warn('Pre-caching non-fatal asset warning:', url, err);
          }})
        )
      );
    }}).then(() => self.skipWaiting())
  );
}});

// Activate: Purge older cache versions
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

// Fetch: Cache-First for documents/rendered/, Network-First with Cache Fallback for everything else
self.addEventListener('fetch', (event) => {{
  if (event.request.method !== 'GET') return;

  const url = event.request.url;

  // Cache-first strategy for rendered ticket pages & documents (instant offline performance)
  if (url.includes('/documents/rendered/') || url.includes('/documents/')) {{
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
          return caches.match(event.request);
        }});
      }})
    );
    return;
  }}

  // Network-First with Cache Fallback for app shell & dynamic data
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {{
        if (networkResponse && networkResponse.status === 200) {{
          const responseClone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {{
            cache.put(event.request, responseClone);
          }});
        }}
        return networkResponse;
      }})
      .catch(() => {{
        return caches.match(event.request).then((cachedResponse) => {{
          if (cachedResponse) {{
            return cachedResponse;
          }}
          if (event.request.mode === 'navigate') {{
            return caches.match('./index.html');
          }}
        }});
      }})
  );
}});
"""

with open("sw.js", "w", encoding="utf-8") as f:
    f.write(sw_content)

print(f"Updated sw.js with {len(precache_set)} precache assets (including {len(rendered_pngs)} rendered pages) on cache {CACHE_NAME}!")
