---
layout: post
title:  "Ranger Architecture"
subtitle:   "Ranger 기초 다지기"
categories: review
tags: Apache Ranger
---

## Ranger 아키텍처

<br>

![Ranger](https://cdn.document360.io/0406ed95-101f-4cde-8dd8-308d03444a94/Images/Documentation/hadoop-vpc-23_ranger-architecture.png?sv=2019-07-07&sig=i7Kv3otxbX3UkZ7PBdIWdzM5FK20H3agmM3vMY4IFWs%3D&spr=https%2Chttp&st=2024-01-16T00%3A05%3A56Z&se=2024-01-16T00%3A15%3A56Z&srt=o&ss=b&sp=r)

- 클라이언트측에서 리소스에 접근할 때 Ranger가 중간에서 Policy 기준으로 접근 제어 기능을 수행한다.
- HDFS 외에도 Hive, HBase 등의 컴포넌트의 리소스에 대하여 접근 제어가 가능하게 한다.
- Apache Ranger는 빅데이터 생태계에 걸쳐 일관성 있게 보안 정책을 정의, 관리 및 운영할 수 있도록 중앙화된 프레임워크를 제공한다.

---

<br>

- 보안 관리자는 Apache Ranger 콘솔을 사용하여 파일, 폴더, 데이터베이스, 테이블 또는 열 액세스 정책을 손쉽게 관리할 수 있
- Ranger는 모든 액세스 요청을 실시간으로 추적하고 HDFS 및 Solr을 비롯한 여러 대상 소스를 지원하는 중앙 집중식 감사 위치를 통해 보안 관리자에게 Hadoop 환경에 대한 심층적인 가시성을 제공한다.