import unittest
import os, sys, json
import filecmp

HERE = os.path.dirname(os.path.realpath(__file__))

sys.path.append(os.path.join(HERE,'..','src'))
from hp import HandyPlotter



class TestLikert(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(HERE, "static", "test_data.json"))as f:
            self.config = json.load(f)

    def test_draw_likert_graph_simple(self):
        a = HandyPlotter(os.path.join(HERE, "static", "test_config.json"))

        a.plot_likert_scales(
            self.config["likert_test_data"]["questions"], 
            self.config["likert_test_data"]["data"], 
            self.config["likert_test_data"]["scale"],
            os.path.join(HERE, "likert_test_instance.png")
        )

        self.assertTrue(
            filecmp.cmp(
                os.path.join(HERE, "likert_test_instance.png"), 
                os.path.join(HERE, "static", "likert_test_instance.png")
            )
        )

    def tearDown(self):
        try:
            os.remove(os.path.join(HERE, "likert_test_instance.png"))
        except:
            pass
        return super().tearDown()