<div align="center">

<h1>Rank Torrent Name (RTN)</h1>

<img src="https://img.shields.io/github/actions/workflow/status/streama-hub/rank-torrent-name/battery.yml?branch=main" alt="GitHub Actions Workflow Status" />

<img src="https://img.shields.io/github/license/streama-hub/rank-torrent-name" alt="GitHub License" />

</div>
<br>

**Rank Torrent Name (RTN)** is a Python library designed to parse and rank torrent names based on customizable criteria. It allows users to define their preferences for filtering and ranking torrents, providing a detailed analysis of each torrent's metadata. RTN is perfect for automating the selection of torrents based on quality, resolution, audio, and more.

Parsed audio and subtitle languages are exposed as `audio_languages` and
`subtitle_languages` in parsed models and JSON. Use these names when constructing
or reading parsed data. Filtering preferences use
`settings.languages`.

> **RTN** is mean't to be used as a Version and Ranking System for parsing and scoring scraped torrent results.

## Features

- **Advanced Torrent Parsing:** Utilizes PTT for parsing and preserves its detailed metadata.
- **Customizable Ranking:** Define detailed preferences for ranking torrents based on attributes like resolution, audio quality, and others.
- **Flexible Filtering:** Easily specify requirements, exclusions, and preferences for torrent selection.
- **Comprehensive Ranking Model:** Includes a default ranking model that can be customized or extended according to your needs.
- **Levenshtein Ratio Comparison:** Compares parsed titles with original titles to ensure accuracy.

## Installation

Install RTN and its dependencies:

```bash
pip install git+https://github.com/streama-hub/rank-torrent-name.git
```

For development, clone the repository and install the dependencies with Poetry:

```bash
git clone https://github.com/streama-hub/rank-torrent-name.git
cd rank-torrent-name
poetry install --with dev
```

PTT is installed automatically from the revision pinned in the project dependencies.

## Quick Start

### Setting Up Your Preferences

1. **Create a Settings Model:** Begin by defining your preferences in a `SettingsModel`. This includes specifying the required patterns, exclusions, preferences, and custom ranks for various torrent attributes.

```python
from RTN.models import SettingsModel, CustomRank

settings = SettingsModel(
    require=["4K", "1080p"],
    exclude=["/CAM/i", "TS"],
    preferred=["HDR", "/BluRay/"],
    custom_ranks={
        "uhd": CustomRank(enable=False, fetch=True, rank=120),
        "fhd": CustomRank(enable=False, fetch=True, rank=90),
        "hd": CustomRank(enable=False, fetch=True, rank=80),
        "sd": CustomRank(enable=False, fetch=True, rank=-120),
        "bluray": CustomRank(enable=False, fetch=True, rank=80),
        "hdr": CustomRank(enable=False, fetch=True, rank=40),
        "hdr10": CustomRank(enable=False, fetch=True, rank=50),
        "dolby_video": CustomRank(enable=False, fetch=True, rank=-100),
        "dts_x": CustomRank(enable=False, fetch=True, rank=0),
        "dts_hd": CustomRank(enable=False, fetch=True, rank=0),
        "dts_hd_ma": CustomRank(enable=False, fetch=True, rank=0),
        "atmos": CustomRank(enable=False, fetch=True, rank=0),
        "truehd": CustomRank(enable=False, fetch=True, rank=0),
        "ddplus": CustomRank(enable=False, fetch=True, rank=0),
        "aac": CustomRank(enable=False, fetch=True, rank=70),
        "remux": CustomRank(enable=False, fetch=True, rank=-1000),
        "webdl": CustomRank(enable=False, fetch=True, rank=90),
        "repack": CustomRank(enable=False, fetch=True, rank=5),
        "proper": CustomRank(enable=False, fetch=True, rank=4),
        "dubbed": CustomRank(enable=False, fetch=True, rank=4),
        "subbed": CustomRank(enable=False, fetch=True, rank=2),
        "av1": CustomRank(enable=False, fetch=True, rank=0),
    }
)
```

> :warning: You don't need to set **CAM** and **TS** as these are already disregarded by default. This is just an example.

We cover a lot already, so users are able to add their own custom regex patterns without worrying about the basic patterns.

#### Understanding Fetch and Enable:

- `fetch`: Determines if RTN should consider a torrent for downloading based on the attribute. True means RTN will fetch torrents matching this criterion.
- `enable`: Controls whether the custom rank value is used in the overall ranking calculation. Disabling it reverts to using the ranking model you set instead. This is useful for toggling custom ranks on and off from a users perspective.
- `rank`: Sets the rank at which that item is graded with.

