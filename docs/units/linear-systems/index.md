# A2: Iterative methods for linear systems

<p class="vm-meta">Level: final-year undergraduate (also an MSc refresher) · Language: Python · Status: prototype</p>

<p class="vm-meta">Students should know: matrices, vectors and eigenvalues, and basic Python with NumPy arrays.</p>

Students write one sweep of three classical methods for $Ax = b$: Jacobi's
method, the Gauss–Seidel method and successive over-relaxation (SOR). Then they
show with evidence that their code works: the error must fall, sweep by sweep,
by exactly the spectral radius of the method's iteration matrix. They also
study how the number of sweeps grows with the size of the system, how to choose
the relaxation factor, when the methods fail, and why a small residual does not
guarantee a small error. This turns the familiar "comparative study of Jacobi
and Gauss–Seidel" into a proper verification study.

## Download

```{include} _download.md
```

The **check-suite fingerprint** lets a supervisor confirm that a student's
report was produced by the official checks for this version (see
[the verification report](../../verification-report.md)).

To confirm that the download is complete and unchanged, compare its SHA-256
with the value above: on Windows run `certutil -hashfile <file> SHA256`, on
macOS `shasum -a 256 <file>`, on Linux `sha256sum <file>`.

## Quick start

Unzip the file, open a terminal in the unzipped folder, and set up once (or
reuse the environment from unit A1).

**Windows** (Command Prompt):

```
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

**macOS and Linux:**

```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Then run `python verify.py` and open `report/verification-report.html` in a
browser. [Tutorial section 0](tutorial/00-setup.md) explains each step, with
help for common problems.

## What students learn

After this unit a student can:

- derive Jacobi's method from the equations, and implement Jacobi, Gauss–Seidel
  and SOR sweeps that work for any size of system;
- explain the iteration matrix and why the error falls by its spectral radius
  per sweep, and measure that factor;
- predict how the number of sweeps grows with the size of the system, and
  choose the relaxation factor for SOR;
- recognise when the methods fail, and why the classical sufficient conditions
  are not the whole story;
- explain the difference between the residual and the error, and choose a
  stopping tolerance.

## What is in the unit

| | |
|---|---|
| [Tutorial](tutorial/index.md) | Nine short sections, from setting up Python to choosing a project brief |
| [Project briefs](briefs/index.md) | Comparing the methods properly; steady temperature in a heated plate; when the methods converge |
| [For supervisors](supervisors/index.md) | Confirming a report, viva questions, a marking rubric, an AI-use statement |
| `verify.py` | Four gates and five reported results, written to an HTML report |

## Licence and citation

Code: BSD 3-Clause. Tutorial, briefs and supervisor material: CC BY 4.0. A DOI
will be added at the first release; until then, cite as: Tiamiyu, A. T. (2026),
*verifiedmethods unit A2: iterative methods for linear systems*, version
0.1.0.dev0, https://verifiedmethods.github.io.

```{toctree}
:hidden:

tutorial/index
briefs/index
supervisors/index
```
