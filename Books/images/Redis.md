# Redis

## Value의 데이터 구조(타입)
### String Data Type
* 가장 기본적인 타입
* text, byte 저장
* 증가/감소에 대한 원자적 연산 지원

```bash
set users:100:name grep
# OK
set users:100:email grep@email.com
# OK

get users:100:name
# grep
mget users:100:name users:100:email
# grep@email.com

setnx users:100:name grep2
# (integer) 0
setnx users:101:name grep2
# (integer) 1
# setnx: 해당하는 key값이 없을 경우에 값 입력
# set users:101:name grep2 nx 명령어와 동일

incr counter1
# (integer) 1
incr counter1
# (integer) 2
decr counter1
# (integer) 1
incrby counter1 10
# (integer) 11
```

* Redis pipelining
  * 여러 명령을 한 번에 서버에 보내서 처리하고 결과를 받는 방식
  * 네트워크 왕복(Round Trip) 시간을 줄여 성능을 향상시킬 수 있음

```java
jedis.set("users:300:name", "imjedis");
jedis.set("users:300:email", "imjedis@email.com");
jedis.set("users:300:age", "30");

Pipeline pipelined = jedis.pipelined();
pipelined.set("users:400:name", "jedisPipe");
pipelined.set("users:400:email", "jedisPipe@email.com");
pipelined.set("users:400:age", "25");
```


### List Data Type
* Linked List Type
  * ArrayList(Java)

```bash
RPUSH stack1 100
# (integer) 1
RPUSH stack1 100
# (integer) 2
RPUSH stack1 200
# (integer) 3
RPOP stack1
# "200"
RPOP stack1
# "100"
RPOP stack1
# "100"
RPOP stack1
# (nil)

RPUSH queue1 100
# (integer) 1
RPUSH queue1 200
# (integer) 2
RPUSH queue1 300
# (integer) 3
LRANGE queue1 0 -1
# 1) "100"
# 2) "200"
# 3) "300"
LPOP queue1
# "100"
LPOP queue1
# "200"
LPOP queue1
# "300"
LPOP queue1
# (nil)

# LTRIM을 활용한 최신값만 남기기
LPUSH queue1 10
LPUSH queue1 20
LPUSH queue1 30
LPUSH queue1 40
LTRIM queue1 0 1 # 40, 30
LPUSH queue1 1
LPUSH queue1 2
LPUSH queue1 3
LTRIM queue1 0 1 # 3, 2
LTRIM queue1 0 1 # 3, 2

# 값이 채워질 때까지 일정 시간 응답하는 기능
BRPOP queue1 5
# 1) "queue1"
# 1) "2"
BRPOP queue1 5
# (nil)
```

```java
// 1. stack
jedis.rpush("stack2", "aaa");
jedis.rpush("stack2", "bbb");
jedis.rpush("stack2", "ccc");

List<String> stack2 = jedis.lrange("stack2", 0, -1);
stack2.forEach(System.out::println);

jedis.rpop("stack2");

// 2. queue
jedis.rpush("queue2", "111");
jedis.rpush("queue2", "222");
jedis.rpush("queue2", "333");

System.out.println(jedis.lpop("queue2"));
System.out.println(jedis.lpop("queue2"));
System.out.println(jedis.lpop("queue2"));

// 3. block brpop, blpop
List<String> blpop = jedis.blpop(10, "queue:blocking");
if (blpop != null) {
  blpop.forEach(System.out::println);
}
```
