const { chromium } = require('playwright');
const [,, base, out, title] = process.argv;
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+base+'-cover.html',{waitUntil:'networkidle'});await p.pdf({path:base+'-cover.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
await p.goto('file://'+base+'.html',{waitUntil:'networkidle'});await p.waitForTimeout(300);
const hdr='<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5pt;color:#94a3b8;padding:0 17mm;display:flex;justify-content:space-between"><span>VAKRATRON SYSTEMS</span><span>'+title+'</span></div>';
const ftr='<div style="width:100%;font-family:Inter,sans-serif;font-size:7.5pt;color:#94a3b8;padding:0 17mm;display:flex;justify-content:space-between"><span>vakratronsys.com</span><span>Page <span class="pageNumber"></span></span></div>';
await p.pdf({path:base+'-body.pdf',format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:hdr,footerTemplate:ftr,preferCSSPageSize:true});
await b.close();})();
