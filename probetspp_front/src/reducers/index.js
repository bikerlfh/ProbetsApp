import { combineReducers } from 'redux';
import dashboard from './dashboard';
import games from './games';
import auth from './auth';

export default combineReducers({
    dashboard,
    games,
    auth
});