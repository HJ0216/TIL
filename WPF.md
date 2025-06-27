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
  * `ControlTemplate`에서 주로 사용
  * DataTemplate은 템플릿의 대상이 데이터 객체이기 때문에 TemplatedParent는 null이 됨
  * TemplatedParent를 찾기 위해서는 `FindAncestor`를 사용
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
  * 각 아이템의 콘텐츠 모양을 정의 → DataTemplate

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



### `OverridesDefaultStyle="True"` 최소화
* WPF가 내부적으로 기본 스타일을 다 무시하고 전부 재정의해야 하기 때문에, 비용이 큼
* 스타일 오버라이딩으로 해결해보도록 노력하고, OverridesDefaultStyle는 꼭 필요한 경우만 사용



### ScrollViewer
ListBox나 ListView 같은 ItemsControl은 자체적으로 ScrollViewer를 내장
```xml
<ListBox>
    <ListBox.ItemsPanel>
        <ItemsPanelTemplate>
            <VirtualizingStackPanel/> 
        </ItemsPanelTemplate>
    </ListBox.ItemsPanel>
    <ListBox.ItemTemplate>
        
    </ListBox.ItemTemplate>
</ListBox>
```
ItemsPanelTemplate에서 설정한 VirtualizingStackPanel은 ScrollViewer의 Content로 사용


### ScrollBar
```xml
<ScrollBar x:Name="PART_VerticalScrollBar" Grid.Column="1"
           Orientation="Vertical" Visibility="Hidden"
           Value="{Binding VerticalOffset, Mode=OneWay, RelativeSource={RelativeSource TemplatedParent}}"
           Maximum="{Binding ScrollableHeight, RelativeSource={RelativeSource TemplatedParent}}"
           Style="{StaticResource ScrollBarStyle}"/>
```
ScrollBar 구현 시, Value와 Maximum을 바인딩하여야 스크롤바가 실제 콘텐츠의 스크롤 위치와 동기화되어 움직임
* Value: VerticalOffset(ScrollViewer의 현재 세로 스크롤 위치)
* Maximum: ScrollableHeight(콘텐츠의 총 스크롤 가능한 높이)
* 마우스 휠로 수평 스크롤을 하려면 PreviewMouseWheel 이벤트를 수신하여 수동으로 수평 스크롤 이벤트로 변환해줘야 함
```cs
private void lb_GeneratedImages_PreviewMouseWheel(object sender, MouseWheelEventArgs e)
{
    // Shift와 마우스 휠로 수평 컨트롤을 하고자 하는 경우
    if (Keyboard.Modifiers == ModifierKeys.Shift)
    {
        var scrollViewer = FindVisualChild<ScrollViewer>(lb_GeneratedImages);
        if (scrollViewer != null)
        {
            scrollViewer.ScrollToHorizontalOffset(scrollViewer.HorizontalOffset - e.Delta);
            // scrollViewer.HorizontalOffset: 현재 스크롤의 가로 위치
            // e.Delta: 마우스 휠을 한 번 움직일 때 생기는 값
            // scrollViewer.ScrollToHorizontalOffset(...): 스크롤 뷰어의 가로 위치를 이동
            e.Handled = true;
            // 부모 컨트롤이나 시스템에서 중복 처리 방지
        }
    }
}
private static T FindVisualChild<T>(DependencyObject parent) where T : DependencyObject
{
    for (int i = 0; i < VisualTreeHelper.GetChildrenCount(parent); i++)
    {
        var child = VisualTreeHelper.GetChild(parent, i);
        if (child is T typedChild)
            return typedChild;

        var result = FindVisualChild<T>(child);
        if (result != null)
            return result;
    }
    return null;
}
```



### 기타
* ControlTemplate 내부의 태그는 x:Name을 통해 코드 비하인드에서 접근이 불가능 → 이벤트의 매개변수인 sender를 통해 접근
```cs
public void button_Click(object sender, EventArgs e)
{
    Button button = (Button)sender;
}
```
* 코드 비하인드에서 ControlTemplate안의 다른 요소에 접근하고자 하는 경우,
  1. VisualTreeHelper 사용
