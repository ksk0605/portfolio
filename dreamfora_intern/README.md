# Dreamfora Internship

### 📌 인턴십 개요
- 회사명: 드림포라 (Dreamfora)
- 기간: 2025년 1월 ~ 2월
- 역할: 백엔드 개발 인턴

✅ 스타트업 환경에서 빠르게 변화하는 요구사항을 처리하며, 개발부터 배포까지 다양한 경험을 쌓음  
✅ 백오피스 시스템 개발 및 API 개선을 통해, 운영 효율성을 향상시키는 데 기여  
✅ ATDD 주도 개발로 백엔드 개발자로서 어떻게 사용자 경험에 기여할 수 있는지 고찰

--- 

## 주요 기여 내용

### 📌 백오피스 시스템 개발 및 운영 효율성 향상
- 문제: 기존의 백오피스 시스템은 레거시로 인해 유지보수가 어려워 개발 및 운영팀이 필요한 기능을 추가하지 못하는 상황이었음.
- 해결책: 기존의 낡은 시스템을 대체할 신규 백오피스 시스템 MVP를 개발하고 배포하여 운영 효율성에 기여함.

✅ NextJS, JAVA, Spring Boot, JPA, MariaDB 기술을 활용, 풀스택 개발  
✅ ATDD, TDD 기반 개발로 테스트 커버리지 75% 달성  
![커버리지](../assets/dreamfora_coverage.png)
✅ Rest Docs를 활용한 문서 자동화  
![REST DOCS](../assets/dreamfora_restdocs.png)
✅ 클라이언트 개발자들이 신규 업데이트 기능인 인앱 재화 관련 기능을 쉽게 테스트 할 수 있도록 포인트 관리 기능 개발 → 불필요한 소통 시간 단축  
✅ 기존에 엑셀로 전달받아 DB에서 직접 쿼리로 작성하던 비효율적인 프로모션 코드 등록 업무를 간편화 → 업무 처리 시간 단축   

---

### 📌 **피드 조회 시 발생한 데드락 문제 개선 및 성능 최적화**  
> **이 문서의 코드는 실제 회사 코드가 아니라, 유사한 문제를 해결하는 과정을 설명하기 위해 작성된 예제 코드입니다.**  
> **클래스명, 메서드명, 로직 일부가 변경되어 있으며, 핵심 해결 원리는 유지되었습니다.**  

---

## **📌 문제 상황: 피드 조회 API에서 발생하는 데드락**  
- **드림포라 서비스에서 사용자들이 가장 많이 사용하는 기능 중 하나가 피드 조회 기능이었음**  
- **그러나 피드 조회 API에서 간헐적으로 데드락이 발생하는 문제가 확인됨**  

#### **🔍 서버 로그 분석 결과 (데드락 발생)**
```json
{
  "httpStatus" : "BAD_REQUEST",
  "apiVersion" : "1.1.0",
  "timestamp" : "2025-02-03 15:06:54",
  "endpoint" : "GET /v2/feeds/detail",
  "code" : 400,
  "message" : "(conn=11180662) Deadlock found when trying to get lock; try restarting transaction",
  "data" : "java.sql.SQLTransactionRollbackException"
}
```
✅ **SQLTransactionRollbackException이 발생하며, Deadlock이 감지됨**  
✅ **특정 사용자가 피드 조회를 요청할 때, 트랜잭션 충돌로 인해 API 응답이 실패하는 경우가 발생**  

---

## **📌 원인 분석: 조회 로직과 업데이트 로직이 섞여 있어 트랜잭션이 길어짐**
📌 **CQRS 패턴을 따르는 쿼리 서비스임에도 불구하고, 조회수 업데이트 로직이 포함되어 있었음**  

