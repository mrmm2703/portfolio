import csv
import os
import json
import time
import requests
from requests.auth import HTTPBasicAuth

coding_tag_id = "7895193"
api_key = "0e3c179345237821002ec070f623a952"

base_url = "https://github.com/mrmm2703/"

repos = [
    "spotify-party",
    "mental-screen",
    "megagon",
    "pepper-project",
    "portfolio"
]

while True:
    data = {"repos": {}}
    total_lines = 0
    response = requests.get("https://www.toggl.com/reports/api/v2/weekly?workspace_id=4274327&user_agent=portfolio&tag_ids="+coding_tag_id, auth=HTTPBasicAuth(api_key, "api_token"))
    js = response.json()
    data["coding_time_week"] = js["total_grand"]
    for repo in repos:
        name = repo
        os.system("git clone " + base_url + repo + ".git")
        os.system("git --git-dir " + repo + "/.git log --pretty=\"%cr\" > " + repo + ".txt")
        os.system("cloc --csv " + repo + " > " + repo + ".csv")
        os.system("rmdir /Q /S " + repo)
        lang = {}
        with open(repo + ".txt", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            total_rows = len(rows)
        i = 0
        with open(repo + ".txt", "r") as file1:
            reader1 = csv.reader(file1)
            for row in reader1:
                if i == 0:
                    last_edit = row[0]
                if i == total_rows-1:
                    creation_date = row[0]
                i += 1
        with open(repo+".csv", "r") as file:
            reader = csv.reader(file)
            # for r in reader:
            #     print(r)
            cont = False
            for row in reader:
                print(row)
                if len(row) == 0:
                    continue
                if row[0] == "files":
                    cont = True
                    continue
                if cont:
                    if row[1] != "SUM":
                        total_lines += int(row[4])
                    lang[row[1]] = row[4]
        os.system("del " + repo + ".csv")
        os.system("del " + repo + ".txt")
        print("---------")
        print(name)
        print(last_edit)
        print(creation_date)
        print(lang)
        print("---------")
        data["repos"][repo] = {
            "name": name,
            "last_edit": last_edit,
            "creation_date": creation_date,
            "lang": lang
        }
        data["total_lines"] = total_lines
    with open("stats.json", "w") as file2:
        json.dump(data, file2)
    print(data)
    print("------------------------------------")
    print("               WAIT")
    print("------------------------------------")
    time.sleep(300)