For example, if we detect a title is **4K** or **2160p** then we use the `uhd` ranking, and add **+120** points. The same goes for the rest of the strings in `custom_ranks`.

Settings can be easily adjusted at runtime if needed. To enable or disable a specific rank dynamically:

```python
settings.custom_ranks["hdr"].enable = False  # To disable HDR ranking
```

### Ranking Torrents

2. **Rank a Torrent:** Feed a torrent title to RTN to parse it and calculate its rank based on your settings.

```python
from RTN import RTN
from RTN.models import DefaultRanking

rtn = RTN(settings=settings, ranking_model=DefaultRanking())
torrent = rtn.rank("Example.Movie.2020.1080p.BluRay.x264-Example", "infohash123456")
```

3. **Inspecting the Torrent Object:** The returned `Torrent` object includes parsed data and a rank. Access its properties to understand its quality:

```python
print(f"Title: {torrent.data.parsed_title}, Rank: {torrent.rank}")
```

### Sorting Torrents

4. **Sort Multiple Torrents:** If you have multiple torrents, RTN can sort them based on rank, helping you select the best one.

```python
torrents = [rtn.rank(title, "infohash") for title in torrent_titles]
sorted_torrents = RTN.sort(torrents)
```

## Torrent Object

A `Torrent` object encapsulates metadata about a torrent, such as its title, parsed information, and rank. Here's an example structure:

```python
Torrent(
    raw_title="Example.Movie.2020.1080p.BluRay.x264-Example",
    infohash="infohash123456",
    data=ParsedData(parsed_title='Example Movie', ...),
    fetch=True,
    rank=150,
    lev_ratio=0.95
)
```

## Understanding SettingsModel and RankingModel

**SettingsModel** and **RankingModel** play crucial roles in RTN, offering users flexibility in filtering and ranking torrents according to specific needs. Here's what each model offers and why they are important:

### SettingsModel

`SettingsModel` is where you define your filtering criteria, including patterns to require, exclude, and prefer in torrent names. This model allows for dynamic configuration of torrent selection based on user-defined patterns and preferences. 

Key functionalities:
- **Filtering Torrents:** Determine which torrents to consider or ignore based on matching patterns.
- **Prioritizing Torrents:** Indicate preferred attributes that give certain torrents higher precedence.
- **Custom Ranks Usage:** Decide how specific attributes influence the overall ranking, enabling or disabling custom ranks.

Example usage:
```python
from RTN.models import SettingsModel, CustomRank

settings = SettingsModel(
    require=["1080p", "4K"],
    exclude=["CAM"],
    preferred=["HDR", "/SenSiTivE/"],
    custom_ranks={
        "uhd": CustomRank(enable=True, fetch=True, rank=200),
        "hdr": CustomRank(enable=True, fetch=True, rank=100),
    }
)
```

As shown above with **"/SenSiTivE/"**, you are able to set explicit case sensitivity as well for entering patterns for `require`, `exclude` and `preferred` attributes. We default to ignore case sensitivity.

### RankingModel

While `SettingsModel` focuses on the selection and preference of torrents, `RankingModel` (such as `BaseRankingModel` or its extensions) is designed to compute the ranking scores based on those preferences. This model allows for the creation of a nuanced scoring system that evaluates each torrent's quality and attributes, translating user preferences into a quantifiable score.

Key functionalities:
- **Scoring Torrent Attributes:** Assign scores to various torrent attributes like resolution, audio quality, etc.
- **Customizable Ranking Logic:** Extend `BaseRankingModel` to tailor ranking criteria and values, enhancing the decision-making process in selecting torrents.

Example usage:
```python
from RTN.models import BaseRankingModel

class MyRankingModel(BaseRankingModel):
    uhd: int = 200  # Ultra HD content
    hdr: int = 100  # HDR content
    # Define more attributes and scores as needed
```

### Why Both Models are Necessary

`SettingsModel` and `RankingModel` work together to provide a comprehensive approach to torrent ranking:
- **SettingsModel** specifies what to look for in torrents, defining the search and preference criteria.
- **RankingModel** quantifies those preferences, assigning scores to make informed decisions on which torrents are of higher quality and relevance.

This separation allows for flexible configuration and a powerful, customizable ranking system tailored to individual user preferences.

### BaseRankingModel

Here is the default BaseRankingModel that RTN uses, and it's attributes.

