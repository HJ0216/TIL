import { BrowserRouter, Route, Routes } from "react-router-dom";
import Detail from "./routes/Detail";
import Home from "./routes/Home";

const MovieApp = () => {
    return (
        <BrowserRouter>
            <Routes>
            {/* Switch: 한 번에 하나의 컴포넌트만 랜더링 */}
                <Route path="/movie/:id" element={<Detail />} />
                {/* :id: React Router-동적 URL(URL에 변수 사용) 지원,  */}
                <Route path="/" element={<Home />} />
            </Routes>
        </BrowserRouter>
    );
};

export default MovieApp;
