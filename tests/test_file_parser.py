import json
from pathlib import Path

import pytest

from RTN.file_parser import parse_media_file

TEST_VIDEO_PATH = Path(__file__).parent / "video" / "[Yameii] Mushoku Tensei - Jobless Reincarnation - S02E15 [English Dub] [CR WEB-DL 1080p] [6CD6B5CA].mkv"


@pytest.mark.skipif(not TEST_VIDEO_PATH.exists(), reason="The optional video fixture is not included in the repository")
def test_media_file_parser():
    """Test the MediaFileParser class"""
    metadata = parse_media_file(TEST_VIDEO_PATH)
    assert metadata is not None
    assert metadata.bitrate is not None
    assert metadata.audio is not None
    assert metadata.video is not None
    assert metadata.subtitles is not None
    assert metadata.filename is not None
    assert metadata.file_size is not None
    assert metadata.duration is not None


@pytest.mark.parametrize("codec_type", ["audio", "subtitle"])
@pytest.mark.parametrize("tags,expected", [(None, ""), ({}, ""), ({"language": None}, ""), ({"language": ""}, ""), ({"language": "jpn"}, "jpn")])
def test_missing_track_language(codec_type, tags, expected, tmp_path, monkeypatch):
    path = tmp_path / "example.mkv"
    path.touch()
    stream = {"codec_type": codec_type, "codec_name": "aac" if codec_type == "audio" else "subrip"}
    if tags is not None:
        stream["tags"] = tags
    monkeypatch.setattr("RTN.file_parser.subprocess.check_output", lambda *_args, **_kwargs: json.dumps({"streams": [stream]}))
    metadata = parse_media_file(path)
    tracks = metadata.audio if codec_type == "audio" else metadata.subtitles
    assert len(tracks) == 1
    assert tracks[0].language == expected
