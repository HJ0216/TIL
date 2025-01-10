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


### Sorted Set Data Type
* ordered collection, Unique strings
  * leader board
  * rate limit

```bash
ZADD "game1:scores" 100 user1 200 user2 300 user3
# (integer) 3
ZADD "game1:scores" 50 user4 150 user5 250 user6
# (integer) 3
ZRANGE "game1:scores" 0 +inf BYSCORE LIMIT 0 10
# 1) "user4"
# 2) "user1"
# 3) "user5"
# 4) "user2"
# 5) "user6"
# 6) "user3"
ZRANGE "game1:scores" +inf 0 BYSCORE REV LIMIT 0 10
# 1) "user3"
# 2) "user6"
# 3) "user2"
# 4) "user5"
# 5) "user1"
# 6) "user4"
ZRANGE "game1:scores" +inf 0 BYSCORE REV LIMIT 0 3
# 1) "user3"
# 2) "user6"
# 3) "user2"

ZREM "game1:scores" user3
# (integer) 1
ZREM "game1:scores" user3
# (integer) 0

ZRANGE "game1:scores" +inf 0 BYSCORE REV LIMIT 0 3
# 1) "user6"
# 2) "user2"
# 3) "user5"

ZCARD "game1:scores"
# (integer) 5
ZCARD "Game1:scores"
# (integer) 0

ZINCRBY "game1:scores" 500 user4
# "550"
ZRANGE "game1:scores" +inf 0 BYSCORE REV LIMIT 0 3
# 1) "user4"
# 2) "user6"
# 3) "user2"
```

```java
HashMap<String, Double> scores = new HashMap<>();
scores.put("user1", 100.0);
scores.put("user2", 10.0);
scores.put("user3", 20.0);
scores.put("user4", 30.0);
scores.put("user5", 40.0);

jedis.zadd("game2:scores", scores);

List<String> zrange = jedis.zrange("game2:scores", 0, Long.MAX_VALUE);
zrange.forEach(System.out::println);
// scores의 value 기준으로 자동 오름차순 정렬

List<Tuple> tuples = jedis.zrangeWithScores("game2:scores", 0, Long.MAX_VALUE);
tuples.forEach(i -> System.out.println("%s %f".formatted(i.getElement(), i.getScore())));

System.out.println(jedis.zcard("game2:scores"));

jedis.zincrby("game2:scores", 50, "user2");

List<Tuple> tuples2 = jedis.zrangeWithScores("game2:scores", 0, Long.MAX_VALUE);
tuples2.forEach(i -> System.out.println("%s %f".formatted(i.getElement(), i.getScore())));
```


### Geospatial Data Type
* Coorinate(Latitude and Longitude)

```bash
GEOADD stores:geo 126.98102606983623 37.57940249726259 경회루
# (integer) 1
GEOADD stores:geo 126.96865587536988 37.570777342456765 경희궁
# (integer) 1
GEODIST stores:geo 경회루 경희궁
# "1452.4463"
GEODIST stores:geo 경회루 경희궁 km
# "1.4524"
GEOSEARCH stores:geo FROMLONLAT 126.974 37.574 BYRADIUS 500 m
# (empty array)
GEOSEARCH stores:geo FROMLONLAT 126.974 37.574 BYRADIUS 1 km
# 1) "\xea\xb2\xbd\xed\x9d\xac\xea\xb6\x81"
# 2) "\xea\xb2\xbd\xed\x9a\x8c\xeb\xa3\xa8"
```

