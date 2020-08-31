# Vse za zabavo API
Vsi POST in PUT poizvedbe morajo biti v JSON obliki.
## /prostori
### GET
Vrne vse objave
Zaenkrat vrne celoten seznam, kasneje bo mogoče filtriranje npr.: ?regija=savinjska&tip=dvorana
### POST
To poizvedbo lahko uporabljajo samo prijavljeni uporabniki. Če je bila poizvedba uspešno izvedena vrne **id_prostora**.
Spodaj so opisane spremenljivke, ki jih mora vsebovati JSON dokument.
| spremenljivka | opis |
|---|---|
| ime | ime objave/prostora, ki bo viden v URL vrstici, nad samo objavo in v seznamu prostorov |
| tip | tip prostora npr.: dvorana, šotor... |
| kratek-opis | kratek opis prostora, ki bo viden na seznamu prostorov in v Googlovih rezultatih |
| dolg-opis | dolg opis, ki bo viden v sami objavi, oblikovan naj bo v MarkDown obliki |
| regija | statistična regija objavljenega prostora |
| naslov | naslov prostora |
| posta | poštna številka prostora |
| kraj | kraj prostora |
| telefon | telefonska številka, na katero lahko pokličejo stranke |
| email | email naslov, na katerega lahko stranka pošlje povpraševanje |
## /prostori/{:id_prostora}
### GET
Vrne vse podatke o objavi
### PUT
Spodaj so opisane spremenljivke, ki jih lahko vsebuje JSON dokument. Ni potrebno posredovati vseh spremenljivk, ampak le tiste, katere želimo spremeniti.
| spremenljivka | opis |
|---|---|
| ime | ime objave/prostora, ki bo viden v URL vrstici, nad samo objavo in v seznamu prostorov |
| tip | tip prostora npr.: dvorana, šotor... |
| kratek-opis | kratek opis prostora, ki bo viden na seznamu prostorov in v Googlovih rezultatih |
| dolg-opis | dolg opis, ki bo viden v sami objavi, oblikovan naj bo v MarkDown obliki |
| regija | statistična regija objavljenega prostora |
| naslov | naslov prostora |
| posta | poštna številka prostora |
| kraj | kraj prostora |
| telefon | telefonska številka, na katero lahko pokličejo stranke |
| email | email naslov, na katerega lahko stranka pošlje povpraševanje |
### DELETE
Ta metoda preprosto izbriše objavo