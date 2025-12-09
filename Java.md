### ArrayDeque vs ArrayList

- ArrayDeque

  - Queue/Stack 용도: FIFO/LIFO 방식으로 데이터 처리
  - 양쪽 끝 조작이 빈번: 앞/뒤에서 추가/제거가 많은 경우
  - 순서대로 처리해야 하는 대기열, 작업 큐, 이벤트 큐 등의 경우

- ArrayList

  - 인덱스 접근: list.get(5) 같은 임의 위치 접근이 필요
  - 리스트의 끝에서 데이터를 추가하거나 제거하는 작업이 대부분일 때
  - 정렬/검색: Collections.sort(), indexOf() 등 사용

- LinkedList
  - 중간 삽입/삭제가 잦을 때

### equals(), hashCode()

- HashMap/HashSet 쓰거나 값이 같으면 같은 것으로 취급하고 싶으면 오버라이드 필수

```java
class Product {
    private String id;
    private String name;

    Product(String id, String name) {
        this.id = id;
        this.name = name;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;

        Product product = (Product) obj;
        return Objects.equals(id, product.id);  // id만으로 동일성 판단
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);  // equals()와 같은 필드 사용!
    }
}

HashSet<Product> set = new HashSet<>();
set.add(new Product("A001", "노트북"));
set.add(new Product("A001", "노트북"));

System.out.println(set.size());  // 1

HashMap<Product, Integer> stock = new HashMap<>();
Product laptop = new Product("A001", "노트북");
stock.put(laptop, 10);

Product sameLaptop = new Product("A001", "노트북");
System.out.println(stock.get(sameLaptop));  // 10
```

- 그렇지 않으면 → 기본 Object.equals()/hashCode()(참조 동등성)만 써도 됨

### Gradle

Java 같은 언어로 만든 프로젝트를 자동으로 빌드(compile, test, 패키징 등)해주는 도구

- 사용 이유
  Java 프로젝트에 필요한 작업: 코드 컴파일, 라이브러리(외부 의존성) 다운로드, 테스트 실행, JAR/WAR 파일 생성, 서버 실행
  → 수동으로 하기엔 너무 번거롭고 복잡하므로 Gradle을 사용해서 자동으로 처리

| 작업           | 설명                                                 |
| -------------- | ---------------------------------------------------- |
| `dependencies` | 외부 라이브러리 가져오기 (예: Spring Boot, JUnit 등) |
| `build`        | 컴파일 + 테스트 + JAR 파일 생성                      |
| `bootRun`      | Spring Boot 앱 실행                                  |
| `test`         | 테스트 코드 실행                                     |

#### 컴파일 (Compile)

Java 소스코드(.java)를 JVM이 실행할 수 있는 바이트코드(.class)로 변환하는 과정

#### JAR(Java Archive) 파일

.class 파일, 설정파일, 라이브러리 등을 하나의 압축 파일처럼 묶은 것  
실행 가능한 애플리케이션으로 만들기 위해 필요  
JVM은 .jar 파일을 통해 프로그램을 실행할 수 있음(`java -jar`)

1. Compile: `.java` → `.class` 변환
2. Process: `application.yaml` 같은 설정 복사
3. Test: 단위 테스트 실행
4. Package: `.class`, 리소스를 JAR로 묶음
5. 결과물: `build/libs/`에 `.jar` 생성

### Gradle Wrapper

- 설치한 적 없는 Gradle이 Spring Boot에서 동작하는 이유
- Spring Boot 프로젝트는 보통 Gradle Wrapper(gradlew)를 포함
- Gradle이 로컬에 설치되어 있지 않아도, 필요한 버전을 자동으로 다운로드해서 실행할 수 있게 해줌

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

> 실행 순서
>
> 1. 사용자가 gradlew 또는 gradlew.bat 실행
> 2. gradle-wrapper.properties 확인
> 3. 필요한 Gradle 버전이 없다면 gradle-wrapper.jar가 자동 다운로드
> 4. 해당 Gradle 버전으로 프로젝트 빌드

```txt
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

- Gradle Wrapper는 CI/CD 환경에서도 항상 동일한 버전의 Gradle을 보장하므로, 설치 유무나 환경 차이 걱정 없이 안정적인 빌드가 가능

#### Gradle vs Maven

| 항목   | Gradle                 | Maven       |
| ------ | ---------------------- | ----------- |
| 설정   | Groovy/Kotlin DSL      | XML         |
| 속도   | 빠름 (캐시, 병렬 빌드) | 비교적 느림 |
| 가독성 | 간결함                 | 장황함      |
| 유연성 | 높음                   | 중간        |

### Spring Initializer

- Group
  - 회사나 조직의 도메인(com.naver)
  - Java의 패키지 네임스페이스처럼 사용됨
  - 명명 규칙
    - 영어 소문자만 사용
    - 숫자 사용 가능 (단, 숫자로 시작하면 안 됨)
    - 하이픈(-)은 허용되지 않음
- Artifact
  - 프로젝트의 고유 이름(com.naver.shopping)
  - 빌드 결과물 이름에도 반영
  - 명명 규칙
    - 하이픈(-) 사용 가능
      - 단, package name에는 하이픈(-) 사용 불가
- Name
  - 프로젝트의 이름 (기본값은 artifact와 동일)
- Package Name
  - 기본값은 group + artifact 조합
- Packaging: JAR vs WAR
  - JAR(Java ARchive)
    - Spring Boot 기본 실행 방식
    - 내장 톰캣 포함되어있음
    - java -jar 명령으로 바로 실행 가능
  - WAR(Web Application Archive)
    - 전통적인 방식 (Java EE 환경)
    - 서버(톰캣, WebLogic 등)에 올려야 실행됨

#### 서버(톰캣)에 올리는 방식

1. WAR 파일을 만든다
2. 웹 서버가 설치된 컴퓨터에 복사한다
3. 톰캣의 webapps/ 폴더에 WAR 파일을 넣는다
4. 톰캣 서버를 실행하면 WAR가 실행된다.  
   (톰캣이 WAR를 읽고 웹사이트를 열어줌)

### Multi Module Project

자바에서 모듈(Module)은 독립적으로 배포될 수 있는 코드의 단위
멀티 모듈이란 서로 독립적인 프로젝트(인증, 어플리케이션)를 하나의 프로젝트로 묶어 모듈로서 사용되는 구조

- 사용 이유
  - 일정 수준 이상의 트래픽을 감당하려면 사용자와의 접점을 담당하는 서버(이하 web프로젝트), DB와의 접점을 담당하는 서버(이하 API 프로젝트)로 구분하여 구성
  - Member클래스를 공통으로 사용할 때, 한 프로젝트에서 Member 클래스파일을 생성하고 이를 다른 프로젝트에서 코드를 복사하는 방식은 가장 간단하지만 연동되는 프로젝트가 늘어날 경우, 혹은 Member 클래스의 코드에 수정이 필요할 경우에 정말 많은 양을 수정해야하고 실수할 여지가 많아짐 → 하나의 공통 프로젝트를 두고, 이 프로젝트를 여러 프로젝트에서 가져가서 사용

### Could not resolve all files for configuration ':buy-me-common:compileClasspath'

- 하위 프로젝트의 build.gradle 파일에 org.springframework.boot 플러그인과 io.spring.dependency-management 플러그인이 누락되어 의존성 버전을 제대로 가져오지 못해 발생하는 오류 → 하위 프로젝트에서도 스프링 부트의 의존성을 사용하려면 플러그인 설정이 필요

```groovy
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
  // 진짜 자바 코드가 있는 하위 모듈에만 java 플러그인을 적용
  // Gradle에서 Java 프로젝트를 빌드하려면 기본적으로 java 플러그인이 필요
  // java 플러그인을 통해 컴파일, 테스트, jar 파일 생성 등의 작업들(tasks)이 수행 가능
  apply plugin: 'io.spring.dependency-management'
  // dependency-management 플러그인은 Spring Boot의 BOM을 직접 알지 못함
  // * BOM: 라이브러리들의 버전 목록

  java {
    toolchain {
      languageVersion = JavaLanguageVersion.of(17) // 어떤 자바 버전으로 빌드할지 지정
    }
  }

  dependencyManagement {
    imports {
      mavenBom "org.springframework.boot:spring-boot-dependencies:3.4.5"
      // plugin에 dependency-management 사용 시, dependency-management에 BOM을 직접 import
      // plugin에 org.springframework.boot 사용 시, dependency-management 자동 적용되어 dependencyManagement 블록 불필요
    }
  }
}
```

### 상위 프로젝트의 spring-boot-starter dependency를 못 읽어오는 오류

```groovy
dependencies {
    implementation project(':web')
}
```

- Gradle의 implementation은 **전이적(transitive)**이지만, 항상 완전히 동작하는 건 아님
  - `@SpringBootApplication`은 Spring Boot의 많은 자동 설정 기능을 쓰기 위한 핵심 애노테이션인데, 그 기반이 되는 자동 구성 메타정보는 `직접 선언된` 의존성을 통해서만 완전히 인식될 수 있음

### Gradle option

- 클래스 패스(class path)

  - 자바로 작성된 프로그램을 컴파일(compile: .java → .class)하고 실행(run)할 때 특정 경로에서부터 시작하여 클래스 파일과 패키지를 탐색

    - Compile classpath: Java 코드를 class 파일로 컴파일 할 때 탐색하는 경로
    - Runtime classpath: 컴파일된 자바 코드(class 파일)을 JVM이 실행할 때 탐색하는 경로

  - 컴파일 시점에만 필요로 하는 의존성도 있고, 실행 시점에만 필요로 하는 의존성도 있음  
    → 그래서 Gradle에서 의존성(dependency)를 추가할 때 어느 범위로 노출시킬 것인지 결정할 수 있음

- compileOnly

  - 컴파일 경로에만 설정
  - 빌드 결과물의 크기가 줄어드는 장점

- runtimeOnly

  - 런타임 경로에만 설정
  - 해당 클래스에서 코드 변경이 발생해도 컴파일을 다시 할 필요가 없음

- implementation, api

  - 두 경로에 모두 설정
  - api는 Java-Library 플러그인 추가 필요
  - implementation으로 설정된 의존성은 전이되지 않으며, 해당 모듈 내부에서만 사용
    - implementation로 설정된 의존성은 다른 모듈의 컴파일 클래스 경로에 포함되지 않으며, 이로 인해 라이브러리를 제공하는 측에서 의존성을 변경하더라도, 사용하는 측은 재컴파일하지 않아도 됨
    - 이를 통해 컴파일 시간을 단축하고 재빌드 빈도를 줄일 수 있는 이점을 얻을 수 있음
    - runtime이 deprecated 되고 나온 것은 implementation
  - api로 설정된 의존성은 전이되어 다른 모듈의 컴파일 클래스 경로(compileClasspath)에도 추가

    - 예를 들어, 현재 모듈이 httpclient 라이브러리를 사용하고 있다면, 이 모듈을 의존하는 다른 모듈도 자동으로 httpclient 라이브러리를 사용할 수 있게 됨
    - compile이 deprecated 되고 나온 것이 api

  - Gradle은 가능한 implementation을 사용하는 것을 권장하는데, api는 의존성이 다른 모듈에 전이되지만 implementation은 해당 모듈 내부에서만 사용되고 다른 모듈에는 노출되지 않기 때문
  - 무분별하게 api를 사용하기보다는 상황에 맞게 implementation을 사용하여 의존성을 캡슐화하고, 이를 통해 컴파일 시간을 단축하여 재빌드 빈도를 줄일 수 있는 이점을 얻는 것이 좋음
    - 해당 모듈에서만 사용하는 경우 implementation을 사용하고, 다른 모듈에서도 함께 사용할 경우 api를 사용

- 예시

```txt
모듈 B가 모듈 A를 api로 의존 + 모듈 C가 모듈 B를 api로 의존
→ 모듈 C에서 모듈 A의 클래스를 사용할 수 있음

모듈 B가 모듈 A를 api로 의존 + 모듈 C가 모듈 B를 implementation으로 의존
→ 모듈 C에서 모듈 A의 클래스를 사용할 수 있음

모듈 B가 모듈 A를 implementation으로 의존 + 모듈 C가 모듈 B를 api로 의존
→ 모듈 B에서 모듈 A의 클래스를 사용할 수 있지만, 모듈 C에서는 사용할 수 없음
```

### JPA 연관 관계

```sql
-- table
create table Person(
  id bigint auto_increment,
  name varchar(255) not null,
  primary key (id)
);

create table Address(
  id bigint auto_increment,
  city varchar(255) not null,
  street varchar(255) not null,
  person_id bigint,
  primary key (id)
);
```

```java
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Entity
public class Person {
  // Address가 person_id를 보유

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private long id;

  @Column(nullable = false)
  private String name;

  @OneToOne(mappedBy = "person")
  private Address address;

  // 양방향 연관관계 설정
  public void setAddress(Address address) {
    this.address = address;
    if (address != null) {
      address.setPerson(this);
    }
  }
}

@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Entity
public class Address {
  // person_id를 보유

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  private long id;

  @Column(nullable = false)
  private String city;

  @Column(nullable = false)
  private String street;

  @OneToOne
  // @JoinColumn(name = "person_id")
  private Person person;

  protected Address() {}

  public Address(String city, String street, Person person) {
    this.city = city;
    this.street = street;
    this.setPerson(person);
  }

  // 양방향 연관관계일 때는 한 번에 연결하는 것이 좋음
  public void setPerson(Person person) {
    this.person = person;
    if (person != null) {
        person.setAddress(this);
    }
  }
}

@Service
@Transactional
public class PersonService {

  private final PersonRepository personRepository;
  private final AddressRepository addressRepository;

  public PersonService(PersonRepository personRepository, AddressRepository addressRepository) {
    this.personRepository = personRepository;
    this.addressRepository = addressRepository;
  }

  public void savePerson(){
    Person saved = personRepository.save(new Person("name"));
    // 연관관계 주인쪽에 설정
    Address address = addressRepository.save(new Address("seoul", "gangnamdaero", saved));
  }
}
```

- cascade: 저장, 삭제 시 연관 관계 테이블까지 함께 동작
- orphanRemoval: 부모 컬렉션에서 제거된 자식 엔티티가 자동으로 DB에서 삭제
- FetchType.Lazy: 지연 로딩, 연관된 엔티티에 실제로 접근하는 시점에 필요한 데이터를 조회하는 방식

### private 필드값 테스트

1. ReflectionTestUtils

- private 필드에도 직접 값을 주입할 수 있어, Entity의 구조를 변경하지 않고도 손쉽게 테스트 할 수 있음

```java
@Test
void myTest() {
    // given
    User user = new User("test@email.com", "nickname", "password"); // 기존 생성자 사용

    // Reflection을 사용해 private인 id 필드에 값을 설정
    ReflectionTestUtils.setField(user, "id", 1L);

    when(userRepository.findById(1L)).thenReturn(Optional.of(user));

    // then
    assertThat(user.getId()).isEqualTo(1L);
}
```

2. 테스트 데이터 빌더(Test Data Builder) 패턴 사용
   테스트용 객체 생성을 전담하는 별도의 빌더 클래스를 생성

```java
// 테스트 소스 폴더(src/test/java)에 빌더 클래스 생성
public class UserTestBuilder {
    private Long id = 1L;
    private String email = "test@example.com";
    // ... 기본값 설정 ...

