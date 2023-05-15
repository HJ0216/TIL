import PropTypes from "prop-types";
import styles from "./Button.module.css"

function Button({ text }) {
  //   return (
  //     <button
  //       style={{
  //         backgroundColor: "tomato",
  //       }}
  //     >
  //       {text}
  //     </button>
  //   );

  return <button className={styles.btn}>{text}</button>;
  // React: CSS → javaScript Object(obj안에 btn 존재)
  // class="Button_btn__nsWGq", className 무작위 지정
}

Button.propTypes = {
  text: PropTypes.string.isRequired,
};

export default Button;
