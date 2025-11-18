## EC2

### AMI(Amazon Machine Image)

- 인스턴스를 실행할 때 필요한 정보를 제공
- 운영 체제와 소프트웨어를 적절히 구성한 상태로 제공되는 템플릿

### Key Pair

- EC2 인스턴스에 연결할 때 자격을 증명하는 보안 키
  - Public Key: EC2 인스턴스에 저장
  - Private Key: 사용자의 컴퓨터에 별도로 저장하고, 해당 키를 이용하여 자격을 증명하고 가상 서버에 접근

### EC2 네트워킹

- Subnet

  - 부분 네트워크
  - Subnet Mask
    - 서브넷을 구분하고 식별하는 수단
    - 네트워크 ID(서브넷을 구분하는 기준)와 호스트 ID(동일한 서브넷에서 대상을 구분하는 기준 값)로 구성
      - 같은 서브넷: IP주소의 네트워크 ID는 동일, 호스트 ID는 상이
      - 다른 서브넷: IP주소의 네트워크 ID가 상이

- Routing

  - 네트워킹 통신을 수행할 때 목적지 경로를 선택하는 작업
  - 라우터: 라우팅을 수행하는 장비
  - 라우팅 테이블: 서브넷의 경로 리스트로 목적지 네트워크에 대한 최적 경로를 선택해서 전달

- 보안 그룹

  - EC2 인스턴스의 송수신 트래픽을 제어하는 가상의 방화벽 역할
    - 트래픽을 정의하는 방법: 프로토콜, 포트 번호, IP 대역 등
  - 인바운드 규칙: 수신 트래픽 허용/거부
  - 아웃바운드 규칙: 송신 트래픽 허용/거부

  | 포트 번호 | 용도                      | 설명                                                                               |
  | --------- | ------------------------- | ---------------------------------------------------------------------------------- |
  | `22`      | **SSH 접속**              | EC2 리눅스 서버에 원격 접속할 때 사용 (예: `ssh ec2-user@IP`)                      |
  | `80`      | HTTP 웹 접속 (기본 포트)  | 브라우저에서 포트 없이 접속 (예: `http://13.209.12.34`)                            |
  | `443`     | HTTPS 웹 접속 (기본 포트) | 보안 연결 (예: `https://example.com`)                                              |
  | `8080`    | 웹 개발/테스트용 포트     | 웹 브라우저나 모바일 앱에서 API 호출을 받아야 함 (`http://public-ip-address:8080`) |

  - 22번 포트는 웹 서버용이 아니므로, 브라우저로 `http://public-ip-address:22` 해도 응답 없음
  - 웹 서비스 사용 시, 80, 443, 또는 8080 같은 포트를 사용해야 함

- 보안그룹과 네트워크 ACL

  - 보안 그룹

    - 인스턴스 별 트래픽 접근 통제
    - 이전 상태 정보를 기억하고 다음에 그 상태를 활용하는 스테이트풀 접근 통제
    - 허용 규칙만 나열하며 허용 규칙에 해당하지 않으면 자동 거부

  - 네트워크 ACL(Access Control List)

    - 서브넷 별 트래픽 접근 통제
    - 이전 상태 정보를 기억하지 않아 다음에 그 상태를 활용하지 않는 스테이트리스 접근 통제
    - 허용 규칙과 거부 규칙이 모두 존재하여 규칙을 순차적으로 확인하고 허용과 거부를 판단

### 탄력적 IP

- 고정 공인 IP 주소
- 필요한 경우
  - 도메인 연결됨
  - 외부 서비스 연동됨(특정 IP 등록 필요)
- 🔴 탄력적 IP 할당했으면 반드시 EC2에 연결하거나, 안 쓰면 삭제!

### MobaXterm을 활용한 EC2 접속

- Remote Host: Public IP address
- Specify username: ec2-user
- Use private key: 해당 인스턴스 key 선택

### EC2에 git 설치 및 프로젝트 빌드

```bash
# linux 기준
sudo yum install git -y
git --version # 설치 확인

git clone https://github.com/hj0216/lucky-log.git

# Java 17 설치 (Spring Boot 3.x용, Amazon Linux 2023 기준)
sudo dnf install java-17-amazon-corretto -y
java -version # 설치 확인

cd lucky-log

chmod +x gradlew # 실행 권한 부여
./gradlew build # 빌드
java -jar build/libs/lucky-log-0.0.1-SNAPSHOT.jar # 빌드 후 생성된 jar 파일 실행
```

#### Build fail

