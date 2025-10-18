### inline, block, inline-block, span

- `display: inline;`은 텍스트처럼
  - inline 요소들은 기본적으로는 옆으로 쭉 나열 되다가, 공간이 모자라면 다음 줄로 넘어감
  - 기본적으로 사각 박스 형태가 아니기 때문에 width, height로 크기를 설정할 수 없음(img 제외)
- `display: block;`은 쌓이는 상자처럼
  - width는 옆으로 늘어날 수 있는 만큼 최대한(자기 부모 요소의 width 만큼) 자리 차지
  - height는 내용물의 높이만큼 자리 차지
    - block 요소에 아무것도 넣지 않는다면, height는 0이기 때문에 우리 눈에는 아무것도 안보임
  - 박스의 width를 300px로 해서 오른쪽에 충분한 공간이 남아있지만, 둘 다 block 요소이기 때문에 다음 줄로 넘어가서 배치
- `inline-block`
  - inline처럼 텍스트 흐름대로 쭉 나열되고, block 처럼 박스 형태라 width, height로 크기 설정이 가능
  - `<태그>` 사이에 스페이스바 공백도 보여줌
- `span`
  - 텍스트의 일부만 스타일을 변경하고 싶을 때 사용
  - 폭, 높이 등을 단독으로 결정할 수 없으므로 `<p>`를 이용해서 폭, 높이를 설정

### margin: auto

- 남아있는 여백을 auto에서 모두 소비
  - 사용 예시
    - 블록 요소 가로 중앙: `margin: 0 auto`
    - Flex 컨테이너에서 세로 방향 공간 채우기: 자식에 `margin-top: auto` 등(컨테이너 높이 필요)

```css
.flex-item {
  margin-left: auto; /*가장 마지막 item만 왼쪽 정렬*/
}
```

### display: none, visibility: hidden, opacity: 0

- `display: none`
  - 모달, 알림창 등 완전히 숨기고 공간도 없애야 할 때
  - 토글 기능
  - DOM에는 존재하나, 대부분의 스크린리더와 SEO에서 무시됨
    ```css
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0); /*보이는 영역을 잘라내는(clipping) 속성*/
      white-space: nowrap;
      border: 0;
    }
    ```
- `visibility: hidden`
  - 레이아웃 유지하면서 일시적으로 숨겨야 할 때
  - 애니메이션에서 중간 상태
  - 자식 요소는 보여야 할 때
  - DOM에는 존재하나, 대부분의 스크린리더와 SEO에서 무시됨
- `opacity: 0`
  - 공간 차지, 포인터/포커스 가능
  - 스크린리더에도 노출됨(의도적 비노출 시 `aria-hidden="true"` 등 추가)
  - 애니메이션에 적합

### position

- static
  - 요소 기본 위치
- absolute
  - absolute는 자기 부모 중에서 처음으로 position이 설정된 요소(static 제외)를 기준으로 위치함
    - 없을 경우, body 기준으로 동작
- fixed
  - 뷰포트(브라우저 창) 기준으로 배치
  - 스크롤해도 항상 같은 위치에 고정
- sticky
  - 스크롤 위치에 따라 동작이 변경
    - 평소: relative처럼 동작
    - 임계값 도달: fixed처럼 고정
  - 주의점
    - 스크롤 컨테이너가 존재해야 함
    - top 등 좌표 속성과 함께 사용
    - 조상에 `overflow`가 설정되면 sticky가 동작하지 않을 수 있음

### flex

- 속성
  - 컨테이너에 적용하는 속성
  - 아이템에 적용하는 속성
