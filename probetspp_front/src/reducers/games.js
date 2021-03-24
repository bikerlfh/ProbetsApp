import { GET_GAMES, GET_GAME_DETAIL, GET_LEAGUES } from '../actions/types.js';

const initialState = {
    leagues: []
};

export default function (state = initialState, action) {
    switch (action.type) {
        case GET_LEAGUES:
            return {
            ...state,
            leagues: action.payload,
            };
        case GET_GAMES:
            return {
            ...state,
            games: action.payload,
            };
        case GET_GAME_DETAIL:
            return {
                ...state,
                game: action.payload,
                };
        default:
            return state;
        }
    }