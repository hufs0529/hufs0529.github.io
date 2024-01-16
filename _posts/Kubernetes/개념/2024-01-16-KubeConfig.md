---
layout: post
title:  "Kubernetes Config"
subtitle:   "쿠버네티스 Config"
categories: review
tags: Kubernetes
---

## kubeconfig 파일을 사용하여 클러스터 접근 구성하기
- kubeconfig 파일들을 사용하여 클러스터, 사용자, 네임스페이스 및 인증 메커니즘에 대한 정보를 관리 가능하다.
- 기본적으로 kubectl은 $HOME/.kube 디렉터리에서 config라는 이름의 파일을 찾는다. KUBECONFIG 환경 변수를 설정하거나 --kubeconfig 플래그를 지정해서 다른 kubeconfig 파일을 사용할 수 있다.

## 컨텍스트
- kubeconfig에서 컨텍스트 요소는 편리한 이름으로 접속 매개 변수를 묶는데 사용한다.
- 기본적으로 kubectl 커맨드라인 툴은 현재 컨텍스트 의 매개 변수를 사용하여 클러스터와 통신한다.
    ```
    kubectl config use-context
    ```

## KUBECONFIG 환경 변수
- KUBECONFIG 환경 변수는 kubeconfig 파일 목록을 보유한다. 리눅스 및 Mac의 경우 이는 콜론(:)으로 구분된 목록이다. 
- KUBECONFIG 환경 변수가 없으면, kubectl은 기본 kubeconfig 파일인 $HOME/.kube/config를 사용한다.


## 프록시
- 다음과 같이 kubeconfig 파일에서 proxy-url를 사용하여 kubectl이 각 클러스터마다 프록시를 거치도록 설정할 수 있다.

```
apiVersion: v1
kind: Config

clusters:
- cluster:
    proxy-url: http://proxy.example.org:3128
    server: https://k8s.example.org/k8s/clusters/c-xxyyzz
  name: development

users:
- name: developer

contexts:
- context:
  name: development
```