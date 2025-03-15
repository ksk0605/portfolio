# JUnit Extension을 활용한 자동 데이터베이스 초기화 방식 개선 

## 1️⃣ 기존 Database Cleaner 방식의 문제점  

### **기존 방식의 한계**
초기에는 **각 테스트 실행 전 `DatabaseCleaner`를 활용하여 데이터베이스를 초기화**하는 방식을 사용했습니다.  
그러나 이 방식에는 **다음과 같은 문제점이 있었습니다.**  

#### **1. 테이블을 일일이 삭제해야 함**  
- 기존 방식에서는 **모든 테이블을 외래 키 제약 조건(FK) 순서에 맞춰 하나씩 삭제**해야 했습니다.  
- 즉, 모든 테이블을 개별적으로 `DELETE` 실행한 후, ID 값을 다시 초기화(`ALTER TABLE ... RESTART WITH 1`) 해야 했습니다.  

```java
@Transactional
public void cleanUp() {
    entityManager.createNativeQuery("DELETE FROM CHAT").executeUpdate();
    entityManager.createNativeQuery("ALTER TABLE CHAT alter column id restart with 1").executeUpdate();

    entityManager.createNativeQuery("DELETE FROM COMMENT").executeUpdate();
    entityManager.createNativeQuery("ALTER TABLE COMMENT alter column id restart with 1").executeUpdate();
    
    entityManager.createNativeQuery("DELETE FROM ZZIM").executeUpdate();
    entityManager.createNativeQuery("ALTER TABLE ZZIM alter column id restart with 1").executeUpdate();
    
    entityManager.createNativeQuery("DELETE FROM CHAMYO").executeUpdate();
    entityManager.createNativeQuery("ALTER TABLE CHAMYO alter column id restart with 1").executeUpdate();
    
    // (생략) 모든 테이블을 개별적으로 처리해야 했음
}
```

**문제점**:  
- **제약 조건을 고려해야 하므로, 테이블 삭제 순서가 중요하고 관리가 번거로움**  
- **테이블이 추가될 때마다 새로운 `DELETE` 및 `ALTER` 쿼리를 추가해야 함**  
- **데이터베이스 클리너의 로직을 제대로 관리하지 못하면 서로 다른 테스트에 영향을 줄 수 있음**

---

#### **2. 테스트 클래스마다 Cleaner를 주입해야 함**  
기존 방식에서는 `DatabaseCleaner` 객체를 **각 테스트 클래스마다 수동으로 주입**해야 했습니다.  
즉, 모든 테스트 클래스에서 `@BeforeEach`를 사용하여 매번 `cleanUp()`을 실행해야 했습니다.  

```java
@SpringBootTest
public class ChamyoServiceTest {

    @Autowired
    private DatabaseCleaner databaseCleaner;

    @BeforeEach
    void setUp() {
        databaseCleaner.cleanUp();
    }

    @Test
    void 모임에_참여하면_정상적으로_저장된다() {
        // 테스트 로직
    }
}
```

**문제점**:  
- **테스트 클래스가 많아질수록 `@BeforeEach`에 `cleanUp()`을 반복적으로 추가해야 하는 비효율성**  
- **테스트 실행 환경을 일관되게 유지하기 어려움**  

---

## 2️⃣ **JUnit Extension을 활용한 자동 초기화 방식 도입

위와 같은 문제를 해결하기 위해, **`JUnit Extension`을 활용한 자동 데이터베이스 초기화 방식을 도입**했습니다.  
이 방식은 **테스트 실행 전에 모든 테이블을 한 번에 초기화**하며, **각 테스트 클래스에서 별도로 설정할 필요 없이 자동으로 실행**됩니다.  

---

### **✅ 개선된 방식**
#### **1. 모든 테이블을 자동으로 삭제하도록 개선**
기존 방식처럼 **테이블을 일일이 지정하여 삭제하는 방식 대신, 데이터베이스의 모든 테이블을 자동으로 찾아 초기화하는 방식**을 적용했습니다.  

📌 **개선된 초기화 로직**  
```java
private static void deleteAll(JdbcTemplate jdbcTemplate, EntityManager entityManager) {
    entityManager.createNativeQuery("SET REFERENTIAL_INTEGRITY FALSE").executeUpdate();
    
    for (String tableName : findDatabaseTableNames(jdbcTemplate)) {
        entityManager.createNativeQuery("DELETE FROM %s".formatted(tableName)).executeUpdate();
        entityManager.createNativeQuery("ALTER TABLE %s alter column id restart with 1".formatted(tableName))
            .executeUpdate();
    }
    
    entityManager.createNativeQuery("SET REFERENTIAL_INTEGRITY TRUE").executeUpdate();
}
```

