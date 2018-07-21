import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import store from "redux/configureStore";
import 'index.css';
import App from 'App';

//console.log(store.getState());
//store.dispatch({type:"HIJINI"}); //dev 환경에서 logger 확인

ReactDOM.render(
    <Provider store={store}>
        <App />
    </Provider>,
    document.getElementById("root")
);

// localStorage.setItem('bestName','seojin')