#### **🔍 기존 코드 구조 (예제 코드, 실제 코드 아님)**
```java
// 📌 이 코드는 실제 회사 코드가 아닌, 유사한 문제 해결을 위한 예제 코드입니다.
@Transactional
public FeedDetailResponse getFeedDetails(Long userId, Long feedId) {
    FeedEntity feed = feedRepository.findById(feedId)
            .orElseThrow(() -> new NotFoundException("Feed not found: " + feedId));

    recordFeedView(new FeedView(userId, feedId));  // 🔴 조회수 업데이트가 포함됨

    return new FeedDetailResponse(fetchFeedData(userId, feed));
}

private void recordFeedView(FeedView feedView) {
    feedViewRepository.save(feedView);
    feedRepository.updateViewCount(feedView.getFeedId());  // 🔴 동기적으로 조회수 업데이트
}
```
✅ **조회 API임에도 불필요하게 DB 트랜잭션이 발생하고 있었음**  
✅ **다른 사용자들이 동일한 피드에 접근할 경우, 트랜잭션 충돌로 인해 데드락 발생 가능성 증가**  

---

## **📌 해결책을 고민하며 사용자 경험을 고려한 선택**  
📌 **데드락 문제를 해결하는 여러 가지 옵션을 고민하며, 최적의 사용자 경험을 제공할 수 있는 방법을 선택**  

### **🚨 해결 옵션 1: 데이터베이스 락을 활용하여 동시성 문제 해결** ❌ (채택하지 않음)  
✅ **장점:** 락을 활용하면 동시 요청이 많아도 데이터 정합성이 유지됨  
❌ **단점:** 사용자의 경험이 개선되지 않으며, **오히려 API 응답 속도가 느려질 위험**  

📌 **사용자 입장에서 피드 조회는 빠르게 이루어져야 하는 기능인데, 락을 걸면 불필요한 대기 시간이 발생할 수 있음**  

---

### **🚀 해결 옵션 2: 조회와 업데이트를 분리하고, 조회수 증가를 비동기 처리** ✅ (채택한 방법)  
📌 **트랜잭션을 짧게 유지하면서, 조회수 업데이트를 비동기로 처리하면 성능을 최적화할 수 있음**  
📌 **Spring Event를 활용하여, 피드 조회는 즉시 응답하고 조회수 업데이트는 별도 비동기 이벤트로 처리**  
📌 **조회수는 사용자가 당장 정확한 정보를 보기 원하는 데이터는 아니라고 판단, Eventual consistency를 활용, 결과적 일치로 충분하다는 결론**  

---

#### **✅ 개선된 코드 (예제 코드, 실제 코드 아님)**
```java
// 📌 이 코드는 실제 회사 코드가 아닌, 유사한 문제 해결을 위한 예제 코드입니다.
@Transactional(readOnly = true)
public FeedDetailResponse getFeedDetails(Long userId, Long feedId) {
    FeedEntity feed = feedRepository.findById(feedId)
            .orElseThrow(() -> new NotFoundException("Feed not found: " + feedId));

    // ✅ 조회 요청이 들어오면 즉시 응답 반환
    eventPublisher.publishEvent(new FeedViewedEvent(userId, feedId));

    return new FeedDetailResponse(fetchFeedData(userId, feed));
}
```
✅ **Spring Event를 활용하여 `FeedViewedEvent`를 발행**  
✅ **조회는 즉시 반환하고, 조회수 업데이트는 비동기로 처리**  

#### **✅ 비동기 조회수 업데이트 처리**
```java
// 📌 이 코드는 실제 회사 코드가 아닌, 유사한 문제 해결을 위한 예제 코드입니다.
@Async
@Transactional(propagation = Propagation.REQUIRES_NEW)
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT, fallbackExecution = true)
public void handleFeedViewedEvent(FeedViewedEvent event) {
    try {
        feedViewRepository.save(new FeedViewEntity(event.getUserId(), event.getFeedId()));
        feedRepository.incrementViewCount(event.getFeedId());
    } catch (Exception error) {
        // 실패시 로깅 처리
    }  
}
```
✅ **비동기(`@Async`)로 실행되므로, API 응답 시간에 영향을 주지 않음**  
✅ **조회 API는 즉시 반환하고, 조회수 업데이트는 백그라운드에서 실행**  
✅ **API 조회 안정성 증가 및 응답 속도 향상**  

---
## **결론**
- **데드락 문제를 해결하는 여러 옵션을 고민하면서, 최적의 사용자 경험을 고려한 방식 선택**  
- **Spring Event를 활용하여 조회수 업데이트를 비동기로 처리함으로써 API 응답 속도 향상**  
- **트랜잭션을 최소화하여, 동시 요청이 많을 때 발생할 수 있는 병목 현상을 완화**  

