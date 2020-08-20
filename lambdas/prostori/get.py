import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from helper import http_response

def getList(table):
    try:
        response = table.scan()
        items = {'data': response['Items']}
    except ClientError as e:
        return http_response(e.response['Error'], 500)
    else:
        return http_response(items, 200)

def getSingle(table, id_prostora):
    try:
        response = table.query(
            KeyConditionExpression=Key('id_prostora').eq(id_prostora)
        )
    except ClientError as e:
        return http_response(e.response['Error'], 500)
    else:
        if len(response['Items']) != 0:
            return http_response({"data": response['Items'][0]}, 200)
        else:
            return http_response({"message": "Ta objava ne obstaja"}, 404)