from data_cleaning import load_csv_files

data = load_csv_files("data")


def test_empty():
    not_empty = True
    for tick in data:
        if tick[1] == '':
            not_empty=False
    assert not_empty

def test_val():
    valid = True
    for tick in data:
        if tick[1] < 100:
            valid=False
    assert valid