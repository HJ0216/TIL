### getElementById
```html
<div id="selection-box">Some content</div>
```
```js
const selectionBox = document.getElementById('selection-box');
```
* id 속성을 기준으로 요소를 하나만 선택
* id는 HTML 문서에서 고유해야 하기 때문에 한 개만 존재 → 반환값은 선택된 하나의 요소  
  (요소가 없다면 null 반환)
* 빠르고 효율적

### querySelector
```html
<div class="side-bar">Some content</div>
<div class="side-bar">Another content</div>
```
```js
const sideBar = document.querySelector('.side-bar');
```
* id뿐만 아니라 class, 속성, 태그 등 다양한 선택자를 지원
* 일치하는 첫 번째 요소만 선택
* 여러 클래스를 동시에 사용할 수도 있음

### JSON.parse vs JSON.stringify
* JSON.parse(string): 문자열을 JS 객체로 변환
* JSON.stringify(object): JS 객체를 JSON 문자열로 변환

### 즉시 실행
```js
// 즉시 실행
document.getElementById('alert-show-btn-1').addEventListener(setAlertMessage('아이디'));

// 화살표 함수: 클릭할 때 나중에 실행됨
document.getElementById('alert-show-btn-1').addEventListener('click', () => setAlertMessage('아이디'));

```

### const, let
* 기본은 const: `const API_KEY = 'abc123';`
* 값이 변경되어야 하면 let: `let count = 0;`

### time
* `setTimeout(function(){ 실행할코드~ }, 기다릴시간);`: 기다릴 시간 이후 1번 실행
* `setInterval(function(){ 실행할코드~ }, 기다릴시간);`: 기다릴 시간이 지날 때마다 실행

### data 속성
* HTML 요소에 추가 정보를 저장하는 HTML5 표준 방법
```html
<button class="slide-btn" data-windex="0">1</button>
<button class="slide-btn" data-windex="1">2</button>
<button class="slide-btn" data-windex="2">3</button>

```
```js
$('.slide-btn').on('click', function () {
    const index = $(this).data('windex');
    updateSlide(index);
})
```