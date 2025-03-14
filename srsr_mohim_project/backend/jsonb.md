# PostgreSQL JSONB 도입 배경 및 MySQL JSON vs PostgreSQL JSONB 성능 비교

## 1️⃣ PostgreSQL 도입 배경  

프로젝트는 **교회별로 다양한 데이터를 저장할 수 있도록 확장성이 높은 데이터 모델**이 필요했습니다. 
이에 데이터베이스에 EAV 모델을 도입하여 json 데이터를 ChurchMember 테이블에 저장하도록 설계하였습니다.
이때 기존 MySQL은 Json 데이터의 조회 성능에 문제가 있다는 사실을 알게 되었습니다.

### 📌 MySQL JSON에서 발생한 문제점  
✅ **조회 성능 저하**  
- JSON 데이터를 조건으로 검색할 때 **쿼리 실행 시간이 길어짐 (1M 개 데이터 기준 평균 1000ms)**  
- MySQL의 `JSON_EXTRACT()`는 **단순 문자열 검색 기반이므로 인덱싱 최적화가 어려움**  

✅ **인덱스 활용 불가**  
- MySQL JSON 필드는 **기본적으로 인덱싱을 지원하지 않음**  
- 특정 필드 검색을 위해 **FULL TABLE SCAN**이 발생하여 성능 저하  

### 📌 PostgreSQL JSONB를 고려하게 된 이유  
PostgreSQL의 **JSONB(Binary JSON)**는 JSON을 바이너리 형태로 저장하며, **인덱싱을 지원**하여 빠른 검색이 가능합니다.  
이를 통해 **JSON 데이터를 활용하면서도 관계형 데이터베이스의 성능을 유지할 수 있습니다.**  

🔹 **PostgreSQL JSONB의 장점**
- ✅ **빠른 검색**: JSON 데이터 내부 요소에도 **인덱스를 생성 가능 (GIN, B-TREE)**
- ✅ **MySQL 대비 최대 2.5배 이상 빠른 조회 속도**

---

## 2️⃣ 실험 환경 및 성능 테스트  

### 📌 **실험 조건 및 데이터 규모 선정 이유**
- **DBMS 비교**: MySQL 8.0 vs PostgreSQL 15  
- **데이터 개수**: **1M 개 (1,000,000 rows)**
- **테스트 쿼리**: 특정 JSON 필드(`membershipLevel`, `joinDate`)를 조건으로 검색하는 속도 비교  

✅ **100만 명 데이터를 사용한 이유**  
2024년 기준 대한민국의 **총 교회 성도 수는 약 200만 명**으로 집계되었습니다.  
실 서비스 환경을 고려하여 서비스가 전국적으로 확장되었을 때 **최대 100만 명의 성도를 수용할 수 있다고 가정**하고, 실험을 진행했습니다.  

### 📌 **실제 데이터 샘플**

```json
{
  "membershipLevel": "gold",
  "joinDate": "2023-01-01",
  "preferredService": "online"
}
```

### 3️⃣ MySQL vs PostgreSQL JSON 조회 성능 비교 실험 결과

### 🔍 기본 성능 비교 (쿼리 조건 개수 2개 기준)

1M rows 데이터를 사용하고 쿼리 조건 개수를 2개(`membershipLevel`, `joinDate`)로 고정하여 실행 속도를 측정했습니다.

| 조회 방식 | MySQL JSON (ms) | PostgreSQL JSONB (ms) |
|-----------|----------------|---------------------|
| 기본 조회 | 1000ms | 400ms |
| 인덱스 적용 후 조회 | 동일(인덱스 적용 불가) | 200ms |

✅ **결과 요약:**
- MySQL은 JSON_EXTRACT()로 조건 검색을 수행할 때 FULL TABLE SCAN이 발생하여 속도가 느림 (약 1000ms)
- PostgreSQL은 JSONB 데이터 타입을 사용하여 MySQL 대비 2.5배 더 빠른 검색이 가능 (약 400ms)
- 특히, GIN or B-tree 인덱스를 적용하면 **MySQL 대비 5배 더 빠른 약 200ms로 검색 가능**


#### 🔍 쿼리 조건 개수별 성능 비교  

각 데이터베이스에서 동일한 데이터(1M rows)를 사용하여 `membershipLevel`, `joinDate`, `preferredService` 등의 필터링 조건을 하나씩 추가하며 실행 속도를 측정했습니다.  

| 조건 개수 | MySQL JSON (ms) | PostgreSQL JSONB (ms) | 차이 |
|----------|----------------|------------------|------|
| **1개 조건** | 40ms  | 40ms  | 차이 없음 |
| **2개 조건** | 1000ms (1.0s) | 200ms  | PostgreSQL이 **5배 더 빠름** |
| **3개 조건** | 1500ms (1.5s) | 40ms   | PostgreSQL이 **37배 더 빠름** |

✅ **결과 요약**
- 쿼리 조건이 1개일 때는 MySQL과 PostgreSQL의 성능 차이가 크지 않음 (40ms로 동일)
- 쿼리 조건이 2개로 증가하면 **MySQL 성능이 급격히 저하 (1000ms, PostgreSQL 대비 5배 느림)**
- 쿼리 조건이 3개 이상일 때 **PostgreSQL이 압도적으로 빠름 (MySQL: 1.5초, PostgreSQL: 40ms → 37배 차이)**

## 4️⃣ 최종 결론: GIN 인덱스를 선택한 이유  

서비스에서는 **각 교회마다 관리하는 속성이 다를 수 있어, 데이터 구조가 동적으로 변경될 가능성이 높습니다.** 따라서 팀에서는 확장성을 고려하여 PostgreSQL의 JSONB를 활용하여 별도의 스키마 변경 없이 각 교회가 맞춤형 데이터를 저장할 수 있도록 하였습니다. 그러나, **JSONB 데이터를 효율적으로 검색하려면 적절한 인덱스 전략이 필요합니다.**  

### 📌 **B-TREE vs GIN 인덱스 비교 후 GIN 인덱스 선택**  
| 인덱스 방식 | 장점 | 단점 | 적용 가능 시나리오 |
|------------|------|------|----------------|
| **B-TREE 인덱스** | 특정 키 값 검색 속도가 빠름 | JSONB 전체에 적용하기 어려움 | 속성이 고정된 경우 |
| **GIN 인덱스** | JSONB 내부의 모든 키-값 검색 최적화 | 인덱스 크기가 큼 | 속성이 유동적으로 변할 경우 |

**우리 서비스의 경우, 각 교회가 서로 다른 속성을 관리할 수 있으므로, 특정 필드에만 인덱스를 거는 B-TREE 방식은 적합하지 않았습니다.**  
대신, **JSONB 전체를 인덱싱하여 속성 변경에도 유연하게 대응할 수 있는 GIN 인덱스를 도입했습니다.**  
