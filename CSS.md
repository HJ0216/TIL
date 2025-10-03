### CSS 변수
```css
.selection-box {
  --border-width: 2px;
}
.selection-box::after {
  top: calc(-1 * var(--border-width));
  left: calc(-1 * var(--border-width));
  /* var(--border-width) = 2px 처럼 동작 */
}
```

### pointer-events
```cs
.selection-box {
  pointer-events: none;
  /* 
  마우스 이벤트(hover, click 등)를 통과시키고 아래 요소가 반응하게 함
  Drag Event: mousedown → mousemove → mouseup 순으로 부모 영역이 이벤트를 받아야 함 
  none으로 설정하지 않을 경우, 드래그를 할 경우 마우스가 selection-box를 누른 걸로 인식하여 드래그 이벤트 끊김
  */
}
```

### position
#### absolute
```css
.selection-box {
  position: absolute;
}
```
* position: absolute일 때
  * .selection-box는 문서 흐름에서 빠짐  
    즉, 다른 요소들과 겹쳐서 띄워지는 레이어처럼 존재  
    레이아웃을 전혀 밀거나 차지하지 않음  
    사이드바 등 다른 요소는 영향을 전혀 받지 않음
* position을 안 줬을 때 (static, 기본값)
  * .selection-box는 일반 블록 요소처럼 작동
    즉, 위치도 흐름대로 잡히고, 공간도 차지  
    너비나 높이 설정에 따라 옆에 있는 .side-bar 등을 밀거나 덮어버릴 수 있음  
    특히 width나 height가 100%라면, 사이드바 위에 확 덮여버려서 보이지 않는 것처럼 됨
* 기준
  * absolute는 자기 부모 중에서 처음으로 position이 설정된 요소를 기준으로 위치함  
    → 없다면 body 기준으로 동작함

### CSS 가상 요소
```css
.element::before {
  content: "이건 앞에";
}
.element::after {
  content: "이건 뒤에";
}
/* 필수 속성 → content (없으면 안 보임) */
```

### +, ~
```html
<div class="fortune-option">
  <input type="checkbox" id="a">
  <input type="checkbox" id="n"> 
  <label>라벨 B</label>
</div>
```
* `+`
  * 체크된 input 바로 뒤가 label이어야 적용됨
* `~`
  * 뒤에 있는 label이면 다 적용됨

### 텍스트의 일부만 스타일을 변경하고 싶을 때
* `<span>`로 감싼 뒤에 스타일 지정
  * `<span>`는 `display: inline`이라는 스타일 속성을 내포 -> 폭, 높이 등을 단독으로 결정할 수 없으므로 `<p>`를 이용해서 폭, 높이를 설정

### `<img>` 가운데 정렬
* `display : block; margin-left : auto; margin-right : auto;`

### 요소를 공중에 띄워 왼쪽/오른쪽 정렬하는 float 속성 
* float를 쓰면 요소를 붕 띄우다보니 그 다음에 오는 HTML 요소들이 제자리를 찾지 못하는 문제 발생
  * 다음 태그에 `clear: both; float: none;` 기재
  * 위의 속성을 설정할 `<div>`를 추가적으로 선언하는 방법도 있음
* float 속성으로 가로정렬할 땐 float 박스들을 싸는 하나의 큰 div 박스를 만들고 폭을 지정해야 모바일에서 안 흘러넘침


### `display : inline-block`
* <태그> 사이에 스페이스바 공백이 있다면 그대로 보여주기 때문에 가로로 정렬하려면 태그 사이의 공백도 제거해줘야 함
  * 주석 사용해서 줄바꿈 처리 가능
    ```html
    <div>
      <div class="left-box"></div><!--
    --><div class="right-box"></div>
    </div>
    ```
  * 부모 태그 폰트 사이즈 0 처리
    ```html
    <div style="font-size : 0px;">
        <div class="left-box"></div>
        <div class="right-box"></div>
    </div>
    ```

### 레이아웃 만들기
1. 뭘 만들든 레이아웃은 항상 박스부터 만들고 시작
  * 이 박스들을 전부 `<div>`로 구현
  * `<div>`는 그냥 쓰면 display : block 때문에 위아래로 배치 -> 좌우로 나란히 배치하고 싶으면 float, 혹은 inline-block 사용
2. PC 레이아웃을 만드실 때 항상 container 또는 wrap 박스 사용
  * container 박스엔 항상 width를 지정 -> 브라우저화면이 축소되어도 내부 `div` 박스들이 찌그러지지 않음

### HTML태그에 클래스 두개 이상 붙이기
* `<div class="container text-center"> </div>`

### Selector
* 공백: 하위 모든 자식 태그 접근
* >: 직계 자손
* 읽기만 해도 어떤 스타일을 주는지 알 수 있는 셀렉터가 좋은 셀렉터 사용법

### background
* background-image: url(../images/bg.jpg);
  * `linear-gradient( rgba(0,0,0,0.5), rgba(0,0,0,0.5) ), url(이미지 경로)`: 투명도 0.5의 검은색을 입힌 후에 배경 겹치기
* background-size: cover;
  * 배경 이미지가 배경 영역에 꽉 차도록 비율을 유지하며 채워짐
  * 배경 영역을 완전히 덮기 위해 이미지의 일부가 잘릴 수 있지만, 여백(빈 공간)은 발생하지 않음
* background-repeat: no-repeat;
* background-position: 100px 50px;
  * 요소에 적용한 배경 이미지가 어디서부터 시작될지 위치를 지정
* background-attachment: fixed;
  * 요소에 적용한 배경 이미지가 어느 기준에 부착(attachment)될지를 지정
  * fixed, scroll, local

# margin collapse effect 
* 박스들의 테두리가 만나면 margin이 합쳐짐
  * 둘 중에 더 큰 마진을 하나만 적용
  * 두 박스의 테두리가 겹치지 않도록 부모 박스에 padding을 1px 조금 주는 것으로 쉽게 해결 가능

### 📚 참고
[코딩 애플](https://codingapple.com/)  
[코딩 에브리바디](https://codingeverybody.kr/)  