import { CREATE_MESSAGE, GET_ERRORS, LOGOUT_SUCCESS } from './types';
import { toast } from 'react-toastify';

export const createMessage = (msg) => {
    return {
        type: CREATE_MESSAGE,
        payload: msg,
    };
};

export const returnErrors = (msg, status) => (dispatch, getState) => {
    if(status==401){
        dispatch({
            type: LOGOUT_SUCCESS,
        });
    }
    try{
        toast.error(msg.errors[0].message, {
            position: toast.POSITION.BOTTOM_RIGHT
        });
    }catch{}
    return {
        type: GET_ERRORS,
        payload: { msg, status },
    };
};