import { CREATE_MESSAGE, GET_ERRORS } from './types';
import { toast } from 'react-toastify';

// CREATE MESSAGE
export const createMessage = (msg) => {
    return {
        type: CREATE_MESSAGE,
        payload: msg,
    };
};

// RETURN ERRORS
export const returnErrors = (msg, status) => {
    toast.error(msg.errors[0].message, {
        position: toast.POSITION.BOTTOM_RIGHT
    });
    return {
        type: GET_ERRORS,
        payload: { msg, status },
    };
};