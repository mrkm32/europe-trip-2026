import os

INDEX_PATH = "/Users/markmatthews/Code/Euro Alps Trip/index.html"
PANEL_DOCS_PATH = "/Users/markmatthews/Code/Euro Alps Trip/scripts/panel_documents.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

with open(PANEL_DOCS_PATH, "r", encoding="utf-8") as f:
    panel_docs_html = f.read()

# 1. Bump version to v3.40
content = content.replace("v3.33</span>", "v3.40</span>")

# 2. Add button in hero nav
old_hero_nav = """            <button onclick="switchMainTab('schedule')" class="px-3.5 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-xs sm:text-sm transition flex items-center gap-1.5 shadow-lg shadow-indigo-600/25">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
              <span>Schedule</span>
            </button>"""

new_hero_nav = old_hero_nav + """
            <button onclick="switchMainTab('documents')" class="px-3.5 py-2 bg-purple-600 hover:bg-purple-500 text-white font-medium rounded-lg text-xs sm:text-sm transition flex items-center gap-1.5 shadow-lg shadow-purple-600/25">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
              <span>Tickets & Docs</span>
              <span class="bg-white/20 px-1.5 py-0.5 rounded-full text-[10px] font-bold">39</span>
            </button>"""

if old_hero_nav in content:
    content = content.replace(old_hero_nav, new_hero_nav, 1)
    print("Added hero nav button.")
else:
    print("WARNING: Could not find old_hero_nav")

# 3. Add button in sticky nav bar
old_sticky_nav = """          <button onclick="switchMainTab('schedule')" id="tab-btn-schedule" class="main-nav-tab flex items-center gap-2 px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition text-slate-300 hover:text-white hover:bg-slate-800">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
            <span class="truncate">Day-by-Day Expedition Schedule</span>
            <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-full border border-emerald-400/30 font-mono">16 Days</span>
          </button>"""

new_sticky_nav = old_sticky_nav + """
          <button onclick="switchMainTab('documents')" id="tab-btn-documents" class="main-nav-tab flex items-center gap-2 px-4 sm:px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition text-slate-300 hover:text-white hover:bg-slate-800">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
            <span class="truncate">Tickets & Docs</span>
            <span class="text-[10px] bg-purple-500/20 text-purple-300 px-2 py-0.5 rounded-full border border-purple-400/30 font-mono">39 Docs</span>
          </button>"""

if old_sticky_nav in content:
    content = content.replace(old_sticky_nav, new_sticky_nav, 1)
    print("Added sticky nav button.")
else:
    print("WARNING: Could not find old_sticky_nav")

# 4. Insert panel_documents right after panel-schedule closing
# Notice Day 16 ends with </section>\n    </div>
target_panel_end = """        </div>

      </div>
    </section>
    </div>"""

target_replacement = target_panel_end + "\n\n" + panel_docs_html

if target_panel_end in content:
    content = content.replace(target_panel_end, target_replacement, 1)
    print("Inserted panel-documents.")
else:
    print("WARNING: Could not find target_panel_end")

