---
permalink: /
title: "About"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

Hi! I am **Ming Li (李明)**, a first-year Ph.D. student jointly trained by **Zhejiang University**, **Westlake University**, and the **Shanghai Innovation Institute**, advised by [Xiangru Huang](https://en.westlake.edu.cn/faculty/xiangru-huang.html) and [Yanwei Fu](https://yanweifu.github.io/). My research focuses on **3D reconstruction** and **3D generation**, with a particular interest in scalable pipelines for automatically acquiring **high-quality, interactive 3D assets**. I am interested not only in **watertight 3D objects**, but also in the modeling of **cloth and garments**.

## News

- 🚀 **2026.4** Joined [Rodin](https://hyper3d.ai/) as an **Intern Researcher**.
- 🏃 **2026.3** Finished the **2026 Suzhou Taihu Digital Half Marathon** with a **PB of 2:43**.
- 📄 **2026.2** Two papers were accepted to **CVPR 2026**: [ReWeaver](https://arxiv.org/abs/2601.16672) (**first author**) and [NI-Tex](https://arxiv.org/abs/2511.18765) (**second author**).
- 🔬 **2025.7** Joined the [Xiangru Huang Lab](https://rcif.westlake.edu.cn/rcdw/wlcls_2159/pi_2160/202503/t20250323_53628.shtml) at **Westlake University** as a **visiting student**.
- 🎓 **2025.6** Graduated from **Harbin Institute of Technology** with a **B.Eng.**

## Education

<style>
.edu-home-list { margin-top: 1rem; }
.edu-home-entry {
  margin: 0 0 1.4rem 0;
  padding-left: 1rem;
  border-left: 3px solid #d8d8d8;
}
.edu-home-title {
  margin: 0 0 0.2rem 0;
  font-size: 1.15rem;
  line-height: 1.4;
  font-weight: 700;
}
.edu-home-program {
  margin: 0 0 0.15rem 0;
  font-size: 0.98rem;
  color: #555;
}
.edu-home-dates {
  margin: 0;
  font-size: 0.95rem;
  color: #666;
}
</style>

<div class="edu-home-list">
  <div class="edu-home-entry">
    <div class="edu-home-title"><a href="https://www.hit.edu.cn/">Harbin Institute of Technology</a></div>
    <div class="edu-home-program">B.Eng. in Computer Science and Technology</div>
    <div class="edu-home-dates">2021.9 - 2025.7</div>
  </div>

  <div class="edu-home-entry">
    <div class="edu-home-title"><a href="https://www.zju.edu.cn/">Zhejiang University</a> - <a href="https://www.westlake.edu.cn/">Westlake University</a> - <a href="https://www.sii.edu.cn/">Shanghai Innovation Institute</a> Joint Program</div>
    <div class="edu-home-program">Ph.D. in Computer Science and Technology</div>
    <div class="edu-home-dates">2025.10 - 2030.6 (expected)</div>
  </div>
</div>

## Intern

<style>
.intern-home-card {
  display: flex;
  gap: 1.2rem;
  align-items: flex-start;
  margin: 1rem 0 1.6rem 0;
}
.intern-home-media {
  flex: 0 0 180px;
  width: 180px;
}
.intern-home-media img {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  display: block;
}
.intern-home-content {
  flex: 1 1 auto;
  min-width: 0;
}
.intern-home-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.2rem;
  line-height: 1.35;
  font-weight: 700;
}
.intern-home-role {
  margin: 0 0 0.35rem 0;
  font-size: 0.98rem;
  color: #555;
}
.intern-home-desc {
  margin: 0;
  font-size: 0.98rem;
  line-height: 1.65;
  color: #444;
}
@media (max-width: 900px) {
  .intern-home-card {
    flex-direction: column;
  }
  .intern-home-media {
    width: 100%;
    max-width: 240px;
  }
}
</style>

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

## Publications

<style>
.pub-list-home {
  margin-top: 1rem;
}
.pub-home-card {
  display: flex;
  gap: 1.2rem;
  align-items: flex-start;
  margin: 0 0 1.6rem 0;
}
.pub-home-media {
  flex: 0 0 180px;
  width: 180px;
}
.pub-home-media img,
.pub-home-placeholder {
  width: 100%;
  aspect-ratio: 4 / 3;
  border: 1px solid var(--global-border-color);
  border-radius: 10px;
  background: #f5f5f5;
  object-fit: cover;
}
.pub-home-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-size: 0.9rem;
}
.pub-home-content {
  flex: 1 1 auto;
  min-width: 0;
}
.pub-home-title {
  margin: 0 0 0.25rem 0;
  font-size: 1.2rem;
  line-height: 1.35;
  font-weight: 700;
}
.pub-home-authors {
  margin: 0 0 0.3rem 0;
  font-size: 0.98rem;
  line-height: 1.6;
  color: #555;
}
.pub-self {
  font-weight: 700;
}
.pub-home-venue {
  margin: 0.35rem 0 0.75rem 0;
  font-size: 0.98rem;
  font-weight: 700;
  color: #222;
}
.pub-home-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem 0.55rem;
}
@media (max-width: 900px) {
  .pub-home-card {
    flex-direction: column;
  }
  .pub-home-media {
    width: 100%;
    max-width: 260px;
  }
}
</style>

{% assign pubs = site.publications | sort: "date" | reverse %}
<div class="pub-list-home">
  {% for post in pubs %}
    <div class="pub-home-card">
      <div class="pub-home-media">
        {% if post.teaser %}
          <img src="{{ post.teaser | prepend: '/images/' | prepend: base_path }}" alt="{{ post.title }}">
        {% else %}
          <div class="pub-home-placeholder">Teaser / Demo</div>
        {% endif %}
      </div>
      <div class="pub-home-content">
        <div class="pub-home-title">{{ post.title }}</div>
        {% if post.authors_html %}
          <div class="pub-home-authors">{{ post.authors_html }}</div>
        {% else %}
          <div class="pub-home-authors">Author list to be updated.</div>
        {% endif %}
        <div class="pub-home-venue">{{ post.venue_display | default: post.venue }}</div>
        <div class="pub-home-links">
          {% if post.projecturl %}<a class="btn btn--inverse btn--small" href="{{ post.projecturl }}">Project Page</a>{% endif %}
          {% if post.paperurl %}<a class="btn btn--inverse btn--small" href="{{ post.paperurl }}">Paper</a>{% endif %}
          {% if post.arxivurl %}<a class="btn btn--inverse btn--small" href="{{ post.arxivurl }}">arXiv</a>{% endif %}
          {% if post.codeurl %}<a class="btn btn--inverse btn--small" href="{{ post.codeurl }}">Code</a>{% endif %}
          {% if post.dataseturl %}<a class="btn btn--inverse btn--small" href="{{ post.dataseturl }}">Dataset</a>{% endif %}
          {% if post.pressurl %}<a class="btn btn--inverse btn--small" href="{{ post.pressurl }}">Press</a>{% endif %}
        </div>
      </div>
    </div>
  {% endfor %}
</div>
