-- 검색 데이터 예제 준비
INSERT INTO NOTICE(TITLE) VALUES(010-1234-1234);
-- '' 사용안할 시, 숫자로 인식되어 연산되는 문제 발생
DELETE FROM NOTICE WHERE TITLE='-2458';

INSERT INTO NOTICE(TITLE) VALUES('010-1234-1234');
INSERT INTO NOTICE(TITLE) VALUES('가나다라 010-1234-1234');
INSERT INTO NOTICE(TITLE) VALUES('가-나-다 한글');
INSERT INTO NOTICE(TITLE) VALUES('010-1234-1234 가나다라');
INSERT INTO NOTICE(TITLE) VALUES('가나다라 010-1234-1234 가나다라');

select * from notice where title like '%-%-%';
-- 전화번호가 들어간 row 추출
-- 가-나-다도 함께 조회되는 문제 발생

-- 정규식을 활용한 검색 효율성 높이기
-- [016789]: 한글자씩 or로 연결
-- [0-9]: 한글자씩 연속된 범위 표현 가능 ([0-9]는 \d와 동일)
-- \d\d\d\d{3,4} \d가 3번 또는 4번 반복
-- 문자열의 시작^, 문자열의 끝 $
-- ^01[016-9]-\d{3,4}-\d{4}$

select * from notice where title like '^01[016-9]-\d{3,4}-\d{4}$';
-- 정규식을 사용하기 위해서는 정규표현식 함수를 사용해야 함

-- where REGEXP_LIKE(COL_NAME, 'REGEXP')
SELECT * FROM NOTICE WHERE REGEXP_LIKE(TITLE, '^01[016-9]-\d{3,4}-\d{4}$');
-- ^REGEXP$: REGEXP로 정확히 시작하고 끝나야 함, 중간에 들어간 경우 검색되지 않음
-- 포함된 문자열로 찾고자하면 ^, $ 삭제

SELECT * FROM NOTICE WHERE REGEXP_LIKE(TITLE, '01[016-9]-\d{3,4}-\d{4}');
