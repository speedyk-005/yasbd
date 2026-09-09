import re  # For simpler patterns
from itertools import pairwise

import regex as re2

from yasbd.utils.trie import build_optimized_pattern

# Backwards-compat alias for the pre-rename public API name.
build_abbr_pattern = build_optimized_pattern


class CJK:
    """Mixin for CJK languages sharing full-width geopolitical abbreviation patterns."""

    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix geopolitical split when used as adj"""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.append(
            # Full-width geopolitical abbreviations
            re.compile(r"(?:[\uFF21-\uFF3A\uFF41-\uFF5A\uFF10-\uFF19]．){1,5}")
        )


# fmt: off
class Rules:
    TERMINATORS = {
        "!", ".", "?", "։", "؟", "۔", "߹", "।", "॥", "။", "።",
        "፧", "᙮", "᠃", "᠉", "‼", "⁈", "⁉", "。", "꓿", "꧉", "！",
        "．", "？", "｡",
    }

    TITLE_ABBRVS = {
        # Standard Professional (Universal Latin roots)
        "dir", "dr", "drs", "hon", "ing", "insp", "med", "prof",
        "rev", "spec", "supt",

        # Global Social
        "br", "fr", "messrs", "mlle", "mme", "mmes", "mr",
        "mrs", "ms", "mssrs", "st", "sr", "jr",

        # Military (NATO/International Standardized Ranks)
        "adm", "brig", "capt", "cmdr", "col", "comdr", "commr",
        "cpl", "gen", "kapt", "kol", "lt", "maj", "pvt", "serg",
        "sgt",

        # Political/Administrative (Common in Western bureaucracy)
        "amb", "asst", "det", "gov", "mgr", "min", "msgr",
        "pres", "rep", "sec", "sen", "surg",
    }

    DOTTED_GEOPOL_ABBRVS = {
        # North Atlantic / Western Europe
        "U.S", "U.S.A", "U.K", "E.U",

        # Multilateral / Intergovernmental
        "U.N", "U.S.S.R",

        # Asia / Middle East
        "U.A.E", "P.R.C", "R.O.K",

        # Major International Organizations
        "N.A.T.O", "U.N.E.S.C.O", "W.H.O", "I.M.F", "W.T.O",
        "O.P.E.C", "F.A.O", "I.A.E.A", "W.B", "N.A.S.A",

        # Regional Organizations
        "A.U", "O.A.S", "A.S.E.A.N",

        # Other sovereign states
        "D.P.R.K", "R.O.C", "R.S.A", "D.R.C",
    }

    CORP_ENTITY_ABBRVS = {
        "assoc", "mfg", "inc", "corp", "ltd", "ltda", "co",
    }

    REFERENCE_ABBRVS = {
        # Publishing / Documents / Manuscripts
        "app", "apps", "cf", "cod", "diag", "ext", "fig",
        "figs", "fol", "illus", "l", "ll", "ms", "mss", "p",
        "pag", "pp", "pt", "pts", "ref", "refs", "tab", "tbl",
        "tbls", "v", "vol", "vols",

        # Section / Structure
        "ann", "art", "arts", "cap", "cl", "cls", "col", "cit",
        "cols", "para", "paras", "quaest", "sec", "sect",
        "secs", "subsec",

        # Legal / Numbering / Cross References
        "a.c", "a.d", "a.u.c", "b.c", "lc", "n", "nn", "nr",
        "no", "nos", "n°", "n.º", "qv", "reg", "regs",

        # Scientific / Technical
        "approx", "deg", "diam", "eq", "eqn", "eqs",
        "est", "ex", "exs", "lat", "long", "max", "min",

        # Commerce / Measurements
        "alt", "fam", "fax", "ord", "qty", "std", "tel", "wt",

        # Academic
        "et al", "s", "univ",
    }

    SECTION_MARKERS = {
        "Part", "Parte", "Section", "Subsection", "Article",
        "Module", "Division", "Usage", "Unit", "Volume",
        "Preface", "Introduction",
    }

    DATE_ABBRVS = {
        # Months
        "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep",
        "sept", "oct", "nov", "dec", "déc",

        # Day
        "mon", "tue", "wed", "thu", "thurs", "thur", "fri",
        "sat", "sun", "lun", "dom",
    }

    INLINE_ONLY_ABBRVS = {
        # Bridge/connectors
        "a.k.a", "ca", "cf", "e.g", "eg", "i.c", "i.e", "i.q",
        "ibid", "ie", "sc", "v", "viz", "vs",

        # Notes & postscript markers
        "n.b", "p.s", "p.p.s", "sci", "scill", "s.vloc",

        # Address elements
        "ave", "blv", "blvd", "ct", "jct", "ln", "pen", "pl",
        "rd", "riv", "rt", "rte", "sq", "st", "wy",

        # Others
        "approx", "intl", "mt",
    }

    NAMES_WITH_EXCLAMATION = {
        # Tech, Corporate Entities, & Major Consumer Brands
        "Boost", "Chips Ahoy", "FreshDirect",
        "I Can't Believe It's Not Butter", "JOOP", "Kahoot",
        "Pop", "Walla", "Yahoo", "Yum",

        # Gaming, Media, Animation, & Entertainment
        "Airplane", "bam", "Fun Radio", "go", "Hailey's On It",
        "Jeopardy", "Mamma Mia", "Oklahoma", "Oliver", "Osu",
        "Shindig", "VSPO", "wham",

        # Geopolitical Quirks / Municipalities
        "Westward Ho", "Saint-Louis-du-Ha", "Baie-des-Ha", "Ha",

        # Public Figures, Politics, & Manufacturing Brands
        "Jeb", "Éxito", "Hey Man", "Basta", "Elliot S",

        # Foods, Snacks & Beverages
        "Crunch", "Banga",
    }

    COMMON_SENT_STARTERS = set()
    POST_QUOTATIVE_PARTICLES = set()
    REPORTING_WORDS = set()

    # https://regex101.com/r/tI9Cmg/5
    DOT_LIKE_PATTERN = r"[.．။।॥·•∙⋅]"
    VERTICAL_LIST_START_FINDER = re2.compile(rf"""
        (?<=^\s*
            (?:
                (?:
                    \p{{L}}\p{{N}}{{0,2}}|
                    \p{{N}}{{1,4}}
                )
                (?:{DOT_LIKE_PATTERN}|\))
            ){{1,3}}
        )
        (?=\s)
        """, re.X | re.M
    )

    # https://regex101.com/r/JYdWZw/8
    QUOTE_AND_PAREN_FINDER = re2.compile(
        r"""
        # Quoted text with quotations or dashes
        "(?:[^"]*)"|(?<=\s)'(?:[^']*)'|
        [\p{Pi}»‚„].+?[\p{Pf}«‘“]|
        —[^—]*[,.!?]\s*—|

        # Parenthesized text
        \p{Ps}[^\p{Pe}]*\p{Pe}
        """,
        re2.X,
    )

    # https://regex101.com/r/0P9f2V/3
    TOC_LEADER_FINDER = re.compile(r".\s*\.[\s\.]{3,}\d")

    # https://regex101.com/r/ZOZlLb/3/substitution
    NEWLINE_INSIDE_SENTENCE_FINDER = re2.compile(r"(?<=[,:;)\w\s])\n(?=(\p{Ll}|[(>]))")

    _REGEX_CACHED = False
    # fmt: on
    def __init__(self):
        """Initialize rule instance with lazy-compiled regex patterns.

        Patterns are compiled once per class and cached via ``_REGEX_CACHED``.
        Subclasses can override data constants (abbreviation sets, terminators, etc.)
        and the classmethod ``_compile_regex_dynamically`` will pick them up.
        """
        if not type(self).__dict__.get("_REGEX_CACHED", False):
            self._compile_regex_dynamically()
            type(self)._REGEX_CACHED = True

    @classmethod
    def _compile_regex_dynamically(cls):
        """Compile language-specific regex patterns."""
        cls.TERMINATORS_PATTERN = f"[{''.join(cls.TERMINATORS)}]"
        cls.DOTS_PATTERN = r"[.．]"
        cls.TITLE_ABBRVS_PATTERN = build_optimized_pattern(cls.TITLE_ABBRVS)
        cls.DOTTED_GEOPOL_ABBRVS_PATTERN = build_optimized_pattern(cls.DOTTED_GEOPOL_ABBRVS)
        cls.COMMON_STARTERS_PATTERN = build_optimized_pattern(cls.COMMON_SENT_STARTERS)

        # https://regex101.com/r/qBSyU5/19
        # Handle flattened lists due to messy OCR.
        cls.HORIZONTAL_LIST_FINDER = re2.compile(
            rf"""
            # Must preceded by string start or word boundary
            # while skipping initialisms
            (?:^|(?<![A-Z](?:\.|\w+))\s+)
            (?:[•◦]\s+)?   # Optional bullet point (e.g., • 9.)
            (?:
                [-*+]|      #  Markdown style list

                # Numbered/alphabetical list
                (?:\d{{1,2}}|[a-eA-Eα-εΑ-Εа-еА-Е])
                (?:{cls.DOT_LIKE_PATTERN}|\)){{1,2}}
            )

            # Must be followed by whitespace
            # Numeric markers only require whitespace
            # Alphabetic markers must not be name initials (e.g. "A. B. Smith")
            (?:
                (?<=\d\.)(?=\s)|(?=\s+(?!\p{{LU}}\.))
            )
            """, re2.X,
        )

        # https://regex101.com/r/VMzYsx/10
        cls.CANDIDATE_BOUNDARY_FINDER = re2.compile(
            rf"""
            (?:
                # Newline not followed by another newline
                 (?<=\n)(?!\n)|

                # Split if left token is a unicase letter (Always)
                (?<=\p{{Lo}}\s*{cls.TERMINATORS_PATTERN})|

                # Split after any terminators followed by a a newline,
                # common sentence starter, Space+Upper or unicase letter
                (?<={cls.TERMINATORS_PATTERN}(?!\s*\p{{Emoji_Presentation}}))
                (?=
                    \s*[\n\p{{Lo}}]|
                    \s+(?:[^\p{{Ll}}&]|
                    \s+(?<!\.\.)(?i:{cls.COMMON_STARTERS_PATTERN})\b)
               )|

               # Emoji after terminator + uppercase, or emoji + common starter
               (?<={cls.TERMINATORS_PATTERN}\s*\p{{Emoji_Presentation}}+)|
               (?<=\s+\p{{Emoji_Presentation}})(?=\s*(?:{cls.COMMON_STARTERS_PATTERN})\b)|

               # Split at transition between Latin letters separate by alien
               (?<=[\p{{LU}}\p{{Ll}}][。！？।])(?=[\p{{Lu}}])
            )

            # Not followed by another terminators (clusters)
            (?!\n|\s*+{cls.TERMINATORS_PATTERN})
            """, re2.X,
        )

        # fmt: off
        # Faster than one big regex
        # https://regex101.com/r/svyCoU/21
        cls.MID_SENTENCE_FINDER_LST = [
            # Title abbrv or initialisms (e.g., Dr. Paul)
            re.compile(rf"\b(?i:{cls.TITLE_ABBRVS_PATTERN}){cls.DOTS_PATTERN}"),

            # Abbrv that NEVER ends a sentence
            re.compile(
               rf"\b(?i:{build_optimized_pattern(cls.INLINE_ONLY_ABBRVS)}){cls.DOTS_PATTERN}"
            ),

            # References abbrv + number/letter/bracket (e.g., p. 55, app. A, et al. [2004])
            re2.compile(rf"""
                \b(?i:{build_optimized_pattern(cls.REFERENCE_ABBRVS)}){cls.DOTS_PATTERN}
                (?=\s+(?:\(|\[|\p{{Lu}}\b|\p{{N}}|[IVXLCDM]+))
                """, re2.X
            ),

            # Date abbrv followed by a number
            re2.compile(
                rf"\b(?i:{build_optimized_pattern(cls.DATE_ABBRVS)}){cls.DOTS_PATTERN}(?=\s+\p{{N}})"
            ),

            # A dot followed by an superscript indicator (e.g. n.º, ​1.º)
            re.compile(r"\.(?=[ºª])"),

            # Initialism/Acronyms/Exclamations words (e.g., Yahoo!, A.B. Holding)
            # excluding coordinate directions or geopolitical ones not followed
            # by a common starters
            re2.compile(rf"""
                (?:
                    (?<=\.)\p{{Lu}}|
                    (?<=\s)\p{{Lu}}(?<![\d°]\s+[NSWE])|
                    \b\p{{Lo}}
                )\.
                (?<!(?i:{cls.DOTTED_GEOPOL_ABBRVS_PATTERN}|[pa]\.m){cls.DOTS_PATTERN})
                (?!\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
                """, re2.X
            ),
            re.compile(rf"""
                (?:(?i:
                    \b{build_optimized_pattern(cls.CORP_ENTITY_ABBRVS)}\.|
                    {build_optimized_pattern(cls.NAMES_WITH_EXCLAMATION)}[! ！‼]
                ))
                (?!\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
               """, re.X
            ),

            # Structural headings (e.g., "Chapter 1. The Beginning.")
            # and markdown headers (e.g., "### 1. The Regex Breakdown").
            re.compile(rf"""
                (?:
                    ^\s*\#{{1,6}}\s*|
                    \b(?:{build_optimized_pattern(cls.SECTION_MARKERS)})\s+
                )
                (?:[\dIVXLCDM]+{cls.DOTS_PATTERN}){{1,3}}
                """, re.M | re.X
            )
        ]

        # https://regex101.com/r/EGkRU8/7
        cls.QUOTE_AND_PAREN_END_FINDER = re2.compile(
            rf"""
            (?<=
                {cls.TERMINATORS_PATTERN}   # A terminator
                (?:'\s|"|\s*[»‘”“\p{{Pf}}\p{{Pe}}])     # Closing quotes/parens
            )
            (?!  # NOT followed by any continuation markers, punctuation, or space+lowercase
                \s*[\p{{Po}}\p{{Ll}}\p{{Pe}}]|
                {build_optimized_pattern(cls.POST_QUOTATIVE_PARTICLES | cls.REPORTING_WORDS)}
            )
            """,
            re2.X,
        )

    # fmt: on
    def _remove_quote_and_paren_spans(
        self,
        sentence_boundaries: set[int],
        text: str,
        preserve_quote_and_paren: bool,
    ) -> None:
        """Remove boundaries inside quoted/parenthesised spans."""
        if preserve_quote_and_paren:
            # Ignore first pos to preserve splits before opening quote/paren,
            # especially for non-whitespace languages
            inner_range = {
                pos for m in self.QUOTE_AND_PAREN_FINDER.finditer(text)
                for pos in range(m.start() + 1, m.end())
            }
            sentence_boundaries.difference_update(inner_range)

            if inner_range:
                sentence_boundaries.update(
                    m.end() for m in self.QUOTE_AND_PAREN_END_FINDER.finditer(text)
                    if m.end() not in inner_range
                )

    def _remove_toc_spans(
        self, sentence_boundaries: set[int], text: str
    ) -> None:
        """Remove boundaries inside TOC leader runs."""
        if "..." in text:
            for m in self.TOC_LEADER_FINDER.finditer(text):
                sentence_boundaries.difference_update(range(*m.span()))

    def _adjust_list_boundaries(self, sentence_boundaries: set[int], text: str) -> None:
        """Remove and re-align boundaries around list markers."""
        horiz_matches = list(self.HORIZONTAL_LIST_FINDER.finditer(text))

        # Quick contextual heuristic
        is_flattened_list = (
            # A flattened list must contain at least two horizontal markers
            len(horiz_matches) >= 2
            and (
                # List is introduced by a colon
                # or starts directly at the beginning of the text
                ":" in text
                or text[horiz_matches[0].start()] == text.lstrip()[0]
            )

            # At least one pair of list markers is close enough to belong
            # to the same flattened list
            and any(
                4 < b.start() - a.end() < 40
                for a, b in pairwise(horiz_matches)
            )
        )

        if is_flattened_list:
            sentence_boundaries.difference_update(m.end() for m in horiz_matches)

            # Shift boundaries back (1.\)| => |1.\), a. | => |a. ) to correctly
            # terminate the preceding sentence before flattened horizontal list.
            sentence_boundaries.update(m.start() + 1 for m in horiz_matches if m.start())

        sentence_boundaries.difference_update(
            m.end() for m in self.VERTICAL_LIST_START_FINDER.finditer(text)
        )

    def post_process_boundaries(
        self, sentence_boundaries: set[int], text: str
    ) -> None:
        """Hook for language-specific boundary filtering.

        Override in subclasses to remove false-positive boundaries that
        the regex passes cannot catch. Mutate ``sentence_boundaries`` in
        place; do not touch any other engine state.
        """

    def apply(
        self,
        text: str,
        preserve_quote_and_paren: bool,
    ) -> list[int]:
        """Detect sentence boundaries in *text*.

        Two-pass algorithm:
        1. Collect boundary candidates from punctuation positions.
        2. Remove false alarms (mid-sentence abbreviations, ellipsis,
           quote/paren spans, list markers).

        Args:
            text: A string to find sentence boundaries in.
            preserve_quote_and_paren: If ``True``, suppress boundaries
               inside quote and parenthesis spans.

        Returns:
            Sorted list of character offsets at which sentences end.
        """
        if not text or text.isspace():
            return [len(text)]

        text = self.NEWLINE_INSIDE_SENTENCE_FINDER.sub(" ", text)
        sentence_boundaries = {
            m.end() for m in self.CANDIDATE_BOUNDARY_FINDER.finditer(text)
        }

        # -- Remove false alarms --
        self._adjust_list_boundaries(sentence_boundaries, text)
        sentence_boundaries.difference_update(
            m.end() for pat in self.MID_SENTENCE_FINDER_LST
            for m in pat.finditer(text)
        )
        self.post_process_boundaries(sentence_boundaries, text)
        self._remove_quote_and_paren_spans(
            sentence_boundaries, text, preserve_quote_and_paren
        )
        self._remove_toc_spans(sentence_boundaries, text)

        sentence_boundaries.update({0, len(text)})
        return sorted(sentence_boundaries)
