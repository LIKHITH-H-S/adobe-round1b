import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import pdfjs from 'pdfjs-dist/legacy/build/pdf.js';
const { getDocument } = pdfjs;


// ES module __dirname fix
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const INPUT_DIR = path.join(__dirname, 'input');
const OUTPUT_DIR = path.join(__dirname, 'output');

function getHeadingLevel(fontSize) {
  if (fontSize > 20) return "H1";
  else if (fontSize > 15) return "H2";
  else if (fontSize > 12) return "H3";
  return null;
}

async function processPDF(filePath) {
  const data = new Uint8Array(fs.readFileSync(filePath));
  const pdfDoc = await getDocument({ data }).promise;

  const outline = [];
  const filename = path.basename(filePath, '.pdf');

  for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
    const page = await pdfDoc.getPage(pageNum);
    const textContent = await page.getTextContent();

    for (let item of textContent.items) {
      const text = item.str.trim();
      const size = item.transform[0]; // estimated font size

      const level = getHeadingLevel(size);
      if (level && text.length > 1 && text.length < 100) {
        outline.push({
          level,
          text,
          page: pageNum
        });
      }
    }
  }

  return {
    title: filename,
    outline
  };
}

async function main() {
  const files = fs.readdirSync(INPUT_DIR).filter(f => f.endsWith('.pdf'));

  for (let file of files) {
    const result = await processPDF(path.join(INPUT_DIR, file));
    fs.writeFileSync(
      path.join(OUTPUT_DIR, file.replace('.pdf', '.json')),
      JSON.stringify(result, null, 2)
    );
    console.log(`✅ Processed: ${file}`);
  }
}

main();
