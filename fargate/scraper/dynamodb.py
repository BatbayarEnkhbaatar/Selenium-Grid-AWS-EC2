import boto3
from boto3.dynamodb.conditions import Attr, Key
import os
# os.environ['AWS_PROFILE'] = default
# os.environ['AWS_DEFAULT_REGION'] = 'ap-northeast-2'

dynamodb = boto3.resource("dynamodb", region_name='ap-northeast-2')
# dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
dynamodbTable = dynamodb.Table("jobs_database")


def getitem_all():
    job_id = dynamodbTable.query(AttributesToGet=['task_id'])
    # print(job_id['Items'])
    return job_id['Items']


# item_list = getitem_all()
# for item in item_list:
#     print(item)

def get_an10_item(task_status) -> object:
    # Key = {"task_status": task_status}
    response = dynamodbTable.query(
        IndexName="task_status-index",
        KeyConditionExpression=Key("task_status").eq(task_status), Limit=10
    )
    # print(response['Items'])
    return response['Items']



def get_count_item(task_status):

    total = dynamodbTable.query(
        IndexName="task_status-index",
        KeyConditionExpression=Key("task_status").eq(task_status)
    )
    # print(total["Items"])
    return len(total["Items"])

def update_item(task_id, job_id, n_status, xpath_link, rule_data):
    response = dynamodbTable.update_item(
        Key={
            'task_id': task_id,
            'job_id': job_id
        },
        UpdateExpression="set task_status=:new_status, xpath_link=:new_xpath, rule_data=:new_rule_data",
        ExpressionAttributeValues={
            ':new_status': n_status,
            ':new_xpath': xpath_link,
            ':new_rule_data': rule_data
        },
        ReturnValues="UPDATED_NEW"
    )
    return response
def input_item(job_id, task_id, result, fullurl):
    dynamodb = boto3.resource("dynamodb", region_name='ap-northeast-2')
    table = dynamodb.Table("resuts")
    table.put_item(
    Item={
        "job_id": job_id,
        "task_id": task_id,
        "url": fullurl,
        "result": result,
    }

)
def get_item_by_id(task_id):

    total = dynamodbTable.query(
        KeyConditionExpression=Key("task_id").eq(task_id)
    )
    # print(total["Items"])
    return total["Items"]

# print(" tasks is: ", get_item_by_id("3c89cc46-0a04-40b8-9045-6d6bbf481db9"))
