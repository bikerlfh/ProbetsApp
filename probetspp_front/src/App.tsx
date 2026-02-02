import {Provider} from 'react-redux';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
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
	return (
		<Provider store={store}>
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<DashBoardView />} />
					<Route path="/login/" element={<LoginView />} />
					<Route path="/game/:gameId/" element={<GameDetailView />} />
					<Route path="/predictions/" element={<PredictionsView />} />
					<Route path="/games/" element={<GameListView />} />
				</Routes>
			</BrowserRouter>
		</Provider>
	);
}

export default App;
