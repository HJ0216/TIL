### 동기와 비동기
```cs
syncMethod1();
syncMethod2();
```
동기 메서드
* syncMethod1 완료 후, syncMethod2 실행
* UI Thread가 멈출 가능성이 존재

```cs
asyncMethod1();
asyncMethod2();
```
비동기 메서드
* 메서드를 호출만 하고, 완료를 기다리지 않음
* 실행 순서가 보장되지 않음

```cs
await asyncMethod1();
await asyncMethod2();
```
await + 비동기 메서드
* 비동기 메서드가 순차적으로 실행됨
* UI Thread가 멈추지 않음
```cs
private async void RunAsyncTask_Click(object sender, RoutedEventArgs e)
{
    Console.WriteLine("1");
    await DoWorkAsync();
    Console.WriteLine("5");
}

private async Task DoWorkAsync()
{
    Console.WriteLine("2");
    await Task.Delay(1000);
    Console.WriteLine("3");
    Console.WriteLine("4");
}

/*
1
2
(1초 후)
3
4
5
*/
```

동기적 로딩
* 모델 객체 내부에 이미지 데이터(BitmapImage)가 UI 바인딩 당시 로드되어 있는 상태 → INotifyPropertyChanged가 필요 없음

비동기적 로딩
1. 객체가 생성되고 리스트에 추가되어 UI에 바인딩될 때, 모델 객체 내부의 이미지 데이터가 아직 완전히 로드되지 않음
2. 비동기 동작이 완료되면 새로운 이미지 데이터가 생성됨
3. 새로운 이미지 데이터를 모델의 데이터 변수에 대입(속성이 참조하는 객체 자체가 변경됨)
4. UI는 속성이 이제 다른 객체를 가리키게 되었다는 사실을 모르므로 `INotifyPropertyChanged`를 사용하여 화면에 이미지를 갱신

```cs
// 동기
public BitmapImage Image { get; set; }

private void LoadImageSync(string source)
{
    BitmapImage loadedImage = GetBitmapImageSync(source);

    Application.Current.Dispatcher.Invoke(() =>
    {
        Image = loadedImage;
    }, DispatcherPriority.Background);
}

// 비동기
private BitmapImage _image;
public BitmapImage Image
{
    get => _image;
    set
    {
        if (!object.Equals(_image, value))
        {
            _image = value;
            OnPropertyChanged(nameof(Image));
        }
    }
}

public async Task LoadImageAsync(string source)
{
    BitmapImage loadedImage = await GetBitmapImageAsync(source);

    _ = Application.Current.Dispatcher.InvokeAsync(() =>
    {
        Image = loadedImage;
    }, DispatcherPriority.Background);
}
```

비동기와 finally
```cs
private async void Method()
{
	try
	{
		await Task.Run(() => MethodAsync());
        return;
	}
	catch(Exception ex)
	{
	}
    finally
    {
        // sample logic..
    }
}
```
* await를 사용한 비동기 작업이 끝나지 않으면, finally는 비동기 작업이 완료된 후에 실행
* return 문이 중간에 있어도 finally는 실행됨

#### 비동기 코드 사용 시, 주의 사항
* 작업이 완료되기 전에 Source에 할당할 경우, 값이 제대로 설정되지 않을 수 있음
```cs
public void Method(string source)
{
    Model model = new Model();
    model.Uri = source;
    model.Image = await GetBitmapImageAsync(source);

    Model selectedModel = model;
    // 문제1: model의 Image를 비동기로 가져오는데, 이미지가 Load되기 전 selectedModel에 model을 할당

    // ...

    CurrentModel = selectedModel
    // 문제2: Image가 없는 selectedModel을 CurrentModel에 할당
    image_CurrentImage.Source = CurrentModel.Image;
    // 비동기로 이미지가 추후에 Load되더라도 image_CurrentImage.Source의 데이터가 자동으로 업데이트되지 않음
    // 해결: image_CurrentImage.Source에 이미지를 따로 Load
    // image_CurrentImage.Source = await GetBitmapImageAsync(source);
}
```
* 이미지 로딩이 진행 중일 때 Image.Source = null로 바꾸면, 기존 비동기 로딩은 취소되지 않음 → 로딩이 완료되면 그 이미지가 다시 나타남(null로 바꿔도 이미지가 보일 수 있음)
  * 동기로 동작하는 데이터 값을 조건문으로 사용하여, 이미지 로딩이 될 수 있도록 할 수 있음