```cs
private void textBlock_MouseDown(object sender, MouseButtonEventArgs e)
{
    if (sender is TextBlock textBlock)
    {
        var parent = VisualTreeHelper.GetParent(textBlock);
        while (parent != null && !(parent is ListBoxItem))
        {
            parent = VisualTreeHelper.GetParent(parent);
        }

        if (parent != null)
        {
            // ListBoxItem 내부에서 TextBox 찾기
            var textBox = FindVisualChild<TextBox>((DependencyObject)parent);
            if (textBox != null)
            {
                textBlock.Visibility = Visibility.Collapsed;
                textBox.Visibility = Visibility.Visible;
            }
        }
    }
}

// VisualTreeHelper를 사용한 하위 요소 탐색 도우미 메서드
private static T FindVisualChild<T>(DependencyObject parent) where T : DependencyObject
{
    int childCount = VisualTreeHelper.GetChildrenCount(parent);
    for (int i = 0; i < childCount; i++)
    {
        var child = VisualTreeHelper.GetChild(parent, i);
        if (child is T tChild)
            return tChild;

        var result = FindVisualChild<T>(child);
        if (result != null)
            return result;
    }
    return null;
}
```
  2. Tag 또는 Uid 활용하기
```xml
<Grid>
    <TextBlock x:Name="textBlock"
               Tag="{Binding RelativeSource={RelativeSource AncestorType=Grid}, Path=Children[1]}"
               MouseDown="txtBlock_Title_MouseDown"/>
    
    <TextBox x:Name="textBox"/>
</Grid>

<Grid>
    <TextBlock x:Name="textBlock"
               Tag="{Binding ElementName=textBox}"
               MouseDown="txtBlock_Title_MouseDown"/>
    
    <TextBox x:Name="textBox"/>
</Grid>
```
```cs
private void textBlock_MouseDown(object sender, MouseButtonEventArgs e)
{
    if (e.ClickCount == 2 && sender is TextBlock tb && tb.Tag is TextBox editBox)
    {
        tb.Visibility = Visibility.Collapsed;
        editBox.Visibility = Visibility.Visible;
    }
}
```


### Grid
* Column이나 Row의 Visibility를 auto 대신 style과 Height를 이용하여 컨트롤할 수 있음
```xml
<Grid>
    <Grid.RowDefinitions>        
        <RowDefinition Height="auto"/>
        <RowDefinition>
            <RowDefinition.Style>
                <Style TargetType="RowDefinition">
                    <Setter Property="Height" Value="1*"/>
                    <Style.Triggers>
                        <DataTrigger Binding="{Binding IsChecked, ElementName=toggle}" Value="false">
                            <Setter Property="Height" Value="0"/>
                        </DataTrigger>
                    </Style.Triggers>
                </Style>
            </RowDefinition.Style>
        </RowDefinition>
    </Grid.RowDefinitions>
<Grid>
```



### DependencyProperty
```cs
public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    // 1. 의존 속성 등록
    public static readonly DependencyProperty MyCustomPropertyProperty =
        DependencyProperty.Register(
            "MyCustomProperty",
            typeof(string),
            typeof(MainWindow),
            new PropertyMetadata(string.Empty));
        // "MyCustomProperty": 속성 이름(실제 사용할 CLR 속성과 동일)
        // typeof(string): 이 속성이 다룰 값의 타입
        // typeof(MainWindow): 이 속성을 정의하고 사용할 클래스
        // new PropertyMetadata(...): 기본값을 설정(여기서는 빈 문자열(string.Empty)이 기본값)
        // + 필요하면 속성 변경 시 실행할 콜백 함수도 지정할 수 있음

    // 2. CLR Wrapper
    public string MyCustomProperty
    {
        get { return (string)GetValue(MyCustomPropertyProperty); }
        set { SetValue(MyCustomPropertyProperty, value); }
    }
}
```
```xml
<local:MainWindow
    x:Class="WpfApp1.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:local="clr-namespace:WpfApp1"
    MyCustomProperty="Hello Custom Property">
</local:MainWindow>
<!--MyCustomProperty="Hello Custom Property": 내부에서는 SetValue(...)가 자동으로 호출-->
```



### Background 기본값
* Panel(Grid, StackPanel 등): Transparent
* Control (ListBox, TextBox, Button 등): 흰색
* 기타(Border, Popup, Window 등): Transparent



### DispatcherPriority.Input
```cs
private void tBlock_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
{
    // 중략 ...
    editArea.Visibility = Visibility.Visible;
    editTextBox.Focus();
}
```
🚨 문제: editTextBox에 Focus가 가지 않음  
💡 원인: editTextBox가 아직 Loaded된 상태가 아님
✅ 해결: 비동기적으로 포커스 호출을 큐에 넣어, UI 업데이트 이후에 포커스가 가도록 수정

