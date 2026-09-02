from tools import prose_index


def test_normalise_lowercases_strips_punctuation_collapses_whitespace():
    text = "Edwin,  said:  \"The   Bittle   is   gone!\"\n\nReally."
    assert prose_index.normalise(text) == "edwin said the bittle is gone really"


def test_shingle_hashes_empty_for_short_text():
    assert prose_index.shingle_hashes("only six words here right now", n=7) == set()


def test_shingle_hashes_nonempty_for_long_enough_text():
    hashes = prose_index.shingle_hashes(
        "the quick brown fox jumps over the lazy dog today", n=7
    )
    assert len(hashes) == 4  # 10 words - 7 + 1


def test_shingle_hashes_deterministic():
    text = "Nine people came into it and only six people came out again."
    assert prose_index.shingle_hashes(text) == prose_index.shingle_hashes(text)


def test_shingle_hashes_insensitive_to_case_and_punctuation():
    a = prose_index.shingle_hashes("Nine people came into it, and only six left.")
    b = prose_index.shingle_hashes("nine people came into it and only six left")
    assert a == b


def test_shingle_hashes_differ_for_different_text():
    a = prose_index.shingle_hashes("the quick brown fox jumps over the lazy dog")
    b = prose_index.shingle_hashes("a slow green frog hops under a sleepy cat")
    assert a.isdisjoint(b)


def test_prose_index_roundtrips_through_pickle(tmp_path):
    index = prose_index.ProseIndex(shingle_size=7)
    index.unpublished = {b"\x01" * 8, b"\x02" * 8}
    index.published = {b"\x02" * 8, b"\x03" * 8}
    index.unpublished_source_count = 3
    index.published_source_count = 1
    path = tmp_path / "index.pkl"
    index.save(path)
    loaded = prose_index.ProseIndex.load(path)
    assert loaded.unpublished == index.unpublished
    assert loaded.published == index.published
    assert loaded.shingle_size == 7
