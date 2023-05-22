import { useEffect, useState } from "react";

import Movie from "../components/Movie";
import Slider from "react-slick";

import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "./home.css"

function Home() {
  const [loading, setLoading] = useState(true);
  const [movies, setMovies] = useState([]);
  //   useEffect(() => {
  //     fetch(
  //       `https://yts.mx/api/v2/list_movies.json?minimum_rating=9&sort_by=year`
  //     )
  //       .then((response) => response.json())
  //       .then((json) => {
  //         setMovies(json.data.movies);
  //         setLoading(false);
  //       });
  //   }, []);

  // const getMovies = async () => {
  //     const response = await fetch(
  //         `https://yts.mx/api/v2/list_movies.json?minimum_rating=9&sort_by=year`
  //     );
  //     const json = await response.json();
  //      setMovies(json.data.movies);
  //      setLoading(false);
  // }

  const getMovies = async () => {
    const json = await (
      await fetch(
        `https://yts.mx/api/v2/list_movies.json?minimum_rating=9&sort_by=year`
      )
    ).json();
    setMovies(json.data.movies);
    setLoading(false);
  };

  useEffect(() => {
    getMovies();
  }, []);
  console.log(movies);
  // 비동기 작업이 완료되기 전에 렌더링되어 이전 목록을 출력
  // 비동기 작업이 완료되고 새로운 목록이 상태로 저장된 후에 렌더링되어 최신 목록을 출력


  const settings = {
    dots: true,
    arrows: true,
    infinite: true,
    speed: 500,
    slidesToShow: 5,
    slidesToScroll: 1
  };


  return (
    <div>
    <div className="homeTitle">Movies with a rating of 9.0 or higher</div>
    <div style={{ width: "90%", margin: "auto" }}>
      {loading ? (
        <h1>Loading...</h1>
      ) : (
        <Slider {...settings} className="homeSlider">
          {movies.map((movie) => (
            <Movie
              key={movie.id}
              // key: map안에서 component들을 render할 때 구분하기 위해 사용
              id={movie.id}
              // Movie.js에서 id에 따른 movie detail load를 위해 movie 데이터 로드가 되는 Home.js에서 데이터 전달
              coverImg={movie.medium_cover_image}
              title={movie.title}
              year={movie.year}
              summary={movie.summary}
              genres={movie.genres}
            />
          ))}
        </Slider>
      )}
    </div>
    </div>
  );
}

export default Home;
