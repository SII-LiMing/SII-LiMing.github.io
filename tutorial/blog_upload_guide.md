# Blog Upload Guide

This document explains how to add a new blog post to the website.

## 1. Create a new post file

All blog posts live in:

`/Users/syu/LiMing/lm.github.io/_posts/`

Create a new Markdown file using this naming pattern:

`YYYY-MM-DD-post-slug.md`

Example:

`2026-04-07-my-new-post.md`

## 2. Add the front matter

Each post should start with:

```yaml
---
title: "My New Post"
date: 2026-04-07
permalink: /posts/2026/04/my-new-post/
tags:
  - tag1
  - tag2
---
```

## 3. Write the content

After the front matter, write normal Markdown content.

Example:

```md
This is my blog post.

## Section

- item 1
- item 2
```

## 4. Deploy

After saving the post:

```bash
cd /Users/syu/LiMing/lm.github.io
git add .
git commit -m "Add blog post"
git push origin main
```

GitHub Pages will then rebuild the website automatically.

## 5. Optional assets

If your post needs images, put them in:

`/Users/syu/LiMing/lm.github.io/images/`

Then reference them in Markdown like:

```md
![caption](/images/example.png)
```
