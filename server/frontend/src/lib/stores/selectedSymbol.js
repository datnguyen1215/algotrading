import { writable } from 'svelte/store';

/** @type {Symbol} */
const symbol = null;

const selectedSymbol = writable(symbol);

export default selectedSymbol;
