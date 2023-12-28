# 5_dotenv는_무엇일까
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2023-12-29
- 수정일: 



#
### 주제를 선정한 이유
React를 사용해서 프로젝트를 진행한 적이 있습니다. 당시, Google Map을 구현을 담당하였습니다. 사용량에 따라 과금이 발생하는 유료 API라 API key 보안이 특히 중요했습니다. 그 때, 처음으로 알게 된 개념이 dotenv 즉, .env입니다. API key 보안에 사용된다는 개념만 알고 있던 .env에 대해 정리해 보고자 합니다.



#
### .env 사용 목적
보안이 필요한 API_KEY나 DB 관련 정보 등을 .env 파일에 환경변수로 만들어 변수를 사용하는 방식으로 중요 정보의 유출을 방지합니다.



#
### .env 사용 방법
1. .env 파일은 프로젝트의 최상위 루트에 저장해야 합니다. 

* 루트 위치에 저장해야 하는 이유
    * 만약 .env 파일이 루트 디렉터리에 위치하지 않는다면, 빌드 프로세스가 해당 파일을 찾지 못해 환경 변수를 올바르게 로드하지 못하게 됩니다.

2. create-react-app에서는 보안이 필요한 환경변수의 외부 유출을 방지하기 위해 REACT_APP_으로 시작되지 않는 환경변수는 무시됩니다. 그러므로 .env에서 변수명은 항상 `REACT_APP_`으로 시작되어야 합니다.

```javascript
REACT_APP_API_KEY=API_VALUE

// 키와 값을 연결해 주는 등호 연산자에 띄어쓰기하지 않음
// 값을 ""로 감싸지 않아도 String으로 인식
```

3. .env에 등록된 변수는 별도의 import가 필요하지 않고, 전역에서 `process.env.REACT＿APP＿`를 사용해 불러올 수 있습니다.

```javascript
process.env.REACT_APP_API_KEY
```

process.env는 실행 시 로드되므로 .env 파일 변경 후에는 React를 다시 실행해야 합니다.

 + 프로젝트를 git에 올릴 경우, 반드시 .gitIgnore .env를 추가하여 환경설정 파일이 외부로 유출되지 않도록 유의해야 합니다.



#
### 정리
5_dotenv는_무엇일까.
- 보안이 필요한 정보를 환경 변수로 설정하여 사용하도록 함으로써 정보의 유출을 방지
- 예약어를 사용해 간단하게 사용할 수 있으나,
    - 파일의 위치는 최상위 루트 디렉터리에 위치 시켜야 하고,
    - .gitIgnore에 포함해 git 저장소에 올리지 않도록 유의해야 함



#
### 📚참고 자료
[[REACT] .env 를 이용한 변수선언 및 사용법](https://carmack-kim.tistory.com/110) <br/>
[[React] 리액트에서 .env 환경변수 사용하기!](https://shape-coding.tistory.com/entry/React-%EB%A6%AC%EC%95%A1%ED%8A%B8%EC%97%90%EC%84%9C-env-%ED%99%98%EA%B2%BD%EB%B3%80%EC%88%98-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0) <br/>
[.env](https://velog.io/@quack777/.env)
