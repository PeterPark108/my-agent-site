// The managed preview supplies Vite-style flags. Translate for the retained Next app.
import {spawn} from 'node:child_process';
const input=process.argv.slice(2),args=[];
for(let i=0;i<input.length;i++){const arg=input[i];if(arg==='--strictPort')continue;args.push(arg==='--host'?'--hostname':arg);}
const child=spawn(process.execPath,['node_modules/next/dist/bin/next','dev',...args],{stdio:'inherit',env:{...process.env,MYAGENT_LOCAL_QA:'1'}});
for(const signal of ['SIGINT','SIGTERM'])process.on(signal,()=>child.kill(signal));
child.on('exit',code=>process.exit(code??0));
