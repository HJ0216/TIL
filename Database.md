### PK
PK에 접두사를 추가하면 좋은 점
* PK 값만 보아도 데이터의 유형이나 생성 위치를 알 수 있음
PK에 생성 시간을 활용하면 좋은 점
* PK가 생성된 시간 정보를 포함하므로 레코드가 언제 생성되었는지 추정할 수 있음



### 드라이빙 테이블
조인(JOIN) 시에 가장 먼저 액세스되는 테이블  
이 테이블을 기준으로 다음 테이블(드리븐 테이블, Driven Table)의 데이터를 찾음

비용 기반 옵티마이저는 테이블의 통계 정보, 인덱스 유무, WHERE절의 조건 등을 종합적으로 고려하여 조인, 필터링 등의 작업에 드는 비용이 가장 낮을 것으로 예상되는 실행 계획을 수립  
FROM절에 먼저 작성되었더라도 데이터량이 많거나 인덱스가 없어 필터링에 불리한 테이블 대신, 더 효율적으로 처리할 수 있는 다른 테이블을 드라이빙 테이블로 선택할 수 있음  
FROM절의 첫 번째 테이블이 드라이빙 테이블이 될 확률이 높지만, 반드시 그런 것은 아니며 옵티마이저가 최종적으로 결정함

**필터링이 먼저 일어날 수 있는 테이블을 FROM절에 먼저 쓰는 것이 유리한 이유**  
조인 작업은 기본적으로 드라이빙 테이블에서 읽은 각 행에 대해 드리븐 테이블에서 일치하는 데이터를 찾는 방식으로 이루어짐
드라이빙 테이블의 행 수가 적을수록 드리븐 테이블을 탐색하는 횟수도 줄어듦
예를 들어, 5000만 건의 데이터를 가진 A 테이블과 1000건의 데이터를 가진 B 테이블을 조인할 경우,  
* A 테이블이 드라이빙 테이블이 되는 경우: A 테이블에서 5000만 건의 데이터를 한 건씩 읽으면서, 각 건마다 B 테이블에서 조인 조건을 만족하는 데이터를 찾아야 하므로 B 테이블을 5000만 번 탐색해야 할 수도 있음
* B 테이블이 드라이빙 테이블이 되는 경우: 먼저 B 테이블의 1000건을 읽고, 각 건에 대해 A 테이블에서 일치하는 데이터를 찾으므로 A 테이블 탐색은 최대 1000번만 일어남  
이처럼 WHERE절을 통해 많은 데이터를 걸러낼 수 있는, 즉 결과 행의 수가 적은 테이블을 드라이빙 테이블로 삼으면 조인 작업의 반복 횟수가 획기적으로 줄어들어 전체 쿼리 처리 속도가 빨라질 수 있음


**JOIN을 할 경우, PK값을 가지고 있는 테이블이 FROM절에 위치하는 것이 유리**
* 인덱스 없는 테이블에서 시작하면 전체 스캔 발생
  * PK는 클러스터드 인덱스로 물리적 정렬
  * 클러스터드에서 시작하는 것이 I/O 효율적
* 인덱스 있는 테이블에서 시작하면 효율적 탐색 가능

### Join Algorithm
1. Hash Match(Hash Join)
* 동작 방식
  * 작은 테이블(Build Input)을 메모리에 해시 테이블로 구성
  * 큰 테이블(Probe Input)을 스캔하면서 해시 테이블에서 매칭되는 레코드 검색

* 특징
  * 시간복잡도: O(M + N) - M, N은 각 테이블의 행 수
  * 메모리에 해시 테이블을 구성할 수 있을 때 매우 효율적
  * 등가 조건(=)에서 주로 사용

* 적합한 상황
  * 한 테이블이 상대적으로 작아 메모리에 올릴 수 있을 때
  * 인덱스가 없는 경우

2. Nested Loops
* 동작 방식
  * 외부 테이블(Outer)의 각 행에 대해 내부 테이블(Inner)을 처음부터 끝까지 스캔하며 매칭 검색

