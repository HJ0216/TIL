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
* Make Chat Publicly Available On 설정을 통해 Chat Url에 접근해서 메시지를 보낼 수 있음
  * Workflow Active 필수


### Manual Trigger
* Execute Workflow를 통해 실행
  * Edit Field 노드를 통해 원하는 input 전달 가능
    * query, value
  * 다음 노드에서는 `{{ $json.query }}`로 key값을 통해 value에 접근 가능

### Web hook Trigger
* Webhook 기반 Trigger를 사용할 경우, http가 아닌 https 통신이 가능해야 함
* ngrok 설치 후, auth-token 설정
```bash
ngrok authtoken '본인의 authtoken 코드'
ngrok http '본인의 로컬 서버 포트'
```
docker-compose.yml 수정
```yml
x-n8n: &service-n8n
  environment:
    - WEBHOOK_URL='ngrok에서 전달받은 https 주소 추가'
```
docker 재시작
```bash
docker compose up -d
-- docker compose: 현재 디렉토리의 docker-compose.yml 파일을 기준으로 컨테이너들을 실행
-- up: 컨테이너들을 생성하고 실행
-- -d: detached 모드로 실행 → 터미널에 계속 붙어 있지 않고 백그라운드로 실행됨
```

* PowerShell 자동화
1. ngrok 환경변수로 설정해서 실행파일이 위치한 곳 뿐만 아니라 전역으로 ngrok 명령어 사용할 수 있도록 설정
2. n8n docker-compose.yml이 위치한 폴더에 *.ps1파일 생성
```sh
Start-Process "cmd.exe" "/k ngrok.exe http 5678"
Start-Sleep -Seconds 5

# Get public ngrok URL
$response = Invoke-RestMethod -Uri "http://127.0.0.1:4040/api/tunnels"
$ngrokUrl = $response.tunnels[0].public_url

# Update docker-compose.yml
$composeFile = "C:\N8N\self-hosted-ai-starter-kit\docker-compose.yml"
$content = Get-Content $composeFile
$content = $content -replace '    - WEBHOOK_URL=.*', "    - WEBHOOK_URL=$ngrokUrl"
Set-Content $composeFile $content

# Restart Docker
cd "C:\N8N\self-hosted-ai-starter-kit"
docker compose down
docker compose up -d
```



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
    * Google Drive
      * Google Cloud Console에서 프로젝트 생성 후, API 사용을 등록
      * Create file을 할 경우, 소유권한이 해당 Google Service의 이메일로 등록되어있으므로 Share 단계가 필요


## Others
### HTTP Request
* 유튜브 자막 API
  * https://kome.ai/api/transcript
    * POST
    * Header: {content-type: application/json}, {origin, https://kome.ai}
    * Body: {"video_id": "{{ $json.url }}", "format": true}

### Merge
다중 Output 값을 1개의 결과로 병합

### Aggregate
Input field의 이름을 기준으로 output 재구성



### Docker 설치 vs 로컬 환경 직접 설치
| 항목 | Docker 사용 | 로컬 환경 직접 설치 |
| --- | --- | --- |
| **의존성 관리** | **완벽히 격리되어 충돌 없음 (매우 우수)** | Node.js 버전 및 다른 프로그램과 충돌 가능성 높음 |
| **환경 일관성** | 개발, 테스트, 운영 환경이 100% 동일 | OS 및 설정에 따라 실행 환경이 달라짐 |
| **버전 관리** | 이미지 태그 변경만으로 간편하고 안전하게 가능 | 명령어 실행 시 호환성 문제 발생 가능 |
| **설치/제거** | **호스트 시스템을 더럽히지 않고 깔끔하게 제거** | 시스템에 불필요한 파일이 남을 수 있음 |
| **이식성** | 볼륨과 명령어만 있으면 어디서든 즉시 복원 가능 | 수동으로 데이터를 백업하고 이전해야 함 |



<br/>

### 📚 참고
[구글 커스텀 서치 (Google Custom Search JSON API, Custom Search Site Restricted JSON API ) 설정하기.](https://mitw.tistory.com/54)