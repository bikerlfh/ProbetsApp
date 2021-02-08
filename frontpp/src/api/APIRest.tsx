/**
 * Copyright (c) 2021, Probetspp.
 * All rights reserved.
 *
 * Maneja las peticiones a la api. Solo se debe acceder mediante
 * métodos de la clase APIRequest
 *
 * @example
 * import APIRest from './lib/APIRest';
 * APIRest.get(URL)
 *  .then((res)=>{
 *      ...
 *  })
 *  .catch((err)=>{
 *      ...
 *  });
 *
 *  Cuando el response retorna un 500 o 401, En "catch" se visualiza el mensaje del response con el componente AlertCustom
 *  siempre que el parámetro showErrorAlert sea true. Para que éste mensaje sea visualizado, en el catch de las vistas
 *  no se debe hacer el Action.pop(), ya que ésto cierra em AlertCustom.
 * @version 1.1
 */

 import {Dictionary} from '../types/interfaces';
 import {APIMethod} from '../types/common'
 import {APIKey, APIUrl, HTTPStatus} from './constants'
 
/**
 * format parameters to stringify
 * @param params
 * @returns {null|string} (JSON.stringify(params))
 */
const formatParameters = (params: Dictionary<any>) => {
    if(params !== null) {
        for (let key of Object.keys(params)) {
            // si el atributo es una instancia de Date
            if (params[key] instanceof Date) {
                // ojo se usa la libreria momentjs (fromat es ProtoType de Date)
                params[key] = params[key].format("YYYY-MM-DD H:mm:ss");
            }
        }
        return JSON.stringify(params);
    }
    return null;
};

export let APIRest = {
    token:'',

    /**
     * send request to server
     * @param url: url
     * @param method: APIMethod (GET, POST, PUT, PATCH, DELETE)
     * @param body: parametros enviados al server
     * @returns {Promise.<TResult>}
     * @constructor
     */
    HttpRequest(url: string, method: APIMethod, body: Dictionary<any> = {}) {
        const config: Dictionary<any> = {
            method: method,
            headers: {
                //'api-key': APIKey,
                'Content-Type': 'application/json',
            },
            //body: formatParameters(body),
            //cache: 'reload'
        };
        /*if(this.token !== null)
            config['headers']['Authorization'] = 'Token ' + this.token;
            */
        url =  APIUrl + url;

        return fetch(url, config)
            .then((response) => {
                /*const status = response.status;
                if(status === HTTPStatus.NOT_FOUND || 
                    status === HTTPStatus.INTERNAL_ERROR)
                    throw {status: status, error:{}};*/
                return response.json()
                }
            )
            .catch((error)=>{
                console.log("ERROR HTTP_REQUEST", error);
                throw error;
            })
    },
    get(url: string) {
        return this.HttpRequest(url, APIMethod.GET);
    },
    post(url: string, params: Dictionary<any>){
        return this.HttpRequest(url, APIMethod.POST, params);
    },
    put(url: string, params: Dictionary<any>){
        return this.HttpRequest(url, APIMethod.PUT, params);
    },
    patch(url: string, params: Dictionary<any>){
        return this.HttpRequest(url, APIMethod.PATCH, params);
    },
};
