# Data Quality

## Lineage

Sample and assay data are captured from both open-file company exploration reports and NTGS projects.

Exploration data are extracted from legacy hardcopy reports by scanning and digitising, including spatial data capture from maps where necessary. Legacy data capture has been completed at various times and usually on a geological terrain basis.

More recent exploration reports and data are supplied in digital formats and uploaded directly into a database after transcription to a standard loading template.

NTGS data primarily relate to rock samples undergoing whole-rock geochemical analysis. NTGS undertakes QA/QC on NTGS-collected samples, assessing precision and accuracy using internationally recognised standard reference materials and NTGS in-house standards, including the identification of duplicates and blanks.

Data are transferred into a SQL Server database and validated twice:
- At the template stage (before entry)
- During loading into the database

Final data are extracted using ETL tools and loaded into STRIKE as ESRI shapefiles.

## Positional Accuracy

Approximately:
- ±20–50 metres using 100k topographical maps
- ±1–10 metres using GPS

Decimal latitude and longitude values are available for each site.

## Attribute Accuracy

- Analyses are performed by laboratories to set standards.
- Geological observations and descriptive attributes are recorded by Geological Survey geologists.

## Logical Consistency

Data are logically consistent for the purposes of geological interpretation.

## Completeness

- Data completeness depends on mandatory fields being completed.
- Data are not entered into the database without location data.
- All sample types are available in NT Geochemistry Datasets.

**Notes:**
- Drill samples are not available on STRIKE (NTGS web mapping application): http://strike.nt.gov.au  
- Laboratory method information is included in Digital Information Package 001 (DIP001).  
- Reports can be searched and downloaded via GEMIS: https://geoscience.nt.gov.au/gemis
