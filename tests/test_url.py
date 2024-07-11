 import theseus.crawler.url as tcu
def test_file_not_found():
    assert tcu.load_urls("randompath.txt ") == []