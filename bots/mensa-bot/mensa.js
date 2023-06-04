import axios from 'axios';
import * as xml2js from 'xml2js';

const EXCLUDED_FOOD = ['zur Pizza', 'Salatbuffet', 'Dessertauswahl', 'Beilagenauswahl'];

export default async function () {
  let meals;
  const res = await axios.get(process.env.MENSA_XML_ENDPOINT);
  const parser = new xml2js.Parser({ explicitArray: false, mergeAttrs: true });
  parser.parseString(res.data, (err, result) => {
    meals = result.DATAPACKET.ROWDATA.ROW.filter((entry =>
      entry.MENSA == process.env.MENSA_NAME &&
      entry.DATUM === new Date().toLocaleString('de-DE', { dateStyle: 'medium' }) &&
      !EXCLUDED_FOOD.includes(entry.SPEISE)));
  });
  meals.sort(((a, b) => a.SPEISE === 'Pizza' ? 1 : (b.SPEISE === 'Pizza' ? -1 : 0)))
  return meals;
}
