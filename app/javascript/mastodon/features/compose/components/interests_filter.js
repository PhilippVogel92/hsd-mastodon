import React from 'react';
import PropTypes from 'prop-types';
import { defineMessages, FormattedMessage, injectIntl } from 'react-intl';
import Icon from 'mastodon/components/icon';
import ImmutablePropTypes from 'react-immutable-proptypes';
import Interest from "./interest";

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
    getFollowedInterests: PropTypes.func.isRequired,
    searchInterests: PropTypes.func.isRequired,
    openInRoute: PropTypes.bool,
    intl: PropTypes.object.isRequired,
    singleColumn: PropTypes.bool,
    results: ImmutablePropTypes.map.isRequired,
    initFollowedInterests: ImmutablePropTypes.list.isRequired,
  };

  state = {
    expanded: false,
    followedInterests: this.props.initFollowedInterests,
  };

  componentDidMount() {
    this.props.getFollowedInterests();
  }

  componentDidUpdate(prevProps) {
    // Check if it's a new user, you can also use some unique property, like the ID  (this.props.user.id !== prevProps.user.id)
    if (this.props.initFollowedInterests !== prevProps.initFollowedInterests) {
      this.setState({ followedInterests: this.props.initFollowedInterests });
    }
  }

  setRef = c => {
    this.searchForm = c;
  };

  handleChange = (e) => {
    this.props.onChange(e.target.value.replace(' ', '_').toLowerCase());
    this.debounceSearch();
  };

  debounce = () => {
    let timer;
    return () => {
      clearTimeout(timer);
      timer = setTimeout(() => this.props.searchInterests(), 250);
    };
  };

  debounceSearch = this.debounce();

  handleFollowInterest = (interest) => {
    this.props.followInterest(interest.get('name'));
    this.setState(state => ({
      followedInterests: state.followedInterests.push(interest),
    }));
  };

  handleUnfollowInterest = (interest) => {
    this.props.unfollowInterest(interest.get('name'));
    this.setState(state => ({
      followedInterests: state.followedInterests.filter(followed => followed !== interest),
    }));
  };

  handleFollowInterestSubmit = () => {
    let interestAlreadyFollowed = this.state.followedInterests.filter(interest => interest.get('name') === this.props.value).size > 0;
    if (interestAlreadyFollowed === true) return;
    this.props.followInterest(this.props.value);
    if (this.props.results.get('interests')?.size === 0) {
      this.props.onChange('');
    }
    let newInterest = new Map();
    newInterest.set('name', this.props.value);
    this.setState((state) => ({
      followedInterests: state.followedInterests.push(newInterest),
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
    const { followedInterests } = this.state;
    const hasValue = value.length > 0 || submitted;
    const notFollowedInterests = results.get('interests')?.filter(interest => followedInterests.filter(followed => followed.get('name') === interest.get('name')).size === 0);
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

        {results.get('interests') !== undefined &&
          results.get('interests').size === 0 &&
          value !== '' ? (
            <div className='new-interest'>
              <p><FormattedMessage id='interests_selection.search.empty' values={{ interest: value }} defaultMessage='The interest {interest} does not yet exist' /> </p>
              <button className='button' onClick={this.handleFollowInterestSubmit}><FormattedMessage id='interests_selection.create_interest' defaultMessage='Create interest' /></button>
            </div>
          ) : !notFollowedInterests?.size ? null : (
            <div className='search-results__section'>
              {notFollowedInterests.map(interest => (
                <Interest
                  interest={interest}
                  isFollowingInterestsList={false}
                  onClick={this.handleFollowInterest}
                  key={interest.get('name')}
                />
              ))}
            </div>
          )}

        <div className='followed-hashtags'>
          <h4><FormattedMessage id='interests_selection.followed_interests.title' defaultMessage='Your followed interests' /></h4>
          {followedInterests.size === 0 ? (
            <p><FormattedMessage id='interests_selection.followed_interests.empty' defaultMessage='You dont follow any interests' /></p>
          ) : (
            <div className='search-results__section'>
              {followedInterests.map(interest => (
                <Interest
                  interest={interest}
                  isFollowingInterestsList
                  onClick={this.handleUnfollowInterest}
                  key={interest.get('name')}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

}
