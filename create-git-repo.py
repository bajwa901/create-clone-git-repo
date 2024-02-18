
import requests
import os

GITHUB_TOKEN='AIUTH TOKEN API'
REPO_NAME = 'REPONAME'
USER_NAME='USERNAME'
API_URL = f"https://api.github.com/user/repos"

repo_data = {
        "name": REPO_NAME,
        "private": False,
        "auto_init":True, # Change to True if you want a private repository
        # Add other options as needed: https://developer.github.com/v3/repos/#create
    }

    # Headers with authentication
headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

response = requests.post(API_URL, json=repo_data, headers=headers)

if response.status_code == 201:
    print(f"Repository '{REPO_NAME}' created successfully on GitHub.")

    url = f"{API_URL}/{USER_NAME}/{REPO_NAME}"
    headers = {}
    if GITHUB_TOKEN:
        headers['Authorization'] = f"Bearer {GITHUB_TOKEN}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            repo_data = response.json()
            clone_url = repo_data['clone_url']
    API_URL = f'https://api.github.com/repos/{USER_NAME}/{REPO_NAME}/git/refs/heads/main'
    headers['Authorization'] = f'token {GITHUB_TOKEN}'
    try:

        response = requests.get(API_URL, headers=headers)
        response.raise_for_status()
        commit_sha = response.json()['object']['sha']
        clone_url = f'https://github.com/{USER_NAME}/{REPO_NAME}.git'
        os.system(f'git clone {clone_url}')
        os.system(f'git checkout {commit_sha}')
        print(f'Repository cloned successfully')
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}')

else:
    print(f"Failed to create repository. Status code: {response.status_code}")
    print(response.text)
