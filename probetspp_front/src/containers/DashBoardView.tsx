import { Component } from 'react';
import {connect} from 'react-redux';
import MainContainer from './MainContainer';
import {getDashboardData} from '../actions/dashboard';
import {getLeagues} from '../actions/games';
import { Dictionary } from '../types/interfaces';
import PredictionPieChart from '../components/PredictionPieChart';
import PredictionBarChart from '../components/PredictionBarChart';


interface IProps {
    data: Dictionary<any>,
    leagues: Dictionary<any>[],
    getDashboardData: Function,
    getLeagues: Function
}



class DashBoardView extends Component<IProps> {
    componentDidMount(){
        console.log('DID MOUNT')
        this.props.getDashboardData()
    }
    render(){
        const data = this.props.data;
        if(data == null){
            return(<></>)
        }
        return(
            <MainContainer>
                <div className='row'>
                    <div className='col-lg-6'>
                        <PredictionPieChart gameData={data}/>
                    </div>
                    <div className='col-lg-6'>
                        <PredictionBarChart gameData={data} />
                    </div>
                </div>
                
            </MainContainer>
        )
    }
}
const mapStateToProps = (state: any) => ({
    data: state.dashboard.data,
    leagues: state.games.leagues
})
export default connect(mapStateToProps, { getDashboardData, getLeagues })(DashBoardView);