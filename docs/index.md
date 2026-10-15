---
myst:
  html_meta:
    description: "Open, verification-first course units for the computational methods used in Nigerian STEM projects and theses."
---

# verifiedmethods

<p class="lead">Open, verification-first course units for the computational methods used in Nigerian STEM projects and theses.</p>

Each unit teaches one family of methods and, just as important, how to show
that a computation is right. Students write the key step themselves, carry out
a convergence, cost and stability study, and finish with a
[verification report](verification-report.md) that a supervisor can check in
two minutes.

[Try unit A1: ODE initial value problems](units/ode-ivp/index.md){.vm-button}

## Who it is for

::::{container} vm-cards

:::{container} vm-card
**Students**

Final-year undergraduates and MSc students. Learn a method properly, check
your own code, and hand in evidence that examiners can trust.

[Start with the A1 tutorial](units/ode-ivp/tutorial/index.md)
:::

:::{container} vm-card
**Supervisors**

Give a unit to your project students. Check their computations from a short
report; viva questions and a marking rubric are included.

[For supervisors](supervisors.md)
:::

:::{container} vm-card
**Departments**

Use the units as course content for a numerical methods or research methods
practical. A six-week outline is ready to adapt.

[For departments](departments.md)
:::

::::

## How it works

1. **Download** a unit: one small zip file that runs offline.
2. **Follow the tutorial** and write the core step of each method.
3. **Run `python verify.py`.** Four checks must pass, and the evidence is
   collected in a report.
4. **Write up** a project brief using the report. The supervisor confirms the
   report and asks a few viva questions.

## Principles

Free and open
: Code under the BSD 3-Clause licence, teaching material under CC BY 4.0. Adapt
  it for your own courses.

Works where students are
: Plain Python, offline, a few seconds on a laptop with 4 GB of memory.

Students do the thinking
: The unit supplies test problems, plots and checks. The student writes the
  method and interprets the evidence.

Verification before application
: Convergence order, cost and stability come before any application.

Honest about evidence
: A report shows that code passes stated checks. It does not show who wrote the
  code; supervisors confirm reports and use viva questions for that.

## Units

| Unit | Topic | Level | Status |
|---|---|---|---|
| [A1](units/ode-ivp/index.md) | ODE initial value problems: Euler, Heun, Runge–Kutta | Undergraduate | **Prototype, ready to try** |
| [A2](units/linear-systems/index.md) | Iterative methods for linear systems: Jacobi, Gauss–Seidel, SOR | Undergraduate | **Prototype, ready to try** |
| A5 | Linear multistep and block methods | MSc / PhD | Planned |
| C1 | Epidemic models: reproduction number, fitting, identifiability | MSc / PhD | Planned |

See the full [curriculum](curriculum.md).

## Status

verifiedmethods is new. Units A1 and A2 are prototypes, to be trialled with
supervisors in Nigerian universities from November 2026. Comments, corrections and
requests for units are welcome: see [About](about.md).

```{toctree}
:hidden:

curriculum
units/ode-ivp/index
units/linear-systems/index
verification-report
supervisors
departments
about
```
