class LobbyTableTemplate:
    KeySchema = [
        {
            'AttributeName': 'lobbyID',
            'KeyType': 'HASH'
        },
    ]
    AttributeDefinitions = [
        {
            'AttributeName': 'lobbyID',
            'AttributeType': 'S'
        },
    ]
    ProvisionedThroughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    