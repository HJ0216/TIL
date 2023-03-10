CREATE TABLE MEMBER
(
    ID       VARCHAR2(50),
    PWD      NVARCHAR2(50),
    NAME     NVARCHAR2(50),
    GENDER   NCHAR(2), --NCHAR(2): 4byte, CHAR(2 CHAR): 6byte
    AGE      NUMBER(3),
    BIRTHDAY CHAR(10),
    PHONE    CHAR(13),
    REGDATE  DATE    
);


DROP TABLE MEMBER;


ALTER TABLE MEMBER MODIFY ID NVARCHAR2(50);
ALTER TABLE MEMBER DROP COLUMN AGE;
ALTER TABLE MEMBER ADD EMAIL VARCHAR2(200);


CREATE TABLE NOTICE
(
    ID        NUMBER,
    TITLE     NVARCHAR2(100),
    WRITER_ID NVARCHAR2(50),
    CONTENT   CLOB,
    REGDATE   TIMESTAMP,
    HIT       NUMBER,
    FILES     NVARCHAR2(1000)
);


CREATE TABLE "COMMENT" -- 예약어로 인해 TABLE NAME 사용불가 시, ""로 감싸기
(
    ID        NUMBER,
    CONTNET   NVARCHAR2(2000),
    REGDATE   TIMESTAMP,
    WRITER_ID NVARCHAR2(50),
    NOTICE_ID NUMBER
);


CREATE TABLE ROLE
(
    ID          VARCHAR2(50),
    DISCRIPTION NVARCHAR2(500)
);


CREATE TABLE MEMBER_ROLE
(
    MEMBER_ID NVARCHAR2(50),
    ROLE_ID VARCHAR2(50)
);
