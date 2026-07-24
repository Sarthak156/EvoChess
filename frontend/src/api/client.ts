const BASE=import.meta.env.VITE_API_URL||'http://localhost:8000/api';
export const api={get:(p:string)=>fetch(BASE+p).then(r=>r.json()),post:(p:string,b:unknown)=>fetch(BASE+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b)}).then(async r=>{const j=await r.json();if(!r.ok)throw Error(j.detail);return j})};
export type Match={id:number;fen:string;turn:string;status:string;result:string;moves:{uci:string;san:string}[];legal_moves:string[];explanation:string;active_rules:{id:number;name:string;description:string}[]}
