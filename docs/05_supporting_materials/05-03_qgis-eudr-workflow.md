# QGIS + Mergin Maps Workflow for EUDR Traceability

This guide distils the “EUDR compliance workflow using QGIS and Mergin Maps” tutorial transcript into a repeatable process. Follow it to build a field data collection pipeline that captures compliant geolocation evidence for Regulation (EU) 2023/1115 (EUDR).

---

## 1. Regulatory Requirements Recap

- **Traceability Precision:** Coordinates must be delivered in WGS84 (EPSG:4326) with at least 6 decimal places (~sub‑metre accuracy).
- **Geometry Rules:** Plots > 4 ha require polygons; smaller plots can be recorded as a single point.
- **Commodities Covered:** cattle, cocoa, coffee, oil palm, rubber, soy, and timber.
- **Reference Date:** Production areas must show no deforestation after 31 December 2020.

Keep these requirements in mind while configuring forms, validation rules, and exports.

---

## 2. Prerequisites

| Tool | Purpose | Notes |
| :--- | :--- | :--- |
| QGIS (3.30+) | Desktop GIS authoring | Make sure Python support is installed if you plan to automate exports. |
| Mergin Maps plugin | Sync between QGIS and Mergin Maps cloud/mobile | Install via `Plugins → Manage and Install Plugins`. |
| Mergin Maps account | Cloud project storage & mobile access | Sign up on [merginmaps.com](https://merginmaps.com). |
| Mobile device w/ Mergin Maps app | Field data capture | Available on iOS & Android. |
| Reference spreadsheet (CSV) | Cooperative/farm metadata | Example headers in the next section. |

Optional but recommended: a shared `docs/Visuals/` folder for base imagery or reference maps, and version control (GitHub) for the QGIS project template.

---

## 3. Prepare Input Metadata (CSV)

Create or export a spreadsheet containing base information about the farms/cooperatives you intend to register. Suggested columns:

| Column | Description |
| :--- | :--- |
| `plot_id` | Unique identifier for each plot/farm. |
| `form_name` | Local farm name (string). |
| `commodity` | Commodity category (coffee, cocoa, etc.). |
| `cooperative` | Cooperative or supplier group. |
| `municipality` | Administrative unit for reporting. |
| `production_date` | Date the plot came into production (ISO `YYYY-MM-DD`). |
| `latitude` / `longitude` | Optional centroids if already available. |
| `area_ha` | Known area in hectares (numeric). |

Export the sheet as CSV (e.g., `forms_metadata.csv`). Place the CSV inside the Mergin Maps project folder **before** you start configuring forms so that value maps resolve correctly on mobile.

---

## 4. Create the Mergin Maps Project

1. Launch QGIS and ensure the Mergin Maps plugin is installed.
2. Sign in to your Mergin Maps account via the plugin toolbar.
3. Click **`+` → New Basic QGIS Project**.
4. Pick the target workspace and folder, give the project a name (e.g., `Farms_Brazil`), and finish the wizard.
5. Remove the default demo layers from the project and project folder (optional).

### Set the Coordinate Reference System (CRS)

1. `Project → Properties → CRS`
2. Search for `EPSG:4326 (WGS 84)` and set it as the project CRS.

This ensures all layers inherit the required EUDR spatial reference.

---

## 5. Add the Metadata CSV to QGIS

1. Drag the exported `forms_metadata.csv` into the Mergin Maps project folder (visible in the browser panel).
2. Add the CSV as a **delimited text layer** in QGIS (`Layer → Add Layer → Add Delimited Text Layer`).
3. Confirm field types (e.g., text vs numeric) and load the layer so it can provide dropdown values for your forms.

---

## 6. Build the Plot Layer (GeoPackage)

1. `Layer → Create Layer → New GeoPackage Layer…`
2. Database: select/create a GeoPackage file within the project folder (e.g., `eudr_plots.gpkg`).
3. Layer name: `plots` (or similar).
4. Geometry type: `Polygon` (use `Point` for plots under 4 ha if required).
5. Set CRS to `EPSG:4326 - WGS 84`.
6. Add the following fields:

| Name | Type | Notes |
| :--- | :--- | :--- |
| `plot_id` | Text | Unique ID (can auto-populate). |
| `form_name` | Text | Display name drawn from metadata CSV. |
| `commodity` | Text | Value map from CSV. |
| `production_date` | Date | Mandatory for EUDR evidence. |
| `latitude` | Decimal (Real) | Optional centroid; can be auto-filled. |
| `longitude` | Decimal (Real) | Optional centroid; can be auto-filled. |
| `area_ha` | Decimal (Real) | Calculated via expression. |
| `country` | Text | Default to the country of operation. |
| `municipality` | Text | Value map from CSV. |
| `cooperative` | Text | Value map from CSV. |
| `collector_name` | Text | Captures Mergin username. |
| `collection_date` | Date/Time | Auto-populated on capture. |

Save the layer; it is now ready for form configuration.

---

## 7. Configure Attribute Forms

1. Right-click the `plots` layer → `Properties → Attributes Form`.
2. Switch the form layout to **Drag-and-Drop Designer**.
3. Hide system fields such as `fid` by setting their widget type to **Hidden**.
4. Configure widgets and defaults:

| Field | Widget | Key Settings |
| :--- | :--- | :--- |
| `plot_id` | Text Edit | Default value: `uuid()` or a custom expression combining cooperative + sequence. |
| `form_name` | Value Map | Load values/descriptions from `forms_metadata` CSV. |
| `commodity` | Value Map | Source: `forms_metadata` CSV. |
| `municipality` | Value Map | Source: `forms_metadata` CSV. |
| `cooperative` | Value Map | Source: `forms_metadata` CSV. |
| `production_date` | Date/Time | Keep as calendar picker; enforce requirement in the field alias or validation. |
| `area_ha` | Text Edit | Default expression: `round(area($geometry) / 10000, 4)`. |
| `latitude` | Text Edit | Default expression: `round(y(centroid($geometry)), 6)`. |
| `longitude` | Text Edit | Default expression: `round(x(centroid($geometry)), 6)`. |
| `country` | Text Edit | Default value: `'Brazil'` (or relevant country). |
| `collector_name` | Text Edit | Default expression: `@mergin_username`. |
| `collection_date` | Date/Time | Default expression: `now()`. |

5. Optionally add **field aliases** or translations (e.g., Portuguese labels for Brazilian cooperatives).
6. Save changes.

---

## 8. Styling for Field Clarity

1. `Layer Properties → Symbology`
2. Choose **Categorized** style based on `commodity`.
3. Assign high-contrast colours and line weights so polygons stand out in the field.
4. Optionally set rule-based styles (e.g., highlight plots lacking production dates).

Set the project extent (Project → Properties → General → Set to Map Canvas Extent) to the target area to speed up mobile map loading.

---

## 9. Sync and Field Deployment

1. Click the **Mergin Maps Sync** button in QGIS. Save edits when prompted.
2. Wait for the upload to complete; the project is now available in the cloud.
3. On the mobile device, open the Mergin Maps app, sign in, and **Install** the project.
4. Go to the field, select the `plots` layer, and start collecting polygons:
   - Use the GPS track mode (walking the boundary) for on-the-ground accuracy.
   - Alternatively, digitise vertices on the satellite basemap when GPS access is limited.
5. Fill in form fields—value maps will show dropdowns populated from the CSV metadata.
6. Sync from the mobile app once data collection is complete.

---

## 10. Review & Export in QGIS

1. Back in QGIS, press **Sync** to download the field edits.
2. Inspect the attribute table to validate completeness (production date, cooperative, etc.).
3. Export for submission: right-click `plots` layer → `Export → Save Features As…`
   - Format: `GeoJSON`
   - File name example: `para_plots_2025-11-07.geojson`
   - CRS: `EPSG:4326`
   - Ensure **“COORDINATE_PRECISION=6”** is set under **Layer Options** to retain six decimal places.
4. Archive the GeoJSON and any accompanying due-diligence notes in your `outputs/` folder for traceability.

---

## 11. Quality Assurance Checklist

- [ ] All polygons captured with the correct CRS and precision.
- [ ] Production date present and ≤ 2020-12-31 for legacy plots.
- [ ] Area auto-calculated and reviewed for outliers (e.g., polygons > expected size).
- [ ] Value-map fields (commodity, cooperative, municipality) populated from authoritative lists.
- [ ] Sync status on both QGIS and mobile shows no pending edits before exporting GeoJSON.
- [ ] GeoJSON validated (open in QGIS or use `ogrinfo`) before submitting with due diligence documentation.

---

## 12. Extension Ideas

- **Template Distribution:** Store a ready-to-use `.qgz` project and the GeoPackage layer in version control so partners can clone it quickly.
- **Automation:** Add a QGIS Python script (`Processing → Scripts`) that batch-exports all synced layers to GeoJSON with correct naming conventions.
- **Validation Rules:** Use the **Field Constraints** tab to prevent missing production dates or ensure `area_ha` falls within acceptable ranges.
- **Training Pack:** Export screenshots of the form and capture process to enrich onboarding materials for cooperative field teams.
- **Integration:** After export, feed the GeoJSON into your EUDR risk assessment scripts to flag any plots intersecting deforestation alerts or protected areas.

---

By following this workflow, you ensure that spatial data captured in the field aligns with EUDR expectations and slots neatly into your broader Forest Compliance Assurance Platform.

