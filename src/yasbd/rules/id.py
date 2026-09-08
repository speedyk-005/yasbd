from yasbd.rules.base import Rules


# fmt: off
class IdRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic, Professional, and Noble Honorifics
        "Ir", "Drs", "Dra", "Pdt", "H", "Hj",
        "Sdr", "Sdri", "Bpk", "Ibu",

        # Formal Correspondence Openings & Name Truncations
        "Yth", "Moh",

        # Medical and Religious Prenominal Titles
        "dr", "drg", "drh", "KH", "Ust", "Rm", "Ps",

        # Traditional Javanese Royal Prenominal Titles
        "R", "RA", "RM", "RB", "RP", "RAy", "Rr", "RNgt", "RNg",

        # Administrative & Bureaucratic Acting Titles
        "Pjs", "Plt",
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "R.I",
    }

    CORP_ENTITY_ABBRVS = Rules.CORP_ENTITY_ABBRVS | {
        "pte", "bhd", "sdn", "pt", "cv",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "hlm", "hal", "bab", "jil", "lamp", "ttd", "stt",
        "cet", "terj", "dok", "pas", "pk", "tgl",
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Bab", "Pasal", "Ayat", "Bagian", "Subbagian",
        "Lampiran", "Paragraf", "Sub-bab",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        # Administrative & Postal Connectors
        "a.n", "u.b", "d.a",

        # Structural & Positional Inline Connectors
        "a.l", "a.s", "s.d", "u.p", "t.t", "d.h", "y.b.m",

        # Street/Address Abbreviations
        "Kp", "Jl", "Gg",
    }

    DATE_ABBRVS = Rules.DATE_ABBRVS | {
        # Months
        "Agu", "Ags", "Des",

        # Days
        "Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min",
    }

    COMMON_SENT_STARTERS = Rules.COMMON_SENT_STARTERS | {
        # Articles
        # (Indonesian lacks true articles; uses structural specifiers)
        "Sang", "Si", "Para", "Kaum", "Para-",

        # Pronouns
        "Saya", "Aku", "Kamu", "Dia", "Ia", "Mereka", "Kami", "Kita",
        "Ini", "Itu",

        # Adverbs & Logical Connectors
        "Tetapi", "Namun", "Oleh karena itu", "Jadi", "Kemudian", "Lalu",
        "Selain itu", "Bahkan", "Meskipun", "Walaupun", "Akhirnya",
        "Pertama", "Kedua", "Ketiga",

        # Question words
        "Siapa", "Apa", "Kapan", "Di mana", "Mengapa", "Bagaimana", "Berapa",
        "Yang mana",

        # Other common starters
        "Apakah", "Juta",
    }

# fmt: on