```bash
FAILURE: Build failed with an exception.

* What went wrong:
Could not determine the dependencies of task ':bootJar'.
> Could not resolve all dependencies for configuration ':runtimeClasspath'.
> Failed to calculate the value of task ':compileJava' property 'javaCompiler'.
> Cannot find a Java installation on your machine (Linux 6.1.156-177.286.amzn2023.x86_64 amd64) matching: {languageVersion=17, vendor=any vendor, implementation=vendor-specific, nativeImageCapable=false}.
Toolchain download repositories have not been configured.
# Java 17 toolchain을 찾지 못해 실패
# EC2 서버에 Java 17이 설치되어 있지 않거나 경로가 설정되지 않은 상황
# Java 설치 및 경로 설정 후에도 발생 시, Gradle이 로컬 JDK를 사용하지 않고 toolchain 다운로드만 허용된 상태에서 자동 검색 실패(toolchain 자동 다운로드만 활성화되고, 로컬 JDK fallback이 비활성화된 상태)

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}
```

```bash
[ec2-user@ip-172-31-43-99 lucky-log]$ ./gradlew -q javaToolchains

+ Options
  | Auto-detection: Enabled
  | Auto-download: Enabled

+ Amazon Corretto JRE 17.0.17+10-LTS
  | Location: /usr/lib/jvm/java-17-amazon-corretto.x86_64
  | Language Version: 17
  | Vendor: Amazon Corretto
  | Architecture: amd64
  | Is JDK: false
  # EC2 서버에서 감지된 것은 JRE이고, Gradle이 요구하는 것은 JDK
  # Gradle toolchain은 javac가 필요하므로 JDK가 아니면 실패
  | Detected by: Common Linux Locations

# java와 javac는 정상적으로 출력되지만, Gradle Toolchain이 이를 JRE로 오인하는 경우 원인
# 시스템 설정이 JRE를 우선 사용하게 되어 있어서 Gradle이 그것만 보고 오류가 나는 상태
# (Amazon Linux에서 alternatives 설정이 JRE 우선으로 잡혀 있기 때문)
# JDK = 개발용 (javac 포함), JRE = 실행용 (javac 없음)

# alternatives에서 JDK로 명시 지정
sudo alternatives --config java
# /usr/lib/jvm/java-17-amazon-corretto.x86_64/bin/java 항목을 선택
sudo alternatives --config javac
# /usr/lib/jvm/java-17-amazon-corretto.x86_64/bin/javac 항목을 선택

```

### EC2에서 백그라운드 실행

```bash
# nohup으로 백그라운드 실행
nohup java -jar build/libs/lucky-log-0.0.1-SNAPSHOT.jar > app.log 2>&1 &

# 실행 확인
ps aux | grep java

# 로그 보기
tail -f app.log

# 종료할 때
ps aux | grep java
kill [PID번호]
```

### 설정 파일 관리

1. Local에서 설정 파일을 서버로 복사 후 빌드

### 환경 변수 관리

1. 환경 변수 설정

```bash
# .env 파일에 있는 환경 변수들을 읽어서, 해당 값들을 java -jar 실행 시 환경 변수로 설정
# 해당 명령 실행에만 적용 (일시적)
# 터미널 세션 종료 전까지 환경에 남게 설정하는 방법은 .env에 DB 설정이 남은 상태에서 다른 프로젝트 실행 → 충돌 가능
env $(cat .env | xargs) java -jar build/libs/xxx.jar
```

### 포트 포워딩

```bash
# 1. Nginx 설치
sudo yum install nginx -y

# 2. 설정 파일 생성
sudo nano /etc/nginx/conf.d/luckylog.conf
server {
    listen 80;
    server_name luckylog.com www.luckylog.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 3. Nginx 시작
sudo systemctl start nginx
sudo systemctl enable nginx

# Nginx 실행 중인지 확인
sudo systemctl status nginx
```

### RDS 설정

- 데이터베이스 생성 방식 선택
  - 표준 생성
- 엔진 옵션
  - 엔진 유형
    - MySQL
  - RDS 확장 지원 활성화
    - 체크 해제(과금)
- 템플릿
  - 프리 티어
- 가용성 및 내구성
  - 배포 옵션
    - 단일 AZ DB 인스턴스 배포(인스턴스 1개)
- 설정
  - DB 인스턴스 식별자
    - 현재 AWS 리전에서 AWS 계정이 소유하는 모든 DB 인스턴스에 대해 고유
  - 자격 증명 설정
    - 마스터 사용자 이름
    - 자격 증명 관리
      - 자체 관리
        - 마스터 암호/암호 확인 입력
- 인스턴스 구성
  - 버스터블 클래스(프리티어 기준)
    - db.t3.micro: CPU아키텍처 x86(EC2 인스턴스와 동일하게 설정)
    - db.t4g.micro: CPU아키텍처 Arm
- 스토리지
  - 스토리지 유형
    - 범용 SSD(gp2)
  - 할당된 스토리지
    - 20 GiB(20보다 용량 넘어가면 과금)
  - 스토리지 자동 조정 활성화
    - 체크 해제(과금)
