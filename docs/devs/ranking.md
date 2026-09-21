# Ranking

## RTN
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/parser.py)
```python 
from RTN import RTN, SettingsModel
rtn = RTN(SettingsModel())
```


---
RTN (Rank Torrent Name) class for parsing and ranking torrent titles based on user preferences.


**Args**

* The settings model with user preferences for parsing and ranking torrents.
* The model defining the ranking logic and score computation.

**Notes**

* `settings` must be a `SettingsModel`. If `ranking_model` is omitted, `DefaultRanking` is used.
* The `lev_threshold` is derived from `settings.options["title_similarity"]` and is used to determine if a torrent title matches the correct title.

---

**Methods:**

### .rank
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/parser.py)
```python
.rank(
   raw_title: str, infohash: str, correct_title: str = '', remove_trash: bool = False
)
```

Parses a torrent title, computes its rank, and returns a Torrent object with metadata and ranking.

**Args**

* The original title of the torrent to parse.
* The SHA-1 hash identifier of the torrent.
* The correct title to compare against for similarity. Defaults to an empty string.
* Whether to raise an error for rejected torrents, low ranks or title mismatches. Defaults to False.

**Returns**

* **Torrent**  : A Torrent object with metadata and ranking information.

**Raises**

* **ValueError**  : If the title or infohash is not provided for any torrent.
* **TypeError**  : If the title or infohash is not a string.
* **GarbageTorrent**  : If the infohash length is not 40, or `remove_trash` is True and the torrent fails filtering, rank or title checks.
* **SettingsDisabled**  : If the settings are disabled.

Notes:
    - If `correct_title` is provided, the Levenshtein ratio will be calculated between the parsed title and the correct title.
    - If the ratio is below the threshold and `remove_trash` is True, a `GarbageTorrent` error will be raised.
    - If no correct title is provided, the Levenshtein ratio will be set to 0.0.


**Example**

```python
from RTN import RTN
from RTN.models import SettingsModel, DefaultRanking, Torrent, ParsedData

settings_model = SettingsModel()
ranking_model = DefaultRanking()
rtn = RTN(settings_model, ranking_model)
torrent = rtn.rank("The Walking Dead S05E03 720p HDTV x264-ASAP[ettv]", "c08a9ee8ce3a5c2c08865e2b05406273cabc97e7", correct_title="The Walking Dead")
assert isinstance(torrent, Torrent)
assert isinstance(torrent.data, ParsedData)
assert torrent.fetch
assert torrent.rank == -4500
assert torrent.lev_ratio > 0.0
```

---

## get_rank
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/ranker.py)
```python
.get_rank(
   data: ParsedData, settings: SettingsModel, rank_model: BaseRankingModel
)
```

Calculate the ranking of the given parsed data.

Parameters:
`data` (ParsedData): The parsed data object containing information about the torrent title.
`settings` (SettingsModel): The user settings object containing custom ranking models.
`rank_model` (BaseRankingModel): The base ranking model used for calculating the ranking.


**Returns**

* **int**  : The calculated ranking value for the parsed data.


**Raises**

* **ValueError**  : If the parsed data is empty.
* **TypeError**  : If the parsed data is not a ParsedData object.

---

## calculate_preferred
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/ranker.py)
```python
.calculate_preferred(
   data: ParsedData, settings: SettingsModel
)
```

Calculate the preferred ranking of a given parsed data.

---

## calculate_quality_rank
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/ranker.py)
```python
.calculate_quality_rank(
   data: ParsedData, settings: SettingsModel, rank_model: BaseRankingModel
)
```

Calculate the quality ranking of the given parsed data.

---

## calculate_codec_rank
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/ranker.py)
```python
.calculate_codec_rank(
   data: ParsedData, settings: SettingsModel, rank_model: BaseRankingModel
)
```

Calculate the codec ranking of the given parsed data.

---

## calculate_audio_rank
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/ranker.py)
```python
.calculate_audio_rank(
   data: ParsedData, settings: SettingsModel, rank_model: BaseRankingModel
)
```

Calculate the audio ranking of the given parsed data.

---

## calculate_extra_ranks
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/ranker.py)
```python
.calculate_extra_ranks(
   data: ParsedData, settings: SettingsModel, rank_model: BaseRankingModel
)
```

Calculate all the other rankings of the given parsed data.
