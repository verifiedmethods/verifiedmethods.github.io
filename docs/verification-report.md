# The verification report

Every unit ends with one command, `python verify.py`. It runs the unit's
checks on the student's code and writes a single HTML file that opens in any
browser, offline. It supports assessment alongside a student's explanation
and a lecturer's rerun; it is not a certificate of research validity.

<a class="vm-button" href="examples/a1-example-report.html">Example report: unit A1</a>
<a class="vm-button" href="examples/a2-example-report.html">Example report: unit A2</a>

New to interpreting the evidence? Follow the
[A1 report walkthrough](a1-report-walkthrough.md) to read the summary, error
tables and plots, then explain what the results support.

## What is in it

The first page
: The student's details, the date, a fingerprint of the student's code, a
  fingerprint of the checks, the modules the code imports, and a summary: for
  each method, how many gates passed and its observed order (A1) or convergence
  factor on the specified test problem (A2).

The comparison plots
: A1 shows error against step size and work. A2 shows sweeps against the SOR
  relaxation factor and residual histories. Both include detailed tables.

The statement
: What the report shows and what it does not (below), and the student's
  disclosure of any use of AI tools.

The details
: For each method, the gates and the reported results with every number.

## Gates and reported results

A **gate** must pass. In unit A1 the gates ask:

| Gate | Question |
|---|---|
| G1 | Does one step give the same numbers as the method, up to rounding? |
| G2 | Does the step evaluate $f$ exactly as often as the method requires? |
| G3 | Does it work for systems, without changing its input? |
| G4 | Does the error fall at the rate theory predicts (observed order within 0.1)? |

The gates were tested against deliberately broken implementations (wrong stage
times, wrong weights, missing step size, a library solver inside the step, and
others): every one fails at least one gate. Unit A2 has four gates of the same
kind; its central one compares an average convergence factor between sweeps
100 and 200 on a specified Poisson problem with the spectral radius of the
method's iteration matrix, allowing a relative difference of 0.1%. The
spectral radius does not prescribe every stepwise error ratio in general.

For a completed submission, `python verify.py --strict` requires every method
to pass. Ordinary local runs allow unfinished work; a zero exit code in that
progress mode is not evidence that all methods are complete. GitHub Actions
uses strict checking automatically.

A **reported result** has no pass mark. It is the evidence the student
interprets in the write-up. In A1 these include error tables, comparison with
SciPy and behaviour on a stiff problem; in A2 they include sweep counts,
relaxation-factor choice, failure cases and residual versus error.

## What a report shows, and what it does not

A report shows that the code with the stated fingerprint passed the stated
checks. Passing gives evidence about those tested cases; it is not a proof
for every input or a validation of a new model or application. It does
**not** show who wrote the code, and a report produced on a student's own
computer could in principle have been edited. So:

1. **To confirm a report,** first look through the student's `steps.py`: it
   should be short and import only NumPy (the report lists its imports and
   warns about anything else, because code in that file runs alongside the
   checks). Then copy the student's `student` folder into a fresh copy of the
   unit and run `python verify.py --strict` yourself. The check-suite fingerprint should
   match the one published on the unit's page.
2. **To confirm understanding,** ask a few of the viva questions in the unit's
   supervisor material, for example: "Show me where your code evaluates $k_2$,
   and why at $t + h/2$."

## Pilot versions and fingerprints

A fingerprint is an identifier, not a signature or proof that a report is
authentic. Confirm the code and checks by rerunning them. A1 and A2 now have
versioned pilot prereleases (`0.1.0a1`), with a tagged download, SHA-256
checksums and a manifest. We will publish corrections under a new version
rather than replace a pilot download. Keep the original unit zip and report
with the submission, and compare results using the same checker version.

GitHub automation is optional. The pilot download's workflow fetches the
official checker for that version, verifies its pinned SHA-256, replaces the
local checker and runs strict submission checks. The workflow can itself be
edited, so a green result alone does not authenticate a submission; lecturers
should still inspect and rerun the student's code.

Older `0.1.0.dev0` downloads used the checker in the student's repository and
could change without a new version label. If reviewing an older report, retain
its original zip and establish which checker was used before comparing results.

```{toctree}
:hidden:

a1-report-walkthrough
```
