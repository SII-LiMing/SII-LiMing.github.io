# Configure Personal Website Guide

这份文档说明如何修改和添加以下几个部分。

当前网站已经做了**单一内容源重构**：

- `About` 页面和对应独立页面不再各自维护一份内容
- 而是通过 `_data/*.yml` + `_includes/sections/*.html` 共享同一份源

也就是说，后续如果你要同时更新首页和对应栏目页，通常只需要改一份数据或一个 section include。

这份文档覆盖以下几个部分：

- `News`
- `Education`
- `Intern`
- `Publications`
- `Honors&Awards`

网站仓库根目录是：

`/Users/syu/LiMing/lm.github.io`

## 1. News

`News` 的共享数据源：

`/Users/syu/LiMing/lm.github.io/_data/news.yml`

`News` 的展示模板：

`/Users/syu/LiMing/lm.github.io/_includes/sections/news.html`

`News` 独立页面对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/talks.html`

首页 `About` 页中的 `News` 区块对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/about.md`

### 修改方法

现在 `talks.html` 和 `about.md` 都只是引用：

```liquid
{% include sections/news.html %}
```

真正的数据在 `news.yml`。每一条新闻大致长这样：

```yaml
- date: "2026.4"
  icon: "🚀"
  html: 'Joined <a href="https://hyper3d.ai/">Rodin</a> as an <span class="news-highlight">Intern Researcher</span>.'
```

你主要修改：

- `date`
  日期

- `icon`
  左侧图标

- `html`
  新闻正文，里面可以包含链接和高亮 HTML

### 添加新 News

直接在：

`/Users/syu/LiMing/lm.github.io/_data/news.yml`

里新增一条 YAML 记录即可。

建议把最新的放在最上面。

## 2. Education

`Education` 的共享数据源：

`/Users/syu/LiMing/lm.github.io/_data/education.yml`

`Education` 的展示模板：

`/Users/syu/LiMing/lm.github.io/_includes/sections/education.html`

`Education` 独立页面对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/teaching.html`

首页 `About` 页中的 `Education` 区块对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/about.md`

### 修改方法

现在 `teaching.html` 和 `about.md` 都只是引用 include。

真正的数据在 `education.yml`。每段经历大致是这样：

```yaml
- title_html: '<a href="https://www.hit.edu.cn/">Harbin Institute of Technology</a>'
  program: "B.Eng. in Computer Science and Technology"
  dates: "2021.9 - 2025.7"
```

你主要可以改：

- `title_html`
  学校名和超链接

- 专业
- 时间

### 添加新的 Education

直接在：

`/Users/syu/LiMing/lm.github.io/_data/education.yml`

里新增一条 YAML 记录即可。

## 3. Intern

`Intern` 的共享数据源：

`/Users/syu/LiMing/lm.github.io/_data/intern.yml`

`Intern` 的展示模板：

`/Users/syu/LiMing/lm.github.io/_includes/sections/intern.html`

`Intern` 页面对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/portfolio.html`

首页 `About` 页中的 `Intern` 区块对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/about.md`

### 修改方法

现在 `portfolio.html` 和 `about.md` 都是通过 include 渲染。

真正的数据在：

`/Users/syu/LiMing/lm.github.io/_data/intern.yml`

结构大致如下：

```yaml
company_html: '<a href="https://hyper3d.ai/">deemos</a>'
team_role: "Rodin team, Intern Researcher"
description: "Research on 3D generation and editing."
logo: "rodin_logo.jpg"
logo_alt: "deemos Rodin logo"
```

你主要可以改：

- `company_html`
  公司名和超链接

- `team_role`
  第二行

- `description`
  描述

- `logo`
  图片文件名

- `logo_alt`
  图片说明文字

### 替换图片

把图片放到：

`/Users/syu/LiMing/lm.github.io/images/`

例如：

`/Users/syu/LiMing/lm.github.io/images/company_logo.jpg`

然后在 `intern.yml` 里把：

```yaml
logo: "company_logo.jpg"
```

改掉即可。

## 4. Publications

`Publications` 目前的内容源已经是单一的，不存在首页和独立页分别维护条目数据的问题。

