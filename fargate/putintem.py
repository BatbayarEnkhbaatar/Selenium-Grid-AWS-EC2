import boto3
table_name = "jobs_database"
def dyna_input_item(job_id, task_id, task_status, rule_data, url):
    dynamodb = boto3.resource("dynamodb")
    dynamodbTable = dynamodb.Table(table_name)
    dynamodbTable.put_item(
    Item={
        "job_id": job_id,
        "task_id": task_id,
        "task_status": task_status,
        "rule_data": rule_data,
        "xpath_link": url
    }

)

print("Items successfully imported to DynamoDB ")
