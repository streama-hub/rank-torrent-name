import argparse
import json
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from time import perf_counter

from PTT import parse_title

from RTN import RTN, ParsedData, SettingsModel, parse
from RTN.fetch import check_fetch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ptt", type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.ptt.resolve()))
    from benchmarks.audit_joint_metadata import cases
    from benchmarks.release_fixture_audit import upstream_fixtures

    _, fixtures = upstream_fixtures(args.ptt)
    combinations = list(cases())
    expected = {row["title"]: row["expected"] for row in combinations}
    titles = list(fixtures) + [row["title"] for row in combinations]
    fields = Counter()
    differences = []
    exceptions = []
    start = perf_counter()
    ranker = RTN(SettingsModel())
    for title in titles:
        try:
            raw = parse_title(title)
            result = parse(title)
            for field, value in raw.items():
                target = {"title": "parsed_title", "3d": "three_d", "convert": "converted"}.get(field, field)
                fields[field] += 1
                if getattr(result, target, None) != value:
                    differences.append((title, field, value, getattr(result, target, None)))
            for field, value in expected.get(title, {}).items():
                target = {"title": "parsed_title", "3d": "three_d"}.get(field, field)
                if getattr(result, target, None) != value:
                    differences.append((title, field, value, getattr(result, target, None)))
            assert ParsedData.model_validate_json(result.model_dump_json()) == result
            assert ranker.rank(title, "a" * 40).data == result
            fast, _ = check_fetch(result, ranker.settings, True)
            full, _ = check_fetch(result, ranker.settings, False)
            assert fast == full
        except Exception as error:
            exceptions.append((title, type(error).__name__, str(error)))
    elapsed = perf_counter() - start
    sample = titles[:100]
    sequential = [parse(title).model_dump() for title in sample]
    with ThreadPoolExecutor(max_workers=8) as executor:
        concurrent = [result.model_dump() for result in executor.map(parse, sample)]
    assert concurrent == sequential
    print(json.dumps({
        "upstream_titles": len(fixtures),
        "combinations": len(combinations),
        "cases": len(titles),
        "field_checks": sum(fields.values()),
        "fields": dict(fields),
        "differences": differences,
        "exceptions": exceptions,
        "threaded_cases": len(sample),
        "elapsed_seconds": round(elapsed, 2),
    }, indent=2))
    return bool(differences or exceptions)


if __name__ == "__main__":
    raise SystemExit(main())
