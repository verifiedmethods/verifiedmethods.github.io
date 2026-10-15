# A1: ODE initial value problems

<p class="vm-meta">Level: final-year undergraduate (also an MSc refresher) · Language: Python · Status: prototype</p>

<p class="vm-meta">Students should know: calculus including Taylor series, a first course in ordinary differential equations, and basic Python with NumPy arrays.</p>

Students write three one-step methods for $y' = f(t, y)$: Euler's method,
Heun's method and the classical fourth-order Runge–Kutta method. Then they show
with evidence that their code works: the observed convergence order, the error
against the cost, and the stability limits. This turns the familiar
"comparative study of Euler and Runge–Kutta methods" into a proper
verification study.

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

Unzip the file, open a terminal in the unzipped folder, and set up once.

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
help for common problems. Anaconda users can skip the setup and run
`python verify.py` from the Anaconda Prompt.

## What students learn

After this unit a student can:

- derive Euler's method from the Taylor series, and implement Euler, Heun and
  classical RK4 for systems of equations;
- measure the observed order of convergence and explain why it departs from
  theory at large step sizes and near rounding level;
- compare methods by the work needed for a target accuracy, not by the error at
  one step size;
- explain stability limits, stiffness and why explicit methods fail on stiff
  problems;
- produce and interpret a verification report.

## What is in the unit

| | |
|---|---|
| [Tutorial](tutorial/index.md) | Nine short sections, from setting up Python to choosing a project brief |
| [Project briefs](briefs/index.md) | Comparing methods properly; Nigeria's population with the logistic model; stiffness |
| [For supervisors](supervisors/index.md) | Confirming a report, viva questions, a marking rubric, an AI-use statement |
| `verify.py` | Four gates and five reported results, written to an HTML report |

## Licence and citation

Code: BSD 3-Clause. Tutorial, briefs and supervisor material: CC BY 4.0.
Population data in brief 2: World Bank, CC BY 4.0. A DOI will be added at the
first release; until then, cite as: Tiamiyu, A. T. (2026), *verifiedmethods
unit A1: ODE initial value problems*, version 0.1.0.dev0,
https://verifiedmethods.github.io.

```{toctree}
:hidden:

tutorial/index
briefs/index
supervisors/index
```
