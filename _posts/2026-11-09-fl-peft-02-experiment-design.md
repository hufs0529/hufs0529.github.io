---
title: "[FL × QLoRA #2] 실험 설계 — 3 × 2 × 4 = 24조합 전수, 네 축 지표"
short_title: "24조합 실험 설계"
date: 2026-11-09 07:02:00 +0900
categories: [Portfolio, FL PEFT Research]
tags: [federated-learning, experiment-design, dirichlet, non-iid, flower, peft]
project: fl-peft-quantization
series_order: 2
mermaid: true
description: 압축 3단계 × FL 알고리즘 2개 × Dirichlet α 4단계 전수 요인 설계, 카테고리별 Dirichlet 파티셔닝, LoRA 학습 설정, 성능 · 속도 · 메모리 · 통신 네 축 지표를 정리합니다.
---

{% include portfolio-style.html %}
{% include project-series.html %}

## 요인 설계 — 상호작용을 보려면 격자 전체가 필요하다

| 요인 | 수준 | 선택 이유 |
| --- | --- | --- |
| **압축** | 무압축 bf16 (LoRA) / INT8 (QLoRA) / NF4 4bit (QLoRA) | 양자화 강도 3단계. 8bit 는 중간 지점 |
| **FL 알고리즘** | FedAvg / FedProx (μ=0.01) | 드리프트 교정 유무 비교 |
| **데이터 이질성** | Dirichlet α = 0.1 / 1 / 10 / 100 | 1000배 범위. α=100 은 near-IID 끝점 |

일부 조합만 골라 돌리면 *압축 × α* 의 상호작용을 볼 수 없습니다. 그래서 **3 × 2 × 4 = 24조합을 전부** 돌렸습니다. 대신 예산 안에 넣으려고 모델을 줄였습니다(3B → 1.5B → **Qwen2.5-0.5B-Instruct**).

## 설계는 세 번 바뀌었다

| 변경 | 이전 | 이후 | 근거 |
| --- | --- | --- | --- |
| 연구 초점 | 3 FL × 2 PEFT (6조합) | **3 압축 × 2 FL × 3 α (18조합)** | *압축률과 non-IID 강도의 관계* 를 중심축으로 삼으라는 피드백 |
| 평가 주체 | 대표 클라이언트 경유 | **서버 직접 평가** | 같은 held-out 이라 값은 같지만 *서버가 평가한다* 는 구조를 코드로 드러내야 함 |
| α 범위 | 0.1 / 1 / 10 | **+ α=100 (24조합)** | near-IID 끝점 필요 |

변경마다 근거를 커밋 메시지에 남기고, 주차별 브랜치(`week1`~`week6`)에 그 시점 코드를 보존했습니다.

## 데이터 파티셔닝 — 카테고리별 Dirichlet

Dolly-15k(15,011건)의 지시 카테고리(open_qa, closed_qa, summarization 등)를 기준으로, 카테고리마다 Dirichlet(α) 에서 비율을 뽑아 8개 클라이언트에 나눴습니다(seed 42).

| | α = 0.1 | α = 100 |
| --- | --- | --- |
| 클라이언트별 최다 카테고리 비중 | **66%** | 25% |
| 샤드 크기 범위 | 119 ~ 3,047건 | 1,645 ~ 1,773건 |

α=0.1 에서는 한 클라이언트가 `open_qa` 만 99% 받는 식으로 극단적으로 쏠립니다.

## 학습 설정

| 항목 | 값 |
| --- | --- |
| 클라이언트 | 8대, 매 라운드 전원 참여 (`fraction_fit=1.0`) |
| PEFT | LoRA r=8, α=16, dropout 0.05, target = `q_proj`, `v_proj` → 학습 파라미터 540,672개 (전체의 0.11%) |
| 최적화 | AdamW, lr 2e-4, micro-batch 4 × accumulation 4 (유효 16), max_len 512 |
| 라운드 | 최대 10, *3라운드 연속 개선률 < 1%* 면 조기 종료 |
| 평가 | 서버가 held-out 1,497건으로 매 라운드 PPL, ROUGE-L 은 마지막 라운드에 층화 표본 200건 1회 |
| 환경 | NVIDIA A10G (23GB) · 총 33.7 GPU-시간 |

## 네 축 지표 — 한 축의 이득이 다른 축의 대가일 수 있다

| 축 | 지표 |
| --- | --- |
| 성능 | `val_loss`, `val_perplexity`, `rouge_l` |
| 속도 | `round_latency_sec`, 수렴 라운드 수 |
| 메모리 | `peak_vram_gb` |
| 통신 | `communication_bytes_this_round` |

압축이 메모리에서 이득을 주면서 다른 축에서 대가를 요구할 수 있다고 보고 **네 축을 모두** 기록했습니다. 결과적으로 이 선택이 가장 유용한 발견, *INT8 은 품질 손실 없이 2.2배 느리다* (4편)를 만들었습니다.

PPL(teacher forcing 기반)과 ROUGE-L(실제 생성 기반)은 측정 원리가 다른 두 지표라, 둘이 같은 방향을 가리키면 결론을 더 믿을 수 있습니다.
