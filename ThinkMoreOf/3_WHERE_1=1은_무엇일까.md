# 3_WHERE_1=1은_무엇일까
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2023-12-09
- 수정일: 2023-12-18



#
### 주제를 선정한 이유
종종 Query와 관련해서 `WHERE 1=1` 조건절을 보게 됩니다.
언제나 참인 조건으로 왜 조건절에 쓰일까에 대해 생각해 보고자 글을 작성하게 되었습니다.



#
### WHERE 1=1의 의미
1은 1과 같다는 의미로 언제나 참인 것을 의미합니다. WHERE 조건절은 주로 데이터에 조건을 추가하여 필터링하는 기능으로 사용되는데, 이러한 측면에서 WHERE 1=1은 특별한 기능을 갖지 않는다고 할 수 있습니다. <br/>



#
### WHERE 1=1의 장점
별다른 기능이 없어 보이는 언제나 참인 조건은 다음과 같은 장점이 있습니다.

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
WHERE 1=1 조건을 사용한다면, 여러 조건이 있을 때 간편한 주석 처리로 디버깅을 편하게 할 수 있습니다.

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
    query2 = " AND USER_ID = " + userId;
}
if(!title.equals("")){
    query3 = " AND TITLE LIKE %" + title + "%"
}
```
또한, WHERE 1=1 조건을 사용하여 동적 쿼리를 쉽게 작성하고 코드의 가독성도 높일 수 있습니다.



#
# WHERE 1=1의 단점
```html
SELECT EMAIL
       , PHONE
  FROM MEMBER
 WHERE 1=1
<if test="email != null">
    AND email = #{email}
</if>
<if test="phone != null">
    AND phone = #{phone}
</if>
```
위의 조건에서 email과 phone이 null일 경우, 전체 데이터가 조회됩니다. 많은 데이터를 한 번에 처리해야 하므로 응답 지연의 문제가 발생합니다. 또한, SELECT절이 아닌 UPDATE, DELETE문일 경우에는 전체 데이터에 변경이 발생하는 위험이 있습니다. <br/>
(최근에 로컬에서 SQL 쿼리를 작성하다가 실수로 UPDATE문을 WHERE 조건절 없이 실행했었습니다. 한 컬럼의 모든 데이터들이 동일한 값을 갖는 무서운 경험을 했습니다..😮)



#
# WHERE 1=1의 대안
1. \<where> 사용
```html
SELECT EMAIL
       , PHONE
FROM MEMBER
<where>
    <if test="email != null"> AND EMAIL = #{email} </if>
    <if test="phone != null"> AND PHONE = #{phone} </if>
</where>
```
\<where>를 사용하면 조건 변경을 유연하게 실행할 수 있습니다. 그러나, email과 phone이 모두 null 값으로 전달되면 `WHERE 1=1`처럼 모든 데이터가 조회되는 위험이 있습니다.
<br/>

2. \<trim> 사용
```html
SELECT EMAIL
       , PHONE
  FROM MEMBER
<trim prefix="WHERE" prefixOverrides="AND">
    <if test="email != null"> AND EMAIL = #{email} </if>
    <if test="phone != null"> AND PHONE = #{phone} </if>
</trim>
```
접두사로 WHERE를 추가하고, \<trim>문 안의 쿼리 가장 앞에 해당하는 문자가 있으면 자동으로 이를 제거(prefixOverrides)하는 trim 태그를 사용할 수도 있습니다. 그러나, 1번과 마찬가지로 인자가 모두 null로 넘어올 경우, `WHERE 1=1`을 사용한 것처럼 모든 데이터가 조회되는 위험이 있습니다.
<br/>

 - `prefixOverrides`: trim 태그 안 문자열의 처음이 일치하는 경우에만 삭제를 시도. 따라서 'AND EMAIL'은 'AND'로 시작하기 때문에 'AND'가 삭제되었지만, 'AND PHONE'은 'AND EMAIL'의 뒤에 있으면 문자열의 시작이 'AND'가 아니므로 'AND'는 삭제되지 않음

3. \<trim> 사용2
```html
SELECT EMAIL
       , PHONE
  FROM MEMBER
 WHERE
<trim prefixOverrides="AND">
    <if test="email != null"> AND EMAIL = #{email} </if>
    <if test="phone != null"> AND PHONE = #{phone} </if>
</trim>
```
WHERE는 trim 밖에서 선언하는 방식으로 EMAIL과 PHONE이 모두 null 값일 경우에는 `BadSqlGrammarException`을 발생시켜 전체 데이터가 조회되는 것을 방지할 수 있게 됩니다.

4. Java에서 검증
이 외에도 추가로 @Valid 또는 @Validated 등 파라미터 검증을 통해 Null 값인 데이터가 DB로 넘어가지 않도록 사전에 안전장치를 마련하는 방법을 활용할 수 있습니다.



#
### 정리
3_WHERE_1=1은_무엇일까.

- 항상 참인 조건으로 디버깅이나 동적 쿼리 작성 시 편리함을 제공
- 파라미터를 전달받아 사용할 경우,
    - 의도치 않은 전체 데이터 조회를 발생시킬 수 있고,
    - UPDATE, DELETE문과 사용 시, 전체 데이터를 변경시킬 수 있는 위험이 존재
- 해당 위험을 제거하려면
    - WHERE와 \<trim>을 함께 사용



#
### 📚참고 자료
[MyBatis(마이바티스)에서 사용하는 WHERE 1=1 의 위험성 및 예방(Feat. 장애)](https://dev-jwblog.tistory.com/143) <br/>
[MyBatis의 where 1=1 사용 대신 trim으로 해결해보자](https://covenant.tistory.com/253)
