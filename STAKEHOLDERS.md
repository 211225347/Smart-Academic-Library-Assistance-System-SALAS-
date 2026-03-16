# STAKEHOLDERS.md — Smart Academic Library Assistance System (SALAS)

> Assignment 4: Stakeholder Analysis  
> Building on Assignment 3 — SALAS (Smart Academic Library Assistance System)

---

## Overview

This document identifies all key stakeholders of the SALAS platform, detailing their roles, key concerns, pain points, and measurable success metrics. Stakeholder analysis was conducted to ensure that all system requirements are traceable to real user needs.

---

## Stakeholder Analysis Table

### Stakeholder 1: University Student

| Attribute | Detail |
|---|---|
| **Role** | Primary end-user of the system. Searches for academic resources, borrows/reserves books, manages their personal dashboard, and receives personalized recommendations. |
| **Key Concerns** | - Quickly finding relevant books and journals for assignments and research. - Knowing real-time availability of physical resources. - Avoiding overdue fines through timely reminders. - Getting recommendations relevant to their course of study. |
| **Pain Points** | - Current library catalogue requires exact title/author matches — no natural language search. - No visibility into due dates or borrowing history in one place. - No personalized suggestions; students rely on word-of-mouth. - Physical reservation requires visiting the library in person. |
| **Success Metrics** | - Resource found within 3 search interactions 90% of the time. - 30% reduction in overdue returns after notification system is live. - Student satisfaction score ≥ 4.0/5.0 in usability surveys. - 50% of students use the recommendation feature monthly. |

---

### Stakeholder 2: University Librarian

| Attribute | Detail |
|---|---|
| **Role** | Manages the library catalogue, processes book check-ins/check-outs, handles reservations, and monitors inventory levels. Uses the Admin Web App. |
| **Key Concerns** | - Accurate, real-time tracking of all physical resources. - Reducing manual workload for routine tasks (reservation confirmations, overdue notices). - Generating usage reports for procurement decisions. |
| **Pain Points** | - Currently updating spreadsheets manually to track loans and returns. - Overdue notices are sent manually via email, which is time-consuming. - No data on which resources are most in demand to guide purchasing. - Adding new books to the catalogue is a multi-step manual process. |
| **Success Metrics** | - Catalogue update time reduced from 15 minutes to under 2 minutes per entry. - 100% automated overdue notification coverage. - Monthly usage reports generated with zero manual effort. - Inventory discrepancy rate reduced to below 1%. |

---

### Stakeholder 3: IT Administrator / DevOps Engineer

| Attribute | Detail |
|---|---|
| **Role** | Responsible for deploying, maintaining, and monitoring the SALAS infrastructure. Manages servers, databases, security patches, and system uptime. |
| **Key Concerns** | - System must remain available during peak academic periods (exam seasons). - All services must be containerized for easy deployment and rollback. - Security vulnerabilities must be patched without downtime. - System logs must be accessible for debugging and auditing. |
| **Pain Points** | - Legacy library systems are monolithic and difficult to update without full downtime. - No centralized logging or monitoring dashboard currently exists. - Manual deployment processes are error-prone and slow. - Bandwidth spikes during semester start cause performance degradation. |
| **Success Metrics** | - System uptime ≥ 99.5% during academic semesters. - Deployment of new releases achievable in under 15 minutes via CI/CD. - Zero critical unpatched security vulnerabilities at any time. - Mean Time to Recovery (MTTR) from incidents under 30 minutes. |

---

### Stakeholder 4: University Administrator / Academic Management

| Attribute | Detail |
|---|---|
| **Role** | Oversees the library as an institutional resource. Concerned with budget allocation, accreditation compliance, strategic resource planning, and student academic outcomes. |
| **Key Concerns** | - Demonstrating return on investment for the SALAS system. - Ensuring the library's digital resources comply with copyright and licensing laws. - Monitoring aggregate usage trends to inform procurement and budget decisions. - Ensuring accessibility standards are met for students with disabilities. |
| **Pain Points** | - No consolidated reporting on library resource utilization. - Difficult to justify new resource purchases without usage data. - Accessibility of the current library portal is poor for students with visual impairments. - No integration between library usage and student academic performance data. |
| **Success Metrics** | - Executive usage dashboard available with monthly auto-generated reports. - 100% of digital resources comply with institutional licensing agreements. - System meets WCAG 2.1 AA accessibility standards. - Annual budget planning supported by data-driven resource demand insights. |

