import {Component} from 'react'
import {Line} from 'react-chartjs-2';
import '../assets/css/gameschart.css';
import {Dictionary} from '../types/interfaces';
import {range} from '../utils/common';

import {chartColors} from '../utils/constants'



const styleWinner = {
    backgroundColor: chartColors.green,
    borderColor: chartColors.green
}
const styleOpponent = {
    backgroundColor: chartColors.red,
    borderColor: chartColors.red
}

const styleOpponent2 = {
    backgroundColor: chartColors.blue,
    borderColor: chartColors.blue
}

const datasetKeyProvider = () =>{ return Math.random().toString() } 


interface IProps {
    title: string,
    h2hGames: Dictionary<any>[],
    hPlayerData: Dictionary<any>,
    aPlayerData?: Dictionary<any>,
    winnerId: number
}


interface IState {
    hData: number[];
    aData: number[];
    data: Dictionary<any>;
    options: Dictionary<any>;
    showPoints: boolean;
}


class GamesChart extends Component<IProps, IState>{
    constructor(props: IProps){
        super(props);
        this.state = {
            hData: [],
            aData: [],
            data: {},
            options: {},
            showPoints: false
        }
    }

    componentDidMount(){
        this.setPlayerData();
    }
    
    componentDidUpdate(prevProps: IProps, prevState: IState){
        if(this.state.showPoints != prevState.showPoints){
            this.setPlayerData();
        }
    }

    setPlayerData() {
        const games = this.props.h2hGames;
        const max_items = (process.env.REACT_APP_NUM_MAX_GAMES_CHART as string);
        let numMaxGames =  0;
        if(max_items){
            numMaxGames = parseInt(max_items);
            if(numMaxGames > games.length)
                numMaxGames = games.length;
        }
        const winnerId = this.props.winnerId;
        const showPoints = this.state.showPoints;
        let labels: string[] = []
        let i = 1;
        range(numMaxGames).forEach(() => {
            labels.push(i.toString());
            i++;
        });
        const playersData = this.getPlayersData(numMaxGames);
        const hPlayerData = this.props.hPlayerData;
        const aPlayerData = this.props.aPlayerData;
        const h_id = hPlayerData.id;
        const a_id = aPlayerData? aPlayerData.id : 0;
        const onlyOpponent = h_id != winnerId &&  a_id != winnerId;
        const hDataSet = {
            id: this.props.hPlayerData.id,
            label: this.props.hPlayerData.name,
            data: playersData.hData,
            fill: false,
        }
        const aDataSet = {
            id: aPlayerData? aPlayerData.id : 0,
            label: aPlayerData? aPlayerData.name: 'Opponent',
            data: playersData.aData,
            fill: false,
        }
        let datasets = [];
        if (onlyOpponent){
            datasets.push(
                Object.assign({}, hDataSet,
                    styleOpponent
                )
            )
            datasets.push(
                Object.assign({}, aDataSet,
                    styleOpponent2
                )
            )
        }
        else{
            datasets.push(
                Object.assign({}, hDataSet,
                    winnerId == h_id? styleWinner : styleOpponent
                )
            )
            datasets.push(
                Object.assign({}, aDataSet,
                    winnerId == a_id? styleWinner : styleOpponent
                )
            )
        }
        const data = {
            labels: labels,
            datasets: datasets,
        }
        const options = {
            responsive: true,
            title: {
                display: true,
                text: this.props.title
            },
            tooltrips: {
                enabled: true,
                mode: 'point',
                intersect: false
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Games'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: !showPoints? 'Won Sets': 'Won Points'
                    },
                    ticks: {
                        beginAtZero: true,
                        callback: (value: number) => {if (value % 1 === 0) return value;}
                    }
                }]
            },
        }
        this.setState({data: data, options: options});
    }

    getPlayersData(numMaxGames: number): Dictionary<any>{
        const games = this.props.h2hGames;
        const h_id = this.props.hPlayerData.id;
        const showPoints = this.state.showPoints;
        let hData: number[] = []
        let aData: number[] = []        
        games.slice().reverse().slice(0, numMaxGames).forEach(game => {
            if(game.h_id == h_id){
                hData.push((showPoints)? game.h_points : game.h_score);
                aData.push((showPoints)? game.a_points : game.a_score);
            }
            else{
                hData.push((showPoints)? game.a_points : game.a_score);
                aData.push((showPoints)? game.h_points : game.h_score);
            }
        });
        return {hData: hData, aData: aData}
    }

    render(){
        const showPoints = this.state.showPoints;
        return (
            <div className='col chart-container'>
                <div className='col-lg-12'>
                    <Line 
                        data={this.state.data} 
                        options={this.state.options} 
                        datasetKeyProvider={datasetKeyProvider} />
                </div>
                <div className='row rb-container'>
                    <div className='rb'>
                        <input type="radio" id="sets" value="sets" checked={!showPoints} onChange={()=>this.setState({showPoints: !showPoints})}/>
                        <label>Sets</label>
                    </div>
                    <div className='rb'>
                        <input type="radio" id="points" value="points" checked={showPoints} onChange={()=>this.setState({showPoints: !showPoints})} />
                        <label>Points</label>
                    </div>
                </div>
            </div>
        )
    }
}
export default GamesChart;