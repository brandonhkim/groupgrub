import boto3
from dataclasses import dataclass
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from .repository import Repository
from .templates.table_template import TableTemplate

IGNORE_STRING = "IGNORE_STR" # required to set "preferences" column as a String Set

@dataclass
class Preference:
    id: str
    email: str
    preferences: set

    def __init__(self, id: str, email: str, preferences: set = set([IGNORE_STRING])):
        self.id = id
        self.email = email
        self.preferences = preferences


class PreferenceRepository(Repository[Preference]):
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.dynamodb_client = boto3.client('dynamodb')
        self.table = self.create_table()
        
    def create_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName = 'PreferenceTable',
                KeySchema = TableTemplate.KeySchema,
                GlobalSecondaryIndexes = TableTemplate.GlobalSecondaryIndexes,
                AttributeDefinitions = TableTemplate.AttributeDefinitions,
                ProvisionedThroughput = TableTemplate.ProvisionedThroughput
            )
            table.wait_until_exists()
            return table
        except ClientError as error:
            if error.response['Error']['Code'] == 'ResourceInUseException':
                return self.dynamodb.Table('PreferenceTable')
            else:
                print("WARNING: error", error.response['Error']['Code'])
                return None
    
    def add(self, **kwargs: object) -> None:
        item = {
            'id':  kwargs['id'],
            'email': kwargs['email'],
            'preferences': kwargs['preferences'],
        }
        self.table.put_item(Item=item)

    def get(self, id: str="", email: str="") -> Preference:
        response = None
        if id and email:
            response = self.table.get_item(
                Key={
                    'id': id,
                    'email': email })
            if 'Item' not in response:
                return None
        if id and not email:
            response = self.table.query(
                KeyConditionExpression=Key('id').eq(id))
        if not id and email:
            response = self.table.query(
                IndexName='email-index',
                KeyConditionExpression=Key('email').eq(email))
        if not id and not email:
            return None
    
        if 'Items' in response and not response['Items']:
            return None
        item = response['Item'] if 'Item' in response else response['Items'][0]

        return Preference(id=item['id'], email=item['email'], preferences=item['preferences'])
    
    # NOTE: very expensive operation; should never need to call this
    def get_all(self) -> list[Preference]:
        return NotImplementedError
    
    def update(self, id: str, email: str, new_preferences: set) -> dict:
        new_preferences.add(IGNORE_STRING)
        response = self.table.update_item(
            Key={
                'id': id,
                'email': email,
            },
            UpdateExpression='add preferences :val1',
            ExpressionAttributeValues={
                ':val1': new_preferences
            },
            ReturnValues="UPDATED_NEW",
        )

        return response["Attributes"]
    
    def delete(self, id: str, email: str) -> None:
        self.table.delete_item(
            Key={
                'id': id,
                'email': email,
            }
        )
        