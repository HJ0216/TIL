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
