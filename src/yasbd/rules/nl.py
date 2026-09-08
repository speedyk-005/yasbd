from yasbd.rules.base import Rules
from yasbd.rules.de import DeRules


# fmt: off
class NlRules(DeRules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic and Professional Titles
        "drs", "ir", "lic", "bc", "bacc", "not",

        # Bachelor / Master Degrees
        "ba", "ma", "bsc", "msc",

        # Social Honorifics and Clergy
        "dhr", "mnr", "mev", "mevr", "mw", "ds", "arts",

        # Military Ranks
        "lt-gen", "maj-gen", "bgen", "kol", "lt-kol",
        "kapt", "lt", "elnt", "tlnt", "korp", "adj",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "A.U", "E.G", "V.S", "N.V", "B.V", "V.K",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Bibliographical, Page, and Document References
        "art", "afb", "hfdst", "blz", "nr", "par", "reg",
        "bijl", "ca", "cf", "ed", "vert", "id",

        # Legal, Corporate, and Formal Citation Markers
        "b.w", "gem", "coll", "hr", "c.q", "ov", "vp",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Afdeling", "Artikel", "Lid", "Paragraaf", "Bijlage",
        "Hoofdstuk", "Deel", "Inleiding", "Voorwoord",
        "Samenvatting", "Conclusie", "Register",
    }

    INLINE_ONLY_ABBRVS = DeRules.INLINE_ONLY_ABBRVS | {
        "bijv", "ca", "d.w.z", "e.v.t.l", "excl", "incl",
        "z.g.n",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "jan", "feb", "mrt", "apr", "jun", "jul",
        "aug", "sep", "okt", "nov", "dec",

        # Days
        "ma", "di", "wo", "do", "vr", "za", "zo",
    }

    NAMES_WITH_EXCLAMATION = Rules.NAMES_WITH_EXCLAMATION | {
        "Nu", "Doe mee", "Tikkie", "Vergeet je tandenborstel niet"
    }

    COMMON_SENT_STARTERS = {
        # Articles
        "De", "Het", "Een",

        # Pronouns
        "Dat", "Deze", "Die", "Dit", "Er", "Gene", "Hij", "Ik",
        "Je", "Jij", "Jullie", "Men", "U", "We", "Wij", "Ze",
        "Zij",

        # Question words
        "Hoe", "Waar", "Waarom", "Wanneer", "Wat", "Welk",
        "Welke", "Wie", "Wiens", "Wier",

        # Adverbs and Connectors
        "Aldus", "Anderzijds", "Bijgevolg", "Bovendien",
        "Daardoor", "Daarentegen", "Daarnaast", "Daarom",
        "Desalniettemin", "Desondanks", "Dus", "Echter",
        "Enerzijds", "Hoewel", "Immers", "Inmiddels",
        "Intussen", "Kortom", "Namelijk", "Niettemin",
        "Ondertussen", "Overigens", "Tenslotte", "Tevens",
        "Toch", "Trouwens", "Uiteindelijk", "Verder",
        "Vervolgens", "Voorlopig", "Zodoende",

        # Time / Sequence Anchors
        "Altijd", "Daarna", "Eerst", "Gisteren", "Later",
        "Morgen", "Nooit", "Nu", "Soms", "Toen", "Vaak",
        "Vandaag", "Vroeger",
    }

    STREET_ABBRVS = {
        "geb", "hbf", "ln", "pl", "plts", "rd", "st", "str",
        "wgh",
    }
    INLINE_ONLY_ABBRVS |= STREET_ABBRVS

    DATE_WORDS = {
        # Months
        "april", "augustus", "december", "februari", "januari",
        "juli", "juni", "maart", "mei", "november", "oktober",
        "september",

        # Days
        "maandag", "dinsdag", "woensdag", "donderdag", "vrijdag",
        "zaterdag", "zondag",
     }

    @classmethod
    def _compile_regex_dynamically(cls):
        """Remove the German ordinal guard inherited from DeRules."""
        super()._compile_regex_dynamically()
        cls.MID_SENTENCE_FINDER_LST = [
            pattern
            for pattern in cls.MID_SENTENCE_FINDER_LST
            if pattern.pattern != r"\s\d{1,3}\."
        ]

# fmt: on
