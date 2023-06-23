import api from '../api';
import { debounce } from 'lodash';
import { showAlertForError } from './alerts';
import {expandHomeTimeline} from "./timelines";

export const SETTING_CHANGE = 'SETTING_CHANGE';
export const SETTING_SAVE   = 'SETTING_SAVE';

export function changeSetting(path, value) {
  return dispatch => {
    dispatch({
      type: SETTING_CHANGE,
      path, 
      value,
    });
    /*if(["home", "enable", "recommendations"].every(v => path.includes(v))) {
      dispatch(expandHomeTimeline({}));
    }*/
    dispatch(saveSettings());
  };
}

const debouncedSave = debounce((dispatch, getState) => {
  if (getState().getIn(['settings', 'saved'])) {
    return;
  }
  const data = getState().get('settings').filter((_, path) => path !== 'saved').toJS();

  api().put('/api/web/settings', { data })
    .then(() => dispatch({ type: SETTING_SAVE }))
    .catch(error => dispatch(showAlertForError(error)));
}, 5000, { trailing: true });

export function saveSettings() {
  return (dispatch, getState) => debouncedSave(dispatch, getState);
}
