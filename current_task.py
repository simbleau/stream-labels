#!/usr/bin/env python3

"""Write the current in progress task to a label"""
import os
import json
import requests
from requests.auth import HTTPBasicAuth

JIRA_EMAIL = os.environ["JIRA_EMAIL"]
JIRA_KEY = os.environ["JIRA_KEY"]


def write_in_progess():
    """Write the ttl.txt file"""
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_KEY)
    headers = {"Accept": "application/json"}
    query = {
        "jql": (
            "project = TRI AND status = 'In Progress' and assignee = 'Spencer C. Imbleau' and issuetype = 'Task'"
        )
    }

    url = "https://vgxgame.atlassian.net/rest/api/3/search"
    response = requests.request(
        "GET", url, headers=headers, params=query, auth=auth, timeout=10
    )
    src = json.loads(response.text)

    issues = src["issues"]

    if len(issues) == 0:
        label_text = "Not tracked"
    else:
        labels = []
        for issue in issues:
            summary = issue["fields"]["summary"]
            points = int(issue["fields"]["customfield_10032"])
            if points > 1:
                labels.append(f"{summary} ({points}pts)")
            elif points == 1:
                labels.append(f"{summary} ({points}pt)")
            else:
                labels.append(f"{summary}")
        label_text = ", ".join(labels)
    label_text = f"Current Task: {label_text}"

    # Get the home directory
    file_path = os.path.join("/Users/simbleau", "Streaming", "inprogress.txt")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Write content to the file
    with open(file_path, "w", encoding="utf8") as file:
        file.write(label_text)
    print(f"Content has been written to {file_path}")


if __name__ == "__main__":
    write_in_progess()
