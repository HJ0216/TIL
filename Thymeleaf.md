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






### 1. 기본 표현식 (Basic Expressions)

| 표현식 | 설명 | 예제 |
| :--- | :--- | :--- |
| `${...}` | **변수 표현식**: 모델에 포함된 값이나 객체 속성에 접근 | `<span th:text="${user.name}"></span>` |
| `*{...}` | **선택 표현식**: `th:object`로 선택한 객체 내부의 속성에 접근 <br/> `${...}`보다 간결 | `<div th:object="${user}"><p th:text="*{name}"></p></div>` |
| `@{...}` | **URL 표현식**: 링크 URL을 생성 <br/>서블릿 컨텍스트 경로가 자동으로 포함 | `<a th:href="@{/board/list}">게시판</a><br><a th:href="@{/board/{id}(id=${board.id})}">게시글 보기</a>` |
| `#{...}` | **메시지 표현식**: `messages.properties`와 같은 메시지 파일의 값을 가져와 다국어 처리에 사용 | `<h1 th:text="#{home.welcome}"></h1>` <br> `<!-- messages.properties: home.welcome=환영합니다 -->` |
| `~{...}` | **조각 표현식**: 템플릿 조각(fragment)을 다른 곳에 포함하거나 파라미터로 전달할 때 사용 | `<div th:replace="~{fragments/footer :: footerFragment}"></div>` |
| `[[...]]` <br> `[(...)]`| **인라인 표현식**: `<span>`과 같은 태그 없이 HTML 텍스트 내에 변수 값을 직접 출력 <br/> `[[...]]`는 `th:text`처럼 처리되고, `[(...)]`는 `th:utext`처럼 처리 | `<p>안녕하세요, [[${user.name}]]님!</p>` <br> `<div>[(${htmlContent})]</div>` |
---
* 문자열 연결과 리터럴
  ```html
  <!--Thymeleaf에서 HTML 속성값을 줄 때는 보통 큰따옴표, EL 안에서는 작은따옴표가 흔함-->
  <p th:text="'제목: ' + ${book.title}"></p>

  <!--파이프 기호(|...|) 사용(⭐권장)-->
  <p th:text="|제목: ${book.title}|"></p>
  ```


* URL 표현식`@{...}`
  ```html
  <a th:href="@{/books}">도서 목록</a>
  <link th:href="@{/css/style.css}" rel="stylesheet">
  ```

* 조각 표현식`(~{...})`
  * **재사용 가능한 HTML 조각(레고 블록)**을 별도의 파일에 만들어두고, 필요한 곳에서 **가져와 조립(import)**하는 기능
  * `~{파일경로 :: 조각이름}`
  * 종류
    * th:replace: 사용된 해당 태그 교체
    * th:insert: 사용된 해당 태그 내 삽입
  * 조각에 파라미터 전달
    ```html
    <header th:fragment="headerFragment(pageTitle, userRole)">
      <h1 th:text="${pageTitle}">Default Title</h1>
      <div th:if="${userRole == 'ADMIN'}">
        <a href="/admin">관리자 페이지</a>
      </div>
    </header>

    <body>
      <!-- header 조각을 부르면서 pageTitle과 userRole 값을 전달 -->
      <div th:replace="~{fragments/header :: headerFragment(pageTitle='마이 페이지', userRole=${currentUser.role})}"></div>
      
      <p>여기는 프로필 페이지입니다.</p>
    </body>
    ```


### 2. 제어 구조 (Control Structures)

| 문법 | 설명 | 예제 |
| :--- | :--- | :--- |
| `th:if` / `th:unless` | **조건부 렌더링**: `th:if`는 조건이 참일 때, `th:unless`는 조건이 거짓일 때 해당 요소를 렌더링 | `<a th:if="${user.isAdmin}">관리자 메뉴</a>` <br> `<p th:unless="${items.isEmpty()}">상품 목록이 있습니다.</p>` |
| `th:each` | **반복문**: 컬렉션(List, Array 등)의 각 요소를 반복하여 렌더 `iterStat`으로 반복 상태(index, count 등)를 알 수 있음 | `<ul><li th:each="item, stat : ${items}">[[${stat.count}]]. [[${item.name}]]</li></ul>` |
| `th:switch` / `th:case` | **Switch 문**: 여러 조건 중 하나를 만족하는 요소를 렌더링= `th:case="*"`는 default 역할 | `<div th:switch="${user.role}"><p th:case="'ADMIN'">관리자</p><p th:case="'USER'">사용자</p><p th:case="*">방문자</p></div>` |
| `? : :` (삼항 연산자) | **조건부 값 표현**: `(조건) ? (참일 때 값) : (거짓일 때 값)` 형태로 간단한 조건부 값을 표현 | `<span th:text="${user.age > 19} ? '성인' : '미성년자'"></span>` |
| `?: :` (Elvis 연산자) | **Null 처리**: 변수가 null이거나 빈 문자열이면 기본값을 반환 | `<span th:text="${user.name} ?: '게스트'"></span>` <br> `// user.name이 null이면 '게스트'를 출력` |
---



### 3. 텍스트와 속성 (Text and Attributes)

