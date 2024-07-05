# 17_Exception_예외입니다_전_특별하니까요
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2024-07-01
- 수정일: 2024-07-05

<br/>



#
### 주제를 선정한 이유
프로젝트가 1차 마무리를 향해 갑니다. 새로운 구현보다는 오류 잡이를 할 시간이라는 뜻입니다. 지난 번에는 Null이었다면 이번에는 Exception입니다. 이번 글은 오류를 나타내는 값을 Null로 처리하는 것이 좋은가, Exception을 던지는 게 좋은가에 대한 고민을 정리해보고자 정리하는 글 시즌2 입니다.



#
### Error VS Exception
Error
* 시스템의 비정상적인 상황에서 발생  
▶ 시스템 레벨에서 발생하기 때문에 개발자가 예측하고 처리할 수 없음

Exception
* 개발자가 구현한 로직에서 발생  
▶ 발생할 상황을 미리 예측하여 처리할 수 있음
  * Checked Exception
    * 컴파일 단계에서 예외를 확인하므로 반드시 예외를 처리해야 함
    * 예외 발생 시, Roll-back하지 않음
    * 예: IOException, SQLException 등
  * UnChecked Exception(Runtime Exception)
    * 실행단계에서 예외를 확인하므로 명시적인 처리를 강제하지 않음
    * 예외 발생 시, Roll-back 실행
    * 예: NullPointerException☠️, IllegalArgumentException☠️, IndexOutOfBoundException☠️



#
### 예외 처리 방법
코드에 최대한 오류가 발생하지 않게 작성한다 하더라도 예상치 못한 상황은 늘 발생합니다. 이런 상황에서 오류로 인해 프로그램이 비정상적으로 종료되지 않도록 하기 위해 예외를 처리해야 합니다.

이러한 예외 처리 방법 중 가장 대표적인 방법은 try-catch-final이 있습니다.
  * try: 예외가 발생할 여지가 있는 로직을 작성하는 부분
  * catch: 예외가 발생할 경우, 처리할 로직을 작성하는 부분
  * final: 예외 발생 유무와 상관없이 무조건 실행할 로직을 작성하는 부분
    * 주로, 커넥션 풀 종료, 임시 파일 삭제, 소켓 종료 등에 사용

```java
try{
  // 예외가 발생할 여지가 있는 로직
} catch(Exception ex) {
  // 예외 발생 시, 처리할 로직
} finally {
  // 예외와 관계없이 수행할 로직
}
```



#
### 예외 처리 전략
try 구문에서 예외가 발생했다면, 그 예외를 처리하는 방법도 여러가지가 있습니다.

1. 예외 복구  
: 예외가 발생하여도 애플리케이션은 정상적인 흐름으로 진행할 수 있도록 하는 방법
  * 예외를 잡아서 일정 시간이나 조건만큼 대기하고 재시도를 반복하고 최대 재시도 횟수를 넘어서면 예외 발생
  * 네트워크 환경이 좋지 않아 서버에 접속이 안되는 상황의 시스템에 적용하면 효율적

```java
final int MAX_RETRY = 100;
int maxRetry = MAX_RETRY;

while(maxRetry){
  try{
    // ...
  } catch(Exception e){
    // log 출력
    // 정해진 시간만큼 대기
  } finally {
    // 리소스 반납 및 정리 작업
  }

  --maxRetry;
}

// 최대 재시도 횟수 초과 시, 예외 발생
throw new RetryFailedException();
```

2. 예외처리 회피  
: 예외 발생 시, throws를 통해 호출한 메서드에 예외를 던짐
  * 호출한 쪽에서 다시 예외를 받아 처리하도록 하거나, 예외를 던지는 것이 최선일 때 사용하는 것이 좋음

```java
public void add() throws SQLException{
  try{
    // ...
  } catch(SQLException e) {
    // 로그 출력 후, throw
    throw e;
  }
}
```

3. 예외 전환  
: 예외 회피와 비슷하게 메서드 밖으로 예외를 위임하지만, 그냥 위임하지 않고 적절한 예외로 전환해서 넘기는 방법
  * 조금 더 명확한 의미로 전달되기 위해 적합한 의미를 가진 예외로 변경해서 throws
  * 예외 처리를 상위 클래스로 단순하게 퉁치기 위해 포장(wrap)

```java
private void add(User user) throws DuplicateUserIdException, SQLException{
  try{
    // ...
  } catch(SQLException se){
    if(se.getErrorCode() == MysqlErrorNumbers.ER_DUP_ENTRY){
      throw DuplicateUserIdException();
    } else {
      throw e;
    }
  }
}
```

```java
public void someMethod() throws EJBException{
  try{
    // ...
  } catch(NamingException | SQLException | RemoteException e){
    throw new EJBException(e);
  }
}
```