* 특징
  * 시간복잡도: O(M × N) - 최악의 경우
  * 내부 테이블에 인덱스가 있으면 O(M × log N)으로 개선
    * 인덱스는 이진 검색과 유사하게 작동하므로, 전체 스캔(N번) 대신 트리 탐색(log N번)으로 매칭 레코드를 찾을 수 있음
  * 작은 데이터셋에서 효율적
  * 첫 번째 결과를 빠르게 반환 (파이프라인 처리)
    * Nested Loops는 스트리밍 방식으로 결과를 하나씩 생성하므로, 전체 작업이 끝나기 전에도 중간 결과를 볼 수 있음
```sql
SELECT * FROM A JOIN B ON A.id = B.id

-- Nested Loops
-- 시간: 0초 → A의 첫 번째 행 처리 시작
-- 시간: 0.1초 → 첫 번째 매칭 결과 발견 → 즉시 사용자에게 반환!
-- 시간: 0.2초 → 두 번째 매칭 결과 발견 → 반환
-- ...계속 진행

-- Hash Join
-- 시간: 0초 → 작은 테이블로 해시 테이블 구성 시작
-- 시간: 2초 → 해시 테이블 구성 완료
-- 시간: 4초 → 큰 테이블 스캔 및 매칭 완료
-- 시간: 4초 → 모든 결과를 한꺼번에 반환!
```

적합한 상황
  * 외부 테이블이 매우 작을 때
  * 내부 테이블에 조인 키에 대한 인덱스가 있을 때
  * OLTP 환경의 소규모 조인
    * Online Transaction Processing, 실시간 트랜잭션 처리 환경
    * OLTP 환경의 특징
      * 실시간성과 빠른 응답
        * 사용자가 버튼을 클릭하면 즉시(보통 1초 이내) 결과를 받아야 함
        * "로그인", "결제", "주문" 같은 일상적인 업무 처리
    * 소량 데이터 처리
      * 한 번에 처리하는 데이터가 적음 (보통 몇 건~수백 건)
      * 특정 사용자나 특정 주문에 대한 정보만 조회
    * 동시성
      * 수백~수천 명의 사용자가 동시에 접속
      * 각자 다른 작업을 빠르게 처리해야 함

3. Merge Join
* 동작 방식
  * 두 테이블 모두 조인 키로 정렬
  * 정렬된 순서대로 포인터를 이동하며 매칭되는 레코드 검색

* 특징
  * 시간복잡도: O(M log M + N log N) - 정렬 비용 포함
  * 이미 정렬되어 있다면 O(M + N)
  * 대용량 데이터에서 안정적인 성능
  * 등가 조건과 범위 조건 모두 지원

* 적합한 상황
  * 두 테이블이 이미 조인 키로 정렬되어 있을 때
  * 대용량 테이블 간 조인
  * 충분한 메모리가 없어 Hash Join을 사용할 수 없을 때

* 옵티마이저의 선택 기준
1. 테이블 크기: 작은 테이블은 Nested Loops, 큰 테이블은 Hash Match나 Merge Join
2. 인덱스 존재 여부: 인덱스가 있으면 Nested Loops 선호
3. 메모리 가용량: 충분한 메모리가 있으면 Hash Match 선호
4. 정렬 상태: 이미 정렬되어 있으면 Merge Join 선호
5. 조인 조건: 등가 조건이면 Hash Match, 범위 조건이면 Merge Join

각 알고리즘은 서로 다른 상황에서 최적의 성능을 보이므로, 데이터 특성과 시스템 환경을 고려한 선택이 중요


**예시**
```sql
-- departments: 10개 부서 (작은 테이블)
-- employees: 100만 명 직원 (큰 테이블)

SELECT d.department_name, e.employee_name, e.salary
FROM departments d
JOIN employees e ON d.dept_id = e.dept_id;
```
1. departments(10건)를 메모리에 해시 테이블 구성  
   Hash Table: {1 → '개발팀', 2 → '영업팀', ...}
2. employees(100만건)을 순차 스캔  
   각 직원의 dept_id로 해시 테이블에서 O(1) 검색

총 시간: O(10 + 1,000,000) = 매우 빠름

* Hash Match가 최적
  * 부서 테이블이 작아서 메모리에 쉽게 올릴 수 있음
  * 직원 테이블이 커도 한 번만 스캔하면 됨
  * 인덱스 없어도 효율적

