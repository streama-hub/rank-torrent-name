import argparse
import json
import sys
from pathlib import Path


def canonical(data):
    result = dict(data)
    if "languages" in result:
        result["audio_languages"] = result.pop("languages")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ptt", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    sys.path.insert(0, str(args.ptt.resolve()))
    from PTT import parse_title

    from benchmarks.audit_joint_metadata import cases
    from benchmarks.release_fixture_audit import upstream_fixtures
    from RTN import RTN, SettingsModel
    from RTN.fetch import check_fetch

    if args.record:
        _, fixtures = upstream_fixtures(args.ptt)
        titles = list(fixtures) + [row["title"] for row in cases()]
        previous = None
    else:
        previous = json.loads(args.snapshot.read_text(encoding="utf-8"))
        titles = list(previous)
    ranker = RTN(SettingsModel(languages={"preferred": ["fr", "ja"], "exclude": ["en"]}))
    results = {}
    for title in titles:
        torrent = ranker.rank(title, "a" * 40)
        if not args.record:
            assert "languages" not in parse_title(title)
            assert "languages" not in torrent.data.model_dump()
        results[title] = {
            "ptt": canonical(parse_title(title)),
            "translated": canonical(parse_title(title, True)),
            "rtn": canonical(torrent.data.model_dump()),
            "rank": torrent.rank,
            "fetch": torrent.fetch,
            "full_fetch": check_fetch(torrent.data, ranker.settings, False)[0],
        }
    if args.record:
        args.snapshot.write_text(json.dumps(results, ensure_ascii=True), encoding="utf-8")
        print(json.dumps({"recorded": len(results)}))
        return 0
    differences = [title for title in titles if previous[title] != results[title]]
    print(json.dumps({"compared": len(results), "differences": differences}, indent=2))
    return bool(differences)


if __name__ == "__main__":
    raise SystemExit(main())
