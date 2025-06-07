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

#### Gradle vs Maven
| 항목  | Gradle               | Maven      |
| ----- | -------------------- | ---------- |
| 설정  | Groovy/Kotlin DSL    | XML        |
| 속도  | 빠름 (캐시, 병렬 빌드) | 비교적 느림 |
| 가독성 | 간결함               | 장황함      |
| 유연성 | 높음                 | 중간       |


### Spring Initializer
![spring initializer](./images/springboot-initializer.png)
* Group
  * 회사나 조직의 도메인(com.naver)
  * Java의 패키지 네임스페이스처럼 사용됨
  * 명명 규칙
    * 영어 소문자만 사용
    * 숫자 사용 가능 (단, 숫자로 시작하면 안 됨)
    * 하이픈(-)은 허용되지 않음
* Artifact
  * 프로젝트의 고유 이름(com.naver.shopping)
  * 빌드 결과물 이름에도 반영
  * 명명 규칙
    * 하이픈(-) 사용 가능
      * 단, package name에는 하이픈(-) 사용 불가
* Name
  * 프로젝트의 이름 (기본값은 artifact와 동일)
* Package Name
  * 기본값은 group + artifact 조합
* Packaging: JAR vs WAR
  * JAR(Java ARchive)
    * Spring Boot 기본 실행 방식
    * 내장 톰캣 포함되어있음
    * java -jar 명령으로 바로 실행 가능
  * WAR(Web Application Archive)
    * 전통적인 방식 (Java EE 환경)
    * 서버(톰캣, WebLogic 등)에 올려야 실행됨

#### 서버(톰캣)에 올리는 방식
1. WAR 파일을 만든다
2. 웹 서버가 설치된 컴퓨터에 복사한다
3. 톰캣의 webapps/ 폴더에 WAR 파일을 넣는다
4. 톰캣 서버를 실행하면 WAR가 실행된다.  
(톰캣이 WAR를 읽고 웹사이트를 열어줌)



### Multi Module Project
자바에서 모듈(Module)은 독립적으로 배포될 수 있는 코드의 단위
멀티 모듈이란 서로 독립적인 프로젝트(인증, 어플리케이션)를 하나의 프로젝트로 묶어 모듈로서 사용되는 구조
* 사용 이유: 일정 수준 이상의 트래픽을 감당하려면 사용자와의 접점을 담당하는 서버(이하 web프로젝트), DB와의 접점을 담당하는 서버(이하 API 프로젝트)로 구분하여 구성
![architecture](./images/springboot-architecture.png)
Member클래스를 공통으로 사용할 때, 한 프로젝트에서 Member 클래스파일을 생성하고 이를 다른 프로젝트에서 코드를 복사하는 방식은 가장 간단하지만 연동되는 프로젝트가 늘어날 경우, 혹은 Member 클래스의 코드에 수정이 필요할 경우에 정말 많은 양을 수정해야하고 실수할 여지가 많아짐  
⭐ 하나의 공통 프로젝트를 두고, 이 프로젝트를 여러 프로젝트에서 가져가서 사용
  * 사용 조건
    1. 개발시에는 바로바로 공통 프로젝트 코드를 사용할 수 있어야 한다.
    2. 빌드시에는 자동으로 공통 프로젝트가 포함되어야 한다.

#### Multi Module Project 만들기
* Root Project는 모듈을 담는 프로젝트로 src가 필요 X
* Root Project settings.gradle 파일에 하위 모듈이 include되어있는지 확인


### Could not resolve all files for configuration ':buy-me-common:compileClasspath'
* 하위 프로젝트의 build.gradle 파일에 org.springframework.boot 플러그인과 io.spring.dependency-management 플러그인이 누락되어 의존성 버전을 제대로 가져오지 못해 발생하는 오류  
▶ 하위 프로젝트에서도 스프링 부트의 의존성을 사용하려면 이러한 플러그인 설정이 필요
```json
// root
allprojects {
	group = 'com.comeus'
	version = '0.0.1-SNAPSHOT'

	repositories {
		mavenCentral() // 외부 라이브러리 받을 저장소 설정
	}
}

subprojects {
	apply plugin: 'java'
	apply plugin: 'io.spring.dependency-management'

	java {
		toolchain {
			languageVersion = JavaLanguageVersion.of(17) // 어떤 자바 버전으로 빌드할지 지정
		}
	}

	dependencyManagement {
		imports {
			mavenBom "org.springframework.boot:spring-boot-dependencies:3.4.5"
			// dependency-management 플러그인은 Spring Boot의 BOM을 직접 알지 못함
			// spring-boot-dependencies BOM은 org.springframework.boot 플러그인이 자동으로 설정
			// dependency-management 플러그인만 적용하면 BOM을 직접 import
			// * BOM:라이브러리들의 버전 목록
		}
	}
}
```
최상위 프로젝트에서 전체 프로젝트/하위 프로젝트에 적용할 설정을 전역으로 선언  
진짜 자바 코드가 있는 하위 모듈에만 java 플러그인을 적용


