import regex as re

from yasbd.rules.base import Rules


# fmt: off
class HiRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Academic & Professional
        "डॉ", "प्रो", "एड", "इंजी", "प्रि", "प्रा", "वै", "वैद्य",

        # Military, Legal & Administrative
        "ले", "कैप्ट", "न्या", "सचि", "अधि", "निदे", "सां", "वि", "मु", "मं",

        # Religious & Classical Honorifics
        "पं", "स्वामी", "स्वा", "सं", "आ", "पू",

        # Social & Formal Address
        "श्रीम", "कु", "सु", "मा"
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        # Native Indian States and Administrative Bodies
        "उ.प्र", "म.प्र", "हि.प्र", "अ.प्र", "सं.रा", "सी.बी.आई", "सी.आई.डी",

        # Transliterated Global and Regional Organizations
        "यू.एस", "यू.एस.ए", "यू.के", "ई.यू", "यू.एस.एस.आर", "यू.ए.ई", "पी.आर.सी",
        "आर.ओ.के", "डी.पी.आर.के", "आर.ओ.सी", "आर.एस.ए", "डी.आर.सी",
        "यू.एन", "डब्ल्यू.एच.ओ", "आई.एम.एफ", "डब्ल्यू.टी.ओ", "एफ.ए.ओ",
        "आई.ए.ई.ए", "डब्ल्यू.बी", "ए.यू", "ओ.ए.एस",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        # Publishing, Citations, Layout, and Document Structures
        "पृ", "चि", "भा", "अनु", "अध", "पैरा", "क्र", "टि", "कृ",
        "अध्या", "परि", "पु", "पन्", "स्त", "सा", "संपा", "अनुवा", "प्रका",
        "सार", "विव", "ता", "तुल", "सू", "सूच",

        # Legal, Structural, and Cross-References
        "ध", "धारा", "उ.ध", "नि", "नियम", "आदे", "या", "याचि",
        "प्रक", "मुक", "ब",
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "उदा", "बनाम", "वि.द्र", "पु.श्च", "स्था", "चौ", "जि"
    }

    COMMON_SENT_STARTERS = {
        # Pronouns
        "आप", "इन्होंने", "उन्होंने", "मैं", "यह", "ये", "वह",
        "वे", "हम",

        # Question words
        "कौन", "क्या", "कहाँ", "कब", "क्यों", "कैसे",

        # Adverbs
        "अंततः", "अतः", "अब", "अभी", "आज", "इसलिए", "किंतु",
        "तदनुसार", "तब", "परंतु", "फिर", "मगर", "लेकिन",
        "वर्तमान", "शायद", "हालांकि",
    }

    REPORTING_WORDS = {
        # Pure Verb Roots (Actions stripped of tense/gender suffixes)
        "कह", "बोल", "पूछ", "बला", "बता", "लिख", "समझ", "समझा",
        "चिल्ला", "पुकार", "फुसफुसा", "दोहरा", "दुहरा", "सुझा",

        # Nominal / Adjectival Components
        # (Unchanged roots of compound verbs)
        "उत्तर", "जवाब", "आदेश", "आज्ञा", "सुझाव",
        "घोषणा", "ऐलान", "टिप्पणी", "स्वीकार", "दावा"
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
