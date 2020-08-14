import json
import datetime


def handler(event, context):
    data = {
        'event': json.dumps(event),
        'context': json.dumps(context)
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
