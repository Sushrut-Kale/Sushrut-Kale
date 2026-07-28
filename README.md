<div align="center">

<img src="https://capsule-render.vercel.app/api?type=venom&color=gradient&customColorList=24&height=180&section=header&text=sushrut_kale.ipynb&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=45" width="100%"/>

<img src="https://img.shields.io/badge/Kernel-Python%203%20(AI%2FML)-blue?style=flat-square&logo=jupyter&logoColor=orange&labelColor=1a1a2e"/>
<img src="https://img.shields.io/badge/Status-Restart%20%26%20Run%20All-success?style=flat-square&labelColor=1a1a2e"/>
<img src="https://komarev.com/ghpvc/?username=Sushrut-Kale&style=flat-square&color=blueviolet&label=views&labelColor=1a1a2e"/>

</div>

---

### `In [1]:`
```python
whoami()
```
### `Out [1]:`
```
Sushrut Kale — 2nd Year, CSE (AI/ML)
MIT Academy of Engineering, Pune  |  CGPA: 8.9

I build systems that model uncertainty instead of hard-coding
answers — a learning agent that tracks what a student actually
knows via Bayesian inference, a solver that untangles an entire
college's timetable instead of doing it by hand.

Currently training on: LLM fine-tuning, distributed systems
```

---

### `In [2]:`
```python
import subprocess
subprocess.run(["pip", "list"])   # what's actually installed
```
### `Out [2]:`

<table>
<tr><td>

**Package**
```
python
javascript / typescript
react
next-js
node-js
fastapi
```

</td><td>

**Version / Notes**
```
3.10+     core language, ML tooling
ES2022    frontend logic
18.x      component layer
16        app router, SSR
—         REST APIs
—         async ML-serving APIs
```

</td></tr>
<tr><td>

```
or-tools
manim
mongodb
firebase
power-bi
gemini-api
```

</td><td>

```
CP-SAT     constraint solving
CE         mathematical animation
—          document store
—          auth + realtime db
DAX        business intelligence
1.5        LLM inference
```

</td></tr>
</table>

<div align="center">
<img src="https://skillicons.dev/icons?i=python,js,ts,react,nextjs,nodejs,fastapi,mongodb,firebase,tailwind,git,github,vercel,docker,vscode&theme=dark&perline=8"/>
</div>

---

### `In [3]:`
```python
import pandas as pd
projects = pd.DataFrame(training_runs)
projects.sort_values("interesting_part", ascending=False)
```
### `Out [3]:`

