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



<br/>

### 📚 참고
[[HTTPS] - HTTPS 사설 인증서 발급 및 구현 & ngrok 사용법](https://velog.io/@donggoo/HTTPS-HTTPS-%EC%82%AC%EC%84%A4-%EC%9D%B8%EC%A6%9D%EC%84%9C-%EB%B0%9C%EA%B8%89-%EB%B0%8F-%EA%B5%AC%ED%98%84-ngrok)