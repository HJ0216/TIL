SELECT * FROM MEMBER WHERE ROWNUM BETWEEN 1 AND 5;

-- 이름 내림차순으로 정렬한 결과에서 상위 5명 조회
SELECT * FROM MEMBER ORDER BY NAME DESC
WHERE ROWNUM BETWEEN 1 AND 5;
-- SQL command not properly ended

-- 의도한 결과와 달리 ROWNUM 추출 후 NAME DESC 실행
SELECT * FROM MEMBER 
WHERE ROWNUM BETWEEN 1 AND 5
ORDER BY NAME DESC;

-- 서브쿼리 사용
SELECT *
FROM(SELECT * FROM MEMBER ORDER BY NAME DESC)
WHERE ROWNUM BETWEEN 1 AND 5;

-- 나이가 30 이상인 회원 목록 조회
SELECT * FROM MEMBER WHERE AGE>=30;

-- 나이가 평균 나이 이상인 회원 목록 조회
SELECT * FROM MEMBER WHERE AGE>=AVG(AGE);
-- WHERE절 그룹 함수 사용 불가

-- 서브쿼리 사용
SELECT * FROM MEMBER WHERE AGE>=(SELECT AVG(AGE) FROM MEMBER);