```sql
-- vip_customers: 50명의 플래티넘 고객 (매우 작은 테이블)
-- orders: 1000만 건 주문 (큰 테이블, customer_id에 인덱스 있음)

SELECT c.customer_name, o.order_date, o.amount
FROM vip_customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.vip_level = 'PLATINUM';
```
1. VIP 고객 50명을 하나씩 처리  
2. 각 고객에 대해:
   - orders 테이블의 customer_id 인덱스로 검색 (O(log N))
   - 해당 고객의 주문들만 빠르게 찾음

고객1 → 인덱스 검색 → 주문 5건 발견 → 즉시 반환  
고객2 → 인덱스 검색 → 주문 3건 발견 → 즉시 반환
...

* Nested Loops가 최적
  * 외부 테이블(VIP 고객)이 매우 작음 (50건)
  * 내부 테이블에 인덱스가 있어 빠른 검색 가능
  * 첫 번째 결과를 즉시 사용자에게 보여줄 수 있음 (파이프라인)

```sql
-- web_logs: 5억 건 (이미 timestamp로 정렬됨)
-- mobile_logs: 3억 건 (이미 timestamp로 정렬됨)
-- 두 테이블 모두 session_id로 클러스터링되어 있음

SELECT w.timestamp, w.page_url, m.user_agent
FROM web_logs w
JOIN mobile_logs m ON w.session_id = m.session_id;
```
1. 두 테이블 모두 이미 정렬되어 있음 (정렬 비용 0)
2. 포인터를 이용해 순차적으로 매칭:

web_logs:    [session001, session002, session005, session007, ...]  
mobile_logs: [session001, session003, session005, session006, ...]

포인터1(web) → session001  
포인터2(mobile) → session001  
→ 매칭! 결과 생성

포인터1 → session002  
포인터2 → session003  
→ 002 < 003이므로 포인터1만 이동

포인터1 → session005  
포인터2 → session003  
→ 005 > 003이므로 포인터2만 이동

* Merge Join이 최적
  * 두 테이블 모두 대용량이라 Hash Join으로는 메모리 부족
  * 이미 정렬되어 있어 추가 정렬 비용 없음
  * 안정적인 O(M + N) 성능 보장
  * 메모리 사용량이 적음



### Clustered Index
데이터가 디스크에 물리적으로 저장되는 순서

클러스터링된 테이블:

특정 키(예: session_id) 순서대로 디스크에 물리적으로 저장  
같은 키값을 가진 레코드들이 디스크에서 인접한 위치에 저장됨

*일반 테이블*  
디스크 블록 1: [session_id: 999, 123, 456]  
디스크 블록 2: [session_id: 789, 123, 234]  
디스크 블록 3: [session_id: 123, 567, 890]

*클러스터링된 테이블 (session_id로 클러스터링)*  
디스크 블록 1: [session_id: 123, 123, 123]  
디스크 블록 2: [session_id: 234, 234, 456]  
디스크 블록 3: [session_id: 567, 789, 890]

장점
* session_id가 123인 데이터를 찾을 때, 한 번의 디스크 읽기로 관련된 모든 데이터를 가져올 수 있음
  * 일반 테이블은 여러 블록을 읽어야 함
* Merge Join에서의 이점
  * 순차적으로 읽으면서 조인하므로 디스크 접근 패턴이 매우 효율적

단점
* INSERT/UPDATE/DELETE 시 물리적 재배치 비용

```sql
-- UUID나 랜덤 값을 PK로 사용
-- INSERT 비용 증가가 SELECT 성능 향상의 폭보다 클 수 있음
INSERT INTO users (id, name) VALUES (UUID(), '김철수'); -- 중간 삽입
INSERT INTO users (id, name) VALUES (UUID(), '이영희'); -- 또 다른 중간 삽입

-- Auto-increment 사용
-- INSERT가 발생하더라도 항상 정렬된 상태를 유지하기 때문에 SELECT 성능 향상이 INSERT 비용 증가보다 훨씬 큼
INSERT INTO users (name) VALUES ('김철수'); -- 항상 끝에 추가
INSERT INTO users (name) VALUES ('이영희'); -- 항상 끝에 추가
```

