import axios from 'axios';
import * as dotenv from 'dotenv';
import { login } from 'masto';
import getTodaysMeals from './mensa.js';

(async () => {
  try {
    dotenv.config();
    const meals = await getTodaysMeals();
    if (!meals) return;
    const masto = await login({
      url: process.env.MASTODON_URL,
      accessToken: process.env.MENSA_BOT_ACCESS_TOKEN,
      timeout: 5000
    });

    let status;
    for (const meal of meals) {
      const imageRaw = await axios.get(meal.PFAD, { responseType: 'arraybuffer' });
      const image = Buffer.from(imageRaw.data, 'binary');
      const media = await masto.v2.mediaAttachments.create({ file: image });
      status = await masto.v1.statuses.create({
        status: `${meal.SPEISE}: ${meal.AUSGABETEXT}\nStudierende: ${meal.STUDIERENDE} € , Bedienstete: ${meal.BEDIENSTETE} € , Gäste: ${meal.GAESTE} €`,
        inReplyToId: status?.id,
        mediaIds: [media.id],
        language: 'de'
      });
    }
  } catch (error) {
    console.error(error);
  }
})()
