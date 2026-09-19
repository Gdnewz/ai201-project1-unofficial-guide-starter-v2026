"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


# Splits after a sentence-ending mark followed by whitespace. Lines without
# terminal punctuation (headings, for example) stay attached to the sentence
# that follows them instead of becoming orphans.
SENTENCE_END = re.compile(r'(?<=[.!?])\s+')


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def _tail_of(text: str, length: int) -> str:
    """
    The last `length` characters of `text`, trimmed forward so the carried-over
    text starts at a word boundary rather than in the middle of a word.
    """
    if length <= 0:
        return ""
    if len(text) <= length:
        return text
    tail = text[-length:]
    space = tail.find(" ")
    return tail[space + 1:] if space != -1 else tail


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks on sentence boundaries.

    Strategy, and why:

      - Sentences are never cut in half. The documents in campus_life are short
        and written in complete sentences, so a boundary in the middle of one
        would strand a fragment that answers nothing.
      - Sentences accumulate until adding the next one would exceed the ceiling
        in config.CHUNK_SIZE. The ceiling exists because a chunk covering many
        subjects embeds as an average of all of them and matches no single
        question strongly.
      - Each chunk after the first carries config.CHUNK_OVERLAP characters from
        the end of the previous one, so context crosses the boundary.
      - A leftover tail shorter than config.CHUNK_MIN is folded back into the
        chunk before it, rather than emitted as a fragment.
    """
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    minimum = getattr(config, "CHUNK_MIN", 170)

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []

    for doc in documents:
        sentences = [s.strip() for s in SENTENCE_END.split(doc.text) if s.strip()]

        # Group whole sentences together without exceeding the ceiling. Groups
        # after the first reserve room for the overlap text prepended below, so
        # the finished chunk still lands under chunk_size.
        groups: list[str] = []
        current = ""
        for sentence in sentences:
            budget = chunk_size if not groups else chunk_size - overlap
            candidate = f"{current} {sentence}".strip()
            if current and len(candidate) > budget:
                groups.append(current)
                current = sentence
            else:
                current = candidate
        if current:
            groups.append(current)

        # A tail below the floor is not worth retrieving on its own.
        if len(groups) > 1 and len(groups[-1]) < minimum:
            tail = groups.pop()
            groups[-1] = f"{groups[-1]} {tail}"

        for index, group in enumerate(groups):
            if index == 0:
                text = group
            else:
                text = f"{_tail_of(groups[index - 1], overlap)} {group}".strip()
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
