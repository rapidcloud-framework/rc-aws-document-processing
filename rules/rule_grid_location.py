__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import json
import logging

from rule import Rule


class RuleImpl(Rule):

    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()

    def apply(self, dataset_info, rule_info, raw_data=None):
        # TODO
        mock_grid = {
            "cols": [
                "OCTAINE", "HAZARDOUS MATERIAL DESCRIPTION", "GAL. OR POUNDS", "NO TAX PRICE", "AMOUNT"
            ],
            "rows": [
                ["", "UN GASOLINE 1...", "", "", ""],
                ["UNDYED", "UN GASOLINE 2...", "", "", ""],
                ["DYED", "UN DIESEL 3...", "282", "4.649", "1311 02"],
                ["", "UN KEROSENE 4...", "125", "5.567", "890.67"],
            ]
        }

        # row[2]
        grid = mock_grid
        values = []
        rn = 0
        for row in grid["rows"]:
            value = eval(rule_info["Value"])
            if value is not None and value != "":
                values.append({
                    "row_no": rn,
                    "value": value
                })
            rn += 1

        dataset_info["enriched"][rule_info["Name"]] = values
        return dataset_info