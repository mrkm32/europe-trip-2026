import json
import html

with open("documents/catalog.json", "r") as f:
    catalog = json.load(f)

# Counts
counts = {
    "total": len(catalog),
    "matthews": sum(1 for x in catalog if x["traveler"] == "Mark & Shelly"),
    "rowe": sum(1 for x in catalog if x["traveler"] == "Bill & Kris"),
    "shared": sum(1 for x in catalog if x["traveler"] == "Shared"),
    "trains": sum(1 for x in catalog if x["category"] == "Train Tickets"),
    "lodging": sum(1 for x in catalog if x["category"] == "Hotel Confirmations"),
    "car": sum(1 for x in catalog if x["category"] == "Car Rental"),
    "tours": sum(1 for x in catalog if x["category"] == "Tours & Lifts"),
    "guides": sum(1 for x in catalog if x["category"] == "Guides & Support")
}

print("Counts:", counts)
