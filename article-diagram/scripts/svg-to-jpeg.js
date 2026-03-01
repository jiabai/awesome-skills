/**
 * SVG to JPEG Converter
 * Converts SVG files to JPEG format with white background
 *
 * Usage:
 *   node svg-to-jpeg.js <svg-path-or-dir> [output-dir]
 *   node svg-to-jpeg.js ./diagrams                    # Convert all SVGs in directory
 *   node svg-to-jpeg.js ./diagrams/chart.svg           # Convert single file
 *   node svg-to-jpeg.js ./diagrams ./output            # Specify output directory
 *
 * Options:
 *   --quality <1-100>   JPEG quality (default: 90)
 *   --bg <color>        Background color in hex (default: #FFFFFF)
 */

const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const DEFAULT_QUALITY = 90;
const DEFAULT_BG = '#FFFFFF';

function parseArgs(args) {
  const result = {
    input: null,
    output: null,
    quality: DEFAULT_QUALITY,
    background: DEFAULT_BG,
    help: false
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];

    if (arg === '--help' || arg === '-h') {
      result.help = true;
    } else if (arg === '--quality') {
      result.quality = parseInt(args[++i], 10);
    } else if (arg === '--bg') {
      result.background = args[++i];
    } else if (!arg.startsWith('-') && !result.input) {
      result.input = arg;
    } else if (!arg.startsWith('-') && !result.output) {
      result.output = arg;
    }
    i++;
  }

  return result;
}

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : { r: 255, g: 255, b: 255 };
}

async function convertSvgToJpeg(svgPath, outputPath, options) {
  const { quality, background } = options;
  const bgRgb = hexToRgb(background);

  try {
    await sharp(svgPath)
      .flatten({ background: bgRgb })
      .jpeg({ quality })
      .toFile(outputPath);

    const stats = fs.statSync(outputPath);
    return { success: true, path: outputPath, size: stats.size };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function processFile(inputPath, outputDir, options) {
  const baseName = path.basename(inputPath, '.svg');
  const outputPath = path.join(outputDir, `${baseName}.jpeg`);

  console.log(`Converting: ${path.basename(inputPath)}`);
  const result = await convertSvgToJpeg(inputPath, outputPath, options);

  if (result.success) {
    console.log(`  -> ${path.basename(outputPath)} (${(result.size / 1024).toFixed(1)} KB)`);
  } else {
    console.error(`  Error: ${result.error}`);
  }

  return result;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.input) {
    console.log(`
SVG to JPEG Converter

Usage:
  node svg-to-jpeg.js <svg-path-or-dir> [output-dir]

Options:
  --quality <1-100>   JPEG quality (default: ${DEFAULT_QUALITY})
  --bg <hex>          Background color (default: ${DEFAULT_BG})

Examples:
  node svg-to-jpeg.js ./diagrams
  node svg-to-jpeg.js ./diagrams/chart.svg
  node svg-to-jpeg.js ./diagrams --quality 95 --bg #F0F0F0
`);
    process.exit(1);
  }

  const inputPath = path.resolve(args.input);
  const options = {
    quality: args.quality,
    background: args.background
  };

  let results = [];

  if (fs.statSync(inputPath).isDirectory()) {
    const outputDir = args.output ? path.resolve(args.output) : inputPath;

    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    const svgFiles = fs.readdirSync(inputPath)
      .filter(f => f.endsWith('.svg'))
      .map(f => path.join(inputPath, f));

    if (svgFiles.length === 0) {
      console.log('No SVG files found in directory.');
      process.exit(0);
    }

    console.log(`Found ${svgFiles.length} SVG file(s)\n`);

    for (const svgFile of svgFiles) {
      const result = await processFile(svgFile, outputDir, options);
      results.push(result);
    }
  } else if (inputPath.endsWith('.svg')) {
    const outputDir = args.output ? path.resolve(args.output) : path.dirname(inputPath);

    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    const result = await processFile(inputPath, outputDir, options);
    results.push(result);
  } else {
    console.error('Input must be an SVG file or directory.');
    process.exit(1);
  }

  const successful = results.filter(r => r.success).length;
  console.log(`\nDone! ${successful}/${results.length} file(s) converted.`);
}

main().catch(console.error);