import unittest
import CORE_Individual

# A test class for the Core_Individual class
class Test_Core_Individual(unittest.TestCase):

    #A function to test if a dictionary is returned after profiling with the correct fields.
    def test_to_see_that_profile_has_valid_dictionary_fields(self):
        example_text_to_be_profiled = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Integer efficitur diam at ex faucibus finibus. Fusce vitae mi bibendum, porta lorem at, semper est."""
        example_name_to_be_profiled = "test"
        example_impact_to_be_profiled = 1

        new_individual = CORE_Individual.Individual(example_text_to_be_profiled, example_name_to_be_profiled, example_impact_to_be_profiled)
        individuals_dictionary_response = new_individual.profile()

        self.assertIn("likelihood", individuals_dictionary_response.keys())
        self.assertIn("impact", individuals_dictionary_response.keys())
        self.assertIn("extra", individuals_dictionary_response.keys())
        self.assertIn("name", individuals_dictionary_response.keys())
        self.assertIn("risk", individuals_dictionary_response.keys())

    #A test which checks if a dictionary is returned of the correct types after profiling. 
    def test_to_see_that_profile_returns_fields_of_correct_type(self):
        example_text_to_be_profiled = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. 
        Integer efficitur diam at ex faucibus finibus. Fusce vitae mi bibendum, porta lorem at, semper est."""
        example_name_to_be_profiled = "test"
        example_impact_to_be_profiled = 1

        new_individual = CORE_Individual.Individual(example_text_to_be_profiled, example_name_to_be_profiled,
                                                    example_impact_to_be_profiled)
        individuals_dictionary_response = new_individual.profile()

        self.assertIs(type(individuals_dictionary_response["likelihood"]), float)
        self.assertIs(type(individuals_dictionary_response["impact"]), int)
        self.assertIs(type(individuals_dictionary_response["extra"]), list)
        self.assertIs(type(individuals_dictionary_response["name"]), str)
        self.assertIs(type(individuals_dictionary_response["risk"]), float)


if __name__ == '__main__':
    unittest.main()