#
### Exception Handling 주의 사항
1. catch에 아무런 로직이 없는 경우
2. catch에 단순히 throw만 하는 경우
3. 로그를 출력하거나, 문제를 원상 복구 시키는 로직을 첨가하는 등 catch만 수행하지 않고 해당 예외에 대한 처리를 해주어야 함



#
### 좋은 예외 처리방법
1. null, -1, 빈 문자열 등 특수값을 예외로 사용하지 않기  
= 예외 상황은 예외 (Exception) 으로 처리하기
2. 추적 가능한 예외 만들기
  * 오류 메세지에 어떠한 값을 사용하다가 실패하였는지
  * 실패한 작업의 이름과 실패 유형

```java
// BAD
private double divideWrong(double a, double b){
  if(b == 0){
    return -1;
  }

  return a / b;
}

// GOOD
private double divideRight(double a, double b){
  if(b == 0){
    throw new Exception("Division by zero is not allowed");
  }

  return a / b;
}
```
3. 추적 가능한 예외 만들기
  * 어떠한 값을 사용하다가 실패하였는지
  * 실패한 작업의 이름과 실패 유형

```java
// BAD
throw new Exception("잘못된 입력입니다.");

// GOOD
throw new Exception("사용자: " + userId + "의 입력 " + inputValue + "가 잘못 되었습니다.");
```

4. 의미를 담고 있는 예외 만들기
  * 예외의 원인과 내용을 정확하게 반영

```java
// BAD
class CustomException extends Exception {}

private void connectToDatabase(){
  throw new CustomException("Connection failed because of invalid credentials.");
}

// GOOD
class InvalidCredentialsException extends Exception {}

private void connectToDatabase(){
  throw new CustomException("Connection failed because of invalid credentials.");
}
```

4. Layer에 맞는 예외
  * 각 계층에서 발생할 수 있는 오류의 성격은 다르기 때문에, 해당 계층에 맞는 예외를 던지는 것이 유용
    * Repository (혹은 DAO) 에서 HttpException을 던진다거나 Presentation (Controller) 에서 SQLException을 처리하는것은 Layer별 역할에 맞지 않음
  * 가능한 가장 늦은 위치에서 처리
  * 적절한 수준으로 추상화된 Exception을 정의하거나 IllegalArgumentException 같은 Java의 표준 Exception을 활용하는 것이 좋음

```java
// BAD
class DuplicatedException extends Exception {}
class UserAlreadyRegisteredException extends Exception {}

// GOOD
class ValidationException extends Exception {}
class DuplicatedException extends ValidationException {}
class UserAlreadyRegisteredException extends ValidationException {}
```

5. 외부 SDK, 외부 API를 통해 발생하는 예외들은 하나로 묶어서 처리
  * 외부 라이브러리에서 발생하는 문제와 우리가 관리하는 코드는 같은 방식으로 해결해서는 안됨

```java
private void billing(){
  try{
    pay.billing();
  } catch (Exception e) {
    if(e instanceof PayNetworkException){
      // ...
    } else if (e instanceof EmptyMoneyException){
      // ...
    } else if (e instanceof PayServerException){
      // ...
    }

    throw new BillingException(e);
  }
}

private void order(){
  Pay pay = new Pay();
  pay.billing();

  try{
    database.save(pay);
  } catch(Exception e){
    pay.cancel();
  }
}
```

6. Catch절에 예외 흐름에 적합한 코드 구현
  * 로깅 혹은 Layer에 적합한 Exception 변환 등  
  ▶ 로깅 혹은 Layer에 적합한 Exception 변환 등이 필요한 것이 아니라면 try catch로 다시 잡지 않는 것이 좋음

7. 정상적인 흐름에서 Catch 금지 (무분별한 Catch 금지)
  * 프로그램의 정상적인 흐름을 제어하기 위해 예외를 사용하지 않음  
  ▶ 예외는 오직 예외적인 경우에만 사용



#
### 📚참고 자료
[[Java] 예외처리(Exception Handling) 이해하기 -1 : try - catch / throws](https://adjh54.tistory.com/362#google_vignette)  
[Java 예외(Exception) 처리에 대한 작은 생각](https://www.nextree.co.kr/p3239/)  
[Exception (예외) 의 개념과 사용 이유](https://jminc00.tistory.com/14)  
[예외처리(exception handling)](https://catsbi.oopy.io/92cfa202-b357-4d47-8de2-b9b3968dfb2e)  
[좋은 예외(Exception) 처리](https://jojoldu.tistory.com/734)  
[[Java] Error와 Exception](https://choiblack.tistory.com/39)  
[Exception Handling - 자바 예외를 처리하는 3가지 기법](https://inpa.tistory.com/entry/JAVA-%E2%98%95-Exception-Handling-%EC%98%88%EC%99%B8%EB%A5%BC-%EC%B2%98%EB%A6%AC%ED%95%98%EB%8A%94-3%EA%B0%80%EC%A7%80-%EA%B8%B0%EB%B2%95)
