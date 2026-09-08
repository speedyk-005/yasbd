from yasbd.rules.nl import NlRules


# fmt: off
class AfRules(NlRules):

    TITLE_ABBRVS = NlRules.TITLE_ABBRVS | {
        "adv", "ds", "at", "mej", "me", "mev",
    }

    DOTTED_GEOPOL_ABBRVS = NlRules.DOTTED_GEOPOL_ABBRVS | {
        "V.S.A", "R.S.A", "S.A"
    }

    REFERENCE_ABBRVS = NlRules.REFERENCE_ABBRVS | {
        # Bibliographical, Document, and Page References
        "a.w", "bg", "bl", "byl", "hers", "red", "samest",
        "uitg",

        # Unique Afrikaans legal and cross-referencing markers
        "kol", "vg", "verg", "hfst"
    }

    SECTION_MARKERS = NlRules.SECTION_MARKERS | {
        "Hoofstuk", "Bylae", "Opsomming", "Gevolgtrekking"
    }

    INLINE_ONLY_ABBRVS = NlRules.INLINE_ONLY_ABBRVS | {
        "d.w.s", "o.a", "m.a.w", "m.m.v", "i.v.m", "n.v.t",
        "v.C", "n.C", "v.m", "n.m",
    }

    DATE_ABBRVS = NlRules.DATE_ABBRVS | {
        # 'dec' becomes 'des' for Desember;
        # 'vry' ensures safe Vrydag tracking
        "des", "vry"
    }

    COMMON_SENT_STARTERS = NlRules.COMMON_SENT_STARTERS | {
        # Unique Afrikaans Articles & Pronouns
        "'n", "Daardie", "Die", "Dié", "Ek", "Hierdie", "Hulle",
        "Jy", "Mens", "Ons", "Sulke", "Sy",

        # Unique Afrikaans Question/Connector Anchors
        "Boonop", "Daarbenewens", "Daarteenoor", "Gevolglik",
        "Inteendeel", "Watter",

        # Sequence/Time Variations
        "Eerstens", "Tweedens", "Gister", "Môre", "Dikwels",
    }

    DATE_WORDS = {
        # Months
        "april", "augustus", "desember", "februarie",
        "januarie", "julie", "junie", "maart", "mei",
        "november", "oktober", "september",

        # Days
        "maandag", "dinsdag", "woensdag", "donderdag", "vrydag",
        "saterdag", "sondag",
     }

# fmt: on
