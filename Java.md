### InvalidDefinitionException
```bash
com.fasterxml.jackson.databind.exc.InvalidDefinitionException: 
No serializer found for class com.mini_prioject.display_board.entity.dto.ImageResponse and no properties discovered to create BeanSerializer (to avoid exception, disable SerializationFeature.FAIL_ON_EMPTY_BEANS)
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
직렬화(Serialization): 객체를 JSON 형식으로 변환  
Jackson은 Java 객체를 JSON으로 변환할 때 해당 객체의 필드를 기반으로 직렬화를 처리  
Jackson은 기본적으로 getter 메서드나 public 필드에 접근하여 값을 읽음
* JSON 데이터가 Java 객체의 필드에 값으로 매핑될 때, Jackson은 setter 메서드를 사용하여 값을 설정  
  객체가 읽기 전용인 경우를 제외하고 Setter도 추가 설정 필요