    public static UserTestBuilder builder() {
        return new UserTestBuilder();
    }

    public UserTestBuilder id(Long id) {
        this.id = id;
        return this;
    }

    // ... 다른 필드 설정 메서드 ...

    public User build() {
        User user = new User(email, ...); // 엔티티의 프로덕션 생성자 사용
        ReflectionTestUtils.setField(user, "id", this.id); // 빌더 내부에서 리플렉션 사용
        return user;
    }
}
```

### Mockito vs BDD Mockito

- Mockito
  - 언제(when) 이 메서드가 호출되면, 이것을 반환해라(thenReturn)
  - `when(mock.method()).thenReturn(value);`
  - `when(...).thenThrow(new Exception());`
  - `verify(mock).method();`
- BDDMockito
  - `given(mock.method()).willReturn(value);`
  - `given(...).willThrow(new Exception());`
  - `then(mock).should().method();`

#### Mockito argument matching

- any(Request.class) → null 매칭 가능
  - 객체 타입(Object 타입)은 null을 허용
- any(Long.class) → null 을 매칭 못함
  - primitive wrapper(Long, Integer 등)는 null을 허용하지 않음
  - 이런 경우, 주로 any() 사용
- nullable(Long.class) → null 매칭 가능
  - 여기 null이 올 수 있고, 그걸 고려하는 테스트다를 드러낼 때 좋음
- any() → null 매칭 가능
  - 가장 일반적으로 사용

### MockMvc

- 실제 서버를 띄우지 않고도 Controller를 테스트할 수 있게 해주는 Spring의 테스트 도구
  - Spring MVC의 HTTP 요청/응답 테스트 도구
- @WebMvcTest가 자동으로 MockMvc를 생성함
  - 이후, @Autowired로 실제 Bean 주입

```java
@WebMvcTest(SignupController.class)
class SignupControllerTest {
  @Autowired
  private MockMvc mockMvc;

  @Test
  void signup_Test() throws Exception {
      mockMvc.perform( // HTTP 요청 시뮬레이션
              post("/signup") // POST /signup
              .param("email", "test@email.com") // 파라미터
              .param("password", "Password123!")
          )
          .andExpect(status().isOk()) // 응답 검증
          .andExpect(view().name("auth/signup")); // 뷰 이름 검증
  }

}
```

### andExpect vs assertThat

- .andExpect()
  - MockMvc 체인 안에서
  - HTTP 응답 관련 검증
    - 상태 코드: status().isOk()
    - JSON 응답: jsonPath("$.field").value("value")
    - 헤더: header().string("Location", "url")
    - 쿠키: cookie().value("name", "value")

```java
mockMvc.perform(post("/signup"))
    .andExpect(status().isCreated())
    .andExpect(jsonPath("$.email").exists())
    .andExpect(header().string("Location", "/api/v1/users/1"));
```

- assertThat()
  - MockMvc 체인 밖에서
  - 비즈니스 로직/데이터 검증
    - DB 저장 확인
    - 서비스 로직 결과 검증
    - 객체 상태 검증

```java
// DB 저장 확인
User savedUser = userRepository.findByEmail(email).orElseThrow();
assertThat(savedUser.getEmail()).isEqualTo(VALID_EMAIL);
assertThat(savedUser.getPassword()).isNotEqualTo(rawPassword);

// 비즈니스 로직 검증
List<User> users = userService.findActiveUsers();
assertThat(users).hasSize(3);
assertThat(users.get(0).getName()).isEqualTo("John");
```

### value() vs is()

- value() 사용
  - 단순 값 비교

```java
.andExpect(jsonPath("$.email").value("test@email.com"))
.andExpect(jsonPath("$.id").value(123))
.andExpect(jsonPath("$.active").value(true))
.andExpect(jsonPath("$.name").value(user.getName()))
```

- Hamcrest 매처 사용
  - 조건/패턴 검증
  - 크기, 포함, 범위, 패턴, 존재여부 등

```java
.andExpect(jsonPath("$", hasSize(3)))                      // 배열 크기
.andExpect(jsonPath("$", is(emptyList())))                 // 빈 배열
.andExpect(jsonPath("$.password").doesNotExist())          // 존재하지 않음
.andExpect(jsonPath("$.age", greaterThan(18)))             // 범위 비교
.andExpect(jsonPath("$.email", containsString("@")))       // 부분 포함
.andExpect(jsonPath("$[*].id", containsInAnyOrder(1,2,3))) // 배열 내용
```

### 테스트 코드 접근 제한자

1. private - 같은 클래스에서만 접근
2. package-private (default) - 같은 패키지에서 접근 가능
3. protected - 같은 패키지 + 상속받은 클래스에서 접근
4. public - 어디서든 접근 가능

- 테스트 메서드
  - private이면 접근할 수 없어서 실행 불가
  - 반드시 package-private 이상이어야 함
  - JUnit이 리플렉션으로 테스트 메서드를 찾음
- 헬퍼 메서드
  - 테스트 클래스 내부에서만 사용
  - 캡슐화 원칙 적용 -> private
  - JUnit이 실행하지 않는 메서드

### JPA 영속성 컨텍스트

```java
User user = createUser(VALID_EMAIL, VALID_NICKNAME, passwordEncoder.encode(VALID_PASSWORD));
// user.getId() = null

userRepository.save(user);
// user.getId() = 1
```

JPA가 save() 할 때

1. 데이터베이스 INSERT 실행
2. 데이터베이스 ID 자동 생성
3. JPA가 생성된 ID를 원본 객체에 다시 설정

### Submit

```java
@PostMapping
public String submit(
    @Valid @ModelAttribute BirthInfoForm birthInfoForm,
    BindingResult result,
    Model model
) throws Exception {

  model.addAttribute("birthInfo", birthInfoForm);

  return "/fortune/option";
}
```

- 문제점
  - POST 요청에서 템플릿을 직접 반환하고 있어서 URL이 변경되지 않음
  - 브라우저 주소창이 사용자가 보고 있는 화면이 일치하지 않음

```java
@PostMapping
public String submit(
    @Valid @ModelAttribute BirthInfoForm birthInfoForm,
    BindingResult result,
    RedirectAttributes redirectAttributes
) throws Exception {

  redirectAttributes.addFlashAttribute("birthInfo", birthInfoForm);

  return "redirect:/fortune/option";
}

```

- 해결
  - 브라우저가 302 리다이렉트 응답을 받음
  - 브라우저가 자동으로 GET 요청을 보냄
  - 서버가 새로운 html 반환

### @Mock

- Mockito가 제공하는 **가짜 객체(Mock)**를 만들어 테스트에서 의존성을 대체할 때 사용
- JUnit 단위 테스트 수준, Spring 컨텍스트를 로드하지 않아도 됨

```java
@ExtendWith(MockitoExtension.class)
// @Mock → mock 객체 생성
// @InjectMocks → mock 객체를 주입(생성자 → Setter → 필드순으로 주입 시도)
// 두 애노테이션을 자동으로 처리
class UserServiceTest {

    @Mock
    private UserRepository userRepository; // 실제 DB X, Mockito mock

    @InjectMocks // 객체가 의존하는 필드(UserRepository 등)에 @Mock 객체를 주입
    private UserService userService;

    @Test
    void testFindUser() {
        User mockUser = new User("hyunji");
        when(userRepository.findById(1L)).thenReturn(Optional.of(mockUser));

        User result = userService.getUser(1L);
        assertEquals("hyunji", result.getName());
    }
}
```

- @InjectMocks

  - 값 객체들: String, Duration, Money → Mock할 필요 없음
    - Mock은 필요한 협력 객체(인터페이스)에만 사용하고, 값 객체는 실제 객체를 사용
  - 테스트마다 다른 값의 경우, Mock할 필요 없음
  - 😵 Mocking하지 않을 필드를 @Mock으로 선언할 경우, InjectMocks가 가짜 객체 주입

  ```java
  //@Mock
  //private ObjectMapper objectMapper;

  @BeforeEach
  void setUp() {
    // 실제 ObjectMapper 인스턴스를 주입
    ReflectionTestUtils.setField(geminiService, "objectMapper", new ObjectMapper());

  }
  ```

### @MockBean

- Spring Boot Test 환경에서 Bean을 대체(Mock)할 때 사용(실제 컨텍스트에 있는 Bean을 Mockito Mock으로 대체해서 테스트)
- Spring Boot Test (@SpringBootTest, @WebMvcTest, @DataJpaTest) 안에서만 의미 있음
  - @WebMvcTest도 컨트롤러 단위 테스트라는 의미지만, Spring 컨텍스트를 일부 띄우기 때문에 순수 Mockito @Mock 대신 @MockBean을 써야 함

```java
@SpringBootTest
class UserServiceIntegrationTest {

    @MockBean
    private UserRepository userRepository; // 실제 DB 접근 X, 컨테이너에서 대체

    @Autowired
    private UserService userService;

    @Test
    void testFindUser() {
        User mockUser = new User("hyunji");
        when(userRepository.findById(1L)).thenReturn(Optional.of(mockUser));

        User result = userService.getUser(1L);
        assertEquals("hyunji", result.getName());
    }
}
```

#### Service는 순수 단위 테스트로 충분한 이유

- 대부분은 HTTP나 직렬화 같은 외부 요소와 무관
  - 따라서 Spring 컨텍스트 불필요, @Mock으로 Repository 대체하고 메소드 호출/리턴값만 검증하면 충분

#### Controller는 순수 단위 테스트로 부족한 이유

- Controller는 단순히 메소드 호출만 검증하면 안 되고, Spring MVC가 실제로 처리하는 여러 요소들을 확인해야 하는 경우가 많음
- @RequestMapping, @GetMapping, @PostMapping 같은 URL 매핑이 올바른지
- @RequestBody, @PathVariable, @RequestParam이 제대로 바인딩되는지
- JSON 직렬화/역직렬화(Jackson)
- Spring Validator 적용 결과 (@Valid)
- 응답 코드 (200 OK, 400 Bad Request, 404 Not Found 등)
  - 👉 이런 부분들은 순수 단위 테스트로는 검증 불가능
  - 👉 그래서 @WebMvcTest + MockMvc로 실제 HTTP 요청을 흉내 내서 검증

### @ParameterizedTest, @CsvSource

- @ParameterizedTest
  - 테스트 메서드가 여러 개의 입력 파라미터를 받아서, 다양한 경우의 수를 자동으로 돌려볼 수 있게 함
  - 같은 로직을 입력값만 바꿔 여러 번 검증
- @CsvSource
  - CSV(Comma-Separated Values) 형식으로 여러 테스트 데이터를 직접 코드에 넣어줌
  - 각 줄이 테스트 1회 실행에 쓰일 파라미터 집합

```java
@ParameterizedTest
@CsvSource({
    "test@email.com, password123",
    "admin@email.com, admin123",
    "invalid-email, short"
})
void validateSignup(String email, String password) {
    // 테스트 로직
}
```

### 배포 전 프로필 분리

1. `application.yaml`

- 공통 속성 기재

```yaml
server:
  servlet:
    session:
      timeout: 10m # 10분 후 자동 만료

spring:
  config:
    import:
      - classpath:application-prompts.yaml
  messages:
    encoding: UTF-8

gemini:
  api:
    key: ${GEMINI_API_KEY}
  model: gemini-2.5-flash

jwt:
  secret: ${JWT_SECRET}
  token-validity: ${JWT_TOKEN_VALIDITY}

logging:
  level:
    root: INFO # 모든 라이브러리(Spring, Hibernate 등) 로그는 INFO 레벨만
    com.fortunehub.luckylog: DEBUG # com.fortunehub.luckylog 패키지의 로그는 DEBUG까지 상세하게
  pattern:
    console: '%d{yyyy-MM-dd HH:mm:ss} [%thread] %highlight(%-5level) %logger{36}.%M - %msg%n'
```

- ✨ 변수는 .env에서 관리하고, .gitignore에 추가하여 공개되지 않도록 유의
  - .env 파일 IntelliJ에서 사용하는 방법
    - EnvFile 플러그인 설치 후, .env 파일 추가
  - 또는 구성 편집 → 환경 변수에서 .env 관련 설정 추가
  - .env 파일 사용이 로컬 개발용으로 프로덕션 배포 시에는 서버에서 환경변수나 시크릿 변수를 처리하는 다른 방법 사용(예: Github Actions: Actions secrets and variables)

2. `application-local.yaml`

- local 환경 전용 속성 기재

```yaml
spring:
  datasource:
    url: ${LOCAL_DB_URL}
    username: ${LOCAL_DB_USER}
    password: ${LOCAL_DB_PASSWORD}
    driver-class-name: org.h2.Driver
  h2:
    console:
      enabled: true
      path: /h2-console
  jpa:
    hibernate:
      ddl-auto: create
    properties:
      hibernate:
        format_sql: true
        show_sql: true
        dialect: org.hibernate.dialect.H2Dialect

logging:
  level:
    org.hibernate.SQL: DEBUG # SQL 쿼리 보기
    org.hibernate.orm.jdbc.bind: TRACE # 파라미터 값까지 보기
```

- IntelliJ에서 profile local 설정하는 방법
  - 구성 편집 → 환경 변수: `SPRING_PROFILES_ACTIVE=local` 추가

3. `application-prod.yaml`

- 운영 환경 전용 속성 기재

```yaml
spring:
  datasource:
    url: ${PROD_DB_URL}
    username: ${PROD_DB_USER}
    password: ${PROD_DB_PASSWORD}
    driver-class-name: com.mysql.cj.jdbc.Driver
  jpa:
    hibernate:
      ddl-auto: none
    properties:
      hibernate:
        format_sql: false
        show_sql: false
        dialect: org.hibernate.dialect.MySQLDialect

logging:
  level:
    root: WARN
    com.fortunehub.luckylog: INFO
```

- 서버에서 profile 및 환경변수 설정하는 방법

```bash
# ~/.bashrc 파일 편집
vi ~/.bashrc

