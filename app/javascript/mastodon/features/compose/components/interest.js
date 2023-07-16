import React from 'react';
import PropTypes from 'prop-types';
import { injectIntl } from 'react-intl';
import Icon from 'mastodon/components/icon';
import ImmutablePropTypes from 'react-immutable-proptypes';

export default
@injectIntl
class Interest extends React.PureComponent {

  static contextTypes = {
    router: PropTypes.object.isRequired,
    identity: PropTypes.object.isRequired,
  };

  static propTypes = {
    interest: ImmutablePropTypes.map.isRequired,
    isFollowingInterestsList: PropTypes.bool.isRequired,
    onClick: PropTypes.func.isRequired,
  };

  handleOnClick = () => {
    this.props.onClick(this.props.interest);
  };

  render() {
    const { interest, isFollowingInterestsList } = this.props;

    return (
      <div
        className='interest'
        onClick={this.handleOnClick}
        key={interest.get('name')}
      >
        {interest.get('name')}
        {isFollowingInterestsList ? <Icon id='times-circle' /> : null}
      </div>
    );
  }

}