```cs
private void tBlock_PreviewMouseLeftButtonDown(object sender, MouseButtonEventArgs e)
{
    // 중략 ...
    editArea.Visibility = Visibility.Visible;
    editTextBox.Dispatcher.BeginInvoke(new Action(() =>
    {
        editTextBox.Focus();
    }), System.Windows.Threading.DispatcherPriority.Input);
}
```
* Dispatcher
  * WPF의 스레드 간 작업 조정기, UI 요소를 만든 스레드에서 실행되도록 작업을 예약할 수 있게 해줌
  * editTextBox.Dispatcher: 텍스트박스를 만든 UI 스레드에 접근할 수 있는 Dispatcher
* Dispatcher.BeginInvoke
  * 지정한 작업(예: Focus)을 UI 스레드에 **비동기적**으로 요청
* new Action(() => { editTextBox.Focus(); })
  * 익명 메서드
* DispatcherPriority.Input
  * 요청된 작업의 우선 순위
  * 키보드/마우스 입력보다 조금 높은 우선 순위
  * Render, Loaded, Layout 같은 UI 갱신이 끝난 후, 가장 빠른 사용자 입력 레벨에서 실행



### textBox_PreviewKeyDown / button_Click
* textBox_PreviewKeyDown
  * 사용자가 Enter/Esc 누를 때 즉시 실행
  * LostFocus가 발생하지 않았으므로 업데이트된 데이터로 바인딩 X
* button_Click
  * 버튼을 누르면 TextBox는 포커스를 잃음
  * LostFocus → 바인딩이 자동 반영됨(= DataContext값이 변경된 값으로 들어가 있음)



### ListBox
* 주어진 범위 내에서 ListBoxItem을 꽉차게 만들고 싶을 경우, HorizontalAlignment/VerticalAlignment를 Stretch로 설정해야 함
* ComputedVerticalScrollBarVisibility
  * ListBox의 속성이 아니라 ListBox 안에 있는 ScrollViewer의 속성
  * 직접 바인딩하는 방식이 아닌 ScrollViewer로 바인딩을 해야함
    * 🚨 ComputedVerticalScrollBarVisibility는 UI가 완전히 로드되고 레이아웃 측정이 완료된 후에야 올바른 값을 갖게 됨  
    → Window나 ListBox가 처음 뜰 때는 아직 ScrollViewer가 스크롤 가능 여부를 판단할 만큼 내용이 완전히 렌더링되지 않은 상태일 수 있어 DataTrigger가 올바르게 동작하지 않을 수 있음
    * 🚨 이후 레이아웃이 변경되면서 `ComputedVerticalScrollBarVisibility`가 `"Collapsed"`로 바뀌어도 **Trigger는 다시 평가되지 않음
    → ComputedVerticalScrollBarVisibility는 ScrollViewer의 DependencyProperty지만, INotifyPropertyChanged를 따르지 않기 때문에 Binding 변화에 따른 트리거 재평가가 즉시 일어나지 않음  
    → ScrollViewer.ComputedVerticalScrollBarVisibility는 ScrollViewer 내 레이아웃이 완전히 갱신되거나 스크롤 컨텐츠 크기 변화가 일어나야 값이 바뀌어서 갱신 타이밍이 다를 수 있음


```xml
<DataTrigger Binding="{Binding ComputedVerticalScrollBarVisibility, ElementName=ListBox_Sample}">

<ListBox x:Name="ListBox_Sample">
  <ListBox.Template>
    <ControlTemplate TargetType="ListBox">
      <ScrollViewer x:Name="ScrollViewer_Sample">
        <ScrollViewer.Style>
            <Style TargetType="ScrollViewer">
                <Setter Property="Width" Value="100"/>
                <Style.Triggers>
                    <DataTrigger Binding="{Binding ComputedVerticalScrollBarVisibility, ElementName=ScrollViewer_Sample}" Value="Collapsed">
                        <Setter Property="Width" Value="200"/>
                    </DataTrigger>
                </Style.Triggers>
            </Style>
        </ScrollViewer.Style>
      </ScrollViewer>
    </ControlTemplate>
  </ListBox.Template>
</ListBox>
```



