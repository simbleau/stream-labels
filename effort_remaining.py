#!/usr/bin/env python3

"""Write the current time left to launch to a label"""
import os
import math
import json
import requests
from requests.auth import HTTPBasicAuth

JIRA_EMAIL = os.environ["JIRA_EMAIL"]
JIRA_KEY = os.environ["JIRA_KEY"]


def write_ttl():
    """Write the ttl.txt file"""
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_KEY)
    headers = {"Accept": "application/json"}
    query = {"jql": ("project = TRI AND status != 'Done' and issuetype = 'Task'")}

    start = 0
    end = 1
    total_points = 0
    while start < end:
        url = f"https://vgxgame.atlassian.net/rest/api/3/search?startAt={start}"
        response = requests.request(
            "GET", url, headers=headers, params=query, auth=auth, timeout=10
        )
        src = json.loads(response.text)
        start = src["startAt"]
        start += src["maxResults"]
        end = src["total"]

        issues = src["issues"]
        for issue in issues:
            points = issue["fields"]["customfield_10032"]
            if points:
                try:
                    points = int(points)
                except ValueError:
                    points = 0
                total_points += points

    file_path = os.path.join("/Users/simbleau", "Streaming", "ttl.txt")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    label_text = (
        "Effort remaining: "
        + str(int(total_points))
        + " points or "
        + str(math.ceil(total_points / 8))
        + " weeks"
    )
    with open(file_path, "w", encoding="utf8") as file:
        file.write(label_text)

    print(f"Content has been written to {file_path}")


if __name__ == "__main__":
    write_ttl()
