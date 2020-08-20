import json

def http_response(body, code):
    return {
        'statusCode': code,
        'body': json.dumps(body),
        'headers': {'Content-Type': 'application/json'}
    }