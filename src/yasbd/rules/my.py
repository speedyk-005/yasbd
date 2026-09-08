import re

from yasbd.rules.base import Rules
from yasbd.utils.trie import build_optimized_pattern


# fmt: off
class MyRules(Rules):


    # Burmese uses the section mark '။' as the primary terminator.
    # Periods are dropped from the terminator set
    # since they typically denote digits or abbreviations.
    TERMINATORS = (Rules.TERMINATORS - {"."}) | {"။", "၏"}

    TITLE_ABBRVS = set()
    DOTTED_GEOPOL_ABBRVS = set()
    REFERENCE_ABBRVS = set()
    SECTION_MARKERS = set()
    DATE_ABBRVS = set()

    COMMON_SENT_STARTERS = {
        # Temporal / Sequential
        "ထို့နောက်", "ထို့ပြင်", "နောက်ဆုံး", "နောက်ပိုင်း",
        "ယခု", "ယခင်က", "မကြာခင်က", "လွန်ခဲ့တဲ့",
        "ထိုအချိန်က", "ထိုခေတ်က", "နောက်မှ", "နောက်ဆုံးတွင်",
        "ထိုနောက်",

        # Causal / Contrast
        "ထို့ကြောင့်", "ဒါကြောင့်", "မည်သို့ပင်ဆိုစေ",
        "သို့ပေမယ့်", "သို့ရာတွင်", "သို့သော်", "သို့သော်လည်း",
        "ဤသို့ဖြင့်",

        # Discourse framing
        "ချုပ်လိုက်ရရင်", "ခြုံငုံကြည့်လျှင်", "ဆိုလိုသည်မှာ",
        "နိဂုံးချုပ်အနေနဲ့", "နောက်ဆုံးအနေနဲ့", "ပထမဦးစွာ",
        "အကျဉ်းချုပ်အားဖြင့်", "အထူးသဖြင့်", "ဥပမာ",
        "ဥပမာအားဖြင့်",

        # Question words
        "ဘာ", "ဘယ်", "ဘယ်သူ", "ဘယ်ဟာ", "ဘယ်နေရာ",
        "ဘယ်လို", "ဘာကြောင့်", "ဘယ်အချိန်", "မည်သူ",
        "မည်သည့်", "မည်သို့", "ဘယ်ခါ", "ဘာဖြစ်လို့",
        "ဘယ်လောက်", "ဘယ်နှစ်", "ဘယ်နှစ်ခု",

        # Common pronouns / subjects (Formal + Informal)
        "ငါ", "ကျွန်တော်", "ကျွန်မ", "သူ", "သူမ",
        "သူတို့", "သင်", "မင်း", "ညည်း", "ငါတို့",
        "ကျွန်ုပ်တို့",
    }

    REPORTING_WORDS = {
        "ပြော", "ဆို", "မေး", "ဖြေ", "ရေး", "အော်", "တင်ပြ",
        "သတင်းပို့", "တိုင်ကြား", "လျှောက်", "ကြေညာ",
        "ရှင်းပြ", "ဖြေရှင်း", "ငြင်း", "သဘောတူ", "ဝန်ခံ",
        "မှတ်", "ကြွေးကြော်",
    }

    POST_QUOTATIVE_PARTICLES = {
        "ဟု", "လို့", "ဟူ၍",
    }

    DISCOURSE_FINAL_PARTICLES = {
        # Declarative (high-confidence  sentence endings)
        "ပါတယ်", "ပါသည်",

        # Question sentence-final markers
        "လား", "မလား", "ပါသလား", "သလား",

        # Formal written completions
        "ခဲ့ပါသည်",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation"""
        super()._compile_regex_dynamically()

        cls.FINAL_PARTICLES_FINDER = re.compile(
            rf"{build_optimized_pattern(cls.DISCOURSE_FINAL_PARTICLES)}(?!\s*[.?!;:။၏၊])"
        )
        cls.DOUBLE_COMMA_FINDER = re.compile("၊၊")

    def post_process_boundaries(
        self, sentence_boundaries: set[int], text: str
    ) -> None:
        sentence_boundaries.update(
            m.end()
            for finder in (self.FINAL_PARTICLES_FINDER, self.DOUBLE_COMMA_FINDER)
            for m in finder.finditer(text)
        )