- 특성

  - Flex 아이템들은 가로 방향으로 배치

    - inline-flex 사용 시, container가 flex-item width만큼으로 맞춰짐

      ```css
      .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 30px;
        height: 30px;
      }

      /* 
      icon 이미지 사이즈가 다를 경우, padding만으로 조절 시 버튼 크기가 달라짐
      버튼에 width와 height를 고정시키고, flex를 활용해서 중앙에 위치
      inline-flex 사용 시, 버튼 옆 글자 위치 가능
      */
      ```

  - 자신이 가진 내용물의 width 만큼만 차지(inline 요소 처럼)
  - height는 컨테이너의 높이만큼 늘어남

- `flex-wrap`
  - nowrap
  - wrap
  - wrap-reverse
- `justify` 메인축 방향으로 정렬
- `align` 수직축 방향으로 정렬
  - baseline: 텍스트 베이스라인 기준으로 정렬
  - align-content: 2줄 이상의 요소에 대해 `모든 요소`에 대해 정렬
  - align-items: 모든 요소들이 `각각` 어떻게 정렬할지를 지정
- `flex-basis`
  - Flex 아이템의 기본 크기를 설정
    ```css
    .flex-item {
      flex-basis: 0; /*콘텐츠 크기 무시, 0부터 시작해서 flex-grow 비율에 따라 확장*/
      flex-basis: auto; /*content 크기, width가 있을 경우, width 값*/
    }
    /*flex: 1; 설정 시, flex-basis: 0;으로 설정됨*/
    ```
  - width가 100px이 안되는 item은 100px로 늘어나고, 원래 100px이 넘는 item은 그대로 유지
    - 반면에 width를 설정하면, 원래 100px을 넘는 item도 100px로 맞춰짐
    - 고정 크기의 column은 width 사용이 편리
      - flex-basis 설정이 width보다 우선하므로 basis는 auto(기본값)로 두고 width를 설정하는 방식
- `flex-grow`
  - flex-basis의 값보다 커질 수 있는지를 결정하는 속성
  - flex-grow에 들어가는 숫자: 아이템들의 flex-basis를 제외한 여백 부분을 flex-grow에 지정된 숫자의 비율로 나누어 가짐
- `flex-shrink`
  - 아이템이 flex-basis의 값보다 작아질 수 있는지를 결정
  - 0으로 세팅해서 하나의 컬럼의 width를 고정하고 나머지 column의 width를 가변적으로 만들 수 있음
    ```css
    .flex-container {
      display: flex;
    }
    .flex-item:nth-child(1) {
      width: 100px;
      flex-shrink: 0;
    }
    .flex-item:nth-child(2) {
      flex-grow: 1;
    }
    ```
- order
  - order를 부여하지 않은 것은 `order:0`;
- 반응형 컬럼

```css
/* 고정 + 가변 컬럼 */
.flex-container {
  display: flex;
}
.flex-item:first-child {
  width: 100px;
  flex-shrink: 0;
}
.flex-item:nth-child(2) {
  flex-grow: 1;
}
.flex-item:last-child {
  width: 100px;
  flex-shrink: 0;
}

/* footer 고정 */
.flex-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.flex-item:nth-child(2) {
  flex-grow: 1;
}
```

#### flex UI

- Menu

```html
<ul class="menu-container">
  <li class="menu-item"><a href="#" class="menu-link">Home</a></li>
  <li class="menu-item"><a href="#" class="menu-link">About</a></li>
  <li class="menu-item"><a href="#" class="menu-link">Product</a></li>
  <li class="menu-item"><a href="#" class="menu-link">Contact</a></li>
</ul>
```

```css
.menu-container {
  display: flex;
}
.menu-item {
  background-color: goldenrod;
  width: 25%;
}
.menu-item:hover {
  background-color: gold;
  width: 35%;
  transition: all 0.3s ease;
}
.menu-link {
  display: block;
  padding: 1rem; /*현재 내 폰트사이즈만큼*/
  font-size: 1.2em;
  font-weight: bold;
  color: #444;
  text-decoration: none;
  text-align: center;
}
```

- search

```html
<form class="search-form">
  <input type="search" />
  <input type="submit" value="찾기" />
</form>
```

