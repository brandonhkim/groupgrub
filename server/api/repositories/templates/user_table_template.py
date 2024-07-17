class UserTableTemplate:
    KeySchema = [
        {
            'AttributeName': 'id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'email',
            'KeyType': 'RANGE'
        }
    ]
    GlobalSecondaryIndexes=[
        {
            'IndexName': 'email-index',
            'KeySchema': [
               {
                  'AttributeName': 'email',
                  'KeyType': 'HASH'
               }
             ],
             'Projection': {
               'ProjectionType': 'ALL'
             },
             'ProvisionedThroughput': {
                  'ReadCapacityUnits': 5,
                  'WriteCapacityUnits': 5
             }
        }
    ]
    AttributeDefinitions = [
        {
            'AttributeName': 'id',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'email',
            'AttributeType': 'S'
        }
    ]
    ProvisionedThroughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    