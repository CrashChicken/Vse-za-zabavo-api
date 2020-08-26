import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# def is_allowed()

def get_owner(table, id_prostora):
    try:
        response = table.query(
            KeyConditionExpression=Key('id_prostora').eq(id_prostora)
        )
    except:
        return None
    if len(response['Items']) != 0:
        return response['Items'][0]['id_uporabnika']
    else:
        return None

def http_response(body, code):
    return {
        'statusCode': code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }