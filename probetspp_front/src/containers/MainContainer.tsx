import { Component } from 'react';
import {connect} from 'react-redux';
import { Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {logout} from '../actions/auth';
import {appendScript} from '../utils/appendScript'

class MainContainer extends Component<any, any> {
    componentDidMount(){
        appendScript(process.env.PUBLIC_URL + '/assets/js/sb-admin-2.min.js')
    }
    render(){
        const auth = this.props.auth;
        
        if(!auth.isAuthenticated){
            return(
                <Navigate to='/login/' replace />
            )
        }
        let username = 'anonymous';
        if(auth.user !== null){
            username = auth.user.username;
        }
        return(
            <div id="wrapper">
                <ul className="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion toggled" id="accordionSidebar">
                    <a className="sidebar-brand d-flex align-items-center justify-content-center" href="/">
                        <div className="sidebar-brand-text mx-3">ProbetsPP</div>
                    </a>
                    <hr className="sidebar-divider my-0"/>
                    <li className="nav-item">
                        <a className="nav-link" href="/">
                            <i className="fas fa-fw fa-tachometer-alt"></i>
                            <span>Dashboard</span></a>
                    </li>
                    <hr className="sidebar-divider"/>
                    <li className="nav-item">
                        <a className="nav-link" href="/predictions/">
                            <i className="fas fa-fw fa-trophy"></i>
                            <span>Predictions</span></a>
                    </li>
                    <hr className="sidebar-divider"/>
                    <li className="nav-item">
                        <a className="nav-link" href="/games/">
                            <i className="fas fa-fw fa-gamepad"></i>
                            <span>Games</span></a>
                    </li>
                    <hr className="sidebar-divider d-none d-md-block"/>
                </ul>
                <div id="content-wrapper" className="d-flex flex-column">
                    <div id="content">
                        <nav className="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top">
                            <button id="sidebarToggleTop" className="btn btn-link d-md-none rounded-circle mr-3">
                                <i className="fa fa-bars"></i>
                            </button>
                            <ul className="navbar-nav ml-auto">
                                <div className="topbar-divider d-none d-sm-block"></div>
                                <li className="nav-item dropdown no-arrow">
                                    <a className="nav-link dropdown-toggle" href="#" id="userDropdown" role="button"
                                        data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <span className="mr-2 d-none d-lg-inline text-gray-600 small">
                                            {username}
                                        </span>
                                        <img className="img-profile rounded-circle"
                                            src={process.env.PUBLIC_URL+'/assets/img/undraw_profile.svg'}/>
                                    </a>
                                    <div className="dropdown-menu dropdown-menu-right shadow animated--grow-in"
                                        aria-labelledby="userDropdown">
                                        <a className="dropdown-item" href="#">
                                            <i className="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                                            Profile
                                        </a>
                                        <a className="dropdown-item" href="#">
                                            <i className="fas fa-cogs fa-sm fa-fw mr-2 text-gray-400"></i>
                                            Settings
                                        </a>
                                        <a className="dropdown-item" href="#">
                                            <i className="fas fa-list fa-sm fa-fw mr-2 text-gray-400"></i>
                                            Activity Log
                                        </a>
                                        <div className="dropdown-divider"></div>
                                        <a className="dropdown-item cursor-pointer" onClick={this.props.logout.bind(this)}>
                                            <i className="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                                            Logout
                                        </a>
                                    </div>
                                </li>
                            </ul>
                        </nav>
                        <div className='container-fluid'>
                            {this.props.children}
                        </div>
                    </div>
                    <footer className="sticky-footer bg-white">
                        <div className="container my-auto">
                            <div className="copyright text-center my-auto">
                                <span>Copyright &copy; Probets 2021</span>
                            </div>
                        </div>
                    </footer>
                </div>
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
export default connect(mapStateToProps, {logout})(MainContainer);