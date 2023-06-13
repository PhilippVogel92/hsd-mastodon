const Mastodon = require("mastodon-api");
const fs = require("fs");

require("dotenv").config();

async function postToot(message, image) {
  try {
    const M = new Mastodon({
      access_token: process.env.ACCESS_TOKEN,
      timeout_ms: 60 * 1000,
      api_url: process.env.BOT_API_URL,
    });

    setTimeout(() => {
      M.post("media", { file: fs.createReadStream(image) }).then((resp) => {
        const id = resp.data.id;
        M.post("statuses", { status: message, media_ids: [id] });
      });
    }, 100);
  } catch (error) {
    console.error("Error:", error);
  }
}

function tootMessageData(response) {
  const currentSemester = response.data.value.find((list) => list.status === "aktiv");
  const lecturesStart = new Date(currentSemester.datum_veranstaltung_start);
  const lecturesEnd = new Date(currentSemester.datum_veranstaltung_ende);
  const examsStart = new Date(currentSemester.datum_pruefung_start);
  const examsEnd = new Date(currentSemester.datum_pruefung_ende);

  const currentPhase = getCurrentPhase();
  const phasePercentage = getPhasePercentage(currentPhase);

  if (currentPhase !== "holidays") {
    const phaseName = currentPhase === "lectures" ? "Vorlesungszeit" : "Prüfungszeit";
    const message = `${phaseName}-Progress: ${phasePercentage}%`;
    return [message, phasePercentage];
  }

  function getCurrentPhase() {
    const currentDate = new Date();

    if (currentDate >= lecturesStart && currentDate <= lecturesEnd) {
      return "lectures";
    } else if (currentDate >= examsStart && currentDate <= examsEnd) {
      return "exams";
    } else {
      return "holidays";
    }
  }

  function getPhasePercentage(currentPhase) {
    const currentDate = new Date();
    const phaseStart = currentPhase === "lectures" ? lecturesStart : examsStart;
    const phaseEnd = currentPhase === "lectures" ? lecturesEnd : examsEnd;
    const phaseDuration = phaseEnd - phaseStart;
    const elapsedTime = currentDate - phaseStart;
    const percentage = Math.round((elapsedTime / phaseDuration) * 100);

    return percentage;
  }
}

module.exports = { postToot, tootMessageData };
