---
layout: post
title:  "Kubernetes Pod Scheduling"
subtitle:   "쿠버네티스 Trouble Shooting"
categories: review
tags: Kubernetes
---

## 파드가 FailedScheduling 이벤트 메시지로 보류 중일 경우
- 파드가 배치될 수 있는 노드를 스케줄러가 찾을 수 없으면, 노드를 찾을 수 있을 때까지 파드는 스케줄되지 않은 상태로 유지한다. 
- 파드가 할당될 곳을 스케줄러가 찾지 못하면 Event가 생성된다. 다음과 같이 kubectl을 사용하여 파드의 이벤트를 볼 수 있다.
    ```
    kubectl describe pod frontend | grep -A 9999999999 Events


    Events:
    Type     Reason            Age   From               Message
    ----     ------            ----  ----               -------
    Warning  FailedScheduling  23s   default-scheduler  0/42 nodes available: insufficient cpu
    ```

- kubectl describe nodes 명령으로 노드 용량과 할당된 양을 확인할 수 있다. 예를 들면, 다음과 같다.
    ```
    kubectl describe nodes e2e-test-node-pool-4lw4


    Name:            e2e-test-node-pool-4lw4
    [ ... 명확하게 하기 위해 라인들을 제거함 ...]
    Capacity:
    cpu:                               2
    memory:                            7679792Ki
    pods:                              110
    Allocatable:
    cpu:                               1800m
    memory:                            7474992Ki
    pods:                              110
    [ ... 명확하게 하기 위해 라인들을 제거함 ...]
    Non-terminated Pods:        (5 in total)
    Namespace    Name                                  CPU Requests  CPU Limits  Memory Requests  Memory Limits
    ---------    ----                                  ------------  ----------  ---------------  -------------
    kube-system  fluentd-gcp-v1.38-28bv1               100m (5%)     0 (0%)      200Mi (2%)       200Mi (2%)
    kube-system  kube-dns-3297075139-61lj3             260m (13%)    0 (0%)      100Mi (1%)       170Mi (2%)
    kube-system  kube-proxy-e2e-test-...               100m (5%)     0 (0%)      0 (0%)           0 (0%)
    kube-system  monitoring-influxdb-grafana-v4-z1m12  200m (10%)    200m (10%)  600Mi (8%)       600Mi (8%)
    kube-system  node-problem-detector-v0.1-fj7m3      20m (1%)      200m (10%)  20Mi (0%)        100Mi (1%)
    Allocated resources:
    (Total limits may be over 100 percent, i.e., overcommitted.)
    CPU Requests    CPU Limits    Memory Requests    Memory Limits
    ------------    ----------    ---------------    -------------
    680m (34%)      400m (20%)    920Mi (11%)        1070Mi (13%)
    ```
    - 

## Pod가 종료되었을 때
- 리소스가 부족하여 컨테이너가 종료될 수 있다. 
- 리소스 제한에 도달하여 컨테이너가 종료되고 있는지 확인하려면, 관심있는 파드에 대해 kubectl describe pod 를 호출한다.

    ```
    kubectl describe pod simmemleak-hra99

    Name:                           simmemleak-hra99
    Namespace:                      default
    Image(s):                       saadali/simmemleak
    Node:                           kubernetes-node-tf0f/10.240.216.66
    Labels:                         name=simmemleak
    Status:                         Running
    Reason:
    Message:
    IP:                             10.244.2.75
    Containers:
    simmemleak:
        Image:  saadali/simmemleak:latest
        Limits:
        cpu:          100m
        memory:       50Mi
        State:          Running
        Started:      Tue, 07 Jul 2019 12:54:41 -0700
        Last State:     Terminated
        Reason:       OOMKilled
        Exit Code:    137
        Started:      Fri, 07 Jul 2019 12:54:30 -0700
        Finished:     Fri, 07 Jul 2019 12:54:33 -0700
        Ready:          False
        Restart Count:  5
    Conditions:
    Type      Status
    Ready     False
    Events:
    Type    Reason     Age   From               Message
    ----    ------     ----  ----               -------
    Normal  Scheduled  42s   default-scheduler  Successfully assigned simmemleak-hra99 to kubernetes-node-tf0f
    Normal  Pulled     41s   kubelet            Container image "saadali/simmemleak:latest" already present on machine
    Normal  Created    41s   kubelet            Created container simmemleak
    Normal  Started    40s   kubelet            Started container simmemleak
    Normal  Killing    32s   kubelet            Killing container with id ead3fb35-5cf5-44ed-9ae1-488115be66c6: Need to kill Pod
    ```

    - Restart Count: 5 표시는 파드의 simmemleak 컨테이너가 종료되고 (지금까지) 5번 다시 시작되었음을 나타낸다.
    - Reason: OOMKilled를 통해 컨테이너가 제한보다 많은 양의 메모리를 사용하려고 했다는 것을 확인할 수 있다.