import {
  FOLLOWED_INTERESTS_FETCH_REQUEST,
  FOLLOWED_INTERESTS_FETCH_SUCCESS,
  FOLLOWED_INTERESTS_FETCH_FAIL,
  FOLLOWED_INTERESTS_EXPAND_REQUEST,
  FOLLOWED_INTERESTS_EXPAND_SUCCESS,
  FOLLOWED_INTERESTS_EXPAND_FAIL,
} from 'mastodon/actions/interests';
import { Map as ImmutableMap, List as ImmutableList, fromJS } from 'immutable';

const initialState = ImmutableMap({
  items: ImmutableList(),
  isLoading: false,
  next: null,
});

export default function followed_interests(state = initialState, action) {
  switch(action.type) {
  case FOLLOWED_INTERESTS_FETCH_REQUEST:
    return state.set('isLoading', true);
  case FOLLOWED_INTERESTS_FETCH_SUCCESS:
    return state.withMutations(map => {
      map.set('items', fromJS(action.followed_interests));
      map.set('isLoading', false);
      map.set('next', action.next);
    });
  case FOLLOWED_INTERESTS_FETCH_FAIL:
    return state.set('isLoading', false);
  case FOLLOWED_INTERESTS_EXPAND_REQUEST:
    return state.set('isLoading', true);
  case FOLLOWED_INTERESTS_EXPAND_SUCCESS:
    return state.withMutations(map => {
      map.update('items', set => set.concat(fromJS(action.followed_interests)));
      map.set('isLoading', false);
      map.set('next', action.next);
    });
  case FOLLOWED_INTERESTS_EXPAND_FAIL:
    return state.set('isLoading', false);
  default:
    return state;
  }
}
