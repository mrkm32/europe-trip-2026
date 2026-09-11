import json
import re
import glob

with open("documents/catalog.json", "r") as f:
    catalog = json.load(f)

with open("documents/rendered_manifest.json", "r") as f:
    manifest = json.load(f)

docs_map = {}

for item in catalog:
    p = item["path"]
    is_png = p.lower().endswith(".png")
    is_pdf = p.lower().endswith(".pdf")
    
    title = item.get("title", "")
    sub = item.get("subtitle", "")
    trav = item.get("traveler", "Shared")
    cat = item.get("category", "Documents")
    size = item.get("size", "")
    fmt = "PNG" if is_png else "PDF"
    
    rendered_info = manifest.get(p, {})
    pages = rendered_info.get("pages", [p] if is_png else [])
    page_count = rendered_info.get("pageCount", 1 if is_png else len(pages))
    
    page_labels = []
    if "WESTbahn" in title:
        page_labels = [
            "Mark Matthews • Ticket BX4-FDC",
            "Shelly Rowe • Ticket VEV-BAZ",
            "Bill Rowe • Ticket DJS-ZDP",
            "Kris Rowe • Ticket F83-AGT"
        ]
    elif "00_Munich_to_Salzburg" in p:
        page_labels = ["Coach 260, Seats 74–77 (All 4 Passengers)"]
    elif cat == "Train Tickets":
        if trav == "Mark & Shelly":
            if page_count == 3:
                page_labels = ["Mark Matthews (Passenger 1)", "Shelly Rowe (Passenger 2)", "Seat Reservation & Route Details"]
            elif page_count == 2:
                page_labels = ["Mark Matthews (Passenger 1)", "Shelly Rowe (Passenger 2)"]
            elif page_count == 4:
                page_labels = ["Mark Matthews (Ticket 1)", "Shelly Rowe (Ticket 2)", "Seat Reservation 1", "Seat Reservation 2"]
            elif page_count == 1:
                page_labels = ["Mark & Shelly (Combined Ticket)"]
        elif trav == "Bill & Kris":
            if page_count == 3:
                page_labels = ["Bill Rowe (Passenger 1)", "Kris Rowe (Passenger 2)", "Seat Reservation & Route Details"]
            elif page_count == 2:
                page_labels = ["Bill Rowe (Passenger 1)", "Kris Rowe (Passenger 2)"]
            elif page_count == 4:
                page_labels = ["Bill Rowe (Ticket 1)", "Kris Rowe (Ticket 2)", "Seat Reservation 1", "Seat Reservation 2"]
            elif page_count == 1:
                page_labels = ["Bill & Kris (Combined Ticket)"]
        elif trav == "Shared":
            page_labels = [f"Ticket / Details Page {i+1} of {page_count}" for i in range(page_count)]
    elif cat == "Hotel Confirmations":
        generic_hotel_labels = [
            "Reservation Voucher & Confirmation",
            "Room Details & Check-In Info",
            "Policies & Amenities",
            "Location & Directions"
        ]
        page_labels = [generic_hotel_labels[i] if i < len(generic_hotel_labels) else f"Page {i+1}" for i in range(page_count)]
    elif cat == "Car Rental":
        generic_car_labels = [
            "Car Rental Voucher & Pickup",
            "Rental Terms & Insurance",
            "Additional Drivers & Fuel Policy",
            "Location & Contact",
        ]
        page_labels = [generic_car_labels[i] if i < len(generic_car_labels) else f"Page {i+1}" for i in range(page_count)]
    
    if len(page_labels) < page_count:
        for i in range(len(page_labels), page_count):
            page_labels.append(f"Page {i+1} of {page_count}")
            
    docs_map[p] = {
        "title": title,
        "subtitle": sub,
        "traveler": trav,
        "category": cat,
        "size": size,
        "format": fmt,
        "pageCount": page_count,
        "pages": pages,
        "pageLabels": page_labels[:page_count]
    }

# Read index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update version badge
html = html.replace("<span>v3.46</span>", "<span>v3.47</span>")

