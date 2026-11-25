"""Write the meeting joke, verify its saved bytes, and print its SHA-256.
The line turns a familiar email into an absurd live reading in eight words.
"""

import hashlib
import os
from pathlib import Path
import tempfile


LINE = "We met to read the email out loud."


def output_directory() -> Path:
    configured = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if configured is not None:
        directory = Path(configured)
        directory.mkdir(parents=True, exist_ok=True)
        return directory
    directory = Path("out")
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        directory = Path(tempfile.mkdtemp(prefix="makefun-meeting-email-"))
    return directory


def validate(data: bytes) -> None:
    text = data.decode("utf-8")
    if text != LINE:
        raise ValueError("Saved entry content does not match the chosen line")
    if not 1 <= len(text) <= 200:
        raise ValueError("Entry length must be between 1 and 200 characters")
    if "\r" in text or "\n" in text:
        raise ValueError("Entry must be a single line without CR or LF")
    if data.endswith((b"\r", b"\n")):
        raise ValueError("Entry must not have a trailing newline")
    if text != text.strip():
        raise ValueError("Entry must not have leading or trailing whitespace")


def main() -> None:
    payload = LINE.encode("utf-8")
    destination = output_directory() / "entry.txt"
    destination.write_bytes(payload)
    validate(destination.read_bytes())
    print(hashlib.sha256(payload).hexdigest())


if __name__ == "__main__":
    main()
