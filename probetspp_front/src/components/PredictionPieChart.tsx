import {Component} from 'react'
import {Pie} from 'react-chartjs-2';
import { Dictionary } from '../types/interfaces';
import {chartColors} from '../utils/constants'


interface IProps {
	gameData: Dictionary<any>
}
interface IState {
    showToday: boolean;
}

class PredictionPieChart extends Component<IProps, IState>{
	constructor(props: IProps){
		super(props);
		this.state = {
			showToday: true
		}
	}
	getPieProperties(){
		let gameData = this.props.gameData.today_predictions;
		const showToday = this.state.showToday;
		if(!showToday){
			gameData = this.props.gameData.history_predictions;
		}
		const data = {
			labels: ['Won', 'Lost', 'Pending'],
			datasets: [{	
				data: [
					gameData.total_won, 
					gameData.total_lost, 
					gameData.total_pending
				],
				backgroundColor: [					
					chartColors.green,
					chartColors.red,
					chartColors.blue
				],
				borderColor: '#fff',
				borderWidth: 1,
			}],
		}
		const options = {
			responsive: true,
			title: {
				display: true,
				text: showToday? 'Today Predictions': 'History Predictions'
			},
			tooltips: {
				enabled: true,
				callbacks: {
					label: (tooltipItem: any, data: any) => {
						var dataset = data.datasets[tooltipItem.datasetIndex];
						var meta = dataset._meta[Object.keys(dataset._meta)[0]];
						var total = meta.total;
						var value = dataset.data[tooltipItem.index];
						var percentage = parseFloat((value/total*100).toFixed(1));
						return value + ' (' + percentage + '%)';
					},
					title: (tooltipItem: any, data:  any) => {
						return data.labels[tooltipItem[0].index];
					}
				}
			},
		}
		return {data: data, options: options};
	}
	
	render(){
		const {data, options} = this.getPieProperties();
		const showToday = this.state.showToday;
		return(
			<div className='col chart-container'>
				<div className='col-lg-12'>
					<Pie data={data} options={options} />
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
							onChange={()=>this.setState({showToday: !showToday})} />
						<label>Today</label>
					</div>
				</div>
			</div>
		)
	}
}
export default PredictionPieChart