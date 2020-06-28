import csv
import os
import json
import time
import requests
from requests.auth import HTTPBasicAuth
from api_key import api_key
from api_key import git_username
from api_key import git_pass
from api_key import git_key
from datetime import datetime

coding_tag_id = "7895193"

base_url = "https://" + git_username + ":" + git_key + "@github.com/mrmm2703/"

repos = []

with open("repolist.txt", "r") as repolistfile:
    reader = csv.reader(repolistfile)
    for line in reader:
        repos = line


times = []
data = {"repos": {}}
total_lines = 0

# Weekly coding time from Toggl
response = requests.get("https://www.toggl.com/reports/api/v2/weekly?workspace_id=4274327&user_agent=portfolio&tag_ids="+coding_tag_id, auth=HTTPBasicAuth(api_key, "api_token"))
js = response.json()
data["coding_time_week"] = js["total_grand"]

json_file = open("stats.json", "r")
json_data = json.load(json_file)
json_file.close()

# Repo loop
for repo in repos:
    name = repo
    # Get last update from GitHub
    response = requests.get("https://api.github.com/repos/mrmm2703/"+name, auth=HTTPBasicAuth(git_username, git_pass))
    js = response.json()
    last_edit = js["updated_at"]
    datetime_obj = datetime.strptime(last_edit, "%Y-%m-%dT%H:%M:%SZ")
    last_edit_ts = datetime_obj.timestamp()
    if name in json_data["repos"]:
        if not (json_data["repos"][name]["last_edit"] == last_edit_ts): # Update detected
            cont2 = True
        else: # No update
            cont2 = False
    else: # Update detected
        cont2 = True

    if not cont2:
        print(name + " already exists. Skipping...")
        data["repos"][repo] = {
            "name": json_data["repos"][repo]["name"],
            "last_edit": last_edit_ts,
            "creation_date": json_data["repos"][repo]["creation_date"],
            "lang": json_data["repos"][repo]["lang"]
        }
        times.append([last_edit_ts, repo])
        total_lines = total_lines + int(json_data["repos"][repo]["lang"]["SUM"])

    if (cont2):
        print(name + " doesn't already exist. Proceeding...")
        # Download and count repo lines
        os.system("git clone " + base_url + repo + ".git")
        os.system("cloc --csv " + repo + " > " + repo + ".csv")
        lang = {}

        # Get UNIX timestamp with git
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
                    last_edit = last_edit_ts
                    times.append([last_edit_ts, repo])
                if i == total_rows-1:
                    creation_date = row[0]
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
        data["repos"][repo] = {
            "name": name,
            "last_edit": last_edit,
            "creation_date": creation_date,
            "lang": lang
        }
    data["total_lines"] = total_lines

# Get the last project
times = sorted(times, key=lambda x: x[0], reverse=True)
last_project = times[0][1]
data["last_project"] = last_project

# Write JSON
with open("stats.json", "w") as file2:
    json.dump(data, file2)