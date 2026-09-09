const fs = require('fs');
const path = require('path');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const { createCanvas, loadImage } = require('canvas');

const dom = new JSDOM('<!DOCTYPE html><html><head></head><body></body></html>', {
    runScripts: 'dangerously'
});

dom.window.HTMLCanvasElement.prototype.getContext = function(type) {
    return createCanvas(100, 100).getContext(type);
};

const code = fs.readFileSync(path.join(__dirname, 'node_modules/scratchblocks/build/scratchblocks.min.js'), 'utf8');
dom.window.eval(code);
const scratchblocks = dom.window.scratchblocks;

const scratch3CSS = `
<style>
.sb3-label { font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; font-size: 12px; font-weight: bold; fill: #ffffff; }
.sb3-motion { fill: #4C97FF; stroke: #3373CC; }
.sb3-looks { fill: #9966FF; stroke: #774DCB; }
.sb3-sound { fill: #D65CD6; stroke: #BD42BD; }
.sb3-events { fill: #FFBF00; stroke: #CC9900; }
.sb3-control { fill: #FFAB19; stroke: #CF8B17; }
.sb3-sensing { fill: #5CB1D6; stroke: #2E8EB8; }
.sb3-operators { fill: #59C059; stroke: #389438; }
.sb3-variables { fill: #FF8C1A; stroke: #DB6E00; }
.sb3-list { fill: #FF661A; stroke: #E64D00; }
.sb3-custom { fill: #FF6680; stroke: #FF3355; }
.sb3-input-string, .sb3-input-number { fill: #FFFFFF !important; stroke: rgba(0,0,0,0.15); }
.sb3-input-dropdown { fill: rgba(0,0,0,0.15) !important; stroke: rgba(0,0,0,0.15); }
.sb3-literal-dropdown, .sb3-literal-string, .sb3-literal-number { fill: #575E75 !important; font-size: 12px; font-weight: bold; }
.sb3-darker { fill: rgba(0,0,0,0.25) !important; }
</style>
`;

async function renderBlockToFiles(scratchCode, baseName, outDir) {
    const doc = scratchblocks.parse(scratchCode);
    const svgEl = scratchblocks.render(doc, { style: 'scratch3' });
    let svgHtml = svgEl.outerHTML;
    
    // Inject CSS into SVG
    svgHtml = svgHtml.replace('<defs>', '<defs>' + scratch3CSS);
    
    const svgPath = path.join(outDir, `${baseName}.svg`);
    const pngPath = path.join(outDir, `${baseName}.png`);
    
    fs.writeFileSync(svgPath, svgHtml);
    
    // Convert to PNG with canvas
    try {
        const img = await loadImage('data:image/svg+xml;base64,' + Buffer.from(svgHtml).toString('base64'));
        const canvas = createCanvas(img.width, img.height);
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);
        fs.writeFileSync(pngPath, canvas.toBuffer('image/png'));
    } catch(e) {
        console.error('PNG conversion error for', baseName, e.message);
    }
    
    console.log(`Generated: ${baseName}.svg and ${baseName}.png`);
}

module.exports = { renderBlockToFiles };