### Button
* Button에서 클릭이나 Hover 영역이 이미지나 Text에 한정될 때, ControlTemplate 안에 있는 ContentPresenter를 Border 같은 걸로 감싸고 `Background="Transparent"` 설정
```xml
<ControlTemplate TargetType="{x:Type Button}">
    <Border Background="Transparent">
        <ContentPresenter Content="{TemplateBinding Content}"/>
    </Border>
    <ControlTemplate.Triggers>
        <Trigger Property="IsMouseOver" Value="True">
            <Setter Property="Opacity" Value="0.7"/>
        </Trigger>
    </ControlTemplate.Triggers>
</ControlTemplate>
```
* 배경을 FFFFFF(흰색)으로 하되 투명도를 최대(00 - 완전 투명)로 설정
  * Background에 색상을 지정하면 그 버튼 영역이 인식되기 때문에 Transparent로 인식 안되던 버튼 공간이 인식됨



### Static Resource, Dynamic Resource
* 리소스가 변경될 일이 없고 성능이 중요할 경우에는 Static 사용
* 리소스가 변경될 가능성이 있을 경우 Dynamic 사용



### TextBlock vs ContentPresenter
```xml
<RadioButton>
    <RadioButton.Content>
        <TextBlock>
            <Run Text="Go" />
            <LineBreak/>
            <Run Text="🏃‍➡️" />
        </TextBlock>
    </RadioButton.Content>
</RadioButton>
```
```xml
<TextBlock Text="{Binding Content, RelativeSource={RelativeSource TemplatedParent}}"/>
```
RadioButton.Content를 TextBlock.Text로 바인딩할 경우, string으로만 처리되므로 <LineBreak/> 같은 XAML 요소를 렌더링할 수 없음  
```xml
<ContentPresenter Content="{TemplateBinding Content}"
                  HorizontalAlignment="Center"
                  VerticalAlignment="Center"
                  TextElement.Foreground="{TemplateBinding Foreground}"/>
```
💡 ContentPresenter를 사용하면 리치한 Content 구조(TextBlock, StackPanel 등)를 그대로 표시할 수 있음



### DataGrid
DataGridCell의 기본 선택 스타일이 DataGridRow의 배경색을 덮어씀
→ Selected나 MouseOver 설정 시, DataGridRow뿐만 아니라 DataGridCell도 설정
```xml
<DataGrid>
    <DataGrid.Resources>
        <Style TargetType="{x:Type DataGridRow}">
            <Style.Triggers>
                <Trigger Property="IsSelected" Value="True">
                    <Setter Property="Background" Value="#D0E3FF"/>
                    <Setter Property="BorderBrush" Value="Transparent"/>
                    <Setter Property="Foreground" Value="Black"/>
                </Trigger>
            </Style.Triggers>
        </Style>

        <Style TargetType="{x:Type DataGridCell}">
            <Setter Property="FocusVisualStyle" Value="{x:Null}"/>
            <Style.Triggers>
                <Trigger Property="IsSelected" Value="True">
                    <Setter Property="Background" Value="Transparent"/>
                    <Setter Property="BorderBrush" Value="Transparent"/>
                    <Setter Property="Foreground" Value="Black"/>
                </Trigger>
            </Style.Triggers>
        </Style>
    </DataGrid.Resources>

    <DataGrid.Columns>
    </DataGrid.Columns>
</DataGrid>s
```



### Border와 Button
Button 대신 Border를 이용해서 Button과 같은 효과를 낼 수 있음  
단, Button의 경우 마우스를 누른 상태에서 범위를 벗어날 경우 클릭으로 인식되지 않음
* MouseDown: Border를 누를 경우, 바로 Event가 동작하므로 범위를 벗어나더라도 클릭으로 인식
* MouseLeftButtonUp: Button과 동일한 동작



### Ellipse
원 또는 타원을 그리는 기본 도형 클래스
```xml
<Ellipse Width="15" Height="15" 
        StrokeThickness="{TemplateBinding BorderThickness}"/>
```
태그에서 BorderThickness를 설정해도 Ellipse의 StrokeThickness에 값이 전달되지 않음  
→ Thickness 객체에서 필요한 Thickness 숫자 값을 직접 꺼내오도록 바인딩 경로를 수정
```xml
<Ellipse Width="15" Height="15" 
         StrokeThickness="{TemplateBinding BorderThickness.Left}"/>
```



