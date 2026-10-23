#!/usr/bin/env python3
"""Publish a new seed set into ``seedset.yaml`` on the §4.6 rotation schedule.

§4.6 ties three separate things to the cohort calendar, and this script keeps all
three straight:

  * **Refresh cadence.** "MLCommons refreshes the seed set once every two cohorts."
    Cohorts are bi-weekly (§4.2), so a new set is due every two publication dates.
    The cadence is derived from the file — the newest set's publication cohort —
    rather than from a hard-coded parity, so a skipped or manually-forced round
    re-anchors the schedule instead of permanently halving it.

  * **Adoption window.** Each set is adoptable for "four consecutive cohorts — the
    cohort it is keyed to and the following three". Because refresh is every two
    and the window is four, two sets are normally adoptable at once.

  * **Binding lifetime.** A submission stays bound to its set "for the full
    applicable Pareto-update window, even after the set's adoption window has
    closed". The checker's ``seed-set-membership`` row fails a submission whose set
    id is absent from this registry, so **a retired set is never deleted** — it is
    only frozen out of the adoption windows. The file grows; that is correct.

The freezing is why every set gets an explicit ``cohorts:`` list. The registry
carries one file-level ``cohort-id`` that the checker otherwise applies to *every*
set in the file, so appending a newer set under a bumped ``cohort-id`` would
silently re-key the older sets and keep retired ones adoptable. Writing the window
per set pins each one to the cohort it was actually published for.

One caveat for the working group, since this script has to pick a reading. §4.6 on
``main`` keys a set "by the cohort ID in which it is **published**", while the
``feat/change-cohort-selection`` branch keys it to "the first cohort that may
**adopt** it". Publishing ahead of time is only coherent under the second reading —
under the first, a set published a week early would claim a cohort that has not
started. This script follows the second, which is also what the checker already
implements: ``submission_checker/seed_sets.py`` derives the window as that cohort
plus the next three. Only ``main``'s prose lags; no behaviour here depends on the
wording being fixed.
"""

from __future__ import annotations

import argparse
import re
import secrets
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import yaml

#: Marks the one audit finding this script fixes itself, by backfilling the window
#: from the file-level cohort-id. Everything else needs a human.
BACKFILLABLE = "no explicit 'cohorts' window"

#: Cohorts per calendar month — §4.2's 1st and 3rd Wednesday.
COHORTS_PER_MONTH = 2
#: §4.6: a set is adoptable for its publication cohort and the following three.
ADOPTION_WINDOW = 4
#: §4.6: "MLCommons refreshes the seed set once every two cohorts."
REFRESH_EVERY = 2
#: Publish this far ahead of the cohort the set becomes adoptable in, so the working
#: group has a review window instead of being asked to merge a rules artifact on the
#: morning it takes effect. The rules set no lead time — §4.6 is silent on it — so this
#: is an operational convention, not a rule. Seven days lands the run on the Wednesday
#: before each cohort date.
LEAD_DAYS = 7
#: The seed fields a set defines, in the spelling the registry uses.
SEED_FIELDS = ("scheduler_rng_seed", "sample_index_rng_seed", "model_seed")
#: Seeds are uint64, matching the reference client's RNG seeding and MLPerf
#: Inference's LoadGen seeds. Zero is excluded: a zero seed is a legitimate uint64
#: but reads as "unset" to a human and to several RNG wrappers.
SEED_MIN = 1
SEED_MAX = 2**64 - 1

COHORT_RE = re.compile(r"(?P<year>\d{4})-(?P<month>\d{2})-C(?P<index>[01])")


class RotationError(RuntimeError):
    """The registry cannot be read, or the requested rotation is not coherent."""


