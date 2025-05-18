### Gradle Wrapper
* 설치한 적 없는 Gradle이 Spring Boot에서 동작하는 이유
* Spring Boot 프로젝트는 보통 Gradle Wrapper(gradlew)를 포함
* Gradle이 로컬에 설치되어 있지 않아도, 필요한 버전을 자동으로 다운로드해서 실행할 수 있게 해줌

```bash
# Gradle Wrapper: 프로젝트 안에 자동 생성되는 다음 파일들
gradlew # 유닉스/맥용 실행 파일
gradlew.bat # Windows용 실행 파일
/gradle/wrapper/gradle-wrapper.jar 
# 이 JAR 파일이 실제 Gradle 다운로드 및 실행을 담당
# gradlew나 gradlew.bat이 이 파일을 이용해 동작
/gradle/wrapper/gradle-wrapper.properties
# Gradle이 어떤 버전을 사용할지, 그리고 어디서 다운로드할지를 정의하는 설정 파일
# gradlew 실행 시 이 파일을 읽고, properties에 지정된 URL에서 지정된 버전의 Gradle을 다운로드해서 사용
```

>실행 순서
1. 사용자가 gradlew 또는 gradlew.bat 실행
2. gradle-wrapper.properties 확인
3. 필요한 Gradle 버전이 없다면 gradle-wrapper.jar가 자동 다운로드
4. 해당 Gradle 버전으로 프로젝트 빌드

```bash
# Gradle Wrapper와 프로젝트 구조
my-springboot-app/
├── build.gradle
├── gradlew
├── gradlew.bat
├── gradle/
│   └── wrapper/
│       ├── gradle-wrapper.jar
│       └── gradle-wrapper.properties
```

장점
1. 자동으로 버전이 관리되어, 모든 개발자가 같은 Gradle 버전 사용할 수 있음
2. Gradle의 로컬 설치가 불필요(시스템에 설치 안 해도 빌드 가능)
3. Jenkins, GitHub Actions 등 CI/CD에서 안정적 빌드할 수 있음
  * Gradle Wrapper는 CI/CD 환경에서도 항상 동일한 버전의 Gradle을 보장하므로, 설치 유무나 환경 차이 걱정 없이 안정적인 빌드가 가능



### Gradle
Java 같은 언어로 만든 프로젝트를 자동으로 빌드(compile, test, 패키징 등)해주는 도구
* 사용 이유
Java 프로젝트에 필요한 작업: 코드 컴파일, 라이브러리(외부 의존성) 다운로드, 테스트 실행, JAR/WAR 파일 생성, 서버 실행
→ 수동으로 하기엔 너무 번거롭고 복잡하므로 Gradle을 사용해서 자동으로 처리

| 작업            | 설명                                              |
| -------------- | --------------------------------------------------|
| `dependencies` | 외부 라이브러리 가져오기 (예: Spring Boot, JUnit 등) |
| `build`        | 컴파일 + 테스트 + JAR 파일 생성                     |
| `bootRun`      | Spring Boot 앱 실행                                |
| `test`         | 테스트 코드 실행                                    |

#### 컴파일 (Compile)
Java 소스코드(.java)를 JVM이 실행할 수 있는 바이트코드(.class)로 변환하는 과정
#### JAR(Java Archive) 파일
.class 파일, 설정파일, 라이브러리 등을 하나의 압축 파일처럼 묶은 것  
실행 가능한 애플리케이션으로 만들기 위해 필요  
JVM은 .jar 파일을 통해 프로그램을 실행할 수 있음(`java -jar`)

1. Compile: `.java` → `.class` 변환      |
2. Process: `application.yml` 같은 설정 복사
3. Test: 단위 테스트 실행
4. Package: `.class`, 리소스를 JAR로 묶음 
5. 결과물: `build/libs/`에 `.jar` 생성