제약사항
* 테이블당 하나만 생성 가능 -> 일반적으로 Primary Key에 자동 생성됨

*물리적 저장 순서 (클러스터링)*
디스크 블록 구조:  
블록1: [id:105, name:'김철수']  
블록2: [id:103, name:'이영희']  
블록3: [id:108, name:'박민수']  
블록4: [id:101, name:'최영호']  

*논리적 정렬 순서 (쿼리 결과)*  
물리적 저장과 상관없이 id 순으로 정렬된 결과
```sql
SELECT * FROM users ORDER BY id;
```

결과:  
101, 최영호  
103, 이영희  
105, 김철수  
108, 박민수

**Merge Join에서 중요한 것**
```sql
SELECT * FROM table_a a
JOIN table_b b ON a.id = b.id
```
Merge Join이 작동하려면:
  * 조인하기 전에 논리적으로 정렬된 데이터만 있으면 됨
  * 물리적으로 어떻게 저장되어 있든 상관없음

시나리오 1: 둘 다 없음
1. table_a를 id로 정렬 (Sort 연산)
2. table_b를 id로 정렬 (Sort 연산)  
3. Merge Join 실행

시나리오 2: 논리적 정렬만 있음 (인덱스)
1. table_a의 id 인덱스 사용 (이미 정렬됨)
2. table_b의 id 인덱스 사용 (이미 정렬됨)
3. Merge Join 실행 (Sort 비용 없음)

시나리오 3: 물리적 클러스터링도 있음
1. 인덱스 사용으로 논리적 정렬 (Sort 비용 없음)
2. 클러스터링으로 디스크 I/O 효율적
3. Merge Join 실행 (가장 빠름)

Merge Join 알고리즘: 논리적으로 정렬된 데이터만 있으면 실행 가능  
클러스터링: 추가적인 성능 향상 (디스크 I/O 효율성)  
둘 다 있으면: 최고의 성능, 하지만 클러스터링이 없어도 Merge Join은 가능

Merge Join은 "정렬된 결과"만 있으면 되고, 물리적 저장은 성능 최적화를 위한 추가 요소



### SELECT
SQL에서 SELECT 문을 사용할 때 명시적으로 ORDER BY를 지정하지 않으면,
정확한 결과 순서가 보장되지 않음
* DBMS는 SELECT 실행 시 가장 효율적인 방식을 선택
* 출력되는 컬럼 수가 다르면 내부 처리 방식이나 인덱스 사용 여부도 달라짐
```sql
select * from users;

-- '1', '션', 'sean@example.com', '서울시 강남구', '1990-01-15', '2025-08-03 08:48:21'
-- '2', '네이트', 'nate@example.com', '경기도 성남시', '1988-05-22', '2025-08-03 08:48:21'
-- '3', '세종대왕', 'sejong@example.com', '서울시 종로구', '1397-05-15', '2025-08-03 08:48:21'

select user_id from users;

'3'
'2'
'1'
```



### JOIN의 특징
* 조인 시 행의 개수가 변하는지 여부는 테이블 간의 관계(PK-FK)와 조인 방향에 따라 결정
* 자식 테이블에서 부모 테이블로 조인(FK -> PK)하면 자식 테이블의 각 행은 부모의 단 하나의 행과 연결되므로 행 개수가 유지
* 부모 테이블에서 자식 테이블로 조인(PK -> FK)하면 부모 테이블의 한 행이 자식의 여러 행과 연결될 수 있으므로 행 개수가 증가할 수 있음
* 조인으로 인한 행 수 변화를 이해해야 `SUM` , `COUNT` 같은 집계 함수를 정확하게 사용할 수 있음

```txt
t_customers
customer_id | name    | city
1          | 김철수   | 서울
2          | 이영희   | 부산
3          | 박민수   | 대구

t_orders
order_id | customer_id | amount | order_date
101      | 1          | 50000  | 2024-01-15
102      | 1          | 30000  | 2024-01-20
103      | 2          | 80000  | 2024-01-18
104      | 1          | 25000  | 2024-01-25

t_order_details
detail_id | order_id | product_id | quantity
1         | 101      | P001      | 2
2         | 101      | P002      | 1
3         | 102      | P001      | 3
4         | 103      | P003      | 1
5         | 104      | P001      | 2
```

