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

### scroll
```js
window.addEventListener('scroll', function(){
  console.log( window.scrollY ); //  현재 페이지를 얼마나 위에서 부터 스크롤했는지 px 단위로 알려줌
});

window.scrollTo(x, y);
// 강제로 스크롤바를 이동

window.scrollBy(0, 100);
// 현재 위치에서부터 +100px 만큼 스크롤

document.documentElement.scrollHeight;
// 문서의 전체 높이 (스크롤 포함)

window.innerHeight;
// 현재 브라우저 창에서 보이는 화면의 높이


/*jQuery*/
$(window).on('scroll', function(){
  $(window).scrollTop();
})

$(window).scrollTop(); // 스크롤한 양
$(window).scrollTop(100) // 스크롤 강제 이동


/*div*/
var 스크롤_양 = document.querySelector('.lorem').scrollTop;
var 스크롤_가능한_실제_높이 = document.querySelector('.lorem').scrollHeight;
var padding_border_스크롤바_포함한_전체_높이 = document.querySelector('.lorem').offsetHeight;

```

### 좋은 관습
* 자주쓰는 selector는 변수에 넣어 쓰기
```js
$(".tab-button").on("click", function () {
  // orange
  let index = $(this).data("index");

  $(".tab-button").removeClass("orange");
  $(this).addClass("orange");

  // show
  $(".tab-content").removeClass("show");
  $(".tab-content").eq(index).addClass("show");
});

// 변수 치환
$(".tab-button").on("click", function () {
  const tabContent = $(".tab-content");

  // orange
  let index = $(this).data("index");

  tab.removeClass("orange");
  $(this).addClass("orange");

  // show
  tabContent.removeClass("show");
  tabContent.eq(index).addClass("show");
});
```

### 이벤트 버블링
* 어떤 HTML 태그에 이벤트가 발생하면 그의 모든 상위요소까지 이벤트가 실행되는 현상
* `e.target`은 실제 클릭한 요소(이벤트 발생한 곳)
* `e.currentTarget`은 지금 이벤트 리스너가 달린 곳(this)
* `e.preventDefault()` 실행하면 이벤트 기본 동작을 막아줌
* `e.stopPropagation()` 실행하면 내 상위요소로의 이벤트 버블링을 중단해줌
```html
<div class="tab-button">
  버튼 텍스트
  <span class="icon">🔥</span>
</div>
```

```js
$('.tab-button').on('click', function(e){
    console.log('target:', e.target);
    console.log('currentTarget:', e.currentTarget);
})

/**
 * "버튼 텍스트"를 클릭
 * target: <div class="tab-button">  (div 자체를 클릭)
 * currentTarget: <div class="tab-button">  (이벤트 등록된 곳)
 * 
 * "🔥 아이콘"을 클릭
 * target: <span class="icon">  (span을 클릭했으니까!)
 * currentTarget: <div class="tab-button">  (여전히 div)
 * */
```

### 이벤트
* 일반 이벤트
```js
$('.tab-button').on('click', function(){
  // 현재 존재하는 .tab-button에만 이벤트 등록
});

// 나중에 버튼 추가
$('.list').append('<li class="tab-button">새 탭</li>');
// → 새 탭은 클릭 안 됨! ❌
```
* 이벤트 위임
```js
$('.list').on('click', '.tab-button', function(){
  // .list에 이벤트 등록하되, .tab-button 클릭만 감지
});

// 나중에 버튼 추가
$('.list').append('<li class="tab-button">새 탭</li>');
// → 새 탭도 클릭 됨! ✅
```

### 복사
1. 얕은 복사(객체 내부 값은 공유)
  * Spread 연산자 `var products1 = [...products];`
  * slice() `var products1 = products.slice();`
3. 깊은 복사
  * `var products1 = JSON.parse(JSON.stringify(products));`

### js libs
* [swiper](https://swiperjs.com/get-started#use-swiper-from-cdn)
* [Chart.js](https://www.chartjs.org/docs/latest/)
* [Animate On Scroll](https://michalsnik.github.io/aos/)
* [EmailJS](https://www.emailjs.com/docs/introduction/how-does-emailjs-work/)

### DOM(Document Object Model)
* 자바스크립트가 HTML에 대한 정보들 (id, class, name, style, innerHTML 등)을 object 자료로 정리한 것
  * 자바스크립트가 HTML 조작을 하기 위해선 HTML을 자바스크립트가 해석할 수 있는 문법으로 변환
  * 실제로 브라우저는 HTML 페이지를 열어줄 때 HTML을 자바스크립트로 쉽게 찾고 바꾸기 위해 object와 비슷한 자료형에 담아둠
```html
<script>
  document.getElementById('test').innerHTML = '안녕'
</script>

<p id="test">임시글자</p>
<!--
아직 <p id="test">를 읽기 전이라 p태그에 대한 DOM이 아직 생성되지 않았으므로 오류 발생
-->
```
```js
// 대안
$(document).ready(function(){ 실행할 코드 }) // DOM 생성만 체크하는 함수
document.addEventListener('DOMContentLoaded', function() { 실행할 코드 }) 

$(window).on('load', function(){
  //document 안의 이미지, js 파일 포함 전부 로드가 되었을 경우 실행할 코드 
});

window.addEventListener('load', function(){
  //document 안의 이미지, js 파일 포함 전부 로드가 되었을 경우 실행할 코드
})
```

* Virtual DOM
  * html DOM의 복사본
  * html 변경사항이 일어나야하면 Virtual DOM에 먼저 반영하고 거기서 꼭 필요한 내용만 실제 DOM에 반영하는 방식으로 React, Vue 동작

### Storage
* Local Storage / Session Storage (key : value 형태로 문자, 숫자 데이터 저장가능)
  * 문자, 숫자만 key : value 형태로 저장가능하고 5MB까지만 저장 가능
  * JSON.stringify() 안에 array/object 집어넣으면 JSON으로 바꿔서 문자로 저장 가능
    * array/object -> JSON 변환하고 싶으면 JSON.stringify()
    * JSON -> array/object 변환하고 싶으면 JSON.parse()
* Indexed DB (크고 많은 구조화된 데이터를 DB처럼 저장가능, 문법더러움)
* Cookies (유저 로그인정보 저장공간)
* Cache Storage (html css js img 파일 저장해두는 공간)

### this
```js
console.log(this);
// window 객체

function 함수() {
    console.log(this);
}
// window 객체
// 단 strict 모드에서는 undefined
```
* window
  * 모든 전역변수, 함수, DOM을 보관하고 관리하는 전역객체

```js
const 오브젝트 = {
    data: {
        함수 : function(){
            console.log(this);
        },
    }
}
// data 객체
```
> `this`를 출력하면 this를 사용한 메소드를 가지고 있는 오브젝트를 출력

```js
function 객체생성(){
    this.이름 = '김';
}
let 새로운오브젝트 = new 객체생성();
console.log(새로운오브젝트);
// this: 새로 생성될 오브젝트
// 객체가 어떤 생성자 함수로부터 만들어졌는지도 확인 가능
```

```js
document.getElementById('버튼').addEventListener('click', function(e){
  console.log(this);
  // e.currentTarget
  // 지금 addEventListener 부착된 HTML 요소
});

document.getElementById('버튼').addEventListener('click', function(e){
  var 어레이 = [1,2,3];
  어레이.forEach(function(){
    console.log(this);
    // window 객체 출력
  });
});
```
* arrow function
  * 함수 내부의 this값을 재정의하지 않아 상위 요소의 this값 상속