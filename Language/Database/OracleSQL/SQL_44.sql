ALTER TABLE TEST ADD CONSTRAINT CK_TEST_PHONE CHECK(PHONE LIKE '010-%-____');
-- PHONE 제약에서 숫자아 아닌 문자도 입력할 수 있는 문제 발생
-- 정규식 표현을 통한 CHECK 제약 강화

ALTER TABLE TEST DROP CONSTRAINT CK_TEST_PHONE;

SELECT * FROM USER_CONSTRAINTS WHERE TABLE_NAME='TEST';
-- USER 소유의 TABLE VIEW 조회

ALTER TABLE TEST ADD CONSTRAINT MEMBER_PHONE_CHK1 CHECK(REGEXP_LIKE(PHONE, '^01[01]-\d{3,4}-\d{4}$'));
-- ^: 문자열의 시작, $: 문자열의 끝
-- ^$ 사용하지 않을 경우, 중간에 전화번호가 포함된 잘못된 데이터가 저장될 수 있음
-- \d: digit, 숫자를 대표하는 정규표현식
-- [01]: 0 또는 1
-- {3,4}: 3자리 또는 4자리