### Dispatcher
WPF: UI 요소 접근은 반드시 UI 스레드에서만 해야 함
1. `Task.Run`, `async/await`, `Thread` 등을 사용할 경우, 작업이 UI 스레드 바깥에서 실행될 수 있음
    * 무거운 작업을 UI 스레드에서 할 경우, 화면이 멈춘 것처럼 보이므로 이런 경우에 `Task.Run`을 사용
2. 이 상황에서 UI 요소에 접근 할 경우, `InvalidOperationException: The calling thread cannot access this object because a different thread owns it` 예외가 발생
3. 다시 UI 스레드로 돌아가기 위해 `Dispatcher` 사용

```cs
private async void Method()
{
	try
	{
		Method1(); // UI Thread
		await Task.Run(() => Method2()); // Background Thread
		Method3(); // UI Thread(ConfigureAwait(false)를 사용하지 않는 한)
	}
	catch(Exception ex)
	{
		// UI Thread
	}
}

public void Task Method2()
{
    Dispatcher.Invoke(() =>
	{
		// UI 작업 실행
	});
}
```
* UI 메서드에서 Dispatcher.Invoke 사용 시, `DeadLock` 문제 발생 유의

⭐ Dispatcher 사용법
* Task 메서드에서만 Dispatcher.Invoke 사용
* UI Event를 제외한 메서드 내부에서는 UI 이벤트, Task 메서드에서 중복으로 사용될 수 있으므로 Dispatcher.Invoke 사용 X

* 간접적으로 바인딩된 데이터를 사용할 때, Dispatcher 사용 여부
  * CurrentModels: UI 바인딩 O / AllModels: UI 바인딩 X
    * CurrentModels = AllModels
      * CurrentList와 AllList가 같은 객체를 참조하므로 UI에도 영향 → AllModels 변경 시 Dispatcher 필요 O
    * CurrentModels = AllModels.toList()
      * CurrentList는 독립된 List → AllModels 변경 시 Dispatcher 필요 X
  * CurrentModel이 UI에 직접적으로 바인딩되어있지 않을 경우, UI 컨트롤에 설정할 때 Dispatcher 선언

### `Dispatcher.InvokeAsync` / `Application.Current.Dispatcher.InvokeAsync`
* Dispatcher.InvokeAsync
    * 클래스가 Window, UserControl 또는 다른 DispatcherObject를 상속받은 클래스(대부분의 UI 요소 클래스)일 경우 사용 가능
* Application.Current.Dispatcher.InvokeAsync
    * ViewModel, Model 등 DispatcherObject를 상속받은 클래스가 아닐 경우 사용



### BitmapImage
```cs
public static async Task<BitmapImage> GetBitmapImageFromWebAsync(string imagePath)
{
    try
    {
        byte[] imageData = await httpClient.GetByteArrayAsync(imagePath);

        var bitmapImage = new BitmapImage();
        using (var stream = new MemoryStream(imageData))
        {
            stream.Position = 0;

            bitmapImage.BeginInit();
            bitmapImage.CacheOption = BitmapCacheOption.OnLoad;
            bitmapImage.StreamSource = stream;
            bitmapImage.EndInit();
        }

        bitmapImage.Freeze();

        return bitmapImage;
    }
    catch (Exception ex)
    {
        return null;
    }
}
```
* `using` 범위
    * MemoryStream은 IDisposable이니까 메모리 누수 방지를 위해 using을 써서 명확하게 해제하는 게 좋음
        * IDisposable Interface: using 문을 쓰면 작업이 끝난 다음에 자동으로 메모리를 해제(using문으로 해제가 되지 않을 경우, 명시적으로 Dispose()를 호출)
    * StreamSource를 BitmapImage에 연결하는, 즉 정확히 메모리스트림이 필요한 부분까지만 감싸는 게 좋음
    