# 파일 맨 아래에 추가 (i 눌러서 입력 모드)
export PROD_DB_URL=jdbc:mysql://your-rds-endpoint:3306/luckylog_prod
export PROD_DB_USER=admin
export PROD_DB_PASSWORD=your-rds-password
export JWT_SECRET=production-super-secret-key-change-this
export JWT_TOKEN_VALIDITY=3600000
export GEMINI_API_KEY=your-gemini-api-key

# ESC 누르고 :wq 입력해서 저장

source ~/.bashrc # 파일을 즉시 적용(또는 . ~/.bashrc)

# 빌드

java -jar -Dspring.profiles.active=prod lucky-log.jar
# nohup으로 백그라운드 실행
nohup java -jar -Dspring.profiles.active=prod lucky-log.jar > app.log 2>&1 &
```

### Spring Security

```bash
dependencies {
  implementation 'org.springframework.boot:spring-boot-starter-security'
}
```

```java
@Configuration
public class SecurityConfig {
  @Bean
  public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.authorizeHttpRequests(auth -> auth.anyRequest().permitAll())
    // 모든 HTTP 요청에 대한 접근 허용
        .csrf(csrf -> csrf.disable())
        // CSRF 보호 기능 비활성화
        .headers(headers -> headers
            .frameOptions(frameOptions -> frameOptions.disable())
            // X-Frame-Options 헤더 비활성화
        );
    return http.build();
  }
}
```

- frameOptions

  - H2 콘솔은 `<iframe>` 구조로 화면을 구성
  - Spring Security는 보안상의 이유로 기본적으로 페이지가 `<iframe>`에 포함되는 것을 금지
  - 따라서 H2 콘솔을 사용하려면 `frameOptions().disable()`을 통해 이 기능을 비활성화해야 함

- CSRF disabled 이유

  - Access Token

  ```js
  // JavaScript 코드로 직접 Header에 넣어서 보냄
  fetch('/api/data', {
    headers: {
      Authorization: 'Bearer ' + accessToken,
    },
  });

  /*
  악성 사이트가 공격 시도할 경우,
  악성 사이트 → 내 API 호출 시도
  ❌ Header에 토큰 못 넣음
  ❌ 공격 실패!
  */
  ```

- Refresh Token

  ```js
  // 쿠키는 브라우저가 자동으로 보냄
  document.cookie = 'refreshToken=abc123';

  // 악성 사이트에서 요청하면?
  // ✅ 쿠키가 자동으로 따라감 → 위험!
  fetch('https://내사이트.com/refresh');

  cookie.setSameSite('Strict');

  /*
  "이 쿠키는 내 사이트에서만 사용해! 다른 사이트에서 온 요청에는 쿠키 안 보내줄게!"
  악성 사이트 → 내 API 호출 시도
  ❌ 쿠키가 안 따라감
  ❌ 공격 실패!  
  */
  ```

```bash
Using generated security password:
This generated password is for development use only.
Your security configuration must be updated before running your application in production.
# Spring Security가 자동으로 활성화되어서 임시 비밀번호를 생성
```

- Spring Security가 활성화되어 있는데 보안 설정을 따로 구성하지 않았을 때 자동으로 기본 보안 설정이 적용되면서 나타남

  - 기본 사용자명: user
  - 기본 비밀번호: 랜덤 생성된 UUID (콘솔에 출력됨)
  - 모든 엔드포인트에 인증 요구

1. 의존성 제외
2. Auto Configuration 제외

```java
@SpringBootApplication(exclude = {SecurityAutoConfiguration.class})
public class YourApplication {
    public static void main(String[] args) {
        SpringApplication.run(YourApplication.class, args);
    }
}
```

3. 임시 비밀번호 설정

```yaml
# application.yaml
spring:
  security:
    user:
      name: admin
      password: password
```

4. Spring Security 관련 설정 등록

#### authenticationEntryPoint

```java
.exceptionHandling(handling -> handling
  .authenticationEntryPoint(new HttpStatusEntryPoint(HttpStatus.UNAUTHORIZED))
);
```

- 미인증 시 Spring Security 기본 동작:

  - 폼 로그인 설정한 경우, 로그인 페이지로 리다이렉트
  - 폼 로그인 설정을 하지 않았을 경우, 403(Forbidden)을 반환
  - 명시적으로 401(Unauthorized) 상태 코드를 반환하기 위해 사용

### Spring Boot 프로파일 활성화 우선순위

1. 커맨드 라인 인자

```bash
java -jar app.jar --spring.profiles.active=prod
```

2. 환경 변수

```bash
export SPRING_PROFILES_ACTIVE=prod
java -jar app.jar
```

3. application.yaml의 spring.profiles.active

```yaml
spring:
  profiles:
    active: ${SPRING_PROFILES_ACTIVE:prod}
```

### Health Check

앱이 살아있고 정상인지 확인하는 것

1. build.gradle에 의존성 추가

```groovy
dependencies {
    implementation 'org.springframework.boot:spring-boot-starter-actuator'
}
```

2. application.yaml 설정

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health, info
        # 외부에 공개할 엔드포인트 목록
        # health: 헬스 체크용
        # info: 앱 정보 (버전, 설명 등)
        # 다른 것들: metrics, env, loggers 등 (보안상 안 열림)

      base-path:
        /actuator
        # URL 시작 경로
        # /actuator/health, /actuator/info 이렇게 접근

  endpoint:
    health:
      show-details:
        when-authorized
        # 헬스 정보를 얼마나 자세히 보여줄지
        # never: {"status":"UP"} 만
        # always: DB상태, 디스크 등 다 보여줌
        # when-authorized: 인증된 사용자에게만 자세히
```

3. 확인

```bash
# 1. 로컬에서 앱 실행 후
curl http://localhost:8080/actuator/health

# 2. 서버에 배포 후
curl http://localhost:8080/actuator/health
```

### 빌드 오류

```bash
LuckylogApplicationTests > contextLoads() FAILED
    java.lang.IllegalStateException at DefaultCacheAwareContextLoaderDelegate.java:180
        Caused by: org.springframework.boot.context.config.ConfigDataResourceNotFoundException at ConfigDataResourceNotFoundException.java:97
```

- `ConfigData`: Spring Boot의 설정 파일 (application.yaml 등)
- `ResourceNotFound`: 리소스를 찾을 수 없음
- `Exception`: 예외 발생
- "설정 파일에서 참조한 리소스를 찾을 수 없다"

* Spring Boot가 테스트 실행할 때
  - `main/resources/application.yaml` 먼저 읽어서 테스트 환경에서 의도하지 않은 동작이 발생할 수 있음
  - `test/resources/application.yaml` 생성해서 main 내용을 오버라이드
    - 프로필 지정 불필요 (자동으로 test 설정이 적용됨)
  - 또는 `application-test.yaml` 사용 시 프로필 활성화 필요:
    - `-Dspring.profiles.active=test` 추가
    - `@SpringBootTest(properties = "spring.profiles.active=test")` 추가

### Neither BindingResult nor plain target object for bean name 'signupForm' available as request attribute

- `@ModelAttribute`는 자동으로 모델에 빈객체를 추가해주지만, 매개변수 이름과 무관하게 클래스 이름의 첫 글자를 소문자로 변경해서 보냄
  - SignupForm → signupForm

```java
  @GetMapping
  public String show(@ModelAttribute SignupForm form) {
    // model.addAttribute("signupForm", new SignupForm());
    // @ModelAttribute가 자동으로 "signupForm" 이름의 빈 객체를 모델에 추가
    return "signup";
  }
```

### Thymeleaf 페이지 상대 경로

- 배포 환경이 바뀌어도 깨지지 않음

```html
<a href="/user/profile"></a>
<!--로컬에선 /user/profile 잘 되지만,
서버가 /app 컨텍스트 루트로 배포되면 /app/user/profile이 아닌 /user/profile로 요청되어 404 발생-->
```

- 템플릿 재사용성과 include 구조에 유리
  - fragment를 여러 경로에서 include하면,
    - 절대경로(/user/profile)를 쓰면 컨텍스트 루트가 다르면 깨짐
    - 상대경로(user/profile)를 쓰면 현재 위치 기준으로 자동 해석

```html
<!-- /templates/fragments/header.html -->
<a href="home">홈</a>
<a href="user/profile">프로필</a>
```

- Thymeleaf에서 컨텍스트 경로 문제를 해결하는 표준적인 방법

```html
<a th:href="@{/user/profile}"></a>
<!--컨텍스트 기반 상대경로로 처리됨-->
```

### `타입 매개변수 'S'에 대한 추론 타입 'S'이(가) 해당 바운드 내에 없으며, 'com.fortunehub.luckylog.domain.member.Member'을(를) 확장해야 합니다`

```java
verify(memberRepository, never()).save(any(Member.class));
// any(Member.class)의 반환 타입이 Member가 아니라 Object로 추론되면서,
// save(S entity)의 제네릭 타입 S extends Member 조건을 만족하지 못함

verify(memberRepository, never()).save(ArgumentMatchers.<Member>any());
// Mockito가 any()의 제네릭 타입을 명확히 Member로 인식
```

### `org.mockito.exceptions.misusing.PotentialStubbingProblem: Strict stubbing argument mismatch`

```java
given(memberRepository.save(req.toEntity(encodedPassword)))
    .willThrow(new DataIntegrityViolationException("Duplicate entry for nickname"));
// req.toEntity()를 호출할 때마다 새로운 Member 객체가 생성되기 때문에, Mock 설정 시의 객체와 실제 서비스에서 save() 호출 시의 객체가 달라서 Stubbing이 매칭되지 않음

// any(Member.class) 사용
given(memberRepository.save(any(Member.class)))
    .willThrow(new DataIntegrityViolationException("Duplicate entry for nickname"));
```

### Spring Security와 Test Code

```java
@WebMvcTest(SignupController.class)
class SignupControllerTest {}

// 컨트롤러, 관련 MVC 컴포넌트, Jackson 등만 로딩하고 나머지 빈(Service, Repository, Security 등)은 로드하지 않음
// Spring Security 설정도 로드되지 않거나, 필요한 경우 기본 설정으로 적용됨

// Test Code 전용 TestSecurityConfig 생성
@TestConfiguration
public class TestSecurityConfig {
    @Bean
    public SecurityFilterChain testSecurityFilterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth.anyRequest().permitAll())
            .csrf(csrf -> csrf.disable());
        return http.build();
    }
}

@Import(TestSecurityConfig.class)
@WebMvcTest(SignupController.class)
class SignupControllerTest {}
```

### Optional Input Value `@Size` 사용 시 유의점

- HTML <input /> 필드에서 아무것도 입력 안 하면, 브라우저는 기본적으로 빈 문자열로 전송
  - null이 아닌 length가 0으로 들어가 `@Size(min=2)` 검증 실패 → 오류 발생

### `@RequiredArgsConstructor`와 super

- Lombok @RequiredArgsConstructor만 사용하면 super(errorCode.getMessage()) 호출이 자동으로 되지 않음
  - 부모 생성자를 호출해야 하는 경우는 직접 생성자를 작성하는 것이 필요

```java
@Getter
public class CustomException extends RuntimeException {

  private final ErrorCode errorCode;

  public CustomException(ErrorCode errorCode) {
    super(errorCode.getMessage()); // @RequiredArgsConstructor만 쓸 경우, 생성되지 않음
    this.errorCode = errorCode;
  }
}
```

### HTTP Basic 인증

- 클라이언트가 서버에 요청할 때 사용자 이름과 비밀번호를 HTTP 헤더에 실어서 보내는 방식
  - Base64는 암호화가 아님, HTTPS 없이는 평문 노출 위험
  - 서버가 세션을 저장할 필요 없이 요청마다 인증 가능
  - Spring Security 등에서 HTTP Basic 인증을 비활성화하는 이유
    - API에서는 주로 JWT, OAuth2 등 다른 인증 방식을 사용

```txt
Authorization: Basic dXNlcjpwYXNzd29yZA==
user:password를 Base64로 인코딩한 문자열
```

### JWT(JSON Web Token)

- 서버와 클라이언트 사이에서 인증 정보를 안전하게 전달하기 위해 사용되는 토큰 기반 인증 방식

- JWT 동작 방식 (로그인 기준)

  1. 클라이언트 → 서버: 로그인 요청
  2. 서버 → 클라이언트: 인증 성공 시 JWT 발급
  3. 클라이언트: JWT를 Authorization: Bearer <token> 헤더에 담아 요청
  4. 서버: JWT 검증 → 사용자 인증/인가 처리

- JWT 저장 위치

  - localStorage
    - 클라이언트 브라우저
    - 스크립트로 토큰 접근 가능하므로 XSS 공격에 매우 취약
  - sessionStorage
    - 탭 세션
    - 스크립트로 토큰 접근 가능하므로 XSS 공격에 매우 취약
  - HttpOnly 쿠키
    - 브라우저 쿠키
    - SameSite, CSRF 토큰 등으로 CSRF 방어 필요

- Access Token + Refresh Token 구조

  - Access Token → 짧은 유효기간 (5~15분)
    - Access Token은 메모리에 보관하고 요청 시 Authorization 헤더에 포함하여 전송 → XSS로 유출되어도 피해 최소화
  - Refresh Token → HttpOnly 쿠키에 저장 (재발급용)

    - 서버 측 권장 설정

    ```http
    Set-Cookie: refresh_token=<token>;
    HttpOnly; Secure; SameSite=Strict; Path=/auth/refresh;
    ```

    - HttpOnly: JS에서 쿠키 접근 불가 → XSS 방어
    - Secure: HTTPS에서만 전송
    - SameSite=Strict: CSRF 공격 방어
    - Path: 특정 경로로만 쿠키 전송 제한

#### JWT와 Storage, Cookie

| 항목                 | localStorage                     | sessionStorage                       | Cookie                                             |
| -------------------- | -------------------------------- | ------------------------------------ | -------------------------------------------------- |
| **저장 위치**        | 브라우저 (클라이언트)            | 브라우저 (클라이언트)                | 브라우저                                           |
| **데이터 지속성**    | **영구 저장** (삭제 전까지 유지) | **세션 단위** (탭/창 닫으면 삭제)    | 만료시간(`expires`)까지 유지                       |
| **자동 전송 여부**   | ❌ 서버로 자동 전송 안 됨        | ❌ 서버로 자동 전송 안 됨            | ✅ 요청 시 자동으로 서버로 전송됨 (`Cookie` 헤더)  |
| **보안 취약성**      | JS 접근 가능 → XSS에 취약        | JS 접근 가능 → XSS에 취약            | JS 접근 가능(기본값), `HttpOnly` 설정 시 접근 불가 |
| **사용 목적**        | 사용자 설정, 캐시, 장기 저장     | 일시적 데이터 (ex. 입력값 임시 저장) | 세션 유지, 인증 정보 전송 등                       |
| **도메인 공유 여부** | 동일 출처(origin) 내에서만 접근  | 동일 탭 내 동일 출처에서만 접근      | 도메인 단위 공유 가능 (`.example.com`)             |

