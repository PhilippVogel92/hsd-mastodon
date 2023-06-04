const axios = require("axios");
const { createProgressBarImage } = require("./image.js");
const { postToot, tootMessageData } = require("./toot.js");

require("dotenv").config();

axios
  .get(process.env.SEMESTER_XML_ENDPOINT)
  .then((response) => {
    const [message, percentage] = tootMessageData(response);
    if (message) {
      createProgressBarImage(percentage);
      postToot(message, "progressbar.png");
    }
  })
  .catch((err) => console.log("Error: ", err));
