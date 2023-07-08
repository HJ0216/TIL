# Java

### 특징
- 객체지향(캡슐화, 상속, 다형성 등) 언어
- JVM(Jva Virtual Machine) 위에서 동작 → 운영체제로부터 독립적이나 실행속도가 느린 단점이 존재
<br/>
<img src="https://www.devkuma.com/docs/java/jvm/java_compile_jvm.png" width="100%" />
- 실행 절차: *.java 파일 생성 → compiler: *.java → *.class 파일인 Byte code로 Compile → JVM: Byte Code → 기계어인 Binary Code로 변환 → CPU에서 실행되어 사용자에게 제공

<br/>
<img src="https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FcgGf08%2Fbtrup9tFZNc%2FdfbotBKGFrZ4mDGIYrNj10%2Fimg.png" width="100%" />

- 다중 상속이나 타입이 엄격

<br />

### JVM
- 구성: Class Loader, Execution Engine, Runtime Data Area
<br/>
<img src="https://images.velog.io/images/raejoonee/post/febb74dc-1b88-45d7-b019-3728f7f1ba93/jvm.png" width="100%" />
- Class Loader:  바이트 코드(*.class)들을 JVM의 메모리 영역인 Runtime Data Areas에 배치
- Execution Engine: 클래스 로더를 통해 런타임 데이터 영역에 배치된 바이트 코드를 명령어 단위로 읽어서 실행
    - Garbage Collector: Heap 메모리 영역에서 사용하지 않는 메모리를 자동으로 회수
- RunTime Data Area: JVM의 메모리 영역

<br/>

### 객체지향프로그래밍(Object Oriented Programming)
- 애플리케이션을 구성하는 요소들을 객체로 바라보고, 객체들을 유기적으로 연결하여 프로그래밍 하는 것
    - 프로그램을 보다 유연하고 변경에 용이하게 만들 수 있음 → 유지보수에 유리
    - 특징
        - 추상화(Abstraction)
        - 상속(Inheritance)
        - 다형성(Polymorphism)
        - 캡슐화(Encapsulation)

<br/>

### Abstraction
- Abstract Class: 클래스 내 추상 메소드가 하나 이상 포함되거나 abstract로 정의된 경우
- Interface: 모든 메소드가 추상 메소드로만 이루어져 있는 경우
    - 공통점:
        - new 연산자를 통한 객체 생성 불가능
        - 하위 클래스에서 확장/구현 해야 사용 가능
    - 차이점:
        - Interface를 구현할 경우, 해당 Interface 내의 모든 메서드를 구현해야 함
        - Abstract Class: 다중 상속 불가, Interface: 다중 구현 가능

<br/>

### Inheritance
- 기존의 클래스를 재활용하여 새로운 클래스를 작성
    - Overriding: 상위 클래스에 있는 메소드를 하위 클래스에서 재정의하는 것
    - Overloading: 매개변수의 개수나 타입을 다르게 하여 같은 이름의 메소드를 여러 개 정의하는 것

<br/>

### Polymorphism
- 상위 클래스 타입의 참조 변수로 그것과 관계있는 하위 클래스들을 참조할 수 있는 것
<br/>
<img src="https://i0.wp.com/blog.codestates.com/wp-content/uploads/2022/11/%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EC%9D%B8%ED%84%B0%ED%8E%98%EC%9D%B4%EC%8A%A4-%EC%A0%81%EC%9A%A9-%EC%A0%84%E3%85%81.png?resize=1024%2C841&ssl=1" width="100%" />
<img src="https://i0.wp.com/blog.codestates.com/wp-content/uploads/2022/11/%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EC%A0%81%EC%9A%A9-%ED%9B%84.png?resize=1024%2C294&ssl=1" width="100%" />
     ＊ 이동 수단에 대해 인터페이스를 구현하여 객체간의 결합도를 낮춰 객체지향 프로그래밍을 실현

<br/>

