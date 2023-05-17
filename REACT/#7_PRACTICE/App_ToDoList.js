import { useState } from "react";

function App_ToDoList() {
  const [toDo, setToDo] = useState("");
  const [toDos, setToDos] = useState([]);
  const onChange = (event) => {
    setToDo(event.target.value);
  };
  const onSubmit = (event) => {
    event.preventDefault();
    if (toDo === "") {
      return; // 함수 종료
    }
    // toDos.push();
    // state 변수는 setter를 통해서만 값 변경
    setToDos((currentArray) => [toDo, ...currentArray]);
    // ...배열: 배열 요소 복사
    setToDo("");
  };

  return (
    <div>
      <h1>My To Dos ({toDos.length})</h1>
      {/* JSX에서 JS 사용 시 {} 선언 */}
      <form onSubmit={onSubmit}>
        <input
          onChange={onChange}
          value={toDo}
          type="text"
          placeholder="Write your to do..."
        />
        <button>Add To Do</button>
      </form>
      <hr />
      <ul>
        {toDos.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export default App_ToDoList;
