import { GET_DASHBOARD } from '../actions/types.js';

const initialState = {
    data: null
};

export default function (state = initialState, action) {
    switch (action.type) {
        case GET_DASHBOARD:
            return {
            ...state,
            data: action.payload,
            };
        default:
            return state;
        }
    }