import api, {getLinks} from '../api';
import {
  fetchFollowedHashtagsFail,
  fetchFollowedHashtagsRequest,
  fetchFollowedHashtagsSuccess, FOLLOWED_HASHTAGS_FETCH_FAIL, FOLLOWED_HASHTAGS_FETCH_REQUEST,
  FOLLOWED_HASHTAGS_FETCH_SUCCESS
} from "./tags";
export const INTERESTS_FILTER_CHANGE = 'INTEREST_FILTER_CHANGE';
export const INTERESTS_FILTER_CLEAR  = 'INTEREST_FILTER_CLEAR';
export const INTERESTS_FETCH_REQUEST   = 'INTERESTS_FETCH_REQUEST';
export const INTERESTS_FETCH_SUCCESS   = 'INTERESTS_FETCH_SUCCESS';
export const INTERESTS_FETCH_FAIL   = 'INTERESTS_FETCH_FAIL';
export const INTEREST_FOLLOW_REQUEST   = 'INTEREST_FOLLOW_REQUEST';
export const INTEREST_FOLLOW_SUCCESS   = 'INTEREST_FOLLOW_SUCCESS';
export const INTEREST_FOLLOW_FAIL   = 'INTEREST_FOLLOW_FAIL';
export const INTEREST_UNFOLLOW_REQUEST   = 'INTEREST_UNFOLLOW_REQUEST';
export const INTEREST_UNFOLLOW_SUCCESS   = 'INTEREST_UNFOLLOW_SUCCESS';
export const INTEREST_UNFOLLOW_FAIL   = 'INTEREST_UNFOLLOW_FAIL';
export const FOLLOWED_INTERESTS_FETCH_REQUEST = 'FOLLOWED_INTERESTS_FETCH_REQUEST';
export const FOLLOWED_INTERESTS_FETCH_SUCCESS = 'FOLLOWED_INTERESTS_FETCH_SUCCESS';
export const FOLLOWED_INTERESTS_FETCH_FAIL    = 'FOLLOWED_INTERESTS_FETCH_FAIL';
export const FOLLOWED_INTERESTS_EXPAND_REQUEST = 'FOLLOWED_INTERESTS_EXPAND_REQUEST';
export const FOLLOWED_INTERESTS_EXPAND_SUCCESS = 'FOLLOWED_INTERESTS_EXPAND_SUCCESS';
export const FOLLOWED_INTERESTS_EXPAND_FAIL    = 'FOLLOWED_INTERESTS_EXPAND_FAIL';


export function changeInterestsFilter(value) {
  return {
    type: INTERESTS_FILTER_CHANGE,
    value,
  };
}

export function clearInterestsFilter() {
  return {
    type: INTERESTS_FILTER_CLEAR,
  };
}

export function fetchInterestsRequest() {
  return {
    type: INTERESTS_FETCH_REQUEST,
  };
}

export const fetchFollowedInterests = () => (dispatch, getState) => {
  dispatch(fetchFollowedInterestsRequest());

  api(getState).get('/api/hsd/followed_interests').then(response => {
    const next = getLinks(response).refs.find(link => link.rel === 'next');
    dispatch(fetchFollowedInterestsSuccess(response.data, next ? next.uri : null));
  }).catch(err => {
    dispatch(fetchFollowedInterestsSuccess(err));
  });
};

export function fetchFollowedInterestsRequest() {
  return {
    type: FOLLOWED_INTERESTS_FETCH_REQUEST,
  };
}

export function fetchFollowedInterestsSuccess(followed_interests, next) {
  return {
    type: FOLLOWED_INTERESTS_FETCH_SUCCESS,
    followed_interests,
    next,
  };
}

export function fetchFollowedInterestsFail(error) {
  return {
    type: FOLLOWED_INTERESTS_FETCH_FAIL,
    error,
  };
}

export function fetchInterestsFilter() {
  return (dispatch, getState) => {
    const value    = getState().getIn(['interests_filter', 'value']);
    if (value.length === 0) {
      dispatch(fetchInterestsSuccess([], ''));
      return;
    }

    dispatch(fetchInterestsRequest());

    api(getState).get('/api/hsd/interests/search', {
      params: {
        q: value,
      },
    }).then(response => {
      dispatch(fetchInterestsSuccess(response.data, value));
    }).catch(error => {
      dispatch(fetchInterestsFail(error));
    });
  };
}

export function fetchInterestsSuccess(results, searchTerm) {
  return {
    type: INTERESTS_FETCH_SUCCESS,
    results,
    searchTerm,
  };
}

export function fetchInterestsFail(error) {
  return {
    type: INTERESTS_FETCH_FAIL,
    error,
  };
}
export const followInterest = name => (dispatch, getState) => {
  dispatch(followInterestRequest(name));

  api(getState).post(`/api/hsd/interests/${name}/follow`).then(({ data }) => {
    dispatch(followInterestSuccess(name, data));
  }).catch(err => {
    dispatch(followInterestFail(name, err));
  });
};

export const followInterestRequest = name => ({
  type: INTEREST_FOLLOW_REQUEST,
  name,
});

export const followInterestSuccess = (name, tag) => ({
  type: INTEREST_FOLLOW_SUCCESS,
  name,
  tag,
});

export const followInterestFail = (name, error) => ({
  type: INTEREST_FOLLOW_FAIL,
  name,
  error,
});

export const unfollowInterest = name => (dispatch, getState) => {
  dispatch(unfollowInterestRequest(name));

  api(getState).post(`/api/hsd/interests/${name}/unfollow`).then(({ data }) => {
    dispatch(unfollowInterestSuccess(name, data));
  }).catch(err => {
    dispatch(unfollowInterestFail(name, err));
  });
};

export const unfollowInterestRequest = name => ({
  type: INTEREST_UNFOLLOW_REQUEST,
  name,
});

export const unfollowInterestSuccess = (name, tag) => ({
  type: INTEREST_UNFOLLOW_SUCCESS,
  name,
  tag,
});

export const unfollowInterestFail = (name, error) => ({
  type: INTEREST_UNFOLLOW_FAIL,
  name,
  error,
});