### Encapsulation
- 클래스 안에 서로 연관있는 속성과 기능들을 하나의 캡슐(capsule)로 만들어 데이터를 외부로부터 보호하는 것
    - 접근제어자
    <img src="https://i0.wp.com/blog.codestates.com/wp-content/uploads/2022/11/%EC%9E%90%EB%B0%94-%EC%A0%91%EA%B7%BC%EC%A0%9C%EC%96%B4%EC%9E%90-%ED%91%9C.png?resize=1024%2C334&ssl=1" width="100%" />
    - Getter/Setter: 속성값을 private으로 선언하여 외부의 직접적인 접근을 제어하고, getter/setter 메서드는 public으로 선언하여 선택적으로 외부 접근을 제어함
    <img src="https://i0.wp.com/blog.codestates.com/wp-content/uploads/2022/11/%EA%B0%9D%EC%B2%B4%EC%A7%80%ED%96%A5%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D%ED%8A%B9%EC%A7%95%EC%BA%A1%EC%8A%90%ED%99%94.png?resize=1024%2C803&ssl=1" width="100%" />
    <img src="https://i0.wp.com/blog.codestates.com/wp-content/uploads/2022/11/%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%ED%81%B4%EB%9E%98%EC%8A%A4-1.png?resize=1024%2C594&ssl=1" width="100%" /> 
    <img src="https://i0.wp.com/blog.codestates.com/wp-content/uploads/2022/11/%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%ED%81%B4%EB%9E%98%EC%8A%A4-1.png?resize=1024%2C594&ssl=1" width="100%" />
    <img src="https://i0.wp.com/blog.codestates.com/wp-content/uploads/2022/11/%EA%B0%9D%EC%B2%B4-%EC%A7%80%ED%96%A5-%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%98%EB%B0%8D-%EB%93%9C%EB%9D%BC%EC%9D%B4%EB%B2%84-%ED%81%B4%EB%9E%98%EC%8A%A4-1.png?resize=1024%2C594&ssl=1" width="100%" />
    ＊ 기존: Driver 클래스가 Car 클래스의 내부 메서드를 직접 호출함으로써, 객체간의 결합도가 높아짐(= Car 클래스의 변경이 Driver 클래스의 결함을 유발할 수 있음)
    <br/>
    ＊ → 캡슐화: Car 클래스와 관련된 기능들은 온전히 Car 에서만 관리되도록 하였고, 불필요한 내부 동작의 노출을 최소화하여 객체지향 프로그래밍 실현

<br/>

### static
- 인스턴스(객체) 생성 없이 바로 사용 가능
- 자주 변하지 않는 값이나 공통으로 사용되는 값에 대해 매번 메모리에 로딩하거나 값을 읽어들이는 것보다 일종의 '전역변수'와 같은 개념을 통해 접근하는 것이 비용도 줄이고 효율을 높일 수 있음

<br/>

### Error & Exception
- Error: 실행 중 일어날 수 있는 치명적 오류, UncheckedException의 일종
- Exception: 경미한 오류, try-catch를 이용해 프로그램의 비정상 종료를 막을 수 있음
    - CheckedException: 실행하기 전에 예측 가능한 예외, 반드시 예외 처리
    - UncheckedException: 실행하고 난 후에 알 수 있는 예외, 따로 예외처리를 하지 않음(예: RuntimeException)

<br/>

### Collection Framework
- 다수의 데이터를 쉽고 효과적으로 관리할 수 있는 표준화된 방법을 제공하는 클래스의 집합
<img src="https://hyuntaekhong.github.io/assets/images/java/java-basic25/collection01.png" alt="java_collection_framework" width="100%">
1. List: 순서가 있는 데이터의 집합, 데이터 중복 허용
    - ArrayList, Vector, LinkedList, ...
<img src="https://open4tech.com/wp-content/uploads/2019/03/array-linked-list.png" alt="list_type" width="100%">
2. Set: 순서가 없는 데이터의 집합, 데이터 중복 불허
    - HashSet, LinkedHashSet(순서 보장), TreeSet, ...
3. Map: 키와 값이 한 쌍, 순서가 없는 데이터 집합, 키를 기준으로 중복 불허
    - HashMap, LinkedHashMap(순서 보장), TreeMap, HashTable, ...
<img src="https://jojozhuang.github.io/assets/images/algorithm/1131//hashmap.png" alt="hash_map" width="100%" />
<br/>

### 직렬화(Serialize)
- 시스템 내부에서 사용되는 객체 또는 데이터를 외부의 시스템에서도 사용할 수 있도록 바이트(byte) 형태로 데이터 변환하는 기술(↔ 역직렬화)
-  SerialVersionUID
    - JVM: 직렬화와 역직렬화를 하는 시점의 클래스에 대한 버전 번호를 부여
    - 직렬화할 때의 버전 번호와 역직렬화를 할 때의 버전 번호가 다르면 역직렬화가 불가능하게 될 수 있기 때문에 이런 문제를 해결하기 위해 SerialVersionUID를 사용

