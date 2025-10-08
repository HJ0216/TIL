### const, let, var
* `const`
  * 재할당 불가능한 상수 선언
  * 선언과 동시에 초기화 필수
  * 블록 스코프
  * 같은 스코프에서 재선언 불가
* let
  * 재할당 가능한 변수 선언
  * 블록 스코프
  * 같은 스코프에서 재선언 불가
* var
  * 재할당 가능
  * 함수 스코프 (블록 무시)
  * 재선언 가능
* 기본은 `const`를 사용하되, 값이 변경되어야 하면 `let` 사용

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

### DOM(Document Object Model)
* 자바스크립트가 HTML에 대한 정보들 (id, class, name, style, innerHTML 등)을 object 자료로 정리한 것
  * 자바스크립트가 HTML 조작을 하기 위해선 HTML을 자바스크립트가 해석할 수 있는 문법으로 변환
  * 실제로 브라우저는 HTML 페이지를 열어줄 때 HTML을 자바스크립트로 쉽게 찾고 바꾸기 위해 object와 비슷한 자료형에 담아둠
```js
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

### data 속성
* HTML 요소에 추가 정보를 저장하는 HTML5 표준 방법
```html
<button class="slide-btn" data-index="0">1</button>
<button class="slide-btn" data-index="1">2</button>
<button class="slide-btn" data-index="2">3</button>

```
```js
$('.slide-btn').on('click', function () {
    const index = $(this).data('index');
    updateSlide(index);
})
```

### 좋은 관습
* 자주쓰는 selector는 변수에 넣어 쓰기
```js
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

### 이벤트 버블링
* 어떤 HTML 태그에 이벤트가 발생하면 그의 모든 상위 요소까지 이벤트가 실행되는 현상
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

### parameter
* arguments
  *  모든 입력된 파라미터를 [ ] 안에 싸매주는 키워드
  ```js
  function 함수(a,b,c){
    for (var i = 0; i < arguments.length; i++){
      console.log(arguments[i])
    }
  }

  함수(2,3,4);
  ```
* rest 파라미터
  * 원하는 파라미터 왼쪽에 ... 기호를 붙여주면 "이 자리에 오는 모든 파라미터를 [] 중괄호로 감싸준 파라미터"
    * rest는 항상 마지막 파라미터로 넣어야 함
    * 2개 이상 사용할 수 없음
  ```js
  function 함수2(a, b, ...파라미터들){
    console.log(파라미터들); // 3,4,5,6,7
  }

  함수2(1,2,3,4,5,6,7);
  ```

* default parameter
  ```js
  function 함수(a = 5, b = a * 2) {
      console.log(a + b);
  }
  함수(undefined, undefined);
  ```

### Storage
* Local Storage / Session Storage (key : value 형태로 문자, 숫자 데이터 저장가능)
  * 문자, 숫자만 key : value 형태로 저장가능하고 5MB까지만 저장 가능
  * JSON.stringify() 안에 array/object 집어넣으면 JSON으로 바꿔서 문자로 저장 가능
    * array/object -> JSON 변환하고 싶으면 JSON.stringify()
    * JSON -> array/object 변환하고 싶으면 JSON.parse()
* Indexed DB (크고 많은 구조화된 데이터를 DB처럼 저장가능, 문법더러움)
* Cookies (유저 로그인정보 저장공간)
* Cache Storage (html css js img 파일 저장해두는 공간)

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
* 함수들 모아서 나중에 자바스크립트 라이브러리화 해서 사용해도 좋음

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
  hello = 'hi'; // 클래스 내부에서 인스턴스 속성 설정
  // const/let/var는 지역 변수를 만들 때 쓰는 거고, 클래스 필드와는 다름

  constructor(id){
    super(id); // 최상단에 작성
    this.company = 'samsung'; 
    // this(현재 인스턴스) 필수
    // this 없이 쓸 경우 지역/전역 변수를 참조하게 됨
  }
  sayHi2(){
    super.sayHi();
  }
}

var user = new 셀러유저('kim')
user.sayHi2()
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

### 오브젝트
```js
function 글자세기(글){
  var 결과 = {};
    [...글].forEach(function(a){
      if( 결과[a] > 0 ){
         결과[a]++; // 원래 없는 요소를 추가하기 가능 
      } else {
         결과[a] = 1 ;
      } 
    }); 

  console.log(결과);
}

var 이름1 = { name : '김' };
var 이름2 = { name : '김' };
console.log(이름1==이름2); // false
// == 등호로 비교한 건 object 두개가 아닌 화살표 두개

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

### getter, setter
```js
var 사람 = {
  name : 'Kim',
  age : 30,
  setAge(나이){
    // 내부에 있는 name, age 변수를 직접 건드리지 않아서 실수를 방지할 수 있음
    this.age = parseInt(나이);
  }

  set setAge2(나이){
    this.age = parseInt(나이);
  }
}