# 5. Update JavaScript logic for tab switching and document filtering
old_js_tab_logic = """    /* MAIN TAB NAVIGATION LOGIC (Overview, Confirmations, Schedule) */
    function switchMainTab(tabId) {
      const pOverview = document.getElementById('panel-overview');
      const pConfirm = document.getElementById('panel-confirmations');
      const pSchedule = document.getElementById('panel-schedule');

      if (pOverview) {
        if (tabId === 'overview') {
          pOverview.classList.remove('hidden');
          pOverview.style.setProperty('display', 'block', 'important');
        } else {
          pOverview.classList.add('hidden');
          pOverview.style.setProperty('display', 'none', 'important');
        }
      }

      if (pConfirm) {
        if (tabId === 'confirmations') {
          pConfirm.classList.remove('hidden');
          pConfirm.style.setProperty('display', 'block', 'important');
        } else {
          pConfirm.classList.add('hidden');
          pConfirm.style.setProperty('display', 'none', 'important');
        }
      }

      if (pSchedule) {
        if (tabId === 'schedule') {
          pSchedule.classList.remove('hidden');
          pSchedule.style.setProperty('display', 'block', 'important');
        } else {
          pSchedule.classList.add('hidden');
          pSchedule.style.setProperty('display', 'none', 'important');
        }
      }

      const btnOverview = document.getElementById('tab-btn-overview');
      const btnConfirm = document.getElementById('tab-btn-confirmations');
      const btnSchedule = document.getElementById('tab-btn-schedule');

      if (btnOverview && btnConfirm && btnSchedule) {
        btnOverview.classList.remove('active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25');
        btnOverview.classList.add('text-slate-300');
        btnConfirm.classList.remove('active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25');
        btnConfirm.classList.add('text-slate-300');
        btnSchedule.classList.remove('active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25');
        btnSchedule.classList.add('text-slate-300');

        if (tabId === 'overview') {
          btnOverview.classList.add('active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25');
          btnOverview.classList.remove('text-slate-300');
        } else if (tabId === 'confirmations') {
          btnConfirm.classList.add('active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25');
          btnConfirm.classList.remove('text-slate-300');
        } else if (tabId === 'schedule') {
          btnSchedule.classList.add('active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25');
          btnSchedule.classList.remove('text-slate-300');
        }
      }

      currentTab = tabId;
      try {
        localStorage.setItem('alps_active_tab', tabId);
      } catch(e) {}
    }"""

