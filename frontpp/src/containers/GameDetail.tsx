import { Component } from 'react';
import APIRequest from '../api/APIRequests'
import {Dictionary} from '../types/interfaces';
import {GameStatus, PredictionStatus} from '../types/common'
import {localTime} from '../utils/dateTime';

import GameList from '../components/GameList';


interface IProps {
  match: Dictionary<any>
}

interface IState {
  game: Dictionary<any>;
  data: Dictionary<any>;
  h2h_games_data: Dictionary<any>
  h2h_games: Dictionary<any>[];
  h_lg_games: Dictionary<any>[];
  a_lg_games: Dictionary<any>[];
  prediction: Dictionary<any>;
  player_winner_id: number;
}

class GameDetail extends Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);
        this.state = {
          game: {},
          data: {},
          h2h_games_data: {},
          h2h_games: [],
          h_lg_games: [],
          a_lg_games: [],
          prediction: {},
          player_winner_id: 0
        }
      }

      async componentDidMount(){
        const params = this.props.match.params;
        const game = await APIRequest.getGameDetail(params.gameId);
        const prediction = game.prediction;
        const player_winner_id = prediction.player_winner_id;
        const h2h_games_data = game.h2h_games_data;
        this.setState({
          game: game, 
          data: game.data_game,
          h2h_games_data: h2h_games_data,
          h2h_games: h2h_games_data.games,
          h_lg_games: game.h_last_games,
          a_lg_games: game.a_last_games,
          prediction: prediction,
          player_winner_id: player_winner_id
        });
      }

      render() {
        const game = this.state.game
        const data = this.state.data
        const h2h_games_data = this.state.h2h_games_data;
        const h2h_games = this.state.h2h_games;
        const h_lg_games = this.state.h_lg_games;
        const a_lg_games = this.state.a_lg_games;
        const start_dt = new Date(game.start_dt);
        const prediction = this.state.prediction;
        const player_winner_id = this.state.player_winner_id;
        if (game != null)
          return(
            <div>
              <div className='row'>
                <div className='col-sm-12 col-lg-4'>
                  <div className="card shadow mb-8">
                    <div className="card-header py-3">
                        <h6 className="m-0 font-weight-bold text-primary">Game Detail</h6>
                    </div>
                    <div className="card-body">
                        <table className='table table-sm table-borderless '>
                          <tbody>
                            <tr>
                              <td>Game</td>
                              <td><b>{game.name}</b></td>
                            </tr>
                            <tr>
                              <td>League</td>
                              <td><b>{game.league}</b></td>
                            </tr>
                            <tr>
                              <td>Start dt</td>
                              <td><b>{localTime(start_dt)}</b></td>
                            </tr>
                            <tr>
                              <td>Status</td>
                              <td><b>{GameStatus[game.status]}</b></td>
                            </tr>
                          </tbody>
                        </table>
                    </div>
                  </div>
                </div>
                <div className='col-sm-12 col-lg-3'>
                  <div className="card shadow mb-8">
                    <div className="card-header py-3">
                        <h6 className="m-0 font-weight-bold text-primary">Prediction</h6>
                    </div>
                    <div className="card-body">
                        <table className='table table-sm table-borderless '>
                          <tbody>
                            <tr>
                              <td>Winner</td>
                              <td>
                                <b>
                                  {player_winner_id == game.h_id? game.h_name: game.a_name}
                                </b>
                              </td>
                            </tr>
                            <tr>
                              <td>Confidence</td>
                              <td><b>{prediction.confidence}</b></td>
                            </tr>
                            <tr>
                              <td>Status</td>
                              <td><b>{PredictionStatus[prediction.status]}</b></td>
                            </tr>
                            <tr>
                              <td>Odds</td>
                              <td>
                                <b>
                                  {player_winner_id == game.h_id? game.h_odds: game.a_odds}
                                </b>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                    </div>
                  </div>
                </div>
                <div className='col'>
                  <div className="card shadow mb-8">
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
                              <td>{data.h_h2h_wt_score}</td>
                              <td>{data.a_h2h_wt_score}</td>
                            </tr>
                            <tr>
                              <td>P score</td>
                              <td>{data.h_wt_score}</td>
                              <td>{data.a_wt_score}</td>
                            </tr>
                            <tr>
                              <td>LG score</td>
                              <td>{data.h_lg_wt_score}</td>
                              <td>{data.a_lg_wt_score}</td>
                            </tr>
                            <tr>
                              <td>DOPP score</td>
                              <td>{data.h_d_opp_wt_score}</td>
                              <td>{data.a_d_opp_wt_score}</td>
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
                  <div className="card shadow mb-8">
                    <div className="card-header py-3">
                        <h6 className="m-0 font-weight-bold text-primary">{game.h_name} (LG Matches)</h6>
                    </div>
                    <div className="card-body">
                        <GameList 
                          games={h_lg_games}
                          player_winner_id={player_winner_id}
                          />
                    </div>
                  </div>
                </div>
                <div className='col-lg-4'>
                  <div className="card shadow mb-8">
                    <div className="card-header py-3">
                        <h6 className="m-0 font-weight-bold text-primary">
                          H2H Matches - {game.h_name} ({h2h_games_data.home_wins}) vs {game.a_name} ({h2h_games_data.away_wins})
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
                <div className='col-lg-4'>
                  <div className="card shadow mb-8">
                    <div className="card-header py-3">
                        <h6 className="m-0 font-weight-bold text-primary">{game.a_name} (LG Matches)</h6>
                    </div>
                    <div className="card-body">
                        <GameList 
                          games={a_lg_games}
                          player_winner_id={player_winner_id}
                          />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )
        return(
          <div>NO DATA</div>
        )
      }
}

export default GameDetail;
