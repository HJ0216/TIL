### InvalidDefinitionException

```bash
com.fasterxml.jackson.databind.exc.InvalidDefinitionException:
No serializer found for class com.mini_project.display_board.entity.dto.ImageResponse and no properties discovered to create BeanSerializer (to avoid exception, disable SerializationFeature.FAIL_ON_EMPTY_BEANS)
```

ImageResponse 클래스가 직렬화할 수 있는 속성이 없거나, Jackson이 ImageResponse 객체를 직렬화할 방법을 찾을 수 없다는 것을 의미  
→ ImageResponse 클래스에 직렬화 가능한 속성을 정의해야 하며, 필요한 경우 Jackson 직렬화/역직렬화에 관련된 어노테이션을 추가

```java
public class ImageService {
  public List<ImageResponse> getAllImages() {
    return imageRepository.findAll().stream()
                          .map(Image::toResponse)
                          .collect(Collectors.toList());
  }
}
```

- 직렬화(Serialization)
  - Jackson은 Java 객체를 JSON으로 변환할 때 해당 객체의 필드를 기반으로 직렬화를 처리
  - Jackson은 기본적으로 getter 메서드나 public 필드에 접근하여 값을 읽음

- 역직렬화(Deserialization)
  - JSON 데이터가 Java 객체의 필드에 값으로 매핑될 때, Jackson은 setter 메서드를 사용하여 값을 설정
  - 객체가 읽기 전용인 경우를 제외하고 Setter도 추가 설정 필요

### ArrayDeque vs ArrayList

- ArrayDeque를 사용해야 하는 경우 ✅
  - Queue/Stack 용도: FIFO/LIFO 방식으로 데이터 처리
  - 양쪽 끝 조작이 빈번: 앞/뒤에서 추가/제거가 많은 경우
  - 순서대로 처리해야 하는 대기열, 작업 큐, 이벤트 큐 등의 경우

- ArrayList를 사용해야 하는 경우 ✅
  - 인덱스 접근: list.get(5) 같은 임의 위치 접근이 필요
  - 끝에 추가/삭제가 많을 때
  - 정렬/검색: Collections.sort(), indexOf() 등 사용

- LinkedList를 사용해야 하는 경우 ✅
  - 중간 삽입/삭제가 잦을 때

### equals(), hashCode()

- "값이 같으면 같은 객체"로 취급해야 하는 경우 → 오버라이드 필수
- HashMap, HashSet 에 key나 element로 쓸 때 → 오버라이드 필수
- 그렇지 않으면 → 기본 Object.equals()/hashCode()(참조 동등성)만 써도 됨
