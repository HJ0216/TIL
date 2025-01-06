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


### Set Data Type
* Unordered collection, Unique strings

```bash
SADD users:100:follow 150 130 120
# (integer) 3
SCARD users:100:follow
# (integer) 3
SADD users:100:follow 150 130 120
# (integer) 0

# Set은 입력 순서대로 데이터가 저장되지 않는 특징에 유의
SMEMBERS users:100:follow
# 1) "120"
# 2) "130"
# 3) "150"
SISMEMBER users:100:follow 100
# (integer) 0
SISMEMBER users:100:follow 120
# (integer) 1

SADD users:200:follow 150 30 20
# (integer) 3
SINTER users:100:follow users:200:follow
# 1) "150"

SREM users:200:follow 30
# (integer) 1
SREM users:200:follow 30
# (integer) 0
SMEMBERS users:200:follow
# 1) "20"
# 2) "150"
```

```java
jedis.sadd("users:300:follow", "100", "200", "300");
jedis.srem("users:300:follow", "100");

Set<String> smembers = jedis.smembers("users:300:follow");
smembers.forEach(System.out::println);

System.out.println(jedis.sismember("users:300:follow", "200"));
System.out.println(jedis.sismember("users:300:follow", "250"));

Set<String> sinter = jedis.sinter("users:200:follow", "users:300:follow");
sinter.forEach(System.out::println);
```


### Hashes Data Type
* field-value pair collection

```bash
HSET users:1:info name grep email grep@email.com phone 010-1234-1234
# (integer) 3
HGET users:1:info name
# "grep"
HGET users:1:info email
# "grep@email.com"
HGETALL users:1:info
# 1) "name"
# 2) "grep"
# 3) "email"
# 4) "grep@email.com"
# 5) "phone"
# 6) "010-1234-1234"

HDEL users:1:info phone
# (integer) 1
HGETALL users:1:info
# 1) "name"
# 2) "grep"
# 3) "email"
# 4) "grep@email.com"

HSET users:1:info visits 0
# (integer) 1
HGET users:1:info visits
# "0"
HINCRBY users:1:info visits 1
# (integer) 1
HINCRBY users:1:info visits 10
# (integer) 11
```

```java
// Hash Set
jedis.hset("users:2:info", "name", "grep2");

HashMap<String, String> userInfo = new HashMap<>();
userInfo.put("email", "grep2@email.com");
userInfo.put("phone", "010-5678-5678");

jedis.hset("users:2:info", userInfo);

// Delete
jedis.hdel("users:2:info", "phone");

// Get
System.out.println(jedis.hget("users:2:info", "email"));

Map<String, String> user2Info = jedis.hgetAll("users:2:info");
user2Info.forEach((k,v) -> System.out.printf("%s %s%n", k, v));

// Increment
jedis.hincrBy("users:2:info", "visits", 10);
```