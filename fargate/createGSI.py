aws --endpoint-url=http://localhost:4566/ dynamodb update-table \
    --table-name jobs_database \
    --attribute-definitions AttributeName=task_status,AttributeType=S \
    --global-secondary-index-updates \
        "[{\"Create\":{\"IndexName\": \"task_status-index\",\"KeySchema\":[{\"AttributeName\":\"task_status\",\"KeyType\":\"HASH\"}], \
        \"ProvisionedThroughput\": {\"ReadCapacityUnits\": 10, \"WriteCapacityUnits\": 5      },\"Projection\":{\"ProjectionType\":\"ALL\"}}}]"