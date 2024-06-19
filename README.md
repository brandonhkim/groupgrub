# Installation:

## Download flask dependencies via a virtual environment(venv):

### **From /groupgrub/server, run:**

### `python3 -m venv venv`

&emsp;&emsp;Creates a virtual environment

### `source venv/bin/activate`

&emsp;&emsp;Activates the virtual environment

### `pip install -r ./requirements.txt`

&emsp;&emsp;Downloads dependencies through pip package installer

### `deactivate`

&emsp;&emsp;Deactivates the virtual environment, allowing you to exit

## Load your API Keys in .env files

### Find ***/groupgrub/.env/*** AND ***/groupgrub/client/.env/***

&emsp;&emsp;Replace placeholders with your API keys

# Running the Project

From the project directory, run:

### `yarn --cwd ./client/ start-api`

&emsp;&emsp;Starts up the backend

### `yarn --cwd ./client/ start`

&emsp;&emsp;Starts up the frontend

### `redis-server`

&emsp;&emsp;Start up redis for Flask-Sessions

&emsp;&emsp;This should be ran in its own terminal window

# Changes in the future:
Switch from NoSQL to SQL

&emsp;&emsp;DynamoDB(NoSQL) -> AWS RDS(SQL)