**개선된 방식의 장점**  
- **모든 테이블을 동적으로 찾아서 초기화하므로, 새로운 테이블이 추가되어도 별도의 코드 수정이 필요 없음**  
- **`SET REFERENTIAL_INTEGRITY FALSE`를 사용하여 FK 제약 조건을 임시로 해제한 후 삭제 → 테이블 삭제 순서를 신경 쓸 필요 없음**  
---

#### **2. JUnit Extension을 활용하여 자동 적용**
이전에는 **각 테스트 클래스에서 `DatabaseCleaner`를 직접 주입받아 호출해야 하는 문제**가 있었습니다.  
이를 해결하기 위해 **JUnit의 `BeforeEachCallback`을 활용하여 자동 실행되도록 개선**했습니다.  

📌 **JUnit Extension 구현 (자동 데이터베이스 초기화)**  
```java
public class NoTransactionExtension implements BeforeEachCallback {

    private static final DatabaseCleaner databaseCleaner = new DatabaseCleaner();

    @Override
    public void beforeEach(ExtensionContext context) {
        databaseCleaner.cleanUp();
    }
}
```

📌 **JUnit Extension 적용 방식**  
```java
@ExtendWith(NoTransactionExtension.class)
@SpringBootTest
public class ChamyoServiceTest {

    @Test
    void 모임에_참여하면_정상적으로_저장된다() {
        // 테스트 로직 (자동으로 DB 초기화가 수행됨)
    }
}
```

- **각 테스트 실행 전 자동으로 데이터베이스 초기화가 실행됨**  
- **테스트 클래스에서 별도로 `DatabaseCleaner`를 주입할 필요 없음**  

---

#### **3. Auto Detection을 적용하여 설정 없이 자동 실행**
JUnit 5의 `ServiceLoader`를 활용하여, **테스트 코드에서 `@ExtendWith(NoTransactionExtension.class)`를 추가하지 않아도 자동으로 실행되도록 설정**했습니다.  

📌 **`META-INF/services/org.junit.jupiter.api.extension.Extension` 파일 생성**
```plaintext
com.mouda.test.NoTransactionExtension
```
📌 **`junit-platform.properties` 파일 생성**
```plaintext
junit.jupiter.extensions.autodetection.enabled=true
```

📌 **Auto Detection 적용 후 테스트 코드**
```java
@SpringBootTest
public class ChamyoServiceTest {

    @Test
    void 모임에_참여하면_정상적으로_저장된다() {
        // 테스트 로직 (자동으로 DB 초기화가 수행됨)
    }
}
```

- **테스트 코드에서 별도의 설정 없이 DB 초기화 기능이 자동 적용됨**  
- **새로운 테스트가 추가될 때도 환경 설정을 신경 쓸 필요 없음**  

---

## 3️⃣ **테스트 환경 개선 효과**

📌 **기존 vs 개선 후 비교**
| 항목 | 기존 방식 | 개선 후 |
|------|----------|----------|
| 테이블 삭제 방식 | 개별 `DELETE FROM` 실행 | 모든 테이블 자동 삭제 |
| FK 제약 조건 처리 | 삭제 순서 고려해야 함 | `SET REFERENTIAL_INTEGRITY FALSE`로 해결 |
| 설정 방식 | `DatabaseCleaner` 직접 주입 필요 | **JUnit Extension으로 자동 실행** |
| 테스트 실행 속도 | 상대적으로 느림 | **빠름 (-20~30%)** |
| 테스트 유지보수성 | 테이블 추가 시 코드 수정 필요 | **자동 감지 (코드 수정 불필요)** |

- **테스트 실행 속도 20~30% 향상(@DirtiesContext 대비)**  
- **설정 없이 모든 테스트에서 자동 실행**  
- **테스트 환경을 일관되게 유지하며, 유지보수 부담 감소**  

---

## 4️⃣ **결론 및 배운 점**
- **기존 Database Cleaner 방식의 한계를 개선하여, 모든 테이블을 동적으로 삭제하는 방식 도입**  
- **JUnit Extension을 활용하여 DB 초기화를 자동화하고, 테스트 실행 시 일관성을 유지**  
- **Auto Detection 적용으로 개발자가 별도의 설정 없이 자동으로 초기화 기능을 활용할 수 있도록 개선**  
- **이 개선을 통해 테스트 실행 속도를 향상시키고, 테스트 환경의 유지보수성을 크게 높였으며, 팀원들이 테스트 코드를 더 쉽게 작성할 수 있도록 기여함**
