# 1_어떤 값을 PK로 설정할 것인가
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2023-12-01
- 수정일: 2023-12-02



#
### 주제를 선정한 이유

교육 과제로 하나의 시스템을 만드는 프로젝트를 시작했습니다.

프로젝트를 진행하면서 느낌으로만 판단하던 부분을 명확히 하고자 글을 작성했습니다.

먼저, 주제 선정 과정은 다음과 같습니다.


프로젝트에서 본격적인 개발을 앞두고 다음과 같은 설계 과정을 거쳤습니다.

- `요구사항 분석`
- `Flow chart`
- `Mockup`
- `테이블 설계서 및 ERD`


`요구사항 분석`은 `과제의 주제`에 초점을 맞춰 작성하였고, <br/>
`Flow Chart`는 해당 시스템을 사용하는 사용자가 어떤 방식으로 업무하고 있는지를 정리하였습니다. <br/>
그다음으로 `Mockup`은 개략적인 화면 설계 및 배치도를 작성하였습니다. <br/>
마지막으로 `테이블 설계서 및 ERD`를 작성하며 `PK를 설정`하는 기준을 명확히 하지 못했다고 생각하여 글을 작성하게 되었습니다.


가장 먼저, PK란 Primary Key(기본 키)의 줄인 말로 테이블에서 레코드 하나하나를 유일하게 식별하는 값을 가진 컬럼을 의미합니다. 그러므로 컬럼 값이 중복되어서도 Null 값이어서도 안 됩니다(= Unique와 Not Null 조건).

예를 들어, <전화번호부> 테이블이 다음과 같을 때

|순번|이름|전화번호|주소|
|---|---|---|---|
|1|김 이름|010-1234-5678|서울시 동작구|
|2|이 전화|010-5678-1234|서울시 서초구|
|3|박 주소|010-1245-2356|서울시 종로구|

전화번호는 1인당 1개, 중복된 번호를 가질 수 없으므로 전화번호만 있다면 이름과 주소를 유일한 행으로 구분할 수 있습니다. 이런 의미에서 전화번호는 <전화번호부> 테이블의 PK, 즉 기본 키입니다.

그러나 테이블을 설계할 때 기본 키는 전화번호보다는 시퀀스 값(1, 2, 3, ...), 또는 코드(TELBOOK001, TELBOOK002, ...) 등으로 설정을 해주었습니다.

왜 시퀀스나 코드를 이용했을까, 생각해 보면 사용했던 DBMS에서 자동으로 값을 증가시켜 주는 기능이 있었기에 `편리`했습니다.
- Oracle에서는 Sequence 기능을 활용하였고,
- MySQL에서는 Auto Increment 기능을 사용했습니다.
또한, 유일한 식별자 역할을 하는 컬럼 값의 경우 데이터 길이가 긴 편에 속하기 때문에 `가독성`이 떨어진다고 생각했습니다.

그러나 한 편으로는 레코드를 식별할 수 컬럼(<전화번호부> 테이블에서는 전화번호)이 있는데, 굳이 새로운 컬럼(<전화번호부> 테이블에서는 순번)을 추가해야할까라는 생각도 했습니다.



#
### 기본키 설정 시 유의 사항
특정 컬럼이 기본키가 되기 위해서는 다음과 같은 조건을 만족해야 합니다.

- `유일성`: 테이블에서 동일한 값을 갖는 레코드가 없어야 함
- `안정성`: 컬럼의 속성 값이 변경되지 않아야 함
- `환원 불가능성`: 복합키 사용 시, 복합키의 일부 키만으로 테이블 내의 모든 레코드를 식별할 수 없어야 함
- `단순성`: 최소로 PK를 설정하고 간단한 값을 갖는 컬럼을 선택해야 함

`유일성`은 PK의 정의와도 맞닿아 있는 개념입니다.

`안정성`은 왜 PK를 전화번호가 아닌 순번으로 PK를 설정하면 좋은가에 대한 답이 될 수 있다고 생각합니다. 전화번호는 일반적으로 1인당 1개의 값을 갖는 특별한 값이지만 손쉽게 변경할 수 있습니다. 기본키로 설정할 경우, 그 값이 쉽게 바뀔 수 있기 때문에 기본키로는 설정하지 않는 것이 권장되는 이유입니다. 뿐만 아니라, 주민등록번호 등도 변경될 가능성은 언제나 존재합니다. <br/>
이럴 때 사용할 수 있는 것이 대체 키(Surrogate Key)입니다. 자연 키(Natural Key)를 대신해서 사용하기 위해 인공적으로 만든 키입니다. 전화번호나 주민등록번호 등은 자연키라고도 하는데, 이는 해당 키 값이 실제 세계에서도 의미를 갖는 값임을 의미합니다.

대체 키를 사용하게 되면 다음과 같은 여러 이점이 있습니다.
- 변경될 가능성이 낮음
    - PK는 여러 인덱스에서도 사용될 가능성이 높으므로, 변경될 경우 여러 파급 효과가 발생할 수 있음
- 주민등록번호와 같은 민감 정보를 대신해서 사용하므로 보안상 이점이 있음
- 단일의 짧은 대체키를 사용해서 성능을 향상 시킬 수 있음
    - PK는 다른 테이블의 FK가 되는 경우가 많고, 여러 인덱스에서도 사용될 가능성이 높음
- 키의 생성과 관리를 완전히 DBMS에 위임하여 데이터 무결성을 보장할 수 있음

따라서 PK는 대체 키를 사용해서 단일 키로 짧게 설정하는 것이 좋습니다.

`환원 불가능성`은 제 2 정규화와 관련된 내용으로 주제를 조금 벗어나는 것 같아 여기서는 추가적으로 언급하지 않겠습니다. <br/>
[데이터베이스 정규화](https://itwiki.kr/w/%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4_%EC%A0%95%EA%B7%9C%ED%99%94#google_vignette)

마지막으로 `단순성`은 대체 키의 장점 중 성능 향상으로 언급했던 부분 관련이 있습니다. 여러 테이블에서 참조되는 값이고, 인덱스로도 활용될 가능성이 높으므로 최대한 단일키로 단순한 값을 설정하는 것이 좋습니다.



#
### 정리
어떤 값을 PK로 설정할 것인가.

- 대체 키를 사용해서
    - 각 레코드를 유일하게 식별하도록 하고,
    - 변경되지 않도록 하며,
    - 단일 키로 짧은 값을 설정하여 성능을 높일 수 있도록 하자.

\* 단, 반드시 대체 키를 사용해야 한다기보다는 자연키가 적합한 경우도 있을 수 있다.



#
### 📚참고 자료
[3.6.9 Using AUTO_INCREMENT](https://dev.mysql.com/doc/refman/8.0/en/example-auto-increment.html) <br/>
[CREATE SEQUENCE](https://docs.oracle.com/en/database/oracle/oracle-database/19/sqlrf/CREATE-SEQUENCE.html#GUID-E9C78A8C-615A-4757-B2A8-5E6EFB130571) <br/>
[What's the best practice for primary keys in tables?](https://stackoverflow.com/questions/337503/whats-the-best-practice-for-primary-keys-in-tables) <br/>
[How to Choose a Good Primary Key](https://vertabelo.com/blog/primary-key/) <br/>
[Surrogate Key](http://databaser.net/moniwiki/wiki.php/SurrogateKey) <br/>
[[Database] 자연키(Natural key)와 대체키(Surrogate Key), PK(기본키)를 대체키로 설정해야 하는 이유](https://mangkyu.tistory.com/287)
