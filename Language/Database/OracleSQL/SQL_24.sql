-- LPAD, RPAD: 문자열 길이 맞추기
SELECT LPAD('HELLO', 5) FROM DUAL;
SELECT LPAD('HELLO', 5, '0') FROM DAUL;
SELECT LPAD('HELLO', 10, '1') FROM DUAL;
SELECT RPAD('WORLD', 7, '2') FROM DUA;'

-- 회원 이름 조회(단, 이름의 길이가 3자가 안되는 경우, 이름 오른쪽을 _로 채우기)
SELECT RPAD(NAME, 3, '_') FROM MEMBERS;
-- 단, 한글의 경우 *2의 길이를 지정해줘야 함
SELECT RPAD('ORACLE', 2, '0') FROM DUAL; -- OR
SELECT RPAD('오라클', 2, '0') FROM DUAL; -- 오


-- INITCAP: 문자열 첫글자를 대문자로 만들어주는 함수
SELECT INITCAP('the ...') FROM DUAL;
-- The
SELECT INITCAP('the most important thing is ...') FROM DUAL;
-- The Most Important Thing Is ...
SELECT INITCAP('the mo가장st 3important thing is ...') FROM DUAL;
-- The Mo가장St 3important Thing Is ...


-- INSTR: 찾을 문자열 첫번째 위치 반환
SELECT INSTR('ALL WE NEED TO IS JUST TO ...', 'TO') FROM DUAL;
-- 첫번째 위치만을 반환하므로 시작 위치를 따로 지정할 수 있음
SELECT INSTR('ALL WE NEED TO IS JUST TO ...', 'TO', 15) FROM DUAL;
--시작위치를 지정하기 어려울 경우, 몇번째 인자를 찾을 것인지를 지정할 수 있음
SELECT INSTR('ALL WE NEED TO IS JUST TO ...', 'TO', 1, 2) FROM DUAL;

-- 회원 전화번호에서 두번째 대시문자가 존재하는 위치 출력
SELECT INSTR(PHONE, '-', 1, 2) FROM MEMBERS;
-- 회원 전화번호에서 첫번째 대시와 두번째 대시 문자 사이 간격
SELECT INSTR(PHONE, '-', 1, 2) - INSTR(PHONE, '-') FROM MEMBER;
-- 위치값-위치값, '-' 자리값까지 포함됨 -> -1로 수치 조정
SELECT INSTR(PHONE, '-', 1, 2) - INSTR(PHONE, '-') -1 FROM MEMBER;
-- 회원 전화번호에서 첫번째와 두번째 사이 국번 출력
SELECT SUBSTR(PHONE, INSTR(PHONE, '-')+1, (INSTR(PHONE, '-', 1, 2)-INSTR(PHONE, '-')-1)) FROM MEMBERS;


-- LENGTH: 문자열 길이를 얻는 함수
SELECT LENGTH('WHERE WE ARE') FROM DUAL;
-- 모든 회원의 핸드폰 번호와 번호의 문자열 길이 조회
SELECT PHONE, LENGTH(PHONE) FROM DAUL;
-- 회원의 전화번호에서 '-'를 제거한 번호의 길이 조회
SELECT LENGTH(REPLACE(PHONE, '-', '')) FROM MEMBERS;


-- 코드값을 반환하는 함수
SELECT ASCII('A') FROM DUAL; -- 65
-- 코드값으로 문자를 반환하는 함수
SELECT CHR(65) FROM DUAL; -- A
