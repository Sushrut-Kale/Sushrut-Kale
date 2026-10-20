#!/usr/bin/env python3
import urllib.request
import json
import os
import sys

headers = {'User-Agent': 'Mozilla/5.0'}

def fetch_repos(username="Sushrut-Kale"):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            repos_data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching repos: {e}", file=sys.stderr)
        return []

    cleaned = []
    for r in repos_data:
        if r.get('fork', False):
            continue
        name = r.get('name')
        desc = r.get('description') or ""
        homepage = r.get('homepage') or ""
        stars = r.get('stargazers_count', 0)
        forks = r.get('forks_count', 0)
        lang = r.get('language') or "Code"
        topics = r.get('topics', [])
        pushed_at = r.get('pushed_at', '')
        
        # If no description, provide meaningful fallback
        if not desc:
            if name.lower() == "mitaoe3d":
                desc = "3D Interactive Digital Twin of MIT AOE campus built with React Three Fiber and A* pathfinding."
            elif name.lower() == "sushrut-kale":
                desc = "Master Shinobi profile repository and dynamic jutsu assets."
            else:
                desc = f"Shinobi engineering project in {lang}."

        cleaned.append({
            "name": name,
            "description": desc,
            "homepage": homepage,
            "stars": stars,
            "forks": forks,
            "language": lang,
            "topics": topics,
            "pushed_at": pushed_at,
            "html_url": r.get('html_url')
        })

    os.makedirs("data", exist_ok=True)
    with open("data/repos.json", "w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=2)
    print(f"Saved {len(cleaned)} repos to data/repos.json")
    return cleaned

if __name__ == "__main__":
    fetch_repos()
