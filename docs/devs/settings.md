## SettingsModel
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/models.py)
```python 
from RTN.models import SettingsModel
settings = SettingsModel()
```

---
Represents user-defined settings for ranking torrents, including preferences for filtering torrents
based on regex patterns and customizing ranks for specific torrent attributes. This model allows for
advanced customization and fine-grained control over the ranking process.

**Attributes**

* **require** (List[str | Pattern]) : Patterns torrents must match to be considered.
* **exclude** (List[str | Pattern]) : Patterns that, if matched, result in torrent exclusion.
* **preferred** (List[str | Pattern]) : Patterns indicating preferred attributes in torrents. Given +5000 points by default.
* **custom_ranks** (Dict[str, Dict[str, CustomRank]]) : Custom ranking configurations for specific attributes, allowing users to define how different torrent qualities and features affect the overall rank.

---

Methods:

    __getitem__(item: str) -> CustomRank: Access custom rank settings via attribute keys.


**Note**

- The `require`, `exclude`, and `preferred` attributes are optional!
- The `custom_ranks` attribute contains default values for common torrent attributes, which can be customized by users.
- Patterns enclosed in '/' without a trailing 'i' are compiled as case-sensitive.
- Patterns not enclosed are compiled as case-insensitive by default.

This model supports advanced regex features, enabling powerful and precise filtering and ranking based on torrent titles and attributes.

----

## CustomRank
[source](https://github.com/streama-hub/rank-torrent-name/blob/main/RTN/models.py)
```python 
CustomRank()
```

Custom Ranks used in SettingsModel.

---

### SettingsModel

`SettingsModel` is designed to be fully customizable by __users__, allowing you to define your own filtering criteria, including patterns to require, exclude, and prefer in torrent names. This model empowers you to dynamically configure torrent selection based on your specific patterns and preferences.

Key functionalities:

- **Filtering Torrents:** You have the control to determine which torrents to consider or ignore based on your matching patterns.
- **Prioritizing Torrents:** Indicate your preferred attributes to give certain torrents higher precedence according to your needs.
- **Custom Ranks Usage:** Decide how specific attributes influence the overall ranking, enabling or disabling custom ranks as you see fit.

!!! warning 
    The `SettingsModel` is only used when ranking torrents, you do not need it if you are just wanting to `parse()` torrents.

## Setup your Settings Model

Begin by defining your preferences in a `SettingsModel`. This includes specifying the required patterns, exclusions, preferences, and custom ranks for various torrent attributes. The `SettingsModel` allows you to customize how torrents are filtered and ranked based on your specific needs.

- **require:** These are patterns that must be present in the torrent name for it to be considered.
- **exclude:** These are patterns that, if present in the torrent name, will exclude the torrent from consideration.
- **preferred:** These are patterns that, if present, will give the torrent a higher priority.
- **resolutions:** These will be used to determine what is fetched when ranking torrents.
- **options:** These are options that can be used to customize the behavior of the RTN.
- **languages:** These are languages that can be used to customize the behavior of the RTN.
- **custom_ranks:** These allow you to assign specific ranks to various attributes of the torrents, such as quality or resolution.

Inspect the current defaults directly from the model:

## Example Usage

```python
from RTN.models import SettingsModel

settings = SettingsModel()
print(settings.model_dump_json(indent=2))
```

To customize only the settings you need:

```python
from RTN.models import CustomRank, SettingsModel

settings = SettingsModel(
    resolutions={"1080p": True, "720p": True},
    languages={"required": ["fr"], "preferred": ["fr-CA"]},
    custom_ranks={
        "quality": {
            "bluray": CustomRank(fetch=True, use_custom_rank=True, rank=150),
        },
    },
)
assert settings.custom_ranks["quality"]["bluray"].rank == 150
```

We cover a lot already, so users are able to add their own custom regex patterns without worrying about the basic patterns.

### Understanding Fetch and Custom Rank

- `fetch`: Determines if RTN should consider a torrent for downloading based on the attribute. True means RTN will fetch torrents matching this criterion.
- `use_custom_rank`: Controls whether the custom rank value is used in the overall ranking calculation. Disabling it reverts to using the ranking model you set instead. This is useful for toggling custom ranks on and off from a users perspective.
- `rank`: Sets the rank at which that item is graded with.
