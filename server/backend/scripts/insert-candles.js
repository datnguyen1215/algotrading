import '../alias';
import 'dotenv/config';
import fs from 'fs';
import readline from 'readline';
import Configuration from '@src/configuration';
import db from '@/src/core/db';

// check whether file path exists
if (!Configuration.data.candles) {
  console.log('File path not specified');
  process.exit();
}

if (!Configuration.data.symbol) {
  console.log('Symbol not specified');
  process.exit();
}

// check whether the file exists
if (!fs.existsSync(Configuration.data.candles)) {
  console.log('File does not exist');
  process.exit();
}

/**
 * @param {any[]} data
 */
const onEnoughData = async data => {
  const symbol = Configuration.data.symbol;

  /**
   * @type {import('@/src/core/db/candles/insert').Candle[]}
   */
  const candles = data.map(x => {
    const [time, open, high, low, close] = x;
    return {
      time: new Date(parseInt(time)).toUTCString(),
      open,
      high,
      low,
      close,
      symbol
    };
  });

  try {
    await db.candles.insert(candles);
  } catch (e) {
    console.error(e);
  }
};

let chunks = [];

/**
 * Read a row from the file
 * @param {string} row
 */
const onRow = async row => {
  const data = row.split(',');
  chunks.push(data);

  if (chunks.length !== 500) return;

  await onEnoughData(chunks);
  chunks = [];
};

(async () => {
  const rl = readline.createInterface({
    input: fs.createReadStream(Configuration.data.candles)
  });

  // must use this syntax to iterate and wait for the insert() to finish
  // otherwise, we'll have data loss.
  for await (const line of rl) await onRow(line);
})();