```css
.search-form {
  display: flex;
  height: 40px;
}

.search-form input[type='search'] {
  border: 0;
  border-radius: 0.3em;
  font-size: 1rem;
  flex-grow: 1;
  margin-right: 10px;
}

.search-form input[type='submit'] {
  width: 4em;
  border: 0;
  border-radius: 0.3em;
  font-size: 1rem;
  background-color: goldenrod;
}
```

- bullet list

```html
<ul class="info-list">
  <li class="info-list-item">
    Lorem ipsum dolor sit amet consectetur, adipisicing elit.
  </li>
  <li class="info-list-item">
    Lorem ipsum dolor sit amet consectetur, adipisicing elit.
  </li>
  <li class="info-list-item">
    Lorem ipsum dolor sit amet consectetur, adipisicing elit.
  </li>
</ul>
```

```css
.info-list-item {
  display: flex;
  margin: 0.5em 0;
}

.info-list-item::before {
  content: '✌️';
  margin-right: 0.5em;
}
```

- profile

```html
<ul class="user-list message-list">
  <li class="user-item message-item">
    <!-- DB에서 불러와서 넣어주기가 inline이 편함 -->
    <figure
      class="user-photo"
      style="background-image: url(/images/ilbuni.png);"
    ></figure>
    <p class="message-content">
      Lorem ipsum dolor sit amet consectetur adipisicing elit.
    </p>
  </li>
  <li class="user-item message-item">
    <figure
      class="user-photo"
      style="background-image: url(/images/ilbuni.png);"
    ></figure>
    <p class="message-content">
      Lorem ipsum dolor sit amet consectetur adipisicing elit.
    </p>
  </li>
  <li class="user-item message-item">
    <figure
      class="user-photo"
      style="background-image: url(/images/ilbuni.png);"
    ></figure>
    <p class="message-content">
      Lorem ipsum dolor sit amet consectetur adipisicing elit.
    </p>
  </li>
</ul>
```

```css
.user-item {
  display: flex;
  margin-bottom: 1.5em;
}

.user-photo {
  width: 50px;
  height: 50px;
  border: 2px solid #333;
  border-radius: 50%;
  background-color: gold;
  background-repeat: no-repeat;
  background-position: top;
  background-size: 150%;
  flex-shrink: 0;
  margin-right: 0.5em;
}
```

- profile2

```html
<ul class="user-list friend-list">
  <li class="user-item friend-item">
    <!-- DB에서 불러와서 넣어주기가 inline이 편함 -->
    <figure
      class="user-photo"
      style="background-image: url(/images/ilbuni.png);"
    ></figure>
    <p class="user-name">
      Lorem ipsum dolor sit amet consectetur adipisicing elit.
    </p>
  </li>
  <li class="user-item friend-item">
    <figure
      class="user-photo"
      style="background-image: url(/images/ilbuni.png);"
    ></figure>
    <p class="user-name">
      Lorem ipsum dolor sit amet consectetur adipisicing elit.
    </p>
  </li>
  <li class="user-item friend-item">
    <figure
      class="user-photo"
      style="background-image: url(/images/ilbuni.png);"
    ></figure>
    <p class="user-name">
      Lorem ipsum dolor sit amet consectetur adipisicing elit.
    </p>
  </li>
</ul>
```

```css
.friend-item {
  align-items: center;
}

.user-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

- modal

```html
<div class="modal">
  <div class="dialog">
    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Facere saepe ullam
    dignissimos unde velit eum consectetur vero. Dolore, dolores! Iusto
    voluptates numquam ipsum qui accusantium, quod magnam excepturi accusamus
    ullam.
  </div>
