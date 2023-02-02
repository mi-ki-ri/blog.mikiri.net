import datetime
import yaml
import codecs
import argparse
import markdown
import re
import urllib.parse
import os
from markdownify import markdownify as md


def main():
    base_url = 'https://blog.mikiri.net/'
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str, default="")
    args = parser.parse_args()
    file_path = args.file
    if file_path == "":
        return

    tags = []

    file_body = ""
    with open(file=file_path, mode="r")as f:
        file_body = f.read()

    find_list = re.finditer(r"(\#[^\#\s]+)\s", file_body)
    for find in find_list:
        print("tag", find.group(0).strip())
        tags.append(find.group(0).strip().replace("#", ""))
        file_body = file_body.replace(find.group(
            0), f"[\\{find.group(0).strip()}]({base_url}tags/{urllib.parse.quote( find.group(0).strip().replace('#',''))}/)")

    html = markdown.markdown(file_body)

    title = ""
    find_h1 = re.finditer(r"(<h1>(.+)</h1>)", html)
    for h1 in find_h1:
        print("title", h1.groups()[1])
        title = h1.groups()[1]
        print("titletag", h1.groups()[0])
        html = html.replace(h1.groups()[0], "")

    yml_obj = {
        "title": title,
        "date": datetime.datetime.fromtimestamp(os.stat(file_path).st_birthtime).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "lastmod": datetime.datetime.fromtimestamp(os.stat(file_path).st_mtime).strftime("%Y-%m-%dT%H:%M:%S+09:00"),
        "tags": tags,
        "categories": 'blog',
    }

    to_write_txt = ""
    # print(yml_obj)
    # print("---")
    to_write_txt += "---\n"
    # print(yaml.dump(yml_obj))
    to_write_txt += f"{yaml.dump(yml_obj)}"
    # print("---")
    to_write_txt += "---\n\n"
    # print(md(html, heading_style="ATX"))
    to_write_txt += f"{md(html, heading_style='ATX', newline_style='BACKSLASH')}"

    print("============")
    print(to_write_txt)

    with codecs.open(f"./content/posts/{os.path.basename( file_path )}", mode="w") as f:
        f.write(to_write_txt)


main()
