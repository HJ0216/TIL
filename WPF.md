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


### `<Style.Triggers>` vs `<ControlTemplate.Triggers>`
* “컨트롤 자체 속성 바꾸고 싶다” → Style.Triggers
* “템플릿 안의 요소를 바꾸고 싶다” → ControlTemplate.Triggers


### `Style 내부 Setter` vs `Inline Property`
1. Style 내부 `Setter`: **공통 스타일을 적용**하고 싶을 때
```xml
<Style TargetType="Button">
    <Setter Property="Background" Value="SkyBlue"/>
    <Setter Property="Foreground" Value="White"/>
</Style>
```

\+ `TemplateBinding`과 Style 내부 Setter 
* Style의 TargetType에 정의된 속성
    * **Style의 Setter로 기본값을 설정**하는 것이 좋음
    * ControlTemplate 내부: `TemplateBinding`을 사용하여 Setter로 설정된 값을 바인딩
*. Style의 TargetType에 없는 속성 
    * 예: ToggleButton 스타일 내 Border의 CornerRadius 등
    * Target Type 자체의 속성이 아닌, 템플릿 **내부 요소**의 속성이 항상 동일한 고정 값을 갖으면 ControlTemplate 내부의 해당 요소 태그에 값을 직접 입력
```xml
<Style TargetType="ToggleButton">
    <Setter Property="Background" Value="Black"/>
    <Setter Property="Foreground" Value="White"/>
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="ToggleButton">
                <Border CornerRadius="5"
                        BorderBrush="{TemplateBinding Foreground}"
                        Background="{TemplateBinding Background}"/>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

2. 태그에 직접 쓰는 경우: **한두 개의 컨트롤만 다른 스타일**을 원할 때
```xml
<Button Background="Red" Foreground="Black" Content="긴급 버튼"/>
```


### `Trigger` vs `DataTrigger` 핵심 차이
Trigger
* 컨트롤의 Dependency Property
* 속성 자체의 값 변화를 감지
* Value 속성에는 Binding을 직접 사용할 수 없음(정적인 값만 사용 가능)
```xml
<Trigger Property="IsMouseOver" Value="True">
    <Setter Property="Background" Value="LightBlue"/>
</Trigger>
```
DataTrigger
* Binding으로 연결된 값
* 바인딩된 데이터의 값 변화를 감지
* Value 속성에는 Binding을 직접 사용할 수 없음(정적인 값만 사용 가능)
```xml
<DataTrigger Binding="{Binding IsHighlighted}" Value="True">
    <Setter Property="Background" Value="LightBlue"/>
</DataTrigger>
```



### 속성 값의 우선순위(Priority)
1. Local Value(Inline)
2. Style Triggers
3. Style Setters
4. Default value

* Trigger가 동작하지 않음
```xml
<Button Margin="0">
    <Button.Style>
        <Style TargetType="Button">
            <Style.Triggers>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter Property="Margin" Value="1"/>
                </Trigger>
            </Style.Triggers>
        </Style>
    </Button.Style>
</Button>
```

* Trigger가 동작함
```xml
<Button>
    <Button.Style>
        <Style TargetType="Button">
            <Setter Property="Margin" Value="0"/>
            <Style.Triggers>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter Property="Margin" Value="1"/>
                </Trigger>
            </Style.Triggers>
        </Style>
    </Button.Style>
</Button>
```



### `Binding` vs `TemplateBinding`
* Binding
  * 무거운 바인딩 객체 생성를 생성하여 상대적으로 느림(PropertyChanged 이벤트를 계속 감시)
  * 아무곳에서나 사용 가능
  * 트리거/스타일 적용 등 유연성 필요할 때 사용

```xml
<Style TargetType="Button">
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="Button">
                <Border x:Name="border" Background="{Binding Background, RelativeSource={RelativeSource TemplatedParent}}">
                    <ContentPresenter Content="{TemplateBinding Content}" />
                </Border>

                <ControlTemplate.Triggers>
                    <Trigger Property="IsMouseOver" Value="True">
                        <Setter Property="Background" Value="LightBlue" />
                    </Trigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

* TemplateBinding
  * 컴파일 타임에 최적화되어 빠름
  * ControlTemplate 내부에서만 사용
  * 값을 단순히 전달하기 위해 사용(단방향 연결로, 한 번 연결되면 그 값만 고정적으로 받아오고 Trigger에 의해 바뀌는 값은 무시됨)
  * Trigger, DataTrigger, Converter 등 사용 불가
  * 단, `ElementName`으로 명시적으로 지정해서 사용할 경우, Trigger 사용 가능

```xml
<Style TargetType="Button">
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="Button">
                <Border x:Name="border" Background="{TemplateBinding Background}">
                    <ContentPresenter Content="{TemplateBinding Content}" />
                </Border>

                <ControlTemplate.Triggers>
                    <Trigger Property="IsMouseOver" Value="True">
                        <!-- 사용 불가 -->
                        <Setter Property="Background" Value="LightBlue" />
                        <!-- 사용 가능 -->
                        <Setter TargetName="border" Property="Background" Value="LightBlue" />
                    </Trigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```



### `RelativeSource`
현재 바인딩 위치 기준으로 다른 요소나 속성을 참조할 때 사용
* Self
```xml
<TextBlock Text="{Binding Width, RelativeSource={RelativeSource Self}}" />
```