</div>
```

```css
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
}
.dialog {
  width: 50vw;
  padding: 0.5em;
  border-radius: 1em;
  background-color: white;
}
```

- card view

```html
<div class="card-list-con">
  <ul class="card-list">
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Molestias
        inventore dignissimos deserunt, magni repudiandae reiciendis quo soluta.
        Sit nisi molestias quis quia natus, laboriosam quas minus! Hic
        necessitatibus facere eius.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt. Lorem ipsum dolor sit amet consectetur adipisicing elit.
        Dolore, nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
    <li class="card-item">
      <figure
        class="card-image"
        style="background-image: url(/images/ilbuni.png);"
      >
        <img src="/images/ilbuni.png" alt="ilbuni" />
      </figure>
      <div class="card-desc">
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Dolore,
        nesciunt.
      </div>
    </li>
  </ul>
</div>
```

```css
.card-list-con {
  overflow-x: hidden;
}
.card-item {
  margin-bottom: 2em;
  display: flex;
  flex-direction: column;
}
.card-image {
  height: 0;
  padding-bottom: 60%; /*padding %: 요소의 가로폭(width)을 기준으로 계산*/
  background-color: lightgray;
  background-repeat: no-repeat;
  background-position: center;
  background-size: cover;
}
.card-image img {
  display: none;
}

.card-desc {
  background-color: white;
  padding: 1em;
  flex-grow: 1;
}

@media (min-width: 600px) {
  .card-list {
    display: flex;
    flex-wrap: wrap;
    margin: 0 -1rem;
  }
  .card-item {
    width: 50%;
    padding: 0 1rem;
  }
}

@media (min-width: 900px) {
  .card-item {
    width: 33.33%;
  }
}
```

### grid

- Edge 포함 기타 최신 브라우저에서 사용 가능
- 부모 `<div>`에 display : grid를 설정하면 자식 `<div>`들은 전부 격자처럼 진열
- 속성
  - 컨테이너에 적용하는 속성
  - 아이템에 적용하는 속성
- `inline-grid`
  - 컨테이너가 inline-block처럼 동작
- grid-template-rows: 격자의 행 높이와 갯수
  - grid-auto-rows: row 개수를 미리 알 수 없는 경우 사용: `grid-auto-rows: minmax(200px, auto)`
- grid-template-columns: 격자의 열 너비와 갯수
  - grid-auto-columns
- grid-auto-flow
  - `row`(기본값) 또는 `column`, `dense` 등의 값을 사용하여 Grid 아이템이 남은 공간을 행 우선 또는 열 우선으로 어떻게 채워나갈지 정의
- fr: 숫자 비율대로 트랙의 크기를 나눔
- repeat(반복횟수, 반복값)
- minmax(최소값, 최대값)

  ```css
  .grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(20%, auto));
    /*min에 맞춰서 반복횟수 결정
    min을 px로 할 경우, 자동으로 반응형 ui 구현 가능
  
    단, auto-fill은 개수가 모자를 경우, 빈공간이 생기지만 auto-fit을 쓸 경우 자동으로 빈 공간을 채워줌
    */
  }
  ```

- grid-column, grid-row
  - grid-column-start가 시작 번호, grid-column-end가 끝 번호
  - grid-column은 start와 end 속성을 한번에 쓰는 축약형
  - 2개의 셀에 같은 column/row를 줄 경우 겹치기도 가능

```css
/*1. */
.item:nth-child(1) {
  grid-column-start: 1;
  grid-column-end: 3;
  grid-row-start: 1;
  grid-row-end: 2;
}

.item:nth-child(1) {
  grid-column: 1 / 3;
  grid-row: 1 / 2;
}

/* 몇 개의 셀을 차지하게 할 것인지를 지정*/
.item:nth-child(1) {
  /* 1번 라인에서 2칸 */
  grid-column: 1 / span 2;
  /* 1번 라인에서 3칸 */
  grid-row: 1 / span 3;
}
```

- grid-template-areas
  - 영역 이름으로 그리드 정의

```css
/*2.*/
.grid-nav {
  grid-area: 헤더;
}
.grid-sidebar {
  grid-area: 사이드;
}

