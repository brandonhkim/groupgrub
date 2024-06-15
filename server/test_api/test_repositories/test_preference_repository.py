import pytest
from moto import mock_aws
from api.repositories.templates.table_template import TableTemplate
from api.repositories.preference_repository import IGNORE_STRING
from api.repositories.preference_repository import Preference, PreferenceRepository

TEST_ID = "test"
TEST_EMAIL = "test@email.com"
TEST_PREFERENCES = set([IGNORE_STRING, "test", "preferences"])

@pytest.fixture
def my_preference() -> Preference:
    return Preference(id=TEST_ID, email=TEST_EMAIL, preferences=TEST_PREFERENCES)

class TestPreference:
    def test_init(self, my_preference):
        assert my_preference.id == TEST_ID
        assert my_preference.email == TEST_EMAIL
        assert my_preference.preferences == TEST_PREFERENCES

class TestPreferenceRepository:
    @mock_aws
    def test_create_table(self):
        dummy_repository = PreferenceRepository()
        dummy_table = dummy_repository.table

        # Get TableTemplate's attributes, updating any that change upon Table creation
        key_schema = TableTemplate.KeySchema
        global_secondary_indexes = dict(TableTemplate.GlobalSecondaryIndexes[0], IndexStatus= 'ACTIVE')
        attribute_definitions = TableTemplate.AttributeDefinitions
        provisioned_throughput = dict(TableTemplate.ProvisionedThroughput, NumberOfDecreasesToday= 0)

        # Assertions:
        assert dummy_table.name == 'PreferenceTable', 'name did not match'
        assert dummy_table.key_schema == key_schema, 'key_schema did not mach'
        assert dummy_table.global_secondary_indexes[0] == global_secondary_indexes, 'secondary indexes did not match'
        assert dummy_table.attribute_definitions == attribute_definitions, 'attribute definitions did not match'
        assert dummy_table.provisioned_throughput == provisioned_throughput, 'provisioned throughput did not match'

    @mock_aws
    def test_add(self, my_preference):
        dummy_repository = PreferenceRepository()
        dummy_table = dummy_repository.table

        # Test add to the table and get its scan
        dummy_repository.add(**vars(my_preference))
        scan = dummy_table.scan()

        assert 'Items' in scan
        assert len(scan['Items']) == 1
        assert Preference(**scan['Items'][0]) == my_preference

    @mock_aws
    def test_get_id_exists(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()
        dummy_repository.add(**vars(my_preference))

        # Get Preference w/ parameter 'id'
        response = dummy_repository.get(id=my_preference.id)

        # Assert Preference is returned correctly
        assert response == my_preference

    @mock_aws
    def test_get_email_exists(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()
        dummy_repository.add(**vars(my_preference))

        # Get Preference w/ parameter 'email'
        response = dummy_repository.get(email=my_preference.email)

        # Assert Preference is returned correctly
        assert response == my_preference

    @mock_aws
    def test_get_both_exists(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()
        dummy_repository.add(**vars(my_preference))

        # Get Preference w/ parameters 'id' and 'email'
        response = dummy_repository.get(id=my_preference.id, email=my_preference.email)

        # Assert Preference is returned correctly
        assert response == my_preference

    @mock_aws
    def test_get_none_exists(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()
        dummy_repository.add(**vars(my_preference))

        # Get Preference w/ no parameters
        response = dummy_repository.get()

        # Assert Preference is returned correctly
        assert response == None
    
    @mock_aws
    def test_get_id_absent(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()

        #dummy_repository.delete(id=my_preference.id, email=my_preference.email)
        # Get Preference w/ parameter 'id'
        response = dummy_repository.get(id=my_preference.id)

        print(response)

        # Assert Preference is returned correctly
        assert response == None

    @mock_aws
    def test_get_email_absent(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()

        # Get Preference w/ parameter 'email'
        response = dummy_repository.get(email=my_preference.email)

        # Assert Preference is returned correctly
        assert response == None

    @mock_aws
    def test_get_both_absent(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()

        # Get Preference w/ parameters 'id' and 'email'
        response = dummy_repository.get(id=my_preference.id, email=my_preference.email)

        # Assert Preference is returned correctly
        assert response == None

    @mock_aws
    def test_get_none_absent(self):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()

        # Get Preference w/ no parameters
        response = dummy_repository.get()

        # Assert Preference is returned correctly
        assert response == None
    
    @mock_aws
    def test_get_all(self):
        dummy_repository = PreferenceRepository()
        assert dummy_repository.get_all() == NotImplementedError

    @mock_aws
    def test_update(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()
        dummy_repository.add(**vars(my_preference))

        # Update the existing entry
        new_preferences = set(['UPDATED', 'PREFERENCES']).union(my_preference.preferences)
        dummy_repository.update(id=my_preference.id, email=my_preference.email, new_preferences=new_preferences)

        # Get the updated entry
        response = dummy_repository.get(id=my_preference.id, email=my_preference.email)

        # Assert that the preferences were updated
        assert response.preferences == new_preferences
    
    @mock_aws
    def test_delete(self, my_preference):
        # Create Repository Object and add a test Preference Object
        dummy_repository = PreferenceRepository()
        dummy_repository.add(**vars(my_preference))

        # Delete the existing entry
        dummy_repository.delete(id=my_preference.id, email=my_preference.email)

        # Try to get the updated entry
        response = dummy_repository.get(id=my_preference.id, email=my_preference.email)

        # Assert that the entry no longer exists
        assert response == None
    