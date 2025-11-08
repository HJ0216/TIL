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
class UserServiceTest {

    @Mock
    private UserRepository userRepository; // 실제 DB X, Mockito mock

    @InjectMocks
    private UserService userService; // userRepository가 주입됨

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
    org.hibernate.type: TRACE # 파라미터 값까지 보기
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
    - `-Dspring.profiles.active=test` 지정 필요 X(application-test.yaml 사용 시, `-Dspring.profiles.active=test` 지정 필요 O)

### 📚 참고

- [Gradle 멀티 프로젝트 관리](https://jojoldu.tistory.com/123)
- [[gradle] implementation, api 차이](https://dkswnkk.tistory.com/759)
- [[Gradle] Gradle Java 플러그인과 implementation와 api의 차이](https://mangkyu.tistory.com/296)
