import { Component } from 'react';
import {Dictionary} from '../types/interfaces'
import '../assets/css/gamelist.css';
import GameRow from './GameRow'

interface IProps {
    games: Dictionary<any>[];
    player_winner_id: number;
    isOpponent?: boolean;
}

class GameList extends Component<IProps> {
    l_score: Dictionary<any>[] = [];

    constructor(props: IProps) {
        super(props);
    }

    render() {
        const games = this.props.games;
        const max_items: string = (process.env.REACT_APP_NUM_MAX_GAMES as string);
        return (
            <div>
                {games.slice(0, parseInt(max_items)).map(game=>
                    <GameRow 
                        player_winner_id={this.props.player_winner_id}
                        key={game.id} 
                        game={game}
                    />
                )}
            </div>
        );
    }
}
export default GameList;