首页和独立页面都通过同一个 section 模板渲染：

- `/Users/syu/LiMing/lm.github.io/_includes/sections/publications.html`

以下内容直接复用现有 publication 教程。

---

# Publication Edit Guide

当前 publication 页面由这两个位置控制：

- 页面模板：`/Users/syu/LiMing/lm.github.io/_pages/publications.html`
- 论文条目：`/Users/syu/LiMing/lm.github.io/_publications/*.md`

## 1. 新增一篇论文

在目录：

`/Users/syu/LiMing/lm.github.io/_publications/`

下新建一个 `.md` 文件。建议命名格式：

`YYYY-MM-DD-short-name.md`

例如：

`2026-02-20-reweaver.md`

## 2. 每篇论文需要填写的字段

最小模板如下：

```yaml
---
title: "Paper Title"
collection: publications
category: conferences
permalink: /publication/paper-slug
date: 2026-02-20
venue_display: "CVPR 2026"
authors_html: 'Author A, <span class="pub-self">Ming Li</span>, Author C'
teaser:
projecturl:
paperurl:
arxivurl:
codeurl:
dataseturl:
pressurl:
---
```

## 3. 字段说明

- `title`
  论文标题

- `date`
  用于排序。publication 页面按日期从新到旧展示

- `venue_display`
  展示的会议/期刊名称
  如果还在投稿，直接写：
  `Under Review`

- `authors_html`
  作者列表
  如果要高亮你自己的名字，请这样写：
  `<span class="pub-self">Ming Li</span>`

- `teaser`
  左侧预览图文件名
  如果暂时没有，就留空

- `projecturl`
  Project Page 按钮链接

- `paperurl`
  Paper 按钮链接

- `arxivurl`
  arXiv 按钮链接

- `codeurl`
  Code 按钮链接

- `dataseturl`
  Dataset 按钮链接

- `pressurl`
  报道 / 新闻 / Media 按钮链接

## 4. 如何添加 teaser 图片

如果你后面要补左侧图片，建议把图片放到：

`/Users/syu/LiMing/lm.github.io/images/`

例如：

`/Users/syu/LiMing/lm.github.io/images/reweaver_teaser.png`

然后在对应论文条目里写：

```yaml
teaser: "reweaver_teaser.png"
```

如果 `teaser` 为空，页面会自动显示一个空的占位框。

## 5. 如何修改 publication 页面排版

排版代码在：

`/Users/syu/LiMing/lm.github.io/_pages/publications.html`

你主要会改到两类内容：

- 上面的 `<style> ... </style>`
  控制卡片布局、字号、间距、按钮样式

- 下面的循环：
  `for post in pubs`
  控制每篇论文显示哪些字段

## 6. 修改后如何部署

进入仓库目录：

```bash
cd /Users/syu/LiMing/lm.github.io
```

提交并推送：

```bash
git add .
git commit -m "Update publications"
git push origin main
```

推送后 GitHub Pages 会自动部署。

---

## 5. Honors&Awards

`Honors&Awards` 的共享数据源：

`/Users/syu/LiMing/lm.github.io/_data/honors.yml`

`Honors&Awards` 的展示模板：

`/Users/syu/LiMing/lm.github.io/_includes/sections/honors.html`

`Honors&Awards` 页面对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/cv.md`

### 修改方法

现在 `cv.md` 只负责 include，真正的数据在：

`/Users/syu/LiMing/lm.github.io/_data/honors.yml`

每条奖项大致这样写：

```yaml
- year: "2024"
  text: "Outstanding Student & Youth League Member, Harbin Institute of Technology"
```

你主要可以改：

- `year`
  左侧年份

- `text`
  奖项名称和说明

### 添加新的奖项

直接在：

`/Users/syu/LiMing/lm.github.io/_data/honors.yml`

里新增一条 YAML 记录即可。

建议按照时间从新到旧排列。

## 6. 通用部署方法

所有修改完成后，进入仓库目录：

```bash
cd /Users/syu/LiMing/lm.github.io
```

然后执行：

```bash
git add .
git commit -m "Update website content"
git push origin main
```

GitHub Pages 会自动重新部署网站。
