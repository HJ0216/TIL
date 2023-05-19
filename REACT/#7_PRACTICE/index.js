import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './style.css';
import CoinTracker from './CoinTracker';
import MovieApp from './MovieApp';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* <App /> */}
    {/* <CoinTracker /> */}
    <MovieApp />
  </React.StrictMode>
);
