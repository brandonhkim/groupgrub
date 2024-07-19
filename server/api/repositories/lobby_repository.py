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
    lobby_ID: str
    host: dict
    timestamp: str
    joinable: bool
    phase: str
    sessions: list
    preferences: dict
    categories: list
    businesses: list
    votes: list

    def __init__(self, 
                 lobby_ID: str, 
                 timestamp: str,
                 host: dict={},
                 joinable: bool = True,
                 phase: str = "setup",
                 sessions: list = [], 
                 preferences: dict = DEFAULT_PREFERENCES,
                 categories: list = [],
                 businesses: list = [],
                 votes: list = []):
        self.lobby_ID = lobby_ID
        self.host = host
        # JavaScript UTC Date format - cannot use default parameter value here b/c the datetime object will be old
        self.timestamp = timestamp if timestamp else datetime.now(timezone.utc).strftime(TIME_FORMAT)
        self.joinable = joinable
        self.phase = phase
        self.sessions = sessions
        self.preferences = preferences
        self.categories = categories
        self.businesses = businesses
        self.votes = votes

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
            'lobby_ID': kwargs['lobby_ID'],
            'host': kwargs['host'],
            'timestamp': kwargs['timestamp'],
            'joinable': kwargs['joinable'],
            'phase': kwargs['phase'],
            'sessions':  kwargs['sessions'],
            'preferences': kwargs['preferences'],
            'categories': kwargs['categories'],
            'businesses': kwargs['businesses'],
            'votes': kwargs['votes'],
        }
        self.table.put_item(Item=item)

    def get(self, lobby_ID: str) -> Lobby:
        response = self.table.get_item(
            Key={ 'lobby_ID': lobby_ID }
        )
        if 'Item' not in response:
            return None
        item = response['Item'] 
        return Lobby(
            lobby_ID=lobby_ID, 
            host=item['host'],
            timestamp=item['timestamp'],
            joinable=item['joinable'],
            phase=item['phase'],
            sessions=item['sessions'],
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
    def update_joinable(self, lobby_ID: str, joinable: bool) -> None:
        response = self.table.update_item(
            Key={
                'lobby_ID': lobby_ID,
            },
            UpdateExpression="SET joinable = :joinable",
            ExpressionAttributeValues={':joinable': joinable},
        )
        return response["Attributes"] if "Attributes" in response else None

    def update_host(self, lobby_ID: str, host: dict) -> None:
        response = self.table.update_item(
            Key={
                'lobby_ID': lobby_ID,
            },
            UpdateExpression="SET host = :host",
            ExpressionAttributeValues={':host': host},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_preferences(self, lobby_ID: str, preferences: dict) -> None:
        response = self.table.update_item(
            Key={
                'lobby_ID': lobby_ID,
            },
            UpdateExpression="SET preferences = :preferences",
            ExpressionAttributeValues={':preferences': preferences},
        )
        return response["Attributes"] if "Attributes" in response else None

    def add_session(self, lobby_ID: str, session: dict) -> None:
        lobby = self.get(lobby_ID=lobby_ID)
        if lobby and session not in lobby.sessions:
            response = self.table.update_item(
                Key={
                    'lobby_ID': lobby_ID,
                },
                UpdateExpression="SET sessions = list_append(sessions, :session)",
                ExpressionAttributeValues={':session': [{
                    "session_info": session,
                    "is_finished": False
                }]},
            )
            return response["Attributes"] if "Attributes" in response else None
    
    def remove_sessions(self, lobby_ID: str, session: dict) -> None:
        lobby = self.get(lobby_ID=lobby_ID)
        if lobby:
            for i, cur in lobby.sessions:
                if cur == session:
                    response = self.table.update_item(
                        Key={
                            'lobby_ID': lobby_ID,
                        },
                        UpdateExpression=f"REMOVE sessions[{i}]",
                    )
                    return response["Attributes"] if "Attributes" in response else None
        return None
    
    def update_sessions(self, lobby_ID: str, i: int, new_session: dict, is_finished: bool) -> None:
        response = self.table.update_item(
            Key={
                'lobby_ID': lobby_ID,
            },
            UpdateExpression=f"SET sessions[{i}] = :session",
            ExpressionAttributeValues={':session': {
                "session_info": new_session,
                "is_finished": is_finished
            }},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_timestamp(self, lobby_ID: str, timestamp: str) -> None:
        response = self.table.update_item(
            Key={
                'lobby_ID': lobby_ID,
            },
            UpdateExpression="SET #timestamp = :timestamp",
            ExpressionAttributeNames = { "#timestamp" : 'timestamp' },
            ExpressionAttributeValues={':timestamp': timestamp},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_categories(self, lobby_ID: str, categories: list) -> None:
        response = self.table.update_item(
            Key={
                'lobby_ID': lobby_ID,
            },
            UpdateExpression="SET categories = :categories",
            ExpressionAttributeValues={':categories': categories},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_businesses(self, lobby_ID: str, businesses: list) -> None:
        response = self.table.update_item(
            Key={
                'lobby_ID': lobby_ID,
            },
            UpdateExpression="SET businesses = :businesses",
            ExpressionAttributeValues={':businesses': businesses},
        )
        return response["Attributes"] if "Attributes" in response else None
    
    def update_votes(self, lobby_ID: str, votes: list) -> None:
        for i, vote in enumerate(votes):
            response = self.table.update_item(
                Key={
                    'lobby_ID': lobby_ID,
                },
                UpdateExpression="SET votes[" + str(i) + "] = if_not_exists(votes[" + str(i) + "], :zero) + :vote",
                ExpressionAttributeValues={
                    ':zero': 0,
                    ':vote': vote
                },
            )

    # Possible phases: lobby, categories, swiping, and results
    def update_phase(self, lobby_ID: str, phase: str) -> None:
        response = self.table.update_item(
            Key={
                'lobby_ID': lobby_ID,
            },
            UpdateExpression="SET phase = :newPhase",
            ExpressionAttributeValues={
                ':newPhase': phase,
            },
        )
        return response["Attributes"] if "Attributes" in response else None

    def delete(self, lobby_ID: str) -> None:
        self.table.delete_item(
            Key={
                'lobby_ID': lobby_ID,
            }
        )
        