# 🍥 Naruto Shinobi Profile — Setup & Deployment Guide

This repository contains the rebuilt, graphics-first Naruto Profile README for **Sushrut-Kale**.

---

## ⚡ 1. Repository Setup & Prerequisites

- **Repo Name**: Must be `Sushrut-Kale/Sushrut-Kale` (public visibility).
- **Workflow Permissions**:
  1. Go to **Settings ➔ Actions ➔ General ➔ Workflow permissions**.
  2. Select **"Read and write permissions"**.
  3. Click **Save**.

---

## 🚀 2. Workflows & First Manual Runs

From the **Actions** tab on GitHub, run these three workflows once manually (or wait for the automatic triggers):

1. **Naruto Rasengan Contribution Strike** (`.github/workflows/naruto-contrib.yml`):
   - Generates the animated SVG heatmap and publishes to the `output` branch.
   - Runs automatically on cron (`0 */6 * * *`) and on push to main.
2. **Generate Repo Cards** (`.github/workflows/repo-cards.yml`):
   - Automatically fetches your real GitHub repos and renders matching Naruto scroll cards.
3. **Generate Shinobi Stats** (`.github/workflows/stats.yml`):
   - Compiles local stats overview and language charts.

---

## 🖼️ 3. Adding Real GIFs (Optional)

All slots are equipped with custom hand-drawn animated SVGs by default. If you want to drop in real GIFs:
1. Refer to [`assets/gifs/README.txt`](./assets/gifs/README.txt).
2. Save your downloaded GIF files into `assets/gifs/` (e.g. `hero.gif`, `kurama.gif`).

---

## 🔍 4. Verified Proof Screenshots

The SMIL animation of the Rasengan Contribution Strike was verified in headless Chromium:
- [t = 0s](./docs/proof/strike-t0s.png)
- [t = 4s](./docs/proof/strike-t4s.png)
- [t = 8s](./docs/proof/strike-t8s.png)
