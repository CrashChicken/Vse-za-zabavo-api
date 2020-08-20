import json
import boto3
from botocore.exceptions import ClientError
import datetime
import uuid
from helper import http_response

def post(table, data):
    id_prostora = str(uuid.uuid4())
    ustvarjeno = str(datetime.datetime.now())
    data.update({
        "id_prostora": id_prostora,
        "ustvarjeno": ustvarjeno
    })
    try:
        table.put_item(Item=data)
    except ClientError as e:
        return http_response(e.response['Error'], 500)
    except Exception as e:
        return http_response({"message": str(e)}, 500)
    else:
        message = {'id_prostora': id_prostora}
        return http_response(message, 201)