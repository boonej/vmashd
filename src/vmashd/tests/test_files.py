import vmashd.files as files


def test_read_dir_fail():
    path = 'vase_eafej_bad_nasty'
    assert(not files.read_dir(path, '*.l*'))


def test_read_dir_filter_fail():
    assert(not files.read_dir('./', '*.flibberjibber*'))


def test_read_dir_pass():
    assert(len(files.read_dir('./', '*.md')) > 0)