---

### Stakeholder 5: Recommendation Engine / Data Science Team

| Attribute | Detail |
|---|---|
| **Role** | Internal technical stakeholder responsible for developing, training, and maintaining the collaborative filtering recommendation model that powers SALAS's personalization features. |
| **Key Concerns** | - Access to sufficient, clean student borrowing and search history data. - Model retraining pipeline must run automatically without manual intervention. - Recommendation quality must be measurable and improvable over time. - Student data used for recommendations must comply with privacy regulations (POPIA/GDPR). |
| **Pain Points** | - Current system captures no behavioral data that could feed a recommendation model. - No data pipeline or feature store exists for ML model training. - Cold-start problem: new students have no history for initial recommendations. - No A/B testing framework to evaluate recommendation quality. |
| **Success Metrics** | - Recommendation click-through rate (CTR) ≥ 25%. - Model retrained automatically at least once every 24 hours. - Cold-start recommendations (for new students) achieve ≥ 15% CTR using course-based defaults. - 100% of data used for training is anonymized and POPIA-compliant. |

---

### Stakeholder 6: External Integration Partners (University Portal / Mobile App)

| Attribute | Detail |
|---|---|
| **Role** | Third-party systems and developers that consume the SALAS REST API to integrate library functionality into the university's main student portal and mobile application. |
| **Key Concerns** | - The SALAS API must be stable, versioned, and well-documented. - Authentication must use a standard protocol (OAuth 2.0 / JWT) compatible with existing SSO infrastructure. - API response times must be fast enough for seamless in-app experiences. - Breaking changes must be communicated in advance with migration guides. |
| **Pain Points** | - Existing library API (if any) has no versioning, making upgrades unpredictable. - No Swagger/OpenAPI documentation exists for current systems. - API rate limits are undocumented, causing unexpected throttling. - No sandbox/test environment available for integration testing. |
| **Success Metrics** | - Full OpenAPI 3.0 documentation published and kept up to date. - API versioning maintained with at least one version of backward compatibility. - API sandbox environment available 100% of the time. - API response time under 300ms for 95% of requests under normal load. |

---

### Stakeholder 7: Student with Accessibility Needs

| Attribute | Detail |
|---|---|
| **Role** | A subset of the student user group who requires accessible design — including screen reader compatibility, keyboard navigation, high-contrast modes, and font resizing — to use the system effectively. |
| **Key Concerns** | - Web interface must be fully navigable without a mouse. - Screen readers must be able to interpret all search results, buttons, and forms. - Color contrast ratios must meet WCAG 2.1 AA standards. - PDFs and e-resources must have text-layer accessibility. |
| **Pain Points** | - Most university library portals have poor accessibility scores. - Images of book covers lack alt-text, making them invisible to screen readers. - Dynamic search results are not announced to assistive technologies. - No keyboard shortcut system for power navigation. |
| **Success Metrics** | - WCAG 2.1 AA compliance verified by automated audit (score ≥ 95 on Lighthouse). - All images include descriptive alt-text. - Full keyboard navigation supported across all pages. - Zero critical accessibility violations reported in annual accessibility audit. |

---

## Stakeholder Priority Matrix

| Stakeholder | Influence | Interest | Priority |
|---|---|---|---|
| University Student | High | High | 🔴 Critical |
| University Librarian | Medium | High | 🔴 Critical |
| IT Administrator | High | Medium | 🟠 High |
| University Administrator | High | Medium | 🟠 High |
| Data Science Team | Low | High | 🟡 Medium |
| External Integration Partners | Medium | Medium | 🟡 Medium |
| Student with Accessibility Needs | Low | High | 🟠 High |
