from .. worddb import listwords




def test_listwords():
    w = listwords()
    assert w > 0


if __name__ == '__main__':
    test_listwords()