@dataclass(frozen=True, order=True)
class Cohort:
    """One publication cohort, ordered chronologically."""

    year: int
    month: int
    index: int

    def __str__(self) -> str:
        return f"{self.year:04d}-{self.month:02d}-C{self.index}"

    @classmethod
    def parse(cls, value: str) -> Cohort:
        match = COHORT_RE.fullmatch(value.strip()) if value else None
        if match is None:
            raise RotationError(f"{value!r} is not a cohort id of the form YYYY-MM-C0/C1")
        month = int(match["month"])
        if not 1 <= month <= 12:
            raise RotationError(f"{value!r} names a month that does not exist")
        return cls(int(match["year"]), month, int(match["index"]))

    def next(self) -> Cohort:
        if self.index + 1 < COHORTS_PER_MONTH:
            return Cohort(self.year, self.month, self.index + 1)
        if self.month == 12:
            return Cohort(self.year + 1, 1, 0)
        return Cohort(self.year, self.month + 1, 0)

    def ordinal(self) -> int:
        """Position on the cohort calendar, for counting distances."""
        return (self.year * 12 + self.month - 1) * COHORTS_PER_MONTH + self.index

    def window(self, length: int = ADOPTION_WINDOW) -> list[str]:
        """This cohort and the ``length - 1`` cohorts after it."""
        out = [self]
        while len(out) < length:
            out.append(out[-1].next())
        return [str(c) for c in out]


def nth_wednesday(year: int, month: int, n: int) -> date:
    """The ``n``-th (1-based) Wednesday of a month."""
    first = date(year, month, 1)
    offset = (2 - first.weekday()) % 7  # Monday=0 … Wednesday=2
    return first + timedelta(days=offset + 7 * (n - 1))


def cohort_for(day: date) -> Cohort:
    """The cohort whose submission window contains *day* (§4.2).

    A window opens on a publication date and runs until the next one, so the cohort
    is the most recent publication date at or before *day* — which, in the first
    days of a month, is the previous month's second cohort.
    """
    year, month = day.year, day.month
    for _ in range(2):
        c1 = nth_wednesday(year, month, 3)
        c0 = nth_wednesday(year, month, 1)
        if day >= c1:
            return Cohort(year, month, 1)
        if day >= c0:
            return Cohort(year, month, 0)
        year, month = (year - 1, 12) if month == 1 else (year, month - 1)
    raise RotationError(f"could not place {day} on the cohort calendar")


def next_set_id(existing: set[str]) -> str:
    """The next unused single-letter set id."""
    for code in range(ord("A"), ord("Z") + 1):
        if chr(code) not in existing:
            return chr(code)
    raise RotationError("all single-letter seed-set ids are taken; extend the scheme")


def new_seeds() -> dict[str, int]:
    """One fresh uint64 per seed field, from the OS CSPRNG."""
    seeds: dict[str, int] = {}
    for name in SEED_FIELDS:
        value = 0
        while not SEED_MIN <= value <= SEED_MAX:
            value = secrets.randbits(64)
        seeds[name] = value
    return seeds


