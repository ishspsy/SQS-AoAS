# Reproducibility components for the AoAS resubmission

The four analysis archives are available from the [reproducibility release](https://github.com/ishspsy/SQS-AoAS/releases/tag/aoas-resubmission-2026-09-15). The repository README and `download_reproducibility.py` explain how to download, verify, and assemble the large ZIPs from their parts. They all extract to `AoAS_revision_complete_20260914`. Extract the two older numerical-record archives first, then the historical-data archive, and the current code archive last, retaining their common directory structure. Extract the current manuscript-source archive last of all when compiling the paper. This order preserves the latest table descriptions and source bindings where older archives contain an earlier copy. Run commands from that combined directory. The code archive alone contains selected summaries, not every public download or fitted array.

| Archive | Contents and role |
| --- | --- |
| `AoAS_code_and_reproducibility_linked_20260915.zip` | Analysis scripts, environments, configurations, scientific protocols and timestamp receipts, source manifests, selected results, and table/figure sources. |
| `AoAS_historical_data_and_records_20260914.zip` | Public raw and derived data for the historical CCLE, AML, PRISM, gCSI, GDSC1 and intervention studies; full reported historical simulations and application records; the final selection tuning pilot; relevant failed execution records. |
| `AoAS_additional_numerical_records_20260914.zip` | Full records for 900 high-dimensional inference data sets, 600 structural-comparison data sets, 200 fixed-panel data sets, the tested-dimension analysis, later NCI-60 follow-up and numerical completion history. |
| `AoAS_NCI60_numerical_records_20260913.zip` | Both official CellMiner processed-data ZIPs, source/compound registries, the primary 400 NCI-60 fitting tasks and their complete records. |

The separately supplied manuscript-source ZIP has self-contained main and supplementary TeX sources. Use its `SOURCE_README.md` to compile the PDFs. Editorial letters and internal manuscript audits are separate from the public analysis supplement.

## Environments and entry points

`README.md` gives the exact historical commands, source URLs and SHA-256 checks; `FULL_REVISION_20260913.md` gives the later numerical commands. Use the environment specified for the relevant study: `requirements.txt`, `requirements-20260913.txt`, or the NCI-60 specification under `config/`. The guides also identify R dependencies for the PharmacoSet and intervention calculations. Relative paths below are within `reproducibility/`.

| Reported analysis | Complete saved records | Main reconstruction or verification script in `code/` |
| --- | --- | --- |
| Selection/estimation/prediction simulations, 30 settings × 100 replications | `results/legacy_selection_100_20260805/`, `results/legacy_selection_100_20260805_baselines/`, `results/legacy_fixed_tuning_20260805.json`, and `results/legacy_kkt_pilot3_seed20260805_v14_current_20260805/` | `summarize_legacy_fixed_results.py`; fitting commands in `README.md` |
| CCLE repeated splits and structural diagnostics | `results/ccle_repeated_30_20260805/`, `results/revision_summary/`, `results/ccle_rank_feasibility_20260817_p6/`, `results/ccle_rank_feasibility_20260817_p20/` | `summarize_revision_results.py`, `summarize_unfiltered_score_factors.py` |
| Misspecification, heavy tails, density dependence and initialization | `results/robustness_100_20260805/`, `results/density_robustness_100_20260820/`, `results/heavy_tail_robustness_100_20260820/`, `results/multistart_100_20260820/` | `summarize_additional_robustness.py` and commands in `README.md` |
| Beat AML development/confirmation and empirical criteria | `results/beataml2_20260821/`, `results/empirical_resolution_20260822/` | `verify_beataml2_complete.py`, `verify_empirical_resolution_complete.py` |
| TCGA-LAML/FIMM-AML fixed-score validation | `results/tcga_laml_external_validation_20260823/`, `results/fimm_aml_external_validation_20260823_v3/`, earlier failed FIMM directories | `verify_tcga_laml_external_validation.py`, `verify_fimm_aml_external_validation_v3.py` |
| FIMM pathway structure and plasma CCL2 | `results/fimm_pathway_structure_20260823/`, `results/modak_development_bridge_20260823/` | `verify_fimm_pathway_structure.py`, `verify_modak_development_bridge_v2.py` |
| PRISM/paired CCLE and population-moment analyses | `results/prism23q2_external_20260821/`, `results/ccle_prism_subspace_20260821/`, `results/stronger_empirical_evidence_20260823/` | `verify_stronger_empirical_evidence_v2.py`; exact PRISM commands in `README.md` |
| gCSI, intervention and GDSC1 | `results/external_rescue_20260823/`, `results/causal_rank_subspace_20260822/` | `validate_gcsi_primary_prediction.py`, `verify_causal_rank_subspace_complete_v4.py`, `validate_shoc2_trametinib_meta.py` |
| Original Wald calibration and direct AML SQS score | `results/inference_calibration_20260913/`, `results/sqs_structural_value_20260913/` | Commands under the corresponding headings in `README.md` |
| Cross-fitted inference, spectral comparisons and NCI-60 | Full later-record directories in the two September numerical archives | Exact saved-array checks and fitting commands in `FULL_REVISION_20260913.md` and the NCI-60 section of `README.md` |

The source downloads and their annotations are retained in the `data_*` directories. Design locks and RFC3161 receipts remain under `locks/`; local production protocols do not become external preregistrations merely because they are included. Their scientific timing and any availability or execution amendments remain as originally recorded.

## Reconstructing versus refitting

Use the saved-array validation and summary commands first when inspecting the reported numbers. These commands require all relevant archive components. Fitting drivers can be substantially more expensive and often refuse to overwrite completed tasks; use a separate fresh output directory and the documented seeds, versions, tuning records and execution plan when refitting. Do not regenerate historical scientific locks or timestamps. Source-download commands can retrieve the public data again, but first compare each download with the recorded hash.

The historical archive excludes superseded August 4 selection results, unused exploratory grids and smoke tests. It retains the independent pilot that selected the reported fixed penalties and the failures or amendments relevant to the reported analyses. Unavailable targets and negative findings remain in the final result directories.

Each archive includes or is bound by a content manifest. `release_manifest.json` in the repository records the original archive sizes and checksums, the download parts, and their extraction order. Those checksums verify delivery; scientific correctness is assessed from the code, data, protocols and full results.

The machine-specific GDSC2 attempt-5 launcher and the optional source-faithful ADMM diagnostics in the historical guide document earlier investigations. Neither supplies a reported result. The failed GDSC2 attempt must not be treated as a completed analysis, and recreating its original locked workstation is unnecessary for the reported PRISM, gCSI or GDSC1 results. The primary reconstruction entry points are those in the table above.
