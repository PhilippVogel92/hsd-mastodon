import api from '../api';
export const INTERESTS_FILTER_CHANGE = 'INTEREST_FILTER_CHANGE';
export const INTERESTS_FILTER_CLEAR  = 'INTEREST_FILTER_CLEAR';
export const INTERESTS_FILTER_FETCH_REQUEST   = 'INTERESTS_FILTER_FETCH_REQUEST';
export const INTERESTS_FILTER_FETCH_SUCCESS   = 'INTERESTS_FILTER_FETCH_SUCCESS';
export const INTERESTS_FILTER_FETCH_FAIL   = 'INTERESTS_FILTER_FETCH_FAIL';
export const INTEREST_FOLLOW_REQUEST   = 'INTEREST_FOLLOW_REQUEST';
export const INTEREST_FOLLOW_SUCCESS   = 'INTEREST_FOLLOW_SUCCESS';
export const INTEREST_FOLLOW_FAIL   = 'INTEREST_FOLLOW_FAIL';
export const INTEREST_UNFOLLOW_REQUEST   = 'INTEREST_UNFOLLOW_REQUEST';
export const INTEREST_UNFOLLOW_SUCCESS   = 'INTEREST_UNFOLLOW_SUCCESS';
export const INTEREST_UNFOLLOW_FAIL   = 'INTEREST_UNFOLLOW_FAIL';

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

export function fetchInterestsFilterRequest() {
  return {
    type: INTERESTS_FILTER_FETCH_REQUEST,
  };
}

export function fetchInterestsFilter() {
  return (dispatch, getState) => {
    const value    = getState().getIn(['interests_filter', 'value']);
    const signedIn = !!getState().getIn(['meta', 'me']);
    if (value.length === 0) {
      dispatch(fetchInterestsFilterSuccess({ accounts: [], statuses: [], interests: [] }, ''));
      return;
    }

    dispatch(fetchInterestsFilterRequest());

    api(getState).get('/api/v2/search', {
      params: {
        q: value,
        resolve: signedIn,
        limit: 5,
      },
    }).then(response => {
      dispatch(fetchInterestsFilterSuccess(response.data, value));
    }).catch(error => {
      dispatch(fetchInterestsFilterFail(error));
    });
  };
}

export function fetchInterestsFilterSuccess(results, searchTerm) {
  return {
    type: INTERESTS_FILTER_FETCH_SUCCESS,
    results,
    searchTerm,
  };
}

export function fetchInterestsFilterFail(error) {
  return {
    type: INTERESTS_FILTER_FETCH_FAIL,
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
