# Judging Rubric

This document fixes, in advance, exactly how the Claude-powered container and the
OpenAI-powered container are compared. It is written and committed before the task
suite, the harness code, or any model API call exists, so the judging criteria
cannot be adjusted after seeing which side performs better.

## What is measured

Each container runs an iterative self-improvement loop (the "self-evolving
harness") against a fixed suite of six programming tasks (see `shared/tasks.py`).
Each iteration is called a generation. A generation's score is the fraction of
unit tests it passes across all six tasks (0.0-1.0), computed purely mechanically
by running the test suite - no human or model judgment is involved in scoring.

A generation whose code does not even parse or import successfully scores 0.0 for
that generation; it does not crash or stop the experiment.

## Winner determination

1. **Primary criterion - best score.** For each container, its final score is the
   *highest* score achieved by any generation during its run - not necessarily the
   last generation, since a later generation may regress. We credit the best code
   the container actually produced, not wherever it happened to land when the
   budget ran out. The container with the higher best score wins.
2. **Tiebreaker - tokens to reach that score.** If both containers reach the same
   best score, the winner is whichever container used fewer cumulative tokens
   (summed from generation 1) up to and including the generation that first
   reached that best score. This rewards reaching a good solution efficiently,
   not just eventually.
3. **Exact tie.** If both the best score and the tokens-to-reach-it are identical,
   the result is declared a tie. No further tiebreaker is introduced after the
   fact.

## Why best score, not an average across generations

The winner is decided by the single best generation, not the average or sum of
all generations' scores. This mirrors standard practice in evolutionary
algorithms, which report the best individual found, not the average fitness
across the whole run - early generations are expected to score low simply
because the loop has just started, and averaging them in would unfairly punish a
container that happens to improve quickly.

The known weakness of this choice: a container that improves steadily across
every generation and one that scores low for a while and then gets lucky once
late in the run can end up with the same "best score", even though they
demonstrate very different quality of self-improvement. We do not fix this by
folding a second number into the win condition - weighting multiple metrics
together quickly becomes arbitrary. Instead, `REPORT.md` shows the full,
generation-by-generation score curve for both containers, so this difference is
visible to any reader even though it does not change who technically wins.

## Out of scope for the ranking

- The closing self-defense statement (the final, separately-budgeted call where
  each model argues for its own result) is not part of the score. It is reported
  verbatim in `REPORT.md` but does not affect who wins.
- Code style, readability, or anything not covered by the automated tests is not
  scored.

## Why this is fixed in advance

The task author (Claude, via this assistant) is not a neutral party in a
Claude-vs-OpenAI comparison. Fixing the win condition before the task suite itself
exists is the main protection against picking a definition of "best" after the
fact that happens to favor one side, consciously or not. See `METHODOLOGY.md` for
the full discussion of this and other bias mitigations.
