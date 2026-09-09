import re

from yasbd.rules.base import Rules
from yasbd.utils.trie import build_optimized_pattern


# fmt: off
class DeRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        "dr.h.c", "di", "dipl", "dipl.-Ing", "mag", "ba", "ma", "bsc", "msc",
        "h", "hr", "hnr", "hll", "frl", "min", "pfr", "ass", "\u200bprojektass",

        # Military Ranks
        "gen", "lt", "maj", "oberstlt", "kpt", "kptlt", "fkpt", "kkpt",
        "stabsgefr", "uoff", "stabsfw",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "D.H", "E.V", "G.M.B.H", "I.G", "A.D", "K.U.K"
    }

    CORP_ENTITY_ABBRVS = Rules.CORP_ENTITY_ABBRVS | {
        "e.V.", "KGaA", "A/S", "A/B",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographical and Document References
        "abb", "anm", "bd", "bzw", "cap", "ed", "hrsg", "kap", "nr",
        "s", "sp", "std", "u.a", "u.ä", "vgl", "z.t", "f", "ff", "o.ä",
        "gl", "a.a.o", "s.o", "s.u", "s.a",

        # Legal and Formal References
        "abs", "art", "az", "lit", "m.w.n", "rspr",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Abschnitt", "Anhang", "Artikel", "Band", "Beispiel",
        "Einleitung", "Exposé", "Kapitel", "Paragraf", "Präambel",
        "Schlusswort", "Seite", "Teil", "Vorwort", "Zusammenfassung",
    }

    # Multi-part abbreviations with spaces (like "d. h.", "z. B.", "i. d. R.")
    # are removed from this literal set. They are caught dynamically later
    # in the pipeline by the cls.MID_SENTENCE_FINDER_LST regex rule.
    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Bridge / Logical connectors
        "bzw", "evtl", "ggf", "ggfs", "inkl", "sog",
        "zzgl", "bspw", "insb", "ca", "bsp",

        # Business/Commercial
        "fa", "Mio", "Mrd",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "mär", "okt", "dez",

        # Days
        "mo", "di", "mi", "do", "fr", "sa", "so",
    }

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "Mach mit", "Jetzt neu"
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "Der", "Die", "Das", "Ein", "Eine",

        # Pronouns
        "Ich", "Wir", "Du", "Ihr", "Er", "Sie", "Es", "Man",
        "Dieser", "Diese", "Dieses", "Jener", "Jene", "Jenes",

        # Question words
        "Wann", "Warum", "Was", "Welche", "Welcher", "Welches",
        "Wem", "Wen", "Wer", "Wessen", "Wie", "Wo",

        # Adverbs and Connectors
        "Allerdings", "Anfangs", "Ansonsten", "Außerdem",
        "Danach", "Dann", "Daraufhin", "Darum", "Darüberhinaus",
        "Denn", "Dennoch", "Derzeit", "Deshalb", "Drittens",
        "Ebenso", "Erstens", "Folglich", "Früher", "Inzwischen",
        "Jedoch", "Letzt", "Letzte", "Mittlerweile", "Nächst",
        "Nächste", "Schließlich", "Somit", "Später", "Zudem",
        "Zuletzt", "Zuvor", "Zweitens",

        # Other starters
        "Tun", "Tat", "Millionen", "Gestern", "Heute", "Morgen",
    }

    STREET_ABBRVS = {
        "str", "pl", "weg", "hbf",
        "ring", "ufer", "damm", "geb"
    }
    INLINE_ONLY_ABBRVS |= STREET_ABBRVS

    DATE_WORDS = {
        # Months
        "april", "august", "dezember", "februar", "januar",
        "juli", "juni", "mai", "märz", "november", "oktober",
        "september",

        # Days
        "dienstag", "donnerstag", "freitag", "mittwoch",
        "montag", "samstag", "sonntag",
     }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle ellipsis, ord num and time"""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend([
            # Spaced three-dot ellipsis mid-thought (e.g., ". . . she didn't")
            # Consecutive dots "..." or "...." still create sentence boundaries.
            re.compile(r"(?<!\.)\.(?:\s\.){2}"),

            # Ordinal numbers
            # https://learngerman.dw.com/en/ordinal-numbers/l-57731450/gr-60885529
            re.compile(r"\s\d{1,3}\."),

            # Multi-part abbreviations with spaces (like "d. h.", "z. B.", "i. d. R.")
            re.compile(r"\b[a-zA-Z]\.(?!\s+\w{2,})"),

            # Number/Time abbreviations followed by a date token (e.g., 9 a.m. Monday)
            re.compile(rf"""
                (?:\d\.|(?:(?<=\d)|\b)(?i:[ap]\.m\.))
                (?=
                    \s+(?i:{build_optimized_pattern(cls.DATE_ABBRVS | cls.DATE_WORDS)})
                    (?:\.|\s|$)
                )
            """, re.X),
        ])

        # Street abbrv followed by a common starters
        cls.ENDING_STREET_ABBRVS_FINDER = re.compile(rf"""
            (?:\b(?i:{build_optimized_pattern(cls.STREET_ABBRVS)})\.)
            (?=\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
           """, re.X
        )

    def post_process_boundaries(
        self, sentence_boundaries: set[int], text: str
    ) -> None:
        sentence_boundaries.update(
            m.end() for m in self.ENDING_STREET_ABBRVS_FINDER.finditer(text)
        )
