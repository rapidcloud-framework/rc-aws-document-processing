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
        dataset_info["enriched"][rule_info["Name"]] = dataset_info["key_value_pairs"].get(rule_info["Value"], "MISSING")
        return dataset_info