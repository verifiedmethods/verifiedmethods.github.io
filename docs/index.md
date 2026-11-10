---
myst:
  html_meta:
    description: "Free numerical methods practicals: implement, test and explain computations, with teaching and assessment material for lecturers."
---

# verifiedmethods

<p class="lead">Turn numerical methods taught in class into computations students can test, explain and reproduce.</p>

verifiedmethods provides free, adaptable practical units for numerical methods
teaching and preparation for computational projects in Nigerian STEM programmes.
Students implement the core methods, examine their numerical behaviour and
interpret the evidence in a [verification report](verification-report.md).
Lecturers get tutorials, assignment briefs, marking rubrics and viva questions.

[Getting started](getting-started.md){.vm-button}
[For lecturers and supervisors](supervisors.md){.vm-button}

## Where it fits in teaching

Use a unit **alongside or shortly after the relevant topic is introduced**.
For example, teach Euler's method, then let students implement it and measure
how the error changes with the step size. Repeat with Heun and Runge–Kutta.
There is no need to wait until the whole course ends. Project students can
also use a unit as a refresher before developing their own investigation.

## Who it is for

::::{container} vm-cards

:::{container} vm-card
**Students**

Undergraduates who have met the relevant mathematics and basic Python;
also MSc students revising the foundations. Implement methods, interpret
results and prepare evidence for assessment.

[Start with the A1 tutorial](units/ode-ivp/tutorial/index.md)
:::

:::{container} vm-card
**Lecturers and supervisors**

Assign a practical after teaching a topic, or use a unit with project students.
Rerun their work and assess their explanations with the included rubric and
viva questions.

[Plan a first trial](supervisors.md)
:::

:::{container} vm-card
**Departments**

Use the units as course content for a numerical methods or research methods
practical. A six-week outline is ready to adapt.

[For departments](departments.md)
:::

::::

## How it works

1. **Choose and download** A1 or A2, then install Python and the required
   packages once. GitHub is optional.
2. **Follow the tutorial** and write the core step of each method. The first
   report normally says the methods are not implemented yet.
3. **Run `python verify.py`** as you work. Before submitting, run
   `python verify.py --strict`; every method must pass all four gates.
4. **Explain the results** in the agreed assignment or project brief. The
   lecturer reruns the checks and uses a short viva to assess understanding.

## Principles

Free and open
: Code under the BSD 3-Clause licence, teaching material under CC BY 4.0. Adapt
  it for your own courses.

Works where students are
: The provided checks and reports run locally after Python and the packages
  are installed. See [getting started](getting-started.md) for offline study
  and setup requirements.

Students do the thinking
: The unit supplies test problems, plots and checks. The student writes the
  method and interprets the evidence.

Verification before application
: Check the implementation and its numerical behaviour before interpreting
  an application.

Honest about evidence
: A report shows that code passes stated checks. It does not show who wrote the
  code; supervisors confirm reports and use viva questions for that.

## Units

| Unit | Topic | Level | Status |
|---|---|---|---|
| [A1](units/ode-ivp/index.md) | ODE initial value problems: Euler, Heun, Runge–Kutta | Undergraduate | **Prototype, ready to try** |
| [A2](units/linear-systems/index.md) | Iterative methods for linear systems: Jacobi, Gauss–Seidel, SOR | Undergraduate | **Prototype, ready to try** |

Only A1 and A2 are available now. See the [curriculum](curriculum.md) for
possible future units; priorities will depend on lecturer and student feedback.

## Status

Units A1 and A2 are **pilot prereleases, version 0.1.0a1**. They have automated checks, but have
not yet been trialled externally with lecturers and students. We welcome small
course trials, corrections and feedback: see [About](about.md).

[Prepare a small trial: lecturer checklist](pilot-checklist.md)

```{toctree}
:hidden:

getting-started
curriculum
units/ode-ivp/index
units/linear-systems/index
verification-report
supervisors
pilot-checklist
departments
about
```
