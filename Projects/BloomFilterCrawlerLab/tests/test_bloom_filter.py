import pytest
from core.bloom_filter import BloomFilter

def test_insert_then_loookup_true():
    bf = BloomFilter(1000, 0.01)
    bf.add_item("apple")
    assert bf.check_item_exist("apple") is True

def test_lookup_unseen_item():
    bf = BloomFilter(1000, 0.01)
    assert bf.check_item_exist("apple") is False

def test_deterministic_indexes():
    bf = BloomFilter(1000, 0.01)
    a = list(bf._indexes("apple"))
    b = list(bf._indexes("apple"))
    assert a == b

def test_bits_set_percent_increases_after_inserts():
    bf = BloomFilter(1000, 0.01)
    before = bf.bits_set_percent()

    for item in ["a", "b", "c", "d", "e"]:
        bf.add_item(item)

    after = bf.bits_set_percent()
    assert after >= before

def test_serialize_deserialize_roundtrip(tmp_path):
    bf = BloomFilter(n=1000, fpr=0.01)
    for k in ["apple", "banana", "carrot"]:
        bf.add_item(k)

    blob = bf.serialize()
    # simulate disk write/read
    p = tmp_path / "bf.snapshot"
    p.write_bytes(blob)
    loaded = BloomFilter.deserialize(p.read_bytes())

    for k in ["apple", "banana", "carrot"]:
        assert loaded.check_item_exist(k) is True
    assert loaded.m == bf.m and loaded.k == bf.k
    assert loaded.bits == bf.bits

def test_invalid_constructor_params():
    import pytest
    with pytest.raises(ValueError):
        BloomFilter(n=0, fpr=0.01)
    with pytest.raises(ValueError):
        BloomFilter(n=100, fpr=0.0)
    with pytest.raises(ValueError):
        BloomFilter(n=100, fpr=1.0)