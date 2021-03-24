import { returnErrors } from './messages';
import APIRequest from '../api/APIRequests';
import {
    CLEAR_USER,
    USER_LOADED,
    USER_LOADING,
    AUTH_ERROR,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT_SUCCESS
} from './types';

// CHECK TOKEN & LOAD USER
export const loadUser = () => (dispatch, getState) => {
  // User Loading
    dispatch({ type: USER_LOADING });
    APIRequest.requestMe()
    .then((res) => {
        console.log('REQUEST ME');
        console.log(res);
        dispatch({
            type: USER_LOADED,
            payload: Object.assign({}, res),
        });
    })
    .catch((err) => {
        dispatch({
            type: AUTH_ERROR,
        });
        dispatch(returnErrors(err.data, err.status));
    });
};

// LOGIN USER
export const login = (username, password) => (dispatch) => {
    APIRequest.requestLoginAPI(username, password).
    then((res) => {
        dispatch({
            type: LOGIN_SUCCESS,
            payload: {token: res.key},
        });
    })
    .catch((err) => {
        dispatch(returnErrors(err.data, err.status));
        dispatch({
            type: LOGIN_FAIL,
        });
    });
};

// LOGOUT USER
export const logout = () => (dispatch, getState) => {
    APIRequest.requestLogout().
    then((res) => {
        dispatch({ type: CLEAR_USER });
        dispatch({
            type: LOGOUT_SUCCESS,
        });
    })
    .catch((err) => {
        dispatch({ type: CLEAR_USER });
        dispatch({
            type: LOGOUT_SUCCESS,
        });
        dispatch(returnErrors(err.data, err.status));
    });
};
