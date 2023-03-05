CREATE TABLE TEST(
	ID VARCHAR2(50) NULL,
	PHONE VARCHAR2(200) CHECK(PHONE LIKE '010-%-____') NOT NULL,
	EMAIL VARCHAR2(500) NULL
);
-- CHECK 제약 조건: 형식, 길이 등 유효한 값 입력 제한

ALTER TABLE TEST DROP CONSTRAINT SYS_C009043;
-- 제약조건에 이름을 지정하지 않은 경우, TABLE - 제약조건에서 확인
ALTER TABLE TEST ADD CONSTRAINT CK_TEST_PHONE CHECK(PHONE LIKE '010-%-____');
-- 또는 테이블 편집-제약조건-새 검사 제약조건
-- 검사조건: PHONE LIKE '010-%-____'

INSERT INTO TEST(ID, EMAIL, PHONE) VALUES('AA', 'A@A.COM', '011111-2222');
-- 체크제약 조건 위배

COMMIT;
-- INSERT, UPDATE, DELETE NON-AUTO COMMIT;
