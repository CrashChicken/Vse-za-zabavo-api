import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from uuid import UUID
from os import environ
from get import getList, getSingle
from post import post
from put import put
from delete import delete
from helper import http_response

production = True
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
            return getList(table)
        else:
            return getSingle(table, id_prostora)

    elif event['httpMethod'] == "POST":
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError as e:
            return http_response(e.msg, 400)
        try:
            ime = body['ime']
            opis = body['opis']
            regija = body['regija']
        except Exception as e:
            return http_response({"message": "Manjkajoči podatki"}, 400)
        else:
            data = {
                "id_uporabnika": id_uporabnika,
                "ime:": ime,
                "opis": opis,
                "regija": regija
            }
            return post(table, data)

    elif event['httpMethod'] == "PUT":
        try:
            response = table.query(
                KeyConditionExpression=Key('id_prostora').eq(id_prostora)
            )
        except ClientError as e:
            return http_response(e.response['Error'], 500)
        if len(response['Items']) != 0:
            lastnik = response['Items'][0]['id_uporabnika']
        else:
            return http_response({"message": "Ta objava ne obstaja"}, 404)
        if id_uporabnika != lastnik:
            message = {"Message": "Nimate pravice za urejanje te objave"}
            return http_response(message, 403)
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError as e:
            return http_response(e.msg, 400)
        data = {}
        keys = ["ime", "opis", "regija"]
        for item in keys:
            if item in body:
                data.update({item: body[item]})
        return put(table, id_prostora, id_uporabnika, data)

    elif event['httpMethod'] == "DELETE":
        try:
            response = table.query(
                KeyConditionExpression=Key('id_prostora').eq(id_prostora)
            )
        except ClientError as e:
            return http_response(e.response['Error'], 500)
        if len(response['Items']) != 0:
            lastnik = response['Items'][0]['id_uporabnika']
        else:
            return http_response({"message": "Ta objava ne obstaja"}, 404)
        if id_uporabnika == lastnik:
            return delete(table, id_prostora, lastnik)
        else:
            message = {"Message": "Nimate pravice za brsianje te objave"}
            return http_response(message, 403)