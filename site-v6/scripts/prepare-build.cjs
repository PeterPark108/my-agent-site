const fs=require('fs'),path=require('path');
if(process.platform==='win32')fs.mkdirSync(path.resolve('.next-v5/server/app/_not-found.segments/_not-found'),{recursive:true});
