import io
import random
import re
import string

import pytest

from tests import ALL_TEST_DATA
from yasbd import (
    BoundaryDetector,
    HookError,
    InvalidInputError,
    ParagraphEOF,
    UnsupportedLanguageError,
)


@pytest.fixture(scope="module")
def en_detector():
    return BoundaryDetector(lang="en")


@pytest.mark.parametrize(
    "input_text",
    [
        "",
        "   ",
        "\n\n\n",
        pytest.param(io.StringIO(""), id="empty_stream"),
    ],
)
def test_segment_empty_input(input_text, en_detector):
    """test that empty or whitespace-only input produces no sentences."""
    assert list(en_detector.segment(input_text)) == []


@pytest.mark.parametrize(
    "lang,exc,msg",
    [
        (None, InvalidInputError, "'lang' is required"),
        ("", InvalidInputError, "'lang' is required"),
        ("xx", UnsupportedLanguageError, "doesn't fit any cutting profile"),
    ],
)
def test_invalid_lang(lang, exc, msg):
    with pytest.raises(exc, match=msg):
        BoundaryDetector(lang=lang)


def test_segment_different_input(en_detector):
    """test that string and stream input produce identical results."""
    text = "Hello world. How are you? I'm fine."

    result_str = list(en_detector.segment(text))
    result_stream = list(en_detector.segment(io.StringIO(text)))

    assert result_stream == result_str
    assert result_stream == ["Hello world.", "How are you?", "I'm fine."]


@pytest.mark.parametrize("lang,test_data", ALL_TEST_DATA.items())
def test_segment_multiple_langs(subtests, lang, test_data):
    """test that each language's test data passes."""
    seg = BoundaryDetector(lang=lang)
    for marked_text in test_data:
        # Extract the expected sentences by splitting on the marker
        expected = [sent.strip() for sent in marked_text.split("|")]

        # Reconstruct the clean original input text by removing the marker
        input_text = marked_text.replace("|", "")

        with subtests.test():
            result = list(seg.segment(input_text))
            assert result == expected, f"Input: {input_text}"


def test_segment_noisy_input(en_detector):
    """test that random noisy input does not crash the segmenter."""
    chars = (
        string.ascii_letters + string.digits + string.punctuation + "z.?! Dr. Mr. Inc. etc."
    )

    for _ in range(100):
        length = random.randint(1, 500)
        text = "".join(random.choices(chars, k=length))
        try:
            list(en_detector.segment(text))
        except Exception as e:
            raise AssertionError(f"Crash on random input (len={length}): {e}") from e


def test_detect_boundary_offsets(en_detector):
    """test that detect yields valid boundary offsets."""
    text = "Hello World. How are you?"

    result = list(en_detector.detect(text))
    assert result == [12, 25]
    assert all(isinstance(b, int) for b in result)
    assert result == sorted(result)


def test_detect_paragraph_eof_sentinel(en_detector):
    """test that detect yields ParagraphEOF between paragraphs in relative mode."""
    # Single paragraph = no sentinel
    result = list(en_detector.detect("Hello. World.", relative=True))
    assert result == [6, 13]

    # Empty paragraph = sentinel at start
    result = list(en_detector.detect("\n\nHello.", relative=True))
    assert result == [ParagraphEOF, 6]

    # Three paragraphs = two sentinels
    result = list(en_detector.detect("Hi.\n\nBye.\n\nOh.", relative=True))
    assert result == [3, ParagraphEOF, 4, ParagraphEOF, 3]

    # Non-relative = no sentinels,
    result = list(en_detector.detect("First.\n\nSecond.", relative=False))
    assert result == [6, 15]


def test_detect_leading_blank_offset(en_detector):
    """test that absolute offsets account for leading blank paragraphs."""
    # Leading blank lines must shift absolute offsets (fix for openmed adapter)
    result = list(en_detector.detect("\n\n\nOne. Two.\n\nThree."))
    assert result == [7, 12, 20]

    # Interior blank paragraphs counted too
    result = list(en_detector.detect("One.\n\n\n\nTwo."))
    assert result == [4, 12]

    # No blank lines: unchanged
    result = list(en_detector.detect("One. Two. Three."))
    assert result == [4, 9, 16]


def test_rule_cache_lru(en_detector):
    """test that rule objects are cached (max 5) and reused on lang switch."""
    # Same lang = same cached object
    r1 = en_detector._get_rule("en")
    r2 = en_detector._get_rule("en")
    assert r1 is r2, "same lang should return cached rule"

    # Different lang = different object
    r_fr = en_detector._get_rule("fr")
    assert r1 is not r_fr, "different lang should return different rule object"

    # Switch back = cached
    r3 = en_detector._get_rule("en")
    assert r1 is r3, "switching back to cached lang should reuse cached rule"

    # LRU eviction: load 5 more languages (cache capacity is 5)
    for lang in ["de", "es", "ht", "ar", "ja"]:
        en_detector._get_rule(lang)
    # 'en' was the first loaded, then pushed out by 5 newer entries
    r_en = en_detector._get_rule("en")
    assert r_en is not r1, "en should have been evicted after 6 other langs"
    assert type(r_en) is type(r1), "freshly loaded en rule should exist"  # type: ignore[unreachable]


