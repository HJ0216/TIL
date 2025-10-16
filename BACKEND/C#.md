### 동기와 비동기

```cs
syncMethod1();
syncMethod2();
```

동기 메서드

- syncMethod1 완료 후, syncMethod2 실행
- UI Thread가 멈출 가능성이 존재

```cs
asyncMethod1();
asyncMethod2();
```

비동기 메서드

- 메서드를 호출만 하고, 완료를 기다리지 않음
- 실행 순서가 보장되지 않음

```cs
await asyncMethod1();
await asyncMethod2();
```

await + 비동기 메서드

- 비동기 메서드가 순차적으로 실행됨
- UI Thread가 멈추지 않음

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

- 모델 객체 내부에 이미지 데이터(BitmapImage)가 UI 바인딩 당시 로드되어 있는 상태 → INotifyPropertyChanged가 필요 없음

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

- await를 사용한 비동기 작업이 끝나지 않으면, finally는 비동기 작업이 완료된 후에 실행
- return 문이 중간에 있어도 finally는 실행됨

#### 비동기 코드 사용 시, 주의 사항

- 작업이 완료되기 전에 Source에 할당할 경우, 값이 제대로 설정되지 않을 수 있음

```cs
public async void Method(string source)
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

### Dispatcher

WPF: UI 요소 접근은 반드시 UI 스레드에서만 해야 함

1. `Task.Run`, `async/await`, `Thread` 등을 사용할 경우, 작업이 UI 스레드 바깥에서 실행될 수 있음
   - 무거운 작업을 UI 스레드에서 할 경우, 화면이 멈춘 것처럼 보이므로 이런 경우에 `Task.Run`을 사용
2. 이 상황에서 UI 요소에 접근 할 경우, `InvalidOperationException: The calling thread cannot access this object because a different thread owns it` 예외가 발생
3. 다시 UI 스레드로 돌아가기 위해 `Dispatcher` 사용

   - UI 메서드에서 Dispatcher.Invoke 사용 시, `DeadLock` 문제 발생 유의

   ```cs
   private async void Button_Click(object sender, RoutedEventArgs e)
   {
       await DoWorkAsync(); // 🔹 (1) UI 스레드는 여기서 "await" 상태로 대기
       MessageBox.Show("완료");
   }

   private Task DoWorkAsync()
   {
       // 🔹 (2) Task.Run으로 백그라운드 스레드 실행
       return Task.Run(() =>
       {
           // 🔹 (3) 백그라운드 스레드에서 UI 접근 시도
           // UI 스레드의 Dispatcher에게 작업을 "Invoke"로 요청 (동기 대기)
           Application.Current.Dispatcher.Invoke(() =>
           {
               // 이 코드는 UI 스레드에서 실행되어야 함
               // 그러나 UI 스레드는 (1) await 상태에서 대기 중이라 실행 불가
               MessageBox.Show("UI 접근");
           });
       });
   }
   ```

### `Dispatcher.InvokeAsync` / `Application.Current.Dispatcher.InvokeAsync`

- Dispatcher.InvokeAsync
  - 클래스가 Window, UserControl 또는 다른 DispatcherObject를 상속받은 클래스(대부분의 UI 요소 클래스)일 경우 사용 가능
- Application.Current.Dispatcher.InvokeAsync
  - ViewModel, Model 등 DispatcherObject를 상속받은 클래스가 아닐 경우 사용

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

- `using` 범위
  - MemoryStream은 IDisposable이니까 메모리 누수 방지를 위해 using을 써서 명확하게 해제하는 게 좋음
    - IDisposable Interface: using 문을 쓰면 작업이 끝난 다음에 자동으로 메모리를 해제(using문으로 해제가 되지 않을 경우, 명시적으로 Dispose()를 호출)
  - StreamSource를 BitmapImage에 연결하는, 즉 정확히 메모리스트림이 필요한 부분까지만 감싸는 게 좋음
  - using 블록 안에서 예외를 던지면 제대로 Dispose되지 않을 수 있으므로 using 블록이 정상 종료된 후 예외를 던지므로 리소스가 확실히 정리되도록 해야 함
- `BitmapImage.CacheOption = OnLoad`
  - 일반적으로 BitmapImage.CacheOption = OnLoad이면, EndInit() 시점에 스트림 내용을 다 읽고 메모리에 올림
  - 이 옵션이 없으면 BitmapImage는 스트림을 실시간으로 읽는 방식이어서, using으로 닫히면 이미지 로딩 실패
    - `Cannot access a closed Stream`
- `stream.Position = 0`
  - byte[]로부터 MemoryStream을 만들면 포인터가 스트림 끝에 위치
  - BitmapImage가 이미지를 읽기 전에 Position을 0으로 초기화해야 정상적으로 데이터를 읽을 수 있음
- `bitmapImage.Freeze()`
  - BitmapImage는 생성한 스레드에서만 수정할 수 있음 → Freeze()를 하면 이미지가 불변 상태가 되어 다른 스레드에서 사용해도 안전
    - `Must create DependencySource on same Thread as the DependencyObject.`
  - Freeze된 객체는 WPF 내부에서 성능 최적화가 가능해지고, 메모리 사용도 줄어듦
- 이미지가 바이트 배열에서 로드된 경우라면 UriSource는 null이고, StreamSource가 설정
- StreamSource 방식을 사용할 경우, Image의 FilePath는 Image의 Tag 속성에 저장해서 사용(UriSource를 사용할 수 없고, BitmapImage 자체에는 Tag 속성이 없음)

#### Stream 방식 vs Uri 방식

- Stream
  - 파일이 잠기지 않음 → 이미지 표시 중에도 파일 삭제/수정 가능
    - 임시 파일 처리: 편집 중간 결과물들 자유롭게 관리
    - 배치 처리: 여러 파일 동시에 처리할 때 파일 잠금 방지
  - CacheOption.OnLoad → 이미지 데이터를 메모리에 완전히 로드 후 스트림 닫음
    - 안전성: 원본 파일 손상 위험 없음
- Uri
  - 파일이 잠길 수 있음 → 이미지 사용 중 파일 삭제/수정 불가능

> 1.  Stream 방식 + OnLoad  
>     BitmapImage 생성 및 초기화  
>     Stream 데이터를 즉시 메모리에 완전 로드  
>     Stream Dispose되어도 메모리에 데이터 유지 ✅  
>     WPF에서 이미지 로드  
>     메모리에 데이터가 있으므로 ✅ 정상 표시

> 2.  Uri 방식 + OnLoad  
>     BitmapImage 생성 및 초기화  
>     파일에서 데이터를 즉시 메모리에 완전 로드  
>     파일 연결 끊음  
>     WPF에서 이미지 로드 → ✅ 정상 표시

> 3.  Stream 방식 + OnDemand  
>     BitmapImage 생성 및 초기화  
>     데이터 로드 안함, 스트림 참조만 저장  
>     Stream Dispose → 접근 경로 차단 🚫  
>     WPF가 렌더링 시 데이터 요청  
>     죽은 스트림에 접근 불가 → ❌ 표시 안됨

> 4.  Uri 방식 + OnDemand  
>     BitmapImage 생성 및 초기화  
>     데이터 로드 안함, 파일 경로만 저장  
>     WPF가 렌더링 시 필요할 때마다 파일에서 읽음  
>     ✅ 정상 표시 (파일이 살아있으니까)

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
3. 이 때 디스카드(\_)를 사용해서 의도적으로 Dispatcher.InvokeAsync가 반환하는 DispatcherOperation 객체를 사용하지 않을 것임을 컴파일러에게 명시적으로 알릴 수 있음

### `값복사` vs `참조복사`

```cs
// TargetImage에 BitmapImage가 설정되지 않음
UpdateBitmapImageAsync(Target, imageUri);
public async Task UpdateBitmapImageAsync(BitmapImage target, string source)
{
    target = await GetBitmapImageFromWebAsync(source);
    // 인스턴스를 새로 할당하는 경우, target = GetBitmapImageFromWebAsync(source);는 단순히 지역 변수 target을 바꾸는 것일 뿐, 실제 바인딩 대상인 Target에는 영향을 주지 않음
}

