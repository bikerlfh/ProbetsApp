import { configureStore } from '@reduxjs/toolkit';
import rootReducer from './reducers';
import {loadState} from './localStorage';

const persistedState = loadState();

const store = configureStore({
  reducer: rootReducer,
  preloadedState: persistedState,
  devTools: process.env.NODE_ENV !== 'production',
});

export default store;