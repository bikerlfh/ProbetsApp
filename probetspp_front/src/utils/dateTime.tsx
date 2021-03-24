import moment from 'moment';


export const DateFormat = {
    date: 'DD/MM/YYYY',
    dateTime: 'DD/MM/YYYY HH:mm',
    dayMonth: 'DD/MM'
}
export const localTime = (date: string, format?: string) => {
    if(format == undefined){
        format=DateFormat.date;
    }
    return moment(date).locale('es-CO').format(format)
}

export const getNow = (format: string) => {
    return moment().format(format);
}