// 해결1: 매개변수로 넘기지 않고 직접 할당
public async Task UpdateBitmapImageAsync(string source)
{
    TargetImage = await GetBitmapImageFromWebAsync(source);
    OnPropertyChanged(nameof(TargetImage));
}

/**
인스턴스를 바꾸지 않고 내부 스트림만 업데이트할 경우
Freeze()한 BitmapImage는 더 이상 Source나 내부 스트림 같은 걸 바꿀 수 없음(객체 자체가 Read-Only 상태로 고정됨)
Freeze()는 BitmapImage를 생성한 UI Thread 이외의 Thread에서도 안전하게 접근할 수 있도록 하므로 사용 권장
*/
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
```

### ref 타입

- 값 자체를 직접 바꿀 수 있도록 변수의 참조(reference) 를 함수에 넘길 때 사용
- async 메서드와는 함께 쓸 수 없음

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
    // Change - After Ref: Change Ref
}

private void ChangeMethodNotRef(Model model)
{
    Trace.WriteLine("Change - Before Not Ref: " + TestModel4.Name);
    model = new Model { Name = "Change Not Ref" };
    Trace.WriteLine("Change - After Not Ref: " + TestModel4.Name);

    // 결과
    // Change - Before Not Ref: Original
    // Change - After Not Ref: Original
}
```

### WebClient vs HttpClient

- WebClient
  - .NET Framework 시절부터 있던 오래된 클래스
  - using을 사용하여 사용할 때마다 생성 및 삭제
  - 파일 및 url 기반 모두 사용 가능
  - **_더 이상 지원하지 않기 때문에 신규 개발에 사용 X_**

```cs
using (var client = new WebClient())
{
    string html = client.DownloadString("https://hj0216.tistory.com");
}
```

- HttpClient
  - .NET 4.5 이후 등장한 더 현대적인 HTTP 요청 방식
  - 생성 후 재사용하는 방식이 성능과 리소스 측면에서 좋음
  - async/await와 완벽하게 호환되어 비동기 작업을 깔끔하게 처리
  - url 기반: `httpClient.GetByteArrayAsync(source)`  
    file 기반: `File.ReadAllBytesAsync(source)`

```cs
public static class HttpClientProvider
{
    public static readonly HttpClient httpClient = new HttpClient();

    public static async Task<byte[]> Method(string source)
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

- 컬렉션 내부의 항목이 추가, 삭제, 변경될 때 CollectionChanged 이벤트를 발생시켜 UI에 변경 사항을 알림
  - 항목이 추가, 삭제, 변경될 때마다 이벤트가 발생하므로 대량의 데이터를 빠른 속도로 변경해야 하는 경우 성능 저하의 원인이 될 수 있음
- new ObservableCollection<T>() 처럼 완전히 새로운 인스턴스를 할당하는 것은 그 속성 자체의 값이 바뀌는 것이지, 기존 컬렉션 내부의 내용이 바뀌는 것이 아님 = CollectionChanged가 발생하지 않음
  - ObservableCollection 자체를 다시 한 번 INotifyPropertyChanged 처리
  ```cs
  private ObservableCollection<MyObject> myCollection;
  public ObservableCollection<MyObject> MyCollection
  {
      get { return myCollection; }
      set
      {
          if (myCollection != value)
          {
              myCollection = value;
              OnPropertyChanged(nameof(MyCollection));
          }
      }
  }
  ```
  - 새로운 인스턴스 할당 대신 Clear() 메서드 활용
  ```cs
  public void ClearData()
  {
      MyCollection.Clear();
  }
  ```

### `Task` vs `void`

- async 메서드의 반환 타입을 왜 void가 아닌 Task로 하는 게 좋은가
  - 호출자가 완료 시점을 알 수 있음
    - 호출한 곳에서 await 키워드를 사용하여 해당 비동기 작업이 완료될 때까지 기다릴 수 있음
    - 완료된 후에 다른 작업을 수행해야 하는 경우 필수적
  - 예외 처리
    - async Task 메서드 내에서 발생하는 예외는 반환되는 Task 객체에 저장
    - 호출자가 이 Task를 await하면, 예외가 await 지점에서 다시 던져지므로 try-catch 블록으로 정상적으로 처리할 수 있음
    - Task 객체들은 Task.WhenAll (여러 작업을 동시에 실행하고 모두 완료될 때까지 대기)이나 Task.WhenAny (여러 작업 중 하나라도 완료될 때까지 대기) 등을 사용하여 조합하여 사용할 수 있음 → 비동기 흐름을 더 유연하게 구성할 수 있음
- async void는 주로 이벤트 핸들러(Event Handler)를 위해 존재(이벤트 핸들러의 시그니처는 반환 타입이 void여야 하기 때문)
  - 이 경우에도 async void 이벤트 핸들러 내부에서는 가능한 한 빨리 async Task 메서드를 호출
  - async void 메서드 자체에는 최소한의 로직(주로 try-catch로 async Task 메서드 호출 감싸기)만 두는 것이 좋음
- 생성자, set 등 동기 코드 블록에서 비동기 메서드를 사용하는 경우, await을 사용할 수 없음
  - async 메서드 내부에서 자체적으로 오류를 처리할 수 있도록 try-catch 블럭 사용
  - 호출부에서는 \_(discard)를 사용하여 컴파일 경고창 제거

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

// Setter with Async
public mMember Member
{
    get { return member; }
    set
    {
        if (member != value)
        {
            member = value;

            _ = MethodAsync(member);
        }
    }
}

private async Task MethodAsync(mMember member)
{
    try
    {
    }
    catch (Exception ex)
    {
        // 예외를 호출한 쪽으로 전파되지 않고 비동기 메서드에서 직접 처리
    }
}
```

### await vs await Task.Run()

- await
  - 현재 컨텍스트 (UI 스레드, 작업자 스레드 등)에서 시작 및 재개
  - await 사이 동기 코드가 UI 스레드에서 실행되면 멈춤 유발 가능
  - 주로 기다리는 일(파일 저장, 네트워크 통신 등)일 때 좋음
- await Task.Run()
  - ThreadPool 스레드에서 전체 실행
  - UI 스레드 멈춤 없음 (작업 전체가 백그라운드에서 실행)
  - 컴퓨터가 머리를 많이 써야 하는 복잡한 계산 같은 부분(기다리는 거 말고 진짜 일하는 부분)이 길게 있을 때 좋음
  - 약간의 스레드 전환 오버헤드 발생

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

- 이미 비동기 I/O 위주인 메서드를 불필요하게 Task.Run으로 감싸는 것은 추가적인 스레드 전환 오버헤드를 발생시킬 수 있으므로 일반적으로 권장되지 않음

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

