
import APIRequest from '../api/APIRequests'
import { createMessage, returnErrors } from './messages';

import { GET_GAMES, GET_GAME_DETAIL, GET_LEAGUES } from './types';


// GET LEAGUES
export const getLeagues = () => (dispatch, getState) => {
    APIRequest.getLeagues()
    .then((res) => {
        dispatch({
            type: GET_LEAGUES,
            payload: res,
        });
    })
    .catch((err) => dispatch(returnErrors(err.data, err.status)));
};

// GET GAMES
export const getGames = (status, startDt, leagueId) => (dispatch, getState) => {
    APIRequest.getGames(status, startDt, leagueId)
    .then((res) => {
        dispatch({
            type: GET_GAMES,
            payload: res,
        });
    })
    .catch((err) => dispatch(returnErrors(err.data, err.status)));
};

export const getGame = (id) => (dispatch, getState) => {
    APIRequest.getGame(id)
    .then((res) => {
        dispatch({
            type: GET_GAME_DETAIL,
            payload: res,
        });
    })
    .catch((err) => dispatch(returnErrors(err.data, err.status)));
};

