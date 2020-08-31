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
from helper import http_response, get_owner, json_data

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
            data = json_data(body)
        except Exception as e:
            return http_response({"message": str(e)}, 400)
        else:
            data.update({"id_uporabnika": id_uporabnika})
            return post(table, data)

    elif event['httpMethod'] == "PUT":
        owner = get_owner(table, id_prostora)
        if owner is None:
            message = {"message": "Ta objava ne obstaja"}
            return http_response(message, 404)
        if id_uporabnika != owner:
            message = {"message": "Nimate pravice za urejanje te objave"}
            return http_response(message, 403)
        try:
            body = json.loads(event['body'])
        except json.JSONDecodeError as e:
            return http_response(e.msg, 400)
        try:
            data = json_data(body)
        except Exception as e:
            return http_response({"message": str(e)}, 400)
        else:
            if len(data) > 0:
                return put(table, id_prostora, id_uporabnika, data)
            else:
                return http_response({"message": "Ni definiranih sprememb"}, 400)

    elif event['httpMethod'] == "DELETE":
        owner = get_owner(table, id_prostora)
        if owner is None:
            message = {"message": "Ta objava ne obstaja"}
            return http_response(message, 404)
        if id_uporabnika != owner:
            message = {"message": "Nimate pravice za urejanje te objave"}
            return http_response(message, 403)
        else:
            return delete(table, id_prostora, owner)