* `BitmapImage.CacheOption = OnLoad`
    * 일반적으로 BitmapImage.CacheOption = OnLoad이면, EndInit() 시점에 스트림 내용을 다 읽고 메모리에 올림
    * 이 옵션이 없으면 BitmapImage는 스트림을 실시간으로 읽는 방식이어서, using으로 닫히면 이미지 로딩 실패
        * `Cannot access a closed Stream`
* `stream.Position = 0`
    * byte[]로부터 MemoryStream을 만들면 포인터가 스트림 끝에 위치
    * BitmapImage가 이미지를 읽기 전에 Position을 0으로 초기화해야 정상적으로 데이터를 읽을 수 있음
* `bitmapImage.Freeze()`
    * BitmapImage는 생성한 스레드에서만 수정할 수 있음 → Freeze()를 하면 이미지가 불변  상태가 되어 다른 스레드에서 사용해도 안전
        * `Must create DependencySource on same Thread as the DependencyObject.`
    * Freeze된 객체는 WPF 내부에서 성능 최적화가 가능해지고, 메모리 사용도 줄어듦
* 이미지가 바이트 배열에서 로드된 경우라면 UriSource는 null이고, StreamSource가 설정



### 디스카드(discard) 패턴
```cs
public async Task LoadImageAsync(string source)
{
    BitmapImage loadedImage = await GetBitmapImageAsync(source);

    _ = Application.Current.Dispatcher.InvokeAsync(() =>
    {
        Image = loadedImage;
    }, DispatcherPriority.Background);
}
```
1. Dispatcher.InvokeAsync 메서드는 DispatcherOperation 객체(Dispatcher 큐에 예약된 작업의 상태)를 반환
2. async 메서드나 이와 유사한 비동기 작업 객체(예: Task, DispatcherOperation)를 반환하는 메서드를 호출할 때, 그 결과를 await 하거나 변수에 할당하지 않으면 컴파일러는 CS4014 경고("이 호출은 await되지 않으므로 현재 메서드의 실행은 호출이 완료되기 전에 계속됩니다...")를 발생(비동기 작업의 완료를 기다리거나 예외를 처리하는 것을 잊었을 수 있음을 알려주기 위함)
3. 이 때 디스카드(_)를 사용해서 의도적으로 Dispatcher.InvokeAsync가 반환하는 DispatcherOperation 객체를 사용하지 않을 것임을 컴파일러에게 명시적으로 알릴 수 있음



### `값복사` vs `참조복사`
```cs
// TargetImage에 BitmapImage가 설정됨
BitmapImage TargetImage { get; set; }
string imageUri = string.empty;
UpdateBitmapImageAsync(imageUri);
public async Task UpdateBitmapImageAsync(string source)
{
    TargetImage = GetBitmapImageFromWebAsync(source);
}

// TargetImage에 BitmapImage가 설정되지 않음
UpdateBitmapImageAsync(Target, imageUri);
public async Task UpdateBitmapImageAsync(BitmapImage target, string source)
{
    target = GetBitmapImageFromWebAsync(source);
}
```
* 인스턴스를 새로 할당하는 경우, target = GetBitmapImageFromWebAsync(source);는 단순히 지역 변수 target을 바꾸는 것일 뿐, 실제 바인딩 대상인 TargetImage 속성에는 영향을 주지 않음
* 매개변수의 `일부 속성을 바꾸는 것`과 매개변수의 `참조값 자체를 바꾸는 것`의 차이