# 2. Update DOCS_CATALOG_MAP
catalog_json_str = json.dumps(docs_map, indent=4)
catalog_map_code = f"    const DOCS_CATALOG_MAP = {catalog_json_str};\n"

start_marker = "    const DOCS_CATALOG_MAP = {"
end_marker = "};\n\n    let currentDocState = null;"

start_pos = html.find(start_marker)
end_pos = html.find(end_marker)
if start_pos == -1 or end_pos == -1:
    raise Exception(f"Markers not found! start_pos={start_pos}, end_pos={end_pos}")

html = html[:start_pos] + catalog_map_code + "\n" + html[end_pos + 3:]

# 3. Update JavaScript logic for openDocViewer, jumpToDocPage, openCurrentDocInSafari
new_js = """    let currentDocState = null;

    function openCurrentDocInSafari() {
      if (!currentDocState || !currentDocState.url) return;
      const absUrl = new URL(currentDocState.url, window.location.href).href;
      window.open(absUrl, '_blank');
    }

    function jumpToDocPage(pageIndex) {
      const pageEl = document.getElementById(`doc-page-${pageIndex}`);
      if (pageEl) {
        pageEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    function openDocViewer(url, fallbackTitle, isSaveAction) {
      if (!url) return;
      const cleanUrl = url.replace(/^\\.\\//, '');
      const docInfo = DOCS_CATALOG_MAP[cleanUrl] || {};

      const title = docInfo.title || fallbackTitle || cleanUrl.split('/').pop().replace(/_/g, ' ').replace(/\\.(pdf|png)$/i, '');
      const traveler = docInfo.traveler || (cleanUrl.includes('matthews') ? 'Mark & Shelly' : (cleanUrl.includes('rowe') ? 'Bill & Kris' : 'Shared'));
      const category = docInfo.category || 'Documents';
      const size = docInfo.size || '';
      const isImage = /\\.(png|jpe?g|webp|gif)$/i.test(cleanUrl);
      const format = docInfo.format || (isImage ? 'PNG' : 'PDF');

      const pages = docInfo.pages && docInfo.pages.length > 0 ? docInfo.pages : (isImage ? [cleanUrl] : []);
      const pageCount = docInfo.pageCount || pages.length || 1;
      const pageLabels = docInfo.pageLabels || [];

      currentDocState = {
        url: cleanUrl,
        title: title,
        traveler: traveler,
        category: category,
        pageCount: pageCount
      };

      const modal = document.getElementById('doc-viewer-modal');
      const titleEl = document.getElementById('doc-modal-title');
      const badgeEl = document.getElementById('doc-modal-badge');
      const catEl = document.getElementById('doc-modal-category');
      const formatEl = document.getElementById('doc-modal-format');
      const pagesBadgeEl = document.getElementById('doc-modal-pages-badge');
      const bannerEl = document.getElementById('doc-modal-pages-banner');
      const bannerCountEl = document.getElementById('doc-modal-banner-count');
      const jumpContainer = document.getElementById('doc-modal-jump-container');
      const galleryContainer = document.getElementById('doc-modal-gallery-container');
      const iframeContainer = document.getElementById('doc-modal-iframe-container');
      const iframe = document.getElementById('doc-modal-iframe');

      if (titleEl) titleEl.textContent = title;
      if (catEl) catEl.textContent = category;
      if (formatEl) formatEl.textContent = `${format}${size ? ' • ' + size : ''}`;

      if (badgeEl) {
        badgeEl.textContent = traveler;
        if (traveler.includes('Mark')) {
          badgeEl.className = 'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black bg-purple-500/20 text-purple-300 border border-purple-400/30 truncate shrink-0';
        } else if (traveler.includes('Bill')) {
          badgeEl.className = 'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black bg-blue-500/20 text-blue-300 border border-blue-400/30 truncate shrink-0';
        } else {
          badgeEl.className = 'inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 truncate shrink-0';
        }
      }

      // Handle pages vs iframe fallback
      if (pages.length > 0) {
        if (iframeContainer) iframeContainer.classList.add('hidden');
        if (iframe) iframe.src = 'about:blank';
        if (galleryContainer) {
          galleryContainer.classList.remove('hidden');
          galleryContainer.scrollTop = 0;
          galleryContainer.innerHTML = '';

          pages.forEach((pagePath, idx) => {
            const pageNum = idx + 1;
            const label = pageLabels[idx] || (pageCount > 1 ? `Page ${pageNum} of ${pageCount}` : title);
            
            const card = document.createElement('div');
            card.id = `doc-page-${pageNum}`;
            card.className = 'w-full max-w-3xl mx-auto bg-slate-900 rounded-2xl border border-slate-800 shadow-2xl overflow-hidden scroll-mt-3';

            card.innerHTML = `
              <div class="w-full bg-slate-800/90 border-b border-slate-700/60 px-3.5 py-2 flex items-center justify-between text-xs">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="px-2 py-0.5 rounded-full bg-sky-500/20 text-sky-300 border border-sky-400/40 text-[10px] font-black shrink-0">Page ${pageNum} of ${pageCount}</span>
                  <span class="text-slate-200 font-bold text-[11px] sm:text-xs truncate">${label}</span>
                </div>
                <span class="text-[10px] font-mono text-emerald-400/90 font-semibold shrink-0 hidden sm:inline">QR / Conductor Scan</span>
              </div>
              <div class="w-full bg-white flex items-center justify-center p-1 sm:p-2 select-text">
                <img src="${pagePath}" alt="${label}" loading="eager" class="w-full h-auto max-w-full object-contain pointer-events-auto" />
              </div>
            `;
            galleryContainer.appendChild(card);
          });
        }

        if (pageCount > 1) {
          if (bannerEl) bannerEl.classList.remove('hidden');
          if (bannerCountEl) bannerCountEl.textContent = pageCount;
          if (pagesBadgeEl) {
            pagesBadgeEl.classList.remove('hidden');
            pagesBadgeEl.textContent = `${pageCount} Tickets / Pages`;
          }
          if (jumpContainer) {
            jumpContainer.innerHTML = pages.map((_, idx) => {
              const p = idx + 1;
              return `<button type="button" onclick="jumpToDocPage(${p})" class="px-2 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 border border-amber-500/30 text-[10px] font-bold active:scale-95 transition cursor-pointer">P${p}</button>`;
            }).join('');
          }
        } else {
          if (bannerEl) bannerEl.classList.add('hidden');
          if (pagesBadgeEl) pagesBadgeEl.classList.add('hidden');
        }
      } else {
        if (galleryContainer) galleryContainer.classList.add('hidden');
        if (bannerEl) bannerEl.classList.add('hidden');
        if (pagesBadgeEl) pagesBadgeEl.classList.add('hidden');
        if (iframeContainer) iframeContainer.classList.remove('hidden');
        if (iframe) iframe.src = cleanUrl;
      }

      if (modal) {
        modal.classList.remove('hidden');
        document.body.classList.add('overflow-hidden');
      }

      try {
        history.pushState({ alpsModal: 'docViewer' }, '', '#viewer');
      } catch (e) {}

      if (isSaveAction && navigator.share) {
        setTimeout(() => {
          shareCurrentDoc();
        }, 300);
      }
    }

    function closeDocViewer(popHistory = true) {
      const modal = document.getElementById('doc-viewer-modal');
      if (!modal || modal.classList.contains('hidden')) return;

      modal.classList.add('hidden');
      document.body.classList.remove('overflow-hidden');

      const iframe = document.getElementById('doc-modal-iframe');
      if (iframe) iframe.src = 'about:blank';
      const galleryContainer = document.getElementById('doc-modal-gallery-container');
      if (galleryContainer) galleryContainer.innerHTML = '';

      currentDocState = null;

      if (popHistory && window.location.hash === '#viewer') {
        history.back();
      }
    }

    async function shareCurrentDoc() {
      if (!currentDocState) return;
      const absUrl = new URL(currentDocState.url, window.location.href).href;

      if (navigator.share) {
        try {
          await navigator.share({
            title: currentDocState.title,
            text: `${currentDocState.title} (${currentDocState.traveler}) - Europe Alps Odyssey 2026`,
            url: absUrl
          });
        } catch (err) {
          if (err.name !== 'AbortError') {
            console.warn('Share error:', err);
          }
        }
      } else {
        const tempLink = document.createElement('a');
        tempLink.href = absUrl;
        tempLink.download = currentDocState.url.split('/').pop();
        document.body.appendChild(tempLink);
        tempLink.click();
        document.body.removeChild(tempLink);
      }
    }

    // Global document link interception
    document.addEventListener('click', function(e) {
      const link = e.target.closest('a[href*="documents/"]');
      if (!link) return;

      const href = link.getAttribute('href');
      if (!href || href.startsWith('#')) return;

      e.preventDefault();

      const isSave = link.hasAttribute('download');
      const cardTitle = link.closest('.doc-card')?.querySelector('h4')?.textContent?.trim();
      const textTitle = link.textContent?.trim();

      openDocViewer(href, cardTitle || textTitle, isSave);
    });

    // History popstate listener for back button & edge-swipe
    window.addEventListener('popstate', (e) => {
      const modal = document.getElementById('doc-viewer-modal');
      if (modal && !modal.classList.contains('hidden')) {
        closeDocViewer(false);
      }
    });

    // Keyboard ESC listener
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeDocViewer(true);
      }
    });"""

