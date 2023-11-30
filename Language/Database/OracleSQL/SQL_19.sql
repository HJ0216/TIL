-- 데이터 삽입
INSERT INTO NOTICE(WRITER_ID) VALUES('ABC@NAVER.COM');
INSERT INTO NOTICE(WRITER_ID) VALUES('가나다라');
INSERT INTO NOTICE(WRITER_ID) VALUES('123@DAUM.NET');
INSERT INTO NOTICE(WRITER_ID) VALUES('AKSK@11YAHOO.KR');

-- [0-9a-zA-Z]: 모든 숫자 문자 포함
-- \w와 동일하나 \w는 [0-9a-zA-Z]에 _도 추가적으로 포함

-- 길이의 제한은 없지만 1개이상 필수: +
-- \w+@: \w가 1개 이상 오고 그 다음 @

-- [net kr com]: n e t 1글자씩 or 처리 됨
-- 단어 형태의 or 표현: net|kr|com
-- 구분을 위해 () 사용: (net|kr|com)

SELECT * FROM NOTICE WHERE REGEXP_LIKE(WRITER_ID, '\w+@\w+.(NET|KR|COM)');
-- \w+@\w+.(net|kr|com)
-- 도메인은 숫자로 시작할 수 없지만 조회되는 문제 발생

SELECT * FROM NOTICE WHERE REGEXP_LIKE(WRITER_ID, '\w+@\D\w*.(NET|KR|COM)');
-- \D\w*: 숫자가 아닌 것이 1개 오고 \w이 0개 이상
-- \w+@\D\w*.(net|kr|com)
