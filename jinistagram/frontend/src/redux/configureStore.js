import { createStore, combineReducers, applyMiddleware } from "redux";
import thunk from "redux-thunk";
import users from 'redux/modules/users';
//import { logger } from "redux-logger"; => prod 일때도  redux-logger를 부름 (무거워짐)

// process: node js 의 전체 정보 가지고 있는 변수
const env = process.env.NODE_ENV;
// console.log(env);

const middlewares = [thunk]; // middlewares 배열

if(env==="development") {
    const { logger } = require("redux-logger");
    middlewares.push(logger);
}

// 리듀서들 합침 -> 한개의 스토어
const reducer = combineReducers({
    users
});

let store = initialState => createStore(reducer, applyMiddleware(...middlewares)); 
// middlewares 만 써주면 배열 [thunk] 를 풀어서 써줌

export default store();
