import React from 'react';
import PropTypes from 'prop-types';
import { defineMessages, FormattedMessage, injectIntl } from 'react-intl';
import Icon from 'mastodon/components/icon';
import InterestsFilterHashtag from './interests_filter_hashtag';
import ImmutablePropTypes from 'react-immutable-proptypes';

const messages = defineMessages({
  placeholder: { id: 'interests_selection.search', defaultMessage: 'Search for tags' },
});

export default
@injectIntl
class InterestsFilter extends React.PureComponent {

  static contextTypes = {
    router: PropTypes.object.isRequired,
    identity: PropTypes.object.isRequired,
  };

  static propTypes = {
    value: PropTypes.string.isRequired,
    submitted: PropTypes.bool,
    onChange: PropTypes.func.isRequired,
    onClear: PropTypes.func.isRequired,
    followInterest: PropTypes.func.isRequired,
    unfollowInterest: PropTypes.func.isRequired,
    getFollowedTags: PropTypes.func.isRequired,
    searchTags: PropTypes.func.isRequired,
    openInRoute: PropTypes.bool,
    intl: PropTypes.object.isRequired,
    singleColumn: PropTypes.bool,
    results: ImmutablePropTypes.map.isRequired,
    initFollowedTags: ImmutablePropTypes.list.isRequired,
  };

  state = {
    expanded: false,
    followedTags: this.props.initFollowedTags,
  };

  componentDidMount() {
    this.props.getFollowedTags();
  }

  componentDidUpdate(prevProps) {
    // Check if it's a new user, you can also use some unique property, like the ID  (this.props.user.id !== prevProps.user.id)
    if (this.props.initFollowedTags !== prevProps.initFollowedTags) {
      this.setState({ followedTags: this.props.initFollowedTags });
    }
  }

  setRef = c => {
    this.searchForm = c;
  };

  handleChange = (e) => {
    this.props.onChange(e.target.value.replace(' ', '_'));
    this.debounceSearch();
  };

  debounce = () => {
    let timer;
    return () => {
      clearTimeout(timer);
      timer = setTimeout(() => this.props.searchTags(), 250);
    };
  };

  debounceSearch = this.debounce();

  handleFollowInterest = (hashtag) => {
    this.props.followInterest(hashtag.get('name'));
    this.setState(state => ({
      followedTags: state.followedTags.push(hashtag),
    }));
  };

  handleUnfollowInterest = (hashtag) => {
    this.props.unfollowInterest(hashtag.get('name'));
    this.setState(state => ({
      followedTags: state.followedTags.filter(followed => followed !== hashtag),
    }));
  };

  handleFollowInterestSubmit = () => {
    let tagAlreadyFollowed = this.state.followedTags.filter(hashtag => hashtag.get('name') === this.props.value).size > 0;
    if (tagAlreadyFollowed === true) return;
    this.props.followInterest(this.props.value);
    if (this.props.results.get('hashtags')?.size === 0) {
      this.props.onChange('');
    }
    let newTag = new Map();
    newTag.set('name', this.props.value);
    this.setState((state) => ({
      followedTags: state.followedTags.push(newTag),
    }));
  };

  handleClear = (e) => {
    e.preventDefault();

    if (this.props.value.length > 0 || this.props.submitted) {
      this.props.onClear();
    }
  };

  handleKeyUp = (e) => {
    if (e.target.value.length === 0) return;
    if (e.key === 'Enter') {
      e.preventDefault();
      this.handleFollowInterestSubmit();
    } else if (e.key === 'Escape') {
      document.querySelector('.ui').parentElement.focus();
    }
  };

  handleFocus = () => {
    this.setState({ expanded: true });

    if (this.searchForm && !this.props.singleColumn) {
      const { left, right } = this.searchForm.getBoundingClientRect();
      if (left < 0 || right > (window.innerWidth || document.documentElement.clientWidth)) {
        this.searchForm.scrollIntoView();
      }
    }
  };

  handleBlur = () => {
    this.setState({ expanded: false });
  };

  render() {
    const { intl, value, submitted, results } = this.props;
    const { followedTags } = this.state;
    const hasValue = value.length > 0 || submitted;
    const notFollowedTags = results.get('hashtags')?.filter(hashtag => followedTags.filter(followed => followed.get('name') === hashtag.get('name')).size === 0);

    return (
      <div className='interests-filter'>
        <input
          ref={this.setRef}
          className='search__input'
          type='text'
          placeholder={intl.formatMessage(messages.placeholder)}
          aria-label={intl.formatMessage(messages.placeholder)}
          value={value}
          onChange={this.handleChange}
          onKeyUp={this.handleKeyUp}
          onFocus={this.handleFocus}
          onBlur={this.handleBlur}
        />

        <div
          role='button'
          tabIndex='0'
          className='search__icon'
          onClick={this.handleClear}
        >
          <Icon id='search' className={hasValue ? '' : 'active'} />
          <Icon
            id='times-circle'
            className={hasValue ? 'active' : ''}
            aria-label={intl.formatMessage(messages.placeholder)}
          />
        </div>

        {results.get('hashtags') !== undefined &&
          results.get('hashtags').size === 0 &&
          value !== '' ? (
            <div className='new-hashtag'>
              <p><FormattedMessage id='interests_selection.search.empty' values={{ hashtag: value }} defaultMessage='The hashtag {hashtag} does not yet exist' /> </p>
              <button className='button' onClick={this.handleFollowInterestSubmit}><FormattedMessage id='interests_selection.create_hashtag' defaultMessage='Create hashtag' /></button>
            </div>
          ) : !notFollowedTags?.size ? null : (
            <div className='search-results__section'>
              {notFollowedTags.map(hashtag => (
                <InterestsFilterHashtag
                  hashtag={hashtag}
                  isFollowingHashtagsList={false}
                  onClick={this.handleFollowInterest}
                  key={hashtag.get('name')}
                />
              ))}
            </div>
          )}

        <h3><FormattedMessage id='interests_selection.followed_hashtags.title' defaultMessage='Your followed hashtags' /></h3>
        {followedTags.size === 0 ? (
          <p><FormattedMessage id='interests_selection.followed_hashtags.empty' defaultMessage='You dont follow any hashtags' /></p>
        ) : (
          <div className='search-results__section'>
            {followedTags.map(hashtag => (
              <InterestsFilterHashtag
                hashtag={hashtag}
                isFollowingHashtagsList
                onClick={this.handleUnfollowInterest}
                key={hashtag.get('name')}
              />
            ))}
          </div>
        )}
      </div>
    );
  }

}
