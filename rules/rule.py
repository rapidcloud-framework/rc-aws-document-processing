__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import logging


class Rule(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    def apply(self, dataset_info, rule_info, raw_data=None):
        raise Exception("This rule has not been implemented yet") 