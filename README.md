# MultiLevelHealthCheck
A MultiLevelHealthCheck for APIs and their dependent downstream systems

## config.yaml
Use this configuration file to define your API entry points and mention dependent APIs/downstream systems

## test.sh
Run tests for all your APIs through curl

## api*.py

Run each of your APIs independently through the command 
uvicorn api1/api1 --reload --port 9001

Run the app.py to test all the apis together 
uvicorn app/app --reload --port 8000
