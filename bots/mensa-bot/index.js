import axios from 'axios';
import * as dotenv from 'dotenv';
import { login } from 'masto';
import getTodaysMeals from './mensa.js';

(async () => {
  try {
    dotenv.config();
    const meals = await getTodaysMeals();
    if (!meals.length) return;
    const masto = await login({
      url: process.env.MASTODON_URL,
      accessToken: process.env.MENSA_BOT_ACCESS_TOKEN,
      timeout: 5000,
    });

    let status = '';
    let mediaIds = [];
    for (const meal of meals) {
      const imageRaw = await axios.get(meal.PFAD, { responseType: 'arraybuffer' });
      const image = Buffer.from(imageRaw.data, 'binary');
      let media = await masto.v2.mediaAttachments.create({ file: image, description: meal.SPEISE });
      mediaIds.push(media.id);
      status += `${meal.SPEISE}: ${meal.AUSGABETEXT.replace(/ \([^)]*\) */g, ' ').trim()}\nStudierende: ${meal.STUDIERENDE}€, Bedienstete: ${meal.BEDIENSTETE}€, Gäste: ${meal.GAESTE}€${meal !== meals[meals.length - 1] ? '\n\n': ''}`;
    }

    await masto.v1.statuses.create({
      status,
      mediaIds,
      language: 'de',
    });
  } catch (error) {
    console.error(error);
  }
})();
