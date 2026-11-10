# For lecturers and supervisors

verifiedmethods provides free, adaptable practical work for students who have
met the relevant mathematics and basic Python. The recommended first use is
alongside or shortly after the corresponding topic is taught.

As a course practical
: Teach the method, then assign the relevant tutorial sections. Students
  implement it, check its numerical behaviour and explain the results. You
  can use a full unit over several sessions or select a smaller exercise.

As a starting point for a project
: The student works through the unit, then develops one of its project briefs
  or a question of your own. Agree the level and required contribution: the
  standard methods and supplied checks alone are not a novel research result.

As a check on a project you have already set
: Where the method and assumptions fit, use the supplied checks as a starting
  point. A project's new model, data or algorithm needs additional validation;
  the unit report covers only the stated unit checks.

## Try one unit first

Use the [pilot checklist](pilot-checklist.md) to prepare, run and review a
small trial. A printable PDF is available on that page; feedback can be sent
by email without creating an account.

1. Choose [A1](units/ode-ivp/index.md) or [A2](units/linear-systems/index.md)
   to match a topic you teach. Check the prerequisites on the unit page.
2. Inspect an [example report](verification-report.md) and the unit's rubric
   before asking students to install anything.
3. Download and extract the unit; follow tutorial section 0 on a machine
   similar to the students' computers. Run `python verify.py`. The starter
   functions are deliberately unfinished, so the first report is incomplete.
4. Start with a small group, for example three to five students. Agree which
   sections, experiments and written explanation they should complete, the
   deadline and how help or AI use must be disclosed.
5. For a full submission, ask students to run `python verify.py --strict`,
   then [confirm their report](verification-report.md) and ask viva questions.
   For an exercise on just one method, assess its individual gate results;
   whole-unit strict mode will still reject the unfinished methods.

Students can work locally without a GitHub account. See
[getting started](getting-started.md) for setup, submission and offline reading,
and [departments](departments.md) for an adaptable six-week outline.

## What you get

| | |
|---|---|
| How to confirm a report | Rerun the student's code in a fresh copy and compare the results and fingerprints |
| Viva questions | Twelve for unit A1, on the code, the results and the project |
| Marking rubric | For a computational chapter; adapt the criteria and weights for coursework |
| AI-use statement | A short statement you can adopt or adapt |
| Marking guides for the briefs | On request: email from your institutional address (see [About](about.md)) |

They are in each unit's supervisor material: [A1](units/ode-ivp/supervisors/index.md), [A2](units/linear-systems/supervisors/index.md).

## What we ask in return

The units have not yet been trialled externally. We would especially value
feedback on setup time and difficulties, mathematical and Python prerequisites,
students' explanations, your assessment workload and whether you would assign
the unit again. Use your usual course assessment and AI rules when adapting
the material. See [About](about.md) to discuss a trial or report a problem.
