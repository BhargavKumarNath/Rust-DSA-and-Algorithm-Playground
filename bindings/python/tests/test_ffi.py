import advanced_ds_playground

def test_sum_as_string():
    assert advanced_ds_playground.sum_as_string(2, 3) == "5"
    assert advanced_ds_playground.sum_as_string(0, 0) == "0"
    assert advanced_ds_playground.sum_as_string(10, 5) == "15"
    