.grid-container {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr; /*repeat(4, 1fr)*/
  grid-template-rows: 100px 100px 100px;
  gap: 10px;
  grid-template-areas:
    '헤더 헤더 헤더 헤더'
    '사이드 사이드 . .'
    '사이드 사이드 . .';
}
```

### 단위

```css
.box {
  width: 16px; /* 기본 px 단위 */
  width: 1.5rem; /* html태그 혹은 기본 폰트사이즈의 1.5배 */
  width: 2em; /* 내 폰트사이즈 혹은 상위요소 폰트사이즈의 2배 */
  width: 50vw; /* 브라우저(viewport) 화면 폭의 50% */
  width: 50vh; /* 브라우저(viewport) 화면 높이의 50% */
}
```

### font-family

```css
body {
  font-family: 'gulim', 'gothic';
}
```

- 웹사이트 이용자의 컴퓨터에 설치가 된 폰트들을 적용

```css
@font-face {
  font-family: '이쁜폰트';
  src: url(nanumsquare.ttf);
}
```

- 사용자의 컴퓨터에 설치되지 않은 폰트를 사이트에서 이용

### background

- `background-image`: url(../images/bg.jpg);
  - `linear-gradient( rgba(0,0,0,0.5), rgba(0,0,0,0.5) ), url(이미지 경로)`: 투명도 0.5의 검은색을 입힌 후에 배경 겹치기
  - 이미지 background overlay  
    `background-image: linear-gradient(rgba(0,0,0,0.4),rgba(0,0,0,0.4)), url(portfolio-1.jpg);`
- `background-size`
  - 배경 이미지가 배경 영역에 꽉 차도록 비율을 유지하며 채워짐
  - 배경 영역을 완전히 덮기 위해 이미지의 일부가 잘릴 수 있지만, 여백(빈 공간)은 발생하지 않음
- `background-repeat`
- `background-position`
  - 요소에 적용한 배경 이미지가 어디서부터 시작될지 위치를 지정
- `background-attachment`
  - 요소에 적용한 배경 이미지가 어느 기준에 부착(attachment)될지를 지정
  - fixed, scroll, local

### 가로선, 세로선

- 가로선 `<hr/>`
- 세로선 `<div class="vr"></div> `

## 주의사항

### width

- width는 content 영역만을 의미하므로 padding을 줄 경우, 태그의 전체 width는 지정한 크기를 넘어설 수 있음
  - `box-sizing: border-box`시, padding과 border값을 포함한 width로 계산됨
    - `content-box;`: 박스 폭 - padding 안쪽
- min-width

```css
.flex-container {
  min-width: 100vw;
  border: 10px solid red;
  /*가로 스크롤이 생길 경우, 100vw를 넘어서는 구간은 border가 사라질 수 있으므로 width보다 min-width 사용*/
}
```

- `width: 0`
  - 시각적 폭만 0일 뿐, 접근성/포커스/SEO 비노출을 보장하지 않음

### float

- float를 쓰면 요소를 띄우다보니 다음에 오는 HTML 요소들이 제자리를 찾지 못하는 문제 발생
  - 다음 태그/현재 태그 가상 요소에 `clear: both; float: none;` 기재

### margin collapse effect

- 박스들의 테두리가 만나면 margin이 합쳐짐
  - 둘 중에 더 큰 마진을 하나만 적용
  - 두 박스의 테두리가 겹치지 않도록 부모 박스에 padding을 1px 조금 주는 것으로 해결

### stacking context

1. 기본 규칙: DOM 순서
2. stacking context가 만들어지면 규칙이 변경

- stacking context 안에서는 DOM 순서보다 z-index 값이 우선 적용
  - position: relative/absolute/fixed/sticky + z-index 지정
  - opacity < 1
  - transform, filter, perspective 등 CSS 속성
  - isolation: isolate
  - flex/grid item 등

### 레이아웃 만들기

1. 레이아웃은 항상 박스부터 만들고 시작

- 박스들을 전부 `<div>`로 구현

2. PC 레이아웃을 만들 때 항상 container 또는 wrap 박스 사용

- container 박스엔 항상 `width`, `max-width`를 지정
  - 브라우저화면이 축소되어도 내부 `div` 박스들이 찌그러지지 않음

### animation 만들기

1. 최종 스타일 모양 만들기
2. 시작 스타일 모양 만들기(트리거가 없는 상황)
3. 트리거 상황에 최종 스타일 부여
4. transition으로 부드러운 동작 만들기

### transform

- 어떤 요소를 독립적으로 움직이게 만들고 싶을 때 사용
- 뭔가 이동시키고 싶으면 margin 쓰는 것 보다 transform 쓰는게 빠르게 동작
  - margin: Layout → Paint → Composiition
  - tanslate: Composiition
- transform을 사용하면 요소가 시각적으로만 이동하지만, 원래 자리는 여전히 차지하고 있음 → 브라우저는 원래 위치부터 변환된 위치까지의 전체 공간을 문서 크기로 계산
  - `position: fixed`를 추가하면 요소가 문서 흐름에서 제거되고, 문서 크기 계산에 포함되지 않음
- `translate(-50%, -50%);`: 요소를 정중앙에 위치

#### Layout → Paint → Composiition

- Layout
  - **요소의 크기와 위치 계산**
  - 요소의 위치, 크기를 계산하는 단계
  - DOM 트리를 기반으로 레이아웃 트리 생성
  - 가장 비용이 큰 작업
  - **Layout을 발생시키는 속성**
    ```css
    width, height, margin, padding, border
    top, left, right, bottom (position)
    display, float, position
    ```
- Paint

  - **실제로 픽셀을 그리는 작업**
  - 계산된 레이아웃을 바탕으로 화면에 그림
  - 색상, 그림자, 테두리 등을 픽셀로 변환
  - Layout보다는 빠르지만 여전히 비용 있음
  - **Paint를 발생시키는 속성**
    ```css
    color, background, border-radius
    box-shadow, visibility, outline
    ```

- Composite
  - **레이어를 합성해서 최종 화면 구성**
  - 여러 레이어를 GPU에서 합성
  - 가장 빠른 작업 (GPU 가속)
  - **Composite만 발생시키는 속성**
    ```css
    transform
    opacity
    filter
    will-change
    ```

### @keyframes

- 커스텀 애니메이션을 정의하기 위한 공간

```css
@keyframes 움찔움찔 {
  0% {
    transform: translateX(0px); /* 애니메이션이 0%만큼 동작시 */
  }
  50% {
    transform: translateX(-20px); /* 애니메이션이 50%만큼 동작시 */
  }
  100% {
    transform: translateX(20px); /* 애니메이션이 100%만큼 동작시 */
  }
}

