import { Component } from 'react';
import APIRequest from '../api/APIRequests'
import {Dictionary} from '../types/interfaces';
import {GameStatus, PredictionStatus} from '../types/common'
import {localTime, DateFormat} from '../utils/dateTime';
import MainContainer from './MainContainer';
import GameList from '../components/GameList';
import GamesChart from '../components/GamesChart';
import '../assets/css/gamedetail.css';
import { toast } from 'react-toastify';
import { Console } from 'console';

interface IProps {
  	match: Dictionary<any>
}

interface IState {
    game: Dictionary<any> | null;
    data: Dictionary<any>;
    h2h_games_data: Dictionary<any>
    h2h_games: Dictionary<any>[];
    h_lg_games: Dictionary<any>[];
    a_lg_games: Dictionary<any>[];
    prediction: Dictionary<any>;
    player_winner_id: number;
    home_player: Dictionary<any>;
    away_player: Dictionary<any>;
}

class GameViewDetail extends Component<IProps, IState> {
    constructor(props: IProps) {
      super(props);
      this.state = {
        game: null,
        data: {},
        h2h_games_data: {},
        h2h_games: [],
        h_lg_games: [],
        a_lg_games: [],
        prediction: {},
        player_winner_id: 0,
        home_player: {},
        away_player: {}
      }
    }

	async componentDidMount(){
        const params = this.props.match.params;
        const game = await APIRequest.getGameDetail(params.gameId);
        let prediction = game.prediction || null;
		if(prediction == null){
			prediction = this.getPredictionByDataGame(game);
		}
        const player_winner_id = prediction? prediction.player_winner_id: null;
        const h2h_games_data = game.h2h_games_data;
        this.setState({
			game: game, 
			data: game.data_game,
			h2h_games_data: h2h_games_data,
			h2h_games: h2h_games_data.games,
			h_lg_games: game.h_last_games,
			a_lg_games: game.a_last_games,
			prediction: prediction,
			player_winner_id: player_winner_id,
			home_player: game.home_player,
			away_player: game.away_player,
        });
	}

	getPredictionByDataGame(game: Dictionary<any>){
		const dataGame = game.data_game;
		if(dataGame == null)
			return {noPrediction: true}
		let h_score = dataGame.h_wt_score + dataGame.h_h2h_wt_score;
        h_score += dataGame.h_lg_wt_score + dataGame.h_d_opp_wt_score;

		let a_score = dataGame.a_wt_score + dataGame.a_h2h_wt_score;
        a_score += dataGame.a_lg_wt_score + dataGame.a_d_opp_wt_score;

		let winnerId = game.h_id;
		if(a_score > h_score)
			winnerId = game.a_id;
		return {
			player_winner_id: winnerId,
			confidence: dataGame.confidence,
			noPrediction: true
		}

	}
	notifyPrediction(){
		const prediction = this.state.prediction;
		APIRequest.notifyPrediction(prediction.id)
		.then((res)=>{
			toast.success("🛩 prediction has been notified", {
				position: toast.POSITION.BOTTOM_RIGHT
			});
		}).catch((res) => {
			toast.error("error to invoke ep", {
				position: toast.POSITION.BOTTOM_RIGHT
			});
		});
	}

