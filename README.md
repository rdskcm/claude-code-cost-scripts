# claude-code-cost-scripts

Scripts behind the "what would this project cost via the API" analysis in the
Habr article (https://habr.com/ru/articles/1063412/). They compute per-API-call
cost from Claude Code `.jsonl` transcripts instead of trusting the built-in
`/usage` summary, which sums the duplicated per-content-block `usage` objects
line by line (measured overcount on this project: 2.11×).

Core rule: group transcript records by `requestId` and keep the record with the
maximum `output_tokens` — one `requestId` = one billable API call. Streaming
writes several lines per call (one per content block, ~2.03 on average here),
each carrying the same `usage` object, and early lines hold partial output
counts.

| Script | Purpose |
|---|---|
| `FINAL.py` | Final per-call cost totals by model and by day |
| `sessions.py` | Per-session breakdown |
| `gapfill.py` | Extrapolation for days with an incomplete archive |
| `dupes.py` | Proof of per-block line duplication (lines per requestId) |
| `reconcile.py` | Day-by-day comparison against `~/.claude/stats-cache.json` |
| `validate.py`, `validate2.py` | Calibration of the price formula against official `/usage` → Session figures (0.1% error) |
| `agg.py`, `exact.py`, `tail.py` | Earlier/auxiliary aggregation passes |

## Status (re-checked October 2026, Claude Code 2.1.312)

- The per-day statistics in `~/.claude/stats-cache.json` (the Overview tab of
  `/usage`) still sum `usage` line by line: 1.7–2.8× the per-call totals on
  every day checked between 2026-10-12 and 2026-10-20.
- The per-session summary printed at the end of a session counts each call once.
  On two sessions it matched the per-call totals for the main model and was
  higher for the others, because it also includes calls that never reach the
  transcripts (for example web searches). For the cost of one session, trust
  that summary over these scripts: the scripts see only transcribed calls and
  undercount slightly.
- These scripts remain useful for totals across many sessions and as the
  reproducible proof of the per-day overcount.

## Usage

    python3 FINAL.py [DIR ...]

The same form works for `sessions.py`, `exact.py`, `dupes.py`, `reconcile.py`,
`agg.py` and `tail.py`. Each DIR is one project transcript directory under
`~/.claude/projects/`, or an archive copy of one. Several DIRs are read in the
given order: put an archive of older transcripts first, then the live
directory. Instead of arguments, set `CLAUDE_TRANSCRIPTS_DIR=dir1:dir2`. With
neither, every project under `~/.claude/projects/` is read. `-h` prints the
usage.

Run the scripts as `python3 path/to/SCRIPT.py`, not with `python3 -I`: they
import `transcripts.py` from their own folder. Python 3 standard library only.

`reconcile.py` also reads `~/.claude/stats-cache.json`.

Prices in the `PR` table are USD per 1M tokens (input, output); cache write is
1.25× input for 5-minute TTL, 2× for 1-hour, cache read 0.1× — taken from each
record's `cache_creation` field, not assumed.

The figures in the output are the article author's data: the $25.62 and $34.02
official `/usage` screens (`sessions.py`, `validate*.py`), the stats-cache totals
line in `dupes.py`, and the constants in `gapfill.py`. They are printed for
comparison; on other data they are only reference points. Output text is in
Russian, as in the article.

## License

MIT, see [LICENSE](LICENSE).