```java
jedis.geoadd("stores2:geo", 126.98102606983623, 37.57940249726259, "Gyeonghoeru");
jedis.geoadd("stores2:geo", 126.96865587536988, 37.570777342456765, "Gyeonghuigung Palace");

Double geodist = jedis.geodist("stores2:geo", "Gyeonghoeru", "Gyeonghuigung Palace");
System.out.println("geodist = " + geodist);

//        List<GeoRadiusResponse> geoSearch = jedis.geosearch(
//            "stores2:geo",
//            new GeoCoordinate(126.974, 37.575),
//            1500,
//            GeoUnit.M);
//        geoSearch.forEach(r -> System.out.println("%s %f %f".formatted(r.getMemberByString(), r.getCoordinate().getLongitude(), r.getCoordinate().getLatitude())));
// GeoSearch는 기본적으로 멤버만 반환
// Jedis에서 WITHCOORD가 활성화되지 않았다면 getCoordinate()가 null을 반환
// Redis에서 명령어 확인 시, 해당 코드에서는 WITHCOORD 옵션이 빠져있음

List<GeoRadiusResponse> geoSearch = jedis.geosearch("stores2:geo",
    new GeoSearchParam()
        .fromLonLat(new GeoCoordinate(126.974, 37.575))
        .byRadius(1500, GeoUnit.M)
        .withCoord()
);

geoSearch.forEach(r ->
    System.out.println("%s %f %f".formatted(
        r.getMemberByString(),
        r.getCoordinate().getLongitude(),
        r.getCoordinate().getLatitude())
    )
);

jedis.unlink("stores2:geo");
```



### Bitmap Data Type
* 메모리를 적게 사용해 대량의 데이터를 저장할 때 유용

```bash
SETBIT request-somepage-20250106 100 1
# (integer) 0
SETBIT request-somepage-20250106 110 1
# (integer) 0
SETBIT request-somepage-20250106 120 1
# (integer) 0
SETBIT request-somepage-20250106 130 1
# (integer) 0
BITCOUNT SETBIT request-somepage-20250106
# (integer) 0
BITCOUNT request-somepage-20250106
# (integer) 4
GETBIT request-somepage-20250106 100
# (integer) 1
GETBIT request-somepage-20250106 101
# (integer) 0
```

```java
jedis.setbit("request-somepage-20250107", 100, true);
jedis.setbit("request-somepage-20250107", 110, true);
jedis.setbit("request-somepage-20250107", 120, true);

System.out.println(jedis.getbit("request-somepage-20250107", 100));
System.out.println(jedis.getbit("request-somepage-20250107", 50));

System.out.println(jedis.bitcount("request-somepage-20250107"));

// bitmap vs set
Pipeline pipelined = jedis.pipelined();
IntStream.rangeClosed(0, 100000).forEach(i -> {
  pipelined.sadd("request-somepage-set-20250106", String.valueOf(i), "1");
  pipelined.setbit("request-somepage-bit-20250106", i, true);

  if(i == 1000){
    pipelined.sync();
  }

  pipelined.sync();
});
```



## Transaction
* MULTI - EXEC / DISCARD
* Isolation
* WATCH with MULTI

```bash
MULTI
# OK
(TX)> SET key 100
# QUEUED
(TX)> SET key2 200
# QUEUED

# EXEC 전 key, key2 조회 X

(TX)> EXEC
# 1) OK
# 2) OK

MULTI
# OK
(TX)> set key 100
# QUEUED
(TX)> sett key2 200
# (error) ERR unknown command `sett`, with args beginning with: `key2`, `200`,
(TX)> EXEC
# (error) EXECABORT Transaction discarded because of previous errors.
# 트랜잭션 준비 단계(MULTI)에서 Redis는 큐에 명령어를 저장하기 전에 명령어의 존재 여부를 확인
# SETT는 Redis에 등록되지 않은 명령어이므로, 즉시 오류를 발생시키며 트랜잭션 전체를 무효화(EXECABORT)

MULTI
# OK
(TX)> set key 100
# QUEUED
(TX)> set key 100 200
# QUEUED
(TX)> set key2 200
# QUEUED
(TX)> set key2 200 300
# QUEUED
(TX)> EXEC
# 1) OK
# 2) (error) ERR syntax error
# 3) OK
# 4) (error) ERR syntax error
# Redis는 트랜잭션 준비 단계에서는 명령어의 구문 유효성까지 검증하지 않음
# 트랜잭션 실행 단계(EXEC)에서 실제로 명령어를 실행하려고 할 때, 구문이 잘못된 것을 확인하고 해당 명령어만 실패
# Redis는 이런 경우 부분 성공을 허용

WATCH key
# OK
MULTI
# OK
(TX)> SET key 500
# QUEUED
(TX)> EXEC
# (nil)
GET key
# "300"

MULTI
# OK
(TX)> SET key 500
# QUEUED
(TX)> SET key2 400
# QUEUED
(TX)> SET key3 300
# QUEUED
(TX)> EXEC
# (nil)
GET key2
# "200"
```