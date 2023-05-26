import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import styles from "./Detail.module.css";

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
    document.body.style.overflowY = "hidden"; // 세로 스크롤 제거
  }, []);
  const onDownloadClick = () => {
    window.location.href = data?.data?.movie?.torrents?.[0]?.url;
  };
  const onWatchNowClick = () => {
    window.location.href = data?.data?.movie?.url;
  }
  
  return (
    <div>
      <div className={styles.detail}>
        <img
          className="styles.detail__img"
          src={data?.data?.movie?.large_cover_image}
          alt="Background Image"
        />
        {/* JSON 데이터 구조 확인 */}
        <div className={styles.detail__inner}>
          <div className={styles.detail__title}>
            {data?.data?.movie?.title_long}
          </div>
          <div className={styles.detail__synopsis}>
            {
              data?.data?.movie?.description_full
              /* console.log()에 찍히는 데이터 확인 후 데이터 입력 */
            }
          </div>
          <br />
          <div className={styles.detail__btn}>
            <div>
              <button
                className={styles.detail__downloadBtn}
                onClick={onDownloadClick}
              >
                DOWNLOAD
              </button>
            </div>
            <div>
              <button
                className={styles.detail__watchNowBtn}
                onClick={onWatchNowClick}
              >
                WATCH NOW
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Detail;