js_start = "    let currentDocState = null;"
js_end = "    /* NETWORK STATUS LISTENER */"
js_start_pos = html.find(js_start)
js_end_pos = html.find(js_end)
if js_start_pos == -1 or js_end_pos == -1:
    raise Exception("JS markers not found!")

html = html[:js_start_pos] + new_js + "\n\n" + html[js_end_pos:]

# 4. Update the Modal HTML
new_modal_html = """  <!-- IN-APP DOCUMENT VIEWER MODAL (SOLVES IOS STANDALONE PWA TRAP & MULTI-PAGE VIEWING) -->
  <div id="doc-viewer-modal" class="fixed inset-0 z-[100] bg-slate-950 flex flex-col hidden select-none no-print">
    <!-- Sticky Safe-Area Header Bar -->
    <header class="bg-slate-900 border-b border-slate-800 px-3 sm:px-5 py-2.5 flex items-center justify-between gap-2 sm:gap-4 shadow-xl shrink-0"
            style="padding-top: max(0.6rem, env(safe-area-inset-top)); padding-left: max(0.75rem, env(safe-area-inset-left)); padding-right: max(0.75rem, env(safe-area-inset-right));">
      <!-- Left: Primary 'Back to App' Button -->
      <button type="button" onclick="closeDocViewer()" class="inline-flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-gradient-to-r from-sky-500 to-blue-600 hover:from-sky-400 hover:to-blue-500 active:scale-95 text-white font-extrabold text-xs sm:text-sm shadow-md transition-all shrink-0 cursor-pointer">
        <svg class="w-4 h-4 stroke-[2.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        <span>Back to App</span>
      </button>

      <!-- Center: Document Title & Badges -->
      <div class="flex flex-col min-w-0 flex-1 px-1 text-left">
        <div class="flex items-center gap-1.5 overflow-hidden flex-wrap sm:flex-nowrap">
          <span id="doc-modal-badge" class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black bg-purple-500/20 text-purple-300 border border-purple-400/30 truncate shrink-0">Mark & Shelly</span>
          <span id="doc-modal-category" class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700 truncate shrink-0">Train Tickets</span>
          <span id="doc-modal-pages-badge" class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-black bg-amber-500/20 text-amber-300 border border-amber-400/40 truncate shrink-0 hidden">3 Tickets / Pages</span>
          <span id="doc-modal-format" class="text-[10px] font-mono text-slate-400 hidden sm:inline shrink-0">PDF • 376 KB</span>
        </div>
        <h3 id="doc-modal-title" class="text-xs sm:text-sm font-black text-white truncate mt-0.5">
          Innsbruck ➔ Bolzano Train Tickets
        </h3>
      </div>

      <!-- Right: Safari ↗, Share / Save to Files & Close Icon -->
      <div class="flex items-center gap-1.5 shrink-0">
        <button type="button" id="doc-modal-safari-btn" onclick="openCurrentDocInSafari()" class="inline-flex items-center gap-1 px-2.5 sm:px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 active:scale-95 text-sky-400 border border-slate-700 text-xs font-bold transition cursor-pointer" title="Open native PDF in Safari">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
          <span class="hidden sm:inline">Safari ↗</span>
        </button>
        <button type="button" onclick="shareCurrentDoc()" class="inline-flex items-center gap-1 px-2.5 sm:px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 active:scale-95 text-sky-400 border border-slate-700 text-xs font-bold transition cursor-pointer" title="Save to Files / Share ticket via AirDrop, Messages, etc.">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"/></svg>
          <span class="hidden sm:inline">Share</span>
        </button>
        <button type="button" onclick="closeDocViewer()" class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 active:scale-95 text-slate-300 hover:text-white border border-slate-700 transition cursor-pointer" title="Close document viewer">
          <svg class="w-5 h-5 stroke-[2.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    </header>

    <!-- Multi-Page Banner (Only shown if pageCount > 1) -->
    <div id="doc-modal-pages-banner" class="bg-gradient-to-r from-amber-950/80 via-slate-900 to-amber-950/80 border-b border-amber-500/30 px-3 sm:px-5 py-2 flex items-center justify-between gap-2 text-xs text-amber-200 shrink-0 select-none hidden">
      <div class="flex items-center gap-2 min-w-0">
        <span class="text-sm shrink-0">🎫</span>
        <span class="font-bold truncate text-[11px] sm:text-xs">Showing ALL <span id="doc-modal-banner-count" class="text-amber-400 font-black">3</span> Pages / Tickets</span>
        <span class="text-amber-300/70 text-[10px] hidden md:inline">• Scroll down for all passengers</span>
      </div>
      <!-- Quick Jump Buttons Container -->
      <div id="doc-modal-jump-container" class="flex items-center gap-1 shrink-0 overflow-x-auto">
      </div>
    </div>

    <!-- Viewer Body -->
    <div class="flex-1 w-full h-full relative overflow-hidden bg-slate-950 flex flex-col">
      <!-- Multi-Page Scrollable Gallery Container -->
      <div id="doc-modal-gallery-container" class="w-full h-full relative overflow-y-auto px-2 sm:px-4 py-4 space-y-6" style="-webkit-overflow-scrolling: touch;">
      </div>

      <!-- Fallback PDF Iframe Container (only if unrendered) -->
      <div id="doc-modal-iframe-container" class="w-full h-full relative overflow-auto hidden" style="-webkit-overflow-scrolling: touch;">
        <iframe id="doc-modal-iframe" src="about:blank" class="w-full h-full border-0 bg-white" title="Trip Document Viewer" allowfullscreen></iframe>
      </div>
    </div>

    <!-- Bottom Helper / Dismiss Bar -->
    <footer class="bg-slate-900/95 border-t border-slate-800/80 px-4 py-2 flex items-center justify-between text-xs shrink-0 select-none"
            style="padding-bottom: max(0.5rem, env(safe-area-inset-bottom)); padding-left: max(0.75rem, env(safe-area-inset-left)); padding-right: max(0.75rem, env(safe-area-inset-right));">
      <span class="text-[11px] text-slate-400 truncate flex items-center gap-1.5">
        <span class="w-2 h-2 rounded-full bg-emerald-400 inline-block animate-pulse"></span>
        <span id="doc-modal-status-text">Available Offline • All Pages Ready</span>
      </span>
      <button type="button" onclick="closeDocViewer()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 active:scale-95 text-slate-200 border border-slate-700 font-bold text-[11px] transition cursor-pointer">
        <span>✕ Done Viewing</span>
      </button>
    </footer>
  </div>"""

modal_start = "  <!-- IN-APP DOCUMENT VIEWER MODAL (SOLVES IOS STANDALONE PWA TRAP) -->"
modal_end = "</body>"
modal_start_pos = html.find(modal_start)
modal_end_pos = html.find(modal_end)
if modal_start_pos == -1 or modal_end_pos == -1:
    raise Exception("Modal markers not found!")

html = html[:modal_start_pos] + new_modal_html + "\n\n" + html[modal_end_pos:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: Updated index.html with multi-page ticket viewer system and v3.47!")
