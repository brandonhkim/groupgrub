class LobbyTableTemplate:
    KeySchema = [
        {
            'AttributeName': 'lobby_ID',
            'KeyType': 'HASH'
        },
    ]
    AttributeDefinitions = [
        {
            'AttributeName': 'lobby_ID',
            'AttributeType': 'S'
        },
    ]
    ProvisionedThroughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    