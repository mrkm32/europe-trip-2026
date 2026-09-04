import json

with open("documents/catalog.json", "r") as f:
    catalog = json.load(f)

def get_traveler_badge(t):
    if t == "Mark & Shelly":
        return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold bg-sky-50 text-sky-700 border border-sky-200"><svg class="w-3 h-3 text-sky-600" fill="currentColor" viewBox="0 0 20 20"><path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/></svg> Mark & Shelly</span>'
    elif t == "Bill & Kris":
        return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200"><svg class="w-3 h-3 text-emerald-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clip-rule="evenodd"/></svg> Bill & Kris</span>'
    else:
        return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-bold bg-slate-100 text-slate-700 border border-slate-200">👥 Shared (All 4)</span>'

def get_category_badge(c):
    if c == "Train Tickets":
        return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-indigo-50 text-indigo-700 border border-indigo-200">🚆 Train Ticket</span>'
    elif c == "Hotel Confirmations":
        return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-amber-50 text-amber-800 border border-amber-200">🏨 Hotel Voucher</span>'
    elif c == "Car Rental":
        return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200">🚗 Car & Driving</span>'
    elif c == "Tours & Lifts":
        return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-purple-50 text-purple-700 border border-purple-200">🚠 Tour / Lift</span>'
    else:
        return '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">🧭 Support Guide</span>'

cards_html = []
for item in catalog:
    is_png = item["path"].endswith(".png")
    icon_type = "PNG • " if is_png else "PDF • "
    t_title = item["title"]
    t_sub = item["subtitle"]
    t_trav = item["traveler"]
    t_cat = item["category"]
    t_city = item["city"]
    t_day = item["day"]
    t_path = item["path"]
    t_size = item["size"]
    
    search_str = f"{t_title} {t_sub} {t_trav} {t_cat} {t_city} {t_day}".lower()
    
    card = f"""        <div class="doc-card bg-white rounded-xl p-4 border border-slate-200 shadow-sm hover:shadow-md transition flex flex-col justify-between gap-3"
             data-traveler="{t_trav}"
             data-category="{t_cat}"
             data-city="{t_city}"
             data-search="{search_str}">
          <div>
            <div class="flex flex-wrap items-center gap-1.5 mb-2">
              {get_traveler_badge(t_trav)}
              {get_category_badge(t_cat)}
              <span class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-md text-[10px] font-medium bg-slate-100 text-slate-600">{t_day}</span>
            </div>
            <h4 class="text-sm sm:text-base font-extrabold text-slate-900 leading-snug">
              {t_title}
            </h4>
            <p class="text-xs text-slate-600 font-medium mt-1 leading-relaxed">
              {t_sub}
            </p>
          </div>
          <div class="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
            <div class="flex items-center gap-1 text-[11px] text-slate-400 font-medium">
              <svg class="w-3.5 h-3.5 text-slate-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
              <span>{icon_type}{t_size}</span>
            </div>
            <div class="flex items-center gap-1.5 shrink-0">
              <a href="{t_path}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-bold bg-sky-600 hover:bg-sky-500 text-white shadow-sm transition" title="Open in new tab">
                <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                <span>View</span>
              </a>
              <a href="{t_path}" download class="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200 transition" title="Download copy">
                <svg class="w-3.5 h-3.5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
                <span class="hidden sm:inline">Save</span>
              </a>
            </div>
          </div>
        </div>"""
    cards_html.append(card)

