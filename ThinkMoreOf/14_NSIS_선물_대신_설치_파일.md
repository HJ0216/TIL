# 14_NSIS_선물_대신_설치_파일
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2024-04-27
- 수정일: 2024-05-01

<br/>



#
### 주제를 선정한 이유
3월에 시작한 프로젝트가 4월 중순에 끝이났습니다. 프로그램 배포도 끝나고 수정은 간단한 UI나 기능 개선만 이뤄지고 있던 중.. 설치파일을 수정하는 일을 맡게 되었습니다. 그간 설치파일 생각없이 다음다음만 눌렀던 제 자신을 돌이켜보기 위해 글을 작성합니다☠️ 다음 번에는 좀 더 깔끔한 UI를 가진 설치파일을 만들 수 있길🔥!

<br/>



#
### NSIS 정의
NSIS (Nullsoft Scriptable Install System) is a professional open source system to create Windows installers.  
즉, Windows 플랫폼에서 개발자가 인스톨러를 구축할 수 있도록 도와주는 도구입니다.  

<br/>



#
# NSIS와 HM NIS Edit
NSIS를 통해 Setup 파일을 간단하게 만들 수는 있지만, HM NIS Edit을 추가적으로 사용한다면 마법사르 통해 설치 파일의 기본 틀을 보다 빠르고 쉽게 만들 수 있습니다.

<br/>



#
# WPF 애플리케이션 실행 파일 만들기
HM NIS Edit과 관련해서 설치부터 실행까지 너무나 잘 정리되어있는 글들이 많기에 저는 실제 프로젝트에서 사용한 기능을 중심으로 정리할 예정입니다.

💀 난관1: 어느 파일까지 복사할 것인가  
.exe 파일을 installer로 만들려면 설치 대상에 .exe만 선택해주면 되지만, WPF 앱은 그렇지 않습니다. 제가 해봤는데, 실행이 안돼요😊..

그래서 설치 경로 먼저 수정이 필요합니다.

```bash
Section "bin" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File "..\source\WPF\SwitchThemes\SwitchThemes\bin\Debug\net8.0-windows\*"
  CreateDirectory "$SMPROGRAMS\SwitchTheme"
SectionEnd

```

File 부분을 기존 .exe에서 folder 전체로 변경을 합니다.  

⭐ WPF는 실행을 위해 다양한 라이브러리에 대한 종속성이 필요해서 .dll이 함께 설치되어야 합니다. 또한, 리소스가 존재할 경우, 설치 파일에 함께 포함되어야 하는 경우도 있습니다.  

⭐ 단, 최종 사용자에게 배포할 때는 Release 폴더로부터 필요한 파일들만 선택하여 포함시키는 것이 더 적절합니다. 그래야 필요 없는 정보를 제외해서 애플리케이션의 크기를 줄이고 정보의 노출을 막을 수 있습니다.  
(실제로 회사에서도 몇 개의 파일을 제외하고 복사합니다)


💀 난관2: 체크 박스를 2개이상 넣으려면 어떻게 할 것인가..

```bash 
; Finish page
!insertmacro MUI_PAGE_FINISH
```

이 구문과 함께라면 설치 완료 페이지를 자동을 만들어줍니다.  
그러나, 문제는 해당 페이지에 체크박스를 2개 이상 포함시키고 싶을 때, 발생합니다.

우선 1개까지는 기본으로 추가하는 기능을 제공하지만, 2개부터는 커스텀이 안되고 페이지를 따로 만들어줘야 합니다.  

그러나, 기본 기능을 달리 써서 어려움을 헤쳐나갈 수 있습니다.

간단하게 예시를 우리의 친구 StackOverFlow에서 가져와 보여드리면,  