- CSR
  - Access Token: localStorage/sessionStorage/JS변수(메모리) 저장 (API 호출 시 Authorization 헤더로 전송)
    - XSS를 막기 위해 쿠키에 HttpOnly를 설정하면 JS에서는 꺼낼 수 없음, auth header에 추가 불가
  - Refresh Token: HttpOnly Cookie에 저장 (자동 전송, JS 접근 불가)
- SSR
  - 서버(예: Next.js, Spring Boot, Nest.js 등) 가 HTML을 렌더링해서 클라이언트에 내려주는 방식
  - 브라우저가 localStorage에 엑세스 토큰을 가지고 있어도, 서버는 “요청 직전에 localStorage를 읽는 방법”이 없음
  - 서버는 오직 HTTP 요청 헤더로 전달되는 쿠키만 접근 가능
  - Access Token, Refresh Token 모두 Cookie 사용

### 테스트 전략별 비교

- 📊 **커버리지 중심 (대기업, 금융권)**

  - Service: 90%+
  - Repository: 80%+
  - Controller: 70%+
  - 목표: 전체 80% 이상

- 🎯 **핵심 로직 중심 (스타트업, 일반 기업)**

  - Service 핵심 로직: 필수
  - Repository 커스텀 쿼리: 권장
  - Controller: 중요 API만
  - 목표: 비즈니스 로직 신뢰성

- ⚡ **실용주의 (소규모, 애자일)**

  - 버그가 자주 나는 부분
  - 리팩토링 예정인 부분
  - 복잡한 비즈니스 로직만

### log 설정

```java
log.error("예상치 못한 오류 발생: {}", e);
// 예외 객체의 toString() 결과만 출력

log.error("예상치 못한 오류 발생", e);
// 전체 스택 트레이스 기록
```

### JPA의 flush 타이밍과 식별자 생성 전략(GenerationType)

- `JpaRepository.save(entity)` 호출 시,
  - 엔티티를 Persistence Context(영속성 컨텍스트) 에 등록 (managed 상태)
  - flush() 되기 전까지 실제 SQL은 실행되지 않음
    → 즉, INSERT SQL은 보통 트랜잭션 커밋 시점에 실행됨
  - `GenerationType.IDENTITY` 전략을 사용할 때 예외적으로 즉시 INSERT가 발생하는 경우

```java
@Id
@GeneratedValue(strategy = GenerationType.IDENTITY)
private Long id;
// DB가 식별자(기본키) 를 생성
// JPA는 엔티티를 DB에 넣기 전까지는 id 값을 알 수 없음
// save() → 즉시 INSERT SQL 실행
// DB에서 auto_increment된 id 값을 가져와서 엔티티에 채움
// 이후 flush/commit 때 다시 INSERT 하지 않음
```

```java
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE) // or TABLE
private Long id;
// DB 시퀀스에서 다음 값을 미리 가져옴
// Hibernate는 @SequenceGenerator 설정을 보고 시퀀스 조회 쿼리를 날림 (select nextval(...))
// ID를 미리 받아오면 INSERT를 지연시킬 수 있으므로 save() 시점에는 insert 안 됨
// flush 또는 트랜잭션 커밋 시점에만 insert 수행됨
// 커밋: @Transactional이 붙은 서비스 메서드가 정상 종료 시
// commit: 트랜잭션 메서드 종료 시
// flush: 변경 내용이 쿼리 결과에 반영되도록 JPQL 실행 시
```

### Exception과 Logging

- `throw exception`: 사용자 관점의 “피드백” 목적
  - 클라이언트(사용자 또는 API 소비자)에게 “무엇이 잘못되었는지”를 알려줌
    - 이메일 중복 → “이미 사용 중인 이메일입니다.”
    - 인증 실패 → “로그인이 필요합니다.”
    - 서버 과부하 → “잠시 후 다시 시도해주세요.”
  - 응답의 일부로 사용자에게 전달
    - View 기반 → 화면에 메시지 표시
    - REST API → JSON 응답 + HTTP 상태코드
    - 사용자 친화적 메시지 (이모지나 설명 포함 가능)
    - 내부 구현 정보(DB 구조, 예외 스택 등)는 절대 노출하지 않음

```java
if (userRepository.existsByEmail(email)) {
    throw new CustomException(ErrorCode.DUPLICATE_EMAIL);
}
```

- `log`: 내부 관점의 “기록/추적” 목적
  - 운영자나 개발자가 사후에 문제를 파악하기 위한 기록
  - 사용자에게는 노출되지 않음 (서버 내부 기록)
  - 예외 객체(e)를 함께 출력해 stack trace 확보
  - 로그 레벨로 심각도 구분:
    - log.debug() → 디버깅용
    - log.info() → 정상 흐름 정보
    - log.warn() → 잠재적 문제
    - log.error() → 실제 장애/예외 상황

```java
catch (Exception e) {
    log.error("오류 발생", e);
    throw new CustomException(ErrorCode.GEMINI_API_ERROR, e);
}
```

### `@JsonValue`

- 직렬화 (Java 객체 → JSON 문자열)
  - FortuneType.OVERALL 객체를 JSON으로 변환할 때, 일반적인 Enum 이름("OVERALL") 대신, @JsonValue가 붙은 필드의 값("overall")을 사용
  - 역직렬화 (JSON 문자열 → Java 객체)
    - JSON 문자열에서 "overall"이라는 값을 읽었을 때, Jackson은 이 문자열을 Enum의 이름으로 매핑하는 대신, Enum 상수 중 @JsonValue 필드 값이 "overall"인 상수를 찾아 매핑(즉, FortuneType.OVERALL을 찾아냄)

```java
@Getter
@RequiredArgsConstructor
public enum FortuneType {
  OVERALL("🔮", "종합", "overall", true),

  @JsonValue
  private final String jsonKey;
}
```

### from(), to()

- form.toRequest();
  - Form이 Request에 대한 의존을 갖게 됨
  - Form의 역할(입력 유효성 검사)이 아닌, 서비스 계층 객체를 만드는 역할까지 맡게 됨

```java
class Form {
    private String name;
    private int age;

    public Request toRequest() {
        return new Request(this.name, this.age);
    }
}
```

- request.from(form);
  - 서비스 레이어(비즈니스 로직)가 필요로 하는 데이터를 정의
  - 변환 책임을 갖고, 필요한 레이어 DTO나 Entity로 만들어 줌
  - Request가 자신을 만드는 모든 방법을 관리(응집도 향상)

```java
class Request {
    private String name;
    private int age;

    public static Request from(Form form) {
        return new Request(form.getName(), form.getAge());
    }
}
```

### 객체 생성 방식

- Entity → 정적 팩토리 메서드
  - 생성 과정이 복잡하고 검증이 필요
  - JPA 때문에 기본 생성자 필수 (protected) → public 생성자 열면 검증 우회 가능
- 검증 필요 → 정적 팩토리 메서드
- DTO → 생성자
- 단순 전달 → 생성자
- 복잡함 → Builder

#### Entity 생성 패턴

1. create (생성)

```java
public static FortuneCategory create(FortuneType fortuneType, Integer displayOrder) {
   FortuneCategory category = new FortuneCategory();
   category.fortuneType = fortuneType;
   category.displayOrder = displayOrder;
   return category;
}
```

2. of (단순 변환)

```java
public static FortuneCategory of(FortuneType fortuneType) {
   FortuneCategory category = new FortuneCategory();
   category.fortuneType = fortuneType;
   return category;
}
```

3. from (타입 변환)

```java
public static FortuneCategory from(String typeCode) {
   FortuneType type = FortuneType.fromCode(typeCode);
   return FortuneCategory.of(type);
}
```

4. builder (복잡한 경우)

```java
@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@Builder
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class FortuneCategory {

   @Id
   @GeneratedValue(strategy = GenerationType.IDENTITY)
   private Integer id;

   @Enumerated(EnumType.STRING)
   private FortuneType fortuneType;

   private Integer displayOrder;
   private Boolean enabled;
}

// 사용
FortuneCategory category = FortuneCategory.builder()
   .fortuneType(FortuneType.LOVE)
   .displayOrder(1)
   .enabled(true)
   .build();
```

#### DTO 생성 패턴

1. 생성자

```java
@Getter
@AllArgsConstructor
public class FortuneTypeResponse {
    private Integer id;
    private String name;
    private String emoji;
    private String code;
}

FortuneTypeResponse response = new FortuneTypeResponse(1, "종합", "🔮", "overall");
```

2. Builder 패턴

```java
@Getter
@Builder
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class FortuneResult {
    private Long id;
    private Member member;
    private String title;
    private Integer resultYear;
    // ... 많은 필드들
}

// 사용
FortuneResult result = FortuneResult.builder()
    .member(member)
    .title("운세")
    .resultYear(2025)
    .build();
```

#### 왜 JPA는 기본 생성자가 필요한가?

```java
// 1. DB에서 조회
// SELECT * FROM member WHERE id = 1;

// 2. JPA가 내부적으로 하는 일
Member member = new Member();  // 리플렉션으로 기본 생성자 호출(일반적으로는 private 필드에 접근 못 함, 리플렉션은 강제로 접근 가능)
member.setEmail("test@email.com");  // 필드에 값 주입
member.setPassword("encrypted");
member.setRole(MemberRole.USER);

// 3. 반환
return member;
```

#### AccessLevel.PROTECTED를 쓰는 이유

지연 로딩 동작 시 프록시 객체 생성

```java
@Entity
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member {
    @Id
    private Long id;

    private String email;
}

// Hibernate가 내부적으로 만드는 프록시
class Member$HibernateProxy extends Member {

    protected Member$HibernateProxy() {
        super();  // protected라서 호출 가능
    }

    @Override
    public String getEmail() {
        // 실제 DB에서 조회
        return loadRealEntity().getEmail();
    }
}
```

```java
@Entity
public class Order {
    @ManyToOne(fetch = FetchType.LAZY)
    private Member member;
}

// 조회
Order order = orderRepository.findById(1L).orElseThrow();

// member는 프록시 객체 (아직 DB 조회 안 함)
Member memberProxy = order.getMember();
// 실제 타입: Member$HibernateProxy (Member를 상속)

// 실제 사용 시점에 DB 조회
String email = memberProxy.getEmail();  // 이때 SELECT 쿼리 실행
```

### spring security 과정

1. 로그인 요청
2. Filter가 요청 받음

```java
// UsernamePasswordAuthenticationFilter
public Authentication attemptAuthentication(
        HttpServletRequest request,
        HttpServletResponse response) {

    // 요청에서 username, password 추출
    String username = request.getParameter("username");
    String password = request.getParameter("password");

    // 인증 전 토큰 생성 (사용자 입력값 담기)
    UsernamePasswordAuthenticationToken authRequest =
        new UsernamePasswordAuthenticationToken(username, password);

    // AuthenticationManager에게 인증 요청
    return this.getAuthenticationManager().authenticate(authRequest);
}
```

3. AuthenticationManager가 인증 처리

```java
// ProviderManager (AuthenticationManager 구현체)
public Authentication authenticate(Authentication authentication) {

    // 여러 AuthenticationProvider 중 적절한 것을 찾아서 위임
    for (AuthenticationProvider provider : getProviders()) {
        if (provider.supports(authentication.getClass())) {
            // Provider에게 실제 인증 처리 위임
            return provider.authenticate(authentication);
        }
    }
}
```

4. AuthenticationProvider가 실제 인증 수행

```java
// DaoAuthenticationProvider
public Authentication authenticate(Authentication authentication) {

    String username = authentication.getName();
    String password = authentication.getCredentials().toString();

    // UserDetailsService 호출하여 DB에서 사용자 조회
    UserDetails user = userDetailsService.loadUserByUsername(username);

    // 비밀번호 검증
    if (!passwordEncoder.matches(password, user.getPassword())) {
        throw new BadCredentialsException("비밀번호 불일치");
    }

    // 인증 성공 시, 인증된 토큰 생성
    UsernamePasswordAuthenticationToken result =
        new UsernamePasswordAuthenticationToken(
            user,                      // UserDetails
            null,                      // 비밀번호는 null 처리
            user.getAuthorities()      // 권한 목록
        );

    return result;
}
```

5. UserDetailsService가 DB 조회

```java
@Service
public class CustomUserDetailsService implements UserDetailsService {

    @Override
    public UserDetails loadUserByUsername(String username) {
        // DB에서 사용자 조회
        User user = userRepository.findByEmail(username)
            .orElseThrow(() -> new UsernameNotFoundException("사용자 없음"));

        // UserDetails로 변환하여 반환
        return new CustomUserDetails(user);
    }
}
```

6. SecurityContext에 저장

```java
// Filter로 돌아와서
protected void successfulAuthentication(
        HttpServletRequest request,
        HttpServletResponse response,
        Authentication authResult) {

    // SecurityContext에 인증 정보 저장
    SecurityContextHolder.getContext().setAuthentication(authResult);

    // 이제 어디서든 사용 가능!
    // @AuthenticationPrincipal CustomUserDetails userDetails
}
```

### 검증 로직

#### 1. Controller

- HTTP 관련 검증
- 세션 체크, 인증 확인
- 목적: 웹 요청의 문제를 빠르게 응답

```java
@PostMapping
public ResponseEntity<Map<String, Object>> save(
    @AuthenticationPrincipal CustomUserDetails userDetails,
    @SessionAttribute(name = "birthInfo", required = false) BirthInfoForm birthInfo,
    @Valid @RequestBody SaveFortuneRequest request
) {
    if (birthInfo == null) {
    // 세션 검증 (Controller 책임)
    }

    try {
    } catch (IllegalArgumentException e) {
      // 비즈니스 검증 예외
    } catch (Exception e) {
      // 시스템 예외
    }
}
```

#### 2. DTO

- 입력값 형식 검증
- `@NotNull`, `@Min`, `@Max`

```java
public record SaveFortuneRequest(
    @NotNull(message = "운세 옵션 정보는 필수입니다.")
    FortuneOptionForm option,

    @NotEmpty(message = "운세 결과는 필수입니다.")
    List<FortuneResponseDto> responses,

    @NotNull(message = "운세 연도는 필수입니다.")
    @Min(value = 2000, message = "운세 연도는 2000년 이상이어야 합니다.")
    @Max(value = 2100, message = "운세 연도는 2100년 이하여야 합니다.")
    Integer fortuneResultYear
) {
}
```

#### 3. Service

- 비즈니스 로직 검증
- 중복 체크, 권한 체크, 개수 제한

