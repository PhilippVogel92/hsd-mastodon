import { connect } from 'react-redux';
import {
  changeInterestsFilter,
  clearInterestsFilter,
  fetchInterestsFilter,
  followInterest,
  unfollowInterest,
  fetchFollowedInterests,
} from 'mastodon/actions/interests';
import InterestsFilter from '../components/interests_filter';

const mapStateToProps = state => ({
  value: state.getIn(['interests_filter', 'value']),
  submitted: state.getIn(['interests_filter', 'submitted']),
  results: state.getIn(['interests_filter', 'results']),
  initFollowedInterests: state.getIn(['followed_interests', 'items']),
});

const mapDispatchToProps = dispatch => ({

  getFollowedInterests () {
    dispatch(fetchFollowedInterests());
  },

  onChange (value) {
    dispatch(changeInterestsFilter(value));
  },

  searchInterests() {
    dispatch(fetchInterestsFilter());
  },

  followInterest(name) {
    dispatch(followInterest(name));
  },

  unfollowInterest(name) {
    dispatch(unfollowInterest(name));
  },

  onClear () {
    dispatch(clearInterestsFilter());
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(InterestsFilter);
