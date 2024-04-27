# 14_NSIS_선물_대신_설치_파일
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2024-04-27
- 수정일: 

<br/>



#
### 주제를 선정한 이유
3월에 시작한 프로젝트가 4월 중순에 끝이났습니다. 프로그램 배포도 끝나고 수정은 간단한 UI나 기능 개선만 이뤄지고 있던 중.. 설치파일을 수정하는 일을 맡게 되었습니다. 그간 설치파일 생각없이 다음다음만 눌렀던 제 자신을 돌이켜보기 위해 글을 작성합니다☠️ 다음 번에는 좀 더 깔끔한 UI를 가진 설치파일을 만들 수 있길🔥!

<br/>



#
### NSIS 정의
NSIS (Nullsoft Scriptable Install System) is a professional open source system to create Windows installers.  
즉, Windows 플랫폼에서 개발자가 인스톨러를 구축할 수 있도록 도와주는 도구입니다.  


#
# NSIS와 HM NIS Edit
NSIS를 통해 Setup 파일을 간단하게 만들 수는 있지만, HM NIS Edit을 추가적으로 사용한다면 마법사르 통해 설치 파일의 기본 틀을 보다 빠르고 쉽게 만들 수 있습니다.


#
### 📚참고 자료
[NSIS Wiki](https://nsis.sourceforge.io/Main_Page)  
[NSIS 사용자 설명서](https://www.opentutorials.org/module/3650/21850)  
[[NSIS] HM NIS Edit로 쉽고 빠르게 설치 파일 만들기](https://luckygg.tistory.com/260)  