```py
class BaseRankingModel(BaseModel):
    """
    A base class for ranking models used in the context of media quality and attributes.
    The ranking values are used to determine the quality of a media item based on its attributes.

    Attributes:
        uhd (int): The ranking value for Ultra HD (4K) resolution.
        fhd (int): The ranking value for Full HD (1080p) resolution.
        hd (int): The ranking value for HD (720p) resolution.
        sd (int): The ranking value for SD (480p) resolution.
        bluray (int): The ranking value for Blu-ray quality.
        hdr (int): The ranking value for HDR quality.
        hdr10 (int): The ranking value for HDR10 quality.
        dolby_video (int): The ranking value for Dolby video quality.
        dts_x (int): The ranking value for DTS:X audio quality.
        dts_hd (int): The ranking value for DTS-HD audio quality.
        dts_hd_ma (int): The ranking value for DTS-HD Master Audio audio quality.
        atmos (int): The ranking value for Dolby Atmos audio quality.
        truehd (int): The ranking value for Dolby TrueHD audio quality.
        ddplus (int): The ranking value for Dolby Digital Plus audio quality.
        ac3 (int): The ranking value for AC3 audio quality.
        aac (int): The ranking value for AAC audio quality.
        remux (int): The ranking value for remux attribute.
        webdl (int): The ranking value for web-dl attribute.
        repack (int): The ranking value for repack attribute.
        proper (int): The ranking value for proper attribute.
        dubbed (int): The ranking value for dubbed attribute.
        subbed (int): The ranking value for subbed attribute.
        av1 (int): The ranking value for AV1 attribute.
    """
    # resolution
    uhd: int = 0
    fhd: int = 0
    hd: int = 0
    sd: int = 0
    # quality
    bluray: int = 0
    hdr: int = 0
    hdr10: int = 0
    dolby_video: int = 0
    # audio
    dts_x: int = 0
    dts_hd: int = 0
    dts_hd_ma: int = 0
    atmos: int = 0
    truehd: int = 0
    ddplus: int = 0
    ac3: int = 0
    aac: int = 0
    # other
    remux: int = 0
    webdl: int = 0
    repack: int = 5
    proper: int = 4
    # extras
    dubbed: int = 4
    subbed: int = 2
    av1: int = 0
```

Keep in mind that these are explicitly set within RTN and are needed in order for RTN to work. You can add new attributes, but it will be up to you to handle them.

Create as many `SettingsModel` and `RankingModel` as you like to use anywhere in your code. They are mean't to be used as a way to version settings for your users. 

# Extras

## Torrent Parser

Use `parse` to parse a torrent title with PTT and return an RTN `ParsedData` model.

Using the example above:

```py
from RTN import parse
parsed = parse("Example.Movie.2020.1080p.BluRay.x264-Example")

print(parsed.raw_title)    # Output: "Example.Movie.2020.1080p.BluRay.x264-Example"
print(parsed.parsed_title) # Output: "Example Movie"
print(parsed.year)         # Output: 2020
```

PTT provides the extracted values; RTN validates them through `ParsedData`.
Fields have explicit types: strings, numbers, booleans and lists. Consult
`ParsedData.model_json_schema()` for each field's type and default.

## Checking Title Similarity

Sometimes, you might just want to check if two titles match closely enough, without going through the entire ranking process. RTN provides a simple function, title_match, for this purpose:

```py
from RTN import title_match

# Check if two titles are similar above a threshold of 0.9
match = title_match("Correct Movie Title 2020", "Correct Movie Title (2020)")
print(match)  # Output: True if similarity is above 0.9, otherwise False
>>> True
```

This functionality is especially useful when you have a list of potential titles and want to find the best match for a given reference title.

## Trash Check

Maybe you just want to use our own garbage collector to weed out bad titles in your current scraping setup?

```py
from RTN import parse

if parse(raw_title).trash:
    # You can safely remove any title or item from being scraped if this returns True!
    ...
```

## Movie Check

Now you can check if a raw torrent title is a `movie` or a `show` type!

```py
from RTN import parse

parsed_data = parse("Joker.2019.PROPER.mHD.10Bits.1080p.BluRay.DD5.1.x265-TMd")
print(parsed_data.type)
>>> "movie"
```

For a boolean, compare the parsed type:

```py
from RTN import parse

parsed_data = parse("Joker.2019.PROPER.mHD.10Bits.1080p.BluRay.DD5.1.x265-TMd")
print(parsed_data.type == "movie")
>>> True
```

# Real World Example

Here is a crude example of how you could use RTN in scraping.