```sql
SELECT 
    c.name,
    SUM(o.amount) as total_amount,
    COUNT(od.detail_id) as total_items
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_details od ON o.order_id = od.order_id
GROUP BY c.customer_id, c.name;
-- 김철수의 주문 101번이 상세 항목 2개 때문에 2번 중복 계산되어 amount가 잘못 합산
```
* 1:N 조인 시 주의: 하나의 레코드가 여러 번 복제되어 집계 결과가 부정확해질 수 있음
* 각 집계를 별도로 계산한 후 조인하는 방법이 가장 정확
```sql
SELECT 
    c.name,
    COALESCE(order_totals.total_amount, 0) as total_amount,
    COALESCE(order_totals.order_count, 0) as order_count,
    COALESCE(item_totals.total_items, 0) as total_items
FROM customers c
LEFT JOIN (
    SELECT 
        customer_id,
        SUM(amount) as total_amount,
        COUNT(*) as order_count
    FROM orders
    GROUP BY customer_id
) order_totals ON c.customer_id = order_totals.customer_id
LEFT JOIN (
    SELECT 
        o.customer_id,
        COUNT(od.detail_id) as total_items
    FROM orders o
    JOIN order_details od ON o.order_id = od.order_id
    GROUP BY o.customer_id
) item_totals ON c.customer_id = item_totals.customer_id;
```



### SELF JOIN
* 테이블 별칭을 활용하여 자기 참조 관계를 풀어내는 기법
* 조직도뿐만 아니라 웹사이트의 카테고리와 서브카테고리, 게시판의 원본 글과 답변 글 같은 계층형 데이터를 다룰 때 사용
```sql
select
	e.name as employee_name,
  m.name as manager_name
from employees e
left join employees m on e.manager_id = m.employee_id;
```



### INSERT INTO ... SELECT
```sql
insert into product_options (product_name, size, color)
select
	concat('기본 티셔츠: ', s.size, '-', c.color) as product_name,
    s.size,
    c.color
from sizes s
cross join colors c;
```



### BETWEEN
```sql
select * 
from orders o
where o.order_date >= '2025-07-01' and o.order_date < '2025-08-01' ;
-- where o.order_date between '2025-07-01' and '2025-07-31';
-- between은 날짜만 입력할 경우, 시간이 00시 00분 00초 기준으로 들어가기 때문에 과소 집계되거나 과다 집계될 수 있음
```



### GROUP BY
```sql
SELECT 
    c.name,
    SUM(o.amount) as total_amount
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.name;  -- name만으로 그룹화
```
1. 동명이인 문제
2. 대부분의 데이터베이스에서는 GROUP BY에 포함되지 않은 컬럼을 SELECT에서 사용하면 오류가 발생

**Primary Key를 GROUP BY에 포함**



### ANY, ALL
* `ANY` 와 `ALL` 은 주로 `>` , `<` 와 같은 비교 연산자와 함께 사용되어, 서브쿼리가 반환한 여러 값들과 비교하는 역할을 함
* `> ANY (서브쿼리)` : 서브쿼리가 반환한 여러 결과값 중 **어느 하나보다만 크면** 참  
즉, **최소값보다 크면** 참
* `> ALL (서브쿼리)` : 서브쿼리가 반환한 여러 결과값 **모두보다 커야만** 참  
즉, **최대값보다 커야** 참
* `= ANY (서브쿼리)` : `IN` 과 완전히 동일한 의미  
목록 중 어느 하나와 같으면 참
```sql
select name, price
from product
where price > any(select price
				  from products
				  where category='전자기기');
-- min(price)가 직관적이라서 any보다 집계 함수를 주로 사용

select name, price
from product
where price > all(select price
				  from products
				  where category='전자기기');
-- max(price)가 직관적이라서 any보다 집계 함수를 주로 사용

```


