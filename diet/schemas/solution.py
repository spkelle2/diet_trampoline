"""
This module describes the constraints placed on data output from the diet engine
"""

from ticdat import TicDatFactory

# define table and column names the engine should write out to
solution_schema = TicDatFactory(
    parameters=[["Parameter"], ["Value"]],
    buy_food=[["Food"], ["Quantity"]],
    consume_nutrition=[["Category"], ["Quantity"]]
)