# Draft chart direct links

The existing `#draft-charts` tab location is unchanged. Draft candidates and their evidence panels now have separate durable URLs, resolved by the same Field velocity history subscription.

- All 19 candidates have explicit IDs: 14 plotted candidates and five evidence gaps.
- All 21 panels have explicit IDs: 20 numeric scatter panels and one categorical timeline. Panel links select that panel rather than a neighboring plot in a multi-panel candidate.
- Fresh URLs, native fragment changes, same-page Direct links (including repeat clicks), and Back/Forward select Draft before scrolling the target below the header. A gap link opens its evidence disclosure. The general section link retains its previous no-forced-scroll behavior.
- Candidate and panel controls expose **Direct link** and **Copy link**. Copy preserves the actual origin, base path and complete query string; it does not navigate. A clipboard failure leaves the native Direct link available and announces the failure.
- Existing Metrics modal URLs, data, chart rendering, provenance and hosted authentication are unchanged. No auth fixture is included in this branch.

## Stable ID contract

`src/data/draft-chart-links.ts` is the public fragment registry. IDs are deliberately not derived from mutable titles or card positions. `plotId` refers to the existing evidence ID; null identifies the categorical timeline. Keep IDs stable when titles change, and retain an alias if a future change truly requires a new identity. The pinned independent regression fixture is `tests/fixtures/draft-chart-links.json`.

Append these fragments to the current Field velocity route, including any deployment prefix (for the PLRD mount, `/neuro-atlas/field-velocity`). These are source-proposed URLs until this feature is merged and released by its owner.

| Candidate | Candidate fragment | Panel fragments |
|---|---|---|
| Brain tissue mapped over time | `#draft-brain-tissue-mapped` | `#draft-panel-tissue-cm3` |
| Largest published connectome over time | `#draft-largest-connectome` | `#draft-panel-largest-connectome-neurons`, `#draft-panel-largest-connectome-synapses` |
| Connectomics imaging throughput over time | `#draft-imaging-throughput` | `#draft-panel-acquisition-rates` |
| Cost to map 1 cm³ over time | `#draft-mapping-cost` | Evidence gap — no panel |
| Automated reconstruction accuracy over time | `#draft-reconstruction-accuracy` | `#draft-panel-pathfinder-nerl` |
| Human proofreading burden over time | `#draft-proofreading-burden` | `#draft-panel-proofreading-effort` |
| Human tissue preservation quality over time | `#draft-tissue-preservation` | Evidence gap — no panel |
| Tissue loss in subdivision/sectioning over time | `#draft-sectioning-loss` | `#draft-panel-gauss-section-rejection`, `#draft-panel-microns-section-loss` |
| Molecular annotation coverage over time | `#draft-molecular-annotation` | Evidence gap — no panel |
| Humans with implanted high-bandwidth BCIs over time | `#draft-implanted-bci-humans` | `#draft-panel-neuralink-cumulative`, `#draft-panel-paradromics-connect-one` |
| Neural recording hours collected over time | `#draft-recording-hours` | `#draft-panel-tusz-scalp-eeg`, `#draft-panel-ajile12-intracranial`, `#draft-panel-poyo-primate-training`, `#draft-panel-japaneeg-scalp-eeg` |
| Paired structure–function dataset scale over time | `#draft-paired-structure-function` | `#draft-panel-paired-manual`, `#draft-panel-paired-auto` |
| Comparative connectomics cohort size over time | `#draft-comparative-cohorts` | `#draft-panel-comparative-specimens` |
| Open-access connectomics data over time | `#draft-open-access-data` | `#draft-panel-public-data-size` |
| Public connectome reuse over time | `#draft-connectome-reuse` | Evidence gap — no panel |
| Simulation/emulation fidelity over time | `#draft-simulation-fidelity` | `#draft-panel-flyvis-contrast` |
| Number of simulations/emulations over time | `#draft-simulation-count` | Evidence gap — no panel |
| NeuroAI performance–cost frontier over time | `#draft-neuroai-frontier` | `#draft-panel-neuroai-imagenet` |
| Demonstrated applications enabled by connectomics over time | `#draft-connectomics-applications` | `#draft-panel-application-events` |

## Reproduction and scope

Run `npm ci`, `npm test`, `npm run typecheck`, changed-source ESLint and `npm run build`. The integration regression mounts real VelocityTabs under StrictMode, exercises every candidate and panel, verifies exact URL preservation, same-target history idempotence, gap disclosure, clipboard success/failure and existing modal return behavior.

Native probe: `scripts/qa/draft-links-browser.py` through **browser-harness**, in an owned window. Set `ATLAS_QA_URL` to the loopback Field velocity route, `ATLAS_QA_OUTPUT` to a scratch directory and `ATLAS_QA_LINKS` to the absolute regression-fixture path. It checks every fresh target at 1440/390/320 px plus native direct/repeat/copy interactions, actual clipboard readback and cross-tab/modal history. The previous Draft and modal probes remain additional regression coverage.

Use a disposable checkout at the pinned source revision, with its own frozen dependency install and the established explicit loopback-only QA auth fixture. Bind the server only to `127.0.0.1`. Never copy a production password into a fixture or commit/push/deploy the fixture. Source-build and local UI evidence do not establish authenticated hosted behavior. Browser policy blocks the hosted PLRD domain, so no positive hosted QA is claimed.
