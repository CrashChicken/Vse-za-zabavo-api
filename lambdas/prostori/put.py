import json
import boto3
from botocore.exceptions import ClientError
import datetime
import uuid
from helper import http_response

def put(table, id_prostora, id_uporabnika, data):
    spremenjeno = str(datetime.datetime.now())
    data.update({
        "spremenjeno": spremenjeno
    })
    values = {}
    expression = "set"
    for p_id, p_data in data.items():
        expression += " " + p_id + "=:" + p_id + ","
        values.update({":"+p_id: p_data})
    expression = expression[:-1]
    #return http_response({"message": expression}, 500)
    try:
        response = table.update_item(
            Key={
                'id_prostora': id_prostora,
                'id_uporabnika': id_uporabnika
            },
            UpdateExpression=expression,
            ExpressionAttributeValues=values,
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        return http_response(e.response['Error'], 500)
    else:
        message = {'data': response}
        return http_response(message, 200)