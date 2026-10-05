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

from dataclasses import dataclass

import config
from ingest import Document
import re


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
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Right now it just calls the fallback. That is the plain, generic behaviour
    the brief is talking about.

    When you write your own strategy, set `produced_by` to
    "chunker.py::split_documents" so your README's Sample Chunks section names
    the right function. `app.py chunks` prints that string for you.

    Things worth thinking about before you write any code:
      - Are your documents short posts or long guides?
      - Is the useful information in one sentence, or spread over a paragraph?
      - Would splitting on paragraph breaks keep more thoughts intact than
        splitting on a character count?
    """
#
    # return fallback_split(documents)

    # Paragraph-based splitting strategy -  since i am using campus_life, i think splitting by paragraph is reasonable since the posts in the documents are short reviews.
    chunk_size = config.CHUNK_SIZE
    overlap = config.CHUNK_OVERLAP
    min_chars = 200  # the floor criterion 4 names; a lone title paragraph should never survive as its own chunk
    max_words = 90   # the cap criterion 4 names; a chunk this dense is covering more than one topic

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        # split on blank lines
        paras = [p.strip() for p in re.split(r"\n\s*\n+", doc.text) if p.strip()]

        # merge tiny paras into previous, but never past the word cap —
        # otherwise four short replies (each fine on its own) can pile into
        # one chunk that's technically under chunk_size but covers four topics
        merged: list[str] = []
        for p in paras:
            if not merged:
                merged.append(p)
                continue
            tiny_threshold = max(50, chunk_size // 4)
            combined = merged[-1] + "\n\n" + p
            if (len(p) < tiny_threshold
                    and len(combined) <= chunk_size
                    and len(combined.split()) <= max_words):
                merged[-1] = combined
            else:
                merged.append(p)

        # The pass above only merges a tiny paragraph *backward*, so a
        # document's first paragraph (its title) has nothing earlier to merge
        # into and always survives alone. Fold anything still under min_chars
        # forward into the block that follows it instead — unless that would
        # push the result over the word cap, in which case the short block
        # stays short rather than trading one violation for the other.
        i = 0
        while i < len(merged) - 1:
            combined = merged[i] + "\n\n" + merged[i + 1]
            if len(merged[i]) < min_chars and len(combined.split()) <= max_words:
                merged[i + 1] = combined
                del merged[i]
            else:
                i += 1
        if len(merged) > 1 and len(merged[-1]) < min_chars:
            combined = merged[-2] + "\n\n" + merged[-1]
            if len(combined.split()) <= max_words:
                merged[-2] = combined
                merged.pop()

        index = 0
        prev_tail = ""
        for block in merged:
            # carry the tail of the previous chunk forward so consecutive
            # chunks in the same document actually overlap — but skip it if
            # it would push this chunk over the word cap
            text = f"{prev_tail}\n\n{block}" if prev_tail else block
            if prev_tail and len(text.split()) > max_words:
                text = block
            if len(text) <= chunk_size and len(text.split()) <= max_words:
                chunks.append(Chunk(text=text, source=doc.source, index=index, produced_by="chunker.py::split_documents"))
                index += 1
                prev_tail = text[-overlap:] if overlap else ""
                continue
            # long block: windowed split
            start = 0
            piece = ""
            while start < len(text):
                piece = text[start : start + chunk_size].strip()
                if piece:
                    chunks.append(Chunk(text=piece, source=doc.source, index=index, produced_by="chunker.py::split_documents"))
                    index += 1
                start += chunk_size - overlap
            prev_tail = piece[-overlap:] if overlap else ""

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
