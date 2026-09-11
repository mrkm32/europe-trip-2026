import json
import re

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
    
    # Generate intelligent, conductor-friendly page labels
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
    
    # Fallback if page_labels count doesn't match page_count
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

print(f"Generated docs_map with {len(docs_map)} entries.")

# Check today's Innsbruck to Bolzano tickets
inns_m = docs_map.get("documents/trains/matthews/01_Innsbruck_to_Bolzano_Train_Tickets_Matthews.pdf")
print("Innsbruck Matthews:", inns_m["pageCount"], inns_m["pageLabels"], inns_m["pages"])

inns_r = docs_map.get("documents/trains/rowe/01_Innsbruck_to_Bolzano_Train_Tickets_Rowe.pdf")
print("Innsbruck Rowe:", inns_r["pageCount"], inns_r["pageLabels"], inns_r["pages"])
