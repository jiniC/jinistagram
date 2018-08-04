import { createStore, combineReducers, applyMiddleware } from "redux";
import { routerReducer, routerMiddleware } from "react-router-redux";
import createHistory from "history/createBrowserHistory";
import thunk from "redux-thunk";
import users from 'redux/modules/users';
import Reactotron from "ReactotronConfig";
import { i18nState } from "redux-i18n";
import { composeWithDevTools } from "redux-devtools-extension";
//import { logger } from "redux-logger"; => prod 일때도  redux-logger를 부름 (무거워짐)

// process: node js 의 전체 정보 가지고 있는 변수
const env = process.env.NODE_ENV;

const history = createHistory();
const middlewares = [thunk, routerMiddleware(history)]; // middlewares 배열

if(env==="development") {
    const { logger } = require("redux-logger");
    middlewares.push(logger);
}

// 리듀서들 합침 -> 한개의 스토어
const reducer = combineReducers({
    users,
    routing: routerReducer,
    i18nState
});

let store;

if(env==="development") {
    // dev일때: 리액토트론, 스토어 생성
    store = initialState => Reactotron.createStore(reducer, composeWithDevTools(applyMiddleware(...middlewares)));
} else {
    // product일때: 노멀 리덕스랑 스토어 생성
    store = initialState => createStore(reducer, applyMiddleware(...middlewares)); 
}

// middlewares 만 써주면 배열 [thunk] 를 풀어서 써줌

export { history };

export default store();