```cs
// 해결1: 매개변수로 넘기지 않고 직접 할당
BitmapImage TargetImage { get; set; }
string imageUri = string.empty;
UpdateBitmapImageAsync(imageUri);
public async Task UpdateBitmapImageAsync(string source)
{
    TargetImage = GetBitmapImageFromWebAsync(source);
    OnPropertyChanged(nameof(TargetImage));
}

// 해결2: 인스턴스를 바꾸지 않고 내부 스트림만 업데이트
public async Task UpdateBitmapImageAsync(BitmapImage bitmapImage, string source)
{
    byte[] imageData = await httpClient.GetByteArrayAsync(source);

    using (var stream = new MemoryStream(imageData))
    {
        stream.Position = 0;

        bitmapImage.BeginInit();
        bitmapImage.StreamSource = stream;
        bitmapImage.CacheOption = BitmapCacheOption.OnLoad;
        bitmapImage.EndInit();
    }

    bitmapImage.Freeze();
}
// 해결2의 문제
// Freeze()한 BitmapImage는 더 이상 Source나 내부 스트림 같은 걸 바꿀 수 없음(객체 자체가 Read-Only 상태로 고정됨)
// Freeze()는 BitmapImage를 생성한 UI Thread 이외의 Thread에서도 안전하게 접근할 수 있도록 하므로 사용 권장
```


### ref 타입
* 값 자체를 직접 바꿀 수 있도록 변수의 참조(reference) 를 함수에 넘길 때 사용
* async 메서드와는 함께 쓸 수 없음
```cs
class Model
{
    public string Name { get; set; }
}

Model TestModel1 = new Model { Name = "Original" };
Model TestModel2 = new Model { Name = "Original" };
Model TestModel3 = new Model { Name = "Original" };
Model TestModel4 = new Model { Name = "Original" };

private void UpdateMethodRef(ref Model model)
{
    Trace.WriteLine("Update - Before Ref: " + TestModel1.Name);
    model.Name = "Update Ref";
    Trace.WriteLine("Update - After Ref: " + TestModel1.Name);

    // 결과
    // Update - Before Ref: Original
    // Update - After Ref: Update Ref
}

private void UpdateMethodNotRef(Model model)
{
    Trace.WriteLine("Update - Before Not Ref: " + TestModel2.Name);
    model.Name = "Update Not Ref";
    Trace.WriteLine("Update - After Not Ref: " + TestModel2.Name);

    // 결과
    // Update - Before Not Ref: Original
    // Update - After Not Ref: Update Not Ref
}

private void ChangeMethodRef(ref Model model)
{
    Trace.WriteLine("Change - Before Ref: " + TestModel3.Name);
    model = new Model { Name = "Change Ref" };
    Trace.WriteLine("Change - After Ref: " + TestModel3.Name);

    // 결과
    // Change - Before Ref: Original
    // Change - After Ref: Update Ref
}

private void ChangeMethodNotRef(Model model)
{
    Trace.WriteLine("Change - Before Not Ref: " + TestModel4.Name);
    model = new Model { Name = "Change Not Ref" };
    Trace.WriteLine("Change - After Not Ref: " + TestModel4.Name);

    // 결과
    // Change - Before Not Ref: Original
    // Change - After Not Ref: Update Not Ref
}
```



### WebClient vs HttpClient
* WebClient
  * .NET Framework 시절부터 있던 오래된 클래스
  * using을 사용하여 사용할 때마다 생성 및 삭제
  * 파일 및 url 기반 모두 사용 가능
  * ***더 이상 지원하지 않기 때문에 신규 개발에 사용 X***
```cs
using (var client = new WebClient())
{
    string html = client.DownloadString("https://hj0216.tistory.com");
}
```

* HttpClient
  * .NET 4.5 이후 등장한 더 현대적인 HTTP 요청 방식
  * 생성 후 재사용하는 방식이 성능과 리소스 측면에서 좋음
  * async/await와 완벽하게 호환되어 비동기 작업을 깔끔하게 처리
  * url 기반: `httpClient.GetByteArrayAsync(source)`  
    file 기반: `File.ReadAllBytesAsync(source)`