### Polygon
다각형을 그리는 기본 도형 클래스
```xml
<Polygon Points="0,7.5 30,0 30,15" Fill="SkyBlue"
         StrokeThickness="2" Stroke="DarkSlateBlue"/>
```
* `Points="0,7.5 30,0 30,15"`: 도형을 구성하는 꼭짓점들의 X,Y 좌표 목록
  * `0,7.5`: 왼쪽 끝 중앙점
  * `30,0`: 오른쪽 위 점
  * `30,15`: 오른쪽 아래 점
* `Fill="SkyBlue"`: 도형 내부 색상
* `StrokeThickness="2"`: 외곽선 두께
* `Stroke="DarkSlateBlue"`: 도형 외곽선 색상



### 속성 값 우선순위
* 데이터 바인딩으로 설정된 값은 WPF 내에서 '로컬 값(Local Value)' 과 같은 매우 높은 우선순위를 갖음
* 로컬 값이 스타일 트리거보다 항상 우선순위가 높음  
→ 스타일 트리거로 바인딩된 값을 변경하려하면 바뀌지 않음
* C# 코드 비하인드에서 수정



### Event Routing
* 터널링(Tunneling): 상위에서부터 이벤트 발생 요소(Element)로 이벤트 발생
  * 부모 요소가 자식 요소의 특정 동작을 막고 싶을 때 사용(이벤트 **가로채기**, **차단**, 사전 감지 등)
  * 버블링(Bubbling) : 이벤트 발생 요소(Element)부터 상위로 이벤트 발생
    * 터널링이 끝난 후 실행됨
* 다이렉트(Direct) : 하나의 요소(Element)에서만 이벤트 발생
```txt
UI 구조: Window > Grid > Button

1. 터널링
이벤트가 최상위 요소(6Window)에서 시작하여 아래로 내려감
- Window에서 Preview Event가 있는지 확인
- Grid에서 Preview Event가 있는지 확인
- Button에서 Preview Event가 있는지 확인

2. 버블링
이벤트가 가장 하위 요소(Button)에 도달한 직후, 이제 반대로 위로 올라가기 시작
- Button에서 MouseDown 발생
- Grid에서 MouseDown 발생
- Window에서 MouseDown 발생
```

