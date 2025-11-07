 # 🛰️ EUDR Spatial Risk Assessment Report (Demo)

 **Sample Supplier Group – Timber Sector (Fictional Data)**  \
 **Prepared by Komba GIS AB – November 2025**

 ---

 ## 1. Summary

 | Parameter | Description |
 | :---- | :---- |
 | **Client / Partner** | OpenForests (Demo Project) |
 | **Commodity** | Timber (Mixed hardwood) |
 | **Country of Origin** | Angola |
 | **Assessment Date** | November 2025 |
 | **Assessed Suppliers** | 5 (fictional concession polygons) |
 | **EUDR Scope** | Deforestation-free verification and spatial risk screening |
 | **Reference Date** | 31 December 2020 baseline |

 **Summary of Results:** All five supplier polygons were geolocated and analyzed using Sentinel-1, Sentinel-2, Hansen GFC, and ESA WorldCover (2020–2024). Three suppliers showed *no deforestation* since the baseline year, one indicated *moderate canopy reduction*, and one showed *recent forest loss*.

 | Risk Level | No. of Suppliers | Area (ha) | Comment |
 | :---- | :---- | :---- | :---- |
 | Low | 3 | 8,940 | Stable vegetation cover |
 | Medium | 1 | 2,450 | Selective canopy degradation detected |
 | High | 1 | 1,870 | Forest loss (2022–2023) observed near concession boundary |

 ---

 ## 2. Data and Methods

 ### 2.1 Datasets Used

 | Dataset | Source | Purpose |
 | :---- | :---- | :---- |
 | **ESA WorldCover 2020 & 2023** | ESA | Baseline forest / non-forest classification |
 | **Hansen GFC v1.11 (2001–2023)** | UMD | Detection of forest loss since 2020 |
 | **Sentinel-2 SR imagery (10 m)** | Copernicus | Visual verification & NDVI analysis |
 | **RADD Alerts (Sentinel-1)** | Wageningen Univ. | Radar-based disturbance detection |
 | **Protected Areas (WDPA)** | UNEP-WCMC | Overlap check with conservation zones |
 | **Elevation (SRTM 30 m)** | NASA | Terrain / slope risk factor |
 | **Administrative Boundaries** | GADM | Supplier polygon geolocation verification |

 ### 2.2 Analytical Workflow

 1. **Polygon Validation** – Verified coordinates and projection (EPSG:32733).
 2. **Forest Baseline (2020)** – Classified polygons using ESA WorldCover.
 3. **Deforestation Detection (2021–2025)** – Extracted GFC and RADD change layers.
 4. **Contextual Overlay** – Protected areas, slope >15°, distance to roads, and disturbance zones.
 5. **Risk Scoring** – Weighted combination of indicators (deforestation, degradation, slope, proximity to forest edge).
 6. **Quality Assurance** – Visual inspection of high-risk areas using Sentinel-2 composites.

 ---

 ## 3. Results

 ### 3.1 Overview Map

 🗺️ *[Placeholder: “Supplier Group Overview”]*

 ---

 ### 3.2 Supplier-Level Summary

 | Supplier ID | Area (ha) | Forest Cover 2020 (%) | Forest Loss 2020–2025 (ha) | Protected Area Overlap | Risk Level |
 | :---- | :---- | :---- | :---- | :---- | :---- |
 | **ANG-001** | 2,970 | 88 | 0 | No | **Low** |
 | **ANG-002** | 3,240 | 91 | 0 | No | **Low** |
 | **ANG-003** | 2,730 | 86 | 40 | Within 1.2 km of buffer | **Medium** |
 | **ANG-004** | 1,870 | 94 | 210 | No | **High** |
 | **ANG-005** | 2,730 | 89 | 0 | No | **Low** |

 ---

 ### 3.3 Spatial Risk Indicators

 | Indicator | Description | Example Finding |
 | :---- | :---- | :---- |
 | **Forest Loss (2020–2025)** | Total loss detected from Hansen GFC (30 m pixels) | 250 ha total (3% of combined area) |
 | **Forest Degradation (Radar)** | RADD alerts indicating canopy disturbance | 12 alerts (mostly 2022–2023) |
 | **Slope (>15°)** | Share of area prone to erosion | 18% of total area |
 | **Proximity to Roads** | Distance < 1 km from access roads | 27% of total area |
 | **Protected Area Buffer (5 km)** | Within 5 km of protected zones | 1 polygon (ANG-003) |
 | **Fire Frequency (MODIS 2001–2024)** | Count of annual fire detections | 4 of 5 polygons show ≤ 3 fires per year |

 ---

 ## 4. Risk Classification Map

 🗺️ *[Placeholder: “Spatial Risk Map by Supplier”]*

 ---

 ## 5. Interpretation and Recommendations

 - **ANG-004 (High Risk):** Clear forest loss (~210 ha) near central portion. Recommend follow-up field inspection and supplier engagement.
 - **ANG-003 (Medium Risk):** Minor degradation and proximity to protected-area buffer. Consider targeted monitoring and management review.
 - **ANG-001, ANG-002, ANG-005 (Low Risk):** Stable vegetation cover; continue routine annual monitoring.

 **Overall Risk Profile:** 80% of total area shows no deforestation since 2020. 20% requires additional verification.

 ---

 ## 6. Monitoring and Next Steps

 | Action | Frequency | Responsible |
 | :---- | :---- | :---- |
 | Satellite monitoring (Sentinel-1 & 2) | Quarterly | Komba GIS |
 | Risk dashboard update | Bi-annually | Komba GIS / Partner |
 | Field verification (high-risk polygons) | As needed | Partner field teams |
 | Annual EUDR report | Every 12 months | Joint output for client |

 ---

 ## 7. Disclaimer

 This report provides a **spatial and environmental risk screening** using publicly available satellite data and open datasets. It does **not** include legal verification or certification of compliance with national laws. Results should support, not replace, the broader due diligence steps required under the EUDR.

 ---

 ## 8. Contact

 **Prepared by:** Komba GIS AB  \
 Johan Karlsson – Remote Sensing & GIS Analyst  \
 📧 [johan@kombagis.se](mailto:johan@kombagis.se)  \
 🌐 [kombagis.se](https://kombagis.se)  \
 📍 Djursholm, Sweden

