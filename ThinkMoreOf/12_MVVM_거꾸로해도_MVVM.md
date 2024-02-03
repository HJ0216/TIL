# 11_MVVM_거꾸로해도_MVVM
조금 더 생각해 보고 싶은 부분을 공부한 글입니다.

- 작성일: 2024-02-02
- 수정일: 2024-02-03

<br/>



#
### 주제를 선정한 이유
최근에 C#과 WPF를 시작하면서 MVVM 패턴을 알게되었습니다. 자바를 배울 때 MVC 패턴이 세상을 지배한 줄 알았는데, 비슷한듯 다른 MVVM 패턴에 대해 한 번 정리해보고자 합니다.

<br/>



#
### MVVM 정의
![MVVM_Structure](./images/11/MVVM_Structure.png)
MVVM은 Model-View-ViewModel의 약어로,  UI 및 비 UI 코드를 분리하기 위한 UI 아키텍처 디자인 패턴입니다. Model의 데이터를 가공하는 ViewModel과, 그 ViewModel을 보여주는 View로 이루어져 있습니다.  
C#과 WPF에서는 XAML로 UI를 정의하고, 데이터 바인딩 태그를 사용하여 데이터 및 명령을 포함하는 ViewModel에 연결합니다.

1. Model
- 데이터의 구조, 속성 등

```cs
namespace Practice.Plugin.Models
{
	public class Student
	{
		public int Id {get; set;}
		public string Name {get; set;}
		public int Age {get; set;}
	}
}
```

2. View
- 유저가 보는 그래픽 컨트롤들의 집합

```html
<Window>
	<Grid>
		<TextBox Name="textBox01" Text="{Binding Id}">
		<TextBox Name="textBox01" Text="{Binding Name}">
		<TextBox Name="textBox01" Text="{Binding Age}">
	</Grid>
</Window>
```

3. ViewModel
- View와 Model를 연결하는 요소
- MVC의 Controller 역할

```cs
namespace Practice.Plugin.ViewModels
{
    public class MainViewModel
    {
		private int id;
		public int Id {get; set;}

		private string name;
		public string Name {get; set;}

		private int age;
		public int Age {get; set;}	
	}
}
```

#
### 정리

<br/>



#
### 📚참고 자료
[MVVM이란?](https://velog.io/@ellyheetov/MVVM%EC%9D%B4%EB%9E%80)  
[데이터 바인딩 및 MVVM](https://learn.microsoft.com/ko-kr/windows/uwp/data-binding/data-binding-and-mvvm)  
[안드로이드 MVVM개념? 이 글 하나로 끝낸다.](https://velog.io/@squart300kg/mvvmComplete)  
[C#으로 본 MVVM 패턴 정리 및 활용](https://www.centbin.com/c%EC%9C%BC%EB%A1%9C-%EB%B3%B8-mvvm-%ED%8C%A8%ED%84%B4-%EC%A0%95%EB%A6%AC-%EB%B0%8F-%ED%99%9C%EC%9A%A9-%EB%B0%A9%EB%B2%95%EC%9D%84-%EC%9D%B4%EC%95%BC%EA%B8%B0%ED%95%A9%EB%8B%88%EB%8B%A4/)  
