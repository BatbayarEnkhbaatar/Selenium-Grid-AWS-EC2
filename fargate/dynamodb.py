import boto3
from boto3.dynamodb.conditions import Attr, Key


def getitem_all():
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
    dynamodbTable = dynamodb.Table("jobs_database")
    job_id = dynamodbTable.query(AttributesToGet=['task_id'])
    # print(job_id['Items'])
    return job_id['Items']


# item_list = getitem_all()
# for item in item_list:
#     print(item)

def get_an_item(task_status):
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
    dynamodbTable = dynamodb.Table("jobs_database")
    # Key = {"task_status": task_status}
    response = dynamodbTable.query(
        IndexName="task_status-index",
        KeyConditionExpression=Key("task_status").eq(task_status), Limit=1
    )
    # print(response['Items'])
    return response['Items']

def get_count_item (task_status):
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
    dynamodbTable = dynamodb.Table("jobs_database")
    total = dynamodbTable.query(
        IndexName="task_status-index",
        KeyConditionExpression=Key("task_status").eq(task_status)
    )
    # print(total["Items"])
    return len(total["Items"])

def update_item(task_id, job_id, n_status, xpath_link, rule_data):
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:4566/dynamodb")
    dynamodbTable = dynamodb.Table("jobs_database")
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


# task_status = "Changed"
# print("Please enter task id: ")
# task_id = input()
#
# print("Please enter JOB ID: ")
# job_id = input()
# print("Please enter New Status: ")
# task_status = input()
# print("Please enter Xpath: ")
# xpath = input()
# print("Please enter Rule_Data ")
# rule = input()
# print(update_item(str(task_id), str(job_id), task_status, xpath, rule))
# print("it is updated")

#
# print("Please enter status: ")
# new_status = input()
# item_returned = get_count_item("ongoing")
# print(item_returned)
get_an_item("ongoing")