- `Loaded Event` vs `Constructor`
  - Loaded
    - UI 요소가 이미 로드된 후 → 안전하게 컨트롤 접근 가능
    - `await` 가능 → 파일, DB, 웹 요청도 자연스럽게 처리
  - Constructor
    - `new`로 객체 만들자마자 바로 필요한 간단한 값 설정
    - UI와 무관한 빠른 세팅 (예: 변수 초기화, 기본값 할당 등)
  - 객체 초기화는 데이터가 생성 시점에 즉시 사용 가능한지, 아니면 UI 로딩 및 환경 정보가 필요한지에 따라 생성자나 Loaded 이벤트를 선택하여 진행
- `속성` vs `생성자`
  - 생성자
    - 초기화에 복잡한 로직이 필요할 때
    - 생성자 매개변수로 값을 받아 초기화할 때
    - 다수의 속성들을 함께 초기화할 때
    - 클래스의 필드 및 속성 초기화가 모두 끝난 후에 생성자가 호출

```cs
public List<string> Holidays { get; set; }

public MyClass(bool isSpecial)
{
    Holidays = isSpecial ? new List<string> { "Special" } : new List<string>();
}
```

- 속성
  - 단순한 기본값을 설정할 때 (무조건 빈 리스트 만들기, 기본 숫자 넣기 등)
  - 복잡한 로직 없이 간단할 때
  - 생성자 호출 전에 초기화

```cs
public List<string> Holidays { get; set; } = new List<string>();
```

### DependencyProperty 값 전달

- 생성자: InitializeComponent()가 내부적으로 호출 → OnApplyTemplate가 호출
- Loaded Event: InitializeComponent()가 이미 호출된 이후이므로, OnApplyTemplate 호출 X
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

- Progress UI의 Visibility는 어느 메서드에 있는 게 좋을까
  - UI Event
    - UI 이외의 메서드는 로직에만 집중할 수 있음
    - 특히 실행 메서드가 다양한 곳에서 호출될 수 있고, UI와 독립적일 때
  - 실행 메서드 내부
    - 호출만 하면 Progress UI까지 신경쓰지 않아도 됨

### Nullable(?)

- 사용
  - 객체가 아직 설정되지 않은 경우가 있을 때
  - null이 정상적인 초기 상태이거나 없는 상태를 의미할 때
  - null일 수도 있는 상황을 코드로 명확히 하고 싶을 때
- 미사용
  - 항상 초기화되어 있을 때
  - 절대 null이 되어서는 안 될 때
- List
  - 초기에 빈 리스트로 만들면 null 체크 안하는 방법으로 주로 사용

### null or empty

- JsonConvert.DeserializeObject
  - 원본 데이터가 null 값이면 null을 반환
  - 원본 데이터가 비어 있는 JSON 배열이면 비어 있는 리스트 객체를 생성
- `from row in dt.Rows select ...`
  - dt.Rows가 비어 있으면 빈 IEnumerable 반환  
    → 빈 리스트는 비어있는 JSON 배열 [] 반환

### LINQ to SQL vs 순수 ADO.NET

- LINQ to SQL
  - .NET Framework에서 제공하는 ORM(Object-Relational Mapping) 도구
    - 요청 데이터의 구조가 DB 테이블과 거의 같을 때 자동 매핑이 가능하여 코드가 간결해짐
  - LINQ를 사용하여 SQL Server와 통신할 수 있음(**다른 DB는 지원하지 않음**)
  - 관련 엔티티는 실제 접근 시 로딩됨(Lazy Loading) → 불필요한 쿼리 실행을 줄일 수 있어 성능 최적화에 유리  
    (_정렬 후 데이터 필터링 사례 참고_)
  - .NET 4.0 이후 업데이트 중단, 현재는 Entity Framework 또는 EF Core 사용이 권장됨

```cs
Northwnd nw = new Northwnd(@"northwnd.mdf");

var companyNameQuery =
    from cust in nw.Customers
    where cust.City == "London"
    select cust.CompanyName;
```

- 순수 ADO.NET
  - .NET에서 데이터베이스와 직접 통신하기 위해 사용하는 저수준의 데이터 액세스 기술
    - FormData 방식처럼 수동 파싱이 필요한 경우, SQL을 직접 작성해서 처리하는 방식이 더 적합
  - 모든 DBMS와 호환 가능
  - SQL 직접 실행하므로 변환 비용 없음  
    (LINQ to SQL은 내부적으로 LINQ를 SQL로 변환하는 오버헤드 발생)
  - 반복적인 코드(보일러플레이트)가 많아지고 유지보수가 어려울 수 있음

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

### string vs enum

- string 값보다 enum 값 타입이 넘어올 때 의도를 더 명확히 할 수 있음

```cs
public class Notification
{
    private readonly string _type;

    public Notification(string type)
    {
        _type = type;
    }
}

var n = new Notification("EMAIL");
```

- "EMAIL"이라는 문자열은 오타가 날 수도 있고

- 의미가 뭔지 정확히 알기 어려움

- 사용할 수 있는 값의 범위도 제한되어 있지 않음

```cs
public enum NotificationType
{
    Email,
    Sms,
    Push
}

public class Notification
{
    private readonly NotificationType _type;

    public Notification(NotificationType type)
    {
        _type = type;
    }
}

var n = new Notification(NotificationType.Email);
```

- 어떤 값들이 허용되는지 명확히 알 수 있음
- 오타 가능성이 사라짐(컴파일러 확인)
- NotificationType.Email처럼 이 값이 무엇을 의미하는지 명확하게 표현할 수 있음

### items.FirstOrDefault() vs items[0]

- items.FirstOrDefault()
  - 리스트의 첫 번째 요소를 반환하거나, 요소가 없으면 null을 반환
  - 리스트가 비어 있거나 null일 경우에도 예외가 발생하지 않고, null을 반환  
    → FirstOrDefault()의 반환 값이 null인지 확인해야 안전하게 사용할 수 있음
- items[0]
  - 리스트가 비어 있거나 0번 인덱스에 접근할 수 없는 경우, 즉시 예외(ArgumentOutOfRangeException)가 발생

### 불변 객체

- 한번 생성된 후에는 그 내부의 상태(속성 값)를 변경할 수 없는 객체
- 표현식 하나로 새로운 객체를 생성하여 할당하는 방식을 자주 사용

```cs
ImmutableModel model = IsShown ? new ImmutableModel(data, true) : new ImmutableModel(data, false);
```

### LockObject

멀티스레딩 환경에서 코드의 특정 부분을 한 번에 하나의 스레드만 실행하도록 보장하기 위한 '자물쇠' 또는 '열쇠' 역할을 하는 객체  
여러 스레드가 동시에 접근할 수 있는 싱글턴(Singleton) 패턴을 안전하게 구현하기 위해 lock 키워드와 함께 사용할 수 있음

```cs
internal static readonly object LockObject = new object();

private static Window instance;
public static Window Instance
{
    get
    {
		if (instance == null)
		{
			lock(LockObject)
			{
				if(instance == null)
				{
					instance = new Window();
				}
			}
		}

		return instance;
	}
}
```

### Lazy

```cs
private static readonly Lazy<Window> lazyInstance =
    new Lazy<Window>(() => new Window());

public static Window Instance
{
    // .Value에 처음 접근할 때 단 한번만 객체가 생성
    get { return lazyInstance.Value; }
}
```

Lazy<Window>는 내부적으로 Value가 한 번 생성되면 변경하거나 초기화할 수 없음  
윈도우를 닫고 다시 열 때 새로 만들 수 없는 구조

### enum값과 캡슐화

메서드 return 값과 직접 비교를 할 때, 중복 호출에 유의

