import unittest
import available_models


class TestAvailableModelUtilFunctions(unittest.TestCase):
    """This test suite tests the functions that give access to the config file"""

    def test_conf_exist(self):
        """This function tests if the config file for the translation server exists"""
        self.assertIsInstance(available_models.conf_exist(), bool, "conf_exist() did not return bool")

    def test_get_conf(self):
        """This function tests if the get_conf function returns a dictionary with the config file"""
        self.assertIsInstance(available_models.get_conf(), dict, "get_conf did not return dict")

    def test_get_model_ids(self):
        """This test tests if the get_model_ids function can extract ids from a config"""
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
    """This test suite checks the contents of the conf.json in the available_models folder"""
    def setUp(self) -> None:
        """Set up function for tests. This function is run before every test"""
        if available_models.conf_exist():
            self.config = available_models.get_conf()
        else:
            return self.fail("Skipping test because available_models//conf.json was not found")

    def test_conf_has_model(self):
        """Test to see if there is a model tag in the config file"""
        self.assertIn("models", self.config, msg="No model tag found in conf.json.")

    def test_conf_has_url(self):
        """See if there is a url in the config file"""
        self.assertIn("translate_url", self.config, msg="No translate_url config found in conf.json.")

    def test_conf_has_a_models(self):
        """See if there are models defined in the config file"""
        self.assertGreater(len(self.config.get("models", {})), 0, "No models defined in conf.json")

    def test_conf_models_have_proper_tags(self):
        """See if the models in the config file have ids"""
        for model in self.config.get("models", [{}]):
            self.assertIn("model", model, "No model name found in model in conf.json")
            self.assertIn("id", model, "No id found in model in conf.json")


if __name__ == '__main__':
    unittest.main()
