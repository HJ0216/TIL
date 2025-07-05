## Trigger
### On Chat Message
* 대화 형식을 통해 Input 전달
```json
{
  "sessionId": "",
  "action": "sendMessage",
  "chatInput": "안뇽"
}
```
### Manual Trigger
* Execute Workflow를 통해 실행
  * Edit Field 노드를 통해 원하는 input 전달 가능
    * query, value
  * 다음 노드에서는 `{{ $json.query }}`로 key값을 통해 value에 접근 가능

## AI
### AI Agent
* Chat Agent
  * LLM 모델 연결
    * Open AI
      * Billing에서 카드 등록 후 사용 가능
      * credential에 추가해서 사용
      * 모델 별로 금액이 상이하므로 상황에 맞는 모델 선택
        * [Pricing](https://openai.com/api/pricing)
      * 최신 데이터 업데이트 일자 확인 필요
    * Gemini
      * key 설정을 위해 Google Cloud에서 Project 생성 필요
      * Google Cloud에서 해당 프로젝트에서 gemini api 사용으로 전환
      * API 생성 시, Generative Language API로 용도 제한
      * credential에 추가해서 사용
      * 모델 별로 금액이 상이하므로 상황에 맞는 모델 선택
        * [Pricing](https://ai.google.dev/gemini-api/docs/pricing?hl=ko&_gl=1*nej4sm*_up*MQ..*_ga*MTA0NTE5NjcxNy4xNzUxNjg4MDE1*_ga_P1DBVKWT6V*czE3NTE2ODgwMTUkbzEkZzAkdDE3NTE2ODgwMTUkajYwJGwwJGgxOTUyMjU0NzA1)
* Memory
  * sessionId 기준으로 사용자와 대화 데이터 기억
  * Context Window Length: 기억할 대화 개수
    * 많은 대화를 기억할 수록 Input이 늘어나므로(이전 대화 기록도 Input에 함께 보냄) 적당량 설정 필요(기본: 5)
* Tools
  * 웹 검색 같은 도구 추가
  * SerpApi
    * https://serpapi.com
    * 다양한 검색 엔진의 검색 결과를 API 형태로 제공하는 서비스
    * 한 달에 100회 무료 가능
  * Http Request Tool
    * 구글 검색 API나 네이버 검색 API처럼 외부 API를 AI 에이전트의 '툴'로 연동할 때 `HTTP Request 노드` 
    * AI 에이전트는 Description 필드에 작성된 설명을 보고 해당 노드의 기능과 사용 방법을 이해하므로 명확히 작성해야 함
    * 한 달에 100회 무료 가능
    * Google Search Api
      * 프로그래밍 검색 엔진[https://programmablesearchengine.google.com/] 필요
      * key 설정을 위해 Google Cloud에서 Project 생성 필요
      * Google Cloud에서 해당 프로젝트에서 Custom Search API 사용으로 전환
      * [API Docs](https://developers.google.com/custom-search/v1/using_rest?hl=ko)
        * 검색 엔진 cx 값(cx)
        * api key 값(key)
        * query string 값(q)
          * Defined automatically by the model
    * Naver Search Api
      * Application 생성 필요: Client ID, Client Secret
      * [API Docs](https://developers.naver.com/docs/serviceapi/search/web/web.md#%EC%9B%B9%EB%AC%B8%EC%84%9C)
        * Header: X-Naver-Client-Id, X-Naver-Client-Secret
        * Query Param: query
      * 일일 호출 허용량: 25,000


## Others
### Merge
다중 Output 값을 1개의 결과로 병합

### Aggregate
Input field의 이름을 기준으로 output 재구성


<br/>

### 📚 참고
[구글 커스텀 서치 (Google Custom Search JSON API, Custom Search Site Restricted JSON API ) 설정하기.](https://mitw.tistory.com/54)