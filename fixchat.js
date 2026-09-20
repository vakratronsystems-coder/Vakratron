// Har page se purana inline chat code hataakar sabko /vakra-chat.js se jodta hai.
// Chalao:  node fixchat.js          -> sirf list dikhayega, kuch nahi badlega
//          node fixchat.js --apply  -> backup banakar changes karega
const fs = require('fs'), path = require('path');
const APPLY = process.argv.includes('--apply');
const ROOT = process.cwd(), DIRS = ['views', 'public'];
const TAG = '<script src="/vakra-chat.js"></script>';

function walk(dir, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const f = path.join(dir, e.name);
    if (e.isDirectory()) {
      if (e.name === 'node_modules' || e.name.startsWith('_backup_')) continue;
      walk(f, out);
    } else if (e.name.toLowerCase().endsWith('.html')) out.push(f);
  }
  return out;
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const e of fs.readdirSync(src, { withFileTypes: true })) {
    if (e.name === 'node_modules' || e.name.startsWith('_backup_')) continue;
    const s = path.join(src, e.name), d = path.join(dest, e.name);
    e.isDirectory() ? copyDir(s, d) : fs.copyFileSync(s, d);
  }
}

function fix(html) {
  let scripts = 0, styles = 0, added = false;
  // Sirf wahi <script> hatao jisme src nahi hai AUR jisme /api/chat likha hai
  let out = html.replace(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi, (m, a, b) =>
    (/\bsrc\s*=/i.test(a) || !b.includes('/api/chat')) ? m : (scripts++, ''));
  // Chat ke apne style blocks (vakra-chat.js khud inject karta hai)
  out = out.replace(/<style\b([^>]*)>([\s\S]*?)<\/style>/gi, (m, a, b) =>
    ['#chatTrigger', '.vakra-chat-window', '.vakra-msg'].some(k => b.includes(k)) ? (styles++, '') : m);
  // Shared tag ek hi baar, aur sirf un pages mein jinme pehle chat tha
  const hasTag = /<script[^>]*\bsrc\s*=\s*["'][^"']*vakra-chat\.js["']/i.test(out);
  if (!hasTag && scripts > 0) {
    out = /<\/body\s*>/i.test(out) ? out.replace(/<\/body\s*>/i, `    ${TAG}\n</body>`) : out + `\n${TAG}\n`;
    added = true;
  }
  out = out.replace(/\n[ \t]*\n[ \t]*\n+/g, '\n\n');
  return { out, scripts, styles, added, hasTag };
}

console.log(APPLY ? '\nAPPLY MODE - files badlenge\n' : '\nDRY RUN - kuch nahi badlega\n');
const files = DIRS.flatMap(d => walk(path.join(ROOT, d)));
if (!files.length) { console.log('Koi .html nahi mili. Project root se chalao (jahan views/ aur public/ hain).'); process.exit(1); }

const plan = [];
let clean = 0;
for (const f of files) {
  const html = fs.readFileSync(f, 'utf8'), r = fix(html);
  if (r.scripts || r.styles || r.added) plan.push({ f, ...r, saved: html.length - r.out.length });
  else clean++;
}
if (!plan.length) { console.log(`Kuch karne ko nahi - ${files.length} pages mein inline chat nahi mila.`); process.exit(0); }

if (APPLY) {
  const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const bk = path.join(ROOT, `_backup_chatfix_${stamp}`);
  for (const d of DIRS) if (fs.existsSync(path.join(ROOT, d))) copyDir(path.join(ROOT, d), path.join(bk, d));
  console.log(`Backup: ${path.basename(bk)}\n`);
}

for (const p of plan) {
  const bits = [];
  if (p.scripts) bits.push(`${p.scripts} inline script`);
  if (p.styles) bits.push(`${p.styles} style block`);
  if (p.added) bits.push('shared tag added');
  if (p.hasTag) bits.push('tag pehle se tha');
  console.log(`  ${path.relative(ROOT, p.f)}`);
  console.log(`     ${bits.join(', ')}  (-${p.saved} chars)`);
  if (APPLY) fs.writeFileSync(p.f, p.out, 'utf8');
}

console.log(`\n${plan.length} page ${APPLY ? 'update ho gaye' : 'update honge'}, ${clean} pehle se theek.`);
console.log(APPLY
  ? '\nServer restart karke 3-4 pages check karo.\nUndo: views/ aur public/ delete karke _backup_chatfix_... se wapas copy karo.'
  : '\nKuch nahi badla. List theek lage toh chalao:\n  node fixchat.js --apply');