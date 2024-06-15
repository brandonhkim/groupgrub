import boto3
from uuid import uuid4
from dataclasses import dataclass
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from .repository import Repository
from .templates.table_template import TableTemplate

@dataclass
class User:
    id: str
    email: str
    password: str

    def __init__(self, email: str, password: str, id: str=None):
        self.id = id if id else uuid4().hex
        self.email = email
        self.password = password


class UserRepository(Repository[User]):
    def __init__(self) -> None:
        self.dynamodb = boto3.resource('dynamodb')
        self.dynamodb_client = boto3.client('dynamodb')
        self.table = self.create_table()
        
    def create_table(self):
        try:
            table = self.dynamodb.create_table(
                TableName = 'UserTable',
                KeySchema = TableTemplate.KeySchema,
                GlobalSecondaryIndexes = TableTemplate.GlobalSecondaryIndexes,
                AttributeDefinitions = TableTemplate.AttributeDefinitions,
                ProvisionedThroughput = TableTemplate.ProvisionedThroughput
            )
            # Wait until the table exists.
            table.wait_until_exists()
            return table
        except ClientError as error:
            if error.response['Error']['Code'] == 'ResourceInUseException':
                return self.dynamodb.Table('UserTable')
            else:
                print("WARNING: error", error.response['Error']['Code'])    

    def add(self, **kwargs: object) -> None:
            item = {
                'id': kwargs['id'],
                'email':  kwargs['email'],
                'password': kwargs['password'],
            }
            self.table.put_item(Item=item)

    def get(self, id: str="", email: str="") -> User:
        response = None
        if email and id:
            response = self.table.get_item(
                Key={
                    'id': id,
                    'email': email })
            if 'Item' not in response:
                return None
        if email and not id:
            response = self.table.query(
                IndexName='email-index',
                KeyConditionExpression=Key('email').eq(email))
        if not email and id:
            response = self.table.query(
                KeyConditionExpression=Key('id').eq(id))
        if not email and not id:
            return None
        
        if 'Items' in response and not response['Items']:
            return None
        item = response['Item'] if 'Item' in response else response['Items'][0]
        
        return User(email=item['email'], password=item['password'], id=item['id'])
    
    # NOTE: very expensive operation; should never need to call this
    def get_all(self) -> list[User]:
        return NotImplementedError

    def update(self, id: str, email: str, new_password: set) -> None:
        response = self.table.update_item(
            Key={
                'id': id,
                'email': email,
            },
            UpdateExpression='set password = :val1',
            ExpressionAttributeValues={
                ':val1': new_password
            }
        )

    def delete(self, id: str, email: str) -> None:
        self.table.delete_item(
            Key={
                'id': id,
                'email': email,
            }
        )
        