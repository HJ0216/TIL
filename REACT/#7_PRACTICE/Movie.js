import PropTypes from "prop-types";
import { Link } from "react-router-dom";
// a tag와 달리 브라우저 새로고침 없이도 유저를 다른 페이지로 이동시켜주는 컴포넌트
import styles from "./Movie.module.css";

function Movie({ id, coverImg, title, year, summary, genres }) {

  return (
    <div>
      <img className={styles.movieImg} src={coverImg} alt={title} />
      <div className={styles.movieContent}>
        <div className={styles.movieTitle}>
          <Link className={styles.movieTitleLink} to={`/movie/${id}`}>{title}</Link>
          {/* ${}: ``안에서 변수 선언 */}
        </div>
        <div className={styles.movieYear}>{year}</div>
        <br/>
        <p className={styles.movieSummaryTitle}>Summary</p>
        <p className={styles.movieSummary}>{summary.length > 80 ? `${summary.slice(0, 80)}...` : summary}</p>
        <br/>
        <ul className={styles.movieGenresUl}>
          {genres.slice(0, 2).map((g, index) => (
            <li className={styles.movieGenresLi} key={index}>#{g}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

Movie.propTypes = {
  id: PropTypes.number.isRequired,
  coverImg: PropTypes.string.isRequired,
  title: PropTypes.string.isRequired,
  summary: PropTypes.string.isRequired,
  genres: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default Movie;

// 페이지 이동을 위한 npm 설치: npm install react-router-dom
