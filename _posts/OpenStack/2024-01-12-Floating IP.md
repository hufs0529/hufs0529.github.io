---
layout: post
title:  "OpenStack"
subtitle:   "Floating IP"
categories: review
tags: Network
---

## Floating IP란?
    - 인터넷에서 인스턴스를 직접 엑세스하기 위해 필요한 기능이다. 인스턴스와 같은 리소스에 1:1로 연결하여 사용할 수 있다.
    - 인스턴스가 생성되면 지정한 서브넷으로부너 하나의 IP 주소를 할당받는데 이를 고정 IP라고 부른다.이 주소는 private 하기때문에 직접 액세스가 불가능하다.
    - 따라서 외부와 접근하려면 Floating IP를 통해 private IP와 통신해서 외부와 통신이 가능하다.

## OpenStack에서 Floating IP 사용 방법
    1. 인스턴스 생성시 internal network만 먼저 연결해야한다.
    2. external network를 동시에 설정하면 floating ip와 인스턴스가 1:1 고정 맵핑되기 때문에 자원 낭비가 발생한다
    3. external network를 나중에 설정함으로써 다수의 인스턴스가 하나의 ip를 사용할 수 있다.(동시에는 불가능)