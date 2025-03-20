# 소플의 처음 만난 AWS
🏪 [교보문고](https://product.kyobobook.co.kr/detail/S000214700630)
📖 2025.03.15 - 

## 2. AWS
멀티 팩터 인증(MFA)
오른쪽 상단 계정 클릭 → 보안 자격 증명 클릭 → 멀티 팩터 인증(MFA) 구역에 ㅡMFA 디바이스 할당 버튼 클릭

1단계  
MFA device name: 이중 보안 디바이스 이름  
MFA device: 이중 보안 디바이스 종류  
  * Google Authentificator 사용 시, 인증 관리자 앱 선택

2단계  
QR코드 표시 후, Google Authentificator에서 스캔  
6자리 코드 입력 → 30초 후 다시 생성되는 6자리 코드 입력


## 3. EC2
>EC2

Elastic Compute Cloud, 컴퓨팅 자원을 클라우드로 제공하는 서비스
가상 서버 서비스
  * Elastic: 다른 서비스와 유연하게 연동해서 사용할 수 있음

>Elastic IP

클라우드 컴퓨팅을 위해 고안된 정적 IPv4 주소  
Elastic IP를 EC2 인스턴스에 연결하면 해당 IP 주소로 EC2 인스턴스에 접속할 수 있음
  * EC2 인스턴스에 장애 발생 시, 기존 Elastic IP를 새로운 EC2 인스턴스에 연결할 경우, 클라이언트에서 접속하는 IP 주소의 변경 없이 서버 장애를 극복할 수 있음
  * Elastic IP는 인스턴스에 연결해둘 경우에만 무료

>Security Group

하나 이상의 인스턴스에 대한 트래픽을 제어하는 가상의 방화벽 역할
  * 방화벽(Firewall): 컴퓨터의 보안을 위해 외부에서 내부 또는 내부에서 외부의 정보통신망에 접근하는 것을 허용하거나 차단하기 위한 시스템
  * 인바운드 트래픽: 서버 입장에서 안으로 들어오는 트래픽
  * 아웃바운드 트래픽: 서버 입장에서 밖에서 나가는 트래픽
    * 기본적으로 보안 그룹은 모든 아웃바운드 트래픽을 허용
  * 액세스를 거부하는 규칙을 생성할 수 없음
    * 특정 IP 주소에서 서버의 3000번 포트로 접속하는 것을 허용하는 것은 가능하나, 허용하지 않는 규칙은 불가능

---
>EC2 생성

1. 인스턴스 시작
  * 이름: HariboServer → 추가 태그 추가
2. 애플리케이션 및 OS 이미지
  * 서버에 설치할 운영체제나 애플리케이션 선택
3. 인스턴스 유형
  * 인스턴스 패밀리, 세대, 용량에 맞춰 선택
4. 키 페어
  * 키를 모르거나 잃어버릴 경우, 인스턴스에 접속할 수 없으므로 유의
  * 새 키 페어 생성
    * private key 파일 형식: Windows 환경: .ppk, Mac: .pem
5. 네트워크 설정
  * 보안 그룹 생성 → 다음에서 SSH 트래픽 허용
  * 위치 무관: 어느 IP 주소에서든지 SSH로 접속하는 것을 허용
6. 스토리지 구성
  * 서버에서 사용할 저장 장치를 선택
7. 인스턴스 시작

>SSH로 EC2 인스턴스 접속(Windows) with PuTTY
  * PuTTY: 윈도우 환경에서 리눅스 서버나 다른 원격 시스템에 SSH (Secure Shell), Telnet, Rlogin 등을 사용하여 접속할 수 있는 클라이언트

1. Connection - SSH - Auth - Credentials
  * private key file for authentification: .ppk 파일 선택
2. Session
  * Host Name(or IP address): EC2 인스턴스 퍼블릭 IPv4 주소
3. Open

>Elastic IP 주소 할당 및 인스턴스 연결
1. Elastic IP 주소 할당 → 할당
2. Elastic IP 주소  선택 → 작업 - Elastic IP 주소 연결 → 인스턴스 선택 → 연결

>Elastic IP 주소 연결 해제 및 Elastic IP 주소 반납
1. Elastic IP 주소가 할당된 인스턴스 요약 → 작업 - 네트워킹 → Elastic IP 주소 연결 해제
2. Elastic IP → Elastic IP 주소  선택 → 작업 - Elastic IP 주소 릴리즈
  * Elastic IP는 인스턴스에 연결해둘 경우에만 무료

>보안 그룹 편집
>* 인바운드 규칙 추가
1. 인바운드 규칙 편집
2. 규칙 추가
3. 유형, 포트 범위, 소스, 설명 입력
  * 포트 범위: 서버에서 사용하는 포트 번호 입력
  * 소스: 서버로 들어오는 트래픽
  * 설명: 규칙 추가 이유를 적어두면 협업에 도움
4. 규칙 저장

>보안 그룹 편집
>* 인바운드 규칙 제거
1. 인바운드 규칙 편집
2. 삭제
3. 규칙 저장

>EC2 인스턴스 종료
  * EC2 인스턴스는 삭제가 따로 없으며, 인스턴스 종료 시, 일정 시간 지난 후 자동으로 삭제
1. 인스턴스 상태 - 인스턴스 종료(삭제)
2. 인스턴스 상태: 실행 중 → 종료 중 → 종료됨

⭐ 클라우드는 사용한 만큼 요금을 지불하므로 사용하지 않는 자원은 곧바로 종료/삭제 ⭐


## 4. EBS
>EBS(Elastic Block Store)
* EC2에 연결해서 쓸 수 있는 Block Storage(* 외장 하드 같은 느낌)
  * 한 개의 EBS를 여러 개의 EC2 인스턴스에 연결하는 것은 불가능
  * 한 개의 EC2 인스턴스에 여러개의 EBS를 연결하는 것은 가능

* Volume: EBS의 가장 기본적인 형태로 EC2에 바로 연결 가능한 것
* Snapshot: 볼륨의 특정 시점을 그대로 복사하여 저장한 파일(* 백업 파일)
* AMI(Amazon Machine Image): OS가 설치된 형태의 이미지 파일
  * AMI를 이용하여 EC2 인스턴스를 생성할 수 있음
* IOPS(Input/Output Operations Per Second): 저장 장치의 성능 측정 단위

>EBS 볼륨 생성
1. Elastic Block Store - 볼륨
2. 볼륨 생성
* 볼륨을 생성할 때 동일한 가용 영역에 생성해야만 EC2 인스턴스와 연결할 수 있음
3. 볼륨 생성
4. 볼륨 상태: 생성 중 → 사용 가능
5. 작업 - 볼륨 연결
6. 연결할 인스턴스 선택
7. 볼륨 연결
8. 첨부된 리소스에서 인스턴스 상태 attached 확인

>EBS 스냅샷 생성 및 삭제
1. Elastic Block Store - 볼륨
2. 작업 - 스냅샷 생성
3. 스냅샷 생성
4. Elastic Block Store - 스냅샷
5. 작업 - 스냅샷 삭제

>EBS 볼륨 삭제
  * 볼륨이 EC2 인스턴스에 연결되어 있지 않은 상태에서 삭제 가능
1. Elastic Block Store - 볼륨
2. 작업 - 볼륨 분리
3. 첨부된 리소스가 없는지 확인
4. 작업 - 볼륨 삭제


## 5. ELB
>Load Balancing(부하 분산)
* 부하를 여러 대의 서버로 잘 분산시켜서 요청을 시간 내에 처리할 수 있게 하는 것
  * Load Balancer: 각 서버로 부하를 분산시켜주는 역할을 하는 것
* 목적
  * 성능 향상: 여러 대의 서버가 나눠서 처리하기 때문에 빠르게 응답할 수 있음
  * 안정성 향상: 여러 개의 EC2 인스턴스에 장애가 생겨도 남은 EC2 인스턴스들이 클라이언트의 요청을 처리할 수 있음
  * 서버 장애 예방: 클라이언트의 요청이 대량으로 들어오거나, 여러 개의 EC2 인스턴스가 중간에 장애가 생겨도 미리 계획해둔 백업 계획에 따라 EC2 인스턴스를 더 추가하여 서버 장애를 예방할 수 있음
* 용어
  * Health Check: 서버가 살아있는지 확인
  * Connection Draining: 등록 취소 지연, 사용자의 요청을 처리 중인 서버를 곧바로 삭제하지 못하도록 방지하는 기능
  * Latency: Load Balancer와 서버 사이의 지연 시간

>ELB

![image](https://github.com/user-attachments/assets/dfa00e04-483e-4e5e-8619-c5cae98ad884)
* 부하를 여러 개의 EC2에 골고루 분산시켜 주는 역할
  * ELB는 리전별로 생성
  * ELB는 여러 개의 가용 영역에 존재하는 EC2 인스턴스들에 부하를 분산
  * 모든 EC2 인스턴스에 부하를 분산시키는 것이 아니라, 대상 그룹에 속한 EC2 인스턴스들에게만 부하를 분산
>ELB Load Balancing 알고리즘: Round Robin Scheduling
  * Round Robin Scheduling:  프로세스가 도착한 순서대로 프로세스를 디스패치하지만 정해진 시간 할당량(또는 시간 간격)에 의해 실행을 제한
* 종류
  * ALB: HTTP 헤더를 기준으로 트래픽 분배(OSI 5-7계층)
  * NLB: IP 주소와 포트 번호를 기준으로 트래픽 분배(OSI 4계층)
  * CLB: HTTP 헤더 및 IP 주소와 포트 번호를 기준으로 트래픽을 분배(이전 버전으로 ALB, NLB 사용 권장)

---
>ELB Load Balancer 생성
1. 로드 밸런싱 - 로드밸런서
2. 로드 밸런서 생성
3. Application Load Balancer
4. 이름, 네트워크 매핑, 보안 그룹, 리스너 및 라우팅 설정
  * 네트워크 매핑: 가용 영역 설정
    * 로드 밸런싱을 적용할 인스턴스가 있는 가용 영역을 무조건 포함해야 함
  * 보안 그룹: 로드 밸런서로 들어오고 나가는 트래픽에 대한 가상 방화벽
  * 리스너 및 라우팅: 부하를 어디로 분산시킬지 설정
    * 대상 그룹: ELB가 부하를 분산시킬 대상 인스턴스들의 집합
5. 대상 그룹 생성
  * 대상 유형, 이름 → 다음 → 인스턴스 선택 → 아래에 보류 중인 것으로 포함(대상 그룹에 인스턴스를 대기 상태로 넣음) 클릭  → 대상 그룹 생성
6. 새로고침 후, 대상 그룹 선택
7. 로드 밸런서 생성
8. 상태
  * 프로비저닝(IT 자원을 사용할 수 있는 상태로 준비하는 것) 중 → 활성
9. 로드 밸런싱 - 대상 그룹 - 대상 탭
  * 상태 확인이 healthy인지 확인(= 부하를 분산받을 수 있는 상태)
10. DNS 이름 주소로 접속 가능한지 확인
![image](https://github.com/user-attachments/assets/75bb2330-a86d-4a70-8fe2-807faeb526ec)

>다른 가용 영역에 EC2 인스턴스 생성
1. 네트워크 설정 → 편집
2. 서브넷에서 기존 인스턴스와 다른 가용 영역 선택

>ELB 대상 그룹에 새로운 EC2 인스턴스 등록
1. 로드 밸런싱 - 대상 그룹
2. 대상 그룹 - 대상 탭 → 대상 등록
3. 인스턴스 선택 → 아래에 보류 중인 것으로 포함 → 보류 중인 대상 등록
![image](https://github.com/user-attachments/assets/08b7ae28-b6ca-46ee-949f-9c0ba07f3171)


## 6. Auto Scaling
>Auto Scaling
* 트래픽에 따라 자동으로 서버의 개수를 조절해주는 기능
 * (EC2 관점에서는 트래픽에 따라 자동으로 EC2 인스턴스 개수를 조절해주는 기능)

> AWS Auto Scaling
* 구조
  * 클라이언트 요청이 ELB로 들어오면, 로드 밸런서에서 ASG(Auto Scaling Group)으로 부하를 분산
    * ASG: Auto Scaling되는 EC2 인스턴스들의 집합
  * ASG(Auto Scaling Group)는 AMI(Amazon Machine Image)를 필요로 하며, Cloud Watch라는 클라우드 모니터링 서비스를 사용해서 서버 용량을 늘릴지 줄일지 결정
  * 시작 구성(Launch Configuration): Auto Scaling을 할 때 사용할 EC2 인스턴스의 사전 설정 정보

>AMI 생성하기
1. 작업 - 이미지 및 템플릿 - 이미지 생성
2. 이름 입력
3. 재부팅 옵션 선택
  * 인스턴스가 잠시라도 중단되면 안될 경우, 옵션을 활성화하지 않으나 파일 시스템의 무결성이 보장되지 않음

ASG 생성
1. Auto Scaling - Auto Scaling 그룹
2. Auto Scaling 그룹 생성
3. (1단계) 시작 템플릿 또는 구성 선택
  * 이름 입력 및 시작 템플릿 생성
    * 만들어둔 AMI 선택, 이 외 EC2 생성 과정과 동일 → 시작 템플릿 생성
  * 시작 템플릿 선택
4. (2단계) 인스턴스 시작 옵션
  * 가용 영역 및 서브넷 선택
    * ELB 만들 때 생성했떤 대상 그룹의 가용 영역과 동일하게 설정 필수
    Auto Scaling으로 생성된 EC2 인스턴스가 대상 그룹에 속하게 되어 트래픽을 전달받아야 함
5. (3단계) 다른 서비스와 통합
  * 로드 밸런서와 Auto Scaling Group을 연결
    * 기존 로드 밸런서에 연결 → 대상 그룹 선택: Auto Scaling으로 생성된 EC2 인스턴스가 대상 그룹에 속하게 되어 트래픽을 전달받을 수 있음
  * 상태 확인 - Elastic Load Balancer 상태 확인 켜기(ELB 상태 체크)
6. (4단계) 그룹 크기 및 크기 조정 구성
  * 크기 조정: EC2 인스턴스의 개수 입력
  * 대상 추적 정책 사용 여부 선택: Auto Scaling 그룹의 크기를 조정하기 위한 조건
7. (5단계) 알림 추가
8. (6단계) 태그 추가
9. (7단계) 검토
  * Auto Scaling 그룹 생성 클릭

>Auto Scaling 작동 테스트
  * ASG를 생성하면 ASG의 최소 크기를 1로 설정했기 때문 EC2 인스턴스가 하나 자동으로 생성
1. 부하 프로그램 사용하여 Auto Scaling 그룹의 크기를 조정하기 위한 조건이 발동하도록 설정
2. Auto Scaling으로 생성된 EC2의 모니터링을 통해 부하 확인
3. Auto Scaling 발동 조건 확인 시, EC2 생성 확인
4. Auto Scaling - Auto Scaling 그룹 - 활동, 인스턴스 관리 확인
5. 로드 밸런싱 - 대상 그룹 - 대상 확인
  * ASG와 대상 그룹의 인스턴스 개수가 다른 이유
    * 대상 그룹: 로드 밸런서가 부하를 분산하기 위한 그룹(수동으로 생성한 인스턴스가 포함됨) 
    * ASG: Auto Scaling된 인스턴스만 관리하기 위한 그룹

![image](https://github.com/user-attachments/assets/7beb075a-c76b-4b12-93b5-ebab4ca8e1ac)
🚨 문제점  
각 EC2 인스턴스가 각각 DB에 연결되어있어 다른 EC2에 연결될 경우, 특정 EC2에 저장된 데이터가 보이지 않는 문제

⭐ 해결  
DB가 EC2 인스턴스에 들어가는 것이 아니라 별도의 DB 인스턴스를 구성해서 모든 EC2 인스턴스들이 해당 DB를 바라보도록 해야 함
