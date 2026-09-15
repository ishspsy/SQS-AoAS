# Quantile Modeling of Correlated Drug Responses with Low-Rank and Sparse Structure

**Youngjin Cho, Eun Ryung Lee, and Seyoung Park**

This repository provides the analysis code, data-source records, and numerical results accompanying our resubmission to *The Annals of Applied Statistics*. The method estimates correlated response quantiles while selecting common predictor rows and low-rank coefficient structure. The materials cover simulations, cross-fitted inference, and the CCLE, AML, NCI-60, and external pharmacogenomic analyses reported in the manuscript.

## Download the materials

[**AoAS resubmission release: September 15, 2026**](https://github.com/ishspsy/SQS-AoAS/releases/tag/aoas-resubmission-2026-09-15)

The release contains four archives. The two largest ZIPs are split into files ending in `.part01`, `.part02`, and `.part03` to meet the hosting limit. These parts must be combined before opening the ZIP. The script below performs the downloads, combination, and SHA-256 checks.

| Archive | Contents |
| --- | --- |
| `AoAS_code_and_reproducibility_linked_20260915.zip` | Analysis scripts, software specifications, configurations, scientific protocols, source manifests, selected summaries, and reconstruction instructions. |
| `AoAS_NCI60_numerical_records_20260913.zip` | Official CellMiner processed-data sources, compound registries, and the primary NCI-60 fitting records. |
| `AoAS_additional_numerical_records_20260914.zip` | Additional inference, structural-comparison, fixed-panel, and NCI-60 records. |
| `AoAS_historical_data_and_records_20260914.zip` | Public data sources and complete records for the earlier simulations and pharmacogenomic studies. |

The compressed files total approximately 8.15 GB. Keep sufficient space for the downloaded parts, reconstructed ZIPs, and extracted data. The code ZIP alone does not contain all raw data or fitted arrays.

### Download and verify

Download this repository using **Code > Download ZIP**, then extract it. From that directory, run the following with Python 3.9 or later:

```bash
python3 download_reproducibility.py --output-dir aoas-records --extract
```

The download script uses only the Python standard library. It verifies each part, reconstructs the original ZIPs, checks their complete hashes, and extracts them in the required order. It does not fit statistical models. Run it again after a network interruption to resume partial downloads; verified completed files are reused.

The combined analysis directory is:

```text
aoas-records/extracted/AoAS_revision_complete_20260914/
```

For files downloaded manually from the release page, place every ZIP and part in one directory and run:

```bash
python3 download_reproducibility.py --output-dir aoas-records --assemble-only --extract
```

`release_manifest.json` records file sizes, SHA-256 hashes, and the extraction order. The extraction command requires a new `extracted/` directory to protect existing analyses. If a downloaded file fails verification, move that file aside before retrying.

## Reproduce a reported analysis

Start with [REPRODUCIBILITY.md](REPRODUCIBILITY.md), which maps each study to its saved records and reconstruction commands. After extracting the archives:

1. Read `reproducibility/README.md` for the original data sources, preprocessing, historical analyses, and software versions.
2. Read `reproducibility/FULL_REVISION_20260913.md` for the additional inference, spectral, and NCI-60 studies.
3. Use the environment specified for the selected study in `requirements.txt`, `requirements-20260913.txt`, or the corresponding `config/` specification.
4. Run the documented saved-result checks before refitting. Refitting can require substantially more computation; use a fresh output directory and the stated seeds and tuning rules.

## Interpretation and data sources

The records retain all reported comparisons, including negative findings, unavailable targets, and relevant unsuccessful computations. The NCI-60 application is exploratory; it does not establish an additional spectral advantage over the row-only or published-marker controls. External observational associations do not establish a causal drug-response mechanism.

Original public data releases, versions, source hashes, and applicable source terms are documented in the study guides and source manifests. Scientific protocols and timestamp receipts document the recorded analysis sequence; they are not external preregistrations.

## Reference

Cho, Y., Lee, E. R., and Park, S. (2026). *Quantile Modeling of Correlated Drug Responses with Low-Rank and Sparse Structure*. Manuscript submitted to *The Annals of Applied Statistics*.