### 상위 프로젝트의 spring-boot-starter dependency를 못 읽어오는 오류
```json
dependencies {
    implementation project(':web')
}
```
* Gradle의 implementation은 **전이적(transitive)**이지만, 항상 완전히 동작하는 건 아님
* `@SpringBootApplication`은 Spring Boot의 많은 자동 설정 기능을 쓰기 위한 핵심 애노테이션인데, 그 기반이 되는 자동 구성 메타정보는 직접 선언된 의존성을 통해서만 완전히 인식될 수 있음

### Gradle option
Gradle에서 Java 프로젝트를 빌드하려면 기본적으로 java 플러그인이 필요  
java 플러그인을 통해 컴파일, 테스트, jar 파일 생성 등의 작업들(tasks)이 수행 가능
```json
plugins {
    id 'java'
}
```

클래스 패스(class path): 자바로 작성된 프로그램을 컴파일(compile: .java → .class)하고 실행(run)할 때 특정 경로에서부터 시작하여 클래스 파일과 패키지를 탐색
* Compile classpath: Java 코드를 class 파일로 컴파일 할 때 탐색하는 경로
* Runtime classpath: 컴파일된 자바 코드(class 파일)을 JVM이 실행할 때 탐색하는 경로

컴파일 시점에만 필요로 하는 의존성도 있고, 실행 시점에만 필요로 하는 의존성도 있음  
→ 그래서 Gradle에서 의존성(dependency)를 추가할 때 어느 범위로 노출시킬 것인지 결정할 수 있도록 도와준다.

complieOnly
* 컴파일 경로에만 설정
* 빌드 결과물의 크기가 줄어드는 장점
runtimeOnly
* 런타임 경로에만 설정
* 해당 클래스에서 코드 변경이 발생해도 컴파일을 다시 할 필요가 없음
implementation, api
* 두 경로에 모두 설정
* api는 Java-Library 플러그인 추가 필요
* implementation으로 설정된 의존성은 전이되지 않으며, 해당 모듈 내부에서만 사용
  * implementation로 설정된 의존성은 다른 모듈의 컴파일 클래스 경로에 포함되지 않으며, 이로 인해 라이브러리를 제공하는 측에서 의존성을 변경하더라도, 사용하는 측은 재컴파일하지 않아도 됨  
  이를 통해 컴파일 시간을 단축하고 재빌드 빈도를 줄일 수 있는 이점을 얻을 수 있음
  * runtime이 deprecated 되고 나온 것은 implementation
* api로 설정된 의존성은 전이되어 다른 모듈의 컴파일 클래스 경로(compileClasspath)에도 추가
  * 예를 들어, 현재 모듈이 httpclient 라이브러리를 사용하고 있다면, 이 모듈을 의존하는 다른 모듈도 자동으로 httpclient 라이브러리를 사용할 수 있게 됨
  * compile이 deprecated 되고 나온 것이 api

예시
* 모듈 B가 모듈 A를 api로 의존 + 모듈 C가 모듈 B를 api로 의존: 모듈 C에서 모듈 A의 클래스를 사용할 수 있음
* 모듈 B가 모듈 A를 api로 의존 + 모듈 C가 모듈 B를 implementation으로 의존: 모듈 C에서 모듈 A의 클래스를 사용할 수 있음
* 모듈 B가 모듈 A를 implementation으로 의존 + 모듈 C가 모듈 B를 api로 의존: 모듈 B에서 모듈 A의 클래스를 사용할 수 있지만, 모듈 C에서는 사용할 수 없음

권장
* Gradle은 가능한 implementation을 사용하는 것을 권장하는데, api는 의존성이 다른 모듈에 전이되지만 implementation은 해당 모듈 내부에서만 사용되고 다른 모듈에는 노출되지 않기 때문
* 무분별하게 api를 사용하기보다는 상황에 맞게 implementation을 사용하여 의존성을 캡슐화하고, 이를 통해 컴파일 시간을 단축하여 재빌드 빈도를 줄일 수 있는 이점을 얻는 것이 좋음
  * 해당 모듈에서만 사용하는 경우 implementation을 사용하고, 다른 모듈에서도 함께 사용할 경우 api를 사용


<br/>

### 📚 참고
[Gradle 멀티 프로젝트 관리](https://jojoldu.tistory.com/123)  
[[gradle] implementation, api 차이](https://dkswnkk.tistory.com/759)  
[[Gradle] Gradle Java 플러그인과 implementation와 api의 차이](https://mangkyu.tistory.com/296)