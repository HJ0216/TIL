# 14_Parameter_파최몇_파라미터_최대_몇개까지_가능
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2024-06-16
- 수정일: 2024-06-17

<br/>



#
### 주제를 선정한 이유
저는 메서드를 만들어도 수정할 일이 많습니다..🥸 생각하지 못했던 부분을 메꾸는 코드를 만들다보면.. 자꾸 매개 변수의 개수도 늘어납니다. 하지만, 기존의 코드를 하나하나 찾아가서 매개 변수가 늘었으니, 너도 인자를 하나 더 보내주렴..🫠 하는 상황에 지쳐 오랜만에 글을 적어봅니다.

<br/>



## 주제1: Parameter를 추가하는 방법
메서드의 파라미터를 변경한다면 어떤 방식들이 있는지 정리해 보았습니다.

<br/>

### Overloading
서로 다른 매개변수를 갖는 같은 이름의 여러 개의 메서드를 정의하는 것을 오버로딩이라고 합니다.  

즉, 기존의 메서드를 수정하는 것이 아니라 이름은 같지만 매개변수 타입이나 개수가 다른 메서드를 하나 더 만들어주는 것이죠.

```java
private void helloMethod(int one){
    int i = one;
}

private void helloMethod(int one, int two){
    int i = one;
    int j = two;
}
```

이런 식으로 매개변수를 2개 사용하는 메서드를 추가로 만들어주게 되는 것입니다.



### Default Parameter
저는 메서드 내용이 길어서, Overloading 시 코드 중복이 문제가 된다고 생각을 했습니다. 그래서 오버로딩보다는 매개변수를 추가할 때 기본값을 설정하는 방식을 사용했습니다.

```java
private void helloMethod(int one, int two = 0){
    int i = one;
    int j = two;
}
```



### Add Parameter
기본 파라미터 값 설정으로 해결이 안되는 경우가 있습니다. 넘어오는 인자값이 모두 유동적인 경우죠. 그럴 땐.. '그냥 기본값으로 처리하고, 메서드 내부에서 추가 처리를 해줄까..?'라는 고민을 하곤 합니다.. 하지만, 매개변수로 넘어온 값을 있는 그대로 사용하려고 해야지 추가적으로 변경해서 쓰려고하지 말라는 책의 조언에 따라.. 대대적인 메서드 수정에 나섭니다.

```java
private void helloMethod(int one, int two){
    int i = one;
    int j = two;
}
```



<br/>




## 주제2: Parameter의 타입을 결정하는 방법

계속해서 메서드의 파라미터를 변경하다보면, 그런 생각을 합니다. 그냥 데이터 객체(DTO, Model 등)를 하나 선언해서 보내는 게 나으려나..🤹 데이터 모델의 장점 중 하나가 확장성이기 때문에 메서드를 수정하지 않도고 필요한 데이터를 추가적으로 선언하면 언제든 쓸 수 있습니다. 하지만, 메서드의 파라미터에 불필요한 데이터까지 넘긴 건 아닌지 걱정이 됩니다..🚨 이것이 곧 성능 저하로 이어지지는 않을까..☠️하는 그런 문제들..

<br/>

### 파라미터 3개 이상부터는 데이터 객체 사용
코드 설계 관련해서 아래 2권의 책을 읽었습니다.
(두 권 모두 추천합니다🫠!)
* [읽기 좋은 코드가 좋은 코드다](https://product.kyobobook.co.kr/detail/S000001223831)
* [내 코드가 그렇게 이상한가요?](https://product.kyobobook.co.kr/detail/S000202521361)
두 권 중에 한 권에서 말했습니다. 파라미터 3개부터는 객체를 만들어 전달하라고.  

즉, 간단한 코드로 작성하자면 다음과 같습니다.

```java
private void helloMethod(String userName, String userPassword, String userNickname){
    String name = userName;
    String password = userPassword;
    String nickname = userNickname;
}

private void helloMethod(UserInfo user){
    String name = user.name;
    String password = user.password;
    String nickname = user.nickname;
}

class UserInfo{
    String name;
    String password;
    String nickname;
}
```

여기서 추가적으로 고민해볼 수 있는 문제는 
1. 데이터 객체의 필드 중 일부만 사용될 때에도 데이터 객체를 사용하는 것이 좋은지
2. 데이터 객체의 필드가 갖는 데이터의 크기가 클 경우에는 성능 저하의 문제가 생기지는 않는지에 대한 것입니다.

개인적으로 구글링하며 내린 결론은
1. 파라미터로 전달하는 데이터 객체는 필요한 데이터만 들어갈 수 있도록 역할 분리를 잘 해야한다.  
저는 데이터 객체를 크게 잡아서 여기저기서 많이 쓰이면 좋지 않을까 생각했습니다. 데이터 객체가 가지는 확장성을 최대한 활용한다는 생각에서요. 그러다보니 데이터 객체가 너무 거대해지면서 1번과 같은 고민이 시작되었습니다. 데이터베이스로 비유하자면, 조인하면 성능이 떨어질 수 있으니 난 테이블을 최대한 적게 만든다하면서 테이블의 역할에 비해 저장해야 할 컬럼이 너무 많게 된 상황인 것이죠.  
그래서 결론은 목적에 맞는 데이터만 저장하는 데이터 객체를 만들자 입니다.
2. 1번과 동일한 결론에 도달하게 되는데, 사용되지 않는 필드의 데이터가 너무 큰 값일 경우가 문제가 되는 것입니다. 만일 사용 목적에 맞는 데이터 객체를 만든다면 2번과 같은 문제도 해결할 수 있을 것입니다.



#
### 정리
1. 메서드의 파라미터를 변경해야할 경우,
* Overloading
* Default Parameter
* Add Parameter
2. 파라미터가 3개 이상일 경우,
* 데이터 객체 활용



#
### 📚참고 자료
[[Java]메서드 오버로딩말고 파라미터를 여러개 받아보자.](https://compogetters.tistory.com/137#google_vignette)  
[읽기 좋은 코드가 좋은 코드다](https://product.kyobobook.co.kr/detail/S000001223831)  
[내 코드가 그렇게 이상한가요?](https://product.kyobobook.co.kr/detail/S000202521361)
