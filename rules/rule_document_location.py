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
        dataset_info["enriched"][rule_info["Name"]] = f"{rule_info['rule_type']}: TBD"
        return dataset_info