#!/usr/bin/env python3
"""
generate_repo_cards.py
Generates polished Naruto-themed SVG project cards ranked by complexity and backend architecture.
"""

import os
import re
import html

PROJECTS_DATA = [
    {
        "name": "Campus-3D",
        "title": "Campus Twin 3D",
        "rank": "S-RANK",
        "rank_color": "#D00000",
        "accent": "#00C2FF",
        "category": "3D Spatial World & WebGL Engine",
        "desc": "3D interactive digital twin of MITAOE with A* pathfinding, FPS/orbit navigation, and WebGL resilience.",
        "lang": "React • Three.js",
        "lang_color": "#00C2FF",
        "live": "https://mitaoe1.vercel.app",
        "repo": "https://github.com/Sushrut-Kale/Campus-3D"
    },
    {
        "name": "AI-challenge",
        "title": "AgentCraft Multi-Agent AI",
        "rank": "S-RANK",
        "rank_color": "#D00000",
        "accent": "#FF6A00",
        "category": "Autonomous Multi-Agent Simulation",
        "desc": "Autonomous agent decision loops, LLM orchestration, and dynamic world state modeling.",
        "lang": "TypeScript • Next.js",
        "lang_color": "#3178C6",
        "live": "https://agentcraft-phi.vercel.app",
        "repo": "https://github.com/Sushrut-Kale/AI-challenge"
    },
    {
        "name": "paytm",
        "title": "FinPath AI Engine",
        "rank": "S-RANK",
        "rank_color": "#D00000",
        "accent": "#FFD700",
        "category": "Goal-First Financial Platform",
        "desc": "Personalized financial goal engine, AI document intelligence, readiness scoring, and risk modeling.",
        "lang": "TypeScript • Next.js",
        "lang_color": "#3178C6",
        "live": "https://finpath-ai-three.vercel.app/",
        "repo": "https://github.com/Sushrut-Kale/paytm"
    },
    {
        "name": "AI-Learning-Conductor",
        "title": "AI Learning Conductor",
        "rank": "S-RANK",
        "rank_color": "#D00000",
        "accent": "#00C2FF",
        "category": "Classroom Intelligence Engine",
        "desc": "Transforms student assessment evidence and teacher observations into adaptive learning intelligence.",
        "lang": "TypeScript • Full Stack",
        "lang_color": "#3178C6",
        "live": "https://ai-learning-conductor.vercel.app/",
        "repo": "https://github.com/Sushrut-Kale/AI-Learning-Conductor"
    },
    {
        "name": "timetable",
        "title": "CampusCompass CP-SAT",
        "rank": "A-RANK",
        "rank_color": "#FF6A00",
        "accent": "#00C2FF",
        "category": "Multi-Constraint Optimization",
        "desc": "Automated NP-hard timetable solver using Google OR-Tools CP-SAT + FastAPI + Next.js.",
        "lang": "Python • OR-Tools",
        "lang_color": "#3572A5",
        "live": "",
        "repo": "https://github.com/Sushrut-Kale/timetable"
    },
    {
        "name": "HBTM",
        "title": "HBTM Self-Evolution",
        "rank": "A-RANK",
        "rank_color": "#FF6A00",
        "accent": "#FFD700",
        "category": "AI Identity & Growth Pipeline",
        "desc": "Personal growth platform transforming digital habits into structured learning and evolution paths.",
        "lang": "Python • ML Pipeline",
        "lang_color": "#3572A5",
        "live": "https://hbtm-delta.vercel.app",
        "repo": "https://github.com/Sushrut-Kale/HBTM"
    },
    {
        "name": "farm-friend",
        "title": "FarmFriend AI",
        "rank": "A-RANK",
        "rank_color": "#FF6A00",
        "accent": "#3FA34D",
        "category": "Explainable AI & Agronomic Engine",
        "desc": "Data-driven crop recommendation engine with SHAP explainability, crop calendars, and soil intelligence.",
        "lang": "Python • Scikit-Learn",
        "lang_color": "#3572A5",
        "live": "https://farm-friend-chi.vercel.app",
        "repo": "https://github.com/Sushrut-Kale/farm-friend"
    },
    {
        "name": "clubsync",
        "title": "ClubSync Campus AI",
        "rank": "A-RANK",
        "rank_color": "#FF6A00",
        "accent": "#00C2FF",
        "category": "Campus Operations & Matching",
        "desc": "Club management system with Gemini-powered club matchmaking, QR attendance, and Firebase auth.",
        "lang": "React • Node.js • Mongo",
        "lang_color": "#F7DF1E",
        "live": "https://clubsync-4qua.vercel.app/",
        "repo": "https://github.com/Sushrut-Kale/clubsync"
    },
    {
        "name": "portfolio",
        "title": "Motion-Driven 3D Portfolio",
        "rank": "B-RANK",
        "rank_color": "#00C2FF",
        "accent": "#FF6A00",
        "category": "Interactive Motion Showcase",
        "desc": "High-fidelity React + Vite portfolio with motion-driven design, shaders, and project architecture.",
        "lang": "React • Vite • Motion",
        "lang_color": "#F7DF1E",
        "live": "https://portfolio-seven-omega-o9wgw7dd59.vercel.app/",
        "repo": "https://github.com/Sushrut-Kale/portfolio"
    },
    {
        "name": "maze_AI",
        "title": "Maze AI Delivery Route",
        "rank": "B-RANK",
        "rank_color": "#00C2FF",
        "accent": "#D00000",
        "category": "C++ / OpenGL Simulation",
        "desc": "Interactive route simulator comparing BFS, DFS, and A* search across weighted traffic graphs.",
        "lang": "C++ • OpenGL",
        "lang_color": "#F34B7D",
        "live": "",
        "repo": "https://github.com/Sushrut-Kale/maze_AI"
    },
    {
        "name": "manim",
        "title": "Manim Mathematical Visuals",
        "rank": "B-RANK",
        "rank_color": "#00C2FF",
        "accent": "#FFD700",
        "category": "Mathematical Animation",
        "desc": "Scientific visualizations bringing mathematics, algorithms, and AI concepts to life via Python.",
        "lang": "Python • Manim CE",
        "lang_color": "#3572A5",
        "live": "",
        "repo": "https://github.com/Sushrut-Kale/manim"
    }
]