panel_html = f"""    <!-- PANEL 4: TICKETS & SUPPORTING DOCUMENTS (39 ITEMS, MULTI-FILTER, 100% OFFLINE) -->
    <div id="panel-documents" class="tab-panel hidden" style="display: none;">
      <!-- Hero Banner -->
      <div class="bg-gradient-to-r from-purple-900 via-indigo-900 to-slate-900 rounded-2xl p-5 sm:p-7 text-white shadow-xl mb-6 border border-purple-800/40 relative overflow-hidden">
        <div class="absolute -right-10 -bottom-10 w-48 h-48 bg-purple-500/10 rounded-full blur-3xl pointer-events-none"></div>
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div class="flex flex-wrap items-center gap-2 mb-2">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-extrabold bg-purple-500/30 text-purple-200 border border-purple-400/30 uppercase tracking-wider">
                🎟️ Complete Document Vault
              </span>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                ⚡ 100% Offline Ready
              </span>
            </div>
            <h2 class="text-2xl sm:text-3xl font-black tracking-tight text-white">
              Official Tickets & Vouchers
            </h2>
            <p class="text-purple-200/90 text-xs sm:text-sm mt-1 max-w-2xl font-light leading-relaxed">
              All 39 official train tickets, hotel confirmations, rental car vouchers, and alpine cable car passes from Madeline (Italy Beyond the Obvious). Stored locally on this site for instant access even without cellular reception in the Alps!
            </p>
          </div>
          <div class="flex flex-row md:flex-col items-center md:items-end justify-between gap-2 shrink-0">
            <div class="text-right hidden sm:block">
              <div class="text-2xl font-black text-white">39 Files</div>
              <div class="text-[11px] text-purple-300 font-mono">18 MB Total Cached</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Multi-Facet Search & Filter Hub (Sticky / Responsive for iPhone 15/16) -->
      <div class="bg-white rounded-2xl p-4 sm:p-5 border border-slate-200 shadow-sm mb-6 space-y-3.5">
        <!-- Search Input -->
        <div class="relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>
          <input type="text" id="doc-search-input" oninput="filterDocuments()" placeholder="Search by city, train number, hotel, or traveler (e.g. Tirano, Rezia, Rowe, Railjet)..." 
                 class="w-full pl-9 pr-8 py-2.5 text-xs sm:text-sm rounded-xl border border-slate-200 bg-slate-50 focus:bg-white focus:outline-none focus:ring-2 focus:ring-purple-500 text-slate-900 placeholder-slate-400 transition" />
          <button onclick="clearDocSearch()" id="doc-search-clear" class="hidden absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>

        <!-- Traveler Filter Pills -->
        <div class="flex flex-col sm:flex-row sm:items-center gap-2">
          <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider shrink-0">Traveler:</span>
          <div class="flex flex-wrap items-center gap-1.5">
            <button onclick="setDocTraveler('all')" id="doc-filter-trav-all" class="doc-trav-btn active-doc-trav px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-900 text-white shadow-sm">
              All Travelers (39)
            </button>
            <button onclick="setDocTraveler('Mark & Shelly')" id="doc-filter-trav-matthews" class="doc-trav-btn px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200">
              ✈ Mark & Shelly (15)
            </button>
            <button onclick="setDocTraveler('Bill & Kris')" id="doc-filter-trav-rowe" class="doc-trav-btn px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200">
              🏔 Bill & Kris (17)
            </button>
            <button onclick="setDocTraveler('Shared')" id="doc-filter-trav-shared" class="doc-trav-btn px-3 py-1.5 rounded-lg text-xs font-bold transition bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200">
              👥 Shared / All 4 (7)
            </button>
          </div>
        </div>

        <!-- Category & City Dropdown Bar -->
        <div class="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-slate-100">
          <!-- Category Pills -->
          <div class="flex items-center gap-1.5 overflow-x-auto custom-scrollbar pb-1 w-full lg:w-auto">
            <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider shrink-0 mr-1">Type:</span>
            <button onclick="setDocCategory('all')" id="doc-filter-cat-all" class="doc-cat-btn active-doc-cat px-2.5 py-1 rounded-lg text-xs font-semibold shrink-0 bg-purple-600 text-white shadow-sm">
              All (39)
            </button>
            <button onclick="setDocCategory('Train Tickets')" id="doc-filter-cat-trains" class="doc-cat-btn px-2.5 py-1 rounded-lg text-xs font-semibold shrink-0 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200">
              🚆 Trains (20)
            </button>
            <button onclick="setDocCategory('Hotel Confirmations')" id="doc-filter-cat-lodging" class="doc-cat-btn px-2.5 py-1 rounded-lg text-xs font-semibold shrink-0 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200">
              🏨 Hotels (11)
            </button>
            <button onclick="setDocCategory('Car Rental')" id="doc-filter-cat-car" class="doc-cat-btn px-2.5 py-1 rounded-lg text-xs font-semibold shrink-0 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200">
              🚗 Car & Driving (3)
            </button>
            <button onclick="setDocCategory('Tours & Lifts')" id="doc-filter-cat-tours" class="doc-cat-btn px-2.5 py-1 rounded-lg text-xs font-semibold shrink-0 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200">
              🚠 Tours & Lifts (4)
            </button>
            <button onclick="setDocCategory('Guides & Support')" id="doc-filter-cat-guides" class="doc-cat-btn px-2.5 py-1 rounded-lg text-xs font-semibold shrink-0 bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200">
              🧭 Support (1)
            </button>
          </div>

          <!-- City Dropdown & Live Counter -->
          <div class="flex items-center gap-2.5 w-full sm:w-auto justify-between sm:justify-end shrink-0">
            <select id="doc-city-filter" onchange="filterDocuments()" class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-slate-100 border border-slate-200 text-slate-700 focus:outline-none focus:ring-2 focus:ring-purple-500">
              <option value="all">📍 All Cities & Legs</option>
              <option value="Innsbruck / Bolzano">Innsbruck / Bolzano</option>
              <option value="Dolomites">Dolomites (Alta Badia)</option>
              <option value="Venice">Venice</option>
              <option value="Tirano / Bernina">Tirano / Bernina Route</option>
              <option value="St. Moritz">St. Moritz</option>
              <option value="Chur / Andermatt">Chur & Andermatt</option>
              <option value="Zermatt">Zermatt & Matterhorn</option>
              <option value="Geneva">Geneva</option>
              <option value="General">General / Italy</option>
            </select>
            <span id="doc-results-counter" class="text-xs font-bold text-purple-700 bg-purple-50 px-2.5 py-1 rounded-lg border border-purple-200 shrink-0">
              39 of 39
            </span>
          </div>
        </div>
      </div>

      <!-- Grid of 39 Document Cards -->
      <div id="docs-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
{chr(10).join(cards_html)}
      </div>

      <!-- Empty State If No Results Found -->
      <div id="docs-empty-state" class="hidden text-center py-12 bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
        <div class="w-16 h-16 rounded-full bg-purple-50 text-purple-600 flex items-center justify-center mx-auto mb-3">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
        <h4 class="text-base font-bold text-slate-900">No matching tickets or vouchers found</h4>
        <p class="text-xs text-slate-500 mt-1 max-w-sm mx-auto">Try clearing your search query or selecting "All Travelers" and "All Types".</p>
        <button onclick="resetDocFilters()" class="mt-4 px-4 py-2 bg-purple-600 hover:bg-purple-500 text-white font-bold rounded-xl text-xs transition shadow-md">
          Reset All Filters
        </button>
      </div>
    </div>
"""

with open("scripts/panel_documents.html", "w", encoding="utf-8") as f:
    f.write(panel_html)

print("SUCCESS: Generated scripts/panel_documents.html with length:", len(panel_html))
