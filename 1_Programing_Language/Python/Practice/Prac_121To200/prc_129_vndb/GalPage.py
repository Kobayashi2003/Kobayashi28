from jinja2 import Environment, FileSystemLoader
from GalSearch import galgame_search

import requests
import os

def download_image(url, folder):
    path = os.path.join(folder, url.split("/")[-1])

    if not os.path.exists(folder):
        os.makedirs(folder)
    if os.path.exists(path):
        print(f"{path} already exists, skipping download")
        return

    with open(path, "wb") as f:
        f.write(requests.get(url).content)
    print(f"Downloaded {url} to {folder}")

def download_images(urls, folder):
    for url in urls:
        download_image(url, folder)

def generate_html(query, DOWNLOAD_IMAGES=False):
    content = galgame_search(query)
    results = content["results"]

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('page_vn_template.html')

    for result in results:
        vn_id               = result["id"]
        vn_title            = result["title"]
        vn_image_url        = result["image"]["url"]
        vn_screenshots_url  = [screenshot["url"] for screenshot in result["screenshots"]]
        vn_titles           = result["titles"]
        vn_aliases          = result["aliases"]
        vn_languages        = result["languages"]
        vn_platforms        = result["platforms"]
        vn_released         = result["released"]
        vn_developers       = [developer["name"] for developer in result["developers"]]
        vn_length           = result["length"]
        vn_length_minutes   = result["length_minutes"]
        vn_description      = result["description"]
        vn_tags             = [tag["name"] for tag in result["tags"]]
        vn_staff            = result["staff"]
        vn_va               = result["va"]

        if DOWNLOAD_IMAGES:
            download_images([vn_image_url] + vn_screenshots_url, f"vn_{vn_id}")
            vn_image_url = f"vn_{vn_id}/{vn_image_url.split('/')[-1]}"
            vn_screenshots_url = [f"vn_{vn_id}/{screenshot.split('/')[-1]}" for screenshot in vn_screenshots_url]
            for char in vn_va:
                if not char["character"]:
                    continue
                if not char["character"]["image"]:
                    continue
                download_image(char["character"]["image"]["url"], f"vn_{vn_id}/characters")
                char["character"]["image"]["url"] = f"vn_{vn_id}/characters/{char['character']['image']['url'].split('/')[-1]}"

        context = {
            "vn_id":                vn_id,
            "vn_image_url":         vn_image_url,
            "vn_screenshots_url":   vn_screenshots_url,
            "vn_titles":            vn_titles,
            "vn_aliases":           vn_aliases,
            "vn_languages":         vn_languages,
            "vn_platforms":         vn_platforms,
            "vn_released":          vn_released,
            "vn_developers":        vn_developers,
            "vn_description":       vn_description,
            "vn_tags":              vn_tags,
            "vn_length":            vn_length,
            "vn_length_minutes":    vn_length_minutes,
            "vn_staff":             vn_staff,
            "vn_va":                vn_va
        }

        output = template.render(context)
        with open(f"{vn_title}.html", "w", encoding="utf-8") as f:
            f.write(output)


# @lambda _:_()
def test():
    query = "ヨスガノソラ"
    generate_html(query)


if __name__ == "__main__":
    query = input("Enter a query: ")
    generate_html(query, DOWNLOAD_IMAGES=False)
