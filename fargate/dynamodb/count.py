import dynamodb


dynamodb.get_count_item("ongoing")
num = dynamodb.get_count_item("ongoing")
print("THERE ARE ", num, " TASKS IN THE QUEUE")