- 연결
  - 컴퓨팅 리소스
    - EC2 컴퓨팅 리소스에 연결
  - VPC
    - Default VPC
    - EC2와 RDS를 같은 VPC&서브넷에 배치
  - DB 서브넷 그룹
    - 자동 설정(기본값)
    - EC2(Public)와 분리하여 선택(Private)
  - 퍼블릭 엑세스
    - 아니오(EC2 내부에서만 접근 가능)
  - VPC 보안 그룹(방화벽) - RDS 전용 보안 그룹 생성 - 인바운드 규칙
    - 타입: MySQL/Aurora (3306)
    - 소스: EC2 보안 그룹 ID (sg-xxxxx)
    - 설명: Allow from EC2 instances
  - 가용 영역
    - 연결할 EC2의 가용 영역과 동일하게 설정(가용 영역이 다를 경우, 통신할 때마다 비용 발생)
- 데이터 베이스 인증
  - 데이터베이스 인증 옵션
    - 암호 인증
- 모니터링
  - Database Insights - 표준
  - 추가 모니터링 설정
    - Enhanced monitoring 활성화
      - 체크 해제(과금)
- 추가 구성
  - 데이터베이스 옵션
    - 초기 데이터베이스 이름
      - db의 schema 이름
    - 백업
      - 자동 백업 활성화
      - 암호화 활성화
      - 마이너 버전 자동 업그레이드 사용
      - 삭제 방지 활성화
        - 체크 해제(과금)
- 파라미터 그룹 설정
  - `time_zone` : Asia/Seoul
  - `character_set_*` : utf8mb4 # 이모지
  - `collation_*` : utf8mb4_general_ci(대소문자 구분하지 않음: email 등)
    - 필요한 컬럼만 utf8mb4_bin으로 변경(대소문자 구분함: key값 등)

### SpringBoot/Thymeleaf 서버에서 빌드 후 배포

1. EC2 생성

- 보안 그룹 인바운드 설정
  - 80 (HTTP): 0.0.0.0/0
  - 443 (HTTPS): 0.0.0.0/0
  - 22 (SSH): 0.0.0.0/0 (위치 무관)
    - 보안상 위험, 특정 IP 주소 또는 IP 범위로 제한
  - 8080(Spring Boot): 0.0.0.0/0
    - 단, nginx 사용 시, nginx를 통해 접속할 수 있도록 삭제

2. RDS 생성

- 버스터블 클래스 선택 시, EC2 인스턴스의 아키텍쳐와 동일하게 설정
- VPC 선택 시, EC2가 동일한 VPC 내에 있어야 통신이 가능
- DB 서브넷 그룹 설정 시, 최소 2개 AZ의 Private 서브넷 선택

  - 역할별 분리
    - Public Subnet: 외부와 통신하는 리소스 (EC2, 로드밸런서)
    - Private Subnet: 내부 전용 리소스 (RDS, 캐시)

- 가용 영역 선택 시, EC2와 같은 AZ 권장 (레이턴시 감소)
- 보안 그룹 설정 시, 인바운드 규칙에 특정 출처(EC2의 보안 그룹 ID)에게 특정 포트(MySQL: 3306) 개방 → EC2만 RDS에 접속 가능
  - EC2 인스턴스의 IP가 아닌 보안 그룹을 참조하면, IP가 변경되어도 규칙을 수정할 필요가 없음

3. EC2에 RDS 연결 및 추가 설정

```bash
# 1. MariaDB 클라이언트 설치
sudo dnf install mariadb105 -y
# dnf: Amazon Linux 2023의 패키지 매니저
# Amazon Linux 2023에는 MySQL이 기본적으로 포함되어 있지 않음
# Amazon Linux 2023에서 RDS MySQL 연결 시 MariaDB 클라이언트 사용

# 2. RDS에 접속
mysql -h rds-endpoint -P 3306 -u root -p
# -h: 호스트(Host) - 연결할 서버 주소
# -P: 포트(Port) - 연결할 포트 번호 (대문자 P)
# -u: 유저(User) - 데이터베이스 사용자 이름
# -p: 패스워드(Password) - 비밀번호 입력 프롬프트 (소문자 p)
# root는 RDS 생성 시, 자격 증명 설정에서 설정했던 값 사용

# 3. 권한 부여
CREATE USER 'db_user'@'%' IDENTIFIED BY 'password';
# '%': 모든 호스트에서 접속 허용 (어디서든 연결 가능)
# RENAME USER 'db_user'@'%' TO 'db_user'@'ec2_private_ip';
# ec2_private_ip에서만 접속 가능
GRANT CREATE, ALTER, SELECT, INSERT, UPDATE, DELETE ON luckylog.* TO 'db_user'@'%';
# luckylog 데이터베이스의 모든 테이블에 대한 권한
FLUSH PRIVILEGES;
# 권한 변경사항을 즉시 적용

# 4. RDS에 접속
mysql -h rds-endpoint -P 3306 -u db_user -p
```

