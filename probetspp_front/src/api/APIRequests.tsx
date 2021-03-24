/**
 * Copyright (c) 2018, Neubs SAS.
 * All rights reserved.
 *
 * Contiene todos los enpoints de la api.
 * Las cadenas que necesiten parametros de url mas no GET se deben poner
 * de la siguiente forma: (?P<nombreParametro>), ejemplo en la url productoDetalle
 * @version 1.3
 */
import {Dictionary} from '../types/interfaces';
import {APIRest} from './APIRest';


const URLS = {
    /** Authentication **/
    login: 'auth/login/',
    logout: 'auth/logout/',
    me: 'auth/user/',
    dashboard: 'core/dashboard/',
    leagues: 'games/league/',
    games: 'games/',
    gameDetail: 'games/<gameId>/',
    predictions: 'predictions/',
    notifyPrediction: 'predictions/notify/'

};

/**
 * Construye la url de las peticiones a la API
 * @param url: url del objeto URLS
 * @param params: parámetros a pasar
 * @returns url con los parámetros
 */
const makeURL = (url: string, params: Dictionary<any>) =>{
    if(params !== null) {
        // se evaluan los parametros no GET que van en la url
        const paramsRequiredList = url.match(/\<\w*\>/g);
        if(paramsRequiredList !== null && paramsRequiredList.length > 0){
            for(let key of paramsRequiredList){
                let keyFormat = key.replace(/\</g,"").replace(/\>/g,"");
                if(params.hasOwnProperty(keyFormat)) {
                    if(params[keyFormat] !== null)
                        url = url.replace("<" + keyFormat + ">", params[keyFormat]);
                    // se elimina el atributo de los parámetors para que
                    // no se agregen como parametros GET
                    delete params[keyFormat];
                }
            }
        }
        // Se agregan los parametros GET
        for (let key of Object.keys(params)) {
            const value = params[key]
            if(value !== null && value !== undefined)
                url += (url.indexOf('?') === -1 ? "?" : "&") + key + "=" + params[key];
        }
    }
    return url;
};

export default class APIRequest {
    static requestLoginAPI = (username: string, password: string) => {
        return APIRest.post(URLS.login, {"username": username, "password": password});
    };

    static requestLogout = () => {
        return APIRest.post(URLS.logout, {});
    };
    static requestMe = () => {
        return APIRest.get(URLS.me);
    }
    static getDashBoardData = () => {
        return APIRest.get(URLS.dashboard);
    }
    static getLeagues = () => {
        return APIRest.get(URLS.leagues);
    }
    static getGames = (status: any, start_dt: any, league_id: any=null) => {
        const url = makeURL(URLS.games,{
            status: status,
            start_dt: start_dt,
            league_id: league_id,
            order_by: 'start_dt'
        });
        return APIRest.get(url);
    }
    static getGameDetail = (id: number) => {
        const url = makeURL(URLS.gameDetail,{gameId: id});
        return APIRest.get(url);
    }
    static getPredictions = (
        status: any=null, 
        leagueId: any=null,
        start_dt: any=null, 
    ) => {
        let data = {
            status: status,
            league_id: leagueId,
            start_dt: start_dt
        }
        const url = makeURL(URLS.predictions, data);
        return APIRest.get(url);
    }
    static notifyPrediction = (id: number) => {
        return APIRest.post(URLS.notifyPrediction, {prediction_id: id});
    }
}