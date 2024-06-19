# Installation:

## Download required JavaScript libraries via npm:

### **From /groupgrub/client, run:**

### `npm install`

&emsp;&emsp;Uses Node Packet Manager(npm) to install all necessary libraries

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

### Find **_/groupgrub/.env/_** AND **_/groupgrub/client/.env/_**

&emsp;&emsp;Replace placeholders with your API keys

# Running the Project

### `redis-server`

In its own separate terminal window,

&emsp;&emsp;Start up redis for Flask-Sessions

From the project directory, run:

### `yarn --cwd ./client/ start-api`

&emsp;&emsp;Starts up the backend

### `yarn --cwd ./client/ start`

&emsp;&emsp;Starts up the frontend

# Testing the Project

From the project directory, run:

### `yarn --cwd ./client/ test-api`

&emsp;&emsp;Runs pytest script to test all the backend api code

# Running Tests




# Changes in the future:

Switch from NoSQL to SQL

&emsp;&emsp;DynamoDB(NoSQL) -> AWS RDS(SQL)
