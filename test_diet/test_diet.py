import unittest
from diet import input_schema, solve, DietException


class TestDiet(unittest.TestCase):

    def test_matching_dataset(self):
        dat = input_schema.csv.create_tic_dat('diet_sample_data')
        sln = solve(dat)
        self.assertTrue(sln.parameters['Total Cost']['Value'] == 11.828861111111111,
                        msg='The matching dataset should generate the cached solution')

    def test_different_values(self):
        dat = input_schema.csv.create_tic_dat('diet_sample_data')
        dat.foods['ice cream']['Cost'] = 1.60
        with self.assertRaises(DietException, msg="Different values should be detected"):
            solve(dat)

    def test_different_primary_keys(self):
        dat = input_schema.csv.create_tic_dat('diet_sample_data')
        dat.foods['brocolli']['Cost'] = 2.25
        with self.assertRaises(DietException, msg="Different pks should be detected"):
            solve(dat)

    def test_gurobi_solve(self):
        dat = input_schema.csv.create_tic_dat('diet_sample_data')
        dat.parameters['How To Make Solution']['Value'] = "Use Gurobi"
        with self.assertRaises(DietException, msg="Gurobi should not be present, causing solve to fail"):
            solve(dat)

    def test_data_integrity_errors(self):
        dat = input_schema.csv.create_tic_dat('diet_dirty_sample_data')
        with self.assertRaises(AssertionError, msg="A dirty dat should fail assertions"):
            solve(dat)

    def test_bad_parameter(self):
        dat = input_schema.csv.create_tic_dat('diet_sample_data')
        dat.parameters['How To Make Solution']['Value'] = "Use Pete"
        with self.assertRaises(AssertionError, msg="Bad parameters should be caught"):
            solve(dat)


if __name__ == '__main__':
    unittest.main()
