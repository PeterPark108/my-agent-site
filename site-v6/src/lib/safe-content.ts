import sanitizeHtml from 'sanitize-html';
// Only the checked-in content inventory enters this renderer. Keep an explicit
// allowlist as a second boundary; do not route customer/chat HTML through it.
export function safeContent(html:string){return sanitizeHtml(html,{
 allowedTags:[...sanitizeHtml.defaults.allowedTags,'img','picture','source','svg','path','rect','circle','ellipse','g','text','title','desc','form','input','select','option','optgroup','textarea','label','button','fieldset','legend','output','details','summary','noscript'],
 allowedAttributes:{
  '*':['id','class','role','aria-*','data-*','tabindex','hidden'],
  a:['href','target','rel'],img:['src','srcset','sizes','alt','width','height','loading','decoding','fetchpriority'],source:['srcset','sizes','media','type'],
  form:['method','action','novalidate','autocomplete'],input:['type','name','value','placeholder','required','maxlength','minlength','min','max','step','autocomplete','inputmode','pattern','readonly','autocapitalize','spellcheck'],
  select:['name','required'],option:['value','selected'],optgroup:['label'],textarea:['name','rows','maxlength','placeholder','required'],label:['for'],button:['type','disabled'],
  svg:['viewBox','width','height','fill','stroke','stroke-width','stroke-linecap','stroke-linejoin','focusable','preserveAspectRatio'],
  path:['d','fill','stroke','stroke-width','stroke-linecap','stroke-linejoin'],rect:['x','y','width','height','rx','ry','fill','stroke','opacity'],circle:['cx','cy','r','fill','stroke','opacity'],ellipse:['cx','cy','rx','ry','fill','stroke'],g:['fill','stroke','opacity'],text:['x','y','fill','font-size','text-anchor'],time:['datetime'],th:['scope','colspan','rowspan'],td:['colspan','rowspan'],
 },
 allowedSchemes:['https','http','mailto','tel'],allowProtocolRelative:false,
 parser:{lowerCaseAttributeNames:false},
 transformTags:{a:(tagName,attribs)=>({tagName,attribs:{...attribs,...(attribs.target==='_blank'?{rel:'noopener noreferrer'}:{})}})},
});}