📚참고: [How to set the checkbox by default checked in the windows installer Finish page using NSIS
](https://stackoverflow.com/questions/54064523/how-to-set-the-checkbox-by-default-checked-in-the-windows-installer-finish-page)

```bash
!define MUI_FINISHPAGE_RUN ""
!define MUI_FINISHPAGE_RUN_TEXT "Run Foo"
!define MUI_FINISHPAGE_RUN_FUNCTION MyRunFoo
;define MUI_FINISHPAGE_RUN_NOTCHECKED
!define MUI_FINISHPAGE_SHOWREADME "$InstDir\Bar.exe"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Run Bar"
;define MUI_FINISHPAGE_SHOWREADME_FUNCTION
!define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED
```

MUI_FINISHPAGE_RUN과 MUI_FINISHPAGE_SHOWREADME를 활용할 수 있습니다.  
이 때, README에는 설명서 대신 다른 동작을 넣는 것이죠.

```bash
Function FinishLeave 
${NSD_GetState} $mui.FinishPage.Run $0 ; or $mui.FinishPage.ShowReadme
${If} $0 <> 0 
MessageBox mb_ok "Checkbox checked"
${Else} 
MessageBox mb_ok "Checkbox not checked" 
${EndIf}
FunctionEnd
```

이렇게 최종 페이지 종료 후, checked 유무에 따라 로직을 추가하면 됩니다.

그러나, 만약 checkbox가 3개 이상 필요하다, 그러면 페이지를 만들어야 합니다.

```bash
!include "nsDialogs.nsh"
; nsDialogs 사용을 위한 include

Page Custom MyFinishPageCreate MyFinishPageLeave


Function MyFinishPageCreate
    nsDialogs::Create 1018
    Pop $0 

    ${If} $0 == error
        Abort
    ${EndIf}

    ${NSD_CreateCheckBox} 0 0 100% 12u "First CheckBox"
    Pop $1
    ${NSD_Check} $1

    ${NSD_CreateCheckBox} 0 15u 100% 12u "Second CheckBox"
    Pop $2
    ${NSD_Check} $2

    nsDialogs::Show
FunctionEnd

Function MyFinishPageLeave
    ${NSD_GetState} $1 $0
    
    ${If} $0 == ${BST_CHECKED}
        ; 로직 추가
    ${EndIf}

    ${NSD_GetState} $2 $0
    ${If} $0 == ${BST_CHECKED}
        ; 로직 추가
    ${Else}
        ; 로직 추가
    ${EndIf}
FunctionEnd
```


💀 난관3: 현재 프로그램 실행 여부를 어떻게 확인할 것인가..  
아래 참고 자료에서 `[NSIS] 프로그램 실행중일때는 확인 메시지후 종료하기`를 참고하시면 됩니다.  
⭐FindWindow 사용 방법을 몰랐는데, WPF 프로그램은 Class 이름을 사용할 수 없어, 윈도우 캡션을 사용한다는 것을 배웠습니다.


💀 난관4: 플러그인(DLL 파일) 추가를 어떻게 하는가..  
사실 난관3을 해결하는 여러 방법 중 하나가 DLL 파일 추가가 있었는데, 알고나면 간단하지만 알기 전까지는 한참을 찾았기에 적어둡니다.

NSIS에 설치된 경로로 들어가면  
`C:\Program Files (x86)\NSIS\Plugins`에  
`x86-ansi` 폴더와 `x86-unicode` 폴더가 있는데, 두 폴더에 모두 .dll 파일을 추가해줘야 합니다.  
⭐ Plugins 폴더 안이 아닌 한 단계 더 들어가야 한다는 것에 주의해야 합니다.

<br/>



#
### 정리
NSIS란, Window에서 Installer를 만들어주는 도구이다.  
HM NIS Edit을 사용하면 마법사를 통해 기본 틀을 빠르게 만들 수 있다.  
자료가 오래된 것이 많아 24년 기준 맞지 않는 내용이 있을 수 있으니, 최대한 여러 자료를 찾아보자.

<br/>



#
### 📚참고 자료
[NSIS Wiki](https://nsis.sourceforge.io/Main_Page)  
[NSIS 사용자 설명서](https://www.opentutorials.org/module/3650/21850)  
[[NSIS] HM NIS Edit로 쉽고 빠르게 설치 파일 만들기](https://luckygg.tistory.com/260)  
[NSIS 설치 및 HM NIS Edit 스크립트 마법사 사용하기](https://yeo-computerclass.tistory.com/149)  
[[NSIS] 프로그램 실행중일때는 확인 메시지후 종료하기](https://sheepone.tistory.com/187)  
[‘처음’ Windows 설치 파일을 ‘배포’하는 개발자들을 위하여](https://blog.dramancompany.com/2015/12/%EC%B2%98%EC%9D%8C-windows-%EC%84%A4%EC%B9%98-%ED%8C%8C%EC%9D%BC%EC%9D%84-%EB%B0%B0%ED%8F%AC%ED%95%98%EB%8A%94-%EA%B0%9C%EB%B0%9C%EC%9E%90%EB%93%A4%EC%9D%84-%EC%9C%84%ED%95%98%EC%97%AC/)  