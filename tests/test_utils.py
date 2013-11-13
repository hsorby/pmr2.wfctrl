from unittest import TestCase

from pmr.wfctrl import utils


class SetUrlCredsTestCase(TestCase):

    def test_set_new(self):
       r = utils.set_url_cred('http://example.com', 'user', 'pass')
       self.assertEqual(r, 'http://user:pass@example.com')

    def test_set_replace_user(self):
       r = utils.set_url_cred('http://nobody@example.com', 'user', 'pass')
       self.assertEqual(r, 'http://user:pass@example.com')

    def test_set_replace_all(self):
       r = utils.set_url_cred('http://no:body@example.com', 'user', 'pass')
       self.assertEqual(r, 'http://user:pass@example.com')

    def test_not_url(self):
       r = utils.set_url_cred('/tmp/filepath', 'user', 'pass')
       self.assertEqual(r, '/tmp/filepath')

    def test_windows_path(self):
       r = utils.set_url_cred('C:\\User\\Tester\\Documents', 'user', 'pass')
       self.assertEqual(r, 'C:\\User\\Tester\\Documents')