import { Component} from 'react';
import { Navigate } from 'react-router-dom';
import {connect} from 'react-redux';
import { login, loadUser } from '../actions/auth';
import '../assets/css/login.css';
import $ from "jquery";
import { ToastContainer } from 'react-toastify';
import { Dictionary } from '../types/interfaces';
interface IProps {
	login: Function,
	loadUser: Function,
	auth: Dictionary<any>;
}

interface IState {
}

class Login extends Component<IProps, IState> {
	componentDidUpdate(prevProps: IProps, prevState: IState){
		if(prevProps.auth.token !== this.props.auth.token){
			this.props.loadUser();
		}
	}

	handleLogin(e: any){
		e.preventDefault();
		const username = $('#inputEmail').val() as string;
		const password = $('#inputPassword').val() as string;
		this.props.login(username, password);
	}

	render(){
		const auth = this.props.auth;
		if (auth.isAuthenticated) {
			return <Navigate to="/predictions/" replace />;
		}
		return(
			<div className='login-container'>
				<form className="form-signin" onSubmit={e => this.handleLogin(e)}>
					<div className="text-center mb-4">
						<img className="mb-4" src={process.env.PUBLIC_URL+'/assets/img/undraw_profile_2.svg'} alt="" width="72" height="72"/>
					</div>
					<div className="form-label-group">
						<input 
							type="text" 
							id="inputEmail" 
							className="form-control" 
							placeholder="Username" 
							required autoFocus
						/>
						<label htmlFor="inputEmail">Username</label>
					</div>
					<div className="form-label-group">
						<input type="password" id="inputPassword" className="form-control" placeholder="Password" required/>
						<label htmlFor="inputPassword">Password</label>
					</div>
					<div className="checkbox mb-3">
						<label>
						<input type="checkbox" value="remember-me"/> Remember me
						</label>
					</div>
					<button className="btn btn-lg btn-success btn-block" type="submit">Sign in</button>
					<p className="mt-5 mb-3 text-muted text-center">&copy; Probets 2021</p>
				</form>
				<ToastContainer
					position="top-right"
					autoClose={5000}
					hideProgressBar={false}
					newestOnTop={false}
					closeOnClick
					rtl={false}
					pauseOnFocusLoss
					draggable
					pauseOnHover/>
			</div>
		)
	}
}
const mapStateToProps = (state: any) => ({
    auth: state.auth,
})
export default connect(mapStateToProps, { login, loadUser })(Login);