```java
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class FortuneService {

    private static final int MAX_SAVE_COUNT = 5;

    private final FortuneResultRepository fortuneResultRepository;

    @Transactional
    public void save(Member member, SaveFortuneRequest request, BirthInfoForm birthInfo) {
        // 비즈니스 규칙 검증
        validateBusinessRules(member, request);

        FortuneResult fortuneResult = FortuneResult.create(member, request, birthInfo);
    }

    private void validateBusinessRules(Member member, SaveFortuneRequest request) {
        // 회원 검증
        if (member == null || !member.isActive()) {
            throw new IllegalArgumentException("유효하지 않은 회원입니다.");
        }

        // 중복 저장 검증
        if (isDuplicateFortune(member, request)) {
            throw new IllegalArgumentException("이미 동일한 운세가 저장되어 있습니다.");
        }

        // 저장 개수 제한 검증
        if (isExceedMaxSaveCount(member)) {
            throw new IllegalArgumentException("저장 가능한 운세 개수를 초과했습니다.");
        }
    }

    private boolean isDuplicateFortune(Member member, SaveFortuneRequest request) {
        return fortuneResultRepository.existsByMemberAndResultYearAndPeriodType(
            member,
            request.getFortuneResultYear(),
            request.getOption().getPeriod()
        );
    }

    private boolean isExceedMaxSaveCount(Member member) {
        long count = fortuneResultRepository.countByMemberAndIsActiveTrue(member);
        return count >= MAX_SAVE_COUNT;
    }
}
```

#### 4. Entity

- 목적: 어떤 경로로 호출되든 도메인 규칙 보장
- 도메인 규칙 검증
- 필수값 체크, 날짜 유효성, 상태 일관성

```java
@Entity
public class FortuneResult extends BaseTimeEntity {

    // ... 필드들

    public static FortuneResult create(
        Member member,
        SaveFortuneRequest request,
        BirthInfoForm birth
    ) {
        // ✅ 엔티티 생성 시 필수값 검증
        validateInputs(member, request, birth);

        FortuneResult result = new FortuneResult();
        result.member = member;
        result.title = generateTitle(request);
        result.resultYear = request.getFortuneResultYear();
        result.gender = birth.getGender();
        result.birthDate = createBirthDate(birth);
        result.birthTimeZone = birth.getTime();
        result.birthRegion = birth.getCity();
        result.aiType = request.getOption().getAi();
        result.periodType = request.getOption().getPeriod();

        return result;
    }

    private static void validateInputs(Member member, SaveFortuneRequest request, BirthInfoForm birth) {
        if (member == null) {
            throw new IllegalArgumentException("회원 정보는 필수입니다.");
        }
        if (request == null) {
            throw new IllegalArgumentException("운세 요청 정보는 필수입니다.");
        }
        if (birth == null) {
            throw new IllegalArgumentException("생년월일 정보는 필수입니다.");
        }
        if (birth.getYear() == null || birth.getMonth() == null || birth.getDay() == null) {
            throw new IllegalArgumentException("생년월일은 필수입니다.");
        }
    }

    private static LocalDate createBirthDate(BirthInfoForm birth) {
        try {
            return LocalDate.of(birth.getYear(), birth.getMonth(), birth.getDay());
        } catch (DateTimeException e) {
            throw new IllegalArgumentException(
                String.format("유효하지 않은 생년월일입니다: %d-%d-%d",
                    birth.getYear(), birth.getMonth(), birth.getDay()),
                e
            );
        }
    }

    private static String generateTitle(SaveFortuneRequest request) {
        return String.format("%d년 %s %s",
            request.getFortuneResultYear(),
            request.getOption().getPeriod().getDisplayName(),
            request.getFortuneTypesAsString()
        );
    }
}
```

### CasCade

- 연관관계 편의 메서드 + Cascade 설정하면 부모만 save해도 자식까지 자동 INSERT

```java
@Entity
public class FortuneResult {

    // ✅ Cascade.ALL 설정
    @OneToMany(mappedBy = "fortuneResult", cascade = CascadeType.ALL)
    private List<FortuneResultCategory> categories = new ArrayList<>();

    // ✅ 연관관계 편의 메서드
    public void addCategory(FortuneResultCategory category) {
        this.categories.add(category);      // 1. 리스트에 추가
        category.setFortuneResult(this);    // 2. 양방향 관계 설정
    }
}
```

```java
@Transactional
public Long save(Member member, SaveFortuneRequest request, BirthInfoForm birth) {
    // 1. FortuneResult 생성 (아직 저장 안 됨)
    FortuneResult result = FortuneResult.create(member, request, birth);

    // 2. Categories 추가 (메모리에만 존재)
    List<FortuneCategory> categories = fortuneCategoryRepository
        .findByFortuneTypeIn(fortuneTypes);

    categories.forEach(category -> {
        FortuneResultCategory resultCategory =
            FortuneResultCategory.create(result, category);
        result.addCategory(resultCategory);  // ← 연관관계 편의 메서드
    });

    // 3. ✅ result만 저장!
    fortuneResultRepository.save(result);
    // → Cascade 덕분에 categories도 자동으로 INSERT됨!

    return result.getId();
}
```

```sql
-- ① FortuneResult INSERT
INSERT INTO fortune_result (member_id, title, result_year, ...)
VALUES (1, '2024년 월별 운세', 2024, ...);
-- id = 1 생성

-- ② FortuneResultCategory INSERT (Cascade로 자동!)
INSERT INTO fortune_result_category (fortune_result_id, fortune_category_id)
VALUES (1, 1);  -- COMPREHENSIVE

INSERT INTO fortune_result_category (fortune_result_id, fortune_category_id)
VALUES (1, 2);  -- WEALTH

INSERT INTO fortune_result_category (fortune_result_id, fortune_category_id)
VALUES (1, 3);  -- HEALTH
```

#### 양방향 연관관계 편의 메서드

```java
@Entity
public class FortuneResult {
    @OneToMany(mappedBy = "fortuneResult", cascade = CascadeType.ALL)
    private List<FortuneResultCategory> categories = new ArrayList<>();
}

@Entity
public class FortuneResultCategory {
    @ManyToOne
    @JoinColumn(name = "fortune_result_id", nullable = false) // ← FK, NOT NULL
    private FortuneResult fortuneResult;
}

    // JPA가 하는 일:
    // 1. fortuneResult 필드를 확인
    // 2. fortuneResult.getId() 호출
    // 3. 그 ID 값을 fortune_result_id 컬럼에 저장
```

```java
FortuneResult result = new FortuneResult();
FortuneResultCategory category = new FortuneResultCategory();

// ❌ 부모 쪽만 설정 (한쪽 관계만 설정)
result.getCategories().add(category);

// ❌ 자식 쪽 설정 누락!
// category.setFortuneResult(result);  ← 이걸 안 함!

fortuneResultRepository.save(result);
```

```sql
-- FortuneResult INSERT
INSERT INTO fortune_result (...) VALUES (...);
-- id = 1 생성

-- FortuneResultCategory INSERT
INSERT INTO fortune_result_category
(fortune_result_id, fortune_category_id)
VALUES (NULL, 1);  -- ❌ fortune_result_id가 NULL!

-- 💥 에러 발생!
-- Column 'fortune_result_id' cannot be null
-- 또는 FK constraint violation
```

```java
@Entity
public class FortuneResult {

    @OneToMany(mappedBy = "fortuneResult", cascade = CascadeType.ALL)
    private List<FortuneResultCategory> categories = new ArrayList<>();

    // ✅ 연관관계 편의 메서드
    public void addCategory(FortuneResultCategory category) {
        this.categories.add(category);      // 1. 부모 쪽 설정 (읽기 전용)
        category.setFortuneResult(this);    // 2. 자식 쪽 설정 (DB 반영!) ← 핵심!
    }
}
```

#### Id만 저장하는 경우

```java
@Column(name = "fortune_result_id")
private Long fortuneResultId;
```

```java
// 매번 Repository로 조회
// 1. 카테고리 조회
FortuneResultCategory category = categoryRepository.findById(1L);

// 2. ID 꺼내기
Long fortuneResultId = category.getFortuneResultId();  // 123

// 3. 그 ID로 다시 조회
FortuneResult result = fortuneResultRepository.findById(fortuneResultId);

// 4. 제목 얻음
String title = result.getTitle();  // "2025년 운세"
```

```java
// cascade 불가능
FortuneResult result = new FortuneResult();
FortuneResultCategory category = new FortuneResultCategory();
category.setFortuneResultId(???);  // result의 ID가 아직 없음! 💥

fortuneResultRepository.save(result); // ID 생성됨
category.setFortuneResultId(result.getId()); // 이제 설정
categoryRepository.save(category); // 따로 저장
```

```java
@ManyToOne
private FortuneResult fortuneResult;
```

```java
// repository 조회 없이 바로 객체 데이터에 접근 가능
// 1. 카테고리 조회
FortuneResultCategory category = categoryRepository.findById(1L);

// 2. 제목 얻음
String title = category.getFortuneResult().getTitle(); // "2025년 운세"
```

```java
// cascade 가능
FortuneResult result = new FortuneResult();
FortuneResultCategory category = new FortuneResultCategory();
category.setFortuneResult(result); // 객체 바로 설정

result.addCategory(category);
fortuneResultRepository.save(result); // Cascade로 category도 자동 저장!
```

### WithMockCustomUser 생성

1. WithMockCustomUser.java

```java
@Retention(RetentionPolicy.RUNTIME)
// 어노테이션이 런타임에도 유지되도록 설정
@WithSecurityContext(factory = WithMockCustomUserSecurityContextFactory.class)
// SecurityContext를 만들 Factory 클래스 지정
public @interface WithMockCustomUser {
  // 커스텀 어노테이션 정의

    long id() default 1L;
    // @WithMockCustomUser(id = 2L) 이런 식으로 사용 가능

    String email() default "test@test.com";

    String nickname() default "테스터";
}
```

2. WithMockCustomUserSecurityContextFactory.java

```java
public class WithMockCustomUserSecurityContextFactory
    implements WithSecurityContextFactory<WithMockCustomUser> {

    @Override
    public SecurityContext createSecurityContext(WithMockCustomUser annotation) {

        // 1. Member 객체 생성
        Member member = new Member(
            annotation.email(),
            "encodedPassword",
            annotation.nickname()
        );

        // 2. ID 설정 (private 필드라서 Reflection 사용)
        ReflectionTestUtils.setField(member, "id", annotation.id());

        // 3. CustomUserDetails 생성
        CustomUserDetails userDetails = new CustomUserDetails(member);

        // 4. Authentication 객체 생성
        // 인증이 완료된 상태를 가정하므로 검증 과정 생략
        Authentication auth = new UsernamePasswordAuthenticationToken(
            userDetails,                    // Principal
            null,      // Credentials, 보안상의 이유로 credentials (비밀번호)를 null로 설정
            userDetails.getAuthorities()    // Authorities
        );

        // 5. SecurityContext 생성 및 Authentication 설정
        SecurityContext context = SecurityContextHolder.createEmptyContext();
        context.setAuthentication(auth);

        return context;
    }
}
```

#### UsernamePasswordAuthenticationToken

```java
new UsernamePasswordAuthenticationToken(
    request.getEmail(),      // 1️⃣ principal: "test@test.com"
    request.getPassword()    // 2️⃣ credentials: "1234"
    // 3️⃣ authorities 없음 → 2개 파라미터 생성자 호출
)
// authenticated = false

new UsernamePasswordAuthenticationToken(
    userDetails,                  // 1️⃣ principal: CustomUserDetails 객체
    userDetails.getPassword(),    // 2️⃣ credentials: "$2a$10$..."
    userDetails.getAuthorities()  // 3️⃣ authorities: [ROLE_USER]
    // 3개 파라미터 생성자 호출
)
// authenticated = true
```

### `@Valid` 검증 실패

1. BindingResult가 있는 경우

```java
@Controller
public class SignupController {

    @PostMapping("/signup")
    public String signup(
        @Valid @ModelAttribute SignupForm signupForm, // @Valid
        BindingResult bindingResult
    ) {
        if (bindingResult.hasErrors()) { // 예외 안 던지고 여기서 처리
            return "auth/signup"; // 폼으로 돌아감
        }

        authService.signup(...);
        return "redirect:/";
    }
}
```

2. BindingResult가 없는 경우

- Validation 실패 → MethodArgumentNotValidException 발생
- Controller 메서드 실행 안 됨
- `@RestControllerAdvice`가 예외 처리

```java
public ResponseEntity<?> save(
    @Valid @RequestBody SaveFortuneRequest request  // BindingResult 없음!
) {
    fortuneService.save(...);
    return ResponseEntity.ok(...);
}
```

```java
// @RestControllerAdvice
@ExceptionHandler(MethodArgumentNotValidException.class)
public ResponseEntity<ApiResponse> handleValidation(
    MethodArgumentNotValidException ex
) {
  log.warn("[API Validation 실패] {}", ex.getMessage());

  Map<String, String> errors = new HashMap<>();
  ex.getBindingResult().getFieldErrors().forEach(error ->
      errors.put(error.getField(), error.getDefaultMessage())
  );

  return ResponseEntity.badRequest()
                        .body(
                            ApiResponse.error(ErrorCode.ARGUMENT_NOT_VALID.getMessage(), errors));
}
```

### 테스트하기 좋은 코드

1. 생성자 주입 사용

- 객체를 직접 생성할 수 있게 해서 단위 테스트가 빠르고 쉬워짐

2. final 필드로 불변성 보장

- final은 생성 후 변경 불가 → 테스트 중 상태가 안 바뀜 → 예측 가능하고 안전함

3. 의존성을 외부에서 주입

- 의존성을 Mock으로 교체 가능

4. 설정값도 생성자로 주입

- 테스트마다 다른 값 사용 가능 → 다양한 시나리오 테스트 쉬움

5. static 메서드 최소화

- static은 Mock 불가 → 제어 불가능한 값(시간, 랜덤)을 제어 가능하게 → 안정적인 테스트

### Entity Fixture

- 테스트에 필요한 엔티티 객체를 미리 생성해두는 패턴

