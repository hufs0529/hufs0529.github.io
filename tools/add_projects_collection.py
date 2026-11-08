"""_config.yml 에 projects 컬렉션과 기본값을 추가한다(이미 있으면 건너뜀).

    python3 tools/add_projects_collection.py      # 블로그 저장소 루트에서
"""

from pathlib import Path

cfg = Path("_config.yml")
s = cfg.read_text(encoding="utf-8")

if "\n  projects:" not in s:
    old = "collections:\n  tabs:\n    output: true\n    sort_by: order\n"
    assert old in s, "_config.yml 의 collections: tabs: 블록을 찾지 못했습니다. 아래 내용을 손으로 넣어 주세요."
    s = s.replace(old, old + "  projects:            # 포트폴리오 상세 페이지 (_projects/*.md)\n    output: true\n    permalink: /portfolio/:name/\n", 1)

if "type: projects" not in s:
    anchor = "defaults:\n"
    assert anchor in s, "defaults: 블록을 찾지 못했습니다."
    s = s.replace(anchor, anchor + "  - scope:\n      path: \"\"\n      type: projects\n    values:\n      layout: page\n      toc: true\n", 1)

cfg.write_text(s, encoding="utf-8")
print("ok: projects 컬렉션·기본값 반영")
