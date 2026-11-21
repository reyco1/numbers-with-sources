# numbers-with-sources

Every number an AI agent reports should show where it came from.
If it can't prove it, it should say "Not verified."

That's the whole idea. This repo is a tiny demo of it.

## What it does

You give it two things:

1. An agent's answer as JSON. A list of claims. Each has the text, a number, and a source (file name plus row key), or null.
2. A folder of CSV files holding the tool results.

For each claim it looks up the cited row and compares the number.

- **Verified**: the source row exists and the number matches.
- **Mismatch**: the source row exists but the number is different. It shows both.
- **Not verified**: no source, or the file or row is missing.

If anything isn't Verified, the command exits with a non-zero code. Easy to drop into a script or a check step.

## 30-second quickstart

Python 3 only. Nothing to install.

```
python -m numbers_with_sources examples/answer.json examples/data/
```

Output:

```
STATUS        CLAIM                                                        SOURCE                      NOTE
Verified      Example Clinic had 1240 visits in January 2026               monthly_visits.csv:2026-01  -
Mismatch      Example Clinic no-show rate in January 2026 was 8.5 percent  no_show_rates.csv:2026-01   agent said 8.5, source says 11.2
Not verified  Example Clinic visits grew 20 percent over last year         -                           no source given

1 of 3 verified.
```

Exit code is 1, because two claims failed.

A source looks like `monthly_visits.csv:2026-01`. The file name, a colon, then the row key. Each CSV has a `key` column and a `value` column.

Need some wiggle room on rounding? Use `--tolerance 0.5`.

Run the tests:

```
python -m unittest
```

## Why it matters

An agent that sounds sure is not the same as an agent that is right.
If it can't show a source, the honest answer is "I can't show that."
This makes that the default, and makes the gap easy to see.

## What it is NOT

- A demo. Small on purpose.
- Not a clinical tool. Don't use it for care decisions.
- Not a fact checker. It only checks that a number matches the row the agent cited. It can't tell if the row was the right one to cite.
- The example data is invented. "Example Clinic" is not a real place.

Written by Rey Columna. More at [reyco.me](https://reyco.me).
