'use client';
import { useEffect,useRef } from 'react';
import type { CSSProperties } from 'react';
export function Cosmos(){const root=useRef<HTMLDivElement>(null);useEffect(()=>{const update=()=>root.current?.setAttribute('data-paused',String(document.hidden));update();document.addEventListener('visibilitychange',update);return()=>document.removeEventListener('visibilitychange',update)},[]);return <div className="cosmos" ref={root} aria-hidden="true"><div className="cosmos-nebula"/><div className="cosmos-stars">{Array.from({length:130},(_,i)=><i key={i} style={{left:((i*73.37)%100)+'%',top:((i*41.19+7)%100)+'%','--star-size':(i%8===0?2.4:1.2)+'px','--twinkle-time':(2+i%7)+'s','--twinkle-delay':(-i%13)+'s'} as CSSProperties}/>)}</div></div>}
