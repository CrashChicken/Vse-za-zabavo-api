import json
import boto3
import os
import datetime

tableName = os.environ['tableName']
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tableName)

def handler(event, context):
    if event['httpMethod'] == "GET":
        response = table.scan()
        items = response['Items']
        return {'statusCode': 200,
            'body': json.dumps(items),
            'headers': {'Content-Type': 'application/json'}}
    elif event['httpMethod'] == "POST":
        try:
            submittedItems = json.loads(event['body'])
        except:
            message = {'error': 'JSON ni pravilno oblikovan'}
            return {
                'statusCode': 400,
                'body': json.dumps(message),
                'headers': {'Content-Type': 'application/json'}
            }
        table.put_item(
            Item={
                'id_prostora': submittedItems['id_prostora'],
                'uporabnik': event['requestContext']['authorizer']['claims']['cognito:username'],
                'ime': submittedItems['ime'],
                'opis': submittedItems['opis'],
                'regija': submittedItems['regija'],
            }
        )
        message = {'id_prostora': submittedItems['id_prostora']}
        return {'statusCode': 201,
                'body': json.dumps(message),
                'headers': {'Content-Type': 'application/json'}}