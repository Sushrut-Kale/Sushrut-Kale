#!/usr/bin/env python3
import json
import os
import re

def get_rank_and_color(repo_name):
    name = repo_name.lower()
    if "campus-3d" in name or "learner" in name or "ai-challenge" in name:
        return "S-RANK", "#D00000", "#FF6A00"
    elif "paytm" in name or "ai-learning" in name or "timetable" in name or "agrin" in name:
        return "A-RANK", "#FF6A00", "#FFD700"
    elif "clubsync" in name or "hbtm" in name or "portfolio" in name or "maze" in name:
        return "B-RANK", "#00C2FF", "#7DF9FF"
    else:
        return "C-RANK", "#3FA34D", "#7DF9FF"

def get_lang_color(lang):
    colors = {
        "Python": "#3572A5",
        "TypeScript": "#3178C6",
        "JavaScript": "#F7DF1E",
        "C++": "#F34B7D",
        "Kotlin": "#A97BFF",
        "HTML": "#E34F26",
        "Code": "#FF6A00"
    }
    return colors.get(lang, "#8E9BB0")

import html

def clean_desc(text, max_len=75):
    # Strip emojis and clean
    clean = re.sub(r'[^\x00-\x7F]+', '', text).strip()
    if not clean:
        clean = "Shinobi engineering and applied intelligent systems."
    if len(clean) > max_len:
        clean = clean[:max_len-3] + "..."
    return html.escape(clean)

def generate_svg_card(repo):
    name = repo["name"]
    desc = clean_desc(repo.get("description", ""))
    lang = repo.get("language") or "Code"
    lang_col = get_lang_color(lang)
    rank, rank_col, accent_col = get_rank_and_color(name)
    stars = repo.get("stars", 0)
    live_url = repo.get("homepage", "")
    is_live = bool(live_url)

    # 2 lines split if long
    words = desc.split()
    line1 = []
    line2 = []
    curr = line1
    for w in words:
        if len(" ".join(curr + [w])) <= 42:
            curr.append(w)
        else:
            if curr is line1:
                curr = line2
                curr.append(w)
            else:
                break
    line1_str = " ".join(line1)
    line2_str = " ".join(line2)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 130" width="380" height="130">
  <defs>
    <linearGradient id="bg_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0F1A"/>
      <stop offset="100%" stop-color="#141B2D"/>
    </linearGradient>
    <linearGradient id="border_{name}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{rank_col}"/>
      <stop offset="100%" stop-color="{accent_col}"/>
    </linearGradient>
    <filter id="glow_{name}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect x="2" y="2" width="376" height="126" rx="8" fill="url(#bg_{name})" stroke="url(#border_{name})" stroke-width="1.6"/>

  <!-- Left Chakra Accent Bar -->
  <rect x="2" y="2" width="5" height="126" rx="2" fill="{rank_col}"/>

  <!-- Rank Badge -->
  <g transform="translate(18, 16)">
    <rect x="0" y="0" width="65" height="18" rx="4" fill="{rank_col}" opacity="0.2"/>
    <rect x="0" y="0" width="65" height="18" rx="4" fill="none" stroke="{rank_col}" stroke-width="1"/>
    <text x="32.5" y="13" fill="{rank_col}" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="800" text-anchor="middle">{rank}</text>
  </g>

  <!-- Repo Title -->
  <text x="92" y="30" fill="#F2E3C0" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="700">{name}</text>

  <!-- Live indicator or repo star -->
  <g transform="translate(340, 20)">
    {'<circle cx="0" cy="5" r="4" fill="#00C2FF" filter="url(#glow_' + name + ')"><animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite"/></circle>' if is_live else '<circle cx="0" cy="5" r="3" fill="#FFD700"/>'}
  </g>

  <!-- Description -->
  <text x="18" y="58" fill="#8E9BB0" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="500">{line1_str}</text>
  <text x="18" y="74" fill="#8E9BB0" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="500">{line2_str}</text>

  <!-- Bottom Metadata Row -->
  <g transform="translate(18, 102)">
    <!-- Language dot -->
    <circle cx="5" cy="5" r="4.5" fill="{lang_col}"/>
    <text x="16" y="9" fill="#F2E3C0" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600">{lang}</text>

    <!-- Status badge -->
    <text x="110" y="9" fill="{rank_col}" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700">{'⚡ LIVE DEPLOYED' if is_live else '📜 SHINOBI REPO'}</text>
  </g>

  <!-- Tiny Animated Chakra Pulse in bottom right corner -->
  <circle cx="355" cy="107" r="3" fill="{accent_col}">
    <animate attributeName="r" values="2;4;2" dur="1.5s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.5;1;0.5" dur="1.5s" repeatCount="indefinite"/>
  </circle>
</svg>'''
    return svg

def main():
    if not os.path.exists("data/repos.json"):
        print("data/repos.json missing!")
        return

    with open("data/repos.json", "r", encoding="utf-8") as f:
        repos = json.load(f)

    os.makedirs("assets/cards", exist_ok=True)
    os.makedirs("dist/cards", exist_ok=True)

    # Filter out Sushrut-Kale meta profile itself
    selected_repos = [r for r in repos if r["name"].lower() != "sushrut-kale"]

    for r in selected_repos:
        svg_content = generate_svg_card(r)
        filename = f"{r['name']}.svg"
        with open(os.path.join("assets/cards", filename), "w", encoding="utf-8") as f:
            f.write(svg_content)
        with open(os.path.join("dist/cards", filename), "w", encoding="utf-8") as f:
            f.write(svg_content)

    print(f"Generated {len(selected_repos)} SVG repo cards in assets/cards/ and dist/cards/")

if __name__ == "__main__":
    main()
