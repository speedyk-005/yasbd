"""
Generates and plays Edge TTS audio sentence-by-sentence with parallel generation.

Prerequisites:
    pip install miniaudio, edge_tts
"""

import asyncio
import os
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor

import edge_tts
import miniaudio

from yasbd import BoundaryDetector


class LiveTTS:
    def __init__(self, voice: str = "en-US-AriaNeural", n_jobs: int = 4) -> None:
        """
        Initialize the streaming client.

        Args:
            voice: Edge TTS voice model name
            n_jobs: Number of parallel TTS generation jobs
        """
        self.voice = voice
        self.n_jobs = n_jobs

    def _handle_async_exception(self, loop, context) -> None:
        """Custom exception handler for async event loop."""
        exception = context.get("exception")
        message = context.get("message", "")

        if exception:
            error_msg = str(exception)
            if "Connection lost" in error_msg and "Connection reset by peer" in error_msg:
                return

        if "SSL handshake failed" in message or "SSLWantReadError" in message:
            return

        loop.default_exception_handler(context)

    def _generate_tts_sync(self, text: str) -> str:
        """Generate TTS for a single sentence and save to temp file."""
        tmp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp_file_path = tmp_file.name
        tmp_file.close()

        async def generate():
            communicate = edge_tts.Communicate(
                text, self.voice, rate="+15%"
            )  # For slight energy boost

            with open(tmp_file_path, "wb") as file:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        file.write(chunk["data"])

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(self._handle_async_exception)
        try:
            loop.run_until_complete(generate())
            return tmp_file_path
        finally:
            loop.close()

    def _play_audio(self, file_path: str) -> None:
        """Play audio file using miniaudio."""
        stream = miniaudio.stream_file(file_path)
        device = miniaudio.PlaybackDevice()
        device.start(stream)

        info = miniaudio.get_file_info(file_path)
        time.sleep(info.duration)

        device.close()

    def play_live(self, text: str) -> None:
        """
        Generate and play text live (sentence-by-sentence).

        Args:
            text: Raw text to synthesize and play
        """
        splitter = BoundaryDetector(lang=self.voice.split("-")[0])
        chunks = splitter.segment(text)

        with ThreadPoolExecutor(max_workers=self.n_jobs) as executor:
            for audio_file in executor.map(self._generate_tts_sync, chunks):
                if audio_file:
                    self._play_audio(audio_file)
                    os.remove(audio_file)


# Example usage
if __name__ == "__main__":
    import textwrap

    text = textwrap.dedent("""
        Got it. I updated my memory:
        PLASMA is no longer an active project for you.
        Ruff is your preferred Python tooling instead of Black, Pylint, and Flake8.
        You mainly use PocketPal and MNN Chat for AI/local model usage.
        Layla AI Lite is no longer considered one of your main tools.
        I'll use these preferences going forward.
    """)

    client = LiveTTS(voice="en-US-AriaNeural", n_jobs=3)
    print(text)
    client.play_live(text)
    print("Playback finished!")