```cs
public static class HttpClientProvider
{
    public static readonly HttpClient httpClient = new HttpClient();

    public static Task<byte[]> Method(string source)
    {
        if(IsWebUrl(source))
            return await httpClient.GetByteArrayAsync(source);
        
        return null;
    }

    public static bool IsWebUrl(string source)
    {
        return Uri.IsWellFormedUriString(source, UriKind.Absolute) &&
            (source.StartsWith("http://", StringComparison.OrdinalIgnoreCase) ||
            source.StartsWith("https://", StringComparison.OrdinalIgnoreCase));
    }
}
```


### ObservableCollection
* 컬렉션 내부의 항목이 추가, 삭제, 변경될 때 CollectionChanged 이벤트를 발생시켜 UI에 변경 사항을 알림
* new ObservableCollection<T>() 처럼 완전히 새로운 인스턴스를 할당하는 것은 그 속성 자체의 값이 바뀌는 것이지, 기존 컬렉션 내부의 내용이 바뀌는 것이 아님 = CollectionChanged가 발생하지 않음
  * 데이터 양이 많거나 변경이 잦을 경우(예: 슬라이드 페이지 넘김), Clear()와 여러 번의 Add() 호출은 각각 CollectionChanged 이벤트를 발생시켜 UI에서 버벅임이 발생할 수 있음
    * List<T>()/IEnumerable<T>() + INotifyPropertyChanged  
    새로운 리스트를 대입



### `Task` vs `void`
* async 메서드의 반환 타입을 왜 void가 아닌 Task로 하는 게 좋은가
  * 호출자가 완료 시점을 알 수 있음
    * 호출한 곳에서 await 키워드를 사용하여 해당 비동기 작업이 완료될 때까지 기다릴 수 있음
    * 완료된 후에 다른 작업을 수행해야 하는 경우 필수적
  * 예외 처리
    * async Task 메서드 내에서 발생하는 예외는 반환되는 Task 객체에 저장
    * 호출자가 이 Task를 await하면, 예외가 await 지점에서 다시 던져지므로 try-catch 블록으로 정상적으로 처리할 수 있음
    * Task 객체들은 Task.WhenAll (여러 작업을 동시에 실행하고 모두 완료될 때까지 대기)이나 Task.WhenAny (여러 작업 중 하나라도 완료될 때까지 대기) 등을 사용하여 조합하여 사용할 수 있음 → 비동기 흐름을 더 유연하게 구성할 수 있음
* async void는 주로 이벤트 핸들러(Event Handler)를 위해 존재(이벤트 핸들러의 시그니처는 반환 타입이 void여야 하기 때문)
  * 이 경우에도 async void 이벤트 핸들러 내부에서는 가능한 한 빨리 async Task 메서드를 호출
  * async void 메서드 자체에는 최소한의 로직(주로 try-catch로 async Task 메서드 호출 감싸기)만 두는 것이 좋음
```cs
private async void Button_Click(object sender, RoutedEventArgs e)
{
    try
    {
        await HandleButtonClickAsync();
    }
    catch (Exception ex)
    {
        ShowError(ex.Message);
    }
}

private async Task HandleButtonClickAsync()
{
    await SomeLongOperationAsync();
    // 여기서 예외가 발생하면 Task에 담겨 호출자(Button_Click)에게 전달됨
}
```



### await vs await Task.Run()
* await
  * 현재 컨텍스트 (UI 스레드, 작업자 스레드 등)에서 시작 및 재개
  * await 사이 동기 코드가 UI 스레드에서 실행되면 멈춤 유발 가능
  * 주로 기다리는 일(파일 저장, 네트워크 통신 등)일 때 좋음
* await Task.Run()
  * ThreadPool 스레드에서 전체 실행
  * UI 스레드 멈춤 없음 (작업 전체가 백그라운드에서 실행)
  * 컴퓨터가 머리를 많이 써야 하는 복잡한 계산 같은 부분(기다리는 거 말고 진짜 일하는 부분)이 길게 있을 때 좋음
  * 약간의 스레드 전환 오버헤드 발생
