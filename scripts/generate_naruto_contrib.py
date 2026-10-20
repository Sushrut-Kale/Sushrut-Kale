#!/usr/bin/env python3
"""
generate_naruto_contrib.py
Autonomous SMIL-animated Naruto Rasengan Contribution Heatmap generator.
"""

import os
import sys
import json
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
            date
            contributionCount
            weekday
          }
        }
      }
    }
  }
}
"""

def fetch_graphql(username, token):
    if not token:
        return None, None
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": "Naruto-Contrib"
    }
    payload = json.dumps({"query": GRAPHQL_QUERY, "variables": {"login": username}}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
            return cal["totalContributions"], cal["weeks"]
    except Exception as e:
        print(f"[!] GraphQL failed: {e}", file=sys.stderr)
        return None, None

def generate_demo_grid():
    random.seed(42)
    weeks = []
    total = 0
    for w in range(53):
        days = []
        for d in range(7):
            r = random.random()
            if r < 0.35:
                c = 0
            elif r < 0.65:
                c = random.randint(1, 3)
            elif r < 0.88:
                c = random.randint(4, 7)
            elif r < 0.96:
                c = random.randint(8, 12)
            else:
                c = random.randint(13, 20)
            total += c
            days.append({
                "contributionCount": c,
                "date": f"2026-w{w:02d}-d{d}",
                "weekday": d
            })
        weeks.append({"contributionDays": days})
    return total, weeks

def get_palette_color(count, is_dark):
    if is_dark:
        if count == 0: return "#161B26"
        if count <= 2: return "#5C2A00"
        if count <= 5: return "#A34400"
        if count <= 9: return "#FF6A00"
        return "#FFB347"
    else:
        if count == 0: return "#E8DCBE"
        if count <= 2: return "#FF944D"
        if count <= 5: return "#FF6A00"
        if count <= 9: return "#D44800"
        return "#8A1C00"

def build_svg(total, weeks, is_dark=True):
    theme_name = "dark" if is_dark else "light"
    bg_color = "#0B0F1A" if is_dark else "#F2E3C0"
    border_color = "#FF6A00" if is_dark else "#C85A00"
    text_color = "#F2E3C0" if is_dark else "#0B0F1A"
    text_muted = "#8E9BB0" if is_dark else "#5A4B32"
    
    total_w = 880
    total_h = 220
    grid_x0 = 65
    grid_y0 = 68
    cell_size = 11
    cell_gap = 3
    step_x = cell_size + cell_gap
    step_y = cell_size + cell_gap
    
    num_weeks = min(len(weeks), 53)
    grid_width = num_weeks * step_x
    D = 10.0  # Master loop duration in seconds

    cells_svg = []

    for c in range(num_weeks):
        w = weeks[c]
        col_x = grid_x0 + c * step_x
        pass_time = c / 53.0
        
        # Calculate keyTimes for single master loop
        t0 = max(0.0, pass_time - 0.001)
        t1 = pass_time
        t2 = min(1.0, pass_time + 0.02)
        t3 = min(1.0, pass_time + 0.07)
        
        kt_str = f"0;{t0:.4f};{t1:.4f};{t2:.4f};{t3:.4f};1"
        
        days = w.get("contributionDays", [])
        for day in days:
            weekday = day.get("weekday", 0)
            count = day.get("contributionCount", 0)
            row_y = grid_y0 + weekday * step_y
            color = get_palette_color(count, is_dark)
            
            if count > 0:
                # Cell burst animation via clean fill & opacity (valid XML and SVG compliant)
                cell_el = f'''<rect x="{col_x}" y="{row_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}">
    <animate attributeName="fill" values="{color};{color};#7DF9FF;#FFD700;{color};{color}"
      keyTimes="{kt_str}" dur="{D}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.75;0.75;1;0.9;0.75;0.75"
      keyTimes="{kt_str}" dur="{D}s" repeatCount="indefinite"/>
  </rect>'''
            else:
                cell_el = f'<rect x="{col_x}" y="{row_y}" width="{cell_size}" height="{cell_size}" rx="2" fill="{color}"/>'
            cells_svg.append(cell_el)

    cells_markup = "\n  ".join(cells_svg)

    # Days labels
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    labels_svg = []
    for d_idx, d_name in day_labels:
        ly = grid_y0 + d_idx * step_y + 9
        labels_svg.append(f'<text x="{grid_x0 - 10}" y="{ly}" text-anchor="end" fill="{text_muted}" font-family="monospace" font-size="9" font-weight="600">{d_name}</text>')

    # Month labels
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    months_svg = []
    for m_i, m_name in enumerate(month_names):
        mx = grid_x0 + int(m_i * 4.41 * step_x)
        if mx < grid_x0 + grid_width - 15:
            months_svg.append(f'<text x="{mx}" y="{grid_y0 - 8}" fill="{text_muted}" font-family="monospace" font-size="9" font-weight="700">{m_name}</text>')

    runner_y = grid_y0 + int(3.5 * step_y) - 20
    runner_start_x = grid_x0 - 45
    runner_end_x = grid_x0 + grid_width + 30

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}">
  <defs>
    <linearGradient id="bgGrad_{theme_name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_color}"/>
      <stop offset="100%" stop-color="{"#121826" if is_dark else "#E6D8BA"}"/>
    </linearGradient>
    <radialGradient id="rasenganGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#7DF9FF"/>
      <stop offset="65%" stop-color="#00C2FF"/>
      <stop offset="100%" stop-color="rgba(0,194,255,0)"/>
    </radialGradient>
    <filter id="chakraFilter" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Frame Background -->
  <rect x="2" y="2" width="{total_w - 4}" height="{total_h - 4}" rx="10" fill="url(#bgGrad_{theme_name})" stroke="{border_color}" stroke-width="2"/>

  <!-- Header -->
  <g transform="translate(24, 22)">
    <text x="0" y="16" fill="{text_color}" font-family="system-ui, -apple-system, sans-serif" font-size="14" font-weight="800" letter-spacing="1">⚡ RASENGAN CHAKRA STRIKE <tspan fill="#FF6A00">•</tspan> <tspan fill="{text_muted}" font-size="11">Sushrut-Kale</tspan></text>
    <text x="0" y="32" fill="{text_muted}" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="600">SHINOBI MISSION COMMIT HEATMAP</text>
  </g>
  <g transform="translate({total_w - 180}, 22)">
    <rect x="0" y="0" width="156" height="28" rx="6" fill="{"#121826" if is_dark else "#E0D0B0"}" stroke="{border_color}" stroke-width="1"/>
    <text x="14" y="18" fill="#FFD700" font-family="monospace" font-size="11" font-weight="700">MISSIONS: {total:,}</text>
  </g>

  <!-- Labels -->
  {"".join(labels_svg)}
  {"".join(months_svg)}

  <!-- Grid Cells -->
  <g id="gridCells">
  {cells_markup}
  </g>

  <!-- Master Animated Runner & Rasengan Group -->
  <g id="masterRunner">
    <animateTransform attributeName="transform" type="translate"
      values="{runner_start_x},{runner_y}; {runner_end_x},{runner_y}"
      keyTimes="0;1"
      dur="{D}s"
      repeatCount="indefinite"/>

    <!-- Trailing Spark Particles -->
    <circle cx="-12" cy="16" r="3" fill="#FF6A00">
      <animate attributeName="opacity" values="0.8;0;0.8" dur="0.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="-22" cy="12" r="2.5" fill="#00C2FF">
      <animate attributeName="opacity" values="0.9;0;0.9" dur="0.35s" repeatCount="indefinite"/>
    </circle>
    <circle cx="-32" cy="18" r="2" fill="#FFD700">
      <animate attributeName="opacity" values="0.7;0;0.7" dur="0.5s" repeatCount="indefinite"/>
    </circle>

    <!-- Pixel Art Naruto Runner with bobbing running motion -->
    <g>
      <animateTransform attributeName="transform" type="translate"
        values="0,0; 0,-2.5; 0,0" dur="0.3s" repeatCount="indefinite"/>
      <!-- Yellow Hair -->
      <polygon points="4,2 10,-4 15,1 20,-5 25,2 20,6 6,6" fill="#FFD700"/>
      <!-- Navy Headband & Metal Plate -->
      <rect x="5" y="6" width="18" height="4" fill="#1C2E56"/>
      <rect x="8" y="7" width="12" height="2.5" fill="#E2E8F0"/>
      <!-- Face -->
      <rect x="6" y="10" width="16" height="7" fill="#FFD2A8"/>
      <!-- Eye -->
      <rect x="16" y="11" width="2" height="2" fill="#00C2FF"/>
      <!-- Orange Torso -->
      <rect x="4" y="17" width="18" height="12" fill="#FF6A00"/>
      <rect x="8" y="17" width="10" height="3" fill="#FFFFFF"/>
      <rect x="6" y="20" width="4" height="4" fill="#1C2E56"/>
      <!-- Back arm -->
      <rect x="-4" y="18" width="8" height="3.5" fill="#FF6A00"/>
      <!-- Front arm pointing forward holding Rasengan -->
      <rect x="22" y="16" width="12" height="4" fill="#FF6A00"/>
      <!-- Running Legs -->
      <rect x="4" y="29" width="5" height="9" fill="#FF6A00"/>
      <rect x="15" y="29" width="5" height="9" fill="#FF6A00"/>
      <rect x="2" y="38" width="7" height="3" fill="#1C2E56"/>
      <rect x="17" y="38" width="7" height="3" fill="#1C2E56"/>
    </g>

    <!-- Spinning Cyan Rasengan in front of Naruto -->
    <g transform="translate(42, 18)" filter="url(#chakraFilter)">
      <!-- Outer Pulsing Aura -->
      <circle cx="0" cy="0" r="16" fill="url(#rasenganGlow)">
        <animate attributeName="r" values="14;18;14" dur="0.3s" repeatCount="indefinite"/>
      </circle>
      <!-- Core -->
      <circle cx="0" cy="0" r="7" fill="#FFFFFF"/>
      <!-- Rotating Swirls -->
      <g>
        <animateTransform attributeName="transform" type="rotate"
          from="0 0 0" to="360 0 0" dur="0.25s" repeatCount="indefinite"/>
        <path d="M-9,0 C-9,-6 0,-9 0,0 C0,6 9,9 9,0" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"/>
        <path d="M0,-9 C6,-9 9,0 0,0 C-6,0 -9,9 0,9" fill="none" stroke="#00C2FF" stroke-width="2" stroke-linecap="round"/>
      </g>
    </g>
  </g>

  <!-- Legend in Footer -->
  <g transform="translate({total_w - 220}, {total_h - 14})">
    <text x="-40" y="8" fill="{text_muted}" font-family="monospace" font-size="9" font-weight="600">LESS</text>
    <rect x="0" y="0" width="9" height="9" rx="2" fill="{'#161B26' if is_dark else '#e8dcbe'}"/>
    <rect x="14" y="0" width="9" height="9" rx="2" fill="{'#5C2A00' if is_dark else '#ff944d'}"/>
    <rect x="28" y="0" width="9" height="9" rx="2" fill="{'#A34400' if is_dark else '#ff6a00'}"/>
    <rect x="42" y="0" width="9" height="9" rx="2" fill="{'#FF6A00' if is_dark else '#d44800'}"/>
    <rect x="56" y="0" width="9" height="9" rx="2" fill="{'#FFB347' if is_dark else '#8a1c00'}"/>
    <text x="74" y="8" fill="{text_muted}" font-family="monospace" font-size="9" font-weight="600">MORE</text>
  </g>
</svg>'''
    return svg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="Sushrut-Kale")
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN", ""))
    parser.add_argument("--output-dark", default="dist/naruto-contrib-dark.svg")
    parser.add_argument("--output-light", default="dist/naruto-contrib-light.svg")
    args = parser.parse_args()

    total, weeks = fetch_graphql(args.username, args.token)
    if not weeks:
        print("[!] Generating demo shinobi grid fallback...")
        total, weeks = generate_demo_grid()

    print(f"Total: {total}, Weeks: {len(weeks)}")

    dark_svg = build_svg(total, weeks, is_dark=True)
    light_svg = build_svg(total, weeks, is_dark=False)

    os.makedirs(os.path.dirname(args.output_dark) or '.', exist_ok=True)
    os.makedirs(os.path.dirname(args.output_light) or '.', exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    with open(args.output_dark, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(args.output_light, "w", encoding="utf-8") as f:
        f.write(light_svg)

    # Local committed fallback
    with open("assets/naruto-contrib-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/naruto-contrib-light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)

    print("Generated dist/naruto-contrib-*.svg and assets/naruto-contrib-*.svg successfully!")

if __name__ == "__main__":
    main()
