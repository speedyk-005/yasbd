import regex as re

from yasbd.rules.base import Rules


# fmt: off
class MlRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        "ഡോ", "പ്രൊ", "അഡ്വ", "എംഎൽഎ", "എംപി",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        # Indian States
        "ഉ.പ്ര", "മ.പ്ര", "ഹി.പ്ര",

        # Organizations
        "സി.ബി.ഐ", "സി.ഐ.ഡി",

        # International
        "യു.എൻ", "യു.എസ്", "യു.എസ്.എ", "യു.കെ",
        "യു.എ.ഇ", "ഇ.യു", "ഡബ്ല്യു.എച്ച്.ഒ", "ഐ.എം.എഫ്",
        "ഡബ്ല്യു.ടി.ഒ", "എഫ്.എ.ഒ", "ഐ.എ.ഇ.എ"
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "പൃ", "സമ്പാ", "അധ്യാ", "വിഭാ", "പരി",
        "പു.കു", "വി.കാ",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "ഉദാ",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "ജനു", "ഫെബ്രു", "മാർ", "ഏപ്രി",
        "മേയ്", "ജൂൺ", "ജൂലൈ",
        "ഓഗ", "സെപ്", "ഒക്ടോ", "നവം", "ഡിസം",

        # Days
        "തിങ്ക", "ചൊവ്വ", "ബുധ", "വ്യാ", "വെള്ളി", "ശനി", "ഞാ"
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "ഞാൻ", "നീ", "അവൻ", "അവൾ", "അത്", "അവർ",
        "നാം", "ഞങ്ങൾ", "നിങ്ങൾ",

        # Interrogatives
        "എന്ത്", "എവിടെ", "എപ്പോൾ", "എങ്ങനെ", "ആര്",
        "ഏത്", "എന്തുകൊണ്ട്"
    }

    REPORTING_WORDS = {
        # Speech / communication verb stems (tense-neutral)
        "പറ", "ചോദി", "എഴുത", "വിളി",
        "വിശദീകരി", "പ്രഖ്യാപി", "അറിയി",
        "അഭിപ്രായപ്പെട", "സമ്മതി", "നിരീക്ഷി",
        "ചൂണ്ടിക്കാട്ട", "കുറി", "അലറി", "മന്ത്രി", "ആക്രോശി",

        # Speech-related nominal stems (supporting signals)
        "മറുപടി", "ഉത്തരം", "അഭിപ്രായ", "പ്രസ്താവന",
        "നിർദേശ", "അവകാശവാദ"
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation to fix ellipsis, geopol and dot+space splits"""
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend([
            # Ellipsis
            re.compile(r"\.{3,}"),

            # Terminators + no space = initialism/acronyms
            re.compile(r"\.(?!\s)"),

            # Geopolitical abbreviations
            re.compile(rf"(?<={cls.DOTTED_GEOPOL_ABBRVS_PATTERN})\.")
        ])