```cs
private async Task InitData()
{
    await Task.Delay(1000); // 비동기 대기 (예: DB에서 불러오기)
    Console.WriteLine("Init 완료!");
}

await InitData();

private void InitData()
{
    Thread.Sleep(3000); // 오래 걸림
    Console.WriteLine("Init 완료!");
}

await Task.Run(() => InitData()); // 백그라운드 스레드에서 처리
```
* 이미 비동기 I/O 위주인 메서드를 불필요하게 Task.Run으로 감싸는 것은 추가적인 스레드 전환 오버헤드를 발생시킬 수 있으므로 일반적으로 권장되지 않음

```cs
private async Task Method()
{
    Console.WriteLine($"[Method] 시작 - Thread ID: {Thread.CurrentThread.ManagedThreadId}");
    await Task.Delay(1000); // 비동기 대기
    Console.WriteLine($"[Method] 완료 - Thread ID: {Thread.CurrentThread.ManagedThreadId}");
}

Console.WriteLine($"[Main] Before await InitData - Thread ID: {Thread.CurrentThread.ManagedThreadId}");
await InitData();
Console.WriteLine($"[Main] After await InitData - Thread ID: {Thread.CurrentThread.ManagedThreadId}");
/*
[Main] Before await InitData - Thread ID: 1
[Method] 시작 - Thread ID: 1
[Method] 완료 - Thread ID: 1
[Main] After await InitData - Thread ID: 1

모든 작업이 UI 스레드(또는 주 스레드)에서 일어남
컨텍스트가 유지됨
*/

Console.WriteLine($"[Main] Before await Task.Run - Thread ID: {Thread.CurrentThread.ManagedThreadId}");
await Task.Run(() => InitData());
Console.WriteLine($"[Main] After await Task.Run - Thread ID: {Thread.CurrentThread.ManagedThreadId}");
/*
[Main] Before await InitData - Thread ID: 1
[Method] 시작 - Thread ID: 6
[Method] 완료 - Thread ID: 6
[Main] After await InitData - Thread ID: 1

불필요한 context switch + 리소스 낭비
*/
```



### 초기화
* `Loaded Event` vs `Constructor`
  * Loaded
    * UI 요소가 이미 로드된 후 → 안전하게 컨트롤 접근 가능
    * `await` 가능 → 파일, DB, 웹 요청도 자연스럽게 처리
  * Constructor
    * `new`로 객체 만들자마자 바로 필요한 간단한 값 설정
    * UI와 무관한 빠른 세팅 (예: 변수 초기화, 기본값 할당 등)
  * 객체 초기화는 데이터가 생성 시점에 즉시 사용 가능한지, 아니면 UI 로딩 및 환경 정보가 필요한지에 따라 생성자나 Loaded 이벤트를 선택하여 진행
* `속성` vs `생성자`
  * 속성
    * 초기화에 복잡한 로직이 필요할 때
    * 생성자 매개변수로 값을 받아 초기화할 때
    * 다수의 속성들을 함께 초기화할 때
```cs
public List<string> Holidays { get; set; }

public MyClass(bool isSpecial)
{
    Holidays = isSpecial ? new List<string> { "Special" } : new List<string>();
}
```
  * 생성자
    * 단순한 기본값을 설정할 때 (무조건 빈 리스트 만들기, 기본 숫자 넣기 등)
    * 복잡한 로직 없이 간단할 때
```cs
public List<string> Holidays { get; set; } = new List<string>();
```


### DependencyProperty 값 전달
* 생성자: InitializeComponent()가 내부적으로 호출 → OnApplyTemplate가 호출
* Loaded Event: InitializeComponent()가 이미 호출된 이후이므로, OnApplyTemplate 호출 X
💡 OnApplyTemplate의 필요 여부에 따라 생성자 또는 Loaded Event 사용
```cs
public class WindowBase_Extended : WindowBase
{
  public static readonly DependencyProperty IsDarkProperty =
      DependencyProperty.Register("IsDark", typeof(bool), typeof(WindowBase), new PropertyMetadata(true));

  public bool IsDark { get; set; }

  public override void OnApplyTemplate()
  {
      base.OnApplyTemplate();

      Border border_Midnight = Template.FindName("border_Midnight", this) as Border;
  }
}
```


