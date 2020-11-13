import unittest
import available_models


class TestAvailableModelUtilFunctions(unittest.TestCase):
    def test_conf_exist(self):
        self.assertIsInstance(available_models.conf_exist(), bool, "conf_exist() did not return bool")

    def test_get_conf(self):
        self.assertIsInstance(available_models.get_conf(), dict, "get_conf did not return dict")

    def test_get_model_ids(self):
        config = """{
"models_root": "./available_models",
"models": [
    { 
        "id": 100,
        "model": "model_step_50000.pt",
        "timeout": 600,
        "opt": {
        "batch_size": 1,
        "beam_size": 10
        }
    },{ 
        "id": 101,
        "model": "model_step_50000-2.pt",
        "timeout": 600,
        "opt": {
        "batch_size": 1,
        "beam_size": 10
        }
    }

],
 "translate_url": "http://DESKTOP-NBG1D5R:5000"
}"""
        self.assertEqual(available_models.get_valid_model_ids(config), [100, 101])


class TestConfFile(unittest.TestCase):

    def setUp(self) -> None:
        if available_models.conf_exist():
            self.config = available_models.get_conf()
        else:
            return self.fail("Skipping test because available_models//conf.json was not found")

    def test_conf_has_model(self):
        self.assertIn("models", self.config, msg="No model tag found in conf.json.")

    def test_conf_has_url(self):
        self.assertIn("translate_url", self.config, msg="No translate_url config found in conf.json.")

    def test_conf_has_a_models(self):
        self.assertGreater(len(self.config.get("models", {})), 0, "No models defined in conf.json")

    def test_conf_models_have_proper_tags(self):
        for model in self.config.get("models", [{}]):
            self.assertIn("model", model, "No model name found in model in conf.json")
            self.assertIn("id", model, "No id found in model in conf.json")


if __name__ == '__main__':
    unittest.main()
