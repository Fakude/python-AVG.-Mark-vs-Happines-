import unittest

from src.analysis import analyse, create_synthetic_dataset, validate_dataset


class AnalysisTests(unittest.TestCase):
    def test_synthetic_data_is_deterministic_and_valid(self):
        first = create_synthetic_dataset(seed=4, students_per_year=3)
        second = create_synthetic_dataset(seed=4, students_per_year=3)
        self.assertTrue(first.equals(second))
        validate_dataset(first)

    def test_analysis_returns_expected_metrics(self):
        results = analyse(create_synthetic_dataset(seed=1, students_per_year=4))
        self.assertEqual(results["sample_size"], 20)
        self.assertGreaterEqual(results["r_squared"], 0)
        self.assertLessEqual(results["r_squared"], 1)


if __name__ == "__main__":
    unittest.main()
