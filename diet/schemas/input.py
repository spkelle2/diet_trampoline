"""
This module describes the constraints placed on data flowing into the diet engine
"""

from ticdat import TicDatFactory

# define table and column names the engine can expect as inputs
input_schema = TicDatFactory(
    categories=[["Name"], ["Min Nutrition", "Max Nutrition"]],
    foods=[["Name"], ["Cost"]],
    nutrition_quantities=[["Food", "Category"], ["Quantity"]],
    parameters=[['Name'], ['Value']]
)

# add the following parameter to the parameters table
input_schema.add_parameter("How To Make Solution", "Use Gurobi", number_allowed=False,
                           strings_allowed=["Use Gurobi", "Use Cache"])

# Define the foreign key relationships
input_schema.add_foreign_key("nutrition_quantities", "foods", ["Food", "Name"])
input_schema.add_foreign_key("nutrition_quantities", "categories",
                             ["Category", "Name"])

# Define the data types
input_schema.set_data_type("categories", "Min Nutrition", min=0, max=float("inf"),
                           inclusive_min=True, inclusive_max=False)
input_schema.set_data_type("categories", "Max Nutrition", min=0, max=float("inf"),
                           inclusive_min=True, inclusive_max=True)
input_schema.set_data_type("foods", "Cost", min=0, max=float("inf"),
                           inclusive_min=True, inclusive_max=False)
input_schema.set_data_type("nutrition_quantities", "Quantity", min=0, max=float("inf"),
                           inclusive_min=True, inclusive_max=False)

# We also want to insure that Max Nutrition doesn't fall below Min Nutrition
input_schema.add_data_row_predicate(
    "categories", predicate_name="Min Max Check",
    predicate=lambda row: row["Max Nutrition"] >= row["Min Nutrition"])

# TicDat's usual default of zero makes sense everywhere except for Max Nutrition
input_schema.set_default_value("categories", "Max Nutrition", float("inf"))
