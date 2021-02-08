import React, { Component } from 'react';
import APIRequest from '../api/APIRequests'
import { Dictionary } from '../types/interfaces';
import { PredictionStatus } from '../types/common';
import {localTime} from '../utils/dateTime';


interface IProps {
    gameId: number | null,
    startDt: Date | null
}

interface IState {
  predictions: Dictionary<any>[];
  leagues: Dictionary<any>[];
  redirect: string | null;
}

class PredictionsView extends Component<IProps, IState> {
    statusRef: React.RefObject<HTMLSelectElement>;
    leagueRef: React.RefObject<HTMLSelectElement>;
    dateRef: React.RefObject<HTMLInputElement>;
    

    constructor(props: IProps) {
        super(props);
        this.statusRef = React.createRef();
        this.dateRef = React.createRef();
        this.leagueRef = React.createRef()
        this.state = {
            predictions: [],
            leagues: [],
            redirect: null
        }
      }

      async componentDidMount(){
        const leagues = await APIRequest.getLeagues();
        this.setState({leagues: leagues})
      }
      async searchPredictions(){
        const status_ = this.statusRef.current?.value || null
        const league_ = this.leagueRef.current?.value || null
        const date_ = this.dateRef.current?.value || null
        
        const predictions = await APIRequest.getPredictions(
            status_,league_,date_
        );
        this.setState({predictions: predictions})
      }
      
      render() {
        const predictions = this.state.predictions;
        const leagues = this.state.leagues;
        return(
            <div className="card shadow mb-8">
                <div className="card-header py-3">
                    <h6 className="m-0 font-weight-bold text-primary">Predictions</h6>
                </div>
                <div className="card-body">
                    <div className="form-group row">
                        <label className="col-sm-1 col-form-label">Status</label>
                        <div className="col-sm-2">
                            <select className="form-control" id="status" ref={this.statusRef}>
                                <option></option>
                                <option value={PredictionStatus.WON}>Won</option>
                                <option value={PredictionStatus.LOST}>Lost</option>
                                <option value={PredictionStatus.PENDING}>Pending</option>
                            </select>
                        </div>
                        <label className="col-sm-1 col-form-label">Leagues</label>
                        <div className="col-sm-2">
                            <select className="form-control" id="leagues" ref={this.leagueRef}>
                                <option value=""></option>
                                {leagues.map(item => {
                                    return <option value={item.id} key={item.id}>{item.name}</option>
                                })}
                            </select>
                        </div>
                        <label className="col-sm-1 col-form-label">Date</label>
                        <div className="col-sm-2">
                            <input 
                                type="date" 
                                className="form-control" 
                                id="date"
                                ref={this.dateRef} 
                                max={Date.now().toLocaleString('es-CO')}
                            />
                        </div>
                        <button 
                            type="button" 
                            className="btn btn-primary" 
                            onClick={this.searchPredictions.bind(this)}>Search</button>
                    </div>
                    
                    <table id="prediction_table" className='table'>
                        <thead>
                            <tr>
                                <th>Game</th>
                                <th>League</th>
                                <th>Start date</th>
                                <th>Winner Prediction</th>
                                <th>Confidence</th>
                                <th>Status</th>
                                <th>Odds</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            {predictions.map(item => {
                                const game = item.game;
                                const start_dt = new Date(game.start_dt);
                                let odds = game.h_odds;
                                if (item.player_winner_id == game.away_player_id){
                                    odds = game.a_odds;
                                }
                                const url = "/game/" + game.id + "/";
                                return (
                                    <tr key={item.id}>
                                        <td>{game.name}</td>
                                        <td>{game.league}</td>
                                        <td>{localTime(start_dt)}</td>
                                        <td>{item.player_winner}</td>
                                        <td>{item.confidence}</td>
                                        <td>{PredictionStatus[item.status]}</td>
                                        <td>{odds}</td>
                                        <td>
                                            <a href={url} target='blank'>show</a>
                                        </td>
                                    </tr>
                                )
                            })}
                            
                        </tbody>
                    </table>
                </div>
            </div>  
        )
    }
}
export default PredictionsView;
