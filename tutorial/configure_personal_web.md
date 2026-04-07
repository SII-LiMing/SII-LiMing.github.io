# Configure Personal Website Guide

这份文档说明如何修改和添加以下几个部分：

- `News`
- `Education`
- `Intern`
- `Publications`
- `Honors&Awards`

网站仓库根目录是：

`/Users/syu/LiMing/lm.github.io`

## 1. News

`News` 页对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/talks.html`

首页 `About` 页中的 `News` 区块对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/about.md`

### 修改方法

现在 `News` 使用的是固定 HTML 列表结构。每一条新闻大致长这样：

```html
<li class="news-item"><span class="news-date">🚀 2026.4</span> Joined <a href="https://hyper3d.ai/">Rodin</a> as an <span class="news-highlight">Intern Researcher</span>.</li>
```

你主要可以修改：

- `news-date`
  左侧日期和图标

- 文本内容
  右侧新闻正文

- `<a href="...">`
  超链接

- `<span class="news-highlight">...</span>`
  需要强调的词

### 添加新 News

直接在 `news-list` 里面新增一条 `<li class="news-item">...</li>` 即可。

建议把最新的放在最上面。

## 2. Education

`Education` 独立页面对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/teaching.html`

首页 `About` 页中的 `Education` 区块对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/about.md`

### 修改方法

当前 `Education` 用的是条目式结构，每段经历大致是这样：

```html
<div class="edu-entry">
  <div class="edu-title"><a href="https://www.hit.edu.cn/">Harbin Institute of Technology</a></div>
  <div class="edu-program">B.Eng. in Computer Science and Technology</div>
  <div class="edu-dates">2021.9 - 2025.7</div>
</div>
```

你主要可以改：

- 学校名
- 学校官网链接
- 专业
- 时间

### 添加新的 Education

复制一整段：

```html
<div class="edu-entry"> ... </div>
```

然后修改内容即可。

如果要在首页和独立页面都保持一致，建议两个文件同时修改。

## 3. Intern

`Intern` 页面对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/portfolio.html`

首页 `About` 页中的 `Intern` 区块对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/about.md`

### 修改方法

当前 `Intern` 的结构大致是：

```html
<div class="intern-home-card">
  <div class="intern-home-media">
    <img src="{{ '/images/rodin_logo.jpg' | prepend: base_path }}" alt="deemos Rodin logo">
  </div>
  <div class="intern-home-content">
    <div class="intern-home-title"><a href="https://hyper3d.ai/">deemos</a></div>
    <div class="intern-home-role">Rodin team, Intern Researcher</div>
    <div class="intern-home-desc">Research on 3D generation and editing.</div>
  </div>
</div>
```

你主要可以改：

- 图片路径
- 公司名
- 公司链接
- 岗位标题
- 描述

### 替换图片

把图片放到：

`/Users/syu/LiMing/lm.github.io/images/`

例如：

`/Users/syu/LiMing/lm.github.io/images/company_logo.jpg`

然后把页面里的 `src` 改成：

```liquid
{{ '/images/company_logo.jpg' | prepend: base_path }}
```

## 4. Publications

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

`Honors&Awards` 页面对应文件：

`/Users/syu/LiMing/lm.github.io/_pages/cv.md`

### 修改方法

当前奖项使用时间排序条目结构：

```html
<div class="award-item">
  <div class="award-year">2024</div>
  <div class="award-text">Outstanding Student &amp; Youth League Member, Harbin Institute of Technology</div>
</div>
```

你主要可以改：

- `award-year`
  左侧年份

- `award-text`
  奖项名称和说明

### 添加新的奖项

复制一整段：

```html
<div class="award-item"> ... </div>
```

然后修改年份和奖项内容即可。

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
