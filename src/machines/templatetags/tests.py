import unittest

import wiki_link

class Test(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual("", wiki_link.wiki_links(""))

    def test_link(self):
        self.assertEqual('<a href="http://url.com">url.com</a>', wiki_link.wiki_links("[[url.com]]"))

    def test_link_with_description(self):
        self.assertEqual('<a href="http://url.com">interesting description</a>', wiki_link.wiki_links("[[url.com|interesting description]]"))

    def test_link_start_with_star(self):
        self.assertEqual('<a href="http://url.com">url.com</a>', wiki_link.wiki_links("[[*url.com]]"))

    def test_link_with_minus(self):
        self.assertEqual('<a href="http://url.com">url.com</a>', wiki_link.wiki_links("[[-url.com]]"))

    def test_several_links(self):
        self.assertEqual('<a href="http://url.com">url.com</a> <a href="http://other.org">other.org</a>', wiki_link.wiki_links("[[url.com]] [[other.org]]"))



if __name__ == '__main__':
    unittest.main()
