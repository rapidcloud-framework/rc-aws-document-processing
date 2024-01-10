__author__ = "Igor Royzis"
__copyright__ = "Copyright 2023, Kinect Consulting"
__license__ = "Commercial"
__email__ = "iroyzis@kinect-consulting.com"

import importlib
import logging
import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

logger = logging.getLogger(__name__)

with open('./rules/rules_config.json', 'r') as f:
    rules_config = json.load(f)


def get_raw_data(env, final_s3_location):
    bucket = f"{env}-raw".replace('_','-')
    obj_key = final_s3_location.replace(f"s3://{bucket}/","")
    s3_client = boto3.Session().client('s3')
    s3_response = s3_client.get_object(Bucket=bucket, Key=obj_key)
    return json.loads(s3_response.get('Body').read())


def exec(cdc_log_item):
    print(json.dumps(cdc_log_item, indent=2))
    fqn = f"{cdc_log_item['profile']}_{cdc_log_item['document_match']}"
    print(f"running rules for {fqn} ...")
    resp = boto3.Session().resource('dynamodb').Table("dataset_unstructured").query(
        KeyConditionExpression=Key('fqn').eq(fqn)
    )['Items']
    if len(resp) > 0:
        dataset = resp[0]
        print(json.dumps(dataset, indent=2, default=str))
        if "enriched" not in cdc_log_item:
            cdc_log_item["enriched"] = {}
        if "rules" in dataset:
            for rule in dataset["rules"]:
                print(f"\n> running {rule['rule_type']} ...")
                print(json.dumps(rule, indent=2))
                rule_impl = importlib.import_module(f"rule_{rule['rule_type']}")
                rule_inst = rule_impl.RuleImpl()
                func = getattr(rule_inst, "apply")
                try:
                    raw_data = None
                    if rules_config[rule['rule_type']].get('load_raw_data', False):
                        raw_data = get_raw_data(cdc_log_item["profile"], cdc_log_item["final_s3_location"])
                        # print(raw_data)
                    cdc_log_item = func(cdc_log_item, rule, raw_data)
                except Exception as e:
                    print(f"{rule['rule_type']}: {e}")
                    pass
        # TODO maybe save enriched cdc_log item
    else:
        raise Exception(f"Dataset {fqn} was not found") 
    print(json.dumps(cdc_log_item, indent=2))
    return cdc_log_item


if __name__ == "__main__":
    import sys
    action = sys.argv[1]
    
    if action == "exec":
        fqns = [
            "s3://igor-textract-dev-ingestion/files/rc-any/Unknown/2023/7/6/AMA-Apr1_diesel.pdf",
            "s3://igor-textract-dev-ingestion/files/rc-any/Unknown/2023/7/3/AMA-Sep_electricity__multi__0001.pdf"
        ]
        for fqn in fqns:
            item = boto3.Session().resource('dynamodb').Table("cdc_log").query(
                KeyConditionExpression=Key('fqn').eq(fqn)
            )['Items'][0]
            result = exec(item)
            with open(f"./test/{item['document_match']}_enriched.json", "w") as f:
                json.dump(result, f, indent=2)
