CREATE TABLE NOTICE(
	ID NUMBER PRIMARY KEY, -- 기본키 제약 조건
	TITLE VARCHAR2(300) NOT NULL, -- NOT NULL
	WRITER_ID VARCHAR2(50) NOT NULL UNIQUE, -- NOT NULL/UNIQUE
	CONTENT VARCHAR2(4000),
	REGDATE DATE DEFAULT SYSDATE, -- 기본값: 현재 날짜
	HIT NUMBER DEFAULT 0 -- 기본값: 0
)


CREATE TABLE NOTICE(
	ID NUMBER, -- 기본키 제약 조건
	TITLE VARCHAR2(300) NOT NULL, -- NOT NULL
	WRITER_ID VARCHAR2(50) NOT NULL UNIQUE, -- NOT NULL/UNIQUE
	CONTENT VARCHAR2(4000),
	REGDATE DATE DEFAULT SYSDATE, -- 기본값: 현재 날짜
	HIT NUMBER DEFAULT 0 -- 기본값: 0

	CONSTRAINT NOTICE_ID_PK PRIMARY KEY(ID),
	CONSTRAINT NOTICE_ID_UK UNIQUE(WRITER_ID)
)
-- CONSTRAINT NOTICE_ID_PK: 제약조건에 대한 이름 부여

-- 기존 TABLE 수정
ALTER TABLE NOTICE
ADD CONSTRAINT NOTICE_ID_PK PRIMARY KEY(ID);
ALTER TABLE NOTICE
ADD CONSTRAINT NOTICE_WRITER_UK UNIQUE(WRITER_ID);
-- 또는 테이블 편집 활용
-- PK 설정: 테이블 편집
-- UK 설정: 테이블 편집 - 제약조건 - 새 고유 제약 조건
