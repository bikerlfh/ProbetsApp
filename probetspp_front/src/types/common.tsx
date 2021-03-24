export enum APIMethod {
    GET = 'GET',
    POST = 'POST',
    PUT = 'PUT',
    PATCH = 'PATCH',
    DELETE = 'DELETE'
}

export enum GameStatus{
    DEFAULT = -1,
    SCHEDULED = 1,
    IN_LIVE = 2,
    FINISHED = 3,
    CANCELED = 4,
    ABANDONMENT = 5,
    DISCONTINUED = 6,
    POSTPONED = 7,
}

export enum PredictionStatus{
    WON = 1,
    LOST = 2,
    PENDING = 0,
    CANCELED = -1,
    ERROR_CORE = -2
}