import axios from 'axios';
import * as xml2js from 'xml2js';

export default async function () {
  let meals;
  const res = await axios.get(process.env.MENSA_XML_ENDPOINT);
  const parser = new xml2js.Parser({ explicitArray: false, mergeAttrs: true });
  parser.parseString(res.data, (err, result) => {
    meals = result.DATAPACKET.ROWDATA.ROW.filter((entry =>
      entry.MENSA == process.env.MENSA_NAME && entry.DATUM === new Date().toLocaleString('de-DE', {
        dateStyle: 'medium'
      })));
  });
  return meals;
}