- 별도 사용자를 만드는 이유
  - 보안과 권한 최소화

4. java 설치

```bash
sudo dnf install java-17-amazon-corretto-devel -y
# Amazon Corretto 17(AWS에서 제공하는 무료 OpenJDK 배포판) 설치

java -version
```

5. git 설치 및 프로젝트 clone

```bash
sudo dnf install git -y
git --version

git clone https://github.com/HJ0216/lucky-log.git
```

6. 프로젝트 빌드

```bash
chmod +x ./gradlew
# gradlew: 프로젝트를 빌드하거나 실행할 때 사용

./gradlew clean build
```

7. deploy 사용자 생성

```bash
# deploy 사용자 생성
sudo useradd -m -s /bin/bash deploy
# -m: 홈 디렉토리 자동 생성(/home/deploy)
# -s /bin/bash: 기본 쉘을 bash로 설정

# 비밀번호 설정 (선택사항)
sudo passwd deploy
```

8. 실행 전 환경 변수 설정

```yaml
# application-prod.yaml
spring:
  datasource:
    url: ${PROD_DB_URL}
    username: ${PROD_DB_USER}
    password: ${PROD_DB_PASSWORD}
    driver-class-name: com.mysql.cj.jdbc.Driver
```

```bash
# 환경 파일 생성
sudo mkdir -p /etc/luckylog
# 필요한 상위 디렉토리까지 자동으로 생성
sudo nano /etc/luckylog/env

# /etc/luckylog/env 내용
PROD_DB_URL=jdbc:mysql://rds-endpoint:3306/schema_name?characterEncoding=UTF-8&serverTimezone=Asia/Seoul
# JDBC URL 파라미터: Java 앱 ↔ MySQL 사이에서 데이터를 어떻게 주고받을지
# 파라미터 그룹: MySQL 서버 설정(MySQL 서버 내부에서 데이터를 어떻게 저장/처리할지)
# characterEncoding=UTF-8, MySQL Connector가 서버 설정 보고 utf8mb4로 알아서 처리함
PROD_DB_USER=db_user
PROD_DB_PASSWORD=db_user_password
SPRING_PROFILES_ACTIVE=prod

# 권한 설정
sudo chmod 600 /etc/luckylog/env
# 소유자(owner)는 읽기·쓰기 가능, 다른 사람은 아무 권한 없음
sudo chown deploy:deploy /etc/luckylog/env
# 소유자를 deploy로 변경
```

- 권한 설정을 하는 이유
  - deploy user만 읽고 쓸 수 있게 하여, 민감 정보가 노출되는 것을 최소화

9. systemd 서비스 생성

- systemd 서비스
  - Linux에서 프로그램을 자동으로 실행하고 관리하는 시스템

| 구분                 | 일반적인 프로그램 실행          | systemd 서비스                   |
| -------------------- | ------------------------------- | -------------------------------- |
| **실행 방식**        | 터미널에서 직접 실행            | 백그라운드에서 자동 실행         |
| **터미널 종속성**    | 터미널 닫으면 프로그램도 종료됨 | 터미널과 독립적으로 실행         |
| **서버 재부팅 후**   | 다시 수동으로 실행해야 함       | 자동으로 시작                    |
| **프로그램 중단 시** | 수동으로 다시 실행해야 함       | 자동으로 재시작                  |
| **로그 관리**        | 수동으로 관리해야 함            | 자동으로 관리됨 (journalctl)     |
| **제어 방법**        | 프로세스 ID로 직접 관리         | systemctl 명령어로 간편하게 제어 |
| **모니터링**         | 별도 도구 필요                  | systemctl status로 즉시 확인     |

```bash
# systemd 서비스 파일 생성
sudo nano /etc/systemd/system/luckylog.service

# 서비스 파일 생성 후
sudo systemctl daemon-reload  # 서비스 파일 변경사항 반영
sudo systemctl enable luckylog  # 부팅 시 자동 시작 활성화
sudo systemctl start luckylog  # 서비스 시작
sudo systemctl status luckylog  # 상태 확인

# 명령어
sudo systemctl start luckylog # 시작
sudo systemctl stop luckylog # 중지
sudo systemctl restart luckylog # 재시작, 업데이트 후 실행
sudo systemctl status luckylog # 상태 확인
sudo journalctl -u luckylog -f # 실시간 로그 보기
sudo journalctl -u luckylog -n 50 # 최근 로그 50줄 보기
```

