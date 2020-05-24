"""search_repos.py"""

import requests


def search_repos(name, language):
    url = "https://api.github.com/search/repositories"
    params = {
        "q": f"{name}+language:{language}",
        "sort": "stars",
        "order": "desc"
    }

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        results = response.json()["items"]
        print(f"Found {len(results)} repos for {name} driver.\n")
        for repo in results[:10]:
            print(f"{repo['svn_url']} - stars={repo['stargazers_count']}")