new_js_tab_logic = """    /* MAIN TAB NAVIGATION LOGIC (Overview, Confirmations, Schedule, Documents) */
    function switchMainTab(tabId) {
      const pOverview = document.getElementById('panel-overview');
      const pConfirm = document.getElementById('panel-confirmations');
      const pSchedule = document.getElementById('panel-schedule');
      const pDocs = document.getElementById('panel-documents');

      const panels = [
        { id: 'overview', el: pOverview },
        { id: 'confirmations', el: pConfirm },
        { id: 'schedule', el: pSchedule },
        { id: 'documents', el: pDocs }
      ];

      panels.forEach(p => {
        if (p.el) {
          if (p.id === tabId) {
            p.el.classList.remove('hidden');
            p.el.style.setProperty('display', 'block', 'important');
          } else {
            p.el.classList.add('hidden');
            p.el.style.setProperty('display', 'none', 'important');
          }
        }
      });

      const btnOverview = document.getElementById('tab-btn-overview');
      const btnConfirm = document.getElementById('tab-btn-confirmations');
      const btnSchedule = document.getElementById('tab-btn-schedule');
      const btnDocs = document.getElementById('tab-btn-documents');

      const buttons = [
        { id: 'overview', el: btnOverview, activeClass: ['active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25'] },
        { id: 'confirmations', el: btnConfirm, activeClass: ['active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25'] },
        { id: 'schedule', el: btnSchedule, activeClass: ['active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25'] },
        { id: 'documents', el: btnDocs, activeClass: ['active-main-tab', 'bg-purple-600', 'text-white', 'shadow-lg', 'shadow-purple-600/25'] }
      ];

      buttons.forEach(b => {
        if (b.el) {
          b.el.classList.remove('active-main-tab', 'bg-gradient-to-r', 'from-sky-500', 'to-emerald-500', 'text-white', 'shadow-lg', 'shadow-sky-500/25', 'bg-purple-600', 'shadow-purple-600/25');
          b.el.classList.add('text-slate-300');

          if (b.id === tabId) {
            b.el.classList.add(...b.activeClass);
            b.el.classList.remove('text-slate-300');
          }
        }
      });

      currentTab = tabId;
      try {
        localStorage.setItem('alps_active_tab', tabId);
      } catch(e) {}
    }

    /* DOCUMENTS VAULT FILTERING LOGIC */
    let currentDocTraveler = 'all';
    let currentDocCategory = 'all';

    function setDocTraveler(trav) {
      currentDocTraveler = trav;
      document.querySelectorAll('.doc-trav-btn').forEach(btn => {
        btn.classList.remove('bg-slate-900', 'text-white', 'shadow-sm');
        btn.classList.add('bg-slate-100', 'text-slate-700', 'border', 'border-slate-200');
      });
      const activeId = trav === 'all' ? 'doc-filter-trav-all' : 
                       trav === 'Mark & Shelly' ? 'doc-filter-trav-matthews' :
                       trav === 'Bill & Kris' ? 'doc-filter-trav-rowe' : 'doc-filter-trav-shared';
      const activeBtn = document.getElementById(activeId);
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700', 'border', 'border-slate-200');
        activeBtn.classList.add('bg-slate-900', 'text-white', 'shadow-sm');
      }
      filterDocuments();
    }

    function setDocCategory(cat) {
      currentDocCategory = cat;
      document.querySelectorAll('.doc-cat-btn').forEach(btn => {
        btn.classList.remove('bg-purple-600', 'text-white', 'shadow-sm');
        btn.classList.add('bg-slate-100', 'text-slate-700', 'border', 'border-slate-200');
      });
      const activeId = cat === 'all' ? 'doc-filter-cat-all' :
                       cat === 'Train Tickets' ? 'doc-filter-cat-trains' :
                       cat === 'Hotel Confirmations' ? 'doc-filter-cat-lodging' :
                       cat === 'Car Rental' ? 'doc-filter-cat-car' :
                       cat === 'Tours & Lifts' ? 'doc-filter-cat-tours' : 'doc-filter-cat-guides';
      const activeBtn = document.getElementById(activeId);
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700', 'border', 'border-slate-200');
        activeBtn.classList.add('bg-purple-600', 'text-white', 'shadow-sm');
      }
      filterDocuments();
    }

    function filterDocuments() {
      const query = (document.getElementById('doc-search-input')?.value || '').trim().toLowerCase();
      const cityFilter = document.getElementById('doc-city-filter')?.value || 'all';
      const clearBtn = document.getElementById('doc-search-clear');
      if (clearBtn) {
        if (query.length > 0) clearBtn.classList.remove('hidden');
        else clearBtn.classList.add('hidden');
      }

      const cards = document.querySelectorAll('.doc-card');
      let visibleCount = 0;

      cards.forEach(card => {
        const cTraveler = card.getAttribute('data-traveler');
        const cCategory = card.getAttribute('data-category');
        const cCity = card.getAttribute('data-city') || '';
        const cSearch = card.getAttribute('data-search') || '';

        const matchesTraveler = (currentDocTraveler === 'all') || (cTraveler === currentDocTraveler);
        const matchesCategory = (currentDocCategory === 'all') || (cCategory === currentDocCategory);
        const matchesCity = (cityFilter === 'all') || (cCity.toLowerCase().includes(cityFilter.toLowerCase()));
        const matchesQuery = !query || cSearch.includes(query);

        if (matchesTraveler && matchesCategory && matchesCity && matchesQuery) {
          card.style.display = 'flex';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      const counter = document.getElementById('doc-results-counter');
      if (counter) counter.innerText = `${visibleCount} of ${cards.length}`;

      const emptyState = document.getElementById('docs-empty-state');
      if (emptyState) {
        if (visibleCount === 0) emptyState.classList.remove('hidden');
        else emptyState.classList.add('hidden');
      }
    }

    function clearDocSearch() {
      const input = document.getElementById('doc-search-input');
      if (input) {
        input.value = '';
        filterDocuments();
        input.focus();
      }
    }

    function resetDocFilters() {
      const input = document.getElementById('doc-search-input');
      if (input) input.value = '';
      const citySelect = document.getElementById('doc-city-filter');
      if (citySelect) citySelect.value = 'all';
      setDocTraveler('all');
      setDocCategory('all');
    }"""

if old_js_tab_logic in content:
    content = content.replace(old_js_tab_logic, new_js_tab_logic, 1)
    print("Updated JavaScript tab switching & filter logic.")
else:
    print("WARNING: Could not find old_js_tab_logic")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: index.html updated successfully.")