```ini
[Unit] # 서비스 기본 정보
Description=Lucky Log Spring Boot Application
After=network.target # 네트워크가 준비된 후에 시작

[Service] # 서비스 실행 방식
Type=simple # 프로세스가 바로 시작되는 단순 타입
User=deploy # deploy 유저 권한으로 실행
WorkingDirectory=/home/deploy/lucky-log # 프로그램이 실행될 작업 디렉토리
EnvironmentFile=/etc/luckylog/env # 환경변수 파일 경로 (DB 비밀번호 등)
ExecStart=/usr/bin/java -jar /home/deploy/lucky-log/luckylog.jar # 실제 실행할 명령어 (Java JAR 파일 실행), 절대 경로를 사용해서 안전하게 실행
ExecStartPost=/bin/bash -c 'sleep 30 && curl -f http://localhost:8080/actuator/health || exit 1' # 앱 시작 후 30초 대기 → health check → curl 실패 시, exit 1 실행하여 systemd가 재시작
SuccessExitStatus=143 # 종료 코드 143을 정상 종료로 간주
Restart=on-failure # 비정상 종료(0이 아닌 코드 값) 시 재시작
RestartSec=10 # 재시작 전 10초 대기 (연속 실패 방지)
StandardOutput=journal # 일반 출력을 journalctl로 전송
StandardError=journal # 에러 출력도 journalctl로 전송

[Install]
WantedBy=multi-user.target # 일반적인 서버 부팅 시 자동 시작
```

10. 빌드 파일 deploy 폴더로 이동

```bash
sudo mkdir -p /home/deploy/lucky-log

sudo cp build/libs/lucky-log-0.0.1-SNAPSHOT.jar /home/deploy/lucky-log/luckylog.jar
# luckylog.jar로 통일할 경우, systemd 서비스 파일 한 번만 설정(배포 스크립트 간단)
sudo chown deploy:deploy /home/deploy/lucky-log/luckylog.jar
```

```txt
/home/ec2-user/
└── lucky-log/ # Git 저장소, 빌드
    ├── src/
    ├── build/
    └── gradlew

/home/deploy/
└── lucky-log/
    └── lucky-log.jar # 실행 파일만
```

11. 도메인 설정

12. 포트 포워딩 설정

```bash
# 1. nginx 설치
sudo dnf install nginx -y

# 2. 설정 파일 작성
sudo nano /etc/nginx/conf.d/luckylog.conf

# 3. 문법 체크
sudo nginx -t

# 4. nginx 재시작
sudo systemctl restart nginx

# 5. 상태 확인
sudo systemctl status nginx
```

```nginx
server {
    listen 80; # 80번 포트(HTTP)로 들어오는 요청을 받음
    server_name lucky-log.duckdns.org; # 이 도메인으로 들어오는 요청만 처리

    location / { # 루트 경로(/) 및 모든 하위 경로에 대한 설정
        proxy_pass http://localhost:8080; # 들어온 요청을 localhost:8080으로 전달
        proxy_set_header Host $host; # 원래 요청 도메인(lucky-log.duckdns.org)를 헤더에 넣어 전달(안 하면 백엔드는 Host: localhost:8080으로 받음)
        proxy_set_header X-Real-IP $remote_addr; # 실제 클라이언트의 IP 주소를 전달
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; # 프록시 체인을 거친 모든 IP 주소를 기록
        proxy_set_header X-Forwarded-Proto $scheme; # 원래 요청이 http인지 https인지 알려줌
    }
}
```

13. https 설정

```bash
# 1. Certbot 설치
sudo dnf install certbot python3-certbot-nginx -y

# 2. SSL 인증서 발급
sudo certbot --nginx -d lucky-log.duckdns.org

# 3. 자동 갱신 테스트(인증서는 90일 유효)
sudo certbot renew --dry-run

# 4. 자동 갱신 타이머 확인
sudo systemctl status certbot-renew.timer
```

- Certbot이 자동으로 만들어주는 설정

```nginx
# before
server {
    listen 80;
    server_name lucky-log.duckdns.org;
    # ...
}

# after
server {
    listen 80;
    server_name lucky-log.duckdns.org;
    return 301 https://$server_name$request_uri;  # HTTP → HTTPS 리다이렉트
}

server {
    listen 443 ssl; # HTTPS 포트 + SSL 활성화
    server_name lucky-log.duckdns.org;

    ssl_certificate /etc/letsencrypt/live/lucky-log.duckdns.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lucky-log.duckdns.org/privkey.pem;

    location / {
        proxy_pass http://localhost:8080;
        # ...
    }
}
```

### GitHub Actions으로 CI/CD 구축하기

1. GitHub Actions에서 환경변수 관리

- GitHub 저장소 Settings > Secrets and variables > Actions에서 등록

2. workflow 작성

