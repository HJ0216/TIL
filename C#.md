### 동기와 비동기
```cs
syncMethod1();
syncMethod2();
```
동기 메서드
* syncMethod1 완료 후, syncMethod2 실행
* UI Thread가 멈출 가능성이 존재

```cs
asyncMethod1();
asyncMethod2();
```
비동기 메서드
* 메서드를 호출만 하고, 완료를 기다리지 않음
* 실행 순서가 보장되지 않음

```cs
await asyncMethod1();
await asyncMethod2();
```
await + 비동기 메서드
* 비동기 메서드가 순차적으로 실행됨
* UI Thread가 멈추지 않음
