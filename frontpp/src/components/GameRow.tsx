import React, { Component } from 'react';
import {Dictionary} from '../types/interfaces'
import './GameRow.css';

interface IProps {
    game: Dictionary<any>;
    player_winner_id: number;
    isOpponent: boolean;
}

interface IState {
    l_score: Dictionary<any>[]
}

class GameRow extends Component<IProps, IState> {
    l_score: Dictionary<any>[] = [];

    constructor(props: IProps) {
        super(props);
        this.state = {
            l_score: []
        }
    }
    componentDidMount(){
       this.setState({
           l_score: this.props.game.l_score
        });
    }

    render() {
        const game = this.props.game;
        const player_winner_id = this.props.player_winner_id;
        let class_name = 'col-sm-12 game row won'
        if (game.winner_id != player_winner_id){
            class_name = 'col-sm-12 game row lost'
        }
        let start_dt = game.start_dt.replace(/(\T\d+:\d+:\d+\Z)/g,"");
        return (
            <div className={class_name}>
                <div className="center col-sm-4 col-lg-4">{start_dt}</div>
                <div className="center col-sm-7 col-lg-7">
                    <div>{game.h_name}</div>
                    <div>{game.a_name}</div>
                </div>
                <div className="center col-sm-1 col-lg-1">
                    <div>{game.h_score}</div>
                    <div>{game.a_score}</div>
                </div>
            </div>
        );
    }
}
    


export default GameRow;