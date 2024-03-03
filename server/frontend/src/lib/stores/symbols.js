import { writable } from 'svelte/store';

/** @type {Symbol[]} */
const symbols = [];

export default writable(symbols);
