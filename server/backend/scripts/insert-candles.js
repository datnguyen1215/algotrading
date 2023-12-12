import '../alias';
import 'dotenv/config';
import fs from 'fs';
import readline from 'readline';
import Configuration from '@src/configuration';
import db from '@/src/core/db';
import format from 'pg-format';

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

const insert = async candles => {
  const data = candles.map(candle => [
    Configuration.data.symbol,
    new Date(candle.timestamp).toISOString(),
    candle.open,
    candle.high,
    candle.low,
    candle.close
  ]);

  const query = format(
    'INSERT INTO candles (symbol, time, open, high, low, close) VALUES %L',
    data
  );

  await db.query.send(query);
};

(async () => {
  let data = fs.readFileSync(Configuration.data.candles, 'utf8');
  const candles = JSON.parse(data);

  // group 500 candles and insert them
  const group = 500;
  for (let i = 0; i < candles.length; i += group)
    await insert(candles.slice(i, i + group));

  process.exit();
})();
