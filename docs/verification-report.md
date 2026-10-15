# The verification report

Every unit ends with one command, `python verify.py`. It runs the unit's
checks on the student's code and writes a single HTML file that opens in any
browser, offline. A supervisor can read the first page in two minutes.

<a class="vm-button" href="examples/a1-example-report.html">See an example report (unit A1)</a>

## What is in it

The first page
: The student's details, the date, a fingerprint of the student's code, a
  fingerprint of the checks, the modules the code imports, and a summary: for
  each method, how many gates passed and the observed order of convergence.

The comparison plots
: Error against step size, with the theoretical slopes, and error against the
  amount of work.

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
others): every one fails at least one gate.

A **reported result** has no pass mark. It is the evidence the student
interprets in the write-up: error tables, comparison with SciPy, behaviour on
a stiff problem.

## What a report shows, and what it does not

A report shows that the code with the stated fingerprint passed the stated
checks: strong evidence that it implements the method correctly. It does
**not** show who wrote the code, and a report produced on a student's own
computer could in principle have been edited. So:

1. **To confirm a report,** first look through the student's `steps.py`: it
   should be short and import only NumPy (the report lists its imports and
   warns about anything else, because code in that file runs alongside the
   checks). Then copy the student's `student` folder into a fresh copy of the
   unit and run `python verify.py` yourself. The check-suite fingerprint should
   match the one published on the unit's page.
2. **To confirm understanding,** ask a few of the viva questions in the unit's
   supervisor material, for example: "Show me where your code evaluates $k_2$,
   and why at $t + h/2$."
