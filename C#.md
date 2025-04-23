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