	render() {
        const game = this.state.game
        if(game == null){
          return(
            <div>NO DATA</div>
          )
        }
        const data = this.state.data || {}
        const h2h_games_data = this.state.h2h_games_data;
        const h2h_games = this.state.h2h_games;
        const h_lg_games = this.state.h_lg_games;
        const a_lg_games = this.state.a_lg_games;
        const prediction = this.state.prediction;
        const player_winner_id = this.state.player_winner_id;

        let player_data = this.state.home_player;
        if(player_winner_id == game.a_id){
            player_data = this.state.away_player;
        }
        let url_game = 'https://www.flashscore.co/partido/'+game.external_id+'/'
        url_game = url_game.replace('g_25_', '');
        
        const h2h_h_player = {
          id: game.h_id,
          name: game.h_name
        }
        const h2h_a_player = {
          id: game.a_id,
          name: game.a_name
        } 
        return(
			<MainContainer>
				<div className='row'>
					<div className='col-sm-12 col-lg-4'>
						<div className="card mb-8">
						<div className="card-header py-3">
							<h6 className="m-0 font-weight-bold text-primary">Game Detail</h6>
						</div>
						<div className="card-body">
							<table className='table table-sm table-borderless '>
								<tbody>
								<tr>
									<td>Game</td>
									<td>
									<b>
										{game.name} 
										{game.status == GameStatus.FINISHED && 
										<b>  ({game.h_score}-{game.a_score})</b>
										}
									</b>
									</td>
								</tr>
								<tr>
									<td>League</td>
									<td><b>{game.league}</b></td>
								</tr>
								<tr>
									<td>Start dt</td>
									<td><b>{localTime(game.start_dt, DateFormat.dateTime)}</b></td>
								</tr>
								<tr>
									<td>Status</td>
									<td><b>{GameStatus[game.status]}</b></td>
								</tr>
								<tr>
									<td>Url</td>
									<td><a href={url_game} target='_blank'>view game</a></td>
								</tr>
								</tbody>
							</table>
						</div>
						</div>
					</div>
					<div className='col-sm-12 col-lg-4'>
						<div className="card mb-8">
							<div className="card-header py-3">
								<h6 className="m-0 font-weight-bold text-primary prediction-card">
									{prediction.noPrediction? 'NO PREDICTION': 'Prediction'}
									{!prediction.noPrediction && 
									<a className='cursor-pointer' onClick={this.notifyPrediction.bind(this)}>Notify</a>}
								</h6>
								
							</div>
							<div className="card-body">
								<table className='table table-sm table-borderless '>
									<tbody>
										<tr>
											<td>Winner</td>
											<td>
											{player_winner_id?	
												<b>
													{player_winner_id == game.h_id? game.h_name: game.a_name}
												</b>
											:
												<b>-----------------</b>
											}
											</td>
										</tr>
										<tr>
											<td>Confidence</td>
											<td>
												<b>{!prediction.noPrediction && prediction.confidence.toFixed(2)}</b>
											</td>
										</tr>
										<tr>
											<td>Status</td>
											<td>
												<b>
													{prediction.noPrediction? 'NOT PREDICTED':PredictionStatus[prediction.status]}
												</b>
											</td>
										</tr>
										<tr>
											<td>Odds</td>
											<td>
											<b>
												{player_winner_id && player_winner_id == game.h_id? game.h_odds: game.a_odds}
											</b>
											</td>
										</tr>
										<tr>
											<td>Predictions</td>
											<td>
												{player_winner_id? 
													<b>
														won: {player_data.w_predictions} / lost: {player_data.l_predictions}
													</b>
												:
													<b>-----------------</b>
												}
											
											</td>
										</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
					
					<div className='col-sm-12 col-lg-4'>
						<div className="card mb-8">
							<div className="card-header py-3">
								<h6 className="m-0 font-weight-bold text-primary">Data score</h6>
							</div>
							<div className="card-body">
								<table className='table table-sm table-borderless'>
									<thead className='thead-dark'>
									<tr>
										<th></th>
										<th>{game.h_name}</th>
										<th>{game.a_name}</th>
									</tr>
									</thead>
									<tbody>
									<tr>
										<td>H2H score</td>
										<td>{data.h_h2h_wt_score && data.h_h2h_wt_score.toFixed(2) || 0}</td>
										<td>{data.a_h2h_wt_score && data.a_h2h_wt_score.toFixed(2) || 0}</td>
									</tr>
									<tr>
										<td>P score</td>
										<td>{data.h_wt_score && data.h_wt_score.toFixed(2) || 0}</td>
										<td>{data.a_wt_score && data.a_wt_score.toFixed(2) || 0}</td>
									</tr>
									<tr>
										<td>LG score</td>
										<td>{data.h_lg_wt_score && data.h_lg_wt_score.toFixed(2) || 0}</td>
										<td>{data.a_lg_wt_score && data.a_lg_wt_score.toFixed(2) || 0}</td>
									</tr>
									<tr>
										<td>DOPP score</td>
										<td>{data.h_d_opp_wt_score && data.h_d_opp_wt_score.toFixed(2) || 0}</td>
										<td>{data.a_d_opp_wt_score && data.a_d_opp_wt_score.toFixed(2) || 0}</td>
									</tr>
									</tbody>
								</table>
							</div>
						</div>
					</div>
				</div>
				<br/>
				
				<div className='row'>
					<div className='col-lg-4'>
						<GamesChart 
							title={h2h_h_player.name + ' Last Games'}
							h2hGames={h_lg_games}
							hPlayerData={h2h_h_player}
							winnerId={player_winner_id}
						/>
					</div>
					<div className='col-lg-4'>
						<GamesChart 
							title='H2H Games'
							h2hGames={h2h_games}
							hPlayerData={h2h_h_player}
							aPlayerData={h2h_a_player}
							winnerId={player_winner_id}
						/>
					</div>
					<div className='col-lg-4'>
						<GamesChart 
							title={h2h_a_player.name + ' Last Games'}
							h2hGames={a_lg_games}
							hPlayerData={h2h_a_player}
							winnerId={player_winner_id}
						/>
					</div>
				</div>
				
				<div className='row'>
					<div className='col-12 col-lg-4'>
						<div className="card mb-8">
							<div className="card-header py-3">
								<h6 className="m-0 font-weight-bold text-primary">{game.h_name} (LG Matches)</h6>
							</div>
							<div className="card-body">
								<GameList 
									games={h_lg_games}
									player_winner_id={game.h_id == player_winner_id? player_winner_id: game.h_id}
									isOpponent={game.h_id == player_winner_id}
								/>
							</div>
						</div>
					</div>
					<div className='col-12 col-lg-4'>
						<div className="card mb-8">
							<div className="card-header py-3">
								<h6 className="m-0 font-weight-bold text-primary">
									H2H - {game.h_name} ({h2h_games_data.home_wins}) vs {game.a_name} ({h2h_games_data.away_wins})
								</h6>
							</div>
							<div className="card-body">
								<GameList 
									games={h2h_games}
									player_winner_id={player_winner_id}
								/>
							</div>
						</div>
					</div>
					<div className='col-12 col-lg-4'>
						<div className="card mb-8">
							<div className="card-header py-3">
								<h6 className="m-0 font-weight-bold text-primary">{game.a_name} (LG Matches)</h6>
							</div>
							<div className="card-body">
								<GameList 
									games={a_lg_games}
									player_winner_id={game.a_id == player_winner_id? player_winner_id: game.a_id}
									isOpponent={game.a_id == player_winner_id}
								/>
							</div>
						</div>
					</div>
				</div>
			</MainContainer>
		)
	}
}

export default GameViewDetail;