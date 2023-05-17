import React, { useEffect, useState } from "react";

const CoinTracker = () => {
  const [loading, setLoading] = useState(true);
  const [coins, setCoins] = useState([]);
  // 기본값으로 빈 배열을 넘겨줄 경우, length = 0
  // 만일 기본값을 설정하지 않을 경우, coins = undefined ▶ length() 사용 시, error
  const [amount, setAmount] = useState();

  useEffect(() => {
    fetch("https://api.coinpaprika.com/v1/tickers")
      .then((response) => response.json())
      .then((json) => {
        setCoins(json);
        setLoading(false);
      });
  }, []);

  const onChange = (event) => {
    setAmount(event.target.value);
  };

  return (
    <div>
      <h1>The Coins{loading ? "" : `(${coins.length})`}</h1>
      {loading ? (
        <strong>Loading...</strong>
      ) : (
        <div>
          Amount(USD):&nbsp;
          <input value={amount} onChange={onChange} />
          <br />
          To be Exchanged: &nbsp;
          <select>
            {coins.map((coin) => (
              <option key={coin.id}>
                {coin.name} ({coin.symbol}): {coin.quotes.USD.price / amount}
              </option>
            ))}
          </select>
          <br />
          Standard: &nbsp;
          <select>
            {coins.map((coin) => (
              <option key={coin.id}>
                {coin.name} ({coin.symbol}): $ {coin.quotes.USD.price} USD
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
};

export default CoinTracker;