### 상관 서브쿼리
* **메인쿼리와 서브쿼리가 서로 '연관' 관계를 맺고 동작**하는 서브쿼리
* 서브쿼리가 독립적으로 실행될 수 없고, 메인쿼리의 값을 참조하여 실행되는 것이 특징
* 서브쿼리가 메인쿼리에서 현재 처리 중인 행의 특정 값(예: 카테고리명)을 알아야만 계산을 수행할 수 있을 때, **상관 서브쿼리(Correlated Subquery)**를 사용

**비상관 서브쿼리 (Non-correlated)**: 서브쿼리가 **단 한 번** 실행된 후, 그 결과를 메인쿼리가 사용한다.  
**상관 서브쿼리 (Correlated)**:
1. 메인쿼리가 먼저 한 행을 읽는다.
2. 읽혀진 행의 값을 서브쿼리에 전달하여, 서브쿼리가 **실행**된다.
3. 서브쿼리 결과를 이용해 메인쿼리의 `WHERE` 조건을 판단한다.
4. 메인쿼리의 다음 행을 읽고, 2-3번 과정을 **반복**한다
* 메인 쿼리의 행의 개수가 많다면 상관 서브쿼리 사용 시, 메인 쿼리 행의 개수만큼 계속 실행되므로 성능 상 불리

```sql
select
	name as 고객명,
    (
		select count(order_id) 
        from orders o 
        where o.user_id = u.user_id
     ) as 총주문횟수
from users u
order by u.user_id;
```
* 많은 경우, 상관 서브쿼리는 `JOIN` (특히 `LEFT JOIN` 과 `GROUP BY` )으로 동일한 결과를 얻도록 재작성할 수 있으며, 데이터베이스 옵티마이저가 `JOIN` 을 더 효율적으로 처리하는 경우가 많다.


### IN, EXISTS
한 번이라도 주문된 상품 조회하기
```sql
select
	product_id,
    name,
    price
from products
where product_id in (select distinct product_id from orders);
```
* 상관 서브쿼리가 아니므로 select distinct 쿼리가 한 번 실행되고 메인 쿼리가 값 비교를 하는 방식으로 효율적
* 그러나, `IN` 방식은 `orders` 테이블이 매우 클 경우, 즉 주문량이 수백만, 수천만 건에 달하면 성능에 문제가 될 수 있음
  * `orders` 를 조회하는 서브쿼리가 반환하는 지금까지 주문한 `product_id` 목록 전체를 메모리에 저장한 뒤, 메인 쿼리의 각 행과 비교해야 하기 때문
* EXISTS` 는 서브쿼리가 **결과를 반환하는지 여부(Existence)**만 확인
  * 서브쿼리 결과 행이 1개 이상이면 `TRUE`
  * 서브쿼리 결과 행이 0개이면 `FALSE`
```sql
select
	product_id,
    name,
    price
from products p
where exists
	(
		select 1
    from orders o
    where o.product_id = p.product_id
  );

