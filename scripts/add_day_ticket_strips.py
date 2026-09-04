INDEX_PATH = "/Users/markmatthews/Code/Euro Alps Trip/index.html"

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    content = f.read()

def make_strip(title, links):
    links_html = "\n".join([
        f'    <a href="{href}" target="_blank" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white hover:bg-purple-100 text-purple-900 border border-purple-200 font-semibold text-[11px] shadow-sm transition">'
        f'<svg class="w-3 h-3 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>'
        f'<span>{lbl}</span></a>'
        for lbl, href in links
    ])
    return f"""
            <!-- Contextual Document Vault Strip -->
            <div class="mt-3 p-3 bg-purple-50/80 rounded-xl border border-purple-200/80 text-xs no-print">
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="font-bold text-purple-950 flex items-center gap-1.5 text-xs">
                  <svg class="w-4 h-4 text-purple-600 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"/></svg>
                  <span>{title}</span>
                </span>
                <button onclick="switchMainTab('documents')" class="text-[11px] font-bold text-purple-700 hover:text-purple-900 underline">
                  All 39 Docs ➔
                </button>
              </div>
              <div class="flex flex-wrap items-center gap-1.5">
{links_html}
              </div>
            </div>"""

# Day 7 Strip
day7_links = [
    ("ÖBB Train (Mark & Shelly)", "documents/trains/matthews/01_Innsbruck_to_Bolzano_Train_Tickets_Matthews.pdf"),
    ("ÖBB Train (Bill & Kris)", "documents/trains/rowe/01_Innsbruck_to_Bolzano_Train_Tickets_Rowe.pdf"),
    ("Train Details & Map", "documents/trains/shared/Innsbruck_to_Bolzano_Train_Details.png"),
    ("Hertz Rental Voucher", "documents/rental_car/Car_Rental_Voucher_Rowe.pdf"),
    ("Hertz Confirmation", "documents/rental_car/Car_Rental_Confirmation_Rowe.pdf"),
    ("Driving in Italy Ebook", "documents/rental_car/IBTO_Driving_in_Italy_Ebook.pdf"),
    ("Hotel Rezia (Mark & Shelly)", "documents/lodging/Hotel_Rezia_Confirmation_Matthews.pdf"),
    ("Hotel Rezia (Bill & Kris)", "documents/lodging/Hotel_Rezia_Confirmation_Rowe.pdf"),
]
day7_strip = make_strip("Day 7 Official Tickets & Vouchers", day7_links)

# Day 10 Strip (Venice Arrival & Fortuny)
day10_links = [
    ("B&B Fortuny (Mark & Shelly)", "documents/lodging/BB_Fortuny_Confirmation_Matthews.pdf"),
    ("B&B Fortuny (Bill & Kris)", "documents/lodging/BB_Fortuny_Confirmation_Rowe.pdf"),
    ("Fortuny Arrival Walking Map", "documents/lodging/BB_Fortuny_Arrival_Map.pdf"),
]
day10_strip = make_strip("Venice Arrival & B&B Fortuny Vouchers", day10_links)

# Day 11 Strip (Venice Tours)
day11_links = [
    ("Venice Tours Receipt (Mark & Shelly)", "documents/tours_excursions/Venice_Tours_Payment_Matthews.pdf"),
    ("Venice Tours Receipt (Bill & Kris)", "documents/tours_excursions/Venice_Tours_Payment_Rowe.pdf"),
]
day11_strip = make_strip("Venice Private Tour Receipts", day11_links)

# Day 13 Strip (Venice to St. Moritz)
day13_links = [
    ("Venice ➔ Mestre (Mark & Shelly)", "documents/trains/matthews/02_Venice_SL_to_Mestre_Train_Tickets_Matthews.pdf"),
    ("Venice ➔ Mestre (Bill & Kris)", "documents/trains/rowe/02_Venice_SL_to_Mestre_Train_Tickets_Rowe.pdf"),
    ("Mestre ➔ Tirano (Mark & Shelly)", "documents/trains/matthews/03_Venice_Mestre_to_Tirano_Train_Tickets_Matthews.pdf"),
    ("Mestre ➔ Tirano (Bill & Kris)", "documents/trains/rowe/03_Venice_Mestre_to_Tirano_Train_Tickets_Rowe.pdf"),
    ("Bernina Express (Mark & Shelly)", "documents/trains/matthews/04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews.pdf"),
    ("Bernina Express (Bill & Kris)", "documents/trains/rowe/04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe.pdf"),
    ("Hotel Arte (Mark & Shelly)", "documents/lodging/Hotel_Arte_St_Moritz_Confirmation_Matthews.pdf"),
    ("Hotel Arte (Bill & Kris)", "documents/lodging/Hotel_Arte_St_Moritz_Confirmation_Rowe.pdf"),
]
day13_strip = make_strip("Day 13 Train Tickets & St. Moritz Voucher", day13_links)

