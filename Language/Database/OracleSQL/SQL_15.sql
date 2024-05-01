SELECT * FROM NOTICE WHERE WRITER_ID='HJ0216';

SELECT * FROM NOTICE WHERE HIT>3;

SELECT * FROM NOTICE WHERE CONTENT IS NULL;
-- CONTENT가 비어있는 레코드 탐색
SELECT * FROM NOTICE WHERE CONTENT = 'NULL';
-- NULL이라는 문자값이 들어간 레코드 탐색

SELECT * FROM NOTICE WHERE CONTENT IS NOT NULL;
-- CONTENT가 비어있지 않은 레코드 탐색