.box:hover {
  animation-name: 움찔움찔;
  animation-duration: 1s;
  animation-timing-function: linear;
  animation-delay: 1s; /*시작 전 딜레이*/
  animation-iteration-count: 3; /*몇회 반복*/
  animation-play-state: paused; /*애니메이션을 멈추고 싶은 경우 자바스크립트로 이거 조정*/
  animation-fill-mode: forwards; /*애니메이션 끝난 후에 원상복구 하지말고 정지*/
}
```

## 문법

### selector

- `공백` 하위 모든 자식 태그
- `>` 바로 아래 자식 태그
- `태그[속성명=속성값]`
  - `^=`: 시작값
  - `$=`: 끝값
  - `*=`: 포함값
- `:nth-child(n)`
  - `ul:nth-child(1)`: 첫번째 ul 요소
  - `ul :nth-child(1)`: ul 자식인 li 첫번째 요소
- `.icon-parents-overlay:hover .icon-overlay`
  - .icon-parents-overlay에 마우스를 올렸을 때 그 안에 있는 .icon-overlay에 스타일을 적용
- `+` (인접 형제)

  - 같은 계층에 있을 때 적용
  - thymeleaf에서 checkbox input 사용 시, hidden input이 생성되어 +가 동작하지 않을 수 있으므로 주의

  ```html
  <h2></h2>
  <p></p>
  <p></p>
  <p></p>
  ```

  ```css
  h2 + p {
    color: red;
  }
  /*<h2> 바로 뒤의 첫 번째 <p>만 빨간색
  h2와 p 태그 사이에 다른 요소가 있을 경우, 적용 X*/

  h2 ~ p {
    color: blue;
  }
  /*<h2> 뒤에 나오는 모든 <p> 가 파란색*/
  ```

### Pseudo-element

- 특정 HTML 요소의 안쪽 일부만 스타일을 주고 싶을 때
- ::after: 내부의 맨 마지막 부분에 특정 글자 추가
  - clear: both; 박스 생성
    ```css
    .box::after {
      content: '';
      display: block;
      clear: both;
      float: none;
    }
    ```
- ::before: 내부의 맨 앞 부분에 특정 글자 추가
  - container에 overlay처럼 추가할 경우, 그 안의 요소들을 가릴 수 있음에 유의

### innerHTML vs innerText vs textContent

- innerHTML
  - HTML 태그 포함 전체를 가져오거나 설정
- innerText
  - 텍스트만 가져오거나 설정, HTML 태그는 무시/제거
  - 보이는 텍스트만 필요하거나 사용자가 보는 그대로 복사할 때 사용
- textContent
  - 렌더링 무시하고 raw 텍스트 그대로 반환하므로 DOM만 읽으면 되어 빠름

```html
<div id="test">
  Hello <strong>World</strong>
  <span style="display:none">Hidden</span>