```cs
if (CheckStatus()== Status.Error) return;
else if(CheckStatus()== Status.Changed) await RefreshData();
```

```cs
Status status = CheckStatus();
if (status == Status.Error) return;
else if(status == Status.Changed) await RefreshData();
```

로직 캡슐화

```cs
// async를 사용하는 메서드에서는 Async를 접미사로 붙이는 게 좋음
public async Task<bool> HandleStatusChangeAsync()
{
    Status status = CheckStatus();

    switch (status)
    {
        case Status.Unchanged:
            return true;

        case Status.Changed:
            return await RefreshDataAsync();

        case Status.Error:
            return false;

        default:
            return false;
    }
}

bool isSuccess = await HandleStatusChangeAsync();
```

### Instance간 데이터 공유

```cs
// parent -> child
// wndInstanceA
wndInstanceB wnd = wndInstanceB.Instance as wndInstance;
wnd.Show(this);

// wndInstanceB
public void Show(wndInstance parents)
{
    Age = parents.Age;

    // ...
}

// child -> parent
// wndInstanceB
public event Action<int> OnAgeChanged;

private int age;
private void IncreaseAge()
{
    age++;
    OnAgeChanged?.Invoke(age);
}

// wndInstanceA
wndInstanceB wnd = wndInstanceB.Instance as wndInstance;
wnd.OnAgeChanged += (changedAge) => Age = changedAge;
wnd.Show(this);
```

### Delegate

- 메서드에 대한 참조를 저장할 수 있는 타입
- 메서드를 변수처럼 저장하고 나중에 호출할 수 있게 함

```cs
public delegate int CalculatorDelegate(int x, int y);

public class SimpleCalculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }

    public int Subtract(int a, int b)
    {
        return a - b;
    }
}

public class Program
{
    public static void Main()
    {
        SimpleCalculator calc = new SimpleCalculator();

        CalculatorDelegate addDelegate = new CalculatorDelegate(calc.Add);
        CalculatorDelegate subtractDelegate = calc.Subtract; // 단축 문법

        int sum = addDelegate(10, 5);
        int difference = subtractDelegate(10, 5);

        Console.WriteLine($"덧셈 결과: {sum}");       // 출력: 덧셈 결과: 15
        Console.WriteLine($"뺄셈 결과: {difference}"); // 출력: 뺄셈 결과: 5
    }
}
```

```cs
public delegate void MessageDelegate(string message);

public class Processor
{
    public void PerformAction(MessageDelegate callback)
    {
        Console.WriteLine("작업을 시작합니다...");

        System.Threading.Thread.Sleep(1000); // 1초 대기

        callback("작업이 완료되었습니다!");
    }
}

public class Program
{
    public static void ShowMessage(string msg)
    {
        Console.WriteLine($"[알림] {msg}");
    }

    public static void LogMessage(string msg)
    {
        Console.WriteLine($"[로그] {DateTime.Now}: {msg}");
    }

    public static void Main()
    {
        Processor processor = new Processor();

        MessageDelegate alertCallback = ShowMessage;
        processor.PerformAction(alertCallback);
        // 작업을 시작합니다...
        // [알림] 작업이 완료되었습니다!

        Console.WriteLine("----------");

        MessageDelegate logCallback = LogMessage;
        processor.PerformAction(logCallback);
        // 작업을 시작합니다...
        // [로그] 2025-06-28 오전 7:54:30: 작업이 완료되었습니다!

    }
}
```

Processor 클래스는 구체적으로 어떤 메시지 처리 방법(ShowMessage 또는 LogMessage)이 실행될지 알지 못하고, MessageDelegate 형식의 대리자를 호출  
Processor 클래스의 변경 없이도 메시지를 화면에 출력하거나 로그 파일에 쓰는 등 다양한 동작을 외부에서 주입할 수 있음

```cs
public delegate void Notify();

public class Broadcaster
{
    public event Notify SendNotification;

    public void Broadcast()
    {
        Console.WriteLine("알림을 보냅니다!");
        SendNotification?.Invoke(); // 연결된 메서드가 있을 경우에만 호출 (?. 연산자)
    }
}

public class Subscriber1
{
    public void ReceiveNotification()
    {
        Console.WriteLine("구독자 1: 알림을 받았습니다.");
    }
}

public class Subscriber2
{
    public void ReceiveNotification()
    {
        Console.WriteLine("구독자 2: 저도 알림을 받았습니다!");
    }
}

public class Program
{
    public static void Main()
    {
        Broadcaster broadcaster = new Broadcaster();
        Subscriber1 sub1 = new Subscriber1();
        Subscriber2 sub2 = new Subscriber2();

        // += 연산자를 사용하여 메서드를 delegate에 추가 (구독)
        broadcaster.SendNotification += sub1.ReceiveNotification;
        broadcaster.SendNotification += sub2.ReceiveNotification;

        // delegate 호출 (알림 발생)
        broadcaster.Broadcast();
        // 알림을 보냅니다!
        // 구독자 1: 알림을 받았습니다.
        // 구독자 2: 저도 알림을 받았습니다!

        Console.WriteLine("\n--- 구독자 1 해지 ---\n");

        // -= 연산자를 사용하여 메서드를 delegate에서 제거 (구독 취소)
        broadcaster.SendNotification -= sub1.ReceiveNotification;

        broadcaster.Broadcast();
        // 알림을 보냅니다!
        // 구독자 2: 저도 알림을 받았습니다!
    }
}
```

+= 와 -= 연산자를 사용하여 SendNotification이라는 하나의 delegate 변수에 여러 메서드를 자유롭게 추가하거나 제거  
Broadcast() 메서드를 호출하면 연결된 모든 메서드가 순차적으로 실행

### 제네릭 대리자

- 대표적인 제네릭 대리자: Func, Action, Predicate
- .NET에서는 매번 delegate를 선언하는 불편함을 덜어주기 위해 가장 일반적으로 사용되는 형태의 제네릭 대리자를 미리 정의

1. Func<T, TResult>
   반환 값이 반드시 있는 메서드를 위한 제네릭 대리자  
   T는 입력 매개변수의 타입을 의미하고, 가장 마지막에 오는 TResult가 항상 반환 타입  
   최대 16개의 입력 매개변수를 가질 수 있음
2. Action<T>
   반환 값이 없는(void) 메서드를 위한 제네릭 대리자  
   입력 매개변수만 지정
3. Predicate<T>
   특정 조건을 검사하고 bool 값을 반환하는 특별한 형태의 제네릭 대리자  
   주로 리스트 등에서 특정 조건을 만족하는 항목을 찾을 때 사용  
   사실상 Func<T, bool>와 동일하지만, '조건을 검사한다'는 의미를 명확히 하기 위해 사용

### Func

- 반환 값이 있는 메서드를 위한 미리 정의된 편리한 delegate
- 반환 값이 있는 메서드를 빠르고 간편하게 대리자로 사용하고 싶을 때, 특히 LINQ나 람다식과 함께 자주 사용

```cs
public class Program
{
    public static int Add(int x, int y)
    {
        return x + y;
    }

    public static void Main()
    {
        // Func<int, int, int>는 int형 매개변수 두 개를 받고, int형을 반환한다는 의미
        Func<int, int, int> addFunc = Add;

        int result = addFunc(10, 5);

        Console.WriteLine($"결과: {result}"); // 결과: 15
    }
}
```