```yaml
# .github/workflows/deploy.yaml
name: CI/CD Pipeline # 워크플로우의 이름

on:
  push:
    branches:
      - main

jobs:
  test: # Job의 고유 ID
    name: Run Tests
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4 # GitHub 저장소의 코드를 가상 환경으로 pull

      - name: Set up JDK 17 # Java 환경 설정
        uses: actions/setup-java@v4 # GitHub Actions에서 제공하는 사전 제작된 액션(Action)을 사용
        with:
          java-version: '17'
          distribution: 'corretto'
          cache: 'gradle' # Gradle 캐싱 추가 (빌드 속도 향상 🚀)

      - name: Make gradlew executable
        run: chmod +x ./gradlew

      - name: Run tests
        run: ./gradlew test # /test/resource/application.yaml을 사용하므로 profile 지정 X

  build:
    name: Build Application
    needs: test # test Job이 성공해야만 실행(의존성)
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17 # 가상 환경에 Java(JDK)를 설치하고 설정해주는 작업
        uses: actions/setup-java@v4
        with:
          java-version: '17'
          distribution: 'corretto'
          cache: 'gradle'

      - name: Create application-prompts.yaml
        run: | # |: 여러 줄의 문자열(줄바꿈 유지)
          cat > src/main/resources/application-prompts.yaml << 'EOF'
          ${{ secrets.APPLICATION_PROMPTS_YAML }}
          EOF

      - name: Make gradlew executable
        run: chmod +x ./gradlew

      - name: Build (without tests)
        run: ./gradlew clean build -x test

      - name: Upload JAR
        uses: actions/upload-artifact@v4
        # 빌드된 JAR 파일을 GitHub Actions 아티팩트로 저장
        # 다음 Job(deploy)에서 이 파일을 다운로드하여 사용
        with:
          name: app-jar
          path: build/libs/*.jar
          retention-days: 1 # 아티팩트 보관 기간

  deploy:
    name: Deploy to EC2
    needs: build # 빌드 성공해야 배포 시작
    runs-on: ubuntu-latest

    steps:
      - name: Download JAR
        uses: actions/download-artifact@v4
        with:
          name: app-jar

      - name: Deploy to EC2
        uses: appleboy/scp-action@v0.1.7
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          source: '*.jar'
          target: '/tmp/'
          # EC2의 임시 폴더 /tmp/로 전송

      - name: Restart Service
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            echo "📦 Deploying JAR file..."
            sudo mv /tmp/*.jar /home/deploy/lucky-log/luckylog.jar
            sudo chown deploy:deploy /home/deploy/lucky-log/luckylog.jar

            echo "🔄 Restarting service..."
            sudo systemctl restart luckylog

            # Health check
            echo "⏳ Waiting for application to start..."
            for i in {1..20}; do
              if curl -s -f http://localhost:8080/actuator/health; then
                echo "✅ Deployment successful!"
                exit 0
              fi
              echo "Health check attempt $i failed. Retrying in 5 seconds..."
              sleep 5
            done

            echo "❌ Health check failed!"
            echo "=== 마지막 50줄 로그 ==="
            sudo journalctl -u luckylog -n 50  # 에러 로그 출력
            exit 1
```

```txt
코드 push (main 브랜치)
    ↓
① Test Job 실행
    - 환경 설정
    - 테스트 실행
    ↓ (성공 시)
② Build Job 실행
    - 환경 설정
    - 설정 파일 생성
    - JAR 파일 빌드
    - 아티팩트 업로드
    ↓ (성공 시)
③ Deploy Job 실행
    - JAR 다운로드
    - EC2로 파일 전송
    - 서비스 재시작
    - 헬스체크
    ↓
배포 완료!
```

- GitHub Actions의 Job들은 서로 독립적

  - `build` Job과 `deploy` Job은 완전히 다른 가상 환경(컴퓨터)에서 실행
  - Artifact = "Job 간에 파일을 전달하기 위한 GitHub Actions 임시 저장소"

- t2.micro (1GB RAM)이므로 빌드에 시간이 오래 걸림
  - 그러므로, CI 빌드 후 파일만 EC2 서버에서 실행

### Grafana Loki

- 로그 집계(log aggregation) 시스템
- 주요 구성 요소

  - Promtail: 로그 수집 에이전트 (로그 파일을 읽어 Loki로 전송)
  - Loki: 로그를 저장하고 조회할 수 있게 해주는 데이터베이스
  - Grafana: 로그 시각화 및 검색 UI

- t2.micro 스펙
  - RAM: 1GB (실제 사용 가능 ~900MB)
  - Spring Boot(~400MB)
  - Loki(~200MB) + Promtail(~50MB) + Grafana(~150MB)  
    → 스왑 메모리 설정 필요

`free -h`

- 시스템의 메모리 사용량을 확인

```bash
$ free -h
        total   used    free   shared  buff/cache   available
Mem:    949Mi   369Mi   239Mi  0.0Ki   340Mi        440Mi
Swap:   0B      0B      0B

# Mem (메모리)
# total: 전체 물리 메모리
# used: 실제 사용 중인 메모리
# free: 완전히 사용되지 않은 메모리
# shared: 공유 메모리(일반적으로 각 프로그램은 자기만의 메모리 공간을 가지지만, shared 메모리는 여러 프로그램이 동시에 접근할 수 있음)
# buff/cache: 버퍼와 캐시로 사용되는 메모리
# available: 실제로 사용 가능한 메모리 (캐시 포함)

# Swap (스왑)
# 디스크를 메모리처럼 사용하는 가상 메모리 영역
```

