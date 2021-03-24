import React, {Component} from 'react';
import {Provider} from 'react-redux';
import { BrowserRouter, Route, useHistory } from 'react-router-dom';
import './App.css';
import DashBoardView from './containers/DashBoardView';
import LoginView from './containers/LoginView';
import GameDetailView from './containers/GameDetailView';
import GameListView from './containers/GameListView';
import PredictionsView from './containers/PredictionView';
import {saveState} from './localStorage';
import store from './store';



store.subscribe(() => {
	saveState(store.getState());
});


function App() {
	let history = useHistory();
	return (
		<Provider store={store}>
			<BrowserRouter >
				<Route exact path="/" component={DashBoardView} />
				<Route exact path="/login/" component={LoginView} />
				<Route exact path="/game/:gameId/" component={GameDetailView} />
				<Route exact path="/predictions/" component={PredictionsView} />
				<Route exact path="/games/" component={GameListView} />
			</BrowserRouter>
		</Provider>
	);
}

export default App;
