import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function Detail() {
  const { id } = useParams();
  // URL을 통해 넘어오는 변수(:id)의 key-value 반환
  // const {id}:  URL 매개 변수 중 id 값을 추출하여 id 변수에 저장
  // const id: useParams()를 호출한 결과를 id 변수에 할당, useParams()의 반환 객체 전체
  console.log(id);
  const [data, setData] = useState({});
  const getMovie = async () => {
    const json = await (
      await fetch(`https://yts.mx/api/v2/movie_details.json?movie_id=${id}`)
    ).json();
    console.log(json);
    setData(json);
  };
  // await는 async() 내부에서만 사용 가능

  useEffect(() => {
    getMovie();
    // useEffect() 내부에서 getMovie()선언 후 호출 가능하나
    // 마운트 당시 한 번만 실행되는 useEffect()이므로 getMovie()가 마운트 될 때만 호출될 수 있음
  }, []);

  return (
    <div>
      <h1>Detail</h1>
      <h2>{data.data.movie.rating}</h2>
      {/* JSON 데이터 구조 확인 */}
    </div>
  );
}

export default Detail;