def load(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], Cohort]:
    """Return ``(document, seed-set entries, file-level publication cohort)``."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise RotationError(f"cannot read {path}: {exc}") from exc
    except yaml.YAMLError as exc:
        raise RotationError(f"invalid YAML in {path}: {exc}") from exc
    if not isinstance(raw, dict) or not isinstance(raw.get("cohort"), dict):
        raise RotationError(f"{path}: expected a top-level 'cohort:' mapping")
    cohort = raw["cohort"]
    entries = cohort.get("seed_sets")
    if not isinstance(entries, list) or not entries:
        raise RotationError(f"{path}: cohort.seed_sets must be a non-empty list")
    if "cohort-id" not in cohort:
        raise RotationError(f"{path}: cohort.cohort-id is required to date the sets")
    return raw, entries, Cohort.parse(str(cohort["cohort-id"]))


def audit(entries: list[dict[str, Any]], file_cohort: Cohort) -> list[str]:
    """Problems with the registry as it stands, as human-readable lines.

    Returned rather than raised: the caller reports them all at once, and a
    ``--check`` run exits non-zero on any.
    """
    problems: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        where = f"seed_sets[{index}]"
        set_id = entry.get("id")
        if not isinstance(set_id, str) or not set_id:
            problems.append(f"{where}: missing a string 'id'")
            continue
        where = f"seed set {set_id}"
        if set_id in seen:
            problems.append(f"{where}: duplicate id")
        seen.add(set_id)
        for name in SEED_FIELDS:
            if name not in entry:
                problems.append(f"{where}: missing {name}")
                continue
            value = entry[name]
            if not isinstance(value, int) or isinstance(value, bool):
                problems.append(f"{where}: {name} is {value!r}, not an integer")
            elif not SEED_MIN <= value <= SEED_MAX:
                problems.append(
                    f"{where}: {name} = {value} is outside the uint64 range "
                    f"[{SEED_MIN}, {SEED_MAX}]"
                )
        window = entry.get("cohorts")
        if window is None:
            problems.append(
                f"{where}: no explicit 'cohorts' window — it would inherit the "
                f"file-level cohort-id ({file_cohort}), which re-keys older sets "
                f"every time a new one is published"
            )
        elif not isinstance(window, list) or not all(isinstance(c, str) for c in window):
            problems.append(f"{where}: 'cohorts' must be a list of cohort ids")
        elif len(window) != ADOPTION_WINDOW:
            problems.append(
                f"{where}: 'cohorts' lists {len(window)} cohort(s); §4.6 gives each "
                f"set a {ADOPTION_WINDOW}-cohort adoption window"
            )
        else:
            # The checker str()-casts these with no validation, so a typo like
            # 2026-13-C0 is accepted into the window and then silently never matches
            # any real target cohort. Catch it here instead.
            malformed = []
            for entry_cohort in window:
                try:
                    Cohort.parse(entry_cohort)
                except RotationError:
                    malformed.append(entry_cohort)
            if malformed:
                problems.append(
                    f"{where}: 'cohorts' contains {', '.join(repr(c) for c in malformed)}, "
                    f"which is not a cohort id of the form YYYY-MM-C0/C1"
                )
                continue
            expected = Cohort.parse(window[0]).window()
            if window != expected:
                problems.append(
                    f"{where}: 'cohorts' is {window}, which is not {window[0]} plus "
                    f"the {ADOPTION_WINDOW - 1} cohorts after it ({expected})"
                )
    return problems


def render(file_cohort: Cohort, entries: list[dict[str, Any]]) -> str:
    """Serialise the registry.

    Written out rather than round-tripped so the column alignment and the header
    survive; the schema is small and fixed, and a generated file that a reviewer
    cannot diff cleanly defeats the point of sending this through a PR.
    """
    width = max(len(name) for name in SEED_FIELDS) + 1
    lines = [
        "# MLPerf Endpoints published seed sets (Submission Rules §4.6 Seed Rotation).",
        "#",
        "# Maintained by .github/workflows/rotate-seed-sets.yml. A set is published every",
        f"# {REFRESH_EVERY} cohorts and is adoptable for {ADOPTION_WINDOW} "
        "(its own cohort and the three after).",
        "#",
        "# Sets are never removed: §4.6 keeps a submission bound to its set for the full",
        "# Pareto-update window, and the checker's seed-set-membership row fails any",
        "# submission whose set is absent here. A retired set simply stops appearing in",
        "# any current adoption window.",
        "#",
        "# Each set carries its own `cohorts:` window. Without it the checker applies the",
        "# file-level `cohort-id` to every set, which would re-date the older ones.",
        "cohort:",
        "  version: 1.0",
        f"  cohort-id: {file_cohort}        # the newest set's first adoptable cohort",
        "  seed_sets:                              # a submission selects exactly one, by id",
    ]
    for entry in entries:
        lines.append(f"    - id: {entry['id']}")
        for name in SEED_FIELDS:
            lines.append(f"      {(name + ':').ljust(width)} {entry[name]}")
        lines.append("      cohorts: [" + ", ".join(entry["cohorts"]) + "]")
    return "\n".join(lines) + "\n"


def rotate(
    path: Path,
    today: date,
    *,
    cohort_override: str | None,
    force: bool,
    write: bool,
    lead_days: int = LEAD_DAYS,
) -> int:
    doc, entries, file_cohort = load(path)

    problems = audit(entries, file_cohort)
    # Backfilling a missing window is this script's job, not a reason to refuse:
    # the first run converts a hand-written registry to the explicit form.
    blocking = [p for p in problems if BACKFILLABLE not in p]
    for line in problems:
        print(f"  audit: {line}", file=sys.stderr)
    if blocking:
        raise RotationError(f"{path}: {len(blocking)} problem(s) above must be fixed by hand")

    for entry in entries:
        entry.setdefault("cohorts", file_cohort.window())

    newest = max(Cohort.parse(e["cohorts"][0]) for e in entries)
    # Look `lead_days` ahead so a run lands on the Wednesday *before* the cohort it
    # publishes for. cohort_for() already answers "which cohort is open on this day",
    # so asking it about next week needs no second calendar.
    #
    # An explicit --cohort names the target outright and ignores the lead time: it is
    # how a specific cycle is published by hand.
    target = (
        Cohort.parse(cohort_override)
        if cohort_override
        else cohort_for(today + timedelta(days=lead_days))
    )
    elapsed = target.ordinal() - newest.ordinal()

    print(f"  today          {today}")
    if not cohort_override:
        print(f"  lead time      {lead_days} day(s)")
    print(f"  target cohort  {target}")
    print(f"  newest set     {entries[-1]['id']} published for {newest}")
    print(f"  elapsed        {elapsed} cohort(s) since the last publication")

    if elapsed < 0:
        raise RotationError(
            f"target cohort {target} precedes the newest published set's cohort {newest}"
        )
    if elapsed < REFRESH_EVERY and not force:
        print(f"  -> not due: a new set is published every {REFRESH_EVERY} cohorts.")
        return 0
    if elapsed < REFRESH_EVERY:
        print(f"  -> forced: publishing early, {elapsed} cohort(s) after the last set.")

    set_id = next_set_id({e["id"] for e in entries})
    entry = {"id": set_id, **new_seeds(), "cohorts": target.window()}
    entries.append(entry)

    # `cohorts` holds strings, so compare as one: `target in e["cohorts"]` with a
    # Cohort object silently matches nothing.
    adoptable = [e["id"] for e in entries if str(target) in e["cohorts"]]
    print(f"  -> publishing set {set_id} for {target}")
    print(f"     adoption window {entry['cohorts'][0]} … {entry['cohorts'][-1]}")
    print(f"     adoptable in {target}: {', '.join(adoptable)}")

    rendered = render(target, entries)
    if write:
        path.write_text(rendered, encoding="utf-8")
        print(f"  wrote {path}")
    else:
        print("  --dry-run: not writing. Rendered file follows.\n")
        print(rendered)
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument(
        "--path", type=Path, default=Path("seedset.yaml"), help="the registry to rotate"
    )
    parser.add_argument(
        "--today", type=date.fromisoformat, default=date.today(), help="override today's date"
    )
    parser.add_argument(
        "--cohort",
        help="publish for this cohort instead of the one today falls in (YYYY-MM-C0/C1)",
    )
    parser.add_argument(
        "--lead-days",
        type=int,
        default=LEAD_DAYS,
        help=f"publish this many days before the target cohort opens (default {LEAD_DAYS}); "
        "ignored when --cohort names the target outright",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="publish even when fewer than two cohorts have passed",
    )
    parser.add_argument("--dry-run", action="store_true", help="render to stdout, write nothing")
    parser.add_argument(
        "--check",
        action="store_true",
        help="audit the registry and exit non-zero on a problem; rotate nothing",
    )
    args = parser.parse_args()

    try:
        if args.check:
            _, entries, file_cohort = load(args.path)
            problems = audit(entries, file_cohort)
            # The missing-window finding is what the next rotation backfills, so it
            # is reported but not failed: failing it would block the very first run
            # against a hand-written registry.
            blocking = [p for p in problems if BACKFILLABLE not in p]
            for line in problems:
                marker = "error" if line in blocking else "note "
                print(f"  {marker}: {line}", file=sys.stderr)
            print(f"{args.path}: {len(blocking)} blocking, "
                  f"{len(problems) - len(blocking)} to be backfilled")
            return 1 if blocking else 0
        changed = rotate(
            args.path,
            args.today,
            cohort_override=args.cohort,
            force=args.force,
            write=not args.dry_run,
            lead_days=args.lead_days,
        )
    except RotationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    # 0 = nothing to do, 1 = a new set was published. The workflow opens a PR on 1.
    return 0 if not changed else 1


if __name__ == "__main__":
    sys.exit(main())
