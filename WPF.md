### `LayoutTransform` vs `RenderTransform`

| 항목 | `LayoutTransform` | `RenderTransform` |
| --- | --- | --- |
| 적용 시점 | **레이아웃 전**에 적용 | **레이아웃 후**에 적용 |
| 공간 차지 | 회전/크기 변경에 따라 **배치 크기도 달라짐** | **원래 배치 크기 그대로** |
| 성능 | 무겁고 느림 (전체 레이아웃 재계산) | 가벼움 |
| 용도 | UI 배치가 변경되는 경우 (예: 텍스트 회전) | 단순 시각 효과 (예: 애니메이션, 회전 등) |

```xml
<ScrollBar Orientation="Horizontal">
    <ScrollBar.LayoutTransform>
        <RotateTransform Angle="-90"/>
    </ScrollBar.LayoutTransform>
</ScrollBar>
```
스크롤바: `PART_Track`, `PART_Thumb` 등의 배치가 orientation에 따라 레이아웃 재계산 필요 → **`LayoutTransform`**
