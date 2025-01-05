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