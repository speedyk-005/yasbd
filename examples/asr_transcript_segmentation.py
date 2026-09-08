"""Split raw ASR/transcription output into complete sentences.

Automatic speech recognition (ASR) engines typically emit a single
run-on block of text: no paragraph breaks, informal phrasing, and
abbreviations left exactly as spoken (e.g. "Dr.", "U.S."). ``yasbd`` is
a sentence boundary detector, not a punctuation restorer, so this
example assumes the transcript already carries terminal punctuation and
capitalized sentence starts (as most modern ASR systems, e.g. Whisper,
produce) and demonstrates recovering clean, complete sentences from
that raw stream without mangling the abbreviations.

Run:
    python examples/asr_transcript_segmentation.py
"""

from yasbd import BoundaryDetector

# A representative raw transcript, as it might arrive from an ASR
# engine: no paragraph breaks, informal phrasing, sparse punctuation.
RAW_TRANSCRIPT = (
    "Okay so today we're going to talk about the quarterly roadmap. "
    "First up is the mobile release which is currently scheduled for "
    "next friday. Dr. Patel's team already finished the backend work "
    "so we're mostly waiting on qa now. Any questions before we move "
    "on to the second topic? Great, let's talk about the U.S. launch "
    "timeline then."
)

EXPECTED_SENTENCES = [
    "Okay so today we're going to talk about the quarterly roadmap.",
    "First up is the mobile release which is currently scheduled for next friday.",
    "Dr. Patel's team already finished the backend work so we're mostly waiting on qa now.",
    "Any questions before we move on to the second topic?",
    "Great, let's talk about the U.S. launch timeline then.",
]


def main() -> None:
    detector = BoundaryDetector(lang="en")
    sentences = list(detector.segment(RAW_TRANSCRIPT))

    for i, sentence in enumerate(sentences, start=1):
        print(f"{i}: {sentence}")

    assert sentences == EXPECTED_SENTENCES, (  # noqa: S101
        f"Segmentation drifted from the expected transcript sentences. Got: {sentences}"
    )
    print("\nOK: transcript segmented into complete sentences as expected.")


if __name__ == "__main__":
    main()
