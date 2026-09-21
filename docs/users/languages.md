# Language Support in RTN

Language preferences accept both base codes and regional tags. `fr` matches all
French variants, including `fr-FR` and `fr-CA`; `fr-CA` only matches that tag.
Matching is case-insensitive. A regional preference does not match an older value
that only contains the base code, because its region is unknown.

These preferences apply to audio (`audio_languages`), not `subtitle_languages`.
`VOSTFR` alone does not satisfy a required French audio preference. `multi` may be
selected explicitly but does not establish any particular language.

The same matching applies to `required`, `allowed`, `exclude`, `preferred` and the
English exception. The built-in `anime`, `non_anime`, `common` and `all` groups
continue to expand for required, allowed and excluded languages. `all` retains
its existing scope (anime and non-anime groups); it does not include English or
the `multi` marker.

---

## Supported Languages {#supported-languages}

Below is a comprehensive list of languages supported by RTN, along with their corresponding ISO 639-1 codes:

| Code | Language   | Code | Language   | Code | Language   |
|------|------------|------|------------|------|------------|
| `ar`   | Arabic     | `fr`   | French     | `ml`   | Malayalam  |
| `bn`   | Bengali    | `de`   | German     | `mr`   | Marathi    |
| `bg`   | Bulgarian  | `el`   | Greek      | `ms`   | Malay      |
| `zh`   | Chinese    | `gu`   | Gujarati   | `no`   | Norwegian  |
| `hr`   | Croatian   | `he`   | Hebrew     | `fa`   | Persian    |
| `cs`   | Czech      | `hi`   | Hindi      | `pl`   | Polish     |
| `da`   | Danish     | `hu`   | Hungarian  | `pt`   | Portuguese |
| `nl`   | Dutch      | `id`   | Indonesian | `pa`   | Punjabi    |
| `en`   | English    | `it`   | Italian    | `ro`   | Romanian   |
| `et`   | Estonian   | `ja`   | Japanese   | `ru`   | Russian    |
| `fi`   | Finnish    | `kn`   | Kannada    | `sr`   | Serbian    |
| `ko`   | Korean     | `la`   | Latin      | `sk`   | Slovak     |
| `lv`   | Latvian    | `lt`   | Lithuanian | `sl`   | Slovenian  |
| `es`   | Spanish    | `sv`   | Swedish    | `ta`   | Tamil      |
| `te`   | Telugu     | `th`   | Thai       | `tr`   | Turkish    |
| `uk`   | Ukrainian  | `vi`   | Vietnamese |        |            |

## Using Language Codes in RTN

When configuring RTN, you can use these language codes to:

1. Set preferred languages for torrent selection
2. Exclude specific languages from your search results
