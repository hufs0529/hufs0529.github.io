---
layout: post
title:  "S3 Encryption"
subtitle:   "S3 암호화"
categories: review
tags: s3
---

## Amazon S3 - Object Encryption

다음 4가지 방법으로 S3 버킷을 암호화할 수 있습니다.

### Server-Side Encryption(SSE)

1. **SSE-S3**
    - AWS에 의해 키가 관리됩니다.
    - 서버 측에서 암호화됩니다.
    - 암호화 유형은 AES-256입니다.
    - "x-amz-server-side-encryption":"AES256" 헤더를 포함해야 합니다.
    - 버킷의 기본 설정값입니다.
    ![AES-256](AES-256.png)

2. **SSE-KMS**
    - 키는 AWS KMS (Key Management Service)에 의해 관리됩니다.
    - 사용자가 컨트롤 가능하며, CloudTrail을 사용하여 관리할 수 있습니다.
    - "x-amz-server-side-encryption":"aws:AES256" 헤더를 포함해야 합니다.
    - KMS의 제한으로 인해 문제가 발생할 수 있습니다.
        - Decrypt KMS API를 사용하여 s3에 업로드, 다운로드하는 동안 사용자가 Quota를 소진할 수 있습니다.
        - 많은 트래픽에 제한이 걸릴 수 있습니다.

3. **SSE-C**
    - HTTPS를 사용합니다.
    - AWS 밖의 사용자에 의해 완전히 관리됩니다.
    - AWS는 제공된 키를 저장하지 않습니다.
    - 요청이 있을 때마다 HTTP 헤더에 키를 포함해야 합니다.

### Client-Side Encryption

1. **Client-Side Encryption(SSL/TLS)**
    - S3와 통신할 때마다 암호화 및 복호화를 수행해야 합니다.
    - 라이브러리를 사용하여 암호화합니다.
    - HTTP, HTTPS는 각각 암호화되지 않음, 암호화됩니다.
    - HTTPS를 권장합니다.
    - HTTPS는 SSE-C에 필수적입니다.

## Default Encryption vs Bucket Policies

SSE-S3 암호화는 S3 버킷에 자동으로 적용됩니다.
    - 추가로, 버킷 정책에 "force encryption"을 사용하여 암호화를 거치지 않고 PUT하는 API 호출을 방지할 수 있습니다.


### Default Encrtyption vs Bucket Policies
- SSE-S3 encryption은 S3 버킷에 자동적으로 적용된다.
    - 추가적으로, "force encryption"을 bucket policy에 사용함으로써 어떠한 API 콜을 encryption을 거치지 않고 PUT하는 것을 방지할 수 있다.
- bucket policy에 상관없이 encryption할 수 있다.