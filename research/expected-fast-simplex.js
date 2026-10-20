const fs=require('fs');
const arg=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const nv=arg.c.length,nr=arg.b.length,width=nv+nr+1;
let rows=arg.A.map((r,i)=>{let a=new Float64Array(width);a.set(r);a[nv+i]=1;a[width-1]=arg.b[i];return a});
let obj=new Float64Array(width);arg.c.forEach((x,i)=>obj[i]=-x);
let bases=Array.from({length:nr},(_,i)=>nv+i);
let count=0;
for(;count<20000;count++){
 let enter=-1;
 for(let j=0;j<width-1;j++){if(obj[j]<-1e-9){enter=j;break}}
 if(enter<0)break;
 let pivot=-1,ratio=Infinity,base=Infinity;
 for(let i=0;i<nr;i++){let row=rows[i];if(row[enter]<=1e-9)continue;let v=row[width-1]/row[enter];if(v<ratio-1e-12||(Math.abs(v-ratio)<1e-12&&bases[i]<base)){pivot=i;ratio=v;base=bases[i]}}
 if(pivot<0)throw Error('unbounded');
 let prow=rows[pivot],scale=prow[enter];for(let j=0;j<width;j++)prow[j]/=scale;
 for(let i=0;i<nr;i++)if(i!=pivot){let a=rows[i],f=a[enter];if(Math.abs(f)>1e-12)for(let j=0;j<width;j++)a[j]-=f*prow[j]}
 let factor=obj[enter];for(let j=0;j<width;j++)obj[j]-=factor*prow[j];bases[pivot]=enter;
}
if(count==20000)throw Error('iterations');
let solution=Array(nv).fill(0);for(let i=0;i<nr;i++)if(bases[i]<nv)solution[bases[i]]=rows[i][width-1];
process.stdout.write(JSON.stringify({value:obj[width-1],solution,iterations:count}));
