# 📌 Mouda 프로젝트 - 백엔드 아키텍처 개선 및 리팩토링  

초기 개발 당시, 백엔드는 전형적인 **Controller - Service - Repository 구조**를 사용했습니다.  
하지만 **서비스 로직이 점점 복잡해지면서 몇 가지 문제점이 발생**했습니다.  

### 🚨 **기존 아키텍처 문제점**  
1. **Service 계층이 비대해짐**  
   - `Service`에서 **여러 개의 로직이 한 메서드에서 혼재되어 가독성이 떨어짐**  
   - 모임 검증, 저장, 상태 변경, 알림 전송 등 **다양한 책임이 한 곳에 집중**  

2. **비즈니스 로직이 흐름을 따라 읽기 어려움**  
   - 비즈니스 흐름상 중요한 로직들이 쉽게 드러나지 않음  
   - **기능을 수정할 때 전체 로직을 분석해야 하는 문제 발생**  

3. **테스트 코드 작성이 어렵다**  
    - `Service`가 지나치게 커지면서, **단위 테스트가 복잡해짐**
    - 단위 테스트가 아닌 **통합 테스트 위주로 작성할 수밖에 없는 구조**  

---

## 2️⃣ 기존 코드 (Before)
```java
@Transactional
public CreateChamyoMoimResponse chamyoMoim(Long darakbangId, Long moimId, DarakbangMember darakbangMember) {
    Moim moim = moimRepository.findByIdForUpdate(moimId)
        .orElseThrow(() -> new ChamyoException(HttpStatus.NOT_FOUND, ChamyoErrorMessage.MOIM_NOT_FOUND));

    if (moim.isNotInDarakbang(darakbangId)) {
        throw new ChamyoException(HttpStatus.BAD_REQUEST, ChamyoErrorMessage.MOIM_NOT_FOUND);
    }

    validateCanChamyoMoim(moim, darakbangMember);

    Chamyo chamyo = Chamyo.builder()
        .moim(moim)
        .darakbangMember(darakbangMember)
        .moimRole(MoimRole.MOIMEE)
        .build();

    try {
        chamyo = chamyoRepository.save(chamyo);
    } catch (DataIntegrityViolationException exception) {
        throw new ChamyoException(HttpStatus.BAD_REQUEST, ChamyoErrorMessage.MOIM_ALREADY_JOINED);
    }

    int currentPeople = chamyoRepository.countByMoim(moim);
    if (currentPeople >= moim.getMaxPeople()) {
        moimRepository.updateMoimStatusById(moim.getId(), MoimStatus.COMPLETED);
    }

    notificationService.notifyToMembers(NotificationType.NEW_MOIMEE_JOINED, darakbangId, moim, darakbangMember);

    return CreateChamyoMoimResponse.from(chamyo);
}
```

---

## 3️⃣ **리팩토링 후 개선된 코드 (After)**
```java
@Transactional
public void chamyoMoim(Long darakbangId, Long moimId, DarakbangMember darakbangMember) {
    Moim moim = moimFinder.read(moimId, darakbangId);
    Chamyo chamyo = chamyoWriter.saveAsMoimee(moim, darakbangMember);
    moimWriter.updateMoimStatusIfFull(moim);

    notificationSender.sendChamyoNotification(chamyo, NotificationType.NEW_MOIMEE_JOINED);
}
```

---

## 4️⃣ **개선된 점 및 리팩토링 효과**
### ✅ **1. 서비스 계층을 역할별로 분리**
- `moimFinder.read(moimId, darakbangId)`  
  → **모임을 조회하고, 해당 다락방에 속해 있는지 검증**  
- `chamyoWriter.saveAsMoimee(moim, darakbangMember)`  
  → **참여자를 저장하며, 데이터 무결성을 보장**  
- `moimWriter.updateMoimStatusIfFull(moim)`  
  → **모임이 가득 찼을 경우 상태를 변경**  
- `notificationSender.sendChamyoNotification(chamyo, NotificationType.NEW_MOIMEE_JOINED)`  
  → **모임에 새로운 참여자가 추가되었음을 알림**  

✅ **각 기능별로 역할을 분리하여, Service 계층이 비대해지는 문제 해결**  

---

### ✅ **2. 비즈니스 로직이 더 직관적으로 표현됨**  
📌 **Before** (로직이 뒤섞여 있음)  
- 모임 조회 → 검증 → 저장 → 인원수 체크 → 상태 변경 → 알림 전송 (흐름이 복잡)  

📌 **After** (단순한 흐름으로 정리됨)  
```java
Moim moim = moimFinder.read(moimId, darakbangId);
Chamyo chamyo = chamyoWriter.saveAsMoimee(moim, darakbangMember);
moimWriter.updateMoimStatusIfFull(moim);
notificationSender.sendChamyoNotification(chamyo, NotificationType.NEW_MOIMEE_JOINED);
```
✅ **메서드명만 읽어도 전체적인 비즈니스 흐름이 명확하게 보임**  

---

### ✅ **3. 테스트 코드 작성 용이성 증가**
📌 **Before**
- `chamyoRepository`와 `moimRepository`를 직접 호출 → **Mocking이 많아지고 테스트가 어려움**  
- **하나의 기능을 테스트하기 위해 많은 의존성을 고려해야 함**  

📌 **After**
- `moimFinder`, `chamyoWriter`, `moimWriter`, `notificationSender` 등의 **단위 테스트가 가능해짐**  
- **기능별로 독립적인 테스트 코드 작성 가능 → 유지보수성 향상**  

✅ **테스트 코드 커버리지 증가: 예시 서비스 클래스 관련 테스트 4개 → 16개**  

---

## 5️⃣ **리팩토링 후 성과**
| 항목 | 리팩토링 전 | 리팩토링 후 |
|------|------------|------------|
| 코드 가독성 | 비즈니스 로직 혼재 | 비즈니스 흐름이 명확 |
| 역할 분리 | Service 계층이 비대함 | 각 계층별 역할이 분리됨 |
| 테스트 가능성 | 여러 의존성으로 인한 단위 테스트 작성 어려움 | 단위 테스트 작성이 쉬워짐 |
| 유지보수성 | 수정 시 영향도가 큼 | 변경이 용이 |

---

## 6️⃣ **결론 및 배운 점**
* 기존 **Service가 담당하던 역할을 Finder, Writer, Sender로 분리하여 가독성과 유지보수성을 향상**  
* **도메인 규칙을 명확하게 분리하고, 테스트 가능성을 높이는 설계 패턴을 적용**  
* **비즈니스 흐름을 메서드 명만으로도 직관적으로 이해할 수 있도록 개선**  
* **이 리팩토링을 통해, 앞으로의 서비스 확장성을 고려한 구조를 설계할 수 있는 경험을 쌓을 수 있었음.** 
