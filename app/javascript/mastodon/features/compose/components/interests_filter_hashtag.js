import React from 'react';
import PropTypes from 'prop-types';
import { injectIntl } from 'react-intl';
import Icon from 'mastodon/components/icon';
import ImmutablePropTypes from 'react-immutable-proptypes';

export default
@injectIntl
class InterestsFilterHashtag extends React.PureComponent {

  static contextTypes = {
    router: PropTypes.object.isRequired,
    identity: PropTypes.object.isRequired,
  };

  static propTypes = {
    hashtag: ImmutablePropTypes.map.isRequired,
    isFollowingHashtagsList: PropTypes.bool.isRequired,
    onClick: PropTypes.func.isRequired,
  };

  handleOnClick = () => {
    this.props.onClick(this.props.hashtag);
  };

  render() {
    const { hashtag, isFollowingHashtagsList } = this.props;

    return (
      <div
        className='interests-hashtag'
        onClick={this.handleOnClick}
        key={hashtag.get('name')}
      >
        {hashtag.get('name')}
        {isFollowingHashtagsList ? <Icon id='times-circle' /> : null}
      </div>
    );
  }

}
