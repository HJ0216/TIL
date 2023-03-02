SELECT COUNT(TITLE) FROM NOTICE;
-- COUNT: NULL 값 제외
SELECT COUNT(*) FROM NOTICE;
-- * 사용 시, 전체 ROW에 대한 연산이므로 처리 속도가 늦어질 수 있음

SELECT SUM(HIT) FROM NOTICE;

-- 작성자 별 집계
SELECT WRITER_ID, COUNT(ID)
FROM NOTICE
GROUP WRITER_ID
ORDER BY COUNT DESC;
-- GROUP BY 그룹화 대상 COL이 아니고 COUNT 집계함수도 아닌 COL 사용 시 오류
-- ORDER BY 별칭 DESC


-- 실행 순서: FROM → CONNECT BY → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
-- SELECT에서 지은 별칭은 그 이후 실행에서만 사용 가능
