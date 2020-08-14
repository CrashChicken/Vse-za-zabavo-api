import json
import datetime


def handler(event, context):
    if event.httpMethod == "GET":
        data = {
            'output': 'GET',
            'timestamp': datetime.datetime.utcnow().isoformat()
        }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
