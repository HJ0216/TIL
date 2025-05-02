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