| # | project | domain | interesting_part | link |
|---|---------|--------|-------------------|------|
| 0 | **Learner-State Engine** | AI / EdTech | Bayesian mastery model + CP-SAT re-planning on every answer | `local` |
| 1 | **CampusCompass** | Optimization | CP-SAT solver turns an Excel upload into a conflict-free college timetable | `local` |
| 2 | **ClubSync** | Full-Stack + AI | Gemini-powered club recommendations, QR attendance | [`live`](https://clubsync-4qua.vercel.app/) |
| 3 | **EduCore** | Full-Stack | Role-based classroom platform, built @ VELORA 2026 | [`live`](https://edu-core-blush.vercel.app/) |
| 4 | **Manim Showcase** | Scientific Viz | Navier–Stokes, wave optics & Q-learning as cinematic animation | `local` |
| 5 | **TradeVision 2030** | Business Intelligence | 51K-row Power BI dashboard mapped to UN SDG 8 & 12 | `local` |

<details>
<summary><b>▸ expand: projects[0].describe()</b> — Learner-State Engine</summary>
<br>

A closed-loop personal learning agent. It keeps a **live, per-topic Bayesian mastery model (BKT)** for each learner and continuously **re-plans their study path via CP-SAT** the moment that model changes — every decision is driven by verified mastery, never a proxy like "video watched."

`Python` `FastAPI` `React` `MongoDB` `Gemini API` `Ollama (offline fallback)`

</details>

<details>
<summary><b>▸ expand: projects[1].describe()</b> — CampusCompass</summary>
<br>

Automated timetable generator for MIT Academy of Engineering. A coordinator uploads a Faculty/Rooms/Time Excel workbook, a **CP-SAT constraint solver** (Google OR-Tools) generates a conflict-free weekly schedule, browsable by faculty, room, and division. The solver is a pure Excel-in/JSON-out service with zero database coupling, by design.

`Next.js 16` `FastAPI` `OR-Tools`

</details>

---

### `In [4]:`
```python
fetch("https://leetcode.com/ryYeqtxZz8/") \
    .then(track_progress)
```
### `Out [4]:`

<div align="center">
<img src="https://leetcard.jacoblin.cool/ryYeqtxZz8?theme=dark&font=Fira%20Code" />
</div>

---

### `In [5]:`
```python
%matplotlib inline
plot_activity(user="Sushrut-Kale")
```
### `Out [5]:`

<div align="center">
<img src="https://github-stats-extended.vercel.app/api?username=Sushrut-Kale&show_icons=true&theme=chartreuse-dark&hide_border=true&bg_color=1a1a2e&title_color=b967ff&icon_color=00d4ff&text_color=e0e0e0" height="165"/>
<img src="https://github-stats-extended.vercel.app/api/top-langs/?username=Sushrut-Kale&layout=compact&theme=chartreuse-dark&hide_border=true&bg_color=1a1a2e&title_color=b967ff&text_color=e0e0e0" height="165"/>
</div>

<div align="center">
<img src="https://github-readme-streak-stats-eight.vercel.app?user=Sushrut-Kale&theme=highcontrast&hide_border=true&background=1a1a2e&ring=b967ff&fire=00d4ff&currStreakLabel=00d4ff" height="165"/>
</div>

<div align="center">
<img src="https://github-profile-trophy.vercel.app/?username=Sushrut-Kale&theme=algolia&no-frame=true&column=4&margin-w=8&margin-h=8&row=1" />
</div>

<div align="center">
<img src="https://raw.githubusercontent.com/Sushrut-Kale/Sushrut-Kale/output/github-contribution-grid-snake.svg" width="90%"/>
</div>

---

### `In [6]:`
```python
history = load_checkpoints()
for epoch in history:
    print(epoch.summary())
```
### `Out [6]:`

```
Epoch 1  (2024)  loss=high        SDG-lab project, Power BI basics
Epoch 2  (2025)  loss=decreasing  ClubSync + EduCore shipped, VELORA 2026
Epoch 3  (2025)  loss=decreasing  CampusCompass — first solver in production
Epoch 4  (2026)  loss=converging  Learner-State Engine — BKT + CP-SAT closed loop
Epoch 5  (now)   loss=?           training on LLM fine-tuning, distributed systems

>>> model has not converged. training continues.
```

---

### `In [7]:`
```python
def connect(): 
    return {
        "linkedin": "linkedin.com/in/sushrut-kale1367",
        "email":    "sushrutkale13@gmail.com",
        "open_to":  ["hackathons", "AI/ML collabs", "open source"],
    }
```
### `Out [7]:`

<div align="center">

<a href="https://www.linkedin.com/in/sushrut-kale1367/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<a href="mailto:sushrutkale13@gmail.com"><img src="https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white"/></a>
<a href="https://leetcode.com/u/ryYeqtxZz8/"><img src="https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=black"/></a>

<br><br>

<sub>Kernel idle. Last checkpoint saved just now.</sub>

<img src="https://capsule-render.vercel.app/api?type=venom&color=gradient&customColorList=24&height=100&section=footer" width="100%"/>

</div>

<!--
========================================================
SETUP + FIX NOTES (delete this block once done)
========================================================

WHY IMAGES BROKE LAST TIME (confirmed, not a guess):
- github-readme-stats.vercel.app: the public instance was
  manually PAUSED by its maintainers (503 DEPLOYMENT_PAUSED,
  ongoing since Jan 2026 — see anuraghazra/github-readme-stats
  issue #4737). Development has since moved to a community fork,
  "GitHub Stats Extended", which is a drop-in replacement.
  FIX APPLIED: swapped every github-readme-stats.vercel.app URL
  to github-stats-extended.vercel.app — same params, same look.
- streak-stats.demolab.com: known intermittent downtime on that
  specific host (widely reported). FIX APPLIED: switched to the
  community-recommended mirror github-readme-streak-stats-eight
  .vercel.app, same project, more stable host.
- leetcard.jacoblin.cool: works, but the `ext=heatmap` option
  can slow it down enough to trip GitHub's image-proxy timeout.
  FIX APPLIED: removed that flag for reliability.

None of this was caused by anything in the file itself — these
are all free, community-run services and occasionally rotate
hosts. If something still looks broken after you push: wait a
minute and hard-refresh, and if it persists, tell me and I'll
swap in another mirror or a fully self-hosted static version.

1) REPO LOCATION (required for every live widget to work):
   This file must be the README.md of a public repo named
   EXACTLY  Sushrut-Kale/Sushrut-Kale  (matches your username).

2) CONTRIBUTION SNAKE (one-time, ~2 min):
   Add .github/workflows/snake.yml in that repo:

   name: generate animated snake
   on:
     schedule:
       - cron: "0 */6 * * *"
     workflow_dispatch: {}
     push:
       branches:
         - main
   jobs:
     generate:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: Platane/snk@v3
           id: snake
           with:
             github_user_name: Sushrut-Kale
             outputs: |
               dist/github-contribution-grid-snake.svg
               dist/github-contribution-grid-snake-dark.svg?palette=github-dark
         - uses: crazy-max/ghaction-github-pages@v4
           with:
             target_branch: output
             build_dir: dist
           env:
             GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

   Then: Settings > Actions > General > enable "Read and write
   permissions" for GITHUB_TOKEN, then run the workflow once
   manually from the Actions tab.

3) LEETCODE CARD:
   Uses your real handle (ryYeqtxZz8) and shows a solved-problem
   breakdown rather than global rank — more meaningful than the
   ~5M rank number right now, and it'll visibly improve as you
   solve more.

4) TROPHY ROW (new):
   Pulls live GitHub achievement trophies (repo count, stars,
   followers, commit streaks, etc.) — fills in automatically,
   no setup needed beyond the repo being named correctly (see 1).
========================================================
-->
