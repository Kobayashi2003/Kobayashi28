def and_filters(*filters):
    return ["and", *filters]

def or_filters(*filters):
    return ["or", *filters]

if __name__ == '__main__':

    import os
    import json
    import httpx

    current_dir = os.path.dirname(os.path.abspath(__file__))
    payload_file_path = os.path.join(current_dir, "payload.json")

    with open(payload_file_path, 'r') as f:
        payload = json.load(f)
    
    # payload['filters'] = and_filters(
    #     or_filters(
    #         ["platform", "=", "psp"],
    #         ["platform", "=", "ps2"],
    #         ["platform", "=", "ps3"],
    #         ["platform", "=", "ps4"],
    #         ["platform", "=", "ps5"],
    #         ["platform", "=", "psv"],
    #     ),
    #     payload['filters']
    # )
    # payload['fields'] = "id,title,titles.title,titles.main,titles.official,platforms"

    response = httpx.post(
        "https://api.vndb.org/kana/vn",
        json=payload
    )

    vns = response.json()['results']

    for vn in vns:
        for title in vn['titles']:
            if title['main'] and title['official']:
                vn['otitle'] = title['title']
                break
        vn.pop('titles')

    print(json.dumps(vns, indent=4, ensure_ascii=False))