```cs
public class Program
{
    public static void Main()
    {
        Func<int, int, int> multiplyFunc = (a, b) => a * b;

        int result = multiplyFunc(10, 5);
        Console.WriteLine($"곱셈 결과: {result}"); // 곱셈 결과: 50

        string[] fruits = { "Apple", "Banana", "Cherry", "Grape" };

        // Enumerable.Count 메서드는 Func<TSource, bool> 타입의 대리자를 인자로 받음
        // Count 메서드는 이 판별 결과를 보고, true일 때만 자기 내부의 카운터를 1씩 증가시킴
        int longNameCount = fruits.Count(name => name.Length > 5); // 이름의 길이가 5보다 큰 과일의 개수

        Console.WriteLine($"이름이 5글자보다 긴 과일의 개수: {longNameCount}"); // 이름이 5글자보다 긴 과일의 개수: 2
    }
}
```

### Action

- .NET에 미리 정의된 제네릭 대리자 중 하나로, 반환 값이 없는(void) 메서드를 참조할 때 사용
- 무언가를 실행하고 끝나기만 하는, 즉 반환 값이 필요 없는 메서드를 위한 것

```cs
public class Program
{
    public static void SayHello()
    {
        Console.WriteLine("안녕하세요!");
    }

    public static void ShowTime()
    {
        Console.WriteLine($"현재 시간: {DateTime.Now.ToShortTimeString()}");
    }

    public static void Main()
    {
        Action simpleAction = SayHello;

        simpleAction = ShowTime;

        simpleAction(); // 현재 시간: (현재 시간)

        Action multiAction = SayHello;
        multiAction += ShowTime;

        multiAction();
        // 안녕하세요!
        // 현재 시간: (현재 시간)
    }
}
```

```cs
using System;
using System.Collections.Generic;

public class Program
{
    public static void LogMessage(string message)
    {
        Console.WriteLine($"[LOG] {DateTime.Now}: {message}");
    }

    public static void DisplayProduct(int id, string name)
    {
        Console.WriteLine($"상품 코드: {id}, 상품명: {name}");
    }

    public static void Main()
    {
        Action<string> logger = LogMessage;
        logger("서버가 시작되었습니다."); // [LOG] (현재 시간): 서버가 시작되었습니다.

        Action<int, string> productDisplayer = DisplayProduct;
        productDisplayer(1001, "노트북"); // 상품 코드: 1001, 상품명: 노트북
    }
}
```

```cs
public class Program
{
    public static void Main()
    {
        List<string> names = new List<string> { "Alice", "Bob", "Charlie" };

        Action<string> printName = name => Console.WriteLine($"이름: {name}");
        names.ForEach(printName);
        // 이름: Alice
        // 이름: Bob
        // 이름: Charlie

        Console.WriteLine("\n--- 구분선 ---");

        names.ForEach(name => Console.WriteLine($"Hello, {name}!"));

        List<int> numbers = new List<int> { 10, 20, 30 };
        numbers.ForEach(num =>
        {
            int doubled = num * 2;
            Console.WriteLine($"{num}의 2배는 {doubled}입니다.");
        });
    }
}
```

### EventHandler

- .NET에서 이벤트를 처리하기 위해 특별히 만들어진 **표준 대리자(Standard Delegate)**
- "이벤트"라는 특정 목적을 위해 설계되었기 때문에 명확한 규약과 패턴을 가지고 있음
- EventHandler는 다음과 같이 정해진 형식의 메서드만 참조할 수 있음

```cs
void MethodName(object sender, EventArgs e)
```

1. void 반환 형식
2. object sender: 이벤트를 **발생시킨 객체(인스턴스)**  
   예: 버튼 클릭 이벤트: sender=해당 버튼 객체 → 어떤 객체가 이벤트를 보냈는지 알 수 있음
3. EventArgs e: 이벤트와 관련된 추가 데이터를 담는 객체  
   만약 전달할 추가 데이터가 없다면, 기본 EventArgs.Empty가 사용  
   더 많은 정보를 전달하고 싶다면 EventArgs를 상속하는 새로운 클래스를 만들어 사용

```cs
public class MessageEventArgs : EventArgs
{
    public string Message { get; }
    public DateTime TimeSent { get; }

    public MessageEventArgs(string message)
    {
        Message = message;
        TimeSent = DateTime.Now;
    }
}

public class Publisher
{
    public event EventHandler<MessageEventArgs> EmergencyEvent;

    public void CheckMessage(string input)
    {
        Console.WriteLine($"입력 확인: '{input}'");
        if (input.Contains("fire"))
        {
            OnEmergencyEvent(new MessageEventArgs(input));
        }
    }

    // 이벤트를 발생시키는 메서드 (protected virtual로 만드는 것이 표준 패턴)
    protected virtual void OnEmergencyEvent(MessageEventArgs e)
    {
        // 구독자가 있는지 확인하고, 있다면 이벤트를 호출(Invoke)
        EmergencyEvent?.Invoke(this, e);
    }
}

public class Program
{
    public static void Main()
    {
        Publisher publisher = new Publisher();

        publisher.EmergencyEvent += HandleEmergency;
        publisher.EmergencyEvent += Call119;

        publisher.CheckMessage("The weather is nice."); // 아무 일도 일어나지 않음
        Console.WriteLine();
        publisher.CheckMessage("Warning! There is a fire in the building!"); // 이벤트 발생!
        /*
        입력 확인: 'Warning! There is a fire in the building!'
                    >> 긴급 상황 처리반: 이벤트 감지!
                    보낸 객체: Publisher
                    메시지: 'Warning! There is a fire in the building!'
                    발생 시각: 2025-06-28 오전 8:45:38
                    >> 119 자동 신고 시스템: 긴급 상황 접수 및 출동 요청!
        */

        publisher.EmergencyEvent -= Call119;
        Console.WriteLine("\n--- 119 신고 핸들러 제거 후 ---");
        publisher.CheckMessage("fire! fire!");
        /*
        입력 확인: 'Warning! There is a fire in the building!'
                    >> 긴급 상황 처리반: 이벤트 감지!
                    보낸 객체: Publisher
                    메시지: 'Warning! There is a fire in the building!'
                    발생 시각: 2025-06-28 오전 8:45:38
        */
    }

    public static void HandleEmergency(object sender, MessageEventArgs e)
    {
        Console.WriteLine(">> 긴급 상황 처리반: 이벤트 감지!");
        Console.WriteLine($"   보낸 객체: {sender.GetType().Name}");
        Console.WriteLine($"   메시지: '{e.Message}'");
        Console.WriteLine($"   발생 시각: {e.TimeSent}");
    }

    public static void Call119(object sender, MessageEventArgs e)
    {
        Console.WriteLine(">> 119 자동 신고 시스템: 긴급 상황 접수 및 출동 요청!");
    }
}
```

### Event

- 대리자(delegate)에 적용하는 한정자(modifier)로, 해당 대리자를 안전한 이벤트 발행/구독 모델로 만들어주는 역할
- `event` 한정자를 쓰는 이유
  - **구독자 목록 덮어쓰기 (`=`) 방지:** 다른 구독자가 실수로 기존 구독자들을 모두 지워버리는 것을 막습니다.
  - **이벤트 임의 발생 방지 (`Invoke`) 방지:** 오직 이벤트를 소유한 클래스만이 이벤트를 발생시킬 수 있도록 합니다.
