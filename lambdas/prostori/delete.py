import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from helper import http_response

def delete(table, id_prostora, id_uporabnika):
    try:
        response = table.delete_item(
            Key={
                'id_prostora': id_prostora,
                'id_uporabnika': id_uporabnika
            }
        )
    except ClientError as e:
        return http_response(e.response['Error'], 500)
    else:
        return http_response({"message": "Objava uspešno izbrisana"}, 200)