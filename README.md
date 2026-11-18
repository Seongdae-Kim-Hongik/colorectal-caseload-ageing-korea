# Population ageing, not rising treatment rates, explains growing colorectal cancer caseloads in Korea

Analysis code for the manuscript

> Kim S. *Population ageing, not rising treatment rates, explains growing colorectal cancer caseloads in Korea.* Manuscript submitted for publication.

Archived release: Zenodo, https://doi.org/10.5281/zenodo.24332391 (v1.0.1).

## Contents

This repository contains code only. The processed district-year data (master table, analytic panel, expected counts, result tables, adjacency graph, and boundary file) are not included; they are available from the author on reasonable request. All source statistics are public (see Data sources).

| Path | What it is |
|---|---|
| `01_스크립트/` | Analysis scripts (below) |
| `04_분석/CRC/sets_CRC_std3.json`, `config_CRC_std3.json`, `narrative_CRC.md` | Prespecified covariates, expected directions, forced controls, and model settings |
| `04_분석/CRC/run_std3_chain.sh` | Order in which the model scripts were run |
| `04_분석/CRC/MS/build/numbers_crc.py` | Reads the result tables and computes every number reported in the manuscript, including the three-factor decomposition of the change in treated people (population growth, population ageing, age-specific treatment rates), with consistency checks |
| `04_분석/CRC/MS/build/figs_crc.py` | Draws Figures 1-2 and Supplementary Fig. S1 from the result tables and the boundary file |

Folder and some column names are in Korean because the source tables are Korean; each script has a header comment that describes its inputs and outputs.

## Data sources

All inputs are public, aggregated statistics. No individual-level data are included.

- Annual numbers of people treated for colorectal cancer (ICD-10 C18-C21, principal diagnosis), by district of residence: National Health Insurance Service, Regional Medical Care Utilization Statistics, 2011-2024.
- Mid-year population by 5-year age group: Ministry of the Interior and Safety, resident registration statistics. The 2023 age block of Changwon duplicated the 2022 block in the source file and was corrected (`population_override` in `sets_CRC_std3.json`).
- District covariates (behaviours, borderline glucose, obesity and abdominal obesity at screening, physical activity, sports facilities, social and deprivation indicators, screening uptake): Korean Statistical Information Service (KOSIS), the Community Health Survey, and NHIS statistics.
- Densities of entertainment and singing bars, general restaurants, and delivery-oriented food outlets, and out-of-district outpatient share: derived from local-government business licensing registers (Ministry of the Interior and Safety, data.go.kr) and NHIS statistics; `01_스크립트/99b_extra_canonical_pool.py` joins them by district code (set `ST_CANON` or `ST_DATA_ROOT`).

## Pipeline

Run from the repository root. Scripts 36, 38, 39, 40 and 80 rebuild the expected counts and the panel from the master tables; their raw-input paths are read from environment variables. With the processed data, the analysis can be reproduced from step 4.

| Step | Script | Output |
|---|---|---|
| 0 | `99b_extra_canonical_pool.py` | Licensing-register and access indicators by district code |
| 1 | `36_build_national_agerates.py`, `38_build_Estd_all.py`, `39_build_Estd_fine.py` | National age rates and expected counts |
| 2 | `98_screen_std.py` | Spatial screening on age-standardised ratios |
| 3 | `80_build_disease_panel_v.py CRC` (`ST_VER=std3`) | Analytic panel |
| 4 | `81_fit_inla.R CRC` (`ST_VER=std3`, `ST_GRAPH=04_분석/CRC/graph_593.graph`, `ST_THREADS=1`; multiverse split with `ST_MV_STOP=1` then `ST_MV_RANGE=a-b` workers, see `04_분석/CRC/run_std3_chain.sh`) | Principal model, covariate-set comparison, 200-subset analysis, window models |
| 5 | `85_window_maps.R`, `86_yearly_maps_ehsa.py`, `86b_ehsa_modified_mk.py`, `87_window_grid.py` | Maps, emerging hot spot analysis |
| 6 | `88g_sens_prep.py CRC std3 GCA,ARTH` then `88g_sens_suite.R` (`GROUP=1..6`) | Sensitivity suite |
| 7 | `88h_ppc_varpart.R` | Posterior predictive checks, variance partition |
| 8 | `88k_struct_kh.R` (groups nb, struct, kh, review) with `kh_constraints.R` | Knorr-Held I-IV, neighbourhood and prior variants, residual Moran's I, parsimonious model, regional slopes, access sensitivity |
| 9 | `89g_sens_combine.py` | Combined sensitivity tables |
| 10 | `04_분석/CRC/MS/build/numbers_crc.py`, `figs_crc.py` | Reported numbers and figures |

Example:

```bash
cd 01_스크립트 && ST_VER=std3 ST_THREADS=1 ST_GRAPH=../04_분석/CRC/graph_593.graph Rscript 81_fit_inla.R CRC
```

The boundary file is found at `data/boundary/final.shp` by default; set `ST_SHP` to use another path.

## Software

R 4.6.0 with R-INLA 25.10.19, spdep 1.4.2 and sf 1.1.1; Python 3.9.6 with pandas 2.3.3, geopandas 1.0.1, numpy 2.0.2 and matplotlib 3.9.4.

## License

Code: MIT License (`LICENSE`).

## Contact

Seongdae Kim, Hongik University (kimsd@hongik.ac.kr)