**예시**
```xml
<Grid>
	<Grid.ColumnDefinitions>
		<ColumnDefinition/>
		<ColumnDefinition/>
		<ColumnDefinition/>
	</Grid.ColumnDefinitions>
	<Grid.RowDefinitions>
		<RowDefinition/>
	</Grid.RowDefinitions>
	<Grid x:Name="TGrid01" Width="300" Height="300" Grid.Row="0" Grid.Column="0" 
		  Background="LightCyan" ButtonBase.Click="grid01_Click">
		<Label Content="TGrid01"/>
		<Grid x:Name="TGrid02" Width="250" Height="250" Background="LightGoldenrodYellow" 
			  ButtonBase.Click="grid02_Click">
			<Label Content="TGrid02"/>
			<Grid x:Name="TGrid03" Width="200" Height="200" Background="LightGreen" 
				  ButtonBase.Click="grid03_Click">
				<Label Content="TGrid03"/>
				<Grid x:Name="TGrid04" Width="150" Height="150" Background="LightPink" 
					  ButtonBase.Click="grid04_Click">
					<Label Content="TGrid04"/>
					<Button Content="Tunneling Test" Width="100" Height="30" Click="T_Button_Click"/>
				</Grid>
			</Grid>
		</Grid>
	</Grid>
	<StackPanel Grid.Row="0" Grid.Column="1" VerticalAlignment="Center">
		<Label Content="◀ Tunneling Event"/>
		<TextBox x:Name="tunnelTbx" Grid.Row="0" Grid.Column="1" Width="200" Height="100" Margin="10,0,10,10"/>
		<Label HorizontalAlignment="Right" Content="Bubbleing  Event ▶"/>
		<TextBox x:Name="bubbleTbx" Grid.Row="0" Grid.Column="1" Width="200" Height="100" Margin="10,0,10,0"/>
	</StackPanel>
	<Grid x:Name="BGrid01" Width="300" Height="300" Grid.Row="0" Grid.Column="2" 
		  Background="LightCyan" PreviewMouseDown="grid01_Click">
		<Label Content="BGrid01"/>
		<Grid x:Name="BGrid02" Width="250" Height="250" Background="LightGoldenrodYellow" 
			  PreviewMouseDown="grid02_Click">
			<Label Content="BGrid02"/>
			<Grid x:Name="BGrid03" Width="200" Height="200" Background="LightGreen" 
				  PreviewMouseDown="grid03_Click">
				<Label Content="BGrid03"/>
				<Grid x:Name="BGrid04" Width="150" Height="150" Background="LightPink" 
					  PreviewMouseDown="grid04_Click">
					<Label Content="BGrid04"/>
					<Button Content="Bubbling Test" Width="100" Height="30" PreviewMouseDown="B_Button_Click"/>
				</Grid>
			</Grid>
		</Grid>
	</Grid>
</Grid>
```
```cs
private void grid01_Click(object sender, RoutedEventArgs e)
{
    Grid grid = sender as Grid;
    string eventType = (grid.Name == "TGrid01") ? "Tunneling" : "Bubbling";
    InputText(eventType, grid);
}

private void grid02_Click(object sender, RoutedEventArgs e)
{
    Grid grid = sender as Grid;
    string eventType = (grid.Name == "TGrid02") ? "Tunneling" : "Bubbling";
    InputText(eventType, grid);
}
private void grid03_Click(object sender, RoutedEventArgs e)
{
    Grid grid = sender as Grid;
    string eventType = (grid.Name == "TGrid03") ? "Tunneling" : "Bubbling";
    InputText(eventType, grid);
    e.Handled = true;   // true이면 이벤트 전달 차단
}
private void grid04_Click(object sender, RoutedEventArgs e)
{
    Grid grid = sender as Grid;
    string eventType = (grid.Name == "TGrid04") ? "Tunneling" : "Bubbling";
    InputText(eventType, grid);
}

private void InputText(string evnetType, Grid grid)
{
    if (evnetType == "Tunneling")
        tunnelTbx.AppendText($"[Tunnling Event] {grid.Name}  \n");
    else
        bubbleTbx.AppendText($"[Bubbling Event] {grid.Name}  \n");
}

private void T_Button_Click(object sender, RoutedEventArgs e)
{
    tunnelTbx.AppendText($"Button_Click event!! \n");
}

private void B_Button_Click(object sender, RoutedEventArgs e)
{
    bubbleTbx.AppendText($"Button_Click event!! \n");
}
```
Tunneling Test  
`ButtonBase.Click`은 버블링(Bubbling) 이벤트  
Button_Click event!! → [Tunnling Event] TGrid04 → [Tunnling Event] TGrid03

Bubbling Test  
`PreviewMouseDown`은 터널링(Tunneling) 이벤트  
[Bubbling Event] BGrid01 → [Bubbling Event] BGrid02 → [Bubbling Event] BGrid03



### DragMove()
```xml
<Border x:Name="border">
    <Button x:Name="button"/>
</Border>
```
```cs
if (border != null)
{
	border.AddHandler(Border.MouseLeftButtonDownEvent, new MouseButtonEventHandler((sender, e) =>
	{
		try
		{
			DragMove();
		}
		catch { }
	}), true);
}

// MouseLeftButtonUpEvent
if (button != null)
{
	button.AddHandler(Button.MouseLeftButtonUpEvent, new RoutedEventHandler((sender, e) =>
	{
		try
		{
            // ...
		}
		catch { }
	}), true);
}

// PreviewMouseLeftButtonUpEvent
if (button != null)
{
	button.AddHandler(Button.PreviewMouseLeftButtonUpEvent, new RoutedEventHandler((sender, e) =>
	{
		try
		{
            // ...
		}
		catch { }
	}), true);
}
```
1. MouseLeftButtonUpEvent  
마우스 왼쪽 버튼 누르기 → MouseLeftButtonDownEvent 발생 → DragMove() → 마우스 왼쪽 버튼 떼기 → MouseLeftButtonUpEvent 터널링 후, 최하위 요소인 button에 도달하면 버블링 시작  
동시에 DragMove()에서 버튼 떼기 동작을 감지하고, 창 이동 모드를 종료하는 데 해당 이벤트를 사용(MouseLeftButtonUp 이벤트는 DragMove() 시스템에 의해 소모(handled)됨)  
이벤트가 시스템 레벨에서 소모되었기 때문에, 이벤트의 원래 발생지인 `button`에서부터 시작되는 버블링(`MouseLeftButtonUp`)은 아예 시작될 기회조차 얻지 못함  
결과적으로 `button`의 `MouseLeftButtonUp` 핸들러는 호출되지 않음
2. PreviewMouseLeftButtonUp
마우스 왼쪽 버튼 누르기 → MouseLeftButtonDownEvent 발생 → DragMove() → 마우스 왼쪽 버튼 떼기 → MouseLeftButtonUpEvent 터널링 후, 최하위 요소인 button에 도달하면 버블링 시작  
동시에 DragMove()에서 버튼 떼기 동작을 감지하고, 창 이동 모드를 종료하는 데 해당 이벤트를 사용하기 전에 **터널링 과정에서 PreviewMouseLeftButtonUp**가 먼저 발생
* DragMove 종료 이벤트보다 터널링은 빠르게 동작하고, 버블링은 늦게 동작하여 무시됨

