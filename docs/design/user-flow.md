## What it does

Specify what a person does, what the product responds with and where the task goes next. The transition table keeps initiating a request separate from confirming its result.

## When to reach for it

Type `/user-flow`, or the agent reaches for it automatically when a task fits.

Use it before implementation when success, interruption, recovery, exit or return still needs a concrete contract. Component state previews are a separate, explicitly requested state-machine workbench.

## Common questions

**Does closing a panel cancel its operation?**

Only if the agreed product behavior says so. When an operation survives closing, the flow tracks visibility separately and covers return before starting, during work and after completion. A task that has not started has no request key to restore.

## It's working if

- Every offered action maps to a transition with feedback, a destination and retained data.
- Unanswered requests remain distinct from confirmed failure, and retries follow the agreed policy.
- Exit and return paths preserve the right data before starting and after completion.

## Where it fits

It is the task contract between [information-architecture](https://github.com/reach0908/paul-skills/blob/main/docs/design/information-architecture.md) and [wireframe](https://github.com/reach0908/paul-skills/blob/main/docs/design/wireframe.md). Use [state-machine](https://github.com/reach0908/paul-skills/blob/main/docs/design/state-machine.md) explicitly only to work with states of an existing component. See [ask-matt](https://github.com/reach0908/paul-skills/blob/main/docs/engineering/ask-matt.md) for the full routing map.