```java
public class UserFixture {

    private UserFixture() {}

    public static User createUser() {
        return User.builder()
            .name("홍길동")
            .email("hong@example.com")
            .age(30)
            .build();
    }

    public static User createUser(String name, String email) {
        return User.builder()
            .name(name)
            .email(email)
            .age(30)
            .build();
    }

    public static User createAdminUser() {
        return User.builder()
            .name("관리자")
            .email("admin@example.com")
            .role(Role.ADMIN)
            .build();
    }
}
```

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService

    @Test
    void 사용자_생성_테스트() {
        User user = UserFixture.createUser();

        User savedUser = userRepository.save(user);

        assertNotNull(savedUser.getId());
        assertEquals("홍길동", savedUser.getName());
    }

    @Test
    void 관리자_권한_테스트() {
        User admin = UserFixture.createAdminUser();

        assertTrue(admin.isAdmin());
    }
}
```

### N+1문제(JPA)

- 보통 특정 엔티티 목록을 조회한 후, 루프를 돌면서 연관된 엔티티에 접근할 때 성능 문제 발생

```java
// 1. 특정 회원의 모든 운세 결과를 조회 (쿼리 1번)
// SQL: SELECT * FROM fortune_result WHERE member_id = ?
List<FortuneResult> results = fortuneResultRepository.findAllByMemberId(memberId);

// 2. 각 운세 결과에 포함된 카테고리 정보에 접근 (결과가 N개일 경우 N번의 추가 쿼리 발생)
for (FortuneResult result : results) {
    // getCategories()는 LAZY 로딩이므로, 실제 데이터에 접근하는 시점에 쿼리가 실행됨
    // SQL: SELECT * FROM fortune_category WHERE id = ? (N번 실행)
    String firstCategoryName = result.getCategories().get(0).getFortuneCategory().getName(); // N+1 문제 발생 지점
}
```

```java
// FortuneResultCategory
@ManyToOne
private FortuneResult fortuneResult;
// FK가 있으므로 FortuneResultId 값으로 조회 가능

// FortuneCategory
@Id
private int id;
private FortuneType fortuneType;
// FK 없으므로 FortuneResultCategoryId 값으로 조회 불가능
// → FortuneCategory 조회 시, FortuneCategoryId마다 조회 쿼리 발생
```

#### 해결 방법

1. `@BatchSize`

- LAZY 로딩할 때, 한 번에 몇 개씩 묶어서 가져올까
  - 프록시 초기화할 때, 대기 중인 프록시들을 최대 n개까지 모아서 IN 쿼리로 한 번에 가져옴
- 전역 설정 후, 필요 시 개별 설정
- Fetch Join보다는 약간 느림
- 고려 사항
  - 너무 작으면 (10):
    - 쿼리가 많이 나감
    - 예: 1000개 조회 시 → 100번 쿼리
  - 너무 크면 (1000):
    - IN 절이 너무 길어짐
    - DB에 부담
    - 메모리 사용 증가

```yml
spring:
  jpa:
    properties:
      hibernate:
        default_batch_fetch_size: 100 # 모든 엔티티에 적용
```

```java
@Entity
public class FortuneResultCategory {
    @ManyToOne(fetch = FetchType.LAZY)
    @BatchSize(size = 100)
    private FortuneCategory fortuneCategory;
}

/**
 * 설정 전
FortuneCategory를 6번 조회
SELECT * FROM fortune_category WHERE id = 2
SELECT * FROM fortune_category WHERE id = 3
SELECT * FROM fortune_category WHERE id = 4
SELECT * FROM fortune_category WHERE id = 5
SELECT * FROM fortune_category WHERE id = 7
SELECT * FROM fortune_category WHERE id = 8

  * 설정 후
FortuneCategory를 1번에 조회
SELECT * FROM fortune_category
WHERE id IN (2, 3, 4, 5, 7, 8)
*/
```

2. `Fetch Join`

- 연관된 엔티티를 한 번의 쿼리로 함께 가져옴
- 성능이 중요한 API에서 사용

```java
@Query("SELECT DISTINCT fr FROM FortuneResult fr " +
       "LEFT JOIN FETCH fr.categories c " +
       "LEFT JOIN FETCH c.fortuneCategory " +
       "WHERE fr.member.id = :memberId AND fr.isActive = true")
List<FortuneResult> findAllByMemberIdWithCategories(@Param("memberId") Long memberId);

