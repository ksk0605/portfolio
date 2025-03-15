## ✅ **우아한테크코스 팀 프로젝트 - Mouda**

📌 **Mouda - 소외감을 줄이고 모임을 쉽게 만들 수 있는 커뮤니티 서비스**  
Mouda는 **집단 및 모임 내 소외감을 해소하고**, 사람들이 쉽게 모임을 생성하고 참여할 수 있도록 돕는 커뮤니티 플랫폼입니다.  
사용자들은 다양한 **크고 작은 모임을 개설하고, 선착순 참여 및 랜덤 추첨을 통해 이벤트에 참여**할 수 있습니다.

### 📌 **프로젝트 개요**
- **개발 기간**: 2024.04 ~ 2024.06  
- **팀 구성**: **8명 (백엔드 5명, 프론트엔드 3명)**
- **기술 스택**: Java, Spring Boot, JPA, MySQL, AWS  
- **GitHub 저장소**: [🔗 2024-mouda](https://github.com/woowacourse-teams/2024-mouda)

---

## 🔥 **내 역할 및 기여**

### 1️⃣ **JWT 기반 인증/인가 시스템 구현**
- Spring Security 없이 **JWT + Interceptor + Argument Resolver**로 인증 처리  

### 2️⃣ **선착순 참여형 모임 및 랜덤 추첨 기능 개발**
- **특정 시간 내에만 참가 가능한 모임** 생성 기능 구현  
- 설정된 시간이 되면 **서버에서 자동으로 당첨자를 추첨하는 기능 개발**  
- **Spring Scheduler**를 활용하여 예약된 시간에 당첨자를 결정하도록 구현  

### 3️⃣ **백엔드 아키텍처 리팩토링**
- 기존 **Controller - Service - Repository** 구조에서  
  **도메인 규칙을 추상화한 Implement Layer**를 추가하여 **Controller - Service - Implement - Repository 구조로 변경**  
- **이점**: 도메인 로직이 명확해지고, **테스트 커버리지를 향상**  

### 4️⃣ **테스트 자동 초기화 환경 구축**
- **문제**: 테스트 간 데이터가 공유되어 **서로 다른 테스트에 영향을 주며 생산성이 저하**됨  
- **해결**: JUnit Extension을 활용하여 **자동으로 테스트 데이터를 초기화하는 환경을 구축**  
- **결과**: 테스트 안정성이 증가하고 **TDD 기반 개발이 더욱 원활해짐**  

---

## 🛠 **기술적 도전과 해결 과정**

### 📌 **[1. 백엔드 아키텍처 개선 & 리팩토링](https://github.com/ksk0605/portfolio/blob/main/mouda_project/backend/backend_architecture_refactoring.md)**
- 도메인 계층을 **Service / Implement / Repository**로 분리하여 **유지보수성 향상**  
- Service는 유스케이스 중심, Implement는 도메인 규칙 중심으로 설계하여 **코드 중복을 줄이고 코드 가독성 향상**  

### 📌 [2. **테스트 자동 초기화 환경 구축**](https://github.com/ksk0605/portfolio/blob/main/mouda_project/backend/test_environment_optimization.md)
- **문제 상황**: 테스트 간 데이터 격리가 되지 않아 테스트 실패 빈번
- **해결 방안**: JUnit Extension으로 테스트 클래스마다 DB 초기화 자동화
- **구현 방법**: `@BeforeEach`와 `@AfterEach`에서 테이블 truncate 처리
- **개선 효과**: 테스트 안정성 향상 및 개발 생산성 증가

---

## 🎯 **협업 및 학습 경험**
- **TDD 기반 개발**로 **대부분의 기능을 테스트 코드와 함께 작성**  
- **팀원들과 협업하여 코드 리뷰 & PR 기반 개발 진행**  
- **백엔드 5명과 함께 서비스 구조 및 도메인 모델을 설계하며 깊은 학습 경험**  

---

## 🔗 **관련 자료**
- **GitHub 저장소**: [🔗 2024-mouda](https://github.com/woowacourse-teams/2024-mouda)  

---