#### 1. 스왑 메모리 생성

```bash
# 1. 스왑 파일 생성(4GB)
sudo dd if=/dev/zero of=/swapfile bs=128M count=32

# 2. 권한 설정
sudo chmod 600 /swapfile

# 3. 스왑 활성화
sudo mkswap /swapfile
sudo swapon /swapfile

# 4. 재부팅 후에도 유지
echo '/swapfile swap swap defaults 0 0' | sudo tee -a /etc/fstab

# 5. 확인
free -h
        total    used     free    shared    buff/cache   available
Mem:    949Mi    369Mi    239Mi   0.0Ki     340Mi        440Mi
Swap:   4.0Gi    0B       4.0Gi
```

#### 2. Docker 설치

```bash
# Amazon Linux 2023
# 1. Docker v2 설치
sudo dnf install -y docker

# 2. Docker 시작
sudo systemctl start docker
sudo systemctl enable docker

# 3. ec2-user에게 Docker 권한 주기
# Docker 데몬은 /var/run/docker.sock 유닉스 소켓을 통해 통신
# 이 소켓 파일은 기본적으로 root 사용자와 docker 그룹만 접근 가능
sudo usermod -a -G docker ec2-user

# 4. 현재 세션에 권한 적용
newgrp docker

# 5. Docker Compose 설치
sudo dnf install -y docker-compose-plugin
# docker compose v2 (플러그인 방식) 사용 권장

# 6. 실행 권한 추가
# curl로 다운로드한 파일은 실행 권한이 없어서 필요
# sudo chmod +x /usr/local/bin/docker-compose

# 7. 설치 확인
docker --version
# Docker version 25.0.13, build 0bab007
docker compose version
# Docker Compose version v2.40.3
```

#### 3. Loki 설치

```bash
# 1. 작업 디렉토리 생성
mkdir -p ~/loki/promtail
cd ~/loki

# 2. docker-compose.yml 생성
# 로그 수집 및 저장 시스템
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  loki: # 이 이름을 주소로 사용(같은 서버 내에서 사용 가능)
    image: grafana/loki:2.9.0
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - loki-data:/loki
    mem_limit: 180m # 최대 180MB까지만 사용 가능
    mem_reservation: 120m # 최소 120MB는 보장받으려고 시도
    restart: unless-stopped

  promtail:
    image: grafana/promtail:2.9.0
    volumes:
      # 호스트 경로 : 컨테이너 경로 : 옵션
      - /home/deploy:/home/deploy:ro
        # 호스트: /home/deploy (EC2 서버의 시스템 로그)
        # 컨테이너: /home/deploy (Promtail 컨테이너 안에서 보이는 경로)
        # :ro: read-only (읽기 전용 - 수정 불가)
      - ./promtail/config.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml
    depends_on:
      - loki # Loki가 먼저 시작된 후 Promtail 시작
    mem_limit: 80m
    mem_reservation: 50m
    restart: unless-stopped # 서버 재부팅 시 자동 시작

  grafana:
    image: grafana/grafana:11.3.0
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=password_입력
    volumes:
      - grafana-data:/var/lib/grafana # 컨테이너 재시작해도 대시보드 설정 유지
      # grafana-data라는 볼륨을 컨테이너의 /var/lib/grafana에 연결
    depends_on:
      - loki
    mem_limit: 256m
    mem_reservation: 128m
    restart: unless-stopped

volumes:
  loki-data:
  grafana-data: # 컨테이너 재시작해도 대시보드 설정 유지
  # grafana-data라는 이름의 볼륨 만들기(EC2(호스트)에 저장 공간 생성)
EOF

# 3. Promtail 설정 파일 생성
cat > promtail/config.yml << 'EOF'
server:
  http_listen_port: 9080 # Promtail 상태 확인용 포트
  # 브라우저에서 http://서버주소:9080/metrics 접속하면 상태 볼 수 있음
  grpc_listen_port: 0
  # grpc: 프로그램끼리 통신하는 방법 중 하나, 0=사용하지 X
  # Promtail → Loki는 HTTP로 전송하면 충분
  # gRPC는 필요 없으니까 끔(포트 절약, 리소스 절약)

positions:
  filename: /tmp/positions.yaml # 로그 파일 어디까지 읽었는지 기록하는 파일 위치

clients:
  - url: http://loki:3100/loki/api/v1/push # Loki로 전송
  # http://loki:3100: Docker 컨테이너 이름
  # Docker가 자동으로 `loki`를 같은 서버의 Loki 컨테이너로 연결해줌

scrape_configs:
  - job_name: springboot # 수집 작업의 이름표
    static_configs:
      - targets:
          - localhost # 지금 Promtail이 실행 중인 서버
        labels: # 로그를 분류하고 검색할 때 사용
          job: springboot # 어떤 작업
          app: luckylog # 어떤 앱
          __path__: /home/deploy/logs/luckylog/*.log # luckylog 폴더의 모든 .log 파일 읽기
EOF

# 4. 설정 파일 확인
cat docker-compose.yml
cat promtail/config.yml
```

