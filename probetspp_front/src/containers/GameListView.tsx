import React, { Component } from 'react';
import {connect} from 'react-redux';
import { getGames, getLeagues } from '../actions/games';
import { Dictionary } from '../types/interfaces';
import { GameStatus } from '../types/common';
import {localTime, getNow, DateFormat} from '../utils/dateTime';
import '../assets/css/predictionview.css';
import MainContainer from './MainContainer';


interface IProps {
    games: Dictionary<any>[];
    leagues: Dictionary<any>[];
    getGames: Function;
    getLeagues: Function;
}

interface IState {
    leagues: Dictionary<any>[];
    redirect: string | null;
}

class GameListView extends Component<IProps, IState> {
    statusRef: React.RefObject<HTMLSelectElement>;
    leagueRef: React.RefObject<HTMLSelectElement>;
    dateRef: React.RefObject<HTMLInputElement>;
    

    constructor(props: IProps) {
        super(props);
        this.statusRef = React.createRef();
        this.dateRef = React.createRef();
        this.leagueRef = React.createRef()
        this.state = {
            leagues: [],
            redirect: null
        }
      }

    componentDidMount(){
        if(this.props.leagues.length == 0){
            this.props.getLeagues();
        }
    }
    searchPredictions(){
        const status_ = this.statusRef.current?.value || null
        const league_ = this.leagueRef.current?.value || null
        const date_ = this.dateRef.current?.value || null
        this.props.getGames(status_, date_, league_);
    }
      
      render() {
        const games = this.props.games || [];
        const leagues = this.props.leagues;
        const now = getNow('YYYY-MM-DD');
        return(
            <MainContainer>
                <div className="card mb-8">
                    <div className="card-header py-3">
                        <h6 className="m-0 font-weight-bold text-primary">Games</h6>
                    </div>
                    <div className="card-body">
                        <div className='row'>
                            <div className='col-sm-12 col-md-6 col-lg-4'>
                                <label>Status</label>
                                <select className="form-control" id="status" ref={this.statusRef}>
                                    <option value={GameStatus.SCHEDULED}>SCHEDULED</option>
                                    <option value={GameStatus.FINISHED}>FINISHED</option>
                                    <option value={GameStatus.IN_LIVE}>IN_LIVE</option>
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
                                        <th>Status</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {games.map(game => {
                                        const url = "/game/" + game.id + "/";
                                        return (
                                            <tr key={game.id}>
                                                <td>{game.name}</td>
                                                <td>{game.league}</td>
                                                <td>{localTime(game.start_dt, DateFormat.dateTime)}</td>
                                                <td>{GameStatus[game.status]}</td>
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
    games: state.games.games,
    leagues: state.games.leagues
})
export default connect(mapStateToProps, {getGames, getLeagues})(GameListView as any);
