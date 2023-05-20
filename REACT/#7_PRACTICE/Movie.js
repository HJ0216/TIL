import PropTypes from "prop-types";
import { Link } from "react-router-dom";
// a tag와 달리 브라우저 새로고침 없이도 유저를 다른 페이지로 이동시켜주는 컴포넌트
import styles from "./Movie.module.css";

function Movie({ id, coverImg, title, year, summary, genres }) {
  return (
    <div>
      <img src={coverImg} alt={title} />
      <div>
        <h2>
          <Link to={`/movie/${id}`}>{title}</Link>
          {/* ${}: ``안에서 변수 선언 */}
        </h2>
        <h3 className={styles.movie__year}>{year}</h3>
        <p>{summary.length > 235 ? `${summary.slice(0, 235)}...` : summary}</p>
        <ul>
          {genres.map((g, index) => (
            <li key={index}>{g}</li>
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
