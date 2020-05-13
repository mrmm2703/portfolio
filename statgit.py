import csv
import os
import json
import time
import requests
from requests.auth import HTTPBasicAuth
from api_key import api_key

coding_tag_id = "7895193"

base_url = "https://github.com/mrmm2703/"

repos = [
    "megagon",
    "spotify-party",
    "mental-screen",
    "pepper-project",
    "portfolio"
]

while True:
    times = []
    data = {"repos": {}}
    total_lines = 0

    # Weekly coding time from Toggl
    response = requests.get("https://www.toggl.com/reports/api/v2/weekly?workspace_id=4274327&user_agent=portfolio&tag_ids="+coding_tag_id, auth=HTTPBasicAuth(api_key, "api_token"))
    js = response.json()
    data["coding_time_week"] = js["total_grand"]

    # Repo loop
    for repo in repos:
        name = repo
        # Download and count repo lines
        os.system("git clone " + base_url + repo + ".git")
        os.system("cloc --csv " + repo + " > " + repo + ".csv")
        lang = {}

        # Get relative time with git
        os.system("git --git-dir " + repo + "/.git log --pretty=\"%cr\" > " + repo + ".txt")
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
        os.system("del " + repo + ".txt")
        
        # Get UNIX timestamp from git
        os.system("git --git-dir " + repo + "/.git log --pretty=\"%ct\" > " + repo + ".txt")
        with open(repo + ".txt", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)
            total_rows = len(rows)
        i = 0
        with open(repo + ".txt", "r") as file1:
            reader1 = csv.reader(file1)
            for row in reader1:
                if i == 0:
                    times.append([int(row[0]), repo])
                i += 1
        os.system("del " + repo + ".txt")

        # Parse count CSV
        with open(repo+".csv", "r") as file:
            reader = csv.reader(file)
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

        # Remove the repo
        os.system("rmdir /Q /S " + repo)

        # Construct JSON
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
    
    # Get the last project
    times = sorted(times, key=lambda x: x[0])
    last_project = times[0][1]
    data["last_project"] = last_project

    # Write JSON
    with open("stats.json", "w") as file2:
        json.dump(data, file2)
    
    # Finish off and wait
    print(data)
    print("------------------------------------")
    print("               WAIT")
    print("------------------------------------")
    time.sleep(300)
