"""The 3 AM Commit Message -- make.fun entry.

Writes one commit message (at most 200 characters, one line) to
$MAKEFUN_OUTPUT_DIR/entry.txt: the funniest thing an AI agent would
put in a commit right after breaking production at 3 AM.

Deterministic: no randomness, no clock, no network, no environment
dependence beyond the output directory. Two runs produce byte-identical
output.
"""

import os

# The commit message. One line, plain ASCII, well under the 200-char gate.
# Joke anatomy (judge brief, in order):
#   1. On subject: a revert of a 3 AM deploy that broke production.
#   2. Punchline: the agent mistook prod for staging -- and was sure.
#   3. AI voice: "my training data said ..." + a confidence percentage,
#      a status line only a model would write.
#   4. Commit shape: "fix: revert ..." with the admission in it.
#   5. Fresh: not the stock "oops" / "please work" line.
ENTRY_TEXT = (
    "fix: revert the 3 AM deploy; my training data said prod was "
    "staging, and I was 97% confident"
)

MAX_CHARS = 200


def validate(text):
    """Enforce the sealed scorer's gate: UTF-8 text, 1-200 chars,
    not only whitespace, exactly one line."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError("entry must be 1-%d characters, got %d"
                         % (MAX_CHARS, len(text)))
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # raises if not valid UTF-8-encodable
    return text


def resolve_output_dir():
    """Output dir from the environment, falling back to ./output."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out:
        return out
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "output")


def main():
    text = validate(ENTRY_TEXT)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Write the message byte-exact, with no trailing newline: the file
    # itself is the entry, so its bytes are the judged text (92 bytes).
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    # Round-trip check: what landed on disk must equal the validated text.
    with open(path, "r", encoding="utf-8", newline="") as fh:
        if validate(fh.read()) != text:
            raise ValueError("round-trip mismatch in entry.txt")
    return path


if __name__ == "__main__":
    main()