\+ handledEventsToo: true가 동작하지 않는 이유
* DragMove()가 호출되면, Window는 마우스 캡처(마우스 입력 독점) 상태에 들어감
* MouseLeftButtonUp 이벤트는 DragMove()라는 특수 프로세스를 종료시키기 위한 신호로 사용
* DragMove()는 이 종료 신호를 받는 즉시, 자신의 임무(프로세스 종료)를 완수하고 MouseLeftButtonUp 이벤트를 시스템 레벨에서 소모  
(= 버블링을 위한 MouseLeftButtonUp 이벤트가 애초에 발생조차 하지 않도록 근원지에서 차단)



### AddHandler
지정된 라우트된 이벤트에 대해 라우트된 이벤트 처리기를 추가하여 처리기를 현재 요소의 처리기 컬렉션에 추가
```cs
public void AddHandler (System.Windows.RoutedEvent routedEvent, Delegate handler, bool handledEventsToo);
```
* routedEvent: 처리할 라우트된 이벤트에 대한 식별자
* handler: 처리기 구현에 대한 참조
* handledEventsToo: 이벤트 경로를 따라 다른 요소에 의해 처리된 것으로 이미 표시된 라우트된 이벤트에 대해 제공된 처리기를 호출하도록 true
  즉, 이 값을 true로 설정하는 것은 "다른 컨트롤이 이미 처리한(e.Handled = true) 이벤트까지도 무시하고, 자신의 순서가 되면 무조건 이 이벤트 핸들러를 무조건 실행하겠다"는 선언
  * 주로 자식 컨트롤이 이벤트를 "독점"하여 부모 컨트롤까지 이벤트가 도달하지 못하는 상황을 해결하기 위해 사용
  * 예시: `ScrollViewer`와 `TextBox`
    1. 사용자가 `TextBox` 내부를 클릭하면, `TextBox`는 캐럿(커서)을 옮기기 위해 `MouseDown` 이벤트를 사용하고, "이 클릭은 내가 처리했어!"라는 의미로 `e.Handled = true`를 설정
    2. 이 때문에 부모인 `ScrollViewer`는 일반적인 방법으로는 `TextBox`에서 발생한 클릭 이벤트를 감지할 수 없음
    3. 하지만 `ScrollViewer`는 내부에서 어떤 클릭이 일어나든 스크롤 상태를 제어해야 할 수 있어야 함 → 이때 `ScrollViewer`는 내부적으로 `AddHandler(..., true)`를 사용하여, `TextBox`가 막아버린 클릭 이벤트까지도 감지하여 필요한 로직(예: 마우스 휠 스크롤을 위한 포커싱)을 처리





### Visibility="Collapsed"
Visibility="Collapsed"인 요소는 XAML.cs 코드에서 FindName이나 x:Name으로 접근은 가능하지만, 그 내부의 자식 요소는 `Loaded`되지 않아서 `null`일 수 있음
```xml
<Grid x:Name="MyGrid" Visibility="Collapsed">
    <Button x:Name="MyButton"/>
</Grid>
```
```cs
MyButton.Content = "Click Me";
// MyGrid는 Collapsed 상태여도 인스턴스가 만들어져 있고 접근 가능
// 내부의 MyButton은 Collapsed 상태에 따라 아직 Visual Tree에 올라오지 않았을 수 있으므로 null이 될 수 있음
```



<br/>

### 📚 참고
[[WPF] 이벤트 라우팅, 터널링(Tunneling), 버블링(Bubbling)](https://memoo-list.tistory.com/19)  