```py
from RTN import RTN, Torrent, DefaultRanking
from RTN.exceptions import GarbageTorrent

# Assuming 'settings' is defined somewhere and passed correctly.
rtn = RTN(settings=settings, ranking_model=DefaultRanking())
...
# Define some function for scraping for results from some API.
    if response.ok:
        torrents = set()
        for stream in response.streams:
            if not stream.infohash or not title_match(correct_title, stream.title):
                # Skip results that don't match the query.
                # We want to do this first to weed out torrents
                # that are below the 90% match criteria. (Default is 90%)
                continue
            try:
                torrent: Torrent = rtn.rank(stream.title, stream.infohash, remove_trash=True)
            except GarbageTorrent:
                # One thing to note is that as we parse titles, we also get rid of garbage.
                # Feel free to add your own logic when this happens!
                # You can bypass this by setting `remove_trash` to `False` in `rank`.
                continue
            if torrent and torrent.fetch:
                # If torrent.fetch is True, then it's a good torrent,
                # as considered by your ranking profile and settings model.
                torrents.add(torrent)

        # Sort the list of torrents based on their rank in descending order
        sorted_torrents = sorted(list(torrents), key=lambda x: x.rank, reverse=True)
        return sorted_torrents
    ...

# Example usage
for torrent in sorted_torrents:
    print(f"Title: {torrent.data.parsed_title}, Infohash: {torrent.infohash}, Rank: {torrent.rank}")
```

# ParsedData Structure

Parsed values are available through `torrent.data`, for example
`torrent.data.audio_languages` or `torrent.data.resolution`. See the
[parsing reference](docs/devs/parsing.md) for field descriptions. Inspect the
model schema for the complete list of fields, types and defaults:

```py
from RTN import ParsedData

print(ParsedData.model_json_schema())
```

This will continue to grow though as we expand on functionality, so keep checking back for this list!

Find the source and proposed changes on [GitHub](https://github.com/streama-hub/rank-torrent-name).

## Performance Benchmarks

These historical upstream measurements are retained for reference. They are not
measurements of this fork or a guarantee for your workload.

### Benchmark Categories

We categorize benchmarks into two main processes:
- **Parsing**: Measures the time to parse a title and return a `ParsedData` object.
- **Ranking**: A comprehensive process that includes parsing and then evaluates the title based on defined criteria. This represents a more "real-world" scenario and is crucial for developers looking to integrate RTN effectively.

### Benchmark Results

To facilitate comparison, we've compiled the results into a single table:

| Operation                                    | Items Count | Mean Time    | Standard Deviation |
|----------------------------------------------|-------------|--------------|--------------------|
| **Parsing Benchmark (Single item)**          | 1           | 583 us       | 10 us              |
| **Batch Parse Benchmark (Small batch)**      | 10          | 6.24 ms      | 0.16 ms            |
| **Batch Parse Benchmark (Large batch)**      | 1000        | 1.57 s       | 0.06 s             |
| **Batch Parse Benchmark (XLarge batch)**     | 2000        | 3.62 s       | 0.11 s             |
| **Ranking Benchmark (Single item)**          | 1           | 616 us       | 11 us              |
| **Batch Rank Benchmark (Small batch)**       | 10          | 24.6 ms      | 2.4 ms             |
| **Batch Rank Benchmark (Large batch)**       | 1000        | 3.13 s       | 0.15 s             |
| **Batch Rank Benchmark (XLarge batch)**      | 2000        | 6.27 s       | 0.13 s             |

> :warning: Test Bench consisted of **R9 5900X CPU** and **64GB DDR4 RAM** - Your mileage may vary.

To run your own benchmark, you can clone the repo and run `make benchmark` from inside the root of the repository.

The current benchmark script runs repeated `parse` and `rank` calls sequentially.
It does not use batch API functions, chunk sizes or worker pools.


This data shows RTN's robust capability to efficiently process both small and extensive datasets.

## Optimizing RTN Performance

Reuse an `RTN` instance when ranking several torrents with the same settings.
The public API processes one title per `parse` or `rank` call; applications own
batching and concurrency. Measure those choices with your own titles and settings.

```python
from RTN import RTN, SettingsModel, parse

titles = ["Example.2024.1080p.BluRay", "Example.S01E02.720p.WEB-DL"]
parsed_data = [parse(title) for title in titles]
rtn = RTN(SettingsModel())
```

For ranking, call `rtn.rank(title, infohash)` with each torrent's actual infohash.

## Contributing

Contributions to RTN are welcomed! Feel free to submit pull requests or open issues to suggest features or report bugs. As we grow, more features will be coming to RTN, there's already a lot planned!

## License

RTN is released under the MIT License. See the LICENSE file for more details.
