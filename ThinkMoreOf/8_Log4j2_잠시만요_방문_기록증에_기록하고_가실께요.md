# 8_Log4j2_잠시만요_방문_기록증에_기록하고_가실께요
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2024-01-05
- 수정일: 2024-01-08

<br/>



#
### 주제를 선정한 이유
최근에 [실전! 스프링 부트와 JPA 활용1 - 웹 애플리케이션 개발](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81%EB%B6%80%ED%8A%B8-JPA-%ED%99%9C%EC%9A%A9-1/dashboard)를 완강하였습니다.  
계획대로라면 JPA 기본 강의를 들어야하는데, 강의만 듣고 혼자서 처음부터 따라해보는 것도 중요하다고 판단해서 강의 노트를 보며 코드를 다시 작성하고 있습니다.  
강의에서 잠깐 로그 기록 관련해서 짧게 Logback, Log4j를 언급하셨는데, 처음으로 로그 관리를 해보기 위해 이 글을 작성하게 되었습니다.

<br/>

#
### Log를 남겨야 하는 이유
로그가 없으면 모니터링이 불가능하고, 사고가 발생했을 때 원인을 분석할 수 없습니다. 따라서 로그를 남기는 것은 시스템의 안정성과 문제 해결에 매우 중요한 역할을 합니다.  

이때, System.out.println()을 사용하지 않는 이유는
- newline()에서 동기화를 진행하는데 multi-thread 간의 Blocking 작업이 일어나고,
- System.out은 콘솔에 출력되기 때문에 별도로 파일로 저장하여 관리하기가 힘들기 때문입니다.

<br/>



#
### Log의 역할
사용자가 서비스를 이용할 때 기록할 수 있는 데이터는 크게 
- 서비스 로그
    - Transaction 결과에 대한 정보
    - 가입, 등록, 결제와 같이 서비스가 정상적으로 돌아가기 위해 필요한 이력이 시스템에 기록
- 행동 로그
    - 사용자가 어떤 페이지 및 정보를 보거나, 특정 버튼을 누르거나, 스크롤을 넘기는 등의 행동을 할 때 관련 정보를 저장

가 있습니다.  
저는 서비스 운영이 목적이 아니므로, 서비스 로그를 Spring Boot에서 서비스 로그를 기록하는 방법에 대해 정리할 예정입니다.  

<br/>



#
### Spring Boot에서 Logger 설정하기
Spring Boot에서 Logger는
1. Log4j
2. Logback
3. Log4j2

가 있는데, Spring boot Starter에 기본적으로 Logback이 설정되어 있습니다.  

Log4j2는 Logback에 비해 더 빠르고 자바의 람다식을 활용할 수 있는 메소드도 정의되어 있기 때문에, 기존의 Logback을 Log4j2로 바꾸도록 하겠습니다.

cf. Logging Library
시스템에서 제공하는 원하는 정보를 기록하여서 일련의 파일에 누적시켜 추후에 확인을 목적으로 사용되는 라이브러리

<br/>

---

1. Log4j2 의존성 추가

```html
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-log4j2")
}
```

2. Logback 제거
Spring에서는 기본적으로 Logback을 이용해서 로깅을 하므로 다른 로깅 라이브러리를 추가하면, 로깅 라이브러리 간 충돌이 발생합니다.  
그러므로 Logback 라이브러리를 제거하도록 하겠습니다.

```html
configurations {
    all {
        exclude group: 'org.springframework.boot', module: 'spring-boot-starter-logging'
    }
}
```

3. application.yml에 log4j2.xml 파일 경로 추가
application.yml 파일에서 직접 log4j2에 대한 설정을 할 수 있지만, 파일이 복잡해질 수 있으므로 따로 log4j2.xml 파일을 만들어 application.yml에 classpath를 추가해주도록 하겠습니다.

```html
# log4j2.xml 파일 경로 설정
logging:
  config: classpath:log4j2.xml
```

4. log4j2.xml 파일 설정

```html
<?xml version="1.0" encoding="UTF-8"?>
<Configuration status="DEBUG">
    <Properties>
        <Property name="logPath">./logs</Property>
        <Property name="logPattern">[%-5level] %d{yyyy-MM-dd HH:mm:ss} [%t] %c{1} - %msg%n</Property>
        <Property name="serviceName">application</Property>
    </Properties>
    <Appenders>
        <Console name="console">
            <PatternLayout pattern="${logPattern}"/>
        </Console>
        <RollingFile
                name="file"
                append="true"
                fileName="${logPath}/${serviceName}.log"
                filePattern="${logPath}/${serviceName}.%d{yyyy-MM-dd}.%i.log.gz">
            <PatternLayout pattern="${logPattern}"/>
            <Policies>
                <SizeBasedTriggeringPolicy size="5MB"/>
                <TimeBasedTriggeringPolicy/>
            </Policies>
            <DefaultRolloverStrategy>
                <Delete basePath="${logPath}" maxDepth="1">
                    <IfFileName glob="${serviceName}.*.log"/>
                    <IfLastModified age="15d"/>
                </Delete>
            </DefaultRolloverStrategy>
        </RollingFile>
    </Appenders>
    <Loggers>
        <Logger name="todowork" level="info" additivity="false">
        <!--name=build.gradle의 group명-->
            <AppenderRef ref="console"/>
            <AppenderRef ref="file"/>
        </Logger>
        <Root level="info">
            <AppenderRef ref="console"/>
        </Root>
    </Loggers>
</Configuration>
```