* FindAncestor
  * 상위 요소를 타입 기준으로 찾을 때 사용
```xml
<TextBlock Text="{Binding DataContext.Title, RelativeSource={RelativeSource AncestorType=Window}}" />
```

* RelativeSource TemplatedParent
  * ControlTemplate 또는 DataTemplate 내부에서 템플릿을 사용하는 컨트롤(Button 등) 을 참조할 때 사용
```xml
<Border Background="{Binding Background, RelativeSource={RelativeSource TemplatedParent}}" />
```


### `TargetName` vs `ElementName`
* TargetName
  * ControlTemplate이나 Trigger 내에서 템플릿 내 특정 요소를 참조하고자 할 때 사용
  * 템플릿 바깥(Style)에서 해당 컨트롤에 직접 적용할 경우, TargetName 필요 X
```xml
<Style TargetType="Button">
    <Setter Property="Template">
        <Setter.Value>
            <ControlTemplate TargetType="Button">
                <Border x:Name="border" Background="LightGray">
                    <ContentPresenter Content="{TemplateBinding Content}" />
                </Border>

                <ControlTemplate.Triggers>
                    <Trigger Property="IsMouseOver" Value="True">
                        <Setter TargetName="border" Property="Background" Value="LightBlue" />
                    </Trigger>
                </ControlTemplate.Triggers>
            </ControlTemplate>
        </Setter.Value>
    </Setter>
</Style>
```

* ElementName
  * 현재 XAML 내 다른 요소를 참조하고자 할 때 사용
```xml
<StackPanel>
    <Button Name="myButton" Content="Click Me!" />
    <TextBlock Name="myText" Text="Hello, WPF!" Width="200" Height="50">
        <TextBlock.Style>
            <Style TargetType="TextBlock">
                <Style.Triggers>
                    <DataTrigger Binding="{Binding IsPressed, ElementName=myButton}" Value="True">
                        <Setter Property="Foreground" Value="Red" />
                    </DataTrigger>
                </Style.Triggers>
            </Style>
        </TextBlock.Style>
    </TextBlock>
</StackPanel>
```


### `Template` vs `ItemContainerStyle` vs `ItemTemplate`
* Template
  * ListBox 전체의 구조(스크롤뷰, 아이템 배치 등)를 정의
* ItemContainerStyle
  * ListBoxItem 자체의 스타일 → ControlTemplate
* ItemTemplate
  *  각 아이템의 콘텐츠 모양을 정의 → DataTemplate

```xml
<Window>
    <Grid>
        <ListBox Name="myListBox" Height="200" Width="300" Margin="10">
            <ListBox.Template>
                <ControlTemplate TargetType="ListBox">
                    <Border x:Name="border" CornerRadius="5">
                        <ScrollViewer>
                            <ItemsPresenter />
                        </ScrollViewer>
                    </Border>

                    <ControlTemplate.Triggers>
                        <Trigger Property="IsKeyboardFocusWithin" Value="True">
                            <Setter TargetName="border" Property="BorderBrush" Value="DodgerBlue" />
                        </Trigger>

                        <Trigger Property="HasItems" Value="False">
                            <Setter TargetName="border" Property="Background" Value="LightGray" />
                        </Trigger>
                    </ControlTemplate.Triggers>
                </ControlTemplate>
            </ListBox.Template>

            <ListBox.ItemTemplate>
                <DataTemplate>
                    <StackPanel>
                        <TextBlock x:Name="nameText" Text="{Binding Name}" FontWeight="Bold" />
                        <TextBlock Text="{Binding Age}" />
                    </StackPanel>

                    <DataTemplate.Triggers>
                        <DataTrigger Binding="{Binding Age}" Value="30">
                            <Setter TargetName="nameText" Property="Foreground" Value="Red"/>
                        </DataTrigger>
                    </DataTemplate.Triggers>
                </DataTemplate>
            </ListBox.ItemTemplate>
            
            <ListBox.ItemContainerStyle>
                <Style TargetType="ListBoxItem">
                    <Setter Property="Margin" Value="5" />
                    <Setter Property="BorderBrush" Value="DarkGray" />
                    <Setter Property="BorderThickness" Value="1" />
                    
                    <Style.Triggers>
                        <Trigger Property="IsMouseOver" Value="True">
                            <Setter Property="Background" Value="LightBlue" />
                        </Trigger>
                    </Style.Triggers>
                </Style>
            </ListBox.ItemContainerStyle>

            <ListBox.Style>
                <Style TargetType="ListBox">
                    <Setter Property="Background" Value="White" />
                    <Style.Triggers>
                        <Trigger Property="IsFocused" Value="True">
                            <Setter Property="Background" Value="LightYellow" />
                        </Trigger>
                    </Style.Triggers>
                </Style>
            </ListBox.Style>
        </ListBox>
    </Grid>
</Window>

```


### 태그 내 Property 나열 순서
1. 식별 관련  
  x:Name, Uid 등
2. 레이아웃 및 위치 관련  
  Grid.Row, Width, Margin 등
3. 데이터 및 중요 기능 관련  
  Content, Binding, Visibility 등
4. 기타
5. 스타일 및 템플릿 관련  
  Style 등
6. 이벤트 핸들러 관련  
  Click, SelectionChanged 등
