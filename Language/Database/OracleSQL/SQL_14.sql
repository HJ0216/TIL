SELECT HIT+1 HIT FROM NOTICE;
-- COL_NAME HIT+1 -> HIT

SELECT 1 + '3' FROM DUAL; -- 4
-- SELECT는 반드시 FROM과 함께 사용해야하므로 TABLE이 없을 경우, 산술값 출력 불가
-- ORACLE에서 제공하는 DUMMY TABLE(DUAL) 사용하여 산술 연산 출력
-- +: 숫자 연산

SELECT 1 || '3' FROM DUAL; -- 13
-- ||: 문자 연산

SELECT NAME || '(' || ID || ')' NEW_NAME FROM MEMBER; -- 손오공(dragon)