# fmt: off
@pytest.mark.parametrize(
    "marked_text",
    [
        # Scientific units (fix for #33)
        "Each tick denotes an increase of 100 meV.| Each data point follows.",
        "The supply reached 10 kV.| Measurements continued.",
        "The frequency was 20 MHz.| The receiver locked.",

        # Day-month ambiguity (fix for #29)
        "The meeting is at 9 a.m. Monday.",
        "The event starts at 11a.m. Tue.",
        "The store opens at 8 p.m. December.",
        "The meeting is at 2 p.m.| Martin called.",
        "The meeting is at 10 a.m.| Monday's agenda was postponed.",

        # "&" separator (fix for #150)
        "Trying to get back to Com. & Adm. through the most direct path in the dark.",

        # Not a list (fix for #52)
        "I really want letter A.| I know that I asked you for the B.| I changed my mind.",
        "You are going to the store, and so am I.| We can go together.",

        # Bracketed references (fix for #34)
        "Yan et al. [2004] analysed SSH variations.| The study was comprehensive.",
        "Fig. [1] shows the architecture.| Figure 2 provides details.",
        "As shown in pp. [55-60], the results are significant.| This confirms our hypothesis.",
        "See sec. [2.1] for details.| The methodology is described there.",

        # Newlines (fix for #50)
        "The simplest way\nto get started is with pip.",
        "10 languages supported today\n|Target is 22+.",
        "> Somewhere, something incredible\n> is waiting to be known",

        # Dot followed by newline (fix for #205)
        "Hello world.\n|Next sentence.",

        # Emojis (fix for #73)
        "Nice work! 👍| Next step.",
        "The alternative is to put it before the full stop 👉.| So cool, right?",

        # Coordinate directions ambiguity (fix for #134)
        "Server A at 40.7128° N, 74.0060° W.| Server B at 34.0522° S, 118.2437° E.",
        "N. Scott Momaday is a writer.| He won the Pulitzer.",

        # Ordinary word + period should not be treated as vertical list marker
        "Note.| The file is ready.",

        # Multi-digit vertical list items
        "12. The first item.\n|13. The second item.",
        "    A12. The first item.\n|    B13. The second item.",

        # Flattened list items (fix for #208)
        "• 9. The first item.| • 10. The second item",
        "α· Πρώτο θέμα| β· Δεύτερο θέμα.",
        "The requirements are simple:| 1.) Python 3.12 environment.| 2. At least 8GB of RAM.",

        # Corporate and personal abbreviation boundaries (fix for #260)
        "Acme Inc. USA is expanding its engineering team this quarter.",
        "Beta Corp. North America leads this hiring initiative.",
        "Martin Luther King Jr. Day is a paid holiday at this company.",
        "John Doe Sr. VP of Engineering will be your hiring manager.",

        # CORP_ENTITY_ABBRVS must use word boundary (fix regression)
        "Kid!| Don't buy tobacco.| Alright!",

        # markdown headers with trailing numbers stay whole (fix for #305)
        "### 1. The Regex Breakdown\n|### 2. Metric Interpretation",
        "        ### 1. The Regex Breakdown\n|        ### 2. Metric Interpretation",
    ],
)
def test_universal_regression(en_detector, marked_text):
    """Test that fixed boundary issues aren't regressed"""
    expected = [sent.strip() for sent in marked_text.split("|")]
    input_text = marked_text.replace("|", "")

    result = list(en_detector.segment(input_text))
    assert result == expected, f"Input: {input_text}"
# fmt: on


def test_cyrillic_newline_inside_sentence():
    """Test that Cyrillic lowercase after a newline is sentence-internal (fix for #274)."""
    detector = BoundaryDetector(lang="ru")
    result = list(detector.segment("Это\nслово продолжается."))
    assert len(result) == 1
    assert result[0].replace("\n", " ") == "Это слово продолжается."


def test_post_processing_hook_supports_mutation():
    """test that a hook can remove and add boundaries in place."""

    def tweak(ctx):
        # Remove the boundary after "Hi." (join) and add one after "There" (split)
        ctx["boundaries"] = [pos for pos in ctx["boundaries"] if pos != 3] + [10]

    detector = BoundaryDetector(lang="en", hook=tweak)
    assert list(detector.segment("Hi. There world.")) == ["Hi. There", "world."]
    assert list(detector.detect("Hi. There world.")) == [10, 16]


def test_post_processing_hook_deduplicates_boundaries():
    """test that duplicate boundaries from a hook are removed."""

    def tweak(ctx):
        ctx["boundaries"] = [0, 5, 5, len(ctx["text"])]

    detector = BoundaryDetector(lang="en", hook=tweak)

    assert detector._run_hook("this is a test", [0, 14], 0) == [0, 5, 14]


@pytest.mark.parametrize(
    "invalid_boundaries, expected_message",
    [
        ("not a list", "must leave 'boundaries' as a list, got str"),
        ([0, "5", 14], "must leave 'boundaries' as a list of int offsets; got '5' (str)"),
        ([-1, 14], "returned offset -1 outside paragraph bounds [0, 14]"),
    ],
)
def test_post_processing_hook_validation_errors(invalid_boundaries, expected_message):
    """Test that invalid hook return values fail fast with specific HookError messages."""

    def bad_hook(ctx):
        ctx["boundaries"] = invalid_boundaries

    detector = BoundaryDetector(lang="en", hook=bad_hook)

    with pytest.raises(HookError, match=re.escape(expected_message)):
        detector._run_hook("this is a test", [0, 14], 0)
