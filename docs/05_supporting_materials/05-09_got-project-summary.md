# GOT Project Summary – Integrated Forest Compliance & Monitoring

## 1. Headline

Deliver a modular, client-tailored pathway that helps forest managers and supply-chain actors prove **deforestation-free origin (EUDR)**, stay **audit-ready (FSC/PEFC)**, operate a **practical monitoring system**, and translate insights into **bankable financial plans**—with embedded training so teams retain control.

By improving traceability and performance of supplier networks, the platform also strengthens the long-term quality and viability of client supply chains.

---

## 2. Modular Offer

| Module | Purpose | Key Outputs | Training & Flexibility Notes |
| :--- | :--- | :--- | :--- |
| **EUDR Traceability Core** | Harmonise supplier geodata, run post-2020 deforestation screening (Sentinel/RADD/GLAD), produce supplier risk ledger. | GeoPackage/PostGIS database, risk ledger, due-diligence brief. | Workflows configurable to existing data; handover includes SOPs and QGIS/Mergin tutorials. |
| **Certification Pre-Audit** | Scope FSC/PEFC (and initial carbon) requirements, assess gaps, design corrective roadmap. | Gap matrix, action plan, pre-audit report. | Co-create remediation plans; train client leads on evidence collection and reporting cadence. |
| **Enhanced Forest Monitoring** | Build alerting/analytics pipeline using satellite, telemetry, and optional partner-supplied drone imagery. | Monitoring playbook, KPI dashboard/workbook, escalation matrix. | Clients select telemetry/drone partners; we configure ingestion and provide SOPs + refresher sessions. |
| **Operational & Financial Readiness** | Convert monitoring/compliance data into Excel-first scenarios (wood-flow + DCF). | Transparent valuation workbook, capex/opex roadmap, financing brief. | Models delivered in Excel with walkthroughs; clients can extend scenarios without proprietary tools. |

---

## 3. Integration of FHCL Wood-Flow Valuation Insights

- **Inventory Backbone:** Adopt compartment × species × planting year structure to schedule harvest volumes and align monitoring cadences.
- **Discounted Cash-Flows:** Mirror cash-in/out (revenues vs harvesting/compliance/capex), making risk-reduction value visible.
- **Risk Overlay:** Attach EUDR and certification flags to compartments to prioritise interventions where value-at-risk is highest.
- **Operational Linkage:** Tie harvest scheduling to monitoring milestones (pre-harvest checks, post-harvest regeneration evidence).

---

## 4. Data Model & Workflow (at a glance)

1. **Data Harmonisation:** PostGIS tables (`compartment`, `species_recipe`, `planting_year`, `yield_curve`, `harvest_schedule`, `compliance_flags`).
2. **Risk Screening:** Multi-temporal deforestation alerts + protected-area overlays attached to each compartment/supplier.
3. **Wood-Flow Engine:** Annual volume computation per compartment/species, aggregated into baseline and improved scenarios.
4. **Financial Translation:** Scenario-based revenues, opex, capex, compliance costs → NPV/sensitivity analysis in Excel.
5. **Monitoring & SOPs:** Schedule field checks, telemetry updates, and partner imagery ingestion; document in playbook + training videos.

---

## 5. Deliverables

- Supplier/Compartment **Risk Ledger** with remediation priorities.
- **Map atlas** and dashboard-ready layers for EUDR submissions and partner integrations.
- **Certification gap matrix** and corrective roadmap.
- **Monitoring playbook** (KPIs, cadences, governance) with recorded training sessions.
- **Wood-flow schedule** linked to a transparent **DCF workbook** (base vs enhanced scenarios).
- **Concise briefing deck** for regulators, certifiers, and investors.

---

## 6. Engagement Flow

1. **Discovery (1 hour):** Clarify existing tools, partner ecosystem, desired outcomes.
2. **Scoping Note (1–2 pages):** Select modules, estimate effort, outline training plan.
3. **Delivery Sprints:** Iterative build with review checkpoints and hands-on sessions.
4. **Handover:** Shared repository access, SOP bundle, training recordings; optional light-touch support retainer.

---

## 7. Positioning for OpenForests & Partners

- Present as a **referral-ready solution**—OpenForests can point clients to Komba GIS AB when they need integrated compliance, monitoring, or finance support.
- Compatible with existing partner services (Globhe, Nadar, Varda, etc.); we ingest their outputs rather than replicate them.
- Emphasise the **training and tech transfer promise**: clients remain independent after rollout.

---

Use this summary for grant applications (e.g., GOT), partner introductions, or as a script for a teaser deck/web brief. Supporting assets live in `docs/05_supporting_materials/`.

