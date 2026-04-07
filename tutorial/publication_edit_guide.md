# Publication Edit Guide

当前 publication 页面主要由这两个位置控制：

- 展示模板：`/Users/syu/LiMing/lm.github.io/_includes/sections/publications.html`
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

排版代码现在在：

`/Users/syu/LiMing/lm.github.io/_includes/sections/publications.html`

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
