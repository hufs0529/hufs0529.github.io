---
layout: post
title:  "Kubernetes StatefulSets"
subtitle:   "쿠버네티스 StatefulSets"
categories: review
tags: Kubernetes
---

## StatefulSets
- Deployment를 관리해주며 Pods의 개수를 스케일링하고 관리해주며 파드의 고유성에 대해 보장해준다.
- Deployment와 비슷하게 Pods를 이상적인 컨테이너 spec에 맞게 관리해준다.
- Deployment와 다르게 StatefulSet은 각 Pods에 유지되는 특성을 가지고 있따.
- 이 Pods들은 같은 spec으로 생성된 이후, 교환불가하다: 각각은 재스케쥴링 되어도 고유한 특성이 유지된다.
- storage 볼륨을 사용하고 싶다면 효과적인 방법이 될 수 있다.

***
<br/>

## Using StatefulSets
- 안정적 고유한 네트워크 인식
- 안정적, 지속적인 저장소
- 질서 있고 점진적인 배포 및 확장
- 순서대로 자동 롤링 업데이트

<br/>


## Limitations
- 각 Pod는 storage class에 의해 요청된 제공된 PersistentVolumeProvisioner가 필요하다.
- StatefulSet을 삭제/축소해도 연결된 볼륨은 삭제되지 않는다.
- StatefulSet은 삭제될 때 Pod 종료를 보장하지 않는다. 정상적으로 종료하려면 Pod 삭제 전 StatefulSet을 0으로 축소할 수 있다.


## Components
```
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  ports:
  - port: 80
    name: web
  clusterIP: None
  selector:
    app: nginx
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  selector:
    matchLabels:
      app: nginx # has to match .spec.template.metadata.labels
  serviceName: "nginx"
  replicas: 3 # by default is 1
  minReadySeconds: 10 # by default is 0
  template:
    metadata:
      labels:
        app: nginx # has to match .spec.selector.matchLabels
    spec:
      terminationGracePeriodSeconds: 10
      containers:
      - name: nginx
        image: registry.k8s.io/nginx-slim:0.8
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "my-storage-class"
      resources:
        requests:
          storage: 1Gi
```
- web이름을 가진 StatefulSet은 3개의 복제본을 갖는다.
- volumeClaimTemplates는 PVC역할로 안정적인 Persistent Volume을 제공해준다.


### Pod Selector
- spec.selector를 반드시 명시해서 spec.template.metadata.labels와 맵칭되게 해야한다.

### Volume Claim Templates
- 안정적인 저장소를 제공할 수 있는 spec.volumeClaimTemplates를 설정한다.

### Minimum ready seconds
- .spec.minReadySeconds는 새로운 파드가 생성될 때, 컨테이너 충돌 없이 실행되고 준비되어 사용 가능한 것으로 간주되는 최소시간을 지정하는 '선택적' 필드


## Pod Identity
- StatefulSet Pod에는 순서형, 안정적인 네트워크 ID, 안정적인 스토리지로 구성된 고유한 ID가 있다.

### Stable Storage
- 각 VolumeClaimTemplate는 StatefulSet에 의해 정의되며, 각 포드는 PersistentVolumeClaim에 최초에 의해 받게 된다.
- StorageClass가 명시되어 있지 않으면, default가 사용된다.


## PersistentVolumeClaim Retention
- spec.persistentVolumeClaimRetentionPolicy 옵션 필드는 어떻게 PVC가 제거, 관리되는지 컨트롤한다.
    - whenDeleted
    - whenScaled

```
apiVersion: apps/v1
kind: StatefulSet
...
spec:
  persistentVolumeClaimRetentionPolicy:
    whenDeleted: Retain
    whenScaled: Delete
``````