import json

with open("documents/catalog.json", "r") as f:
    catalog = json.load(f)

doc_lines = []
for item in catalog:
    p = item["path"]
    doc_lines.append(f'  "./{p}",')

doc_paths_str = "\n".join(doc_lines)

sw_content = f"""// Service Worker for Europe Alps Odyssey 2026
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
{doc_paths_str}
];

// Install: Cache essential application assets immediately
self.addEventListener('install', (event) => {{
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {{
      return cache.addAll(PRECACHE_URLS).catch((err) => {{
        console.warn('Pre-caching non-fatal asset warning:', err);
      }});
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

// Fetch: Network-First with Cache Fallback
self.addEventListener('fetch', (event) => {{
  if (event.request.method !== 'GET') return;

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

print(f"Updated sw.js with {len(catalog)} offline travel documents!")
