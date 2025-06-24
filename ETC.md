### Ngrok
로컬 개발 서버를 안전하게 외부에 노출시킬 수 있는 HTTPS 터널링 도구 
* 터널링: 로컬(내 컴퓨터에서만 접근 가능한) 서버를 외부 인터넷에서도 접근할 수 있도록 ‘가상 통로’를 만드는 것

로컬 개발환경인 localhost에서 구동 중인 웹 서비스를 외부 인터넷 환경에서 접근할 수 있도록 만들어줌  
Webhook 테스트, 실시간 데모, 로컬 개발환경 접근 등에 유용
* Webhook: 외부 서비스에서 특정 이벤트가 발생했을 때, 내 서버에 실시간으로 알림을 보내주는 시스템

```bash
ngrok authtoken '본인의 authtoken 코드'
ngrok http '본인의 로컬 서버 포트'
```


### Prompt Engineering
1. 효과적인 코드 프롬프트의 기본 원칙
* 풍부한 맥락 제공: 사용 언어·프레임워크·라이브러리·에러 메시지·코드 목적 등 관련 정보 명시
* 명확한 목표나 질문 제시: “왜 코드가 안 돼?”와 같은 모호한 질의 대신, 원하는 결과와 현재 상황을 명확하게 기술
* 복잡한 작업 분할: 대규모 기능 개발 등은 한 번에 모두 요청하지 않고, 작은 단계로 쪼개어 요구
* 입출력 예시나 기대 동작 포함: 실제 입력·출력이나 동작 예시 제공
* 역할(페르소나) 활용: “React 시니어 개발자처럼 코드 검토” “성능 전문 지도로 최적화 요청” 등 책임 있는 역할을 부여
* 회화적 반복 개선: AI의 첫 번째 답변을 바탕으로 추가 요청이나 수정 요구를 통해 점진적으로 원하는 결과에 도달
* 코드 일관성 유지: AI가 코드 스타일, 네이밍, 주석을 참고하므로 코드의 일관성과 명확성을 항상 유지함
2. 디버깅을 위한 프롬프트 패턴
```javascript
function mapUsersById(users) {
  const userMap = {};
  for (let i = 0; i <= users.length; i++) {  
    const user = users[i];
    userMap[user.id] = user;
  }
  return userMap;
}
const result = mapUsersById([{ id: 1, name: "Alice" }]);
```
“왜 mapUsersById 함수가 동작하지 않을까?”
→ “mapUsersById 함수가 사용자 배열을 id별로 매핑해야 하는데, [ {id: 1, name: "Alice"} ] 입력 시 TypeError: Cannot read property 'id' of undefined 에러 발생. 코드는 다음과 같다: [코드 포함] 기대 결과는 { "1": ... } 이런 현상 원인과 해결책은?”
* 추가 디버깅 프롬프트 전략
  * 버그 원인 후보 목록화 요청(“TypeError의 가능한 원인?” 등)
  * 코드 동작 논리 직접 설명 후 검토 요청(“내 설명이 맞는지, 문제점을 찾아달라”)
  * 돌발 상황 테스트케이스 요청(“이 함수가 실패할 수 있는 입력 2개만 제안”)
  * 꼼꼼한 코드 리뷰어 역할 부여(“이 코드를 리뷰하며 문제점과 개선사항을 설명”)
3. 리팩토링/최적화를 위한 프롬프트 패턴
```javascript
async function getCombinedData(apiClient) {
  // Fetch list of users
  const usersResponse = await apiClient.fetch('/users');
  if (!usersResponse.ok) {
    throw new Error('Failed to fetch users');
  }
  // ... (이하 생략)
}
```
“getCombinedData 함수를 리팩토링 하라”
→ “중복 제거, 성능 개선, 두 fetch 병렬화, 에러 메세지 분리, 데이터 결합은 효율적 방식으로 개선하라. 주석과 개선 포인트 설명까지”
* 추가 리팩토링 팁
  * 단계별 요청(“가독성 개선→알고리듬 최적화” 순차 적용)
  * 다른 접근 방식 요청(“함수형 스타일로도 구현해줘” 등)
  * 코드+설명 방식 요청을 통한 학습과 튜토리얼화
  * 결과 코드에 대한 테스트 추가 요청



### Prompt Engineering(2)
핵심은 프로젝트마다 ‘CLAUDE.md’ 파일을 활용해 컨벤션, 아키텍처, 패턴, 금지사항 등을 명확히 문서화하고, 코드 내 ‘anchor comment’로 AI를 효과적으로 가이드하는 것

테스트 코드는 반드시 사람이 작성해야 하며, AI가 테스트, 마이그레이션, 보안, 등 핵심 영역을 수정하지 못하도록 경계를 엄격히 설정해야 함

[예제 md 파일](https://github.com/julep-ai/julep/blob/dev/AGENTS.md)

세션 관리와 맥락 오염 방지  
작업별로 Claude 세션을 새로 시작하는 것이 중요
하나의 긴 대화에 여러 작업(예: DB 마이그레이션, 프론트엔드 디자인 등)을 혼합하면 컨텍스트가 섞여 의도하지 않은 결과 초래  
규칙: 한 작업 = 한 세션, 완료 시 세션 새로 시작  



### 커밋 전 주의사항
작업 파일 커밋 전 항상 어떤 파일에 어떤 내용 수정했는지 확인 후 커밋
* 잠시 테스트한다고 작성하거나 주석 처리한 내역까지 같이 올리지 않도록 유의



### 관심사 분리
컴퓨터 프로그램을 만들 때, 서로 다른 역할을 하는 코드들을 독립적인 별개의 모듈(부분)로 나누어 작성하는 설계 원칙  
각 모듈은 오직 하나의 관심사(역할, 책임)에만 집중  
* 판단 기준
  * 클래스/메서드가 한 번에 너무 많은 일을 하고 있지는 않은가
  * 요구사항이 변경된다면, 코드의 한 부분만 수정해서 해결할 수 있는가
  * 로직을 다른 곳에서도 사용할 가능성이 있는가

예시
* View
  * 사용자에게 정보를 보여주고(Presentation), 사용자 입력을 받는 것에만 집중
* Business Logic
  * 잔액을 계산하고, 업데이트하고, 유효성을 검사하는 등 실제 '일'을 처리하는 것에 집중
```cs
public partial class wndRegister : Window
{
    private void Button_Register_Click(object sender, RoutedEventArgs e)
    {
        string username = txtUsername.Text;
        string password = txtPassword.Password;

        if (!ValidationHelper.IsValid(username, password, out string errorMessage))
        {
            MessageBox.Show(errorMessage);
            return;
        }
    }
}
```



<br/>

### 📚 참고
[[HTTPS] - HTTPS 사설 인증서 발급 및 구현 & ngrok 사용법](https://velog.io/@donggoo/HTTPS-HTTPS-%EC%82%AC%EC%84%A4-%EC%9D%B8%EC%A6%9D%EC%84%9C-%EB%B0%9C%EA%B8%89-%EB%B0%8F-%EA%B5%AC%ED%98%84-ngrok)
[프로그래머를 위한 프롬프트 엔지니어링 플레이북](https://news.hada.io/topic?id=21303)
[Claude로 실제 코드를 배포하며 얻은 실전 노트](https://news.hada.io/topic?id=21352)