사람.setAge('200');
사람.setAge = '200';
```
* get 함수는 파라미터가 있으면 안되고 함수 내에 return을 가져야함
* set 함수는 데이터를 입력해서 수정해주는 함수니까 파라미터가 `한 개만` 꼭 존재해야함
  * `...rest` 사용 불가능

### Destructuring
```js
var [a,b,c] = [2,3,4];

var { name : a, age : b } = { name : 'Kim', age : 30 };

var { name, age } = { name : 'Kim', age : 30 }; // key와 이름이 동일할 경우

var name = 'Kim';
var age = 30;
var obj = { name, age } // key와 동일한 이름으로 생성

function 함수( { name, age }){
  console.log(name);
  console.log(age);
}

var obj = { name : 'Kim', age : 20 };
함수(obj);
```

### 모듈
* 리액트 뷰 nodejs 이런거할 때 많이 사용
```js
var a = 10;
var b = 20;
export default a; // 1회만 사용 가능
export {a, b}; // 여러번 사용 가능
```
```html
<script type="module">
  import a from 'library.js'; //export default, 변수명 새롭게 작명 가능

  import {a,b} from 'library.js'; // export
  import {a as newA,b as newB} from 'library.js'; // export, 변수명 변경

  import a, {a,b} from 'library.js'; // export default 가장 왼쪽에 기재

  import a, * as all from '/libraray.js';
  // * : export { } 했던 애들을 모두 import
  // as로 별명을 꼭 부여
</script>
```

### Callback 함수
```js
// 즉시 실행
document.getElementById('alert-show-btn-1').addEventListener('click',
  setAlertMessage('아이디');
);

// 클릭할 때 나중에 실행됨
document.getElementById('alert-show-btn-1').addEventListener('click', 
  () => setAlertMessage('아이디')
);
```

### Promise
* 콜백함수의 문제점
  * 코드 실행 순서를 보장하는 대신, 가독성이 떨어질 수 있음
```js
첫째함수(function(){
  둘째함수(function(){
    셋째함수(function(){
      어쩌구..
    });
  });
}):
```
* 대안: Promise
```js
// Producer
var promise = new Promise(function(resolve, reject){
  // doing some heavy work(network, file read...)
  // promise가 생성되는 순간 function이 실행됨
  // function이 바로 실행되지 않는 상태일 때는 생성 시점에 유의
  resolve(data);
  reject(new Error(''));
});

// consumer
promise.then(function(value){
  // 성공(); 시
  // then은 현재 promise를 return하므로 method chaining으로 catch를 사용할 수 있음
  // return 프로미스2; // Promise 객체 리턴 시, 연속적으로 실행 및 실행 결과를 처리할 수 있음

}).catch(function(error){
  // 실패(); 시
}).finally(function(){
  //
});
```
* Promise 상태
  * 성공/실패 판정 전: <pending>
  * 성공 후: <resolved>
  * 실패 후: <rejected>
* Promise 특징
  * 동기를 비동기로 만들어주는 코드가 아님
    * Promise 안에 10초 걸리는 어려운 연산을 시키면 10초동안 브라우저가 멈춤
    * 원래 자바스크립트는 평상시엔 동기적으로 실행이 되며 비동기 실행을 지원하는 특수한 함수들(Web API,  setTimeout, addEventListener, ajax 관련 함수 등) 덕분에 가끔 비동기적 실행됨

### async, await
* async
  * 함수 앞에 붙여서 해당 함수가 항상 Promise를 반환
* await
  * async 함수 내에서만 사용 가능하며, Promise가 처리될 때까지 기다림
```js
async function fetchData() {
  try {
    const response = await fetch('https://api.example.com/data');
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}
```

### 기타 JS 라이브러리
* [swiper](https://swiperjs.com/get-started#use-swiper-from-cdn)
* [Chart.js](https://www.chartjs.org/docs/latest/)
* [Animate On Scroll](https://michalsnik.github.io/aos/)
* [EmailJS](https://www.emailjs.com/docs/introduction/how-does-emailjs-work/)



### 📚 참고
[코딩 애플](https://codingapple.com/)  
[드림 코딩](https://www.youtube.com/@dream-coding)  