import pytest
from moto import mock_aws
from api.repositories.templates.user_table_template import UserTableTemplate
from api.repositories.user_repository import User, UserRepository

TEST_ID = "test"
TEST_EMAIL = "test@email.com"
TEST_PASSWORD = "abc123"    # <-- not my actual password
TEST_PREFERENCES = {
    "TEST" : {
        "name" : "TEST",
        "code" : "TEST_code"
    }
}

@pytest.fixture
def my_user() -> User:
    return User(email=TEST_EMAIL, password=TEST_PASSWORD, id=TEST_ID, preferences=TEST_PREFERENCES)

class TestUser:
    def test_init_id(self, my_user):
        assert my_user.id == TEST_ID
        assert my_user.email == TEST_EMAIL
        assert my_user.password == TEST_PASSWORD
        assert my_user.preferences == TEST_PREFERENCES
    
    def test_init_none(self):
        user = User(email=TEST_EMAIL, password=TEST_PASSWORD, preferences=TEST_PREFERENCES)

        assert int(user.id, 16) and user.id.islower()
        assert user.email == TEST_EMAIL
        assert user.password == TEST_PASSWORD
        assert user.preferences == TEST_PREFERENCES

class TestUserRepository:
    @mock_aws
    def test_create_table(self):
        dummy_repository = UserRepository()
        dummy_table = dummy_repository.table

        # Get UserTableTemplate's attributes, updating any that change upon Table creation
        key_schema = UserTableTemplate.KeySchema
        global_secondary_indexes = dict(UserTableTemplate.GlobalSecondaryIndexes[0], IndexStatus= 'ACTIVE')
        attribute_definitions = UserTableTemplate.AttributeDefinitions
        provisioned_throughput = dict(UserTableTemplate.ProvisionedThroughput, NumberOfDecreasesToday= 0)

        # Assertions:
        assert dummy_table.name == 'UserTable', 'name did not match'
        assert dummy_table.key_schema == key_schema, 'key_schema did not mach'
        assert dummy_table.global_secondary_indexes[0] == global_secondary_indexes, 'secondary indexes did not match'
        assert dummy_table.attribute_definitions == attribute_definitions, 'attribute definitions did not match'
        assert dummy_table.provisioned_throughput == provisioned_throughput, 'provisioned throughput did not match'

    @mock_aws
    def test_add(self, my_user):
        dummy_repository = UserRepository()
        dummy_table = dummy_repository.table

        # Test add to the table and get its scan
        dummy_repository.add(**vars(my_user))
        scan = dummy_table.scan()

        assert 'Items' in scan
        assert len(scan['Items']) == 1
        assert User(**scan['Items'][0]) == my_user

    @mock_aws
    def test_get_id_exists(self, my_user):
        # Create Repository Object and add a test Preference Object
        dummy_repository = UserRepository()
        dummy_repository.add(**vars(my_user))

        # Get User w/ parameter 'id'
        response = dummy_repository.get(id=my_user.id)

        # Assert User is returned correctly
        assert response == my_user

    @mock_aws
    def test_get_email_exists(self, my_user):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()
        dummy_repository.add(**vars(my_user))

        # Get User w/ parameter 'email'
        response = dummy_repository.get(email=my_user.email)

        # Assert User is returned correctly
        assert response == my_user

    @mock_aws
    def test_get_both_exists(self, my_user):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()
        dummy_repository.add(**vars(my_user))

        # Get User w/ parameters 'id' and 'email'
        response = dummy_repository.get(id=my_user.id, email=my_user.email)

        # Assert User is returned correctly
        assert response == my_user

    @mock_aws
    def test_get_none_exists(self, my_user):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()
        dummy_repository.add(**vars(my_user))

        # Get User w/ no parameters
        response = dummy_repository.get()

        # Assert User is returned correctly
        assert response == None
    
    @mock_aws
    def test_get_id_absent(self, my_user):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()

        # Get User w/ parameter 'id'
        response = dummy_repository.get(id=my_user.id)

        # Assert User is returned correctly
        assert response == None

    @mock_aws
    def test_get_email_absent(self, my_user):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()

        # Get User w/ parameter 'email'
        response = dummy_repository.get(email=my_user.email)

        # Assert User is returned correctly
        assert response == None

    @mock_aws
    def test_get_both_absent(self, my_user):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()

        # Get User w/ parameters 'id' and 'email'
        response = dummy_repository.get(id=my_user.id, email=my_user.email)

        # Assert User is returned correctly
        assert response == None

    @mock_aws
    def test_get_none_absent(self):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()

        # Get User w/ no parameters
        response = dummy_repository.get()

        # Assert User is returned correctly
        assert response == None
    
    @mock_aws
    def test_get_all(self):
        dummy_repository = UserRepository()
        assert dummy_repository.get_all() == NotImplementedError

    @mock_aws
    def test_update_preference(self, my_user):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()
        dummy_repository.add(**vars(my_user))

        # Update the existing entry
        new_preferences = {
            "name": {
                "name": "test_name",
                "code": "test_code"
            }
        }
        dummy_repository.update(id=my_user.id, email=my_user.email, new_preferences=new_preferences)

        # Get the updated entry
        response = dummy_repository.get(id=my_user.id, email=my_user.email)

        # Assert that the preferences were updated
        assert response.preferences == new_preferences | TEST_PREFERENCES

    @mock_aws
    def test_update_password(self, my_user):
        # Create Repository Object and add a test User Object
        dummy_repository = UserRepository()
        dummy_repository.add(**vars(my_user))

        # Update the existing entry
        new_password = "321cba" # <-- Might be one of my passwords
        dummy_repository.update_password(id=my_user.id, email=my_user.email, new_password=new_password)

        # Get the updated entry
        response = dummy_repository.get(id=my_user.id, email=my_user.email)

        # Assert that the preferences were updated
        assert response.password == new_password
    
    @mock_aws
    def test_delete(self, my_user):
        # Create Repository Object and add a test Preference Object
        dummy_repository = UserRepository()
        dummy_repository.add(**vars(my_user))

        # Delete the existing entry
        dummy_repository.delete(id=my_user.id, email=my_user.email)

        # Try to get the updated entry
        response = dummy_repository.get(id=my_user.id, email=my_user.email)

        # Assert that the entry no longer exists
        assert response == None
    
    