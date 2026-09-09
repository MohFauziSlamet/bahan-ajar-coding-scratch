const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const { createCanvas } = require('canvas');

const dom = new JSDOM('<!DOCTYPE html><html><head></head><body></body></html>', {
    runScripts: 'dangerously'
});

dom.window.HTMLCanvasElement.prototype.getContext = function(type) {
    return createCanvas(100, 100).getContext(type);
};

const code = fs.readFileSync('./node_modules/scratchblocks/build/scratchblocks.min.js', 'utf8');
dom.window.eval(code);

const scratchblocks = dom.window.scratchblocks;
console.log('Scratchblocks initialized on window:', typeof scratchblocks);

const script = `
when flag clicked
set [GameState v] to [Menu]
set [Score v] to [0]
set [Lives v] to [3]
set [CurrentLevel v] to [1]
switch backdrop to [bg_menu v]
stop all sounds
start sound [bgm_patriotik v]
broadcast [Show_Menu v]
`;

const doc = scratchblocks.parse(script);
const svg = scratchblocks.render(doc, { style: 'scratch3' });

fs.writeFileSync('test_render.svg', svg.outerHTML);
console.log('Successfully written test_render.svg! Size:', svg.outerHTML.length);