- 동작 방식
  - 애플리케이션  
    → 로그 파일 생성  
    → Promtail이 로그 파일 읽기 (/var/log, /home/deploy)  
    → Loki로 전송 (포트 3100)  
    → Loki에 저장 (loki-data 볼륨)  
    → Grafana 등으로 조회 가능

#### 4. AWS 보안그룹 설정

- EC2의 3000번 포트를 열어야 Grafana에 접속할 수 있음
- EC2 인스턴스 - 보안 - 보안그룹 - 인바운드 규칙 편집
  - 규칙 추가
    - 유형: 사용자 지정 TCP
    - 포트 범위: 3000
    - 소스: 내 IP(IP 고정 시)
    - 설명: Grafana Web UI

#### 5. Docker Compose 실행

```bash
# Docker Compose 실행
docker compose up -d

# 상태 확인
docker compose ps
# NAME      IMAGE                        STATUS
# loki      grafana/loki:2.9.0           Up
# promtail  grafana/promtail:2.9.0       Up
# grafana   grafana/grafana:11.3.0       Up

# 메모리 사용량
docker stats --no-stream

CONTAINER ID   NAME              CPU %     MEM USAGE / LIMIT   MEM %     NET I/O           BLOCK I/O        PIDS
f6bb1514c186   loki-promtail-1   0.21%     21.16MiB / 80MiB    26.46%    2.95kB / 13.8kB   2.39MB / 770kB   6
a8166ded3d8d   loki-loki-1       0.18%     56.45MiB / 180MiB   31.36%    15.2kB / 1.71kB   30.4MB / 201kB   6

# Promtail 로그 확인 (로그 파일 잘 읽는지 체크)
docker compose logs promtail | tail -30

promtail-1  | ts=2025-11-17T11:40:53.075847665Z caller=log.go:168 level=info msg="Seeked /home/deploy/logs/luckylog/luckylog-2025-11-11.0.log - &{Offset:0 Whence:0}"
promtail-1  | level=info ts=2025-11-17T11:40:53.07633742Z caller=tailer.go:145 component=tailer msg="tail routine: started" path=/home/deploy/logs/luckylog/luckylog-2025-11-11.0.log
# Promtail이 로그 파일들을 찾아서 읽기 시작했다는 메시지
# Seeked 메시지: 로그 파일의 읽기 시작 위치를 찾음, Offset:0 Whence:0 = 파일 처음부터 읽기 시작
# tail routine: started: 해당 파일을 추적(tail) 시작, 새로운 로그가 추가되면 실시간으로 읽어서 Loki로 전송
```

#### 6. Grafana 접속

- `http://EC2-IP:3000`
- Username: admin
- Password: password

#### 7. Grafana에서 Loki 연결

- Add data source
- loki
  - HTTP 섹션
    - URL: `http://loki:3100`
  - Save & Test
    - Data source successfully connected. 문구 확인

#### 8. 로그 확인하기

- Explore
  - 상단 데이터소스에서 Loki 선택
  - label filters: job, springboot
  - run query

#### 9. 대시보드 만들기

- 시간당 로그 발생량
  - create dashboard
  - Add visualization
  - 데이터소스: Loki
  - Code 쿼리: `sum(count_over_time({job="springboot"}[1h]))`
    - run queries
  - Title: 시간당 로그 발생량
  - Visualization: Time series
  - Time range: Last 30days
  - apply
- 최근 경고/에러
  - Code 쿼리: `{job="springboot"} |~ "WARN|ERROR"`
  - Visualization: **Logs** 또는 **Table**
  - Title: 최근 경고/에러
  - apply
- save dashboard

### 📚 참고

- [AWS 교과서](https://product.kyobobook.co.kr/detail/S000210532528)
- [SpringBoot 프로젝트 EC2 배포하기](https://velog.io/@jonghyun3668/SpringBoot-%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-EC2-%EB%B0%B0%ED%8F%AC%ED%95%98%EA%B8%B0)
- [[aws] EC2 Public instance(EIP) 생성 및 연결](https://minjii-ya.tistory.com/21)
- [내 도메인을 만들어보자!](https://co-de.tistory.com/69)
- [[AWS] 프리티어 RDS PostgreSQL DB생성과 연결하기](https://coasis.tistory.com/77)
