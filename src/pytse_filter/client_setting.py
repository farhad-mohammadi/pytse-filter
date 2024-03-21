# This module defines the settings for client-specific calculations.
# It contains a dictionary named 'calculations' which outlines various financial metrics
# and their corresponding calculation methods and periods.

calculations = {
    "sell_per_capita": [
        {
            "columns": [
                "sell_per_capita_avg10"
            ],
            "args": {
                "method": "mean",
                "period": 10
            }
        }
    ],
    "buy_per_capita": [
        {
            "columns": [
                "buy_per_capita_avg10"
            ],
            "args": {
                "method": "mean",
                "period": 10
            }
        }
    ],
    "power_of_demand": [
        {
            "columns": [
                "power_of_demand_avg10"
            ],
            "args": {
                "method": "mean",
                "period": 10
            }
        }
    ],
    "indivisual_mony_flow": [
        {
            "columns": [
                "indivisual_mony_flow_total10"
            ],
            "args": {
                "method": "sum",
                "period": 10
            }
        }
    ],

}