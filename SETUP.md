# 🍥 Naruto Shinobi Profile README — Setup & Deployment Guide

This guide details the step-by-step instructions to configure, deploy, and maintain your Naruto-themed GitHub Profile README for **Sushrut-Kale**.

---

## ⚡ 1. Repository Setup & Prerequisites

1. **Repository Name**:
   - The repository **MUST** be named exactly matching your GitHub username:
     ```
     https://github.com/Sushrut-Kale/Sushrut-Kale
     ```
   - The repository visibility **MUST** be set to **Public** for GitHub profile readmes and external widget generators to read your public stats.

---

## ⚙️ 2. GitHub Actions Permissions (Critical for Rasengan Strike)

The Rasengan Contribution Strike workflow (`.github/workflows/naruto-contrib.yml`) queries your GitHub GraphQL contributions and automatically deploys the animated SVGs (`dist/naruto-contrib-dark.svg` and `dist/naruto-contrib-light.svg`) to an orphan `output` branch.

To enable this:
1. Navigate to your repository on GitHub:
   ```
   https://github.com/Sushrut-Kale/Sushrut-Kale/settings/actions
   ```
2. Scroll down to **Workflow permissions**.
3. Select **"Read and write permissions"**.
4. Check **"Allow GitHub Actions to create and approve pull requests"** (optional but recommended).
5. Click **Save**.

---

## 🚀 3. First Manual Run of Rasengan Strike Action

After pushing this repo to GitHub:
1. Go to the **Actions** tab:
   ```
   https://github.com/Sushrut-Kale/Sushrut-Kale/actions
   ```
2. In the left sidebar, click on **"Naruto Rasengan Contribution Strike"**.
3. Click the **"Run workflow"** dropdown on the right side and press **"Run workflow"** (branch: `main`).
4. Wait ~25 seconds for the workflow to complete.
5. Once completed, a new branch named `output` will be created automatically containing:
   - `naruto-contrib-dark.svg`
   - `naruto-contrib-light.svg`
6. The `<picture>` element in your `README.md` will now automatically display your real-time live SVG straight from the `output` branch!
   *(Note: The README includes `./assets/naruto-contrib-dark.svg` as a local fallback so it renders immediately even before the first action run!)*

---

## ✏️ 4. Placeholders to Customize

Search for these placeholders in `README.md` when you are ready to replace them:

| Placeholder | Location in `README.md` | Action Needed |
|---|---|---|
| `Shinobi Scroll [PLACEHOLDER]` | Top Hero Badges (line ~43) | Replace `#` with your live portfolio URL. |
| `ADD_YOUR_PORTFOLIO_URL_HERE` | Contact JSON block (line ~394) | Replace with your portfolio domain or GitHub profile URL. |
| `View Shinobi Scroll` | Contact Badges (line ~407) | Replace `#` with your portfolio URL. |
| `ADD_CAMPUS_TWIN_URL` | Final Valley Showdown (line ~204) | Replace with your live Vercel / deployment URL for Campus Twin, or leave repo-only link. |
| `Sushrut-Kale/mitaoe3d` | Final Valley Showdown (line ~205) | Confirm your 3D campus twin repository is located at `github.com/Sushrut-Kale/mitaoe3d`. |

---

## 🌀 5. Regenerating Contributions Locally

You can run the generator locally at any time:

```bash
# Run using public fallback or your GITHUB_TOKEN
python scripts/generate_naruto_contrib.py --username Sushrut-Kale
```

This will automatically refresh both `dist/` and `assets/` copies.

---

## 📁 6. Directory Overview

```
Sushrut-Kale/
├── .github/
│   └── workflows/
│       ├── naruto-contrib.yml       # Nightly Rasengan contribution generator
│       └── snake.yml                # Legacy / backup workflow
├── assets/
│   ├── CREDITS.md                   # Source attribution for all GIFs & SVGs
│   ├── chakra_pulse.svg             # Custom animated chakra aura divider
│   ├── falling_leaves.svg           # Custom animated Konoha leaves divider
│   ├── kakashi_handsigns.gif        # Hand signs GIF for Jutsu Lab
│   ├── konoha_headband.svg          # Centered metallic Leaf Village headband
│   ├── kurama_eyes.gif              # Kurama Nine-Tails blazing eyes for Chakra Meter
│   ├── naruto-contrib-dark.svg      # Local dark contribution SVG fallback
│   ├── naruto-contrib-light.svg     # Local light contribution SVG fallback
│   ├── naruto_ninja_way.gif         # Naruto thumbs up animation
│   ├── naruto_pixel_run.gif         # Pixel Naruto run sprite
│   ├── naruto_ramen.gif             # Naruto ramen noodle refuel
│   ├── naruto_rasengan.gif          # Rasengan sprint hero banner
│   ├── naruto_shadow_clones.gif     # Kage Bunshin no Jutsu footer team
│   ├── naruto_sprint.gif            # Naruto sprint animation
│   ├── sharingan.gif                # Spinning Tomoe divider
│   └── shuriken_divider.svg         # Animated rolling Shuriken with sparks
├── scripts/
│   └── generate_naruto_contrib.py   # Python SVG animation compiler
├── README.md                        # The complete Naruto Shinobi Profile
└── SETUP.md                         # This setup & configuration document
```
