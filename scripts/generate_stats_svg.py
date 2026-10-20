#!/usr/bin/env python3
"""
generate_stats_svg.py
Generates local Naruto-themed SVGs for Stats Overview and Top Languages.
"""

import json
import os

def generate_stats_overview():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 195" width="420" height="195">
  <defs>
    <linearGradient id="statsBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0F1A"/>
      <stop offset="100%" stop-color="#141B2D"/>
    </linearGradient>
    <linearGradient id="orangeLine" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6A00"/>
      <stop offset="50%" stop-color="#D00000"/>
      <stop offset="100%" stop-color="#00C2FF"/>
    </linearGradient>
  </defs>

  <rect x="2" y="2" width="416" height="191" rx="8" fill="url(#statsBg)" stroke="url(#orangeLine)" stroke-width="1.8"/>

  <!-- Title -->
  <g transform="translate(20, 24)">
    <text x="0" y="8" fill="#FF6A00" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800">⚡ SHINOBI STATS DOSSIER</text>
    <text x="0" y="24" fill="#8E9BB0" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600">Sushrut-Kale • Hidden Leaf Intelligence</text>
  </g>

  <!-- Metric Rows -->
  <g transform="translate(20, 68)" font-family="system-ui, -apple-system, sans-serif" font-size="12">
    <!-- Row 1: Total Repos -->
    <text x="0" y="10" fill="#F2E3C0" font-weight="600">📜 Shinobi Repositories</text>
    <text x="380" y="10" fill="#FFD700" font-weight="800" text-anchor="end">21</text>
    <line x1="0" y1="18" x2="380" y2="18" stroke="#1A243B" stroke-width="1"/>

    <!-- Row 2: Live Deployments -->
    <text x="0" y="38" fill="#F2E3C0" font-weight="600">🌐 Live Mission Deployments</text>
    <text x="380" y="38" fill="#00C2FF" font-weight="800" text-anchor="end">6</text>
    <line x1="0" y1="46" x2="380" y2="46" stroke="#1A243B" stroke-width="1"/>

    <!-- Row 3: Specialty Jutsu (Replaced CGPA so CGPA is only in ID Card!) -->
    <text x="0" y="66" fill="#F2E3C0" font-weight="600">🌀 Primary Specialty Jutsu</text>
    <text x="380" y="66" fill="#FF6A00" font-weight="800" text-anchor="end">AI/ML &amp; 3D Spatial Engines</text>
    <line x1="0" y1="74" x2="380" y2="74" stroke="#1A243B" stroke-width="1"/>

    <!-- Row 4: Ninja Rank -->
    <text x="0" y="94" fill="#F2E3C0" font-weight="600">🥷 Shinobi Rank</text>
    <text x="380" y="94" fill="#7DF9FF" font-weight="800" text-anchor="end">Genin ➔ Chunin (In Progress)</text>
  </g>
</svg>'''
    return svg

def generate_languages_svg():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 195" width="420" height="195">
  <defs>
    <linearGradient id="langBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0B0F1A"/>
      <stop offset="100%" stop-color="#141B2D"/>
    </linearGradient>
    <linearGradient id="orangeLine2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00C2FF"/>
      <stop offset="50%" stop-color="#FF6A00"/>
      <stop offset="100%" stop-color="#FFD700"/>
    </linearGradient>
  </defs>

  <rect x="2" y="2" width="416" height="191" rx="8" fill="url(#langBg)" stroke="url(#orangeLine2)" stroke-width="1.8"/>

  <g transform="translate(20, 24)">
    <text x="0" y="8" fill="#00C2FF" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800">🌀 JUTSU NATURE AFFINITIES</text>
    <text x="0" y="24" fill="#8E9BB0" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600">Top Languages &amp; Core Technologies</text>
  </g>

  <!-- Multi-segment Progress Bar -->
  <g transform="translate(20, 60)">
    <rect x="0" y="0" width="380" height="10" rx="5" fill="#1C2E56"/>
    <!-- Segments -->
    <rect x="0" y="0" width="129" height="10" rx="5" fill="#3572A5"/>
    <rect x="131" y="0" width="106" height="10" fill="#3178C6"/>
    <rect x="239" y="0" width="83" height="10" fill="#F7DF1E"/>
    <rect x="324" y="0" width="38" height="10" fill="#F34B7D"/>
    <rect x="364" y="0" width="16" height="10" rx="5" fill="#FF6A00"/>
  </g>

  <!-- Language List -->
  <g transform="translate(20, 92)" font-family="system-ui, -apple-system, sans-serif" font-size="11">
    <circle cx="5" cy="5" r="4.5" fill="#3572A5"/><text x="16" y="9" fill="#F2E3C0" font-weight="600">Python: 34%</text>
    <circle cx="140" cy="5" r="4.5" fill="#3178C6"/><text x="151" y="9" fill="#F2E3C0" font-weight="600">TypeScript: 28%</text>
    <circle cx="280" cy="5" r="4.5" fill="#F7DF1E"/><text x="291" y="9" fill="#F2E3C0" font-weight="600">JavaScript: 22%</text>
    
    <circle cx="5" cy="30" r="4.5" fill="#F34B7D"/><text x="16" y="34" fill="#F2E3C0" font-weight="600">C++: 10%</text>
    <circle cx="140" cy="30" r="4.5" fill="#FF6A00"/><text x="151" y="34" fill="#F2E3C0" font-weight="600">Kotlin / HTML: 6%</text>
  </g>
</svg>'''
    return svg

def main():
    os.makedirs("assets", exist_ok=True)
    os.makedirs("dist", exist_ok=True)

    stats_svg = generate_stats_overview()
    langs_svg = generate_languages_svg()

    with open("assets/stats-overview.svg", "w", encoding="utf-8") as f:
        f.write(stats_svg)
    with open("dist/stats-overview.svg", "w", encoding="utf-8") as f:
        f.write(stats_svg)

    with open("assets/languages.svg", "w", encoding="utf-8") as f:
        f.write(langs_svg)
    with open("dist/languages.svg", "w", encoding="utf-8") as f:
        f.write(langs_svg)

    print("Regenerated stats-overview.svg and languages.svg with valid XML and no CGPA duplication!")

if __name__ == "__main__":
    main()