</div>

<script>
  const div = document.getElementById('test');

  console.log(div.innerHTML);
  // 'Hello <strong>World</strong> <span style="display:none">Hidden</span>'

  console.log(div.innerText);
  // 'Hello World' (보이는 텍스트만, Hidden은 제외)

  console.log(div.textContent);
  // 'Hello World \nHidden' (Hidden 포함)
</script>
```

### media query

- 권장 Breakpoint: 1200px / 992px / 768px / 576px
  - 1200px 이하는 태블릿, 768px 이하는 모바일 가장 간편
- orientation
  - landscape(가로 모드), portrait(세로 모드)

### scss

- SASS로 코드를 짰으면 그걸 CSS 파일로 변환해주는 변환기를 돌려서 변환된 CSS 파일을 HTML 파일과 함께 써야함
- SASS 문법

  - 값을 저장해놓고 쓰는 '변수'

    ```css
    $main-color: #5d58ff;

    .box {
      width: 100%;
      color: $main-color;
    }

    /*기존 css*/
    :root {
      --main-color: red;
    }
    .box {
      width: 100%;
      color: var(--main-color);
    }
    ```

    - 덧셈, 뺄셈: px 단위는 px 단위끼리, % 단위는 % 단위끼리
    - 곱셈 나눗셈은 보통 뒤에 단위를 쓰지 않음
    - 곱셈 나눗셈은 괄호 안에 작성

  - Nesting

    - Nesting할 때 괄호를 3개 4개 타고 들어가는 대신 새로운 class를 부여

      ```css
      .navbar {
        ul {
          width: 100%;
        }
        li {
          color: black;
        }
      }

      .navbar ul {
        width: 100%;
      }
      .navbar li {
        color: black;
      }

      div.container {
        > div {
          p.first {
            > span {
            }
          }
        }
      }

      div.container > div p.first > span {
      }

      .navbar {
        :hover {
          color: blue;
        }
      }

      .navbar :hover {
      }

      .navbar {
        &:hover {
          color: blue;
        }
      }

      .navbar:hover {
      }
      ```

  - @extend

    - 이미 있는 클래스를 확장

      ```css
      .btn {
        font-size: 16px;
        padding: 10px;
        background: grey;
      }

      .btn-green {
        @extend .btn;
        background: green;
      }
      /*% 기호는 .대신 쓸 수 있는 임시클래스, CSS파일에서 클래스로 컴파일하지 않고싶을 때 쓰는 기호*/
      ```

    - @mixin

      - 코드를 한단어로 축약

        ```css
        @mixin 버튼기본디자인() {
          font-size: 16px;
          padding: 10px;
        }

        .btn-green {
          @include 버튼기본디자인();
          background: green;
        }

        @mixin 버튼기본디자인($구멍) {
          font-size: 16px;
          padding: 10px;
          background: $구멍;
        }

        .btn-green {
          @include 버튼기본디자인(#229f72);
        }
        ```

    - @use와 언더바 파일

      - @use: `scss 파일(css 파일 x)`을 해당 SCSS파일에 전부 복붙
      - 언더바 \_기호를 파일명 맨앞에 사용하시면 "이 파일은 CSS파일로 따로 컴파일하지 말아주세요" 라는 의미

      ```css
      @use '_reset.scss';

      reset.$변수명;  /* 다른 파일의 변수쓰는법 */
      @include reset.mixin이름();  /* 다른 파일의 mixin쓰는법 */
      ```

- 먼저 CSS로 모든 기능을 구현해본 뒤에 눈에띄는 반복적인 속성들을 mixin, extend 등으로 축약

### head

```html
<head>
  <meta charset="UTF-8" />
  <meta name="description" content="html 공부 중" />
  <meta name="keywords" content="HTML,CSS" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
```

- `<meta charset="UTF-8" />`
  - HTML 문서의 문자 인코딩(encoding)을 지정
  - HTML 문서의 최상단에 넣어야 브라우저가 올바르게 문자 해석 가능
- `<meta name="description" content="..." />`
  - 페이지 설명(description)을 검색 엔진에 전달
- `<meta name="keywords" content="..." />`
  - 페이지와 관련된 키워드를 검색 엔진에 제공
- `<meta name="viewport" content="width=device-width, initial-scale=1.0" />`
  - 화면 너비에 맞춰 페이지 크기 설정, 페이지 초기 확대 비율 설정

```html
<head>
  <meta property="og:image" content="/이미지경로.jpg" />
  <meta property="og:description" content="사이트설명" />
  <meta property="og:title" content="사이트제목" />
</head>
```

- OG 태그(Open Graph tags)
  - 페이스북, 카카오톡, 트위터 같은 SNS에서 공유될 때 웹페이지의 미리보기(썸네일, 제목, 설명 등)를 제어하는 메타 태그
  - `<meta property="og:image" content="/이미지경로.jpg" />`
    - 공유 시 표시할 썸네일 이미지 지정
  - `<meta property="og:description" content="페이지 설명" />`
    - 공유될 때 보이는 페이지 설명
  - `<meta property="og:title" content="사이트제목" />`
    - 공유될 때 보이는 페이지 제목

### 📚 참고

[코딩 애플](https://codingapple.com/)  
[코딩 에브리바디](https://codingeverybody.kr/)  
[1분 코딩](https://studiomeal.com/)  
[CSS Flex와 Grid 제대로 익히기](https://www.inflearn.com/course/css-flex-grid-%EC%A0%9C%EB%8C%80%EB%A1%9C-%EC%9D%B5%ED%9E%88%EA%B8%B0?srsltid=AfmBOoph2CvkviehXncsxNd9-Uu8JZSRjEGRb3s1xcZ5p1skChqZDGpo)  
[flukeout](https://flukeout.github.io/)  
[CSS Triggers](https://css-triggers.com/)  
[Adobe Color](https://color.adobe.com/ko/create/color-wheel)
