---
layout: post
title:  "Kubernetes ConfigMap"
subtitle:   "쿠버네티스 ConfigMap"
categories: review
tags: Kubernetes
---

## Configmap
- 컨테이너에서 필요한 환경설정 내용을 컨테이너와 분리해서 제공해 주기 위한 기능
- 컨피그맵을 컨테이너와 분리해 둠으로써 하나의 동일한 컨테이너를 가지고 개발용, 스테이지용, 서비스용으로 모두 사용하는 것이 가능해진다.

    ```
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: config-dev
      namespace: default
    data:
      DB_URL: localhost
      DB_USER: myuser
      DB_PASS: mypass
      DEBUG_INFO: debug
    ```

    ```
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: configapp
      labels:
        app: configapp
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: configapp
      template:
        metadata:
          labels:
            app: configapp
        spec:
          containers:
          - name: testapp
            image: arisu1000/simple-container-app:latest
            ports:
            - containerPort: 8080
            env:
              - name: DEBUG_LEVEL
                valueFrom: 
                  configMapKeyRef:
                     name: config-dev
                     key: DEBUG_INFO
    ---
    apiVersion: v1
    kind: Service
    metadata:
      labels:
        app: configapp
      name: configapp-svc
      namespace: default
    spec:
      ports:
      - nodePort: 30800
        port: 8080
        protocol: TCP
        targetPort: 8080
      selector:
        app: configapp
      type: NodePort
    ```