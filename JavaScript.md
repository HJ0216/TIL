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

### const, let, var
* 기본은 const: `const API_KEY = 'abc123';`
* 값이 변경되어야 하면 let: `let count = 0;`
```js
let a = 1;
var 함수 = function () {
    a = 2;
}
console.log(a); // 1

// 변수의 범위
for (var i = 1; i < 6; i++) { 
  setTimeout(function() { console.log(i); }, i*1000 ); 
}

for (let i = 1; i < 6; i++) { 
  setTimeout(function() { console.log(i); }, i*1000 ); 
}
```

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
  * Spread 연산자(shallow copy, 맨 위의 오브젝트하나만 카피)
    ```js
    // object
    const original = {
      name: "John",
      age: 30,
      address: {
        city: "Seoul"
      }
    };

    const copied = { ...original };

    // 1단계 속성은 독립적
    copied.name = "Jane";
    console.log(original.name); // "John" (영향 없음)

    // 중첩된 객체는 참조를 공유
    copied.address.city = "Busan";
    console.log(original.address.city); // "Busan" (변경됨!)

    // array
    const arr1 = [1, 2, [3, 4]];
    const arr2 = [...arr1];

    arr2[0] = 99;
    console.log(arr1[0]); // 1 (영향 없음)

    arr2[2][0] = 99;
    console.log(arr1[2][0]); // 99 (변경됨!)
    ```
  * slice() `var products1 = products.slice();`
2. 깊은 복사
  * `var products1 = JSON.parse(JSON.stringify(products));`

### ES6 Spread Operator 
* 괄호제거 해주는 연산자

```js
var 어레이 = ['hello', 'world'];
console.log(어레이); // ['hello', 'world']
console.log(...어레이); // 'hello', 'world'

var 문자 = 'hello';
console.log(문자); // hello
console.log(...문자); // h e l l o
```
* 활용
  * Array 합치기/복사
    ```js
    var a = [1,2,3];
    var b = [4,5];
    var c = [...a, ...b];

    var a = [1,2,3];
    var b = [...a]; // 값 복사

    console.log(a);
    console.log(b)
    ```
  * Object 합치기/복사
  * array를 파라미터형태로 집어넣고 싶을 때
    ```js
    function 더하기(a,b,c){
      console.log(a + b + c)
    }

    var 어레이 = [10, 20, 30];
    더하기(...어레이);
    ```

### apply, call 함수
* apply: 이 함수를 실행하는데.. 저기 오브젝트에다가 적용해서 실행
  * 여러가지 유용한 함수들을 내가 원하는 곳에 붙여서 쉽게 실행가능
  * call은 apply와 동일하나 apply는 파라미터를 [array]로 한꺼번에 집어넣을 수 있고, call은 1,2,3처럼만 집어넣을 수 있음
```js
var person = {
    인사 : function(){
      console.log(this.name + '안녕')
    }
}
  
var person2 = {
    name : '손흥민'
}

person.인사.apply(person2); // person.인사()라는 함수를 쓰는데 person2라는 오브젝트에 적용해서 실행

person.인사.apply(person2, [1,2,3]);
person.인사.call(person2, 1,2,3);
```

### arguments
*  모든 입력된 파라미터를 [ ] 안에 싸매주는 키워드
```js
function 함수(a,b,c){
  for (var i = 0; i < arguments.length; i++){
    console.log(arguments[i])
  }
}

함수(2,3,4);
```

### rest 파라미터
* 원하는 파라미터 왼쪽에 ... 기호를 붙여주면 "이 자리에 오는 모든 파라미터를 [] 중괄호로 감싸준 파라미터"
  * rest는 항상 마지막 파라미터로 넣어야 함
  * 2개 이상 사용할 수 없음
```js
function 함수2(a, b, ...파라미터들){
  console.log(파라미터들); // 3,4,5,6,7
}

함수2(1,2,3,4,5,6,7);
```

### default parameter
```js
function 함수(a = 5, b = a * 2) {
    console.log(a + b);
}
함수(undefined, undefined);
```

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

### constructor
```js
function MakeInstance(){ // constructor는 대문자로 시작
  this.name = 'Kim';
  this.age = 15;
  this.sayHi = function(){
    console.log('안녕하세요');
  }
}

var 학생1 = new MakeInstance();
```
* 파라미터 문법
  ```js
  function MakeInstance(name){
    this.name = name;
    this.age = 15;
    this.sayHi = function(){
      console.log('안녕하세요' + this.name);
    }
  }
  var 학생1 = new MakeInstance('kim')
  var 학생2 = new MakeInstance('lee')

  학생1.sayHi()
  ```
