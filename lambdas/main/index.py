import json
import datetime


def handler(event, context):
    data = {
        'event': event,
        'context': context
    }
    return {'statusCode': 200,
            'body': json.dumps(data),
            'headers': {'Content-Type': 'application/json'}}
