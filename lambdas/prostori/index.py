import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from os import environ
import datetime
import uuid

production = False
if production:
    tableName = environ['tableName']
    dynamodb = boto3.resource('dynamodb')
else:
    tableName = "prostori"
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://172.18.0.2:8000")
    production = False
table = dynamodb.Table(tableName)

def handler(event, context):
    # Used for local testing
    if not production:
        event.update({"requestContext": {"authorizer": {"claims": {"sub": "0dac22ef-8074-4db0-9314-6d031b41c74b"}}}})
    try:
        id_prostora = event['pathParameters']['id_prostora']
    except:
        id_prostora = None
    if event['httpMethod'] == "GET":
        if id_prostora is None:
            try:
                response = table.scan()
                items = {'data': response['Items']}
            except ClientError as e:
                return http_response(str(e.response['Error']), 500)
            else:
                return http_response(items, 200)
        else:
            try:
                response = table.query(
                    KeyConditionExpression=Key('id_prostora').eq(id_prostora)
                )
            except ClientError as e:
                return http_response(e.response['Error'], 400)
            else:
                if len(response['Items']) != 0:
                    return http_response({"data": response['Items'][0]}, 200)
                else:
                    return http_response({"message": "Ta objava ne obstaja"}, 404)

    elif event['httpMethod'] == "POST":
        try:
            submittedItems = json.loads(event['body'])
        except ClientError as e:
            return http_response(str(e.response['Error']), 400)
        else:
            id_prostora = str(uuid.uuid4())
            id_uporabnika = event['requestContext']['authorizer']['claims']['sub']
            ime = submittedItems['ime']
            opis = submittedItems['opis']
            regija = submittedItems['regija']
            ustvarjeno = str(datetime.datetime.now())
            try:
                table.put_item(
                    Item={
                        'id_prostora': id_prostora,
                        'id_uporabnika': id_uporabnika,
                        'ime': ime,
                        'opis': opis,
                        'regija': regija,
                        'ustvarjeno': ustvarjeno
                    }
                )
            except ClientError as e:
                return http_response(str(e.response['Error']), 500)
            else:
                message = {'id_prostora': id_prostora}
                return http_response(message, 201)

    elif event['httpMethod'] == "DELETE":
        id_prostora = event['pathParameters']['id_prostora']
        id_uporabnika = event['requestContext']['authorizer']['claims']['sub']
        try:
            response = table.query(
                KeyConditionExpression=Key('id_prostora').eq(id_prostora)
            )
        except ClientError as e:
            return http_response(e.response['Error'], 400)
        if len(response['Items']) != 0:
            lastnik = response['Items'][0]['id_uporabnika']
        else:
            return http_response({"message": "Ta objava ne obstaja"}, 404)
        if id_uporabnika == lastnik:
            try:
                response = table.delete_item(
                    Key={
                        'id_prostora': id_prostora,
                        'id_uporabnika': id_uporabnika
                    }
                )
            except ClientError as e:
                return http_response(str(e.response['Error']), 400)
            else:
                return http_response({"message": "Objava uspešno izbrisana"}, 200)
        else:
            message = {"Message": "Nimate pravice za brsianje te objave"}
            return http_response(response, 403)

def http_response(body, code):
    return {
        'statusCode': code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }