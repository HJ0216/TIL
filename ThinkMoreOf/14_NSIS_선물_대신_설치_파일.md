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
# WPF 애플리케이션 실행 파일 만들기
HM NIS Edit과 관련해서 설치부터 실행까지 너무나 잘 정리되어있는 글들이 많기에 저는 실제 프로젝트에서 사용한 기능을 중심으로 정리할 예정입니다.

💀 난관1: 어느 파일까지 복사할 것인가
처음에 Visual Studio에서 

```bash


```




#
### 📚참고 자료
[NSIS Wiki](https://nsis.sourceforge.io/Main_Page)  
[NSIS 사용자 설명서](https://www.opentutorials.org/module/3650/21850)  
[[NSIS] HM NIS Edit로 쉽고 빠르게 설치 파일 만들기](https://luckygg.tistory.com/260)  
[NSIS 설치 및 HM NIS Edit 스크립트 마법사 사용하기](https://yeo-computerclass.tistory.com/149)  
[[NSIS] 프로그램 실행중일때는 확인 메시지후 종료하기](https://sheepone.tistory.com/187)  
[‘처음’ Windows 설치 파일을 ‘배포’하는 개발자들을 위하여](https://blog.dramancompany.com/2015/12/%EC%B2%98%EC%9D%8C-windows-%EC%84%A4%EC%B9%98-%ED%8C%8C%EC%9D%BC%EC%9D%84-%EB%B0%B0%ED%8F%AC%ED%95%98%EB%8A%94-%EA%B0%9C%EB%B0%9C%EC%9E%90%EB%93%A4%EC%9D%84-%EC%9C%84%ED%95%98%EC%97%AC/)  