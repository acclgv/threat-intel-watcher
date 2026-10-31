#!/usr/bin/env python3
"""
Threat Intelligence & Cloud Vulnerability Watcher
Automated Git Scraping pipeline fetching Known Exploited Vulnerabilities (KEV) from CISA.
Runs autonomously in GitHub Actions to maintain an immutable, version-controlled feed.
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

FEED_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
OUTPUT_JSON = os.path.join(DATA_DIR, "cisa_kev.json")
OUTPUT_MD = os.path.join(DATA_DIR, "LATEST_VULNERABILITIES.md")
README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")


def fetch_kev_catalog():
    print(f"[*] Fetching CISA KEV catalog from: {FEED_URL}")
    req = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ThreatIntelWatcher/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP error {response.status} while fetching feed")
        raw_data = response.read().decode("utf-8")
        return json.loads(raw_data)


def process_and_save_data(catalog):
    os.makedirs(DATA_DIR, exist_ok=True)
    vulnerabilities = catalog.get("vulnerabilities", [])
    count = catalog.get("count", len(vulnerabilities))
    catalog_version = catalog.get("catalogVersion", "Unknown")
    date_released = catalog.get("dateReleased", datetime.now(timezone.utc).isoformat())

    print(f"[+] Catalog version: {catalog_version}")
    print(f"[+] Total vulnerabilities indexed: {count}")

    # Sort vulnerabilities deterministically: dateAdded DESC, then cveID DESC
    sorted_vulns = sorted(
        vulnerabilities,
        key=lambda v: (v.get("dateAdded", ""), v.get("cveID", "")),
        reverse=True
    )
    catalog["vulnerabilities"] = sorted_vulns

    # Save normalized JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    print(f"[+] Saved structured JSON dataset to: {OUTPUT_JSON}")

    # Generate Markdown Summary
    latest_25 = sorted_vulns[:25]
    md_content = [
        "# 🛡️ CISA Known Exploited Vulnerabilities (KEV) — Live Tracker",
        "",
        f"> **Automated Feed**: Updated continuously via GitHub Actions Git Scraping pipeline.  ",
        f"> **Total Tracked CVEs**: `{count}` | **Catalog Version**: `{catalog_version}` | **Last Sync**: `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`",
        "",
        "---",
        "",
        "## 📌 Top 25 Most Recently Added Vulnerabilities",
        "",
        "| CVE ID | Vendor / Project | Product | Vulnerability Name | Date Added | Action Due Date |",
        "| :--- | :--- | :--- | :--- | :---: | :---: |"
    ]

    for v in latest_25:
        cve = v.get("cveID", "N/A")
        vendor = v.get("vendorProject", "N/A").replace("|", "\\|")
        product = v.get("product", "N/A").replace("|", "\\|")
        vuln_name = v.get("vulnerabilityName", "N/A").replace("|", "\\|")
        date_added = v.get("dateAdded", "N/A")
        due_date = v.get("dueDate", "N/A")
        cve_link = f"[{cve}](https://nvd.nist.gov/vuln/detail/{cve})"
        md_content.append(f"| {cve_link} | {vendor} | {product} | {vuln_name} | {date_added} | {due_date} |")

    md_content.append("")
    md_content.append("---")
    md_content.append("*Data source: Cybersecurity and Infrastructure Security Agency (CISA) official KEV feed.*")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md_content) + "\n")
    print(f"[+] Saved Markdown summary to: {OUTPUT_MD}")

    # Update main README
    readme_content = f"""# 🛡️ Cloud & Enterprise Threat Intel Watcher

[![Sync Threat Intel Feed](https://github.com/GarciaVillenaLuis/threat-intel-watcher/actions/workflows/daily-threat-intel.yml/badge.svg)](https://github.com/GarciaVillenaLuis/threat-intel-watcher/actions/workflows/daily-threat-intel.yml)
[![Source: CISA KEV](https://img.shields.io/badge/Feed_Source-CISA_KEV-blue.svg)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated, cloud-native **Git Scraping** telemetry pipeline developed by [Luis García Villena](https://www.linkedin.com/in/luis-garcia-villena/) (*Security Transformation Analyst at Accenture*).

This pipeline continuously monitors, ingests, normalizes, and version-controls the official **Known Exploited Vulnerabilities (KEV)** catalog published by the Cybersecurity and Infrastructure Security Agency (CISA).

---

## 📊 Live Feed Status

- **Total Exploited CVEs Tracked**: `{count}`
- **Catalog Version**: `{catalog_version}`
- **Last Automated Sync**: `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`
- **Execution Engine**: 100% Cloud-Native GitHub Actions (Ubuntu ephemeral runners)

---

## 📋 Latest Ingested Vulnerabilities (Preview)

| CVE ID | Vendor / Project | Product | Vulnerability Name | Date Added |
| :--- | :--- | :--- | :--- | :---: |
"""
    for v in sorted_vulns[:10]:
        cve = v.get("cveID", "N/A")
        vendor = v.get("vendorProject", "N/A").replace("|", "\\|")
        product = v.get("product", "N/A").replace("|", "\\|")
        vuln_name = v.get("vulnerabilityName", "N/A").replace("|", "\\|")
        date_added = v.get("dateAdded", "N/A")
        cve_link = f"[{cve}](https://nvd.nist.gov/vuln/detail/{cve})"
        readme_content += f"| {cve_link} | {vendor} | {product} | {vuln_name} | {date_added} |\n"

    readme_content += """
👉 **[View Full 25-Entry Executive Table](data/LATEST_VULNERABILITIES.md)** | **[Download Complete Normalized Dataset (JSON)](data/cisa_kev.json)**

---

## ⚙️ Architecture & Git Scraping Pattern

This repository implements the **Git Scraping** pattern:
1. A GitHub Actions workflow triggers automatically on a daily schedule (`cron: '37 5 * * *'`).
2. The ephemeral runner fetches the authoritative CISA feed over HTTPS.
3. The dataset is parsed, sorted deterministically, and formatted to prevent spurious diffs.
4. If new exploited vulnerabilities have been published, a semantic commit is recorded and pushed to `main`.
5. Every commit represents real-world threat telemetry with complete diff auditability.

---

## 👤 Author & Contact

**Luis García Villena**  
*Security Transformation Analyst at Accenture*  
- 💼 **LinkedIn**: [linkedin.com/in/luis-garcia-villena](https://www.linkedin.com/in/luis-garcia-villena/)  
- 🛡️ **Certifications**: CCSP & CCGP (ISMS Forum) | Master in Cybersecurity
"""

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme_content.strip() + "\n")
    print(f"[+] Updated root README to: {README_PATH}")


def main():
    try:
        catalog = fetch_kev_catalog()
        process_and_save_data(catalog)
        print("[OK] Threat Intel sync completed successfully.")
    except Exception as e:
        print(f"[!] Error syncing Threat Intel feed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
