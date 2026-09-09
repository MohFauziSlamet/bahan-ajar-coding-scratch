const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const { createCanvas } = require('canvas');

const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
dom.window.HTMLCanvasElement.prototype.getContext = function(type) {
    return createCanvas(100, 100).getContext(type);
};

const scratchblocks = require('scratchblocks')(dom.window);

const script = `
when flag clicked
set [GameState v] to [Menu]
set [Score v] to (0)
set [Lives v] to (3)
set [CurrentLevel v] to (1)
switch backdrop to [bg_menu v]
stop all sounds
start sound [bgm_patriotik v]
broadcast [Show_Menu v]
`;

const doc = scratchblocks.parse(script);
const svg = scratchblocks.render(doc, { style: 'scratch3' });

fs.writeFileSync('test_output.svg', svg.outerHTML);
console.log('Successfully generated test_output.svg! File size:', svg.outerHTML.length);
