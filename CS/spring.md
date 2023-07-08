# Spring

### POJO(Plain Old Java Object)
- 외부의 종속성이 없는 단순한 자바 객체 프로그래밍 지향하는 프레임워크
- 다른 클래스나 인터페이스를 상속하지 않고 getter, setter와 같이 기본적인 기능만 가진 자바 객체

        public class example {
          private int age;
          private String name;

          public int getAge(){return age;}
          public String getName(){return name;}

          public void setAge(){this.age = age;}
          public void setAge(){this.name = name;}
        }

<br/>


### IoC(Inversion of Control, 제어의 역전)
- 인스턴스 생명주기 관리를 개발자가 아닌 컨테이너가 대신하는 것
- IoC container: Spring에서 객체를 생성하고 관리하고 책임지고 의존성을 관리해주는 컨테이너
- 종류
    - DL(Dependency Lookup): 저장소에 저장되어 있는 Bean(스프링 컨테이너가 관리하는 객체)에 접근하기 위해 컨테이너가 제공하는 API를 이용하여 Bean을 Lockup하는 것
    - DI(Dependency Injection): 필요한 객체를 직접 생성하는 것이 아닌 외부로부터 객체를 받아 사용하는 것
        - :star:Constructor Injection(생성자 주입)
            - 장점
                - 순환 참조 방지: 다른 주입 방식과 달리 스프링 애플리케이션 로딩시점에서 예외가 발생하여 실제 코드가 호출되기 전 오류를 확인할 수 있음
                - 불변성(Immutability): final로 참조형 변수는 반드시 선언과 함께 초기화가 되어야 하므로 누군가 해당 객체값을 임의로 변경할 수 없음
        - Setter Injection(수정자 주입)
            - 단점: 주입이 필요한 객체가 주입이 되지 않아도 객체를 생성할 수 있어 NullPointerException이 발생할 위험이 있음
        - Field Injection(필드 주입)
            - 단점: 주입이 필요한 객체가 주입이 되지 않아도 객체를 생성할 수 있어 NullPointerException이 발생할 위험이 있음

<br/>


### AOP(Aspect Oriented Programming, 관심 지향 프로그래밍)
- 핵심 로직과 부가 기능을 분리하여 애플리케이션 전체에 걸쳐 사용되는 부가 기능을 모듈화하여 재사용할 수 있도록 지원하는 것
- OOP: Business Logic의 모듈화, AOP: 기능의 모듈화

<br/>

### PSA(Portable Service Abstraction, 일관된 서비스 추상화)
- 작업 환경이나 기술이 변하더라도 일관된 방식의 접근 방식을 제공하여 의존성을 크게 고려하지 않아도 되는 구조
- 예시
    <img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FqBlwL%2FbtrpGzxt8xd%2FnXY5EU8z7Y4Q7hH4SVhZU1%2Fimg.png" alt="psa" width="100%">
    - @Transactional: JDBC에 특화된 DatasourceTransactionManager, JPA에 특화되어 Entity Manager를 사용하는 JPATransactionManager를 각각 구현하는 것이 아니라, 최상위 추상화 인터페이스인 PlatformTransactionManager를 만들고 각각의 TransactionManager가 구현하도록 만들어서 DI로 주입받아 사용하도록 만들어짐

<br/>

### Spring MVC
- View: 비즈니스 로직의 처리 결과를 통해 유저 인터페이스가 표현되는 구간
- Controller: 사용자의 요청을 처리하고 Model과 View를 중개하는 역할
- Model: 데이터 관리 및 비즈니스 로직을 처리하는 부분

<br/>

### Spring Boot와 Spring의 차이점
1. Spring Boot: Spring-boot-starter를 통해 dependency를 보다 쉽게 설정할 수 있으며, 버전 관리도 자동으로 됨
2. Jetty 및 Tomcat 등과 같은 임베디드 서버를 제공

<br/>

### 용어
1. Entity: 실제 DataBase의 테이블과 1 : 1로 매핑되는 클래스
    - DB의 테이블내에 존재하는 컬럼만을 속성(필드)으로 가져야 함
    - 상속을 받거나 구현체여서는 안됨
    - Entity 클래스는 다른 클래스에 영향을 미칠 수 있으므로 View와 통신하며 자주 변경될 수 있는 DTO 클래스로 따로 분리해야 함
2. DTO(Data Transfer Object): 각 계층(Layer)간 데이터 교환을 위한 객체(Java Beans)
    - 로직을 갖고 있지 않는 순수한 데이터 객체이며, getter/setter 메소드만을 갖음
    - 예: View <-(DTO) -> Controller <- (DTO) -> Service 
3. VO(Value Object): 변하지 않는 데이터 객체, 오직 read만 가능하며 getter만 사용
    - 예: 고정된 값은 VO로 저장 후 Getter 호출
            
            DTO a = new DTO(1);
            DTO b = new DTO(1);
            // a != b

            VO a = new VO(1);
            VO b = new VO(1);
            // a==b
