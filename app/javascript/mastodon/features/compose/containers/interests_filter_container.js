import { connect } from 'react-redux';
import {
  changeInterestsFilter,
  clearInterestsFilter,
  fetchInterestsFilter,
} from '../../../actions/interests_filter';
import InterestsFilter from '../components/interests_filter';
import { unfollowHashtag, followHashtag, fetchFollowedHashtags } from 'mastodon/actions/tags';

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
    dispatch(followHashtag(name));
  },

  unfollowInterest(name) {
    dispatch(unfollowHashtag(name));
  },

  onClear () {
    dispatch(clearInterestsFilter());
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(InterestsFilter);