/**
SELECT
    fr.id,      c.id,       fc.id
    fr.title,   c.id,       fc.fortune_type
FROM fortune_result fr
JOIN fortune_result_category c ON fr.id = c.fortune_result_id
JOIN fortune_category fc ON c.fortune_category_id = fc.id

-- 결과 (카테시안 곱)
fr.id | fr.title  | c.id | fc.id | fc.type
------|-----------|------|-------|--------
1     | "2025운세" | 1    | 2     | LOVE
1     | "2025운세" | 2    | 3     | MONEY    ← FortuneResult 중복!
1     | "2025운세" | 3    | 4     | HEALTH   ← FortuneResult 중복!
*/
```

- 카테시안 곱

  - 메모리 증가 가능
  - 네트워크 오버헤드
  - MultipleBagFetchException
    - Bag = 순서 없는 컬렉션 (중복 허용)
  - 추가 작업 필요
    - 8 rows → 1개의 FortuneResult 객체로 변환

```java
// OneToMany가 2개 이상일 때
@Query("SELECT fr FROM FortuneResult fr
        JOIN FETCH fr.categories
        JOIN FETCH fr.items")  // ← MultipleBagFetchException!

// 데이터가 엄청 많을 때
// FortuneResult 1000개 × Category 평균 8개 = 8000 rows
// → 메모리 부족 가능
```

- MultipleBagFetchException
- 해결 방법
  - 쿼리 2번 작성
    - `@Query("SELECT fr FROM FortuneResult fr JOIN FETCH fr.categories")`
    - `@Query("SELECT fr FROM FortuneResult fr JOIN FETCH fr.items")`
  - `Set`으로 컬렉션 타입 변경
    - `Set`은 중복을 허용하지 않는 자료구조이므로, Hibernate가 Cartesian 곱으로 인해 발생한 중복 데이터를 명확히 식별하고 제거할 수 있음
    - `List`는 중복을 허용하기 때문에, Hibernate는 JOIN으로 발생한 중복이 의도된 것인지 아닌지 판단할 수 없어 예외를 발생

```java
@Entity
public class FortuneResult {
    @OneToMany
    private List<Category> categories;  // Bag 1

    @OneToMany
    private List<Item> items;           // Bag 2
}

@Query("SELECT fr FROM FortuneResult fr
        JOIN FETCH fr.categories
        JOIN FETCH fr.items")
```

```sql
SELECT fr.*, c.*, i.*
FROM fortune_result fr
JOIN fortune_result_category c ON ...
JOIN fortune_result_item i ON ...


-- 데이터
FortuneResult 1개
├─ categories: [C1, C2, C3]
└─ items: [I1, I2]

-- 데이터베이스 결과 (카테시안 곱)
fr.id | c.id | i.id
------|------|-----
1     | C1   | I1
1     | C1   | I2   ← C1이 I1, I2와 각각 조합
1     | C2   | I1
1     | C2   | I2
1     | C3   | I1
1     | C3   | I2
------|------|-----
6 rows!
```

```java
// Hibernate: "이 6개 row를 어떻게 변환하지?"

// Row 1: FR(1) + C1 + I1
//   → categories에 C1 추가, items에 I1 추가

// Row 2: FR(1) + C1 + I2
//   → categories에 C1 추가? (이미 있는데?)
//   → items에 I2 추가

// Row 3: FR(1) + C2 + I1
//   → categories에 C2 추가
//   → items에 I1 추가? (이미 있는데?)

// Hibernate: "뭐가 뭔지 모르겠어! 에러!"
// → MultipleBagFetchException 발생! 💥
```

```txt
데이터
FortuneResult(id=1, title="2025운세")
├─ categories
│   ├─ Category(id=1, type=LOVE)
│   ├─ Category(id=2, type=MONEY)
│   └─ Category(id=3, type=HEALTH)
└─ items
    ├─ Item(id=1, content="좋음")
    └─ Item(id=2, content="나쁨")

JOIN 결과 (6 rows)
Row 1: FR(1) + Category(LOVE)   + Item(좋음)
Row 2: FR(1) + Category(LOVE)   + Item(나쁨)  ← LOVE 중복
Row 3: FR(1) + Category(MONEY)  + Item(좋음)
Row 4: FR(1) + Category(MONEY)  + Item(나쁨)  ← MONEY 중복
Row 5: FR(1) + Category(HEALTH) + Item(좋음)
Row 6: FR(1) + Category(HEALTH) + Item(나쁨)  ← HEALTH 중복
```

```java
// 목표: 이렇게 만들고 싶음
FortuneResult(
  id=1,
  categories=[LOVE, MONEY, HEALTH],  // 3개
  items=[좋음, 나쁨]                  // 2개
)

// 문제: 6개 row에서 어떻게?
// Row 1 처리 → categories=[LOVE], items=[좋음]
// Row 2 처리 → categories=[LOVE, LOVE?], items=[좋음, 나쁨]  ← LOVE 중복?
// Row 3 처리 → categories=[LOVE, LOVE?, MONEY], items=[좋음, 나쁨, 좋음?]  ← 좋음 중복?

// Hibernate: "List는 중복 허용하는데, 이게 진짜 중복인지 같은 객체인지 모르겠어!"
// → 포기하고 에러 발생!
```

- Distinct의 역할
  - SQL의 `DISTINCT`와는 다르게 동작
    - SQL에 `DISTINCT`가 적용되더라도, JOIN된 컬럼들 때문에 row 데이터가 달라져서 중복이 제거되지 않음(이미 카테시안 곱 실행)
  - JPQL의 `DISTINCT`는 추가적으로, 애플리케이션 레벨에서 조회된 루트 엔티티(root entity)의 중복을 제거하는 기능을 보장

1. DISTINCT 없을 때

```java
@Query("SELECT fr FROM FortuneResult fr
        JOIN FETCH fr.categories")
List<FortuneResult> find();
```

```sql
SELECT fr.*, c.*
FROM fortune_result fr
JOIN fortune_result_category c ON fr.id = c.fortune_result_id

-- 데이터베이스 결과
fr.id | fr.title  | c.id | c.type
------|-----------|------|--------
1     | "2025운세" | 1    | LOVE
1     | "2025운세" | 2    | MONEY
1     | "2025운세" | 3    | HEALTH
```

```java
// Hibernate가 Java 객체로 변환
[
  FortuneResult(id=1, categories=[LOVE]),
  FortuneResult(id=1, categories=[MONEY]),     // 중복!
  FortuneResult(id=1, categories=[HEALTH])     // 중복!
]
```

2. DISTINCT 있을 때

```java
@Query("SELECT DISTINCT fr FROM FortuneResult fr
        JOIN FETCH fr.categories")
List<FortuneResult> find();
```

```sql
SELECT fr.*, c.*
FROM fortune_result fr
JOIN fortune_result_category c ON fr.id = c.fortune_result_id
-- DISTINCT 없음!

--데이터베이스 결과
fr.id | fr.title  | c.id | c.type
------|-----------|------|--------
1     | "2025운세" | 1    | LOVE
1     | "2025운세" | 2    | MONEY
1     | "2025운세" | 3    | HEALTH
```

```java
// Hibernate가 Java 객체로 변환
// 1단계: DB에서 3 rows 받음
ResultSet:
  Row 1: FR(id=1), Category(LOVE)
  Row 2: FR(id=1), Category(MONEY)
  Row 3: FR(id=1), Category(HEALTH)

// 2단계: Hibernate가 메모리에서 처리
// "어? id=1이 3번 나왔네? DISTINCT 있으니까 하나로 합치자!"

// 3단계: 최종 결과
[
  FortuneResult(id=1, categories=[LOVE, MONEY, HEALTH])  // 하나로 합쳐짐!
]
// size = 1  ✅
```

- 일반 JOIN
  - 연관된 Entity는 LAZY 로딩 (나중에 N+1 발생할 수 있음)

```java
// 일반 JOIN
FortuneResult result = repository.find...();
result.getCategories();  // ← 여기서 추가 쿼리! (N+1)

// FETCH JOIN
FortuneResult result = repository.find...();
result.getCategories();  // ← 이미 로딩됨! (추가 쿼리 없음)
```

### `@EntityGraph` vs `@BatchSize`

- `@EntityGraph`

```java
@EntityGraph(attributePaths = {"categories", "items"})
Optional<FortuneResult> findById(Long id);
```

```sql
-- 한 방에 모든 걸 JOIN으로 가져오려고 시도!
-- List 2개를 동시에 JOIN 못 함 ❌
SELECT
    fr.*,
    c.*,   -- categories를 JOIN으로!
    i.*    -- items를 JOIN으로!
FROM fortune_result fr
LEFT JOIN fortune_result_category c ON c.fortune_result_id = fr.id
LEFT JOIN fortune_result_item i ON i.fortune_result_id = fr.id
WHERE fr.id = 1;
```

- `@BatchSize`

```java
// @EntityGraph 없음!
Optional<FortuneResult> findById(Long id);

@BatchSize(size = 10)
private List<FortuneResultCategory> categories;
```

```sql
-- 여러 쿼리로 나눠서 가져옴

-- 1번: FortuneResult만
SELECT * FROM fortune_result WHERE id = 1;

-- 2번: categories 접근할 때 (Lazy Loading)
SELECT * FROM fortune_result_category
WHERE fortune_result_id IN (1, 2, 3, ..., 10);  -- Batch로!

-- 3번: items 접근할 때 (Lazy Loading)
SELECT * FROM fortune_result_item
WHERE fortune_result_id IN (1, 2, 3, ..., 10);
```

#### 시각적 비교

- **@EntityGraph (한 방에 JOIN)**
  - List 2개를 동시에 JOIN 하면 **카테시안 곱** 발생
  - Hibernate가 막아버림 (MultipleBagFetchException)

```txt
┌──────────────┐
│ FortuneResult│
│     +        │  ← 한 번의 쿼리로
│  categories  │     모든 걸 JOIN!
│     +        │
│    items     │
└──────────────┘
      ↓
[단일 거대 쿼리]
```

- **@BatchSize (나눠서 가져오기)**
  - 쿼리를 나눠서 실행

```txt
┌──────────────┐
│ FortuneResult│ ← 1번 쿼리
└──────────────┘
↓
┌──────────────┐
│ categories │ ← 2번 쿼리 (Lazy)
└──────────────┘
↓
┌──────────────┐
│ items │ ← 3번 쿼리 (Lazy)
└──────────────┘
```

#### 코드 비교

- `@EntityGraph`

```java
// Repository
@EntityGraph(attributePaths = {"categories", "items"})
Optional<FortuneResult> findById(Long id);

// 사용
FortuneResult result = repository.findById(1L).get();
// ↑ 이 시점에 categories, items 전부 로딩됨! (JOIN 쿼리 1번)

result.getCategories();  // 이미 로딩됨 (쿼리 안 나감)
result.getItems();       // 이미 로딩됨 (쿼리 안 나감)
```

```sql
-- 딱 1번! (하지만 List 2개면 에러)
SELECT fr.*, c.*, i.*
FROM fortune_result fr
LEFT JOIN fortune_result_category c ...
LEFT JOIN fortune_result_item i ...
WHERE fr.id = 1;
```

- `@BatchSize`

```java
// Repository - @EntityGraph 없음!
Optional<FortuneResult> findById(Long id);

// Entity
@BatchSize(size = 10)
private List<FortuneResultCategory> categories;

@BatchSize(size = 10)
private List<FortuneResultItem> items;

// 사용
FortuneResult result = repository.findById(1L).get();
// ↑ 이 시점엔 FortuneResult만 로딩됨! (쿼리 1번)

result.getCategories();  // 이 시점에 쿼리 나감 (Lazy)
result.getItems();       // 이 시점에 쿼리 나감 (Lazy)
```

```sql
-- 1번: FortuneResult만
SELECT * FROM fortune_result WHERE id = 1;

-- 2번: categories 접근할 때(만약 여러 FortuneResult를 조회했다면 IN 절에 ID 목록이 들어감)
SELECT * FROM fortune_result_category
WHERE fortune_result_id IN (1);

-- 3번: items 접근할 때(만약 여러 FortuneResult를 조회했다면 IN 절에 ID 목록이 들어감)
SELECT * FROM fortune_result_item
WHERE fortune_result_id IN (1);
```

### `@EntityGraph` vs `Fetch Join`

- `@EntityGraph`

- 조건 간단함
- 정렬 필요 없음
- 1단계만 로딩

```java
// 1. ID로 조회
@EntityGraph(attributePaths = {"member", "categories"})
Optional<FortuneResult> findById(Long id);

// 2. 간단한 조건
@EntityGraph(attributePaths = {"member"})
Optional<FortuneResult> findByIdAndIsActiveTrue(Long id);

// 3. 전체 조회
@EntityGraph(attributePaths = {"writer"})
List<Post> findAll();
```

- `Fetch Join`
  - 2단계 로딩 (categories.fortuneCategory)
  - DISTINCT 필요
  - ORDER BY 필요
  - WHERE 조건 복잡

```java
// 1. 2단계 이상 로딩
@Query("SELECT f FROM FortuneResult f "
    + "JOIN FETCH f.categories c "
    + "JOIN FETCH c.fortuneCategory fc")

// 2. DISTINCT 필요(목록 조회 시, 일대다 관계)
@Query("SELECT DISTINCT f FROM FortuneResult f "
    + "JOIN FETCH f.items")

// 3. 정렬 필요
@Query("SELECT f FROM FortuneResult f "
    + "JOIN FETCH f.member "
    + "ORDER BY f.createdAt DESC")

// 4. 복잡한 WHERE
@Query("SELECT f FROM FortuneResult f "
    + "JOIN FETCH f.member m "
    + "WHERE m.status = 'ACTIVE' AND f.type IN :types")
```

#### 일대다 관계에서의 선택

1. 1개만 조회 (ID로 찾기)

- ID로 조회 → **FortuneResult 1개만** 나옴
- 그 1개에 딸린 categories, items 로딩
- **중복 없음!** (FortuneResult가 1개니까)

```java
@EntityGraph(attributePaths = {"categories", "items"})
Optional<FortuneResult> findById(Long id);

// FortuneResult(1) - Category(1)
// FortuneResult(1) - Category(2)
// FortuneResult(1) - Category(3)
```

2. 여러 개 조회 (List로 받기)

- 중복 발생 가능

```java
// Fetch Join + DISTINCT 필요!
@Query("SELECT DISTINCT fr FROM FortuneResult fr "
    + "LEFT JOIN FETCH fr.categories "
    + "WHERE fr.member.id = :memberId")
List<FortuneResult> findByMemberId(@Param("memberId") Long memberId);

// Distinct 없으면
// FortuneResult(1) - Category(1)
// FortuneResult(1) - Category(2) // 중복 발생
// FortuneResult(2) - Category(3)
// FortuneResult(2) - Category(4) // 중복 발생
```

### SELECT 쿼리가 발생한 이유

```java
// FortuneResultRepository
@EntityGraph(attributePaths = {"categories.fortuneCategory", "items"})
Optional<FortuneResult> findByIdAndMember_IdAndIsActiveTrue(Long fortuneId, Long memberId);


// EntityGraph가 실제로 N+1 문제를 방지하는지 검증하는 테스트
@Test
@DisplayName("EntityGraph로 items와 categories를 함께 조회한다 (N+1 없음)")
void findByIdAndMember_IdAndIsActiveTrue_FetchesItemsAndCategories() {
  // given
  FortuneResult saved = fortuneResultRepository.save(result);
  fortuneResultRepository.flush(); // DB에 실제로 저장

  entityManager.clear();
  // 영속성 컨텍스트(1차 캐시)를 초기화하여 DB에서 새로 조회하도록 강제함 → 이를 생략하면 캐시된 엔티티를 반환하므로 EntityGraph 동작을 정확히 검증할 수 없음

  // (repository.save 시, 영속성 컨텍스트(JPA가 엔티티를 관리하는 환경)에 캐시됨)

  // when
  Optional<FortuneResult> found = fortuneResultRepository
      .findByIdAndMember_IdAndIsActiveTrue(saved.getId(), member.getId());
  // 실제로 DB 조회 쿼리 실행

  // then
  assertThat(found).isPresent();
  FortuneResult foundResult = found.get();

  // 지연 로딩 없이 접근 가능
  assertThat(foundResult.getItems()).isNotEmpty();
  assertThat(foundResult.getCategories()).isNotEmpty();

  // 2단계 fetch 확인
  foundResult.getCategories().forEach(category -> {
    assertThat(category.getFortuneCategory()).isNotNull();
    assertThat(category.getFortuneCategory().getFortuneType()).isNotNull();
  });
}
```

```bash
Hibernate: select null,fc1_0.fortune_type from fortune_category fc1_0 where fc1_0.id=?
Hibernate: select null,fc1_0.fortune_type from fortune_category fc1_0 where fc1_0.id=?
Hibernate: select fr1_0.id,fr1_0.ai_type,fr1_0.birth_date,fr1_0.birth_region,fr1_0.birth_time_zone,fr1_0.calendar,c1_0.fortune_result_id,c1_0.id,c1_0.fortune_category_id,fc1_0.id,fc1_0.fortune_type,fr1_0.created_at,fr1_0.gender,fr1_0.is_active,i1_0.fortune_result_id,i1_0.id,i1_0.accuracy,i1_0.content,i1_0.created_at,i1_0.period_value,i1_0.updated_at,fr1_0.member_id,fr1_0.period_type,fr1_0.result_year,fr1_0.title,fr1_0.updated_at from fortune_result fr1_0 left join member m1_0 on m1_0.id=fr1_0.member_id left join fortune_result_category c1_0 on fr1_0.id=c1_0.fortune_result_id left join fortune_category fc1_0 on fc1_0.id=c1_0.fortune_category_id left join fortune_result_item i1_0 on fr1_0.id=i1_0.fortune_result_id where fr1_0.id=? and m1_0.id=? and fr1_0.is_active order by fc1_0.id,i1_0.period_value
```

- `select fortune_category` 쿼리는 N+1이 아니라, JPA가 FortuneResultCategory를 저장할 때 @manytoone 연관 엔티티(FortuneCategory)를 검증하려고 하는 과정에서 JPA가 FortuneCategory 엔티티를 '조회(validate)'하려고 발생한 SELECT입니다.
- Fixture 코드에서 CATEGORY_MAP에 미리 만들어 둔 FortuneCategory 엔티티들이 영속성 컨텍스트에 없어서 발생하는 쿼리

```java
static {
    CATEGORY_MAP = Map.of(
        FortuneType.OVERALL, FortuneCategory.create(1, FortuneType.OVERALL),
        ...
    );
}
```

- FortuneCategory.create(1, ...)는 DB에서 가져온 엔티티가 아니라, 단순히 new FortuneCategory(...) 한 것과 같은 **비영속 엔티티**
  - 메모리상에만 존재하고 영속성 컨텍스트에 관리되지 않음
- FortuneResultCategory.create(result, category) 호출 시, JPA는 FortuneResultCategory를 영속화하려고 할 때 내부적으로 다음을 수행
  - FortuneResultCategory는 @ManyToOne FortuneCategory 를 가짐
  - JPA는 연관된 Category가 영속 엔티티인지 확인해야 함
  - Category는 비영속이기 때문에 JPA는 Category.id가 유효한지 조회하려고 SELECT 실행

### Set과 `equals`/`hashCode`

- equals/hashCode 미구현 시 Object 기본 구현(참조 비교) 사용 → 같은 데이터여도 다른 객체면 Set에 중복 추가 가능

```java
// Set에 추가할 때
set.add(category1);
// hashCode() 확인 → equals() 확인 → 중복이면 추가 안함
```

#### 클래스 기반 hashCode

- 영속화 전후 hashCode가 동일하게 유지

```java
@Override
public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof FortuneResultCategory)) return false;
    FortuneResultCategory that = (FortuneResultCategory) o;
    return id != null && Objects.equals(id, that.id);
    // 영속화 전(id=null) 객체는 항상 다른 객체로 취급
}

@Override
public int hashCode() {
    return getClass().hashCode();
}
```

```java
// 1. Id로 설정 시
FortuneResultCategory category = new FortuneResultCategory();

// 1. Set에 추가 (id = null)
set.add(category);
// hashCode = 0 (null의 hash)
// Set 내부: {bucket[0] = category}

// 2. DB 저장 후 id 생김
entityManager.persist(...);  // id = 1L로 변경됨!

// 3. hashCode가 바뀜!
category.hashCode();  // 이제 1의 hash 값
// Set 내부에서는 여전히 bucket[0]에 있는데
// hashCode로 찾으면 bucket[1]을 찾음
// → Set이 자기가 가진 객체를 못 찾음!

set.contains(category);  // false!? (있는데도!)
set.remove(category);    // 삭제 안됨!
```

- 지연 로딩 시 생성되는 프록시 객체와 사용하면 equals()는 true이지만 hashCode()가 달라짐

```java
FortuneResultCategory real = new FortuneResultCategory();
real.setId(1L);

FortuneResultCategory proxy = entityManager.getReference(FortuneResultCategory.class, 1L);

// equals: instanceof를 사용하므로 → true (프록시도 FortuneResultCategory의 인스턴스)
real.equals(proxy); // true

// hashCode: getClass()를 사용하므로 → 다른 값!
real.getClass();  // FortuneResultCategory.class
proxy.getClass(); // FortuneResultCategory$HibernateProxy$xxx.class

// 결과: equals는 true인데 hashCode가 달라서 Set에서 문제 발생 가능
```

#### 고정값 hashCode

```java
@Override
public int hashCode() {
    return 0;
}

// 모든 FortuneResultCategory가 hashCode = 0
// → Set의 성능이 떨어짐 (모두 같은 bucket에 저장)
// O(1) 검색이 O(n)이 됨
```

#### id 기반 hashCode

- 프록시 객체와도 일관성 있게 동작
- 영속화 전에 Set에 추가하면, 영속화 후 id가 생기면서 hashCode가 변경되어 Set에서 객체를 찾지 못하는 문제가 발생

```java
@Override
public int hashCode() {
    return Objects.hashCode(id);  // 클래스 정보 빼고 id만
}

// public static int hashCode(Object o) {
//     return o != null ? o.hashCode() : 0;
// }
// 내부 구현에서 null check 함
```

#### 사용 방식

- ID 기반 equals/hashCode를 사용
  - 영속화 전(id가 null) 객체끼리는 동등하지 않다고 처리
- 엔티티를 Set에 추가하기 전, 반드시 영속화(save)

```java
// ❌ 나쁜 예 - save 전에 Set에 추가
Set<FortuneResultCategory> categories = new HashSet<>();
categories.add(new FortuneResultCategory("행운"));  // id = null
categories.add(new FortuneResultCategory("재물"));  // id = null
// equals가 엉망이 됨

// ✅ 좋은 예 - save 후에 Set에 추가
FortuneResultCategory cat1 = repository.save(new FortuneResultCategory("행운")); // id = 1
FortuneResultCategory cat2 = repository.save(new FortuneResultCategory("재물")); // id = 2
Set<FortuneResultCategory> categories = new HashSet<>();
categories.add(cat1);  // id로 비교 가능
categories.add(cat2);
```

- `@OneToMany`
- @OneToMany 관계에서 CascadeType.ALL을 사용하면 JPA가 부모 엔티티를 영속화할 때 자식 엔티티도 함께 영속화한 후 컬렉션에 추가

```java
@OneToMany(
  mappedBy = "fortuneResult",
  cascade = CascadeType.ALL,
  orphanRemoval = true)
@OrderBy("fortuneCategory.id ASC")
private Set<FortuneResultCategory> categories = new LinkedHashSet<>();
```

- Child 엔티티는 영속화 전에는 Parent의 Set에 들어가지 않음
- CascadeType.ALL → persist()할 때 Child도 동시에 영속화
- 영속화 시점 이후에야 Parent가 Set을 채움

  - `id=null` 상태에서 Set에 들어가는 상황 자체가 발생하지 않음

#### 정리

| 전략        | 특징                    | 장점               | 단점                      |
| ----------- | ----------------------- | ------------------ | ------------------------- |
| 클래스 기반 | `getClass().hashCode()` | 영속화 전후 일관성 | 프록시 객체와 불일치      |
| ID 기반     | `Objects.hashCode(id)`  | 프록시와 일관성    | id null 상태에서 Set 문제 |
| 고정값      | 상수 반환               | 간단함             | 성능 저하                 |

### Redis Session

- 서버 인스턴스가 여러 개여도 세션 공유 가능
- 서버 재시작해도 세션 유지됨
- 메모리 기반으로 속도가 빠름 → 인증 요청, 사용자 상태 정보 조회에 적합

#### 설정

1. 의존성 추가

```java
dependencies {
    implementation 'org.springframework.session:spring-session-data-redis'
    implementation 'org.springframework.boot:spring-boot-starter-data-redis'
}
```

2. docker-compose.redis.yml

```yml
services:
  redis: # 실제 Redis 서버
    image: redis:7.2 # Redis 공식 Docker 이미지 7.2 버전을 사용
    container_name: redis-local
    ports:
      - '6379:6379' # PC(호스트)에서 6379 포트로 접근하면 Docker 컨테이너 내부의 6379로 연결됨
    command: ['redis-server', '--appendonly', 'yes']
    # Docker 컨테이너 안에서 Redis 서버를 실행할 때 추가 옵션을 적용하는 명령
    # redis-server Redis 실행 명령어
    # --appendonly yes 옵션, Redis 데이터를 디스크에 영구 저장(AOF, Append Only File)
    volumes:
      - redis-data:/data # 컨테이너 내부 폴더 /data를 로컬 볼륨 redis-data에 저장

  redis-insight: # Redis 모니터링/관리 웹 UI
    image: redis/redisinsight:latest
    container_name: redis-insight
    ports:
      - '5540:5540'
    depends_on:
      - redis

volumes:
  redis-data: # Docker가 내부적으로 redis-data라는 persistent volume을 생성해서 데이터 유지
```

- 도커 관련 명령어

```bash
docker compose -f docker-compose.redis.yml up -d
docker compose -f docker-compose.redis.yml down
```

3. application-local.yml 설정

- 운영은 AWS이므로 Docker 기반 Redis 사용
  - Docker로 Redis 설치하면 local이나 AWS나 동일한 Redis를 사용하게 되므로 관리가 편리

```yml
spring:
  redis:
    host: localhost
    port: 6379

  session:
    store-type: redis
    timeout: 30m
```

- TTL 우선순위
  - `@EnableRedisHttpSession(maxInactiveIntervalInSeconds = 60)`
  - `spring.session.timeout`
  - `server.servlet.session.timeout`

4. @EnableRedisHttpSession 추가

- 세션이 Redis에 저장됨
  - 기존: 로컬에서 띄운 서버 → 로컬 JVM 메모리 안에 세션 저장
- WAS memory session(In-memory session, Tomcat session)은 비활성화됨
- JSESSIONID는 Redis 기반으로 변경됨

```java
@Configuration
@EnableRedisHttpSession
public class RedisSessionConfig {
}
```

5. RedisInsight에서 Session 데이터 확인하기

- RedisInsight는 Docker 컨테이너 안에서 실행 중이라면, RedisInsight에서 localhost는 사용자 PC가 아니라 자기 컨테이너 자신
- RedisInsight와 Redis는 같은 docker-compose 안에서 실행되고 있어서 서로 컨테이너 이름으로 통신
  - 내부 Docker 네트워크에서 컨테이너는 서로를 컨테이너 이름으로 주소처럼 사용
- Redis 연결 시, localhost가 아닌 컨테이너 이름을 지정

### Session과 Security User 객체

세션(특히 Redis 세션)에 JPA 엔티티(Member 등)를 저장하면 위험

- Redis는 세션 데이터를 저장할 때 byte로 직렬화(serialization)
  - 엔티티는 직렬화가 안정적이지 않음
    - 엔티티 내부에는 프록시 객체, 영속성 핸들러, Lazy 객체 등이 포함됨 → 직렬화 실패(Serialization error) 발생
- 세션과 DB 상태가 불일치 → 버그 발생 가능
  - 사용자가 로그인함
  - 그 시점의 Member 엔티티가 세션에 저장됨
  - 사용자가 DB에서 닉네임을 변경
  - 하지만 세션에는 옛날 Member 엔티티 그대로 남아있음
- Redis 메모리 낭비

#### 세션에는 최소 정보만 저장

- 사용자 ID, 닉네임, 권한 등 꼭 필요한 정보만 담은 가벼운 DTO(Data Transfer Object)를 만들어 세션에 저장
- DTO는 `Serializable` 인터페이스를 구현

```java
public class UserSessionDto implements Serializable {
    private static final long serialVersionUID = 1L; // 직렬화 버전 UID
    private Long id;
    private String nickname;
    private String role;
    // 생성자, Getter 등
}
```

- serialVersionUID를 명시적으로 설정하는 이유
  - 코드가 조금만 변해도 UID가 달라져서 역직렬화가 깨질 위험이 있음
  - 명시적으로 UID를 고정해두면 동일한 클래스 구조라면 안정적으로 역직렬화 가능
    - 만일, Java가 컴파일러가 자동 생성한 UID를 사용할 경우, 필드 하나만 추가해도 UID가 달라짐 → Redis 같은 세션 저장소에 저장된 이전 객체와 호환 안 됨

### JSON 직렬화 오류

```bash
com.fasterxml.jackson.databind.exc.InvalidDefinitionException: Cannot construct instance of org.springframework.security.authentication.UsernamePasswordAuthenticationToken (no Creators, like default constructor, exist): cannot deserialize from Object value (no delegate- or property-based Creator)
```

- Redis에서 SecurityContext를 가져올 때,
  - UsernamePasswordAuthenticationToken을 JSON → 객체로 역직렬화(deserialize) 해야 하는데
  - 이 클래스에는 기본 생성자(default constructor) 가 없어서 Jackson이 객체를 만들 수 없음
  - 그래서 SecurityContext 저장/복원 과정에서 에러 발생

#### 해결책

— Spring Data Redis에서 제공하는 JdkSerializationRedisSerializer 사용(Java의 기본 직렬화를 사용)

```java
// JSON 직렬화 대신 Java 기본 직렬화를 사용하도록 설정하여 역직렬화 오류를 해결
// 단, 등록하지 않을 경우에도 JdkSerializationRedisSerializer 적용
@Bean
public RedisSerializer<Object> springSessionDefaultRedisSerializer() {
    return new JdkSerializationRedisSerializer();
}
```

### 운영 환경에서 Redis 설치하기

#### 운영 서버(EC2)에서 Redis 컨테이너 직접 띄우기

특징

- 로컬과 거의 동일한 구성 → 운영 설정 변경 최소화
- 네트워크 Latency 거의 없음
- Redis 장애 → 서비스 전체 장애 가능
- 백업 스냅샷 관리 직접해야 함

1. EC2에 Docker 설치

```bash
docker --version
docker compose version

# 없을 경우,
sudo yum update -y
sudo yum install -y docker
# 부팅 시 자동으로 Docker 서비스가 실행되도록 설정
sudo systemctl enable docker
# 지금 당장 Docker 데몬을 실행시키기
sudo systemctl start docker
# Docker 그룹 반영(로그아웃 후 다시 로그인)
# 기본적으로 docker 명령은 root 권한 필요
# docker 그룹에 넣어주면 일반 사용자도 root 없이 docker 명령 사용 가능
# -aG: append to Group (기존 그룹 유지 + docker 그룹 추가)
sudo usermod -aG docker ec2-user

# Docker Compose Plugin 설치
sudo mkdir -p /usr/local/lib/docker/cli-plugins/

sudo curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m)" -o /usr/local/lib/docker/cli-plugins/docker-compose
# sudo curl -SL "URL": GitHub 릴리스 페이지에서 컴퓨터 CPU 아키텍처(arm64/x86_64)에 맞는 Docker Compose 바이너리를 다운로드하는 명령
# -S : 에러 있을 때 메시지 보여줌
# -L : 리다이렉트를 따라감(최신 릴리스 링크가 보통 리다이렉트됨)
# "$(uname -m)" 부분이 CPU 아키텍처를 자동으로 넣어서 다운로드

