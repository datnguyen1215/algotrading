const format = ({ level, timestamp, label, messages }) => {
  const msg = messages.join(' ');
  return `${timestamp} - [${level}] - (${label}) - ${msg}`;
};

export default format;
