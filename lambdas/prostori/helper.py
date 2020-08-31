import json
import re
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

# def is_allowed()

allowed_keys = ["ime", "tip", "kratek-opis", "dolg-opis", "regija", "naslov", "posta", "kraj", "telefon", "email"]

def json_data(data):
    parsed_data = {}
    for key, value in data.items():
        if key in allowed_keys:
            parsed = parser(key, value)
            if parsed is not None:
                parsed_data.update(parsed)
    return parsed_data

def parser(key, value):
    regije = ["osrednjeslovenska", "podravska", "koroška", "pomurska", "savinjska", "zasavska", "gorenjska", "goriška", "notranjsko kraška", "obalna", "spodnjeposavska", "dolenjska"]
    tipi = ["šotor", "dvorana"]
    if key == "ime":
        if len(value) <= 60:
            return {key, value}
        else:
            raise Exception("Ime objave je dolgo več kot 60 znakov")

    elif key == "tip":
        if value.lower() in tipi:
            return {key, value.lower()}
        else:
            raise Exception("Vnešen tip ni pravilen")

    elif key == "kratek-opis":
        if len(value) <= 160:
            return {key, value}
        else:
            raise Exception("Kratek opis je dolg več kot 160 znakov")

    elif key == "dolg-opis":
        if len(value) <= 10000:
            return {key, value}
        else:
            raise Exception("Dolg opis je dolg več kot 10000 znakov")

    elif key == "regija":
        if value.lower() in regije:
            return {key, value.lower()}
        else:
            raise Exception("Vnešena regija ni pravilna")

    elif key == "naslov":
        if len(value) <= 60:
            return {key, value}
        else:
            raise Exception("Naslov je dolg več kot 60 znakov")

    elif key == "posta":
        try:
            value = int(value)
        except:
            raise Exception("Vnešena poštna številka ni številka") 
        if 1000 <= value <= 9999:
            return {key, value}
        else:
            raise Exception("Vnešena poštna številka ni med 1000 in 9999")

    elif key == "kraj":
        if len(value) <= 60:
            return {key, value}
        else:
            raise Exception("Kraj je dolg več kot 60 znakov")

    elif key == "telefon":
        if not len(value) <= 12:
            raise Exception("Telefonska številka je dolga več kot 12 znakov")
        is_valid = True
        counter = 0
        for letter in value:
            if not letter.isnumeric() or (counter == 0 and letter == "+"):
                is_valid = False
            counter += 1
        if is_valid:
            return {key, value}
        else:
            raise Exception("Telefonska številka ni v pravilnem formatu")
        return {key, value}

    elif key == "email":
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, value)):  
            return {key, value}  
        else:  
            raise Exception("E-poštni naslov ni v pravilni obliki")
    else:
        return None


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