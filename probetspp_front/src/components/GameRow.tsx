import React, { Component } from 'react';
import {Dictionary} from '../types/interfaces';
import {localTime, DateFormat} from '../utils/dateTime';
import '../assets/css/gamerow.css';
import $ from 'jquery';


interface IProps {
    game: Dictionary<any>;
    player_winner_id: number;
}

interface IState {
}

class GameRow extends Component<IProps, IState> {
    l_score: Dictionary<any>[] = [];
    

    constructor(props: IProps) {
        super(props);
        this.state = {
            showLineScore: false
        }
    }
    componentDidMount(){
         const gameId = this.props.game.id;
         $(document).on('click', '#'+ gameId, () =>{
             window.open('/game/'+ gameId + '/');
         })
     }
    renderBadge(){
        const game = this.props.game;
        const winnerId = this.props.player_winner_id;
        if(winnerId == game.winner_id)
            return(
                <span className="badge badge-pill badge-success ml-2">W</span>
            )
        return(
            <span className="badge badge-pill badge-danger ml-2">L</span>
        )
    }
    
    render() {
        const game = this.props.game;
        const lineScore = game.l_score;
        let start_dt = localTime(game.start_dt, DateFormat.dayMonth);
        return (
            <div className='game' id={game.id}>
                <div className='game-row'>
                    <div className='col-2 col-md-2 col-lg-2 game-item'>
                        {start_dt}
                    </div>
                    <div className="col-6 col-md-6 col-lg-5 players game-item">
                        <div>{game.h_name}</div>
                        <div>{game.a_name}</div>
                    </div>
                    <div className="col-3 col-md-3 col-lg-4 score">
                        <table className='line-score-table'>
                            <tbody>
                                <tr className='set-score'>
                                    {lineScore.map((item: any, index: number) =>
                                        <td key={index}>{item.home}</td>
                                    )}
                                    <td className='fscore'>{game.h_score}</td>
                                </tr>
                                <tr className='set-score'>
                                    {lineScore.map((item: any, index: number) =>
                                        <td key={index}>{item.away}</td>
                                    )}
                                    <td className='fscore'>{game.a_score}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div className="col-1 col-md-1 col-lg-1 badge-container">
                        {this.renderBadge()}
                    </div>
                </div>
            </div>
        );
    }
}
export default GameRow;