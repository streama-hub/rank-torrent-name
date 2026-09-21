# Changelog

## 1.0.0

- Require PTT 1.0.0 from a pinned Git revision.
- Preserve subtitle languages and Dolby Vision profiles in parsed models and JSON.
- Use `audio_languages` throughout parsing, filtering, ranking and serialization, replacing the `languages` result field and accessor.
- Keep `settings.languages` unchanged and match regional audio tags in language preferences.
- Expose 3D through `three_d` in Python and `3d` in aliased JSON, replacing `_3d`.
- Map PTT's `convert` flag to `converted`.
- Handle detailed audio codecs, HDR formats and height-channel layouts in ranking and filtering.
- Allow DTS-HD and DTS-X policies to inherit existing DTS policies when unspecified.
- Apply extra ranks independently of season, episode and HDR metadata.
- Preserve an unknown FFprobe track language as an empty string.
- Correct parsing documentation and retain the upstream authors and license.

The filename parser remains PTT. RTN does not duplicate its extraction rules or
introduce application-specific title cleanup or pack classification.