- Configuration status
    - 로깅 프레임워크 자체의 로그 수준
    - Log Level: Trace < Debug < Info < Warning < Error < Fatal
    - 로그 수준이 INFO라면 INFO 이상의 중요도를 갖는 로그들만 찍힘

- Properties
    - Property
        - logPath: log 파일 저장 위치
        - logPattern: 

- Appenders
    - 각 Appender는 로그 메시지를 어디에, 어떻게 기록할지를 정의
    - Console
        - 콘솔에 로그를 출력하는 appender
        - PatternLayout: 출력되는 로그 형식 정의
    - RollingFile
        - 파일에 로그를 기록하는 appender
        - 파일의 크기 또는 시간에 따라 새로운 파일을 생성
        - append: 기존 파일에 로그를 추가할 것인지 여부
        - fileName: 로그 파일의 경로와 이름
        - filePattern: 새롭게 생성될 로그 파일의 이름 패턴
        - PatternLayout: 파일에 기록될 로그의 형식을 정의
        - Policies
            - rolling file의 행동을 결정하는 정책
            - SizeBasedTriggeringPolicy: 파일 크기에 따라 새로운 파일로 롤오버
            - TimeBasedTriggeringPolicy: 시간 기반으로도 파일을 롤오버
        - DefaultRolloverStrategy
            - rolling file이 일어날 때 사용할 기본 롤오버 전략 정의
            - Delete basePath: 일정 조건에 따라 로그 파일을 삭제하는 전략 설정
            - IfFileName glob: 특정 파일명 패턴에 따라 파일 삭제
            - IfLastModified age: 파일의 마지막 수정일 기준으로 파일 삭제

- Loggers
    - 로그 레벨과 로깅 이벤트를 특정 appender에 연결하는 것을 설정
    - name: 로거가 적용되는 패키지 이름을 지정
        - ⭐프로젝트 내의 로그가 출력되지 않는 경우,  
        build.gradle 파일 내에 group 속성값을 추가
    - level: 특정 Logger 인스턴스가 기록할 메시지의 수준, 실제 애플리케이션의 동작과 관련된 로그를 필터링하는 데 사용
    - additivity: 상위 로거로 로그 전파 여부
    - AppenderRef
        - ref="console": 이 로거에 콘솔 appender를 참조, 이 패키지의 로그는 콘솔에 출력
        - ref="file": 이 로거에 파일 appender를 참조, 이 패키지의 로그는 파일에 기록
    - Root
        - Root logger 설정, 다른 모든 로거의 기본 설정을 제공
        - 루트 로거는 'console' Appender를 통해 info 이상의 로그를 출력

```html
<!-- Spring 관련 로그  -->
<Logger name="org.springframework" additivity="false" level="INFO">
    <AppenderRef ref="Console_Appender"/>
    <AppenderRef ref="File_Info_Appender"/>
    <AppenderRef ref="File_Error_Appender"/>
</Logger>
```

- 결과

```java
@RestController
@Log4j2
public class TestController {
    @GetMapping("/log")
    public void logTest() {
        log.info("Hello. This is Lombok's logger");

        log.fatal("FATAL");
        log.error("ERROR");
        log.warn("WARN");
        log.info("INFO");
        log.debug("DEBUG");
        log.trace("TRACE");
    }
}
```

```bash
# application.log file
# logger level을 info로 설정하여 info보다 낮은 단계인 debug와 trace는 기록되지 않음

[INFO ] 2024-01-07 12:14:44 [http-nio-8080-exec-2] TestController - Hello. This is Lombok's logger
[FATAL] 2024-01-07 12:14:44 [http-nio-8080-exec-2] TestController - FATAL
[ERROR] 2024-01-07 12:14:44 [http-nio-8080-exec-2] TestController - ERROR
[WARN ] 2024-01-07 12:14:44 [http-nio-8080-exec-2] TestController - WARN
[INFO ] 2024-01-07 12:14:44 [http-nio-8080-exec-2] TestController - INFO

```

<br/>



#
### 📚참고 자료
[log를 남겨야 하는 이유](https://yozm.wishket.com/magazine/questions/share/4V05WlMtiVoqgtUY/)  
[사용자 행동 로그, 파종부터 수확까지 | 잘 쌓기 — 1편](https://medium.com/@connect2yh/%EC%82%AC%EC%9A%A9%EC%9E%90-%ED%96%89%EB%8F%99-%EB%A1%9C%EA%B7%B8-%ED%8C%8C%EC%A2%85%EB%B6%80%ED%84%B0-%EC%88%98%ED%99%95%EA%B9%8C%EC%A7%80-%EC%9E%98-%EC%8C%93%EA%B8%B0-1%ED%8E%B8-9733422dd00d)  
[Spring Boot Log4j2 설정하기](https://medium.com/@201924576/spring-boot-log4j2-%EC%84%A4%EC%A0%95-21f3b6da38c6)  
[[Java/Library] Slf4j - Log4j2 이해하고 설정하기](https://adjh54.tistory.com/74)