- `event` 한정자를 쓰지 않는 경우

  - `public Action`이나 `public Func`처럼 `event` 없이 델리게이트를 그대로 노출하는 경우는, 알림이 아니라 외부에서 클래스의 행동 방식 자체를 교체하도록 허용하고 싶을 때 사용
  - 여러 구독자(`+=`)를 갖는 것이 아니라, 단 하나의 메서드만 할당(`=`)하여 **클래스의 특정 로직을 위임**하는 것이 목적

  ```cs
  // "문자열 하나를 받아 아무것도 안하는" 로직을 위임받을 설계도
  public delegate void LogStrategy(string message);

  public class Worker
  {
      // 이 Worker의 "로그 기록 전략"은 외부에서 주입/교체할 수 있음
      public LogStrategy Logger;

      public void DoWork()
      {
          Console.WriteLine("작업을 시작합니다...");
          // ... 어떤 작업 수행 ...

          Logger?.Invoke("작업이 완료되었습니다.");
      }
  }

  // --- 사용하는 쪽 ---
  public static class Program
  {
      public static void Main()
      {
          var worker1 = new Worker();
          // 작업자1의 로그 기록 전략은 "콘솔에 출력하는 것"으로 설정
          worker1.Logger = (message) => Console.WriteLine($"[Console] {message}");
          worker1.DoWork();

          Console.WriteLine("---");

          var worker2 = new Worker();
          // 작업자2의 로그 기록 전략은 "파일에 쓰는 것"으로 설정
          worker2.Logger = (message) => File.AppendAllText("log.txt", message + "\n");
          worker2.DoWork();
      }
  }
  ```

### `abstract` / `virtual`

- 추상 메서드(Abstract Method)

  - `abstract`(추상) 메서드로 선언하면 그 클래스를 상속받는 모든 자식 클래스가 반드시 해당 메서드를 구현(override)해야함
  - 부모: 규칙(추상 메서드)만 정의
  - 자식: 부모가 정의한 그 규칙을 자신에 맞게 구체적으로 구현(override)

  ```cs
  // Child
  public partial class wndChild : Window
  {
      // "멤버가 변경되었음"을 알릴 이벤트
      public event Action MemberChanged;

      private void SaveButton_Click(object sender, RoutedEventArgs e)
      {
          // ... 멤버 정보 저장 로직 ...

          // 구독자들에게 알림
          MemberChanged?.Invoke();
          this.Close();
      }
  }

  // 자식 클래스가 반드시 구현해야 할 메서드를 포함하므로, wndBase는 abstract 클래스
  public abstract partial class wndBase : Window
  {
      // ... wndBase의 다른 코드들 ...

    protected void OpenChildWindow()
      {
          wndChild childWindow = new wndChild();

          // 자식 창의 MemberChanged 이벤트가 발생하면,
          // 이 클래스를 상속받은 자식 클래스가 구현할 OnChildMemberChanged 메서드를 호출하도록 구독
          childWindow.MemberChanged += OnChildMemberChanged;

          childWindow.ShowDialog();
      }

      /// <summary>
      /// 자식 창에서 멤버가 변경되었을 때 호출될 추상 메서드입니다.
      /// { } 몸통이 없으며, 이 클래스를 상속받는 클래스는 반드시 이 메서드를 구현(override)
      /// </summary>
      protected abstract void OnChildMemberChanged();
  }

  public partial class wndParents : wndBase // wndBase를 상속
  {
      // 목표: 이 필드의 값을 "arrived"로 변경하기
      public string Test;

      public wndParents()
      {
          InitializeComponent();
      }

      // wndBase에 있는 OpenChildWindow()를 호출하는 버튼 (예시)
      private void SomeButton_Click(object sender, RoutedEventArgs e)
      {
          // 부모 클래스에 정의된 자식 창 열기 메서드를 호출
          base.OpenChildWindow();
      }

      /// 부모 클래스(wndBase)에 abstract로 선언된 메서드를 override 키워드를 사용하여 구체적으로 구현
      protected override void OnChildMemberChanged()
      {
          // 이 로직은 wndParents 클래스에만 존재
          this.Test = "arrived";

          Debug.WriteLine($"wndParents: 자식 창으로부터 Member 변경 알림 도착!");
          Debug.WriteLine($"wndParents: Test 필드 값이 '{this.Test}'로 변경되었습니다.");
      }
  }
  ```

- 가상 메서드(Virtual Method)

  - 어떤 자식은 구현하고, 어떤 자식은 구현하지 않아도 되는' **선택적인 재정의**가 필요할 때는, `abstract` 대신 **`virtual`(가상)** 키워드를 사용
  - `wndParents`처럼 알림 처리가 필요한 클래스만 해당 메서드를 재정의하고, 다른 자식 클래스들은 무시할 수 있음

  ```csharp
  // wndBase
  public partial class wndBase : Window
  {
      // ...

      protected void OpenChildWindow()
      {
          wndChild childWindow = new wndChild();
          childWindow.MemberChanged += OnChildMemberChanged;
          childWindow.ShowDialog();
      }

      /// <summary>
      /// 자식 창에서 멤버가 변경되었을 때 호출될 가상 메서드입니다.
      /// 'virtual' 이므로 자식 클래스에서 재정의(override)하는 것이 선택사항이 됩니다.
      /// 기본 동작은 아무것도 하지 않는 것입니다.
      /// </summary>
      protected virtual void OnChildMemberChanged()
      {
          // 기본적으로는 아무 일도 하지 않음
      }
  }

  public partial class wndParents : wndBase
  {
      public string Test;

      // ...

      /// <summary>
      /// 부모의 virtual 메서드를 override 하여 자신만의 특별한 동작을 구현합니다.
      /// </summary>
      protected override void OnChildMemberChanged()
      {
          this.Test = "arrived";
          Debug.WriteLine($"wndParents: 알림을 받아 Test 필드를 변경했습니다.");
      }
  }

  public partial class wndAnotherParents : wndBase
  {
      // OnChildMemberChanged를 재정의(override)하지 않아도 아무 문제가 없습니다.
      // 만약 이 창에서 OpenChildWindow()를 호출하고 자식 창에서 이벤트가 발생하면,
      // 아무 내용 없는 부모(wndBase)의 OnChildMemberChanged()가 호출되고 조용히 넘어갑니다.
  }
  ```

| 구분            | `abstract` 메서드                                           | `virtual` 메서드                                             |
| --------------- | ----------------------------------------------------------- | ------------------------------------------------------------ |
| **구현 강제성** | **강제 (자식은 반드시 `override` 해야 함)**                 | **선택 (자식이 `override` 해도 되고 안 해도 됨)**            |
| **기본 구현**   | **불가능** (몸통 `{}`을 가질 수 없음)                       | **가능** (기본 동작을 `{}` 안에 구현해 둘 수 있음)           |
| **클래스 선언** | 메서드를 가진 클래스는 `abstract`여야 함                    | 일반 클래스에서도 선언 가능                                  |
| **주요 용도**   | 자식들이 **반드시 가져야 하는** 핵심 기능의 **'규칙'** 정의 | 자식들이 **선택적으로 확장/변경할 수 있는 '기본 동작'** 제공 |

### 다형성

C# 런타임은 `OnChildMemberChanged()`를 호출하는 시점에, 변수의 타입(`wndBase`)이 아니라 그 변수가 **실제로 가리키고 있는 객체의 타입(`wndParents`)**을 확인

그리고 그 실제 객체에 `override`된 메서드가 있다면, 언제나 부모의 `virtual` 메서드보다 **자식의 `override`된 메서드를 우선적으로 호출**

따라서 `wndBase`에 있는 코드가 `OnChildMemberChanged()`를 호출하더라도, 그 코드를 실행하는 실제 객체가 `wndParents`의 인스턴스라면 `wndParents`에 있는 `override`된 버전이 실행

