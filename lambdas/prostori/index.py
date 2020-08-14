import json
import boto3
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('awscodestar-vse-za-zabavo-a-infrastructure-DynamoDBTable-122E23LCYBJKL')

def handler(event, context):
    if event['httpMethod'] == "GET":
        response = table.scan()
        items = response['Items']
        return {'statusCode': 200,
            'body': json.dumps(items),
            'headers': {'Content-Type': 'application/json'}}
    elif event['httpMethod'] == "POST":
        try:
            submittedItems = json.loads(event.body)
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