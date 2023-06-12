const { createSVGWindow } = require("svgdom");
const { SVG, registerWindow } = require("@svgdotjs/svg.js");
const fs = require("fs");
const sharp = require("sharp");

function createProgressBarSVG(percentage) {
  // Set up a simulated DOM environment
  const window = createSVGWindow();
  const document = window.document;
  registerWindow(window, document);

  const svgWidth = 400;
  const svgHeight = 300;
  const padding = 50;
  const progressBarWidth = svgWidth - padding * 2;
  const progressBarHeight = 30;
  const progressBarRadius = 15;
  const hsdRed = "#e60028";
  const progressWidth = (progressBarWidth * percentage) / 100;
  const svg = SVG().size(svgWidth, svgHeight);

  // Background rectangle
  const backgroundRect = svg
    .rect(progressBarWidth, progressBarHeight)
    .stroke({ color: hsdRed, width: 3 })
    .attr({
      fill: "transparent",
      rx: progressBarRadius,
      ry: progressBarRadius,
      x: padding,
      y: svgHeight / 2,
    });

  // Progress rectangle
  const progressRect = svg.rect(progressWidth, progressBarHeight).attr({
    fill: hsdRed,
    rx: progressBarRadius,
    ry: progressBarRadius,
    x: padding,
    y: svgHeight / 2,
  });

  // Text label
  const textLabel = svg
    .text(`${percentage}%`)
    .font({ size: 30 })
    .attr({
      fill: hsdRed,
      'font-weight': 'bold',
      x: svgWidth / 2,
      y: svgHeight / 2 - progressBarHeight / 2,
      'text-anchor': 'middle',
    });

  fs.writeFileSync("progressbar.svg", svg.svg());
}

function svgToPng(inputFilePath, outputFilePath) {
  // Read the SVG file and convert it to PNG
  sharp(inputFilePath)
    .png()
    .toFile(outputFilePath)
    .catch((error) => {
      console.error("Error converting SVG to PNG:", error);
    });
}

function createProgressBarImage(percentage) {
  createProgressBarSVG(percentage);
  svgToPng("progressbar.svg", "progressbar.png");
}

module.exports = { createProgressBarImage };