### Casting

ItemsSource의 실제 타입이 무엇이든 관계없이, 그 내용물을 새로운 List<T>로 안전하게 만들고 싶다면 LINQ의 ToList() 확장 메서드를 사용

```cs
IEnumerable<Item> itemsSourceAsEnumerable = treeview.ItemsSource as IEnumerable<Item>;

List<Item> treeviewItemList = null;

if (itemsSourceAsEnumerable != null)
{
    // 3. ToList(): 새로운 List<T> 생성
    treeviewItemList = itemsSourceAsEnumerable.ToList();
}
```

### BuildHierarchy, FlatHierarchy

```cs
private List<Item> BuildHierarchy(List<Item> items)
{
    var nodeDict = new Dictionary<string, Item>();

    foreach (var item in items)
    {
        nodeDict[item.Id] = new Item(item);
    }

    var rootNodes = new List<Item>();

    foreach (var item in items)
    {
        Item currentNode = nodeDict[item.Id];
        string parentId = item.ParentId;

        if (!string.IsNullOrEmpty(parentId) && nodeDict.ContainsKey(parentId))
        {
            nodeDict[parentId].Children.Add(currentNode);
        }
        else
        {
            rootNodes.Add(currentNode);
        }
    }

    return rootNodes;
}


public List<Item> FlattenHierarchy(IEnumerable<Item> hierarchicalItems)
{
    var flatList = new List<Item>();
    if (hierarchicalItems == null) return flatList;

    foreach (var item in hierarchicalItems)
    {
        flatList.Add(item);

        if (item.Children != null && item.Children.Any())
        {
            flatList.AddRange(FlattenHierarchy(item.Children));
        }
    }

    return flatList;
}
```

### 다형성과 List

```cs
public class Animal { }
public class Dog : Animal { }
public class Cat : Animal { }

// 만약 List<T>가 공변성을 지원한다면...
List<Animal> animals = new List<Dog>();

// 가정: 이게 허용된다면
animals.Add(new Cat());

// 💥 런타임 에러! Dog 리스트에 Cat을 넣으려고 함
```

### TreeView, TreeViewItem

`CommonTreeView` class와 `CommonTreeViewItem` class를 함께 두는 것이 좋음

1. **밀접한 관계**: `CommonTreeViewItem`은 `CommonTreeView`의 전용 컨테이너로만 사용됨
2. **단순성**: 하나의 기능을 위한 두 클래스를 한 곳에서 관리
3. **WPF 관례**: 많은 WPF 커스텀 컨트롤들이 이런 방식 사용

### IDisposable

- IDisposable를 인터페이스로 구현하는 클래스의 객체는 사용이 끝난 후 Dispose()를 호출하여 메모리를 정리해줘야한다.
- 정리해주지 않아도 GC에서 정리를 해주지만 정리 타이밍을 알 수 없고, 정리 중 오류가 날 경우 TryCatch로도 잡을 수 없기 때문에 정리를 해줘야한다.

StreamReader(IDisposable 구현)

```cs
StreamReader reader = new StreamReader("content.txt");

try {
    string content = reader.ReadToEnd();
} catch(IOException e) {
    Debug.Log ("Error: " + e.Message);
} finally {
    reader.Close();
    // StreamReader의 Close()에서는 해당 객체를 Dispose()

}

// using을 사용할 경우 생략할 수 있음
using (StreamReader reader = new StreamReader("content.txt"))
{
    string content = reader.ReadToEnd();
}
// {}을 벗어나는 순간 reader.Close()을 자동으로 해줌
```

### Server Model

- 서버에서 Id를 자동 생성하려면 서버 쪽 모델에서 Id 필드를 optional로 선언해야 함

```cs
public string? Id { get; set; }

// public string Id { get; set; } // C# 8.0+ 에서는 자동으로 Required
```

### Tuple

- Tuple<uint, uint>
  - Item1, Item2로만 접근 (의미 불명확)
  - 힙 메모리 사용 (느림)
  - .NET Framework 4.0+에서 사용 가능

```cs
// 선언
private static Tuple<uint, uint> GetSize()
{
    return new Tuple<uint, uint>(1920, 1080);
}

// 사용
var result = GetSize();
uint width = result.Item1;   // 😵 Item1이 뭔지 모호
uint height = result.Item2;  // 😵 Item2가 뭔지 모호
```

- (uint width, uint height)
  - 이름으로 접근 (의미 명확)
  - 스택 메모리 사용 (빠름)
  - 분해(destructuring) 지원
  - C# 7.0+ 필요

```cs
// 선언
private static (uint width, uint height) GetSize()
{
    return (1920, 1080);
}

// 사용
var (width, height) = GetSize();
// 또는
var result = GetSize();
uint w = result.width;   // 😍 의미가 명확
uint h = result.height;  // 😍 의미가 명확
```

- Stack Memory / Heap Memory
  - Stack Memory
    - 빠름 - 바로 접근 가능
    - 자동 정리 - 함수 끝나면 자동으로 사라짐
    - 크기 제한 - 보통 1MB 정도
    ```cs
    int age = 25;
    bool isActive = true;
    (int x, int y) point = (10, 20);
    ```
  - Heap Memory
    - 느림 - 찾아서 가야 함
    - 수동 정리 - 가비지 컬렉터가 나중에 청소
    - 크기 자유 - 큰 데이터도 OK
    ```cs
    string name = "홍길동";
    List<int> numbers = new List<int>();
    Tuple<int, int> tuple = new Tuple<int, int>(1, 2);
    ```

### Tuple List vs Dictionary

- Tuple List
  ```cs
  List<(string Key, int Value)> tupleList = new List<(string Key, int Value)>
  {
      ("apple", 10),
      ("banana", 5),
      ("orange", 8)
  };
  ```
  - 순서가 보장됨
  - 중복 키 허용
- Dictionary
  ```cs
  Dictionary<string, int> dictionary = new Dictionary<string, int>
  {
      {"apple", 10},
      {"banana", 5},
      {"orange", 8}
  };
  ```
  - 순서 보장 안됨
  - 중복 키 불허용
  - 해시테이블 기반으로 빠른 조회

### throw Exception vs return null

- throw Exception
  - 다양한 예외를 다르게 처리하고 싶을 때
    - 세부적 예외 처리가 좋은 경우
      - 사용자가 해결할 수 있는 문제
      - 각 예외마다 다른 대응이 필요한 경우
      - 중요한 비즈니스 로직이 있는 경우
    - 일반적 예외 처리가 좋은 경우
      - 단순한 기능
      - 예외 종류를 예측하기 어려운 경우
  - 디버깅 정보가 중요할 때
  - 예외가 예상되는 상황일 때
  - 특정 예외만 의미있게 처리하고 나머지는 일반 처리하는 것이 좋음
- return null
  - 실패를 정상적인 흐름으로 처리할 때
  - 간단한 성공/실패만 구분하면 될 때

### 조기 return vs catch

- 조기 return
  - 예외 발생 → catch → 처리보다 적은 비용
  - null 체크는 일반적인 방어용
- catch
  - 예외적인 상황용

### var

- 🎯 var를 쓰는 게 좋은 경우

  ```cs
  var bitmapImage = new BitmapImage();
  var list = new List<string>();
  var path = GetImagePath();

  var imageDict = new Dictionary<string, List<BitmapImage>>();
  ```

  - 타입이 명확할 때
  - 긴 제네릭 타입

- 📋 명시적 타입이 좋은 경우

  ```cs
  BitmapImage image = GetSomeImage();

  IList<string> items = new List<string>();
  ```

  - 타입이 불분명할 때
  - 인터페이스 사용할 때

