// Polyfill para TextEncoder e TextDecoder, necessário para JSDOM > 16
const { TextEncoder, TextDecoder } = require('util');

global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;
