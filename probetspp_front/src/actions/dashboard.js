
import APIRequest from '../api/APIRequests'
import { createMessage, returnErrors } from './messages';

import { GET_DASHBOARD } from './types';


// GET DASCHBOARD
export const getDashboardData = () => (dispatch, getState) => {
    APIRequest.getDashBoardData()
    .then((res) => {
        dispatch({
            type: GET_DASHBOARD,
            payload: res,
        });
    })
    .catch((err) => dispatch(returnErrors(err.data, err.status)));
};
