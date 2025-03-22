# 스르스르 (구 모힘)

📌 **교회 멤버 관리 SaaS, 모힘 프로젝트**
- **기간**: 2023년 4월 ~ 현재 
- **사용자 수**: 900+ 명 이상 (현재 서비스 개편 중)
- **기술 스택**: Java, Spring Boot, PostgreSQL, MySQL, AWS
- **스르스르 서비스 홈페이지**: [www.srsr.kr](https://www.srsr.kr)  

---

## 🔥 프로젝트 소개

스르스르(구 모힘)은 교회 멤버 관리 및 주소록 기능을 제공하는 SaaS 플랫폼입니다. 기존의 낡은 교적 관리 시스템을 대체하며, 전국의 교회가 사용할 수 있도록 확장 가능하게 설계되었습니다.

### 🌟 주요 기능 및 적용 기술
- **교회 멤버 등록 및 관리** (CRUD 기능)
- **EAV(Entity-Attribute-Value) 모델 적용** (확장성 있는 데이터베이스 구조)
- **PostgreSQL JSONB 기반 데이터 저장**
- **AWS 배포 및 Github Actions 배포 자동화**

---

## 📂 프로젝트 구조
```
└── com
    └── mohim
        └── api
            ├── MohimApplication.java
            ├── sharedkernel
            └── domain
                ├── application
                ├── domain
                ├── infra
                └── presentation
```

---

### 📌 **각 디렉토리 및 모듈의 역할**
#### 📂 **presentation layer**  
- **역할**: 유저 인터페이스 (Controller, API)  
- **설명**: API 요청을 받아 유저가 원하는 기능을 실행하고, 데이터를 반환  

#### 📂 **application layer**  
- **역할**: 유저 요청을 처리하는 서비스 계층  
- **설명**: 도메인 계층을 조합하여 비즈니스 로직을 실행  

#### 📂 **domain layer**  
- **역할**: 핵심 도메인 규칙 및 비즈니스 로직 구현  
- **설명**: 데이터와 핵심 비즈니스 로직을 담당  

#### 📂 **infra layer**  
- **역할**: 외부 시스템과의 연동 (DB, API, 메시지 큐)  
- **설명**: 구현 기술과 관련된 모듈 (예: PostgreSQL, AWS 연동)  

#### 📂 **shared kernel**  
- **역할**: 여러 바운디드 컨텍스트에서 공유하는 핵심 로직과 인터페이스  
- **설명**: 도메인 간 공통으로 사용되는 객체 및 로직 포함  

---

## 🛠 기술적 도전과 해결 과정

### 📌 [**1. EAV 모델을 활용한 확장성 있는 데이터베이스 설계**](https://github.com/ksk0605/portfolio/blob/main/srsr_mohim_project/backend/EAV-model.md)
- 기존 교회별 정형화된 테이블 구조를 **유연하게 확장 가능한 구조로 변경**
- 다양한 교회에서 **각자의 속성을 정의할 수 있도록 EAV 모델 도입**
- 이를 통해 **데이터 저장 구조를 변경하지 않고도 새로운 기능을 추가할 수 있도록 개선**

### 📌 [**2. PostgreSQL JSONB 적용 및 성능 최적화**](https://github.com/ksk0605/portfolio/blob/main/srsr_mohim_project/backend/jsonb.md)
- 기존 MySQL JSON 필드를 사용하던 방식에서 **PostgreSQL JSONB를 활용하여 조회 성능 향상**
- JSON 필드 내 속성에 대한 **GIN 인덱싱 및 빠른 검색 가능**

---

## 🎯 협업 방식 및 팀워크 [(링크 보기)](https://github.com/ksk0605/portfolio/tree/main/srsr_mohim_project/soft-skills)
- **👥 개발 인원**: 2명 (풀스택 개발)
- **📌 Git 협업 전략**
  - 이슈별 브랜치 전략 사용 (`SRSR-{issue number}`)
  - PR 템플릿 적용 및 코드 리뷰 문화 정착
- **🛠 협업 도구**: Notion (지라 스타일 태스크 관리)

---
