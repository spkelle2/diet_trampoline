from diet.schemas.input import input_schema
from diet.schemas.solution import solution_schema
from diet.solve.cache import input_dict, sln_dict
from diet.solve.utils import verify

try:
    import gurobipy as gu
except ModuleNotFoundError:
    gu = None


def solve(dat):
    """
    core solving routine. Checks data integrity before either solving or
    attempting to return cached solution
    :param dat: a ticdat to solve for
    :return: a good ticdat for the solution_schema, or None
    """
    assert input_schema.good_tic_dat_object(dat)
    assert not input_schema.find_foreign_key_failures(dat)
    assert not input_schema.find_data_type_failures(dat)
    assert not input_schema.find_data_row_failures(dat)
    print('No data integrity issues found')

    full_parameters = input_schema.create_full_parameters_dict(dat)

    if full_parameters["How To Make Solution"] == "Use Cache":
        print('attempting to return hard coded solution')
        input_dat = input_schema.TicDat(**input_dict)

        for table in input_schema.all_tables:
            verify(getattr(dat, table).keys() == getattr(input_dat, table).keys(),
                   f"the given dat has different pks than expected in {table}")
            for pk, flds in getattr(dat, table).items():
                for f, v in flds.items():
                    verify(v == getattr(input_dat, table)[pk][f],
                           f"the given dat has different values for {pk} in {table}")
        print('The inputs look the same')
        return solution_schema.TicDat(**sln_dict)

    print('solving with gurobi')
    verify(gu is not None, "gurobipy needs to be installed for this example code to solve!")
    mdl = gu.Model("diet")

    nutrition = {c: mdl.addVar(lb=n["Min Nutrition"], ub=n["Max Nutrition"], name=c)
                 for c, n in dat.categories.items()}

    # Create decision variables for the foods to buy
    buy = {f: mdl.addVar(name=f) for f in dat.foods}

    # Nutrition constraints
    for c in dat.categories:
        mdl.addConstr(gu.quicksum(dat.nutrition_quantities[f, c]["Quantity"]*buy[f]
                                  for f in dat.foods) == nutrition[c], name=c)

    mdl.setObjective(gu.quicksum(buy[f]*c["Cost"] for f, c in dat.foods.items()),
                     sense=gu.GRB.MINIMIZE)
    mdl.optimize()

    if mdl.status == gu.GRB.OPTIMAL:
        sln = solution_schema.TicDat()
        for f, x in buy.items():
            if x.x > 0:
                sln.buy_food[f] = x.x
        for c, x in nutrition.items():
            sln.consume_nutrition[c] = x.x
        sln.parameters['Total Cost'] = sum(dat.foods[f]["Cost"] * r["Quantity"]
                                           for f, r in sln.buy_food.items())
        return sln
