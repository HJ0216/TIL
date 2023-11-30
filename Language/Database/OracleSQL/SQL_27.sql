SELECT TO_CHAR(12345678, '$9,999,999,999.99') FROM DUAL;
-- 문자의 단위표시 형식은 숫자의 길이보다 길어야 함
-- 숫자 > 표현 형식: 출력시 #으로 나타남
-- 숫자 < 표현 형식: 지정 형식에 따라 공백 OR 0으로 표시

-- FORMAT CHAR
-- 9: 숫자
-- 0: 빈자리를 채우는 문자
-- $: 앞에 $ 표시
-- ,: 천단위 구분자 표시
--.: 소수점 구자 표시

SELECT 123 || 'HELLO' FROM DUAL;
-- 문자열과의 결합을 위해 숫자 -> 문자
SELECT TO_CHAR(123) || 'HELLO' FROM DUAL;
SELECT TO_CHAR(1234, '999,999') || 'HELLO' FROM DUAL;
SELECT TO_CHAR(1234, '099,999') || 'HELLO' FROM DUAL;
SELECT TO_CHAR(1234, '$099,999') || 'HELLO' FROM DUAL;
-- 공백을 제거하고자 하는 경우,
SELECT TRIM(TO_CHAR(1234, '999,999')) || '원' FROM DUAL;

SELECT TO_CHAR(12.4567, '9,999.99') FROM DUAL;
SELECT TO_CHAR(12.4, '9,999.00') FROM DUAL;


SELECT TO_DATE('1994-02-16') FROM DUAL;
-- YYYY/RRRR/YY/YEAR: 년도표시: 4자리/Y2K/2자리/영문
-- MM/MON/MONTH: 월표시: 2자리/영문3자리/영문전체
-- DD/DAY/DDTH: 일표시: 2자리/영문/2자리ST
-- AM/PM: 오전/오후
-- HH/HH24: 시간표시: 12시간/24시간
-- MI: 분표시: 0-59분
-- SS: 초표시: 0-59초

SELECT TO_DATE('2023-02-28 12:23:34') FROM DUAL;
SELECT TO_DATE('2023-02-18 12:23:34', 'YYYY-MM-DD HH:MI:SS') FROM DUAL;


SELECT TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') FROM DUAL;
-- YYYY/RRRR/YY/YEAR: 년도표시: 4자리/Y2K/2자리/영문
-- MM/MON/MONTH: 월표시: 2자리/영문3자리/영문전체
-- DD/DAY/DDTH: 일표시: 2자리/영문/2자리ST
-- AM/PM: 오전/오후
-- HH/HH24: 시간표시: 12시간/24시간
-- MI: 분표시: 0-59분
-- SS: 초표시: 0-59초

SELECT TO_CHAR(SYSDATE) FROM DUAL;
SELECT TO_CHAR(SYSDATE, 'YY/MM/DD HH:MI') FROM DUAL;
SELECT TO_CHAR(SYSDATE, 'YYYY/MM/DD HH24:MI:SS') FROM DUAL;


SELECT TO_NUMBER('1994') FROM DUAL;

SELECT '2' + 3 FROM DUAL;
-- + 연산자는 숫자에 사용되므로 '2' -> 2로 자동 형변환
SELECT TO_NUMBER('2') + 3 FROM DUAL;
-- 명시적으로 형변환 진행하는 것이 좋음


SELECT TO_TIMESTAMP('1994-02-02 12:23:34') FROM DUAL;