# Day 14 Strip (St. Moritz to Zermatt)
day14_links = [
    ("St. Moritz ➔ Chur (Mark & Shelly)", "documents/trains/matthews/05_St_Moritz_to_Chur_Train_Tickets_Matthews.pdf"),
    ("St. Moritz ➔ Chur (Bill & Kris)", "documents/trains/rowe/05_St_Moritz_to_Chur_Train_Tickets_Rowe.pdf"),
    ("Chur ➔ Andermatt (Mark & Shelly)", "documents/trains/matthews/06_Chur_to_Andermatt_Train_Tickets_Matthews.pdf"),
    ("Chur ➔ Andermatt (Bill & Kris)", "documents/trains/rowe/06_Chur_to_Andermatt_Train_Tickets_Rowe.pdf"),
    ("Andermatt ➔ Zermatt (Mark & Shelly)", "documents/trains/matthews/07_Andermatt_to_Zermatt_Train_Tickets_Matthews.pdf"),
    ("Andermatt ➔ Zermatt (Bill & Kris)", "documents/trains/rowe/07_Andermatt_to_Zermatt_Train_Tickets_Rowe.pdf"),
    ("Hotel Beau-Rivage (Mark & Shelly)", "documents/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Matthews.pdf"),
    ("Hotel Beau-Rivage (Bill & Kris)", "documents/lodging/Hotel_Beau_Rivage_Zermatt_Confirmation_Rowe.pdf"),
]
day14_strip = make_strip("Day 14 Glacier Route Train Tickets & Zermatt Voucher", day14_links)

# Day 15 Strip (Zermatt to Geneva)
day15_links = [
    ("Gornergrat Train Timetable", "documents/trains/shared/Zermatt_to_Gornergrat_Train_Schedule.pdf"),
    ("Zermatt ➔ Geneva (Mark & Shelly)", "documents/trains/matthews/08_Zermatt_to_Geneva_Train_Tickets_Matthews.pdf"),
    ("Zermatt ➔ Geneva (Bill & Kris)", "documents/trains/rowe/08_Zermatt_to_Geneva_Train_Tickets_Rowe.pdf"),
    ("The New Midi Geneva (Mark & Shelly)", "documents/lodging/The_New_Midi_Geneva_Confirmation_Matthews.pdf"),
    ("The New Midi Geneva (Bill & Kris)", "documents/lodging/The_New_Midi_Geneva_Confirmation_Rowe.pdf"),
]
day15_strip = make_strip("Day 15 Zermatt ➔ Geneva Train Tickets & Hotel Voucher", day15_links)

# Day 16 Strip (Geneva to Airport)
day16_links = [
    ("Geneva ➔ Airport Express (Mark & Shelly)", "documents/trains/matthews/09_Geneva_to_Airport_Train_Tickets_Matthews.pdf"),
    ("Geneva ➔ Airport Express (Bill & Kris)", "documents/trains/rowe/09_Geneva_to_Airport_Train_Tickets_Rowe.pdf"),
]
day16_strip = make_strip("Airport Train Tickets", day16_links)

# Insert into Day 7
# Look for closing of Day 7: <!-- DAY 8
if '<!-- DAY 8' in content:
    idx = content.find('<!-- DAY 8')
    # find the preceding </div> before DAY 8
    div_idx = content.rfind('</div>', 0, idx)
    content = content[:div_idx] + day7_strip + "\n        </div>\n\n        " + content[idx:]
    print("Inserted Day 7 strip.")

# Insert into Day 10
if '<!-- DAY 11' in content:
    idx = content.find('<!-- DAY 11')
    div_idx = content.rfind('</div>', 0, idx)
    content = content[:div_idx] + day10_strip + "\n        </div>\n\n        " + content[idx:]
    print("Inserted Day 10 strip.")

# Insert into Day 11
if '<!-- DAY 12' in content:
    idx = content.find('<!-- DAY 12')
    div_idx = content.rfind('</div>', 0, idx)
    content = content[:div_idx] + day11_strip + "\n        </div>\n\n        " + content[idx:]
    print("Inserted Day 11 strip.")

# Insert into Day 13
if '<!-- DAY 14' in content:
    idx = content.find('<!-- DAY 14')
    div_idx = content.rfind('</div>', 0, idx)
    content = content[:div_idx] + day13_strip + "\n        </div>\n\n        " + content[idx:]
    print("Inserted Day 13 strip.")

# Insert into Day 14
if '<!-- DAY 15' in content:
    idx = content.find('<!-- DAY 15')
    div_idx = content.rfind('</div>', 0, idx)
    content = content[:div_idx] + day14_strip + "\n        </div>\n\n        " + content[idx:]
    print("Inserted Day 14 strip.")

# Insert into Day 15
if '<!-- DAY 16' in content:
    idx = content.find('<!-- DAY 16')
    div_idx = content.rfind('</div>', 0, idx)
    content = content[:div_idx] + day15_strip + "\n        </div>\n\n        " + content[idx:]
    print("Inserted Day 15 strip.")

# Insert into Day 16
# Look for </section> before </main>
if '</section>' in content:
    idx = content.find('</section>')
    div_idx = content.rfind('</div>', 0, idx)
    content = content[:div_idx] + day16_strip + "\n        </div>\n\n      " + content[idx:]
    print("Inserted Day 16 strip.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("SUCCESS: Finished adding day ticket strips!")
