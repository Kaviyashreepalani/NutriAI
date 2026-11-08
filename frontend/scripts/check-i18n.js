import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const localesDir = path.resolve(__dirname, '../public/locales');
const languages = ['en', 'ta', 'hi', 'te', 'ml'];

console.log('Checking i18n translation key completeness across all 5 languages...');

const loadJson = (lang) => {
  const filePath = path.join(localesDir, lang, 'translation.json');
  if (!fs.existsSync(filePath)) {
    console.error(`Missing translation file for language: ${lang} at ${filePath}`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
};

const getKeys = (obj, prefix = '') => {
  let keys = [];
  for (const [k, v] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${k}` : k;
    if (typeof v === 'object' && v !== null && !Array.isArray(v)) {
      keys = keys.concat(getKeys(v, fullKey));
    } else {
      keys.push(fullKey);
    }
  }
  return keys;
};

const baseTranslations = loadJson('en');
const baseKeys = new Set(getKeys(baseTranslations));

let hasErrors = false;

languages.forEach((lang) => {
  if (lang === 'en') return;
  const langTranslations = loadJson(lang);
  const langKeys = new Set(getKeys(langTranslations));

  const missing = [...baseKeys].filter((k) => !langKeys.has(k));
  if (missing.length > 0) {
    console.error(`Language '${lang}' is missing ${missing.length} keys:`);
    missing.slice(0, 10).forEach((k) => console.error(`  - ${k}`));
    if (missing.length > 10) console.error(`  ... and ${missing.length - 10} more.`);
    hasErrors = true;
  } else {
    console.log(`Language '${lang}' has 100% complete keys (${langKeys.size}/${baseKeys.size}).`);
  }
});

if (hasErrors) {
  console.error('i18n completeness check FAILED.');
  process.exit(1);
} else {
  console.log('All 5 languages (en, ta, hi, te, ml) have 100% key parity! Check PASSED.');
}

