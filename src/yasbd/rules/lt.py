import regex as re

from yasbd.rules.base import Rules


# fmt: off
class LtRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Respectful & Social Address
        "p", "pon", "ponia", "ponios", "panelė", "pan", "gerb", "šv",

        # Academic & Professional
        "doc", "akad", "habil", "inž", "arch", "gyd", "teis",

        # Military, Clergy & Clerical Titles
        "gen", "plk", "mjr", "kpt", "ltn", "kun", "prel", "vysk",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "L.R", "J.A.V", "E.S", "U.R.M", "V.R.M", "S.A.D.M",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographical & Citation Indicators
        # (Typically precede numbers/values)
        "t", "l", "psl", "str", "skyr", "pav", "lent", "sk",
        "red", "leid", "žr", "plg", "nr",
        "t.t", "ir kt",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "pvz", "egz", "t.y", "š.m", "b.m", "g", "pr",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Skyrius", "Poskyris", "Priedas", "Lentelė",
        "Paveikslas", "Įvadas", "Išvados"
    }

    DATE_ABBRVS = {
        # Months
        "saus", "vas", "kov", "bal", "geg", "birž",
        "liep", "rugp", "rugs", "spal", "lapkr", "gruod",

        # Days (Used in running prose)
        "pirm", "antr", "treč", "ketv", "penkt", "šešt", "sekm",
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "Aš", "Ji", "Jie", "Jis", "Jos", "Jūs", "Kas", "Koks",
        "Mes", "Tai", "Tu", "Ši", "Šis",

        # Logical Connectors & Adverbs
        "Antra", "Be", "Beje", "Bet", "Dabar", "Jeigu",
        "Kadangi", "Kai", "Nors", "Pirmiausia", "Tada",
        "Tačiau", "Todėl", "Vėliau", "Štai",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to handle single letter abbrvs."""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.append(
            re.compile(
                r"""
                # A lowercase letter + dot  followed by any char + dot
                (?<=[a-ząčęėįšųūž]\.)(?=\s+.\.)|

                # A number or any char + dot
                # followed by space + lowercase letter + dot
                (?<=(?:\d|.\.)\s+[a-ząčęėįšųūž]\.)
                """, re.X
            )
        )
