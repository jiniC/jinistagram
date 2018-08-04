import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from "react-redux";
import { ConnectedRouter } from "react-router-redux";
import store, { history } from "redux/configureStore";
import 'index.css';
import App from 'App';
import "ReactotronConfig";
import I18n from "redux-i18n";
import {translations} from "translations";

//console.log(store.getState());
//store.dispatch({type:"HIJINI"}); //dev 환경에서 logger 확인

ReactDOM.render(
	<Provider store={store}>
		<ConnectedRouter history={history}>
			<I18n translations={translations} initialLang="en" fallbackLang="en">
				<App />
			</I18n>
		</ConnectedRouter>
	</Provider>,
	document.getElementById('root')
);

// localStorage.setItem('bestName','seojin')