# Europe Alpine Odyssey 2026 — Project Context & Conversation History

This document consolidates all context, architecture decisions, and feature developments established across the three prior planning sessions, linking directly to their original transcripts.

---

## 🔗 Incorporated Prior Conversations

1. **[Conversation 1: Initial Itinerary & High-Alpine Architecture](conversation://58863c92-0627-4aea-ae98-1076b4c0d55d)** (`58863c92-0627-4aea-ae98-1076b4c0d55d`)
   * **Core Scope:** Built the foundational 16-day European Alps itinerary spanning Germany (Bavaria), Austria (Salzburg & Innsbruck), Italy (Dolomites & Venice), and Switzerland (Bernina Express, Zermatt, Geneva).
   * **Artifacts Created:** Initial markdown itinerary guide (`Europe_Grand_Alpine_Tour_2026.md`), interactive single-page app (`itinerary.html`), hero imagery, and custom alpine topographic satellite relief maps.
   * **Formatting & Print:** Addressed early page-break formatting for PDF export and fixed header cutoff issues.

2. **[Conversation 2: GitHub Publishing, 3-Tab Architecture, Maps, PWA & Security](conversation://6256af95-2782-4114-85b1-30b101bf8d91)** (`6256af95-2782-4114-85b1-30b101bf8d91`)
   * **Excel Integration:** Ingested the master spreadsheet `September 2026 Europe Trip Itinerary V3.xlsx`.
   * **Travel Party Dynamics:** Explicitly acknowledged **Bill & Kris Rowe** as key trip curators and co-planners who designed much of the journey, alongside **Mark & Shelly Matthews**. All four are equal lead travelers.
   * **Madeline Consultation:** Noted upcoming session with travel planner **Madeline** (Monday evening, August 31) to finalize the Dolomites vehicle rental and Swiss segments (Tirano, Zermatt, Geneva).
   * **GitHub & Privacy:** Published to GitHub repo [`mrkm32/europe-trip-2026`](https://github.com/mrkm32/europe-trip-2026) with GitHub Pages. Added client-side SHA-256 passcode protection to keep personal travel details private, purged sensitive passwords and suggestions, and eliminated credential autofill triggers.
   * **Navigation Enhancements:** Added direct one-tap buttons for both **Apple Maps** and **Google Maps** on every hotel, transit hub, and excursion.
   * **Tab Restructuring:** Replaced long infinite scrolling with 3 dedicated tabs:
     1. `Overview` (Hero, Stats, Relief Map, Travel Notes)
     2. `Confirmations & Essential Contacts` (Master reservations table, emergency numbers, flight references)
     3. `Day-by-Day Expedition Schedule` (Full 16-day chronological timeline)
   * **Safari Tab Isolation:** Implemented strict DOM display toggling to resolve Safari-specific content leakage between tabs.
   * **PWA / Web App Support:** Added `manifest.json`, alpine touch icons (192px, 512px, apple-touch-icon), and an "Add as Web App" button with step-by-step iOS instructions and standalone mode detection.
   * **Print Booklet Support:** Implemented `triggerPrintBooklet()` with iOS AirPrint detection and clean pagination.

3. **[Conversation 3: Confirmations Print Pagination & Countdown to Adventure](conversation://42316458-a567-4346-a5a1-c640970ecdc4)** (`42316458-a567-4346-a5a1-c640970ecdc4`)
   * **Print Page Break Fixes:** Resolved orphaned cards and awkward table cutoffs in the Confirmations group using CSS `break-inside: avoid` and targeted print styling.
   * **"Countdown to Adventure":** Added a real-time countdown clock counting down to the outbound flight (Delta DL 164 departing MSP on September 4, 2026 at 9:45 PM CDT). Positioned in the header badge, confirmations summary, and Day 1 departure card.
   * **Version Bumps:** Advanced application through v3.10 and pushed directly to `origin/main`.
   * **Workspace Migration Request:** Initiated moving from scratch space into the permanent project workspace `/Users/markmatthews/Code/Euro Alps Trip`.

4. **Conversation 4: Madeline's Gmail Itinerary Integration (Venice, St. Moritz, Glacier Route, Zermatt & Geneva)**
   * **Gmail Details Integration:** Ingested Madeline's detailed travel itinerary:
     * **Wed Sep 16:** Venice check-out at Fortuny B&B, 7:00 AM water taxi to Santa Lucia station, 8:00 AM train to Tirano via Milan (arr 1:52 PM), 3:00 PM regional train along Bernina Route to St. Moritz (arr 5:11 PM). Check-in at Hotel Arte St. Moritz.
     * **Thu Sep 17:** St. Moritz to Zermatt across Switzerland on regional trains following the exact sold-out Glacier Express route with 4 connections (9:05 AM to Chur, 11:55 AM via Disentis to Andermatt, 3:37 PM via Brig to Zermatt arr 7:50 PM). Check-in at Hotel Beau Rivage Zermatt.
     * **Fri Sep 18:** Zermatt morning high-alpine excursion confirmed: **Option B — Matterhorn Glacier Paradise (3,883m)** & Glacier Palace via 3S cable cars, followed by 1:06 PM scenic train to Geneva via Visp (arr 4:55 PM). Check-in at Hotel New Midi Geneva. Old Town stroll & farewell celebration.
     * **Sat Sep 19:** 6:58 AM train to Geneva Airport (GVA arr 7:05 AM), 10:10 AM flight EI 0681 to Dublin with US CBP Preclearance, connecting to EI 0089 to MSP (arr 5:00 PM CDT).
   * **Application Updates:**
     * Upgraded web app to **v3.21**.
     * Confirmed **Option B: Matterhorn Glacier Paradise & Glacier Palace (Klein Matterhorn, 3,883m)** as the selected Day 15 morning excursion in both the schedule and confirmations luggage guidance.
     * Updated Interactive SVG Topographic Map: added St. Moritz pin and routing traces for the Bernina railway and the multi-segment Glacier Express regional rail corridor.
     * Replaced placeholder planning cards in `Confirmations` with verified lodging cards for Fortuny B&B, Hotel Arte, Hotel Beau Rivage, and Hotel New Midi, complete with 1-tap Apple Maps & Google Maps links.
     * Updated Day-by-Day schedule for Days 11 to 16 with full transport schedules, transfer buffers, and accommodation details.
     * Synchronized `Europe_Grand_Alpine_Tour_2026.md` and `README.md`.

5. **Conversation 5: Madeline's Axus Travel App Integration (Dolomites, Venice & Switzerland Confirmed Vouchers, Guides & Dining)**
   * **Axus Itinerary Data Ingestion:** Processed full shared Axus itinerary (`axustravelapp.com/shared/itinerary/4984d555-2c81-4965-8866-a8c1b59ee77e`) containing all confirmed vouchers, exact booking references, seat assignments, dispatch contacts, and dining recommendations.
   * **Key Logistics Incorporated:**
     * **Dedicated Support:** Added Rebecca (`+39 331 222 2349`, WhatsApp) and Madeline Jhawar (`+1 773 621 3024`, WhatsApp) to 24/7 Emergency Contacts.
     * **Car Rental (Auto Europe / Europcar):** Voucher `#745646711`, Europcar `#1206017591`, Peugeot 508 SW SWAR Diesel Automatic, pickup Bolzano Airport (Sep 11 @ 12 PM), drop Venice Piazzale Roma 496 (Sep 14 @ 12 PM). William Rowe primary driver.
     * **Venice Private Water Taxis (VLS Agency):** Dispatch `+39 345 1879941`. Sep 14 transfer (€120 prepaid) 3 Ponti ➔ S. Angelo; Sep 16 early 6:30 AM transfer (€140 prepaid) S. Angelo ➔ Santa Lucia station.
     * **Venice Private Guided Tours (Maria Andrea):** Certified guide `+39 388 642 0499`. Sep 14 (4–7 PM) Intro Walking Tour (€270 prepaid); Sep 15 (10 AM–1 PM) Doge's Palace & St. Mark's Basilica VIP Tour (€510 prepaid incl tickets).
     * **Hotel Bookings & Exact Rooms:**
       * Hotel Pension Rezia (La Villa): Res `#R3653`, 2 x Mansard rooms (35m² with balconies), pre-check-in completed, spa 4–7 PM.
       * B&B Fortuny (Venice): Ref `TY78554084-1`, Canal View (Matthews) & Courtyard View (Rowe).
       * Hotel Arte St. Moritz: Ref `2026080150736583` (Matthews) & `2026080150736489` (Rowe), Double Balcony rooms.
       * Beau-Rivage Hotel Garni (Zermatt): Ref `60682436` (Matthews, Double Standard Valley) & `60682402` (Rowe, Double Queen Valley).
       * The New Midi Geneva: Ref `1091654581` (Matthews) & `1091652434` (Rowe), Superior River View rooms.
     * **Swiss & Italian Rail Details:** ÖBB Railjet 81 (Coach 261, Seats 111, 116, 113, 115); Frecciarossa 9713 (Coach 3 Business, Seats 15A/B, 16A/B); Bernina RE 1660 (Coach 3 1st Class, Seats 11, 12, 21, 22); Glacier route regional trains with tight 6-min connection alert at Disentis.
     * **Dining Reservations & Recommendations:** Added verified lunch and dinner venues across Ortisei (Tubladel), San Cassiano (Mumant, La Raisc, Armentarola), Venice (Rosa Rossa, Da Cherubino, Bistrot de Venise, Testiere, Ai Assassini), St. Moritz (La Stalla, Lapin Bleu), Andermatt (Bahnhofbuffet), Zermatt (Chez Max Julen, Spycher), and Geneva (Café PAPON, Bistrot du Bœuf Rouge).
   * **Version Upgrade:** Bumped web app to **v3.30**.
   * **Full Documentation Sync:** Updated `index.html`, `Europe_Grand_Alpine_Tour_2026.md`, `README.md`, and `PROJECT_HISTORY.md`.

6. **Conversation 6: Scheduled Monitoring of Axus Itinerary & Foreign Currency/ATM Strategy (v3.31)**
   * **Automated Cron Schedule for Axus Updates:**
     * Configured background daemon cron (`0 8,14,20 * * *`, 3x daily at 8 AM, 2 PM, 8 PM through Sep 19 return) to monitor Madeline's live Axus itinerary URL for changes and notify the user if adjustments occur.
   * **Foreign Currency & ATM Banking Strategy Incorporated:**
     * **Euros in Munich (Deutsche Bank Filiale):** Located at Schwanthalerstraße 32 (less than 1-minute walk / 40m right of Boutique Hotel Germania entrance). 24/7 self-service indoor lobby with secure ATMs. $0.00 local German ATM surcharge.
     * **Swiss Francs (UBS Switzerland AG / Cantonal Banks):** Primary recommendation upon Swiss arrival in St. Moritz (Wed Sep 16) at UBS Switzerland AG (Plazza da Scoula 10, 8-min walk) or GKB Bancomat at St. Moritz Bahnhof concourse. Secondary backup at UBS Zermatt (Bahnhofstrasse 37) / BCVs (Bahnhofstrasse 24).
     * **USAA Debit Card Fee Architecture:** Confirmed $0.00 local bank fee for foreign debit cards at official branches; USAA charges only a standard 1% foreign transaction fee (~$1.65 on €150).
     * **The Golden Rule on Dynamic Currency Conversion (DCC):** Always select *"Without Conversion / Settle in EUR or CHF"* to force card network wholesale mid-market rate and avoid 5%–15% ATM owner markups. Avoid standalone Euronet kiosks.
   * **Application & Documentation Updates:**
     * Upgraded web app to **v3.31**.
     * Added **Official Bank & ATM Cash Strategy** wallet card in Confirmations tab.
     * Added interactive map links & callout tips in Day 2, Day 13, and Day 14 schedule cards.
     * Updated Overview Quick Facts currency card and synchronized `Europe_Grand_Alpine_Tour_2026.md` and `README.md`.

---

## 👥 Travel Party & Planning Status

* **Bill & Kris Rowe:** Trip Curators & Co-Planners (spearheading itinerary details; full 16-day journey from MSP).
* **Mark & Shelly Matthews:** Co-Planners & Travelers (Flight confs DL `GYXLN6`, Aer Lingus `2AXKMS`, Hotels.com bookings).
* **Madeline Jhawar & Rebecca (Italy Beyond the Obvious):** Professional travel planners for Italy & Switzerland segments; all bookings, vouchers, private tours, and rail passes fully confirmed in Axus.

---

## 💻 Project Architecture & Local Assets

* **Repository:** [`https://github.com/mrkm32/europe-trip-2026.git`](https://github.com/mrkm32/europe-trip-2026.git) (`main` branch)
* **Live Site:** `https://mrkm32.github.io/europe-trip-2026/`
* **Local Workspace:** `/Users/markmatthews/Code/Euro Alps Trip`
* **Key Files:**
  * `index.html`: Complete standalone web app (Tailwind CSS, Font Awesome, Passcode guard, PWA support, Tab navigation, Maps links, Countdown timer, Print formatting).
  * `manifest.json`: Web App Manifest for mobile installation.
  * `apple-touch-icon.png`, `icon-192.png`, `icon-512.png`: App icons for iOS & Android.
  * `hero.jpg` & `alps_map.jpg`: Local high-resolution photography and satellite terrain relief map.
  * `September 2026 Europe Trip Itinerary V3.xlsx`: Source spreadsheet downloaded from travel planners.
  * `Europe_Grand_Alpine_Tour_2026.md`: Comprehensive reference guide of the entire 16-day expedition.
  * `README.md`: GitHub repository documentation.
