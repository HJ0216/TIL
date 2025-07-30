### PK
PK에 접두사를 추가하면 좋은 점
* PK 값만 보아도 데이터의 유형이나 생성 위치를 알 수 있음
PK에 생성 시간을 활용하면 좋은 점
* PK가 생성된 시간 정보를 포함하므로 레코드가 언제 생성되었는지 추정할 수 있음


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