---
layout: post
title:  "RedShift"
subtitle:   "Data Sharing"
categories: review
tags: RedShift
---


## Redshift Data Sharing
- Producer/ Consumer Architecture
    - Producer가 security를 관리한다
    - 데이터는 실시간 그리고 지속적으로 전이 가능해야한다
    - consumer에게 영향을 받는 것을 막기 위해 isolation 필요

 - RA3 node를 사용하여, 암호화해야한다
 - Cross-region data sharing은 transfer charges를 포함한다
 - data share의 종류
    1. Standard
    2. AWS Data Exchange
    3. AWS Lake Formation - managed