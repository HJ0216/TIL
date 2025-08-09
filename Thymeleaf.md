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
