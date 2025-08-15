### model attribute 받는 법
```java
model.addAttribute("errorFields", errorFields);
```

```html
<script th:inline="javascript" th:if="${errorFields != null}">
        window.errorFields = [[${errorFields}]];
</script>
```
1. inline javascript를 선언하지 않으면, 배열의 값을 문자로 인식하지 않고 변수로 인식하여 해당 id값을 가진 요소를 할당
  * JavaScript의 문자열 배열 리터럴(소스 코드에 고정된 값으로 표현된 데이터)로 안전하게 변환
2. js에서 사용할 값을 html에서 먼저 변수로 설정 필요



### th:field
* id와 name 속성을 자동으로 생성하고 관리
  * 개발자가 직접 id를 명시하면 그 id를 존중하여 그대로 사용
* 눈에 보이지 않는 <input type="hidden"> 태그를 자동으로 생성
  * 스프링은 폼이 전송될 때 체크되지 않은 체크박스의 값은 아예 전송되지 않는 문제를 해결하기 위해, 이 필드가 폼에 존재했었다는 것을 알려주는 용도로 _<fieldName> 형태의 hidden 필드를 만듦
  * th:field를 사용하지 않고 name, value, th:checked를 직접 작성하여 Thymeleaf가 hidden 필드를 생성하지 않도록 할 수 있음
```html
<!-- th:field를 아래와 같이 분리하여 수정 -->
<div class="fortune-option" data-tooltip="종합">
  <input type="checkbox" 
         id="overall" 
         name="fortunes" 
         value="overall"
         th:checked="${#lists.contains(fortuneOptionForm.fortunes, 'overall')}">
  <label for="overall">🔮</label>
</div>
```


## Thymeleaf 표준 표현식

### 1. 변수 표현식 `${...}`
```html
<p th:text="${message}">기본 메시지</p>
<p th:utext="${htmlContent}">HTML 내용</p>
```

### 2. 선택 표현식 `*{...}`
```html
<div th:object="${user}">
    <p th:text="*{name}">이름</p>
    <p th:text="*{email}">이메일</p>
</div>
```

### 3. 메시지 표현식 `#{...}`
```html
<p th:text="#{welcome.message}">환영 메시지</p>
```

### 4. 링크 표현식 `@{...}`
```html
<a th:href="@{/books}">도서 목록</a>
<link th:href="@{/css/style.css}" rel="stylesheet">
```

### 5. 조각 표현식 `~{...}`
```html
<div th:insert="~{fragments/header :: header}">헤더</div>
```

## 객체 네비게이션 (`user.name` vs `user['name']`)
| 표기법          | 사용 예시          | 특징                                |
| -------------- | ----------------- | ----------------------------------- |
| `user.name`    | `${user.name}`    | **Java Bean 표준 getter** 호출       |
| `user['name']` | `${user['name']}` | **Map 키** 또는 **동적 속성명** 접근   |


```java
public class User {
    private String name;
    public String getName() { return name; }
}

Map<String, Object> user = new HashMap<>();
user.put("name", "홍길동");
```

```html
<!--Java Bean 객체-->
<p th:text="${user.name}"></p>       <!-- getName() 호출 -->
<p th:text="${user['name']}"></p>    <!-- 가능하지만 잘 안 씀 -->

<!--Map 객체-->
<p th:text="${user.name}"></p>       <!-- null (getter 없어서) -->
<p th:text="${user['name']}"></p>    <!-- "홍길동" -->
```


## 조건 연산자와 Elvis 연산자
```html
<p th:text="${book.available} ? '대출 가능' : '대출 중'"></p>

<!--변수가 null이거나 빈 문자열이면 기본값을 반환-->
<p th:text="${user.name ?: '이름 없음'}"></p>
```


## 문자열 연결과 리터럴
```html
<!--Thymeleaf에서 HTML 속성값을 줄 때는 보통 큰따옴표, EL 안에서는 작은따옴표가 흔함-->
<p th:text="'제목: ' + ${book.title}"></p>

<!--파이프 기호(|...|) 사용(⭐권장)-->
<p th:text="|제목: ${book.title}|"></p>

```


