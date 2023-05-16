import { useEffect, useState } from "react";

function App() {
  const [counter, setCounter] = useState(0);
  const [keyword, setKeyword] = useState("");
  const [showing, setShowing] = useState(false);

  const onClick = () => setCounter((prev) => prev + 1);
  console.log("i run all the time");
  // rendering할 때마다 호출
  const onChange = (event) => {
    setKeyword(event.target.value);
  };
  const onClick2 = () => setShowing((prev) => !prev);
  // prev, prevState: useState에서 이전 상태값을 나타내는 매개변수 이름
  function Hello() {
    /*
    1.
    function byFn() {
      console.log("bye:(");
    }
    function hiFn() {
      console.log("Hi :)");
      return byFn;
    }
    useEffect(hiFn, [])
    */

    // 2.
    useEffect(() => {
      console.log("create :)");
      return () => console.log("destroyed :(");
      // useEffect - cleanUp Function
    }, []);
    /*
    3. 
    useEffect(function() {
      console.log("hi :)");
      return function () {
        console.log("bye:(");
      };
    }, []);
    */
    return <h1>Hello</h1>;
  }
  function GoodNight() {
    useEffect(() => {
      console.log("Im here, Good Night!");
    }, []);
    return <h1>Good Night!</h1>;
  }

  useEffect(() => {
    console.log("I run when 'counter' changes");
  }, [counter]);
  const iRunOnlyOnce = () => {
    console.log("i run only once");
  };
  useEffect(iRunOnlyOnce, []);
  // 의존성배열: [] ▶ 컴포넌트 마운트(생성) 시에만 실행
  useEffect(() => {
    if ((keyword !== "") & (keyword.length > 5)) {
      console.log("SEARCH FOR", keyword);
    }
  }, [keyword]);

  return (
    <div>
      <input value={keyword} onChange={onChange} type="text" />
      <h1>{counter}</h1>
      <button onClick={onClick}>click me</button>
      <br />
      <br />
      {showing ? <Hello /> : <GoodNight />}
      {/* Component: jsx를 return하는 function */}
      <button onClick={onClick2}>{showing ? "Hide" : "Show"}</button>
    </div>
  );
}

export default App;
