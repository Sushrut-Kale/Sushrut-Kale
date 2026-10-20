#!/usr/bin/env python3
"""
generate_naruto_contrib.py
Fetches REAL contributions for Sushrut-Kale from GitHub and generates
an animated Naruto Rasengan contribution heatmap SVG with snake-style
2D patrol (Up, Down, Left, Right) striking contribution tiles.
"""

import os
import sys
import re
import math
import argparse
import urllib.request
from datetime import datetime

def fetch_real_github_contributions(username="Sushrut-Kale"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8")
    except Exception as e:
        print(f"[!] Failed to fetch public contributions: {e}", file=sys.stderr)
        return 0, []

    # Total contributions count
    total_match = re.search(r'([0-9,]+)\s+contributions\s+in\s+the\s+last\s+year', html)
    total_count = int(total_match.group(1).replace(",", "")) if total_match else 192

    # Matches td with data-date and data-level
    days_data = re.findall(r'<td[^>]*data-date="([^"]+)"[^>]*data-level="([0-9])"[^>]*>', html)
    if not days_data:
        days_data = re.findall(r'data-date="([^"]+)".*?data-level="([0-9])"', html)

    print(f"[+] Found {len(days_data)} real calendar days for {username}. Total: {total_count}")

    # Map entries by date
    date_map = {}
    for d_str, lvl_str in days_data:
        try:
            date_map[d_str] = int(lvl_str)
        except Exception:
            pass

    if not date_map:
        return total_count, []

    sorted_dates = sorted([datetime.strptime(d, "%Y-%m-%d") for d in date_map.keys()])
    start_date = sorted_dates[0]

    # Group into 7-day columns (weeks) Sunday through Saturday
    week_dict = {}
    for dt in sorted_dates:
        d_str = dt.strftime("%Y-%m-%d")
        weekday = (dt.weekday() + 1) % 7
        week_idx = (dt - start_date).days // 7
        level = date_map[d_str]
        count_map = {0: 0, 1: 2, 2: 5, 3: 8, 4: 15}
        count = count_map.get(level, 0)

        if week_idx not in week_dict:
            week_dict[week_idx] = []
        
        week_dict[week_idx].append({
            "date": d_str,
            "level": level,
            "contributionCount": count,
            "weekday": weekday
        })

    weeks = []
    for w_idx in sorted(week_dict.keys()):
        weeks.append({"contributionDays": week_dict[w_idx]})

    return total_count, weeks

def get_palette_color(level, is_dark):
    if is_dark:
        if level == 0: return "#161B26"
        if level == 1: return "#5C2A00"
        if level == 2: return "#A34400"
        if level == 3: return "#FF6A00"
        return "#FFB347"
    else:
        if level == 0: return "#E8DCBE"
        if level == 1: return "#FF944D"
        if level == 2: return "#FF6A00"
        if level == 3: return "#D44800"
        return "#8A1C00"

def build_svg(total, weeks, is_dark=True):
    theme_name = "dark" if is_dark else "light"
    bg_color = "#0B0F1A" if is_dark else "#F7EFE2"
    border_color = "#FF6A00" if is_dark else "#C85A00"
    text_color = "#F2E3C0" if is_dark else "#0B0F1A"
    text_muted = "#8E9BB0" if is_dark else "#6A583E"
    idle_cell_color = "#161B26" if is_dark else "#E5D9C2"
    badge_bg = "#121826" if is_dark else "#EADBCE"
    
    total_w = 980
    total_h = 280
    grid_x0 = 65
    grid_y0 = 94
    cell_size = 13.0
    cell_gap = 3.5
    step_x = cell_size + cell_gap
    step_y = cell_size + cell_gap
    
    num_weeks = min(len(weeks), 53)
    grid_width = num_weeks * step_x
    D = 22.0  # Master snake loop duration in seconds

    def cell_center(c, r):
        return (grid_x0 + c * step_x + cell_size / 2.0, grid_y0 + r * step_y + cell_size / 2.0)

    # 51-Point Snake Path covering the grid and targeting active cells
    grid_waypoints = [
        (-1.0, 3.0),
        (0.0, 3.0),
        (5.0, 3.0),
        (5.0, 5.0),
        (11.0, 5.0),
        (11.0, 1.0),
        (17.0, 1.0),
        (17.0, 6.0),
        (24.0, 6.0),  # Active strike
        (24.0, 2.0),
        (31.0, 2.0),
        (31.0, 5.0),
        (37.0, 5.0),
        (39.0, 6.0),
        (40.0, 6.0),  # Strike
        (40.0, 3.0),  # Strike
        (40.0, 2.0),  # Strike
        (40.0, 1.0),  # Strike
        (40.0, 0.0),  # Strike
        (41.0, 0.0),
        (41.0, 1.0),  # Strike
        (41.0, 5.0),  # Strike
        (42.0, 5.0),  # Strike
        (42.0, 4.0),  # Strike
        (42.0, 6.0),
        (44.0, 6.0),  # Strike
        (44.0, 0.0),
        (45.0, 0.0),  # Strike
        (47.0, 0.0),
        (48.0, 1.0),  # Strike
        (48.0, 3.0),  # Strike
        (48.0, 5.0),  # Strike
        (48.0, 6.0),  # Strike
        (49.0, 6.0),
        (49.0, 3.0),  # Strike
        (49.0, 2.0),  # Strike
        (49.0, 0.0),  # Strike
        (50.0, 0.0),
        (51.0, 1.0),  # Strike
        (51.0, 2.0),  # Strike
        (51.0, 3.0),  # Strike
        (51.0, 4.0),  # Strike
        (51.0, 5.0),  # Strike
        (52.0, 5.0),
        (52.0, 2.0),  # Strike
        (52.0, 1.0),  # Strike
        (52.0, 0.0),  # Final Grand Boss Strike!
        (53.0, 0.0),
        (53.0, -1.0),
        (-1.0, -1.0),
        (-1.0, 3.0)
    ]

    coords = [cell_center(c, r) for c, r in grid_waypoints]
    dists = [0.0]
    for i in range(1, len(coords)):
        dx = coords[i][0] - coords[i-1][0]
        dy = coords[i][1] - coords[i-1][1]
        dists.append(dists[-1] + math.hypot(dx, dy))

    total_dist = dists[-1]
    keytimes = [d / total_dist for d in dists]

    # Map first hit timestamp for each active cell
    active_hits = {}
    for idx, (c, r) in enumerate(grid_waypoints):
        if 0 <= c < 53 and 0 <= r < 7 and c == int(c) and r == int(r):
            coord_key = (int(c), int(r))
            if coord_key not in active_hits:
                active_hits[coord_key] = keytimes[idx]

    # Build motion path SVG string
    path_cmds = [f"M {coords[0][0]:.1f},{coords[0][1]:.1f}"]
    for x, y in coords[1:]:
        path_cmds.append(f"L {x:.1f},{y:.1f}")
    path_d = " ".join(path_cmds)

    cells_svg = []

    for c in range(num_weeks):
        w = weeks[c]
        col_x = grid_x0 + c * step_x
        days = w.get("contributionDays", [])
        for day in days:
            weekday = day.get("weekday", 0)
            level = day.get("level", 0)
            row_y = grid_y0 + weekday * step_y
            active_col = get_palette_color(level, is_dark)
            idle_col = idle_cell_color

            hit_t = active_hits.get((c, weekday))
            if level > 0 and hit_t is not None:
                t0 = max(0.0, hit_t - 0.002)
                t1 = hit_t
                t2 = min(0.997, hit_t + 0.015)
                t3 = min(0.999, hit_t + 0.035)

                kt = f"0;{t0:.4f};{t1:.4f};{t2:.4f};{t3:.4f};1"
                fill_vals = f"{idle_col};{idle_col};#FFFFFF;#7DF9FF;{active_col};{active_col}"
                op_vals = "0.45;0.45;1;1;0.95;0.95"
                stroke_vals = "none;none;#FFFFFF;#7DF9FF;none;none"
                sw_vals = "0;0;2;1.5;0;0"

                cell_el = f'''<rect x="{col_x}" y="{row_y}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{idle_col}">
    <animate attributeName="fill" values="{fill_vals}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="{op_vals}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/>
    <animate attributeName="stroke" values="{stroke_vals}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/>
    <animate attributeName="stroke-width" values="{sw_vals}" keyTimes="{kt}" dur="{D}s" repeatCount="indefinite"/>
  </rect>'''
            else:
                cell_el = f'<rect x="{col_x}" y="{row_y}" width="{cell_size}" height="{cell_size}" rx="2.5" fill="{idle_col}" opacity="0.6"/>'
            cells_svg.append(cell_el)

    cells_markup = "\n  ".join(cells_svg)

    # Days labels
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    labels_svg = []
    for d_idx, d_name in day_labels:
        ly = grid_y0 + d_idx * step_y + 10.5
        labels_svg.append(f'<text x="{grid_x0 - 12}" y="{ly}" text-anchor="end" fill="{text_muted}" font-family="monospace" font-size="10" font-weight="700">{d_name}</text>')

    # Month labels with clean spacing
    months_svg = []
    last_m = None
    last_w = -5
    for w_idx, w in enumerate(weeks):
        days = w.get("contributionDays", [])
        if not days: continue
        try:
            d_dt = datetime.strptime(days[0]["date"], "%Y-%m-%d")
            m_name = d_dt.strftime("%b")
            if m_name != last_m and (w_idx - last_w) >= 3:
                col_x = grid_x0 + w_idx * step_x
                if col_x < grid_x0 + grid_width - 25:
                    months_svg.append(f'<text x="{col_x}" y="{grid_y0 - 12}" fill="{text_muted}" font-family="monospace" font-size="10" font-weight="700">{m_name}</text>')
                    last_m = m_name
                    last_w = w_idx
        except Exception:
            pass

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {total_w} {total_h}" width="{total_w}" height="{total_h}">
  <defs>
    <linearGradient id="bgGrad_{theme_name}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{bg_color}"/>
      <stop offset="50%" stop-color="{"#0E1424" if is_dark else "#F2E5D3"}"/>
      <stop offset="100%" stop-color="{"#090D17" if is_dark else "#E8DAC2"}"/>
    </linearGradient>
    <radialGradient id="rasenganCore" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="25%" stop-color="#FFFFFF"/>
      <stop offset="55%" stop-color="#7DF9FF"/>
      <stop offset="85%" stop-color="#00C2FF"/>
      <stop offset="100%" stop-color="rgba(0,194,255,0)"/>
    </radialGradient>
    <radialGradient id="rasenganAura" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="rgba(125,249,255,0.7)"/>
      <stop offset="50%" stop-color="rgba(0,194,255,0.3)"/>
      <stop offset="100%" stop-color="rgba(0,194,255,0)"/>
    </radialGradient>
    <filter id="chakraGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3.5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Frame Background -->
  <rect x="2" y="2" width="{total_w - 4}" height="{total_h - 4}" rx="12" fill="url(#bgGrad_{theme_name})" stroke="{border_color}" stroke-width="2"/>

  <!-- Header -->
  <g transform="translate(28, 22)">
    <text x="0" y="16" fill="{text_color}" font-family="system-ui, -apple-system, sans-serif" font-size="15" font-weight="900" letter-spacing="1">⚡ RASENGAN CHAKRA STRIKE <tspan fill="#FF6A00">•</tspan> <tspan fill="{text_muted}" font-size="12">Sushrut-Kale</tspan></text>
    <text x="0" y="34" fill="#FF8C38" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="700" letter-spacing="0.5">SHINOBI MISSIONS SNAKE PATROL • DEVILS OF THE LEAF</text>
  </g>
  
  <!-- Missions Badge Top Right -->
  <g transform="translate({total_w - 190}, 20)">
    <rect x="0" y="0" width="162" height="32" rx="6" fill="{badge_bg}" stroke="{border_color}" stroke-width="1.2"/>
    <circle cx="16" cy="16" r="4" fill="#00C2FF" filter="url(#chakraGlow)">
      <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite"/>
    </circle>
    <text x="30" y="20" fill="#FFD700" font-family="monospace" font-size="11.5" font-weight="800">MISSIONS: {total:,}</text>
  </g>

  <!-- Labels -->
  {"".join(labels_svg)}
  {"".join(months_svg)}

  <!-- Grid Cells -->
  <g id="gridCells">
  {cells_markup}
  </g>

  <!-- Animated Naruto Runner & Rasengan with Snake Motion -->
  <g id="masterRunner">
    <animateMotion
      path="{path_d}"
      dur="{D}s"
      repeatCount="indefinite"/>

    <!-- Trailing Chakra Sparks -->
    <g transform="translate(-20, 0)">
      <circle cx="-10" cy="0" r="3" fill="#FF6A00">
        <animate attributeName="opacity" values="0.8;0;0.8" dur="0.3s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-18" cy="-5" r="2.5" fill="#00C2FF">
        <animate attributeName="opacity" values="0.9;0;0.9" dur="0.25s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-26" cy="6" r="2" fill="#FFD700">
        <animate attributeName="opacity" values="0.7;0;0.7" dur="0.35s" repeatCount="indefinite"/>
      </circle>
    </g>

    <!-- Naruto Ninja Sprite (Trailing behind Rasengan) -->
    <g transform="translate(-24, -18)">
      <animateTransform attributeName="transform" type="translate"
        values="-24,-18; -24,-21; -24,-18" dur="0.3s" repeatCount="indefinite"/>

      <!-- Yellow Spiky Hair -->
      <polygon points="5,3 12,-5 18,1 25,-6 31,2 25,7 7,7" fill="#FFD700"/>
      <polygon points="12,-5 18,1 20,-3" fill="#FFE57F"/>
      
      <!-- Navy Headband & Metal Plate -->
      <rect x="6" y="7" width="22" height="5" rx="1" fill="#1C2E56"/>
      <rect x="10" y="8" width="14" height="3" rx="1" fill="#E2E8F0"/>
      <circle cx="17" cy="9.5" r="1" fill="#1C2E56"/>
      
      <!-- Face & Whiskers -->
      <rect x="7" y="12" width="20" height="9" fill="#FFD2A8"/>
      <!-- Blue Ninja Eyes -->
      <rect x="20" y="13" width="3" height="3" fill="#00C2FF"/>
      <rect x="21" y="14" width="1" height="1" fill="#FFFFFF"/>
      <!-- Whisker Marks -->
      <line x1="10" y1="17" x2="15" y2="17" stroke="#C88B60" stroke-width="1"/>
      <line x1="9" y1="19" x2="14" y2="19" stroke="#C88B60" stroke-width="1"/>

      <!-- Orange Tracksuit Torso & Arms -->
      <rect x="5" y="21" width="22" height="14" rx="2" fill="#FF6A00"/>
      <!-- White fur collar -->
      <rect x="8" y="21" width="14" height="3.5" rx="1" fill="#FFFFFF"/>
      <rect x="7" y="24" width="5" height="5" fill="#1C2E56"/>
      
      <!-- Back arm -->
      <rect x="-4" y="23" width="10" height="4.5" rx="2" fill="#FF6A00"/>
      <!-- Forward arm extending into Rasengan -->
      <rect x="24" y="21" width="12" height="5" rx="2" fill="#FF6A00"/>
      <rect x="33" y="22" width="4" height="4" rx="1" fill="#FFD2A8"/>

      <!-- Running Legs with ninja sandals -->
      <rect x="5" y="35" width="6" height="11" rx="1" fill="#FF6A00"/>
      <rect x="18" y="35" width="6" height="11" rx="1" fill="#FF6A00"/>
      <!-- Navy sandals & wraps -->
      <rect x="3" y="44" width="9" height="4" rx="1" fill="#1C2E56"/>
      <rect x="19" y="44" width="9" height="4" rx="1" fill="#1C2E56"/>
    </g>

    <!-- Blazing Rasengan at (12, 4) - Center of Action! -->
    <g transform="translate(12, 4)" filter="url(#chakraGlow)">
      <!-- Outer Pulsing Glow -->
      <circle cx="0" cy="0" r="22" fill="url(#rasenganAura)">
        <animate attributeName="r" values="18;23;18" dur="0.3s" repeatCount="indefinite"/>
      </circle>
      
      <!-- Middle Chakra Sphere -->
      <circle cx="0" cy="0" r="14" fill="url(#rasenganCore)">
        <animate attributeName="r" values="13;15;13" dur="0.25s" repeatCount="indefinite"/>
      </circle>
      
      <!-- Pure White Core -->
      <circle cx="0" cy="0" r="6" fill="#FFFFFF"/>
      
      <!-- High-speed rotating Wind Swirls -->
      <g>
        <animateTransform attributeName="transform" type="rotate"
          from="0 0 0" to="360 0 0" dur="0.2s" repeatCount="indefinite"/>
        <path d="M-12,0 C-12,-8 0,-12 0,0 C0,8 12,12 12,0" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
        <path d="M0,-12 C8,-12 12,0 0,0 C-8,0 -12,12 0,12" fill="none" stroke="#00C2FF" stroke-width="2.5" stroke-linecap="round"/>
      </g>
      
      <!-- Counter-rotating lightning ring -->
      <g>
        <animateTransform attributeName="transform" type="rotate"
          from="360 0 0" to="0 0 0" dur="0.15s" repeatCount="indefinite"/>
        <circle cx="0" cy="0" r="10" fill="none" stroke="#7DF9FF" stroke-width="1.2" stroke-dasharray="6,4"/>
      </g>
    </g>
  </g>

  <!-- Legend in Footer -->
  <g transform="translate(28, {total_h - 18})">
    <text x="0" y="8" fill="{text_muted}" font-family="monospace" font-size="10" font-weight="700">⚔️ SHINOBI CHAKRA RANKS</text>
  </g>
  <g transform="translate({total_w - 240}, {total_h - 18})">
    <text x="-40" y="8" fill="{text_muted}" font-family="monospace" font-size="10" font-weight="700">LESS</text>
    <rect x="0" y="-1" width="10" height="10" rx="2" fill="{'#161B26' if is_dark else '#E5D9C2'}"/>
    <rect x="16" y="-1" width="10" height="10" rx="2" fill="{'#5C2A00' if is_dark else '#FF944D'}"/>
    <rect x="32" y="-1" width="10" height="10" rx="2" fill="{'#A34400' if is_dark else '#FF6A00'}"/>
    <rect x="48" y="-1" width="10" height="10" rx="2" fill="{'#FF6A00' if is_dark else '#D44800'}"/>
    <rect x="64" y="-1" width="10" height="10" rx="2" fill="{'#FFB347' if is_dark else '#8A1C00'}"/>
    <text x="84" y="8" fill="{text_muted}" font-family="monospace" font-size="10" font-weight="700">MORE</text>
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

    total, weeks = fetch_real_github_contributions(args.username)
    print(f"[+] Loaded {total} real contributions across {len(weeks)} weeks for {args.username}")

    dark_svg = build_svg(total, weeks, is_dark=True)
    light_svg = build_svg(total, weeks, is_dark=False)

    os.makedirs(os.path.dirname(args.output_dark) or '.', exist_ok=True)
    os.makedirs(os.path.dirname(args.output_light) or '.', exist_ok=True)
    os.makedirs("assets", exist_ok=True)

    with open(args.output_dark, "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open(args.output_light, "w", encoding="utf-8") as f:
        f.write(light_svg)

    with open("assets/naruto-contrib-dark.svg", "w", encoding="utf-8") as f:
        f.write(dark_svg)
    with open("assets/naruto-contrib-light.svg", "w", encoding="utf-8") as f:
        f.write(light_svg)

    print("[+] Successfully generated 2D snake-style Rasengan contribution heatmaps!")

if __name__ == "__main__":
    main()
