#!/usr/bin/env python3
"""
generate_naruto_contrib.py
Generates the animated Naruto "Rasengan Contribution Strike" SVGs
for GitHub profile README (dark and light theme).

Author: Antigravity for Sushrut-Kale
"""

import os
import sys
import json
import math
import random
import argparse
import urllib.request
import urllib.error

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            color
            contributionCount
            date
            weekday
          }
        }
      }
    }
  }
}
"""

def fetch_contributions_graphql(username, token):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Naruto-Contribution-Generator"
    }
    payload = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": username}}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
            return calendar['totalContributions'], calendar['weeks']
    except Exception as e:
        print(f"[!] GraphQL fetch failed: {e}")
        return None, None

def fetch_contributions_fallback(username):
    # Try public fallback API or construct synthetic realistic calendar
    url = f"https://github-contributions-api.jogruber.de/v4/{username}?y=last"
    headers = {"User-Agent": "Naruto-Contribution-Generator"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            total = data.get('total', {}).get('lastYear', 0)
            contributions = data.get('contributions', [])
            # Group into weeks
            weeks = []
            curr_week = []
            for day in contributions:
                curr_week.append({
                    "contributionCount": day.get("count", 0),
                    "date": day.get("date", ""),
                    "weekday": len(curr_week)
                })
                if len(curr_week) == 7:
                    weeks.append({"contributionDays": curr_week})
                    curr_week = []
            if curr_week:
                weeks.append({"contributionDays": curr_week})
            return total, weeks
    except Exception as e:
        print(f"[!] Fallback API failed: {e}")
        return None, None

def generate_synthetic_data():
    weeks = []
    total = 0
    random.seed(42)
    for w in range(53):
        days = []
        for d in range(7):
            # simulate active student/ninja commit distribution
            rand_val = random.random()
            if rand_val < 0.35:
                count = 0
            elif rand_val < 0.65:
                count = random.randint(1, 3)
            elif rand_val < 0.88:
                count = random.randint(4, 7)
            elif rand_val < 0.96:
                count = random.randint(8, 14)
            else:
                count = random.randint(15, 24)
            total += count
            days.append({
                "contributionCount": count,
                "date": f"2026-week{w}-day{d}",
                "weekday": d
            })
        weeks.append({"contributionDays": days})
    return total, weeks

def get_color_level(count, is_dark=True):
    # Naruto palette: Level 0 (Navy/parchment) -> Level 4 (Gold / Kyuubi Nine-Tails Chakra)
    if is_dark:
        if count == 0: return "#161d2d", 0
        if count <= 2: return "#803000", 1
        if count <= 5: return "#c94d00", 2
        if count <= 9: return "#ff6a00", 3
        return "#ffd700", 4
    else:
        if count == 0: return "#e8dcbe", 0
        if count <= 2: return "#ff944d", 1
        if count <= 5: return "#ff6a00", 2
        if count <= 9: return "#d44800", 3
        return "#8a1c00", 4

def render_naruto_svg(total, weeks, is_dark=True):
    theme_name = "dark" if is_dark else "light"
    bg_color = "#0B0F1A" if is_dark else "#F7F2E7"
    border_color = "#FF6A00" if is_dark else "#C85A00"
    text_primary = "#F2E3C0" if is_dark else "#1B2234"
    text_muted = "#8E9BB0" if is_dark else "#6F634A"
    accent_chakra = "#00C2FF"
    rasengan_cyan = "#7DF9FF"
    badge_bg = "#121826" if is_dark else "#E6D8BA"
    
    # Grid coordinates
    grid_start_x = 70
    grid_start_y = 75
    cell_size = 11
    cell_gap = 3.5
    step_x = cell_size + cell_gap
    step_y = cell_size + cell_gap
    
    num_weeks = min(len(weeks), 53)
    grid_width = num_weeks * step_x
    total_svg_width = 890
    total_svg_height = 220
    
    cells_svg = []
    
    # Time parameters for animation
    anim_duration = 7.0  # seconds per sweep
    
    for w_idx in range(num_weeks):
        w = weeks[w_idx]
        col_x = grid_start_x + w_idx * step_x
        # Timing when Naruto's Rasengan hits this column (normalized 0 to 1)
        t_hit = (w_idx / max(1, num_weeks - 1)) * (anim_duration * 0.85)
        t_hit_str = f"{t_hit:.2f}s"
        t_decay = t_hit + 0.35
        t_decay_str = f"{t_decay:.2f}s"
        
        days = w.get("contributionDays", [])
        for d in days:
            weekday = d.get("weekday", 0)
            count = d.get("contributionCount", 0)
            row_y = grid_start_y + weekday * step_y
            color, level = get_color_level(count, is_dark)
            
            # Subtle diamond shuriken corner cut via polygon or rounded rect
            # Add dynamic shockwave response to each cell when rasengan hits!
            cell_element = f'''
      <rect x="{col_x:.1f}" y="{row_y:.1f}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}">
        <title>{count} ninja missions on {d.get("date", "")}</title>
        <animate attributeName="opacity" values="0.75;1;0.75" dur="{anim_duration}s" repeatCount="indefinite"
          keyTimes="0;{(t_hit/anim_duration):.3f};1"/>
        <animate attributeName="transform" type="scale" 
          values="1;1.2;1" dur="0.4s" begin="{t_hit_str}" repeatCount="1"
          additive="sum"/>
      </rect>'''
            cells_svg.append(cell_element)

    cells_markup = "".join(cells_svg)
    
    # Days labels (Mon, Wed, Fri)
    day_labels = [
        (1, "Mon"),
        (3, "Wed"),
        (5, "Fri")
    ]
    labels_svg = []
    for d_idx, d_name in day_labels:
        ly = grid_start_y + d_idx * step_y + 9
        labels_svg.append(f'<text x="{grid_start_x - 12}" y="{ly:.1f}" text-anchor="end" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="600">{d_name}</text>')
    
    # Months labels across the top
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    months_svg = []
    for m_i, m_name in enumerate(month_names):
        mx = grid_start_x + (m_i * 4.4) * step_x
        if mx < grid_start_x + grid_width - 20:
            months_svg.append(f'<text x="{mx:.1f}" y="{grid_start_y - 10}" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="700">{m_name}</text>')

    # Running path calculation:
    run_start_x = grid_start_x - 35
    run_end_x = grid_start_x + grid_width + 25
    naruto_y = grid_start_y + (3.5 * step_y) - 15  # centered vertically on the grid
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_svg_width} {total_svg_height}" width="{total_svg_width}" height="{total_svg_height}">
  <defs>
    <!-- Ninja Scroll & Chakra Filters -->
    <linearGradient id="bgGrad_{theme_name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_color}"/>
      <stop offset="50%" stop-color="{"#111726" if is_dark else "#F1EAD9"}"/>
      <stop offset="100%" stop-color="{bg_color}"/>
    </linearGradient>

    <linearGradient id="scrollBorder_{theme_name}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6A00"/>
      <stop offset="25%" stop-color="#D00000"/>
      <stop offset="50%" stop-color="#00C2FF"/>
      <stop offset="75%" stop-color="#FF6A00"/>
      <stop offset="100%" stop-color="#FFD700"/>
    </linearGradient>

    <!-- Rasengan Energy Radial Gradient -->
    <radialGradient id="rasenganCore" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="35%" stop-color="{rasengan_cyan}"/>
      <stop offset="70%" stop-color="{accent_chakra}"/>
      <stop offset="100%" stop-color="rgba(0,194,255,0)"/>
    </radialGradient>

    <radialGradient id="chakraAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="rgba(0,194,255,0.85)"/>
      <stop offset="60%" stop-color="rgba(125,249,255,0.4)"/>
      <stop offset="100%" stop-color="rgba(0,194,255,0)"/>
    </radialGradient>

    <filter id="chakraGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="flameGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <style>
    .ninja-title {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 800; font-size: 14px; fill: {text_primary}; letter-spacing: 1px; }}
    .ninja-sub {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 600; font-size: 10px; fill: {text_muted}; letter-spacing: 0.5px; }}
    .stat-badge {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; font-weight: 800; font-size: 11px; fill: #FFD700; }}
  </style>

  <!-- Background Canvas -->
  <rect x="2" y="2" width="{total_svg_width - 4}" height="{total_svg_height - 4}" rx="12" fill="url(#bgGrad_{theme_name})" stroke="url(#scrollBorder_{theme_name})" stroke-width="2"/>

  <!-- Konoha Leaf Symbol Background Watermark -->
  <g opacity="{'0.06' if is_dark else '0.04'}" transform="translate({total_svg_width/2 - 90}, 20) scale(1.5)">
    <path fill="#FF6A00" d="M60,10 C90,10 110,35 110,65 C110,95 85,115 55,115 C25,115 5,95 5,65 C5,35 25,15 50,15 L60,10 Z M55,30 C35,30 20,45 20,65 C20,85 35,100 55,100 C75,100 90,85 90,65 C90,45 75,35 60,35 C50,35 40,42 40,55 C40,65 48,72 58,72 C65,72 70,68 70,62 C70,57 66,54 61,54 C58,54 55,56 55,59 C55,61 56,63 58,63 C57,64 56,64 55,64 C52,64 50,62 50,59 C50,55 54,51 60,51 C66,51 72,56 72,63 C72,70 65,76 56,76 C46,76 36,67 36,55 C36,40 48,31 60,31 L55,30 Z"/>
    <path stroke="#FF6A00" stroke-width="3" stroke-linecap="round" d="M100,20 L125,5"/>
  </g>

  <!-- Header Section -->
  <g transform="translate(24, 22)">
    <!-- Konoha Forehead Protector Badge -->
    <rect x="0" y="0" width="34" height="20" rx="4" fill="{"#1E2638" if is_dark else "#DDD0B5"}" stroke="#8E9BB0" stroke-width="1.5"/>
    <circle cx="4" cy="10" r="1.5" fill="#C0C8D8"/>
    <circle cx="30" cy="10" r="1.5" fill="#C0C8D8"/>
    <!-- Leaf engraving -->
    <path fill="none" stroke="{border_color}" stroke-width="1.5" stroke-linecap="round" d="M14,13 C12,11 12,8 15,7 C18,6 20,9 19,11 C18,12 16,12 16,10"/>
    <path stroke="{border_color}" stroke-width="1.2" stroke-linecap="round" d="M20,7 L23,5"/>

    <!-- Title Texts -->
    <text x="44" y="14" class="ninja-title">⚡ RASENGAN CHAKRA STRIKE <tspan fill="#FF6A00">•</tspan> <tspan font-weight="600" fill="{text_muted}">NINJA MISSION LOG</tspan></text>
    <text x="44" y="32" class="ninja-sub">SHINOBI CODE RECORD: <tspan fill="{accent_chakra}">SUSHRUT KALE</tspan> [RANK: S-CLASS GRIND]</text>

    <!-- Missions Counter Badge -->
    <g transform="translate({total_svg_width - 240}, 0)">
      <rect x="0" y="0" width="190" height="32" rx="6" fill="{badge_bg}" stroke="{border_color}" stroke-width="1.2"/>
      <circle cx="16" cy="16" r="6" fill="#FF6A00"/>
      <circle cx="16" cy="16" r="3" fill="#FFD700">
        <animate attributeName="r" values="2;4;2" dur="1.5s" repeatCount="indefinite"/>
      </circle>
      <text x="30" y="15" fill="{text_muted}" font-family="system-ui, sans-serif" font-size="9" font-weight="700">TOTAL JUTSU MISSIONS</text>
      <text x="30" y="27" class="stat-badge">{total:,} COMMITS CLEARED</text>
    </g>
  </g>

  <!-- Labels -->
  {"".join(labels_svg)}
  {"".join(months_svg)}

  <!-- Contribution Grid Cells -->
  <g id="contribGrid">
    {cells_markup}
  </g>

  <!-- Dynamic Rasengan Shockwave Line (Sweeps across grid) -->
  <line y1="{grid_start_y - 8}" y2="{grid_start_y + 7 * step_y + 4}" stroke="{rasengan_cyan}" stroke-width="2" opacity="0.6" filter="url(#chakraGlow)">
    <animate attributeName="x1" values="{run_start_x + 30};{run_end_x + 30}" dur="{anim_duration}s" repeatCount="indefinite"/>
    <animate attributeName="x2" values="{run_start_x + 30};{run_end_x + 30}" dur="{anim_duration}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.2;0.8;0.2" dur="{anim_duration}s" repeatCount="indefinite"/>
  </line>

  <!-- NARUTO RUNNER + SPINNING RASENGAN SPRITE GROUP -->
  <g id="narutoRunnerGroup">
    <!-- Horizontal translation across the entire calendar -->
    <animateTransform attributeName="transform" type="translate"
      values="{run_start_x},{naruto_y}; {run_end_x},{naruto_y}"
      dur="{anim_duration}s"
      repeatCount="indefinite" />

    <!-- Trailing Chakra Particles & Sparks -->
    <g id="chakraTrail">
      <circle cx="-15" cy="15" r="4" fill="#FF6A00" opacity="0.7">
        <animate attributeName="r" values="4;1" dur="0.6s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.8;0" dur="0.6s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-25" cy="10" r="3" fill="{accent_chakra}" opacity="0.6">
        <animate attributeName="r" values="3;0.5" dur="0.5s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.7;0" dur="0.5s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-35" cy="18" r="2.5" fill="#FFD700" opacity="0.5">
        <animate attributeName="r" values="2.5;0" dur="0.7s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.6;0" dur="0.7s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- Pixel Naruto Running Sprite (Authentic pixel vector construction) -->
    <!-- Scale: 2x pixel size for crisp retro look -->
    <g id="narutoSprite" transform="translate(0, 0)">
      <!-- Bobbing running animation -->
      <animateTransform attributeName="transform" type="translate"
        values="0,0; 0,-3; 0,0; 0,-2; 0,0"
        dur="0.4s"
        repeatCount="indefinite"/>

      <!-- Naruto Spiky Yellow Hair -->
      <polygon points="5,2 10,-5 14,0 18,-6 22,1 25,-4 27,4 20,6 7,6" fill="#FFE500" stroke="#E69500" stroke-width="0.8"/>
      
      <!-- Konoha Headband (Navy Cloth + Metal Plate) -->
      <rect x="6" y="5" width="20" height="5" rx="1" fill="#1C263B"/>
      <rect x="10" y="5.5" width="12" height="4" rx="0.8" fill="#C5CFDE"/>
      <circle cx="16" cy="7.5" r="1.2" fill="#202A3D"/>

      <!-- Face / Head (Skin Tone) -->
      <rect x="8" y="10" width="17" height="9" rx="1.5" fill="#FFD2A8"/>
      <!-- Whiskers on cheeks -->
      <line x1="8" y1="13" x2="11" y2="13.5" stroke="#C88452" stroke-width="0.7"/>
      <line x1="8" y1="15" x2="11" y2="15.5" stroke="#C88452" stroke-width="0.7"/>
      <line x1="22" y1="13.5" x2="25" y2="13" stroke="#C88452" stroke-width="0.7"/>
      <line x1="22" y1="15.5" x2="25" y2="15" stroke="#C88452" stroke-width="0.7"/>
      <!-- Determined Eye & Smirk -->
      <rect x="18" y="12" width="3" height="2" fill="#1B2234"/>
      <rect x="19" y="12" width="1" height="1" fill="#00C2FF"/> <!-- Blue eyes! -->
      <line x1="17" y1="17" x2="21" y2="17.5" stroke="#3A2412" stroke-width="0.8"/>

      <!-- Torso: Classic Orange Jumpsuit with Blue Shoulders & White Collar -->
      <path d="M7,19 L25,19 L27,32 L6,32 Z" fill="#FF6A00"/>
      <!-- Blue shoulder yoke -->
      <path d="M7,19 L13,19 L11,26 L6,25 Z" fill="#1C2E56"/>
      <path d="M20,19 L25,19 L26,25 L21,26 Z" fill="#1C2E56"/>
      <!-- White fur/fleece neck collar -->
      <rect x="9" y="18" width="14" height="2.5" rx="1" fill="#FFFFFF"/>
      <!-- Red Uzumaki swirl crest on back/chest -->
      <circle cx="15" cy="25" r="3" fill="#D00000"/>
      <circle cx="15" cy="25" r="1.5" fill="#FF6A00"/>

      <!-- Trailing Arm (thrust backward in famous Naruto run) -->
      <line x1="8" y1="22" x2="-6" y2="14" stroke="#FF6A00" stroke-width="3" stroke-linecap="round"/>
      <circle cx="-6" cy="14" r="2" fill="#FFD2A8"/>

      <!-- Leading Arm (thrust forward wielding Rasengan!) -->
      <line x1="24" y1="22" x2="35" y2="18" stroke="#FF6A00" stroke-width="3.2" stroke-linecap="round"/>
      <circle cx="35" cy="18" r="2.2" fill="#FFD2A8"/>

      <!-- Running Legs (Scissors Cycle) -->
      <g>
        <!-- Leg 1 -->
        <line x1="12" y1="32" x2="7" y2="42" stroke="#FF6A00" stroke-width="3.5" stroke-linecap="round">
          <animate attributeName="x2" values="7;22;7" dur="0.3s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="42;36;42" dur="0.3s" repeatCount="indefinite"/>
        </line>
        <!-- Shin bandage & blue ninja shoe -->
        <circle cx="7" cy="42" r="2" fill="#1B2234">
          <animate attributeName="cx" values="7;22;7" dur="0.3s" repeatCount="indefinite"/>
          <animate attributeName="cy" values="42;36;42" dur="0.3s" repeatCount="indefinite"/>
        </circle>

        <!-- Leg 2 -->
        <line x1="19" y1="32" x2="24" y2="42" stroke="#FF6A00" stroke-width="3.5" stroke-linecap="round">
          <animate attributeName="x2" values="24;8;24" dur="0.3s" repeatCount="indefinite"/>
          <animate attributeName="y2" values="42;35;42" dur="0.3s" repeatCount="indefinite"/>
        </line>
        <circle cx="24" cy="42" r="2" fill="#1B2234">
          <animate attributeName="cx" values="24;8;24" dur="0.3s" repeatCount="indefinite"/>
          <animate attributeName="cy" values="42;35;42" dur="0.3s" repeatCount="indefinite"/>
        </circle>
      </g>
    </g>

    <!-- THE SPINNING RASENGAN ORB -->
    <g id="rasenganOrb" transform="translate(42, 17)">
      <!-- Outer Pulsing Chakra Flare -->
      <circle cx="0" cy="0" r="16" fill="url(#chakraAura)" filter="url(#chakraGlow)">
        <animate attributeName="r" values="14;18;14" dur="0.35s" repeatCount="indefinite"/>
        <animate attributeName="opacity" values="0.7;1;0.7" dur="0.35s" repeatCount="indefinite"/>
      </circle>

      <!-- Dense Glowing Core -->
      <circle cx="0" cy="0" r="9" fill="url(#rasenganCore)" filter="url(#chakraGlow)"/>

      <!-- Rapidly Swirling Chakra Spirals (Pure SVG animateTransform) -->
      <g>
        <animateTransform attributeName="transform" type="rotate"
          from="0" to="360" dur="0.25s" repeatCount="indefinite"/>
        <path d="M-8,0 C-8,-6 0,-8 0,0 C0,6 8,8 8,0" fill="none" stroke="#FFFFFF" stroke-width="1.8" stroke-linecap="round"/>
        <path d="M0,-8 C6,-8 8,0 0,0 C-8,0 -8,8 0,8" fill="none" stroke="{rasengan_cyan}" stroke-width="1.8" stroke-linecap="round"/>
      </g>
      <g>
        <animateTransform attributeName="transform" type="rotate"
          from="360" to="0" dur="0.18s" repeatCount="indefinite"/>
        <circle cx="4" cy="-4" r="1.5" fill="#FFFFFF"/>
        <circle cx="-4" cy="4" r="1.5" fill="{accent_chakra}"/>
        <path d="M-6,-4 C-2,-7 4,-6 5,-2 C6,3 1,6 -3,5" fill="none" stroke="{rasengan_cyan}" stroke-width="1.2"/>
      </g>
    </g>
  </g>

  <!-- Legend in Footer -->
  <g transform="translate({total_svg_width - 240}, {total_svg_height - 18})">
    <text x="-40" y="9" fill="{text_muted}" font-family="system-ui, sans-serif" font-size="9" font-weight="600">CHAKRA LEVEL</text>
    <rect x="35" y="0" width="10" height="10" rx="2" fill="{'#161d2d' if is_dark else '#e8dcbe'}"/>
    <rect x="50" y="0" width="10" height="10" rx="2" fill="{'#803000' if is_dark else '#ff944d'}"/>
    <rect x="65" y="0" width="10" height="10" rx="2" fill="{'#c94d00' if is_dark else '#ff6a00'}"/>
    <rect x="80" y="0" width="10" height="10" rx="2" fill="{'#ff6a00' if is_dark else '#d44800'}"/>
    <rect x="95" y="0" width="10" height="10" rx="2" fill="{'#ffd700' if is_dark else '#8a1c00'}"/>
    <text x="112" y="9" fill="{border_color}" font-family="system-ui, sans-serif" font-size="9" font-weight="800">SAGE MODE</text>
  </g>

  <!-- Footer Tagline -->
  <text x="24" y="{total_svg_height - 9}" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="9" font-weight="600">
    DATTEBAYO! • REAL-TIME COMMIT CHAKRA CONVERTED TO SHINOBI MISSIONS
  </text>
</svg>'''
    return svg

def main():
    parser = argparse.ArgumentParser(description="Generate Naruto Rasengan Contribution SVG")
    parser.add_argument("--username", default="Sushrut-Kale", help="GitHub username")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""), help="GitHub Personal Access Token")
    parser.add_argument("--output-dark", default="dist/naruto-contrib-dark.svg", help="Output path for dark SVG")
    parser.add_argument("--output-light", default="dist/naruto-contrib-light.svg", help="Output path for light SVG")
    args = parser.parse_args()

    total = None
    weeks = None

    if args.token:
        print(f"[*] Querying GitHub GraphQL for user '{args.username}'...")
        total, weeks = fetch_contributions_graphql(args.username, args.token)

    if not weeks:
        print(f"[*] Trying public contribution fallback for '{args.username}'...")
        total, weeks = fetch_contributions_fallback(args.username)

    if not weeks:
        print("[!] Generating synthetic shinobi activity calendar...")
        total, weeks = generate_synthetic_data()

    print(f"[+] Loaded {total} contributions across {len(weeks)} weeks.")

    # Render SVGs
    dark_svg = render_naruto_svg(total, weeks, is_dark=True)
    light_svg = render_naruto_svg(total, weeks, is_dark=False)

    os.makedirs(os.path.dirname(args.output_dark) or '.', exist_ok=True)
    os.makedirs(os.path.dirname(args.output_light) or '.', exist_ok=True)

    with open(args.output_dark, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    print(f"[+] Saved dark SVG to {args.output_dark}")

    with open(args.output_light, "w", encoding="utf-8") as f:
        f.write(light_svg)
    print(f"[+] Saved light SVG to {args.output_light}")

    # Also save fallback copies directly in assets/ so repo has them immediately!
    assets_dark = "assets/naruto-contrib-dark.svg"
    assets_light = "assets/naruto-contrib-light.svg"
    with open(assets_dark, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(assets_light, "w", encoding="utf-8") as f:
        f.write(light_svg)
    print(f"[+] Copied to {assets_dark} and {assets_light} for immediate local fallback")

if __name__ == "__main__":
    main()