| 속성 | 설명 | 예제 |
| :--- | :--- | :--- |
| `th:text` | **텍스트 설정 (이스케이프)**: HTML 태그를 일반 텍스트로 처리하여 출력(XSS 방어) | `<p th:text="${comment}"></p>` <br> `// <script>alert(1)</script> -> &lt;script&gt;alert(1)&lt;/script>` |
| `th:utext` | **텍스트 설정 (이스케이프 안 함)**: HTML 태그를 해석하여 그대로 출력, 신뢰할 수 없는 데이터에 사용 시 주의 | `<div th:utext="${htmlContent}"></div>` <br> `// "<b>Hello</b>" -> <b>Hello</b>` |
| `th:attr` | **동적 속성 설정**: HTML 요소의 속성 값을 동적으로 설정, 여러 속성을 한 번에 설정할 수 있음 | `<img th:attr="src=@{/images/logo.png}, alt=#{logo.alt}" />` |
| `th:class` / `th:classappend` | **CSS 클래스 관리**: `th:class`는 클래스를 완전히 교체하고, `th:classappend`는 기존 클래스에 값을 추가 | `<div class="box" th:classappend="${isActive} ? 'active' : ''"></div>` |
| `th:style` | **인라인 스타일 설정**: `style` 속성 값을 동적으로 설정합니다. | `<div th:style="'color: ' + ${fontColor} + ';'"></div>` |
---
* 텍스트 설정 (이스케이프)`th:text`
  * 사용자가 게시판에 댓글을 달 경우, 어떤 내용이든 안전하게 **"글자"**로만 취급
  * 해커가 `<script>` 같은 위험한 코드를 넣어도 그냥 글자로 보일 뿐, 실행되지 않아 안전

* 텍스트 설정 (이스케이프 안 함)`th:utext`
  * 편리하지만, 사용자가 입력한 내용에 사용하면 해커의 공격(XSS)에 매우 취약

* 동적 속성 설정`th:attr`
  * data-* 형태의 속성을 사용해 태그에 추가 정보를 숨겨둘 때가 많음, 이럴 때 사용
    * 예를 들어, 버튼을 클릭했을 때 어떤 상품의 ID를 자바스크립트에서 쉽게 알아내고 싶을 때 사용
  ```html
  <!-- 버튼에 'data-product-id'라는 속성을 만들고, 그 값을 상품 ID로 설정 -->
  <button th:attr="data-product-id=${product.id}">
      장바구니 담기
  </button>
  ```
  * 이미지 태그(`<img>`)에는 보통 src(이미지 경로)와 alt(이미지가 안 보일 때 나올 설명) 속성이 함께 쓰임
    * th:attr을 사용해 한 번에 설정할 수 있음
  ```html
  <!-- src 속성과 alt 속성을 콤마(,)로 구분해서 한 번에 설정 -->
  <img th:attr="src=${product.imagePath}, alt=${product.name}" />
  ```

* CSS 클래스 관리`th:class`와 속성 처리
  ```html
  <div th:class="${book.available ? 'available' : 'unavailable'}">
    상태에 따른 클래스 적용
  </div>
  <input type="text" th:value="${book.title}" th:readonly="${!isAdmin}">
  <button th:disabled="${!book.available}">대출하기</button>
  ```


### 4. 유틸리티 객체 (Utility Objects)

Thymeleaf는 자주 사용되는 기능을 편리하게 사용할 수 있도록 유틸리티 객체를 제공합니다. `#` 기호를 사용하여 접근합니다.

| 객체 | 설명 | 예제 |
| :--- | :--- | :--- |
| `#strings` | **문자열 처리**: `isEmpty`, `contains`, `startsWith`, `toUpperCase` 등 다양한 문자열 처리 기능을 제공합니다. | `<p th:if="${#strings.isEmpty(user.name)}">이름이 없습니다.</p>` |
| `#numbers` | **숫자 포맷팅**: `formatDecimal`(천 단위 콤마), `formatCurrency`(통화 형식) 등 숫자 서식을 지정합니다. | `<p th:text="${#numbers.formatDecimal(price, 0, 'COMMA')}">1,000</p>` |
| `#temporals` | **날짜/시간 처리**: Java 8의 `java.time` 객체(LocalDate, LocalDateTime 등)를 포맷팅합니다. | `<p th:text="${#temporals.format(createdDate, 'yyyy-MM-dd HH:mm')}"></p>` |
| `#lists` | **리스트 조작**: `size`, `isEmpty`, `contains` 등 리스트 관련 유용한 기능을 제공합니다. | `<p th:text="'총 ' + ${#lists.size(items)} + '개'"></p>` |
| `#maps` | **맵 조작**: `size`, `isEmpty`, `containsKey` 등 맵 관련 유용한 기능을 제공합니다. | `<div th:if="${#maps.containsKey(myMap, 'error')}">오류 발생</div>` |
| `#aggregates`| **집계 함수**: 리스트나 배열의 합계(`sum`), 평균(`avg`) 등을 계산합니다. | `<p th:text="'총 금액: ' + ${#aggregates.sum(items.![price])} + '원'"></p>` |



## 폼 처리
* `th:object`: 폼 전체가 어떤 객체와 연결되어 있는지
* `th:field`: id, name, value 속성을 한 번에 자동으로 만들어주고, 서버에서 검증 오류가 발생했을 때 사용자가 입력했던 값을 그대로 다시 채워주는 기능 
* `th:errors`: 특정 필드의 검증(validation) 에러 메시지 반환



### 객체 네비게이션 (`user.name` vs `user['name']`)
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

