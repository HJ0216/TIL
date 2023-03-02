-- 회원 중에서 ‘박’씨인 사람을 조회
SELECT * FROM MEMBER WHERE NAME = '박%';
-- '=' 사용 시, DATA 값이 박%를 탐색
SELECT * FROM MEMBER WHERE NAME LIKE '박%';
-- 패턴 비교 시, =이 아닌 LIKE 사용

-- 회원 중에서 ‘박’씨이고 외자인 회원을 조회
SELECT * FROM MEMBER WHERE NAME LIKE '박_';
-- 박씨성의 2글자 이름 조회
SELECT * FROM MEMBER WHERE NAME LIKE '박__';
-- 박씨성의 3글자 이름 조회

-- 회원 중에서 ‘박’씨 성을 제외한 회원을 조회
SELECT * FROM MEMBER WHERE NAME NOT LIKE '박%';

-- 회원 중에서 이름에 ‘도’자가 들어간 회원을 조회
SELECT * FROM MEMBER WHERE NAME LIKE '%도%';
