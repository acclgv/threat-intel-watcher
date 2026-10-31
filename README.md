# 🛡️ Cloud & Enterprise Threat Intel Watcher

[![Sync Threat Intel Feed](https://github.com/GarciaVillenaLuis/threat-intel-watcher/actions/workflows/daily-threat-intel.yml/badge.svg)](https://github.com/GarciaVillenaLuis/threat-intel-watcher/actions/workflows/daily-threat-intel.yml)
[![Source: CISA KEV](https://img.shields.io/badge/Feed_Source-CISA_KEV-blue.svg)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated, cloud-native **Git Scraping** telemetry pipeline developed by [Luis García Villena](https://www.linkedin.com/in/luis-garcia-villena/) (*Security Transformation Analyst at Accenture*).

This pipeline continuously monitors, ingests, normalizes, and version-controls the official **Known Exploited Vulnerabilities (KEV)** catalog published by the Cybersecurity and Infrastructure Security Agency (CISA).

---

## 📊 Live Feed Status

- **Total Exploited CVEs Tracked**: `1766`
- **Catalog Version**: `2026.10.30`
- **Last Automated Sync**: `2026-10-31 22:45:01 UTC`
- **Execution Engine**: 100% Cloud-Native GitHub Actions (Ubuntu ephemeral runners)

---

## 📋 Latest Ingested Vulnerabilities (Preview)

| CVE ID | Vendor / Project | Product | Vulnerability Name | Date Added |
| :--- | :--- | :--- | :--- | :---: |
| [CVE-2026-118527](https://nvd.nist.gov/vuln/detail/CVE-2026-118527) | Ivanti | Connect Secure | Ivanti Connect Secure Generation of Predictable Numbers or Identifiers Vulnerability | 2026-10-30 |
| [CVE-2026-111357](https://nvd.nist.gov/vuln/detail/CVE-2026-111357) | Ivanti | Connect Secure | Ivanti Connect Secure Missing Authentication for Critical Function Vulnerability | 2026-10-30 |
| [CVE-2026-97229](https://nvd.nist.gov/vuln/detail/CVE-2026-97229) | GitLab | Community Edition and Enterprise Edition | GitLab Community Edition and Enterprise Edition Integer Overflow or Wraparound Vulnerability | 2026-10-29 |
| [CVE-2026-76418](https://nvd.nist.gov/vuln/detail/CVE-2026-76418) | Cisco | Secure Firewall ASA Software and Cisco Secure FTD Software | Cisco Secure Firewall ASA Software and Cisco Secure FTD Software Unchecked Return Value to NULL Pointer Dereference Vulnerability | 2026-10-29 |
| [CVE-2026-46300](https://nvd.nist.gov/vuln/detail/CVE-2026-46300) | Linux | Kernel | Linux Kernel Missing Initialization of a Variable Vulnerability | 2026-10-28 |
| [CVE-2026-41709](https://nvd.nist.gov/vuln/detail/CVE-2026-41709) | Broadcom | VMware ESX | Broadcom VMWare ESX Insufficient Logging Vulnerability | 2026-10-28 |
| [CVE-2026-48356](https://nvd.nist.gov/vuln/detail/CVE-2026-48356) | Adobe | Commerce and Magento | Adobe Commerce and Magento Unrestricted Upload of File with Dangerous Type Vulnerability | 2026-10-27 |
| [CVE-2026-111497](https://nvd.nist.gov/vuln/detail/CVE-2026-111497) | Google | Brotli | Google Brotli Unchecked Return Value Vulnerability | 2026-10-27 |
| [CVE-2026-109619](https://nvd.nist.gov/vuln/detail/CVE-2026-109619) | PHP Group | PHP | PHP Stale Internal Request-State Vulnerability | 2026-10-26 |
| [CVE-2026-109618](https://nvd.nist.gov/vuln/detail/CVE-2026-109618) | PHP Group | PHP | PHP Memory Corruption Vulnerability | 2026-10-26 |

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
