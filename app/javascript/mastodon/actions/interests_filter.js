import api from '../api';

export const INTERESTS_FILTER_CHANGE = 'INTEREST_FILTER_CHANGE';
export const INTERESTS_FILTER_CLEAR  = 'INTEREST_FILTER_CLEAR';
export const INTERESTS_FILTER_FETCH_REQUEST   = 'INTERESTS_FILTER_FETCH_REQUEST';
export const INTERESTS_FILTER_FETCH_SUCCESS   = 'INTERESTS_FILTER_FETCH_SUCCESS';
export const INTERESTS_FILTER_FETCH_FAIL   = 'INTERESTS_FILTER_FETCH_FAIL';

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
      dispatch(fetchInterestsFilterSuccess({ accounts: [], statuses: [], hashtags: [] }, ''));
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
