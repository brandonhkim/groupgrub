'''
The following Repository Tests rely on the assumption that only valid inputs are being passed into Repository methods.
- This can be assumed as ALL 'Input Validation' is done within its respective Flask Route before being passed to the
Repository


in the venv, run:
    'python3 -m pytest -v -W ignore'

TODO:
    look into pytest.ini for warnings

Notes:
- Do not create DynamoDB Table in a fixture as moto will not be able to make mock calls to it
by the time it enters the test function

'''