# Docker CLI 플러그인 전용 위치로 설치
# 여기에 docker-compose라는 실행 파일을 두면, `docker compose` 명령이 자동으로 활성화됨
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
docker compose version
# Docker Compose version v5.0.0
```

2. `.env`

- `docker-compose.redis.yaml`과 같은 위치에 `.env` 생성 시, Docker Compose가 자동으로 읽으므로 해당 방식으로 사용
  - ⛑️ 전역 env 파일을 command에서 `env_file:/etc/luckylog/.env`로 설정했으나, env파일을 인식하지 못함
- 관리의 편의성을 위해 전역 env 파일을 복사해서 사용

```bash
# 수정
sudo nano /etc/luckylog/.env

# 서비스 설정 파일이 바뀌었으니 다시 조회
# systemd는 서비스 파일을 메모리에 캐싱해 두기 때문에 /etc/systemd/system/luckylog.service 또는 EnvironmentFile 같은 외부 파일을 변경해도 바로 반영되지 않음
sudo systemctl daemon-reload

# luckylog 서비스를 재시작
# 변경된 환경변수(.env), 변경된 service 파일 등이 새 프로세스에 적용됨
sudo systemctl restart luckylog

# 정상 동작 확인
sudo systemctl status luckylog
```

systemd에서 EnvironmentFile을 로드하는 과정

- systemd가 (root 권한으로) unit 파일과 EnvironmentFile을 읽어들임
  - EnvironmentFile을 systemd가 직접 읽음 → root 로 읽기 때문에 파일 권한이 root:600이어도 문제 없음
  - 서비스 내부에서 실행된 스크립트나 애플리케이션이 직접 .env 파일을 읽는 경우 → deploy가 읽을 수 없어서 실패
- 이후 User=deploy 로 프로세스 권한을 낮춰 실행

```bash
# 파일의 소유자(owner) 를 root로, 그룹(group) 을 deploy로 변경
sudo chown root:deploy /etc/luckylog/.env

# 파일 권한 설정
# 6 → owner(root): read + write
# 4 → group(deploy): read
# 0 → others(그 외 사용자): no access
sudo chmod 640 /etc/luckylog/.env
```

3. `docker-compose.redis.yaml`

- 어떤 서비스에 대한 docker compose 파일인지 표시하면 구분하기 좋음
- docker compose 파일은 infra 폴더에서 한꺼번에 관리하는 것이 좋음

```yaml
services:
  redis:
    image: redis:7.2
    container_name: redis-prod
    restart: unless-stopped # 사용자가 ‘stop’으로 멈추지만 않으면 자동 재시작
    ports:
      - '6379:6379'
    command: [
        'redis-server',
        '--appendonly',
        'yes',
        '--appendfsync',
        'everysec', # 언제 디스크에 실제로 기록(sync)할지, 1초 마다
        '--maxmemory',
        '300mb',
        '--maxmemory-policy', # Redis가 메모리를 넘지 않고 오래된 키부터 자동 제거
        'allkeys-lru',
        '--protected-mode',
        'yes',
        '--requirepass',
        '${REDIS_PASSWORD}', # .env 환경변수 주입
      ]
    environment:
      - TZ=Asia/Seoul
    volumes:
      - redis-data:/data

volumes:
  redis-data: # Docker가 내부적으로 redis-data라는 persistent volume을 생성해서 데이터 유지
```

4. Docker Compose로 Redis 실행

```bash
# Redis 재시작
cd /home/deploy/infra

sudo docker compose -f docker-compose.redis.yaml up -d # 비밀번호가 설정되지 않았을 경우, 경고 발생
# sudo docker compose -f docker-compose.redis.yaml down

# 비밀번호 확인
sudo docker exec redis-prod redis-cli CONFIG GET requirepass
# sudo docker exec redis-prod redis-cli CONFIG GET requirepass NOAUTH Authentication required.
# Redis에 비밀번호(requirepass)가 설정되어 있어서, redis-cli 명령을 실행하려면 먼저 AUTH(인증) 필요

# Redis 조회
sudo docker exec -it redis-prod redis-cli
AUTH <password>
ping
KEYS *
HGETALL spring:session:sessions:<sessionId>
```

5. `application-prod.yaml`

```yaml
spring:
  session:
    store-type: redis
    timeout: 30m
  data:
    redis:
      host: ${REDIS_HOST}
      port: ${REDIS_PORT}
      password: ${REDIS_PASSWORD}
```

6. 애플리케이션 정상 동작 확인

```bash
# 애플리케이션 재시작
sudo systemctl restart luckylog
sleep 5
sudo systemctl status luckylog

# Redis 연결 성공했는지 확인
sudo journalctl -u luckylog -n 50 --no-pager | grep -i redis

# Health check 확인
# 정상: {"status":"UP"}
curl http://localhost:8080/actuator/health

# 해당 프로세스 환경 확인
sudo cat /proc/$(pgrep -f luckylog.jar)/environ | tr '\0' '\n'

REDIS_HOST=...
REDIS_PORT=...
REDIS_PASSWORD=...

# systemd가 EnvironmentFile을 읽었는지 확인
systemctl show luckylog --property=EnvironmentFiles
EnvironmentFiles=/etc/luckylog/.env
```

7. CI/CD 파일에 Redis Health Check 추가

- Redis Health Check
- Restart luckylog
- Luckylog Health Check

```yaml
- name: Check Redis Health
  uses: appleboy/ssh-action@v1.0.3
  with:
    host: ${{ secrets.EC2_HOST }}
    username: ${{ secrets.EC2_USERNAME }}
    key: ${{ secrets.EC2_SSH_KEY }}
    script: |
      echo "🔐 Loading REDIS_PASSWORD from /etc/luckylog/.env..."

      # /etc/luckylog/.env 파일에서 REDIS_PASSWORD= 로 시작하는 줄을 찾고 = 뒤 문자열(비밀번호)만 잘라서 가져옴
      # 소유자가 root, 그룹이 root인 파일로 sudo 명령어로 조회 
      REDIS_PASSWORD=$(sudo grep '^REDIS_PASSWORD=' /etc/luckylog/.env | cut -d'=' -f2-)

      # 비밀번호가 비어 있으면 실패 처리
      if [ -z "$REDIS_PASSWORD" ]; then
        echo "❌ REDIS_PASSWORD not found in /etc/luckylog/.env"
        exit 1
      fi

      # Redis 컨테이너가 실행 중인지 확인
      echo "🧪 Checking Redis container status..."
      if ! docker ps --format '{{.Names}}' | grep -q 'redis-prod'; then
        echo "❌ Redis container is NOT running!"
        exit 1
      fi

      # Redis PING 테스트
      echo "🧪 Testing Redis PING..."
      PING_RESULT=$(docker exec redis-prod sh -c "timeout 3 redis-cli -a \"$REDIS_PASSWORD\" ping" 2>&1)
      RET=$?

      # exit code 실패면 바로 실패
      if [ $RET -ne 0 ]; then
        echo "❌ Redis PING failed (exit code $RET)"
        exit 1
      fi

      # exit code는 0인데 PONG이 없으면 실패 처리
      if ! echo "$PING_RESULT" | grep -q "PONG"; then
        echo "❌ Redis PING failed (no PONG in output)"
        exit 1
      fi

      echo "✅ Redis is healthy."
```

#### AWS ElastiCache for Redis 사용

특징

- connection endpoint 제공 → docker에서 사용하는 것보다 단순
- 관리형 → 장애 자동 복구, 스냅샷 자동 백업, 패치 자동 적용
- 비용 발생 (하지만 운영 부담 감소와 장애 감소로 대부분 가치 있음)
- VPC/Subnet/Security Group 설정 필요

> TODO: 이 외 내용 추가

### 📚 참고

- [Gradle 멀티 프로젝트 관리](https://jojoldu.tistory.com/123)
- [[gradle] implementation, api 차이](https://dkswnkk.tistory.com/759)
- [[Gradle] Gradle Java 플러그인과 implementation와 api의 차이](https://mangkyu.tistory.com/296)
