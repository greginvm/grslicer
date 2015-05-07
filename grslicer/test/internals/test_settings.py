from unittest import TestCase
import grslicer.settings as gs


class TestSettings(TestCase):

    def test_args(self):
        d = set()
        for group_key, prop in gs.settings_iter():
            self.assertNotIn(prop.arg, d)
            d.add(prop.arg)