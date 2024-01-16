---
layout: post
title:  "Hadoop Component"
subtitle:   "하둡 구성요소"
categories: review
tags: hadoop
---

<br>

![Hadoop](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FRQAoD%2FbtqCsH4nMHv%2FzTMhBe1CMqih6cYRHoTrl1%2Fimg.png)

<br>

## NameNode
- 하둡에서는 데이터를 block단위로 관리하고 NameNode는 데이터 block이 어디 DataNode에 있는지 관리한다.
- read시 어느 데이터 노드에 작업을 할당해야하는지와 write시 여유로운 데이터 노드를 찾아 작업 할당을 한다.
- NameNode에 이상이 생긴다면 관리하고 있던 정보가 사라져 데이터가 유실될 수 있다.
    - 이를 위해 하둡에서는 별도 FS에 데이터를 동기화하며, NameNode 유실시 Secondary NameNode는 별도 FS에서 NameNode의 관리 정보를 새 NameNode에 할당
- NameNode는 메타데이터를 관리하기 위해 EditLog와 FsImage 사용
    - EditLog: HDFS의 메타데이터에 대한 모든 변화를 기록하는 로그 파일
    - FsImage: 파일 시스템의 네임스페이스(디렉토리명, 파일명, 상태 정보)와 파일에 대한 블록 매핑 정보를 저장하는 파일


## Secondary NameNode
- EditLog와 FsImage를 주기적으로 병합하는 역할
    - 하둡 2.x부터 Secondary NameNode를 두지 않고 NameNode를 HA 구성으로 아키텍쳐를 변경했다.
    - Active-Standby 구조


## DataNode
- 데이터 노드는 파일을 저장하고 제공하는 역할
- client가 데이터 읽기, 쓰기 요청을 한다면 NameNode는 요청 데이터에 맞는 데이터 노드 탐색 후 Client는 탐색된 DataNode와 통신하여 데이터를 읽고 쓴다.
- DataNode는 NameNode에게  자신의 정보 전달
    - 클러스터가 처음 시작될 때, 각 DataNode는 block 정보를 NameNode에게 전달
    - 주기적으로 NameNode에게 Heartbeat와 블록 목록 정보를 전달
    - 변경사항이 발생할 때마다 NameNode에게 변경사항 전달


## JobTracker
- 일반적으로 NameNode에서 실행시키는 하나의 프로세스
- TaskTracker(DataNode)의 리소스를 관리하여, MapReduce 작업 요청시 작업을 알맞는 TaskTracker에서 할당한다.


## ResourceManager
- Resource Manager는 두 개의 주 요소로 구성되어 있다: Scheduler, Application Manager
Scheduler는 자원을 다양한 애플리케이션에 종속된 것들에 대해 자원을 할당해주는 역할을 한다. 모니터링, 트래킹 등 기능을 제외한 순수하게 할당해주는 역할을 수행한다. 또한, 실패에 대한 재시작에 대한 책임은 없다.
- Scheduler는 다양한 큐, 애플리케이션 등 여러 형태와 플러그 가능한 형태를 지닌다.
- Application Manager는 작업 제출을 수락하고, 애플리케이션별 Application Manager를 실행하기 위한 첫 번째 컨테이너를 정하며, 실패시 Application Manager 컨테이너를 다시 시작하기 위한 서비스를 제공한다.
- ResourceManager이 수천개가 넘는 노드를 관리해 줌으로써 단일의 거대한 클러스터를 구성할 수 있게 해준다.
- ResourceManager의 핵심 아이디어는 resource management와 job scheduling/monitoring 기능을 분리하는 것이다.  Resource Manager과 Node Manager의 형태는데이터 연산 프레임워크이다. 
- Resource Manager는 모든 애플리케이션 시스템간 중재할 수 있는 궁극적인 권한을 가지고 있다. Node Manager는 각 노드마다 존재하며 자원들(cpu, memory, disk, network)들을 모니터링하고 Resource Manager/Scheduler에게 보고해주는 역할을 한다. / https://mangkyu.tistory.com/127
    1. scheduler: 
        - 용량 대기열 등의 제한조건에 따라 실행중인 다양한 applications들에 자원을 할당한다.
        - fail보장하지 않는다.
    2. applications manager: 
        - job의 제출을 수락하고, application master를 실행하기 위한 첫 번째 container 설정하고 실패시 container 재시작
        - 선정된 container를 트랙킹, 모니터링 한다.

<br/>

![yarn](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbwXQ6k%2FbtqVvODO28B%2FkK0yROyby7cOgaY4rkqlFk%2Fimg.png)

<br/>




## NodeManager
- 개별 노드들을 관리하고 주어진 노드에서 사용자의 작업 및 Work Flow를 관리한다.
- Resource Manager에 등록되며 노드의 상태를 판별하기 위해 주기적으로 hearbeat를 전송한다.
- Resource Manager을 통해 할당받은 Container를 관리한다.
    1. Application Master
        - 클러스터에서 응용의 실행을 조정하고 오류를 관리한다.
        - node manager 안에서 작동하여 task를 실행시키고 모니터링하여 resource manager와 자원을 협상한다.
        - 주기적으로 resource manager에 hearbeat를 전송하여 자원의 요구사항을 갱신한다
    2. Container
        - 하나의 노드에 할당받은 자원들로, 특정 호스트에서 특정 자원(메모리, cpu 등)을 사용한다.

<br/>

![yarn](https://i.stack.imgur.com/HyDHF.png)

<br/>

<br/>

![yarn 동작 방식](https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbgaZp1%2FbtqVuhsJBp5%2FD6HMNGVPIYnYJkJu4g1Zf1%2Fimg.png)

<br/>

* 참고사항
- Application Master는 애플리케이션별 리소스를 요청, 실행 및 모니터링하는 기본 컨테이너인 반면
- Application Manager는 ResourceManager 내부의 구성 요소이다.
    - Applications Manager는 Job의 제출을 수락하고, Application Master를 실행하기 위한 첫번째 컨테이너를 설정하고 실패 시 Application Master의 Container를 재시작하게 해준다. 
    - Application Master는 Scheduler를 통해 적합한 Container를 선정하고, 그것을 Tracking하고 진행 상황을 모니터링하는 역할을 수행한다.

