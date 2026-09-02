from bbo_capstone.data import load_datasets


def test_round_slice_does_not_include_future_data() -> None:
    dataset = load_datasets()[0]
    partial = dataset.through_round(4)
    assert partial.rounds.tolist() == [1, 2, 3, 4]
    assert len(partial.y) == 4
