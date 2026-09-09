# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- **Inline example abbreviations** ([#291](https://github.com/speedyk-005/yasbd-lib/pull/291)): Keep Hindi, Lithuanian, Malayalam, and Russian equivalents of "for example" from ending sentences.
- **Afrikaans/Dutch title `Mev.`** ([#297](https://github.com/speedyk-005/yasbd-lib/pull/297)): Added the missing `mev` honorific to `TITLE_ABBRVS` in `nl.py`, which Afrikaans inherits, preventing false sentence splits after `Mev. Jansen` (e.g., `Mev. Jansen praat.` no longer splits after `Mev.`).
- **Telephone and fax abbreviations** ([#284](https://github.com/speedyk-005/yasbd-lib/pull/284)): Treat `tel.` and `fax.` as shared reference abbreviations before contact numbers across language profiles.
- **Portuguese `aprox.` abbreviation** ([#282](https://github.com/speedyk-005/yasbd-lib/pull/282)): Added `aprox` to the Portuguese reference abbreviations so `aprox.` stays inline when introducing an approximate value (e.g., `O total, aprox. 500 reais`).
- **Unicode newline-inside-sentence detection** ([#276](https://github.com/speedyk-005/yasbd-lib/pull/276)): `NEWLINE_INSIDE_SENTENCE_FINDER` now uses the Unicode lowercase property `\p{Ll}` instead of ASCII-only `[a-z]`, so newlines before Cyrillic and other non-ASCII lowercase letters are no longer treated as sentence boundaries.
- **Russian abbreviation coverage** ([#278](https://github.com/speedyk-005/yasbd-lib/pull/278)): Expanded `TITLE_ABBRVS`, `REFERENCE_ABBRVS`, and `INLINE_ONLY_ABBRVS` with missing Russian abbreviations, and added Cyrillic initial-chain handling to `MID_SENTENCE_FINDER_LST` to prevent false splits (e.g., `Арх. Иванов` and `Проф. Петров А.К.`).
- **List boundary ordering** ([#277](https://github.com/speedyk-005/yasbd-lib/pull/277)): Run list boundary adjustment before mid-sentence filtering to prevent re-adding boundaries suppressed by abbreviation handling (e.g., `И т. д.` no longer splits).
- **Markdown numbered headers** ([#306](https://github.com/speedyk-005/yasbd-lib/pull/306)/[#307](https://github.com/speedyk-005/yasbd-lib/pull/307)): Markdown headings with trailing numbers (e.g., `### 1. The Regex Breakdown`) are kept whole instead of being split into `### 1.` and the header title.

---

## [0.16.2] - 2026-09-02

### Changed

- **Safer installation**: Constrained the `retrie`, `beartype`, and `radicli` dependencies to prevent breaking changes.

---

## [0.16.1] - 2026-08-26

### Fixed

- **Word boundary for corp entity abbreviations** ([#271](https://github.com/speedyk-005/yasbd-lib/pull/271)): Added `\b` to `CORP_ENTITY_ABBRVS` regex pattern to prevent substring matches (e.g., "co" inside "tobacco" was falsely matching as a corporate abbreviation).

---

## [0.16.0] - 2026-08-26

### Changed

- **Per-instance lang pack registry** ([#270](https://github.com/speedyk-005/yasbd-lib/pull/270)): Removed global `_LANG_PACK_REGISTRY`. `BoundaryDetector` now accepts `external_lang_packs` param and manages its own isolated registry. `register_lang_packs` renamed to `load_external_lang_packs`. `clear_lang_packs` removed.

---

## [0.15.1] - 2026-08-14

### Changed

- **Separate hook boundary validation** ([#264](https://github.com/speedyk-005/yasbd-lib/pull/264)): Split type and bounds checks in `BoundaryDetector._run_hook()` into single-pass, fast-failing guards with specific error messages.                                 

### Fixed

- **Duplicate boundary offsets** ([#261](https://github.com/speedyk-005/yasbd-lib/pull/261)): Ensure that offsets are deduplicated prior to sorting in `BoundaryDetector._run_hook()` to guarantee the uniqueness of the final boundaries.
- **False sentence splits on corporate abbreviations** ([#262](https://github.com/speedyk-005/yasbd-lib/pull/262)): Updated rules and boundary detector regex to prevent premature splits when corporate entities precede capitalized names or titles.

---

## [0.15.0] - 2026-08-13

### Changed

- **Language auto-detection is now opt-in** ([#256](https://github.com/speedyk-005/yasbd-lib/pull/256)): `py3langid` is no longer a core dependency. It is imported lazily inside `classify_language()`, so `import yasbd` no longer pulls in numpy for users who never use `lang="auto"`. It must be installed separately.[span_0](start_span)[span_0](end_span)

### Fixed

- **Words concatenated across line breaks** ([#255](https://github.com/speedyk-005/yasbd-lib/pull/255)): StreamCleaner now replaces newlines between word characters with a space, preserving word boundaries in OCR text.[span_1](start_span)[span_1](end_span)
- **False sentence splits after geopolitical abbreviations** ([#257](https://github.com/speedyk-005/yasbd-lib/pull/257)): Expanded `ORG_PROPER_NOUNS` in English rules to prevent premature sentence breaks when abbreviations like `U.S.` or `U.K.` precede common government and organizational nouns (e.g., `Government`, `Department`, `Persons`). Fixes [#253](https://github.com/speedyk-005/yasbd-lib/issues/253).

---

## [0.14.0] - 2026-08-09

### Added

- **Expanded SUFFIXES in hyphenated word finder** ([#249](https://github.com/speedyk-005/yasbd-lib/pull/249)): Added common Latin inflectional and derivational suffixes to the `SUFFIXES` set used by `HYPHENATED_WORD_FINDER`, so wrap-around line breaks like `work-\ning` join correctly to `working`.
- **Line ending normalization in default cleaning pipeline** ([#232](https://github.com/speedyk-005/yasbd-lib/issues/232)): Added `normalize_newlines` to `src/yasbd/utils/cleaner.py` and registered it in `DEFAULT_CLEANING_PIPELINE` to normalize `\r\n` and `\r` line endings to `\n`.
- **Post-processing hook on BoundaryDetector** ([#234](https://github.com/speedyk-005/yasbd-lib/pull/234)): `BoundaryDetector` now accepts a `hook` callback that runs per paragraph after the language rules apply. It receives a dict with `text`, `lang`, `boundaries` and `paragraph_index` keys and can add or remove sentence boundaries in place. A new `HookError` is raised if the hook fails or leaves invalid boundaries. This replaces monkey-patching rule internals for custom boundary logic (e.g. OpenMed's `_split_yasbd_chinese_semicolons` hack).

### Changed

- **Trie pattern builder moved to utils and renamed** ([#230](https://github.com/speedyk-005/yasbd-lib/pull/230)): `build_abbr_pattern` moved from `yasbd.rules.base` to a new `yasbd.utils.trie` module and renamed to `build_optimized_pattern`. The old name stays as a backwards-compatible alias, and language rule files now import it from `yasbd.utils.trie`.

### Fixed

- **Hyphens dropped at line breaks in hyphenated compounds** ([#231](https://github.com/speedyk-005/yasbd-lib/pull/231)): StreamCleaner removed the hyphen when a line broke at a legitimate hyphenated compound, turning `state-of-the-\nart` into `state-of-theart`. Now only known prefixes/suffixes join across line breaks; all other cases keep the hyphen. Unicode hyphen variants are normalized to ASCII first.
- **Absolute offsets ignore leading blank lines** ([#236](https://github.com/speedyk-005/yasbd-lib/pull/236)): `detect()` skipped whitespace-only paragraphs before accumulating the offset, so text starting with blank lines produced offsets relative to the first non-whitespace paragraph. Whitespace paragraphs now advance the offset.

---

### [0.13.1] - 2026-07-25

### Fixed

- **Vertical list false positive on ordinary text** ([#214](https://github.com/speedyk-005/yasbd-lib/pull/214)): VERTICAL_LIST_START_FINDER matched any 1-4 character alphanumeric prefix as a list marker, causing false boundary removal in normal sentences. Restricts detection to pure digits and single-letter + optional digit markers.

---

## [0.13.0] - 2026-07-23

### Changed

- **Code quality cleanup** ([#203](https://github.com/speedyk-005/yasbd-lib/pull/203)):
  - Extracted `_apply_cleaning_pipeline` from `StreamCleaner.__next__` and renamed `CLEANING_PIPELINE` to `DEFAULT_CLEANING_PIPELINE`.
  - Simplified `detect()` offset calculation by removing unnecessary ternary.
  - Simplified `TextSpan.__eq__` with `all()` for cleaner `hasattr` checks.
  - Fixed double spaces after commas (nl, my, sv, tr, id) and double space after operator (bg).
- **Merged "Pronouns & Demonstratives" header into "Pronouns"** ([#196](https://github.com/speedyk-005/yasbd-lib/pull/196)): comment-only change in id.py and vi.py.
- **Python 3.10 support** ([#212](https://github.com/speedyk-005/yasbd-lib/pull/212)): Lowered minimum from 3.11 to 3.10. Added classifier and CI entry.

### Fixed

- **Double boundary for `.\n`** ([#207](https://github.com/speedyk-005/yasbd-lib/pull/207)): `detect()` yielded two consecutive offsets for `.\n`, leaving an empty span when sentences were reconstructed. Added `\n` to the negative lookahead in `CANDIDATE_BOUNDARY_FINDER` so the terminator no longer creates a separate boundary when a newline follows.
- **Flattened list segmentation** ([#211](https://github.com/speedyk-005/yasbd-lib/pull/211)): Guarded `QUOTE_AND_PAREN_END_FINDER` behind `inner_range` check and relaxed the adjacency check so list markers at varying distances are recognized as part of the same list.
- **Vertical list detection for multi-digit numbers** ([#204](https://github.com/speedyk-005/yasbd-lib/pull/204)): Expanded VERTICAL_LIST_START_FINDER quantifier to `{1,4}` and added `re.M` flag so multi-digit list markers at any line start are not mistaken for sentence boundaries.

### Removed

- **Unused timeout parameter from `_create_external_cleaner`** ([#193](https://github.com/speedyk-005/yasbd-lib/pull/193)).

---

## [0.12.0] - 2026-07-18

### Added

- **Brand/snack exclamation entries**: Crunch and Banga added to `NAMES_WITH_EXCLAMATION`.
- **Extended `REFERENCE_ABBRVS`** ([#189](https://github.com/speedyk-005/yasbd-lib/pull/189)): added `cit` and `nr` for cross-language use.
- **Set literal reformatting script** ([#165](https://github.com/speedyk-005/yasbd-lib/pull/165)): `scripts/reformat_sets.py` automatically balances set items to ≤70 chars per line.
- **Lithuanian (lt) language support** ([#168](https://github.com/speedyk-005/yasbd-lib/pull/168)).
- **Turkish (tr) language support** ([#180](https://github.com/speedyk-005/yasbd-lib/pull/180)).
- **Bulgarian (bg) language support** ([#185](https://github.com/speedyk-005/yasbd-lib/pull/185)).
- **Kazakh (kk) language support** ([#171](https://github.com/speedyk-005/yasbd-lib/pull/171)).
- **Romanian (ro) language support** ([#189](https://github.com/speedyk-005/yasbd-lib/pull/189)).
- **Armenian (hy) language support** ([#195](https://github.com/speedyk-005/yasbd-lib/pull/195)).

### Changed

- **Consistent set literal formatting** ([#165](https://github.com/speedyk-005/yasbd-lib/pull/165)): sets across 21 rule files reformatted.

### Fixed

- **Missing commas in set literals** ([#173](https://github.com/speedyk-005/yasbd-lib/pull/173)): 3 files had missing commas causing silent string concatenation; 5 files had missing space after comma.
- **Flattened list heuristic** ([#169](https://github.com/speedyk-005/yasbd-lib/pull/169)): pairwise proximity check prevents false positives from randomly spaced horizontal markers.
- **Removed ambiguous shared abbreviations** ([#166](https://github.com/speedyk-005/yasbd-lib/pull/166)): `est`, `dist`, `misc`, `tel` removed from base `INLINE_ONLY_ABBRVS`. French also excludes `est` from reference abbreviations.
- **HTML markup leaking through cleaner** ([#162](https://github.com/speedyk-005/yasbd-lib/pull/162)): doctype declarations, comments, and processing instructions no longer pass through. Void elements removed from content-stripping group. Math expressions like `x < 5 and y > 3` no longer mangled.

---

## [0.10.0] - 2026-07-09

### Added

- **Bengali (bn) language support** ([#147](https://github.com/speedyk-005/yasbd-lib/pull/147)).
- **Czech (cs) language support** ([#146](https://github.com/speedyk-005/yasbd-lib/pull/146)).
- **Polish (pl) language support** ([#144](https://github.com/speedyk-005/yasbd-lib/pull/144)).
- **Swahili (sw) language support** ([#149](https://github.com/speedyk-005/yasbd-lib/pull/149)).
- **Urdu (ur) language support** ([#154](https://github.com/speedyk-005/yasbd-lib/pull/154)).

### Changed

- **Code quality improvements** ([#161](https://github.com/speedyk-005/yasbd-lib/pull/161)):
  - Language abbreviation/section sets extended instead of replaced in 8 modules (ar, fa, ru, am, cs, pl, sw, el).
  - Boolean parameters made keyword-only in `load_rule()`, `ParagraphStream`, and pysbd `Segmenter`.
  - Named constants `_MIN_CONFIDENCE` and `_MAX_CACHED_RULES` extracted from magic numbers.
  - Expanded ruff lint rules with FBT, ARG, PLR, and other rule sets; auto-fixes applied.
  - `TextSpan.__hash__` added; unused parameters cleaned up.

### Fixed

- **Clock abbreviations** ([#152](https://github.com/speedyk-005/yasbd-lib/pull/152)): protect kl, hod, год from false sentence boundaries in cs, sk, uk, sv.
- **Non-German ordinal boundary inheritance** ([#153](https://github.com/speedyk-005/yasbd-lib/pull/153)): remove inherited German ordinal pattern from nl, sv, da, af to fix false negatives on numbered sentence boundaries.
- **Nested quote boundary leak** ([#156](https://github.com/speedyk-005/yasbd-lib/pull/156)): prevent inner single quotes inside double quotes from creating false sentence boundaries.
- **`&` after title abbreviation** ([#157](https://github.com/speedyk-005/yasbd-lib/pull/157)): prevent & from triggering false sentence boundary after Com. or similar title abbreviations.
- **Name initials at start of text** ([#160](https://github.com/speedyk-005/yasbd-lib/pull/160)): prevent `A. B. Smith` from being split by horizontal list marker pattern.

---

## [0.9.0] - 2026-07-03

### Added

- **Marathi (mr) language support** ([#139](https://github.com/speedyk-005/yasbd-lib/pull/139)).
- **Indonesian (id) language support** ([#137](https://github.com/speedyk-005/yasbd-lib/pull/137)).
- **Slovak (sk) language support** ([#129](https://github.com/speedyk-005/yasbd-lib/pull/129)).
- **Vietnamese (vi) language support** ([#131](https://github.com/speedyk-005/yasbd-lib/pull/131)).
- **Persian (fa) language support** ([#128](https://github.com/speedyk-005/yasbd-lib/pull/128)).
- **Malayalam (ml) language support** ([#124](https://github.com/speedyk-005/yasbd-lib/pull/124)).
- **Ukrainian (uk) language support** ([#122](https://github.com/speedyk-005/yasbd-lib/pull/122)).
- **`--from-pack` CLI flag** ([#140](https://github.com/speedyk-005/yasbd-lib/pull/140)): lets you load external language packs right from the terminal.

### Changed

- **`--lang` now required** in CLI `segment` and `detect` commands ([#140](https://github.com/speedyk-005/yasbd-lib/pull/140)): dropped the default to match the Python API. Pass `--lang` explicitly or get an error.
- **`register_lang_packs()` return type** ([#140](https://github.com/speedyk-005/yasbd-lib/pull/140)): now returns a `list[str]` of language codes instead of `None`. No more reaching into `_LANG_PACK_REGISTRY`.
- **CJKV mixin renamed to CJK** ([#131](https://github.com/speedyk-005/yasbd-lib/pull/131)): Vietnamese uses Latin script, not CJK ideographs.
- **Internal refactors** ([#141](https://github.com/speedyk-005/yasbd-lib/pull/141)):
  - Etc-style entries removed from abbreviation sets; and-others moved to `REFERENCE` for context-limited suppression.
  - Full-word honorifics and geopolitical names stripped from script-language abbreviation sets.
  - `_post_process_boundaries` and `_build_abbr_pattern` made public; `main_boundaries` renamed to `sentence_boundaries`.
  - Project and CLI descriptions updated to rule-based.

### Fixed

- **CLI error handling**: catch `UnsupportedLanguageError` in `main()` for a clean error message instead of a Python traceback.
- **Coordinate direction abbreviations** ([#134](https://github.com/speedyk-005/yasbd-lib/pull/134)): N., S., E., W. after digits/degree signs now terminate sentences (e.g., "40.7128° N."). Initials like "N. Scott Momaday" are preserved.

---

## [0.8.0] - 2026-06-28

### Added
- **py.typed marker** ([#116](https://github.com/speedyk-005/yasbd-lib/pull/116)): PEP 561 compliance marker for Mypy and Pyright static type checking.
- **Language pack system** ([#111](https://github.com/speedyk-005/yasbd-lib/pull/111)): `register_lang_packs()` with handshake validation and lang pack registry.
- **`LangPackError` exception class** ([#111](https://github.com/speedyk-005/yasbd-lib/pull/111)): raised when a language pack module fails validation or handshake.
- **Korean (ko) language support** ([#113](https://github.com/speedyk-005/yasbd-lib/pull/113)).
- **Dutch (nl) language support** ([#114](https://github.com/speedyk-005/yasbd-lib/pull/114)).
- **Afrikaans (af) language support** ([#120](https://github.com/speedyk-005/yasbd-lib/pull/120)).
- **German military rank titles** ([#114](https://github.com/speedyk-005/yasbd-lib/pull/114)): Added to `TITLE_ABBRVS`.
- **Swedish (sv) language support** ([#121](https://github.com/speedyk-005/yasbd-lib/pull/121)).
- **Danish (da) language support** ([#121](https://github.com/speedyk-005/yasbd-lib/pull/121)).

### Changed

- **CJKV mixin** ([#115](https://github.com/speedyk-005/yasbd-lib/pull/115)): Shared full-width abbreviation pattern extracted from ``zh``, ``ja``, ``ko`` into ``base.py``.

### Fixed
- **German `DATE_ABBRVS`**: Removed "mai" — it's a full word, not an abbreviation.
- **ORDINAL regex (de, nl)** ([#114](https://github.com/speedyk-005/yasbd-lib/pull/114)): Changed `\d+` to `\d{1,3}` to avoid false sentence breaks after 3+ digit numbers.
- **Language tag normalization helper** ([#112](https://github.com/speedyk-005/yasbd-lib/pull/112)).
- **Thai discourse final particles**: Removed false positives `นะ` and `จ๋า` from `DISCOURSE_FINAL_PARTICLES`.
- **Burmese and Thai reporting words** ([#118](https://github.com/speedyk-005/yasbd-lib/pull/118)): Corrected attribute name from `REPORTING_VERBS` to `REPORTING_WORDS` — without this, the rules had no effect.

---

## [0.7.0] - 2026-06-22

### Added
- **Burmese (my) language support** ([#104](https://github.com/speedyk-005/yasbd-lib/pull/104)).
- **Hindi (hi) language support** ([#108](https://github.com/speedyk-005/yasbd-lib/pull/108)).

### Changed
- **CLI zero-copy file input** ([#107](https://github.com/speedyk-005/yasbd-lib/pull/107)): `--file` and stdin pipe now pass file handles directly to the detector instead of reading the entire file into memory first.
- **Refactored benchmark scripts** ([#105](https://github.com/speedyk-005/yasbd-lib/pull/105)): wrapped all benchmark scripts in `run_*` functions with `if __name__ == "__main__"` guards, migrated to `rich` console output, and cleaned up `bench_utils.py` (removed unused `langs` attributes, added docstrings, renamed `_console` for consistency).
- **Thai & Burmese ellipsis regex removal**: removed redundant `MID_SENTENCE_FINDER_LST` ellipsis pattern since `.` is not a sentence terminator in either language.
- **Input validation refactor** ([#106](https://github.com/speedyk-005/yasbd-lib/pull/106)): Replaced Pydantic's `validate_call` with beartype.

### Fixed
- **ParagraphStream auto-cleanup** ([#107](https://github.com/speedyk-005/yasbd-lib/pull/107)): added ``__del__`` and ``close()`` to ``ParagraphStream`` so opened file handles are closed on garbage collection.
- **List marker detection for non-Latin scripts** ([#103](https://github.com/speedyk-005/yasbd-lib/pull/103)): expanded `VERTICAL_LIST_START_FINDER` and `HORIZONTAL_LIST_FINDER` to accept Burmese, Devanagari, and other dot-like characters (။, ।, ·, •, etc.).
- **Thai & Burmese UTTERANCE_FINDER removal** ([#104](https://github.com/speedyk-005/yasbd-lib/pull/104)): removed `UTTERANCE_FINDER` and `STANDALONE_UTTERANCES` set from both `th.py` and `my.py` to prevent false sentence boundaries after discourse particles.

---

## [0.6.0] - 2026-06-15

### Added
- **spaCy v3+ pipeline component** ([#95](https://github.com/speedyk-005/yasbd-lib/pull/95)): Register yasbd as a native spaCy component, with lazy import guard and configurable via pipe.
- **Italian (it) language support** ([#99](https://github.com/speedyk-005/yasbd-lib/pull/99)).
- **Expanded base `TERMINATORS`** ([#96](https://github.com/speedyk-005/yasbd-lib/pull/96)): across major scripts (Armenian, Devanagari, Ethiopic, Mongolian, etc.) for better mixed-script support.
- **Book benchmarking script** ([#97](https://github.com/speedyk-005/yasbd-lib/pull/97)): `bench_books.py` benchmarks all SBD libraries on full-length books (Alice in Wonderland, Sherlock Holmes) with cold/warm timings and sentence counts.
- **Thai (th) language support** ([#100](https://github.com/speedyk-005/yasbd-lib/pull/100)): By far the hardest language to add — unicase, no word-boundary whitespace, punctuation used mainly in abbreviations, and discourse particles that required careful negative lookaheads to avoid double-splitting.
- **Greek (el) language support** ([#101](https://github.com/speedyk-005/yasbd-lib/pull/101)).
- **Expanded base `DOTTED_GEOPOL_ABBRVS`** ([#102](https://github.com/speedyk-005/yasbd-lib/pull/102)): major international organizations (N.A.T.O., U.N.E.S.C.O., W.H.O., etc.), regional bodies (A.U., O.A.S., A.S.E.A.N.), and additional sovereign state abbreviations.

### Changed
- **`QUOTATIVE_PARTICLES` renamed to `POST_QUOTATIVE_PARTICLES`** across all language rules to clarify they appear after quoted speech.

### Fixed
- **Conflict with quote/paren removal** ([#100](https://github.com/speedyk-005/yasbd-lib/pull/100)): reordered base pipeline so `_post_process_boundaries` runs before quote/paren spans are stripped.

---

## [0.5.0] - 2026-06-13

### Added
- **Automatic language detection** ([#86](https://github.com/speedyk-005/yasbd-lib/pull/86)): Pass `lang="auto"` to detect language via py3langid. Logs when confidence < 0.8.
- **`classify_language` utility** ([#86](https://github.com/speedyk-005/yasbd-lib/pull/86)): Wraps py3langid with softmax normalization and preference for supported languages.
- **Amharic (am) language support** ([#91](https://github.com/speedyk-005/yasbd-lib/pull/91)).

### Changed
- **Benchmarks expanded** ([#94](https://github.com/speedyk-005/yasbd-lib/pull/94)): EN golden data grew from 85 to 92 cases with academic citation patterns. Updated scores, refreshed cold/warm speed numbers, added per-language comparison links.
- **Internal refactors** ([#86](https://github.com/speedyk-005/yasbd-lib/pull/86)):
  - Cached up to 5 rule objects, evicting least recently used on overflow.
  - Moved `load_rule` because rule loading belongs to the rules package, not the detector.
  - Restructured `detect()` loop with first paragraph peeked before loop, uses `chain()` to rejoin — cleaner separation of EOF logic from content processing.
- **`NEWLINE_IN_MIDDLE_OF_WORD_FINDER` renamed to `NEWLINE_BETWEEN_WORD_CHARS`** and expanded pattern from `(?<=\b[a-zA-Z]{1,2})\n` to `(?<=\w)\n(?=\w)` to join mid-word newlines at any word-character boundary.

---

## [0.4.0] - 2026-06-10

### Added
- **`StreamCleaner` extra steps**: Custom cleaning functions run after the built-in pipeline. CLI via `--extra-step` / `-e` on `yasbd clean`, repeatable.
- **`CleanStepError`**: Raised when an extra step fails or returns non-string.
- **CLI short flags**: `-w` for `--preserve-whitespace`, `-r` for `--relative`.
- **Custom exception classes**: `YasbdError` (base), `UnsupportedLanguageError`, and `InvalidInputError` with ValueError/TypeError mixins.
- **Flat utils imports** ([#84](https://github.com/speedyk-005/yasbd-lib/pull/84)): Utils submodules now importable at package root via `__path__` extension — `from yasbd.cleaner import StreamCleaner` as an alternative to `from yasbd.utils.cleaner import StreamCleaner`.
- **Radicli-based CLI** ([#79](https://github.com/speedyk-005/yasbd-lib/pull/79)): `segment`, `detect`, `clean`, and `langs` subcommands with auto-stdin detection, JSONL output, and ~3.3x faster startup vs typer.

### Fixed
- **Emoji boundary detection** ([#77](https://github.com/speedyk-005/yasbd-lib/pull/77)): Emojis following terminal punctuation now stay with the preceding sentence. Besides, split after emoji + common sentence starter.
- **English `TITLE_ABBRVS`**: Excluded `min` to prevent false split suppression (minute/minimum should not suppress sentence boundaries).

### Changed
- **API doc generation** ([#83](https://github.com/speedyk-005/yasbd-lib/pull/83)): Replaced `python_docstring_markdown` with `pydoc-markdown`, fixing broken anchor links for re-exported symbols. Added `scripts/gen_api_docs.sh` for easy regeneration.
- **`log_info` helper**: Extracted to `yasbd.utils.logger` — gated logging without repeating `if verbose:`.
- **Unsupported language error messages** ([#78](https://github.com/speedyk-005/yasbd-lib/pull/78)): now list supported codes and suggest close matches (e.g. `eng` => `en`).
- **Variable renames for clarity**:
  - `MID_SENTENCE_ABBRVS` => `INLINE_ONLY_ABBRVS`
  - `HEADING_TOKENS` => `SECTION_MARKERS`
  - `GEOPOLITICAL_ABBRVS` => `DOTTED_GEOPOL_ABBRVS`
- **Spanish `COMMON_SENT_STARTERS` cleaned**: Removed 15 prepositions (En, Por, Para, De, etc.) and 15 verbs (Es, Son, Fue, Hay, etc.) that caused false sentence boundaries after `Ud.`/`Vd.` abbreviations.

---

## [0.3.0] - 2026-06-08

### Added
- **Five new languages** ([#48](https://github.com/speedyk-005/yasbd-lib/pull/48), [#54](https://github.com/speedyk-005/yasbd-lib/pull/54)): Russian (ru), Arabic (ar), Chinese (zh), German (de), and Portuguese (pt)
- **Base abbreviation expansion**: Added `diag` to `REFERENCE_ABBRVS`.
- **`Rules.apply` early return**: Added guard for empty/whitespace-only input to skip processing.

### Changed
- **`NAIVE_BOUNDARY_FINDER` cluster logic unification**: Merged contiguous terminator handling into the lookahead assertion for more consistent behavior and fewer edge-case bugs.
- **`FULLWIDTH_GEOPOLITICAL_ABBRVS` moved to class-level attribute** with dynamic regex matching instead of static sets.
- **`COMMON_SENT_STARTERS` expanded** with time-related adverbs (Then, Afterwards, Later, etc.) across all 9 languages.
- **`BoundaryDetector.detect` refactored**: Simplified paragraph iteration logic to reduce cognitive complexity from 20.

### Fixed
- **Full-width geopolitical abbreviation over-matching**: Replaced static set with dynamic regex to prevent false splits in mixed-script text.
- **Acronym/initialism boundary constraint**: Simplified lookbehind to `[.\s]` to reduce false positive matches in edge cases.
- **Superscript indicator false splits**: Added protection to prevent boundary breaks after ordinal markers.
- **Em-dash quoted text splitting**: Added em-dash pattern to `QUOTE_AND_PAREN_FINDER` so dialogue quoted with dashes (`—text! —`) is no longer split prematurely.
- **Newline boundary handling** ([#64](https://github.com/speedyk-005/yasbd-lib/pull/64)): Added `\n` to `NAIVE_BOUNDARY_FINDER` and updated `NEWLINE_INSIDE_SENTENCE_FINDER` to recognize `>` continuation, preventing markdown heading merging.
- **Single-letter list marker false splits** ([#71](https://github.com/speedyk-005/yasbd-lib/pull/71)): Added context-aware heuristic to `_adjust_list_boundaries` so standalone "A." or "B." in prose are no longer split as list items.

---

## [0.2.0] - 2026-06-04

### Added
- **`_post_process_boundaries` hook** ([#39](https://github.com/speedyk-005/yasbd-lib/pull/39)): Language-aware sentence boundary correction without modifying regex core pipeline.
- **StreamCleaner step pipeline control (`steps_to_skip`)** ([#41](https://github.com/speedyk-005/yasbd-lib/pull/41)): Selectively disable cleanup stages like OCR normalization, HTML sanitization, whitespace normalization, and mojibake correction.

### Changed
- **Regex architecture refactor in `base.py`**: Promoted local regex patterns into class-level attributes for consistency and reuse.
- **`STREET_ABBRVS` merged into `MID_SENTENCE_ABBRVS`**: Street abbreviations are now strictly non-splitting; English restores boundary logic via post-processing hook.
- **`COMMON_ORG_NOUNS` renamed to `ORG_PROPER_NOUNS`**: Renamed and restricted to proper nouns only.
- **Geopolitical abbreviations normalization**: Standardized casing across languages for consistent detection behavior.

### Fixed
- **Multilingual structural heading detection** ([#44](https://github.com/speedyk-005/yasbd-lib/pull/44)): Prevents structural headings from triggering false sentence splits in EN, ES, FR, and HT context.
- **Sentence splitting after mixed-case scientific units** ([#42](https://github.com/speedyk-005/yasbd-lib/pull/42)): Fixes boundary suppression caused by treating mixed-case units (e.g., `meV.`, `kV.`) as standard abbreviations. Fixes [#33](https://github.com/speedyk-005/yasbd-lib/issues/33).
- **Sentence splitting bug after `a.m./p.m.` + date tokens** ([#40](https://github.com/speedyk-005/yasbd-lib/pull/40)): Prevented incorrect segmentation when time tokens precede month/day expressions.
- **Japanese over-matching boundary logic**: Removed invalid `\b` dependency in CJK context.
- **Spanish `Ud.` / `Vd.` context splitting issue** ([#31](https://github.com/speedyk-005/yasbd-lib/pull/31)): Prevents incorrect sentence break when followed by proper nouns.
- **Reference abbreviation bracket edge case** ([#35](https://github.com/speedyk-005/yasbd-lib/pull/35)): Added `[` to lookahead set to prevent false boundary triggers.
- **Time-date pipeline cleanup (English-specific logic)** ([#40](https://github.com/speedyk-005/yasbd-lib/pull/40)): Ensures time/date handling is isolated to English rules without affecting other languages.

---

## [0.1.3] - 2026-06-01

### Fixed
- **Horizontal list finder over-match safety**: Restricts single-letter abbreviations (`p.`, `h.`, `s.`) from being incorrectly identified as alphabetic list markers by capping the range to `[a-eA-E]`.

---

## [0.1.2] - 2026-06-01

### Added
- **English golden benchmark suite (`EN_GOLDEN_DATA.py`)**: Introduced an 84-case golden validation set for English accuracy testing.
- **Golden benchmark execution runner (`run_golden.py`)**: Added an automated script to run accuracy comparisons across seven different libraries against the golden suite.
- **Expanded abbreviation coverage**: Added dozens of new terms across all core abbreviation categories (TITLE, REFERENCE, DATE, MID_SENTENCE, STREET, NAMES_WITH_EXCLAMATION).

### Changed
- **Trie-based pattern compilation** ([Commit 2c2f7df](https://github.com/speedyk-005/yasbd-lib/commit/2c2f7dfbeac91162c25df4ea5c2d17ea4150fdd7)): Replaced sorted `"|".join()` with `retrie.Trie` for optimized abbreviation regex generation.
- **Performance benchmarks rewrite**: Re-engineered cold/warm benchmarking tables, updated eight scenario tables with empirical runtimes, and appended accuracy metrics and conclusions.
- **Abbreviation logical redistribution**: Migrated shared tokens (e.g., `fr`, `ing`, `mme`) to the base configuration, allowing language-specific inheritance to handle localized overrides.
- **Pydantic version requirement relaxation**: Lowered the dependency constraint from `>=2.12.2` to `>=2.11.0` to maximize environment compatibility.

### Fixed
- **Module import error resolution**: Patched `boundary_detector.py` to stop swallowing unrelated import issues when a valid language class exists but lacks a sub-dependency.
- **PM/AM boundary false positives**: Excluded all-caps `P.M.` from being captured by the general acronym rules via targeted exclusions.

---

## [0.1.1] - 2026-05-30

### Fixed
- **Single-quote dialogue split bug** ([#35](https://github.com/speedyk-005/yasbd-lib/pull/35)): Fixed issues where the engine split text prematurely before a trailing dialogue tag (e.g., `'Is this great?' she said.`).
- **Ellipsis split suppression**: Prevented three-dot ellipsis (`...`) from acting as a terminal boundary, reserving splits strictly for four-dot boundaries.
- **Roman numeral initialism protection**: Stopped the pronoun `I` from triggering false sentence breaks in name strings like `Albert I. Jones`.
- **Numero reference split suppression**: Added `N°.` to the reference abbreviation lexicon to prevent false breaks.

### Changed
- **List finder regex backend migration**: Replaced standard regex search with `re2` to utilize lookbehinds, supporting non-Latin scripts via unicode class properties.

---

## [0.1.0] - 2026-05-29

Initial release.

### Added
- **Multilingual language engine**: Added core splitting support for 5 initial languages including English, French, Spanish, Haitian Creole, and Japanese.
- **Two-pass boundary engine**: Implements an optimized two-pass architecture featuring pre-processing rules and a main lookbehind abbreviation guard.
- **High-speed performance benchmark**: Tested speeds up to 16.5× faster than `pysbd` on 10.8K character benchmarking datasets.
- **Drop-in PySBD compatibility**: Included a drop-in `Segmenter` adapter that mirrors `pysbd`'s API interface, exposing `segment()`, `clean`, and `char_span` capabilities.
- **Flexible dual-mode API**: Exposes `detect()` for retrieving raw boundary offset slices and `segment()` for producing rich text string spans.
- **Comprehensive benchmarking harness**: Bundles comparative analysis scripts comparing seven libraries across seven distinct edge-case scenarios.
