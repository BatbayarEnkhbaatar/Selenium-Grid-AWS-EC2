import boto3

def delete_movie_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('jobs_database')
    table.delete()


if __name__ == '__main__':
    delete_movie_table()
    print("The table deleted.")