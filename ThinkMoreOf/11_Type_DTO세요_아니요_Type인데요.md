# 11_Type_DTO세요_아니요_Type인데요
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2024-01-27
- 수정일: 

<br/>



#
### 주제를 선정한 이유
최근에 처음으로 DB에서 사용자 정의 타입을 만들어보았습니다. Object를 만들었는데, 마침 생성 방법과 사용 방법도 정리해 두면 좋을 것 같아 주제로 선정했습니다.

<br/>



#
### 사용자 정의 타입
가장 먼저 사용자 정의 타입이 필요한 이유는 `재사용성`입니다. 마치 Java에서는 자주 사용하는 데이터를 하나의 DTO에 묶어둔 것처럼 DB에서도 자주 사용되는 타입을 사용자 정의 타입으로 만들 수 있습니다.  
저 또한 Procedure에서 자주 사용되는 데이터 집합을 하나의 Type으로 만들어 간편하게 불러오기 위해 사용했습니다.  

이러한 Object 타입의 정의는 사용자가 정의한 복합 테이터 타입으로, 데이터 타입과 함수, 프로시저 등을 묶어 사용자가 정의한 새로운 데이터 타입입니다.


<br/>



#
### Object의 활용
저는 우선 하나의 프로시저가 있고, 그 안에 사용되는 여러 데이터가 있는 상태였습니다. 그 중 일부는 동적으로 넘어오는 데이터이고, 해당 데이터를 이용해서 프로시저를 동작시키는 구조였습니다.  

그래서 간단하게 구현하기 위해 다음과 같은 구조를 만들었습니다.
1. 페이지 -> Function: PK
2. Function -> Type: Value 주입
3. Procedure : Type에 Function을 이용해 값 주입

순서는 Object 생성 -> Function 생성 -> Procedure 생성입니다.

1. Object 생성

```sql
create or replace TYPE OBJECT_SAMPLE AS OBJECT (
  object_id               VARCHAR2(50)
, object_name             VARCHAR2(50)
, create_date             DATE
);
```

2. Object에 값을 주입하는 Function 생성

```sql
create or replace function get_obj_sample (p_object_id IN VARCHAR2)
return OBJECT_SAMPLE 
IS
	v_obj_sample OBJECT_SAMPLE;
 
BEGIN   

	SELECT 
		OBJECT_SAMPLE(
			  object_id                 
			, object_name     
			, create_date)
	INTO
		v_obj_sample              		
	FROM 
		OBJ_SAMPLE_T
	WHERE   
		object_id = p_object_id
	;

	RETURN 
		v_obj_sample
	;

EXCEPTION 
   WHEN NO_DATA_FOUND THEN
        NULL;
    WHEN OTHERS THEN
        RAISE;

END;
```

3. 사용하는 Procedure 생성

```sql
create or replace procedure OBJECT_SAMPLE (p_object_id in VARCHAR2)
as

    v_obj_sample OBJECT_SAMPLE := get_obj_sample(p_object_id);
	
	v_count NUMBER;

BEGIN

	SELECT COUNT(*)
	INTO   v_count
	FROM   SAMPLE_REF_T
	WHERE  object_id = v_obj_sample.object_id;

EXCEPTION 
    WHEN OTHERS THEN
        RAISE;
   
END "OBJECT_SAMPLE";
```

<br/>



#
### 정리
Oracle DB 기준 필요한 데이터 집합을 Object 타입으로 만들 수 있다.
    - 가독성과
    - 재사용성에 좋다.

<br/>



#
### 📚참고 자료
[사용자 정의 데이터 타입](https://thebook.io/006696/0299/)  
[Microsoft PowerPoint - Tech-iSeminar_DataType.ppt](https://dataonair.or.kr/upload//20050727/1122430689633.pdf)  
