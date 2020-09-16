import re
import json
import datetime
import uuid
from uuid import UUID
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
from const import TIPI, REGIJE

class Prostori:
    def __init__(self, table):
        #if id_prostora != "":
        #    self.id_prostora = id_prostora
        self.table = table
        self._changed = {}
        self._change_all(False)

    @property
    def ime(self):
        return self._ime

    @ime.setter
    def ime(self, value):
        if len(value) >= 60:
            raise ValueError("Ime objave je dolgo več kot 60 znakov")
        elif len(value) < 1:
            raise ValueError("Ime mora imeti vrednost")
        if hasattr(self, "ime"):
            if value != self.ime:
                self._ime = value
                self._changed["ime"] = True
        else:
            self._ime = value
            self._changed["ime"] = True


    @property
    def tip(self):
        return self._tip

    @tip.setter
    def tip(self, value):
        value = value.lower()
        if not value in TIPI:
            raise ValueError("Vnešen tip ni pravilen")
        if hasattr(self, "tip"):
            if value != self.tip:
                self._tip = value
                self._changed["tip"] = True
        else:
            self._tip = value
            self._changed["tip"] = True


    @property
    def kratek_opis(self):
        return self._kratek_opis

    @kratek_opis.setter
    def kratek_opis(self, value):
        if len(value) >= 160:
            raise ValueError("Kratek opis je dolg več kot 160 znakov")
        elif len(value) < 1:
            raise ValueError("Kratek opis mora imeti vrednost")
        if hasattr(self, "kratek_opis"):
            if value != self.kratek_opis:
                self._kratek_opis = value
                self._changed["kratek_opis"] = True
        else:
            self._kratek_opis = value
            self._changed["kratek_opis"] = True


    @property
    def dolg_opis(self):
        return self._dolg_opis

    @dolg_opis.setter
    def dolg_opis(self, value):
        if len(value) >= 100000:
            raise ValueError("Dolg opis je dolg več kot 100000 znakov")
        elif len(value) < 1:
            raise ValueError("Dolg opis mora imeti vrednost")
        if hasattr(self, "dolg_opis"):
            if value != self.dolg_opis:
                self._dolg_opis = value
                self._changed["dolg_opis"] = True
        else:
            self._dolg_opis = value
            self._changed["dolg_opis"] = True


    @property
    def regija(self):
        return self._regija

    @regija.setter
    def regija(self, value):
        value = value.lower()
        if not value in REGIJE:
            raise ValueError("Vnešena regija ni pravilna")
        if hasattr(self, "regija"):
            if value != self.regija:
                self._regija = value
                self._changed["regija"] = True
        else:
            self._regija = value
            self._changed["regija"] = True



    @property
    def naslov(self):
        return self._naslov

    @naslov.setter
    def naslov(self, value):
        if len(value) >= 60:
            raise ValueError("Naslov je dolg več kot 60 znakov")
        elif len(value) < 1:
            raise ValueError("Naslov mora imeti vrednost")
        if hasattr(self, "naslov"):
            if value != self.naslov:
                self._naslov = value
                self._changed["naslov"] = True
        else:
            self._naslov = value
            self._changed["naslov"] = True


    @property
    def posta(self):
        return self._posta

    @posta.setter
    def posta(self, value):
        try:
            value = int(value)
        except:
            raise ValueError("Vnešena poštna številka ni številka")
        if 1000 >= value >= 9999:
            raise ValueError("Vnešena poštna številka ni med 1000 in 9999")
        if hasattr(self, "posta"):
            if value != self.posta:
                self._posta = str(value)
                self._changed["posta"] = True
        else:
            self._posta = str(value)
            self._changed["posta"] = True


    @property
    def kraj(self):
        return self._kraj

    @kraj.setter
    def kraj(self, value):
        if len(value) >= 60:
            raise ValueError("Kraj je dolg več kot 60 znakov")
        elif len(value) < 1:
            raise ValueError("Kraj mora imeti vrednost")
        if hasattr(self, "kraj"):
            if value != self.kraj:
                self._kraj = value
                self._changed["kraj"] = True
        else:
            self._kraj = value
            self._changed["kraj"] = True


    @property
    def telefon(self):
        return self._telefon

    @telefon.setter
    def telefon(self, value):
        if not len(value) <= 12:
            raise ValueError("Telefonska številka je dolga več kot 12 znakov")
        is_valid = True
        counter = 0
        for letter in value:
            if not letter.isnumeric() or (counter == 0 and letter == "+"):
                is_valid = False
            counter += 1
        if not is_valid:
            raise ValueError("Telefonska številka ni v pravilnem formatu")
        if hasattr(self, "telefon"):
            if value != self.telefon:
                self._telefon = value
                self._changed["telefon"] = True
        else:
            self._telefon = value
            self._changed["telefon"] = True


    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex, value)):  
            if hasattr(self, "email"):
                if value != self.email:
                    self._email = value
                    self._changed["email"] = True
            else:
                self._email = value
                self._changed["email"] = True
        else:  
            raise ValueError("E-poštni naslov ni v pravilni obliki")

    
    @property
    def id_prostora(self):
        return self._id_prostora

    @property
    def id_uporabnika(self):
        return self._id_uporabnika

    @property
    def ustvarjeno(self):
        return self._ustvarjeno

    @property
    def spremenjeno(self):
        return self._spremenjeno

    def _change_all(self, state):
        self._changed["ime"] = state
        self._changed["tip"] = state
        self._changed["kratek_opis"] = state
        self._changed["dolg_opis"] = state
        self._changed["regija"] = state
        self._changed["naslov"] = state
        self._changed["posta"] = state
        self._changed["kraj"] = state
        self._changed["telefon"] = state
        self._changed["email"] = state

    def get_all(self):
        data = {}
        if hasattr(self, "id_prostora"):
            data["id_prostora"] = self.id_prostora
        if hasattr(self, "id_uporabnika"):
            data["id_uporabnika"] = self.id_uporabnika
        if hasattr(self, "ime"):
            data["ime"] = self.ime
        if hasattr(self, "tip"):
            data["tip"] = self.tip
        if hasattr(self, "kratek_opis"):
            data["kratek_opis"] = self.kratek_opis
        if hasattr(self, "dolg_opis"):
            data["dolg_opis"] = self.dolg_opis
        if hasattr(self, "regija"):
            data["regija"] = self.regija
        if hasattr(self, "naslov"):
            data["naslov"] = self.naslov
        if hasattr(self, "posta"):
            data["posta"] = self.posta
        if hasattr(self, "kraj"):
            data["kraj"] = self.kraj
        if hasattr(self, "telefon"):
            data["telefon"] = self.telefon
        if hasattr(self, "email"):
            data["email"] = self.email
        if hasattr(self, "spremenjeno"):
            data["spremenjeno"] = self.spremenjeno
        if hasattr(self, "ustvarjeno"):
            data["ustvarjeno"] = self.ustvarjeno
        return data

    def _set_all(self, data):
        if "id_prostora" in data:
            self._id_prostora = data['id_prostora']
        if "id_uporabnika" in data:
            self._id_uporabnika = data['id_uporabnika']
        if "ime" in data:
            self._ime = data['ime']
        if "tip" in data:
            self._tip = data['tip']
        if "kratek_opis" in data:
            self._kratek_opis = data['kratek_opis']
        if "dolg_opis" in data:
            self._dolg_opis = data['dolg_opis']
        if "regija" in data:
            self._regija = data['regija']
        if "naslov" in data:
            self._naslov = data['naslov']
        if "posta" in data:
            self._posta = data['posta']
        if "kraj" in data:
            self._kraj = data['kraj']
        if "telefon" in data:
            self._telefon = data['telefon']
        if "email" in data:
            self._email = data['email']
        if "ustvarjeno" in data:
            self._ustvarjeno = data['ustvarjeno']
        if "spremenjeno" in data:
            self._spremenjeno = data['spremenjeno']

    def set_all(self, data):
        if "ime" in data:
            self.ime = data['ime']
        if "tip" in data:
            self.tip = data['tip']
        if "kratek_opis" in data:
            self.kratek_opis = data['kratek_opis']
        if "dolg_opis" in data:
            self.dolg_opis = data['dolg_opis']
        if "regija" in data:
            self.regija = data['regija']
        if "naslov" in data:
            self.naslov = data['naslov']
        if "posta" in data:
            self.posta = data['posta']
        if "kraj" in data:
            self.kraj = data['kraj']
        if "telefon" in data:
            self.telefon = data['telefon']
        if "email" in data:
            self.email = data['email']

    def create(self, id_uporabnika):
        self._id_prostora = str(uuid.uuid4())
        try:
            UUID(id_uporabnika, version=4)
        except:
            raise ValueError("ID uporabnika ni v pravilni obliki")
        self._id_uporabnika = id_uporabnika
        self._new = True

    def get(self, id_prostora):
        try:
            response = self.table.query(
                KeyConditionExpression=Key('id_prostora').eq(id_prostora)
            )
        except ClientError as e:
            raise Exception(str(e.response['Error']))
        if len(response['Items']) == 0:
            return ValueError("Ta prostor ne obstaja")
        self._set_all(response['Items'][0])
        self._new = False

    def delete(self):
        try:
            response = self.table.delete_item(
                Key={
                    'id_prostora': self.id_prostora,
                    'id_uporabnika': self.id_uporabnika
                }
            )
        except ClientError as e:
            raise Exception(str(e.response['Error']))
        return response

    def save(self):
        if self._new:
            not_required = ["email", "telefon"]
            for key, value in self._changed.items():
                if key not in not_required and not value:
                    raise ValueError("Polje " + key + " ne sme ostati prazno")
            self._ustvarjeno = str(datetime.datetime.now())
            response = self.table.put_item(Item=self.get_all())
        else:
            self._spremenjeno = str(datetime.datetime.now()) 
            values = {}
            expression = "set"
            counter = 0
            for key, value in self.get_all().items():
                if not (key == "id_prostora" or key == "id_uporabnika"):
                    if self._changed[key]:
                        expression += " " + key + "=:" + key + ","
                        values[":"+key] = value
                        counter += 1
            expression = expression[:-1]
            if counter == 0:
                return {"message": "Ni sprememb"}

            try:
                response = self.table.update_item(
                    Key={
                        'id_prostora': self.id_prostora,
                        'id_uporabnika': self.id_uporabnika
                    },
                    UpdateExpression=expression,
                    ExpressionAttributeValues=values,
                    ReturnValues="UPDATED_NEW"
                )
            except ClientError as e:
                raise Exception(str(e.response['Error']))
        self._change_all(False)
        return response