-- EXISTS` 는 결과 데이터가 무엇인지는 전혀 신경 쓰지 않고, 행이 존재하는지 여부만 보기 때문에 관례적으로 `SELECT 1` 과 같이 상수를 사용해 불필요한 데이터 조회를 피함
-- EXISTS 는 첫 번째 행만 찾으면 바로 TRUE 를 반환 -> products` 테이블의 모든 행에 대해 반복
```

* IN
  * 실행 방식: 서브쿼리를 먼저 실행해 결과 목록을 만든 후, 메인쿼리에서 사용
  * 서브쿼리 결과가 작을 때 직관적이고 빠를 수 있음
  * `orders` 테이블 전체를 스캔해야 할 수 있음  -> 서브쿼리의 대상이 되는 테이블( `orders` )이 크다면 `EXISTS` 가 유리
* EXISTS
  * 메인쿼리의 각 행에 대해 서브쿼리를 실행하여 조건 확인
  * 서브쿼리 테이블이 클 때 효율적
  * 조건을 만족하는 첫 행만 찾으면 스캔을 멈춤



### 서브쿼리 vs JOIN
* 일반적으로 데이터베이스 옵티마이저는 `JOIN` 을 더 효율적으로 처리하여 성능이 좋은 경우가 많음
* 가독성 측면에서는 서브쿼리가 논리적 단계를 명확히 보여줘 더 쉬울 때가 있음
* `JOIN` 을 우선 고려하되 쿼리가 너무 복잡해지면 가독성이 좋은 서브쿼리를 사용
  * 특히 인라인 뷰를 사용해야만 깔끔하게 풀리는 문제의 경우



### 제약 조건
* `UNIQUE` **: **중복 불가 항목 지정**
  * 이 제약 조건이 걸린 열의 값은 테이블 내에서 항상 고유해야 한다.  
  * 고객의 아이디(ID), 이메일 주소, 사업자 등록번호 등은 다른 사람과 중복되면 안 되므로 `UNIQUE` 제약 조건을 사용
  * `PRIMARY KEY` 와의 차이점: `PRIMARY KEY` 는 테이블 당 단 하나만 존재할 수 있지만, `UNIQUE` 는 여러 열에 설정할 수 있음  
  `PRIMARY KEY` 는 `UNIQUE` 와 `NOT NULL` 속성을 모두 포함



### DDL
* DEFAULT CURRENT_TIMESTAMP
  * 새로운 데이터 행(row)이 추가될 때, 해당 컬럼에 별도의 값을 지정하지 않으면 현재의 날짜와 시간이 자동으로 입력
* DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
  * 새로운 데이터 행(row)이 추가될 때는 물론이고, 같은 행의 컬럼 값이 변경되어 업데이트될 때, 이 컬럼의 값은 현재 날짜와 시간으로 자동 갱신
```sql
CREATE TABLE test (
  ...
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```
* ALTER TABLE
  * 수백만, 수천만 건의 데이터가 들어있는 거대한 테이블의 구조를 변경하는 작업은 엄청나게 많은 시간과 시스템 자원을 소모 -> 작업
중에는 테이블이 잠겨서 서비스가 일시적으로 멈출 수도 있음
  * 대부분의 라이브 변경 작업은 데이터베이스 버전에 맞는 매뉴얼을 확인한 다음에 어느정도 잠금이 발생하는지, 라이브 상황에 수행할 수 있는지 확인한 다음에 실행하는 것을 권장



### DML
* INSERT
  * 열 목록을 생략하고 `INSERT INTO products VALUES (NULL, '베이직 반팔 티셔츠', ...)` 와 같이 값만 순서대로 나열하는 방법은 추천하지 않음
  * 나중에 테이블 구조가 변경(예: `ALTER TABLE` 로 열 추가)되면 기존의 `INSERT` 코드는 모두 오류를 일으키기 때문이다. 항상 데이터를 추가할 열의 목록을 명시적으로 작성하는 것이 안전
  * 한 번에 등록
  ```sql
  INSERT INTO products (name, price, stock_quantity) VALUES ('검정 양말', 5000, 100), ('갈색 양말', 5000, 150), ('흰색 양말', 5000, 200);
  ```
  * AUTO_INCREMENT` , `DEFAULT` 가 있는 컬럼은 생략가능
  * NULL을 입력할 수 있는 컬럼도 생략 가능
* UPDATE/DELETE
  * `UPDATE` 나 `DELETE` 문을 실행하기 전에는, **반드시 동일한 `WHERE` 절을 사용한 `SELECT` 문을 먼저 실행해서 내가 변경하려는 데이터가 정확히 맞는지를 눈으로 확인**
* SELECT
  * 실무에서는 `SELECT *` 사용을 최소화하고, 꼭 필요한 열만 명시적으로 지정해서 조회
  * AS 사용 시, 명시적으로 작성하는 것이 좋음


### DELETE vs TRUNCATE
* DELETE FROM table;
  * 한 줄씩, 조건에 따라 삭제 가능
  * 속도 느림 (각 행의 삭제를 기록)
  * AUTO_INCREMENT 초기화되지 않음
  * 트랜잭션 내에서 `ROLLBACK` 가능 
* TRUNCATE TABLE table;
  * 테이블 전체를 한 번에 삭제 ( `WHERE` 사용 불가)
  * 매우 빠름 (테이블을 잘라내고 새로 만드는 개념)
  * AUTO_INCREMENT 1부터 다시 시작하도록 초기화
  * ROLLBACK` 불가능


