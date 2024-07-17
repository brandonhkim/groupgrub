import boto3
from uuid import uuid4
from datetime import datetime, timezone
from dataclasses import dataclass
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from .repository import Repository
from .templates.lobby_table_template import LobbyTableTemplate

TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'
DEFAULT_PREFERENCES = {
    "coordinates": {
        "latitude": 91,
        "longitude": 181,
        "name": ""
    },
    "numResults": "10",
    "driveRadius": "5",
    "priceRange": "$"
}

@dataclass 
class Lobby:
    lobbyID: str
    host: str
    timestamp: str
    joinable: bool
    phase: str
    sockets: dict
    preferences: dict
    categories: list
    businesses: list
    votes: list

    def __init__(self, 
                 lobbyID: str, 
                 timestamp: str,
                 host: str="",
                 joinable: bool = True,
                 phase: str = "setup",
                 sockets: dict = {}, 
                 preferences: dict = DEFAULT_PREFERENCES,
                 categories: list = [],
                 businesses: list = [],
                 votes: list = []):
        self.lobbyID = lobbyID
        self.host = host
        # JavaScript UTC Date format - cannot use default parameter value here b/c the datetime object will be old
        self.timestamp = timestamp if timestamp else datetime.now(timezone.utc).strftime(TIME_FORMAT)
        self.joinable = joinable
        self.phase = phase
        self.sockets = sockets
        self.preferences = preferences
        self.categories = categories
        self.businesses = businesses
        self.votes = votes

'''
lobbyID (Parition key): ID's of each existing lobby
sockets: Map of Socket ID's (keys) in the lobby AND bools 
        representing if they're doine swiping (values)
categories: Array where indices are objects: 
    { 
        name: "CategoryName",
        sockets: ["Socket1", "Socket2", "Socket3"]
    }
'''
class LobbyRepository(Repository[Lobby]):
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.dynamodb_client = boto3.client('dynamodb')
        self.table = self.create_table()
        
    def create_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName = 'LobbyTable',
                KeySchema = LobbyTableTemplate.KeySchema,
                AttributeDefinitions = LobbyTableTemplate.AttributeDefinitions,
                ProvisionedThroughput = LobbyTableTemplate.ProvisionedThroughput
            )
            # Wait until the table exists.
            table.wait_until_exists()
            return table
        except ClientError as error:
            if error.response['Error']['Code'] == 'ResourceInUseException':
                return self.dynamodb.Table('LobbyTable')
            else:
                print("WARNING: error", error.response['Error']['Code'])    

    def add(self, **kwargs: object) -> None:
        item = {
            'lobbyID': kwargs['lobbyID'],
            'host': kwargs['host'],
            'timestamp': kwargs['timestamp'],
            'joinable': kwargs['joinable'],
            'phase': kwargs['phase'],
            'sockets':  kwargs['sockets'],
            'preferences': kwargs['preferences'],
            'categories': kwargs['categories'],
            'businesses': kwargs['businesses'],
            'votes': kwargs['votes'],
        }
        print(item)
        self.table.put_item(Item=item)

    def get(self, lobbyID: str) -> Lobby:
        response = self.table.get_item(
            Key={ 'lobbyID': lobbyID }
        )
        if 'Item' not in response:
            return None
        item = response['Item'] 
        return Lobby(
            lobbyID=lobbyID, 
            host=item['host'],
            timestamp=item['timestamp'],
            joinable=item['joinable'],
            phase=item['phase'],
            sockets=item['sockets'],
            preferences=item['preferences'],
            categories=item['categories'],
            businesses=item['businesses'],
            votes=item['votes'])
    
    # NOTE: Expensive operation, should never (need to) call this
    def get_all(self) -> list[Lobby]:
        return NotImplementedError
    
    # Not defined in exchange for better method names
    def update(self) -> None:
        return NotImplementedError
    
    # TODO: Update method return types
    def update_joinable(self, lobbyID: str, joinable: bool) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET joinable = :joinable",
            ExpressionAttributeValues={':joinable': joinable},
        )
        return response["Attributes"] if "Attributes" in response else None

    def update_host(self, lobbyID: str, host: str) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET host = :host",
            ExpressionAttributeValues={':host': host},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_preferences(self, lobbyID: str, preferences: dict) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET preferences = :preferences",
            ExpressionAttributeValues={':preferences': preferences},
        )
        return response["Attributes"] if "Attributes" in response else None

    def add_sockets(self, lobbyID: str, socketID: str) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET sockets.#socketID = :false",
            ExpressionAttributeNames = { "#socketID" : socketID },
            ExpressionAttributeValues={':false': False},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def remove_sockets(self, lobbyID: str, socketID: str) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="REMOVE sockets.#socketID",
            ExpressionAttributeNames = { "#socketID" : socketID },
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_sockets(self, lobbyID: str, socketID: str) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET sockets.#socketID = :true",
            ExpressionAttributeNames = { "#socketID" : socketID },
            ExpressionAttributeValues={':true': True},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_timestamp(self, lobbyID: str) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET #timestamp = :timestamp",
            ExpressionAttributeNames = { "#timestamp" : 'timestamp' },
            ExpressionAttributeValues={':timestamp': datetime.now(timezone.utc).strftime(TIME_FORMAT)},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_categories(self, lobbyID: str, categories: list) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET categories = :categories",
            ExpressionAttributeValues={':categories': categories},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_businesses(self, lobbyID: str, businesses: list) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET businesses = :businesses",
            ExpressionAttributeValues={':businesses': businesses},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_votes(self, lobbyID: str, votes: list) -> None:
        for i, vote in enumerate(votes):
            response = self.table.update_item(
                Key={
                    'lobbyID': lobbyID,
                },
                UpdateExpression="SET votes[" + str(i) + "] = if_not_exists(votes[" + str(i) + "], :zero) + :vote",
                ExpressionAttributeValues={
                    ':zero': 0,
                    ':vote': vote
                },
            )

    '''
    lobby, categories, swiping, and results Phases
    '''
    def update_phase(self, lobbyID: str, phase: str) -> None:
        response = self.table.update_item(
            Key={
                'lobbyID': lobbyID,
            },
            UpdateExpression="SET phase = :newPhase",
            ExpressionAttributeValues={
                ':newPhase': phase,
            },
        )
        return response["Attributes"] if "Attributes" in response else None

    def delete(self, lobbyID: str) -> None:
        self.table.delete_item(
            Key={
                'lobbyID': lobbyID,
            }
        )
        