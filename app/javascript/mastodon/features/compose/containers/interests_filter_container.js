import { connect } from 'react-redux';
import {
  changeInterestsFilter,
  clearInterestsFilter,
  fetchInterestsFilter,
  followInterest,
  unfollowInterest,
} from 'mastodon/actions/interests_filter';
import InterestsFilter from '../components/interests_filter';
import { unfollowHashtag, fetchFollowedHashtags } from 'mastodon/actions/tags';

const mapStateToProps = state => ({
  value: state.getIn(['interests_filter', 'value']),
  submitted: state.getIn(['interests_filter', 'submitted']),
  results: state.getIn(['interests_filter', 'results']),
  initFollowedTags: state.getIn(['followed_tags', 'items']),
});

const mapDispatchToProps = dispatch => ({

  getFollowedTags () {
    dispatch(fetchFollowedHashtags());
  },

  onChange (value) {
    dispatch(changeInterestsFilter(value));
  },

  searchTags() {
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
