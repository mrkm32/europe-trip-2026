#!/usr/bin/env python3
"""
Downloads and organizes all 39 supporting travel documents from Madeline's Axus itinerary.
Categorizes them with mobile-optimized display titles, traveler tags, category tags, city tags, and day numbers.
"""

import os
import re
import json
import urllib.request
from html.parser import HTMLParser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(BASE_DIR, "documents")

AXUS_URL = "https://axustravelapp.com/shared/itinerary/4984d555-2c81-4965-8866-a8c1b59ee77e"

# Mapping of raw Axus document text to clean, mobile-optimized display metadata and storage paths
# Designed specifically so iPhone 15/16 screens display clean, concise route titles and clear traveler badges
DOC_MAPPINGS = [
    # 1. On-Trip Support
    {
        "raw_name": "On-Trip Support Overview.pdf",
        "folder": "guides_support",
        "file_name": "On_Trip_Support_Overview_IBTO.pdf",
        "title": "On-Trip Support & Emergency Contacts",
        "subtitle": "Madeline & Rebecca (Italy Beyond the Obvious)",
        "traveler": "Shared",
        "category": "Guides & Support",
        "city": "General",
        "day": "Days 1–16"
    },
    # 2. Innsbruck to Bolzano
    {
        "raw_name": "Innsbruck to Bolzano Train Details Rowe Matthews.png",
        "folder": "trains/shared",
        "file_name": "Innsbruck_to_Bolzano_Train_Details.png",
        "title": "Innsbruck ➔ Bolzano Train Details",
        "subtitle": "ÖBB Railjet 81 Route, Transit Info & Map",
        "traveler": "Shared",
        "category": "Train Tickets",
        "city": "Innsbruck / Bolzano",
        "day": "Day 5 • Tue Sep 8"
    },
    {
        "raw_name": "Innsbruck to Bolzano Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "01_Innsbruck_to_Bolzano_Train_Tickets_Rowe.pdf",
        "title": "Innsbruck ➔ Bolzano Train Tickets",
        "subtitle": "ÖBB Railjet 81 (Seats 113 & 115)",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "Innsbruck / Bolzano",
        "day": "Day 5 • Tue Sep 8"
    },
    {
        "raw_name": "Innsbruck to Bolzano Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "01_Innsbruck_to_Bolzano_Train_Tickets_Matthews.pdf",
        "title": "Innsbruck ➔ Bolzano Train Tickets",
        "subtitle": "ÖBB Railjet 81 (Seats 111 & 116)",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "Innsbruck / Bolzano",
        "day": "Day 5 • Tue Sep 8"
    },
    # 3. Car Rental & Driving Ebook
    {
        "raw_name": "Car Rental Confirmation Rowe William.pdf",
        "folder": "rental_car",
        "file_name": "Car_Rental_Confirmation_Rowe.pdf",
        "title": "Hertz Car Rental Confirmation",
        "subtitle": "Bolzano Pickup ➔ Venice Piazzale Roma Return",
        "traveler": "Bill & Kris",
        "category": "Car Rental",
        "city": "Bolzano / Venice",
        "day": "Days 5–10"
    },
    {
        "raw_name": "Car Rental Voucher Rowe William.pdf",
        "folder": "rental_car",
        "file_name": "Car_Rental_Voucher_Rowe.pdf",
        "title": "Hertz Car Rental Voucher",
        "subtitle": "Official Booking Voucher for Counter Presentation",
        "traveler": "Bill & Kris",
        "category": "Car Rental",
        "city": "Bolzano / Venice",
        "day": "Days 5–10"
    },
    {
        "raw_name": "IBTO Driving Ebook.pdf",
        "folder": "rental_car",
        "file_name": "IBTO_Driving_in_Italy_Ebook.pdf",
        "title": "Driving in Italy Guide & Ebook",
        "subtitle": "ZTL zones, tolls, speed limits & road rules",
        "traveler": "Shared",
        "category": "Car Rental",
        "city": "Italy",
        "day": "Days 5–10"
    },
    # 4. Hotel Rezia (La Villa)
    {
        "raw_name": "Hotel Rezia Confirmation Rowe.pdf",
        "folder": "lodging",
        "file_name": "Hotel_Rezia_Confirmation_Rowe.pdf",
        "title": "Hotel Pension Rezia Voucher",
        "subtitle": "Mansard Room (La Villa / Badia)",
        "traveler": "Bill & Kris",
        "category": "Hotel Confirmations",
        "city": "Dolomites",
        "day": "Days 5–10"
    },
    {
        "raw_name": "Hotel Rezia Confirmation Matthews.pdf",
        "folder": "lodging",
        "file_name": "Hotel_Rezia_Confirmation_Matthews.pdf",
        "title": "Hotel Pension Rezia Voucher",
        "subtitle": "Mansard Room (La Villa / Badia)",
        "traveler": "Mark & Shelly",
        "category": "Hotel Confirmations",
        "city": "Dolomites",
        "day": "Days 5–10"
    },
    # 5. Cable Cars Dolomites
    {
        "raw_name": "Piz La Ila, Boé Gondola etc Cable Car Prices&Schedule.pdf",
        "folder": "tours_excursions",
        "file_name": "Dolomites_Cable_Car_Prices_Schedule_Boe.pdf",
        "title": "Dolomites Cable Cars Schedule & Prices",
        "subtitle": "Piz La Ila, Boé Gondola & Alta Badia Lifts",
        "traveler": "Shared",
        "category": "Tours & Lifts",
        "city": "Dolomites",
        "day": "Days 6–9"
    },
    {
        "raw_name": "La Crusc Lift Prices.png",
        "folder": "tours_excursions",
        "file_name": "Dolomites_La_Crusc_Lift_Prices.png",
        "title": "La Crusc Chairlift Prices & Timetable",
        "subtitle": "Santa Croce & Armentara Meadows Excursion",
        "traveler": "Shared",
        "category": "Tours & Lifts",
        "city": "Dolomites",
        "day": "Day 8 • Fri Sep 11"
    },
    # 6. B&B Fortuny (Venice)
    {
        "raw_name": "B&B Fortuny Map.pdf",
        "folder": "lodging",
        "file_name": "BB_Fortuny_Arrival_Map.pdf",
        "title": "B&B Fortuny Arrival Walking Map",
        "subtitle": "Directions from S. Angelo Water Taxi Dock",
        "traveler": "Shared",
        "category": "Hotel Confirmations",
        "city": "Venice",
        "day": "Days 10–13"
    },
    {
        "raw_name": "B&B Fortuny Confirmation Rowe.pdf",
        "folder": "lodging",
        "file_name": "BB_Fortuny_Confirmation_Rowe.pdf",
        "title": "B&B Fortuny Venice Voucher",
        "subtitle": "Courtyard View Room (Ref: TY78554084-1)",
        "traveler": "Bill & Kris",
        "category": "Hotel Confirmations",
        "city": "Venice",
        "day": "Days 10–13"
    },
    {
        "raw_name": "B&B Fortuny Confirmation Matthews.pdf",
        "folder": "lodging",
        "file_name": "BB_Fortuny_Confirmation_Matthews.pdf",
        "title": "B&B Fortuny Venice Voucher",
        "subtitle": "Canal View Room (Ref: TY78554084-1)",
        "traveler": "Mark & Shelly",
        "category": "Hotel Confirmations",
        "city": "Venice",
        "day": "Days 10–13"
    },
    # 7. Venice Tours Payment
    {
        "raw_name": "Venice Tours Payment Rowe.pdf",
        "folder": "tours_excursions",
        "file_name": "Venice_Tours_Payment_Rowe.pdf",
        "title": "Venice Private Tours Receipt",
        "subtitle": "St. Mark's Basilica & Doge's Palace VIP Guide",
        "traveler": "Bill & Kris",
        "category": "Tours & Lifts",
        "city": "Venice",
        "day": "Day 11 • Mon Sep 14"
    },
    {
        "raw_name": "Venice Tours Payment Matthews.pdf",
        "folder": "tours_excursions",
        "file_name": "Venice_Tours_Payment_Matthews.pdf",
        "title": "Venice Private Tours Receipt",
        "subtitle": "St. Mark's Basilica & Doge's Palace VIP Guide",
        "traveler": "Mark & Shelly",
        "category": "Tours & Lifts",
        "city": "Venice",
        "day": "Day 11 • Mon Sep 14"
    },
    # 8. Train: Venice Santa Lucia to Mestre
    {
        "raw_name": "Venice Santa Lucia to Venice Mestre Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "02_Venice_SL_to_Mestre_Train_Tickets_Matthews.pdf",
        "title": "Venice S.L. ➔ Venice Mestre Tickets",
        "subtitle": "Regionale Veloce 3644 (7:31 AM – 7:41 AM)",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "Venice",
        "day": "Day 13 • Wed Sep 16"
    },
    {
        "raw_name": "Venice Santa Lucia to Venice Mestre Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "02_Venice_SL_to_Mestre_Train_Tickets_Rowe.pdf",
        "title": "Venice S.L. ➔ Venice Mestre Tickets",
        "subtitle": "Regionale Veloce 3644 (7:31 AM – 7:41 AM)",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "Venice",
        "day": "Day 13 • Wed Sep 16"
    },
    # 9. Train: Venice Mestre to Tirano (via Milan)
    {
        "raw_name": "Venice Mestre to Tirano Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "03_Venice_Mestre_to_Tirano_Train_Tickets_Rowe.pdf",
        "title": "Venice Mestre ➔ Tirano Tickets",
        "subtitle": "Frecciarossa 9713 + Trenord 2822 (Seats 16A/B)",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "Venice / Milan / Tirano",
        "day": "Day 13 • Wed Sep 16"
    },
    {
        "raw_name": "Venice Mestre to Tirano Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "03_Venice_Mestre_to_Tirano_Train_Tickets_Matthews.pdf",
        "title": "Venice Mestre ➔ Tirano Tickets",
        "subtitle": "Frecciarossa 9713 + Trenord 2822 (Seats 15A/B)",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "Venice / Milan / Tirano",
        "day": "Day 13 • Wed Sep 16"
    },
    # 10. Train: Tirano to St. Moritz (Bernina Route)
    {
        "raw_name": "Tirano to St. Moritz Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "04_Tirano_to_St_Moritz_Bernina_Tickets_Rowe.pdf",
        "title": "Tirano ➔ St. Moritz (Bernina Line)",
        "subtitle": "Bernina RE 1660 1st Class (Seats 21 & 22)",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "Tirano / St. Moritz",
        "day": "Day 13 • Wed Sep 16"
    },
    {
        "raw_name": "Tirano to St. Moritz Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "04_Tirano_to_St_Moritz_Bernina_Tickets_Matthews.pdf",
        "title": "Tirano ➔ St. Moritz (Bernina Line)",
        "subtitle": "Bernina RE 1660 1st Class (Seats 11 & 12)",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "Tirano / St. Moritz",
        "day": "Day 13 • Wed Sep 16"
    },
    # 11. Hotel Arte St. Moritz
    {
        "raw_name": "Hotel Arte St. Moritz Confirmation Rowe.pdf",
        "folder": "lodging",
        "file_name": "Hotel_Arte_St_Moritz_Confirmation_Rowe.pdf",
        "title": "Hotel Arte St. Moritz Voucher",
        "subtitle": "Double Balcony Room (Ref: 2026080150736489)",
        "traveler": "Bill & Kris",
        "category": "Hotel Confirmations",
        "city": "St. Moritz",
        "day": "Day 13 • Wed Sep 16"
    },
    {
        "raw_name": "Hotel Arte St. Moritz Confirmation Matthews.pdf",
        "folder": "lodging",
        "file_name": "Hotel_Arte_St_Moritz_Confirmation_Matthews.pdf",
        "title": "Hotel Arte St. Moritz Voucher",
        "subtitle": "Double Balcony Room (Ref: 2026080150736583)",
        "traveler": "Mark & Shelly",
        "category": "Hotel Confirmations",
        "city": "St. Moritz",
        "day": "Day 13 • Wed Sep 16"
    },
    # 12. Train: St. Moritz to Chur
    {
        "raw_name": "St. Moritz to Chur Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "05_St_Moritz_to_Chur_Train_Tickets_Rowe.pdf",
        "title": "St. Moritz ➔ Chur Train Tickets",
        "subtitle": "Train IR 1128 across Landwasser Viaduct",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "St. Moritz / Chur",
        "day": "Day 14 • Thu Sep 17"
    },
    {
        "raw_name": "St. Moritz to Chur Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "05_St_Moritz_to_Chur_Train_Tickets_Matthews.pdf",
        "title": "St. Moritz ➔ Chur Train Tickets",
        "subtitle": "Train IR 1128 across Landwasser Viaduct",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "St. Moritz / Chur",
        "day": "Day 14 • Thu Sep 17"
    },
    # 13. Train: Chur to Andermatt (Rhine Gorge)
    {
        "raw_name": "Chur to Andermatt Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "06_Chur_to_Andermatt_Train_Tickets_Rowe.pdf",
        "title": "Chur ➔ Andermatt Train Tickets",
        "subtitle": "RE 1737 Rhine Gorge (Disentis Connection)",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "Chur / Andermatt",
        "day": "Day 14 • Thu Sep 17"
    },
    {
        "raw_name": "Chur to Andermatt Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "06_Chur_to_Andermatt_Train_Tickets_Matthews.pdf",
        "title": "Chur ➔ Andermatt Train Tickets",
        "subtitle": "RE 1737 Rhine Gorge (Disentis Connection)",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "Chur / Andermatt",
        "day": "Day 14 • Thu Sep 17"
    },
    # 14. Train: Andermatt to Zermatt
    {
        "raw_name": "Andermatt to Zermatt Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "07_Andermatt_to_Zermatt_Train_Tickets_Rowe.pdf",
        "title": "Andermatt ➔ Zermatt Train Tickets",
        "subtitle": "Train R 557 + R 257 up Matter Valley",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "Andermatt / Zermatt",
        "day": "Day 14 • Thu Sep 17"
    },
    {
        "raw_name": "Andermatt to Zermatt Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "07_Andermatt_to_Zermatt_Train_Tickets_Matthews.pdf",
        "title": "Andermatt ➔ Zermatt Train Tickets",
        "subtitle": "Train R 557 + R 257 up Matter Valley",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "Andermatt / Zermatt",
        "day": "Day 14 • Thu Sep 17"
    },
    # 15. Hotel Beau Rivage (Zermatt)
    {
        "raw_name": "Hotel Beau Rivage Confirmation Rowe.pdf",
        "folder": "lodging",
        "file_name": "Hotel_Beau_Rivage_Zermatt_Confirmation_Rowe.pdf",
        "title": "Hotel Beau-Rivage Zermatt Voucher",
        "subtitle": "Double Queen Valley (Ref: 60682402)",
        "traveler": "Bill & Kris",
        "category": "Hotel Confirmations",
        "city": "Zermatt",
        "day": "Day 14 • Thu Sep 17"
    },
    {
        "raw_name": "Hotel Beau Rivage Confirmation Matthews.pdf",
        "folder": "lodging",
        "file_name": "Hotel_Beau_Rivage_Zermatt_Confirmation_Matthews.pdf",
        "title": "Hotel Beau-Rivage Zermatt Voucher",
        "subtitle": "Double Standard Valley (Ref: 60682436)",
        "traveler": "Mark & Shelly",
        "category": "Hotel Confirmations",
        "city": "Zermatt",
        "day": "Day 14 • Thu Sep 17"
    },
    # 16. Gornergrat Schedule
    {
        "raw_name": "Zermatt to Gornergrat Train Schedule.pdf",
        "folder": "trains/shared",
        "file_name": "Zermatt_to_Gornergrat_Train_Schedule.pdf",
        "title": "Zermatt ➔ Gornergrat Train Timetable",
        "subtitle": "Cogwheel Railway Departure Schedule & Info",
        "traveler": "Shared",
        "category": "Train Tickets",
        "city": "Zermatt",
        "day": "Day 15 • Fri Sep 18"
    },
    # 17. Train: Zermatt to Geneva
    {
        "raw_name": "Zermatt to Geneva Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "08_Zermatt_to_Geneva_Train_Tickets_Rowe.pdf",
        "title": "Zermatt ➔ Geneva Train Tickets",
        "subtitle": "Train R 344 + IR 1824 via Lake Geneva",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "Zermatt / Geneva",
        "day": "Day 15 • Fri Sep 18"
    },
    {
        "raw_name": "Zermatt to Geneva Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "08_Zermatt_to_Geneva_Train_Tickets_Matthews.pdf",
        "title": "Zermatt ➔ Geneva Train Tickets",
        "subtitle": "Train R 344 + IR 1824 via Lake Geneva",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "Zermatt / Geneva",
        "day": "Day 15 • Fri Sep 18"
    },
    # 18. The New Midi (Geneva)
    {
        "raw_name": "The New Midi Geneva Confirmation Rowe.pdf",
        "folder": "lodging",
        "file_name": "The_New_Midi_Geneva_Confirmation_Rowe.pdf",
        "title": "The New Midi Geneva Voucher",
        "subtitle": "Superior River View (Ref: 1091652434)",
        "traveler": "Bill & Kris",
        "category": "Hotel Confirmations",
        "city": "Geneva",
        "day": "Day 15 • Fri Sep 18"
    },
    {
        "raw_name": "The New Midi Geneva Confirmation Matthews.pdf",
        "folder": "lodging",
        "file_name": "The_New_Midi_Geneva_Confirmation_Matthews.pdf",
        "title": "The New Midi Geneva Voucher",
        "subtitle": "Superior River View (Ref: 1091654581)",
        "traveler": "Mark & Shelly",
        "category": "Hotel Confirmations",
        "city": "Geneva",
        "day": "Day 15 • Fri Sep 18"
    },
    # 19. Train: Geneva to Airport
    {
        "raw_name": "Geneva to Geneva Airport Train Tickets Rowe.pdf",
        "folder": "trains/rowe",
        "file_name": "09_Geneva_to_Airport_Train_Tickets_Rowe.pdf",
        "title": "Geneva ➔ Airport Train Tickets",
        "subtitle": "Cornavin to GVA Terminal 1 (7-min express)",
        "traveler": "Bill & Kris",
        "category": "Train Tickets",
        "city": "Geneva",
        "day": "Day 16 • Sat Sep 19"
    },
    {
        "raw_name": "Geneva to Geneva Airport Train Tickets Matthews.pdf",
        "folder": "trains/matthews",
        "file_name": "09_Geneva_to_Airport_Train_Tickets_Matthews.pdf",
        "title": "Geneva ➔ Airport Train Tickets",
        "subtitle": "Cornavin to GVA Terminal 1 (7-min express)",
        "traveler": "Mark & Shelly",
        "category": "Train Tickets",
        "city": "Geneva",
        "day": "Day 16 • Sat Sep 19"
    }
]

class AxusHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_a = None
        self.doc_urls = {}

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            attrs_dict = dict(attrs)
            href = attrs_dict.get("href", "")
            if ".pdf" in href.lower() or "supporting-documents" in href.lower():
                self.current_a = {"href": href, "text": ""}

    def handle_endtag(self, tag):
        if tag == "a" and self.current_a:
            text = self.current_a["text"].strip()
            if text:
                self.doc_urls[text] = self.current_a["href"]
            self.current_a = None

    def handle_data(self, data):
        if self.current_a:
            self.current_a["text"] += data.strip() + " "

def download_all():
    print(f"Fetching Axus HTML from {AXUS_URL}...")
    req = urllib.request.Request(AXUS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8")

    parser = AxusHTMLParser()
    parser.feed(html)
    found_urls = parser.doc_urls
    print(f"Extracted {len(found_urls)} unique documents from Axus.")

    catalog = []
    success_count = 0

    for item in DOC_MAPPINGS:
        raw = item["raw_name"]
        url = found_urls.get(raw)
        if not url:
            # Fallback search if slight whitespace difference
            for k, v in found_urls.items():
                if raw.lower().replace(" ", "") in k.lower().replace(" ", ""):
                    url = v
                    break
        
        if not url:
            print(f"WARNING: Could not find URL for: {raw}")
            continue

        target_dir = os.path.join(DOCS_DIR, item["folder"])
        os.makedirs(target_dir, exist_ok=True)
        target_path = os.path.join(target_dir, item["file_name"])
        rel_path = os.path.relpath(target_path, BASE_DIR)

        print(f"Downloading: {raw} -> {rel_path}...")
        try:
            req_file = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req_file, timeout=30) as f_resp:
                content = f_resp.read()
                with open(target_path, "wb") as f_out:
                    f_out.write(content)
                size_kb = round(len(content) / 1024, 1)
                size_str = f"{size_kb} KB" if size_kb < 1000 else f"{round(size_kb/1024, 1)} MB"
                
                catalog_entry = dict(item)
                catalog_entry["remote_url"] = url
                catalog_entry["path"] = rel_path.replace("\\", "/")
                catalog_entry["size"] = size_str
                catalog_entry["bytes"] = len(content)
                catalog.append(catalog_entry)
                success_count += 1
        except Exception as e:
            print(f"ERROR downloading {raw}: {e}")

    catalog_path = os.path.join(DOCS_DIR, "catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print(f"\nSUCCESS: Downloaded {success_count} / {len(DOC_MAPPINGS)} documents.")
    print(f"Saved catalog to: {catalog_path}")

if __name__ == "__main__":
    download_all()
