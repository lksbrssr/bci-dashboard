# Draft direct-link verification

Runtime source: `3947525f2e43a081d544cd5e00b93872c28ea989`, based on `d81c9751e225a044ce44b823d6b423b15f7b05fd`.

- **187 tests pass** (`npm test`); typecheck, changed-source ESLint and production build pass.
- A separate frozen-install production build with `NEXT_PUBLIC_BASE_PATH=/neuro-atlas` passes. This disposable checkout alone uses the established explicit loopback-only auth fixture; it is not committed or deployed.
- **120 fresh-link browser cases pass:** each of the 19 candidates and 21 panels at 1440/390/320 px. They select Draft, reveal the exact target, open gap details where applicable and retain the actual path/query. The report enumerates every case.
- Native Direct/repeat/Copy controls, actual clipboard readback, cross-tab Back/Forward and existing Metrics modal return/Forward/Close pass at all three widths. Clipboard permission is scoped to the loopback origin and restored.
- Existing Draft regression passes at all three widths: 19 candidates, 57 numeric marks, explicit gaps, unclipped SVG text, point/keyboard/source-table interactions and existing metric-link focus restoration.
- All **15 existing modal/viewport cases** and supplementary graph history, filtering, dark/reduced-motion and route checks pass. The modal probe now preserves the configured base path for its ancillary route checks.
- No document overflow in these cases. Narrow checks use desktop Chrome viewport emulation and native pointer/keyboard input, not physical-phone touch.

Screenshots in `docs/screenshots/draft-links-*.png` show actual local production UI at the runtime revision above: the desktop candidate with both panels, a 390px candidate landing, a 320px independent panel landing, and a 390px expanded evidence gap. They contain only the repository's existing public-source chart material.

All later commits are QA/docs/evidence only; runtime, data, dependencies and authentication are byte-identical to the pinned source. Neither a local fixture nor an unchanged authentication source proves authenticated hosted behavior. Hosted PLRD browser QA is blocked by browser policy; no positive hosted verification, merge or deployment is claimed.

The frozen install reports pre-existing audit warnings (nine high, one critical); this feature does not change dependencies or lockfile.

## Harness notes

The native probe retries only read errors during document reload. In shared headed Chrome, another task window can make this page hidden and suspend animation frames; it brings the exact task page to front during bounded waits. It rechecks viewport and hit geometry after capture before dispatching native input. These are test-harness corrections, not application changes or simulated clicks.
