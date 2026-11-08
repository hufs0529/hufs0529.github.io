---
title: "[단비 P1 #12] 실제 AWS 배포 트러블슈팅 — 코드와 테스트가 통과해도 클라우드에서 막힌 것들"
short_title: "실제 AWS 배포 트러블슈팅"
date: 2026-11-08 08:12:00 +0900
categories: [Portfolio, Danbi P1]
tags: [aws, troubleshooting, terraform, flink, msk, mwaa, emr, lake-formation]
project: danbi-p1
series_order: 12
description: 로컬 테스트를 모두 통과한 코드를 실제 AWS 에 올리며 만난 관리형 서비스의 숨은 제약과, 원인을 확정하고 고친 과정을 정리합니다.
---

{% include portfolio-style.html %}
{% include project-series.html %}

로컬에서는 테스트가 모두 통과했습니다. 하지만 실제 AWS 에 올리자 *문서에 잘 드러나지 않는 제약* 이 서비스마다 하나씩 나왔습니다. 원인 하나당 커밋 하나로 고쳤고, 커밋 메시지에 *왜·무엇·검증* 을 남겼습니다.

## 한눈에 보기

| # | 서비스 | 증상 | 원인 | 해결 |
| --- | --- | --- | --- | --- |
| 1 | Terraform | 첫 plan 에서 `Invalid count` | `count` 가 apply 후에야 정해지는 값(버킷 ARN, 정책 JSON)에 걸림 | plan 시점에 아는 bool 변수로 |
| 2 | SSM | 빈 값 저장 실패 | Parameter Store 는 빈 문자열을 거부 | 빈 값은 `"none"` 으로 |
| 3 | IAM | 역할·보안 그룹 생성 실패 | description 은 ASCII·Latin-1 만 | 영어 설명 + 한국어 주석 |
| 4 | MSK | `Unsupported InstanceType` | KRaft 모드는 t3.small 미지원 | ZooKeeper 모드 Kafka 3.9.x |
| 5 | MSK | 레지스트리 그룹 가입 시간 초과 | 내부 토픽 기본 복제 수 3 > 브로커 2 | 내부 토픽 복제 수 2 |
| 6 | MSK IAM | `ClusterAuthorizationException` | 멱등 프로듀서는 클러스터 단위 `WriteDataIdempotently` 필요 | IAM 정책 추가 |
| 7 | Schema Registry | 컨테이너가 시작 전 점검에서 종료 | 점검 도구가 별도 클래스패스라 IAM jar 를 못 찾음 | jar 를 그 경로에도 |
| 8 | librdkafka | `Broker transport failure` | AdminClient 는 `poll()` 안에서만 IAM 토큰 콜백 실행 | 생성 직후 `poll()` |
| 9 | MSK Connect | 플러그인 생성 실패 | 이름에 점(.) 불가 | 버전의 점을 하이픈으로 |
| 10 | Managed Flink | `NoClassDefFoundError` → `NoSuchMethodError` | 런타임에 Hadoop 없음 + 부모 우선 로딩, Hadoop 만 relocation 하면 `HadoopUtils` 와 어긋남 | Hadoop 과 `HadoopUtils` 를 함께 relocation |
| 11 | Managed Flink | `AuthenticateCallbackHandler` 없음 | SQL Kafka 커넥터는 kafka-clients 를 숨긴 이름으로 포함 | MSK IAM 라이브러리 참조를 같은 이름으로 relocation (적용 후 재배포 확인 필요) |
| 12 | PyFlink | `Column 'ok' not found` | UDTF 에 ROW 하나를 주면 컬럼 1개로 취급 | 컬럼별 타입 + `AS d(컬럼들)` |
| 13 | EMR Serverless | `datetime.UTC` 없음 | EMR 7 의 PySpark 는 Python 3.9 | 3.9 호환 코드 |
| 14 | MWAA | `INCORRECT_CONFIGURATION` | 원본 버킷과 같은 KMS 키를 써야 하는데 키 정책에 Logs 허용 없음 | 키 정책에 CloudWatch Logs 허용 |
| 15 | Lake Formation | EMR 이 있는 테이블을 "없다" 고 함 | LF 관리 DB 에 Describe 권한 없음 | 거버넌스 스택 선적용 |
| 16 | Lake Formation | MWAA 의 Athena 쿼리 실패 | IAM `lakeformation:GetDataAccess` 누락 | 실행 역할에 추가 |

