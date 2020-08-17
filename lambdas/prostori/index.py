import json
import boto3
import os
import datetime
import uuid

tableName = os.environ['tableName']
dynamodb = boto3.resource('dynamodb')
#tableName = "prostori"
#dynamodb = boto3.resource('dynamodb', endpoint_url="http://172.18.0.2:8000")
table = dynamodb.Table(tableName)

def handler(event, context):
    
    if event['httpMethod'] == "GET":
        try:
            response = table.scan()
            items = {'data': response['Items']}
        except Exception as e:
            message = {'error': str(e)}
            return http_response(message, 500)
        else:
            return http_response(items, 200)

    elif event['httpMethod'] == "POST":
        try:
            submittedItems = json.loads(event['body'])
        except:
            message = {'error': 'JSON ni pravilno oblikovan'}
            return http_response(message, 400)
        else:
            id_prostora = str(uuid.uuid4())
            try:
                table.put_item(
                    Item={
                        'id_prostora': id_prostora,
                        'id_uporabnika': event['requestContext']['authorizer']['claims']['cognito:username'],
                        'ime': submittedItems['ime'],
                        'opis': submittedItems['opis'],
                        'regija': submittedItems['regija'],
                        'ustvarjeno': datetime.datetime.now()
                    }
                )
            except:
                message = {'error': 'Podatki niso bili shranjeni'}
                return http_response(message, 500)
            else:
                message = {'id_prostora': id_prostora}
                return http_response(message, 201)

    elif event['httpMethod'] == "DELETE":
        try:
            response = table.delete_item(
                Key={
                    'id_prostora': event['pathParameters']['id_prostora'],
                    'id_uporabnika': event['requestContext']['authorizer']['claims']['cognito:username']
                }
            )
        except ClientError as e:
            return http_response(e, 400)
        else:
            return http_response(response, 200)
def http_response(body, code):
    return {
        'statusCode': code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }