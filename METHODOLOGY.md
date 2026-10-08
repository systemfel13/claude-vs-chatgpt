# Methodology

This document explains how the Claude-vs-OpenAI comparison is set up and why,
including the fairness considerations behind each choice. It is written and
committed before the task suite or any harness code exists, for the same reason
as `RUBRIC.md`: so the design can't be adjusted after seeing which side performs
better.

## The task suite

Both containers are given the identical suite of six small, well-known
programming exercises (run-length encoding, balanced brackets, interval
merging, an LRU cache, topological sort, and a stack-based expression
evaluator - see `shared/tasks.py`). These are standard exercises commonly seen
in technical interviews, not problems invented for this comparison, to avoid
picking a benchmark that happens to suit one model's training.

## Equal, hard-enforced token budgets

Each container gets `TASK_TOKEN_BUDGET` (50,000) tokens for the self-improvement
loop and a separate `DEFENSE_TOKEN_BUDGET` (3,000) tokens for a closing
statement (see `shared/config.py`). The cap is enforced by our own code, which
sums `input + output` tokens after every API call and stops the loop before the
next call would risk exceeding the budget - not by a provider-specific
"advisory" budget feature, since those differ between Anthropic and OpenAI and
would not guarantee the two sides actually get the same allowance.

## The model-harness protocol

The model is asked, in plain text, to reply with a single fenced code block
containing the full contents of `solution.py`. We deliberately did not use
either provider's structured tool-calling feature for this, even though both
support one: that would mean the comparison partly measures which provider's
tool-calling API is more convenient, rather than which model solves the task
better. A plain-text contract is identical overhead for both sides.

## Sandboxed execution and context management

Every candidate `solution.py` runs in a subprocess with a hard timeout of 5
seconds, so a buggy infinite loop in generated code cannot hang the experiment
indefinitely. The six tasks run on small inputs, so correct code - even an
inefficient implementation - is expected to finish in milliseconds; 5 seconds
gives a large safety margin against killing legitimate but slow code, while
still being short enough that a genuine hang does not cost much total time
across up to 40 generations per container.

Only the last two generations' code and test feedback are kept in the prompt,
rather than the full history. Sending everything every turn would consume the
budget fast and limit how many generations fit within it; keeping only the
single most recent generation would be cheaper still but risks the model
repeating an approach it already tried a couple of steps back. Two generations
is a middle ground between budget efficiency (fewer tokens spent per turn means
more generations fit within the budget) and giving the model enough memory to
avoid looping on the same failed idea.

## Stopping conditions

A container's loop stops when one of three things happens:

1. **The token budget is exhausted.** This is the intended, primary stopping
   mechanism.
2. **A perfect score (1.0) is reached and holds for two consecutive generations.**
   The test suite itself is deterministic - the same code always gives the
   same test result - but the model's code generation is not: the same
   prompt can produce different code each time. A single generation reaching
   1.0 could therefore be an unrepresentative sample from the model's own
   variance, not evidence that it reliably solves the task. Requiring the
   score to hold for a second generation gives some confidence it wasn't a
   fluke, at the cost of one extra call once the problem is already solved.
3. **A 40-generation safety cap is hit.** This is only a backup limit, not the
   normal way the loop is meant to stop - that should be the token budget.
   It exists in case a container's responses happen to be unusually short
   and cheap, letting it run through far more generations than expected
   before the budget runs out. The cap is set higher than a normal run is
   expected to need, so in practice the budget - not this cap - is almost
   always what actually stops the loop. A lower cap (e.g. 30) could have
   stopped a container early, even while it still had budget left and was
   still improving, just because its generations happened to be cheap.

## Possible bias and how it is mitigated

The task author, Claude, is not a neutral party in this comparison - that risk
cannot be fully removed by disclosure alone, but it can be reduced:

- **Task selection**: the six tasks are standard, widely known exercises, not
  invented for this comparison.
- **No hidden conventions**: both models receive the exact same, complete task
  specification up front, so neither has to guess undocumented edge-case
  behavior (e.g. how `calc_eval` handles division by zero).
- **Independent review**: the developer reviews and approves both `RUBRIC.md`
  and `shared/tasks.py` before either is committed, since the developer has no
  stake in which provider wins.
- **Judging criteria fixed in advance**: `RUBRIC.md` is committed before the
  task suite, the harness code, or any model API call exists.
- **Mechanical scoring**: a generation's score is the fraction of automated
  tests it passes - no human or model judgment is involved.
- **Best score vs. average, kept separate**: the formal winner is decided by the
  best score any generation reached (reflects whether the code actually works,
  appropriate for pass/fail tests), while the full generation-by-generation
  curve is reported separately in `REPORT.md` as a view of how consistent each
  container's improvement process was - without letting that affect who wins.
  See `RUBRIC.md` for the full reasoning.

## Secrets

API keys are read from a local `.env` file (gitignored) and passed to each
container as environment variables at run time - never baked into the image,
logged, or written to a results file.
