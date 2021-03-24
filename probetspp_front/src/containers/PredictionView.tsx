import React, { Component } from 'react';
import {connect} from 'react-redux';
import APIRequest from '../api/APIRequests'
import {getLeagues} from '../actions/games'
import { Dictionary } from '../types/interfaces';
import { PredictionStatus } from '../types/common';
import {localTime, getNow, DateFormat} from '../utils/dateTime';
import '../assets/css/predictionview.css';
import MainContainer from './MainContainer';

interface IProps {
    leagues: Dictionary<any>[],
    getLeagues: Function
}

interface IState {
    predictions: Dictionary<any>[];
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
            redirect: null
        }
    }

    componentDidMount(){
        if(this.props.leagues.length == 0){
            this.props.getLeagues();
        }
        this.searchPredictions();
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
        const leagues = this.props.leagues;
        const now = getNow('YYYY-MM-DD');
        return(
            <MainContainer>
            <div className="card mb-8">
                <div className="card-header py-3">
                    <h6 className="m-0 font-weight-bold text-primary">Predictions</h6>
                </div>
                <div className="card-body">
                    <div className='row'>
                        <div className='col-sm-12 col-md-6 col-lg-4'>
                            <label>Status</label>
                            <select className="form-control" id="status" ref={this.statusRef}>
                                <option value={PredictionStatus.PENDING}>PENDING</option>
                                <option value={PredictionStatus.WON}>WON</option>
                                <option value={PredictionStatus.LOST}>LOST</option>
                            </select>
                        </div>
                        <div className='col-sm-12 col-md-6 col-lg-4'>
                            <label>Leagues</label>
                            <select className="form-control" id="leagues" ref={this.leagueRef}>
                                <option value=""></option>
                                {leagues.map(item => {
                                    return <option value={item.id} key={item.id}>{item.name}</option>
                                })}
                            </select>
                        </div>
                        <div className='col-sm-12 col-md-6 col-lg-4'>
                            <label>Date</label>
                            <input 
                                type="date" 
                                className="form-control" 
                                defaultValue={now}
                                id="date"
                                ref={this.dateRef} 
                                max={now}
                            />
                        </div>
                    </div>
                    <div className='btn-container'>
                        <button
                            type="button" 
                            className="btn btn-primary col-sm-12 col-md-4 col-lg-1"
                            onClick={this.searchPredictions.bind(this)}>Search</button>
                    </div>
                    <div className='row table-responsive'>
                        <table id="prediction_table" className='table'>
                            <thead>
                                <tr>
                                    <th>Game</th>
                                    <th>League</th>
                                    <th>Date</th>
                                    <th>Winner</th>
                                    <th>Confidence</th>
                                    <th>Status</th>
                                    <th>Odds</th>
                                    <th></th>
                                </tr>
                            </thead>
                            <tbody>
                                {predictions.map(item => {
                                    const game = item.game;
                                    let odds = game.h_odds;
                                    if (item.player_winner_id == game.away_player_id){
                                        odds = game.a_odds;
                                    }
                                    const url = "/game/" + game.id + "/";
                                    return (
                                        <tr key={item.id}>
                                            <td>{game.name}</td>
                                            <td>{game.league}</td>
                                            <td>{localTime(game.start_dt, DateFormat.dateTime)}</td>
                                            <td>{item.player_winner}</td>
                                            <td>{item.confidence}</td>
                                            <td>{PredictionStatus[item.status]}</td>
                                            <td>{odds}</td>
                                            <td>
                                                <a href={url} target='_blank'>show</a>
                                            </td>
                                        </tr>
                                    )
                                })}
                                
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>  
            </MainContainer>
        )
    }
}
const mapStateToProps = (state: any) => ({
    leagues: state.games.leagues,
})
export default connect(mapStateToProps, { getLeagues })(PredictionsView);
