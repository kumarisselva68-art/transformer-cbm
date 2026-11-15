const pptx = require('pptxgenjs');
const pres = new pptx();
const slide = pres.addSlide();
slide.addText([
  { text: 'T', options: { italic: true, fontSize: 24, fontFace: 'Cambria Math' } },
  { text: 'p', options: { subscript: true, fontSize: 16, fontFace: 'Cambria Math' } },
  { text: ' = T', options: { fontSize: 24, fontFace: 'Cambria Math' } },
  { text: 'f', options: { subscript: true, fontSize: 16, fontFace: 'Cambria Math' } },
  { text: ' + H \u00B7 max(0, ', options: { fontSize: 24, fontFace: 'Cambria Math' } },
  { text: 'r', options: { italic: true, fontSize: 24, fontFace: 'Cambria Math' } },
  { text: ')', options: { fontSize: 24, fontFace: 'Cambria Math' } }
], { x: 1, y: 1, w: 6, h: 1 });
pres.writeFile({ fileName: 'E:/Client/Transformer_CBM/PPT/test_math.pptx' }).then(() => console.log('OK')).catch(console.error);
