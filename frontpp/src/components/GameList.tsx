import React, { Component } from 'react';
import { setFlagsFromString } from 'v8';
import {Dictionary} from '../types/interfaces'
import './GameList.css';
import GameRow from './GameRow'

interface IProps {
    games: Dictionary<any>[];
    player_winner_id: number;
}

interface IState {
    isOpponent: boolean
}

class GameList extends Component<IProps, IState> {
    l_score: Dictionary<any>[] = [];

    constructor(props: IProps) {
        super(props);
        this.state = {
            isOpponent: false
        }
    }

    componentDidMount(){
        const winner_id = this.props.player_winner_id;
        const games = this.props.games;
        this.props.games.forEach(game => {
            if(winner_id != game.h_id && winner_id != game.a_id){
                this.setState({isOpponent: true});
            }
        })
    }

    render() {
        const games = this.props.games;
      
        return (
            <div className="col-sm-12">
                {games.map(game=>
                    <GameRow 
                        player_winner_id={this.props.player_winner_id}
                        key={game.id} 
                        game={game}
                        isOpponent={this.state.isOpponent}
                    />
                )}
            </div>
        );
    }
}
export default GameList;