import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { Route, Link, useHistory } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';
import GameDetail from './containers/GameDetail';
import PredictionsView from './containers/PredictionView';
const  BaseLayout  = () => (
    <div className="container-fluid">
      <Route path="/game/:gameId/" component={GameDetail} />
      <Route path="/predictions/" component={PredictionsView} />
    </div>
  )
  
function App() {
  let history = useHistory();
  return (
    <BrowserRouter>
      <BaseLayout/>
    </BrowserRouter>
  );
}

export default App;
