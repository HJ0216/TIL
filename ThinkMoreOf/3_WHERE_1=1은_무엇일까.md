# 3_WHERE_1=1은_무엇일까
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2023-12-09
- 수정일: 2023-12-17



#
### 주제를 선정한 이유
종종 Query와 관련해서 `WHERE 1=1` 조건절을 보게 됩니다.
언제나 참인 조건으로 왜 조건절에 쓰일까에 대해 생각해보고자 글을 작성하게 되었습니다.



#
### WHERE 1=1의 의미
1은 1과 같다는 의미로 언제나 참인 것을 의미합니다. WHERE 조건절은 주로 데이터에 조건을 추가하여 필터링하는 기능으로 사용되는데, 이러한 측면에서 WHERE 1=1은 특별한 기능을 갖지 않는다고 할 수 있습니다. <br/>



#
### WHERE 1=1의 장점
별 다른 기능이 없어보이는 언제나 참인 조건은 다음과 같은 장점이 있습니다.
1. 코드 디버깅의 간편함
```sql
SELECT NAME
FROM USER_T
WHERE MARKETING_YN_FLAG = 'Y'
AND PHONE_NUMBER IS NOT NULL
;

SELECT NAME
FROM USER_T
-- WHERE MARKETING_YN_FLAG = 'Y'
WHERE PHONE_NUMBER IS NOT NULL
;

```

```sql
SELECT NAME
FROM USER_T
WHERE 1=1
AND MARKETING_YN_FLAG = 'Y'
AND PHONE_NUMBER IS NOT NULL
;

SELECT NAME
FROM USER_T
WHERE 1=1
-- AND MARKETING_YN_FLAG = 'Y'
AND PHONE_NUMBER IS NOT NULL
;
```
WHERE 1=1 조건을 사용한다면 여러 조건이 있을 때, 간편하게 주석을 처리해서 디버깅을 편리하게 할 수 있습니다.

2. 동적 쿼리에서의 유용성
```java
query1 = "SELECT * FROM BOARD";

if(!userId.equals("")){
    query2 = " WHERE USER_ID = " + userId;
}
if(!title.equals("")){
    if(!userId.equals("")){
        query3 = " AND";
    } else {
        query3 = " WHERE";
    }
    query4 = " WHERE TITLE LIKE %" + title + "%";
}
```
```java
query1 = "SELECT * FROM BOARD WHERE 1=1";

if(!userId.equals("")){
    query2 = " WHERE USER_ID = " + userId;
}
if(!title.equals("")){
    query3 = " WHERE TITLE LIKE %" + title + "%"
}
```
WHERE 구문을 1=1 조건을 통해 항상 사용하면서 동적 쿼리 작성을 쉽게 작성하고 코드의 가독성을 높일 수 있습니다.



#
### 📚참고 자료
[Cafe24 Developers](https://developers.cafe24.com/docs/en/api/admin/#cashreceipt) <br/>
