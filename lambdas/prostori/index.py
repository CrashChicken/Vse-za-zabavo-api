import json
import boto3
from botocore.exceptions import ClientError
from uuid import UUID
from os import environ
from prostori import Prostori

production = True
if production:
    tableName = environ['tableName']
    dynamodb = boto3.resource('dynamodb')
else:
    tableName = "prostori"
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://172.18.0.2:8000")
table = dynamodb.Table(tableName)

def handler(event, context):
    # Used for local testing
    # Account: jan@gradic.net
    if not production:
        event.update({"requestContext": {"authorizer": {"claims": {"sub": "0dac22ef-8074-4db0-9314-6d031b41c74b"}}}})
    try:
        id_prostora = event['pathParameters']['id_prostora']
    except:
        id_prostora = None

    try:
        id_uporabnika = event['requestContext']['authorizer']['claims']['sub']
    except:
        id_uporabnika = None

    if id_prostora is not None:
        try:
            UUID(id_prostora, version=4)
        except:
            return http_response({"message": "ID ni v pravilni obliki"}, 400)

    if event['httpMethod'] == "GET":
        if id_prostora is None:
            try:
                response = table.scan()
                items = {'data': response['Items']}
            except ClientError as e:
                return http_response(e.response['Error'], 500)
            else:
                return http_response(items, 200)
        else:
            prostor = Prostori(table)
            try:
                prostor.get(id_prostora)
            except Exception as e:
                return http_response({"message": str(e)}, 400)
            
            return http_response({"data": prostor.get_all()}, 200)

    elif event['httpMethod'] == "POST":
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError as e:
            return http_response(e.msg, 400)
        
        prostor = Prostori(table)
        prostor.create(id_uporabnika)

        try:
            prostor.set_all(body)
        except Exception as e:
            return http_response({"message": str(e)}, 400)

        try:
            response = prostor.save()
        except Exception as e:
            return http_response({"message": str(e)}, 400)
        return http_response({"data": prostor.id_prostora}, 201)

    elif event['httpMethod'] == "PUT":
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError as e:
            return http_response(e.msg, 400)

        prostor = Prostori(table)
        prostor.get(id_prostora)
        if prostor.id_uporabnika == id_uporabnika:
            try:
                prostor.set_all(body)
            except Exception as e:
                return http_response({"message": str(e)}, 400)
        else:
            message = {"message": "Nimate pravice za urejanje te objave"}
            return http_response(message, 403)
        try:
            response = prostor.save()
        except Exception as e:
            return http_response({"message": str(e)}, 400)
        return http_response({"data": response}, 201)


    elif event['httpMethod'] == "DELETE":
        prostor = Prostori(table)
        prostor.get(id_prostora)
        if prostor.id_uporabnika != id_uporabnika:
            message = {"message": "Nimate pravice za brisanje te objave"}
            return http_response(message, 403)
        try:
            response = prostor.delete()
        except Exception as e:
            return http_response({"message": str(e)}, 400)
        return http_response({"data": response}, 200)

def http_response(body, code):
    return {
        'statusCode': code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }