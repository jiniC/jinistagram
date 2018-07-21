import { createStore, combineReducers} from "redux";
import users from './modules/users';

// 리듀서들 합침 -> 한개의 스토어
const reducer = combineReducers({
    users
});

let store = initialState => createStore(reducer);

export default store();