## 가장 오래 걸린 문제 — Flink 클래스로딩

Managed Flink 에서 Iceberg Glue 카탈로그를 만들자마자 실패했습니다.

1. **`NoClassDefFoundError: org/apache/hadoop/conf/Configuration`** — 런타임에 Hadoop 이 없습니다. 그래서 Hadoop 을 uber jar 에 넣었는데도 같은 오류가 났습니다. 원인은 Flink 가 `org.apache.hadoop` 패키지를 **부모 클래스로더 우선**으로 로딩한다는 점이었습니다. jar 안에 있어도 부모에서 먼저 찾다가 없으면 실패합니다.
2. Hadoop 을 다른 이름(`com.danbi.shaded.org.apache.hadoop`)으로 relocation 하자 **`NoSuchMethodError`** 로 바뀌었습니다. Flink 런타임의 `HadoopUtils` 는 원래 이름의 Hadoop 타입을 받는데, 우리 코드는 바뀐 이름의 타입을 넘겼기 때문입니다.
3. `flink-hadoop-fs` 를 의존성에 넣어 `HadoopUtils` 까지 jar 에 포함시키고 **함께 relocation** 하자 카탈로그가 만들어졌습니다.

중간에 오류가 바뀐 것을 *진전* 으로 착각해 시간을 썼습니다. 이후에는 로그에서 **가장 안쪽 `Caused by`** 를 먼저 뽑고, 원인을 한 문장으로 쓸 수 있을 때만 고쳤습니다.

> 앱 코드를 고쳤는데 같은 오류가 반복된 적도 있습니다. 확인해 보니 `applicationVersionId` 가 그대로 1 이었습니다. 새 zip 이 S3 에 올라갔지만 앱이 업데이트되지 않았던 것입니다. 오류를 다시 분석하기 전에 *새 코드가 실제로 돌고 있는지* 부터 확인해야 합니다.
{: .prompt-tip }

## 로컬에서 재현할 수 있으면 로컬에서

`Column 'ok' not found` 는 클라우드에서 앱을 다시 올리는 데 몇 분씩 걸렸습니다. PyFlink 1.20 을 로컬에 설치하고 Kafka·Iceberg 대신 datagen·blackhole 커넥터로 같은 SQL 을 실행해 몇 초 만에 재현했습니다. 같은 방법으로 수정 후 INSERT 6개의 스키마가 모두 맞는지 확인한 뒤에 배포했습니다.

## 오류 메시지가 원인을 말해 주지 않을 때

| 보인 메시지 | 실제 원인 |
| --- | --- |
| `TABLE_OR_VIEW_NOT_FOUND glue.ops.pipeline_watermarks` | 테이블은 있음. Lake Formation 권한이 없어 보이지 않았음 |
| `athena FAILED: SELECT …` | 헬퍼가 사유를 버리고 있었음 → `StateChangeReason` 을 같이 남기게 고침 → `GetDataAccess` 누락이 드러남 |
| 센서 `UP_FOR_RESCHEDULE` 반복 | 오류가 아님. Silver 가 아직 20분 이내로 신선하지 않아 기다리는 정상 동작 |

진단용 EMR 잡을 따로 만들어 Spark 가 보는 카탈로그 네임스페이스를 출력해 보고서야 첫 번째 문제의 원인이 권한이라는 것을 알았습니다.

## 배운 점

- **관리형 서비스의 제약은 첫 배포에서만 드러난다.** 인스턴스 종류, 문자 집합, 클래스로더, 런타임 Python 버전, 권한 모델이 모두 그랬습니다.
- **오류가 바뀐 것은 진전이 아닐 수 있다.** 원인을 한 문장으로 쓸 수 있을 때 고친다.
- **새 코드가 실제로 실행 중인지 먼저 확인한다.** 버전 ID, 이미지 태그, S3 키.
- **오류 메시지를 버리지 않는다.** 실패 사유를 로그에 남기는 한 줄이 다음 장애의 시간을 줄인다.
