import {Component} from 'react'
import {connect} from 'react-redux';
import {Bar} from 'react-chartjs-2';
import {getLeagues} from '../actions/games';
import { Dictionary } from '../types/interfaces';
import {chartColors} from '../utils/constants'
import { GameStatus, PredictionStatus } from '../types/common';


interface IProps {
    leagues: Dictionary<any>[];
    gameData: Dictionary<any>;
    getLeagues: Function
}
interface IState {
    showToday: boolean;
    options: Dictionary<any>;
    data: Dictionary<any>;
}

class PredictionBarChart extends Component<IProps, IState>{
	constructor(props: IProps){
        super(props);
        this.state = {
            showToday: true,
            data: {},
            options: {}
        }
    }
    componentDidMount(){
        if(this.props.leagues.length == 0){
            this.props.getLeagues();
        }else{
            this.getBarProperties();
        }
    }
    
    componentDidUpdate(prevProps: IProps, prevState: IState){
        if(this.state.showToday != prevState.showToday){
            this.getBarProperties();
        }
    }

    filterValue(obj: Dictionary<any>[], value: number, status: number) {
        for(let i=0; i<obj.length; i++){
            let item = obj[i];
            if(item.status == status && item.league_id==value){
                return item;
            }
        }
    }

    getBarProperties(){
        const leagues = this.props.leagues;
		const showToday = this.state.showToday;
        let gameData = this.props.gameData.today_predictions;
		if(!showToday){
			gameData = this.props.gameData.history_predictions;
		}
        let labels: string[] = [];
        let won_data: number[] = [];
        let lost_data: number[] = [];
        leagues.forEach(item => {
            const won = this.filterValue(
                gameData.predictions, 
                item.id,
                PredictionStatus.WON
            );
            const lost = this.filterValue(
                gameData.predictions, 
                item.id,
                PredictionStatus.LOST
            );
            if(won != undefined || lost != undefined){
                labels.push(item.name);
                if(won != undefined){
                    won_data.push(won.count);
                }
                else{
                    won_data.push(0);
                }
                if(lost != undefined){
                    lost_data.push(lost.count);
                }
                else{
                    lost_data.push(0);
                }
            }
        });
		const data = {
            labels: labels,
            datasets: [
                {
                    label: '# won games',
                    data: won_data,
                    backgroundColor: chartColors.green,
                },
                {
                    label: '# lost games',
                    data: lost_data,
                    backgroundColor: 'rgb(255, 99, 132)',
                },
            ],
        }
		const options = {
			responsive: true,
			title: {
				display: true,
				text: showToday? 'Today Predictions': 'History Predictions'
			},
			scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                        callback: (value: number) => {if (value % 1 === 0) return value;}
                    },
                }],
            }
		}
		this.setState({data: data, options: options});
	}

	render(){
        const showToday = this.state.showToday;
        const {data, options} = this.state;
		return(
            <div className='col chart-container'>
				<div className='col-lg-12'>
                    <Bar data={data} options={options} />
				</div>
				<div className='row rb-container'>
					<div className='rb'>
						<input 
							type="radio" id="history" 
							value="History" checked={!showToday} 
							onChange={()=>this.setState({showToday: !showToday})}/>
						<label>History</label>
					</div>
					<div className='rb'>
						<input 
							type="radio" id="today" 
							value="Today" checked={showToday}
                            onChange={()=>this.setState({showToday: !showToday})}
							 />
						<label>Today</label>
					</div>
				</div>
			</div>
		)
	}
}

const mapStateToProps = (state: any) => ({
    leagues: state.games.leagues
})
export default connect(mapStateToProps, {getLeagues})(PredictionBarChart)