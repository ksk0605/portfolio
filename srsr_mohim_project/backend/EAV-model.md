# EAV(Entity-Attribute-Value) 모델을 활용한 확장성 있는 데이터베이스 설계

## 1️⃣ 배경 및 문제 정의

해당 프로젝트는 전국의 다양한 교회가 사용할 수 있도록 설계되었습니다.  
하지만 기존의 데이터베이스 구조는 특정 교회의 요구사항에 맞춰져 있어, 새로운 교회가 추가될 때마다 **데이터 스키마를 수정해야 하는 문제**가 있었습니다.  

**기존 문제점**  
- 테이블이 정형화되어 있어, 새로운 필드를 추가할 때마다 스키마 변경이 필요함  
- 교회마다 필요한 정보(예: 추가적인 속성)가 다르기 때문에 **확장성이 부족함**  
- **서비스를 지속적으로 확장하기 어려운 구조**  

이에 따라, **각 교회가 원하는 속성을 자유롭게 추가할 수 있도록** EAV(Entity-Attribute-Value) 모델을 적용했습니다.  

---

## 2️⃣ EAV 모델 개념 설명

EAV(Entity-Attribute-Value) 모델은 **데이터의 속성을 동적으로 저장할 수 있도록 설계된 데이터베이스 모델**입니다.  

- **Entity (엔티티)**: 데이터의 주체 (예: 교회, 성도)  
- **Attribute (속성)**: 해당 엔티티가 가질 수 있는 속성 (예: 전화번호, 직분)  
- **Value (값)**: 속성에 해당하는 실제 값  

**EAV 모델의 장점**  
✅ **유연한 데이터 모델**: 미리 정의된 속성이 아니라, 동적으로 속성을 추가할 수 있음  
✅ **스키마 변경이 불필요**: 새로운 요구사항이 생겨도 DB 스키마를 변경하지 않아도 됨  

---

## 3️⃣ EAV 모델을 적용한 설계 과정

기존에는 **각 속성을 개별 컬럼으로 저장하는 방식**을 사용했습니다.

```sql
CREATE TABLE church_member (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    phone VARCHAR(20),
    role VARCHAR(50),
    ...
);
```

하지만 각 교회마다 추가적으로 관리해야 할 정보가 다를 경우 확장성이 떨어지는 문제가 있었습니다.
이를 해결하기 위해, EAV 모델을 적용하여 속성을 동적으로 관리하는 방식으로 변경했습니다.

📌 EAV 기반 데이터 모델

```sql
코드 복사
CREATE TABLE church_member (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    church_id INT REFERENCES church(id),
    custom_properties JSONB
    ...
);

CREATE TABLE church (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE church_member_attributes (
    id SERIAL PRIMARY KEY,
    church_id INT REFERENCES church(id),
    name VARCHAR(255),
    data_type VARCHAR(255),
    ...
);

```

### 📌 데이터 저장 예시
| church_id | name | data_type |
|-----------|---------------|-----------------|
| 1         | phone         | string |
| 1         | role          | string |
| 2         | email         | string |
| 2         | age           | integer |

✅ 결과:

- 이제 새로운 속성을 추가할 때, 기존 테이블을 변경할 필요 없이 새로운 row를 삽입하면 됨
- 교회마다 필요한 속성을 자유롭게 추가할 수 있는 구조가 됨