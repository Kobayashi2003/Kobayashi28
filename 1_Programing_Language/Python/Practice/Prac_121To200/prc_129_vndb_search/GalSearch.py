import requests
import json

def galgame_search(query):
    url = "https://api.vndb.org/kana/vn"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "filters": ["search", "=", query],
        "fields": """
        id,                         title,
        image.url,                  screenshots.url,
        titles.title,               titles.lang,
        titles.official,            aliases,
        languages,                  platforms,
        released,                   developers.name,
        length,                     length_minutes,
        description,                tags.name,
        staff.name,                 staff.role,
        va.staff.name,              
        va.character.name,          va.character.original,
        va.character.description,   va.character.image.url,
        va.character.blood_type,    va.character.height,
        va.character.weight,        va.character.bust,
        va.character.waist,         va.character.hips,
        va.character.cup,           va.character.age,
        va.character.birthday,      va.character.sex,
        va.character.vns.title,     va.character.vns.role
        """
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return json.loads(response.text)

    return None


# @lambda _:_()
def test():
    query = "ヨスガノソラ"
    result = galgame_search(query)
    if result:
        print(json.dump(result, indent=4))
    else:
        print("No result found")


if __name__ == "__main__":

    query = input("Enter a query: ")
    result = galgame_search(query)
    if result:
        with open("result.json", "w") as f:
            json.dump(result, f, indent=4)
        print("Result saved to result.json")
    else:
        print("No result found")