### 책임의 분리
* Progress UI의 Visibility는 어느 메서드에 있는 게 좋을까
  * UI Event
    * UI 이외의 메서드는 로직에만 집중할 수 있음
    * 특히 실행 메서드가 다양한 곳에서 호출될 수 있고, UI와 독립적일 때
  * 실행 메서드 내부
    * 호출만 하면 Progress UI까지 신경쓰지 않아도 됨



### Nullable(?)
* 사용
  * 객체가 아직 설정되지 않은 경우가 있을 때
  * null이 정상적인 초기 상태이거나 없는 상태를 의미할 때
  * null일 수도 있는 상황을 코드로 명확히 하고 싶을 때
* 미사용
  * 항상 초기화되어 있을 때
  * 절대 null이 되어서는 안 될 때
* List
  * 초기에 빈 리스트로 만들면 null 체크 안하는 방법으로 주로 사용



### null or empty
* JsonConvert.DeserializeObject
  * 원본 데이터가 null 값이면 null을 반환
  * 원본 데이터가 비어 있는 JSON 배열이면 비어 있는 리스트 객체를 생성
* `from row in dt.Rows select ...`
  * dt.Rows가 비어 있으면 빈 IEnumerable 반환  
  → 빈 리스트는 비어있는 JSON 배열 [] 반환



### LINQ to SQL vs 순수 ADO.NET
* LINQ to SQL
  * .NET Framework에서 제공하는 ORM(Object-Relational Mapping) 도구
    * 요청 데이터의 구조가 DB 테이블과 거의 같을 때 자동 매핑이 가능하여 코드가 간결해짐
  * LINQ를 사용하여 SQL Server와 통신할 수 있음(**다른 DB는 지원하지 않음**)
  * 관련 엔티티는 실제 접근 시 로딩됨(Lazy Loading) → 불필요한 쿼리 실행을 줄일 수 있어 성능 최적화에 유리  
    (*정렬 후 데이터 필터링 사례 참고*)
  *  .NET 4.0 이후 업데이트 중단, 현재는 Entity Framework 또는 EF Core 사용이 권장됨
```cs
Northwnd nw = new Northwnd(@"northwnd.mdf");

var companyNameQuery =
    from cust in nw.Customers
    where cust.City == "London"
    select cust.CompanyName;
```
* 순수 ADO.NET
  * .NET에서 데이터베이스와 직접 통신하기 위해 사용하는 저수준의 데이터 액세스 기술
    * FormData 방식처럼 수동 파싱이 필요한 경우, SQL을 직접 작성해서 처리하는 방식이 더 적합
  * 모든 DBMS와 호환 가능
  * SQL 직접 실행하므로 변환 비용 없음  
    (LINQ to SQL은 내부적으로 LINQ를 SQL로 변환하는 오버헤드 발생)
  * 반복적인 코드(보일러플레이트)가 많아지고 유지보수가 어려울 수 있음
```cs
string connectionString = "Server=.;Database=MyDB;Trusted_Connection=True;";

using (SqlConnection conn = new SqlConnection(connectionString))
{
    conn.Open();

    string query = "SELECT Id, Name FROM Users WHERE Age > @Age";

    using (SqlCommand cmd = new SqlCommand(query, conn))
    {
        cmd.Parameters.AddWithValue("@Age", 20);

        using (SqlDataReader reader = cmd.ExecuteReader())
        {
            while (reader.Read())
            {
                int id = reader.GetInt32(0);
                string name = reader.GetString(1);
                Console.WriteLine($"Id: {id}, Name: {name}");
            }
        }
    }
}
```