* prototype
  * prototype에 추가된 데이터들은 자식들이 직접 가지는게 아니라 부모만 가지고 있음
  ```js
  function Product(name, price){
      this.name = name;
      this.price = price;
      this.vat = function(){
          console.log(this.price * 0.1);
      }
  }

  const product1 = new Product('shirts', 50_000);
  console.log(product1);

  Product.prototype.isBestSeller = true;
  console.log(product1.isBestSeller); // true

  var arr = [1,2,3];
  // var arr = new Array(1,2,3);
  console.log( arr.sort() );
  // Array라는 Constructor에 prototype으로 sort()가 있음

  Student.prototype = {
    sayHi: function(){
        console.log('안녕 나는 ' + this.name);
    },
    getAge: function(){
        return this.age;
    },
    introduce: function(){
        console.log(`${this.name}이고 ${this.age}살입니다`);
    }
  }
  ```
* 변경이 잦은 변수나 함수는 constructor, 변경이 없는 변수나 함수는 prototype에 보관
* prototype에 넣은 것들은 복사되지 않기 때문에 "메모리 절약"이라는 이점
  * 함수같은 경우엔 변동사항이 거의 없어서 prototype에 보관
* 자주 사용할법한 내장함수들을 많이 만들어두시면 더 효율적인 코딩생활이 가능 
* 혹은 이런 함수들 모아서 나중에 자바스크립트 라이브러리화 해서 사용해도 좋음

### class
```js
class 유저{
  constructor(id){
    this.id = id;
    this.email = name;
  }
  sayHi(){ // prototype에 저장
    console.log('안녕');
  }
}

class 셀러유저 extends 유저{
  constructor(id){
    super(id); // 최상단에 작성
    this.company = 'samsung';
  }
  sayHi2(){
    super.sayHi();
  }
}

var user = new 셀러유저('kim')
user.sayHi2()
```

### Hoisting
* 변수나 함수의 선언부분을 변수의 범위 맨 위로 강제로 끌고가서 가장 먼저 해석
```js
console.log(이름); // 오류가 아닌 undefined
var 이름 = 'Kim';
console.log(이름);

함수();
function 함수() {
  console.log(안녕); // Cannot access '안녕' before initialization
  let 안녕 = 'Hello!';
} 

함수(); // 함수 is not a function, 아직 함수 할당이 아니라 함수 호출 X
var 함수 = function() {
  console.log(안녕);
  var 안녕 = 'Hello!';
} 
```

### 전역변수
* 전역변수를 조금 더 엄격하게 관리하거나 구분짓고 싶으면 전역변수를 만들 때와 사용할 때 window를 추가
```js
let a = 1;
var b = 2;
window.a = 3;
window.b = 4;

console.log(a + b); // 5
// var만 window를 활용한 재할당 가능
```

### Tagged Literals
* 문자 중간중간에 있는 단어 순서를 바꾸거나 변수를 제거하거나 할 때 유용
```js
var 변수 = '손흥민';

function 해체분석기(문자들, 변수1, 변수2){
  console.log(문자들); // array
  console.log(변수1);
  console.log(변수2);
}

해체분석기`안녕하세요 ${변수} 입니다`;
// 첫째 파라미터 문자들은 `백틱` 내의 순수 문자만 골라서 Array로 만들어놓은 파라미터
// 둘째 파라미터 변수들은 `백틱` 내의 ${} 변수를 담는 파라미터
```

### 오브젝트
```js
function 글자세기(글){
  var 결과 = {};
    [...글].forEach(function(a){
      if( 결과[a] > 0 ){ 결과[a]++ } else { 결과[a] = 1 } // 원래 없는 요소를 추가하기 가능
    }); 
  console.log(결과);
}
```
```js
var 이름1 = { name : '김' };
var 이름2 = { name : '김' };
console.log(이름1==이름2); // false
// == 등호로 비교한 건 object 두개가 아닌 화살표 두개

var 이름3 = 이름1;
console.log(이름1==이름3); // true
```
* 함수를 이용해 object를 변경
```js
var 이름1 = { name : '김' };  // 이름1 → 객체A를 가리킴

function 변경(obj){
    // obj도 객체A를 가리킴 (같은 곳을 봄)
    
    obj = { name : 'park' };  
    // obj가 새로운 객체B를 가리키도록 변경
    // 하지만 이름1은 여전히 객체A를 가리킴!
}

// 이름1에 새로운 객체를 할당하려면
변경(이름1);
console.log(이름1.name);  // '김' (객체A는 그대로)

var 이름1 = { name : '김' };

function 변경(obj){
    return { name : 'park' };  // 새 객체를 반환
}

이름1 = 변경(이름1);  // 반환값을 이름1에 다시 할당
console.log(이름1.name);  // 'park' ✅
```
