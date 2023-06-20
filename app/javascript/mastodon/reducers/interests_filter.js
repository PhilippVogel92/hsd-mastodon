import {
  INTERESTS_FILTER_CHANGE,
  INTERESTS_FILTER_CLEAR,
  INTERESTS_FILTER_FETCH_SUCCESS,
  INTERESTS_FILTER_FETCH_FAIL,
  INTERESTS_FILTER_FETCH_REQUEST,
} from '../actions/interests_filter';
import { Map as ImmutableMap, fromJS } from 'immutable';

const initialState = ImmutableMap({
  value: '',
  submitted: false,
  results: ImmutableMap(),
  isLoading: false,
  searchTerm: '',
});

export default function interests_filter(state = initialState, action) {
  switch(action.type) {
  case INTERESTS_FILTER_CHANGE:
    return state.withMutations(map => {
      map.set('value', action.value);
      map.set('results', ImmutableMap());
    });
  case INTERESTS_FILTER_CLEAR:
    return state.withMutations(map => {
      map.set('value', '');
      map.set('results', ImmutableMap());
      map.set('submitted', false);
    });
  case INTERESTS_FILTER_FETCH_REQUEST:
    return state.withMutations(map => {
      map.set('isLoading', true);
      map.set('submitted', true);
    });
  case INTERESTS_FILTER_FETCH_SUCCESS:
    return state.withMutations(map => {
      map.set('results', ImmutableMap({
        hashtags: fromJS(action.results.hashtags),
      }));

      map.set('searchTerm', action.searchTerm);
      map.set('isLoading', false);
    });
  case INTERESTS_FILTER_FETCH_FAIL:
    return state.set('isLoading', false);
  default:
    return state;
  }
}
