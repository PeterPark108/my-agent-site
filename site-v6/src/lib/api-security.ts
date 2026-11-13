import { createHash } from 'node:crypto';
import type { NextRequest } from 'next/server';

export class ApiError extends Error {
  constructor(public status:number,message:string,public retryAfter?:number){super(message)}
}
export function failure(error:unknown){
  const e=error instanceof ApiError?error:new ApiError(503,'Dịch vụ tạm thời chưa sẵn sàng. Vui lòng thử lại.');
  return Response.json({ok:false,error:e.message},{status:e.status,headers:{'Cache-Control':'no-store',...(e.retryAfter?{'Retry-After':String(e.retryAfter)}:{})}});
}
export async function readJson(request:NextRequest,maxBytes:number):Promise<Record<string,unknown>>{
  const origin=request.headers.get('origin');
  if(origin){let same=false;try{same=new URL(origin).origin===(process.env.MYAGENT_PUBLIC_ORIGIN||request.nextUrl.protocol+'//'+(request.headers.get('host')||request.nextUrl.host))}catch{}if(!same)throw new ApiError(403,'Yêu cầu không được phép.');}
  if(request.headers.get('sec-fetch-site')==='cross-site')throw new ApiError(403,'Yêu cầu không được phép.');
  if(request.headers.get('content-type')?.split(';')[0].trim()!=='application/json')throw new ApiError(415,'Yêu cầu JSON.');
  if(Number(request.headers.get('content-length'))>maxBytes)throw new ApiError(413,'Dữ liệu quá lớn.');
  const reader=request.body?.getReader();if(!reader)throw new ApiError(400,'Thiếu dữ liệu.');
  const chunks:Uint8Array[]=[];let size=0;let timer:ReturnType<typeof setTimeout>|undefined;
  const timeout=new Promise<never>((_,reject)=>{timer=setTimeout(()=>{void reader.cancel();reject(new ApiError(408,'Yêu cầu quá thời gian.'));},5000)});
  try{
    while(true){const {done,value}=await Promise.race([reader.read(),timeout]);if(done)break;size+=value.byteLength;if(size>maxBytes){void reader.cancel();throw new ApiError(413,'Dữ liệu quá lớn.');}chunks.push(value);}
    let value:unknown;try{value=JSON.parse(Buffer.concat(chunks).toString('utf8'))}catch{throw new ApiError(400,'JSON không hợp lệ.');}
    if(!value||typeof value!=='object'||Array.isArray(value))throw new ApiError(400,'Dữ liệu không hợp lệ.');
    return value as Record<string,unknown>;
  }finally{clearTimeout(timer);reader.releaseLock();}
}
export function onlyFields(input:Record<string,unknown>,fields:string[]){if(Object.keys(input).some(k=>!fields.includes(k)))throw new ApiError(400,'Trường dữ liệu không hợp lệ.');}
export function textField(input:Record<string,unknown>,key:string,max:number){const value=input[key];if(value===undefined)return '';if(typeof value!=='string'||value.length>max)throw new ApiError(400,'Trường dữ liệu không hợp lệ.');return value.trim();}
const local=new Map<string,{count:number;until:number}>();
const pending=new Map<string,number>();
function localOnly(){return process.env.NODE_ENV!=='production'||process.env.MYAGENT_LOCAL_QA==='1';}
async function redis(command:(string|number)[]){
  const endpoint=process.env.MYAGENT_REDIS_REST_URL,token=process.env.MYAGENT_REDIS_REST_TOKEN;
  if(!endpoint||!token)throw new ApiError(503,'Dịch vụ đang được cấu hình. Vui lòng liên hệ trực tiếp.');
  const url=new URL(endpoint);if(url.protocol!=='https:'||url.username||url.password)throw new ApiError(503,'Dịch vụ chưa sẵn sàng.');
  const r=await fetch(url,{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json'},body:JSON.stringify(command),signal:AbortSignal.timeout(2500),cache:'no-store',redirect:'error'});
  if(!r.ok)throw new ApiError(503,'Dịch vụ tạm thời chưa sẵn sàng.');const body=await r.json();if(body.error)throw new ApiError(503,'Dịch vụ tạm thời chưa sẵn sàng.');return body.result;
}
export async function consume(key:string,limit:number,seconds:number){
  if(!localOnly()){
    const lua="local n=redis.call('INCR',KEYS[1]); if n==1 then redis.call('EXPIRE',KEYS[1],ARGV[1]) end; return n";
    const n=await redis(['EVAL',lua,1,'myagent:rate:'+key,seconds]);if(!Number.isInteger(n))throw new ApiError(503,'Dịch vụ tạm thời chưa sẵn sàng.');if(n>limit)throw new ApiError(429,'Bạn thao tác quá nhanh. Vui lòng thử lại sau.',seconds);return;
  }
  const now=Date.now();for(const [k,v] of local)if(v.until<=now)local.delete(k);
  const entry=local.get(key)||{count:0,until:now+seconds*1000};entry.count++;local.set(key,entry);
  if(entry.count>limit)throw new ApiError(429,'Bạn thao tác quá nhanh. Vui lòng thử lại sau.',Math.ceil((entry.until-now)/1000));
}
export async function guard(request:NextRequest,kind:string,limit:number){
  // Only configure this header when the trusted edge OVERWRITES it. Otherwise use a shared bucket.
  const header=process.env.MYAGENT_TRUSTED_IP_HEADER;
  const client=header?request.headers.get(header)?.slice(0,128)||'shared':'shared';
  const identity=createHash('sha256').update(client).digest('hex');
  await consume(kind+':all',kind==='quote'?60:120,60);
  await consume(kind+':'+identity,limit,60);
}
export function enter(kind:string,limit:number){const n=pending.get(kind)||0;if(n>=limit)throw new ApiError(429,'Dịch vụ đang bận. Vui lòng thử lại.',10);pending.set(kind,n+1);return ()=>pending.set(kind,Math.max(0,(pending.get(kind)||1)-1));}
export async function reserveDuplicate(value:unknown){
 const key='contact:'+createHash('sha256').update(JSON.stringify(value)).digest('hex');
 if(!localOnly()){const result=await redis(['SET','myagent:duplicate:'+key,'1','NX','EX',60]);if(result!==null&&result!=='OK')throw new ApiError(503,'Dịch vụ tạm thời chưa sẵn sàng.');if(result===null)throw new ApiError(409,'Yêu cầu vừa được gửi. Vui lòng chờ trước khi gửi lại.',60);}
 else await consume(key,1,60);
 return async()=>{if(!localOnly())await redis(['DEL','myagent:duplicate:'+key]);else local.delete(key);};
}
export function backend(request:NextRequest,path:string){
 const origin=process.env.MYAGENT_BACKEND_ORIGIN;if(!origin)throw new ApiError(503,'Dịch vụ đang được cấu hình. Vui lòng liên hệ trực tiếp.');
 const url=new URL(origin);if(url.protocol!=='https:'||url.username||url.password||url.origin===request.nextUrl.origin||url.hostname===request.nextUrl.hostname||url.host===(request.headers.get('host')||request.nextUrl.host)||url.origin===process.env.MYAGENT_PUBLIC_ORIGIN)throw new ApiError(503,'Dịch vụ chưa sẵn sàng.');
 return new URL(path,url.origin);
}
