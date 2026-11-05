# CSRF Attack Lab (SEED Lab on CyberRangeCZ) - Game Design Document

## 1. Overview
- **Scenario Name**: `csrf-seedlab`
- **Topic**: Web Application Security - Cross-Site Request Forgery (CSRF) on Elgg
- **Reference**: SEED Labs CSRF Lab (Wenliang Du) & CyberRangeCZ scenario structure (`library-junior-hacker`)
- **Total Points**: 20 / 20 points
- **Student Capacity**: 30+ students (with unique dynamic flags per sandbox to prevent cheating)
- **Target Audience**: Cybersecurity students / Junior penetration testers

---

## 2. Infrastructure & Topology

The topology uses **flavor `m1.medium`** and replaced Kali with **SEED Ubuntu 20.04 (`seed`)**:

| Host | Image | Mgmt User | Flavor | IP Address | Purpose |
|------|-------|-----------|--------|------------|---------|
| `seed` | `seed-ubuntu2004` | `ubuntu` | `m1.medium` | `10.1.30.10` | Student workstation with desktop GUI, Firefox, and attack files |
| `server` | `debian-12-x86_64` | `debian` | `m1.medium` | `10.1.30.5` | Docker host hosting Elgg, Attacker site, MySQL DB, and Flag server |
| `router` | `debian-12-x86_64` | `debian` | `standard.small` | `10.1.30.1` | Network routing and internet gateway |

### DNS & Virtual Hosts:
- `www.seed-server.com` -> `10.1.30.5` (Elgg Social Network)
- `www.attacker32.com` -> `10.1.30.5` (Attacker Website)
- `www.example32.com` -> `10.1.30.5` (Defense/Cookie Test Site)

---

## 3. Scoring Breakdown (Total 20 / 20) & Anti-Cheating Strategy

To accommodate 30+ students simultaneously without sharing answers, the lab uses CyberRangeCZ's **Automatic Problem Generation (APG)** through `variables.yml` (`variant_sandboxes: true`). Each student's sandbox instantiates dynamic flags bound to their sandbox ID.

| Level | Title | Max Score | Hints & Penalties | Flag / Answer | Anti-Cheating |
|---|---|---|---|---|---|
| **0** | Introduction | 0 pt | None | None (Info Level) | N/A |
| **1** | Access the Sandbox | 0 pt | None | `start` (Access Level) | Verification check |
| **2** | Task 1: Observing HTTP Requests | 2 pt | Hint 1 (-0.5 pt) | `GET` | Found via Firefox DevTools |
| **3** | Task 2: CSRF via GET Request | 5 pt | Hint 1 (-1.0 pt)<br>Hint 2 (-1.5 pt)<br>Hint 3 (-2.0 pt) | `{{ flag_task2 }}` | Dynamic per-sandbox flag |
| **4** | Task 3: CSRF via POST Request | 5 pt | Hint 1 (-1.0 pt)<br>Hint 2 (-1.5 pt)<br>Hint 3 (-2.0 pt) | `{{ flag_task3 }}` | Dynamic per-sandbox flag |
| **5** | Task 4: CSRF Countermeasure | 4 pt | Hint 1 (-1.0 pt)<br>Hint 2 (-1.5 pt)<br>Hint 3 (-2.0 pt) | `{{ flag_task4 }}` | Dynamic per-sandbox flag |
| **6** | Task 5: SameSite Cookie Defense | 4 pt | Hint 1 (-1.0 pt)<br>Hint 2 (-2.0 pt) | `{{ flag_task5 }}` | Dynamic per-sandbox flag |
| **Total** | | **20 / 20 pt** | **Penalties: -0.5 to -2.0** | | Unique flags for each student |

---

## 4. Educational Workflow

1. **Reconnaissance**: Students analyze legitimate HTTP requests using Firefox Web Developer Tools.
2. **GET Exploitation**: Craft an invisible image tag `<img src="...">` triggering an automated Add-Friend action under Alice's authenticated session.
3. **POST Exploitation**: Construct an auto-submitting hidden HTML form in JavaScript that changes Alice's bio to "Samy is my Hero".
4. **Token Defense**: Inspect `Csrf.php`, remove the testing bypass line, and verify how `__elgg_token` and `__elgg_ts` prevent CSRF.
5. **Cookie Defense**: Explore modern SameSite cookie policies (`Strict`, `Lax`, `None`) on `example32.com` and observe cross-origin request filtering.