### Nullable

- int? (Nullable<int>)
  - int는 값 타입(value type)
  - 값 타입은 원래 null을 가질 수 없음
  - HasValue (bool) : null인지 여부
  - Value (T) : 실제 값 (null이면 접근 시 예외 발생)
- string?
  - string은 참조 타입(reference type)
  - 참조 타입은 원래부터 null 허용
  - string과 string?은 런타임 동작이 동일
  - string에는 Nullable<T> 같은 wrapper가 필요 없고, 따라서 .Value 속성도 없음

### const vs readonly

- const
  - 컴파일 타임 상수
  - 반드시 컴파일러가 알 수 있는 리터럴 값이어야 함
    - 리터럴 값: 코드에 직접 적는 값 (숫자, 문자열, true/false 등)
  - 버전 관리 / 다중 어셈블리 환경에서는 const값 불일치 문제
    - const를 라이브러리 A에 정의, 라이브러리 B가 참조
    - B를 빌드할 때, A의 const 값은 그대로 B의 라이브러리에 남아있음(값 복사)
    - 나중에 A의 const 값을 수정해도, B는 재빌드하지 않으면 옛날 값을 계속 사용하게 됨
- readonly
  - 값이 런타임 시점에 결정
  - 리터럴뿐 아니라, new, DateTime.Now, Guid.NewGuid() 같은 복잡한 표현식도 할당 가능
  - readonly는 "필드 참조"로 남아있음
  - 따라서 라이브러리 A의 값을 바꿔도, B는 재컴파일 없이도 새로운 값을 가져옴

```cs
// 라이브러리 A
public class Constants
{
    public const string ApiVersionConst = "v1";       // 컴파일 타임에 박힘
    public static readonly string ApiVersionReadonly = "v1"; // 런타임 참조
}

// 라이브러리 B
Console.WriteLine(Constants.ApiVersionConst);
Console.WriteLine(Constants.ApiVersionReadonly);

// A에서 "v1" → "v2"로 수정 후 A만 빌드해서 배포했을 때:
// const → 여전히 B는 "v1" 출력 (재컴파일 필요)
// readonly → 자동으로 "v2" 출력 (재컴파일 불필요)
```

### 매개변수 vs 전역변수

- 매개변수 방식
  - 테스트 용이
  - 재사용성
  - 전역 상태에 의존하지 않음
- 전역변수 방식
  - 함수 시그니처만 봐서는 뭐가 필요한지 모름
  - 특정 전역 상태에 종속되어 재사용 불가
- 매개변수가 많을 경우
  - 매개변수 객체 패턴 사용 가능

### finally

- 리소스 정리, 파일 닫기, 연결 해제 같은 필수 작업
- return문
  - try/catch의 return 값을 덮어씀
  - 예외가 완전히 숨겨짐

### Query Parameter vs Path Parameter

- Query Parameter
  - `GET /api/images?id=123&type=1`
  - 리소스 계층 구조가 명확하지 않음
  - 검색/필터링과 같이 선택적 필터 추가 용이
- Path Parameter
  - `GET /api/images/123/1`
  - 북마크/공유에 더 적합
    - id, type 같은 파라미터 조합이 많아질 경우 링크가 길어지고, 나중에 API 버전 업이나 쿼리 파라미터 변경 시 깨질 확률이 높음

### 계층별 Error 처리 방식

- 하위 계층 (Data/API Layer)
  - 복구 가능하면 catch에서 복구, 아니면 throw
- 중간 계층 (Business Logic)
  - 보통 catch 하지 않음, 또는 로깅만
- 상위 계층 (UI/Presentation)
  - 사용자에게 오류 메시지 표시

### Using statement vs Using declaration

- Using statement
  - 중괄호 블록이 없어도 스코프 끝에서 자동 Dispose
- Using declaration
  - 블록({})이 끝날 때 자동 Dispose

#### Dispose

- C#에는 메모리 관리는 자동(GC가 처리)되지만, 파일, 네트워크, 이미지, DB 연결처럼 `외부 자원`은 직접 해제해야 함
  - Dispose를 안할 경우
    - 파일이 계속 점유되어 “다른 곳에서 못 염”
    - DB 연결이 닫히지 않음
    - 이미지나 스트림이 메모리를 계속 잡고 있음

```cs
// 직접 Dispose
var stream = File.OpenRead("data.txt");
try
{
    // 파일 읽기
}
finally
{
    stream.Dispose(); // 자원 해제
}

// 자동 Dispose
using (var stream = File.OpenRead("data.txt"))
{
    // 파일 읽기
}
// 여기를 벗어나면 자동으로 stream.Dispose() 호출됨

public void TestDispose()
{
  using var stream = File.OpenRead("data.text");
}
// 여기를 벗어나면 자동으로 stream.Dispose() 호출됨

```

### Base64

- 바이너리 데이터를 텍스트 형태로 인코딩하는 방식
- 이메일이나 웹 같은 시스템은 원래 텍스트만 다룰 수 있음 → 이미지, 동영상, 실행 파일 같은 바이너리 데이터를 전송해야 할 때, Base64는 바이너리 데이터를 텍스트로 변환해서 안전하게 전송할 수 있게 해줌
  - 바이너리 데이터란 컴퓨터가 0과 1로만 표현하는 모든 데이터
- 단점: 원본보다 약 33% 정도 크기가 커짐
- 이메일 첨부파일, 웹에서 이미지 임베딩 (Data URL), API에서 바이너리 데이터 전송, 인증 토큰 등에서 사용

#### 이미지 임베딩

- 장점

  - 서버 요청 횟수가 줄어듦
  - 작은 아이콘이나 로고에 유용

- 단점

  - HTML 파일 크기가 커짐
  - 큰 이미지에는 비효율적
    - 원본보다 약 33% 크기가 커지므로 큰 이미지일 때는 HTML 파일 크기가 커져 페이지 로딩이 느려짐
  - 캐싱이 안 됨
    - 브라우저는 URL을 기준으로 파일을 캐싱하는데, 일반 이미지 파일은 URL이 고유한 식별자 역할을 하여 같은 URL을 만나면 저장된 파일 사용
    - Data URL은 파일 경로가 아니라 데이터 자체가 들어있어 HTML 파일의 일부로 취급됨

- 보통 작은 아이콘이나 로고처럼 자주 바뀌지 않는 작은 이미지에만 사용

```html
<img src="photo.jpg" />
<!--이미지 파일이 서버에 별도로 저장되어 있어야 함
브라우저가 HTML을 읽고, 다시 서버에 이미지 파일을 요청해서 가져옴
총 2번의 요청이 필요 (HTML 1번 + 이미지 1번)-->

<img src="data:image/png;base64,iVBORw0KGgoAAAANS..." />
<!--이미지 데이터가 HTML 코드 안에 포함됨
별도의 이미지 파일 요청이 필요 없음
1번의 요청으로 끝-->
```

### asp-for

```html
<input type="hidden" id="product-id" value="@Model.ProductId" />
<!--단방향: 서버 → 클라이언트만 전달
    POST 시 서버로 자동 바인딩 안 됨-->
<input type="hidden" asp-for="product-color" id="product-color" />
<!-- 양방향: 서버 ↔ 클라이언트
name 속성 자동 생성 (모델 바인딩용)
value 자동 설정
유효성 검사 속성 자동 추가
  [BindProperty]와 함께 사용 시 POST 자동 바인딩-->
```
