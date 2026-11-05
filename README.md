# CSRF SeedLab Scenario for CyberRangeCZ Platform

This repository contains a full **CyberRangeCZ / KYPO-compatible training scenario** implementing the **SEED Labs Cross-Site Request Forgery (CSRF) on Elgg** lab described in `Web_CSRF_Elgg.pdf`.

It is modeled after the official [`library-junior-hacker`](https://github.com/cyberrangecz/library-junior-hacker) template.

---

## 🛠️ Infrastructure & Topology

- **Topology File**: [`topology.yml`](topology.yml)
- **Workstation Flavor**: `m1.medium`
- **Workstation Image**: `seed-ubuntu2004` (replaces Kali with SEED Ubuntu workstation)
- **Target Server Image**: `debian-12-x86_64` (flavor `m1.medium`)
- **Router Image**: `debian-12-x86_64` (flavor `standard.small`)

### Virtual Hostnames Configured:
- `www.seed-server.com` (10.1.30.5): Vulnerable Elgg social networking app
- `www.attacker32.com` (10.1.30.5): Attacker malicious website
- `www.example32.com` (10.1.30.5): SameSite defense test site

---

## 🎓 Grading & Scoring (20 / 20 Points Total)

The scenario is scored out of **20 points**, with hint penalties ranging from **-0.5 to -2.0 points**:

- **Task 1: Observing HTTP Requests** — `2 points` (Hint penalty: -0.5)
- **Task 2: CSRF Attack via GET Request** — `5 points` (Hint penalties: -1.0, -1.5, -2.0)
- **Task 3: CSRF Attack via POST Request** — `5 points` (Hint penalties: -1.0, -1.5, -2.0)
- **Task 4: Enabling CSRF Countermeasure** — `4 points` (Hint penalties: -1.0, -1.5, -2.0)
- **Task 5: SameSite Cookie Defense** — `4 points` (Hint penalties: -1.0, -2.0)

**Total = 20 / 20 Points**

---

## 🛡️ Anti-Cheating Strategy for 30+ Students

To prevent students from copying flags:
- Utilizes the CyberRangeCZ **Automatic Problem Generation (APG)** feature via [`variables.yml`](variables.yml) with `variant_sandboxes: true`.
- Each student sandbox generates unique alphanumeric tokens for `flag_task2`, `flag_task3`, `flag_task4`, and `flag_task5`.
- Flag verification is served dynamically by the internal sandbox service (`flag_server.py`) so every student must solve their own instance.

---

## 🚀 Deployment Instructions

1. Zip or push this directory to your CyberRangeCZ scenario repository:
   ```bash
   git init
   git add .
   git commit -m "CSRF SeedLab scenario"
   ```
2. In the CyberRangeCZ Web Interface:
   - Go to **Sandboxes** -> **Sandbox Definitions** -> **Add Definition** (point to repo with `topology.yml` and `provisioning/`).
   - Go to **Trainings** -> **Training Definitions** -> **Import** -> Select `training.json`.
3. Create a **Training Instance** with a pool of 30+ sandboxes.
