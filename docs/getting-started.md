# Getting started

Use these units as practical work alongside or after the corresponding topic
has been introduced. You can work independently if you already have the
prerequisites. The tutorials explain the methods; they assume some mathematics
and basic Python rather than teaching a first programming course.

## Choose a unit

| Unit | Mathematics to know | What you will investigate |
|---|---|---|
| [A1: ODE initial value problems](units/ode-ivp/index.md) | Calculus, Taylor series and introductory ODEs | Euler, Heun and RK4; error, order, cost and stability |
| [A2: Linear systems](units/linear-systems/index.md) | Matrices, vectors and eigenvalues | Jacobi, Gauss–Seidel and SOR; convergence, cost and stopping |

Both units assume Python variables, functions and NumPy arrays; A2 also uses
loops. **A1 is not a prerequisite for A2.** Ask your lecturer for preparation
if these ideas are unfamiliar. If you are new to NumPy, start with the
[official beginner's guide](https://numpy.org/doc/stable/user/absolute_beginners.html).

## Your first session

1. Download the zip from the chosen unit's page and extract it completely.
   Open the folder containing `verify.py`.
2. Follow **tutorial section 0**: [A1 setup](units/ode-ivp/tutorial/00-setup.md)
   or [A2 setup](units/linear-systems/tutorial/00-setup.md). Install Python and
   NumPy, SciPy and Matplotlib, then check that they import successfully.
3. Run `python verify.py` in a terminal in that folder. Open
   `report/verification-report.html` in a browser. **Not implemented yet** is
   the expected starting result.
4. Edit `student/steps.py` in a plain-text or code editor, save it, and run the
   command again. Start with Euler in A1 or Jacobi in A2. Leave `verify.py`
   and `vm/` unchanged.

The code runs on your own computer. You do not need a GitHub account, a paid
service or an AI tool. A phone can be used for reading, but a computer is
needed for the practical. GitHub automation is an optional extension.

## Read the result

| Result | Meaning | Next step |
|---|---|---|
| Not implemented or missing | A method still needs to be written | Continue the tutorial and save your function |
| FAIL | A stated numerical check failed | Read its hint, inspect the code and rerun |
| All four gates pass | That method passed the supplied checks | Interpret the reported experiments; passing alone is not the whole assignment |
| A Python error | Setup or code needs attention | Read the error and the setup troubleshooting table; ask your lecturer if stuck |

Before submission, run `python verify.py --strict`. It requires all three
methods to be implemented and pass. An ordinary progress run can finish
successfully while some methods are unfinished.

## What to submit

Agree the scope with your lecturer. A full unit submission normally includes:

- your `student` folder, including `steps.py`, `student_info.txt` and
  `CONTRIBUTION.md`;
- the generated verification report;
- your AI-use disclosure in `student_info.txt`;
- a short explanation of the results and the agreed assignment or project brief.

You should be able to explain your code and conclusions in a viva. A report
records stated checks; it does not establish authorship or prove a whole
research project correct. Read [how the report works](verification-report.md).

## Working offline and planning your time

Download the unit and install Python and the packages while you have internet
access. After that, the supplied checks, bundled data and generated HTML
reports work offline. No software packages are included in the unit zip.

The bundled tutorials are Markdown (`.md`) source files. For formatted
equations offline, open the web tutorial while connected and use your browser's
**Print → Save as PDF** for the sections you need, or use a Markdown reader
that supports mathematical notation. External references need internet access.

Working time depends on your mathematics, programming experience and the
assignment scope. Allow separate time for setup, the tutorial and the project
brief; the [six-week practical outline](departments.md) is one suggested
teaching arrangement, not a measured completion time.

## For lecturers

Use the [pilot checklist and printable copy](pilot-checklist.md) to plan a
small trial. The [lecturer guide](supervisors.md) includes assessment options
and feedback questions. Send questions or setup difficulties through
[About and contact](about.md). Please describe the unit,
operating system, Python version and exact error; omit student identifiers.
