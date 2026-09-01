#!/usr/bin/env python3
"""
Native macOS background monitor for Madeline's Axus Travel App itinerary.
Runs 3x daily (8:00 AM, 2:00 PM, 8:00 PM) via launchd.
Monitors: https://axustravelapp.com/shared/itinerary/4984d555-2c81-4965-8866-a8c1b59ee77e
Active through: September 19, 2026
"""

import sys
import os
import urllib.request
import datetime
import difflib
import subprocess
from html.parser import HTMLParser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "axus_monitor.log")
BASELINE_FILE = os.path.join(SCRIPT_DIR, "baseline_axus.txt")
CHANGES_LOG = os.path.join(SCRIPT_DIR, "changes_detected.log")

URL = "https://axustravelapp.com/shared/itinerary/4984d555-2c81-4965-8866-a8c1b59ee77e"
END_DATE = datetime.date(2026, 9, 20)

def log(msg: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted + "\n")
    except Exception as e:
        print(f"Failed to write to log file: {e}", file=sys.stderr)

class TextExtract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.texts = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ["script", "style", "noscript", "svg"]:
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ["script", "style", "noscript", "svg"]:
            self.skip = False

    def handle_data(self, data):
        if not self.skip:
            t = data.strip()
            if t:
                self.texts.append(t)

def notify_macos(title: str, subtitle: str, message: str):
    clean_title = title.replace('"', '\\"')
    clean_sub = subtitle.replace('"', '\\"')
    clean_msg = message.replace('"', '\\"')
    script = f'display notification "{clean_msg}" with title "{clean_title}" subtitle "{clean_sub}" sound name "Glass"'
    try:
        subprocess.run(["osascript", "-e", script], check=True)
    except Exception as e:
        log(f"Failed to send macOS notification: {e}")

def run_check():
    today = datetime.date.today()
    if today > END_DATE:
        log("Monitoring period ended (after Sep 19, 2026). Exiting.")
        return

    log("Checking Axus itinerary for updates...")
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        log(f"Network error fetching Axus: {e}")
        return

    parser = TextExtract()
    parser.feed(html)
    current_texts = parser.texts

    if not os.path.exists(BASELINE_FILE):
        with open(BASELINE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(current_texts))
        log(f"Baseline saved ({len(current_texts)} content elements). Monitoring is active.")
        return

    with open(BASELINE_FILE, "r", encoding="utf-8") as f:
        previous_texts = [line.rstrip("\n") for line in f]

    diff = list(difflib.unified_diff(
        previous_texts,
        current_texts,
        fromfile="Previous Axus Itinerary",
        tofile="Current Axus Itinerary",
        lineterm=""
    ))

    if diff:
        log(f"ALERT: Changes detected in Axus itinerary! Diff lines: {len(diff)}")
        
        with open(CHANGES_LOG, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"\n{'='*60}\nCHANGES DETECTED AT {timestamp}\n{'='*60}\n")
            f.write("\n".join(diff) + "\n")
        
        with open(BASELINE_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(current_texts))

        notify_macos(
            title="Europe Trip 2026",
            subtitle="Axus Itinerary Updated",
            message="Madeline updated trip details! Check scripts/changes_detected.log."
        )
    else:
        log("Check complete: Itinerary unchanged.")

if __name__ == "__main__":
    run_check()
