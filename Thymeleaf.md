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