def render_card(p):
    name = p["name"]
    title = html.escape(p["title"])
    rank = p["rank"]
    rank_col = p["rank_color"]
    accent = p["accent"]
    category = html.escape(p["category"])
    desc = html.escape(p["desc"])
    lang = html.escape(p["lang"])
    lang_col = p["lang_color"]
    is_live = bool(p["live"])

    # Split desc into 2 lines cleanly
    words = desc.split()
    line1, line2 = [], []
    curr = line1
    for w in words:
        if len(" ".join(curr + [w])) <= 44:
            curr.append(w)
        else:
            if curr is line1:
                curr = line2
                curr.append(w)
            else:
                break
    l1 = " ".join(line1)
    l2 = " ".join(line2)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 135" width="380" height="135">
  <defs>
    <linearGradient id="bg_{name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0F1A"/>
      <stop offset="60%" stop-color="#121828"/>
      <stop offset="100%" stop-color="#0B0F1A"/>
    </linearGradient>
    <linearGradient id="edge_{name}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{rank_col}"/>
      <stop offset="50%" stop-color="{accent}"/>
      <stop offset="100%" stop-color="{rank_col}"/>
    </linearGradient>
    <filter id="glow_{name}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Scroll Frame -->
  <rect x="2" y="2" width="376" height="131" rx="8" fill="url(#bg_{name})" stroke="url(#edge_{name})" stroke-width="1.6"/>

  <!-- Left Accent Line -->
  <rect x="2" y="2" width="5" height="131" rx="2" fill="{rank_col}"/>

  <!-- Rank Badge -->
  <g transform="translate(16, 14)">
    <rect x="0" y="0" width="62" height="18" rx="4" fill="{rank_col}" opacity="0.2"/>
    <rect x="0" y="0" width="62" height="18" rx="4" fill="none" stroke="{rank_col}" stroke-width="1"/>
    <text x="31" y="13" fill="{rank_col}" font-family="system-ui, sans-serif" font-size="9" font-weight="900" text-anchor="middle">{rank}</text>
  </g>

  <!-- Title -->
  <text x="86" y="27" fill="#F2E3C0" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="700">{title}</text>

  <!-- Live Pulse Dot -->
  <g transform="translate(345, 18)">
    {'<circle cx="0" cy="5" r="4" fill="#00C2FF" filter="url(#glow_' + name + ')"><animate attributeName="opacity" values="0.4;1;0.4" dur="1.8s" repeatCount="indefinite"/></circle>' if is_live else '<circle cx="0" cy="5" r="3" fill="#FFD700"/>'}
  </g>

  <!-- Subtitle Category -->
  <text x="16" y="48" fill="{accent}" font-family="system-ui, sans-serif" font-size="10" font-weight="700">{category}</text>

  <!-- Description -->
  <text x="16" y="66" fill="#8E9BB0" font-family="system-ui, -apple-system, sans-serif" font-size="10.5" font-weight="500">{l1}</text>
  <text x="16" y="80" fill="#8E9BB0" font-family="system-ui, -apple-system, sans-serif" font-size="10.5" font-weight="500">{l2}</text>

  <!-- Bottom Row: Stack and Deployment Status -->
  <g transform="translate(16, 108)">
    <circle cx="5" cy="5" r="4" fill="{lang_col}"/>
    <text x="15" y="9" fill="#F2E3C0" font-family="system-ui, sans-serif" font-size="10" font-weight="600">{lang}</text>

    <rect x="250" y="-3" width="96" height="18" rx="3" fill="{'#00C2FF' if is_live else '#1C2E56'}" opacity="0.2"/>
    <text x="298" y="9" fill="{'#00C2FF' if is_live else '#FFD700'}" font-family="system-ui, sans-serif" font-size="9" font-weight="800" text-anchor="middle">{'⚡ LIVE DEMO' if is_live else '📜 SHINOBI REPO'}</text>
  </g>
</svg>'''
    return svg

def main():
    os.makedirs("assets/cards", exist_ok=True)
    os.makedirs("dist/cards", exist_ok=True)

    for p in PROJECTS_DATA:
        content = render_card(p)
        filename = f"{p['name']}.svg"
        with open(os.path.join("assets/cards", filename), "w", encoding="utf-8") as f:
            f.write(content)
        with open(os.path.join("dist/cards", filename), "w", encoding="utf-8") as f:
            f.write(content)

    print(f"Generated {len(PROJECTS_DATA)} ranked repo cards in assets/cards/ and dist/cards/")

if __name__ == "__main__":
    main()
