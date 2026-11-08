---
# 사이드바 탭. order 가 작을수록 위에 보인다(기본 탭: categories 1 · tags 2 · archives 3 · about 4)
icon: fas fa-briefcase
order: 0
title: Portfolio
---

{% include portfolio-style.html %}

데이터 엔지니어링 프로젝트 모음입니다. 카드를 누르면 프로젝트의 구조·설계·기능을 정리한 상세 페이지로, 상세 페이지에서는 기능별 설명 글로 들어갈 수 있습니다.

<div class="pf-grid">
{%- for p in site.data.projects -%}
{%- assign url = '/portfolio/' | append: p.id | append: '/' | relative_url -%}
<article class="pf-card{% if p.featured %} featured{% endif %}">
<a class="pf-cover-link" href="{{ url }}"><img class="pf-cover" src="{{ p.cover | relative_url }}" alt="{{ p.title }}" loading="lazy"></a>
<div class="pf-body">
<h3><a href="{{ url }}">{{ p.title }}</a>{% if p.status %}<span class="pf-status">{{ p.status }}</span>{% endif %}</h3>
<div class="pf-meta">{{ p.period }}{% if p.role %} · {{ p.role }}{% endif %}</div>
<p class="pf-summary">{{ p.summary }}</p>
{%- if p.highlights and p.featured -%}
<ul class="pf-hl">{% for h in p.highlights %}<li>{{ h }}</li>{% endfor %}</ul>
{%- endif -%}
<div class="pf-tags">{% for s in p.stack %}<span>{{ s }}</span>{% endfor %}</div>
<div class="pf-links"><a href="{{ url }}">상세 보기 →</a>{% if p.repo %}<a href="{{ p.repo }}" target="_blank" rel="noopener">GitHub</a>{% endif %}</div>
</div>
</article>
{%- endfor -%}
</div>
