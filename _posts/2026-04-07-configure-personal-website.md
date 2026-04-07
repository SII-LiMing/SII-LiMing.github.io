---
title: "How I Configure My Personal Website"
date: 2026-04-07
permalink: /posts/2026/04/configure-personal-website/
tags:
  - personal website
  - github pages
  - jekyll
---

This post records the basic workflow I use to maintain my personal website built with **GitHub Pages** and **Jekyll**.

## Site Structure

The website repository is organized around a few key folders:

- `_pages/` for major pages such as About, Publications, Education, Intern, and Honors
- `_publications/` for individual publication entries
- `_posts/` for blog posts
- `images/` for portraits, teasers, logos, and other visual assets
- `tutorial/` for lightweight documentation that I may want to keep inside the repo

## Common Editing Tasks

Here are the files I update most often:

- `about.md` for homepage content
- `publications.html` for publication page layout
- `teaching.html` for education
- `portfolio.html` for intern experience
- `cv.md` for honors and awards
- `_publications/*.md` for individual paper entries

## Deployment Workflow

After editing locally, I deploy with the standard git workflow:

```bash
cd /Users/syu/LiMing/lm.github.io
git add .
git commit -m "Update website"
git push origin main
```

Once the changes are pushed, GitHub Actions automatically rebuilds and deploys the site.

## Notes

- Use local assets whenever possible so the site remains self-contained.
- Keep content files structured and focused; layout logic should stay in page templates.
- If a section needs repeated cards or lists, it is usually better to encode them explicitly in the page rather than overcomplicate the template too early.
