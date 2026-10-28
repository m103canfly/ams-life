/* ams-life brain map (AGPL-3.0). Built by tools/brain/build.mjs; source in tools/brain/src/. Third-party licenses: licenses/. */
(()=>{var Dm=Object.defineProperty;var Fm=(i,t,e)=>t in i?Dm(i,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):i[t]=e;var q=(i,t,e)=>Fm(i,typeof t!="symbol"?t+"":t,e);var vo="184",Nn={LEFT:0,MIDDLE:1,RIGHT:2,ROTATE:0,DOLLY:1,PAN:2},Ni={ROTATE:0,PAN:1,DOLLY_PAN:2,DOLLY_ROTATE:3},Qu=0,Fc=1,tf=2;var Pr=1,ef=2,ks=3,ai=0,je=1,Xn=2,wn=0,Gn=1,Dn=2,Uc=3,Oc=4,nf=5;var Ai=100,sf=101,rf=102,af=103,of=104,lf=200,cf=201,hf=202,uf=203,Fa=204,Ua=205,ff=206,df=207,pf=208,mf=209,gf=210,_f=211,xf=212,vf=213,yf=214,Oa=0,Ba=1,ka=2,is=3,za=4,Va=5,Ga=6,Ha=7,Bc=0,Mf=1,bf=2,xn=0,Ir=1,Lr=2,Nr=3,Di=4,Dr=5,Fr=6,Ur=7;var kc=300,Fi=301,os=302,yo=303,Mo=304,Or=306,Wa=1e3,Vn=1001,Xa=1002,Be=1003,Sf=1004;var Br=1005;var Ge=1006,bo=1007;var Ui=1008;var vn=1009,zc=1010,Vc=1011,zs=1012,So=1013,Fn=1014,Un=1015,Ze=1016,wo=1017,Ao=1018,Vs=1020,Gc=35902,Hc=35899,Wc=1021,Xc=1022,An=1023,Hn=1026,Oi=1027,qc=1028,To=1029,Bi=1030,Eo=1031;var Co=1033,kr=33776,zr=33777,Vr=33778,Gr=33779,Ro=35840,Po=35841,Io=35842,Lo=35843,No=36196,Do=37492,Fo=37496,Uo=37488,Oo=37489,Hr=37490,Bo=37491,ko=37808,zo=37809,Vo=37810,Go=37811,Ho=37812,Wo=37813,Xo=37814,qo=37815,Yo=37816,Zo=37817,Ko=37818,Jo=37819,$o=37820,jo=37821,Qo=36492,tl=36494,el=36495,nl=36283,il=36284,Wr=36285,sl=36286;var hr=2300,qa=2301,Da=2302,Tc=2303,Ec=2400,Cc=2401,Rc=2402;var wf=3200;var Yc=0,Af=1,ui="",mn="srgb",ur="srgb-linear",fr="linear",jt="srgb";var ns=7680;var Pc=519,Tf=512,Ef=513,Cf=514,rl=515,Rf=516,Pf=517,al=518,If=519,Ic=35044,ki=35048;var Zc="300 es",In=2e3,dr=2001;function Um(i){for(let t=i.length-1;t>=0;--t)if(i[t]>=65535)return!0;return!1}function Om(i){return ArrayBuffer.isView(i)&&!(i instanceof DataView)}function pr(i){return document.createElementNS("http://www.w3.org/1999/xhtml",i)}function Lf(){let i=pr("canvas");return i.style.display="block",i}var Tu={},Ns=null;function Kc(...i){let t="THREE."+i.shift();Ns?Ns("log",t,...i):console.log(t,...i)}function Nf(i){let t=i[0];if(typeof t=="string"&&t.startsWith("TSL:")){let e=i[1];e&&e.isStackTrace?i[0]+=" "+e.getLocation():i[1]='Stack trace not available. Enable "THREE.Node.captureStackTrace" to capture stack traces.'}return i}function Ct(...i){i=Nf(i);let t="THREE."+i.shift();if(Ns)Ns("warn",t,...i);else{let e=i[0];e&&e.isStackTrace?console.warn(e.getError(t)):console.warn(t,...i)}}function Pt(...i){i=Nf(i);let t="THREE."+i.shift();if(Ns)Ns("error",t,...i);else{let e=i[0];e&&e.isStackTrace?console.error(e.getError(t)):console.error(t,...i)}}function Ya(...i){let t=i.join(" ");t in Tu||(Tu[t]=!0,Ct(...i))}function Df(i,t,e){return new Promise(function(n,s){function r(){switch(i.clientWaitSync(t,i.SYNC_FLUSH_COMMANDS_BIT,0)){case i.WAIT_FAILED:s();break;case i.TIMEOUT_EXPIRED:setTimeout(r,e);break;default:n()}}setTimeout(r,e)})}var Ff={[Oa]:Ba,[ka]:Ga,[za]:Ha,[is]:Va,[Ba]:Oa,[Ga]:ka,[Ha]:za,[Va]:is},Ln=class{addEventListener(t,e){this._listeners===void 0&&(this._listeners={});let n=this._listeners;n[t]===void 0&&(n[t]=[]),n[t].indexOf(e)===-1&&n[t].push(e)}hasEventListener(t,e){let n=this._listeners;return n===void 0?!1:n[t]!==void 0&&n[t].indexOf(e)!==-1}removeEventListener(t,e){let n=this._listeners;if(n===void 0)return;let s=n[t];if(s!==void 0){let r=s.indexOf(e);r!==-1&&s.splice(r,1)}}dispatchEvent(t){let e=this._listeners;if(e===void 0)return;let n=e[t.type];if(n!==void 0){t.target=this;let s=n.slice(0);for(let r=0,a=s.length;r<a;r++)s[r].call(this,t);t.target=null}}},Xe=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"],Eu=1234567,lr=Math.PI/180,Ds=180/Math.PI;function Gs(){let i=Math.random()*4294967295|0,t=Math.random()*4294967295|0,e=Math.random()*4294967295|0,n=Math.random()*4294967295|0;return(Xe[i&255]+Xe[i>>8&255]+Xe[i>>16&255]+Xe[i>>24&255]+"-"+Xe[t&255]+Xe[t>>8&255]+"-"+Xe[t>>16&15|64]+Xe[t>>24&255]+"-"+Xe[e&63|128]+Xe[e>>8&255]+"-"+Xe[e>>16&255]+Xe[e>>24&255]+Xe[n&255]+Xe[n>>8&255]+Xe[n>>16&255]+Xe[n>>24&255]).toLowerCase()}function Vt(i,t,e){return Math.max(t,Math.min(e,i))}function Jc(i,t){return(i%t+t)%t}function Bm(i,t,e,n,s){return n+(i-t)*(s-n)/(e-t)}function km(i,t,e){return i!==t?(e-i)/(t-i):0}function cr(i,t,e){return(1-e)*i+e*t}function zm(i,t,e,n){return cr(i,t,1-Math.exp(-e*n))}function Vm(i,t=1){return t-Math.abs(Jc(i,t*2)-t)}function Gm(i,t,e){return i<=t?0:i>=e?1:(i=(i-t)/(e-t),i*i*(3-2*i))}function Hm(i,t,e){return i<=t?0:i>=e?1:(i=(i-t)/(e-t),i*i*i*(i*(i*6-15)+10))}function Wm(i,t){return i+Math.floor(Math.random()*(t-i+1))}function Xm(i,t){return i+Math.random()*(t-i)}function qm(i){return i*(.5-Math.random())}function Ym(i){i!==void 0&&(Eu=i);let t=Eu+=1831565813;return t=Math.imul(t^t>>>15,t|1),t^=t+Math.imul(t^t>>>7,t|61),((t^t>>>14)>>>0)/4294967296}function Zm(i){return i*lr}function Km(i){return i*Ds}function Jm(i){return(i&i-1)===0&&i!==0}function $m(i){return Math.pow(2,Math.ceil(Math.log(i)/Math.LN2))}function jm(i){return Math.pow(2,Math.floor(Math.log(i)/Math.LN2))}function Qm(i,t,e,n,s){let r=Math.cos,a=Math.sin,o=r(e/2),l=a(e/2),c=r((t+n)/2),h=a((t+n)/2),f=r((t-n)/2),u=a((t-n)/2),d=r((n-t)/2),m=a((n-t)/2);switch(s){case"XYX":i.set(o*h,l*f,l*u,o*c);break;case"YZY":i.set(l*u,o*h,l*f,o*c);break;case"ZXZ":i.set(l*f,l*u,o*h,o*c);break;case"XZX":i.set(o*h,l*m,l*d,o*c);break;case"YXY":i.set(l*d,o*h,l*m,o*c);break;case"ZYZ":i.set(l*m,l*d,o*h,o*c);break;default:Ct("MathUtils: .setQuaternionFromProperEuler() encountered an unknown order: "+s)}}function Is(i,t){switch(t.constructor){case Float32Array:return i;case Uint32Array:return i/4294967295;case Uint16Array:return i/65535;case Uint8Array:return i/255;case Int32Array:return Math.max(i/2147483647,-1);case Int16Array:return Math.max(i/32767,-1);case Int8Array:return Math.max(i/127,-1);default:throw new Error("Invalid component type.")}}function $e(i,t){switch(t.constructor){case Float32Array:return i;case Uint32Array:return Math.round(i*4294967295);case Uint16Array:return Math.round(i*65535);case Uint8Array:return Math.round(i*255);case Int32Array:return Math.round(i*2147483647);case Int16Array:return Math.round(i*32767);case Int8Array:return Math.round(i*127);default:throw new Error("Invalid component type.")}}var $c={DEG2RAD:lr,RAD2DEG:Ds,generateUUID:Gs,clamp:Vt,euclideanModulo:Jc,mapLinear:Bm,inverseLerp:km,lerp:cr,damp:zm,pingpong:Vm,smoothstep:Gm,smootherstep:Hm,randInt:Wm,randFloat:Xm,randFloatSpread:qm,seededRandom:Ym,degToRad:Zm,radToDeg:Km,isPowerOfTwo:Jm,ceilPowerOfTwo:$m,floorPowerOfTwo:jm,setQuaternionFromProperEuler:Qm,normalize:$e,denormalize:Is},ih=class ih{constructor(t=0,e=0){this.x=t,this.y=e}get width(){return this.x}set width(t){this.x=t}get height(){return this.y}set height(t){this.y=t}set(t,e){return this.x=t,this.y=e,this}setScalar(t){return this.x=t,this.y=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y)}copy(t){return this.x=t.x,this.y=t.y,this}add(t){return this.x+=t.x,this.y+=t.y,this}addScalar(t){return this.x+=t,this.y+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this}subScalar(t){return this.x-=t,this.y-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this}multiply(t){return this.x*=t.x,this.y*=t.y,this}multiplyScalar(t){return this.x*=t,this.y*=t,this}divide(t){return this.x/=t.x,this.y/=t.y,this}divideScalar(t){return this.multiplyScalar(1/t)}applyMatrix3(t){let e=this.x,n=this.y,s=t.elements;return this.x=s[0]*e+s[3]*n+s[6],this.y=s[1]*e+s[4]*n+s[7],this}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this}clamp(t,e){return this.x=Vt(this.x,t.x,e.x),this.y=Vt(this.y,t.y,e.y),this}clampScalar(t,e){return this.x=Vt(this.x,t,e),this.y=Vt(this.y,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(Vt(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(t){return this.x*t.x+this.y*t.y}cross(t){return this.x*t.y-this.y*t.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(t){let e=Math.sqrt(this.lengthSq()*t.lengthSq());if(e===0)return Math.PI/2;let n=this.dot(t)/e;return Math.acos(Vt(n,-1,1))}distanceTo(t){return Math.sqrt(this.distanceToSquared(t))}distanceToSquared(t){let e=this.x-t.x,n=this.y-t.y;return e*e+n*n}manhattanDistanceTo(t){return Math.abs(this.x-t.x)+Math.abs(this.y-t.y)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this}equals(t){return t.x===this.x&&t.y===this.y}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this}rotateAround(t,e){let n=Math.cos(e),s=Math.sin(e),r=this.x-t.x,a=this.y-t.y;return this.x=r*n-a*s+t.x,this.y=r*s+a*n+t.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}};ih.prototype.isVector2=!0;var Et=ih,gn=class{constructor(t=0,e=0,n=0,s=1){this.isQuaternion=!0,this._x=t,this._y=e,this._z=n,this._w=s}static slerpFlat(t,e,n,s,r,a,o){let l=n[s+0],c=n[s+1],h=n[s+2],f=n[s+3],u=r[a+0],d=r[a+1],m=r[a+2],_=r[a+3];if(f!==_||l!==u||c!==d||h!==m){let g=l*u+c*d+h*m+f*_;g<0&&(u=-u,d=-d,m=-m,_=-_,g=-g);let p=1-o;if(g<.9995){let y=Math.acos(g),S=Math.sin(y);p=Math.sin(p*y)/S,o=Math.sin(o*y)/S,l=l*p+u*o,c=c*p+d*o,h=h*p+m*o,f=f*p+_*o}else{l=l*p+u*o,c=c*p+d*o,h=h*p+m*o,f=f*p+_*o;let y=1/Math.sqrt(l*l+c*c+h*h+f*f);l*=y,c*=y,h*=y,f*=y}}t[e]=l,t[e+1]=c,t[e+2]=h,t[e+3]=f}static multiplyQuaternionsFlat(t,e,n,s,r,a){let o=n[s],l=n[s+1],c=n[s+2],h=n[s+3],f=r[a],u=r[a+1],d=r[a+2],m=r[a+3];return t[e]=o*m+h*f+l*d-c*u,t[e+1]=l*m+h*u+c*f-o*d,t[e+2]=c*m+h*d+o*u-l*f,t[e+3]=h*m-o*f-l*u-c*d,t}get x(){return this._x}set x(t){this._x=t,this._onChangeCallback()}get y(){return this._y}set y(t){this._y=t,this._onChangeCallback()}get z(){return this._z}set z(t){this._z=t,this._onChangeCallback()}get w(){return this._w}set w(t){this._w=t,this._onChangeCallback()}set(t,e,n,s){return this._x=t,this._y=e,this._z=n,this._w=s,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(t){return this._x=t.x,this._y=t.y,this._z=t.z,this._w=t.w,this._onChangeCallback(),this}setFromEuler(t,e=!0){let n=t._x,s=t._y,r=t._z,a=t._order,o=Math.cos,l=Math.sin,c=o(n/2),h=o(s/2),f=o(r/2),u=l(n/2),d=l(s/2),m=l(r/2);switch(a){case"XYZ":this._x=u*h*f+c*d*m,this._y=c*d*f-u*h*m,this._z=c*h*m+u*d*f,this._w=c*h*f-u*d*m;break;case"YXZ":this._x=u*h*f+c*d*m,this._y=c*d*f-u*h*m,this._z=c*h*m-u*d*f,this._w=c*h*f+u*d*m;break;case"ZXY":this._x=u*h*f-c*d*m,this._y=c*d*f+u*h*m,this._z=c*h*m+u*d*f,this._w=c*h*f-u*d*m;break;case"ZYX":this._x=u*h*f-c*d*m,this._y=c*d*f+u*h*m,this._z=c*h*m-u*d*f,this._w=c*h*f+u*d*m;break;case"YZX":this._x=u*h*f+c*d*m,this._y=c*d*f+u*h*m,this._z=c*h*m-u*d*f,this._w=c*h*f-u*d*m;break;case"XZY":this._x=u*h*f-c*d*m,this._y=c*d*f-u*h*m,this._z=c*h*m+u*d*f,this._w=c*h*f+u*d*m;break;default:Ct("Quaternion: .setFromEuler() encountered an unknown order: "+a)}return e===!0&&this._onChangeCallback(),this}setFromAxisAngle(t,e){let n=e/2,s=Math.sin(n);return this._x=t.x*s,this._y=t.y*s,this._z=t.z*s,this._w=Math.cos(n),this._onChangeCallback(),this}setFromRotationMatrix(t){let e=t.elements,n=e[0],s=e[4],r=e[8],a=e[1],o=e[5],l=e[9],c=e[2],h=e[6],f=e[10],u=n+o+f;if(u>0){let d=.5/Math.sqrt(u+1);this._w=.25/d,this._x=(h-l)*d,this._y=(r-c)*d,this._z=(a-s)*d}else if(n>o&&n>f){let d=2*Math.sqrt(1+n-o-f);this._w=(h-l)/d,this._x=.25*d,this._y=(s+a)/d,this._z=(r+c)/d}else if(o>f){let d=2*Math.sqrt(1+o-n-f);this._w=(r-c)/d,this._x=(s+a)/d,this._y=.25*d,this._z=(l+h)/d}else{let d=2*Math.sqrt(1+f-n-o);this._w=(a-s)/d,this._x=(r+c)/d,this._y=(l+h)/d,this._z=.25*d}return this._onChangeCallback(),this}setFromUnitVectors(t,e){let n=t.dot(e)+1;return n<1e-8?(n=0,Math.abs(t.x)>Math.abs(t.z)?(this._x=-t.y,this._y=t.x,this._z=0,this._w=n):(this._x=0,this._y=-t.z,this._z=t.y,this._w=n)):(this._x=t.y*e.z-t.z*e.y,this._y=t.z*e.x-t.x*e.z,this._z=t.x*e.y-t.y*e.x,this._w=n),this.normalize()}angleTo(t){return 2*Math.acos(Math.abs(Vt(this.dot(t),-1,1)))}rotateTowards(t,e){let n=this.angleTo(t);if(n===0)return this;let s=Math.min(1,e/n);return this.slerp(t,s),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(t){return this._x*t._x+this._y*t._y+this._z*t._z+this._w*t._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let t=this.length();return t===0?(this._x=0,this._y=0,this._z=0,this._w=1):(t=1/t,this._x=this._x*t,this._y=this._y*t,this._z=this._z*t,this._w=this._w*t),this._onChangeCallback(),this}multiply(t){return this.multiplyQuaternions(this,t)}premultiply(t){return this.multiplyQuaternions(t,this)}multiplyQuaternions(t,e){let n=t._x,s=t._y,r=t._z,a=t._w,o=e._x,l=e._y,c=e._z,h=e._w;return this._x=n*h+a*o+s*c-r*l,this._y=s*h+a*l+r*o-n*c,this._z=r*h+a*c+n*l-s*o,this._w=a*h-n*o-s*l-r*c,this._onChangeCallback(),this}slerp(t,e){let n=t._x,s=t._y,r=t._z,a=t._w,o=this.dot(t);o<0&&(n=-n,s=-s,r=-r,a=-a,o=-o);let l=1-e;if(o<.9995){let c=Math.acos(o),h=Math.sin(c);l=Math.sin(l*c)/h,e=Math.sin(e*c)/h,this._x=this._x*l+n*e,this._y=this._y*l+s*e,this._z=this._z*l+r*e,this._w=this._w*l+a*e,this._onChangeCallback()}else this._x=this._x*l+n*e,this._y=this._y*l+s*e,this._z=this._z*l+r*e,this._w=this._w*l+a*e,this.normalize();return this}slerpQuaternions(t,e,n){return this.copy(t).slerp(e,n)}random(){let t=2*Math.PI*Math.random(),e=2*Math.PI*Math.random(),n=Math.random(),s=Math.sqrt(1-n),r=Math.sqrt(n);return this.set(s*Math.sin(t),s*Math.cos(t),r*Math.sin(e),r*Math.cos(e))}equals(t){return t._x===this._x&&t._y===this._y&&t._z===this._z&&t._w===this._w}fromArray(t,e=0){return this._x=t[e],this._y=t[e+1],this._z=t[e+2],this._w=t[e+3],this._onChangeCallback(),this}toArray(t=[],e=0){return t[e]=this._x,t[e+1]=this._y,t[e+2]=this._z,t[e+3]=this._w,t}fromBufferAttribute(t,e){return this._x=t.getX(e),this._y=t.getY(e),this._z=t.getZ(e),this._w=t.getW(e),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(t){return this._onChangeCallback=t,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}},sh=class sh{constructor(t=0,e=0,n=0){this.x=t,this.y=e,this.z=n}set(t,e,n){return n===void 0&&(n=this.z),this.x=t,this.y=e,this.z=n,this}setScalar(t){return this.x=t,this.y=t,this.z=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setZ(t){return this.z=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;case 2:this.z=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(t){return this.x=t.x,this.y=t.y,this.z=t.z,this}add(t){return this.x+=t.x,this.y+=t.y,this.z+=t.z,this}addScalar(t){return this.x+=t,this.y+=t,this.z+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this.z=t.z+e.z,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this.z+=t.z*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this.z-=t.z,this}subScalar(t){return this.x-=t,this.y-=t,this.z-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this.z=t.z-e.z,this}multiply(t){return this.x*=t.x,this.y*=t.y,this.z*=t.z,this}multiplyScalar(t){return this.x*=t,this.y*=t,this.z*=t,this}multiplyVectors(t,e){return this.x=t.x*e.x,this.y=t.y*e.y,this.z=t.z*e.z,this}applyEuler(t){return this.applyQuaternion(Cu.setFromEuler(t))}applyAxisAngle(t,e){return this.applyQuaternion(Cu.setFromAxisAngle(t,e))}applyMatrix3(t){let e=this.x,n=this.y,s=this.z,r=t.elements;return this.x=r[0]*e+r[3]*n+r[6]*s,this.y=r[1]*e+r[4]*n+r[7]*s,this.z=r[2]*e+r[5]*n+r[8]*s,this}applyNormalMatrix(t){return this.applyMatrix3(t).normalize()}applyMatrix4(t){let e=this.x,n=this.y,s=this.z,r=t.elements,a=1/(r[3]*e+r[7]*n+r[11]*s+r[15]);return this.x=(r[0]*e+r[4]*n+r[8]*s+r[12])*a,this.y=(r[1]*e+r[5]*n+r[9]*s+r[13])*a,this.z=(r[2]*e+r[6]*n+r[10]*s+r[14])*a,this}applyQuaternion(t){let e=this.x,n=this.y,s=this.z,r=t.x,a=t.y,o=t.z,l=t.w,c=2*(a*s-o*n),h=2*(o*e-r*s),f=2*(r*n-a*e);return this.x=e+l*c+a*f-o*h,this.y=n+l*h+o*c-r*f,this.z=s+l*f+r*h-a*c,this}project(t){return this.applyMatrix4(t.matrixWorldInverse).applyMatrix4(t.projectionMatrix)}unproject(t){return this.applyMatrix4(t.projectionMatrixInverse).applyMatrix4(t.matrixWorld)}transformDirection(t){let e=this.x,n=this.y,s=this.z,r=t.elements;return this.x=r[0]*e+r[4]*n+r[8]*s,this.y=r[1]*e+r[5]*n+r[9]*s,this.z=r[2]*e+r[6]*n+r[10]*s,this.normalize()}divide(t){return this.x/=t.x,this.y/=t.y,this.z/=t.z,this}divideScalar(t){return this.multiplyScalar(1/t)}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this.z=Math.min(this.z,t.z),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this.z=Math.max(this.z,t.z),this}clamp(t,e){return this.x=Vt(this.x,t.x,e.x),this.y=Vt(this.y,t.y,e.y),this.z=Vt(this.z,t.z,e.z),this}clampScalar(t,e){return this.x=Vt(this.x,t,e),this.y=Vt(this.y,t,e),this.z=Vt(this.z,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(Vt(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(t){return this.x*t.x+this.y*t.y+this.z*t.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this.z+=(t.z-this.z)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this.z=t.z+(e.z-t.z)*n,this}cross(t){return this.crossVectors(this,t)}crossVectors(t,e){let n=t.x,s=t.y,r=t.z,a=e.x,o=e.y,l=e.z;return this.x=s*l-r*o,this.y=r*a-n*l,this.z=n*o-s*a,this}projectOnVector(t){let e=t.lengthSq();if(e===0)return this.set(0,0,0);let n=t.dot(this)/e;return this.copy(t).multiplyScalar(n)}projectOnPlane(t){return ec.copy(this).projectOnVector(t),this.sub(ec)}reflect(t){return this.sub(ec.copy(t).multiplyScalar(2*this.dot(t)))}angleTo(t){let e=Math.sqrt(this.lengthSq()*t.lengthSq());if(e===0)return Math.PI/2;let n=this.dot(t)/e;return Math.acos(Vt(n,-1,1))}distanceTo(t){return Math.sqrt(this.distanceToSquared(t))}distanceToSquared(t){let e=this.x-t.x,n=this.y-t.y,s=this.z-t.z;return e*e+n*n+s*s}manhattanDistanceTo(t){return Math.abs(this.x-t.x)+Math.abs(this.y-t.y)+Math.abs(this.z-t.z)}setFromSpherical(t){return this.setFromSphericalCoords(t.radius,t.phi,t.theta)}setFromSphericalCoords(t,e,n){let s=Math.sin(e)*t;return this.x=s*Math.sin(n),this.y=Math.cos(e)*t,this.z=s*Math.cos(n),this}setFromCylindrical(t){return this.setFromCylindricalCoords(t.radius,t.theta,t.y)}setFromCylindricalCoords(t,e,n){return this.x=t*Math.sin(e),this.y=n,this.z=t*Math.cos(e),this}setFromMatrixPosition(t){let e=t.elements;return this.x=e[12],this.y=e[13],this.z=e[14],this}setFromMatrixScale(t){let e=this.setFromMatrixColumn(t,0).length(),n=this.setFromMatrixColumn(t,1).length(),s=this.setFromMatrixColumn(t,2).length();return this.x=e,this.y=n,this.z=s,this}setFromMatrixColumn(t,e){return this.fromArray(t.elements,e*4)}setFromMatrix3Column(t,e){return this.fromArray(t.elements,e*3)}setFromEuler(t){return this.x=t._x,this.y=t._y,this.z=t._z,this}setFromColor(t){return this.x=t.r,this.y=t.g,this.z=t.b,this}equals(t){return t.x===this.x&&t.y===this.y&&t.z===this.z}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this.z=t[e+2],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t[e+2]=this.z,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this.z=t.getZ(e),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){let t=Math.random()*Math.PI*2,e=Math.random()*2-1,n=Math.sqrt(1-e*e);return this.x=n*Math.cos(t),this.y=e,this.z=n*Math.sin(t),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}};sh.prototype.isVector3=!0;var P=sh,ec=new P,Cu=new gn,rh=class rh{constructor(t,e,n,s,r,a,o,l,c){this.elements=[1,0,0,0,1,0,0,0,1],t!==void 0&&this.set(t,e,n,s,r,a,o,l,c)}set(t,e,n,s,r,a,o,l,c){let h=this.elements;return h[0]=t,h[1]=s,h[2]=o,h[3]=e,h[4]=r,h[5]=l,h[6]=n,h[7]=a,h[8]=c,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(t){let e=this.elements,n=t.elements;return e[0]=n[0],e[1]=n[1],e[2]=n[2],e[3]=n[3],e[4]=n[4],e[5]=n[5],e[6]=n[6],e[7]=n[7],e[8]=n[8],this}extractBasis(t,e,n){return t.setFromMatrix3Column(this,0),e.setFromMatrix3Column(this,1),n.setFromMatrix3Column(this,2),this}setFromMatrix4(t){let e=t.elements;return this.set(e[0],e[4],e[8],e[1],e[5],e[9],e[2],e[6],e[10]),this}multiply(t){return this.multiplyMatrices(this,t)}premultiply(t){return this.multiplyMatrices(t,this)}multiplyMatrices(t,e){let n=t.elements,s=e.elements,r=this.elements,a=n[0],o=n[3],l=n[6],c=n[1],h=n[4],f=n[7],u=n[2],d=n[5],m=n[8],_=s[0],g=s[3],p=s[6],y=s[1],S=s[4],b=s[7],T=s[2],w=s[5],R=s[8];return r[0]=a*_+o*y+l*T,r[3]=a*g+o*S+l*w,r[6]=a*p+o*b+l*R,r[1]=c*_+h*y+f*T,r[4]=c*g+h*S+f*w,r[7]=c*p+h*b+f*R,r[2]=u*_+d*y+m*T,r[5]=u*g+d*S+m*w,r[8]=u*p+d*b+m*R,this}multiplyScalar(t){let e=this.elements;return e[0]*=t,e[3]*=t,e[6]*=t,e[1]*=t,e[4]*=t,e[7]*=t,e[2]*=t,e[5]*=t,e[8]*=t,this}determinant(){let t=this.elements,e=t[0],n=t[1],s=t[2],r=t[3],a=t[4],o=t[5],l=t[6],c=t[7],h=t[8];return e*a*h-e*o*c-n*r*h+n*o*l+s*r*c-s*a*l}invert(){let t=this.elements,e=t[0],n=t[1],s=t[2],r=t[3],a=t[4],o=t[5],l=t[6],c=t[7],h=t[8],f=h*a-o*c,u=o*l-h*r,d=c*r-a*l,m=e*f+n*u+s*d;if(m===0)return this.set(0,0,0,0,0,0,0,0,0);let _=1/m;return t[0]=f*_,t[1]=(s*c-h*n)*_,t[2]=(o*n-s*a)*_,t[3]=u*_,t[4]=(h*e-s*l)*_,t[5]=(s*r-o*e)*_,t[6]=d*_,t[7]=(n*l-c*e)*_,t[8]=(a*e-n*r)*_,this}transpose(){let t,e=this.elements;return t=e[1],e[1]=e[3],e[3]=t,t=e[2],e[2]=e[6],e[6]=t,t=e[5],e[5]=e[7],e[7]=t,this}getNormalMatrix(t){return this.setFromMatrix4(t).invert().transpose()}transposeIntoArray(t){let e=this.elements;return t[0]=e[0],t[1]=e[3],t[2]=e[6],t[3]=e[1],t[4]=e[4],t[5]=e[7],t[6]=e[2],t[7]=e[5],t[8]=e[8],this}setUvTransform(t,e,n,s,r,a,o){let l=Math.cos(r),c=Math.sin(r);return this.set(n*l,n*c,-n*(l*a+c*o)+a+t,-s*c,s*l,-s*(-c*a+l*o)+o+e,0,0,1),this}scale(t,e){return this.premultiply(nc.makeScale(t,e)),this}rotate(t){return this.premultiply(nc.makeRotation(-t)),this}translate(t,e){return this.premultiply(nc.makeTranslation(t,e)),this}makeTranslation(t,e){return t.isVector2?this.set(1,0,t.x,0,1,t.y,0,0,1):this.set(1,0,t,0,1,e,0,0,1),this}makeRotation(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,-n,0,n,e,0,0,0,1),this}makeScale(t,e){return this.set(t,0,0,0,e,0,0,0,1),this}equals(t){let e=this.elements,n=t.elements;for(let s=0;s<9;s++)if(e[s]!==n[s])return!1;return!0}fromArray(t,e=0){for(let n=0;n<9;n++)this.elements[n]=t[n+e];return this}toArray(t=[],e=0){let n=this.elements;return t[e]=n[0],t[e+1]=n[1],t[e+2]=n[2],t[e+3]=n[3],t[e+4]=n[4],t[e+5]=n[5],t[e+6]=n[6],t[e+7]=n[7],t[e+8]=n[8],t}clone(){return new this.constructor().fromArray(this.elements)}};rh.prototype.isMatrix3=!0;var Ft=rh,nc=new Ft,Ru=new Ft().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),Pu=new Ft().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function tg(){let i={enabled:!0,workingColorSpace:ur,spaces:{},convert:function(s,r,a){return this.enabled===!1||r===a||!r||!a||(this.spaces[r].transfer===jt&&(s.r=ri(s.r),s.g=ri(s.g),s.b=ri(s.b)),this.spaces[r].primaries!==this.spaces[a].primaries&&(s.applyMatrix3(this.spaces[r].toXYZ),s.applyMatrix3(this.spaces[a].fromXYZ)),this.spaces[a].transfer===jt&&(s.r=Ls(s.r),s.g=Ls(s.g),s.b=Ls(s.b))),s},workingToColorSpace:function(s,r){return this.convert(s,this.workingColorSpace,r)},colorSpaceToWorking:function(s,r){return this.convert(s,r,this.workingColorSpace)},getPrimaries:function(s){return this.spaces[s].primaries},getTransfer:function(s){return s===ui?fr:this.spaces[s].transfer},getToneMappingMode:function(s){return this.spaces[s].outputColorSpaceConfig.toneMappingMode||"standard"},getLuminanceCoefficients:function(s,r=this.workingColorSpace){return s.fromArray(this.spaces[r].luminanceCoefficients)},define:function(s){Object.assign(this.spaces,s)},_getMatrix:function(s,r,a){return s.copy(this.spaces[r].toXYZ).multiply(this.spaces[a].fromXYZ)},_getDrawingBufferColorSpace:function(s){return this.spaces[s].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(s=this.workingColorSpace){return this.spaces[s].workingColorSpaceConfig.unpackColorSpace},fromWorkingColorSpace:function(s,r){return Ya("ColorManagement: .fromWorkingColorSpace() has been renamed to .workingToColorSpace()."),i.workingToColorSpace(s,r)},toWorkingColorSpace:function(s,r){return Ya("ColorManagement: .toWorkingColorSpace() has been renamed to .colorSpaceToWorking()."),i.colorSpaceToWorking(s,r)}},t=[.64,.33,.3,.6,.15,.06],e=[.2126,.7152,.0722],n=[.3127,.329];return i.define({[ur]:{primaries:t,whitePoint:n,transfer:fr,toXYZ:Ru,fromXYZ:Pu,luminanceCoefficients:e,workingColorSpaceConfig:{unpackColorSpace:mn},outputColorSpaceConfig:{drawingBufferColorSpace:mn}},[mn]:{primaries:t,whitePoint:n,transfer:jt,toXYZ:Ru,fromXYZ:Pu,luminanceCoefficients:e,outputColorSpaceConfig:{drawingBufferColorSpace:mn}}}),i}var Wt=tg();function ri(i){return i<.04045?i*.0773993808:Math.pow(i*.9478672986+.0521327014,2.4)}function Ls(i){return i<.0031308?i*12.92:1.055*Math.pow(i,.41666)-.055}var vs,Za=class{static getDataURL(t,e="image/png"){if(/^data:/i.test(t.src)||typeof HTMLCanvasElement>"u")return t.src;let n;if(t instanceof HTMLCanvasElement)n=t;else{vs===void 0&&(vs=pr("canvas")),vs.width=t.width,vs.height=t.height;let s=vs.getContext("2d");t instanceof ImageData?s.putImageData(t,0,0):s.drawImage(t,0,0,t.width,t.height),n=vs}return n.toDataURL(e)}static sRGBToLinear(t){if(typeof HTMLImageElement<"u"&&t instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&t instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&t instanceof ImageBitmap){let e=pr("canvas");e.width=t.width,e.height=t.height;let n=e.getContext("2d");n.drawImage(t,0,0,t.width,t.height);let s=n.getImageData(0,0,t.width,t.height),r=s.data;for(let a=0;a<r.length;a++)r[a]=ri(r[a]/255)*255;return n.putImageData(s,0,0),e}else if(t.data){let e=t.data.slice(0);for(let n=0;n<e.length;n++)e instanceof Uint8Array||e instanceof Uint8ClampedArray?e[n]=Math.floor(ri(e[n]/255)*255):e[n]=ri(e[n]);return{data:e,width:t.width,height:t.height}}else return Ct("ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),t}},eg=0,Fs=class{constructor(t=null){this.isSource=!0,Object.defineProperty(this,"id",{value:eg++}),this.uuid=Gs(),this.data=t,this.dataReady=!0,this.version=0}getSize(t){let e=this.data;return typeof HTMLVideoElement<"u"&&e instanceof HTMLVideoElement?t.set(e.videoWidth,e.videoHeight,0):typeof VideoFrame<"u"&&e instanceof VideoFrame?t.set(e.displayWidth,e.displayHeight,0):e!==null?t.set(e.width,e.height,e.depth||0):t.set(0,0,0),t}set needsUpdate(t){t===!0&&this.version++}toJSON(t){let e=t===void 0||typeof t=="string";if(!e&&t.images[this.uuid]!==void 0)return t.images[this.uuid];let n={uuid:this.uuid,url:""},s=this.data;if(s!==null){let r;if(Array.isArray(s)){r=[];for(let a=0,o=s.length;a<o;a++)s[a].isDataTexture?r.push(ic(s[a].image)):r.push(ic(s[a]))}else r=ic(s);n.url=r}return e||(t.images[this.uuid]=n),n}};function ic(i){return typeof HTMLImageElement<"u"&&i instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&i instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&i instanceof ImageBitmap?Za.getDataURL(i):i.data?{data:Array.from(i.data),width:i.width,height:i.height,type:i.data.constructor.name}:(Ct("Texture: Unable to serialize Texture."),{})}var ng=0,sc=new P,nn=class i extends Ln{constructor(t=i.DEFAULT_IMAGE,e=i.DEFAULT_MAPPING,n=Vn,s=Vn,r=Ge,a=Ui,o=An,l=vn,c=i.DEFAULT_ANISOTROPY,h=ui){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:ng++}),this.uuid=Gs(),this.name="",this.source=new Fs(t),this.mipmaps=[],this.mapping=e,this.channel=0,this.wrapS=n,this.wrapT=s,this.magFilter=r,this.minFilter=a,this.anisotropy=c,this.format=o,this.internalFormat=null,this.type=l,this.offset=new Et(0,0),this.repeat=new Et(1,1),this.center=new Et(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Ft,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=h,this.userData={},this.updateRanges=[],this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.isArrayTexture=!!(t&&t.depth&&t.depth>1),this.pmremVersion=0,this.normalized=!1}get width(){return this.source.getSize(sc).x}get height(){return this.source.getSize(sc).y}get depth(){return this.source.getSize(sc).z}get image(){return this.source.data}set image(t){this.source.data=t}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}addUpdateRange(t,e){this.updateRanges.push({start:t,count:e})}clearUpdateRanges(){this.updateRanges.length=0}clone(){return new this.constructor().copy(this)}copy(t){return this.name=t.name,this.source=t.source,this.mipmaps=t.mipmaps.slice(0),this.mapping=t.mapping,this.channel=t.channel,this.wrapS=t.wrapS,this.wrapT=t.wrapT,this.magFilter=t.magFilter,this.minFilter=t.minFilter,this.anisotropy=t.anisotropy,this.format=t.format,this.internalFormat=t.internalFormat,this.type=t.type,this.normalized=t.normalized,this.offset.copy(t.offset),this.repeat.copy(t.repeat),this.center.copy(t.center),this.rotation=t.rotation,this.matrixAutoUpdate=t.matrixAutoUpdate,this.matrix.copy(t.matrix),this.generateMipmaps=t.generateMipmaps,this.premultiplyAlpha=t.premultiplyAlpha,this.flipY=t.flipY,this.unpackAlignment=t.unpackAlignment,this.colorSpace=t.colorSpace,this.renderTarget=t.renderTarget,this.isRenderTargetTexture=t.isRenderTargetTexture,this.isArrayTexture=t.isArrayTexture,this.userData=JSON.parse(JSON.stringify(t.userData)),this.needsUpdate=!0,this}setValues(t){for(let e in t){let n=t[e];if(n===void 0){Ct(`Texture.setValues(): parameter '${e}' has value of undefined.`);continue}let s=this[e];if(s===void 0){Ct(`Texture.setValues(): property '${e}' does not exist.`);continue}s&&n&&s.isVector2&&n.isVector2||s&&n&&s.isVector3&&n.isVector3||s&&n&&s.isMatrix3&&n.isMatrix3?s.copy(n):this[e]=n}}toJSON(t){let e=t===void 0||typeof t=="string";if(!e&&t.textures[this.uuid]!==void 0)return t.textures[this.uuid];let n={metadata:{version:4.7,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(t).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,normalized:this.normalized,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(n.userData=this.userData),e||(t.textures[this.uuid]=n),n}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(t){if(this.mapping!==kc)return t;if(t.applyMatrix3(this.matrix),t.x<0||t.x>1)switch(this.wrapS){case Wa:t.x=t.x-Math.floor(t.x);break;case Vn:t.x=t.x<0?0:1;break;case Xa:Math.abs(Math.floor(t.x)%2)===1?t.x=Math.ceil(t.x)-t.x:t.x=t.x-Math.floor(t.x);break}if(t.y<0||t.y>1)switch(this.wrapT){case Wa:t.y=t.y-Math.floor(t.y);break;case Vn:t.y=t.y<0?0:1;break;case Xa:Math.abs(Math.floor(t.y)%2)===1?t.y=Math.ceil(t.y)-t.y:t.y=t.y-Math.floor(t.y);break}return this.flipY&&(t.y=1-t.y),t}set needsUpdate(t){t===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(t){t===!0&&this.pmremVersion++}};nn.DEFAULT_IMAGE=null;nn.DEFAULT_MAPPING=kc;nn.DEFAULT_ANISOTROPY=1;var ah=class ah{constructor(t=0,e=0,n=0,s=1){this.x=t,this.y=e,this.z=n,this.w=s}get width(){return this.z}set width(t){this.z=t}get height(){return this.w}set height(t){this.w=t}set(t,e,n,s){return this.x=t,this.y=e,this.z=n,this.w=s,this}setScalar(t){return this.x=t,this.y=t,this.z=t,this.w=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setZ(t){return this.z=t,this}setW(t){return this.w=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;case 2:this.z=e;break;case 3:this.w=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(t){return this.x=t.x,this.y=t.y,this.z=t.z,this.w=t.w!==void 0?t.w:1,this}add(t){return this.x+=t.x,this.y+=t.y,this.z+=t.z,this.w+=t.w,this}addScalar(t){return this.x+=t,this.y+=t,this.z+=t,this.w+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this.z=t.z+e.z,this.w=t.w+e.w,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this.z+=t.z*e,this.w+=t.w*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this.z-=t.z,this.w-=t.w,this}subScalar(t){return this.x-=t,this.y-=t,this.z-=t,this.w-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this.z=t.z-e.z,this.w=t.w-e.w,this}multiply(t){return this.x*=t.x,this.y*=t.y,this.z*=t.z,this.w*=t.w,this}multiplyScalar(t){return this.x*=t,this.y*=t,this.z*=t,this.w*=t,this}applyMatrix4(t){let e=this.x,n=this.y,s=this.z,r=this.w,a=t.elements;return this.x=a[0]*e+a[4]*n+a[8]*s+a[12]*r,this.y=a[1]*e+a[5]*n+a[9]*s+a[13]*r,this.z=a[2]*e+a[6]*n+a[10]*s+a[14]*r,this.w=a[3]*e+a[7]*n+a[11]*s+a[15]*r,this}divide(t){return this.x/=t.x,this.y/=t.y,this.z/=t.z,this.w/=t.w,this}divideScalar(t){return this.multiplyScalar(1/t)}setAxisAngleFromQuaternion(t){this.w=2*Math.acos(t.w);let e=Math.sqrt(1-t.w*t.w);return e<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=t.x/e,this.y=t.y/e,this.z=t.z/e),this}setAxisAngleFromRotationMatrix(t){let e,n,s,r,l=t.elements,c=l[0],h=l[4],f=l[8],u=l[1],d=l[5],m=l[9],_=l[2],g=l[6],p=l[10];if(Math.abs(h-u)<.01&&Math.abs(f-_)<.01&&Math.abs(m-g)<.01){if(Math.abs(h+u)<.1&&Math.abs(f+_)<.1&&Math.abs(m+g)<.1&&Math.abs(c+d+p-3)<.1)return this.set(1,0,0,0),this;e=Math.PI;let S=(c+1)/2,b=(d+1)/2,T=(p+1)/2,w=(h+u)/4,R=(f+_)/4,v=(m+g)/4;return S>b&&S>T?S<.01?(n=0,s=.707106781,r=.707106781):(n=Math.sqrt(S),s=w/n,r=R/n):b>T?b<.01?(n=.707106781,s=0,r=.707106781):(s=Math.sqrt(b),n=w/s,r=v/s):T<.01?(n=.707106781,s=.707106781,r=0):(r=Math.sqrt(T),n=R/r,s=v/r),this.set(n,s,r,e),this}let y=Math.sqrt((g-m)*(g-m)+(f-_)*(f-_)+(u-h)*(u-h));return Math.abs(y)<.001&&(y=1),this.x=(g-m)/y,this.y=(f-_)/y,this.z=(u-h)/y,this.w=Math.acos((c+d+p-1)/2),this}setFromMatrixPosition(t){let e=t.elements;return this.x=e[12],this.y=e[13],this.z=e[14],this.w=e[15],this}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this.z=Math.min(this.z,t.z),this.w=Math.min(this.w,t.w),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this.z=Math.max(this.z,t.z),this.w=Math.max(this.w,t.w),this}clamp(t,e){return this.x=Vt(this.x,t.x,e.x),this.y=Vt(this.y,t.y,e.y),this.z=Vt(this.z,t.z,e.z),this.w=Vt(this.w,t.w,e.w),this}clampScalar(t,e){return this.x=Vt(this.x,t,e),this.y=Vt(this.y,t,e),this.z=Vt(this.z,t,e),this.w=Vt(this.w,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(Vt(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(t){return this.x*t.x+this.y*t.y+this.z*t.z+this.w*t.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this.z+=(t.z-this.z)*e,this.w+=(t.w-this.w)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this.z=t.z+(e.z-t.z)*n,this.w=t.w+(e.w-t.w)*n,this}equals(t){return t.x===this.x&&t.y===this.y&&t.z===this.z&&t.w===this.w}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this.z=t[e+2],this.w=t[e+3],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t[e+2]=this.z,t[e+3]=this.w,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this.z=t.getZ(e),this.w=t.getW(e),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}};ah.prototype.isVector4=!0;var ve=ah,Ka=class extends Ln{constructor(t=1,e=1,n={}){super(),n=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:Ge,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1,depth:1,multiview:!1},n),this.isRenderTarget=!0,this.width=t,this.height=e,this.depth=n.depth,this.scissor=new ve(0,0,t,e),this.scissorTest=!1,this.viewport=new ve(0,0,t,e),this.textures=[];let s={width:t,height:e,depth:n.depth},r=new nn(s),a=n.count;for(let o=0;o<a;o++)this.textures[o]=r.clone(),this.textures[o].isRenderTargetTexture=!0,this.textures[o].renderTarget=this;this._setTextureOptions(n),this.depthBuffer=n.depthBuffer,this.stencilBuffer=n.stencilBuffer,this.resolveDepthBuffer=n.resolveDepthBuffer,this.resolveStencilBuffer=n.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=n.depthTexture,this.samples=n.samples,this.multiview=n.multiview}_setTextureOptions(t={}){let e={minFilter:Ge,generateMipmaps:!1,flipY:!1,internalFormat:null};t.mapping!==void 0&&(e.mapping=t.mapping),t.wrapS!==void 0&&(e.wrapS=t.wrapS),t.wrapT!==void 0&&(e.wrapT=t.wrapT),t.wrapR!==void 0&&(e.wrapR=t.wrapR),t.magFilter!==void 0&&(e.magFilter=t.magFilter),t.minFilter!==void 0&&(e.minFilter=t.minFilter),t.format!==void 0&&(e.format=t.format),t.type!==void 0&&(e.type=t.type),t.anisotropy!==void 0&&(e.anisotropy=t.anisotropy),t.colorSpace!==void 0&&(e.colorSpace=t.colorSpace),t.flipY!==void 0&&(e.flipY=t.flipY),t.generateMipmaps!==void 0&&(e.generateMipmaps=t.generateMipmaps),t.internalFormat!==void 0&&(e.internalFormat=t.internalFormat);for(let n=0;n<this.textures.length;n++)this.textures[n].setValues(e)}get texture(){return this.textures[0]}set texture(t){this.textures[0]=t}set depthTexture(t){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),t!==null&&(t.renderTarget=this),this._depthTexture=t}get depthTexture(){return this._depthTexture}setSize(t,e,n=1){if(this.width!==t||this.height!==e||this.depth!==n){this.width=t,this.height=e,this.depth=n;for(let s=0,r=this.textures.length;s<r;s++)this.textures[s].image.width=t,this.textures[s].image.height=e,this.textures[s].image.depth=n,this.textures[s].isData3DTexture!==!0&&(this.textures[s].isArrayTexture=this.textures[s].image.depth>1);this.dispose()}this.viewport.set(0,0,t,e),this.scissor.set(0,0,t,e)}clone(){return new this.constructor().copy(this)}copy(t){this.width=t.width,this.height=t.height,this.depth=t.depth,this.scissor.copy(t.scissor),this.scissorTest=t.scissorTest,this.viewport.copy(t.viewport),this.textures.length=0;for(let e=0,n=t.textures.length;e<n;e++){this.textures[e]=t.textures[e].clone(),this.textures[e].isRenderTargetTexture=!0,this.textures[e].renderTarget=this;let s=Object.assign({},t.textures[e].image);this.textures[e].source=new Fs(s)}return this.depthBuffer=t.depthBuffer,this.stencilBuffer=t.stencilBuffer,this.resolveDepthBuffer=t.resolveDepthBuffer,this.resolveStencilBuffer=t.resolveStencilBuffer,t.depthTexture!==null&&(this.depthTexture=t.depthTexture.clone()),this.samples=t.samples,this.multiview=t.multiview,this}dispose(){this.dispatchEvent({type:"dispose"})}},Ne=class extends Ka{constructor(t=1,e=1,n={}){super(t,e,n),this.isWebGLRenderTarget=!0}},mr=class extends nn{constructor(t=null,e=1,n=1,s=1){super(null),this.isDataArrayTexture=!0,this.image={data:t,width:e,height:n,depth:s},this.magFilter=Be,this.minFilter=Be,this.wrapR=Vn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(t){this.layerUpdates.add(t)}clearLayerUpdates(){this.layerUpdates.clear()}};var Ja=class extends nn{constructor(t=null,e=1,n=1,s=1){super(null),this.isData3DTexture=!0,this.image={data:t,width:e,height:n,depth:s},this.magFilter=Be,this.minFilter=Be,this.wrapR=Vn,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}};var xo=class xo{constructor(t,e,n,s,r,a,o,l,c,h,f,u,d,m,_,g){this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],t!==void 0&&this.set(t,e,n,s,r,a,o,l,c,h,f,u,d,m,_,g)}set(t,e,n,s,r,a,o,l,c,h,f,u,d,m,_,g){let p=this.elements;return p[0]=t,p[4]=e,p[8]=n,p[12]=s,p[1]=r,p[5]=a,p[9]=o,p[13]=l,p[2]=c,p[6]=h,p[10]=f,p[14]=u,p[3]=d,p[7]=m,p[11]=_,p[15]=g,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new xo().fromArray(this.elements)}copy(t){let e=this.elements,n=t.elements;return e[0]=n[0],e[1]=n[1],e[2]=n[2],e[3]=n[3],e[4]=n[4],e[5]=n[5],e[6]=n[6],e[7]=n[7],e[8]=n[8],e[9]=n[9],e[10]=n[10],e[11]=n[11],e[12]=n[12],e[13]=n[13],e[14]=n[14],e[15]=n[15],this}copyPosition(t){let e=this.elements,n=t.elements;return e[12]=n[12],e[13]=n[13],e[14]=n[14],this}setFromMatrix3(t){let e=t.elements;return this.set(e[0],e[3],e[6],0,e[1],e[4],e[7],0,e[2],e[5],e[8],0,0,0,0,1),this}extractBasis(t,e,n){return this.determinant()===0?(t.set(1,0,0),e.set(0,1,0),n.set(0,0,1),this):(t.setFromMatrixColumn(this,0),e.setFromMatrixColumn(this,1),n.setFromMatrixColumn(this,2),this)}makeBasis(t,e,n){return this.set(t.x,e.x,n.x,0,t.y,e.y,n.y,0,t.z,e.z,n.z,0,0,0,0,1),this}extractRotation(t){if(t.determinant()===0)return this.identity();let e=this.elements,n=t.elements,s=1/ys.setFromMatrixColumn(t,0).length(),r=1/ys.setFromMatrixColumn(t,1).length(),a=1/ys.setFromMatrixColumn(t,2).length();return e[0]=n[0]*s,e[1]=n[1]*s,e[2]=n[2]*s,e[3]=0,e[4]=n[4]*r,e[5]=n[5]*r,e[6]=n[6]*r,e[7]=0,e[8]=n[8]*a,e[9]=n[9]*a,e[10]=n[10]*a,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,this}makeRotationFromEuler(t){let e=this.elements,n=t.x,s=t.y,r=t.z,a=Math.cos(n),o=Math.sin(n),l=Math.cos(s),c=Math.sin(s),h=Math.cos(r),f=Math.sin(r);if(t.order==="XYZ"){let u=a*h,d=a*f,m=o*h,_=o*f;e[0]=l*h,e[4]=-l*f,e[8]=c,e[1]=d+m*c,e[5]=u-_*c,e[9]=-o*l,e[2]=_-u*c,e[6]=m+d*c,e[10]=a*l}else if(t.order==="YXZ"){let u=l*h,d=l*f,m=c*h,_=c*f;e[0]=u+_*o,e[4]=m*o-d,e[8]=a*c,e[1]=a*f,e[5]=a*h,e[9]=-o,e[2]=d*o-m,e[6]=_+u*o,e[10]=a*l}else if(t.order==="ZXY"){let u=l*h,d=l*f,m=c*h,_=c*f;e[0]=u-_*o,e[4]=-a*f,e[8]=m+d*o,e[1]=d+m*o,e[5]=a*h,e[9]=_-u*o,e[2]=-a*c,e[6]=o,e[10]=a*l}else if(t.order==="ZYX"){let u=a*h,d=a*f,m=o*h,_=o*f;e[0]=l*h,e[4]=m*c-d,e[8]=u*c+_,e[1]=l*f,e[5]=_*c+u,e[9]=d*c-m,e[2]=-c,e[6]=o*l,e[10]=a*l}else if(t.order==="YZX"){let u=a*l,d=a*c,m=o*l,_=o*c;e[0]=l*h,e[4]=_-u*f,e[8]=m*f+d,e[1]=f,e[5]=a*h,e[9]=-o*h,e[2]=-c*h,e[6]=d*f+m,e[10]=u-_*f}else if(t.order==="XZY"){let u=a*l,d=a*c,m=o*l,_=o*c;e[0]=l*h,e[4]=-f,e[8]=c*h,e[1]=u*f+_,e[5]=a*h,e[9]=d*f-m,e[2]=m*f-d,e[6]=o*h,e[10]=_*f+u}return e[3]=0,e[7]=0,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,this}makeRotationFromQuaternion(t){return this.compose(ig,t,sg)}lookAt(t,e,n){let s=this.elements;return dn.subVectors(t,e),dn.lengthSq()===0&&(dn.z=1),dn.normalize(),xi.crossVectors(n,dn),xi.lengthSq()===0&&(Math.abs(n.z)===1?dn.x+=1e-4:dn.z+=1e-4,dn.normalize(),xi.crossVectors(n,dn)),xi.normalize(),ha.crossVectors(dn,xi),s[0]=xi.x,s[4]=ha.x,s[8]=dn.x,s[1]=xi.y,s[5]=ha.y,s[9]=dn.y,s[2]=xi.z,s[6]=ha.z,s[10]=dn.z,this}multiply(t){return this.multiplyMatrices(this,t)}premultiply(t){return this.multiplyMatrices(t,this)}multiplyMatrices(t,e){let n=t.elements,s=e.elements,r=this.elements,a=n[0],o=n[4],l=n[8],c=n[12],h=n[1],f=n[5],u=n[9],d=n[13],m=n[2],_=n[6],g=n[10],p=n[14],y=n[3],S=n[7],b=n[11],T=n[15],w=s[0],R=s[4],v=s[8],E=s[12],L=s[1],C=s[5],D=s[9],H=s[13],W=s[2],U=s[6],z=s[10],V=s[14],$=s[3],tt=s[7],ct=s[11],Mt=s[15];return r[0]=a*w+o*L+l*W+c*$,r[4]=a*R+o*C+l*U+c*tt,r[8]=a*v+o*D+l*z+c*ct,r[12]=a*E+o*H+l*V+c*Mt,r[1]=h*w+f*L+u*W+d*$,r[5]=h*R+f*C+u*U+d*tt,r[9]=h*v+f*D+u*z+d*ct,r[13]=h*E+f*H+u*V+d*Mt,r[2]=m*w+_*L+g*W+p*$,r[6]=m*R+_*C+g*U+p*tt,r[10]=m*v+_*D+g*z+p*ct,r[14]=m*E+_*H+g*V+p*Mt,r[3]=y*w+S*L+b*W+T*$,r[7]=y*R+S*C+b*U+T*tt,r[11]=y*v+S*D+b*z+T*ct,r[15]=y*E+S*H+b*V+T*Mt,this}multiplyScalar(t){let e=this.elements;return e[0]*=t,e[4]*=t,e[8]*=t,e[12]*=t,e[1]*=t,e[5]*=t,e[9]*=t,e[13]*=t,e[2]*=t,e[6]*=t,e[10]*=t,e[14]*=t,e[3]*=t,e[7]*=t,e[11]*=t,e[15]*=t,this}determinant(){let t=this.elements,e=t[0],n=t[4],s=t[8],r=t[12],a=t[1],o=t[5],l=t[9],c=t[13],h=t[2],f=t[6],u=t[10],d=t[14],m=t[3],_=t[7],g=t[11],p=t[15],y=l*d-c*u,S=o*d-c*f,b=o*u-l*f,T=a*d-c*h,w=a*u-l*h,R=a*f-o*h;return e*(_*y-g*S+p*b)-n*(m*y-g*T+p*w)+s*(m*S-_*T+p*R)-r*(m*b-_*w+g*R)}transpose(){let t=this.elements,e;return e=t[1],t[1]=t[4],t[4]=e,e=t[2],t[2]=t[8],t[8]=e,e=t[6],t[6]=t[9],t[9]=e,e=t[3],t[3]=t[12],t[12]=e,e=t[7],t[7]=t[13],t[13]=e,e=t[11],t[11]=t[14],t[14]=e,this}setPosition(t,e,n){let s=this.elements;return t.isVector3?(s[12]=t.x,s[13]=t.y,s[14]=t.z):(s[12]=t,s[13]=e,s[14]=n),this}invert(){let t=this.elements,e=t[0],n=t[1],s=t[2],r=t[3],a=t[4],o=t[5],l=t[6],c=t[7],h=t[8],f=t[9],u=t[10],d=t[11],m=t[12],_=t[13],g=t[14],p=t[15],y=e*o-n*a,S=e*l-s*a,b=e*c-r*a,T=n*l-s*o,w=n*c-r*o,R=s*c-r*l,v=h*_-f*m,E=h*g-u*m,L=h*p-d*m,C=f*g-u*_,D=f*p-d*_,H=u*p-d*g,W=y*H-S*D+b*C+T*L-w*E+R*v;if(W===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);let U=1/W;return t[0]=(o*H-l*D+c*C)*U,t[1]=(s*D-n*H-r*C)*U,t[2]=(_*R-g*w+p*T)*U,t[3]=(u*w-f*R-d*T)*U,t[4]=(l*L-a*H-c*E)*U,t[5]=(e*H-s*L+r*E)*U,t[6]=(g*b-m*R-p*S)*U,t[7]=(h*R-u*b+d*S)*U,t[8]=(a*D-o*L+c*v)*U,t[9]=(n*L-e*D-r*v)*U,t[10]=(m*w-_*b+p*y)*U,t[11]=(f*b-h*w-d*y)*U,t[12]=(o*E-a*C-l*v)*U,t[13]=(e*C-n*E+s*v)*U,t[14]=(_*S-m*T-g*y)*U,t[15]=(h*T-f*S+u*y)*U,this}scale(t){let e=this.elements,n=t.x,s=t.y,r=t.z;return e[0]*=n,e[4]*=s,e[8]*=r,e[1]*=n,e[5]*=s,e[9]*=r,e[2]*=n,e[6]*=s,e[10]*=r,e[3]*=n,e[7]*=s,e[11]*=r,this}getMaxScaleOnAxis(){let t=this.elements,e=t[0]*t[0]+t[1]*t[1]+t[2]*t[2],n=t[4]*t[4]+t[5]*t[5]+t[6]*t[6],s=t[8]*t[8]+t[9]*t[9]+t[10]*t[10];return Math.sqrt(Math.max(e,n,s))}makeTranslation(t,e,n){return t.isVector3?this.set(1,0,0,t.x,0,1,0,t.y,0,0,1,t.z,0,0,0,1):this.set(1,0,0,t,0,1,0,e,0,0,1,n,0,0,0,1),this}makeRotationX(t){let e=Math.cos(t),n=Math.sin(t);return this.set(1,0,0,0,0,e,-n,0,0,n,e,0,0,0,0,1),this}makeRotationY(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,0,n,0,0,1,0,0,-n,0,e,0,0,0,0,1),this}makeRotationZ(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,-n,0,0,n,e,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(t,e){let n=Math.cos(e),s=Math.sin(e),r=1-n,a=t.x,o=t.y,l=t.z,c=r*a,h=r*o;return this.set(c*a+n,c*o-s*l,c*l+s*o,0,c*o+s*l,h*o+n,h*l-s*a,0,c*l-s*o,h*l+s*a,r*l*l+n,0,0,0,0,1),this}makeScale(t,e,n){return this.set(t,0,0,0,0,e,0,0,0,0,n,0,0,0,0,1),this}makeShear(t,e,n,s,r,a){return this.set(1,n,r,0,t,1,a,0,e,s,1,0,0,0,0,1),this}compose(t,e,n){let s=this.elements,r=e._x,a=e._y,o=e._z,l=e._w,c=r+r,h=a+a,f=o+o,u=r*c,d=r*h,m=r*f,_=a*h,g=a*f,p=o*f,y=l*c,S=l*h,b=l*f,T=n.x,w=n.y,R=n.z;return s[0]=(1-(_+p))*T,s[1]=(d+b)*T,s[2]=(m-S)*T,s[3]=0,s[4]=(d-b)*w,s[5]=(1-(u+p))*w,s[6]=(g+y)*w,s[7]=0,s[8]=(m+S)*R,s[9]=(g-y)*R,s[10]=(1-(u+_))*R,s[11]=0,s[12]=t.x,s[13]=t.y,s[14]=t.z,s[15]=1,this}decompose(t,e,n){let s=this.elements;t.x=s[12],t.y=s[13],t.z=s[14];let r=this.determinant();if(r===0)return n.set(1,1,1),e.identity(),this;let a=ys.set(s[0],s[1],s[2]).length(),o=ys.set(s[4],s[5],s[6]).length(),l=ys.set(s[8],s[9],s[10]).length();r<0&&(a=-a),Cn.copy(this);let c=1/a,h=1/o,f=1/l;return Cn.elements[0]*=c,Cn.elements[1]*=c,Cn.elements[2]*=c,Cn.elements[4]*=h,Cn.elements[5]*=h,Cn.elements[6]*=h,Cn.elements[8]*=f,Cn.elements[9]*=f,Cn.elements[10]*=f,e.setFromRotationMatrix(Cn),n.x=a,n.y=o,n.z=l,this}makePerspective(t,e,n,s,r,a,o=In,l=!1){let c=this.elements,h=2*r/(e-t),f=2*r/(n-s),u=(e+t)/(e-t),d=(n+s)/(n-s),m,_;if(l)m=r/(a-r),_=a*r/(a-r);else if(o===In)m=-(a+r)/(a-r),_=-2*a*r/(a-r);else if(o===dr)m=-a/(a-r),_=-a*r/(a-r);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=h,c[4]=0,c[8]=u,c[12]=0,c[1]=0,c[5]=f,c[9]=d,c[13]=0,c[2]=0,c[6]=0,c[10]=m,c[14]=_,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(t,e,n,s,r,a,o=In,l=!1){let c=this.elements,h=2/(e-t),f=2/(n-s),u=-(e+t)/(e-t),d=-(n+s)/(n-s),m,_;if(l)m=1/(a-r),_=a/(a-r);else if(o===In)m=-2/(a-r),_=-(a+r)/(a-r);else if(o===dr)m=-1/(a-r),_=-r/(a-r);else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=h,c[4]=0,c[8]=0,c[12]=u,c[1]=0,c[5]=f,c[9]=0,c[13]=d,c[2]=0,c[6]=0,c[10]=m,c[14]=_,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(t){let e=this.elements,n=t.elements;for(let s=0;s<16;s++)if(e[s]!==n[s])return!1;return!0}fromArray(t,e=0){for(let n=0;n<16;n++)this.elements[n]=t[n+e];return this}toArray(t=[],e=0){let n=this.elements;return t[e]=n[0],t[e+1]=n[1],t[e+2]=n[2],t[e+3]=n[3],t[e+4]=n[4],t[e+5]=n[5],t[e+6]=n[6],t[e+7]=n[7],t[e+8]=n[8],t[e+9]=n[9],t[e+10]=n[10],t[e+11]=n[11],t[e+12]=n[12],t[e+13]=n[13],t[e+14]=n[14],t[e+15]=n[15],t}};xo.prototype.isMatrix4=!0;var ge=xo,ys=new P,Cn=new ge,ig=new P(0,0,0),sg=new P(1,1,1),xi=new P,ha=new P,dn=new P,Iu=new ge,Lu=new gn,Ti=class i{constructor(t=0,e=0,n=0,s=i.DEFAULT_ORDER){this.isEuler=!0,this._x=t,this._y=e,this._z=n,this._order=s}get x(){return this._x}set x(t){this._x=t,this._onChangeCallback()}get y(){return this._y}set y(t){this._y=t,this._onChangeCallback()}get z(){return this._z}set z(t){this._z=t,this._onChangeCallback()}get order(){return this._order}set order(t){this._order=t,this._onChangeCallback()}set(t,e,n,s=this._order){return this._x=t,this._y=e,this._z=n,this._order=s,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(t){return this._x=t._x,this._y=t._y,this._z=t._z,this._order=t._order,this._onChangeCallback(),this}setFromRotationMatrix(t,e=this._order,n=!0){let s=t.elements,r=s[0],a=s[4],o=s[8],l=s[1],c=s[5],h=s[9],f=s[2],u=s[6],d=s[10];switch(e){case"XYZ":this._y=Math.asin(Vt(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-h,d),this._z=Math.atan2(-a,r)):(this._x=Math.atan2(u,c),this._z=0);break;case"YXZ":this._x=Math.asin(-Vt(h,-1,1)),Math.abs(h)<.9999999?(this._y=Math.atan2(o,d),this._z=Math.atan2(l,c)):(this._y=Math.atan2(-f,r),this._z=0);break;case"ZXY":this._x=Math.asin(Vt(u,-1,1)),Math.abs(u)<.9999999?(this._y=Math.atan2(-f,d),this._z=Math.atan2(-a,c)):(this._y=0,this._z=Math.atan2(l,r));break;case"ZYX":this._y=Math.asin(-Vt(f,-1,1)),Math.abs(f)<.9999999?(this._x=Math.atan2(u,d),this._z=Math.atan2(l,r)):(this._x=0,this._z=Math.atan2(-a,c));break;case"YZX":this._z=Math.asin(Vt(l,-1,1)),Math.abs(l)<.9999999?(this._x=Math.atan2(-h,c),this._y=Math.atan2(-f,r)):(this._x=0,this._y=Math.atan2(o,d));break;case"XZY":this._z=Math.asin(-Vt(a,-1,1)),Math.abs(a)<.9999999?(this._x=Math.atan2(u,c),this._y=Math.atan2(o,r)):(this._x=Math.atan2(-h,d),this._y=0);break;default:Ct("Euler: .setFromRotationMatrix() encountered an unknown order: "+e)}return this._order=e,n===!0&&this._onChangeCallback(),this}setFromQuaternion(t,e,n){return Iu.makeRotationFromQuaternion(t),this.setFromRotationMatrix(Iu,e,n)}setFromVector3(t,e=this._order){return this.set(t.x,t.y,t.z,e)}reorder(t){return Lu.setFromEuler(this),this.setFromQuaternion(Lu,t)}equals(t){return t._x===this._x&&t._y===this._y&&t._z===this._z&&t._order===this._order}fromArray(t){return this._x=t[0],this._y=t[1],this._z=t[2],t[3]!==void 0&&(this._order=t[3]),this._onChangeCallback(),this}toArray(t=[],e=0){return t[e]=this._x,t[e+1]=this._y,t[e+2]=this._z,t[e+3]=this._order,t}_onChange(t){return this._onChangeCallback=t,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}};Ti.DEFAULT_ORDER="XYZ";var gr=class{constructor(){this.mask=1}set(t){this.mask=(1<<t|0)>>>0}enable(t){this.mask|=1<<t|0}enableAll(){this.mask=-1}toggle(t){this.mask^=1<<t|0}disable(t){this.mask&=~(1<<t|0)}disableAll(){this.mask=0}test(t){return(this.mask&t.mask)!==0}isEnabled(t){return(this.mask&(1<<t|0))!==0}},rg=0,Nu=new P,Ms=new gn,Qn=new ge,ua=new P,ir=new P,ag=new P,og=new gn,Du=new P(1,0,0),Fu=new P(0,1,0),Uu=new P(0,0,1),Ou={type:"added"},lg={type:"removed"},bs={type:"childadded",child:null},rc={type:"childremoved",child:null},sn=class i extends Ln{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:rg++}),this.uuid=Gs(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=i.DEFAULT_UP.clone();let t=new P,e=new Ti,n=new gn,s=new P(1,1,1);function r(){n.setFromEuler(e,!1)}function a(){e.setFromQuaternion(n,void 0,!1)}e._onChange(r),n._onChange(a),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:t},rotation:{configurable:!0,enumerable:!0,value:e},quaternion:{configurable:!0,enumerable:!0,value:n},scale:{configurable:!0,enumerable:!0,value:s},modelViewMatrix:{value:new ge},normalMatrix:{value:new Ft}}),this.matrix=new ge,this.matrixWorld=new ge,this.matrixAutoUpdate=i.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=i.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new gr,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.customDepthMaterial=void 0,this.customDistanceMaterial=void 0,this.static=!1,this.userData={},this.pivot=null}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(t){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(t),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(t){return this.quaternion.premultiply(t),this}setRotationFromAxisAngle(t,e){this.quaternion.setFromAxisAngle(t,e)}setRotationFromEuler(t){this.quaternion.setFromEuler(t,!0)}setRotationFromMatrix(t){this.quaternion.setFromRotationMatrix(t)}setRotationFromQuaternion(t){this.quaternion.copy(t)}rotateOnAxis(t,e){return Ms.setFromAxisAngle(t,e),this.quaternion.multiply(Ms),this}rotateOnWorldAxis(t,e){return Ms.setFromAxisAngle(t,e),this.quaternion.premultiply(Ms),this}rotateX(t){return this.rotateOnAxis(Du,t)}rotateY(t){return this.rotateOnAxis(Fu,t)}rotateZ(t){return this.rotateOnAxis(Uu,t)}translateOnAxis(t,e){return Nu.copy(t).applyQuaternion(this.quaternion),this.position.add(Nu.multiplyScalar(e)),this}translateX(t){return this.translateOnAxis(Du,t)}translateY(t){return this.translateOnAxis(Fu,t)}translateZ(t){return this.translateOnAxis(Uu,t)}localToWorld(t){return this.updateWorldMatrix(!0,!1),t.applyMatrix4(this.matrixWorld)}worldToLocal(t){return this.updateWorldMatrix(!0,!1),t.applyMatrix4(Qn.copy(this.matrixWorld).invert())}lookAt(t,e,n){t.isVector3?ua.copy(t):ua.set(t,e,n);let s=this.parent;this.updateWorldMatrix(!0,!1),ir.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?Qn.lookAt(ir,ua,this.up):Qn.lookAt(ua,ir,this.up),this.quaternion.setFromRotationMatrix(Qn),s&&(Qn.extractRotation(s.matrixWorld),Ms.setFromRotationMatrix(Qn),this.quaternion.premultiply(Ms.invert()))}add(t){if(arguments.length>1){for(let e=0;e<arguments.length;e++)this.add(arguments[e]);return this}return t===this?(Pt("Object3D.add: object can't be added as a child of itself.",t),this):(t&&t.isObject3D?(t.removeFromParent(),t.parent=this,this.children.push(t),t.dispatchEvent(Ou),bs.child=t,this.dispatchEvent(bs),bs.child=null):Pt("Object3D.add: object not an instance of THREE.Object3D.",t),this)}remove(t){if(arguments.length>1){for(let n=0;n<arguments.length;n++)this.remove(arguments[n]);return this}let e=this.children.indexOf(t);return e!==-1&&(t.parent=null,this.children.splice(e,1),t.dispatchEvent(lg),rc.child=t,this.dispatchEvent(rc),rc.child=null),this}removeFromParent(){let t=this.parent;return t!==null&&t.remove(this),this}clear(){return this.remove(...this.children)}attach(t){return this.updateWorldMatrix(!0,!1),Qn.copy(this.matrixWorld).invert(),t.parent!==null&&(t.parent.updateWorldMatrix(!0,!1),Qn.multiply(t.parent.matrixWorld)),t.applyMatrix4(Qn),t.removeFromParent(),t.parent=this,this.children.push(t),t.updateWorldMatrix(!1,!0),t.dispatchEvent(Ou),bs.child=t,this.dispatchEvent(bs),bs.child=null,this}getObjectById(t){return this.getObjectByProperty("id",t)}getObjectByName(t){return this.getObjectByProperty("name",t)}getObjectByProperty(t,e){if(this[t]===e)return this;for(let n=0,s=this.children.length;n<s;n++){let a=this.children[n].getObjectByProperty(t,e);if(a!==void 0)return a}}getObjectsByProperty(t,e,n=[]){this[t]===e&&n.push(this);let s=this.children;for(let r=0,a=s.length;r<a;r++)s[r].getObjectsByProperty(t,e,n);return n}getWorldPosition(t){return this.updateWorldMatrix(!0,!1),t.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(t){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ir,t,ag),t}getWorldScale(t){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(ir,og,t),t}getWorldDirection(t){this.updateWorldMatrix(!0,!1);let e=this.matrixWorld.elements;return t.set(e[8],e[9],e[10]).normalize()}raycast(){}traverse(t){t(this);let e=this.children;for(let n=0,s=e.length;n<s;n++)e[n].traverse(t)}traverseVisible(t){if(this.visible===!1)return;t(this);let e=this.children;for(let n=0,s=e.length;n<s;n++)e[n].traverseVisible(t)}traverseAncestors(t){let e=this.parent;e!==null&&(t(e),e.traverseAncestors(t))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale);let t=this.pivot;if(t!==null){let e=t.x,n=t.y,s=t.z,r=this.matrix.elements;r[12]+=e-r[0]*e-r[4]*n-r[8]*s,r[13]+=n-r[1]*e-r[5]*n-r[9]*s,r[14]+=s-r[2]*e-r[6]*n-r[10]*s}this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(t){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||t)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,t=!0);let e=this.children;for(let n=0,s=e.length;n<s;n++)e[n].updateMatrixWorld(t)}updateWorldMatrix(t,e){let n=this.parent;if(t===!0&&n!==null&&n.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),e===!0){let s=this.children;for(let r=0,a=s.length;r<a;r++)s[r].updateWorldMatrix(!1,!0)}}toJSON(t){let e=t===void 0||typeof t=="string",n={};e&&(t={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},n.metadata={version:4.7,type:"Object",generator:"Object3D.toJSON"});let s={};s.uuid=this.uuid,s.type=this.type,this.name!==""&&(s.name=this.name),this.castShadow===!0&&(s.castShadow=!0),this.receiveShadow===!0&&(s.receiveShadow=!0),this.visible===!1&&(s.visible=!1),this.frustumCulled===!1&&(s.frustumCulled=!1),this.renderOrder!==0&&(s.renderOrder=this.renderOrder),this.static!==!1&&(s.static=this.static),Object.keys(this.userData).length>0&&(s.userData=this.userData),s.layers=this.layers.mask,s.matrix=this.matrix.toArray(),s.up=this.up.toArray(),this.pivot!==null&&(s.pivot=this.pivot.toArray()),this.matrixAutoUpdate===!1&&(s.matrixAutoUpdate=!1),this.morphTargetDictionary!==void 0&&(s.morphTargetDictionary=Object.assign({},this.morphTargetDictionary)),this.morphTargetInfluences!==void 0&&(s.morphTargetInfluences=this.morphTargetInfluences.slice()),this.isInstancedMesh&&(s.type="InstancedMesh",s.count=this.count,s.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(s.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(s.type="BatchedMesh",s.perObjectFrustumCulled=this.perObjectFrustumCulled,s.sortObjects=this.sortObjects,s.drawRanges=this._drawRanges,s.reservedRanges=this._reservedRanges,s.geometryInfo=this._geometryInfo.map(o=>({...o,boundingBox:o.boundingBox?o.boundingBox.toJSON():void 0,boundingSphere:o.boundingSphere?o.boundingSphere.toJSON():void 0})),s.instanceInfo=this._instanceInfo.map(o=>({...o})),s.availableInstanceIds=this._availableInstanceIds.slice(),s.availableGeometryIds=this._availableGeometryIds.slice(),s.nextIndexStart=this._nextIndexStart,s.nextVertexStart=this._nextVertexStart,s.geometryCount=this._geometryCount,s.maxInstanceCount=this._maxInstanceCount,s.maxVertexCount=this._maxVertexCount,s.maxIndexCount=this._maxIndexCount,s.geometryInitialized=this._geometryInitialized,s.matricesTexture=this._matricesTexture.toJSON(t),s.indirectTexture=this._indirectTexture.toJSON(t),this._colorsTexture!==null&&(s.colorsTexture=this._colorsTexture.toJSON(t)),this.boundingSphere!==null&&(s.boundingSphere=this.boundingSphere.toJSON()),this.boundingBox!==null&&(s.boundingBox=this.boundingBox.toJSON()));function r(o,l){return o[l.uuid]===void 0&&(o[l.uuid]=l.toJSON(t)),l.uuid}if(this.isScene)this.background&&(this.background.isColor?s.background=this.background.toJSON():this.background.isTexture&&(s.background=this.background.toJSON(t).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(s.environment=this.environment.toJSON(t).uuid);else if(this.isMesh||this.isLine||this.isPoints){s.geometry=r(t.geometries,this.geometry);let o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){let l=o.shapes;if(Array.isArray(l))for(let c=0,h=l.length;c<h;c++){let f=l[c];r(t.shapes,f)}else r(t.shapes,l)}}if(this.isSkinnedMesh&&(s.bindMode=this.bindMode,s.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(r(t.skeletons,this.skeleton),s.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){let o=[];for(let l=0,c=this.material.length;l<c;l++)o.push(r(t.materials,this.material[l]));s.material=o}else s.material=r(t.materials,this.material);if(this.children.length>0){s.children=[];for(let o=0;o<this.children.length;o++)s.children.push(this.children[o].toJSON(t).object)}if(this.animations.length>0){s.animations=[];for(let o=0;o<this.animations.length;o++){let l=this.animations[o];s.animations.push(r(t.animations,l))}}if(e){let o=a(t.geometries),l=a(t.materials),c=a(t.textures),h=a(t.images),f=a(t.shapes),u=a(t.skeletons),d=a(t.animations),m=a(t.nodes);o.length>0&&(n.geometries=o),l.length>0&&(n.materials=l),c.length>0&&(n.textures=c),h.length>0&&(n.images=h),f.length>0&&(n.shapes=f),u.length>0&&(n.skeletons=u),d.length>0&&(n.animations=d),m.length>0&&(n.nodes=m)}return n.object=s,n;function a(o){let l=[];for(let c in o){let h=o[c];delete h.metadata,l.push(h)}return l}}clone(t){return new this.constructor().copy(this,t)}copy(t,e=!0){if(this.name=t.name,this.up.copy(t.up),this.position.copy(t.position),this.rotation.order=t.rotation.order,this.quaternion.copy(t.quaternion),this.scale.copy(t.scale),this.pivot=t.pivot!==null?t.pivot.clone():null,this.matrix.copy(t.matrix),this.matrixWorld.copy(t.matrixWorld),this.matrixAutoUpdate=t.matrixAutoUpdate,this.matrixWorldAutoUpdate=t.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=t.matrixWorldNeedsUpdate,this.layers.mask=t.layers.mask,this.visible=t.visible,this.castShadow=t.castShadow,this.receiveShadow=t.receiveShadow,this.frustumCulled=t.frustumCulled,this.renderOrder=t.renderOrder,this.static=t.static,this.animations=t.animations.slice(),this.userData=JSON.parse(JSON.stringify(t.userData)),e===!0)for(let n=0;n<t.children.length;n++){let s=t.children[n];this.add(s.clone())}return this}};sn.DEFAULT_UP=new P(0,1,0);sn.DEFAULT_MATRIX_AUTO_UPDATE=!0;sn.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;var si=class extends sn{constructor(){super(),this.isGroup=!0,this.type="Group"}},cg={type:"move"},Us=class{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new si,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new si,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new P,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new P),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new si,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new P,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new P,this._grip.eventsEnabled=!1),this._grip}dispatchEvent(t){return this._targetRay!==null&&this._targetRay.dispatchEvent(t),this._grip!==null&&this._grip.dispatchEvent(t),this._hand!==null&&this._hand.dispatchEvent(t),this}connect(t){if(t&&t.hand){let e=this._hand;if(e)for(let n of t.hand.values())this._getHandJoint(e,n)}return this.dispatchEvent({type:"connected",data:t}),this}disconnect(t){return this.dispatchEvent({type:"disconnected",data:t}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(t,e,n){let s=null,r=null,a=null,o=this._targetRay,l=this._grip,c=this._hand;if(t&&e.session.visibilityState!=="visible-blurred"){if(c&&t.hand){a=!0;for(let _ of t.hand.values()){let g=e.getJointPose(_,n),p=this._getHandJoint(c,_);g!==null&&(p.matrix.fromArray(g.transform.matrix),p.matrix.decompose(p.position,p.rotation,p.scale),p.matrixWorldNeedsUpdate=!0,p.jointRadius=g.radius),p.visible=g!==null}let h=c.joints["index-finger-tip"],f=c.joints["thumb-tip"],u=h.position.distanceTo(f.position),d=.02,m=.005;c.inputState.pinching&&u>d+m?(c.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:t.handedness,target:this})):!c.inputState.pinching&&u<=d-m&&(c.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:t.handedness,target:this}))}else l!==null&&t.gripSpace&&(r=e.getPose(t.gripSpace,n),r!==null&&(l.matrix.fromArray(r.transform.matrix),l.matrix.decompose(l.position,l.rotation,l.scale),l.matrixWorldNeedsUpdate=!0,r.linearVelocity?(l.hasLinearVelocity=!0,l.linearVelocity.copy(r.linearVelocity)):l.hasLinearVelocity=!1,r.angularVelocity?(l.hasAngularVelocity=!0,l.angularVelocity.copy(r.angularVelocity)):l.hasAngularVelocity=!1,l.eventsEnabled&&l.dispatchEvent({type:"gripUpdated",data:t,target:this})));o!==null&&(s=e.getPose(t.targetRaySpace,n),s===null&&r!==null&&(s=r),s!==null&&(o.matrix.fromArray(s.transform.matrix),o.matrix.decompose(o.position,o.rotation,o.scale),o.matrixWorldNeedsUpdate=!0,s.linearVelocity?(o.hasLinearVelocity=!0,o.linearVelocity.copy(s.linearVelocity)):o.hasLinearVelocity=!1,s.angularVelocity?(o.hasAngularVelocity=!0,o.angularVelocity.copy(s.angularVelocity)):o.hasAngularVelocity=!1,this.dispatchEvent(cg)))}return o!==null&&(o.visible=s!==null),l!==null&&(l.visible=r!==null),c!==null&&(c.visible=a!==null),this}_getHandJoint(t,e){if(t.joints[e.jointName]===void 0){let n=new si;n.matrixAutoUpdate=!1,n.visible=!1,t.joints[e.jointName]=n,t.add(n)}return t.joints[e.jointName]}},Uf={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},vi={h:0,s:0,l:0},fa={h:0,s:0,l:0};function ac(i,t,e){return e<0&&(e+=1),e>1&&(e-=1),e<1/6?i+(t-i)*6*e:e<1/2?t:e<2/3?i+(t-i)*6*(2/3-e):i}var dt=class{constructor(t,e,n){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(t,e,n)}set(t,e,n){if(e===void 0&&n===void 0){let s=t;s&&s.isColor?this.copy(s):typeof s=="number"?this.setHex(s):typeof s=="string"&&this.setStyle(s)}else this.setRGB(t,e,n);return this}setScalar(t){return this.r=t,this.g=t,this.b=t,this}setHex(t,e=mn){return t=Math.floor(t),this.r=(t>>16&255)/255,this.g=(t>>8&255)/255,this.b=(t&255)/255,Wt.colorSpaceToWorking(this,e),this}setRGB(t,e,n,s=Wt.workingColorSpace){return this.r=t,this.g=e,this.b=n,Wt.colorSpaceToWorking(this,s),this}setHSL(t,e,n,s=Wt.workingColorSpace){if(t=Jc(t,1),e=Vt(e,0,1),n=Vt(n,0,1),e===0)this.r=this.g=this.b=n;else{let r=n<=.5?n*(1+e):n+e-n*e,a=2*n-r;this.r=ac(a,r,t+1/3),this.g=ac(a,r,t),this.b=ac(a,r,t-1/3)}return Wt.colorSpaceToWorking(this,s),this}setStyle(t,e=mn){function n(r){r!==void 0&&parseFloat(r)<1&&Ct("Color: Alpha component of "+t+" will be ignored.")}let s;if(s=/^(\w+)\(([^\)]*)\)/.exec(t)){let r,a=s[1],o=s[2];switch(a){case"rgb":case"rgba":if(r=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(r[4]),this.setRGB(Math.min(255,parseInt(r[1],10))/255,Math.min(255,parseInt(r[2],10))/255,Math.min(255,parseInt(r[3],10))/255,e);if(r=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(r[4]),this.setRGB(Math.min(100,parseInt(r[1],10))/100,Math.min(100,parseInt(r[2],10))/100,Math.min(100,parseInt(r[3],10))/100,e);break;case"hsl":case"hsla":if(r=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(r[4]),this.setHSL(parseFloat(r[1])/360,parseFloat(r[2])/100,parseFloat(r[3])/100,e);break;default:Ct("Color: Unknown color model "+t)}}else if(s=/^\#([A-Fa-f\d]+)$/.exec(t)){let r=s[1],a=r.length;if(a===3)return this.setRGB(parseInt(r.charAt(0),16)/15,parseInt(r.charAt(1),16)/15,parseInt(r.charAt(2),16)/15,e);if(a===6)return this.setHex(parseInt(r,16),e);Ct("Color: Invalid hex color "+t)}else if(t&&t.length>0)return this.setColorName(t,e);return this}setColorName(t,e=mn){let n=Uf[t.toLowerCase()];return n!==void 0?this.setHex(n,e):Ct("Color: Unknown color "+t),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(t){return this.r=t.r,this.g=t.g,this.b=t.b,this}copySRGBToLinear(t){return this.r=ri(t.r),this.g=ri(t.g),this.b=ri(t.b),this}copyLinearToSRGB(t){return this.r=Ls(t.r),this.g=Ls(t.g),this.b=Ls(t.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(t=mn){return Wt.workingToColorSpace(qe.copy(this),t),Math.round(Vt(qe.r*255,0,255))*65536+Math.round(Vt(qe.g*255,0,255))*256+Math.round(Vt(qe.b*255,0,255))}getHexString(t=mn){return("000000"+this.getHex(t).toString(16)).slice(-6)}getHSL(t,e=Wt.workingColorSpace){Wt.workingToColorSpace(qe.copy(this),e);let n=qe.r,s=qe.g,r=qe.b,a=Math.max(n,s,r),o=Math.min(n,s,r),l,c,h=(o+a)/2;if(o===a)l=0,c=0;else{let f=a-o;switch(c=h<=.5?f/(a+o):f/(2-a-o),a){case n:l=(s-r)/f+(s<r?6:0);break;case s:l=(r-n)/f+2;break;case r:l=(n-s)/f+4;break}l/=6}return t.h=l,t.s=c,t.l=h,t}getRGB(t,e=Wt.workingColorSpace){return Wt.workingToColorSpace(qe.copy(this),e),t.r=qe.r,t.g=qe.g,t.b=qe.b,t}getStyle(t=mn){Wt.workingToColorSpace(qe.copy(this),t);let e=qe.r,n=qe.g,s=qe.b;return t!==mn?`color(${t} ${e.toFixed(3)} ${n.toFixed(3)} ${s.toFixed(3)})`:`rgb(${Math.round(e*255)},${Math.round(n*255)},${Math.round(s*255)})`}offsetHSL(t,e,n){return this.getHSL(vi),this.setHSL(vi.h+t,vi.s+e,vi.l+n)}add(t){return this.r+=t.r,this.g+=t.g,this.b+=t.b,this}addColors(t,e){return this.r=t.r+e.r,this.g=t.g+e.g,this.b=t.b+e.b,this}addScalar(t){return this.r+=t,this.g+=t,this.b+=t,this}sub(t){return this.r=Math.max(0,this.r-t.r),this.g=Math.max(0,this.g-t.g),this.b=Math.max(0,this.b-t.b),this}multiply(t){return this.r*=t.r,this.g*=t.g,this.b*=t.b,this}multiplyScalar(t){return this.r*=t,this.g*=t,this.b*=t,this}lerp(t,e){return this.r+=(t.r-this.r)*e,this.g+=(t.g-this.g)*e,this.b+=(t.b-this.b)*e,this}lerpColors(t,e,n){return this.r=t.r+(e.r-t.r)*n,this.g=t.g+(e.g-t.g)*n,this.b=t.b+(e.b-t.b)*n,this}lerpHSL(t,e){this.getHSL(vi),t.getHSL(fa);let n=cr(vi.h,fa.h,e),s=cr(vi.s,fa.s,e),r=cr(vi.l,fa.l,e);return this.setHSL(n,s,r),this}setFromVector3(t){return this.r=t.x,this.g=t.y,this.b=t.z,this}applyMatrix3(t){let e=this.r,n=this.g,s=this.b,r=t.elements;return this.r=r[0]*e+r[3]*n+r[6]*s,this.g=r[1]*e+r[4]*n+r[7]*s,this.b=r[2]*e+r[5]*n+r[8]*s,this}equals(t){return t.r===this.r&&t.g===this.g&&t.b===this.b}fromArray(t,e=0){return this.r=t[e],this.g=t[e+1],this.b=t[e+2],this}toArray(t=[],e=0){return t[e]=this.r,t[e+1]=this.g,t[e+2]=this.b,t}fromBufferAttribute(t,e){return this.r=t.getX(e),this.g=t.getY(e),this.b=t.getZ(e),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}},qe=new dt;dt.NAMES=Uf;var _r=class extends sn{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new Ti,this.environmentIntensity=1,this.environmentRotation=new Ti,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(t,e){return super.copy(t,e),t.background!==null&&(this.background=t.background.clone()),t.environment!==null&&(this.environment=t.environment.clone()),t.fog!==null&&(this.fog=t.fog.clone()),this.backgroundBlurriness=t.backgroundBlurriness,this.backgroundIntensity=t.backgroundIntensity,this.backgroundRotation.copy(t.backgroundRotation),this.environmentIntensity=t.environmentIntensity,this.environmentRotation.copy(t.environmentRotation),t.overrideMaterial!==null&&(this.overrideMaterial=t.overrideMaterial.clone()),this.matrixAutoUpdate=t.matrixAutoUpdate,this}toJSON(t){let e=super.toJSON(t);return this.fog!==null&&(e.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(e.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(e.object.backgroundIntensity=this.backgroundIntensity),e.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(e.object.environmentIntensity=this.environmentIntensity),e.object.environmentRotation=this.environmentRotation.toArray(),e}},Rn=new P,ti=new P,oc=new P,ei=new P,Ss=new P,ws=new P,Bu=new P,lc=new P,cc=new P,hc=new P,uc=new ve,fc=new ve,dc=new ve,wi=class i{constructor(t=new P,e=new P,n=new P){this.a=t,this.b=e,this.c=n}static getNormal(t,e,n,s){s.subVectors(n,e),Rn.subVectors(t,e),s.cross(Rn);let r=s.lengthSq();return r>0?s.multiplyScalar(1/Math.sqrt(r)):s.set(0,0,0)}static getBarycoord(t,e,n,s,r){Rn.subVectors(s,e),ti.subVectors(n,e),oc.subVectors(t,e);let a=Rn.dot(Rn),o=Rn.dot(ti),l=Rn.dot(oc),c=ti.dot(ti),h=ti.dot(oc),f=a*c-o*o;if(f===0)return r.set(0,0,0),null;let u=1/f,d=(c*l-o*h)*u,m=(a*h-o*l)*u;return r.set(1-d-m,m,d)}static containsPoint(t,e,n,s){return this.getBarycoord(t,e,n,s,ei)===null?!1:ei.x>=0&&ei.y>=0&&ei.x+ei.y<=1}static getInterpolation(t,e,n,s,r,a,o,l){return this.getBarycoord(t,e,n,s,ei)===null?(l.x=0,l.y=0,"z"in l&&(l.z=0),"w"in l&&(l.w=0),null):(l.setScalar(0),l.addScaledVector(r,ei.x),l.addScaledVector(a,ei.y),l.addScaledVector(o,ei.z),l)}static getInterpolatedAttribute(t,e,n,s,r,a){return uc.setScalar(0),fc.setScalar(0),dc.setScalar(0),uc.fromBufferAttribute(t,e),fc.fromBufferAttribute(t,n),dc.fromBufferAttribute(t,s),a.setScalar(0),a.addScaledVector(uc,r.x),a.addScaledVector(fc,r.y),a.addScaledVector(dc,r.z),a}static isFrontFacing(t,e,n,s){return Rn.subVectors(n,e),ti.subVectors(t,e),Rn.cross(ti).dot(s)<0}set(t,e,n){return this.a.copy(t),this.b.copy(e),this.c.copy(n),this}setFromPointsAndIndices(t,e,n,s){return this.a.copy(t[e]),this.b.copy(t[n]),this.c.copy(t[s]),this}setFromAttributeAndIndices(t,e,n,s){return this.a.fromBufferAttribute(t,e),this.b.fromBufferAttribute(t,n),this.c.fromBufferAttribute(t,s),this}clone(){return new this.constructor().copy(this)}copy(t){return this.a.copy(t.a),this.b.copy(t.b),this.c.copy(t.c),this}getArea(){return Rn.subVectors(this.c,this.b),ti.subVectors(this.a,this.b),Rn.cross(ti).length()*.5}getMidpoint(t){return t.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(t){return i.getNormal(this.a,this.b,this.c,t)}getPlane(t){return t.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(t,e){return i.getBarycoord(t,this.a,this.b,this.c,e)}getInterpolation(t,e,n,s,r){return i.getInterpolation(t,this.a,this.b,this.c,e,n,s,r)}containsPoint(t){return i.containsPoint(t,this.a,this.b,this.c)}isFrontFacing(t){return i.isFrontFacing(this.a,this.b,this.c,t)}intersectsBox(t){return t.intersectsTriangle(this)}closestPointToPoint(t,e){let n=this.a,s=this.b,r=this.c,a,o;Ss.subVectors(s,n),ws.subVectors(r,n),lc.subVectors(t,n);let l=Ss.dot(lc),c=ws.dot(lc);if(l<=0&&c<=0)return e.copy(n);cc.subVectors(t,s);let h=Ss.dot(cc),f=ws.dot(cc);if(h>=0&&f<=h)return e.copy(s);let u=l*f-h*c;if(u<=0&&l>=0&&h<=0)return a=l/(l-h),e.copy(n).addScaledVector(Ss,a);hc.subVectors(t,r);let d=Ss.dot(hc),m=ws.dot(hc);if(m>=0&&d<=m)return e.copy(r);let _=d*c-l*m;if(_<=0&&c>=0&&m<=0)return o=c/(c-m),e.copy(n).addScaledVector(ws,o);let g=h*m-d*f;if(g<=0&&f-h>=0&&d-m>=0)return Bu.subVectors(r,s),o=(f-h)/(f-h+(d-m)),e.copy(s).addScaledVector(Bu,o);let p=1/(g+_+u);return a=_*p,o=u*p,e.copy(n).addScaledVector(Ss,a).addScaledVector(ws,o)}equals(t){return t.a.equals(this.a)&&t.b.equals(this.b)&&t.c.equals(this.c)}},Ei=class{constructor(t=new P(1/0,1/0,1/0),e=new P(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=t,this.max=e}set(t,e){return this.min.copy(t),this.max.copy(e),this}setFromArray(t){this.makeEmpty();for(let e=0,n=t.length;e<n;e+=3)this.expandByPoint(Pn.fromArray(t,e));return this}setFromBufferAttribute(t){this.makeEmpty();for(let e=0,n=t.count;e<n;e++)this.expandByPoint(Pn.fromBufferAttribute(t,e));return this}setFromPoints(t){this.makeEmpty();for(let e=0,n=t.length;e<n;e++)this.expandByPoint(t[e]);return this}setFromCenterAndSize(t,e){let n=Pn.copy(e).multiplyScalar(.5);return this.min.copy(t).sub(n),this.max.copy(t).add(n),this}setFromObject(t,e=!1){return this.makeEmpty(),this.expandByObject(t,e)}clone(){return new this.constructor().copy(this)}copy(t){return this.min.copy(t.min),this.max.copy(t.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(t){return this.isEmpty()?t.set(0,0,0):t.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(t){return this.isEmpty()?t.set(0,0,0):t.subVectors(this.max,this.min)}expandByPoint(t){return this.min.min(t),this.max.max(t),this}expandByVector(t){return this.min.sub(t),this.max.add(t),this}expandByScalar(t){return this.min.addScalar(-t),this.max.addScalar(t),this}expandByObject(t,e=!1){t.updateWorldMatrix(!1,!1);let n=t.geometry;if(n!==void 0){let r=n.getAttribute("position");if(e===!0&&r!==void 0&&t.isInstancedMesh!==!0)for(let a=0,o=r.count;a<o;a++)t.isMesh===!0?t.getVertexPosition(a,Pn):Pn.fromBufferAttribute(r,a),Pn.applyMatrix4(t.matrixWorld),this.expandByPoint(Pn);else t.boundingBox!==void 0?(t.boundingBox===null&&t.computeBoundingBox(),da.copy(t.boundingBox)):(n.boundingBox===null&&n.computeBoundingBox(),da.copy(n.boundingBox)),da.applyMatrix4(t.matrixWorld),this.union(da)}let s=t.children;for(let r=0,a=s.length;r<a;r++)this.expandByObject(s[r],e);return this}containsPoint(t){return t.x>=this.min.x&&t.x<=this.max.x&&t.y>=this.min.y&&t.y<=this.max.y&&t.z>=this.min.z&&t.z<=this.max.z}containsBox(t){return this.min.x<=t.min.x&&t.max.x<=this.max.x&&this.min.y<=t.min.y&&t.max.y<=this.max.y&&this.min.z<=t.min.z&&t.max.z<=this.max.z}getParameter(t,e){return e.set((t.x-this.min.x)/(this.max.x-this.min.x),(t.y-this.min.y)/(this.max.y-this.min.y),(t.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(t){return t.max.x>=this.min.x&&t.min.x<=this.max.x&&t.max.y>=this.min.y&&t.min.y<=this.max.y&&t.max.z>=this.min.z&&t.min.z<=this.max.z}intersectsSphere(t){return this.clampPoint(t.center,Pn),Pn.distanceToSquared(t.center)<=t.radius*t.radius}intersectsPlane(t){let e,n;return t.normal.x>0?(e=t.normal.x*this.min.x,n=t.normal.x*this.max.x):(e=t.normal.x*this.max.x,n=t.normal.x*this.min.x),t.normal.y>0?(e+=t.normal.y*this.min.y,n+=t.normal.y*this.max.y):(e+=t.normal.y*this.max.y,n+=t.normal.y*this.min.y),t.normal.z>0?(e+=t.normal.z*this.min.z,n+=t.normal.z*this.max.z):(e+=t.normal.z*this.max.z,n+=t.normal.z*this.min.z),e<=-t.constant&&n>=-t.constant}intersectsTriangle(t){if(this.isEmpty())return!1;this.getCenter(sr),pa.subVectors(this.max,sr),As.subVectors(t.a,sr),Ts.subVectors(t.b,sr),Es.subVectors(t.c,sr),yi.subVectors(Ts,As),Mi.subVectors(Es,Ts),ji.subVectors(As,Es);let e=[0,-yi.z,yi.y,0,-Mi.z,Mi.y,0,-ji.z,ji.y,yi.z,0,-yi.x,Mi.z,0,-Mi.x,ji.z,0,-ji.x,-yi.y,yi.x,0,-Mi.y,Mi.x,0,-ji.y,ji.x,0];return!pc(e,As,Ts,Es,pa)||(e=[1,0,0,0,1,0,0,0,1],!pc(e,As,Ts,Es,pa))?!1:(ma.crossVectors(yi,Mi),e=[ma.x,ma.y,ma.z],pc(e,As,Ts,Es,pa))}clampPoint(t,e){return e.copy(t).clamp(this.min,this.max)}distanceToPoint(t){return this.clampPoint(t,Pn).distanceTo(t)}getBoundingSphere(t){return this.isEmpty()?t.makeEmpty():(this.getCenter(t.center),t.radius=this.getSize(Pn).length()*.5),t}intersect(t){return this.min.max(t.min),this.max.min(t.max),this.isEmpty()&&this.makeEmpty(),this}union(t){return this.min.min(t.min),this.max.max(t.max),this}applyMatrix4(t){return this.isEmpty()?this:(ni[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(t),ni[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(t),ni[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(t),ni[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(t),ni[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(t),ni[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(t),ni[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(t),ni[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(t),this.setFromPoints(ni),this)}translate(t){return this.min.add(t),this.max.add(t),this}equals(t){return t.min.equals(this.min)&&t.max.equals(this.max)}toJSON(){return{min:this.min.toArray(),max:this.max.toArray()}}fromJSON(t){return this.min.fromArray(t.min),this.max.fromArray(t.max),this}},ni=[new P,new P,new P,new P,new P,new P,new P,new P],Pn=new P,da=new Ei,As=new P,Ts=new P,Es=new P,yi=new P,Mi=new P,ji=new P,sr=new P,pa=new P,ma=new P,Qi=new P;function pc(i,t,e,n,s){for(let r=0,a=i.length-3;r<=a;r+=3){Qi.fromArray(i,r);let o=s.x*Math.abs(Qi.x)+s.y*Math.abs(Qi.y)+s.z*Math.abs(Qi.z),l=t.dot(Qi),c=e.dot(Qi),h=n.dot(Qi);if(Math.max(-Math.max(l,c,h),Math.min(l,c,h))>o)return!1}return!0}var Ce=new P,ga=new Et,hg=0,Lt=class extends Ln{constructor(t,e,n=!1){if(super(),Array.isArray(t))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:hg++}),this.name="",this.array=t,this.itemSize=e,this.count=t!==void 0?t.length/e:0,this.normalized=n,this.usage=Ic,this.updateRanges=[],this.gpuType=Un,this.version=0}onUploadCallback(){}set needsUpdate(t){t===!0&&this.version++}setUsage(t){return this.usage=t,this}addUpdateRange(t,e){this.updateRanges.push({start:t,count:e})}clearUpdateRanges(){this.updateRanges.length=0}copy(t){return this.name=t.name,this.array=new t.array.constructor(t.array),this.itemSize=t.itemSize,this.count=t.count,this.normalized=t.normalized,this.usage=t.usage,this.gpuType=t.gpuType,this}copyAt(t,e,n){t*=this.itemSize,n*=e.itemSize;for(let s=0,r=this.itemSize;s<r;s++)this.array[t+s]=e.array[n+s];return this}copyArray(t){return this.array.set(t),this}applyMatrix3(t){if(this.itemSize===2)for(let e=0,n=this.count;e<n;e++)ga.fromBufferAttribute(this,e),ga.applyMatrix3(t),this.setXY(e,ga.x,ga.y);else if(this.itemSize===3)for(let e=0,n=this.count;e<n;e++)Ce.fromBufferAttribute(this,e),Ce.applyMatrix3(t),this.setXYZ(e,Ce.x,Ce.y,Ce.z);return this}applyMatrix4(t){for(let e=0,n=this.count;e<n;e++)Ce.fromBufferAttribute(this,e),Ce.applyMatrix4(t),this.setXYZ(e,Ce.x,Ce.y,Ce.z);return this}applyNormalMatrix(t){for(let e=0,n=this.count;e<n;e++)Ce.fromBufferAttribute(this,e),Ce.applyNormalMatrix(t),this.setXYZ(e,Ce.x,Ce.y,Ce.z);return this}transformDirection(t){for(let e=0,n=this.count;e<n;e++)Ce.fromBufferAttribute(this,e),Ce.transformDirection(t),this.setXYZ(e,Ce.x,Ce.y,Ce.z);return this}set(t,e=0){return this.array.set(t,e),this}getComponent(t,e){let n=this.array[t*this.itemSize+e];return this.normalized&&(n=Is(n,this.array)),n}setComponent(t,e,n){return this.normalized&&(n=$e(n,this.array)),this.array[t*this.itemSize+e]=n,this}getX(t){let e=this.array[t*this.itemSize];return this.normalized&&(e=Is(e,this.array)),e}setX(t,e){return this.normalized&&(e=$e(e,this.array)),this.array[t*this.itemSize]=e,this}getY(t){let e=this.array[t*this.itemSize+1];return this.normalized&&(e=Is(e,this.array)),e}setY(t,e){return this.normalized&&(e=$e(e,this.array)),this.array[t*this.itemSize+1]=e,this}getZ(t){let e=this.array[t*this.itemSize+2];return this.normalized&&(e=Is(e,this.array)),e}setZ(t,e){return this.normalized&&(e=$e(e,this.array)),this.array[t*this.itemSize+2]=e,this}getW(t){let e=this.array[t*this.itemSize+3];return this.normalized&&(e=Is(e,this.array)),e}setW(t,e){return this.normalized&&(e=$e(e,this.array)),this.array[t*this.itemSize+3]=e,this}setXY(t,e,n){return t*=this.itemSize,this.normalized&&(e=$e(e,this.array),n=$e(n,this.array)),this.array[t+0]=e,this.array[t+1]=n,this}setXYZ(t,e,n,s){return t*=this.itemSize,this.normalized&&(e=$e(e,this.array),n=$e(n,this.array),s=$e(s,this.array)),this.array[t+0]=e,this.array[t+1]=n,this.array[t+2]=s,this}setXYZW(t,e,n,s,r){return t*=this.itemSize,this.normalized&&(e=$e(e,this.array),n=$e(n,this.array),s=$e(s,this.array),r=$e(r,this.array)),this.array[t+0]=e,this.array[t+1]=n,this.array[t+2]=s,this.array[t+3]=r,this}onUpload(t){return this.onUploadCallback=t,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){let t={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(t.name=this.name),this.usage!==Ic&&(t.usage=this.usage),t}dispose(){this.dispatchEvent({type:"dispose"})}};var xr=class extends Lt{constructor(t,e,n){super(new Uint16Array(t),e,n)}};var vr=class extends Lt{constructor(t,e,n){super(new Uint32Array(t),e,n)}};var Ve=class extends Lt{constructor(t,e,n){super(new Float32Array(t),e,n)}},ug=new Ei,rr=new P,mc=new P,Ci=class{constructor(t=new P,e=-1){this.isSphere=!0,this.center=t,this.radius=e}set(t,e){return this.center.copy(t),this.radius=e,this}setFromPoints(t,e){let n=this.center;e!==void 0?n.copy(e):ug.setFromPoints(t).getCenter(n);let s=0;for(let r=0,a=t.length;r<a;r++)s=Math.max(s,n.distanceToSquared(t[r]));return this.radius=Math.sqrt(s),this}copy(t){return this.center.copy(t.center),this.radius=t.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(t){return t.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(t){return t.distanceTo(this.center)-this.radius}intersectsSphere(t){let e=this.radius+t.radius;return t.center.distanceToSquared(this.center)<=e*e}intersectsBox(t){return t.intersectsSphere(this)}intersectsPlane(t){return Math.abs(t.distanceToPoint(this.center))<=this.radius}clampPoint(t,e){let n=this.center.distanceToSquared(t);return e.copy(t),n>this.radius*this.radius&&(e.sub(this.center).normalize(),e.multiplyScalar(this.radius).add(this.center)),e}getBoundingBox(t){return this.isEmpty()?(t.makeEmpty(),t):(t.set(this.center,this.center),t.expandByScalar(this.radius),t)}applyMatrix4(t){return this.center.applyMatrix4(t),this.radius=this.radius*t.getMaxScaleOnAxis(),this}translate(t){return this.center.add(t),this}expandByPoint(t){if(this.isEmpty())return this.center.copy(t),this.radius=0,this;rr.subVectors(t,this.center);let e=rr.lengthSq();if(e>this.radius*this.radius){let n=Math.sqrt(e),s=(n-this.radius)*.5;this.center.addScaledVector(rr,s/n),this.radius+=s}return this}union(t){return t.isEmpty()?this:this.isEmpty()?(this.copy(t),this):(this.center.equals(t.center)===!0?this.radius=Math.max(this.radius,t.radius):(mc.subVectors(t.center,this.center).setLength(t.radius),this.expandByPoint(rr.copy(t.center).add(mc)),this.expandByPoint(rr.copy(t.center).sub(mc))),this)}equals(t){return t.center.equals(this.center)&&t.radius===this.radius}clone(){return new this.constructor().copy(this)}toJSON(){return{radius:this.radius,center:this.center.toArray()}}fromJSON(t){return this.radius=t.radius,this.center.fromArray(t.center),this}},fg=0,bn=new ge,gc=new sn,Cs=new P,pn=new Ei,ar=new Ei,Oe=new P,te=class i extends Ln{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:fg++}),this.uuid=Gs(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.indirectOffset=0,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(t){return Array.isArray(t)?this.index=new(Um(t)?vr:xr)(t,1):this.index=t,this}setIndirect(t,e=0){return this.indirect=t,this.indirectOffset=e,this}getIndirect(){return this.indirect}getAttribute(t){return this.attributes[t]}setAttribute(t,e){return this.attributes[t]=e,this}deleteAttribute(t){return delete this.attributes[t],this}hasAttribute(t){return this.attributes[t]!==void 0}addGroup(t,e,n=0){this.groups.push({start:t,count:e,materialIndex:n})}clearGroups(){this.groups=[]}setDrawRange(t,e){this.drawRange.start=t,this.drawRange.count=e}applyMatrix4(t){let e=this.attributes.position;e!==void 0&&(e.applyMatrix4(t),e.needsUpdate=!0);let n=this.attributes.normal;if(n!==void 0){let r=new Ft().getNormalMatrix(t);n.applyNormalMatrix(r),n.needsUpdate=!0}let s=this.attributes.tangent;return s!==void 0&&(s.transformDirection(t),s.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(t){return bn.makeRotationFromQuaternion(t),this.applyMatrix4(bn),this}rotateX(t){return bn.makeRotationX(t),this.applyMatrix4(bn),this}rotateY(t){return bn.makeRotationY(t),this.applyMatrix4(bn),this}rotateZ(t){return bn.makeRotationZ(t),this.applyMatrix4(bn),this}translate(t,e,n){return bn.makeTranslation(t,e,n),this.applyMatrix4(bn),this}scale(t,e,n){return bn.makeScale(t,e,n),this.applyMatrix4(bn),this}lookAt(t){return gc.lookAt(t),gc.updateMatrix(),this.applyMatrix4(gc.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(Cs).negate(),this.translate(Cs.x,Cs.y,Cs.z),this}setFromPoints(t){let e=this.getAttribute("position");if(e===void 0){let n=[];for(let s=0,r=t.length;s<r;s++){let a=t[s];n.push(a.x,a.y,a.z||0)}this.setAttribute("position",new Ve(n,3))}else{let n=Math.min(t.length,e.count);for(let s=0;s<n;s++){let r=t[s];e.setXYZ(s,r.x,r.y,r.z||0)}t.length>e.count&&Ct("BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),e.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Ei);let t=this.attributes.position,e=this.morphAttributes.position;if(t&&t.isGLBufferAttribute){Pt("BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new P(-1/0,-1/0,-1/0),new P(1/0,1/0,1/0));return}if(t!==void 0){if(this.boundingBox.setFromBufferAttribute(t),e)for(let n=0,s=e.length;n<s;n++){let r=e[n];pn.setFromBufferAttribute(r),this.morphTargetsRelative?(Oe.addVectors(this.boundingBox.min,pn.min),this.boundingBox.expandByPoint(Oe),Oe.addVectors(this.boundingBox.max,pn.max),this.boundingBox.expandByPoint(Oe)):(this.boundingBox.expandByPoint(pn.min),this.boundingBox.expandByPoint(pn.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&Pt('BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new Ci);let t=this.attributes.position,e=this.morphAttributes.position;if(t&&t.isGLBufferAttribute){Pt("BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new P,1/0);return}if(t){let n=this.boundingSphere.center;if(pn.setFromBufferAttribute(t),e)for(let r=0,a=e.length;r<a;r++){let o=e[r];ar.setFromBufferAttribute(o),this.morphTargetsRelative?(Oe.addVectors(pn.min,ar.min),pn.expandByPoint(Oe),Oe.addVectors(pn.max,ar.max),pn.expandByPoint(Oe)):(pn.expandByPoint(ar.min),pn.expandByPoint(ar.max))}pn.getCenter(n);let s=0;for(let r=0,a=t.count;r<a;r++)Oe.fromBufferAttribute(t,r),s=Math.max(s,n.distanceToSquared(Oe));if(e)for(let r=0,a=e.length;r<a;r++){let o=e[r],l=this.morphTargetsRelative;for(let c=0,h=o.count;c<h;c++)Oe.fromBufferAttribute(o,c),l&&(Cs.fromBufferAttribute(t,c),Oe.add(Cs)),s=Math.max(s,n.distanceToSquared(Oe))}this.boundingSphere.radius=Math.sqrt(s),isNaN(this.boundingSphere.radius)&&Pt('BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){let t=this.index,e=this.attributes;if(t===null||e.position===void 0||e.normal===void 0||e.uv===void 0){Pt("BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}let n=e.position,s=e.normal,r=e.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new Lt(new Float32Array(4*n.count),4));let a=this.getAttribute("tangent"),o=[],l=[];for(let v=0;v<n.count;v++)o[v]=new P,l[v]=new P;let c=new P,h=new P,f=new P,u=new Et,d=new Et,m=new Et,_=new P,g=new P;function p(v,E,L){c.fromBufferAttribute(n,v),h.fromBufferAttribute(n,E),f.fromBufferAttribute(n,L),u.fromBufferAttribute(r,v),d.fromBufferAttribute(r,E),m.fromBufferAttribute(r,L),h.sub(c),f.sub(c),d.sub(u),m.sub(u);let C=1/(d.x*m.y-m.x*d.y);isFinite(C)&&(_.copy(h).multiplyScalar(m.y).addScaledVector(f,-d.y).multiplyScalar(C),g.copy(f).multiplyScalar(d.x).addScaledVector(h,-m.x).multiplyScalar(C),o[v].add(_),o[E].add(_),o[L].add(_),l[v].add(g),l[E].add(g),l[L].add(g))}let y=this.groups;y.length===0&&(y=[{start:0,count:t.count}]);for(let v=0,E=y.length;v<E;++v){let L=y[v],C=L.start,D=L.count;for(let H=C,W=C+D;H<W;H+=3)p(t.getX(H+0),t.getX(H+1),t.getX(H+2))}let S=new P,b=new P,T=new P,w=new P;function R(v){T.fromBufferAttribute(s,v),w.copy(T);let E=o[v];S.copy(E),S.sub(T.multiplyScalar(T.dot(E))).normalize(),b.crossVectors(w,E);let C=b.dot(l[v])<0?-1:1;a.setXYZW(v,S.x,S.y,S.z,C)}for(let v=0,E=y.length;v<E;++v){let L=y[v],C=L.start,D=L.count;for(let H=C,W=C+D;H<W;H+=3)R(t.getX(H+0)),R(t.getX(H+1)),R(t.getX(H+2))}}computeVertexNormals(){let t=this.index,e=this.getAttribute("position");if(e!==void 0){let n=this.getAttribute("normal");if(n===void 0)n=new Lt(new Float32Array(e.count*3),3),this.setAttribute("normal",n);else for(let u=0,d=n.count;u<d;u++)n.setXYZ(u,0,0,0);let s=new P,r=new P,a=new P,o=new P,l=new P,c=new P,h=new P,f=new P;if(t)for(let u=0,d=t.count;u<d;u+=3){let m=t.getX(u+0),_=t.getX(u+1),g=t.getX(u+2);s.fromBufferAttribute(e,m),r.fromBufferAttribute(e,_),a.fromBufferAttribute(e,g),h.subVectors(a,r),f.subVectors(s,r),h.cross(f),o.fromBufferAttribute(n,m),l.fromBufferAttribute(n,_),c.fromBufferAttribute(n,g),o.add(h),l.add(h),c.add(h),n.setXYZ(m,o.x,o.y,o.z),n.setXYZ(_,l.x,l.y,l.z),n.setXYZ(g,c.x,c.y,c.z)}else for(let u=0,d=e.count;u<d;u+=3)s.fromBufferAttribute(e,u+0),r.fromBufferAttribute(e,u+1),a.fromBufferAttribute(e,u+2),h.subVectors(a,r),f.subVectors(s,r),h.cross(f),n.setXYZ(u+0,h.x,h.y,h.z),n.setXYZ(u+1,h.x,h.y,h.z),n.setXYZ(u+2,h.x,h.y,h.z);this.normalizeNormals(),n.needsUpdate=!0}}normalizeNormals(){let t=this.attributes.normal;for(let e=0,n=t.count;e<n;e++)Oe.fromBufferAttribute(t,e),Oe.normalize(),t.setXYZ(e,Oe.x,Oe.y,Oe.z)}toNonIndexed(){function t(o,l){let c=o.array,h=o.itemSize,f=o.normalized,u=new c.constructor(l.length*h),d=0,m=0;for(let _=0,g=l.length;_<g;_++){o.isInterleavedBufferAttribute?d=l[_]*o.data.stride+o.offset:d=l[_]*h;for(let p=0;p<h;p++)u[m++]=c[d++]}return new Lt(u,h,f)}if(this.index===null)return Ct("BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;let e=new i,n=this.index.array,s=this.attributes;for(let o in s){let l=s[o],c=t(l,n);e.setAttribute(o,c)}let r=this.morphAttributes;for(let o in r){let l=[],c=r[o];for(let h=0,f=c.length;h<f;h++){let u=c[h],d=t(u,n);l.push(d)}e.morphAttributes[o]=l}e.morphTargetsRelative=this.morphTargetsRelative;let a=this.groups;for(let o=0,l=a.length;o<l;o++){let c=a[o];e.addGroup(c.start,c.count,c.materialIndex)}return e}toJSON(){let t={metadata:{version:4.7,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(t.uuid=this.uuid,t.type=this.type,this.name!==""&&(t.name=this.name),Object.keys(this.userData).length>0&&(t.userData=this.userData),this.parameters!==void 0){let l=this.parameters;for(let c in l)l[c]!==void 0&&(t[c]=l[c]);return t}t.data={attributes:{}};let e=this.index;e!==null&&(t.data.index={type:e.array.constructor.name,array:Array.prototype.slice.call(e.array)});let n=this.attributes;for(let l in n){let c=n[l];t.data.attributes[l]=c.toJSON(t.data)}let s={},r=!1;for(let l in this.morphAttributes){let c=this.morphAttributes[l],h=[];for(let f=0,u=c.length;f<u;f++){let d=c[f];h.push(d.toJSON(t.data))}h.length>0&&(s[l]=h,r=!0)}r&&(t.data.morphAttributes=s,t.data.morphTargetsRelative=this.morphTargetsRelative);let a=this.groups;a.length>0&&(t.data.groups=JSON.parse(JSON.stringify(a)));let o=this.boundingSphere;return o!==null&&(t.data.boundingSphere=o.toJSON()),t}clone(){return new this.constructor().copy(this)}copy(t){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;let e={};this.name=t.name;let n=t.index;n!==null&&this.setIndex(n.clone());let s=t.attributes;for(let c in s){let h=s[c];this.setAttribute(c,h.clone(e))}let r=t.morphAttributes;for(let c in r){let h=[],f=r[c];for(let u=0,d=f.length;u<d;u++)h.push(f[u].clone(e));this.morphAttributes[c]=h}this.morphTargetsRelative=t.morphTargetsRelative;let a=t.groups;for(let c=0,h=a.length;c<h;c++){let f=a[c];this.addGroup(f.start,f.count,f.materialIndex)}let o=t.boundingBox;o!==null&&(this.boundingBox=o.clone());let l=t.boundingSphere;return l!==null&&(this.boundingSphere=l.clone()),this.drawRange.start=t.drawRange.start,this.drawRange.count=t.drawRange.count,this.userData=t.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}};var dg=0,oi=class extends Ln{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:dg++}),this.uuid=Gs(),this.name="",this.type="Material",this.blending=Gn,this.side=ai,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Fa,this.blendDst=Ua,this.blendEquation=Ai,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new dt(0,0,0),this.blendAlpha=0,this.depthFunc=is,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=Pc,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=ns,this.stencilZFail=ns,this.stencilZPass=ns,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.allowOverride=!0,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(t){this._alphaTest>0!=t>0&&this.version++,this._alphaTest=t}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(t){if(t!==void 0)for(let e in t){let n=t[e];if(n===void 0){Ct(`Material: parameter '${e}' has value of undefined.`);continue}let s=this[e];if(s===void 0){Ct(`Material: '${e}' is not a property of THREE.${this.type}.`);continue}s&&s.isColor?s.set(n):s&&s.isVector3&&n&&n.isVector3?s.copy(n):this[e]=n}}toJSON(t){let e=t===void 0||typeof t=="string";e&&(t={textures:{},images:{}});let n={metadata:{version:4.7,type:"Material",generator:"Material.toJSON"}};n.uuid=this.uuid,n.type=this.type,this.name!==""&&(n.name=this.name),this.color&&this.color.isColor&&(n.color=this.color.getHex()),this.roughness!==void 0&&(n.roughness=this.roughness),this.metalness!==void 0&&(n.metalness=this.metalness),this.sheen!==void 0&&(n.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(n.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(n.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(n.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(n.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(n.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(n.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(n.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(n.shininess=this.shininess),this.clearcoat!==void 0&&(n.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(n.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(n.clearcoatMap=this.clearcoatMap.toJSON(t).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(n.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(t).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(n.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(t).uuid,n.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.sheenColorMap&&this.sheenColorMap.isTexture&&(n.sheenColorMap=this.sheenColorMap.toJSON(t).uuid),this.sheenRoughnessMap&&this.sheenRoughnessMap.isTexture&&(n.sheenRoughnessMap=this.sheenRoughnessMap.toJSON(t).uuid),this.dispersion!==void 0&&(n.dispersion=this.dispersion),this.iridescence!==void 0&&(n.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(n.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(n.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(n.iridescenceMap=this.iridescenceMap.toJSON(t).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(n.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(t).uuid),this.anisotropy!==void 0&&(n.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(n.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(n.anisotropyMap=this.anisotropyMap.toJSON(t).uuid),this.map&&this.map.isTexture&&(n.map=this.map.toJSON(t).uuid),this.matcap&&this.matcap.isTexture&&(n.matcap=this.matcap.toJSON(t).uuid),this.alphaMap&&this.alphaMap.isTexture&&(n.alphaMap=this.alphaMap.toJSON(t).uuid),this.lightMap&&this.lightMap.isTexture&&(n.lightMap=this.lightMap.toJSON(t).uuid,n.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(n.aoMap=this.aoMap.toJSON(t).uuid,n.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(n.bumpMap=this.bumpMap.toJSON(t).uuid,n.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(n.normalMap=this.normalMap.toJSON(t).uuid,n.normalMapType=this.normalMapType,n.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(n.displacementMap=this.displacementMap.toJSON(t).uuid,n.displacementScale=this.displacementScale,n.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(n.roughnessMap=this.roughnessMap.toJSON(t).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(n.metalnessMap=this.metalnessMap.toJSON(t).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(n.emissiveMap=this.emissiveMap.toJSON(t).uuid),this.specularMap&&this.specularMap.isTexture&&(n.specularMap=this.specularMap.toJSON(t).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(n.specularIntensityMap=this.specularIntensityMap.toJSON(t).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(n.specularColorMap=this.specularColorMap.toJSON(t).uuid),this.envMap&&this.envMap.isTexture&&(n.envMap=this.envMap.toJSON(t).uuid,this.combine!==void 0&&(n.combine=this.combine)),this.envMapRotation!==void 0&&(n.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(n.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(n.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(n.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(n.gradientMap=this.gradientMap.toJSON(t).uuid),this.transmission!==void 0&&(n.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(n.transmissionMap=this.transmissionMap.toJSON(t).uuid),this.thickness!==void 0&&(n.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(n.thicknessMap=this.thicknessMap.toJSON(t).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(n.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(n.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(n.size=this.size),this.shadowSide!==null&&(n.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(n.sizeAttenuation=this.sizeAttenuation),this.blending!==Gn&&(n.blending=this.blending),this.side!==ai&&(n.side=this.side),this.vertexColors===!0&&(n.vertexColors=!0),this.opacity<1&&(n.opacity=this.opacity),this.transparent===!0&&(n.transparent=!0),this.blendSrc!==Fa&&(n.blendSrc=this.blendSrc),this.blendDst!==Ua&&(n.blendDst=this.blendDst),this.blendEquation!==Ai&&(n.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(n.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(n.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(n.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(n.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(n.blendAlpha=this.blendAlpha),this.depthFunc!==is&&(n.depthFunc=this.depthFunc),this.depthTest===!1&&(n.depthTest=this.depthTest),this.depthWrite===!1&&(n.depthWrite=this.depthWrite),this.colorWrite===!1&&(n.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(n.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==Pc&&(n.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(n.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(n.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==ns&&(n.stencilFail=this.stencilFail),this.stencilZFail!==ns&&(n.stencilZFail=this.stencilZFail),this.stencilZPass!==ns&&(n.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(n.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(n.rotation=this.rotation),this.polygonOffset===!0&&(n.polygonOffset=!0),this.polygonOffsetFactor!==0&&(n.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(n.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(n.linewidth=this.linewidth),this.dashSize!==void 0&&(n.dashSize=this.dashSize),this.gapSize!==void 0&&(n.gapSize=this.gapSize),this.scale!==void 0&&(n.scale=this.scale),this.dithering===!0&&(n.dithering=!0),this.alphaTest>0&&(n.alphaTest=this.alphaTest),this.alphaHash===!0&&(n.alphaHash=!0),this.alphaToCoverage===!0&&(n.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(n.premultipliedAlpha=!0),this.forceSinglePass===!0&&(n.forceSinglePass=!0),this.allowOverride===!1&&(n.allowOverride=!1),this.wireframe===!0&&(n.wireframe=!0),this.wireframeLinewidth>1&&(n.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(n.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(n.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(n.flatShading=!0),this.visible===!1&&(n.visible=!1),this.toneMapped===!1&&(n.toneMapped=!1),this.fog===!1&&(n.fog=!1),Object.keys(this.userData).length>0&&(n.userData=this.userData);function s(r){let a=[];for(let o in r){let l=r[o];delete l.metadata,a.push(l)}return a}if(e){let r=s(t.textures),a=s(t.images);r.length>0&&(n.textures=r),a.length>0&&(n.images=a)}return n}clone(){return new this.constructor().copy(this)}copy(t){this.name=t.name,this.blending=t.blending,this.side=t.side,this.vertexColors=t.vertexColors,this.opacity=t.opacity,this.transparent=t.transparent,this.blendSrc=t.blendSrc,this.blendDst=t.blendDst,this.blendEquation=t.blendEquation,this.blendSrcAlpha=t.blendSrcAlpha,this.blendDstAlpha=t.blendDstAlpha,this.blendEquationAlpha=t.blendEquationAlpha,this.blendColor.copy(t.blendColor),this.blendAlpha=t.blendAlpha,this.depthFunc=t.depthFunc,this.depthTest=t.depthTest,this.depthWrite=t.depthWrite,this.stencilWriteMask=t.stencilWriteMask,this.stencilFunc=t.stencilFunc,this.stencilRef=t.stencilRef,this.stencilFuncMask=t.stencilFuncMask,this.stencilFail=t.stencilFail,this.stencilZFail=t.stencilZFail,this.stencilZPass=t.stencilZPass,this.stencilWrite=t.stencilWrite;let e=t.clippingPlanes,n=null;if(e!==null){let s=e.length;n=new Array(s);for(let r=0;r!==s;++r)n[r]=e[r].clone()}return this.clippingPlanes=n,this.clipIntersection=t.clipIntersection,this.clipShadows=t.clipShadows,this.shadowSide=t.shadowSide,this.colorWrite=t.colorWrite,this.precision=t.precision,this.polygonOffset=t.polygonOffset,this.polygonOffsetFactor=t.polygonOffsetFactor,this.polygonOffsetUnits=t.polygonOffsetUnits,this.dithering=t.dithering,this.alphaTest=t.alphaTest,this.alphaHash=t.alphaHash,this.alphaToCoverage=t.alphaToCoverage,this.premultipliedAlpha=t.premultipliedAlpha,this.forceSinglePass=t.forceSinglePass,this.allowOverride=t.allowOverride,this.visible=t.visible,this.toneMapped=t.toneMapped,this.userData=JSON.parse(JSON.stringify(t.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(t){t===!0&&this.version++}};var ii=new P,_c=new P,_a=new P,bi=new P,xc=new P,xa=new P,vc=new P,Ri=class{constructor(t=new P,e=new P(0,0,-1)){this.origin=t,this.direction=e}set(t,e){return this.origin.copy(t),this.direction.copy(e),this}copy(t){return this.origin.copy(t.origin),this.direction.copy(t.direction),this}at(t,e){return e.copy(this.origin).addScaledVector(this.direction,t)}lookAt(t){return this.direction.copy(t).sub(this.origin).normalize(),this}recast(t){return this.origin.copy(this.at(t,ii)),this}closestPointToPoint(t,e){e.subVectors(t,this.origin);let n=e.dot(this.direction);return n<0?e.copy(this.origin):e.copy(this.origin).addScaledVector(this.direction,n)}distanceToPoint(t){return Math.sqrt(this.distanceSqToPoint(t))}distanceSqToPoint(t){let e=ii.subVectors(t,this.origin).dot(this.direction);return e<0?this.origin.distanceToSquared(t):(ii.copy(this.origin).addScaledVector(this.direction,e),ii.distanceToSquared(t))}distanceSqToSegment(t,e,n,s){_c.copy(t).add(e).multiplyScalar(.5),_a.copy(e).sub(t).normalize(),bi.copy(this.origin).sub(_c);let r=t.distanceTo(e)*.5,a=-this.direction.dot(_a),o=bi.dot(this.direction),l=-bi.dot(_a),c=bi.lengthSq(),h=Math.abs(1-a*a),f,u,d,m;if(h>0)if(f=a*l-o,u=a*o-l,m=r*h,f>=0)if(u>=-m)if(u<=m){let _=1/h;f*=_,u*=_,d=f*(f+a*u+2*o)+u*(a*f+u+2*l)+c}else u=r,f=Math.max(0,-(a*u+o)),d=-f*f+u*(u+2*l)+c;else u=-r,f=Math.max(0,-(a*u+o)),d=-f*f+u*(u+2*l)+c;else u<=-m?(f=Math.max(0,-(-a*r+o)),u=f>0?-r:Math.min(Math.max(-r,-l),r),d=-f*f+u*(u+2*l)+c):u<=m?(f=0,u=Math.min(Math.max(-r,-l),r),d=u*(u+2*l)+c):(f=Math.max(0,-(a*r+o)),u=f>0?r:Math.min(Math.max(-r,-l),r),d=-f*f+u*(u+2*l)+c);else u=a>0?-r:r,f=Math.max(0,-(a*u+o)),d=-f*f+u*(u+2*l)+c;return n&&n.copy(this.origin).addScaledVector(this.direction,f),s&&s.copy(_c).addScaledVector(_a,u),d}intersectSphere(t,e){ii.subVectors(t.center,this.origin);let n=ii.dot(this.direction),s=ii.dot(ii)-n*n,r=t.radius*t.radius;if(s>r)return null;let a=Math.sqrt(r-s),o=n-a,l=n+a;return l<0?null:o<0?this.at(l,e):this.at(o,e)}intersectsSphere(t){return t.radius<0?!1:this.distanceSqToPoint(t.center)<=t.radius*t.radius}distanceToPlane(t){let e=t.normal.dot(this.direction);if(e===0)return t.distanceToPoint(this.origin)===0?0:null;let n=-(this.origin.dot(t.normal)+t.constant)/e;return n>=0?n:null}intersectPlane(t,e){let n=this.distanceToPlane(t);return n===null?null:this.at(n,e)}intersectsPlane(t){let e=t.distanceToPoint(this.origin);return e===0||t.normal.dot(this.direction)*e<0}intersectBox(t,e){let n,s,r,a,o,l,c=1/this.direction.x,h=1/this.direction.y,f=1/this.direction.z,u=this.origin;return c>=0?(n=(t.min.x-u.x)*c,s=(t.max.x-u.x)*c):(n=(t.max.x-u.x)*c,s=(t.min.x-u.x)*c),h>=0?(r=(t.min.y-u.y)*h,a=(t.max.y-u.y)*h):(r=(t.max.y-u.y)*h,a=(t.min.y-u.y)*h),n>a||r>s||((r>n||isNaN(n))&&(n=r),(a<s||isNaN(s))&&(s=a),f>=0?(o=(t.min.z-u.z)*f,l=(t.max.z-u.z)*f):(o=(t.max.z-u.z)*f,l=(t.min.z-u.z)*f),n>l||o>s)||((o>n||n!==n)&&(n=o),(l<s||s!==s)&&(s=l),s<0)?null:this.at(n>=0?n:s,e)}intersectsBox(t){return this.intersectBox(t,ii)!==null}intersectTriangle(t,e,n,s,r){xc.subVectors(e,t),xa.subVectors(n,t),vc.crossVectors(xc,xa);let a=this.direction.dot(vc),o;if(a>0){if(s)return null;o=1}else if(a<0)o=-1,a=-a;else return null;bi.subVectors(this.origin,t);let l=o*this.direction.dot(xa.crossVectors(bi,xa));if(l<0)return null;let c=o*this.direction.dot(xc.cross(bi));if(c<0||l+c>a)return null;let h=-o*bi.dot(vc);return h<0?null:this.at(h/a,r)}applyMatrix4(t){return this.origin.applyMatrix4(t),this.direction.transformDirection(t),this}equals(t){return t.origin.equals(this.origin)&&t.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}},ss=class extends oi{constructor(t){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new dt(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new Ti,this.combine=Bc,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(t)}copy(t){return super.copy(t),this.color.copy(t.color),this.map=t.map,this.lightMap=t.lightMap,this.lightMapIntensity=t.lightMapIntensity,this.aoMap=t.aoMap,this.aoMapIntensity=t.aoMapIntensity,this.specularMap=t.specularMap,this.alphaMap=t.alphaMap,this.envMap=t.envMap,this.envMapRotation.copy(t.envMapRotation),this.combine=t.combine,this.reflectivity=t.reflectivity,this.refractionRatio=t.refractionRatio,this.wireframe=t.wireframe,this.wireframeLinewidth=t.wireframeLinewidth,this.wireframeLinecap=t.wireframeLinecap,this.wireframeLinejoin=t.wireframeLinejoin,this.fog=t.fog,this}},ku=new ge,ts=new Ri,va=new Ci,zu=new P,ya=new P,Ma=new P,ba=new P,yc=new P,Sa=new P,Vu=new P,wa=new P,rn=class extends sn{constructor(t=new te,e=new ss){super(),this.isMesh=!0,this.type="Mesh",this.geometry=t,this.material=e,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.count=1,this.updateMorphTargets()}copy(t,e){return super.copy(t,e),t.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=t.morphTargetInfluences.slice()),t.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},t.morphTargetDictionary)),this.material=Array.isArray(t.material)?t.material.slice():t.material,this.geometry=t.geometry,this}updateMorphTargets(){let e=this.geometry.morphAttributes,n=Object.keys(e);if(n.length>0){let s=e[n[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,a=s.length;r<a;r++){let o=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=r}}}}getVertexPosition(t,e){let n=this.geometry,s=n.attributes.position,r=n.morphAttributes.position,a=n.morphTargetsRelative;e.fromBufferAttribute(s,t);let o=this.morphTargetInfluences;if(r&&o){Sa.set(0,0,0);for(let l=0,c=r.length;l<c;l++){let h=o[l],f=r[l];h!==0&&(yc.fromBufferAttribute(f,t),a?Sa.addScaledVector(yc,h):Sa.addScaledVector(yc.sub(e),h))}e.add(Sa)}return e}raycast(t,e){let n=this.geometry,s=this.material,r=this.matrixWorld;s!==void 0&&(n.boundingSphere===null&&n.computeBoundingSphere(),va.copy(n.boundingSphere),va.applyMatrix4(r),ts.copy(t.ray).recast(t.near),!(va.containsPoint(ts.origin)===!1&&(ts.intersectSphere(va,zu)===null||ts.origin.distanceToSquared(zu)>(t.far-t.near)**2))&&(ku.copy(r).invert(),ts.copy(t.ray).applyMatrix4(ku),!(n.boundingBox!==null&&ts.intersectsBox(n.boundingBox)===!1)&&this._computeIntersections(t,e,ts)))}_computeIntersections(t,e,n){let s,r=this.geometry,a=this.material,o=r.index,l=r.attributes.position,c=r.attributes.uv,h=r.attributes.uv1,f=r.attributes.normal,u=r.groups,d=r.drawRange;if(o!==null)if(Array.isArray(a))for(let m=0,_=u.length;m<_;m++){let g=u[m],p=a[g.materialIndex],y=Math.max(g.start,d.start),S=Math.min(o.count,Math.min(g.start+g.count,d.start+d.count));for(let b=y,T=S;b<T;b+=3){let w=o.getX(b),R=o.getX(b+1),v=o.getX(b+2);s=Aa(this,p,t,n,c,h,f,w,R,v),s&&(s.faceIndex=Math.floor(b/3),s.face.materialIndex=g.materialIndex,e.push(s))}}else{let m=Math.max(0,d.start),_=Math.min(o.count,d.start+d.count);for(let g=m,p=_;g<p;g+=3){let y=o.getX(g),S=o.getX(g+1),b=o.getX(g+2);s=Aa(this,a,t,n,c,h,f,y,S,b),s&&(s.faceIndex=Math.floor(g/3),e.push(s))}}else if(l!==void 0)if(Array.isArray(a))for(let m=0,_=u.length;m<_;m++){let g=u[m],p=a[g.materialIndex],y=Math.max(g.start,d.start),S=Math.min(l.count,Math.min(g.start+g.count,d.start+d.count));for(let b=y,T=S;b<T;b+=3){let w=b,R=b+1,v=b+2;s=Aa(this,p,t,n,c,h,f,w,R,v),s&&(s.faceIndex=Math.floor(b/3),s.face.materialIndex=g.materialIndex,e.push(s))}}else{let m=Math.max(0,d.start),_=Math.min(l.count,d.start+d.count);for(let g=m,p=_;g<p;g+=3){let y=g,S=g+1,b=g+2;s=Aa(this,a,t,n,c,h,f,y,S,b),s&&(s.faceIndex=Math.floor(g/3),e.push(s))}}}};function pg(i,t,e,n,s,r,a,o){let l;if(t.side===je?l=n.intersectTriangle(a,r,s,!0,o):l=n.intersectTriangle(s,r,a,t.side===ai,o),l===null)return null;wa.copy(o),wa.applyMatrix4(i.matrixWorld);let c=e.ray.origin.distanceTo(wa);return c<e.near||c>e.far?null:{distance:c,point:wa.clone(),object:i}}function Aa(i,t,e,n,s,r,a,o,l,c){i.getVertexPosition(o,ya),i.getVertexPosition(l,Ma),i.getVertexPosition(c,ba);let h=pg(i,t,e,n,ya,Ma,ba,Vu);if(h){let f=new P;wi.getBarycoord(Vu,ya,Ma,ba,f),s&&(h.uv=wi.getInterpolatedAttribute(s,o,l,c,f,new Et)),r&&(h.uv1=wi.getInterpolatedAttribute(r,o,l,c,f,new Et)),a&&(h.normal=wi.getInterpolatedAttribute(a,o,l,c,f,new P),h.normal.dot(n.direction)>0&&h.normal.multiplyScalar(-1));let u={a:o,b:l,c,normal:new P,materialIndex:0};wi.getNormal(ya,Ma,ba,u.normal),h.face=u,h.barycoord=f}return h}var $a=class extends nn{constructor(t=null,e=1,n=1,s,r,a,o,l,c=Be,h=Be,f,u){super(null,a,o,l,c,h,s,r,f,u),this.isDataTexture=!0,this.image={data:t,width:e,height:n},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}};var Mc=new P,mg=new P,gg=new Ft,Sn=class{constructor(t=new P(1,0,0),e=0){this.isPlane=!0,this.normal=t,this.constant=e}set(t,e){return this.normal.copy(t),this.constant=e,this}setComponents(t,e,n,s){return this.normal.set(t,e,n),this.constant=s,this}setFromNormalAndCoplanarPoint(t,e){return this.normal.copy(t),this.constant=-e.dot(this.normal),this}setFromCoplanarPoints(t,e,n){let s=Mc.subVectors(n,e).cross(mg.subVectors(t,e)).normalize();return this.setFromNormalAndCoplanarPoint(s,t),this}copy(t){return this.normal.copy(t.normal),this.constant=t.constant,this}normalize(){let t=1/this.normal.length();return this.normal.multiplyScalar(t),this.constant*=t,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(t){return this.normal.dot(t)+this.constant}distanceToSphere(t){return this.distanceToPoint(t.center)-t.radius}projectPoint(t,e){return e.copy(t).addScaledVector(this.normal,-this.distanceToPoint(t))}intersectLine(t,e,n=!0){let s=t.delta(Mc),r=this.normal.dot(s);if(r===0)return this.distanceToPoint(t.start)===0?e.copy(t.start):null;let a=-(t.start.dot(this.normal)+this.constant)/r;return n===!0&&(a<0||a>1)?null:e.copy(t.start).addScaledVector(s,a)}intersectsLine(t){let e=this.distanceToPoint(t.start),n=this.distanceToPoint(t.end);return e<0&&n>0||n<0&&e>0}intersectsBox(t){return t.intersectsPlane(this)}intersectsSphere(t){return t.intersectsPlane(this)}coplanarPoint(t){return t.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(t,e){let n=e||gg.getNormalMatrix(t),s=this.coplanarPoint(Mc).applyMatrix4(t),r=this.normal.applyMatrix3(n).normalize();return this.constant=-s.dot(r),this}translate(t){return this.constant-=t.dot(this.normal),this}equals(t){return t.normal.equals(this.normal)&&t.constant===this.constant}clone(){return new this.constructor().copy(this)}},es=new Ci,_g=new Et(.5,.5),Ta=new P,yr=class{constructor(t=new Sn,e=new Sn,n=new Sn,s=new Sn,r=new Sn,a=new Sn){this.planes=[t,e,n,s,r,a]}set(t,e,n,s,r,a){let o=this.planes;return o[0].copy(t),o[1].copy(e),o[2].copy(n),o[3].copy(s),o[4].copy(r),o[5].copy(a),this}copy(t){let e=this.planes;for(let n=0;n<6;n++)e[n].copy(t.planes[n]);return this}setFromProjectionMatrix(t,e=In,n=!1){let s=this.planes,r=t.elements,a=r[0],o=r[1],l=r[2],c=r[3],h=r[4],f=r[5],u=r[6],d=r[7],m=r[8],_=r[9],g=r[10],p=r[11],y=r[12],S=r[13],b=r[14],T=r[15];if(s[0].setComponents(c-a,d-h,p-m,T-y).normalize(),s[1].setComponents(c+a,d+h,p+m,T+y).normalize(),s[2].setComponents(c+o,d+f,p+_,T+S).normalize(),s[3].setComponents(c-o,d-f,p-_,T-S).normalize(),n)s[4].setComponents(l,u,g,b).normalize(),s[5].setComponents(c-l,d-u,p-g,T-b).normalize();else if(s[4].setComponents(c-l,d-u,p-g,T-b).normalize(),e===In)s[5].setComponents(c+l,d+u,p+g,T+b).normalize();else if(e===dr)s[5].setComponents(l,u,g,b).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+e);return this}intersectsObject(t){if(t.boundingSphere!==void 0)t.boundingSphere===null&&t.computeBoundingSphere(),es.copy(t.boundingSphere).applyMatrix4(t.matrixWorld);else{let e=t.geometry;e.boundingSphere===null&&e.computeBoundingSphere(),es.copy(e.boundingSphere).applyMatrix4(t.matrixWorld)}return this.intersectsSphere(es)}intersectsSprite(t){es.center.set(0,0,0);let e=_g.distanceTo(t.center);return es.radius=.7071067811865476+e,es.applyMatrix4(t.matrixWorld),this.intersectsSphere(es)}intersectsSphere(t){let e=this.planes,n=t.center,s=-t.radius;for(let r=0;r<6;r++)if(e[r].distanceToPoint(n)<s)return!1;return!0}intersectsBox(t){let e=this.planes;for(let n=0;n<6;n++){let s=e[n];if(Ta.x=s.normal.x>0?t.max.x:t.min.x,Ta.y=s.normal.y>0?t.max.y:t.min.y,Ta.z=s.normal.z>0?t.max.z:t.min.z,s.distanceToPoint(Ta)<0)return!1}return!0}containsPoint(t){let e=this.planes;for(let n=0;n<6;n++)if(e[n].distanceToPoint(t)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}};var li=class extends oi{constructor(t){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new dt(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(t)}copy(t){return super.copy(t),this.color.copy(t.color),this.map=t.map,this.linewidth=t.linewidth,this.linecap=t.linecap,this.linejoin=t.linejoin,this.fog=t.fog,this}},ja=new P,Qa=new P,Gu=new ge,or=new Ri,Ea=new Ci,bc=new P,Hu=new P,to=class extends sn{constructor(t=new te,e=new li){super(),this.isLine=!0,this.type="Line",this.geometry=t,this.material=e,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(t,e){return super.copy(t,e),this.material=Array.isArray(t.material)?t.material.slice():t.material,this.geometry=t.geometry,this}computeLineDistances(){let t=this.geometry;if(t.index===null){let e=t.attributes.position,n=[0];for(let s=1,r=e.count;s<r;s++)ja.fromBufferAttribute(e,s-1),Qa.fromBufferAttribute(e,s),n[s]=n[s-1],n[s]+=ja.distanceTo(Qa);t.setAttribute("lineDistance",new Ve(n,1))}else Ct("Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(t,e){let n=this.geometry,s=this.matrixWorld,r=t.params.Line.threshold,a=n.drawRange;if(n.boundingSphere===null&&n.computeBoundingSphere(),Ea.copy(n.boundingSphere),Ea.applyMatrix4(s),Ea.radius+=r,t.ray.intersectsSphere(Ea)===!1)return;Gu.copy(s).invert(),or.copy(t.ray).applyMatrix4(Gu);let o=r/((this.scale.x+this.scale.y+this.scale.z)/3),l=o*o,c=this.isLineSegments?2:1,h=n.index,u=n.attributes.position;if(h!==null){let d=Math.max(0,a.start),m=Math.min(h.count,a.start+a.count);for(let _=d,g=m-1;_<g;_+=c){let p=h.getX(_),y=h.getX(_+1),S=Ca(this,t,or,l,p,y,_);S&&e.push(S)}if(this.isLineLoop){let _=h.getX(m-1),g=h.getX(d),p=Ca(this,t,or,l,_,g,m-1);p&&e.push(p)}}else{let d=Math.max(0,a.start),m=Math.min(u.count,a.start+a.count);for(let _=d,g=m-1;_<g;_+=c){let p=Ca(this,t,or,l,_,_+1,_);p&&e.push(p)}if(this.isLineLoop){let _=Ca(this,t,or,l,m-1,d,m-1);_&&e.push(_)}}}updateMorphTargets(){let e=this.geometry.morphAttributes,n=Object.keys(e);if(n.length>0){let s=e[n[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,a=s.length;r<a;r++){let o=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=r}}}}};function Ca(i,t,e,n,s,r,a){let o=i.geometry.attributes.position;if(ja.fromBufferAttribute(o,s),Qa.fromBufferAttribute(o,r),e.distanceSqToSegment(ja,Qa,bc,Hu)>n)return;bc.applyMatrix4(i.matrixWorld);let c=t.ray.origin.distanceTo(bc);if(!(c<t.near||c>t.far))return{distance:c,point:Hu.clone().applyMatrix4(i.matrixWorld),index:a,face:null,faceIndex:null,barycoord:null,object:i}}var Wu=new P,Xu=new P,rs=class extends to{constructor(t,e){super(t,e),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){let t=this.geometry;if(t.index===null){let e=t.attributes.position,n=[];for(let s=0,r=e.count;s<r;s+=2)Wu.fromBufferAttribute(e,s),Xu.fromBufferAttribute(e,s+1),n[s]=s===0?0:n[s-1],n[s+1]=n[s]+Wu.distanceTo(Xu);t.setAttribute("lineDistance",new Ve(n,1))}else Ct("LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}};var ci=class extends oi{constructor(t){super(),this.isPointsMaterial=!0,this.type="PointsMaterial",this.color=new dt(16777215),this.map=null,this.alphaMap=null,this.size=1,this.sizeAttenuation=!0,this.fog=!0,this.setValues(t)}copy(t){return super.copy(t),this.color.copy(t.color),this.map=t.map,this.alphaMap=t.alphaMap,this.size=t.size,this.sizeAttenuation=t.sizeAttenuation,this.fog=t.fog,this}},qu=new ge,Lc=new Ri,Ra=new Ci,Pa=new P,an=class extends sn{constructor(t=new te,e=new ci){super(),this.isPoints=!0,this.type="Points",this.geometry=t,this.material=e,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(t,e){return super.copy(t,e),this.material=Array.isArray(t.material)?t.material.slice():t.material,this.geometry=t.geometry,this}raycast(t,e){let n=this.geometry,s=this.matrixWorld,r=t.params.Points.threshold,a=n.drawRange;if(n.boundingSphere===null&&n.computeBoundingSphere(),Ra.copy(n.boundingSphere),Ra.applyMatrix4(s),Ra.radius+=r,t.ray.intersectsSphere(Ra)===!1)return;qu.copy(s).invert(),Lc.copy(t.ray).applyMatrix4(qu);let o=r/((this.scale.x+this.scale.y+this.scale.z)/3),l=o*o,c=n.index,f=n.attributes.position;if(c!==null){let u=Math.max(0,a.start),d=Math.min(c.count,a.start+a.count);for(let m=u,_=d;m<_;m++){let g=c.getX(m);Pa.fromBufferAttribute(f,g),Yu(Pa,g,l,s,t,e,this)}}else{let u=Math.max(0,a.start),d=Math.min(f.count,a.start+a.count);for(let m=u,_=d;m<_;m++)Pa.fromBufferAttribute(f,m),Yu(Pa,m,l,s,t,e,this)}}updateMorphTargets(){let e=this.geometry.morphAttributes,n=Object.keys(e);if(n.length>0){let s=e[n[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,a=s.length;r<a;r++){let o=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=r}}}}};function Yu(i,t,e,n,s,r,a){let o=Lc.distanceSqToPoint(i);if(o<e){let l=new P;Lc.closestPointToPoint(i,l),l.applyMatrix4(n);let c=s.ray.origin.distanceTo(l);if(c<s.near||c>s.far)return;r.push({distance:c,distanceToRay:Math.sqrt(o),point:l,index:t,face:null,faceIndex:null,barycoord:null,object:a})}}var Mr=class extends nn{constructor(t=[],e=Fi,n,s,r,a,o,l,c,h){super(t,e,n,s,r,a,o,l,c,h),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(t){this.image=t}};var hi=class extends nn{constructor(t,e,n=Fn,s,r,a,o=Be,l=Be,c,h=Hn,f=1){if(h!==Hn&&h!==Oi)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");let u={width:t,height:e,depth:f};super(u,s,r,a,o,l,h,n,c),this.isDepthTexture=!0,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(t){return super.copy(t),this.source=new Fs(Object.assign({},t.image)),this.compareFunction=t.compareFunction,this}toJSON(t){let e=super.toJSON(t);return this.compareFunction!==null&&(e.compareFunction=this.compareFunction),e}},eo=class extends hi{constructor(t,e=Fn,n=Fi,s,r,a=Be,o=Be,l,c=Hn){let h={width:t,height:t,depth:1},f=[h,h,h,h,h,h];super(t,t,e,n,s,r,a,o,l,c),this.image=f,this.isCubeDepthTexture=!0,this.isCubeTexture=!0}get images(){return this.image}set images(t){this.image=t}},br=class extends nn{constructor(t=null){super(),this.sourceTexture=t,this.isExternalTexture=!0}copy(t){return super.copy(t),this.sourceTexture=t.sourceTexture,this}},Os=class i extends te{constructor(t=1,e=1,n=1,s=1,r=1,a=1){super(),this.type="BoxGeometry",this.parameters={width:t,height:e,depth:n,widthSegments:s,heightSegments:r,depthSegments:a};let o=this;s=Math.floor(s),r=Math.floor(r),a=Math.floor(a);let l=[],c=[],h=[],f=[],u=0,d=0;m("z","y","x",-1,-1,n,e,t,a,r,0),m("z","y","x",1,-1,n,e,-t,a,r,1),m("x","z","y",1,1,t,n,e,s,a,2),m("x","z","y",1,-1,t,n,-e,s,a,3),m("x","y","z",1,-1,t,e,n,s,r,4),m("x","y","z",-1,-1,t,e,-n,s,r,5),this.setIndex(l),this.setAttribute("position",new Ve(c,3)),this.setAttribute("normal",new Ve(h,3)),this.setAttribute("uv",new Ve(f,2));function m(_,g,p,y,S,b,T,w,R,v,E){let L=b/R,C=T/v,D=b/2,H=T/2,W=w/2,U=R+1,z=v+1,V=0,$=0,tt=new P;for(let ct=0;ct<z;ct++){let Mt=ct*C-H;for(let St=0;St<U;St++){let qt=St*L-D;tt[_]=qt*y,tt[g]=Mt*S,tt[p]=W,c.push(tt.x,tt.y,tt.z),tt[_]=0,tt[g]=0,tt[p]=w>0?1:-1,h.push(tt.x,tt.y,tt.z),f.push(St/R),f.push(1-ct/v),V+=1}}for(let ct=0;ct<v;ct++)for(let Mt=0;Mt<R;Mt++){let St=u+Mt+U*ct,qt=u+Mt+U*(ct+1),ee=u+(Mt+1)+U*(ct+1),kt=u+(Mt+1)+U*ct;l.push(St,qt,kt),l.push(qt,ee,kt),$+=6}o.addGroup(d,$,E),d+=$,u+=V}}copy(t){return super.copy(t),this.parameters=Object.assign({},t.parameters),this}static fromJSON(t){return new i(t.width,t.height,t.depth,t.widthSegments,t.heightSegments,t.depthSegments)}};var no=class{constructor(){this.type="Curve",this.arcLengthDivisions=200,this.needsUpdate=!1,this.cacheArcLengths=null}getPoint(){Ct("Curve: .getPoint() not implemented.")}getPointAt(t,e){let n=this.getUtoTmapping(t);return this.getPoint(n,e)}getPoints(t=5){let e=[];for(let n=0;n<=t;n++)e.push(this.getPoint(n/t));return e}getSpacedPoints(t=5){let e=[];for(let n=0;n<=t;n++)e.push(this.getPointAt(n/t));return e}getLength(){let t=this.getLengths();return t[t.length-1]}getLengths(t=this.arcLengthDivisions){if(this.cacheArcLengths&&this.cacheArcLengths.length===t+1&&!this.needsUpdate)return this.cacheArcLengths;this.needsUpdate=!1;let e=[],n,s=this.getPoint(0),r=0;e.push(0);for(let a=1;a<=t;a++)n=this.getPoint(a/t),r+=n.distanceTo(s),e.push(r),s=n;return this.cacheArcLengths=e,e}updateArcLengths(){this.needsUpdate=!0,this.getLengths()}getUtoTmapping(t,e=null){let n=this.getLengths(),s=0,r=n.length,a;e?a=e:a=t*n[r-1];let o=0,l=r-1,c;for(;o<=l;)if(s=Math.floor(o+(l-o)/2),c=n[s]-a,c<0)o=s+1;else if(c>0)l=s-1;else{l=s;break}if(s=l,n[s]===a)return s/(r-1);let h=n[s],u=n[s+1]-h,d=(a-h)/u;return(s+d)/(r-1)}getTangent(t,e){let s=t-1e-4,r=t+1e-4;s<0&&(s=0),r>1&&(r=1);let a=this.getPoint(s),o=this.getPoint(r),l=e||(a.isVector2?new Et:new P);return l.copy(o).sub(a).normalize(),l}getTangentAt(t,e){let n=this.getUtoTmapping(t);return this.getTangent(n,e)}computeFrenetFrames(t,e=!1){let n=new P,s=[],r=[],a=[],o=new P,l=new ge;for(let d=0;d<=t;d++){let m=d/t;s[d]=this.getTangentAt(m,new P)}r[0]=new P,a[0]=new P;let c=Number.MAX_VALUE,h=Math.abs(s[0].x),f=Math.abs(s[0].y),u=Math.abs(s[0].z);h<=c&&(c=h,n.set(1,0,0)),f<=c&&(c=f,n.set(0,1,0)),u<=c&&n.set(0,0,1),o.crossVectors(s[0],n).normalize(),r[0].crossVectors(s[0],o),a[0].crossVectors(s[0],r[0]);for(let d=1;d<=t;d++){if(r[d]=r[d-1].clone(),a[d]=a[d-1].clone(),o.crossVectors(s[d-1],s[d]),o.length()>Number.EPSILON){o.normalize();let m=Math.acos(Vt(s[d-1].dot(s[d]),-1,1));r[d].applyMatrix4(l.makeRotationAxis(o,m))}a[d].crossVectors(s[d],r[d])}if(e===!0){let d=Math.acos(Vt(r[0].dot(r[t]),-1,1));d/=t,s[0].dot(o.crossVectors(r[0],r[t]))>0&&(d=-d);for(let m=1;m<=t;m++)r[m].applyMatrix4(l.makeRotationAxis(s[m],d*m)),a[m].crossVectors(s[m],r[m])}return{tangents:s,normals:r,binormals:a}}clone(){return new this.constructor().copy(this)}copy(t){return this.arcLengthDivisions=t.arcLengthDivisions,this}toJSON(){let t={metadata:{version:4.7,type:"Curve",generator:"Curve.toJSON"}};return t.arcLengthDivisions=this.arcLengthDivisions,t.type=this.type,t}fromJSON(t){return this.arcLengthDivisions=t.arcLengthDivisions,this}};function jc(){let i=0,t=0,e=0,n=0;function s(r,a,o,l){i=r,t=o,e=-3*r+3*a-2*o-l,n=2*r-2*a+o+l}return{initCatmullRom:function(r,a,o,l,c){s(a,o,c*(o-r),c*(l-a))},initNonuniformCatmullRom:function(r,a,o,l,c,h,f){let u=(a-r)/c-(o-r)/(c+h)+(o-a)/h,d=(o-a)/h-(l-a)/(h+f)+(l-o)/f;u*=h,d*=h,s(a,o,u,d)},calc:function(r){let a=r*r,o=a*r;return i+t*r+e*a+n*o}}}var Zu=new P,Ku=new P,Sc=new jc,wc=new jc,Ac=new jc,Sr=class extends no{constructor(t=[],e=!1,n="centripetal",s=.5){super(),this.isCatmullRomCurve3=!0,this.type="CatmullRomCurve3",this.points=t,this.closed=e,this.curveType=n,this.tension=s}getPoint(t,e=new P){let n=e,s=this.points,r=s.length,a=(r-(this.closed?0:1))*t,o=Math.floor(a),l=a-o;this.closed?o+=o>0?0:(Math.floor(Math.abs(o)/r)+1)*r:l===0&&o===r-1&&(o=r-2,l=1);let c,h;this.closed||o>0?c=s[(o-1)%r]:(Ku.subVectors(s[0],s[1]).add(s[0]),c=Ku);let f=s[o%r],u=s[(o+1)%r];if(this.closed||o+2<r?h=s[(o+2)%r]:(Zu.subVectors(s[r-1],s[r-2]).add(s[r-1]),h=Zu),this.curveType==="centripetal"||this.curveType==="chordal"){let d=this.curveType==="chordal"?.5:.25,m=Math.pow(c.distanceToSquared(f),d),_=Math.pow(f.distanceToSquared(u),d),g=Math.pow(u.distanceToSquared(h),d);_<1e-4&&(_=1),m<1e-4&&(m=_),g<1e-4&&(g=_),Sc.initNonuniformCatmullRom(c.x,f.x,u.x,h.x,m,_,g),wc.initNonuniformCatmullRom(c.y,f.y,u.y,h.y,m,_,g),Ac.initNonuniformCatmullRom(c.z,f.z,u.z,h.z,m,_,g)}else this.curveType==="catmullrom"&&(Sc.initCatmullRom(c.x,f.x,u.x,h.x,this.tension),wc.initCatmullRom(c.y,f.y,u.y,h.y,this.tension),Ac.initCatmullRom(c.z,f.z,u.z,h.z,this.tension));return n.set(Sc.calc(l),wc.calc(l),Ac.calc(l)),n}copy(t){super.copy(t),this.points=[];for(let e=0,n=t.points.length;e<n;e++){let s=t.points[e];this.points.push(s.clone())}return this.closed=t.closed,this.curveType=t.curveType,this.tension=t.tension,this}toJSON(){let t=super.toJSON();t.points=[];for(let e=0,n=this.points.length;e<n;e++){let s=this.points[e];t.points.push(s.toArray())}return t.closed=this.closed,t.curveType=this.curveType,t.tension=this.tension,t}fromJSON(t){super.fromJSON(t),this.points=[];for(let e=0,n=t.points.length;e<n;e++){let s=t.points[e];this.points.push(new P().fromArray(s))}return this.closed=t.closed,this.curveType=t.curveType,this.tension=t.tension,this}};var wr=class i extends te{constructor(t=1,e=1,n=1,s=1){super(),this.type="PlaneGeometry",this.parameters={width:t,height:e,widthSegments:n,heightSegments:s};let r=t/2,a=e/2,o=Math.floor(n),l=Math.floor(s),c=o+1,h=l+1,f=t/o,u=e/l,d=[],m=[],_=[],g=[];for(let p=0;p<h;p++){let y=p*u-a;for(let S=0;S<c;S++){let b=S*f-r;m.push(b,-y,0),_.push(0,0,1),g.push(S/o),g.push(1-p/l)}}for(let p=0;p<l;p++)for(let y=0;y<o;y++){let S=y+c*p,b=y+c*(p+1),T=y+1+c*(p+1),w=y+1+c*p;d.push(S,b,w),d.push(b,T,w)}this.setIndex(d),this.setAttribute("position",new Ve(m,3)),this.setAttribute("normal",new Ve(_,3)),this.setAttribute("uv",new Ve(g,2))}copy(t){return super.copy(t),this.parameters=Object.assign({},t.parameters),this}static fromJSON(t){return new i(t.width,t.height,t.widthSegments,t.heightSegments)}};function ls(i){let t={};for(let e in i){t[e]={};for(let n in i[e]){let s=i[e][n];if(Ju(s))s.isRenderTargetTexture?(Ct("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),t[e][n]=null):t[e][n]=s.clone();else if(Array.isArray(s))if(Ju(s[0])){let r=[];for(let a=0,o=s.length;a<o;a++)r[a]=s[a].clone();t[e][n]=r}else t[e][n]=s.slice();else t[e][n]=s}}return t}function Ke(i){let t={};for(let e=0;e<i.length;e++){let n=ls(i[e]);for(let s in n)t[s]=n[s]}return t}function Ju(i){return i&&(i.isColor||i.isMatrix3||i.isMatrix4||i.isVector2||i.isVector3||i.isVector4||i.isTexture||i.isQuaternion)}function xg(i){let t=[];for(let e=0;e<i.length;e++)t.push(i[e].clone());return t}function Qc(i){let t=i.getRenderTarget();return t===null?i.outputColorSpace:t.isXRRenderTarget===!0?t.texture.colorSpace:Wt.workingColorSpace}var fi={clone:ls,merge:Ke},vg=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,yg=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`,re=class extends oi{constructor(t){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=vg,this.fragmentShader=yg,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,t!==void 0&&this.setValues(t)}copy(t){return super.copy(t),this.fragmentShader=t.fragmentShader,this.vertexShader=t.vertexShader,this.uniforms=ls(t.uniforms),this.uniformsGroups=xg(t.uniformsGroups),this.defines=Object.assign({},t.defines),this.wireframe=t.wireframe,this.wireframeLinewidth=t.wireframeLinewidth,this.fog=t.fog,this.lights=t.lights,this.clipping=t.clipping,this.extensions=Object.assign({},t.extensions),this.glslVersion=t.glslVersion,this.defaultAttributeValues=Object.assign({},t.defaultAttributeValues),this.index0AttributeName=t.index0AttributeName,this.uniformsNeedUpdate=t.uniformsNeedUpdate,this}toJSON(t){let e=super.toJSON(t);e.glslVersion=this.glslVersion,e.uniforms={};for(let s in this.uniforms){let a=this.uniforms[s].value;a&&a.isTexture?e.uniforms[s]={type:"t",value:a.toJSON(t).uuid}:a&&a.isColor?e.uniforms[s]={type:"c",value:a.getHex()}:a&&a.isVector2?e.uniforms[s]={type:"v2",value:a.toArray()}:a&&a.isVector3?e.uniforms[s]={type:"v3",value:a.toArray()}:a&&a.isVector4?e.uniforms[s]={type:"v4",value:a.toArray()}:a&&a.isMatrix3?e.uniforms[s]={type:"m3",value:a.toArray()}:a&&a.isMatrix4?e.uniforms[s]={type:"m4",value:a.toArray()}:e.uniforms[s]={value:a}}Object.keys(this.defines).length>0&&(e.defines=this.defines),e.vertexShader=this.vertexShader,e.fragmentShader=this.fragmentShader,e.lights=this.lights,e.clipping=this.clipping;let n={};for(let s in this.extensions)this.extensions[s]===!0&&(n[s]=!0);return Object.keys(n).length>0&&(e.extensions=n),e}},Bs=class extends re{constructor(t){super(t),this.isRawShaderMaterial=!0,this.type="RawShaderMaterial"}};var io=class extends oi{constructor(t){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=wf,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(t)}copy(t){return super.copy(t),this.depthPacking=t.depthPacking,this.map=t.map,this.alphaMap=t.alphaMap,this.displacementMap=t.displacementMap,this.displacementScale=t.displacementScale,this.displacementBias=t.displacementBias,this.wireframe=t.wireframe,this.wireframeLinewidth=t.wireframeLinewidth,this}},so=class extends oi{constructor(t){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(t)}copy(t){return super.copy(t),this.map=t.map,this.alphaMap=t.alphaMap,this.displacementMap=t.displacementMap,this.displacementScale=t.displacementScale,this.displacementBias=t.displacementBias,this}};var Ar=class extends li{constructor(t){super(),this.isLineDashedMaterial=!0,this.type="LineDashedMaterial",this.scale=1,this.dashSize=3,this.gapSize=1,this.setValues(t)}copy(t){return super.copy(t),this.scale=t.scale,this.dashSize=t.dashSize,this.gapSize=t.gapSize,this}};function Ia(i,t){return!i||i.constructor===t?i:typeof t.BYTES_PER_ELEMENT=="number"?new t(i):Array.prototype.slice.call(i)}var Pi=class{constructor(t,e,n,s){this.parameterPositions=t,this._cachedIndex=0,this.resultBuffer=s!==void 0?s:new e.constructor(n),this.sampleValues=e,this.valueSize=n,this.settings=null,this.DefaultSettings_={}}evaluate(t){let e=this.parameterPositions,n=this._cachedIndex,s=e[n],r=e[n-1];n:{t:{let a;e:{i:if(!(t<s)){for(let o=n+2;;){if(s===void 0){if(t<r)break i;return n=e.length,this._cachedIndex=n,this.copySampleValue_(n-1)}if(n===o)break;if(r=s,s=e[++n],t<s)break t}a=e.length;break e}if(!(t>=r)){let o=e[1];t<o&&(n=2,r=o);for(let l=n-2;;){if(r===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(n===l)break;if(s=r,r=e[--n-1],t>=r)break t}a=n,n=0;break e}break n}for(;n<a;){let o=n+a>>>1;t<e[o]?a=o:n=o+1}if(s=e[n],r=e[n-1],r===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(s===void 0)return n=e.length,this._cachedIndex=n,this.copySampleValue_(n-1)}this._cachedIndex=n,this.intervalChanged_(n,r,s)}return this.interpolate_(n,r,t,s)}getSettings_(){return this.settings||this.DefaultSettings_}copySampleValue_(t){let e=this.resultBuffer,n=this.sampleValues,s=this.valueSize,r=t*s;for(let a=0;a!==s;++a)e[a]=n[r+a];return e}interpolate_(){throw new Error("call to abstract method")}intervalChanged_(){}},ro=class extends Pi{constructor(t,e,n,s){super(t,e,n,s),this._weightPrev=-0,this._offsetPrev=-0,this._weightNext=-0,this._offsetNext=-0,this.DefaultSettings_={endingStart:Ec,endingEnd:Ec}}intervalChanged_(t,e,n){let s=this.parameterPositions,r=t-2,a=t+1,o=s[r],l=s[a];if(o===void 0)switch(this.getSettings_().endingStart){case Cc:r=t,o=2*e-n;break;case Rc:r=s.length-2,o=e+s[r]-s[r+1];break;default:r=t,o=n}if(l===void 0)switch(this.getSettings_().endingEnd){case Cc:a=t,l=2*n-e;break;case Rc:a=1,l=n+s[1]-s[0];break;default:a=t-1,l=e}let c=(n-e)*.5,h=this.valueSize;this._weightPrev=c/(e-o),this._weightNext=c/(l-n),this._offsetPrev=r*h,this._offsetNext=a*h}interpolate_(t,e,n,s){let r=this.resultBuffer,a=this.sampleValues,o=this.valueSize,l=t*o,c=l-o,h=this._offsetPrev,f=this._offsetNext,u=this._weightPrev,d=this._weightNext,m=(n-e)/(s-e),_=m*m,g=_*m,p=-u*g+2*u*_-u*m,y=(1+u)*g+(-1.5-2*u)*_+(-.5+u)*m+1,S=(-1-d)*g+(1.5+d)*_+.5*m,b=d*g-d*_;for(let T=0;T!==o;++T)r[T]=p*a[h+T]+y*a[c+T]+S*a[l+T]+b*a[f+T];return r}},ao=class extends Pi{constructor(t,e,n,s){super(t,e,n,s)}interpolate_(t,e,n,s){let r=this.resultBuffer,a=this.sampleValues,o=this.valueSize,l=t*o,c=l-o,h=(n-e)/(s-e),f=1-h;for(let u=0;u!==o;++u)r[u]=a[c+u]*f+a[l+u]*h;return r}},oo=class extends Pi{constructor(t,e,n,s){super(t,e,n,s)}interpolate_(t){return this.copySampleValue_(t-1)}},lo=class extends Pi{interpolate_(t,e,n,s){let r=this.resultBuffer,a=this.sampleValues,o=this.valueSize,l=t*o,c=l-o,h=this.settings||this.DefaultSettings_,f=h.inTangents,u=h.outTangents;if(!f||!u){let _=(n-e)/(s-e),g=1-_;for(let p=0;p!==o;++p)r[p]=a[c+p]*g+a[l+p]*_;return r}let d=o*2,m=t-1;for(let _=0;_!==o;++_){let g=a[c+_],p=a[l+_],y=m*d+_*2,S=u[y],b=u[y+1],T=t*d+_*2,w=f[T],R=f[T+1],v=(n-e)/(s-e),E,L,C,D,H;for(let W=0;W<8;W++){E=v*v,L=E*v,C=1-v,D=C*C,H=D*C;let z=H*e+3*D*v*S+3*C*E*w+L*s-n;if(Math.abs(z)<1e-10)break;let V=3*D*(S-e)+6*C*v*(w-S)+3*E*(s-w);if(Math.abs(V)<1e-10)break;v=v-z/V,v=Math.max(0,Math.min(1,v))}r[_]=H*g+3*D*v*b+3*C*E*R+L*p}return r}},_n=class{constructor(t,e,n,s){if(t===void 0)throw new Error("THREE.KeyframeTrack: track name is undefined");if(e===void 0||e.length===0)throw new Error("THREE.KeyframeTrack: no keyframes in track named "+t);this.name=t,this.times=Ia(e,this.TimeBufferType),this.values=Ia(n,this.ValueBufferType),this.setInterpolation(s||this.DefaultInterpolation)}static toJSON(t){let e=t.constructor,n;if(e.toJSON!==this.toJSON)n=e.toJSON(t);else{n={name:t.name,times:Ia(t.times,Array),values:Ia(t.values,Array)};let s=t.getInterpolation();s!==t.DefaultInterpolation&&(n.interpolation=s)}return n.type=t.ValueTypeName,n}InterpolantFactoryMethodDiscrete(t){return new oo(this.times,this.values,this.getValueSize(),t)}InterpolantFactoryMethodLinear(t){return new ao(this.times,this.values,this.getValueSize(),t)}InterpolantFactoryMethodSmooth(t){return new ro(this.times,this.values,this.getValueSize(),t)}InterpolantFactoryMethodBezier(t){let e=new lo(this.times,this.values,this.getValueSize(),t);return this.settings&&(e.settings=this.settings),e}setInterpolation(t){let e;switch(t){case hr:e=this.InterpolantFactoryMethodDiscrete;break;case qa:e=this.InterpolantFactoryMethodLinear;break;case Da:e=this.InterpolantFactoryMethodSmooth;break;case Tc:e=this.InterpolantFactoryMethodBezier;break}if(e===void 0){let n="unsupported interpolation for "+this.ValueTypeName+" keyframe track named "+this.name;if(this.createInterpolant===void 0)if(t!==this.DefaultInterpolation)this.setInterpolation(this.DefaultInterpolation);else throw new Error(n);return Ct("KeyframeTrack:",n),this}return this.createInterpolant=e,this}getInterpolation(){switch(this.createInterpolant){case this.InterpolantFactoryMethodDiscrete:return hr;case this.InterpolantFactoryMethodLinear:return qa;case this.InterpolantFactoryMethodSmooth:return Da;case this.InterpolantFactoryMethodBezier:return Tc}}getValueSize(){return this.values.length/this.times.length}shift(t){if(t!==0){let e=this.times;for(let n=0,s=e.length;n!==s;++n)e[n]+=t}return this}scale(t){if(t!==1){let e=this.times;for(let n=0,s=e.length;n!==s;++n)e[n]*=t}return this}trim(t,e){let n=this.times,s=n.length,r=0,a=s-1;for(;r!==s&&n[r]<t;)++r;for(;a!==-1&&n[a]>e;)--a;if(++a,r!==0||a!==s){r>=a&&(a=Math.max(a,1),r=a-1);let o=this.getValueSize();this.times=n.slice(r,a),this.values=this.values.slice(r*o,a*o)}return this}validate(){let t=!0,e=this.getValueSize();e-Math.floor(e)!==0&&(Pt("KeyframeTrack: Invalid value size in track.",this),t=!1);let n=this.times,s=this.values,r=n.length;r===0&&(Pt("KeyframeTrack: Track is empty.",this),t=!1);let a=null;for(let o=0;o!==r;o++){let l=n[o];if(typeof l=="number"&&isNaN(l)){Pt("KeyframeTrack: Time is not a valid number.",this,o,l),t=!1;break}if(a!==null&&a>l){Pt("KeyframeTrack: Out of order keys.",this,o,l,a),t=!1;break}a=l}if(s!==void 0&&Om(s))for(let o=0,l=s.length;o!==l;++o){let c=s[o];if(isNaN(c)){Pt("KeyframeTrack: Value is not a valid number.",this,o,c),t=!1;break}}return t}optimize(){let t=this.times.slice(),e=this.values.slice(),n=this.getValueSize(),s=this.getInterpolation()===Da,r=t.length-1,a=1;for(let o=1;o<r;++o){let l=!1,c=t[o],h=t[o+1];if(c!==h&&(o!==1||c!==t[0]))if(s)l=!0;else{let f=o*n,u=f-n,d=f+n;for(let m=0;m!==n;++m){let _=e[f+m];if(_!==e[u+m]||_!==e[d+m]){l=!0;break}}}if(l){if(o!==a){t[a]=t[o];let f=o*n,u=a*n;for(let d=0;d!==n;++d)e[u+d]=e[f+d]}++a}}if(r>0){t[a]=t[r];for(let o=r*n,l=a*n,c=0;c!==n;++c)e[l+c]=e[o+c];++a}return a!==t.length?(this.times=t.slice(0,a),this.values=e.slice(0,a*n)):(this.times=t,this.values=e),this}clone(){let t=this.times.slice(),e=this.values.slice(),n=this.constructor,s=new n(this.name,t,e);return s.createInterpolant=this.createInterpolant,s}};_n.prototype.ValueTypeName="";_n.prototype.TimeBufferType=Float32Array;_n.prototype.ValueBufferType=Float32Array;_n.prototype.DefaultInterpolation=qa;var Ii=class extends _n{constructor(t,e,n){super(t,e,n)}};Ii.prototype.ValueTypeName="bool";Ii.prototype.ValueBufferType=Array;Ii.prototype.DefaultInterpolation=hr;Ii.prototype.InterpolantFactoryMethodLinear=void 0;Ii.prototype.InterpolantFactoryMethodSmooth=void 0;var co=class extends _n{constructor(t,e,n,s){super(t,e,n,s)}};co.prototype.ValueTypeName="color";var ho=class extends _n{constructor(t,e,n,s){super(t,e,n,s)}};ho.prototype.ValueTypeName="number";var uo=class extends Pi{constructor(t,e,n,s){super(t,e,n,s)}interpolate_(t,e,n,s){let r=this.resultBuffer,a=this.sampleValues,o=this.valueSize,l=(n-e)/(s-e),c=t*o;for(let h=c+o;c!==h;c+=4)gn.slerpFlat(r,0,a,c-o,a,c,l);return r}},Tr=class extends _n{constructor(t,e,n,s){super(t,e,n,s)}InterpolantFactoryMethodLinear(t){return new uo(this.times,this.values,this.getValueSize(),t)}};Tr.prototype.ValueTypeName="quaternion";Tr.prototype.InterpolantFactoryMethodSmooth=void 0;var Li=class extends _n{constructor(t,e,n){super(t,e,n)}};Li.prototype.ValueTypeName="string";Li.prototype.ValueBufferType=Array;Li.prototype.DefaultInterpolation=hr;Li.prototype.InterpolantFactoryMethodLinear=void 0;Li.prototype.InterpolantFactoryMethodSmooth=void 0;var fo=class extends _n{constructor(t,e,n,s){super(t,e,n,s)}};fo.prototype.ValueTypeName="vector";var po=class{constructor(t,e,n){let s=this,r=!1,a=0,o=0,l,c=[];this.onStart=void 0,this.onLoad=t,this.onProgress=e,this.onError=n,this._abortController=null,this.itemStart=function(h){o++,r===!1&&s.onStart!==void 0&&s.onStart(h,a,o),r=!0},this.itemEnd=function(h){a++,s.onProgress!==void 0&&s.onProgress(h,a,o),a===o&&(r=!1,s.onLoad!==void 0&&s.onLoad())},this.itemError=function(h){s.onError!==void 0&&s.onError(h)},this.resolveURL=function(h){return l?l(h):h},this.setURLModifier=function(h){return l=h,this},this.addHandler=function(h,f){return c.push(h,f),this},this.removeHandler=function(h){let f=c.indexOf(h);return f!==-1&&c.splice(f,2),this},this.getHandler=function(h){for(let f=0,u=c.length;f<u;f+=2){let d=c[f],m=c[f+1];if(d.global&&(d.lastIndex=0),d.test(h))return m}return null},this.abort=function(){return this.abortController.abort(),this._abortController=null,this}}get abortController(){return this._abortController||(this._abortController=new AbortController),this._abortController}},Of=new po,mo=class{constructor(t){this.manager=t!==void 0?t:Of,this.crossOrigin="anonymous",this.withCredentials=!1,this.path="",this.resourcePath="",this.requestHeader={},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}load(){}loadAsync(t,e){let n=this;return new Promise(function(s,r){n.load(t,s,e,r)})}parse(){}setCrossOrigin(t){return this.crossOrigin=t,this}setWithCredentials(t){return this.withCredentials=t,this}setPath(t){return this.path=t,this}setResourcePath(t){return this.resourcePath=t,this}setRequestHeader(t){return this.requestHeader=t,this}abort(){return this}};mo.DEFAULT_MATERIAL_NAME="__DEFAULT";var La=new P,Na=new gn,zn=new P,Er=class extends sn{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new ge,this.projectionMatrix=new ge,this.projectionMatrixInverse=new ge,this.coordinateSystem=In,this._reversedDepth=!1}get reversedDepth(){return this._reversedDepth}copy(t,e){return super.copy(t,e),this.matrixWorldInverse.copy(t.matrixWorldInverse),this.projectionMatrix.copy(t.projectionMatrix),this.projectionMatrixInverse.copy(t.projectionMatrixInverse),this.coordinateSystem=t.coordinateSystem,this}getWorldDirection(t){return super.getWorldDirection(t).negate()}updateMatrixWorld(t){super.updateMatrixWorld(t),this.matrixWorld.decompose(La,Na,zn),zn.x===1&&zn.y===1&&zn.z===1?this.matrixWorldInverse.copy(this.matrixWorld).invert():this.matrixWorldInverse.compose(La,Na,zn.set(1,1,1)).invert()}updateWorldMatrix(t,e){super.updateWorldMatrix(t,e),this.matrixWorld.decompose(La,Na,zn),zn.x===1&&zn.y===1&&zn.z===1?this.matrixWorldInverse.copy(this.matrixWorld).invert():this.matrixWorldInverse.compose(La,Na,zn.set(1,1,1)).invert()}clone(){return new this.constructor().copy(this)}},Si=new P,$u=new Et,ju=new Et,Ye=class extends Er{constructor(t=50,e=1,n=.1,s=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=t,this.zoom=1,this.near=n,this.far=s,this.focus=10,this.aspect=e,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(t,e){return super.copy(t,e),this.fov=t.fov,this.zoom=t.zoom,this.near=t.near,this.far=t.far,this.focus=t.focus,this.aspect=t.aspect,this.view=t.view===null?null:Object.assign({},t.view),this.filmGauge=t.filmGauge,this.filmOffset=t.filmOffset,this}setFocalLength(t){let e=.5*this.getFilmHeight()/t;this.fov=Ds*2*Math.atan(e),this.updateProjectionMatrix()}getFocalLength(){let t=Math.tan(lr*.5*this.fov);return .5*this.getFilmHeight()/t}getEffectiveFOV(){return Ds*2*Math.atan(Math.tan(lr*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(t,e,n){Si.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),e.set(Si.x,Si.y).multiplyScalar(-t/Si.z),Si.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),n.set(Si.x,Si.y).multiplyScalar(-t/Si.z)}getViewSize(t,e){return this.getViewBounds(t,$u,ju),e.subVectors(ju,$u)}setViewOffset(t,e,n,s,r,a){this.aspect=t/e,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=t,this.view.fullHeight=e,this.view.offsetX=n,this.view.offsetY=s,this.view.width=r,this.view.height=a,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let t=this.near,e=t*Math.tan(lr*.5*this.fov)/this.zoom,n=2*e,s=this.aspect*n,r=-.5*s,a=this.view;if(this.view!==null&&this.view.enabled){let l=a.fullWidth,c=a.fullHeight;r+=a.offsetX*s/l,e-=a.offsetY*n/c,s*=a.width/l,n*=a.height/c}let o=this.filmOffset;o!==0&&(r+=t*o/this.getFilmWidth()),this.projectionMatrix.makePerspective(r,r+s,e,e-n,t,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(t){let e=super.toJSON(t);return e.object.fov=this.fov,e.object.zoom=this.zoom,e.object.near=this.near,e.object.far=this.far,e.object.focus=this.focus,e.object.aspect=this.aspect,this.view!==null&&(e.object.view=Object.assign({},this.view)),e.object.filmGauge=this.filmGauge,e.object.filmOffset=this.filmOffset,e}};var as=class extends Er{constructor(t=-1,e=1,n=1,s=-1,r=.1,a=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=t,this.right=e,this.top=n,this.bottom=s,this.near=r,this.far=a,this.updateProjectionMatrix()}copy(t,e){return super.copy(t,e),this.left=t.left,this.right=t.right,this.top=t.top,this.bottom=t.bottom,this.near=t.near,this.far=t.far,this.zoom=t.zoom,this.view=t.view===null?null:Object.assign({},t.view),this}setViewOffset(t,e,n,s,r,a){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=t,this.view.fullHeight=e,this.view.offsetX=n,this.view.offsetY=s,this.view.width=r,this.view.height=a,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let t=(this.right-this.left)/(2*this.zoom),e=(this.top-this.bottom)/(2*this.zoom),n=(this.right+this.left)/2,s=(this.top+this.bottom)/2,r=n-t,a=n+t,o=s+e,l=s-e;if(this.view!==null&&this.view.enabled){let c=(this.right-this.left)/this.view.fullWidth/this.zoom,h=(this.top-this.bottom)/this.view.fullHeight/this.zoom;r+=c*this.view.offsetX,a=r+c*this.view.width,o-=h*this.view.offsetY,l=o-h*this.view.height}this.projectionMatrix.makeOrthographic(r,a,o,l,this.near,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(t){let e=super.toJSON(t);return e.object.zoom=this.zoom,e.object.left=this.left,e.object.right=this.right,e.object.top=this.top,e.object.bottom=this.bottom,e.object.near=this.near,e.object.far=this.far,this.view!==null&&(e.object.view=Object.assign({},this.view)),e}};var Rs=-90,Ps=1,go=class extends sn{constructor(t,e,n){super(),this.type="CubeCamera",this.renderTarget=n,this.coordinateSystem=null,this.activeMipmapLevel=0;let s=new Ye(Rs,Ps,t,e);s.layers=this.layers,this.add(s);let r=new Ye(Rs,Ps,t,e);r.layers=this.layers,this.add(r);let a=new Ye(Rs,Ps,t,e);a.layers=this.layers,this.add(a);let o=new Ye(Rs,Ps,t,e);o.layers=this.layers,this.add(o);let l=new Ye(Rs,Ps,t,e);l.layers=this.layers,this.add(l);let c=new Ye(Rs,Ps,t,e);c.layers=this.layers,this.add(c)}updateCoordinateSystem(){let t=this.coordinateSystem,e=this.children.concat(),[n,s,r,a,o,l]=e;for(let c of e)this.remove(c);if(t===In)n.up.set(0,1,0),n.lookAt(1,0,0),s.up.set(0,1,0),s.lookAt(-1,0,0),r.up.set(0,0,-1),r.lookAt(0,1,0),a.up.set(0,0,1),a.lookAt(0,-1,0),o.up.set(0,1,0),o.lookAt(0,0,1),l.up.set(0,1,0),l.lookAt(0,0,-1);else if(t===dr)n.up.set(0,-1,0),n.lookAt(-1,0,0),s.up.set(0,-1,0),s.lookAt(1,0,0),r.up.set(0,0,1),r.lookAt(0,1,0),a.up.set(0,0,-1),a.lookAt(0,-1,0),o.up.set(0,-1,0),o.lookAt(0,0,1),l.up.set(0,-1,0),l.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+t);for(let c of e)this.add(c),c.updateMatrixWorld()}update(t,e){this.parent===null&&this.updateMatrixWorld();let{renderTarget:n,activeMipmapLevel:s}=this;this.coordinateSystem!==t.coordinateSystem&&(this.coordinateSystem=t.coordinateSystem,this.updateCoordinateSystem());let[r,a,o,l,c,h]=this.children,f=t.getRenderTarget(),u=t.getActiveCubeFace(),d=t.getActiveMipmapLevel(),m=t.xr.enabled;t.xr.enabled=!1;let _=n.texture.generateMipmaps;n.texture.generateMipmaps=!1;let g=!1;t.isWebGLRenderer===!0?g=t.state.buffers.depth.getReversed():g=t.reversedDepthBuffer,t.setRenderTarget(n,0,s),g&&t.autoClear===!1&&t.clearDepth(),t.render(e,r),t.setRenderTarget(n,1,s),g&&t.autoClear===!1&&t.clearDepth(),t.render(e,a),t.setRenderTarget(n,2,s),g&&t.autoClear===!1&&t.clearDepth(),t.render(e,o),t.setRenderTarget(n,3,s),g&&t.autoClear===!1&&t.clearDepth(),t.render(e,l),t.setRenderTarget(n,4,s),g&&t.autoClear===!1&&t.clearDepth(),t.render(e,c),n.texture.generateMipmaps=_,t.setRenderTarget(n,5,s),g&&t.autoClear===!1&&t.clearDepth(),t.render(e,h),t.setRenderTarget(f,u,d),t.xr.enabled=m,n.texture.needsPMREMUpdate=!0}},_o=class extends Ye{constructor(t=[]){super(),this.isArrayCamera=!0,this.isMultiViewCamera=!1,this.cameras=t}},Cr=class{constructor(){this._previousTime=0,this._currentTime=0,this._startTime=performance.now(),this._delta=0,this._elapsed=0,this._timescale=1,this._document=null,this._pageVisibilityHandler=null}connect(t){this._document=t,t.hidden!==void 0&&(this._pageVisibilityHandler=Mg.bind(this),t.addEventListener("visibilitychange",this._pageVisibilityHandler,!1))}disconnect(){this._pageVisibilityHandler!==null&&(this._document.removeEventListener("visibilitychange",this._pageVisibilityHandler),this._pageVisibilityHandler=null),this._document=null}getDelta(){return this._delta/1e3}getElapsed(){return this._elapsed/1e3}getTimescale(){return this._timescale}setTimescale(t){return this._timescale=t,this}reset(){return this._currentTime=performance.now()-this._startTime,this}dispose(){this.disconnect()}update(t){return this._pageVisibilityHandler!==null&&this._document.hidden===!0?this._delta=0:(this._previousTime=this._currentTime,this._currentTime=(t!==void 0?t:performance.now())-this._startTime,this._delta=(this._currentTime-this._previousTime)*this._timescale,this._elapsed+=this._delta),this}};function Mg(){this._document.hidden===!1&&this.reset()}var th="\\[\\]\\.:\\/",bg=new RegExp("["+th+"]","g"),eh="[^"+th+"]",Sg="[^"+th.replace("\\.","")+"]",wg=/((?:WC+[\/:])*)/.source.replace("WC",eh),Ag=/(WCOD+)?/.source.replace("WCOD",Sg),Tg=/(?:\.(WC+)(?:\[(.+)\])?)?/.source.replace("WC",eh),Eg=/\.(WC+)(?:\[(.+)\])?/.source.replace("WC",eh),Cg=new RegExp("^"+wg+Ag+Tg+Eg+"$"),Rg=["material","materials","bones","map"],Nc=class{constructor(t,e,n){let s=n||de.parseTrackName(e);this._targetGroup=t,this._bindings=t.subscribe_(e,s)}getValue(t,e){this.bind();let n=this._targetGroup.nCachedObjects_,s=this._bindings[n];s!==void 0&&s.getValue(t,e)}setValue(t,e){let n=this._bindings;for(let s=this._targetGroup.nCachedObjects_,r=n.length;s!==r;++s)n[s].setValue(t,e)}bind(){let t=this._bindings;for(let e=this._targetGroup.nCachedObjects_,n=t.length;e!==n;++e)t[e].bind()}unbind(){let t=this._bindings;for(let e=this._targetGroup.nCachedObjects_,n=t.length;e!==n;++e)t[e].unbind()}},de=class i{constructor(t,e,n){this.path=e,this.parsedPath=n||i.parseTrackName(e),this.node=i.findNode(t,this.parsedPath.nodeName),this.rootNode=t,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}static create(t,e,n){return t&&t.isAnimationObjectGroup?new i.Composite(t,e,n):new i(t,e,n)}static sanitizeNodeName(t){return t.replace(/\s/g,"_").replace(bg,"")}static parseTrackName(t){let e=Cg.exec(t);if(e===null)throw new Error("PropertyBinding: Cannot parse trackName: "+t);let n={nodeName:e[2],objectName:e[3],objectIndex:e[4],propertyName:e[5],propertyIndex:e[6]},s=n.nodeName&&n.nodeName.lastIndexOf(".");if(s!==void 0&&s!==-1){let r=n.nodeName.substring(s+1);Rg.indexOf(r)!==-1&&(n.nodeName=n.nodeName.substring(0,s),n.objectName=r)}if(n.propertyName===null||n.propertyName.length===0)throw new Error("PropertyBinding: can not parse propertyName from trackName: "+t);return n}static findNode(t,e){if(e===void 0||e===""||e==="."||e===-1||e===t.name||e===t.uuid)return t;if(t.skeleton){let n=t.skeleton.getBoneByName(e);if(n!==void 0)return n}if(t.children){let n=function(r){for(let a=0;a<r.length;a++){let o=r[a];if(o.name===e||o.uuid===e)return o;let l=n(o.children);if(l)return l}return null},s=n(t.children);if(s)return s}return null}_getValue_unavailable(){}_setValue_unavailable(){}_getValue_direct(t,e){t[e]=this.targetObject[this.propertyName]}_getValue_array(t,e){let n=this.resolvedProperty;for(let s=0,r=n.length;s!==r;++s)t[e++]=n[s]}_getValue_arrayElement(t,e){t[e]=this.resolvedProperty[this.propertyIndex]}_getValue_toArray(t,e){this.resolvedProperty.toArray(t,e)}_setValue_direct(t,e){this.targetObject[this.propertyName]=t[e]}_setValue_direct_setNeedsUpdate(t,e){this.targetObject[this.propertyName]=t[e],this.targetObject.needsUpdate=!0}_setValue_direct_setMatrixWorldNeedsUpdate(t,e){this.targetObject[this.propertyName]=t[e],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_array(t,e){let n=this.resolvedProperty;for(let s=0,r=n.length;s!==r;++s)n[s]=t[e++]}_setValue_array_setNeedsUpdate(t,e){let n=this.resolvedProperty;for(let s=0,r=n.length;s!==r;++s)n[s]=t[e++];this.targetObject.needsUpdate=!0}_setValue_array_setMatrixWorldNeedsUpdate(t,e){let n=this.resolvedProperty;for(let s=0,r=n.length;s!==r;++s)n[s]=t[e++];this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_arrayElement(t,e){this.resolvedProperty[this.propertyIndex]=t[e]}_setValue_arrayElement_setNeedsUpdate(t,e){this.resolvedProperty[this.propertyIndex]=t[e],this.targetObject.needsUpdate=!0}_setValue_arrayElement_setMatrixWorldNeedsUpdate(t,e){this.resolvedProperty[this.propertyIndex]=t[e],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_fromArray(t,e){this.resolvedProperty.fromArray(t,e)}_setValue_fromArray_setNeedsUpdate(t,e){this.resolvedProperty.fromArray(t,e),this.targetObject.needsUpdate=!0}_setValue_fromArray_setMatrixWorldNeedsUpdate(t,e){this.resolvedProperty.fromArray(t,e),this.targetObject.matrixWorldNeedsUpdate=!0}_getValue_unbound(t,e){this.bind(),this.getValue(t,e)}_setValue_unbound(t,e){this.bind(),this.setValue(t,e)}bind(){let t=this.node,e=this.parsedPath,n=e.objectName,s=e.propertyName,r=e.propertyIndex;if(t||(t=i.findNode(this.rootNode,e.nodeName),this.node=t),this.getValue=this._getValue_unavailable,this.setValue=this._setValue_unavailable,!t){Ct("PropertyBinding: No target node found for track: "+this.path+".");return}if(n){let c=e.objectIndex;switch(n){case"materials":if(!t.material){Pt("PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!t.material.materials){Pt("PropertyBinding: Can not bind to material.materials as node.material does not have a materials array.",this);return}t=t.material.materials;break;case"bones":if(!t.skeleton){Pt("PropertyBinding: Can not bind to bones as node does not have a skeleton.",this);return}t=t.skeleton.bones;for(let h=0;h<t.length;h++)if(t[h].name===c){c=h;break}break;case"map":if("map"in t){t=t.map;break}if(!t.material){Pt("PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!t.material.map){Pt("PropertyBinding: Can not bind to material.map as node.material does not have a map.",this);return}t=t.material.map;break;default:if(t[n]===void 0){Pt("PropertyBinding: Can not bind to objectName of node undefined.",this);return}t=t[n]}if(c!==void 0){if(t[c]===void 0){Pt("PropertyBinding: Trying to bind to objectIndex of objectName, but is undefined.",this,t);return}t=t[c]}}let a=t[s];if(a===void 0){let c=e.nodeName;Pt("PropertyBinding: Trying to update property for track: "+c+"."+s+" but it wasn't found.",t);return}let o=this.Versioning.None;this.targetObject=t,t.isMaterial===!0?o=this.Versioning.NeedsUpdate:t.isObject3D===!0&&(o=this.Versioning.MatrixWorldNeedsUpdate);let l=this.BindingType.Direct;if(r!==void 0){if(s==="morphTargetInfluences"){if(!t.geometry){Pt("PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.",this);return}if(!t.geometry.morphAttributes){Pt("PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.morphAttributes.",this);return}t.morphTargetDictionary[r]!==void 0&&(r=t.morphTargetDictionary[r])}l=this.BindingType.ArrayElement,this.resolvedProperty=a,this.propertyIndex=r}else a.fromArray!==void 0&&a.toArray!==void 0?(l=this.BindingType.HasFromToArray,this.resolvedProperty=a):Array.isArray(a)?(l=this.BindingType.EntireArray,this.resolvedProperty=a):this.propertyName=s;this.getValue=this.GetterByBindingType[l],this.setValue=this.SetterByBindingTypeAndVersioning[l][o]}unbind(){this.node=null,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}};de.Composite=Nc;de.prototype.BindingType={Direct:0,EntireArray:1,ArrayElement:2,HasFromToArray:3};de.prototype.Versioning={None:0,NeedsUpdate:1,MatrixWorldNeedsUpdate:2};de.prototype.GetterByBindingType=[de.prototype._getValue_direct,de.prototype._getValue_array,de.prototype._getValue_arrayElement,de.prototype._getValue_toArray];de.prototype.SetterByBindingTypeAndVersioning=[[de.prototype._setValue_direct,de.prototype._setValue_direct_setNeedsUpdate,de.prototype._setValue_direct_setMatrixWorldNeedsUpdate],[de.prototype._setValue_array,de.prototype._setValue_array_setNeedsUpdate,de.prototype._setValue_array_setMatrixWorldNeedsUpdate],[de.prototype._setValue_arrayElement,de.prototype._setValue_arrayElement_setNeedsUpdate,de.prototype._setValue_arrayElement_setMatrixWorldNeedsUpdate],[de.prototype._setValue_fromArray,de.prototype._setValue_fromArray_setNeedsUpdate,de.prototype._setValue_fromArray_setMatrixWorldNeedsUpdate]];var UM=new Float32Array(1);var Wn=class{constructor(t=1,e=0,n=0){this.radius=t,this.phi=e,this.theta=n}set(t,e,n){return this.radius=t,this.phi=e,this.theta=n,this}copy(t){return this.radius=t.radius,this.phi=t.phi,this.theta=t.theta,this}makeSafe(){return this.phi=Vt(this.phi,1e-6,Math.PI-1e-6),this}setFromVector3(t){return this.setFromCartesianCoords(t.x,t.y,t.z)}setFromCartesianCoords(t,e,n){return this.radius=Math.sqrt(t*t+e*e+n*n),this.radius===0?(this.theta=0,this.phi=0):(this.theta=Math.atan2(t,n),this.phi=Math.acos(Vt(e/this.radius,-1,1))),this}clone(){return new this.constructor().copy(this)}};var oh=class oh{constructor(t,e,n,s){this.elements=[1,0,0,1],t!==void 0&&this.set(t,e,n,s)}identity(){return this.set(1,0,0,1),this}fromArray(t,e=0){for(let n=0;n<4;n++)this.elements[n]=t[n+e];return this}set(t,e,n,s){let r=this.elements;return r[0]=t,r[2]=e,r[1]=n,r[3]=s,this}};oh.prototype.isMatrix2=!0;var Dc=oh;var Rr=class extends Ln{constructor(t,e=null){super(),this.object=t,this.domElement=e,this.enabled=!0,this.state=-1,this.keys={},this.mouseButtons={LEFT:null,MIDDLE:null,RIGHT:null},this.touches={ONE:null,TWO:null}}connect(t){if(t===void 0){Ct("Controls: connect() now requires an element.");return}this.domElement!==null&&this.disconnect(),this.domElement=t}disconnect(){}dispose(){}update(){}};function nh(i,t,e,n){let s=Pg(n);switch(e){case Wc:return i*t;case qc:return i*t/s.components*s.byteLength;case To:return i*t/s.components*s.byteLength;case Bi:return i*t*2/s.components*s.byteLength;case Eo:return i*t*2/s.components*s.byteLength;case Xc:return i*t*3/s.components*s.byteLength;case An:return i*t*4/s.components*s.byteLength;case Co:return i*t*4/s.components*s.byteLength;case kr:case zr:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*8;case Vr:case Gr:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*16;case Po:case Lo:return Math.max(i,16)*Math.max(t,8)/4;case Ro:case Io:return Math.max(i,8)*Math.max(t,8)/2;case No:case Do:case Uo:case Oo:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*8;case Fo:case Hr:case Bo:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*16;case ko:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*16;case zo:return Math.floor((i+4)/5)*Math.floor((t+3)/4)*16;case Vo:return Math.floor((i+4)/5)*Math.floor((t+4)/5)*16;case Go:return Math.floor((i+5)/6)*Math.floor((t+4)/5)*16;case Ho:return Math.floor((i+5)/6)*Math.floor((t+5)/6)*16;case Wo:return Math.floor((i+7)/8)*Math.floor((t+4)/5)*16;case Xo:return Math.floor((i+7)/8)*Math.floor((t+5)/6)*16;case qo:return Math.floor((i+7)/8)*Math.floor((t+7)/8)*16;case Yo:return Math.floor((i+9)/10)*Math.floor((t+4)/5)*16;case Zo:return Math.floor((i+9)/10)*Math.floor((t+5)/6)*16;case Ko:return Math.floor((i+9)/10)*Math.floor((t+7)/8)*16;case Jo:return Math.floor((i+9)/10)*Math.floor((t+9)/10)*16;case $o:return Math.floor((i+11)/12)*Math.floor((t+9)/10)*16;case jo:return Math.floor((i+11)/12)*Math.floor((t+11)/12)*16;case Qo:case tl:case el:return Math.ceil(i/4)*Math.ceil(t/4)*16;case nl:case il:return Math.ceil(i/4)*Math.ceil(t/4)*8;case Wr:case sl:return Math.ceil(i/4)*Math.ceil(t/4)*16}throw new Error(`Unable to determine texture byte length for ${e} format.`)}function Pg(i){switch(i){case vn:case zc:return{byteLength:1,components:1};case zs:case Vc:case Ze:return{byteLength:2,components:1};case wo:case Ao:return{byteLength:2,components:4};case Fn:case So:case Un:return{byteLength:4,components:1};case Gc:case Hc:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${i}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:vo}}));typeof window<"u"&&(window.__THREE__?Ct("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=vo);function ad(){let i=null,t=!1,e=null,n=null;function s(r,a){e(r,a),n=i.requestAnimationFrame(s)}return{start:function(){t!==!0&&e!==null&&i!==null&&(n=i.requestAnimationFrame(s),t=!0)},stop:function(){i!==null&&i.cancelAnimationFrame(n),t=!1},setAnimationLoop:function(r){e=r},setContext:function(r){i=r}}}function Ig(i){let t=new WeakMap;function e(o,l){let c=o.array,h=o.usage,f=c.byteLength,u=i.createBuffer();i.bindBuffer(l,u),i.bufferData(l,c,h),o.onUploadCallback();let d;if(c instanceof Float32Array)d=i.FLOAT;else if(typeof Float16Array<"u"&&c instanceof Float16Array)d=i.HALF_FLOAT;else if(c instanceof Uint16Array)o.isFloat16BufferAttribute?d=i.HALF_FLOAT:d=i.UNSIGNED_SHORT;else if(c instanceof Int16Array)d=i.SHORT;else if(c instanceof Uint32Array)d=i.UNSIGNED_INT;else if(c instanceof Int32Array)d=i.INT;else if(c instanceof Int8Array)d=i.BYTE;else if(c instanceof Uint8Array)d=i.UNSIGNED_BYTE;else if(c instanceof Uint8ClampedArray)d=i.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+c);return{buffer:u,type:d,bytesPerElement:c.BYTES_PER_ELEMENT,version:o.version,size:f}}function n(o,l,c){let h=l.array,f=l.updateRanges;if(i.bindBuffer(c,o),f.length===0)i.bufferSubData(c,0,h);else{f.sort((d,m)=>d.start-m.start);let u=0;for(let d=1;d<f.length;d++){let m=f[u],_=f[d];_.start<=m.start+m.count+1?m.count=Math.max(m.count,_.start+_.count-m.start):(++u,f[u]=_)}f.length=u+1;for(let d=0,m=f.length;d<m;d++){let _=f[d];i.bufferSubData(c,_.start*h.BYTES_PER_ELEMENT,h,_.start,_.count)}l.clearUpdateRanges()}l.onUploadCallback()}function s(o){return o.isInterleavedBufferAttribute&&(o=o.data),t.get(o)}function r(o){o.isInterleavedBufferAttribute&&(o=o.data);let l=t.get(o);l&&(i.deleteBuffer(l.buffer),t.delete(o))}function a(o,l){if(o.isInterleavedBufferAttribute&&(o=o.data),o.isGLBufferAttribute){let h=t.get(o);(!h||h.version<o.version)&&t.set(o,{buffer:o.buffer,type:o.type,bytesPerElement:o.elementSize,version:o.version});return}let c=t.get(o);if(c===void 0)t.set(o,e(o,l));else if(c.version<o.version){if(c.size!==o.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");n(c.buffer,o,l),c.version=o.version}}return{get:s,remove:r,update:a}}var Lg=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,Ng=`#ifdef USE_ALPHAHASH
	const float ALPHA_HASH_SCALE = 0.05;
	float hash2D( vec2 value ) {
		return fract( 1.0e4 * sin( 17.0 * value.x + 0.1 * value.y ) * ( 0.1 + abs( sin( 13.0 * value.y + value.x ) ) ) );
	}
	float hash3D( vec3 value ) {
		return hash2D( vec2( hash2D( value.xy ), value.z ) );
	}
	float getAlphaHashThreshold( vec3 position ) {
		float maxDeriv = max(
			length( dFdx( position.xyz ) ),
			length( dFdy( position.xyz ) )
		);
		float pixScale = 1.0 / ( ALPHA_HASH_SCALE * maxDeriv );
		vec2 pixScales = vec2(
			exp2( floor( log2( pixScale ) ) ),
			exp2( ceil( log2( pixScale ) ) )
		);
		vec2 alpha = vec2(
			hash3D( floor( pixScales.x * position.xyz ) ),
			hash3D( floor( pixScales.y * position.xyz ) )
		);
		float lerpFactor = fract( log2( pixScale ) );
		float x = ( 1.0 - lerpFactor ) * alpha.x + lerpFactor * alpha.y;
		float a = min( lerpFactor, 1.0 - lerpFactor );
		vec3 cases = vec3(
			x * x / ( 2.0 * a * ( 1.0 - a ) ),
			( x - 0.5 * a ) / ( 1.0 - a ),
			1.0 - ( ( 1.0 - x ) * ( 1.0 - x ) / ( 2.0 * a * ( 1.0 - a ) ) )
		);
		float threshold = ( x < ( 1.0 - a ) )
			? ( ( x < a ) ? cases.x : cases.y )
			: cases.z;
		return clamp( threshold , 1.0e-6, 1.0 );
	}
#endif`,Dg=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,Fg=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,Ug=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,Og=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,Bg=`#ifdef USE_AOMAP
	float ambientOcclusion = ( texture2D( aoMap, vAoMapUv ).r - 1.0 ) * aoMapIntensity + 1.0;
	reflectedLight.indirectDiffuse *= ambientOcclusion;
	#if defined( USE_CLEARCOAT ) 
		clearcoatSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_SHEEN ) 
		sheenSpecularIndirect *= ambientOcclusion;
	#endif
	#if defined( USE_ENVMAP ) && defined( STANDARD )
		float dotNV = saturate( dot( geometryNormal, geometryViewDir ) );
		reflectedLight.indirectSpecular *= computeSpecularOcclusion( dotNV, ambientOcclusion, material.roughness );
	#endif
#endif`,kg=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,zg=`#ifdef USE_BATCHING
	#if ! defined( GL_ANGLE_multi_draw )
	#define gl_DrawID _gl_DrawID
	uniform int _gl_DrawID;
	#endif
	uniform highp sampler2D batchingTexture;
	uniform highp usampler2D batchingIdTexture;
	mat4 getBatchingMatrix( const in float i ) {
		int size = textureSize( batchingTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( batchingTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( batchingTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( batchingTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( batchingTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
	float getIndirectIndex( const in int i ) {
		int size = textureSize( batchingIdTexture, 0 ).x;
		int x = i % size;
		int y = i / size;
		return float( texelFetch( batchingIdTexture, ivec2( x, y ), 0 ).r );
	}
#endif
#ifdef USE_BATCHING_COLOR
	uniform sampler2D batchingColorTexture;
	vec4 getBatchingColor( const in float i ) {
		int size = textureSize( batchingColorTexture, 0 ).x;
		int j = int( i );
		int x = j % size;
		int y = j / size;
		return texelFetch( batchingColorTexture, ivec2( x, y ), 0 );
	}
#endif`,Vg=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,Gg=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,Hg=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,Wg=`float G_BlinnPhong_Implicit( ) {
	return 0.25;
}
float D_BlinnPhong( const in float shininess, const in float dotNH ) {
	return RECIPROCAL_PI * ( shininess * 0.5 + 1.0 ) * pow( dotNH, shininess );
}
vec3 BRDF_BlinnPhong( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in vec3 specularColor, const in float shininess ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( specularColor, 1.0, dotVH );
	float G = G_BlinnPhong_Implicit( );
	float D = D_BlinnPhong( shininess, dotNH );
	return F * ( G * D );
} // validated`,Xg=`#ifdef USE_IRIDESCENCE
	const mat3 XYZ_TO_REC709 = mat3(
		 3.2404542, -0.9692660,  0.0556434,
		-1.5371385,  1.8760108, -0.2040259,
		-0.4985314,  0.0415560,  1.0572252
	);
	vec3 Fresnel0ToIor( vec3 fresnel0 ) {
		vec3 sqrtF0 = sqrt( fresnel0 );
		return ( vec3( 1.0 ) + sqrtF0 ) / ( vec3( 1.0 ) - sqrtF0 );
	}
	vec3 IorToFresnel0( vec3 transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - vec3( incidentIor ) ) / ( transmittedIor + vec3( incidentIor ) ) );
	}
	float IorToFresnel0( float transmittedIor, float incidentIor ) {
		return pow2( ( transmittedIor - incidentIor ) / ( transmittedIor + incidentIor ));
	}
	vec3 evalSensitivity( float OPD, vec3 shift ) {
		float phase = 2.0 * PI * OPD * 1.0e-9;
		vec3 val = vec3( 5.4856e-13, 4.4201e-13, 5.2481e-13 );
		vec3 pos = vec3( 1.6810e+06, 1.7953e+06, 2.2084e+06 );
		vec3 var = vec3( 4.3278e+09, 9.3046e+09, 6.6121e+09 );
		vec3 xyz = val * sqrt( 2.0 * PI * var ) * cos( pos * phase + shift ) * exp( - pow2( phase ) * var );
		xyz.x += 9.7470e-14 * sqrt( 2.0 * PI * 4.5282e+09 ) * cos( 2.2399e+06 * phase + shift[ 0 ] ) * exp( - 4.5282e+09 * pow2( phase ) );
		xyz /= 1.0685e-7;
		vec3 rgb = XYZ_TO_REC709 * xyz;
		return rgb;
	}
	vec3 evalIridescence( float outsideIOR, float eta2, float cosTheta1, float thinFilmThickness, vec3 baseF0 ) {
		vec3 I;
		float iridescenceIOR = mix( outsideIOR, eta2, smoothstep( 0.0, 0.03, thinFilmThickness ) );
		float sinTheta2Sq = pow2( outsideIOR / iridescenceIOR ) * ( 1.0 - pow2( cosTheta1 ) );
		float cosTheta2Sq = 1.0 - sinTheta2Sq;
		if ( cosTheta2Sq < 0.0 ) {
			return vec3( 1.0 );
		}
		float cosTheta2 = sqrt( cosTheta2Sq );
		float R0 = IorToFresnel0( iridescenceIOR, outsideIOR );
		float R12 = F_Schlick( R0, 1.0, cosTheta1 );
		float T121 = 1.0 - R12;
		float phi12 = 0.0;
		if ( iridescenceIOR < outsideIOR ) phi12 = PI;
		float phi21 = PI - phi12;
		vec3 baseIOR = Fresnel0ToIor( clamp( baseF0, 0.0, 0.9999 ) );		vec3 R1 = IorToFresnel0( baseIOR, iridescenceIOR );
		vec3 R23 = F_Schlick( R1, 1.0, cosTheta2 );
		vec3 phi23 = vec3( 0.0 );
		if ( baseIOR[ 0 ] < iridescenceIOR ) phi23[ 0 ] = PI;
		if ( baseIOR[ 1 ] < iridescenceIOR ) phi23[ 1 ] = PI;
		if ( baseIOR[ 2 ] < iridescenceIOR ) phi23[ 2 ] = PI;
		float OPD = 2.0 * iridescenceIOR * thinFilmThickness * cosTheta2;
		vec3 phi = vec3( phi21 ) + phi23;
		vec3 R123 = clamp( R12 * R23, 1e-5, 0.9999 );
		vec3 r123 = sqrt( R123 );
		vec3 Rs = pow2( T121 ) * R23 / ( vec3( 1.0 ) - R123 );
		vec3 C0 = R12 + Rs;
		I = C0;
		vec3 Cm = Rs - T121;
		for ( int m = 1; m <= 2; ++ m ) {
			Cm *= r123;
			vec3 Sm = 2.0 * evalSensitivity( float( m ) * OPD, float( m ) * phi );
			I += Cm * Sm;
		}
		return max( I, vec3( 0.0 ) );
	}
#endif`,qg=`#ifdef USE_BUMPMAP
	uniform sampler2D bumpMap;
	uniform float bumpScale;
	vec2 dHdxy_fwd() {
		vec2 dSTdx = dFdx( vBumpMapUv );
		vec2 dSTdy = dFdy( vBumpMapUv );
		float Hll = bumpScale * texture2D( bumpMap, vBumpMapUv ).x;
		float dBx = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdx ).x - Hll;
		float dBy = bumpScale * texture2D( bumpMap, vBumpMapUv + dSTdy ).x - Hll;
		return vec2( dBx, dBy );
	}
	vec3 perturbNormalArb( vec3 surf_pos, vec3 surf_norm, vec2 dHdxy, float faceDirection ) {
		vec3 vSigmaX = normalize( dFdx( surf_pos.xyz ) );
		vec3 vSigmaY = normalize( dFdy( surf_pos.xyz ) );
		vec3 vN = surf_norm;
		vec3 R1 = cross( vSigmaY, vN );
		vec3 R2 = cross( vN, vSigmaX );
		float fDet = dot( vSigmaX, R1 ) * faceDirection;
		vec3 vGrad = sign( fDet ) * ( dHdxy.x * R1 + dHdxy.y * R2 );
		return normalize( abs( fDet ) * surf_norm - vGrad );
	}
#endif`,Yg=`#if NUM_CLIPPING_PLANES > 0
	vec4 plane;
	#ifdef ALPHA_TO_COVERAGE
		float distanceToPlane, distanceGradient;
		float clipOpacity = 1.0;
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
			distanceGradient = fwidth( distanceToPlane ) / 2.0;
			clipOpacity *= smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			if ( clipOpacity == 0.0 ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			float unionClipOpacity = 1.0;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				distanceToPlane = - dot( vClipPosition, plane.xyz ) + plane.w;
				distanceGradient = fwidth( distanceToPlane ) / 2.0;
				unionClipOpacity *= 1.0 - smoothstep( - distanceGradient, distanceGradient, distanceToPlane );
			}
			#pragma unroll_loop_end
			clipOpacity *= 1.0 - unionClipOpacity;
		#endif
		diffuseColor.a *= clipOpacity;
		if ( diffuseColor.a == 0.0 ) discard;
	#else
		#pragma unroll_loop_start
		for ( int i = 0; i < UNION_CLIPPING_PLANES; i ++ ) {
			plane = clippingPlanes[ i ];
			if ( dot( vClipPosition, plane.xyz ) > plane.w ) discard;
		}
		#pragma unroll_loop_end
		#if UNION_CLIPPING_PLANES < NUM_CLIPPING_PLANES
			bool clipped = true;
			#pragma unroll_loop_start
			for ( int i = UNION_CLIPPING_PLANES; i < NUM_CLIPPING_PLANES; i ++ ) {
				plane = clippingPlanes[ i ];
				clipped = ( dot( vClipPosition, plane.xyz ) > plane.w ) && clipped;
			}
			#pragma unroll_loop_end
			if ( clipped ) discard;
		#endif
	#endif
#endif`,Zg=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,Kg=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,Jg=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,$g=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#endif`,jg=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#endif`,Qg=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec4 vColor;
#endif`,t0=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	vColor = vec4( 1.0 );
#endif
#ifdef USE_COLOR_ALPHA
	vColor *= color;
#elif defined( USE_COLOR )
	vColor.rgb *= color;
#endif
#ifdef USE_INSTANCING_COLOR
	vColor.rgb *= instanceColor.rgb;
#endif
#ifdef USE_BATCHING_COLOR
	vColor *= getBatchingColor( getIndirectIndex( gl_DrawID ) );
#endif`,e0=`#define PI 3.141592653589793
#define PI2 6.283185307179586
#define PI_HALF 1.5707963267948966
#define RECIPROCAL_PI 0.3183098861837907
#define RECIPROCAL_PI2 0.15915494309189535
#define EPSILON 1e-6
#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
#define whiteComplement( a ) ( 1.0 - saturate( a ) )
float pow2( const in float x ) { return x*x; }
vec3 pow2( const in vec3 x ) { return x*x; }
float pow3( const in float x ) { return x*x*x; }
float pow4( const in float x ) { float x2 = x*x; return x2*x2; }
float max3( const in vec3 v ) { return max( max( v.x, v.y ), v.z ); }
float average( const in vec3 v ) { return dot( v, vec3( 0.3333333 ) ); }
highp float rand( const in vec2 uv ) {
	const highp float a = 12.9898, b = 78.233, c = 43758.5453;
	highp float dt = dot( uv.xy, vec2( a,b ) ), sn = mod( dt, PI );
	return fract( sin( sn ) * c );
}
#ifdef HIGH_PRECISION
	float precisionSafeLength( vec3 v ) { return length( v ); }
#else
	float precisionSafeLength( vec3 v ) {
		float maxComponent = max3( abs( v ) );
		return length( v / maxComponent ) * maxComponent;
	}
#endif
struct IncidentLight {
	vec3 color;
	vec3 direction;
	bool visible;
};
struct ReflectedLight {
	vec3 directDiffuse;
	vec3 directSpecular;
	vec3 indirectDiffuse;
	vec3 indirectSpecular;
};
#ifdef USE_ALPHAHASH
	varying vec3 vPosition;
#endif
vec3 transformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );
}
vec3 inverseTransformDirection( in vec3 dir, in mat4 matrix ) {
	return normalize( ( vec4( dir, 0.0 ) * matrix ).xyz );
}
bool isPerspectiveMatrix( mat4 m ) {
	return m[ 2 ][ 3 ] == - 1.0;
}
vec2 equirectUv( in vec3 dir ) {
	float u = atan( dir.z, dir.x ) * RECIPROCAL_PI2 + 0.5;
	float v = asin( clamp( dir.y, - 1.0, 1.0 ) ) * RECIPROCAL_PI + 0.5;
	return vec2( u, v );
}
vec3 BRDF_Lambert( const in vec3 diffuseColor ) {
	return RECIPROCAL_PI * diffuseColor;
}
vec3 F_Schlick( const in vec3 f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
}
float F_Schlick( const in float f0, const in float f90, const in float dotVH ) {
	float fresnel = exp2( ( - 5.55473 * dotVH - 6.98316 ) * dotVH );
	return f0 * ( 1.0 - fresnel ) + ( f90 * fresnel );
} // validated`,n0=`#ifdef ENVMAP_TYPE_CUBE_UV
	#define cubeUV_minMipLevel 4.0
	#define cubeUV_minTileSize 16.0
	float getFace( vec3 direction ) {
		vec3 absDirection = abs( direction );
		float face = - 1.0;
		if ( absDirection.x > absDirection.z ) {
			if ( absDirection.x > absDirection.y )
				face = direction.x > 0.0 ? 0.0 : 3.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		} else {
			if ( absDirection.z > absDirection.y )
				face = direction.z > 0.0 ? 2.0 : 5.0;
			else
				face = direction.y > 0.0 ? 1.0 : 4.0;
		}
		return face;
	}
	vec2 getUV( vec3 direction, float face ) {
		vec2 uv;
		if ( face == 0.0 ) {
			uv = vec2( direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 1.0 ) {
			uv = vec2( - direction.x, - direction.z ) / abs( direction.y );
		} else if ( face == 2.0 ) {
			uv = vec2( - direction.x, direction.y ) / abs( direction.z );
		} else if ( face == 3.0 ) {
			uv = vec2( - direction.z, direction.y ) / abs( direction.x );
		} else if ( face == 4.0 ) {
			uv = vec2( - direction.x, direction.z ) / abs( direction.y );
		} else {
			uv = vec2( direction.x, direction.y ) / abs( direction.z );
		}
		return 0.5 * ( uv + 1.0 );
	}
	vec3 bilinearCubeUV( sampler2D envMap, vec3 direction, float mipInt ) {
		float face = getFace( direction );
		float filterInt = max( cubeUV_minMipLevel - mipInt, 0.0 );
		mipInt = max( mipInt, cubeUV_minMipLevel );
		float faceSize = exp2( mipInt );
		highp vec2 uv = getUV( direction, face ) * ( faceSize - 2.0 ) + 1.0;
		if ( face > 2.0 ) {
			uv.y += faceSize;
			face -= 3.0;
		}
		uv.x += face * faceSize;
		uv.x += filterInt * 3.0 * cubeUV_minTileSize;
		uv.y += 4.0 * ( exp2( CUBEUV_MAX_MIP ) - faceSize );
		uv.x *= CUBEUV_TEXEL_WIDTH;
		uv.y *= CUBEUV_TEXEL_HEIGHT;
		#ifdef texture2DGradEXT
			return texture2DGradEXT( envMap, uv, vec2( 0.0 ), vec2( 0.0 ) ).rgb;
		#else
			return texture2D( envMap, uv ).rgb;
		#endif
	}
	#define cubeUV_r0 1.0
	#define cubeUV_m0 - 2.0
	#define cubeUV_r1 0.8
	#define cubeUV_m1 - 1.0
	#define cubeUV_r4 0.4
	#define cubeUV_m4 2.0
	#define cubeUV_r5 0.305
	#define cubeUV_m5 3.0
	#define cubeUV_r6 0.21
	#define cubeUV_m6 4.0
	float roughnessToMip( float roughness ) {
		float mip = 0.0;
		if ( roughness >= cubeUV_r1 ) {
			mip = ( cubeUV_r0 - roughness ) * ( cubeUV_m1 - cubeUV_m0 ) / ( cubeUV_r0 - cubeUV_r1 ) + cubeUV_m0;
		} else if ( roughness >= cubeUV_r4 ) {
			mip = ( cubeUV_r1 - roughness ) * ( cubeUV_m4 - cubeUV_m1 ) / ( cubeUV_r1 - cubeUV_r4 ) + cubeUV_m1;
		} else if ( roughness >= cubeUV_r5 ) {
			mip = ( cubeUV_r4 - roughness ) * ( cubeUV_m5 - cubeUV_m4 ) / ( cubeUV_r4 - cubeUV_r5 ) + cubeUV_m4;
		} else if ( roughness >= cubeUV_r6 ) {
			mip = ( cubeUV_r5 - roughness ) * ( cubeUV_m6 - cubeUV_m5 ) / ( cubeUV_r5 - cubeUV_r6 ) + cubeUV_m5;
		} else {
			mip = - 2.0 * log2( 1.16 * roughness );		}
		return mip;
	}
	vec4 textureCubeUV( sampler2D envMap, vec3 sampleDir, float roughness ) {
		float mip = clamp( roughnessToMip( roughness ), cubeUV_m0, CUBEUV_MAX_MIP );
		float mipF = fract( mip );
		float mipInt = floor( mip );
		vec3 color0 = bilinearCubeUV( envMap, sampleDir, mipInt );
		if ( mipF == 0.0 ) {
			return vec4( color0, 1.0 );
		} else {
			vec3 color1 = bilinearCubeUV( envMap, sampleDir, mipInt + 1.0 );
			return vec4( mix( color0, color1, mipF ), 1.0 );
		}
	}
#endif`,i0=`vec3 transformedNormal = objectNormal;
#ifdef USE_TANGENT
	vec3 transformedTangent = objectTangent;
#endif
#ifdef USE_BATCHING
	mat3 bm = mat3( batchingMatrix );
	transformedNormal /= vec3( dot( bm[ 0 ], bm[ 0 ] ), dot( bm[ 1 ], bm[ 1 ] ), dot( bm[ 2 ], bm[ 2 ] ) );
	transformedNormal = bm * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = bm * transformedTangent;
	#endif
#endif
#ifdef USE_INSTANCING
	mat3 im = mat3( instanceMatrix );
	transformedNormal /= vec3( dot( im[ 0 ], im[ 0 ] ), dot( im[ 1 ], im[ 1 ] ), dot( im[ 2 ], im[ 2 ] ) );
	transformedNormal = im * transformedNormal;
	#ifdef USE_TANGENT
		transformedTangent = im * transformedTangent;
	#endif
#endif
transformedNormal = normalMatrix * transformedNormal;
#ifdef FLIP_SIDED
	transformedNormal = - transformedNormal;
#endif
#ifdef USE_TANGENT
	transformedTangent = ( modelViewMatrix * vec4( transformedTangent, 0.0 ) ).xyz;
	#ifdef FLIP_SIDED
		transformedTangent = - transformedTangent;
	#endif
#endif`,s0=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,r0=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,a0=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,o0=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,l0="gl_FragColor = linearToOutputTexel( gl_FragColor );",c0=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,h0=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vec3 cameraToFrag;
		if ( isOrthographic ) {
			cameraToFrag = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToFrag = normalize( vWorldPosition - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vec3 reflectVec = reflect( cameraToFrag, worldNormal );
		#else
			vec3 reflectVec = refract( cameraToFrag, worldNormal, refractionRatio );
		#endif
	#else
		vec3 reflectVec = vReflect;
	#endif
	#ifdef ENVMAP_TYPE_CUBE
		vec4 envColor = textureCube( envMap, envMapRotation * reflectVec );
		#ifdef ENVMAP_BLENDING_MULTIPLY
			outgoingLight = mix( outgoingLight, outgoingLight * envColor.xyz, specularStrength * reflectivity );
		#elif defined( ENVMAP_BLENDING_MIX )
			outgoingLight = mix( outgoingLight, envColor.xyz, specularStrength * reflectivity );
		#elif defined( ENVMAP_BLENDING_ADD )
			outgoingLight += envColor.xyz * specularStrength * reflectivity;
		#endif
	#endif
#endif`,u0=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
#endif`,f0=`#ifdef USE_ENVMAP
	uniform float reflectivity;
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		varying vec3 vWorldPosition;
		uniform float refractionRatio;
	#else
		varying vec3 vReflect;
	#endif
#endif`,d0=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,p0=`#ifdef USE_ENVMAP
	#ifdef ENV_WORLDPOS
		vWorldPosition = worldPosition.xyz;
	#else
		vec3 cameraToVertex;
		if ( isOrthographic ) {
			cameraToVertex = normalize( vec3( - viewMatrix[ 0 ][ 2 ], - viewMatrix[ 1 ][ 2 ], - viewMatrix[ 2 ][ 2 ] ) );
		} else {
			cameraToVertex = normalize( worldPosition.xyz - cameraPosition );
		}
		vec3 worldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
		#ifdef ENVMAP_MODE_REFLECTION
			vReflect = reflect( cameraToVertex, worldNormal );
		#else
			vReflect = refract( cameraToVertex, worldNormal, refractionRatio );
		#endif
	#endif
#endif`,m0=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,g0=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,_0=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,x0=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,v0=`#ifdef USE_GRADIENTMAP
	uniform sampler2D gradientMap;
#endif
vec3 getGradientIrradiance( vec3 normal, vec3 lightDirection ) {
	float dotNL = dot( normal, lightDirection );
	vec2 coord = vec2( dotNL * 0.5 + 0.5, 0.0 );
	#ifdef USE_GRADIENTMAP
		return vec3( texture2D( gradientMap, coord ).r );
	#else
		vec2 fw = fwidth( coord ) * 0.5;
		return mix( vec3( 0.7 ), vec3( 1.0 ), smoothstep( 0.7 - fw.x, 0.7 + fw.x, coord.x ) );
	#endif
}`,y0=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,M0=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,b0=`varying vec3 vViewPosition;
struct LambertMaterial {
	vec3 diffuseColor;
	float specularStrength;
};
void RE_Direct_Lambert( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Lambert( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in LambertMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Lambert
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,S0=`uniform bool receiveShadow;
uniform vec3 ambientLightColor;
#if defined( USE_LIGHT_PROBES )
	uniform vec3 lightProbe[ 9 ];
#endif
vec3 shGetIrradianceAt( in vec3 normal, in vec3 shCoefficients[ 9 ] ) {
	float x = normal.x, y = normal.y, z = normal.z;
	vec3 result = shCoefficients[ 0 ] * 0.886227;
	result += shCoefficients[ 1 ] * 2.0 * 0.511664 * y;
	result += shCoefficients[ 2 ] * 2.0 * 0.511664 * z;
	result += shCoefficients[ 3 ] * 2.0 * 0.511664 * x;
	result += shCoefficients[ 4 ] * 2.0 * 0.429043 * x * y;
	result += shCoefficients[ 5 ] * 2.0 * 0.429043 * y * z;
	result += shCoefficients[ 6 ] * ( 0.743125 * z * z - 0.247708 );
	result += shCoefficients[ 7 ] * 2.0 * 0.429043 * x * z;
	result += shCoefficients[ 8 ] * 0.429043 * ( x * x - y * y );
	return result;
}
vec3 getLightProbeIrradiance( const in vec3 lightProbe[ 9 ], const in vec3 normal ) {
	vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
	vec3 irradiance = shGetIrradianceAt( worldNormal, lightProbe );
	return irradiance;
}
vec3 getAmbientLightIrradiance( const in vec3 ambientLightColor ) {
	vec3 irradiance = ambientLightColor;
	return irradiance;
}
float getDistanceAttenuation( const in float lightDistance, const in float cutoffDistance, const in float decayExponent ) {
	float distanceFalloff = 1.0 / max( pow( lightDistance, decayExponent ), 0.01 );
	if ( cutoffDistance > 0.0 ) {
		distanceFalloff *= pow2( saturate( 1.0 - pow4( lightDistance / cutoffDistance ) ) );
	}
	return distanceFalloff;
}
float getSpotAttenuation( const in float coneCosine, const in float penumbraCosine, const in float angleCosine ) {
	return smoothstep( coneCosine, penumbraCosine, angleCosine );
}
#if NUM_DIR_LIGHTS > 0
	struct DirectionalLight {
		vec3 direction;
		vec3 color;
	};
	uniform DirectionalLight directionalLights[ NUM_DIR_LIGHTS ];
	void getDirectionalLightInfo( const in DirectionalLight directionalLight, out IncidentLight light ) {
		light.color = directionalLight.color;
		light.direction = directionalLight.direction;
		light.visible = true;
	}
#endif
#if NUM_POINT_LIGHTS > 0
	struct PointLight {
		vec3 position;
		vec3 color;
		float distance;
		float decay;
	};
	uniform PointLight pointLights[ NUM_POINT_LIGHTS ];
	void getPointLightInfo( const in PointLight pointLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = pointLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float lightDistance = length( lVector );
		light.color = pointLight.color;
		light.color *= getDistanceAttenuation( lightDistance, pointLight.distance, pointLight.decay );
		light.visible = ( light.color != vec3( 0.0 ) );
	}
#endif
#if NUM_SPOT_LIGHTS > 0
	struct SpotLight {
		vec3 position;
		vec3 direction;
		vec3 color;
		float distance;
		float decay;
		float coneCos;
		float penumbraCos;
	};
	uniform SpotLight spotLights[ NUM_SPOT_LIGHTS ];
	void getSpotLightInfo( const in SpotLight spotLight, const in vec3 geometryPosition, out IncidentLight light ) {
		vec3 lVector = spotLight.position - geometryPosition;
		light.direction = normalize( lVector );
		float angleCos = dot( light.direction, spotLight.direction );
		float spotAttenuation = getSpotAttenuation( spotLight.coneCos, spotLight.penumbraCos, angleCos );
		if ( spotAttenuation > 0.0 ) {
			float lightDistance = length( lVector );
			light.color = spotLight.color * spotAttenuation;
			light.color *= getDistanceAttenuation( lightDistance, spotLight.distance, spotLight.decay );
			light.visible = ( light.color != vec3( 0.0 ) );
		} else {
			light.color = vec3( 0.0 );
			light.visible = false;
		}
	}
#endif
#if NUM_RECT_AREA_LIGHTS > 0
	struct RectAreaLight {
		vec3 color;
		vec3 position;
		vec3 halfWidth;
		vec3 halfHeight;
	};
	uniform sampler2D ltc_1;	uniform sampler2D ltc_2;
	uniform RectAreaLight rectAreaLights[ NUM_RECT_AREA_LIGHTS ];
#endif
#if NUM_HEMI_LIGHTS > 0
	struct HemisphereLight {
		vec3 direction;
		vec3 skyColor;
		vec3 groundColor;
	};
	uniform HemisphereLight hemisphereLights[ NUM_HEMI_LIGHTS ];
	vec3 getHemisphereLightIrradiance( const in HemisphereLight hemiLight, const in vec3 normal ) {
		float dotNL = dot( normal, hemiLight.direction );
		float hemiDiffuseWeight = 0.5 * dotNL + 0.5;
		vec3 irradiance = mix( hemiLight.groundColor, hemiLight.skyColor, hemiDiffuseWeight );
		return irradiance;
	}
#endif
#include <lightprobes_pars_fragment>`,w0=`#ifdef USE_ENVMAP
	vec3 getIBLIrradiance( const in vec3 normal ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 worldNormal = inverseTransformDirection( normal, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * worldNormal, 1.0 );
			return PI * envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	vec3 getIBLRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness ) {
		#ifdef ENVMAP_TYPE_CUBE_UV
			vec3 reflectVec = reflect( - viewDir, normal );
			reflectVec = normalize( mix( reflectVec, normal, pow4( roughness ) ) );
			reflectVec = inverseTransformDirection( reflectVec, viewMatrix );
			vec4 envMapColor = textureCubeUV( envMap, envMapRotation * reflectVec, roughness );
			return envMapColor.rgb * envMapIntensity;
		#else
			return vec3( 0.0 );
		#endif
	}
	#ifdef USE_ANISOTROPY
		vec3 getIBLAnisotropyRadiance( const in vec3 viewDir, const in vec3 normal, const in float roughness, const in vec3 bitangent, const in float anisotropy ) {
			#ifdef ENVMAP_TYPE_CUBE_UV
				vec3 bentNormal = cross( bitangent, viewDir );
				bentNormal = normalize( cross( bentNormal, bitangent ) );
				bentNormal = normalize( mix( bentNormal, normal, pow2( pow2( 1.0 - anisotropy * ( 1.0 - roughness ) ) ) ) );
				return getIBLRadiance( viewDir, bentNormal, roughness );
			#else
				return vec3( 0.0 );
			#endif
		}
	#endif
#endif`,A0=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,T0=`varying vec3 vViewPosition;
struct ToonMaterial {
	vec3 diffuseColor;
};
void RE_Direct_Toon( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 irradiance = getGradientIrradiance( geometryNormal, directLight.direction ) * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
void RE_IndirectDiffuse_Toon( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in ToonMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_Toon
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,E0=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,C0=`varying vec3 vViewPosition;
struct BlinnPhongMaterial {
	vec3 diffuseColor;
	vec3 specularColor;
	float specularShininess;
	float specularStrength;
};
void RE_Direct_BlinnPhong( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
	reflectedLight.directSpecular += irradiance * BRDF_BlinnPhong( directLight.direction, geometryViewDir, geometryNormal, material.specularColor, material.specularShininess ) * material.specularStrength;
}
void RE_IndirectDiffuse_BlinnPhong( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in BlinnPhongMaterial material, inout ReflectedLight reflectedLight ) {
	reflectedLight.indirectDiffuse += irradiance * BRDF_Lambert( material.diffuseColor );
}
#define RE_Direct				RE_Direct_BlinnPhong
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,R0=`PhysicalMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.diffuseContribution = diffuseColor.rgb * ( 1.0 - metalnessFactor );
material.metalness = metalnessFactor;
vec3 dxy = max( abs( dFdx( nonPerturbedNormal ) ), abs( dFdy( nonPerturbedNormal ) ) );
float geometryRoughness = max( max( dxy.x, dxy.y ), dxy.z );
material.roughness = max( roughnessFactor, 0.0525 );material.roughness += geometryRoughness;
material.roughness = min( material.roughness, 1.0 );
#ifdef IOR
	material.ior = ior;
	#ifdef USE_SPECULAR
		float specularIntensityFactor = specularIntensity;
		vec3 specularColorFactor = specularColor;
		#ifdef USE_SPECULAR_COLORMAP
			specularColorFactor *= texture2D( specularColorMap, vSpecularColorMapUv ).rgb;
		#endif
		#ifdef USE_SPECULAR_INTENSITYMAP
			specularIntensityFactor *= texture2D( specularIntensityMap, vSpecularIntensityMapUv ).a;
		#endif
		material.specularF90 = mix( specularIntensityFactor, 1.0, metalnessFactor );
	#else
		float specularIntensityFactor = 1.0;
		vec3 specularColorFactor = vec3( 1.0 );
		material.specularF90 = 1.0;
	#endif
	material.specularColor = min( pow2( ( material.ior - 1.0 ) / ( material.ior + 1.0 ) ) * specularColorFactor, vec3( 1.0 ) ) * specularIntensityFactor;
	material.specularColorBlended = mix( material.specularColor, diffuseColor.rgb, metalnessFactor );
#else
	material.specularColor = vec3( 0.04 );
	material.specularColorBlended = mix( material.specularColor, diffuseColor.rgb, metalnessFactor );
	material.specularF90 = 1.0;
#endif
#ifdef USE_CLEARCOAT
	material.clearcoat = clearcoat;
	material.clearcoatRoughness = clearcoatRoughness;
	material.clearcoatF0 = vec3( 0.04 );
	material.clearcoatF90 = 1.0;
	#ifdef USE_CLEARCOATMAP
		material.clearcoat *= texture2D( clearcoatMap, vClearcoatMapUv ).x;
	#endif
	#ifdef USE_CLEARCOAT_ROUGHNESSMAP
		material.clearcoatRoughness *= texture2D( clearcoatRoughnessMap, vClearcoatRoughnessMapUv ).y;
	#endif
	material.clearcoat = saturate( material.clearcoat );	material.clearcoatRoughness = max( material.clearcoatRoughness, 0.0525 );
	material.clearcoatRoughness += geometryRoughness;
	material.clearcoatRoughness = min( material.clearcoatRoughness, 1.0 );
#endif
#ifdef USE_DISPERSION
	material.dispersion = dispersion;
#endif
#ifdef USE_IRIDESCENCE
	material.iridescence = iridescence;
	material.iridescenceIOR = iridescenceIOR;
	#ifdef USE_IRIDESCENCEMAP
		material.iridescence *= texture2D( iridescenceMap, vIridescenceMapUv ).r;
	#endif
	#ifdef USE_IRIDESCENCE_THICKNESSMAP
		material.iridescenceThickness = (iridescenceThicknessMaximum - iridescenceThicknessMinimum) * texture2D( iridescenceThicknessMap, vIridescenceThicknessMapUv ).g + iridescenceThicknessMinimum;
	#else
		material.iridescenceThickness = iridescenceThicknessMaximum;
	#endif
#endif
#ifdef USE_SHEEN
	material.sheenColor = sheenColor;
	#ifdef USE_SHEEN_COLORMAP
		material.sheenColor *= texture2D( sheenColorMap, vSheenColorMapUv ).rgb;
	#endif
	material.sheenRoughness = clamp( sheenRoughness, 0.0001, 1.0 );
	#ifdef USE_SHEEN_ROUGHNESSMAP
		material.sheenRoughness *= texture2D( sheenRoughnessMap, vSheenRoughnessMapUv ).a;
	#endif
#endif
#ifdef USE_ANISOTROPY
	#ifdef USE_ANISOTROPYMAP
		mat2 anisotropyMat = mat2( anisotropyVector.x, anisotropyVector.y, - anisotropyVector.y, anisotropyVector.x );
		vec3 anisotropyPolar = texture2D( anisotropyMap, vAnisotropyMapUv ).rgb;
		vec2 anisotropyV = anisotropyMat * normalize( 2.0 * anisotropyPolar.rg - vec2( 1.0 ) ) * anisotropyPolar.b;
	#else
		vec2 anisotropyV = anisotropyVector;
	#endif
	material.anisotropy = length( anisotropyV );
	if( material.anisotropy == 0.0 ) {
		anisotropyV = vec2( 1.0, 0.0 );
	} else {
		anisotropyV /= material.anisotropy;
		material.anisotropy = saturate( material.anisotropy );
	}
	material.alphaT = mix( pow2( material.roughness ), 1.0, pow2( material.anisotropy ) );
	material.anisotropyT = tbn[ 0 ] * anisotropyV.x + tbn[ 1 ] * anisotropyV.y;
	material.anisotropyB = tbn[ 1 ] * anisotropyV.x - tbn[ 0 ] * anisotropyV.y;
#endif`,P0=`uniform sampler2D dfgLUT;
struct PhysicalMaterial {
	vec3 diffuseColor;
	vec3 diffuseContribution;
	vec3 specularColor;
	vec3 specularColorBlended;
	float roughness;
	float metalness;
	float specularF90;
	float dispersion;
	#ifdef USE_CLEARCOAT
		float clearcoat;
		float clearcoatRoughness;
		vec3 clearcoatF0;
		float clearcoatF90;
	#endif
	#ifdef USE_IRIDESCENCE
		float iridescence;
		float iridescenceIOR;
		float iridescenceThickness;
		vec3 iridescenceFresnel;
		vec3 iridescenceF0;
		vec3 iridescenceFresnelDielectric;
		vec3 iridescenceFresnelMetallic;
	#endif
	#ifdef USE_SHEEN
		vec3 sheenColor;
		float sheenRoughness;
	#endif
	#ifdef IOR
		float ior;
	#endif
	#ifdef USE_TRANSMISSION
		float transmission;
		float transmissionAlpha;
		float thickness;
		float attenuationDistance;
		vec3 attenuationColor;
	#endif
	#ifdef USE_ANISOTROPY
		float anisotropy;
		float alphaT;
		vec3 anisotropyT;
		vec3 anisotropyB;
	#endif
};
vec3 clearcoatSpecularDirect = vec3( 0.0 );
vec3 clearcoatSpecularIndirect = vec3( 0.0 );
vec3 sheenSpecularDirect = vec3( 0.0 );
vec3 sheenSpecularIndirect = vec3(0.0 );
vec3 Schlick_to_F0( const in vec3 f, const in float f90, const in float dotVH ) {
    float x = clamp( 1.0 - dotVH, 0.0, 1.0 );
    float x2 = x * x;
    float x5 = clamp( x * x2 * x2, 0.0, 0.9999 );
    return ( f - vec3( f90 ) * x5 ) / ( 1.0 - x5 );
}
float V_GGX_SmithCorrelated( const in float alpha, const in float dotNL, const in float dotNV ) {
	float a2 = pow2( alpha );
	float gv = dotNL * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNV ) );
	float gl = dotNV * sqrt( a2 + ( 1.0 - a2 ) * pow2( dotNL ) );
	return 0.5 / max( gv + gl, EPSILON );
}
float D_GGX( const in float alpha, const in float dotNH ) {
	float a2 = pow2( alpha );
	float denom = pow2( dotNH ) * ( a2 - 1.0 ) + 1.0;
	return RECIPROCAL_PI * a2 / pow2( denom );
}
#ifdef USE_ANISOTROPY
	float V_GGX_SmithCorrelated_Anisotropic( const in float alphaT, const in float alphaB, const in float dotTV, const in float dotBV, const in float dotTL, const in float dotBL, const in float dotNV, const in float dotNL ) {
		float gv = dotNL * length( vec3( alphaT * dotTV, alphaB * dotBV, dotNV ) );
		float gl = dotNV * length( vec3( alphaT * dotTL, alphaB * dotBL, dotNL ) );
		return 0.5 / max( gv + gl, EPSILON );
	}
	float D_GGX_Anisotropic( const in float alphaT, const in float alphaB, const in float dotNH, const in float dotTH, const in float dotBH ) {
		float a2 = alphaT * alphaB;
		highp vec3 v = vec3( alphaB * dotTH, alphaT * dotBH, a2 * dotNH );
		highp float v2 = dot( v, v );
		float w2 = a2 / v2;
		return RECIPROCAL_PI * a2 * pow2 ( w2 );
	}
#endif
#ifdef USE_CLEARCOAT
	vec3 BRDF_GGX_Clearcoat( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material) {
		vec3 f0 = material.clearcoatF0;
		float f90 = material.clearcoatF90;
		float roughness = material.clearcoatRoughness;
		float alpha = pow2( roughness );
		vec3 halfDir = normalize( lightDir + viewDir );
		float dotNL = saturate( dot( normal, lightDir ) );
		float dotNV = saturate( dot( normal, viewDir ) );
		float dotNH = saturate( dot( normal, halfDir ) );
		float dotVH = saturate( dot( viewDir, halfDir ) );
		vec3 F = F_Schlick( f0, f90, dotVH );
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
		return F * ( V * D );
	}
#endif
vec3 BRDF_GGX( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 f0 = material.specularColorBlended;
	float f90 = material.specularF90;
	float roughness = material.roughness;
	float alpha = pow2( roughness );
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float dotVH = saturate( dot( viewDir, halfDir ) );
	vec3 F = F_Schlick( f0, f90, dotVH );
	#ifdef USE_IRIDESCENCE
		F = mix( F, material.iridescenceFresnel, material.iridescence );
	#endif
	#ifdef USE_ANISOTROPY
		float dotTL = dot( material.anisotropyT, lightDir );
		float dotTV = dot( material.anisotropyT, viewDir );
		float dotTH = dot( material.anisotropyT, halfDir );
		float dotBL = dot( material.anisotropyB, lightDir );
		float dotBV = dot( material.anisotropyB, viewDir );
		float dotBH = dot( material.anisotropyB, halfDir );
		float V = V_GGX_SmithCorrelated_Anisotropic( material.alphaT, alpha, dotTV, dotBV, dotTL, dotBL, dotNV, dotNL );
		float D = D_GGX_Anisotropic( material.alphaT, alpha, dotNH, dotTH, dotBH );
	#else
		float V = V_GGX_SmithCorrelated( alpha, dotNL, dotNV );
		float D = D_GGX( alpha, dotNH );
	#endif
	return F * ( V * D );
}
vec2 LTC_Uv( const in vec3 N, const in vec3 V, const in float roughness ) {
	const float LUT_SIZE = 64.0;
	const float LUT_SCALE = ( LUT_SIZE - 1.0 ) / LUT_SIZE;
	const float LUT_BIAS = 0.5 / LUT_SIZE;
	float dotNV = saturate( dot( N, V ) );
	vec2 uv = vec2( roughness, sqrt( 1.0 - dotNV ) );
	uv = uv * LUT_SCALE + LUT_BIAS;
	return uv;
}
float LTC_ClippedSphereFormFactor( const in vec3 f ) {
	float l = length( f );
	return max( ( l * l + f.z ) / ( l + 1.0 ), 0.0 );
}
vec3 LTC_EdgeVectorFormFactor( const in vec3 v1, const in vec3 v2 ) {
	float x = dot( v1, v2 );
	float y = abs( x );
	float a = 0.8543985 + ( 0.4965155 + 0.0145206 * y ) * y;
	float b = 3.4175940 + ( 4.1616724 + y ) * y;
	float v = a / b;
	float theta_sintheta = ( x > 0.0 ) ? v : 0.5 * inversesqrt( max( 1.0 - x * x, 1e-7 ) ) - v;
	return cross( v1, v2 ) * theta_sintheta;
}
vec3 LTC_Evaluate( const in vec3 N, const in vec3 V, const in vec3 P, const in mat3 mInv, const in vec3 rectCoords[ 4 ] ) {
	vec3 v1 = rectCoords[ 1 ] - rectCoords[ 0 ];
	vec3 v2 = rectCoords[ 3 ] - rectCoords[ 0 ];
	vec3 lightNormal = cross( v1, v2 );
	if( dot( lightNormal, P - rectCoords[ 0 ] ) < 0.0 ) return vec3( 0.0 );
	vec3 T1, T2;
	T1 = normalize( V - N * dot( V, N ) );
	T2 = - cross( N, T1 );
	mat3 mat = mInv * transpose( mat3( T1, T2, N ) );
	vec3 coords[ 4 ];
	coords[ 0 ] = mat * ( rectCoords[ 0 ] - P );
	coords[ 1 ] = mat * ( rectCoords[ 1 ] - P );
	coords[ 2 ] = mat * ( rectCoords[ 2 ] - P );
	coords[ 3 ] = mat * ( rectCoords[ 3 ] - P );
	coords[ 0 ] = normalize( coords[ 0 ] );
	coords[ 1 ] = normalize( coords[ 1 ] );
	coords[ 2 ] = normalize( coords[ 2 ] );
	coords[ 3 ] = normalize( coords[ 3 ] );
	vec3 vectorFormFactor = vec3( 0.0 );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 0 ], coords[ 1 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 1 ], coords[ 2 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 2 ], coords[ 3 ] );
	vectorFormFactor += LTC_EdgeVectorFormFactor( coords[ 3 ], coords[ 0 ] );
	float result = LTC_ClippedSphereFormFactor( vectorFormFactor );
	return vec3( result );
}
#if defined( USE_SHEEN )
float D_Charlie( float roughness, float dotNH ) {
	float alpha = pow2( roughness );
	float invAlpha = 1.0 / alpha;
	float cos2h = dotNH * dotNH;
	float sin2h = max( 1.0 - cos2h, 0.0078125 );
	return ( 2.0 + invAlpha ) * pow( sin2h, invAlpha * 0.5 ) / ( 2.0 * PI );
}
float V_Neubelt( float dotNV, float dotNL ) {
	return saturate( 1.0 / ( 4.0 * ( dotNL + dotNV - dotNL * dotNV ) ) );
}
vec3 BRDF_Sheen( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, vec3 sheenColor, const in float sheenRoughness ) {
	vec3 halfDir = normalize( lightDir + viewDir );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	float dotNH = saturate( dot( normal, halfDir ) );
	float D = D_Charlie( sheenRoughness, dotNH );
	float V = V_Neubelt( dotNV, dotNL );
	return sheenColor * ( D * V );
}
#endif
float IBLSheenBRDF( const in vec3 normal, const in vec3 viewDir, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	float r2 = roughness * roughness;
	float rInv = 1.0 / ( roughness + 0.1 );
	float a = -1.9362 + 1.0678 * roughness + 0.4573 * r2 - 0.8469 * rInv;
	float b = -0.6014 + 0.5538 * roughness - 0.4670 * r2 - 0.1255 * rInv;
	float DG = exp( a * dotNV + b );
	return saturate( DG );
}
vec3 EnvironmentBRDF( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness ) {
	float dotNV = saturate( dot( normal, viewDir ) );
	vec2 fab = texture2D( dfgLUT, vec2( roughness, dotNV ) ).rg;
	return specularColor * fab.x + specularF90 * fab.y;
}
#ifdef USE_IRIDESCENCE
void computeMultiscatteringIridescence( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float iridescence, const in vec3 iridescenceF0, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#else
void computeMultiscattering( const in vec3 normal, const in vec3 viewDir, const in vec3 specularColor, const in float specularF90, const in float roughness, inout vec3 singleScatter, inout vec3 multiScatter ) {
#endif
	float dotNV = saturate( dot( normal, viewDir ) );
	vec2 fab = texture2D( dfgLUT, vec2( roughness, dotNV ) ).rg;
	#ifdef USE_IRIDESCENCE
		vec3 Fr = mix( specularColor, iridescenceF0, iridescence );
	#else
		vec3 Fr = specularColor;
	#endif
	vec3 FssEss = Fr * fab.x + specularF90 * fab.y;
	float Ess = fab.x + fab.y;
	float Ems = 1.0 - Ess;
	vec3 Favg = Fr + ( 1.0 - Fr ) * 0.047619;	vec3 Fms = FssEss * Favg / ( 1.0 - Ems * Favg );
	singleScatter += FssEss;
	multiScatter += Fms * Ems;
}
vec3 BRDF_GGX_Multiscatter( const in vec3 lightDir, const in vec3 viewDir, const in vec3 normal, const in PhysicalMaterial material ) {
	vec3 singleScatter = BRDF_GGX( lightDir, viewDir, normal, material );
	float dotNL = saturate( dot( normal, lightDir ) );
	float dotNV = saturate( dot( normal, viewDir ) );
	vec2 dfgV = texture2D( dfgLUT, vec2( material.roughness, dotNV ) ).rg;
	vec2 dfgL = texture2D( dfgLUT, vec2( material.roughness, dotNL ) ).rg;
	vec3 FssEss_V = material.specularColorBlended * dfgV.x + material.specularF90 * dfgV.y;
	vec3 FssEss_L = material.specularColorBlended * dfgL.x + material.specularF90 * dfgL.y;
	float Ess_V = dfgV.x + dfgV.y;
	float Ess_L = dfgL.x + dfgL.y;
	float Ems_V = 1.0 - Ess_V;
	float Ems_L = 1.0 - Ess_L;
	vec3 Favg = material.specularColorBlended + ( 1.0 - material.specularColorBlended ) * 0.047619;
	vec3 Fms = FssEss_V * FssEss_L * Favg / ( 1.0 - Ems_V * Ems_L * Favg + EPSILON );
	float compensationFactor = Ems_V * Ems_L;
	vec3 multiScatter = Fms * compensationFactor;
	return singleScatter + multiScatter;
}
#if NUM_RECT_AREA_LIGHTS > 0
	void RE_Direct_RectArea_Physical( const in RectAreaLight rectAreaLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
		vec3 normal = geometryNormal;
		vec3 viewDir = geometryViewDir;
		vec3 position = geometryPosition;
		vec3 lightPos = rectAreaLight.position;
		vec3 halfWidth = rectAreaLight.halfWidth;
		vec3 halfHeight = rectAreaLight.halfHeight;
		vec3 lightColor = rectAreaLight.color;
		float roughness = material.roughness;
		vec3 rectCoords[ 4 ];
		rectCoords[ 0 ] = lightPos + halfWidth - halfHeight;		rectCoords[ 1 ] = lightPos - halfWidth - halfHeight;
		rectCoords[ 2 ] = lightPos - halfWidth + halfHeight;
		rectCoords[ 3 ] = lightPos + halfWidth + halfHeight;
		vec2 uv = LTC_Uv( normal, viewDir, roughness );
		vec4 t1 = texture2D( ltc_1, uv );
		vec4 t2 = texture2D( ltc_2, uv );
		mat3 mInv = mat3(
			vec3( t1.x, 0, t1.y ),
			vec3(    0, 1,    0 ),
			vec3( t1.z, 0, t1.w )
		);
		vec3 fresnel = ( material.specularColorBlended * t2.x + ( material.specularF90 - material.specularColorBlended ) * t2.y );
		reflectedLight.directSpecular += lightColor * fresnel * LTC_Evaluate( normal, viewDir, position, mInv, rectCoords );
		reflectedLight.directDiffuse += lightColor * material.diffuseContribution * LTC_Evaluate( normal, viewDir, position, mat3( 1.0 ), rectCoords );
		#ifdef USE_CLEARCOAT
			vec3 Ncc = geometryClearcoatNormal;
			vec2 uvClearcoat = LTC_Uv( Ncc, viewDir, material.clearcoatRoughness );
			vec4 t1Clearcoat = texture2D( ltc_1, uvClearcoat );
			vec4 t2Clearcoat = texture2D( ltc_2, uvClearcoat );
			mat3 mInvClearcoat = mat3(
				vec3( t1Clearcoat.x, 0, t1Clearcoat.y ),
				vec3(             0, 1,             0 ),
				vec3( t1Clearcoat.z, 0, t1Clearcoat.w )
			);
			vec3 fresnelClearcoat = material.clearcoatF0 * t2Clearcoat.x + ( material.clearcoatF90 - material.clearcoatF0 ) * t2Clearcoat.y;
			clearcoatSpecularDirect += lightColor * fresnelClearcoat * LTC_Evaluate( Ncc, viewDir, position, mInvClearcoat, rectCoords );
		#endif
	}
#endif
void RE_Direct_Physical( const in IncidentLight directLight, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	float dotNL = saturate( dot( geometryNormal, directLight.direction ) );
	vec3 irradiance = dotNL * directLight.color;
	#ifdef USE_CLEARCOAT
		float dotNLcc = saturate( dot( geometryClearcoatNormal, directLight.direction ) );
		vec3 ccIrradiance = dotNLcc * directLight.color;
		clearcoatSpecularDirect += ccIrradiance * BRDF_GGX_Clearcoat( directLight.direction, geometryViewDir, geometryClearcoatNormal, material );
	#endif
	#ifdef USE_SHEEN
 
 		sheenSpecularDirect += irradiance * BRDF_Sheen( directLight.direction, geometryViewDir, geometryNormal, material.sheenColor, material.sheenRoughness );
 
 		float sheenAlbedoV = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
 		float sheenAlbedoL = IBLSheenBRDF( geometryNormal, directLight.direction, material.sheenRoughness );
 
 		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * max( sheenAlbedoV, sheenAlbedoL );
 
 		irradiance *= sheenEnergyComp;
 
 	#endif
	reflectedLight.directSpecular += irradiance * BRDF_GGX_Multiscatter( directLight.direction, geometryViewDir, geometryNormal, material );
	reflectedLight.directDiffuse += irradiance * BRDF_Lambert( material.diffuseContribution );
}
void RE_IndirectDiffuse_Physical( const in vec3 irradiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight ) {
	vec3 diffuse = irradiance * BRDF_Lambert( material.diffuseContribution );
	#ifdef USE_SHEEN
		float sheenAlbedo = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * sheenAlbedo;
		diffuse *= sheenEnergyComp;
	#endif
	reflectedLight.indirectDiffuse += diffuse;
}
void RE_IndirectSpecular_Physical( const in vec3 radiance, const in vec3 irradiance, const in vec3 clearcoatRadiance, const in vec3 geometryPosition, const in vec3 geometryNormal, const in vec3 geometryViewDir, const in vec3 geometryClearcoatNormal, const in PhysicalMaterial material, inout ReflectedLight reflectedLight) {
	#ifdef USE_CLEARCOAT
		clearcoatSpecularIndirect += clearcoatRadiance * EnvironmentBRDF( geometryClearcoatNormal, geometryViewDir, material.clearcoatF0, material.clearcoatF90, material.clearcoatRoughness );
	#endif
	#ifdef USE_SHEEN
		sheenSpecularIndirect += irradiance * material.sheenColor * IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness ) * RECIPROCAL_PI;
 	#endif
	vec3 singleScatteringDielectric = vec3( 0.0 );
	vec3 multiScatteringDielectric = vec3( 0.0 );
	vec3 singleScatteringMetallic = vec3( 0.0 );
	vec3 multiScatteringMetallic = vec3( 0.0 );
	#ifdef USE_IRIDESCENCE
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.iridescence, material.iridescenceFresnelDielectric, material.roughness, singleScatteringDielectric, multiScatteringDielectric );
		computeMultiscatteringIridescence( geometryNormal, geometryViewDir, material.diffuseColor, material.specularF90, material.iridescence, material.iridescenceFresnelMetallic, material.roughness, singleScatteringMetallic, multiScatteringMetallic );
	#else
		computeMultiscattering( geometryNormal, geometryViewDir, material.specularColor, material.specularF90, material.roughness, singleScatteringDielectric, multiScatteringDielectric );
		computeMultiscattering( geometryNormal, geometryViewDir, material.diffuseColor, material.specularF90, material.roughness, singleScatteringMetallic, multiScatteringMetallic );
	#endif
	vec3 singleScattering = mix( singleScatteringDielectric, singleScatteringMetallic, material.metalness );
	vec3 multiScattering = mix( multiScatteringDielectric, multiScatteringMetallic, material.metalness );
	vec3 totalScatteringDielectric = singleScatteringDielectric + multiScatteringDielectric;
	vec3 diffuse = material.diffuseContribution * ( 1.0 - totalScatteringDielectric );
	vec3 cosineWeightedIrradiance = irradiance * RECIPROCAL_PI;
	vec3 indirectSpecular = radiance * singleScattering;
	indirectSpecular += multiScattering * cosineWeightedIrradiance;
	vec3 indirectDiffuse = diffuse * cosineWeightedIrradiance;
	#ifdef USE_SHEEN
		float sheenAlbedo = IBLSheenBRDF( geometryNormal, geometryViewDir, material.sheenRoughness );
		float sheenEnergyComp = 1.0 - max3( material.sheenColor ) * sheenAlbedo;
		indirectSpecular *= sheenEnergyComp;
		indirectDiffuse *= sheenEnergyComp;
	#endif
	reflectedLight.indirectSpecular += indirectSpecular;
	reflectedLight.indirectDiffuse += indirectDiffuse;
}
#define RE_Direct				RE_Direct_Physical
#define RE_Direct_RectArea		RE_Direct_RectArea_Physical
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Physical
#define RE_IndirectSpecular		RE_IndirectSpecular_Physical
float computeSpecularOcclusion( const in float dotNV, const in float ambientOcclusion, const in float roughness ) {
	return saturate( pow( dotNV + ambientOcclusion, exp2( - 16.0 * roughness - 1.0 ) ) - 1.0 + ambientOcclusion );
}`,I0=`
vec3 geometryPosition = - vViewPosition;
vec3 geometryNormal = normal;
vec3 geometryViewDir = ( isOrthographic ) ? vec3( 0, 0, 1 ) : normalize( vViewPosition );
vec3 geometryClearcoatNormal = vec3( 0.0 );
#ifdef USE_CLEARCOAT
	geometryClearcoatNormal = clearcoatNormal;
#endif
#ifdef USE_IRIDESCENCE
	float dotNVi = saturate( dot( normal, geometryViewDir ) );
	if ( material.iridescenceThickness == 0.0 ) {
		material.iridescence = 0.0;
	} else {
		material.iridescence = saturate( material.iridescence );
	}
	if ( material.iridescence > 0.0 ) {
		material.iridescenceFresnelDielectric = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.specularColor );
		material.iridescenceFresnelMetallic = evalIridescence( 1.0, material.iridescenceIOR, dotNVi, material.iridescenceThickness, material.diffuseColor );
		material.iridescenceFresnel = mix( material.iridescenceFresnelDielectric, material.iridescenceFresnelMetallic, material.metalness );
		material.iridescenceF0 = Schlick_to_F0( material.iridescenceFresnel, 1.0, dotNVi );
	}
#endif
IncidentLight directLight;
#if ( NUM_POINT_LIGHTS > 0 ) && defined( RE_Direct )
	PointLight pointLight;
	#if defined( USE_SHADOWMAP ) && NUM_POINT_LIGHT_SHADOWS > 0
	PointLightShadow pointLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHTS; i ++ ) {
		pointLight = pointLights[ i ];
		getPointLightInfo( pointLight, geometryPosition, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_POINT_LIGHT_SHADOWS ) && ( defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_BASIC ) )
		pointLightShadow = pointLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getPointShadow( pointShadowMap[ i ], pointLightShadow.shadowMapSize, pointLightShadow.shadowIntensity, pointLightShadow.shadowBias, pointLightShadow.shadowRadius, vPointShadowCoord[ i ], pointLightShadow.shadowCameraNear, pointLightShadow.shadowCameraFar ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_SPOT_LIGHTS > 0 ) && defined( RE_Direct )
	SpotLight spotLight;
	vec4 spotColor;
	vec3 spotLightCoord;
	bool inSpotLightMap;
	#if defined( USE_SHADOWMAP ) && NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHTS; i ++ ) {
		spotLight = spotLights[ i ];
		getSpotLightInfo( spotLight, geometryPosition, directLight );
		#if ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#define SPOT_LIGHT_MAP_INDEX UNROLLED_LOOP_INDEX
		#elif ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		#define SPOT_LIGHT_MAP_INDEX NUM_SPOT_LIGHT_MAPS
		#else
		#define SPOT_LIGHT_MAP_INDEX ( UNROLLED_LOOP_INDEX - NUM_SPOT_LIGHT_SHADOWS + NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS )
		#endif
		#if ( SPOT_LIGHT_MAP_INDEX < NUM_SPOT_LIGHT_MAPS )
			spotLightCoord = vSpotLightCoord[ i ].xyz / vSpotLightCoord[ i ].w;
			inSpotLightMap = all( lessThan( abs( spotLightCoord * 2. - 1. ), vec3( 1.0 ) ) );
			spotColor = texture2D( spotLightMap[ SPOT_LIGHT_MAP_INDEX ], spotLightCoord.xy );
			directLight.color = inSpotLightMap ? directLight.color * spotColor.rgb : directLight.color;
		#endif
		#undef SPOT_LIGHT_MAP_INDEX
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
		spotLightShadow = spotLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( spotShadowMap[ i ], spotLightShadow.shadowMapSize, spotLightShadow.shadowIntensity, spotLightShadow.shadowBias, spotLightShadow.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_DIR_LIGHTS > 0 ) && defined( RE_Direct )
	DirectionalLight directionalLight;
	#if defined( USE_SHADOWMAP ) && NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLightShadow;
	#endif
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHTS; i ++ ) {
		directionalLight = directionalLights[ i ];
		getDirectionalLightInfo( directionalLight, directLight );
		#if defined( USE_SHADOWMAP ) && ( UNROLLED_LOOP_INDEX < NUM_DIR_LIGHT_SHADOWS )
		directionalLightShadow = directionalLightShadows[ i ];
		directLight.color *= ( directLight.visible && receiveShadow ) ? getShadow( directionalShadowMap[ i ], directionalLightShadow.shadowMapSize, directionalLightShadow.shadowIntensity, directionalLightShadow.shadowBias, directionalLightShadow.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
		#endif
		RE_Direct( directLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if ( NUM_RECT_AREA_LIGHTS > 0 ) && defined( RE_Direct_RectArea )
	RectAreaLight rectAreaLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_RECT_AREA_LIGHTS; i ++ ) {
		rectAreaLight = rectAreaLights[ i ];
		RE_Direct_RectArea( rectAreaLight, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
	}
	#pragma unroll_loop_end
#endif
#if defined( RE_IndirectDiffuse )
	vec3 iblIrradiance = vec3( 0.0 );
	vec3 irradiance = getAmbientLightIrradiance( ambientLightColor );
	#if defined( USE_LIGHT_PROBES )
		irradiance += getLightProbeIrradiance( lightProbe, geometryNormal );
	#endif
	#if ( NUM_HEMI_LIGHTS > 0 )
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_HEMI_LIGHTS; i ++ ) {
			irradiance += getHemisphereLightIrradiance( hemisphereLights[ i ], geometryNormal );
		}
		#pragma unroll_loop_end
	#endif
	#ifdef USE_LIGHT_PROBES_GRID
		vec3 probeWorldPos = ( ( vec4( geometryPosition, 1.0 ) - viewMatrix[ 3 ] ) * viewMatrix ).xyz;
		vec3 probeWorldNormal = inverseTransformDirection( geometryNormal, viewMatrix );
		irradiance += getLightProbeGridIrradiance( probeWorldPos, probeWorldNormal );
	#endif
#endif
#if defined( RE_IndirectSpecular )
	vec3 radiance = vec3( 0.0 );
	vec3 clearcoatRadiance = vec3( 0.0 );
#endif`,L0=`#if defined( RE_IndirectDiffuse )
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		vec3 lightMapIrradiance = lightMapTexel.rgb * lightMapIntensity;
		irradiance += lightMapIrradiance;
	#endif
	#if defined( USE_ENVMAP ) && defined( ENVMAP_TYPE_CUBE_UV )
		#if defined( STANDARD ) || defined( LAMBERT ) || defined( PHONG )
			iblIrradiance += getIBLIrradiance( geometryNormal );
		#endif
	#endif
#endif
#if defined( USE_ENVMAP ) && defined( RE_IndirectSpecular )
	#ifdef USE_ANISOTROPY
		radiance += getIBLAnisotropyRadiance( geometryViewDir, geometryNormal, material.roughness, material.anisotropyB, material.anisotropy );
	#else
		radiance += getIBLRadiance( geometryViewDir, geometryNormal, material.roughness );
	#endif
	#ifdef USE_CLEARCOAT
		clearcoatRadiance += getIBLRadiance( geometryViewDir, geometryClearcoatNormal, material.clearcoatRoughness );
	#endif
#endif`,N0=`#if defined( RE_IndirectDiffuse )
	#if defined( LAMBERT ) || defined( PHONG )
		irradiance += iblIrradiance;
	#endif
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,D0=`#ifdef USE_LIGHT_PROBES_GRID
uniform highp sampler3D probesSH;
uniform vec3 probesMin;
uniform vec3 probesMax;
uniform vec3 probesResolution;
vec3 getLightProbeGridIrradiance( vec3 worldPos, vec3 worldNormal ) {
	vec3 res = probesResolution;
	vec3 gridRange = probesMax - probesMin;
	vec3 resMinusOne = res - 1.0;
	vec3 probeSpacing = gridRange / resMinusOne;
	vec3 samplePos = worldPos + worldNormal * probeSpacing * 0.5;
	vec3 uvw = clamp( ( samplePos - probesMin ) / gridRange, 0.0, 1.0 );
	uvw = uvw * resMinusOne / res + 0.5 / res;
	float nz          = res.z;
	float paddedSlices = nz + 2.0;
	float atlasDepth  = 7.0 * paddedSlices;
	float uvZBase     = uvw.z * nz + 1.0;
	vec4 s0 = texture( probesSH, vec3( uvw.xy, ( uvZBase                       ) / atlasDepth ) );
	vec4 s1 = texture( probesSH, vec3( uvw.xy, ( uvZBase +       paddedSlices   ) / atlasDepth ) );
	vec4 s2 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 2.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s3 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 3.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s4 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 4.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s5 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 5.0 * paddedSlices   ) / atlasDepth ) );
	vec4 s6 = texture( probesSH, vec3( uvw.xy, ( uvZBase + 6.0 * paddedSlices   ) / atlasDepth ) );
	vec3 c0 = s0.xyz;
	vec3 c1 = vec3( s0.w, s1.xy );
	vec3 c2 = vec3( s1.zw, s2.x );
	vec3 c3 = s2.yzw;
	vec3 c4 = s3.xyz;
	vec3 c5 = vec3( s3.w, s4.xy );
	vec3 c6 = vec3( s4.zw, s5.x );
	vec3 c7 = s5.yzw;
	vec3 c8 = s6.xyz;
	float x = worldNormal.x, y = worldNormal.y, z = worldNormal.z;
	vec3 result = c0 * 0.886227;
	result += c1 * 2.0 * 0.511664 * y;
	result += c2 * 2.0 * 0.511664 * z;
	result += c3 * 2.0 * 0.511664 * x;
	result += c4 * 2.0 * 0.429043 * x * y;
	result += c5 * 2.0 * 0.429043 * y * z;
	result += c6 * ( 0.743125 * z * z - 0.247708 );
	result += c7 * 2.0 * 0.429043 * x * z;
	result += c8 * 0.429043 * ( x * x - y * y );
	return max( result, vec3( 0.0 ) );
}
#endif`,F0=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,U0=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,O0=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,B0=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,k0=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,z0=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,V0=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
	#if defined( USE_POINTS_UV )
		vec2 uv = vUv;
	#else
		vec2 uv = ( uvTransform * vec3( gl_PointCoord.x, 1.0 - gl_PointCoord.y, 1 ) ).xy;
	#endif
#endif
#ifdef USE_MAP
	diffuseColor *= texture2D( map, uv );
#endif
#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, uv ).g;
#endif`,G0=`#if defined( USE_POINTS_UV )
	varying vec2 vUv;
#else
	#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
		uniform mat3 uvTransform;
	#endif
#endif
#ifdef USE_MAP
	uniform sampler2D map;
#endif
#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,H0=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,W0=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,X0=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,q0=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,Y0=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,Z0=`#ifdef USE_MORPHTARGETS
	#ifndef USE_INSTANCING_MORPH
		uniform float morphTargetBaseInfluence;
		uniform float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	#endif
	uniform sampler2DArray morphTargetsTexture;
	uniform ivec2 morphTargetsTextureSize;
	vec4 getMorph( const in int vertexIndex, const in int morphTargetIndex, const in int offset ) {
		int texelIndex = vertexIndex * MORPHTARGETS_TEXTURE_STRIDE + offset;
		int y = texelIndex / morphTargetsTextureSize.x;
		int x = texelIndex - y * morphTargetsTextureSize.x;
		ivec3 morphUV = ivec3( x, y, morphTargetIndex );
		return texelFetch( morphTargetsTexture, morphUV, 0 );
	}
#endif`,K0=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,J0=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
#ifdef FLAT_SHADED
	vec3 fdx = dFdx( vViewPosition );
	vec3 fdy = dFdy( vViewPosition );
	vec3 normal = normalize( cross( fdx, fdy ) );
#else
	vec3 normal = normalize( vNormal );
	#ifdef DOUBLE_SIDED
		normal *= faceDirection;
	#endif
#endif
#if defined( USE_NORMALMAP_TANGENTSPACE ) || defined( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY )
	#ifdef USE_TANGENT
		mat3 tbn = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn = getTangentFrame( - vViewPosition, normal,
		#if defined( USE_NORMALMAP )
			vNormalMapUv
		#elif defined( USE_CLEARCOAT_NORMALMAP )
			vClearcoatNormalMapUv
		#else
			vUv
		#endif
		);
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn[0] *= faceDirection;
		tbn[1] *= faceDirection;
	#endif
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	#ifdef USE_TANGENT
		mat3 tbn2 = mat3( normalize( vTangent ), normalize( vBitangent ), normal );
	#else
		mat3 tbn2 = getTangentFrame( - vViewPosition, normal, vClearcoatNormalMapUv );
	#endif
	#if defined( DOUBLE_SIDED ) && ! defined( FLAT_SHADED )
		tbn2[0] *= faceDirection;
		tbn2[1] *= faceDirection;
	#endif
#endif
vec3 nonPerturbedNormal = normal;`,$0=`#ifdef USE_NORMALMAP_OBJECTSPACE
	normal = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#ifdef FLIP_SIDED
		normal = - normal;
	#endif
	#ifdef DOUBLE_SIDED
		normal = normal * faceDirection;
	#endif
	normal = normalize( normalMatrix * normal );
#elif defined( USE_NORMALMAP_TANGENTSPACE )
	vec3 mapN = texture2D( normalMap, vNormalMapUv ).xyz * 2.0 - 1.0;
	#if defined( USE_PACKED_NORMALMAP )
		mapN = vec3( mapN.xy, sqrt( saturate( 1.0 - dot( mapN.xy, mapN.xy ) ) ) );
	#endif
	mapN.xy *= normalScale;
	normal = normalize( tbn * mapN );
#elif defined( USE_BUMPMAP )
	normal = perturbNormalArb( - vViewPosition, normal, dHdxy_fwd(), faceDirection );
#endif`,j0=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,Q0=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,t_=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,e_=`#ifdef USE_NORMALMAP
	uniform sampler2D normalMap;
	uniform vec2 normalScale;
#endif
#ifdef USE_NORMALMAP_OBJECTSPACE
	uniform mat3 normalMatrix;
#endif
#if ! defined ( USE_TANGENT ) && ( defined ( USE_NORMALMAP_TANGENTSPACE ) || defined ( USE_CLEARCOAT_NORMALMAP ) || defined( USE_ANISOTROPY ) )
	mat3 getTangentFrame( vec3 eye_pos, vec3 surf_norm, vec2 uv ) {
		vec3 q0 = dFdx( eye_pos.xyz );
		vec3 q1 = dFdy( eye_pos.xyz );
		vec2 st0 = dFdx( uv.st );
		vec2 st1 = dFdy( uv.st );
		vec3 N = surf_norm;
		vec3 q1perp = cross( q1, N );
		vec3 q0perp = cross( N, q0 );
		vec3 T = q1perp * st0.x + q0perp * st1.x;
		vec3 B = q1perp * st0.y + q0perp * st1.y;
		float det = max( dot( T, T ), dot( B, B ) );
		float scale = ( det == 0.0 ) ? 0.0 : inversesqrt( det );
		return mat3( T * scale, B * scale, N );
	}
#endif`,n_=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,i_=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,s_=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,r_=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,a_=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,o_=`vec3 packNormalToRGB( const in vec3 normal ) {
	return normalize( normal ) * 0.5 + 0.5;
}
vec3 unpackRGBToNormal( const in vec3 rgb ) {
	return 2.0 * rgb.xyz - 1.0;
}
const float PackUpscale = 256. / 255.;const float UnpackDownscale = 255. / 256.;const float ShiftRight8 = 1. / 256.;
const float Inv255 = 1. / 255.;
const vec4 PackFactors = vec4( 1.0, 256.0, 256.0 * 256.0, 256.0 * 256.0 * 256.0 );
const vec2 UnpackFactors2 = vec2( UnpackDownscale, 1.0 / PackFactors.g );
const vec3 UnpackFactors3 = vec3( UnpackDownscale / PackFactors.rg, 1.0 / PackFactors.b );
const vec4 UnpackFactors4 = vec4( UnpackDownscale / PackFactors.rgb, 1.0 / PackFactors.a );
vec4 packDepthToRGBA( const in float v ) {
	if( v <= 0.0 )
		return vec4( 0., 0., 0., 0. );
	if( v >= 1.0 )
		return vec4( 1., 1., 1., 1. );
	float vuf;
	float af = modf( v * PackFactors.a, vuf );
	float bf = modf( vuf * ShiftRight8, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec4( vuf * Inv255, gf * PackUpscale, bf * PackUpscale, af );
}
vec3 packDepthToRGB( const in float v ) {
	if( v <= 0.0 )
		return vec3( 0., 0., 0. );
	if( v >= 1.0 )
		return vec3( 1., 1., 1. );
	float vuf;
	float bf = modf( v * PackFactors.b, vuf );
	float gf = modf( vuf * ShiftRight8, vuf );
	return vec3( vuf * Inv255, gf * PackUpscale, bf );
}
vec2 packDepthToRG( const in float v ) {
	if( v <= 0.0 )
		return vec2( 0., 0. );
	if( v >= 1.0 )
		return vec2( 1., 1. );
	float vuf;
	float gf = modf( v * 256., vuf );
	return vec2( vuf * Inv255, gf );
}
float unpackRGBAToDepth( const in vec4 v ) {
	return dot( v, UnpackFactors4 );
}
float unpackRGBToDepth( const in vec3 v ) {
	return dot( v, UnpackFactors3 );
}
float unpackRGToDepth( const in vec2 v ) {
	return v.r * UnpackFactors2.r + v.g * UnpackFactors2.g;
}
vec4 pack2HalfToRGBA( const in vec2 v ) {
	vec4 r = vec4( v.x, fract( v.x * 255.0 ), v.y, fract( v.y * 255.0 ) );
	return vec4( r.x - r.y / 255.0, r.y, r.z - r.w / 255.0, r.w );
}
vec2 unpackRGBATo2Half( const in vec4 v ) {
	return vec2( v.x + ( v.y / 255.0 ), v.z + ( v.w / 255.0 ) );
}
float viewZToOrthographicDepth( const in float viewZ, const in float near, const in float far ) {
	return ( viewZ + near ) / ( near - far );
}
float orthographicDepthToViewZ( const in float depth, const in float near, const in float far ) {
	#ifdef USE_REVERSED_DEPTH_BUFFER
	
		return depth * ( far - near ) - far;
	#else
		return depth * ( near - far ) - near;
	#endif
}
float viewZToPerspectiveDepth( const in float viewZ, const in float near, const in float far ) {
	return ( ( near + viewZ ) * far ) / ( ( far - near ) * viewZ );
}
float perspectiveDepthToViewZ( const in float depth, const in float near, const in float far ) {
	
	#ifdef USE_REVERSED_DEPTH_BUFFER
		return ( near * far ) / ( ( near - far ) * depth - near );
	#else
		return ( near * far ) / ( ( far - near ) * depth - far );
	#endif
}`,l_=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,c_=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,h_=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,u_=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,f_=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,d_=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,p_=`#if NUM_SPOT_LIGHT_COORDS > 0
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#if NUM_SPOT_LIGHT_MAPS > 0
	uniform sampler2D spotLightMap[ NUM_SPOT_LIGHT_MAPS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		#else
			uniform sampler2D directionalShadowMap[ NUM_DIR_LIGHT_SHADOWS ];
		#endif
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform sampler2DShadow spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		#else
			uniform sampler2D spotShadowMap[ NUM_SPOT_LIGHT_SHADOWS ];
		#endif
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#if defined( SHADOWMAP_TYPE_PCF )
			uniform samplerCubeShadow pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		#elif defined( SHADOWMAP_TYPE_BASIC )
			uniform samplerCube pointShadowMap[ NUM_POINT_LIGHT_SHADOWS ];
		#endif
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
	#if defined( SHADOWMAP_TYPE_PCF )
		float interleavedGradientNoise( vec2 position ) {
			return fract( 52.9829189 * fract( dot( position, vec2( 0.06711056, 0.00583715 ) ) ) );
		}
		vec2 vogelDiskSample( int sampleIndex, int samplesCount, float phi ) {
			const float goldenAngle = 2.399963229728653;
			float r = sqrt( ( float( sampleIndex ) + 0.5 ) / float( samplesCount ) );
			float theta = float( sampleIndex ) * goldenAngle + phi;
			return vec2( cos( theta ), sin( theta ) ) * r;
		}
	#endif
	#if defined( SHADOWMAP_TYPE_PCF )
		float getShadow( sampler2DShadow shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			shadowCoord.z += shadowBias;
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				vec2 texelSize = vec2( 1.0 ) / shadowMapSize;
				float radius = shadowRadius * texelSize.x;
				float phi = interleavedGradientNoise( gl_FragCoord.xy ) * PI2;
				shadow = (
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 0, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 1, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 2, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 3, 5, phi ) * radius, shadowCoord.z ) ) +
					texture( shadowMap, vec3( shadowCoord.xy + vogelDiskSample( 4, 5, phi ) * radius, shadowCoord.z ) )
				) * 0.2;
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#elif defined( SHADOWMAP_TYPE_VSM )
		float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				shadowCoord.z -= shadowBias;
			#else
				shadowCoord.z += shadowBias;
			#endif
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				vec2 distribution = texture2D( shadowMap, shadowCoord.xy ).rg;
				float mean = distribution.x;
				float variance = distribution.y * distribution.y;
				#ifdef USE_REVERSED_DEPTH_BUFFER
					float hard_shadow = step( mean, shadowCoord.z );
				#else
					float hard_shadow = step( shadowCoord.z, mean );
				#endif
				
				if ( hard_shadow == 1.0 ) {
					shadow = 1.0;
				} else {
					variance = max( variance, 0.0000001 );
					float d = shadowCoord.z - mean;
					float p_max = variance / ( variance + d * d );
					p_max = clamp( ( p_max - 0.3 ) / 0.65, 0.0, 1.0 );
					shadow = max( hard_shadow, p_max );
				}
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#else
		float getShadow( sampler2D shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord ) {
			float shadow = 1.0;
			shadowCoord.xyz /= shadowCoord.w;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				shadowCoord.z -= shadowBias;
			#else
				shadowCoord.z += shadowBias;
			#endif
			bool inFrustum = shadowCoord.x >= 0.0 && shadowCoord.x <= 1.0 && shadowCoord.y >= 0.0 && shadowCoord.y <= 1.0;
			bool frustumTest = inFrustum && shadowCoord.z <= 1.0;
			if ( frustumTest ) {
				float depth = texture2D( shadowMap, shadowCoord.xy ).r;
				#ifdef USE_REVERSED_DEPTH_BUFFER
					shadow = step( depth, shadowCoord.z );
				#else
					shadow = step( shadowCoord.z, depth );
				#endif
			}
			return mix( 1.0, shadow, shadowIntensity );
		}
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
	#if defined( SHADOWMAP_TYPE_PCF )
	float getPointShadow( samplerCubeShadow shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		vec3 bd3D = normalize( lightToPosition );
		vec3 absVec = abs( lightToPosition );
		float viewSpaceZ = max( max( absVec.x, absVec.y ), absVec.z );
		if ( viewSpaceZ - shadowCameraFar <= 0.0 && viewSpaceZ - shadowCameraNear >= 0.0 ) {
			#ifdef USE_REVERSED_DEPTH_BUFFER
				float dp = ( shadowCameraNear * ( shadowCameraFar - viewSpaceZ ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
				dp -= shadowBias;
			#else
				float dp = ( shadowCameraFar * ( viewSpaceZ - shadowCameraNear ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
				dp += shadowBias;
			#endif
			float texelSize = shadowRadius / shadowMapSize.x;
			vec3 absDir = abs( bd3D );
			vec3 tangent = absDir.x > absDir.z ? vec3( 0.0, 1.0, 0.0 ) : vec3( 1.0, 0.0, 0.0 );
			tangent = normalize( cross( bd3D, tangent ) );
			vec3 bitangent = cross( bd3D, tangent );
			float phi = interleavedGradientNoise( gl_FragCoord.xy ) * PI2;
			vec2 sample0 = vogelDiskSample( 0, 5, phi );
			vec2 sample1 = vogelDiskSample( 1, 5, phi );
			vec2 sample2 = vogelDiskSample( 2, 5, phi );
			vec2 sample3 = vogelDiskSample( 3, 5, phi );
			vec2 sample4 = vogelDiskSample( 4, 5, phi );
			shadow = (
				texture( shadowMap, vec4( bd3D + ( tangent * sample0.x + bitangent * sample0.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample1.x + bitangent * sample1.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample2.x + bitangent * sample2.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample3.x + bitangent * sample3.y ) * texelSize, dp ) ) +
				texture( shadowMap, vec4( bd3D + ( tangent * sample4.x + bitangent * sample4.y ) * texelSize, dp ) )
			) * 0.2;
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	#elif defined( SHADOWMAP_TYPE_BASIC )
	float getPointShadow( samplerCube shadowMap, vec2 shadowMapSize, float shadowIntensity, float shadowBias, float shadowRadius, vec4 shadowCoord, float shadowCameraNear, float shadowCameraFar ) {
		float shadow = 1.0;
		vec3 lightToPosition = shadowCoord.xyz;
		vec3 absVec = abs( lightToPosition );
		float viewSpaceZ = max( max( absVec.x, absVec.y ), absVec.z );
		if ( viewSpaceZ - shadowCameraFar <= 0.0 && viewSpaceZ - shadowCameraNear >= 0.0 ) {
			float dp = ( shadowCameraFar * ( viewSpaceZ - shadowCameraNear ) ) / ( viewSpaceZ * ( shadowCameraFar - shadowCameraNear ) );
			dp += shadowBias;
			vec3 bd3D = normalize( lightToPosition );
			float depth = textureCube( shadowMap, bd3D ).r;
			#ifdef USE_REVERSED_DEPTH_BUFFER
				depth = 1.0 - depth;
			#endif
			shadow = step( dp, depth );
		}
		return mix( 1.0, shadow, shadowIntensity );
	}
	#endif
	#endif
#endif`,m_=`#if NUM_SPOT_LIGHT_COORDS > 0
	uniform mat4 spotLightMatrix[ NUM_SPOT_LIGHT_COORDS ];
	varying vec4 vSpotLightCoord[ NUM_SPOT_LIGHT_COORDS ];
#endif
#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
		uniform mat4 directionalShadowMatrix[ NUM_DIR_LIGHT_SHADOWS ];
		varying vec4 vDirectionalShadowCoord[ NUM_DIR_LIGHT_SHADOWS ];
		struct DirectionalLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform DirectionalLightShadow directionalLightShadows[ NUM_DIR_LIGHT_SHADOWS ];
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
		struct SpotLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
		};
		uniform SpotLightShadow spotLightShadows[ NUM_SPOT_LIGHT_SHADOWS ];
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		uniform mat4 pointShadowMatrix[ NUM_POINT_LIGHT_SHADOWS ];
		varying vec4 vPointShadowCoord[ NUM_POINT_LIGHT_SHADOWS ];
		struct PointLightShadow {
			float shadowIntensity;
			float shadowBias;
			float shadowNormalBias;
			float shadowRadius;
			vec2 shadowMapSize;
			float shadowCameraNear;
			float shadowCameraFar;
		};
		uniform PointLightShadow pointLightShadows[ NUM_POINT_LIGHT_SHADOWS ];
	#endif
#endif`,g_=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
	#ifdef HAS_NORMAL
		vec3 shadowWorldNormal = inverseTransformDirection( transformedNormal, viewMatrix );
	#else
		vec3 shadowWorldNormal = vec3( 0.0 );
	#endif
	vec4 shadowWorldPosition;
#endif
#if defined( USE_SHADOWMAP )
	#if NUM_DIR_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * directionalLightShadows[ i ].shadowNormalBias, 0 );
			vDirectionalShadowCoord[ i ] = directionalShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0
		#pragma unroll_loop_start
		for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
			shadowWorldPosition = worldPosition + vec4( shadowWorldNormal * pointLightShadows[ i ].shadowNormalBias, 0 );
			vPointShadowCoord[ i ] = pointShadowMatrix[ i ] * shadowWorldPosition;
		}
		#pragma unroll_loop_end
	#endif
#endif
#if NUM_SPOT_LIGHT_COORDS > 0
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_COORDS; i ++ ) {
		shadowWorldPosition = worldPosition;
		#if ( defined( USE_SHADOWMAP ) && UNROLLED_LOOP_INDEX < NUM_SPOT_LIGHT_SHADOWS )
			shadowWorldPosition.xyz += shadowWorldNormal * spotLightShadows[ i ].shadowNormalBias;
		#endif
		vSpotLightCoord[ i ] = spotLightMatrix[ i ] * shadowWorldPosition;
	}
	#pragma unroll_loop_end
#endif`,__=`float getShadowMask() {
	float shadow = 1.0;
	#ifdef USE_SHADOWMAP
	#if NUM_DIR_LIGHT_SHADOWS > 0
	DirectionalLightShadow directionalLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_DIR_LIGHT_SHADOWS; i ++ ) {
		directionalLight = directionalLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( directionalShadowMap[ i ], directionalLight.shadowMapSize, directionalLight.shadowIntensity, directionalLight.shadowBias, directionalLight.shadowRadius, vDirectionalShadowCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_SPOT_LIGHT_SHADOWS > 0
	SpotLightShadow spotLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_SPOT_LIGHT_SHADOWS; i ++ ) {
		spotLight = spotLightShadows[ i ];
		shadow *= receiveShadow ? getShadow( spotShadowMap[ i ], spotLight.shadowMapSize, spotLight.shadowIntensity, spotLight.shadowBias, spotLight.shadowRadius, vSpotLightCoord[ i ] ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#if NUM_POINT_LIGHT_SHADOWS > 0 && ( defined( SHADOWMAP_TYPE_PCF ) || defined( SHADOWMAP_TYPE_BASIC ) )
	PointLightShadow pointLight;
	#pragma unroll_loop_start
	for ( int i = 0; i < NUM_POINT_LIGHT_SHADOWS; i ++ ) {
		pointLight = pointLightShadows[ i ];
		shadow *= receiveShadow ? getPointShadow( pointShadowMap[ i ], pointLight.shadowMapSize, pointLight.shadowIntensity, pointLight.shadowBias, pointLight.shadowRadius, vPointShadowCoord[ i ], pointLight.shadowCameraNear, pointLight.shadowCameraFar ) : 1.0;
	}
	#pragma unroll_loop_end
	#endif
	#endif
	return shadow;
}`,x_=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,v_=`#ifdef USE_SKINNING
	uniform mat4 bindMatrix;
	uniform mat4 bindMatrixInverse;
	uniform highp sampler2D boneTexture;
	mat4 getBoneMatrix( const in float i ) {
		int size = textureSize( boneTexture, 0 ).x;
		int j = int( i ) * 4;
		int x = j % size;
		int y = j / size;
		vec4 v1 = texelFetch( boneTexture, ivec2( x, y ), 0 );
		vec4 v2 = texelFetch( boneTexture, ivec2( x + 1, y ), 0 );
		vec4 v3 = texelFetch( boneTexture, ivec2( x + 2, y ), 0 );
		vec4 v4 = texelFetch( boneTexture, ivec2( x + 3, y ), 0 );
		return mat4( v1, v2, v3, v4 );
	}
#endif`,y_=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,M_=`#ifdef USE_SKINNING
	mat4 skinMatrix = mat4( 0.0 );
	skinMatrix += skinWeight.x * boneMatX;
	skinMatrix += skinWeight.y * boneMatY;
	skinMatrix += skinWeight.z * boneMatZ;
	skinMatrix += skinWeight.w * boneMatW;
	skinMatrix = bindMatrixInverse * skinMatrix * bindMatrix;
	objectNormal = vec4( skinMatrix * vec4( objectNormal, 0.0 ) ).xyz;
	#ifdef USE_TANGENT
		objectTangent = vec4( skinMatrix * vec4( objectTangent, 0.0 ) ).xyz;
	#endif
#endif`,b_=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,S_=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,w_=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,A_=`#ifndef saturate
#define saturate( a ) clamp( a, 0.0, 1.0 )
#endif
uniform float toneMappingExposure;
vec3 LinearToneMapping( vec3 color ) {
	return saturate( toneMappingExposure * color );
}
vec3 ReinhardToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	return saturate( color / ( vec3( 1.0 ) + color ) );
}
vec3 CineonToneMapping( vec3 color ) {
	color *= toneMappingExposure;
	color = max( vec3( 0.0 ), color - 0.004 );
	return pow( ( color * ( 6.2 * color + 0.5 ) ) / ( color * ( 6.2 * color + 1.7 ) + 0.06 ), vec3( 2.2 ) );
}
vec3 RRTAndODTFit( vec3 v ) {
	vec3 a = v * ( v + 0.0245786 ) - 0.000090537;
	vec3 b = v * ( 0.983729 * v + 0.4329510 ) + 0.238081;
	return a / b;
}
vec3 ACESFilmicToneMapping( vec3 color ) {
	const mat3 ACESInputMat = mat3(
		vec3( 0.59719, 0.07600, 0.02840 ),		vec3( 0.35458, 0.90834, 0.13383 ),
		vec3( 0.04823, 0.01566, 0.83777 )
	);
	const mat3 ACESOutputMat = mat3(
		vec3(  1.60475, -0.10208, -0.00327 ),		vec3( -0.53108,  1.10813, -0.07276 ),
		vec3( -0.07367, -0.00605,  1.07602 )
	);
	color *= toneMappingExposure / 0.6;
	color = ACESInputMat * color;
	color = RRTAndODTFit( color );
	color = ACESOutputMat * color;
	return saturate( color );
}
const mat3 LINEAR_REC2020_TO_LINEAR_SRGB = mat3(
	vec3( 1.6605, - 0.1246, - 0.0182 ),
	vec3( - 0.5876, 1.1329, - 0.1006 ),
	vec3( - 0.0728, - 0.0083, 1.1187 )
);
const mat3 LINEAR_SRGB_TO_LINEAR_REC2020 = mat3(
	vec3( 0.6274, 0.0691, 0.0164 ),
	vec3( 0.3293, 0.9195, 0.0880 ),
	vec3( 0.0433, 0.0113, 0.8956 )
);
vec3 agxDefaultContrastApprox( vec3 x ) {
	vec3 x2 = x * x;
	vec3 x4 = x2 * x2;
	return + 15.5 * x4 * x2
		- 40.14 * x4 * x
		+ 31.96 * x4
		- 6.868 * x2 * x
		+ 0.4298 * x2
		+ 0.1191 * x
		- 0.00232;
}
vec3 AgXToneMapping( vec3 color ) {
	const mat3 AgXInsetMatrix = mat3(
		vec3( 0.856627153315983, 0.137318972929847, 0.11189821299995 ),
		vec3( 0.0951212405381588, 0.761241990602591, 0.0767994186031903 ),
		vec3( 0.0482516061458583, 0.101439036467562, 0.811302368396859 )
	);
	const mat3 AgXOutsetMatrix = mat3(
		vec3( 1.1271005818144368, - 0.1413297634984383, - 0.14132976349843826 ),
		vec3( - 0.11060664309660323, 1.157823702216272, - 0.11060664309660294 ),
		vec3( - 0.016493938717834573, - 0.016493938717834257, 1.2519364065950405 )
	);
	const float AgxMinEv = - 12.47393;	const float AgxMaxEv = 4.026069;
	color *= toneMappingExposure;
	color = LINEAR_SRGB_TO_LINEAR_REC2020 * color;
	color = AgXInsetMatrix * color;
	color = max( color, 1e-10 );	color = log2( color );
	color = ( color - AgxMinEv ) / ( AgxMaxEv - AgxMinEv );
	color = clamp( color, 0.0, 1.0 );
	color = agxDefaultContrastApprox( color );
	color = AgXOutsetMatrix * color;
	color = pow( max( vec3( 0.0 ), color ), vec3( 2.2 ) );
	color = LINEAR_REC2020_TO_LINEAR_SRGB * color;
	color = clamp( color, 0.0, 1.0 );
	return color;
}
vec3 NeutralToneMapping( vec3 color ) {
	const float StartCompression = 0.8 - 0.04;
	const float Desaturation = 0.15;
	color *= toneMappingExposure;
	float x = min( color.r, min( color.g, color.b ) );
	float offset = x < 0.08 ? x - 6.25 * x * x : 0.04;
	color -= offset;
	float peak = max( color.r, max( color.g, color.b ) );
	if ( peak < StartCompression ) return color;
	float d = 1. - StartCompression;
	float newPeak = 1. - d * d / ( peak + d - StartCompression );
	color *= newPeak / peak;
	float g = 1. - 1. / ( Desaturation * ( peak - newPeak ) + 1. );
	return mix( color, vec3( newPeak ), g );
}
vec3 CustomToneMapping( vec3 color ) { return color; }`,T_=`#ifdef USE_TRANSMISSION
	material.transmission = transmission;
	material.transmissionAlpha = 1.0;
	material.thickness = thickness;
	material.attenuationDistance = attenuationDistance;
	material.attenuationColor = attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		material.transmission *= texture2D( transmissionMap, vTransmissionMapUv ).r;
	#endif
	#ifdef USE_THICKNESSMAP
		material.thickness *= texture2D( thicknessMap, vThicknessMapUv ).g;
	#endif
	vec3 pos = vWorldPosition;
	vec3 v = normalize( cameraPosition - pos );
	vec3 n = inverseTransformDirection( normal, viewMatrix );
	vec4 transmitted = getIBLVolumeRefraction(
		n, v, material.roughness, material.diffuseContribution, material.specularColorBlended, material.specularF90,
		pos, modelMatrix, viewMatrix, projectionMatrix, material.dispersion, material.ior, material.thickness,
		material.attenuationColor, material.attenuationDistance );
	material.transmissionAlpha = mix( material.transmissionAlpha, transmitted.a, material.transmission );
	totalDiffuse = mix( totalDiffuse, transmitted.rgb, material.transmission );
#endif`,E_=`#ifdef USE_TRANSMISSION
	uniform float transmission;
	uniform float thickness;
	uniform float attenuationDistance;
	uniform vec3 attenuationColor;
	#ifdef USE_TRANSMISSIONMAP
		uniform sampler2D transmissionMap;
	#endif
	#ifdef USE_THICKNESSMAP
		uniform sampler2D thicknessMap;
	#endif
	uniform vec2 transmissionSamplerSize;
	uniform sampler2D transmissionSamplerMap;
	uniform mat4 modelMatrix;
	uniform mat4 projectionMatrix;
	varying vec3 vWorldPosition;
	float w0( float a ) {
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - a + 3.0 ) - 3.0 ) + 1.0 );
	}
	float w1( float a ) {
		return ( 1.0 / 6.0 ) * ( a *  a * ( 3.0 * a - 6.0 ) + 4.0 );
	}
	float w2( float a ){
		return ( 1.0 / 6.0 ) * ( a * ( a * ( - 3.0 * a + 3.0 ) + 3.0 ) + 1.0 );
	}
	float w3( float a ) {
		return ( 1.0 / 6.0 ) * ( a * a * a );
	}
	float g0( float a ) {
		return w0( a ) + w1( a );
	}
	float g1( float a ) {
		return w2( a ) + w3( a );
	}
	float h0( float a ) {
		return - 1.0 + w1( a ) / ( w0( a ) + w1( a ) );
	}
	float h1( float a ) {
		return 1.0 + w3( a ) / ( w2( a ) + w3( a ) );
	}
	vec4 bicubic( sampler2D tex, vec2 uv, vec4 texelSize, float lod ) {
		uv = uv * texelSize.zw + 0.5;
		vec2 iuv = floor( uv );
		vec2 fuv = fract( uv );
		float g0x = g0( fuv.x );
		float g1x = g1( fuv.x );
		float h0x = h0( fuv.x );
		float h1x = h1( fuv.x );
		float h0y = h0( fuv.y );
		float h1y = h1( fuv.y );
		vec2 p0 = ( vec2( iuv.x + h0x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p1 = ( vec2( iuv.x + h1x, iuv.y + h0y ) - 0.5 ) * texelSize.xy;
		vec2 p2 = ( vec2( iuv.x + h0x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		vec2 p3 = ( vec2( iuv.x + h1x, iuv.y + h1y ) - 0.5 ) * texelSize.xy;
		return g0( fuv.y ) * ( g0x * textureLod( tex, p0, lod ) + g1x * textureLod( tex, p1, lod ) ) +
			g1( fuv.y ) * ( g0x * textureLod( tex, p2, lod ) + g1x * textureLod( tex, p3, lod ) );
	}
	vec4 textureBicubic( sampler2D sampler, vec2 uv, float lod ) {
		vec2 fLodSize = vec2( textureSize( sampler, int( lod ) ) );
		vec2 cLodSize = vec2( textureSize( sampler, int( lod + 1.0 ) ) );
		vec2 fLodSizeInv = 1.0 / fLodSize;
		vec2 cLodSizeInv = 1.0 / cLodSize;
		vec4 fSample = bicubic( sampler, uv, vec4( fLodSizeInv, fLodSize ), floor( lod ) );
		vec4 cSample = bicubic( sampler, uv, vec4( cLodSizeInv, cLodSize ), ceil( lod ) );
		return mix( fSample, cSample, fract( lod ) );
	}
	vec3 getVolumeTransmissionRay( const in vec3 n, const in vec3 v, const in float thickness, const in float ior, const in mat4 modelMatrix ) {
		vec3 refractionVector = refract( - v, normalize( n ), 1.0 / ior );
		vec3 modelScale;
		modelScale.x = length( vec3( modelMatrix[ 0 ].xyz ) );
		modelScale.y = length( vec3( modelMatrix[ 1 ].xyz ) );
		modelScale.z = length( vec3( modelMatrix[ 2 ].xyz ) );
		return normalize( refractionVector ) * thickness * modelScale;
	}
	float applyIorToRoughness( const in float roughness, const in float ior ) {
		return roughness * clamp( ior * 2.0 - 2.0, 0.0, 1.0 );
	}
	vec4 getTransmissionSample( const in vec2 fragCoord, const in float roughness, const in float ior ) {
		float lod = log2( transmissionSamplerSize.x ) * applyIorToRoughness( roughness, ior );
		return textureBicubic( transmissionSamplerMap, fragCoord.xy, lod );
	}
	vec3 volumeAttenuation( const in float transmissionDistance, const in vec3 attenuationColor, const in float attenuationDistance ) {
		if ( isinf( attenuationDistance ) ) {
			return vec3( 1.0 );
		} else {
			vec3 attenuationCoefficient = -log( attenuationColor ) / attenuationDistance;
			vec3 transmittance = exp( - attenuationCoefficient * transmissionDistance );			return transmittance;
		}
	}
	vec4 getIBLVolumeRefraction( const in vec3 n, const in vec3 v, const in float roughness, const in vec3 diffuseColor,
		const in vec3 specularColor, const in float specularF90, const in vec3 position, const in mat4 modelMatrix,
		const in mat4 viewMatrix, const in mat4 projMatrix, const in float dispersion, const in float ior, const in float thickness,
		const in vec3 attenuationColor, const in float attenuationDistance ) {
		vec4 transmittedLight;
		vec3 transmittance;
		#ifdef USE_DISPERSION
			float halfSpread = ( ior - 1.0 ) * 0.025 * dispersion;
			vec3 iors = vec3( ior - halfSpread, ior, ior + halfSpread );
			for ( int i = 0; i < 3; i ++ ) {
				vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, iors[ i ], modelMatrix );
				vec3 refractedRayExit = position + transmissionRay;
				vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
				vec2 refractionCoords = ndcPos.xy / ndcPos.w;
				refractionCoords += 1.0;
				refractionCoords /= 2.0;
				vec4 transmissionSample = getTransmissionSample( refractionCoords, roughness, iors[ i ] );
				transmittedLight[ i ] = transmissionSample[ i ];
				transmittedLight.a += transmissionSample.a;
				transmittance[ i ] = diffuseColor[ i ] * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance )[ i ];
			}
			transmittedLight.a /= 3.0;
		#else
			vec3 transmissionRay = getVolumeTransmissionRay( n, v, thickness, ior, modelMatrix );
			vec3 refractedRayExit = position + transmissionRay;
			vec4 ndcPos = projMatrix * viewMatrix * vec4( refractedRayExit, 1.0 );
			vec2 refractionCoords = ndcPos.xy / ndcPos.w;
			refractionCoords += 1.0;
			refractionCoords /= 2.0;
			transmittedLight = getTransmissionSample( refractionCoords, roughness, ior );
			transmittance = diffuseColor * volumeAttenuation( length( transmissionRay ), attenuationColor, attenuationDistance );
		#endif
		vec3 attenuatedColor = transmittance * transmittedLight.rgb;
		vec3 F = EnvironmentBRDF( n, v, specularColor, specularF90, roughness );
		float transmittanceFactor = ( transmittance.r + transmittance.g + transmittance.b ) / 3.0;
		return vec4( ( 1.0 - F ) * attenuatedColor, 1.0 - ( 1.0 - transmittedLight.a ) * transmittanceFactor );
	}
#endif`,C_=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_SPECULARMAP
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,R_=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	varying vec2 vUv;
#endif
#ifdef USE_MAP
	uniform mat3 mapTransform;
	varying vec2 vMapUv;
#endif
#ifdef USE_ALPHAMAP
	uniform mat3 alphaMapTransform;
	varying vec2 vAlphaMapUv;
#endif
#ifdef USE_LIGHTMAP
	uniform mat3 lightMapTransform;
	varying vec2 vLightMapUv;
#endif
#ifdef USE_AOMAP
	uniform mat3 aoMapTransform;
	varying vec2 vAoMapUv;
#endif
#ifdef USE_BUMPMAP
	uniform mat3 bumpMapTransform;
	varying vec2 vBumpMapUv;
#endif
#ifdef USE_NORMALMAP
	uniform mat3 normalMapTransform;
	varying vec2 vNormalMapUv;
#endif
#ifdef USE_DISPLACEMENTMAP
	uniform mat3 displacementMapTransform;
	varying vec2 vDisplacementMapUv;
#endif
#ifdef USE_EMISSIVEMAP
	uniform mat3 emissiveMapTransform;
	varying vec2 vEmissiveMapUv;
#endif
#ifdef USE_METALNESSMAP
	uniform mat3 metalnessMapTransform;
	varying vec2 vMetalnessMapUv;
#endif
#ifdef USE_ROUGHNESSMAP
	uniform mat3 roughnessMapTransform;
	varying vec2 vRoughnessMapUv;
#endif
#ifdef USE_ANISOTROPYMAP
	uniform mat3 anisotropyMapTransform;
	varying vec2 vAnisotropyMapUv;
#endif
#ifdef USE_CLEARCOATMAP
	uniform mat3 clearcoatMapTransform;
	varying vec2 vClearcoatMapUv;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform mat3 clearcoatNormalMapTransform;
	varying vec2 vClearcoatNormalMapUv;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform mat3 clearcoatRoughnessMapTransform;
	varying vec2 vClearcoatRoughnessMapUv;
#endif
#ifdef USE_SHEEN_COLORMAP
	uniform mat3 sheenColorMapTransform;
	varying vec2 vSheenColorMapUv;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	uniform mat3 sheenRoughnessMapTransform;
	varying vec2 vSheenRoughnessMapUv;
#endif
#ifdef USE_IRIDESCENCEMAP
	uniform mat3 iridescenceMapTransform;
	varying vec2 vIridescenceMapUv;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform mat3 iridescenceThicknessMapTransform;
	varying vec2 vIridescenceThicknessMapUv;
#endif
#ifdef USE_SPECULARMAP
	uniform mat3 specularMapTransform;
	varying vec2 vSpecularMapUv;
#endif
#ifdef USE_SPECULAR_COLORMAP
	uniform mat3 specularColorMapTransform;
	varying vec2 vSpecularColorMapUv;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	uniform mat3 specularIntensityMapTransform;
	varying vec2 vSpecularIntensityMapUv;
#endif
#ifdef USE_TRANSMISSIONMAP
	uniform mat3 transmissionMapTransform;
	varying vec2 vTransmissionMapUv;
#endif
#ifdef USE_THICKNESSMAP
	uniform mat3 thicknessMapTransform;
	varying vec2 vThicknessMapUv;
#endif`,P_=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
	vUv = vec3( uv, 1 ).xy;
#endif
#ifdef USE_MAP
	vMapUv = ( mapTransform * vec3( MAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ALPHAMAP
	vAlphaMapUv = ( alphaMapTransform * vec3( ALPHAMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_LIGHTMAP
	vLightMapUv = ( lightMapTransform * vec3( LIGHTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_AOMAP
	vAoMapUv = ( aoMapTransform * vec3( AOMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_BUMPMAP
	vBumpMapUv = ( bumpMapTransform * vec3( BUMPMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_NORMALMAP
	vNormalMapUv = ( normalMapTransform * vec3( NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_DISPLACEMENTMAP
	vDisplacementMapUv = ( displacementMapTransform * vec3( DISPLACEMENTMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_EMISSIVEMAP
	vEmissiveMapUv = ( emissiveMapTransform * vec3( EMISSIVEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_METALNESSMAP
	vMetalnessMapUv = ( metalnessMapTransform * vec3( METALNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ROUGHNESSMAP
	vRoughnessMapUv = ( roughnessMapTransform * vec3( ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_ANISOTROPYMAP
	vAnisotropyMapUv = ( anisotropyMapTransform * vec3( ANISOTROPYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOATMAP
	vClearcoatMapUv = ( clearcoatMapTransform * vec3( CLEARCOATMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	vClearcoatNormalMapUv = ( clearcoatNormalMapTransform * vec3( CLEARCOAT_NORMALMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	vClearcoatRoughnessMapUv = ( clearcoatRoughnessMapTransform * vec3( CLEARCOAT_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCEMAP
	vIridescenceMapUv = ( iridescenceMapTransform * vec3( IRIDESCENCEMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	vIridescenceThicknessMapUv = ( iridescenceThicknessMapTransform * vec3( IRIDESCENCE_THICKNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_COLORMAP
	vSheenColorMapUv = ( sheenColorMapTransform * vec3( SHEEN_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SHEEN_ROUGHNESSMAP
	vSheenRoughnessMapUv = ( sheenRoughnessMapTransform * vec3( SHEEN_ROUGHNESSMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULARMAP
	vSpecularMapUv = ( specularMapTransform * vec3( SPECULARMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_COLORMAP
	vSpecularColorMapUv = ( specularColorMapTransform * vec3( SPECULAR_COLORMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_SPECULAR_INTENSITYMAP
	vSpecularIntensityMapUv = ( specularIntensityMapTransform * vec3( SPECULAR_INTENSITYMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_TRANSMISSIONMAP
	vTransmissionMapUv = ( transmissionMapTransform * vec3( TRANSMISSIONMAP_UV, 1 ) ).xy;
#endif
#ifdef USE_THICKNESSMAP
	vThicknessMapUv = ( thicknessMapTransform * vec3( THICKNESSMAP_UV, 1 ) ).xy;
#endif`,I_=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`,L_=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,N_=`uniform sampler2D t2D;
uniform float backgroundIntensity;
varying vec2 vUv;
void main() {
	vec4 texColor = texture2D( t2D, vUv );
	#ifdef DECODE_VIDEO_TEXTURE
		texColor = vec4( mix( pow( texColor.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), texColor.rgb * 0.0773993808, vec3( lessThanEqual( texColor.rgb, vec3( 0.04045 ) ) ) ), texColor.w );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,D_=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,F_=`#ifdef ENVMAP_TYPE_CUBE
	uniform samplerCube envMap;
#elif defined( ENVMAP_TYPE_CUBE_UV )
	uniform sampler2D envMap;
#endif
uniform float backgroundBlurriness;
uniform float backgroundIntensity;
uniform mat3 backgroundRotation;
varying vec3 vWorldDirection;
#include <cube_uv_reflection_fragment>
void main() {
	#ifdef ENVMAP_TYPE_CUBE
		vec4 texColor = textureCube( envMap, backgroundRotation * vWorldDirection );
	#elif defined( ENVMAP_TYPE_CUBE_UV )
		vec4 texColor = textureCubeUV( envMap, backgroundRotation * vWorldDirection, backgroundBlurriness );
	#else
		vec4 texColor = vec4( 0.0, 0.0, 0.0, 1.0 );
	#endif
	texColor.rgb *= backgroundIntensity;
	gl_FragColor = texColor;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,U_=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,O_=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,B_=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
varying vec2 vHighPrecisionZW;
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vHighPrecisionZW = gl_Position.zw;
}`,k_=`#if DEPTH_PACKING == 3200
	uniform float opacity;
#endif
#include <common>
#include <packing>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
varying vec2 vHighPrecisionZW;
void main() {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#if DEPTH_PACKING == 3200
		diffuseColor.a = opacity;
	#endif
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <logdepthbuf_fragment>
	#ifdef USE_REVERSED_DEPTH_BUFFER
		float fragCoordZ = vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ];
	#else
		float fragCoordZ = 0.5 * vHighPrecisionZW[ 0 ] / vHighPrecisionZW[ 1 ] + 0.5;
	#endif
	#if DEPTH_PACKING == 3200
		gl_FragColor = vec4( vec3( 1.0 - fragCoordZ ), opacity );
	#elif DEPTH_PACKING == 3201
		gl_FragColor = packDepthToRGBA( fragCoordZ );
	#elif DEPTH_PACKING == 3202
		gl_FragColor = vec4( packDepthToRGB( fragCoordZ ), 1.0 );
	#elif DEPTH_PACKING == 3203
		gl_FragColor = vec4( packDepthToRG( fragCoordZ ), 0.0, 1.0 );
	#endif
}`,z_=`#define DISTANCE
varying vec3 vWorldPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <skinbase_vertex>
	#include <morphinstance_vertex>
	#ifdef USE_DISPLACEMENTMAP
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <worldpos_vertex>
	#include <clipping_planes_vertex>
	vWorldPosition = worldPosition.xyz;
}`,V_=`#define DISTANCE
uniform vec3 referencePosition;
uniform float nearDistance;
uniform float farDistance;
varying vec3 vWorldPosition;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <clipping_planes_pars_fragment>
void main () {
	vec4 diffuseColor = vec4( 1.0 );
	#include <clipping_planes_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	float dist = length( vWorldPosition - referencePosition );
	dist = ( dist - nearDistance ) / ( farDistance - nearDistance );
	dist = saturate( dist );
	gl_FragColor = vec4( dist, 0.0, 0.0, 1.0 );
}`,G_=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,H_=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,W_=`uniform float scale;
attribute float lineDistance;
varying float vLineDistance;
#include <common>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	vLineDistance = scale * lineDistance;
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,X_=`uniform vec3 diffuse;
uniform float opacity;
uniform float dashSize;
uniform float totalSize;
varying float vLineDistance;
#include <common>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	if ( mod( vLineDistance, totalSize ) > dashSize ) {
		discard;
	}
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,q_=`#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#if defined ( USE_ENVMAP ) || defined ( USE_SKINNING )
		#include <beginnormal_vertex>
		#include <morphnormal_vertex>
		#include <skinbase_vertex>
		#include <skinnormal_vertex>
		#include <defaultnormal_vertex>
	#endif
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <fog_vertex>
}`,Y_=`uniform vec3 diffuse;
uniform float opacity;
#ifndef FLAT_SHADED
	varying vec3 vNormal;
#endif
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <fog_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	#ifdef USE_LIGHTMAP
		vec4 lightMapTexel = texture2D( lightMap, vLightMapUv );
		reflectedLight.indirectDiffuse += lightMapTexel.rgb * lightMapIntensity * RECIPROCAL_PI;
	#else
		reflectedLight.indirectDiffuse += vec3( 1.0 );
	#endif
	#include <aomap_fragment>
	reflectedLight.indirectDiffuse *= diffuseColor.rgb;
	vec3 outgoingLight = reflectedLight.indirectDiffuse;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,Z_=`#define LAMBERT
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,K_=`#define LAMBERT
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_lambert_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_lambert_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,J_=`#define MATCAP
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <color_pars_vertex>
#include <displacementmap_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
	vViewPosition = - mvPosition.xyz;
}`,$_=`#define MATCAP
uniform vec3 diffuse;
uniform float opacity;
uniform sampler2D matcap;
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	vec3 viewDir = normalize( vViewPosition );
	vec3 x = normalize( vec3( viewDir.z, 0.0, - viewDir.x ) );
	vec3 y = cross( viewDir, x );
	vec2 uv = vec2( dot( x, normal ), dot( y, normal ) ) * 0.495 + 0.5;
	#ifdef USE_MATCAP
		vec4 matcapColor = texture2D( matcap, uv );
	#else
		vec4 matcapColor = vec4( vec3( mix( 0.2, 0.8, uv.y ) ), 1.0 );
	#endif
	vec3 outgoingLight = diffuseColor.rgb * matcapColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,j_=`#define NORMAL
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	vViewPosition = - mvPosition.xyz;
#endif
}`,Q_=`#define NORMAL
uniform float opacity;
#if defined( FLAT_SHADED ) || defined( USE_BUMPMAP ) || defined( USE_NORMALMAP_TANGENTSPACE )
	varying vec3 vViewPosition;
#endif
#include <uv_pars_fragment>
#include <normal_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( 0.0, 0.0, 0.0, opacity );
	#include <clipping_planes_fragment>
	#include <logdepthbuf_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	gl_FragColor = vec4( normalize( normal ) * 0.5 + 0.5, diffuseColor.a );
	#ifdef OPAQUE
		gl_FragColor.a = 1.0;
	#endif
}`,tx=`#define PHONG
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <envmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <envmap_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,ex=`#define PHONG
uniform vec3 diffuse;
uniform vec3 emissive;
uniform vec3 specular;
uniform float shininess;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_phong_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <specularmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <specularmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_phong_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + reflectedLight.directSpecular + reflectedLight.indirectSpecular + totalEmissiveRadiance;
	#include <envmap_fragment>
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,nx=`#define STANDARD
varying vec3 vViewPosition;
#ifdef USE_TRANSMISSION
	varying vec3 vWorldPosition;
#endif
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
#ifdef USE_TRANSMISSION
	vWorldPosition = worldPosition.xyz;
#endif
}`,ix=`#define STANDARD
#ifdef PHYSICAL
	#define IOR
	#define USE_SPECULAR
#endif
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float roughness;
uniform float metalness;
uniform float opacity;
#ifdef IOR
	uniform float ior;
#endif
#ifdef USE_SPECULAR
	uniform float specularIntensity;
	uniform vec3 specularColor;
	#ifdef USE_SPECULAR_COLORMAP
		uniform sampler2D specularColorMap;
	#endif
	#ifdef USE_SPECULAR_INTENSITYMAP
		uniform sampler2D specularIntensityMap;
	#endif
#endif
#ifdef USE_CLEARCOAT
	uniform float clearcoat;
	uniform float clearcoatRoughness;
#endif
#ifdef USE_DISPERSION
	uniform float dispersion;
#endif
#ifdef USE_IRIDESCENCE
	uniform float iridescence;
	uniform float iridescenceIOR;
	uniform float iridescenceThicknessMinimum;
	uniform float iridescenceThicknessMaximum;
#endif
#ifdef USE_SHEEN
	uniform vec3 sheenColor;
	uniform float sheenRoughness;
	#ifdef USE_SHEEN_COLORMAP
		uniform sampler2D sheenColorMap;
	#endif
	#ifdef USE_SHEEN_ROUGHNESSMAP
		uniform sampler2D sheenRoughnessMap;
	#endif
#endif
#ifdef USE_ANISOTROPY
	uniform vec2 anisotropyVector;
	#ifdef USE_ANISOTROPYMAP
		uniform sampler2D anisotropyMap;
	#endif
#endif
varying vec3 vViewPosition;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <iridescence_fragment>
#include <cube_uv_reflection_fragment>
#include <envmap_common_pars_fragment>
#include <envmap_physical_pars_fragment>
#include <fog_pars_fragment>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_physical_pars_fragment>
#include <transmission_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <clearcoat_pars_fragment>
#include <iridescence_pars_fragment>
#include <roughnessmap_pars_fragment>
#include <metalnessmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <roughnessmap_fragment>
	#include <metalnessmap_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <clearcoat_normal_fragment_begin>
	#include <clearcoat_normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_physical_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 totalDiffuse = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse;
	vec3 totalSpecular = reflectedLight.directSpecular + reflectedLight.indirectSpecular;
	#include <transmission_fragment>
	vec3 outgoingLight = totalDiffuse + totalSpecular + totalEmissiveRadiance;
	#ifdef USE_SHEEN
 
		outgoingLight = outgoingLight + sheenSpecularDirect + sheenSpecularIndirect;
 
 	#endif
	#ifdef USE_CLEARCOAT
		float dotNVcc = saturate( dot( geometryClearcoatNormal, geometryViewDir ) );
		vec3 Fcc = F_Schlick( material.clearcoatF0, material.clearcoatF90, dotNVcc );
		outgoingLight = outgoingLight * ( 1.0 - material.clearcoat * Fcc ) + ( clearcoatSpecularDirect + clearcoatSpecularIndirect ) * material.clearcoat;
	#endif
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,sx=`#define TOON
varying vec3 vViewPosition;
#include <common>
#include <batching_pars_vertex>
#include <uv_pars_vertex>
#include <displacementmap_pars_vertex>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <normal_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <shadowmap_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <normal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <displacementmap_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	vViewPosition = - mvPosition.xyz;
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,rx=`#define TOON
uniform vec3 diffuse;
uniform vec3 emissive;
uniform float opacity;
#include <common>
#include <dithering_pars_fragment>
#include <color_pars_fragment>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <aomap_pars_fragment>
#include <lightmap_pars_fragment>
#include <emissivemap_pars_fragment>
#include <gradientmap_pars_fragment>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <normal_pars_fragment>
#include <lights_toon_pars_fragment>
#include <shadowmap_pars_fragment>
#include <bumpmap_pars_fragment>
#include <normalmap_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	ReflectedLight reflectedLight = ReflectedLight( vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ), vec3( 0.0 ) );
	vec3 totalEmissiveRadiance = emissive;
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <color_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	#include <normal_fragment_begin>
	#include <normal_fragment_maps>
	#include <emissivemap_fragment>
	#include <lights_toon_fragment>
	#include <lights_fragment_begin>
	#include <lights_fragment_maps>
	#include <lights_fragment_end>
	#include <aomap_fragment>
	vec3 outgoingLight = reflectedLight.directDiffuse + reflectedLight.indirectDiffuse + totalEmissiveRadiance;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
	#include <dithering_fragment>
}`,ax=`uniform float size;
uniform float scale;
#include <common>
#include <color_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
#ifdef USE_POINTS_UV
	varying vec2 vUv;
	uniform mat3 uvTransform;
#endif
void main() {
	#ifdef USE_POINTS_UV
		vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	#endif
	#include <color_vertex>
	#include <morphinstance_vertex>
	#include <morphcolor_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <project_vertex>
	gl_PointSize = size;
	#ifdef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) gl_PointSize *= ( scale / - mvPosition.z );
	#endif
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <worldpos_vertex>
	#include <fog_vertex>
}`,ox=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <color_pars_fragment>
#include <map_particle_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_particle_fragment>
	#include <color_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,lx=`#include <common>
#include <batching_pars_vertex>
#include <fog_pars_vertex>
#include <morphtarget_pars_vertex>
#include <skinning_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <shadowmap_pars_vertex>
void main() {
	#include <batching_vertex>
	#include <beginnormal_vertex>
	#include <morphinstance_vertex>
	#include <morphnormal_vertex>
	#include <skinbase_vertex>
	#include <skinnormal_vertex>
	#include <defaultnormal_vertex>
	#include <begin_vertex>
	#include <morphtarget_vertex>
	#include <skinning_vertex>
	#include <project_vertex>
	#include <logdepthbuf_vertex>
	#include <worldpos_vertex>
	#include <shadowmap_vertex>
	#include <fog_vertex>
}`,cx=`uniform vec3 color;
uniform float opacity;
#include <common>
#include <fog_pars_fragment>
#include <bsdfs>
#include <lights_pars_begin>
#include <logdepthbuf_pars_fragment>
#include <shadowmap_pars_fragment>
#include <shadowmask_pars_fragment>
void main() {
	#include <logdepthbuf_fragment>
	gl_FragColor = vec4( color, opacity * ( 1.0 - getShadowMask() ) );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
	#include <premultiplied_alpha_fragment>
}`,hx=`uniform float rotation;
uniform vec2 center;
#include <common>
#include <uv_pars_vertex>
#include <fog_pars_vertex>
#include <logdepthbuf_pars_vertex>
#include <clipping_planes_pars_vertex>
void main() {
	#include <uv_vertex>
	vec4 mvPosition = modelViewMatrix[ 3 ];
	vec2 scale = vec2( length( modelMatrix[ 0 ].xyz ), length( modelMatrix[ 1 ].xyz ) );
	#ifndef USE_SIZEATTENUATION
		bool isPerspective = isPerspectiveMatrix( projectionMatrix );
		if ( isPerspective ) scale *= - mvPosition.z;
	#endif
	vec2 alignedPosition = ( position.xy - ( center - vec2( 0.5 ) ) ) * scale;
	vec2 rotatedPosition;
	rotatedPosition.x = cos( rotation ) * alignedPosition.x - sin( rotation ) * alignedPosition.y;
	rotatedPosition.y = sin( rotation ) * alignedPosition.x + cos( rotation ) * alignedPosition.y;
	mvPosition.xy += rotatedPosition;
	gl_Position = projectionMatrix * mvPosition;
	#include <logdepthbuf_vertex>
	#include <clipping_planes_vertex>
	#include <fog_vertex>
}`,ux=`uniform vec3 diffuse;
uniform float opacity;
#include <common>
#include <uv_pars_fragment>
#include <map_pars_fragment>
#include <alphamap_pars_fragment>
#include <alphatest_pars_fragment>
#include <alphahash_pars_fragment>
#include <fog_pars_fragment>
#include <logdepthbuf_pars_fragment>
#include <clipping_planes_pars_fragment>
void main() {
	vec4 diffuseColor = vec4( diffuse, opacity );
	#include <clipping_planes_fragment>
	vec3 outgoingLight = vec3( 0.0 );
	#include <logdepthbuf_fragment>
	#include <map_fragment>
	#include <alphamap_fragment>
	#include <alphatest_fragment>
	#include <alphahash_fragment>
	outgoingLight = diffuseColor.rgb;
	#include <opaque_fragment>
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
	#include <fog_fragment>
}`,Gt={alphahash_fragment:Lg,alphahash_pars_fragment:Ng,alphamap_fragment:Dg,alphamap_pars_fragment:Fg,alphatest_fragment:Ug,alphatest_pars_fragment:Og,aomap_fragment:Bg,aomap_pars_fragment:kg,batching_pars_vertex:zg,batching_vertex:Vg,begin_vertex:Gg,beginnormal_vertex:Hg,bsdfs:Wg,iridescence_fragment:Xg,bumpmap_pars_fragment:qg,clipping_planes_fragment:Yg,clipping_planes_pars_fragment:Zg,clipping_planes_pars_vertex:Kg,clipping_planes_vertex:Jg,color_fragment:$g,color_pars_fragment:jg,color_pars_vertex:Qg,color_vertex:t0,common:e0,cube_uv_reflection_fragment:n0,defaultnormal_vertex:i0,displacementmap_pars_vertex:s0,displacementmap_vertex:r0,emissivemap_fragment:a0,emissivemap_pars_fragment:o0,colorspace_fragment:l0,colorspace_pars_fragment:c0,envmap_fragment:h0,envmap_common_pars_fragment:u0,envmap_pars_fragment:f0,envmap_pars_vertex:d0,envmap_physical_pars_fragment:w0,envmap_vertex:p0,fog_vertex:m0,fog_pars_vertex:g0,fog_fragment:_0,fog_pars_fragment:x0,gradientmap_pars_fragment:v0,lightmap_pars_fragment:y0,lights_lambert_fragment:M0,lights_lambert_pars_fragment:b0,lights_pars_begin:S0,lights_toon_fragment:A0,lights_toon_pars_fragment:T0,lights_phong_fragment:E0,lights_phong_pars_fragment:C0,lights_physical_fragment:R0,lights_physical_pars_fragment:P0,lights_fragment_begin:I0,lights_fragment_maps:L0,lights_fragment_end:N0,lightprobes_pars_fragment:D0,logdepthbuf_fragment:F0,logdepthbuf_pars_fragment:U0,logdepthbuf_pars_vertex:O0,logdepthbuf_vertex:B0,map_fragment:k0,map_pars_fragment:z0,map_particle_fragment:V0,map_particle_pars_fragment:G0,metalnessmap_fragment:H0,metalnessmap_pars_fragment:W0,morphinstance_vertex:X0,morphcolor_vertex:q0,morphnormal_vertex:Y0,morphtarget_pars_vertex:Z0,morphtarget_vertex:K0,normal_fragment_begin:J0,normal_fragment_maps:$0,normal_pars_fragment:j0,normal_pars_vertex:Q0,normal_vertex:t_,normalmap_pars_fragment:e_,clearcoat_normal_fragment_begin:n_,clearcoat_normal_fragment_maps:i_,clearcoat_pars_fragment:s_,iridescence_pars_fragment:r_,opaque_fragment:a_,packing:o_,premultiplied_alpha_fragment:l_,project_vertex:c_,dithering_fragment:h_,dithering_pars_fragment:u_,roughnessmap_fragment:f_,roughnessmap_pars_fragment:d_,shadowmap_pars_fragment:p_,shadowmap_pars_vertex:m_,shadowmap_vertex:g_,shadowmask_pars_fragment:__,skinbase_vertex:x_,skinning_pars_vertex:v_,skinning_vertex:y_,skinnormal_vertex:M_,specularmap_fragment:b_,specularmap_pars_fragment:S_,tonemapping_fragment:w_,tonemapping_pars_fragment:A_,transmission_fragment:T_,transmission_pars_fragment:E_,uv_pars_fragment:C_,uv_pars_vertex:R_,uv_vertex:P_,worldpos_vertex:I_,background_vert:L_,background_frag:N_,backgroundCube_vert:D_,backgroundCube_frag:F_,cube_vert:U_,cube_frag:O_,depth_vert:B_,depth_frag:k_,distance_vert:z_,distance_frag:V_,equirect_vert:G_,equirect_frag:H_,linedashed_vert:W_,linedashed_frag:X_,meshbasic_vert:q_,meshbasic_frag:Y_,meshlambert_vert:Z_,meshlambert_frag:K_,meshmatcap_vert:J_,meshmatcap_frag:$_,meshnormal_vert:j_,meshnormal_frag:Q_,meshphong_vert:tx,meshphong_frag:ex,meshphysical_vert:nx,meshphysical_frag:ix,meshtoon_vert:sx,meshtoon_frag:rx,points_vert:ax,points_frag:ox,shadow_vert:lx,shadow_frag:cx,sprite_vert:hx,sprite_frag:ux},ut={common:{diffuse:{value:new dt(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Ft},alphaMap:{value:null},alphaMapTransform:{value:new Ft},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Ft}},envmap:{envMap:{value:null},envMapRotation:{value:new Ft},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98},dfgLUT:{value:null}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Ft}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Ft}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Ft},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Ft},normalScale:{value:new Et(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Ft},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Ft}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Ft}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Ft}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new dt(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null},probesSH:{value:null},probesMin:{value:new P},probesMax:{value:new P},probesResolution:{value:new P}},points:{diffuse:{value:new dt(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Ft},alphaTest:{value:0},uvTransform:{value:new Ft}},sprite:{diffuse:{value:new dt(16777215)},opacity:{value:1},center:{value:new Et(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Ft},alphaMap:{value:null},alphaMapTransform:{value:new Ft},alphaTest:{value:0}}},Yn={basic:{uniforms:Ke([ut.common,ut.specularmap,ut.envmap,ut.aomap,ut.lightmap,ut.fog]),vertexShader:Gt.meshbasic_vert,fragmentShader:Gt.meshbasic_frag},lambert:{uniforms:Ke([ut.common,ut.specularmap,ut.envmap,ut.aomap,ut.lightmap,ut.emissivemap,ut.bumpmap,ut.normalmap,ut.displacementmap,ut.fog,ut.lights,{emissive:{value:new dt(0)},envMapIntensity:{value:1}}]),vertexShader:Gt.meshlambert_vert,fragmentShader:Gt.meshlambert_frag},phong:{uniforms:Ke([ut.common,ut.specularmap,ut.envmap,ut.aomap,ut.lightmap,ut.emissivemap,ut.bumpmap,ut.normalmap,ut.displacementmap,ut.fog,ut.lights,{emissive:{value:new dt(0)},specular:{value:new dt(1118481)},shininess:{value:30},envMapIntensity:{value:1}}]),vertexShader:Gt.meshphong_vert,fragmentShader:Gt.meshphong_frag},standard:{uniforms:Ke([ut.common,ut.envmap,ut.aomap,ut.lightmap,ut.emissivemap,ut.bumpmap,ut.normalmap,ut.displacementmap,ut.roughnessmap,ut.metalnessmap,ut.fog,ut.lights,{emissive:{value:new dt(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:Gt.meshphysical_vert,fragmentShader:Gt.meshphysical_frag},toon:{uniforms:Ke([ut.common,ut.aomap,ut.lightmap,ut.emissivemap,ut.bumpmap,ut.normalmap,ut.displacementmap,ut.gradientmap,ut.fog,ut.lights,{emissive:{value:new dt(0)}}]),vertexShader:Gt.meshtoon_vert,fragmentShader:Gt.meshtoon_frag},matcap:{uniforms:Ke([ut.common,ut.bumpmap,ut.normalmap,ut.displacementmap,ut.fog,{matcap:{value:null}}]),vertexShader:Gt.meshmatcap_vert,fragmentShader:Gt.meshmatcap_frag},points:{uniforms:Ke([ut.points,ut.fog]),vertexShader:Gt.points_vert,fragmentShader:Gt.points_frag},dashed:{uniforms:Ke([ut.common,ut.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:Gt.linedashed_vert,fragmentShader:Gt.linedashed_frag},depth:{uniforms:Ke([ut.common,ut.displacementmap]),vertexShader:Gt.depth_vert,fragmentShader:Gt.depth_frag},normal:{uniforms:Ke([ut.common,ut.bumpmap,ut.normalmap,ut.displacementmap,{opacity:{value:1}}]),vertexShader:Gt.meshnormal_vert,fragmentShader:Gt.meshnormal_frag},sprite:{uniforms:Ke([ut.sprite,ut.fog]),vertexShader:Gt.sprite_vert,fragmentShader:Gt.sprite_frag},background:{uniforms:{uvTransform:{value:new Ft},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:Gt.background_vert,fragmentShader:Gt.background_frag},backgroundCube:{uniforms:{envMap:{value:null},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Ft}},vertexShader:Gt.backgroundCube_vert,fragmentShader:Gt.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:Gt.cube_vert,fragmentShader:Gt.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:Gt.equirect_vert,fragmentShader:Gt.equirect_frag},distance:{uniforms:Ke([ut.common,ut.displacementmap,{referencePosition:{value:new P},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:Gt.distance_vert,fragmentShader:Gt.distance_frag},shadow:{uniforms:Ke([ut.lights,ut.fog,{color:{value:new dt(0)},opacity:{value:1}}]),vertexShader:Gt.shadow_vert,fragmentShader:Gt.shadow_frag}};Yn.physical={uniforms:Ke([Yn.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Ft},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Ft},clearcoatNormalScale:{value:new Et(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Ft},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Ft},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Ft},sheen:{value:0},sheenColor:{value:new dt(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Ft},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Ft},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Ft},transmissionSamplerSize:{value:new Et},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Ft},attenuationDistance:{value:0},attenuationColor:{value:new dt(0)},specularColor:{value:new dt(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Ft},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Ft},anisotropyVector:{value:new Et},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Ft}}]),vertexShader:Gt.meshphysical_vert,fragmentShader:Gt.meshphysical_frag};var ol={r:0,b:0,g:0},fx=new ge,od=new Ft;od.set(-1,0,0,0,1,0,0,0,1);function dx(i,t,e,n,s,r){let a=new dt(0),o=s===!0?0:1,l,c,h=null,f=0,u=null;function d(y){let S=y.isScene===!0?y.background:null;if(S&&S.isTexture){let b=y.backgroundBlurriness>0;S=t.get(S,b)}return S}function m(y){let S=!1,b=d(y);b===null?g(a,o):b&&b.isColor&&(g(b,1),S=!0);let T=i.xr.getEnvironmentBlendMode();T==="additive"?e.buffers.color.setClear(0,0,0,1,r):T==="alpha-blend"&&e.buffers.color.setClear(0,0,0,0,r),(i.autoClear||S)&&(e.buffers.depth.setTest(!0),e.buffers.depth.setMask(!0),e.buffers.color.setMask(!0),i.clear(i.autoClearColor,i.autoClearDepth,i.autoClearStencil))}function _(y,S){let b=d(S);b&&(b.isCubeTexture||b.mapping===Or)?(c===void 0&&(c=new rn(new Os(1,1,1),new re({name:"BackgroundCubeMaterial",uniforms:ls(Yn.backgroundCube.uniforms),vertexShader:Yn.backgroundCube.vertexShader,fragmentShader:Yn.backgroundCube.fragmentShader,side:je,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),c.geometry.deleteAttribute("normal"),c.geometry.deleteAttribute("uv"),c.onBeforeRender=function(T,w,R){this.matrixWorld.copyPosition(R.matrixWorld)},Object.defineProperty(c.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),n.update(c)),c.material.uniforms.envMap.value=b,c.material.uniforms.backgroundBlurriness.value=S.backgroundBlurriness,c.material.uniforms.backgroundIntensity.value=S.backgroundIntensity,c.material.uniforms.backgroundRotation.value.setFromMatrix4(fx.makeRotationFromEuler(S.backgroundRotation)).transpose(),b.isCubeTexture&&b.isRenderTargetTexture===!1&&c.material.uniforms.backgroundRotation.value.premultiply(od),c.material.toneMapped=Wt.getTransfer(b.colorSpace)!==jt,(h!==b||f!==b.version||u!==i.toneMapping)&&(c.material.needsUpdate=!0,h=b,f=b.version,u=i.toneMapping),c.layers.enableAll(),y.unshift(c,c.geometry,c.material,0,0,null)):b&&b.isTexture&&(l===void 0&&(l=new rn(new wr(2,2),new re({name:"BackgroundMaterial",uniforms:ls(Yn.background.uniforms),vertexShader:Yn.background.vertexShader,fragmentShader:Yn.background.fragmentShader,side:ai,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),l.geometry.deleteAttribute("normal"),Object.defineProperty(l.material,"map",{get:function(){return this.uniforms.t2D.value}}),n.update(l)),l.material.uniforms.t2D.value=b,l.material.uniforms.backgroundIntensity.value=S.backgroundIntensity,l.material.toneMapped=Wt.getTransfer(b.colorSpace)!==jt,b.matrixAutoUpdate===!0&&b.updateMatrix(),l.material.uniforms.uvTransform.value.copy(b.matrix),(h!==b||f!==b.version||u!==i.toneMapping)&&(l.material.needsUpdate=!0,h=b,f=b.version,u=i.toneMapping),l.layers.enableAll(),y.unshift(l,l.geometry,l.material,0,0,null))}function g(y,S){y.getRGB(ol,Qc(i)),e.buffers.color.setClear(ol.r,ol.g,ol.b,S,r)}function p(){c!==void 0&&(c.geometry.dispose(),c.material.dispose(),c=void 0),l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0)}return{getClearColor:function(){return a},setClearColor:function(y,S=1){a.set(y),o=S,g(a,o)},getClearAlpha:function(){return o},setClearAlpha:function(y){o=y,g(a,o)},render:m,addToRenderList:_,dispose:p}}function px(i,t){let e=i.getParameter(i.MAX_VERTEX_ATTRIBS),n={},s=u(null),r=s,a=!1;function o(C,D,H,W,U){let z=!1,V=f(C,W,H,D);r!==V&&(r=V,c(r.object)),z=d(C,W,H,U),z&&m(C,W,H,U),U!==null&&t.update(U,i.ELEMENT_ARRAY_BUFFER),(z||a)&&(a=!1,b(C,D,H,W),U!==null&&i.bindBuffer(i.ELEMENT_ARRAY_BUFFER,t.get(U).buffer))}function l(){return i.createVertexArray()}function c(C){return i.bindVertexArray(C)}function h(C){return i.deleteVertexArray(C)}function f(C,D,H,W){let U=W.wireframe===!0,z=n[D.id];z===void 0&&(z={},n[D.id]=z);let V=C.isInstancedMesh===!0?C.id:0,$=z[V];$===void 0&&($={},z[V]=$);let tt=$[H.id];tt===void 0&&(tt={},$[H.id]=tt);let ct=tt[U];return ct===void 0&&(ct=u(l()),tt[U]=ct),ct}function u(C){let D=[],H=[],W=[];for(let U=0;U<e;U++)D[U]=0,H[U]=0,W[U]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:D,enabledAttributes:H,attributeDivisors:W,object:C,attributes:{},index:null}}function d(C,D,H,W){let U=r.attributes,z=D.attributes,V=0,$=H.getAttributes();for(let tt in $)if($[tt].location>=0){let Mt=U[tt],St=z[tt];if(St===void 0&&(tt==="instanceMatrix"&&C.instanceMatrix&&(St=C.instanceMatrix),tt==="instanceColor"&&C.instanceColor&&(St=C.instanceColor)),Mt===void 0||Mt.attribute!==St||St&&Mt.data!==St.data)return!0;V++}return r.attributesNum!==V||r.index!==W}function m(C,D,H,W){let U={},z=D.attributes,V=0,$=H.getAttributes();for(let tt in $)if($[tt].location>=0){let Mt=z[tt];Mt===void 0&&(tt==="instanceMatrix"&&C.instanceMatrix&&(Mt=C.instanceMatrix),tt==="instanceColor"&&C.instanceColor&&(Mt=C.instanceColor));let St={};St.attribute=Mt,Mt&&Mt.data&&(St.data=Mt.data),U[tt]=St,V++}r.attributes=U,r.attributesNum=V,r.index=W}function _(){let C=r.newAttributes;for(let D=0,H=C.length;D<H;D++)C[D]=0}function g(C){p(C,0)}function p(C,D){let H=r.newAttributes,W=r.enabledAttributes,U=r.attributeDivisors;H[C]=1,W[C]===0&&(i.enableVertexAttribArray(C),W[C]=1),U[C]!==D&&(i.vertexAttribDivisor(C,D),U[C]=D)}function y(){let C=r.newAttributes,D=r.enabledAttributes;for(let H=0,W=D.length;H<W;H++)D[H]!==C[H]&&(i.disableVertexAttribArray(H),D[H]=0)}function S(C,D,H,W,U,z,V){V===!0?i.vertexAttribIPointer(C,D,H,U,z):i.vertexAttribPointer(C,D,H,W,U,z)}function b(C,D,H,W){_();let U=W.attributes,z=H.getAttributes(),V=D.defaultAttributeValues;for(let $ in z){let tt=z[$];if(tt.location>=0){let ct=U[$];if(ct===void 0&&($==="instanceMatrix"&&C.instanceMatrix&&(ct=C.instanceMatrix),$==="instanceColor"&&C.instanceColor&&(ct=C.instanceColor)),ct!==void 0){let Mt=ct.normalized,St=ct.itemSize,qt=t.get(ct);if(qt===void 0)continue;let ee=qt.buffer,kt=qt.type,J=qt.bytesPerElement,mt=kt===i.INT||kt===i.UNSIGNED_INT||ct.gpuType===So;if(ct.isInterleavedBufferAttribute){let st=ct.data,Rt=st.stride,Ut=ct.offset;if(st.isInstancedInterleavedBuffer){for(let It=0;It<tt.locationSize;It++)p(tt.location+It,st.meshPerAttribute);C.isInstancedMesh!==!0&&W._maxInstanceCount===void 0&&(W._maxInstanceCount=st.meshPerAttribute*st.count)}else for(let It=0;It<tt.locationSize;It++)g(tt.location+It);i.bindBuffer(i.ARRAY_BUFFER,ee);for(let It=0;It<tt.locationSize;It++)S(tt.location+It,St/tt.locationSize,kt,Mt,Rt*J,(Ut+St/tt.locationSize*It)*J,mt)}else{if(ct.isInstancedBufferAttribute){for(let st=0;st<tt.locationSize;st++)p(tt.location+st,ct.meshPerAttribute);C.isInstancedMesh!==!0&&W._maxInstanceCount===void 0&&(W._maxInstanceCount=ct.meshPerAttribute*ct.count)}else for(let st=0;st<tt.locationSize;st++)g(tt.location+st);i.bindBuffer(i.ARRAY_BUFFER,ee);for(let st=0;st<tt.locationSize;st++)S(tt.location+st,St/tt.locationSize,kt,Mt,St*J,St/tt.locationSize*st*J,mt)}}else if(V!==void 0){let Mt=V[$];if(Mt!==void 0)switch(Mt.length){case 2:i.vertexAttrib2fv(tt.location,Mt);break;case 3:i.vertexAttrib3fv(tt.location,Mt);break;case 4:i.vertexAttrib4fv(tt.location,Mt);break;default:i.vertexAttrib1fv(tt.location,Mt)}}}}y()}function T(){E();for(let C in n){let D=n[C];for(let H in D){let W=D[H];for(let U in W){let z=W[U];for(let V in z)h(z[V].object),delete z[V];delete W[U]}}delete n[C]}}function w(C){if(n[C.id]===void 0)return;let D=n[C.id];for(let H in D){let W=D[H];for(let U in W){let z=W[U];for(let V in z)h(z[V].object),delete z[V];delete W[U]}}delete n[C.id]}function R(C){for(let D in n){let H=n[D];for(let W in H){let U=H[W];if(U[C.id]===void 0)continue;let z=U[C.id];for(let V in z)h(z[V].object),delete z[V];delete U[C.id]}}}function v(C){for(let D in n){let H=n[D],W=C.isInstancedMesh===!0?C.id:0,U=H[W];if(U!==void 0){for(let z in U){let V=U[z];for(let $ in V)h(V[$].object),delete V[$];delete U[z]}delete H[W],Object.keys(H).length===0&&delete n[D]}}}function E(){L(),a=!0,r!==s&&(r=s,c(r.object))}function L(){s.geometry=null,s.program=null,s.wireframe=!1}return{setup:o,reset:E,resetDefaultState:L,dispose:T,releaseStatesOfGeometry:w,releaseStatesOfObject:v,releaseStatesOfProgram:R,initAttributes:_,enableAttribute:g,disableUnusedAttributes:y}}function mx(i,t,e){let n;function s(l){n=l}function r(l,c){i.drawArrays(n,l,c),e.update(c,n,1)}function a(l,c,h){h!==0&&(i.drawArraysInstanced(n,l,c,h),e.update(c,n,h))}function o(l,c,h){if(h===0)return;t.get("WEBGL_multi_draw").multiDrawArraysWEBGL(n,l,0,c,0,h);let u=0;for(let d=0;d<h;d++)u+=c[d];e.update(u,n,1)}this.setMode=s,this.render=r,this.renderInstances=a,this.renderMultiDraw=o}function gx(i,t,e,n){let s;function r(){if(s!==void 0)return s;if(t.has("EXT_texture_filter_anisotropic")===!0){let R=t.get("EXT_texture_filter_anisotropic");s=i.getParameter(R.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else s=0;return s}function a(R){return!(R!==An&&n.convert(R)!==i.getParameter(i.IMPLEMENTATION_COLOR_READ_FORMAT))}function o(R){let v=R===Ze&&(t.has("EXT_color_buffer_half_float")||t.has("EXT_color_buffer_float"));return!(R!==vn&&n.convert(R)!==i.getParameter(i.IMPLEMENTATION_COLOR_READ_TYPE)&&R!==Un&&!v)}function l(R){if(R==="highp"){if(i.getShaderPrecisionFormat(i.VERTEX_SHADER,i.HIGH_FLOAT).precision>0&&i.getShaderPrecisionFormat(i.FRAGMENT_SHADER,i.HIGH_FLOAT).precision>0)return"highp";R="mediump"}return R==="mediump"&&i.getShaderPrecisionFormat(i.VERTEX_SHADER,i.MEDIUM_FLOAT).precision>0&&i.getShaderPrecisionFormat(i.FRAGMENT_SHADER,i.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let c=e.precision!==void 0?e.precision:"highp",h=l(c);h!==c&&(Ct("WebGLRenderer:",c,"not supported, using",h,"instead."),c=h);let f=e.logarithmicDepthBuffer===!0,u=e.reversedDepthBuffer===!0&&t.has("EXT_clip_control");e.reversedDepthBuffer===!0&&u===!1&&Ct("WebGLRenderer: Unable to use reversed depth buffer due to missing EXT_clip_control extension. Fallback to default depth buffer.");let d=i.getParameter(i.MAX_TEXTURE_IMAGE_UNITS),m=i.getParameter(i.MAX_VERTEX_TEXTURE_IMAGE_UNITS),_=i.getParameter(i.MAX_TEXTURE_SIZE),g=i.getParameter(i.MAX_CUBE_MAP_TEXTURE_SIZE),p=i.getParameter(i.MAX_VERTEX_ATTRIBS),y=i.getParameter(i.MAX_VERTEX_UNIFORM_VECTORS),S=i.getParameter(i.MAX_VARYING_VECTORS),b=i.getParameter(i.MAX_FRAGMENT_UNIFORM_VECTORS),T=i.getParameter(i.MAX_SAMPLES),w=i.getParameter(i.SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:r,getMaxPrecision:l,textureFormatReadable:a,textureTypeReadable:o,precision:c,logarithmicDepthBuffer:f,reversedDepthBuffer:u,maxTextures:d,maxVertexTextures:m,maxTextureSize:_,maxCubemapSize:g,maxAttributes:p,maxVertexUniforms:y,maxVaryings:S,maxFragmentUniforms:b,maxSamples:T,samples:w}}function _x(i){let t=this,e=null,n=0,s=!1,r=!1,a=new Sn,o=new Ft,l={value:null,needsUpdate:!1};this.uniform=l,this.numPlanes=0,this.numIntersection=0,this.init=function(f,u){let d=f.length!==0||u||n!==0||s;return s=u,n=f.length,d},this.beginShadows=function(){r=!0,h(null)},this.endShadows=function(){r=!1},this.setGlobalState=function(f,u){e=h(f,u,0)},this.setState=function(f,u,d){let m=f.clippingPlanes,_=f.clipIntersection,g=f.clipShadows,p=i.get(f);if(!s||m===null||m.length===0||r&&!g)r?h(null):c();else{let y=r?0:n,S=y*4,b=p.clippingState||null;l.value=b,b=h(m,u,S,d);for(let T=0;T!==S;++T)b[T]=e[T];p.clippingState=b,this.numIntersection=_?this.numPlanes:0,this.numPlanes+=y}};function c(){l.value!==e&&(l.value=e,l.needsUpdate=n>0),t.numPlanes=n,t.numIntersection=0}function h(f,u,d,m){let _=f!==null?f.length:0,g=null;if(_!==0){if(g=l.value,m!==!0||g===null){let p=d+_*4,y=u.matrixWorldInverse;o.getNormalMatrix(y),(g===null||g.length<p)&&(g=new Float32Array(p));for(let S=0,b=d;S!==_;++S,b+=4)a.copy(f[S]).applyMatrix4(y,o),a.normal.toArray(g,b),g[b+3]=a.constant}l.value=g,l.needsUpdate=!0}return t.numPlanes=_,t.numIntersection=0,g}}var zi=4,Bf=[.125,.215,.35,.446,.526,.582],cs=20,xx=256,Xr=new as,kf=new dt,lh=null,ch=0,hh=0,uh=!1,vx=new P,cl=class{constructor(t){this._renderer=t,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._sizeLods=[],this._sigmas=[],this._lodMeshes=[],this._backgroundBox=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._blurMaterial=null,this._ggxMaterial=null}fromScene(t,e=0,n=.1,s=100,r={}){let{size:a=256,position:o=vx}=r;lh=this._renderer.getRenderTarget(),ch=this._renderer.getActiveCubeFace(),hh=this._renderer.getActiveMipmapLevel(),uh=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(a);let l=this._allocateTargets();return l.depthBuffer=!0,this._sceneToCubeUV(t,n,s,l,o),e>0&&this._blur(l,0,0,e),this._applyPMREM(l),this._cleanup(l),l}fromEquirectangular(t,e=null){return this._fromTexture(t,e)}fromCubemap(t,e=null){return this._fromTexture(t,e)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=Gf(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=Vf(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose(),this._backgroundBox!==null&&(this._backgroundBox.geometry.dispose(),this._backgroundBox.material.dispose())}_setSize(t){this._lodMax=Math.floor(Math.log2(t)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._ggxMaterial!==null&&this._ggxMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let t=0;t<this._lodMeshes.length;t++)this._lodMeshes[t].geometry.dispose()}_cleanup(t){this._renderer.setRenderTarget(lh,ch,hh),this._renderer.xr.enabled=uh,t.scissorTest=!1,Hs(t,0,0,t.width,t.height)}_fromTexture(t,e){t.mapping===Fi||t.mapping===os?this._setSize(t.image.length===0?16:t.image[0].width||t.image[0].image.width):this._setSize(t.image.width/4),lh=this._renderer.getRenderTarget(),ch=this._renderer.getActiveCubeFace(),hh=this._renderer.getActiveMipmapLevel(),uh=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;let n=e||this._allocateTargets();return this._textureToCubeUV(t,n),this._applyPMREM(n),this._cleanup(n),n}_allocateTargets(){let t=3*Math.max(this._cubeSize,112),e=4*this._cubeSize,n={magFilter:Ge,minFilter:Ge,generateMipmaps:!1,type:Ze,format:An,colorSpace:ur,depthBuffer:!1},s=zf(t,e,n);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==t||this._pingPongRenderTarget.height!==e){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=zf(t,e,n);let{_lodMax:r}=this;({lodMeshes:this._lodMeshes,sizeLods:this._sizeLods,sigmas:this._sigmas}=yx(r)),this._blurMaterial=bx(r,t,e),this._ggxMaterial=Mx(r,t,e)}return s}_compileMaterial(t){let e=new rn(new te,t);this._renderer.compile(e,Xr)}_sceneToCubeUV(t,e,n,s,r){let l=new Ye(90,1,e,n),c=[1,-1,1,1,1,1],h=[1,1,1,-1,-1,-1],f=this._renderer,u=f.autoClear,d=f.toneMapping;f.getClearColor(kf),f.toneMapping=xn,f.autoClear=!1,f.state.buffers.depth.getReversed()&&(f.setRenderTarget(s),f.clearDepth(),f.setRenderTarget(null)),this._backgroundBox===null&&(this._backgroundBox=new rn(new Os,new ss({name:"PMREM.Background",side:je,depthWrite:!1,depthTest:!1})));let _=this._backgroundBox,g=_.material,p=!1,y=t.background;y?y.isColor&&(g.color.copy(y),t.background=null,p=!0):(g.color.copy(kf),p=!0);for(let S=0;S<6;S++){let b=S%3;b===0?(l.up.set(0,c[S],0),l.position.set(r.x,r.y,r.z),l.lookAt(r.x+h[S],r.y,r.z)):b===1?(l.up.set(0,0,c[S]),l.position.set(r.x,r.y,r.z),l.lookAt(r.x,r.y+h[S],r.z)):(l.up.set(0,c[S],0),l.position.set(r.x,r.y,r.z),l.lookAt(r.x,r.y,r.z+h[S]));let T=this._cubeSize;Hs(s,b*T,S>2?T:0,T,T),f.setRenderTarget(s),p&&f.render(_,l),f.render(t,l)}f.toneMapping=d,f.autoClear=u,t.background=y}_textureToCubeUV(t,e){let n=this._renderer,s=t.mapping===Fi||t.mapping===os;s?(this._cubemapMaterial===null&&(this._cubemapMaterial=Gf()),this._cubemapMaterial.uniforms.flipEnvMap.value=t.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=Vf());let r=s?this._cubemapMaterial:this._equirectMaterial,a=this._lodMeshes[0];a.material=r;let o=r.uniforms;o.envMap.value=t;let l=this._cubeSize;Hs(e,0,0,3*l,2*l),n.setRenderTarget(e),n.render(a,Xr)}_applyPMREM(t){let e=this._renderer,n=e.autoClear;e.autoClear=!1;let s=this._lodMeshes.length;for(let r=1;r<s;r++)this._applyGGXFilter(t,r-1,r);e.autoClear=n}_applyGGXFilter(t,e,n){let s=this._renderer,r=this._pingPongRenderTarget,a=this._ggxMaterial,o=this._lodMeshes[n];o.material=a;let l=a.uniforms,c=n/(this._lodMeshes.length-1),h=e/(this._lodMeshes.length-1),f=Math.sqrt(c*c-h*h),u=0+c*1.25,d=f*u,{_lodMax:m}=this,_=this._sizeLods[n],g=3*_*(n>m-zi?n-m+zi:0),p=4*(this._cubeSize-_);l.envMap.value=t.texture,l.roughness.value=d,l.mipInt.value=m-e,Hs(r,g,p,3*_,2*_),s.setRenderTarget(r),s.render(o,Xr),l.envMap.value=r.texture,l.roughness.value=0,l.mipInt.value=m-n,Hs(t,g,p,3*_,2*_),s.setRenderTarget(t),s.render(o,Xr)}_blur(t,e,n,s,r){let a=this._pingPongRenderTarget;this._halfBlur(t,a,e,n,s,"latitudinal",r),this._halfBlur(a,t,n,n,s,"longitudinal",r)}_halfBlur(t,e,n,s,r,a,o){let l=this._renderer,c=this._blurMaterial;a!=="latitudinal"&&a!=="longitudinal"&&Pt("blur direction must be either latitudinal or longitudinal!");let h=3,f=this._lodMeshes[s];f.material=c;let u=c.uniforms,d=this._sizeLods[n]-1,m=isFinite(r)?Math.PI/(2*d):2*Math.PI/(2*cs-1),_=r/m,g=isFinite(r)?1+Math.floor(h*_):cs;g>cs&&Ct(`sigmaRadians, ${r}, is too large and will clip, as it requested ${g} samples when the maximum is set to ${cs}`);let p=[],y=0;for(let R=0;R<cs;++R){let v=R/_,E=Math.exp(-v*v/2);p.push(E),R===0?y+=E:R<g&&(y+=2*E)}for(let R=0;R<p.length;R++)p[R]=p[R]/y;u.envMap.value=t.texture,u.samples.value=g,u.weights.value=p,u.latitudinal.value=a==="latitudinal",o&&(u.poleAxis.value=o);let{_lodMax:S}=this;u.dTheta.value=m,u.mipInt.value=S-n;let b=this._sizeLods[s],T=3*b*(s>S-zi?s-S+zi:0),w=4*(this._cubeSize-b);Hs(e,T,w,3*b,2*b),l.setRenderTarget(e),l.render(f,Xr)}};function yx(i){let t=[],e=[],n=[],s=i,r=i-zi+1+Bf.length;for(let a=0;a<r;a++){let o=Math.pow(2,s);t.push(o);let l=1/o;a>i-zi?l=Bf[a-i+zi-1]:a===0&&(l=0),e.push(l);let c=1/(o-2),h=-c,f=1+c,u=[h,h,f,h,f,f,h,h,f,f,h,f],d=6,m=6,_=3,g=2,p=1,y=new Float32Array(_*m*d),S=new Float32Array(g*m*d),b=new Float32Array(p*m*d);for(let w=0;w<d;w++){let R=w%3*2/3-1,v=w>2?0:-1,E=[R,v,0,R+2/3,v,0,R+2/3,v+1,0,R,v,0,R+2/3,v+1,0,R,v+1,0];y.set(E,_*m*w),S.set(u,g*m*w);let L=[w,w,w,w,w,w];b.set(L,p*m*w)}let T=new te;T.setAttribute("position",new Lt(y,_)),T.setAttribute("uv",new Lt(S,g)),T.setAttribute("faceIndex",new Lt(b,p)),n.push(new rn(T,null)),s>zi&&s--}return{lodMeshes:n,sizeLods:t,sigmas:e}}function zf(i,t,e){let n=new Ne(i,t,e);return n.texture.mapping=Or,n.texture.name="PMREM.cubeUv",n.scissorTest=!0,n}function Hs(i,t,e,n,s){i.viewport.set(t,e,n,s),i.scissor.set(t,e,n,s)}function Mx(i,t,e){return new re({name:"PMREMGGXConvolution",defines:{GGX_SAMPLES:xx,CUBEUV_TEXEL_WIDTH:1/t,CUBEUV_TEXEL_HEIGHT:1/e,CUBEUV_MAX_MIP:`${i}.0`},uniforms:{envMap:{value:null},roughness:{value:0},mipInt:{value:0}},vertexShader:fl(),fragmentShader:`

			precision highp float;
			precision highp int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform float roughness;
			uniform float mipInt;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			#define PI 3.14159265359

			// Van der Corput radical inverse
			float radicalInverse_VdC(uint bits) {
				bits = (bits << 16u) | (bits >> 16u);
				bits = ((bits & 0x55555555u) << 1u) | ((bits & 0xAAAAAAAAu) >> 1u);
				bits = ((bits & 0x33333333u) << 2u) | ((bits & 0xCCCCCCCCu) >> 2u);
				bits = ((bits & 0x0F0F0F0Fu) << 4u) | ((bits & 0xF0F0F0F0u) >> 4u);
				bits = ((bits & 0x00FF00FFu) << 8u) | ((bits & 0xFF00FF00u) >> 8u);
				return float(bits) * 2.3283064365386963e-10; // / 0x100000000
			}

			// Hammersley sequence
			vec2 hammersley(uint i, uint N) {
				return vec2(float(i) / float(N), radicalInverse_VdC(i));
			}

			// GGX VNDF importance sampling (Eric Heitz 2018)
			// "Sampling the GGX Distribution of Visible Normals"
			// https://jcgt.org/published/0007/04/01/
			vec3 importanceSampleGGX_VNDF(vec2 Xi, vec3 V, float roughness) {
				float alpha = roughness * roughness;

				// Section 4.1: Orthonormal basis
				vec3 T1 = vec3(1.0, 0.0, 0.0);
				vec3 T2 = cross(V, T1);

				// Section 4.2: Parameterization of projected area
				float r = sqrt(Xi.x);
				float phi = 2.0 * PI * Xi.y;
				float t1 = r * cos(phi);
				float t2 = r * sin(phi);
				float s = 0.5 * (1.0 + V.z);
				t2 = (1.0 - s) * sqrt(1.0 - t1 * t1) + s * t2;

				// Section 4.3: Reprojection onto hemisphere
				vec3 Nh = t1 * T1 + t2 * T2 + sqrt(max(0.0, 1.0 - t1 * t1 - t2 * t2)) * V;

				// Section 3.4: Transform back to ellipsoid configuration
				return normalize(vec3(alpha * Nh.x, alpha * Nh.y, max(0.0, Nh.z)));
			}

			void main() {
				vec3 N = normalize(vOutputDirection);
				vec3 V = N; // Assume view direction equals normal for pre-filtering

				vec3 prefilteredColor = vec3(0.0);
				float totalWeight = 0.0;

				// For very low roughness, just sample the environment directly
				if (roughness < 0.001) {
					gl_FragColor = vec4(bilinearCubeUV(envMap, N, mipInt), 1.0);
					return;
				}

				// Tangent space basis for VNDF sampling
				vec3 up = abs(N.z) < 0.999 ? vec3(0.0, 0.0, 1.0) : vec3(1.0, 0.0, 0.0);
				vec3 tangent = normalize(cross(up, N));
				vec3 bitangent = cross(N, tangent);

				for(uint i = 0u; i < uint(GGX_SAMPLES); i++) {
					vec2 Xi = hammersley(i, uint(GGX_SAMPLES));

					// For PMREM, V = N, so in tangent space V is always (0, 0, 1)
					vec3 H_tangent = importanceSampleGGX_VNDF(Xi, vec3(0.0, 0.0, 1.0), roughness);

					// Transform H back to world space
					vec3 H = normalize(tangent * H_tangent.x + bitangent * H_tangent.y + N * H_tangent.z);
					vec3 L = normalize(2.0 * dot(V, H) * H - V);

					float NdotL = max(dot(N, L), 0.0);

					if(NdotL > 0.0) {
						// Sample environment at fixed mip level
						// VNDF importance sampling handles the distribution filtering
						vec3 sampleColor = bilinearCubeUV(envMap, L, mipInt);

						// Weight by NdotL for the split-sum approximation
						// VNDF PDF naturally accounts for the visible microfacet distribution
						prefilteredColor += sampleColor * NdotL;
						totalWeight += NdotL;
					}
				}

				if (totalWeight > 0.0) {
					prefilteredColor = prefilteredColor / totalWeight;
				}

				gl_FragColor = vec4(prefilteredColor, 1.0);
			}
		`,blending:wn,depthTest:!1,depthWrite:!1})}function bx(i,t,e){let n=new Float32Array(cs),s=new P(0,1,0);return new re({name:"SphericalGaussianBlur",defines:{n:cs,CUBEUV_TEXEL_WIDTH:1/t,CUBEUV_TEXEL_HEIGHT:1/e,CUBEUV_MAX_MIP:`${i}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:n},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:s}},vertexShader:fl(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;
			uniform int samples;
			uniform float weights[ n ];
			uniform bool latitudinal;
			uniform float dTheta;
			uniform float mipInt;
			uniform vec3 poleAxis;

			#define ENVMAP_TYPE_CUBE_UV
			#include <cube_uv_reflection_fragment>

			vec3 getSample( float theta, vec3 axis ) {

				float cosTheta = cos( theta );
				// Rodrigues' axis-angle rotation
				vec3 sampleDirection = vOutputDirection * cosTheta
					+ cross( axis, vOutputDirection ) * sin( theta )
					+ axis * dot( axis, vOutputDirection ) * ( 1.0 - cosTheta );

				return bilinearCubeUV( envMap, sampleDirection, mipInt );

			}

			void main() {

				vec3 axis = latitudinal ? poleAxis : cross( poleAxis, vOutputDirection );

				if ( all( equal( axis, vec3( 0.0 ) ) ) ) {

					axis = vec3( vOutputDirection.z, 0.0, - vOutputDirection.x );

				}

				axis = normalize( axis );

				gl_FragColor = vec4( 0.0, 0.0, 0.0, 1.0 );
				gl_FragColor.rgb += weights[ 0 ] * getSample( 0.0, axis );

				for ( int i = 1; i < n; i++ ) {

					if ( i >= samples ) {

						break;

					}

					float theta = dTheta * float( i );
					gl_FragColor.rgb += weights[ i ] * getSample( -1.0 * theta, axis );
					gl_FragColor.rgb += weights[ i ] * getSample( theta, axis );

				}

			}
		`,blending:wn,depthTest:!1,depthWrite:!1})}function Vf(){return new re({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:fl(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			varying vec3 vOutputDirection;

			uniform sampler2D envMap;

			#include <common>

			void main() {

				vec3 outputDirection = normalize( vOutputDirection );
				vec2 uv = equirectUv( outputDirection );

				gl_FragColor = vec4( texture2D ( envMap, uv ).rgb, 1.0 );

			}
		`,blending:wn,depthTest:!1,depthWrite:!1})}function Gf(){return new re({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:fl(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:wn,depthTest:!1,depthWrite:!1})}function fl(){return`

		precision mediump float;
		precision mediump int;

		attribute float faceIndex;

		varying vec3 vOutputDirection;

		// RH coordinate system; PMREM face-indexing convention
		vec3 getDirection( vec2 uv, float face ) {

			uv = 2.0 * uv - 1.0;

			vec3 direction = vec3( uv, 1.0 );

			if ( face == 0.0 ) {

				direction = direction.zyx; // ( 1, v, u ) pos x

			} else if ( face == 1.0 ) {

				direction = direction.xzy;
				direction.xz *= -1.0; // ( -u, 1, -v ) pos y

			} else if ( face == 2.0 ) {

				direction.x *= -1.0; // ( -u, v, 1 ) pos z

			} else if ( face == 3.0 ) {

				direction = direction.zyx;
				direction.xz *= -1.0; // ( -1, v, -u ) neg x

			} else if ( face == 4.0 ) {

				direction = direction.xzy;
				direction.xy *= -1.0; // ( -u, -1, v ) neg y

			} else if ( face == 5.0 ) {

				direction.z *= -1.0; // ( u, v, -1 ) neg z

			}

			return direction;

		}

		void main() {

			vOutputDirection = getDirection( uv, faceIndex );
			gl_Position = vec4( position, 1.0 );

		}
	`}var hl=class extends Ne{constructor(t=1,e={}){super(t,t,e),this.isWebGLCubeRenderTarget=!0;let n={width:t,height:t,depth:1},s=[n,n,n,n,n,n];this.texture=new Mr(s),this._setTextureOptions(e),this.texture.isRenderTargetTexture=!0}fromEquirectangularTexture(t,e){this.texture.type=e.type,this.texture.colorSpace=e.colorSpace,this.texture.generateMipmaps=e.generateMipmaps,this.texture.minFilter=e.minFilter,this.texture.magFilter=e.magFilter;let n={uniforms:{tEquirect:{value:null}},vertexShader:`

				varying vec3 vWorldDirection;

				vec3 transformDirection( in vec3 dir, in mat4 matrix ) {

					return normalize( ( matrix * vec4( dir, 0.0 ) ).xyz );

				}

				void main() {

					vWorldDirection = transformDirection( position, modelMatrix );

					#include <begin_vertex>
					#include <project_vertex>

				}
			`,fragmentShader:`

				uniform sampler2D tEquirect;

				varying vec3 vWorldDirection;

				#include <common>

				void main() {

					vec3 direction = normalize( vWorldDirection );

					vec2 sampleUV = equirectUv( direction );

					gl_FragColor = texture2D( tEquirect, sampleUV );

				}
			`},s=new Os(5,5,5),r=new re({name:"CubemapFromEquirect",uniforms:ls(n.uniforms),vertexShader:n.vertexShader,fragmentShader:n.fragmentShader,side:je,blending:wn});r.uniforms.tEquirect.value=e;let a=new rn(s,r),o=e.minFilter;return e.minFilter===Ui&&(e.minFilter=Ge),new go(1,10,this).update(t,a),e.minFilter=o,a.geometry.dispose(),a.material.dispose(),this}clear(t,e=!0,n=!0,s=!0){let r=t.getRenderTarget();for(let a=0;a<6;a++)t.setRenderTarget(this,a),t.clear(e,n,s);t.setRenderTarget(r)}};function Sx(i){let t=new WeakMap,e=new WeakMap,n=null;function s(u,d=!1){return u==null?null:d?a(u):r(u)}function r(u){if(u&&u.isTexture){let d=u.mapping;if(d===yo||d===Mo)if(t.has(u)){let m=t.get(u).texture;return o(m,u.mapping)}else{let m=u.image;if(m&&m.height>0){let _=new hl(m.height);return _.fromEquirectangularTexture(i,u),t.set(u,_),u.addEventListener("dispose",c),o(_.texture,u.mapping)}else return null}}return u}function a(u){if(u&&u.isTexture){let d=u.mapping,m=d===yo||d===Mo,_=d===Fi||d===os;if(m||_){let g=e.get(u),p=g!==void 0?g.texture.pmremVersion:0;if(u.isRenderTargetTexture&&u.pmremVersion!==p)return n===null&&(n=new cl(i)),g=m?n.fromEquirectangular(u,g):n.fromCubemap(u,g),g.texture.pmremVersion=u.pmremVersion,e.set(u,g),g.texture;if(g!==void 0)return g.texture;{let y=u.image;return m&&y&&y.height>0||_&&y&&l(y)?(n===null&&(n=new cl(i)),g=m?n.fromEquirectangular(u):n.fromCubemap(u),g.texture.pmremVersion=u.pmremVersion,e.set(u,g),u.addEventListener("dispose",h),g.texture):null}}}return u}function o(u,d){return d===yo?u.mapping=Fi:d===Mo&&(u.mapping=os),u}function l(u){let d=0,m=6;for(let _=0;_<m;_++)u[_]!==void 0&&d++;return d===m}function c(u){let d=u.target;d.removeEventListener("dispose",c);let m=t.get(d);m!==void 0&&(t.delete(d),m.dispose())}function h(u){let d=u.target;d.removeEventListener("dispose",h);let m=e.get(d);m!==void 0&&(e.delete(d),m.dispose())}function f(){t=new WeakMap,e=new WeakMap,n!==null&&(n.dispose(),n=null)}return{get:s,dispose:f}}function wx(i){let t={};function e(n){if(t[n]!==void 0)return t[n];let s=i.getExtension(n);return t[n]=s,s}return{has:function(n){return e(n)!==null},init:function(){e("EXT_color_buffer_float"),e("WEBGL_clip_cull_distance"),e("OES_texture_float_linear"),e("EXT_color_buffer_half_float"),e("WEBGL_multisampled_render_to_texture"),e("WEBGL_render_shared_exponent")},get:function(n){let s=e(n);return s===null&&Ya("WebGLRenderer: "+n+" extension not supported."),s}}}function Ax(i,t,e,n){let s={},r=new WeakMap;function a(f){let u=f.target;u.index!==null&&t.remove(u.index);for(let m in u.attributes)t.remove(u.attributes[m]);u.removeEventListener("dispose",a),delete s[u.id];let d=r.get(u);d&&(t.remove(d),r.delete(u)),n.releaseStatesOfGeometry(u),u.isInstancedBufferGeometry===!0&&delete u._maxInstanceCount,e.memory.geometries--}function o(f,u){return s[u.id]===!0||(u.addEventListener("dispose",a),s[u.id]=!0,e.memory.geometries++),u}function l(f){let u=f.attributes;for(let d in u)t.update(u[d],i.ARRAY_BUFFER)}function c(f){let u=[],d=f.index,m=f.attributes.position,_=0;if(m===void 0)return;if(d!==null){let y=d.array;_=d.version;for(let S=0,b=y.length;S<b;S+=3){let T=y[S+0],w=y[S+1],R=y[S+2];u.push(T,w,w,R,R,T)}}else{let y=m.array;_=m.version;for(let S=0,b=y.length/3-1;S<b;S+=3){let T=S+0,w=S+1,R=S+2;u.push(T,w,w,R,R,T)}}let g=new(m.count>=65535?vr:xr)(u,1);g.version=_;let p=r.get(f);p&&t.remove(p),r.set(f,g)}function h(f){let u=r.get(f);if(u){let d=f.index;d!==null&&u.version<d.version&&c(f)}else c(f);return r.get(f)}return{get:o,update:l,getWireframeAttribute:h}}function Tx(i,t,e){let n;function s(f){n=f}let r,a;function o(f){r=f.type,a=f.bytesPerElement}function l(f,u){i.drawElements(n,u,r,f*a),e.update(u,n,1)}function c(f,u,d){d!==0&&(i.drawElementsInstanced(n,u,r,f*a,d),e.update(u,n,d))}function h(f,u,d){if(d===0)return;t.get("WEBGL_multi_draw").multiDrawElementsWEBGL(n,u,0,r,f,0,d);let _=0;for(let g=0;g<d;g++)_+=u[g];e.update(_,n,1)}this.setMode=s,this.setIndex=o,this.render=l,this.renderInstances=c,this.renderMultiDraw=h}function Ex(i){let t={geometries:0,textures:0},e={frame:0,calls:0,triangles:0,points:0,lines:0};function n(r,a,o){switch(e.calls++,a){case i.TRIANGLES:e.triangles+=o*(r/3);break;case i.LINES:e.lines+=o*(r/2);break;case i.LINE_STRIP:e.lines+=o*(r-1);break;case i.LINE_LOOP:e.lines+=o*r;break;case i.POINTS:e.points+=o*r;break;default:Pt("WebGLInfo: Unknown draw mode:",a);break}}function s(){e.calls=0,e.triangles=0,e.points=0,e.lines=0}return{memory:t,render:e,programs:null,autoReset:!0,reset:s,update:n}}function Cx(i,t,e){let n=new WeakMap,s=new ve;function r(a,o,l){let c=a.morphTargetInfluences,h=o.morphAttributes.position||o.morphAttributes.normal||o.morphAttributes.color,f=h!==void 0?h.length:0,u=n.get(o);if(u===void 0||u.count!==f){let E=function(){R.dispose(),n.delete(o),o.removeEventListener("dispose",E)};u!==void 0&&u.texture.dispose();let d=o.morphAttributes.position!==void 0,m=o.morphAttributes.normal!==void 0,_=o.morphAttributes.color!==void 0,g=o.morphAttributes.position||[],p=o.morphAttributes.normal||[],y=o.morphAttributes.color||[],S=0;d===!0&&(S=1),m===!0&&(S=2),_===!0&&(S=3);let b=o.attributes.position.count*S,T=1;b>t.maxTextureSize&&(T=Math.ceil(b/t.maxTextureSize),b=t.maxTextureSize);let w=new Float32Array(b*T*4*f),R=new mr(w,b,T,f);R.type=Un,R.needsUpdate=!0;let v=S*4;for(let L=0;L<f;L++){let C=g[L],D=p[L],H=y[L],W=b*T*4*L;for(let U=0;U<C.count;U++){let z=U*v;d===!0&&(s.fromBufferAttribute(C,U),w[W+z+0]=s.x,w[W+z+1]=s.y,w[W+z+2]=s.z,w[W+z+3]=0),m===!0&&(s.fromBufferAttribute(D,U),w[W+z+4]=s.x,w[W+z+5]=s.y,w[W+z+6]=s.z,w[W+z+7]=0),_===!0&&(s.fromBufferAttribute(H,U),w[W+z+8]=s.x,w[W+z+9]=s.y,w[W+z+10]=s.z,w[W+z+11]=H.itemSize===4?s.w:1)}}u={count:f,texture:R,size:new Et(b,T)},n.set(o,u),o.addEventListener("dispose",E)}if(a.isInstancedMesh===!0&&a.morphTexture!==null)l.getUniforms().setValue(i,"morphTexture",a.morphTexture,e);else{let d=0;for(let _=0;_<c.length;_++)d+=c[_];let m=o.morphTargetsRelative?1:1-d;l.getUniforms().setValue(i,"morphTargetBaseInfluence",m),l.getUniforms().setValue(i,"morphTargetInfluences",c)}l.getUniforms().setValue(i,"morphTargetsTexture",u.texture,e),l.getUniforms().setValue(i,"morphTargetsTextureSize",u.size)}return{update:r}}function Rx(i,t,e,n,s){let r=new WeakMap;function a(c){let h=s.render.frame,f=c.geometry,u=t.get(c,f);if(r.get(u)!==h&&(t.update(u),r.set(u,h)),c.isInstancedMesh&&(c.hasEventListener("dispose",l)===!1&&c.addEventListener("dispose",l),r.get(c)!==h&&(e.update(c.instanceMatrix,i.ARRAY_BUFFER),c.instanceColor!==null&&e.update(c.instanceColor,i.ARRAY_BUFFER),r.set(c,h))),c.isSkinnedMesh){let d=c.skeleton;r.get(d)!==h&&(d.update(),r.set(d,h))}return u}function o(){r=new WeakMap}function l(c){let h=c.target;h.removeEventListener("dispose",l),n.releaseStatesOfObject(h),e.remove(h.instanceMatrix),h.instanceColor!==null&&e.remove(h.instanceColor)}return{update:a,dispose:o}}var Px={[Ir]:"LINEAR_TONE_MAPPING",[Lr]:"REINHARD_TONE_MAPPING",[Nr]:"CINEON_TONE_MAPPING",[Di]:"ACES_FILMIC_TONE_MAPPING",[Fr]:"AGX_TONE_MAPPING",[Ur]:"NEUTRAL_TONE_MAPPING",[Dr]:"CUSTOM_TONE_MAPPING"};function Ix(i,t,e,n,s){let r=new Ne(t,e,{type:i,depthBuffer:n,stencilBuffer:s,depthTexture:n?new hi(t,e):void 0}),a=new Ne(t,e,{type:Ze,depthBuffer:!1,stencilBuffer:!1}),o=new te;o.setAttribute("position",new Ve([-1,3,0,-1,-1,0,3,-1,0],3)),o.setAttribute("uv",new Ve([0,2,0,0,2,0],2));let l=new Bs({uniforms:{tDiffuse:{value:null}},vertexShader:`
			precision highp float;

			uniform mat4 modelViewMatrix;
			uniform mat4 projectionMatrix;

			attribute vec3 position;
			attribute vec2 uv;

			varying vec2 vUv;

			void main() {
				vUv = uv;
				gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
			}`,fragmentShader:`
			precision highp float;

			uniform sampler2D tDiffuse;

			varying vec2 vUv;

			#include <tonemapping_pars_fragment>
			#include <colorspace_pars_fragment>

			void main() {
				gl_FragColor = texture2D( tDiffuse, vUv );

				#ifdef LINEAR_TONE_MAPPING
					gl_FragColor.rgb = LinearToneMapping( gl_FragColor.rgb );
				#elif defined( REINHARD_TONE_MAPPING )
					gl_FragColor.rgb = ReinhardToneMapping( gl_FragColor.rgb );
				#elif defined( CINEON_TONE_MAPPING )
					gl_FragColor.rgb = CineonToneMapping( gl_FragColor.rgb );
				#elif defined( ACES_FILMIC_TONE_MAPPING )
					gl_FragColor.rgb = ACESFilmicToneMapping( gl_FragColor.rgb );
				#elif defined( AGX_TONE_MAPPING )
					gl_FragColor.rgb = AgXToneMapping( gl_FragColor.rgb );
				#elif defined( NEUTRAL_TONE_MAPPING )
					gl_FragColor.rgb = NeutralToneMapping( gl_FragColor.rgb );
				#elif defined( CUSTOM_TONE_MAPPING )
					gl_FragColor.rgb = CustomToneMapping( gl_FragColor.rgb );
				#endif

				#ifdef SRGB_TRANSFER
					gl_FragColor = sRGBTransferOETF( gl_FragColor );
				#endif
			}`,depthTest:!1,depthWrite:!1}),c=new rn(o,l),h=new as(-1,1,1,-1,0,1),f=null,u=null,d=!1,m,_=null,g=[],p=!1;this.setSize=function(y,S){r.setSize(y,S),a.setSize(y,S);for(let b=0;b<g.length;b++){let T=g[b];T.setSize&&T.setSize(y,S)}},this.setEffects=function(y){g=y,p=g.length>0&&g[0].isRenderPass===!0;let S=r.width,b=r.height;for(let T=0;T<g.length;T++){let w=g[T];w.setSize&&w.setSize(S,b)}},this.begin=function(y,S){if(d||y.toneMapping===xn&&g.length===0)return!1;if(_=S,S!==null){let b=S.width,T=S.height;(r.width!==b||r.height!==T)&&this.setSize(b,T)}return p===!1&&y.setRenderTarget(r),m=y.toneMapping,y.toneMapping=xn,!0},this.hasRenderPass=function(){return p},this.end=function(y,S){y.toneMapping=m,d=!0;let b=r,T=a;for(let w=0;w<g.length;w++){let R=g[w];if(R.enabled!==!1&&(R.render(y,T,b,S),R.needsSwap!==!1)){let v=b;b=T,T=v}}if(f!==y.outputColorSpace||u!==y.toneMapping){f=y.outputColorSpace,u=y.toneMapping,l.defines={},Wt.getTransfer(f)===jt&&(l.defines.SRGB_TRANSFER="");let w=Px[u];w&&(l.defines[w]=""),l.needsUpdate=!0}l.uniforms.tDiffuse.value=b.texture,y.setRenderTarget(_),y.render(c,h),_=null,d=!1},this.isCompositing=function(){return d},this.dispose=function(){r.depthTexture&&r.depthTexture.dispose(),r.dispose(),a.dispose(),o.dispose(),l.dispose()}}var ld=new nn,ph=new hi(1,1),cd=new mr,hd=new Ja,ud=new Mr,Hf=[],Wf=[],Xf=new Float32Array(16),qf=new Float32Array(9),Yf=new Float32Array(4);function Xs(i,t,e){let n=i[0];if(n<=0||n>0)return i;let s=t*e,r=Hf[s];if(r===void 0&&(r=new Float32Array(s),Hf[s]=r),t!==0){n.toArray(r,0);for(let a=1,o=0;a!==t;++a)o+=e,i[a].toArray(r,o)}return r}function De(i,t){if(i.length!==t.length)return!1;for(let e=0,n=i.length;e<n;e++)if(i[e]!==t[e])return!1;return!0}function Fe(i,t){for(let e=0,n=t.length;e<n;e++)i[e]=t[e]}function dl(i,t){let e=Wf[t];e===void 0&&(e=new Int32Array(t),Wf[t]=e);for(let n=0;n!==t;++n)e[n]=i.allocateTextureUnit();return e}function Lx(i,t){let e=this.cache;e[0]!==t&&(i.uniform1f(this.addr,t),e[0]=t)}function Nx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y)&&(i.uniform2f(this.addr,t.x,t.y),e[0]=t.x,e[1]=t.y);else{if(De(e,t))return;i.uniform2fv(this.addr,t),Fe(e,t)}}function Dx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z)&&(i.uniform3f(this.addr,t.x,t.y,t.z),e[0]=t.x,e[1]=t.y,e[2]=t.z);else if(t.r!==void 0)(e[0]!==t.r||e[1]!==t.g||e[2]!==t.b)&&(i.uniform3f(this.addr,t.r,t.g,t.b),e[0]=t.r,e[1]=t.g,e[2]=t.b);else{if(De(e,t))return;i.uniform3fv(this.addr,t),Fe(e,t)}}function Fx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z||e[3]!==t.w)&&(i.uniform4f(this.addr,t.x,t.y,t.z,t.w),e[0]=t.x,e[1]=t.y,e[2]=t.z,e[3]=t.w);else{if(De(e,t))return;i.uniform4fv(this.addr,t),Fe(e,t)}}function Ux(i,t){let e=this.cache,n=t.elements;if(n===void 0){if(De(e,t))return;i.uniformMatrix2fv(this.addr,!1,t),Fe(e,t)}else{if(De(e,n))return;Yf.set(n),i.uniformMatrix2fv(this.addr,!1,Yf),Fe(e,n)}}function Ox(i,t){let e=this.cache,n=t.elements;if(n===void 0){if(De(e,t))return;i.uniformMatrix3fv(this.addr,!1,t),Fe(e,t)}else{if(De(e,n))return;qf.set(n),i.uniformMatrix3fv(this.addr,!1,qf),Fe(e,n)}}function Bx(i,t){let e=this.cache,n=t.elements;if(n===void 0){if(De(e,t))return;i.uniformMatrix4fv(this.addr,!1,t),Fe(e,t)}else{if(De(e,n))return;Xf.set(n),i.uniformMatrix4fv(this.addr,!1,Xf),Fe(e,n)}}function kx(i,t){let e=this.cache;e[0]!==t&&(i.uniform1i(this.addr,t),e[0]=t)}function zx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y)&&(i.uniform2i(this.addr,t.x,t.y),e[0]=t.x,e[1]=t.y);else{if(De(e,t))return;i.uniform2iv(this.addr,t),Fe(e,t)}}function Vx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z)&&(i.uniform3i(this.addr,t.x,t.y,t.z),e[0]=t.x,e[1]=t.y,e[2]=t.z);else{if(De(e,t))return;i.uniform3iv(this.addr,t),Fe(e,t)}}function Gx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z||e[3]!==t.w)&&(i.uniform4i(this.addr,t.x,t.y,t.z,t.w),e[0]=t.x,e[1]=t.y,e[2]=t.z,e[3]=t.w);else{if(De(e,t))return;i.uniform4iv(this.addr,t),Fe(e,t)}}function Hx(i,t){let e=this.cache;e[0]!==t&&(i.uniform1ui(this.addr,t),e[0]=t)}function Wx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y)&&(i.uniform2ui(this.addr,t.x,t.y),e[0]=t.x,e[1]=t.y);else{if(De(e,t))return;i.uniform2uiv(this.addr,t),Fe(e,t)}}function Xx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z)&&(i.uniform3ui(this.addr,t.x,t.y,t.z),e[0]=t.x,e[1]=t.y,e[2]=t.z);else{if(De(e,t))return;i.uniform3uiv(this.addr,t),Fe(e,t)}}function qx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z||e[3]!==t.w)&&(i.uniform4ui(this.addr,t.x,t.y,t.z,t.w),e[0]=t.x,e[1]=t.y,e[2]=t.z,e[3]=t.w);else{if(De(e,t))return;i.uniform4uiv(this.addr,t),Fe(e,t)}}function Yx(i,t,e){let n=this.cache,s=e.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s);let r;this.type===i.SAMPLER_2D_SHADOW?(ph.compareFunction=e.isReversedDepthBuffer()?al:rl,r=ph):r=ld,e.setTexture2D(t||r,s)}function Zx(i,t,e){let n=this.cache,s=e.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),e.setTexture3D(t||hd,s)}function Kx(i,t,e){let n=this.cache,s=e.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),e.setTextureCube(t||ud,s)}function Jx(i,t,e){let n=this.cache,s=e.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),e.setTexture2DArray(t||cd,s)}function $x(i){switch(i){case 5126:return Lx;case 35664:return Nx;case 35665:return Dx;case 35666:return Fx;case 35674:return Ux;case 35675:return Ox;case 35676:return Bx;case 5124:case 35670:return kx;case 35667:case 35671:return zx;case 35668:case 35672:return Vx;case 35669:case 35673:return Gx;case 5125:return Hx;case 36294:return Wx;case 36295:return Xx;case 36296:return qx;case 35678:case 36198:case 36298:case 36306:case 35682:return Yx;case 35679:case 36299:case 36307:return Zx;case 35680:case 36300:case 36308:case 36293:return Kx;case 36289:case 36303:case 36311:case 36292:return Jx}}function jx(i,t){i.uniform1fv(this.addr,t)}function Qx(i,t){let e=Xs(t,this.size,2);i.uniform2fv(this.addr,e)}function tv(i,t){let e=Xs(t,this.size,3);i.uniform3fv(this.addr,e)}function ev(i,t){let e=Xs(t,this.size,4);i.uniform4fv(this.addr,e)}function nv(i,t){let e=Xs(t,this.size,4);i.uniformMatrix2fv(this.addr,!1,e)}function iv(i,t){let e=Xs(t,this.size,9);i.uniformMatrix3fv(this.addr,!1,e)}function sv(i,t){let e=Xs(t,this.size,16);i.uniformMatrix4fv(this.addr,!1,e)}function rv(i,t){i.uniform1iv(this.addr,t)}function av(i,t){i.uniform2iv(this.addr,t)}function ov(i,t){i.uniform3iv(this.addr,t)}function lv(i,t){i.uniform4iv(this.addr,t)}function cv(i,t){i.uniform1uiv(this.addr,t)}function hv(i,t){i.uniform2uiv(this.addr,t)}function uv(i,t){i.uniform3uiv(this.addr,t)}function fv(i,t){i.uniform4uiv(this.addr,t)}function dv(i,t,e){let n=this.cache,s=t.length,r=dl(e,s);De(n,r)||(i.uniform1iv(this.addr,r),Fe(n,r));let a;this.type===i.SAMPLER_2D_SHADOW?a=ph:a=ld;for(let o=0;o!==s;++o)e.setTexture2D(t[o]||a,r[o])}function pv(i,t,e){let n=this.cache,s=t.length,r=dl(e,s);De(n,r)||(i.uniform1iv(this.addr,r),Fe(n,r));for(let a=0;a!==s;++a)e.setTexture3D(t[a]||hd,r[a])}function mv(i,t,e){let n=this.cache,s=t.length,r=dl(e,s);De(n,r)||(i.uniform1iv(this.addr,r),Fe(n,r));for(let a=0;a!==s;++a)e.setTextureCube(t[a]||ud,r[a])}function gv(i,t,e){let n=this.cache,s=t.length,r=dl(e,s);De(n,r)||(i.uniform1iv(this.addr,r),Fe(n,r));for(let a=0;a!==s;++a)e.setTexture2DArray(t[a]||cd,r[a])}function _v(i){switch(i){case 5126:return jx;case 35664:return Qx;case 35665:return tv;case 35666:return ev;case 35674:return nv;case 35675:return iv;case 35676:return sv;case 5124:case 35670:return rv;case 35667:case 35671:return av;case 35668:case 35672:return ov;case 35669:case 35673:return lv;case 5125:return cv;case 36294:return hv;case 36295:return uv;case 36296:return fv;case 35678:case 36198:case 36298:case 36306:case 35682:return dv;case 35679:case 36299:case 36307:return pv;case 35680:case 36300:case 36308:case 36293:return mv;case 36289:case 36303:case 36311:case 36292:return gv}}var mh=class{constructor(t,e,n){this.id=t,this.addr=n,this.cache=[],this.type=e.type,this.setValue=$x(e.type)}},gh=class{constructor(t,e,n){this.id=t,this.addr=n,this.cache=[],this.type=e.type,this.size=e.size,this.setValue=_v(e.type)}},_h=class{constructor(t){this.id=t,this.seq=[],this.map={}}setValue(t,e,n){let s=this.seq;for(let r=0,a=s.length;r!==a;++r){let o=s[r];o.setValue(t,e[o.id],n)}}},fh=/(\w+)(\])?(\[|\.)?/g;function Zf(i,t){i.seq.push(t),i.map[t.id]=t}function xv(i,t,e){let n=i.name,s=n.length;for(fh.lastIndex=0;;){let r=fh.exec(n),a=fh.lastIndex,o=r[1],l=r[2]==="]",c=r[3];if(l&&(o=o|0),c===void 0||c==="["&&a+2===s){Zf(e,c===void 0?new mh(o,i,t):new gh(o,i,t));break}else{let f=e.map[o];f===void 0&&(f=new _h(o),Zf(e,f)),e=f}}}var Ws=class{constructor(t,e){this.seq=[],this.map={};let n=t.getProgramParameter(e,t.ACTIVE_UNIFORMS);for(let a=0;a<n;++a){let o=t.getActiveUniform(e,a),l=t.getUniformLocation(e,o.name);xv(o,l,this)}let s=[],r=[];for(let a of this.seq)a.type===t.SAMPLER_2D_SHADOW||a.type===t.SAMPLER_CUBE_SHADOW||a.type===t.SAMPLER_2D_ARRAY_SHADOW?s.push(a):r.push(a);s.length>0&&(this.seq=s.concat(r))}setValue(t,e,n,s){let r=this.map[e];r!==void 0&&r.setValue(t,n,s)}setOptional(t,e,n){let s=e[n];s!==void 0&&this.setValue(t,n,s)}static upload(t,e,n,s){for(let r=0,a=e.length;r!==a;++r){let o=e[r],l=n[o.id];l.needsUpdate!==!1&&o.setValue(t,l.value,s)}}static seqWithValue(t,e){let n=[];for(let s=0,r=t.length;s!==r;++s){let a=t[s];a.id in e&&n.push(a)}return n}};function Kf(i,t,e){let n=i.createShader(t);return i.shaderSource(n,e),i.compileShader(n),n}var vv=37297,yv=0;function Mv(i,t){let e=i.split(`
`),n=[],s=Math.max(t-6,0),r=Math.min(t+6,e.length);for(let a=s;a<r;a++){let o=a+1;n.push(`${o===t?">":" "} ${o}: ${e[a]}`)}return n.join(`
`)}var Jf=new Ft;function bv(i){Wt._getMatrix(Jf,Wt.workingColorSpace,i);let t=`mat3( ${Jf.elements.map(e=>e.toFixed(4))} )`;switch(Wt.getTransfer(i)){case fr:return[t,"LinearTransferOETF"];case jt:return[t,"sRGBTransferOETF"];default:return Ct("WebGLProgram: Unsupported color space: ",i),[t,"LinearTransferOETF"]}}function $f(i,t,e){let n=i.getShaderParameter(t,i.COMPILE_STATUS),r=(i.getShaderInfoLog(t)||"").trim();if(n&&r==="")return"";let a=/ERROR: 0:(\d+)/.exec(r);if(a){let o=parseInt(a[1]);return e.toUpperCase()+`

`+r+`

`+Mv(i.getShaderSource(t),o)}else return r}function Sv(i,t){let e=bv(t);return[`vec4 ${i}( vec4 value ) {`,`	return ${e[1]}( vec4( value.rgb * ${e[0]}, value.a ) );`,"}"].join(`
`)}var wv={[Ir]:"Linear",[Lr]:"Reinhard",[Nr]:"Cineon",[Di]:"ACESFilmic",[Fr]:"AgX",[Ur]:"Neutral",[Dr]:"Custom"};function Av(i,t){let e=wv[t];return e===void 0?(Ct("WebGLProgram: Unsupported toneMapping:",t),"vec3 "+i+"( vec3 color ) { return LinearToneMapping( color ); }"):"vec3 "+i+"( vec3 color ) { return "+e+"ToneMapping( color ); }"}var ll=new P;function Tv(){Wt.getLuminanceCoefficients(ll);let i=ll.x.toFixed(4),t=ll.y.toFixed(4),e=ll.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${i}, ${t}, ${e} );`,"	return dot( weights, rgb );","}"].join(`
`)}function Ev(i){return[i.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",i.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Yr).join(`
`)}function Cv(i){let t=[];for(let e in i){let n=i[e];n!==!1&&t.push("#define "+e+" "+n)}return t.join(`
`)}function Rv(i,t){let e={},n=i.getProgramParameter(t,i.ACTIVE_ATTRIBUTES);for(let s=0;s<n;s++){let r=i.getActiveAttrib(t,s),a=r.name,o=1;r.type===i.FLOAT_MAT2&&(o=2),r.type===i.FLOAT_MAT3&&(o=3),r.type===i.FLOAT_MAT4&&(o=4),e[a]={type:r.type,location:i.getAttribLocation(t,a),locationSize:o}}return e}function Yr(i){return i!==""}function jf(i,t){let e=t.numSpotLightShadows+t.numSpotLightMaps-t.numSpotLightShadowsWithMaps;return i.replace(/NUM_DIR_LIGHTS/g,t.numDirLights).replace(/NUM_SPOT_LIGHTS/g,t.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,t.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,e).replace(/NUM_RECT_AREA_LIGHTS/g,t.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,t.numPointLights).replace(/NUM_HEMI_LIGHTS/g,t.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,t.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,t.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,t.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,t.numPointLightShadows)}function Qf(i,t){return i.replace(/NUM_CLIPPING_PLANES/g,t.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,t.numClippingPlanes-t.numClipIntersection)}var Pv=/^[ \t]*#include +<([\w\d./]+)>/gm;function xh(i){return i.replace(Pv,Lv)}var Iv=new Map;function Lv(i,t){let e=Gt[t];if(e===void 0){let n=Iv.get(t);if(n!==void 0)e=Gt[n],Ct('WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',t,n);else throw new Error("Can not resolve #include <"+t+">")}return xh(e)}var Nv=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function td(i){return i.replace(Nv,Dv)}function Dv(i,t,e,n){let s="";for(let r=parseInt(t);r<parseInt(e);r++)s+=n.replace(/\[\s*i\s*\]/g,"[ "+r+" ]").replace(/UNROLLED_LOOP_INDEX/g,r);return s}function ed(i){let t=`precision ${i.precision} float;
	precision ${i.precision} int;
	precision ${i.precision} sampler2D;
	precision ${i.precision} samplerCube;
	precision ${i.precision} sampler3D;
	precision ${i.precision} sampler2DArray;
	precision ${i.precision} sampler2DShadow;
	precision ${i.precision} samplerCubeShadow;
	precision ${i.precision} sampler2DArrayShadow;
	precision ${i.precision} isampler2D;
	precision ${i.precision} isampler3D;
	precision ${i.precision} isamplerCube;
	precision ${i.precision} isampler2DArray;
	precision ${i.precision} usampler2D;
	precision ${i.precision} usampler3D;
	precision ${i.precision} usamplerCube;
	precision ${i.precision} usampler2DArray;
	`;return i.precision==="highp"?t+=`
#define HIGH_PRECISION`:i.precision==="mediump"?t+=`
#define MEDIUM_PRECISION`:i.precision==="lowp"&&(t+=`
#define LOW_PRECISION`),t}var Fv={[Pr]:"SHADOWMAP_TYPE_PCF",[ks]:"SHADOWMAP_TYPE_VSM"};function Uv(i){return Fv[i.shadowMapType]||"SHADOWMAP_TYPE_BASIC"}var Ov={[Fi]:"ENVMAP_TYPE_CUBE",[os]:"ENVMAP_TYPE_CUBE",[Or]:"ENVMAP_TYPE_CUBE_UV"};function Bv(i){return i.envMap===!1?"ENVMAP_TYPE_CUBE":Ov[i.envMapMode]||"ENVMAP_TYPE_CUBE"}var kv={[os]:"ENVMAP_MODE_REFRACTION"};function zv(i){return i.envMap===!1?"ENVMAP_MODE_REFLECTION":kv[i.envMapMode]||"ENVMAP_MODE_REFLECTION"}var Vv={[Bc]:"ENVMAP_BLENDING_MULTIPLY",[Mf]:"ENVMAP_BLENDING_MIX",[bf]:"ENVMAP_BLENDING_ADD"};function Gv(i){return i.envMap===!1?"ENVMAP_BLENDING_NONE":Vv[i.combine]||"ENVMAP_BLENDING_NONE"}function Hv(i){let t=i.envMapCubeUVHeight;if(t===null)return null;let e=Math.log2(t)-2,n=1/t;return{texelWidth:1/(3*Math.max(Math.pow(2,e),7*16)),texelHeight:n,maxMip:e}}function Wv(i,t,e,n){let s=i.getContext(),r=e.defines,a=e.vertexShader,o=e.fragmentShader,l=Uv(e),c=Bv(e),h=zv(e),f=Gv(e),u=Hv(e),d=Ev(e),m=Cv(r),_=s.createProgram(),g,p,y=e.glslVersion?"#version "+e.glslVersion+`
`:"";e.isRawShaderMaterial?(g=["#define SHADER_TYPE "+e.shaderType,"#define SHADER_NAME "+e.shaderName,m].filter(Yr).join(`
`),g.length>0&&(g+=`
`),p=["#define SHADER_TYPE "+e.shaderType,"#define SHADER_NAME "+e.shaderName,m].filter(Yr).join(`
`),p.length>0&&(p+=`
`)):(g=[ed(e),"#define SHADER_TYPE "+e.shaderType,"#define SHADER_NAME "+e.shaderName,m,e.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",e.batching?"#define USE_BATCHING":"",e.batchingColor?"#define USE_BATCHING_COLOR":"",e.instancing?"#define USE_INSTANCING":"",e.instancingColor?"#define USE_INSTANCING_COLOR":"",e.instancingMorph?"#define USE_INSTANCING_MORPH":"",e.useFog&&e.fog?"#define USE_FOG":"",e.useFog&&e.fogExp2?"#define FOG_EXP2":"",e.map?"#define USE_MAP":"",e.envMap?"#define USE_ENVMAP":"",e.envMap?"#define "+h:"",e.lightMap?"#define USE_LIGHTMAP":"",e.aoMap?"#define USE_AOMAP":"",e.bumpMap?"#define USE_BUMPMAP":"",e.normalMap?"#define USE_NORMALMAP":"",e.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",e.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",e.displacementMap?"#define USE_DISPLACEMENTMAP":"",e.emissiveMap?"#define USE_EMISSIVEMAP":"",e.anisotropy?"#define USE_ANISOTROPY":"",e.anisotropyMap?"#define USE_ANISOTROPYMAP":"",e.clearcoatMap?"#define USE_CLEARCOATMAP":"",e.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",e.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",e.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",e.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",e.specularMap?"#define USE_SPECULARMAP":"",e.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",e.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",e.roughnessMap?"#define USE_ROUGHNESSMAP":"",e.metalnessMap?"#define USE_METALNESSMAP":"",e.alphaMap?"#define USE_ALPHAMAP":"",e.alphaHash?"#define USE_ALPHAHASH":"",e.transmission?"#define USE_TRANSMISSION":"",e.transmissionMap?"#define USE_TRANSMISSIONMAP":"",e.thicknessMap?"#define USE_THICKNESSMAP":"",e.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",e.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",e.mapUv?"#define MAP_UV "+e.mapUv:"",e.alphaMapUv?"#define ALPHAMAP_UV "+e.alphaMapUv:"",e.lightMapUv?"#define LIGHTMAP_UV "+e.lightMapUv:"",e.aoMapUv?"#define AOMAP_UV "+e.aoMapUv:"",e.emissiveMapUv?"#define EMISSIVEMAP_UV "+e.emissiveMapUv:"",e.bumpMapUv?"#define BUMPMAP_UV "+e.bumpMapUv:"",e.normalMapUv?"#define NORMALMAP_UV "+e.normalMapUv:"",e.displacementMapUv?"#define DISPLACEMENTMAP_UV "+e.displacementMapUv:"",e.metalnessMapUv?"#define METALNESSMAP_UV "+e.metalnessMapUv:"",e.roughnessMapUv?"#define ROUGHNESSMAP_UV "+e.roughnessMapUv:"",e.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+e.anisotropyMapUv:"",e.clearcoatMapUv?"#define CLEARCOATMAP_UV "+e.clearcoatMapUv:"",e.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+e.clearcoatNormalMapUv:"",e.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+e.clearcoatRoughnessMapUv:"",e.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+e.iridescenceMapUv:"",e.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+e.iridescenceThicknessMapUv:"",e.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+e.sheenColorMapUv:"",e.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+e.sheenRoughnessMapUv:"",e.specularMapUv?"#define SPECULARMAP_UV "+e.specularMapUv:"",e.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+e.specularColorMapUv:"",e.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+e.specularIntensityMapUv:"",e.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+e.transmissionMapUv:"",e.thicknessMapUv?"#define THICKNESSMAP_UV "+e.thicknessMapUv:"",e.vertexTangents&&e.flatShading===!1?"#define USE_TANGENT":"",e.vertexNormals?"#define HAS_NORMAL":"",e.vertexColors?"#define USE_COLOR":"",e.vertexAlphas?"#define USE_COLOR_ALPHA":"",e.vertexUv1s?"#define USE_UV1":"",e.vertexUv2s?"#define USE_UV2":"",e.vertexUv3s?"#define USE_UV3":"",e.pointsUvs?"#define USE_POINTS_UV":"",e.flatShading?"#define FLAT_SHADED":"",e.skinning?"#define USE_SKINNING":"",e.morphTargets?"#define USE_MORPHTARGETS":"",e.morphNormals&&e.flatShading===!1?"#define USE_MORPHNORMALS":"",e.morphColors?"#define USE_MORPHCOLORS":"",e.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+e.morphTextureStride:"",e.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+e.morphTargetsCount:"",e.doubleSided?"#define DOUBLE_SIDED":"",e.flipSided?"#define FLIP_SIDED":"",e.shadowMapEnabled?"#define USE_SHADOWMAP":"",e.shadowMapEnabled?"#define "+l:"",e.sizeAttenuation?"#define USE_SIZEATTENUATION":"",e.numLightProbes>0?"#define USE_LIGHT_PROBES":"",e.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",e.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Yr).join(`
`),p=[ed(e),"#define SHADER_TYPE "+e.shaderType,"#define SHADER_NAME "+e.shaderName,m,e.useFog&&e.fog?"#define USE_FOG":"",e.useFog&&e.fogExp2?"#define FOG_EXP2":"",e.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",e.map?"#define USE_MAP":"",e.matcap?"#define USE_MATCAP":"",e.envMap?"#define USE_ENVMAP":"",e.envMap?"#define "+c:"",e.envMap?"#define "+h:"",e.envMap?"#define "+f:"",u?"#define CUBEUV_TEXEL_WIDTH "+u.texelWidth:"",u?"#define CUBEUV_TEXEL_HEIGHT "+u.texelHeight:"",u?"#define CUBEUV_MAX_MIP "+u.maxMip+".0":"",e.lightMap?"#define USE_LIGHTMAP":"",e.aoMap?"#define USE_AOMAP":"",e.bumpMap?"#define USE_BUMPMAP":"",e.normalMap?"#define USE_NORMALMAP":"",e.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",e.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",e.packedNormalMap?"#define USE_PACKED_NORMALMAP":"",e.emissiveMap?"#define USE_EMISSIVEMAP":"",e.anisotropy?"#define USE_ANISOTROPY":"",e.anisotropyMap?"#define USE_ANISOTROPYMAP":"",e.clearcoat?"#define USE_CLEARCOAT":"",e.clearcoatMap?"#define USE_CLEARCOATMAP":"",e.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",e.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",e.dispersion?"#define USE_DISPERSION":"",e.iridescence?"#define USE_IRIDESCENCE":"",e.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",e.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",e.specularMap?"#define USE_SPECULARMAP":"",e.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",e.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",e.roughnessMap?"#define USE_ROUGHNESSMAP":"",e.metalnessMap?"#define USE_METALNESSMAP":"",e.alphaMap?"#define USE_ALPHAMAP":"",e.alphaTest?"#define USE_ALPHATEST":"",e.alphaHash?"#define USE_ALPHAHASH":"",e.sheen?"#define USE_SHEEN":"",e.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",e.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",e.transmission?"#define USE_TRANSMISSION":"",e.transmissionMap?"#define USE_TRANSMISSIONMAP":"",e.thicknessMap?"#define USE_THICKNESSMAP":"",e.vertexTangents&&e.flatShading===!1?"#define USE_TANGENT":"",e.vertexColors||e.instancingColor?"#define USE_COLOR":"",e.vertexAlphas||e.batchingColor?"#define USE_COLOR_ALPHA":"",e.vertexUv1s?"#define USE_UV1":"",e.vertexUv2s?"#define USE_UV2":"",e.vertexUv3s?"#define USE_UV3":"",e.pointsUvs?"#define USE_POINTS_UV":"",e.gradientMap?"#define USE_GRADIENTMAP":"",e.flatShading?"#define FLAT_SHADED":"",e.doubleSided?"#define DOUBLE_SIDED":"",e.flipSided?"#define FLIP_SIDED":"",e.shadowMapEnabled?"#define USE_SHADOWMAP":"",e.shadowMapEnabled?"#define "+l:"",e.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",e.numLightProbes>0?"#define USE_LIGHT_PROBES":"",e.numLightProbeGrids>0?"#define USE_LIGHT_PROBES_GRID":"",e.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",e.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",e.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",e.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",e.toneMapping!==xn?"#define TONE_MAPPING":"",e.toneMapping!==xn?Gt.tonemapping_pars_fragment:"",e.toneMapping!==xn?Av("toneMapping",e.toneMapping):"",e.dithering?"#define DITHERING":"",e.opaque?"#define OPAQUE":"",Gt.colorspace_pars_fragment,Sv("linearToOutputTexel",e.outputColorSpace),Tv(),e.useDepthPacking?"#define DEPTH_PACKING "+e.depthPacking:"",`
`].filter(Yr).join(`
`)),a=xh(a),a=jf(a,e),a=Qf(a,e),o=xh(o),o=jf(o,e),o=Qf(o,e),a=td(a),o=td(o),e.isRawShaderMaterial!==!0&&(y=`#version 300 es
`,g=[d,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+g,p=["#define varying in",e.glslVersion===Zc?"":"layout(location = 0) out highp vec4 pc_fragColor;",e.glslVersion===Zc?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+p);let S=y+g+a,b=y+p+o,T=Kf(s,s.VERTEX_SHADER,S),w=Kf(s,s.FRAGMENT_SHADER,b);s.attachShader(_,T),s.attachShader(_,w),e.index0AttributeName!==void 0?s.bindAttribLocation(_,0,e.index0AttributeName):e.morphTargets===!0&&s.bindAttribLocation(_,0,"position"),s.linkProgram(_);function R(C){if(i.debug.checkShaderErrors){let D=s.getProgramInfoLog(_)||"",H=s.getShaderInfoLog(T)||"",W=s.getShaderInfoLog(w)||"",U=D.trim(),z=H.trim(),V=W.trim(),$=!0,tt=!0;if(s.getProgramParameter(_,s.LINK_STATUS)===!1)if($=!1,typeof i.debug.onShaderError=="function")i.debug.onShaderError(s,_,T,w);else{let ct=$f(s,T,"vertex"),Mt=$f(s,w,"fragment");Pt("THREE.WebGLProgram: Shader Error "+s.getError()+" - VALIDATE_STATUS "+s.getProgramParameter(_,s.VALIDATE_STATUS)+`

Material Name: `+C.name+`
Material Type: `+C.type+`

Program Info Log: `+U+`
`+ct+`
`+Mt)}else U!==""?Ct("WebGLProgram: Program Info Log:",U):(z===""||V==="")&&(tt=!1);tt&&(C.diagnostics={runnable:$,programLog:U,vertexShader:{log:z,prefix:g},fragmentShader:{log:V,prefix:p}})}s.deleteShader(T),s.deleteShader(w),v=new Ws(s,_),E=Rv(s,_)}let v;this.getUniforms=function(){return v===void 0&&R(this),v};let E;this.getAttributes=function(){return E===void 0&&R(this),E};let L=e.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return L===!1&&(L=s.getProgramParameter(_,vv)),L},this.destroy=function(){n.releaseStatesOfProgram(this),s.deleteProgram(_),this.program=void 0},this.type=e.shaderType,this.name=e.shaderName,this.id=yv++,this.cacheKey=t,this.usedTimes=1,this.program=_,this.vertexShader=T,this.fragmentShader=w,this}var Xv=0,vh=class{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(t){let e=t.vertexShader,n=t.fragmentShader,s=this._getShaderStage(e),r=this._getShaderStage(n),a=this._getShaderCacheForMaterial(t);return a.has(s)===!1&&(a.add(s),s.usedTimes++),a.has(r)===!1&&(a.add(r),r.usedTimes++),this}remove(t){let e=this.materialCache.get(t);for(let n of e)n.usedTimes--,n.usedTimes===0&&this.shaderCache.delete(n.code);return this.materialCache.delete(t),this}getVertexShaderID(t){return this._getShaderStage(t.vertexShader).id}getFragmentShaderID(t){return this._getShaderStage(t.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(t){let e=this.materialCache,n=e.get(t);return n===void 0&&(n=new Set,e.set(t,n)),n}_getShaderStage(t){let e=this.shaderCache,n=e.get(t);return n===void 0&&(n=new yh(t),e.set(t,n)),n}},yh=class{constructor(t){this.id=Xv++,this.code=t,this.usedTimes=0}};function qv(i){return i===Bi||i===Hr||i===Wr}function Yv(i,t,e,n,s,r){let a=new gr,o=new vh,l=new Set,c=[],h=new Map,f=n.logarithmicDepthBuffer,u=n.precision,d={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distance",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function m(v){return l.add(v),v===0?"uv":`uv${v}`}function _(v,E,L,C,D,H){let W=C.fog,U=D.geometry,z=v.isMeshStandardMaterial||v.isMeshLambertMaterial||v.isMeshPhongMaterial?C.environment:null,V=v.isMeshStandardMaterial||v.isMeshLambertMaterial&&!v.envMap||v.isMeshPhongMaterial&&!v.envMap,$=t.get(v.envMap||z,V),tt=$&&$.mapping===Or?$.image.height:null,ct=d[v.type];v.precision!==null&&(u=n.getMaxPrecision(v.precision),u!==v.precision&&Ct("WebGLProgram.getParameters:",v.precision,"not supported, using",u,"instead."));let Mt=U.morphAttributes.position||U.morphAttributes.normal||U.morphAttributes.color,St=Mt!==void 0?Mt.length:0,qt=0;U.morphAttributes.position!==void 0&&(qt=1),U.morphAttributes.normal!==void 0&&(qt=2),U.morphAttributes.color!==void 0&&(qt=3);let ee,kt,J,mt;if(ct){let Ot=Yn[ct];ee=Ot.vertexShader,kt=Ot.fragmentShader}else ee=v.vertexShader,kt=v.fragmentShader,o.update(v),J=o.getVertexShaderID(v),mt=o.getFragmentShaderID(v);let st=i.getRenderTarget(),Rt=i.state.buffers.depth.getReversed(),Ut=D.isInstancedMesh===!0,It=D.isBatchedMesh===!0,pe=!!v.map,Yt=!!v.matcap,ne=!!$,fe=!!v.aoMap,Xt=!!v.lightMap,Ie=!!v.bumpMap,me=!!v.normalMap,un=!!v.displacementMap,N=!!v.emissiveMap,Le=!!v.metalnessMap,Zt=!!v.roughnessMap,he=v.anisotropy>0,ht=v.clearcoat>0,_e=v.dispersion>0,A=v.iridescence>0,x=v.sheen>0,O=v.transmission>0,Z=he&&!!v.anisotropyMap,Q=ht&&!!v.clearcoatMap,et=ht&&!!v.clearcoatNormalMap,lt=ht&&!!v.clearcoatRoughnessMap,X=A&&!!v.iridescenceMap,K=A&&!!v.iridescenceThicknessMap,gt=x&&!!v.sheenColorMap,vt=x&&!!v.sheenRoughnessMap,rt=!!v.specularMap,nt=!!v.specularColorMap,Dt=!!v.specularIntensityMap,zt=O&&!!v.transmissionMap,$t=O&&!!v.thicknessMap,I=!!v.gradientMap,it=!!v.alphaMap,Y=v.alphaTest>0,_t=!!v.alphaHash,at=!!v.extensions,j=xn;v.toneMapped&&(st===null||st.isXRRenderTarget===!0)&&(j=i.toneMapping);let wt={shaderID:ct,shaderType:v.type,shaderName:v.name,vertexShader:ee,fragmentShader:kt,defines:v.defines,customVertexShaderID:J,customFragmentShaderID:mt,isRawShaderMaterial:v.isRawShaderMaterial===!0,glslVersion:v.glslVersion,precision:u,batching:It,batchingColor:It&&D._colorsTexture!==null,instancing:Ut,instancingColor:Ut&&D.instanceColor!==null,instancingMorph:Ut&&D.morphTexture!==null,outputColorSpace:st===null?i.outputColorSpace:st.isXRRenderTarget===!0?st.texture.colorSpace:Wt.workingColorSpace,alphaToCoverage:!!v.alphaToCoverage,map:pe,matcap:Yt,envMap:ne,envMapMode:ne&&$.mapping,envMapCubeUVHeight:tt,aoMap:fe,lightMap:Xt,bumpMap:Ie,normalMap:me,displacementMap:un,emissiveMap:N,normalMapObjectSpace:me&&v.normalMapType===Af,normalMapTangentSpace:me&&v.normalMapType===Yc,packedNormalMap:me&&v.normalMapType===Yc&&qv(v.normalMap.format),metalnessMap:Le,roughnessMap:Zt,anisotropy:he,anisotropyMap:Z,clearcoat:ht,clearcoatMap:Q,clearcoatNormalMap:et,clearcoatRoughnessMap:lt,dispersion:_e,iridescence:A,iridescenceMap:X,iridescenceThicknessMap:K,sheen:x,sheenColorMap:gt,sheenRoughnessMap:vt,specularMap:rt,specularColorMap:nt,specularIntensityMap:Dt,transmission:O,transmissionMap:zt,thicknessMap:$t,gradientMap:I,opaque:v.transparent===!1&&v.blending===Gn&&v.alphaToCoverage===!1,alphaMap:it,alphaTest:Y,alphaHash:_t,combine:v.combine,mapUv:pe&&m(v.map.channel),aoMapUv:fe&&m(v.aoMap.channel),lightMapUv:Xt&&m(v.lightMap.channel),bumpMapUv:Ie&&m(v.bumpMap.channel),normalMapUv:me&&m(v.normalMap.channel),displacementMapUv:un&&m(v.displacementMap.channel),emissiveMapUv:N&&m(v.emissiveMap.channel),metalnessMapUv:Le&&m(v.metalnessMap.channel),roughnessMapUv:Zt&&m(v.roughnessMap.channel),anisotropyMapUv:Z&&m(v.anisotropyMap.channel),clearcoatMapUv:Q&&m(v.clearcoatMap.channel),clearcoatNormalMapUv:et&&m(v.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:lt&&m(v.clearcoatRoughnessMap.channel),iridescenceMapUv:X&&m(v.iridescenceMap.channel),iridescenceThicknessMapUv:K&&m(v.iridescenceThicknessMap.channel),sheenColorMapUv:gt&&m(v.sheenColorMap.channel),sheenRoughnessMapUv:vt&&m(v.sheenRoughnessMap.channel),specularMapUv:rt&&m(v.specularMap.channel),specularColorMapUv:nt&&m(v.specularColorMap.channel),specularIntensityMapUv:Dt&&m(v.specularIntensityMap.channel),transmissionMapUv:zt&&m(v.transmissionMap.channel),thicknessMapUv:$t&&m(v.thicknessMap.channel),alphaMapUv:it&&m(v.alphaMap.channel),vertexTangents:!!U.attributes.tangent&&(me||he),vertexNormals:!!U.attributes.normal,vertexColors:v.vertexColors,vertexAlphas:v.vertexColors===!0&&!!U.attributes.color&&U.attributes.color.itemSize===4,pointsUvs:D.isPoints===!0&&!!U.attributes.uv&&(pe||it),fog:!!W,useFog:v.fog===!0,fogExp2:!!W&&W.isFogExp2,flatShading:v.wireframe===!1&&(v.flatShading===!0||U.attributes.normal===void 0&&me===!1&&(v.isMeshLambertMaterial||v.isMeshPhongMaterial||v.isMeshStandardMaterial||v.isMeshPhysicalMaterial)),sizeAttenuation:v.sizeAttenuation===!0,logarithmicDepthBuffer:f,reversedDepthBuffer:Rt,skinning:D.isSkinnedMesh===!0,morphTargets:U.morphAttributes.position!==void 0,morphNormals:U.morphAttributes.normal!==void 0,morphColors:U.morphAttributes.color!==void 0,morphTargetsCount:St,morphTextureStride:qt,numDirLights:E.directional.length,numPointLights:E.point.length,numSpotLights:E.spot.length,numSpotLightMaps:E.spotLightMap.length,numRectAreaLights:E.rectArea.length,numHemiLights:E.hemi.length,numDirLightShadows:E.directionalShadowMap.length,numPointLightShadows:E.pointShadowMap.length,numSpotLightShadows:E.spotShadowMap.length,numSpotLightShadowsWithMaps:E.numSpotLightShadowsWithMaps,numLightProbes:E.numLightProbes,numLightProbeGrids:H.length,numClippingPlanes:r.numPlanes,numClipIntersection:r.numIntersection,dithering:v.dithering,shadowMapEnabled:i.shadowMap.enabled&&L.length>0,shadowMapType:i.shadowMap.type,toneMapping:j,decodeVideoTexture:pe&&v.map.isVideoTexture===!0&&Wt.getTransfer(v.map.colorSpace)===jt,decodeVideoTextureEmissive:N&&v.emissiveMap.isVideoTexture===!0&&Wt.getTransfer(v.emissiveMap.colorSpace)===jt,premultipliedAlpha:v.premultipliedAlpha,doubleSided:v.side===Xn,flipSided:v.side===je,useDepthPacking:v.depthPacking>=0,depthPacking:v.depthPacking||0,index0AttributeName:v.index0AttributeName,extensionClipCullDistance:at&&v.extensions.clipCullDistance===!0&&e.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(at&&v.extensions.multiDraw===!0||It)&&e.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:e.has("KHR_parallel_shader_compile"),customProgramCacheKey:v.customProgramCacheKey()};return wt.vertexUv1s=l.has(1),wt.vertexUv2s=l.has(2),wt.vertexUv3s=l.has(3),l.clear(),wt}function g(v){let E=[];if(v.shaderID?E.push(v.shaderID):(E.push(v.customVertexShaderID),E.push(v.customFragmentShaderID)),v.defines!==void 0)for(let L in v.defines)E.push(L),E.push(v.defines[L]);return v.isRawShaderMaterial===!1&&(p(E,v),y(E,v),E.push(i.outputColorSpace)),E.push(v.customProgramCacheKey),E.join()}function p(v,E){v.push(E.precision),v.push(E.outputColorSpace),v.push(E.envMapMode),v.push(E.envMapCubeUVHeight),v.push(E.mapUv),v.push(E.alphaMapUv),v.push(E.lightMapUv),v.push(E.aoMapUv),v.push(E.bumpMapUv),v.push(E.normalMapUv),v.push(E.displacementMapUv),v.push(E.emissiveMapUv),v.push(E.metalnessMapUv),v.push(E.roughnessMapUv),v.push(E.anisotropyMapUv),v.push(E.clearcoatMapUv),v.push(E.clearcoatNormalMapUv),v.push(E.clearcoatRoughnessMapUv),v.push(E.iridescenceMapUv),v.push(E.iridescenceThicknessMapUv),v.push(E.sheenColorMapUv),v.push(E.sheenRoughnessMapUv),v.push(E.specularMapUv),v.push(E.specularColorMapUv),v.push(E.specularIntensityMapUv),v.push(E.transmissionMapUv),v.push(E.thicknessMapUv),v.push(E.combine),v.push(E.fogExp2),v.push(E.sizeAttenuation),v.push(E.morphTargetsCount),v.push(E.morphAttributeCount),v.push(E.numDirLights),v.push(E.numPointLights),v.push(E.numSpotLights),v.push(E.numSpotLightMaps),v.push(E.numHemiLights),v.push(E.numRectAreaLights),v.push(E.numDirLightShadows),v.push(E.numPointLightShadows),v.push(E.numSpotLightShadows),v.push(E.numSpotLightShadowsWithMaps),v.push(E.numLightProbes),v.push(E.shadowMapType),v.push(E.toneMapping),v.push(E.numClippingPlanes),v.push(E.numClipIntersection),v.push(E.depthPacking)}function y(v,E){a.disableAll(),E.instancing&&a.enable(0),E.instancingColor&&a.enable(1),E.instancingMorph&&a.enable(2),E.matcap&&a.enable(3),E.envMap&&a.enable(4),E.normalMapObjectSpace&&a.enable(5),E.normalMapTangentSpace&&a.enable(6),E.clearcoat&&a.enable(7),E.iridescence&&a.enable(8),E.alphaTest&&a.enable(9),E.vertexColors&&a.enable(10),E.vertexAlphas&&a.enable(11),E.vertexUv1s&&a.enable(12),E.vertexUv2s&&a.enable(13),E.vertexUv3s&&a.enable(14),E.vertexTangents&&a.enable(15),E.anisotropy&&a.enable(16),E.alphaHash&&a.enable(17),E.batching&&a.enable(18),E.dispersion&&a.enable(19),E.batchingColor&&a.enable(20),E.gradientMap&&a.enable(21),E.packedNormalMap&&a.enable(22),E.vertexNormals&&a.enable(23),v.push(a.mask),a.disableAll(),E.fog&&a.enable(0),E.useFog&&a.enable(1),E.flatShading&&a.enable(2),E.logarithmicDepthBuffer&&a.enable(3),E.reversedDepthBuffer&&a.enable(4),E.skinning&&a.enable(5),E.morphTargets&&a.enable(6),E.morphNormals&&a.enable(7),E.morphColors&&a.enable(8),E.premultipliedAlpha&&a.enable(9),E.shadowMapEnabled&&a.enable(10),E.doubleSided&&a.enable(11),E.flipSided&&a.enable(12),E.useDepthPacking&&a.enable(13),E.dithering&&a.enable(14),E.transmission&&a.enable(15),E.sheen&&a.enable(16),E.opaque&&a.enable(17),E.pointsUvs&&a.enable(18),E.decodeVideoTexture&&a.enable(19),E.decodeVideoTextureEmissive&&a.enable(20),E.alphaToCoverage&&a.enable(21),E.numLightProbeGrids>0&&a.enable(22),v.push(a.mask)}function S(v){let E=d[v.type],L;if(E){let C=Yn[E];L=fi.clone(C.uniforms)}else L=v.uniforms;return L}function b(v,E){let L=h.get(E);return L!==void 0?++L.usedTimes:(L=new Wv(i,E,v,s),c.push(L),h.set(E,L)),L}function T(v){if(--v.usedTimes===0){let E=c.indexOf(v);c[E]=c[c.length-1],c.pop(),h.delete(v.cacheKey),v.destroy()}}function w(v){o.remove(v)}function R(){o.dispose()}return{getParameters:_,getProgramCacheKey:g,getUniforms:S,acquireProgram:b,releaseProgram:T,releaseShaderCache:w,programs:c,dispose:R}}function Zv(){let i=new WeakMap;function t(a){return i.has(a)}function e(a){let o=i.get(a);return o===void 0&&(o={},i.set(a,o)),o}function n(a){i.delete(a)}function s(a,o,l){i.get(a)[o]=l}function r(){i=new WeakMap}return{has:t,get:e,remove:n,update:s,dispose:r}}function Kv(i,t){return i.groupOrder!==t.groupOrder?i.groupOrder-t.groupOrder:i.renderOrder!==t.renderOrder?i.renderOrder-t.renderOrder:i.material.id!==t.material.id?i.material.id-t.material.id:i.materialVariant!==t.materialVariant?i.materialVariant-t.materialVariant:i.z!==t.z?i.z-t.z:i.id-t.id}function nd(i,t){return i.groupOrder!==t.groupOrder?i.groupOrder-t.groupOrder:i.renderOrder!==t.renderOrder?i.renderOrder-t.renderOrder:i.z!==t.z?t.z-i.z:i.id-t.id}function id(){let i=[],t=0,e=[],n=[],s=[];function r(){t=0,e.length=0,n.length=0,s.length=0}function a(u){let d=0;return u.isInstancedMesh&&(d+=2),u.isSkinnedMesh&&(d+=1),d}function o(u,d,m,_,g,p){let y=i[t];return y===void 0?(y={id:u.id,object:u,geometry:d,material:m,materialVariant:a(u),groupOrder:_,renderOrder:u.renderOrder,z:g,group:p},i[t]=y):(y.id=u.id,y.object=u,y.geometry=d,y.material=m,y.materialVariant=a(u),y.groupOrder=_,y.renderOrder=u.renderOrder,y.z=g,y.group=p),t++,y}function l(u,d,m,_,g,p){let y=o(u,d,m,_,g,p);m.transmission>0?n.push(y):m.transparent===!0?s.push(y):e.push(y)}function c(u,d,m,_,g,p){let y=o(u,d,m,_,g,p);m.transmission>0?n.unshift(y):m.transparent===!0?s.unshift(y):e.unshift(y)}function h(u,d){e.length>1&&e.sort(u||Kv),n.length>1&&n.sort(d||nd),s.length>1&&s.sort(d||nd)}function f(){for(let u=t,d=i.length;u<d;u++){let m=i[u];if(m.id===null)break;m.id=null,m.object=null,m.geometry=null,m.material=null,m.group=null}}return{opaque:e,transmissive:n,transparent:s,init:r,push:l,unshift:c,finish:f,sort:h}}function Jv(){let i=new WeakMap;function t(n,s){let r=i.get(n),a;return r===void 0?(a=new id,i.set(n,[a])):s>=r.length?(a=new id,r.push(a)):a=r[s],a}function e(){i=new WeakMap}return{get:t,dispose:e}}function $v(){let i={};return{get:function(t){if(i[t.id]!==void 0)return i[t.id];let e;switch(t.type){case"DirectionalLight":e={direction:new P,color:new dt};break;case"SpotLight":e={position:new P,direction:new P,color:new dt,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":e={position:new P,color:new dt,distance:0,decay:0};break;case"HemisphereLight":e={direction:new P,skyColor:new dt,groundColor:new dt};break;case"RectAreaLight":e={color:new dt,position:new P,halfWidth:new P,halfHeight:new P};break}return i[t.id]=e,e}}}function jv(){let i={};return{get:function(t){if(i[t.id]!==void 0)return i[t.id];let e;switch(t.type){case"DirectionalLight":e={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Et};break;case"SpotLight":e={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Et};break;case"PointLight":e={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Et,shadowCameraNear:1,shadowCameraFar:1e3};break}return i[t.id]=e,e}}}var Qv=0;function ty(i,t){return(t.castShadow?2:0)-(i.castShadow?2:0)+(t.map?1:0)-(i.map?1:0)}function ey(i){let t=new $v,e=jv(),n={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let c=0;c<9;c++)n.probe.push(new P);let s=new P,r=new ge,a=new ge;function o(c){let h=0,f=0,u=0;for(let E=0;E<9;E++)n.probe[E].set(0,0,0);let d=0,m=0,_=0,g=0,p=0,y=0,S=0,b=0,T=0,w=0,R=0;c.sort(ty);for(let E=0,L=c.length;E<L;E++){let C=c[E],D=C.color,H=C.intensity,W=C.distance,U=null;if(C.shadow&&C.shadow.map&&(C.shadow.map.texture.format===Bi?U=C.shadow.map.texture:U=C.shadow.map.depthTexture||C.shadow.map.texture),C.isAmbientLight)h+=D.r*H,f+=D.g*H,u+=D.b*H;else if(C.isLightProbe){for(let z=0;z<9;z++)n.probe[z].addScaledVector(C.sh.coefficients[z],H);R++}else if(C.isDirectionalLight){let z=t.get(C);if(z.color.copy(C.color).multiplyScalar(C.intensity),C.castShadow){let V=C.shadow,$=e.get(C);$.shadowIntensity=V.intensity,$.shadowBias=V.bias,$.shadowNormalBias=V.normalBias,$.shadowRadius=V.radius,$.shadowMapSize=V.mapSize,n.directionalShadow[d]=$,n.directionalShadowMap[d]=U,n.directionalShadowMatrix[d]=C.shadow.matrix,y++}n.directional[d]=z,d++}else if(C.isSpotLight){let z=t.get(C);z.position.setFromMatrixPosition(C.matrixWorld),z.color.copy(D).multiplyScalar(H),z.distance=W,z.coneCos=Math.cos(C.angle),z.penumbraCos=Math.cos(C.angle*(1-C.penumbra)),z.decay=C.decay,n.spot[_]=z;let V=C.shadow;if(C.map&&(n.spotLightMap[T]=C.map,T++,V.updateMatrices(C),C.castShadow&&w++),n.spotLightMatrix[_]=V.matrix,C.castShadow){let $=e.get(C);$.shadowIntensity=V.intensity,$.shadowBias=V.bias,$.shadowNormalBias=V.normalBias,$.shadowRadius=V.radius,$.shadowMapSize=V.mapSize,n.spotShadow[_]=$,n.spotShadowMap[_]=U,b++}_++}else if(C.isRectAreaLight){let z=t.get(C);z.color.copy(D).multiplyScalar(H),z.halfWidth.set(C.width*.5,0,0),z.halfHeight.set(0,C.height*.5,0),n.rectArea[g]=z,g++}else if(C.isPointLight){let z=t.get(C);if(z.color.copy(C.color).multiplyScalar(C.intensity),z.distance=C.distance,z.decay=C.decay,C.castShadow){let V=C.shadow,$=e.get(C);$.shadowIntensity=V.intensity,$.shadowBias=V.bias,$.shadowNormalBias=V.normalBias,$.shadowRadius=V.radius,$.shadowMapSize=V.mapSize,$.shadowCameraNear=V.camera.near,$.shadowCameraFar=V.camera.far,n.pointShadow[m]=$,n.pointShadowMap[m]=U,n.pointShadowMatrix[m]=C.shadow.matrix,S++}n.point[m]=z,m++}else if(C.isHemisphereLight){let z=t.get(C);z.skyColor.copy(C.color).multiplyScalar(H),z.groundColor.copy(C.groundColor).multiplyScalar(H),n.hemi[p]=z,p++}}g>0&&(i.has("OES_texture_float_linear")===!0?(n.rectAreaLTC1=ut.LTC_FLOAT_1,n.rectAreaLTC2=ut.LTC_FLOAT_2):(n.rectAreaLTC1=ut.LTC_HALF_1,n.rectAreaLTC2=ut.LTC_HALF_2)),n.ambient[0]=h,n.ambient[1]=f,n.ambient[2]=u;let v=n.hash;(v.directionalLength!==d||v.pointLength!==m||v.spotLength!==_||v.rectAreaLength!==g||v.hemiLength!==p||v.numDirectionalShadows!==y||v.numPointShadows!==S||v.numSpotShadows!==b||v.numSpotMaps!==T||v.numLightProbes!==R)&&(n.directional.length=d,n.spot.length=_,n.rectArea.length=g,n.point.length=m,n.hemi.length=p,n.directionalShadow.length=y,n.directionalShadowMap.length=y,n.pointShadow.length=S,n.pointShadowMap.length=S,n.spotShadow.length=b,n.spotShadowMap.length=b,n.directionalShadowMatrix.length=y,n.pointShadowMatrix.length=S,n.spotLightMatrix.length=b+T-w,n.spotLightMap.length=T,n.numSpotLightShadowsWithMaps=w,n.numLightProbes=R,v.directionalLength=d,v.pointLength=m,v.spotLength=_,v.rectAreaLength=g,v.hemiLength=p,v.numDirectionalShadows=y,v.numPointShadows=S,v.numSpotShadows=b,v.numSpotMaps=T,v.numLightProbes=R,n.version=Qv++)}function l(c,h){let f=0,u=0,d=0,m=0,_=0,g=h.matrixWorldInverse;for(let p=0,y=c.length;p<y;p++){let S=c[p];if(S.isDirectionalLight){let b=n.directional[f];b.direction.setFromMatrixPosition(S.matrixWorld),s.setFromMatrixPosition(S.target.matrixWorld),b.direction.sub(s),b.direction.transformDirection(g),f++}else if(S.isSpotLight){let b=n.spot[d];b.position.setFromMatrixPosition(S.matrixWorld),b.position.applyMatrix4(g),b.direction.setFromMatrixPosition(S.matrixWorld),s.setFromMatrixPosition(S.target.matrixWorld),b.direction.sub(s),b.direction.transformDirection(g),d++}else if(S.isRectAreaLight){let b=n.rectArea[m];b.position.setFromMatrixPosition(S.matrixWorld),b.position.applyMatrix4(g),a.identity(),r.copy(S.matrixWorld),r.premultiply(g),a.extractRotation(r),b.halfWidth.set(S.width*.5,0,0),b.halfHeight.set(0,S.height*.5,0),b.halfWidth.applyMatrix4(a),b.halfHeight.applyMatrix4(a),m++}else if(S.isPointLight){let b=n.point[u];b.position.setFromMatrixPosition(S.matrixWorld),b.position.applyMatrix4(g),u++}else if(S.isHemisphereLight){let b=n.hemi[_];b.direction.setFromMatrixPosition(S.matrixWorld),b.direction.transformDirection(g),_++}}}return{setup:o,setupView:l,state:n}}function sd(i){let t=new ey(i),e=[],n=[],s=[];function r(u){f.camera=u,e.length=0,n.length=0,s.length=0}function a(u){e.push(u)}function o(u){n.push(u)}function l(u){s.push(u)}function c(){t.setup(e)}function h(u){t.setupView(e,u)}let f={lightsArray:e,shadowsArray:n,lightProbeGridArray:s,camera:null,lights:t,transmissionRenderTarget:{},textureUnits:0};return{init:r,state:f,setupLights:c,setupLightsView:h,pushLight:a,pushShadow:o,pushLightProbeGrid:l}}function ny(i){let t=new WeakMap;function e(s,r=0){let a=t.get(s),o;return a===void 0?(o=new sd(i),t.set(s,[o])):r>=a.length?(o=new sd(i),a.push(o)):o=a[r],o}function n(){t=new WeakMap}return{get:e,dispose:n}}var iy=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,sy=`uniform sampler2D shadow_pass;
uniform vec2 resolution;
uniform float radius;
void main() {
	const float samples = float( VSM_SAMPLES );
	float mean = 0.0;
	float squared_mean = 0.0;
	float uvStride = samples <= 1.0 ? 0.0 : 2.0 / ( samples - 1.0 );
	float uvStart = samples <= 1.0 ? 0.0 : - 1.0;
	for ( float i = 0.0; i < samples; i ++ ) {
		float uvOffset = uvStart + i * uvStride;
		#ifdef HORIZONTAL_PASS
			vec2 distribution = texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( uvOffset, 0.0 ) * radius ) / resolution ).rg;
			mean += distribution.x;
			squared_mean += distribution.y * distribution.y + distribution.x * distribution.x;
		#else
			float depth = texture2D( shadow_pass, ( gl_FragCoord.xy + vec2( 0.0, uvOffset ) * radius ) / resolution ).r;
			mean += depth;
			squared_mean += depth * depth;
		#endif
	}
	mean = mean / samples;
	squared_mean = squared_mean / samples;
	float std_dev = sqrt( max( 0.0, squared_mean - mean * mean ) );
	gl_FragColor = vec4( mean, std_dev, 0.0, 1.0 );
}`,ry=[new P(1,0,0),new P(-1,0,0),new P(0,1,0),new P(0,-1,0),new P(0,0,1),new P(0,0,-1)],ay=[new P(0,-1,0),new P(0,-1,0),new P(0,0,1),new P(0,0,-1),new P(0,-1,0),new P(0,-1,0)],rd=new ge,qr=new P,dh=new P;function oy(i,t,e){let n=new yr,s=new Et,r=new Et,a=new ve,o=new io,l=new so,c={},h=e.maxTextureSize,f={[ai]:je,[je]:ai,[Xn]:Xn},u=new re({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new Et},radius:{value:4}},vertexShader:iy,fragmentShader:sy}),d=u.clone();d.defines.HORIZONTAL_PASS=1;let m=new te;m.setAttribute("position",new Lt(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));let _=new rn(m,u),g=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=Pr;let p=this.type;this.render=function(w,R,v){if(g.enabled===!1||g.autoUpdate===!1&&g.needsUpdate===!1||w.length===0)return;this.type===ef&&(Ct("WebGLShadowMap: PCFSoftShadowMap has been deprecated. Using PCFShadowMap instead."),this.type=Pr);let E=i.getRenderTarget(),L=i.getActiveCubeFace(),C=i.getActiveMipmapLevel(),D=i.state;D.setBlending(wn),D.buffers.depth.getReversed()===!0?D.buffers.color.setClear(0,0,0,0):D.buffers.color.setClear(1,1,1,1),D.buffers.depth.setTest(!0),D.setScissorTest(!1);let H=p!==this.type;H&&R.traverse(function(W){W.material&&(Array.isArray(W.material)?W.material.forEach(U=>U.needsUpdate=!0):W.material.needsUpdate=!0)});for(let W=0,U=w.length;W<U;W++){let z=w[W],V=z.shadow;if(V===void 0){Ct("WebGLShadowMap:",z,"has no shadow.");continue}if(V.autoUpdate===!1&&V.needsUpdate===!1)continue;s.copy(V.mapSize);let $=V.getFrameExtents();s.multiply($),r.copy(V.mapSize),(s.x>h||s.y>h)&&(s.x>h&&(r.x=Math.floor(h/$.x),s.x=r.x*$.x,V.mapSize.x=r.x),s.y>h&&(r.y=Math.floor(h/$.y),s.y=r.y*$.y,V.mapSize.y=r.y));let tt=i.state.buffers.depth.getReversed();if(V.camera._reversedDepth=tt,V.map===null||H===!0){if(V.map!==null&&(V.map.depthTexture!==null&&(V.map.depthTexture.dispose(),V.map.depthTexture=null),V.map.dispose()),this.type===ks){if(z.isPointLight){Ct("WebGLShadowMap: VSM shadow maps are not supported for PointLights. Use PCF or BasicShadowMap instead.");continue}V.map=new Ne(s.x,s.y,{format:Bi,type:Ze,minFilter:Ge,magFilter:Ge,generateMipmaps:!1}),V.map.texture.name=z.name+".shadowMap",V.map.depthTexture=new hi(s.x,s.y,Un),V.map.depthTexture.name=z.name+".shadowMapDepth",V.map.depthTexture.format=Hn,V.map.depthTexture.compareFunction=null,V.map.depthTexture.minFilter=Be,V.map.depthTexture.magFilter=Be}else z.isPointLight?(V.map=new hl(s.x),V.map.depthTexture=new eo(s.x,Fn)):(V.map=new Ne(s.x,s.y),V.map.depthTexture=new hi(s.x,s.y,Fn)),V.map.depthTexture.name=z.name+".shadowMap",V.map.depthTexture.format=Hn,this.type===Pr?(V.map.depthTexture.compareFunction=tt?al:rl,V.map.depthTexture.minFilter=Ge,V.map.depthTexture.magFilter=Ge):(V.map.depthTexture.compareFunction=null,V.map.depthTexture.minFilter=Be,V.map.depthTexture.magFilter=Be);V.camera.updateProjectionMatrix()}let ct=V.map.isWebGLCubeRenderTarget?6:1;for(let Mt=0;Mt<ct;Mt++){if(V.map.isWebGLCubeRenderTarget)i.setRenderTarget(V.map,Mt),i.clear();else{Mt===0&&(i.setRenderTarget(V.map),i.clear());let St=V.getViewport(Mt);a.set(r.x*St.x,r.y*St.y,r.x*St.z,r.y*St.w),D.viewport(a)}if(z.isPointLight){let St=V.camera,qt=V.matrix,ee=z.distance||St.far;ee!==St.far&&(St.far=ee,St.updateProjectionMatrix()),qr.setFromMatrixPosition(z.matrixWorld),St.position.copy(qr),dh.copy(St.position),dh.add(ry[Mt]),St.up.copy(ay[Mt]),St.lookAt(dh),St.updateMatrixWorld(),qt.makeTranslation(-qr.x,-qr.y,-qr.z),rd.multiplyMatrices(St.projectionMatrix,St.matrixWorldInverse),V._frustum.setFromProjectionMatrix(rd,St.coordinateSystem,St.reversedDepth)}else V.updateMatrices(z);n=V.getFrustum(),b(R,v,V.camera,z,this.type)}V.isPointLightShadow!==!0&&this.type===ks&&y(V,v),V.needsUpdate=!1}p=this.type,g.needsUpdate=!1,i.setRenderTarget(E,L,C)};function y(w,R){let v=t.update(_);u.defines.VSM_SAMPLES!==w.blurSamples&&(u.defines.VSM_SAMPLES=w.blurSamples,d.defines.VSM_SAMPLES=w.blurSamples,u.needsUpdate=!0,d.needsUpdate=!0),w.mapPass===null&&(w.mapPass=new Ne(s.x,s.y,{format:Bi,type:Ze})),u.uniforms.shadow_pass.value=w.map.depthTexture,u.uniforms.resolution.value=w.mapSize,u.uniforms.radius.value=w.radius,i.setRenderTarget(w.mapPass),i.clear(),i.renderBufferDirect(R,null,v,u,_,null),d.uniforms.shadow_pass.value=w.mapPass.texture,d.uniforms.resolution.value=w.mapSize,d.uniforms.radius.value=w.radius,i.setRenderTarget(w.map),i.clear(),i.renderBufferDirect(R,null,v,d,_,null)}function S(w,R,v,E){let L=null,C=v.isPointLight===!0?w.customDistanceMaterial:w.customDepthMaterial;if(C!==void 0)L=C;else if(L=v.isPointLight===!0?l:o,i.localClippingEnabled&&R.clipShadows===!0&&Array.isArray(R.clippingPlanes)&&R.clippingPlanes.length!==0||R.displacementMap&&R.displacementScale!==0||R.alphaMap&&R.alphaTest>0||R.map&&R.alphaTest>0||R.alphaToCoverage===!0){let D=L.uuid,H=R.uuid,W=c[D];W===void 0&&(W={},c[D]=W);let U=W[H];U===void 0&&(U=L.clone(),W[H]=U,R.addEventListener("dispose",T)),L=U}if(L.visible=R.visible,L.wireframe=R.wireframe,E===ks?L.side=R.shadowSide!==null?R.shadowSide:R.side:L.side=R.shadowSide!==null?R.shadowSide:f[R.side],L.alphaMap=R.alphaMap,L.alphaTest=R.alphaToCoverage===!0?.5:R.alphaTest,L.map=R.map,L.clipShadows=R.clipShadows,L.clippingPlanes=R.clippingPlanes,L.clipIntersection=R.clipIntersection,L.displacementMap=R.displacementMap,L.displacementScale=R.displacementScale,L.displacementBias=R.displacementBias,L.wireframeLinewidth=R.wireframeLinewidth,L.linewidth=R.linewidth,v.isPointLight===!0&&L.isMeshDistanceMaterial===!0){let D=i.properties.get(L);D.light=v}return L}function b(w,R,v,E,L){if(w.visible===!1)return;if(w.layers.test(R.layers)&&(w.isMesh||w.isLine||w.isPoints)&&(w.castShadow||w.receiveShadow&&L===ks)&&(!w.frustumCulled||n.intersectsObject(w))){w.modelViewMatrix.multiplyMatrices(v.matrixWorldInverse,w.matrixWorld);let H=t.update(w),W=w.material;if(Array.isArray(W)){let U=H.groups;for(let z=0,V=U.length;z<V;z++){let $=U[z],tt=W[$.materialIndex];if(tt&&tt.visible){let ct=S(w,tt,E,L);w.onBeforeShadow(i,w,R,v,H,ct,$),i.renderBufferDirect(v,null,H,ct,w,$),w.onAfterShadow(i,w,R,v,H,ct,$)}}}else if(W.visible){let U=S(w,W,E,L);w.onBeforeShadow(i,w,R,v,H,U,null),i.renderBufferDirect(v,null,H,U,w,null),w.onAfterShadow(i,w,R,v,H,U,null)}}let D=w.children;for(let H=0,W=D.length;H<W;H++)b(D[H],R,v,E,L)}function T(w){w.target.removeEventListener("dispose",T);for(let v in c){let E=c[v],L=w.target.uuid;L in E&&(E[L].dispose(),delete E[L])}}}function ly(i,t){function e(){let I=!1,it=new ve,Y=null,_t=new ve(0,0,0,0);return{setMask:function(at){Y!==at&&!I&&(i.colorMask(at,at,at,at),Y=at)},setLocked:function(at){I=at},setClear:function(at,j,wt,Ot,be){be===!0&&(at*=Ot,j*=Ot,wt*=Ot),it.set(at,j,wt,Ot),_t.equals(it)===!1&&(i.clearColor(at,j,wt,Ot),_t.copy(it))},reset:function(){I=!1,Y=null,_t.set(-1,0,0,0)}}}function n(){let I=!1,it=!1,Y=null,_t=null,at=null;return{setReversed:function(j){if(it!==j){let wt=t.get("EXT_clip_control");j?wt.clipControlEXT(wt.LOWER_LEFT_EXT,wt.ZERO_TO_ONE_EXT):wt.clipControlEXT(wt.LOWER_LEFT_EXT,wt.NEGATIVE_ONE_TO_ONE_EXT),it=j;let Ot=at;at=null,this.setClear(Ot)}},getReversed:function(){return it},setTest:function(j){j?st(i.DEPTH_TEST):Rt(i.DEPTH_TEST)},setMask:function(j){Y!==j&&!I&&(i.depthMask(j),Y=j)},setFunc:function(j){if(it&&(j=Ff[j]),_t!==j){switch(j){case Oa:i.depthFunc(i.NEVER);break;case Ba:i.depthFunc(i.ALWAYS);break;case ka:i.depthFunc(i.LESS);break;case is:i.depthFunc(i.LEQUAL);break;case za:i.depthFunc(i.EQUAL);break;case Va:i.depthFunc(i.GEQUAL);break;case Ga:i.depthFunc(i.GREATER);break;case Ha:i.depthFunc(i.NOTEQUAL);break;default:i.depthFunc(i.LEQUAL)}_t=j}},setLocked:function(j){I=j},setClear:function(j){at!==j&&(at=j,it&&(j=1-j),i.clearDepth(j))},reset:function(){I=!1,Y=null,_t=null,at=null,it=!1}}}function s(){let I=!1,it=null,Y=null,_t=null,at=null,j=null,wt=null,Ot=null,be=null;return{setTest:function(ie){I||(ie?st(i.STENCIL_TEST):Rt(i.STENCIL_TEST))},setMask:function(ie){it!==ie&&!I&&(i.stencilMask(ie),it=ie)},setFunc:function(ie,jn,Bn){(Y!==ie||_t!==jn||at!==Bn)&&(i.stencilFunc(ie,jn,Bn),Y=ie,_t=jn,at=Bn)},setOp:function(ie,jn,Bn){(j!==ie||wt!==jn||Ot!==Bn)&&(i.stencilOp(ie,jn,Bn),j=ie,wt=jn,Ot=Bn)},setLocked:function(ie){I=ie},setClear:function(ie){be!==ie&&(i.clearStencil(ie),be=ie)},reset:function(){I=!1,it=null,Y=null,_t=null,at=null,j=null,wt=null,Ot=null,be=null}}}let r=new e,a=new n,o=new s,l=new WeakMap,c=new WeakMap,h={},f={},u={},d=new WeakMap,m=[],_=null,g=!1,p=null,y=null,S=null,b=null,T=null,w=null,R=null,v=new dt(0,0,0),E=0,L=!1,C=null,D=null,H=null,W=null,U=null,z=i.getParameter(i.MAX_COMBINED_TEXTURE_IMAGE_UNITS),V=!1,$=0,tt=i.getParameter(i.VERSION);tt.indexOf("WebGL")!==-1?($=parseFloat(/^WebGL (\d)/.exec(tt)[1]),V=$>=1):tt.indexOf("OpenGL ES")!==-1&&($=parseFloat(/^OpenGL ES (\d)/.exec(tt)[1]),V=$>=2);let ct=null,Mt={},St=i.getParameter(i.SCISSOR_BOX),qt=i.getParameter(i.VIEWPORT),ee=new ve().fromArray(St),kt=new ve().fromArray(qt);function J(I,it,Y,_t){let at=new Uint8Array(4),j=i.createTexture();i.bindTexture(I,j),i.texParameteri(I,i.TEXTURE_MIN_FILTER,i.NEAREST),i.texParameteri(I,i.TEXTURE_MAG_FILTER,i.NEAREST);for(let wt=0;wt<Y;wt++)I===i.TEXTURE_3D||I===i.TEXTURE_2D_ARRAY?i.texImage3D(it,0,i.RGBA,1,1,_t,0,i.RGBA,i.UNSIGNED_BYTE,at):i.texImage2D(it+wt,0,i.RGBA,1,1,0,i.RGBA,i.UNSIGNED_BYTE,at);return j}let mt={};mt[i.TEXTURE_2D]=J(i.TEXTURE_2D,i.TEXTURE_2D,1),mt[i.TEXTURE_CUBE_MAP]=J(i.TEXTURE_CUBE_MAP,i.TEXTURE_CUBE_MAP_POSITIVE_X,6),mt[i.TEXTURE_2D_ARRAY]=J(i.TEXTURE_2D_ARRAY,i.TEXTURE_2D_ARRAY,1,1),mt[i.TEXTURE_3D]=J(i.TEXTURE_3D,i.TEXTURE_3D,1,1),r.setClear(0,0,0,1),a.setClear(1),o.setClear(0),st(i.DEPTH_TEST),a.setFunc(is),Ie(!1),me(Fc),st(i.CULL_FACE),fe(wn);function st(I){h[I]!==!0&&(i.enable(I),h[I]=!0)}function Rt(I){h[I]!==!1&&(i.disable(I),h[I]=!1)}function Ut(I,it){return u[I]!==it?(i.bindFramebuffer(I,it),u[I]=it,I===i.DRAW_FRAMEBUFFER&&(u[i.FRAMEBUFFER]=it),I===i.FRAMEBUFFER&&(u[i.DRAW_FRAMEBUFFER]=it),!0):!1}function It(I,it){let Y=m,_t=!1;if(I){Y=d.get(it),Y===void 0&&(Y=[],d.set(it,Y));let at=I.textures;if(Y.length!==at.length||Y[0]!==i.COLOR_ATTACHMENT0){for(let j=0,wt=at.length;j<wt;j++)Y[j]=i.COLOR_ATTACHMENT0+j;Y.length=at.length,_t=!0}}else Y[0]!==i.BACK&&(Y[0]=i.BACK,_t=!0);_t&&i.drawBuffers(Y)}function pe(I){return _!==I?(i.useProgram(I),_=I,!0):!1}let Yt={[Ai]:i.FUNC_ADD,[sf]:i.FUNC_SUBTRACT,[rf]:i.FUNC_REVERSE_SUBTRACT};Yt[af]=i.MIN,Yt[of]=i.MAX;let ne={[lf]:i.ZERO,[cf]:i.ONE,[hf]:i.SRC_COLOR,[Fa]:i.SRC_ALPHA,[gf]:i.SRC_ALPHA_SATURATE,[pf]:i.DST_COLOR,[ff]:i.DST_ALPHA,[uf]:i.ONE_MINUS_SRC_COLOR,[Ua]:i.ONE_MINUS_SRC_ALPHA,[mf]:i.ONE_MINUS_DST_COLOR,[df]:i.ONE_MINUS_DST_ALPHA,[_f]:i.CONSTANT_COLOR,[xf]:i.ONE_MINUS_CONSTANT_COLOR,[vf]:i.CONSTANT_ALPHA,[yf]:i.ONE_MINUS_CONSTANT_ALPHA};function fe(I,it,Y,_t,at,j,wt,Ot,be,ie){if(I===wn){g===!0&&(Rt(i.BLEND),g=!1);return}if(g===!1&&(st(i.BLEND),g=!0),I!==nf){if(I!==p||ie!==L){if((y!==Ai||T!==Ai)&&(i.blendEquation(i.FUNC_ADD),y=Ai,T=Ai),ie)switch(I){case Gn:i.blendFuncSeparate(i.ONE,i.ONE_MINUS_SRC_ALPHA,i.ONE,i.ONE_MINUS_SRC_ALPHA);break;case Dn:i.blendFunc(i.ONE,i.ONE);break;case Uc:i.blendFuncSeparate(i.ZERO,i.ONE_MINUS_SRC_COLOR,i.ZERO,i.ONE);break;case Oc:i.blendFuncSeparate(i.DST_COLOR,i.ONE_MINUS_SRC_ALPHA,i.ZERO,i.ONE);break;default:Pt("WebGLState: Invalid blending: ",I);break}else switch(I){case Gn:i.blendFuncSeparate(i.SRC_ALPHA,i.ONE_MINUS_SRC_ALPHA,i.ONE,i.ONE_MINUS_SRC_ALPHA);break;case Dn:i.blendFuncSeparate(i.SRC_ALPHA,i.ONE,i.ONE,i.ONE);break;case Uc:Pt("WebGLState: SubtractiveBlending requires material.premultipliedAlpha = true");break;case Oc:Pt("WebGLState: MultiplyBlending requires material.premultipliedAlpha = true");break;default:Pt("WebGLState: Invalid blending: ",I);break}S=null,b=null,w=null,R=null,v.set(0,0,0),E=0,p=I,L=ie}return}at=at||it,j=j||Y,wt=wt||_t,(it!==y||at!==T)&&(i.blendEquationSeparate(Yt[it],Yt[at]),y=it,T=at),(Y!==S||_t!==b||j!==w||wt!==R)&&(i.blendFuncSeparate(ne[Y],ne[_t],ne[j],ne[wt]),S=Y,b=_t,w=j,R=wt),(Ot.equals(v)===!1||be!==E)&&(i.blendColor(Ot.r,Ot.g,Ot.b,be),v.copy(Ot),E=be),p=I,L=!1}function Xt(I,it){I.side===Xn?Rt(i.CULL_FACE):st(i.CULL_FACE);let Y=I.side===je;it&&(Y=!Y),Ie(Y),I.blending===Gn&&I.transparent===!1?fe(wn):fe(I.blending,I.blendEquation,I.blendSrc,I.blendDst,I.blendEquationAlpha,I.blendSrcAlpha,I.blendDstAlpha,I.blendColor,I.blendAlpha,I.premultipliedAlpha),a.setFunc(I.depthFunc),a.setTest(I.depthTest),a.setMask(I.depthWrite),r.setMask(I.colorWrite);let _t=I.stencilWrite;o.setTest(_t),_t&&(o.setMask(I.stencilWriteMask),o.setFunc(I.stencilFunc,I.stencilRef,I.stencilFuncMask),o.setOp(I.stencilFail,I.stencilZFail,I.stencilZPass)),N(I.polygonOffset,I.polygonOffsetFactor,I.polygonOffsetUnits),I.alphaToCoverage===!0?st(i.SAMPLE_ALPHA_TO_COVERAGE):Rt(i.SAMPLE_ALPHA_TO_COVERAGE)}function Ie(I){C!==I&&(I?i.frontFace(i.CW):i.frontFace(i.CCW),C=I)}function me(I){I!==Qu?(st(i.CULL_FACE),I!==D&&(I===Fc?i.cullFace(i.BACK):I===tf?i.cullFace(i.FRONT):i.cullFace(i.FRONT_AND_BACK))):Rt(i.CULL_FACE),D=I}function un(I){I!==H&&(V&&i.lineWidth(I),H=I)}function N(I,it,Y){I?(st(i.POLYGON_OFFSET_FILL),(W!==it||U!==Y)&&(W=it,U=Y,a.getReversed()&&(it=-it),i.polygonOffset(it,Y))):Rt(i.POLYGON_OFFSET_FILL)}function Le(I){I?st(i.SCISSOR_TEST):Rt(i.SCISSOR_TEST)}function Zt(I){I===void 0&&(I=i.TEXTURE0+z-1),ct!==I&&(i.activeTexture(I),ct=I)}function he(I,it,Y){Y===void 0&&(ct===null?Y=i.TEXTURE0+z-1:Y=ct);let _t=Mt[Y];_t===void 0&&(_t={type:void 0,texture:void 0},Mt[Y]=_t),(_t.type!==I||_t.texture!==it)&&(ct!==Y&&(i.activeTexture(Y),ct=Y),i.bindTexture(I,it||mt[I]),_t.type=I,_t.texture=it)}function ht(){let I=Mt[ct];I!==void 0&&I.type!==void 0&&(i.bindTexture(I.type,null),I.type=void 0,I.texture=void 0)}function _e(){try{i.compressedTexImage2D(...arguments)}catch(I){Pt("WebGLState:",I)}}function A(){try{i.compressedTexImage3D(...arguments)}catch(I){Pt("WebGLState:",I)}}function x(){try{i.texSubImage2D(...arguments)}catch(I){Pt("WebGLState:",I)}}function O(){try{i.texSubImage3D(...arguments)}catch(I){Pt("WebGLState:",I)}}function Z(){try{i.compressedTexSubImage2D(...arguments)}catch(I){Pt("WebGLState:",I)}}function Q(){try{i.compressedTexSubImage3D(...arguments)}catch(I){Pt("WebGLState:",I)}}function et(){try{i.texStorage2D(...arguments)}catch(I){Pt("WebGLState:",I)}}function lt(){try{i.texStorage3D(...arguments)}catch(I){Pt("WebGLState:",I)}}function X(){try{i.texImage2D(...arguments)}catch(I){Pt("WebGLState:",I)}}function K(){try{i.texImage3D(...arguments)}catch(I){Pt("WebGLState:",I)}}function gt(I){return f[I]!==void 0?f[I]:i.getParameter(I)}function vt(I,it){f[I]!==it&&(i.pixelStorei(I,it),f[I]=it)}function rt(I){ee.equals(I)===!1&&(i.scissor(I.x,I.y,I.z,I.w),ee.copy(I))}function nt(I){kt.equals(I)===!1&&(i.viewport(I.x,I.y,I.z,I.w),kt.copy(I))}function Dt(I,it){let Y=c.get(it);Y===void 0&&(Y=new WeakMap,c.set(it,Y));let _t=Y.get(I);_t===void 0&&(_t=i.getUniformBlockIndex(it,I.name),Y.set(I,_t))}function zt(I,it){let _t=c.get(it).get(I);l.get(it)!==_t&&(i.uniformBlockBinding(it,_t,I.__bindingPointIndex),l.set(it,_t))}function $t(){i.disable(i.BLEND),i.disable(i.CULL_FACE),i.disable(i.DEPTH_TEST),i.disable(i.POLYGON_OFFSET_FILL),i.disable(i.SCISSOR_TEST),i.disable(i.STENCIL_TEST),i.disable(i.SAMPLE_ALPHA_TO_COVERAGE),i.blendEquation(i.FUNC_ADD),i.blendFunc(i.ONE,i.ZERO),i.blendFuncSeparate(i.ONE,i.ZERO,i.ONE,i.ZERO),i.blendColor(0,0,0,0),i.colorMask(!0,!0,!0,!0),i.clearColor(0,0,0,0),i.depthMask(!0),i.depthFunc(i.LESS),a.setReversed(!1),i.clearDepth(1),i.stencilMask(4294967295),i.stencilFunc(i.ALWAYS,0,4294967295),i.stencilOp(i.KEEP,i.KEEP,i.KEEP),i.clearStencil(0),i.cullFace(i.BACK),i.frontFace(i.CCW),i.polygonOffset(0,0),i.activeTexture(i.TEXTURE0),i.bindFramebuffer(i.FRAMEBUFFER,null),i.bindFramebuffer(i.DRAW_FRAMEBUFFER,null),i.bindFramebuffer(i.READ_FRAMEBUFFER,null),i.useProgram(null),i.lineWidth(1),i.scissor(0,0,i.canvas.width,i.canvas.height),i.viewport(0,0,i.canvas.width,i.canvas.height),i.pixelStorei(i.PACK_ALIGNMENT,4),i.pixelStorei(i.UNPACK_ALIGNMENT,4),i.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,!1),i.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,!1),i.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,i.BROWSER_DEFAULT_WEBGL),i.pixelStorei(i.PACK_ROW_LENGTH,0),i.pixelStorei(i.PACK_SKIP_PIXELS,0),i.pixelStorei(i.PACK_SKIP_ROWS,0),i.pixelStorei(i.UNPACK_ROW_LENGTH,0),i.pixelStorei(i.UNPACK_IMAGE_HEIGHT,0),i.pixelStorei(i.UNPACK_SKIP_PIXELS,0),i.pixelStorei(i.UNPACK_SKIP_ROWS,0),i.pixelStorei(i.UNPACK_SKIP_IMAGES,0),h={},f={},ct=null,Mt={},u={},d=new WeakMap,m=[],_=null,g=!1,p=null,y=null,S=null,b=null,T=null,w=null,R=null,v=new dt(0,0,0),E=0,L=!1,C=null,D=null,H=null,W=null,U=null,ee.set(0,0,i.canvas.width,i.canvas.height),kt.set(0,0,i.canvas.width,i.canvas.height),r.reset(),a.reset(),o.reset()}return{buffers:{color:r,depth:a,stencil:o},enable:st,disable:Rt,bindFramebuffer:Ut,drawBuffers:It,useProgram:pe,setBlending:fe,setMaterial:Xt,setFlipSided:Ie,setCullFace:me,setLineWidth:un,setPolygonOffset:N,setScissorTest:Le,activeTexture:Zt,bindTexture:he,unbindTexture:ht,compressedTexImage2D:_e,compressedTexImage3D:A,texImage2D:X,texImage3D:K,pixelStorei:vt,getParameter:gt,updateUBOMapping:Dt,uniformBlockBinding:zt,texStorage2D:et,texStorage3D:lt,texSubImage2D:x,texSubImage3D:O,compressedTexSubImage2D:Z,compressedTexSubImage3D:Q,scissor:rt,viewport:nt,reset:$t}}function cy(i,t,e,n,s,r,a){let o=t.has("WEBGL_multisampled_render_to_texture")?t.get("WEBGL_multisampled_render_to_texture"):null,l=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),c=new Et,h=new WeakMap,f=new Set,u,d=new WeakMap,m=!1;try{m=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function _(A,x){return m?new OffscreenCanvas(A,x):pr("canvas")}function g(A,x,O){let Z=1,Q=_e(A);if((Q.width>O||Q.height>O)&&(Z=O/Math.max(Q.width,Q.height)),Z<1)if(typeof HTMLImageElement<"u"&&A instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&A instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&A instanceof ImageBitmap||typeof VideoFrame<"u"&&A instanceof VideoFrame){let et=Math.floor(Z*Q.width),lt=Math.floor(Z*Q.height);u===void 0&&(u=_(et,lt));let X=x?_(et,lt):u;return X.width=et,X.height=lt,X.getContext("2d").drawImage(A,0,0,et,lt),Ct("WebGLRenderer: Texture has been resized from ("+Q.width+"x"+Q.height+") to ("+et+"x"+lt+")."),X}else return"data"in A&&Ct("WebGLRenderer: Image in DataTexture is too big ("+Q.width+"x"+Q.height+")."),A;return A}function p(A){return A.generateMipmaps}function y(A){i.generateMipmap(A)}function S(A){return A.isWebGLCubeRenderTarget?i.TEXTURE_CUBE_MAP:A.isWebGL3DRenderTarget?i.TEXTURE_3D:A.isWebGLArrayRenderTarget||A.isCompressedArrayTexture?i.TEXTURE_2D_ARRAY:i.TEXTURE_2D}function b(A,x,O,Z,Q,et=!1){if(A!==null){if(i[A]!==void 0)return i[A];Ct("WebGLRenderer: Attempt to use non-existing WebGL internal format '"+A+"'")}let lt;Z&&(lt=t.get("EXT_texture_norm16"),lt||Ct("WebGLRenderer: Unable to use normalized textures without EXT_texture_norm16 extension"));let X=x;if(x===i.RED&&(O===i.FLOAT&&(X=i.R32F),O===i.HALF_FLOAT&&(X=i.R16F),O===i.UNSIGNED_BYTE&&(X=i.R8),O===i.UNSIGNED_SHORT&&lt&&(X=lt.R16_EXT),O===i.SHORT&&lt&&(X=lt.R16_SNORM_EXT)),x===i.RED_INTEGER&&(O===i.UNSIGNED_BYTE&&(X=i.R8UI),O===i.UNSIGNED_SHORT&&(X=i.R16UI),O===i.UNSIGNED_INT&&(X=i.R32UI),O===i.BYTE&&(X=i.R8I),O===i.SHORT&&(X=i.R16I),O===i.INT&&(X=i.R32I)),x===i.RG&&(O===i.FLOAT&&(X=i.RG32F),O===i.HALF_FLOAT&&(X=i.RG16F),O===i.UNSIGNED_BYTE&&(X=i.RG8),O===i.UNSIGNED_SHORT&&lt&&(X=lt.RG16_EXT),O===i.SHORT&&lt&&(X=lt.RG16_SNORM_EXT)),x===i.RG_INTEGER&&(O===i.UNSIGNED_BYTE&&(X=i.RG8UI),O===i.UNSIGNED_SHORT&&(X=i.RG16UI),O===i.UNSIGNED_INT&&(X=i.RG32UI),O===i.BYTE&&(X=i.RG8I),O===i.SHORT&&(X=i.RG16I),O===i.INT&&(X=i.RG32I)),x===i.RGB_INTEGER&&(O===i.UNSIGNED_BYTE&&(X=i.RGB8UI),O===i.UNSIGNED_SHORT&&(X=i.RGB16UI),O===i.UNSIGNED_INT&&(X=i.RGB32UI),O===i.BYTE&&(X=i.RGB8I),O===i.SHORT&&(X=i.RGB16I),O===i.INT&&(X=i.RGB32I)),x===i.RGBA_INTEGER&&(O===i.UNSIGNED_BYTE&&(X=i.RGBA8UI),O===i.UNSIGNED_SHORT&&(X=i.RGBA16UI),O===i.UNSIGNED_INT&&(X=i.RGBA32UI),O===i.BYTE&&(X=i.RGBA8I),O===i.SHORT&&(X=i.RGBA16I),O===i.INT&&(X=i.RGBA32I)),x===i.RGB&&(O===i.UNSIGNED_SHORT&&lt&&(X=lt.RGB16_EXT),O===i.SHORT&&lt&&(X=lt.RGB16_SNORM_EXT),O===i.UNSIGNED_INT_5_9_9_9_REV&&(X=i.RGB9_E5),O===i.UNSIGNED_INT_10F_11F_11F_REV&&(X=i.R11F_G11F_B10F)),x===i.RGBA){let K=et?fr:Wt.getTransfer(Q);O===i.FLOAT&&(X=i.RGBA32F),O===i.HALF_FLOAT&&(X=i.RGBA16F),O===i.UNSIGNED_BYTE&&(X=K===jt?i.SRGB8_ALPHA8:i.RGBA8),O===i.UNSIGNED_SHORT&&lt&&(X=lt.RGBA16_EXT),O===i.SHORT&&lt&&(X=lt.RGBA16_SNORM_EXT),O===i.UNSIGNED_SHORT_4_4_4_4&&(X=i.RGBA4),O===i.UNSIGNED_SHORT_5_5_5_1&&(X=i.RGB5_A1)}return(X===i.R16F||X===i.R32F||X===i.RG16F||X===i.RG32F||X===i.RGBA16F||X===i.RGBA32F)&&t.get("EXT_color_buffer_float"),X}function T(A,x){let O;return A?x===null||x===Fn||x===Vs?O=i.DEPTH24_STENCIL8:x===Un?O=i.DEPTH32F_STENCIL8:x===zs&&(O=i.DEPTH24_STENCIL8,Ct("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):x===null||x===Fn||x===Vs?O=i.DEPTH_COMPONENT24:x===Un?O=i.DEPTH_COMPONENT32F:x===zs&&(O=i.DEPTH_COMPONENT16),O}function w(A,x){return p(A)===!0||A.isFramebufferTexture&&A.minFilter!==Be&&A.minFilter!==Ge?Math.log2(Math.max(x.width,x.height))+1:A.mipmaps!==void 0&&A.mipmaps.length>0?A.mipmaps.length:A.isCompressedTexture&&Array.isArray(A.image)?x.mipmaps.length:1}function R(A){let x=A.target;x.removeEventListener("dispose",R),E(x),x.isVideoTexture&&h.delete(x),x.isHTMLTexture&&f.delete(x)}function v(A){let x=A.target;x.removeEventListener("dispose",v),C(x)}function E(A){let x=n.get(A);if(x.__webglInit===void 0)return;let O=A.source,Z=d.get(O);if(Z){let Q=Z[x.__cacheKey];Q.usedTimes--,Q.usedTimes===0&&L(A),Object.keys(Z).length===0&&d.delete(O)}n.remove(A)}function L(A){let x=n.get(A);i.deleteTexture(x.__webglTexture);let O=A.source,Z=d.get(O);delete Z[x.__cacheKey],a.memory.textures--}function C(A){let x=n.get(A);if(A.depthTexture&&(A.depthTexture.dispose(),n.remove(A.depthTexture)),A.isWebGLCubeRenderTarget)for(let Z=0;Z<6;Z++){if(Array.isArray(x.__webglFramebuffer[Z]))for(let Q=0;Q<x.__webglFramebuffer[Z].length;Q++)i.deleteFramebuffer(x.__webglFramebuffer[Z][Q]);else i.deleteFramebuffer(x.__webglFramebuffer[Z]);x.__webglDepthbuffer&&i.deleteRenderbuffer(x.__webglDepthbuffer[Z])}else{if(Array.isArray(x.__webglFramebuffer))for(let Z=0;Z<x.__webglFramebuffer.length;Z++)i.deleteFramebuffer(x.__webglFramebuffer[Z]);else i.deleteFramebuffer(x.__webglFramebuffer);if(x.__webglDepthbuffer&&i.deleteRenderbuffer(x.__webglDepthbuffer),x.__webglMultisampledFramebuffer&&i.deleteFramebuffer(x.__webglMultisampledFramebuffer),x.__webglColorRenderbuffer)for(let Z=0;Z<x.__webglColorRenderbuffer.length;Z++)x.__webglColorRenderbuffer[Z]&&i.deleteRenderbuffer(x.__webglColorRenderbuffer[Z]);x.__webglDepthRenderbuffer&&i.deleteRenderbuffer(x.__webglDepthRenderbuffer)}let O=A.textures;for(let Z=0,Q=O.length;Z<Q;Z++){let et=n.get(O[Z]);et.__webglTexture&&(i.deleteTexture(et.__webglTexture),a.memory.textures--),n.remove(O[Z])}n.remove(A)}let D=0;function H(){D=0}function W(){return D}function U(A){D=A}function z(){let A=D;return A>=s.maxTextures&&Ct("WebGLTextures: Trying to use "+A+" texture units while this GPU supports only "+s.maxTextures),D+=1,A}function V(A){let x=[];return x.push(A.wrapS),x.push(A.wrapT),x.push(A.wrapR||0),x.push(A.magFilter),x.push(A.minFilter),x.push(A.anisotropy),x.push(A.internalFormat),x.push(A.format),x.push(A.type),x.push(A.generateMipmaps),x.push(A.premultiplyAlpha),x.push(A.flipY),x.push(A.unpackAlignment),x.push(A.colorSpace),x.join()}function $(A,x){let O=n.get(A);if(A.isVideoTexture&&he(A),A.isRenderTargetTexture===!1&&A.isExternalTexture!==!0&&A.version>0&&O.__version!==A.version){let Z=A.image;if(Z===null)Ct("WebGLRenderer: Texture marked for update but no image data found.");else if(Z.complete===!1)Ct("WebGLRenderer: Texture marked for update but image is incomplete");else{Rt(O,A,x);return}}else A.isExternalTexture&&(O.__webglTexture=A.sourceTexture?A.sourceTexture:null);e.bindTexture(i.TEXTURE_2D,O.__webglTexture,i.TEXTURE0+x)}function tt(A,x){let O=n.get(A);if(A.isRenderTargetTexture===!1&&A.version>0&&O.__version!==A.version){Rt(O,A,x);return}else A.isExternalTexture&&(O.__webglTexture=A.sourceTexture?A.sourceTexture:null);e.bindTexture(i.TEXTURE_2D_ARRAY,O.__webglTexture,i.TEXTURE0+x)}function ct(A,x){let O=n.get(A);if(A.isRenderTargetTexture===!1&&A.version>0&&O.__version!==A.version){Rt(O,A,x);return}e.bindTexture(i.TEXTURE_3D,O.__webglTexture,i.TEXTURE0+x)}function Mt(A,x){let O=n.get(A);if(A.isCubeDepthTexture!==!0&&A.version>0&&O.__version!==A.version){Ut(O,A,x);return}e.bindTexture(i.TEXTURE_CUBE_MAP,O.__webglTexture,i.TEXTURE0+x)}let St={[Wa]:i.REPEAT,[Vn]:i.CLAMP_TO_EDGE,[Xa]:i.MIRRORED_REPEAT},qt={[Be]:i.NEAREST,[Sf]:i.NEAREST_MIPMAP_NEAREST,[Br]:i.NEAREST_MIPMAP_LINEAR,[Ge]:i.LINEAR,[bo]:i.LINEAR_MIPMAP_NEAREST,[Ui]:i.LINEAR_MIPMAP_LINEAR},ee={[Tf]:i.NEVER,[If]:i.ALWAYS,[Ef]:i.LESS,[rl]:i.LEQUAL,[Cf]:i.EQUAL,[al]:i.GEQUAL,[Rf]:i.GREATER,[Pf]:i.NOTEQUAL};function kt(A,x){if(x.type===Un&&t.has("OES_texture_float_linear")===!1&&(x.magFilter===Ge||x.magFilter===bo||x.magFilter===Br||x.magFilter===Ui||x.minFilter===Ge||x.minFilter===bo||x.minFilter===Br||x.minFilter===Ui)&&Ct("WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),i.texParameteri(A,i.TEXTURE_WRAP_S,St[x.wrapS]),i.texParameteri(A,i.TEXTURE_WRAP_T,St[x.wrapT]),(A===i.TEXTURE_3D||A===i.TEXTURE_2D_ARRAY)&&i.texParameteri(A,i.TEXTURE_WRAP_R,St[x.wrapR]),i.texParameteri(A,i.TEXTURE_MAG_FILTER,qt[x.magFilter]),i.texParameteri(A,i.TEXTURE_MIN_FILTER,qt[x.minFilter]),x.compareFunction&&(i.texParameteri(A,i.TEXTURE_COMPARE_MODE,i.COMPARE_REF_TO_TEXTURE),i.texParameteri(A,i.TEXTURE_COMPARE_FUNC,ee[x.compareFunction])),t.has("EXT_texture_filter_anisotropic")===!0){if(x.magFilter===Be||x.minFilter!==Br&&x.minFilter!==Ui||x.type===Un&&t.has("OES_texture_float_linear")===!1)return;if(x.anisotropy>1||n.get(x).__currentAnisotropy){let O=t.get("EXT_texture_filter_anisotropic");i.texParameterf(A,O.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(x.anisotropy,s.getMaxAnisotropy())),n.get(x).__currentAnisotropy=x.anisotropy}}}function J(A,x){let O=!1;A.__webglInit===void 0&&(A.__webglInit=!0,x.addEventListener("dispose",R));let Z=x.source,Q=d.get(Z);Q===void 0&&(Q={},d.set(Z,Q));let et=V(x);if(et!==A.__cacheKey){Q[et]===void 0&&(Q[et]={texture:i.createTexture(),usedTimes:0},a.memory.textures++,O=!0),Q[et].usedTimes++;let lt=Q[A.__cacheKey];lt!==void 0&&(Q[A.__cacheKey].usedTimes--,lt.usedTimes===0&&L(x)),A.__cacheKey=et,A.__webglTexture=Q[et].texture}return O}function mt(A,x,O){return Math.floor(Math.floor(A/O)/x)}function st(A,x,O,Z){let et=A.updateRanges;if(et.length===0)e.texSubImage2D(i.TEXTURE_2D,0,0,0,x.width,x.height,O,Z,x.data);else{et.sort((vt,rt)=>vt.start-rt.start);let lt=0;for(let vt=1;vt<et.length;vt++){let rt=et[lt],nt=et[vt],Dt=rt.start+rt.count,zt=mt(nt.start,x.width,4),$t=mt(rt.start,x.width,4);nt.start<=Dt+1&&zt===$t&&mt(nt.start+nt.count-1,x.width,4)===zt?rt.count=Math.max(rt.count,nt.start+nt.count-rt.start):(++lt,et[lt]=nt)}et.length=lt+1;let X=e.getParameter(i.UNPACK_ROW_LENGTH),K=e.getParameter(i.UNPACK_SKIP_PIXELS),gt=e.getParameter(i.UNPACK_SKIP_ROWS);e.pixelStorei(i.UNPACK_ROW_LENGTH,x.width);for(let vt=0,rt=et.length;vt<rt;vt++){let nt=et[vt],Dt=Math.floor(nt.start/4),zt=Math.ceil(nt.count/4),$t=Dt%x.width,I=Math.floor(Dt/x.width),it=zt,Y=1;e.pixelStorei(i.UNPACK_SKIP_PIXELS,$t),e.pixelStorei(i.UNPACK_SKIP_ROWS,I),e.texSubImage2D(i.TEXTURE_2D,0,$t,I,it,Y,O,Z,x.data)}A.clearUpdateRanges(),e.pixelStorei(i.UNPACK_ROW_LENGTH,X),e.pixelStorei(i.UNPACK_SKIP_PIXELS,K),e.pixelStorei(i.UNPACK_SKIP_ROWS,gt)}}function Rt(A,x,O){let Z=i.TEXTURE_2D;(x.isDataArrayTexture||x.isCompressedArrayTexture)&&(Z=i.TEXTURE_2D_ARRAY),x.isData3DTexture&&(Z=i.TEXTURE_3D);let Q=J(A,x),et=x.source;e.bindTexture(Z,A.__webglTexture,i.TEXTURE0+O);let lt=n.get(et);if(et.version!==lt.__version||Q===!0){if(e.activeTexture(i.TEXTURE0+O),(typeof ImageBitmap<"u"&&x.image instanceof ImageBitmap)===!1){let Y=Wt.getPrimaries(Wt.workingColorSpace),_t=x.colorSpace===ui?null:Wt.getPrimaries(x.colorSpace),at=x.colorSpace===ui||Y===_t?i.NONE:i.BROWSER_DEFAULT_WEBGL;e.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,x.flipY),e.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,x.premultiplyAlpha),e.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,at)}e.pixelStorei(i.UNPACK_ALIGNMENT,x.unpackAlignment);let K=g(x.image,!1,s.maxTextureSize);K=ht(x,K);let gt=r.convert(x.format,x.colorSpace),vt=r.convert(x.type),rt=b(x.internalFormat,gt,vt,x.normalized,x.colorSpace,x.isVideoTexture);kt(Z,x);let nt,Dt=x.mipmaps,zt=x.isVideoTexture!==!0,$t=lt.__version===void 0||Q===!0,I=et.dataReady,it=w(x,K);if(x.isDepthTexture)rt=T(x.format===Oi,x.type),$t&&(zt?e.texStorage2D(i.TEXTURE_2D,1,rt,K.width,K.height):e.texImage2D(i.TEXTURE_2D,0,rt,K.width,K.height,0,gt,vt,null));else if(x.isDataTexture)if(Dt.length>0){zt&&$t&&e.texStorage2D(i.TEXTURE_2D,it,rt,Dt[0].width,Dt[0].height);for(let Y=0,_t=Dt.length;Y<_t;Y++)nt=Dt[Y],zt?I&&e.texSubImage2D(i.TEXTURE_2D,Y,0,0,nt.width,nt.height,gt,vt,nt.data):e.texImage2D(i.TEXTURE_2D,Y,rt,nt.width,nt.height,0,gt,vt,nt.data);x.generateMipmaps=!1}else zt?($t&&e.texStorage2D(i.TEXTURE_2D,it,rt,K.width,K.height),I&&st(x,K,gt,vt)):e.texImage2D(i.TEXTURE_2D,0,rt,K.width,K.height,0,gt,vt,K.data);else if(x.isCompressedTexture)if(x.isCompressedArrayTexture){zt&&$t&&e.texStorage3D(i.TEXTURE_2D_ARRAY,it,rt,Dt[0].width,Dt[0].height,K.depth);for(let Y=0,_t=Dt.length;Y<_t;Y++)if(nt=Dt[Y],x.format!==An)if(gt!==null)if(zt){if(I)if(x.layerUpdates.size>0){let at=nh(nt.width,nt.height,x.format,x.type);for(let j of x.layerUpdates){let wt=nt.data.subarray(j*at/nt.data.BYTES_PER_ELEMENT,(j+1)*at/nt.data.BYTES_PER_ELEMENT);e.compressedTexSubImage3D(i.TEXTURE_2D_ARRAY,Y,0,0,j,nt.width,nt.height,1,gt,wt)}x.clearLayerUpdates()}else e.compressedTexSubImage3D(i.TEXTURE_2D_ARRAY,Y,0,0,0,nt.width,nt.height,K.depth,gt,nt.data)}else e.compressedTexImage3D(i.TEXTURE_2D_ARRAY,Y,rt,nt.width,nt.height,K.depth,0,nt.data,0,0);else Ct("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else zt?I&&e.texSubImage3D(i.TEXTURE_2D_ARRAY,Y,0,0,0,nt.width,nt.height,K.depth,gt,vt,nt.data):e.texImage3D(i.TEXTURE_2D_ARRAY,Y,rt,nt.width,nt.height,K.depth,0,gt,vt,nt.data)}else{zt&&$t&&e.texStorage2D(i.TEXTURE_2D,it,rt,Dt[0].width,Dt[0].height);for(let Y=0,_t=Dt.length;Y<_t;Y++)nt=Dt[Y],x.format!==An?gt!==null?zt?I&&e.compressedTexSubImage2D(i.TEXTURE_2D,Y,0,0,nt.width,nt.height,gt,nt.data):e.compressedTexImage2D(i.TEXTURE_2D,Y,rt,nt.width,nt.height,0,nt.data):Ct("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):zt?I&&e.texSubImage2D(i.TEXTURE_2D,Y,0,0,nt.width,nt.height,gt,vt,nt.data):e.texImage2D(i.TEXTURE_2D,Y,rt,nt.width,nt.height,0,gt,vt,nt.data)}else if(x.isDataArrayTexture)if(zt){if($t&&e.texStorage3D(i.TEXTURE_2D_ARRAY,it,rt,K.width,K.height,K.depth),I)if(x.layerUpdates.size>0){let Y=nh(K.width,K.height,x.format,x.type);for(let _t of x.layerUpdates){let at=K.data.subarray(_t*Y/K.data.BYTES_PER_ELEMENT,(_t+1)*Y/K.data.BYTES_PER_ELEMENT);e.texSubImage3D(i.TEXTURE_2D_ARRAY,0,0,0,_t,K.width,K.height,1,gt,vt,at)}x.clearLayerUpdates()}else e.texSubImage3D(i.TEXTURE_2D_ARRAY,0,0,0,0,K.width,K.height,K.depth,gt,vt,K.data)}else e.texImage3D(i.TEXTURE_2D_ARRAY,0,rt,K.width,K.height,K.depth,0,gt,vt,K.data);else if(x.isData3DTexture)zt?($t&&e.texStorage3D(i.TEXTURE_3D,it,rt,K.width,K.height,K.depth),I&&e.texSubImage3D(i.TEXTURE_3D,0,0,0,0,K.width,K.height,K.depth,gt,vt,K.data)):e.texImage3D(i.TEXTURE_3D,0,rt,K.width,K.height,K.depth,0,gt,vt,K.data);else if(x.isFramebufferTexture){if($t)if(zt)e.texStorage2D(i.TEXTURE_2D,it,rt,K.width,K.height);else{let Y=K.width,_t=K.height;for(let at=0;at<it;at++)e.texImage2D(i.TEXTURE_2D,at,rt,Y,_t,0,gt,vt,null),Y>>=1,_t>>=1}}else if(x.isHTMLTexture){if("texElementImage2D"in i){let Y=i.canvas;if(Y.hasAttribute("layoutsubtree")||Y.setAttribute("layoutsubtree","true"),K.parentNode!==Y){Y.appendChild(K),f.add(x),Y.onpaint=Ot=>{let be=Ot.changedElements;for(let ie of f)be.includes(ie.image)&&(ie.needsUpdate=!0)},Y.requestPaint();return}let _t=0,at=i.RGBA,j=i.RGBA,wt=i.UNSIGNED_BYTE;i.texElementImage2D(i.TEXTURE_2D,_t,at,j,wt,K),i.texParameteri(i.TEXTURE_2D,i.TEXTURE_MIN_FILTER,i.LINEAR),i.texParameteri(i.TEXTURE_2D,i.TEXTURE_WRAP_S,i.CLAMP_TO_EDGE),i.texParameteri(i.TEXTURE_2D,i.TEXTURE_WRAP_T,i.CLAMP_TO_EDGE)}}else if(Dt.length>0){if(zt&&$t){let Y=_e(Dt[0]);e.texStorage2D(i.TEXTURE_2D,it,rt,Y.width,Y.height)}for(let Y=0,_t=Dt.length;Y<_t;Y++)nt=Dt[Y],zt?I&&e.texSubImage2D(i.TEXTURE_2D,Y,0,0,gt,vt,nt):e.texImage2D(i.TEXTURE_2D,Y,rt,gt,vt,nt);x.generateMipmaps=!1}else if(zt){if($t){let Y=_e(K);e.texStorage2D(i.TEXTURE_2D,it,rt,Y.width,Y.height)}I&&e.texSubImage2D(i.TEXTURE_2D,0,0,0,gt,vt,K)}else e.texImage2D(i.TEXTURE_2D,0,rt,gt,vt,K);p(x)&&y(Z),lt.__version=et.version,x.onUpdate&&x.onUpdate(x)}A.__version=x.version}function Ut(A,x,O){if(x.image.length!==6)return;let Z=J(A,x),Q=x.source;e.bindTexture(i.TEXTURE_CUBE_MAP,A.__webglTexture,i.TEXTURE0+O);let et=n.get(Q);if(Q.version!==et.__version||Z===!0){e.activeTexture(i.TEXTURE0+O);let lt=Wt.getPrimaries(Wt.workingColorSpace),X=x.colorSpace===ui?null:Wt.getPrimaries(x.colorSpace),K=x.colorSpace===ui||lt===X?i.NONE:i.BROWSER_DEFAULT_WEBGL;e.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,x.flipY),e.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,x.premultiplyAlpha),e.pixelStorei(i.UNPACK_ALIGNMENT,x.unpackAlignment),e.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,K);let gt=x.isCompressedTexture||x.image[0].isCompressedTexture,vt=x.image[0]&&x.image[0].isDataTexture,rt=[];for(let j=0;j<6;j++)!gt&&!vt?rt[j]=g(x.image[j],!0,s.maxCubemapSize):rt[j]=vt?x.image[j].image:x.image[j],rt[j]=ht(x,rt[j]);let nt=rt[0],Dt=r.convert(x.format,x.colorSpace),zt=r.convert(x.type),$t=b(x.internalFormat,Dt,zt,x.normalized,x.colorSpace),I=x.isVideoTexture!==!0,it=et.__version===void 0||Z===!0,Y=Q.dataReady,_t=w(x,nt);kt(i.TEXTURE_CUBE_MAP,x);let at;if(gt){I&&it&&e.texStorage2D(i.TEXTURE_CUBE_MAP,_t,$t,nt.width,nt.height);for(let j=0;j<6;j++){at=rt[j].mipmaps;for(let wt=0;wt<at.length;wt++){let Ot=at[wt];x.format!==An?Dt!==null?I?Y&&e.compressedTexSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,wt,0,0,Ot.width,Ot.height,Dt,Ot.data):e.compressedTexImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,wt,$t,Ot.width,Ot.height,0,Ot.data):Ct("WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):I?Y&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,wt,0,0,Ot.width,Ot.height,Dt,zt,Ot.data):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,wt,$t,Ot.width,Ot.height,0,Dt,zt,Ot.data)}}}else{if(at=x.mipmaps,I&&it){at.length>0&&_t++;let j=_e(rt[0]);e.texStorage2D(i.TEXTURE_CUBE_MAP,_t,$t,j.width,j.height)}for(let j=0;j<6;j++)if(vt){I?Y&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,0,0,0,rt[j].width,rt[j].height,Dt,zt,rt[j].data):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,0,$t,rt[j].width,rt[j].height,0,Dt,zt,rt[j].data);for(let wt=0;wt<at.length;wt++){let be=at[wt].image[j].image;I?Y&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,wt+1,0,0,be.width,be.height,Dt,zt,be.data):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,wt+1,$t,be.width,be.height,0,Dt,zt,be.data)}}else{I?Y&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,0,0,0,Dt,zt,rt[j]):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,0,$t,Dt,zt,rt[j]);for(let wt=0;wt<at.length;wt++){let Ot=at[wt];I?Y&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,wt+1,0,0,Dt,zt,Ot.image[j]):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+j,wt+1,$t,Dt,zt,Ot.image[j])}}}p(x)&&y(i.TEXTURE_CUBE_MAP),et.__version=Q.version,x.onUpdate&&x.onUpdate(x)}A.__version=x.version}function It(A,x,O,Z,Q,et){let lt=r.convert(O.format,O.colorSpace),X=r.convert(O.type),K=b(O.internalFormat,lt,X,O.normalized,O.colorSpace),gt=n.get(x),vt=n.get(O);if(vt.__renderTarget=x,!gt.__hasExternalTextures){let rt=Math.max(1,x.width>>et),nt=Math.max(1,x.height>>et);Q===i.TEXTURE_3D||Q===i.TEXTURE_2D_ARRAY?e.texImage3D(Q,et,K,rt,nt,x.depth,0,lt,X,null):e.texImage2D(Q,et,K,rt,nt,0,lt,X,null)}e.bindFramebuffer(i.FRAMEBUFFER,A),Zt(x)?o.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,Z,Q,vt.__webglTexture,0,Le(x)):(Q===i.TEXTURE_2D||Q>=i.TEXTURE_CUBE_MAP_POSITIVE_X&&Q<=i.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&i.framebufferTexture2D(i.FRAMEBUFFER,Z,Q,vt.__webglTexture,et),e.bindFramebuffer(i.FRAMEBUFFER,null)}function pe(A,x,O){if(i.bindRenderbuffer(i.RENDERBUFFER,A),x.depthBuffer){let Z=x.depthTexture,Q=Z&&Z.isDepthTexture?Z.type:null,et=T(x.stencilBuffer,Q),lt=x.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;Zt(x)?o.renderbufferStorageMultisampleEXT(i.RENDERBUFFER,Le(x),et,x.width,x.height):O?i.renderbufferStorageMultisample(i.RENDERBUFFER,Le(x),et,x.width,x.height):i.renderbufferStorage(i.RENDERBUFFER,et,x.width,x.height),i.framebufferRenderbuffer(i.FRAMEBUFFER,lt,i.RENDERBUFFER,A)}else{let Z=x.textures;for(let Q=0;Q<Z.length;Q++){let et=Z[Q],lt=r.convert(et.format,et.colorSpace),X=r.convert(et.type),K=b(et.internalFormat,lt,X,et.normalized,et.colorSpace);Zt(x)?o.renderbufferStorageMultisampleEXT(i.RENDERBUFFER,Le(x),K,x.width,x.height):O?i.renderbufferStorageMultisample(i.RENDERBUFFER,Le(x),K,x.width,x.height):i.renderbufferStorage(i.RENDERBUFFER,K,x.width,x.height)}}i.bindRenderbuffer(i.RENDERBUFFER,null)}function Yt(A,x,O){let Z=x.isWebGLCubeRenderTarget===!0;if(e.bindFramebuffer(i.FRAMEBUFFER,A),!(x.depthTexture&&x.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");let Q=n.get(x.depthTexture);if(Q.__renderTarget=x,(!Q.__webglTexture||x.depthTexture.image.width!==x.width||x.depthTexture.image.height!==x.height)&&(x.depthTexture.image.width=x.width,x.depthTexture.image.height=x.height,x.depthTexture.needsUpdate=!0),Z){if(Q.__webglInit===void 0&&(Q.__webglInit=!0,x.depthTexture.addEventListener("dispose",R)),Q.__webglTexture===void 0){Q.__webglTexture=i.createTexture(),e.bindTexture(i.TEXTURE_CUBE_MAP,Q.__webglTexture),kt(i.TEXTURE_CUBE_MAP,x.depthTexture);let gt=r.convert(x.depthTexture.format),vt=r.convert(x.depthTexture.type),rt;x.depthTexture.format===Hn?rt=i.DEPTH_COMPONENT24:x.depthTexture.format===Oi&&(rt=i.DEPTH24_STENCIL8);for(let nt=0;nt<6;nt++)i.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+nt,0,rt,x.width,x.height,0,gt,vt,null)}}else $(x.depthTexture,0);let et=Q.__webglTexture,lt=Le(x),X=Z?i.TEXTURE_CUBE_MAP_POSITIVE_X+O:i.TEXTURE_2D,K=x.depthTexture.format===Oi?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;if(x.depthTexture.format===Hn)Zt(x)?o.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,K,X,et,0,lt):i.framebufferTexture2D(i.FRAMEBUFFER,K,X,et,0);else if(x.depthTexture.format===Oi)Zt(x)?o.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,K,X,et,0,lt):i.framebufferTexture2D(i.FRAMEBUFFER,K,X,et,0);else throw new Error("Unknown depthTexture format")}function ne(A){let x=n.get(A),O=A.isWebGLCubeRenderTarget===!0;if(x.__boundDepthTexture!==A.depthTexture){let Z=A.depthTexture;if(x.__depthDisposeCallback&&x.__depthDisposeCallback(),Z){let Q=()=>{delete x.__boundDepthTexture,delete x.__depthDisposeCallback,Z.removeEventListener("dispose",Q)};Z.addEventListener("dispose",Q),x.__depthDisposeCallback=Q}x.__boundDepthTexture=Z}if(A.depthTexture&&!x.__autoAllocateDepthBuffer)if(O)for(let Z=0;Z<6;Z++)Yt(x.__webglFramebuffer[Z],A,Z);else{let Z=A.texture.mipmaps;Z&&Z.length>0?Yt(x.__webglFramebuffer[0],A,0):Yt(x.__webglFramebuffer,A,0)}else if(O){x.__webglDepthbuffer=[];for(let Z=0;Z<6;Z++)if(e.bindFramebuffer(i.FRAMEBUFFER,x.__webglFramebuffer[Z]),x.__webglDepthbuffer[Z]===void 0)x.__webglDepthbuffer[Z]=i.createRenderbuffer(),pe(x.__webglDepthbuffer[Z],A,!1);else{let Q=A.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,et=x.__webglDepthbuffer[Z];i.bindRenderbuffer(i.RENDERBUFFER,et),i.framebufferRenderbuffer(i.FRAMEBUFFER,Q,i.RENDERBUFFER,et)}}else{let Z=A.texture.mipmaps;if(Z&&Z.length>0?e.bindFramebuffer(i.FRAMEBUFFER,x.__webglFramebuffer[0]):e.bindFramebuffer(i.FRAMEBUFFER,x.__webglFramebuffer),x.__webglDepthbuffer===void 0)x.__webglDepthbuffer=i.createRenderbuffer(),pe(x.__webglDepthbuffer,A,!1);else{let Q=A.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,et=x.__webglDepthbuffer;i.bindRenderbuffer(i.RENDERBUFFER,et),i.framebufferRenderbuffer(i.FRAMEBUFFER,Q,i.RENDERBUFFER,et)}}e.bindFramebuffer(i.FRAMEBUFFER,null)}function fe(A,x,O){let Z=n.get(A);x!==void 0&&It(Z.__webglFramebuffer,A,A.texture,i.COLOR_ATTACHMENT0,i.TEXTURE_2D,0),O!==void 0&&ne(A)}function Xt(A){let x=A.texture,O=n.get(A),Z=n.get(x);A.addEventListener("dispose",v);let Q=A.textures,et=A.isWebGLCubeRenderTarget===!0,lt=Q.length>1;if(lt||(Z.__webglTexture===void 0&&(Z.__webglTexture=i.createTexture()),Z.__version=x.version,a.memory.textures++),et){O.__webglFramebuffer=[];for(let X=0;X<6;X++)if(x.mipmaps&&x.mipmaps.length>0){O.__webglFramebuffer[X]=[];for(let K=0;K<x.mipmaps.length;K++)O.__webglFramebuffer[X][K]=i.createFramebuffer()}else O.__webglFramebuffer[X]=i.createFramebuffer()}else{if(x.mipmaps&&x.mipmaps.length>0){O.__webglFramebuffer=[];for(let X=0;X<x.mipmaps.length;X++)O.__webglFramebuffer[X]=i.createFramebuffer()}else O.__webglFramebuffer=i.createFramebuffer();if(lt)for(let X=0,K=Q.length;X<K;X++){let gt=n.get(Q[X]);gt.__webglTexture===void 0&&(gt.__webglTexture=i.createTexture(),a.memory.textures++)}if(A.samples>0&&Zt(A)===!1){O.__webglMultisampledFramebuffer=i.createFramebuffer(),O.__webglColorRenderbuffer=[],e.bindFramebuffer(i.FRAMEBUFFER,O.__webglMultisampledFramebuffer);for(let X=0;X<Q.length;X++){let K=Q[X];O.__webglColorRenderbuffer[X]=i.createRenderbuffer(),i.bindRenderbuffer(i.RENDERBUFFER,O.__webglColorRenderbuffer[X]);let gt=r.convert(K.format,K.colorSpace),vt=r.convert(K.type),rt=b(K.internalFormat,gt,vt,K.normalized,K.colorSpace,A.isXRRenderTarget===!0),nt=Le(A);i.renderbufferStorageMultisample(i.RENDERBUFFER,nt,rt,A.width,A.height),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+X,i.RENDERBUFFER,O.__webglColorRenderbuffer[X])}i.bindRenderbuffer(i.RENDERBUFFER,null),A.depthBuffer&&(O.__webglDepthRenderbuffer=i.createRenderbuffer(),pe(O.__webglDepthRenderbuffer,A,!0)),e.bindFramebuffer(i.FRAMEBUFFER,null)}}if(et){e.bindTexture(i.TEXTURE_CUBE_MAP,Z.__webglTexture),kt(i.TEXTURE_CUBE_MAP,x);for(let X=0;X<6;X++)if(x.mipmaps&&x.mipmaps.length>0)for(let K=0;K<x.mipmaps.length;K++)It(O.__webglFramebuffer[X][K],A,x,i.COLOR_ATTACHMENT0,i.TEXTURE_CUBE_MAP_POSITIVE_X+X,K);else It(O.__webglFramebuffer[X],A,x,i.COLOR_ATTACHMENT0,i.TEXTURE_CUBE_MAP_POSITIVE_X+X,0);p(x)&&y(i.TEXTURE_CUBE_MAP),e.unbindTexture()}else if(lt){for(let X=0,K=Q.length;X<K;X++){let gt=Q[X],vt=n.get(gt),rt=i.TEXTURE_2D;(A.isWebGL3DRenderTarget||A.isWebGLArrayRenderTarget)&&(rt=A.isWebGL3DRenderTarget?i.TEXTURE_3D:i.TEXTURE_2D_ARRAY),e.bindTexture(rt,vt.__webglTexture),kt(rt,gt),It(O.__webglFramebuffer,A,gt,i.COLOR_ATTACHMENT0+X,rt,0),p(gt)&&y(rt)}e.unbindTexture()}else{let X=i.TEXTURE_2D;if((A.isWebGL3DRenderTarget||A.isWebGLArrayRenderTarget)&&(X=A.isWebGL3DRenderTarget?i.TEXTURE_3D:i.TEXTURE_2D_ARRAY),e.bindTexture(X,Z.__webglTexture),kt(X,x),x.mipmaps&&x.mipmaps.length>0)for(let K=0;K<x.mipmaps.length;K++)It(O.__webglFramebuffer[K],A,x,i.COLOR_ATTACHMENT0,X,K);else It(O.__webglFramebuffer,A,x,i.COLOR_ATTACHMENT0,X,0);p(x)&&y(X),e.unbindTexture()}A.depthBuffer&&ne(A)}function Ie(A){let x=A.textures;for(let O=0,Z=x.length;O<Z;O++){let Q=x[O];if(p(Q)){let et=S(A),lt=n.get(Q).__webglTexture;e.bindTexture(et,lt),y(et),e.unbindTexture()}}}let me=[],un=[];function N(A){if(A.samples>0){if(Zt(A)===!1){let x=A.textures,O=A.width,Z=A.height,Q=i.COLOR_BUFFER_BIT,et=A.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,lt=n.get(A),X=x.length>1;if(X)for(let gt=0;gt<x.length;gt++)e.bindFramebuffer(i.FRAMEBUFFER,lt.__webglMultisampledFramebuffer),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+gt,i.RENDERBUFFER,null),e.bindFramebuffer(i.FRAMEBUFFER,lt.__webglFramebuffer),i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0+gt,i.TEXTURE_2D,null,0);e.bindFramebuffer(i.READ_FRAMEBUFFER,lt.__webglMultisampledFramebuffer);let K=A.texture.mipmaps;K&&K.length>0?e.bindFramebuffer(i.DRAW_FRAMEBUFFER,lt.__webglFramebuffer[0]):e.bindFramebuffer(i.DRAW_FRAMEBUFFER,lt.__webglFramebuffer);for(let gt=0;gt<x.length;gt++){if(A.resolveDepthBuffer&&(A.depthBuffer&&(Q|=i.DEPTH_BUFFER_BIT),A.stencilBuffer&&A.resolveStencilBuffer&&(Q|=i.STENCIL_BUFFER_BIT)),X){i.framebufferRenderbuffer(i.READ_FRAMEBUFFER,i.COLOR_ATTACHMENT0,i.RENDERBUFFER,lt.__webglColorRenderbuffer[gt]);let vt=n.get(x[gt]).__webglTexture;i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0,i.TEXTURE_2D,vt,0)}i.blitFramebuffer(0,0,O,Z,0,0,O,Z,Q,i.NEAREST),l===!0&&(me.length=0,un.length=0,me.push(i.COLOR_ATTACHMENT0+gt),A.depthBuffer&&A.resolveDepthBuffer===!1&&(me.push(et),un.push(et),i.invalidateFramebuffer(i.DRAW_FRAMEBUFFER,un)),i.invalidateFramebuffer(i.READ_FRAMEBUFFER,me))}if(e.bindFramebuffer(i.READ_FRAMEBUFFER,null),e.bindFramebuffer(i.DRAW_FRAMEBUFFER,null),X)for(let gt=0;gt<x.length;gt++){e.bindFramebuffer(i.FRAMEBUFFER,lt.__webglMultisampledFramebuffer),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+gt,i.RENDERBUFFER,lt.__webglColorRenderbuffer[gt]);let vt=n.get(x[gt]).__webglTexture;e.bindFramebuffer(i.FRAMEBUFFER,lt.__webglFramebuffer),i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0+gt,i.TEXTURE_2D,vt,0)}e.bindFramebuffer(i.DRAW_FRAMEBUFFER,lt.__webglMultisampledFramebuffer)}else if(A.depthBuffer&&A.resolveDepthBuffer===!1&&l){let x=A.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;i.invalidateFramebuffer(i.DRAW_FRAMEBUFFER,[x])}}}function Le(A){return Math.min(s.maxSamples,A.samples)}function Zt(A){let x=n.get(A);return A.samples>0&&t.has("WEBGL_multisampled_render_to_texture")===!0&&x.__useRenderToTexture!==!1}function he(A){let x=a.render.frame;h.get(A)!==x&&(h.set(A,x),A.update())}function ht(A,x){let O=A.colorSpace,Z=A.format,Q=A.type;return A.isCompressedTexture===!0||A.isVideoTexture===!0||O!==ur&&O!==ui&&(Wt.getTransfer(O)===jt?(Z!==An||Q!==vn)&&Ct("WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):Pt("WebGLTextures: Unsupported texture color space:",O)),x}function _e(A){return typeof HTMLImageElement<"u"&&A instanceof HTMLImageElement?(c.width=A.naturalWidth||A.width,c.height=A.naturalHeight||A.height):typeof VideoFrame<"u"&&A instanceof VideoFrame?(c.width=A.displayWidth,c.height=A.displayHeight):(c.width=A.width,c.height=A.height),c}this.allocateTextureUnit=z,this.resetTextureUnits=H,this.getTextureUnits=W,this.setTextureUnits=U,this.setTexture2D=$,this.setTexture2DArray=tt,this.setTexture3D=ct,this.setTextureCube=Mt,this.rebindTextures=fe,this.setupRenderTarget=Xt,this.updateRenderTargetMipmap=Ie,this.updateMultisampleRenderTarget=N,this.setupDepthRenderbuffer=ne,this.setupFrameBufferTexture=It,this.useMultisampledRTT=Zt,this.isReversedDepthBuffer=function(){return e.buffers.depth.getReversed()}}function hy(i,t){function e(n,s=ui){let r,a=Wt.getTransfer(s);if(n===vn)return i.UNSIGNED_BYTE;if(n===wo)return i.UNSIGNED_SHORT_4_4_4_4;if(n===Ao)return i.UNSIGNED_SHORT_5_5_5_1;if(n===Gc)return i.UNSIGNED_INT_5_9_9_9_REV;if(n===Hc)return i.UNSIGNED_INT_10F_11F_11F_REV;if(n===zc)return i.BYTE;if(n===Vc)return i.SHORT;if(n===zs)return i.UNSIGNED_SHORT;if(n===So)return i.INT;if(n===Fn)return i.UNSIGNED_INT;if(n===Un)return i.FLOAT;if(n===Ze)return i.HALF_FLOAT;if(n===Wc)return i.ALPHA;if(n===Xc)return i.RGB;if(n===An)return i.RGBA;if(n===Hn)return i.DEPTH_COMPONENT;if(n===Oi)return i.DEPTH_STENCIL;if(n===qc)return i.RED;if(n===To)return i.RED_INTEGER;if(n===Bi)return i.RG;if(n===Eo)return i.RG_INTEGER;if(n===Co)return i.RGBA_INTEGER;if(n===kr||n===zr||n===Vr||n===Gr)if(a===jt)if(r=t.get("WEBGL_compressed_texture_s3tc_srgb"),r!==null){if(n===kr)return r.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(n===zr)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(n===Vr)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(n===Gr)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(r=t.get("WEBGL_compressed_texture_s3tc"),r!==null){if(n===kr)return r.COMPRESSED_RGB_S3TC_DXT1_EXT;if(n===zr)return r.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(n===Vr)return r.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(n===Gr)return r.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(n===Ro||n===Po||n===Io||n===Lo)if(r=t.get("WEBGL_compressed_texture_pvrtc"),r!==null){if(n===Ro)return r.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(n===Po)return r.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(n===Io)return r.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(n===Lo)return r.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(n===No||n===Do||n===Fo||n===Uo||n===Oo||n===Hr||n===Bo)if(r=t.get("WEBGL_compressed_texture_etc"),r!==null){if(n===No||n===Do)return a===jt?r.COMPRESSED_SRGB8_ETC2:r.COMPRESSED_RGB8_ETC2;if(n===Fo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:r.COMPRESSED_RGBA8_ETC2_EAC;if(n===Uo)return r.COMPRESSED_R11_EAC;if(n===Oo)return r.COMPRESSED_SIGNED_R11_EAC;if(n===Hr)return r.COMPRESSED_RG11_EAC;if(n===Bo)return r.COMPRESSED_SIGNED_RG11_EAC}else return null;if(n===ko||n===zo||n===Vo||n===Go||n===Ho||n===Wo||n===Xo||n===qo||n===Yo||n===Zo||n===Ko||n===Jo||n===$o||n===jo)if(r=t.get("WEBGL_compressed_texture_astc"),r!==null){if(n===ko)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:r.COMPRESSED_RGBA_ASTC_4x4_KHR;if(n===zo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:r.COMPRESSED_RGBA_ASTC_5x4_KHR;if(n===Vo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:r.COMPRESSED_RGBA_ASTC_5x5_KHR;if(n===Go)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:r.COMPRESSED_RGBA_ASTC_6x5_KHR;if(n===Ho)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:r.COMPRESSED_RGBA_ASTC_6x6_KHR;if(n===Wo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:r.COMPRESSED_RGBA_ASTC_8x5_KHR;if(n===Xo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:r.COMPRESSED_RGBA_ASTC_8x6_KHR;if(n===qo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:r.COMPRESSED_RGBA_ASTC_8x8_KHR;if(n===Yo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:r.COMPRESSED_RGBA_ASTC_10x5_KHR;if(n===Zo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:r.COMPRESSED_RGBA_ASTC_10x6_KHR;if(n===Ko)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:r.COMPRESSED_RGBA_ASTC_10x8_KHR;if(n===Jo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:r.COMPRESSED_RGBA_ASTC_10x10_KHR;if(n===$o)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:r.COMPRESSED_RGBA_ASTC_12x10_KHR;if(n===jo)return a===jt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:r.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(n===Qo||n===tl||n===el)if(r=t.get("EXT_texture_compression_bptc"),r!==null){if(n===Qo)return a===jt?r.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:r.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(n===tl)return r.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(n===el)return r.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(n===nl||n===il||n===Wr||n===sl)if(r=t.get("EXT_texture_compression_rgtc"),r!==null){if(n===nl)return r.COMPRESSED_RED_RGTC1_EXT;if(n===il)return r.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(n===Wr)return r.COMPRESSED_RED_GREEN_RGTC2_EXT;if(n===sl)return r.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return n===Vs?i.UNSIGNED_INT_24_8:i[n]!==void 0?i[n]:null}return{convert:e}}var uy=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,fy=`
uniform sampler2DArray depthColor;
uniform float depthWidth;
uniform float depthHeight;

void main() {

	vec2 coord = vec2( gl_FragCoord.x / depthWidth, gl_FragCoord.y / depthHeight );

	if ( coord.x >= 1.0 ) {

		gl_FragDepth = texture( depthColor, vec3( coord.x - 1.0, coord.y, 1 ) ).r;

	} else {

		gl_FragDepth = texture( depthColor, vec3( coord.x, coord.y, 0 ) ).r;

	}

}`,Mh=class{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(t,e){if(this.texture===null){let n=new br(t.texture);(t.depthNear!==e.depthNear||t.depthFar!==e.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=n}}getMesh(t){if(this.texture!==null&&this.mesh===null){let e=t.cameras[0].viewport,n=new re({vertexShader:uy,fragmentShader:fy,uniforms:{depthColor:{value:this.texture},depthWidth:{value:e.z},depthHeight:{value:e.w}}});this.mesh=new rn(new wr(20,20),n)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}},bh=class extends Ln{constructor(t,e){super();let n=this,s=null,r=1,a=null,o="local-floor",l=1,c=null,h=null,f=null,u=null,d=null,m=null,_=typeof XRWebGLBinding<"u",g=new Mh,p={},y=e.getContextAttributes(),S=null,b=null,T=[],w=[],R=new Et,v=null,E=new Ye;E.viewport=new ve;let L=new Ye;L.viewport=new ve;let C=[E,L],D=new _o,H=null,W=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(J){let mt=T[J];return mt===void 0&&(mt=new Us,T[J]=mt),mt.getTargetRaySpace()},this.getControllerGrip=function(J){let mt=T[J];return mt===void 0&&(mt=new Us,T[J]=mt),mt.getGripSpace()},this.getHand=function(J){let mt=T[J];return mt===void 0&&(mt=new Us,T[J]=mt),mt.getHandSpace()};function U(J){let mt=w.indexOf(J.inputSource);if(mt===-1)return;let st=T[mt];st!==void 0&&(st.update(J.inputSource,J.frame,c||a),st.dispatchEvent({type:J.type,data:J.inputSource}))}function z(){s.removeEventListener("select",U),s.removeEventListener("selectstart",U),s.removeEventListener("selectend",U),s.removeEventListener("squeeze",U),s.removeEventListener("squeezestart",U),s.removeEventListener("squeezeend",U),s.removeEventListener("end",z),s.removeEventListener("inputsourceschange",V);for(let J=0;J<T.length;J++){let mt=w[J];mt!==null&&(w[J]=null,T[J].disconnect(mt))}H=null,W=null,g.reset();for(let J in p)delete p[J];t.setRenderTarget(S),d=null,u=null,f=null,s=null,b=null,kt.stop(),n.isPresenting=!1,t.setPixelRatio(v),t.setSize(R.width,R.height,!1),n.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(J){r=J,n.isPresenting===!0&&Ct("WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(J){o=J,n.isPresenting===!0&&Ct("WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return c||a},this.setReferenceSpace=function(J){c=J},this.getBaseLayer=function(){return u!==null?u:d},this.getBinding=function(){return f===null&&_&&(f=new XRWebGLBinding(s,e)),f},this.getFrame=function(){return m},this.getSession=function(){return s},this.setSession=async function(J){if(s=J,s!==null){if(S=t.getRenderTarget(),s.addEventListener("select",U),s.addEventListener("selectstart",U),s.addEventListener("selectend",U),s.addEventListener("squeeze",U),s.addEventListener("squeezestart",U),s.addEventListener("squeezeend",U),s.addEventListener("end",z),s.addEventListener("inputsourceschange",V),y.xrCompatible!==!0&&await e.makeXRCompatible(),v=t.getPixelRatio(),t.getSize(R),_&&"createProjectionLayer"in XRWebGLBinding.prototype){let st=null,Rt=null,Ut=null;y.depth&&(Ut=y.stencil?e.DEPTH24_STENCIL8:e.DEPTH_COMPONENT24,st=y.stencil?Oi:Hn,Rt=y.stencil?Vs:Fn);let It={colorFormat:e.RGBA8,depthFormat:Ut,scaleFactor:r};f=this.getBinding(),u=f.createProjectionLayer(It),s.updateRenderState({layers:[u]}),t.setPixelRatio(1),t.setSize(u.textureWidth,u.textureHeight,!1),b=new Ne(u.textureWidth,u.textureHeight,{format:An,type:vn,depthTexture:new hi(u.textureWidth,u.textureHeight,Rt,void 0,void 0,void 0,void 0,void 0,void 0,st),stencilBuffer:y.stencil,colorSpace:t.outputColorSpace,samples:y.antialias?4:0,resolveDepthBuffer:u.ignoreDepthValues===!1,resolveStencilBuffer:u.ignoreDepthValues===!1})}else{let st={antialias:y.antialias,alpha:!0,depth:y.depth,stencil:y.stencil,framebufferScaleFactor:r};d=new XRWebGLLayer(s,e,st),s.updateRenderState({baseLayer:d}),t.setPixelRatio(1),t.setSize(d.framebufferWidth,d.framebufferHeight,!1),b=new Ne(d.framebufferWidth,d.framebufferHeight,{format:An,type:vn,colorSpace:t.outputColorSpace,stencilBuffer:y.stencil,resolveDepthBuffer:d.ignoreDepthValues===!1,resolveStencilBuffer:d.ignoreDepthValues===!1})}b.isXRRenderTarget=!0,this.setFoveation(l),c=null,a=await s.requestReferenceSpace(o),kt.setContext(s),kt.start(),n.isPresenting=!0,n.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(s!==null)return s.environmentBlendMode},this.getDepthTexture=function(){return g.getDepthTexture()};function V(J){for(let mt=0;mt<J.removed.length;mt++){let st=J.removed[mt],Rt=w.indexOf(st);Rt>=0&&(w[Rt]=null,T[Rt].disconnect(st))}for(let mt=0;mt<J.added.length;mt++){let st=J.added[mt],Rt=w.indexOf(st);if(Rt===-1){for(let It=0;It<T.length;It++)if(It>=w.length){w.push(st),Rt=It;break}else if(w[It]===null){w[It]=st,Rt=It;break}if(Rt===-1)break}let Ut=T[Rt];Ut&&Ut.connect(st)}}let $=new P,tt=new P;function ct(J,mt,st){$.setFromMatrixPosition(mt.matrixWorld),tt.setFromMatrixPosition(st.matrixWorld);let Rt=$.distanceTo(tt),Ut=mt.projectionMatrix.elements,It=st.projectionMatrix.elements,pe=Ut[14]/(Ut[10]-1),Yt=Ut[14]/(Ut[10]+1),ne=(Ut[9]+1)/Ut[5],fe=(Ut[9]-1)/Ut[5],Xt=(Ut[8]-1)/Ut[0],Ie=(It[8]+1)/It[0],me=pe*Xt,un=pe*Ie,N=Rt/(-Xt+Ie),Le=N*-Xt;if(mt.matrixWorld.decompose(J.position,J.quaternion,J.scale),J.translateX(Le),J.translateZ(N),J.matrixWorld.compose(J.position,J.quaternion,J.scale),J.matrixWorldInverse.copy(J.matrixWorld).invert(),Ut[10]===-1)J.projectionMatrix.copy(mt.projectionMatrix),J.projectionMatrixInverse.copy(mt.projectionMatrixInverse);else{let Zt=pe+N,he=Yt+N,ht=me-Le,_e=un+(Rt-Le),A=ne*Yt/he*Zt,x=fe*Yt/he*Zt;J.projectionMatrix.makePerspective(ht,_e,A,x,Zt,he),J.projectionMatrixInverse.copy(J.projectionMatrix).invert()}}function Mt(J,mt){mt===null?J.matrixWorld.copy(J.matrix):J.matrixWorld.multiplyMatrices(mt.matrixWorld,J.matrix),J.matrixWorldInverse.copy(J.matrixWorld).invert()}this.updateCamera=function(J){if(s===null)return;let mt=J.near,st=J.far;g.texture!==null&&(g.depthNear>0&&(mt=g.depthNear),g.depthFar>0&&(st=g.depthFar)),D.near=L.near=E.near=mt,D.far=L.far=E.far=st,(H!==D.near||W!==D.far)&&(s.updateRenderState({depthNear:D.near,depthFar:D.far}),H=D.near,W=D.far),D.layers.mask=J.layers.mask|6,E.layers.mask=D.layers.mask&-5,L.layers.mask=D.layers.mask&-3;let Rt=J.parent,Ut=D.cameras;Mt(D,Rt);for(let It=0;It<Ut.length;It++)Mt(Ut[It],Rt);Ut.length===2?ct(D,E,L):D.projectionMatrix.copy(E.projectionMatrix),St(J,D,Rt)};function St(J,mt,st){st===null?J.matrix.copy(mt.matrixWorld):(J.matrix.copy(st.matrixWorld),J.matrix.invert(),J.matrix.multiply(mt.matrixWorld)),J.matrix.decompose(J.position,J.quaternion,J.scale),J.updateMatrixWorld(!0),J.projectionMatrix.copy(mt.projectionMatrix),J.projectionMatrixInverse.copy(mt.projectionMatrixInverse),J.isPerspectiveCamera&&(J.fov=Ds*2*Math.atan(1/J.projectionMatrix.elements[5]),J.zoom=1)}this.getCamera=function(){return D},this.getFoveation=function(){if(!(u===null&&d===null))return l},this.setFoveation=function(J){l=J,u!==null&&(u.fixedFoveation=J),d!==null&&d.fixedFoveation!==void 0&&(d.fixedFoveation=J)},this.hasDepthSensing=function(){return g.texture!==null},this.getDepthSensingMesh=function(){return g.getMesh(D)},this.getCameraTexture=function(J){return p[J]};let qt=null;function ee(J,mt){if(h=mt.getViewerPose(c||a),m=mt,h!==null){let st=h.views;d!==null&&(t.setRenderTargetFramebuffer(b,d.framebuffer),t.setRenderTarget(b));let Rt=!1;st.length!==D.cameras.length&&(D.cameras.length=0,Rt=!0);for(let Yt=0;Yt<st.length;Yt++){let ne=st[Yt],fe=null;if(d!==null)fe=d.getViewport(ne);else{let Ie=f.getViewSubImage(u,ne);fe=Ie.viewport,Yt===0&&(t.setRenderTargetTextures(b,Ie.colorTexture,Ie.depthStencilTexture),t.setRenderTarget(b))}let Xt=C[Yt];Xt===void 0&&(Xt=new Ye,Xt.layers.enable(Yt),Xt.viewport=new ve,C[Yt]=Xt),Xt.matrix.fromArray(ne.transform.matrix),Xt.matrix.decompose(Xt.position,Xt.quaternion,Xt.scale),Xt.projectionMatrix.fromArray(ne.projectionMatrix),Xt.projectionMatrixInverse.copy(Xt.projectionMatrix).invert(),Xt.viewport.set(fe.x,fe.y,fe.width,fe.height),Yt===0&&(D.matrix.copy(Xt.matrix),D.matrix.decompose(D.position,D.quaternion,D.scale)),Rt===!0&&D.cameras.push(Xt)}let Ut=s.enabledFeatures;if(Ut&&Ut.includes("depth-sensing")&&s.depthUsage=="gpu-optimized"&&_){f=n.getBinding();let Yt=f.getDepthInformation(st[0]);Yt&&Yt.isValid&&Yt.texture&&g.init(Yt,s.renderState)}if(Ut&&Ut.includes("camera-access")&&_){t.state.unbindTexture(),f=n.getBinding();for(let Yt=0;Yt<st.length;Yt++){let ne=st[Yt].camera;if(ne){let fe=p[ne];fe||(fe=new br,p[ne]=fe);let Xt=f.getCameraImage(ne);fe.sourceTexture=Xt}}}}for(let st=0;st<T.length;st++){let Rt=w[st],Ut=T[st];Rt!==null&&Ut!==void 0&&Ut.update(Rt,mt,c||a)}qt&&qt(J,mt),mt.detectedPlanes&&n.dispatchEvent({type:"planesdetected",data:mt}),m=null}let kt=new ad;kt.setAnimationLoop(ee),this.setAnimationLoop=function(J){qt=J},this.dispose=function(){}}},dy=new ge,fd=new Ft;fd.set(-1,0,0,0,1,0,0,0,1);function py(i,t){function e(g,p){g.matrixAutoUpdate===!0&&g.updateMatrix(),p.value.copy(g.matrix)}function n(g,p){p.color.getRGB(g.fogColor.value,Qc(i)),p.isFog?(g.fogNear.value=p.near,g.fogFar.value=p.far):p.isFogExp2&&(g.fogDensity.value=p.density)}function s(g,p,y,S,b){p.isNodeMaterial?p.uniformsNeedUpdate=!1:p.isMeshBasicMaterial?r(g,p):p.isMeshLambertMaterial?(r(g,p),p.envMap&&(g.envMapIntensity.value=p.envMapIntensity)):p.isMeshToonMaterial?(r(g,p),f(g,p)):p.isMeshPhongMaterial?(r(g,p),h(g,p),p.envMap&&(g.envMapIntensity.value=p.envMapIntensity)):p.isMeshStandardMaterial?(r(g,p),u(g,p),p.isMeshPhysicalMaterial&&d(g,p,b)):p.isMeshMatcapMaterial?(r(g,p),m(g,p)):p.isMeshDepthMaterial?r(g,p):p.isMeshDistanceMaterial?(r(g,p),_(g,p)):p.isMeshNormalMaterial?r(g,p):p.isLineBasicMaterial?(a(g,p),p.isLineDashedMaterial&&o(g,p)):p.isPointsMaterial?l(g,p,y,S):p.isSpriteMaterial?c(g,p):p.isShadowMaterial?(g.color.value.copy(p.color),g.opacity.value=p.opacity):p.isShaderMaterial&&(p.uniformsNeedUpdate=!1)}function r(g,p){g.opacity.value=p.opacity,p.color&&g.diffuse.value.copy(p.color),p.emissive&&g.emissive.value.copy(p.emissive).multiplyScalar(p.emissiveIntensity),p.map&&(g.map.value=p.map,e(p.map,g.mapTransform)),p.alphaMap&&(g.alphaMap.value=p.alphaMap,e(p.alphaMap,g.alphaMapTransform)),p.bumpMap&&(g.bumpMap.value=p.bumpMap,e(p.bumpMap,g.bumpMapTransform),g.bumpScale.value=p.bumpScale,p.side===je&&(g.bumpScale.value*=-1)),p.normalMap&&(g.normalMap.value=p.normalMap,e(p.normalMap,g.normalMapTransform),g.normalScale.value.copy(p.normalScale),p.side===je&&g.normalScale.value.negate()),p.displacementMap&&(g.displacementMap.value=p.displacementMap,e(p.displacementMap,g.displacementMapTransform),g.displacementScale.value=p.displacementScale,g.displacementBias.value=p.displacementBias),p.emissiveMap&&(g.emissiveMap.value=p.emissiveMap,e(p.emissiveMap,g.emissiveMapTransform)),p.specularMap&&(g.specularMap.value=p.specularMap,e(p.specularMap,g.specularMapTransform)),p.alphaTest>0&&(g.alphaTest.value=p.alphaTest);let y=t.get(p),S=y.envMap,b=y.envMapRotation;S&&(g.envMap.value=S,g.envMapRotation.value.setFromMatrix4(dy.makeRotationFromEuler(b)).transpose(),S.isCubeTexture&&S.isRenderTargetTexture===!1&&g.envMapRotation.value.premultiply(fd),g.reflectivity.value=p.reflectivity,g.ior.value=p.ior,g.refractionRatio.value=p.refractionRatio),p.lightMap&&(g.lightMap.value=p.lightMap,g.lightMapIntensity.value=p.lightMapIntensity,e(p.lightMap,g.lightMapTransform)),p.aoMap&&(g.aoMap.value=p.aoMap,g.aoMapIntensity.value=p.aoMapIntensity,e(p.aoMap,g.aoMapTransform))}function a(g,p){g.diffuse.value.copy(p.color),g.opacity.value=p.opacity,p.map&&(g.map.value=p.map,e(p.map,g.mapTransform))}function o(g,p){g.dashSize.value=p.dashSize,g.totalSize.value=p.dashSize+p.gapSize,g.scale.value=p.scale}function l(g,p,y,S){g.diffuse.value.copy(p.color),g.opacity.value=p.opacity,g.size.value=p.size*y,g.scale.value=S*.5,p.map&&(g.map.value=p.map,e(p.map,g.uvTransform)),p.alphaMap&&(g.alphaMap.value=p.alphaMap,e(p.alphaMap,g.alphaMapTransform)),p.alphaTest>0&&(g.alphaTest.value=p.alphaTest)}function c(g,p){g.diffuse.value.copy(p.color),g.opacity.value=p.opacity,g.rotation.value=p.rotation,p.map&&(g.map.value=p.map,e(p.map,g.mapTransform)),p.alphaMap&&(g.alphaMap.value=p.alphaMap,e(p.alphaMap,g.alphaMapTransform)),p.alphaTest>0&&(g.alphaTest.value=p.alphaTest)}function h(g,p){g.specular.value.copy(p.specular),g.shininess.value=Math.max(p.shininess,1e-4)}function f(g,p){p.gradientMap&&(g.gradientMap.value=p.gradientMap)}function u(g,p){g.metalness.value=p.metalness,p.metalnessMap&&(g.metalnessMap.value=p.metalnessMap,e(p.metalnessMap,g.metalnessMapTransform)),g.roughness.value=p.roughness,p.roughnessMap&&(g.roughnessMap.value=p.roughnessMap,e(p.roughnessMap,g.roughnessMapTransform)),p.envMap&&(g.envMapIntensity.value=p.envMapIntensity)}function d(g,p,y){g.ior.value=p.ior,p.sheen>0&&(g.sheenColor.value.copy(p.sheenColor).multiplyScalar(p.sheen),g.sheenRoughness.value=p.sheenRoughness,p.sheenColorMap&&(g.sheenColorMap.value=p.sheenColorMap,e(p.sheenColorMap,g.sheenColorMapTransform)),p.sheenRoughnessMap&&(g.sheenRoughnessMap.value=p.sheenRoughnessMap,e(p.sheenRoughnessMap,g.sheenRoughnessMapTransform))),p.clearcoat>0&&(g.clearcoat.value=p.clearcoat,g.clearcoatRoughness.value=p.clearcoatRoughness,p.clearcoatMap&&(g.clearcoatMap.value=p.clearcoatMap,e(p.clearcoatMap,g.clearcoatMapTransform)),p.clearcoatRoughnessMap&&(g.clearcoatRoughnessMap.value=p.clearcoatRoughnessMap,e(p.clearcoatRoughnessMap,g.clearcoatRoughnessMapTransform)),p.clearcoatNormalMap&&(g.clearcoatNormalMap.value=p.clearcoatNormalMap,e(p.clearcoatNormalMap,g.clearcoatNormalMapTransform),g.clearcoatNormalScale.value.copy(p.clearcoatNormalScale),p.side===je&&g.clearcoatNormalScale.value.negate())),p.dispersion>0&&(g.dispersion.value=p.dispersion),p.iridescence>0&&(g.iridescence.value=p.iridescence,g.iridescenceIOR.value=p.iridescenceIOR,g.iridescenceThicknessMinimum.value=p.iridescenceThicknessRange[0],g.iridescenceThicknessMaximum.value=p.iridescenceThicknessRange[1],p.iridescenceMap&&(g.iridescenceMap.value=p.iridescenceMap,e(p.iridescenceMap,g.iridescenceMapTransform)),p.iridescenceThicknessMap&&(g.iridescenceThicknessMap.value=p.iridescenceThicknessMap,e(p.iridescenceThicknessMap,g.iridescenceThicknessMapTransform))),p.transmission>0&&(g.transmission.value=p.transmission,g.transmissionSamplerMap.value=y.texture,g.transmissionSamplerSize.value.set(y.width,y.height),p.transmissionMap&&(g.transmissionMap.value=p.transmissionMap,e(p.transmissionMap,g.transmissionMapTransform)),g.thickness.value=p.thickness,p.thicknessMap&&(g.thicknessMap.value=p.thicknessMap,e(p.thicknessMap,g.thicknessMapTransform)),g.attenuationDistance.value=p.attenuationDistance,g.attenuationColor.value.copy(p.attenuationColor)),p.anisotropy>0&&(g.anisotropyVector.value.set(p.anisotropy*Math.cos(p.anisotropyRotation),p.anisotropy*Math.sin(p.anisotropyRotation)),p.anisotropyMap&&(g.anisotropyMap.value=p.anisotropyMap,e(p.anisotropyMap,g.anisotropyMapTransform))),g.specularIntensity.value=p.specularIntensity,g.specularColor.value.copy(p.specularColor),p.specularColorMap&&(g.specularColorMap.value=p.specularColorMap,e(p.specularColorMap,g.specularColorMapTransform)),p.specularIntensityMap&&(g.specularIntensityMap.value=p.specularIntensityMap,e(p.specularIntensityMap,g.specularIntensityMapTransform))}function m(g,p){p.matcap&&(g.matcap.value=p.matcap)}function _(g,p){let y=t.get(p).light;g.referencePosition.value.setFromMatrixPosition(y.matrixWorld),g.nearDistance.value=y.shadow.camera.near,g.farDistance.value=y.shadow.camera.far}return{refreshFogUniforms:n,refreshMaterialUniforms:s}}function my(i,t,e,n){let s={},r={},a=[],o=i.getParameter(i.MAX_UNIFORM_BUFFER_BINDINGS);function l(y,S){let b=S.program;n.uniformBlockBinding(y,b)}function c(y,S){let b=s[y.id];b===void 0&&(m(y),b=h(y),s[y.id]=b,y.addEventListener("dispose",g));let T=S.program;n.updateUBOMapping(y,T);let w=t.render.frame;r[y.id]!==w&&(u(y),r[y.id]=w)}function h(y){let S=f();y.__bindingPointIndex=S;let b=i.createBuffer(),T=y.__size,w=y.usage;return i.bindBuffer(i.UNIFORM_BUFFER,b),i.bufferData(i.UNIFORM_BUFFER,T,w),i.bindBuffer(i.UNIFORM_BUFFER,null),i.bindBufferBase(i.UNIFORM_BUFFER,S,b),b}function f(){for(let y=0;y<o;y++)if(a.indexOf(y)===-1)return a.push(y),y;return Pt("WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function u(y){let S=s[y.id],b=y.uniforms,T=y.__cache;i.bindBuffer(i.UNIFORM_BUFFER,S);for(let w=0,R=b.length;w<R;w++){let v=Array.isArray(b[w])?b[w]:[b[w]];for(let E=0,L=v.length;E<L;E++){let C=v[E];if(d(C,w,E,T)===!0){let D=C.__offset,H=Array.isArray(C.value)?C.value:[C.value],W=0;for(let U=0;U<H.length;U++){let z=H[U],V=_(z);typeof z=="number"||typeof z=="boolean"?(C.__data[0]=z,i.bufferSubData(i.UNIFORM_BUFFER,D+W,C.__data)):z.isMatrix3?(C.__data[0]=z.elements[0],C.__data[1]=z.elements[1],C.__data[2]=z.elements[2],C.__data[3]=0,C.__data[4]=z.elements[3],C.__data[5]=z.elements[4],C.__data[6]=z.elements[5],C.__data[7]=0,C.__data[8]=z.elements[6],C.__data[9]=z.elements[7],C.__data[10]=z.elements[8],C.__data[11]=0):ArrayBuffer.isView(z)?C.__data.set(new z.constructor(z.buffer,z.byteOffset,C.__data.length)):(z.toArray(C.__data,W),W+=V.storage/Float32Array.BYTES_PER_ELEMENT)}i.bufferSubData(i.UNIFORM_BUFFER,D,C.__data)}}}i.bindBuffer(i.UNIFORM_BUFFER,null)}function d(y,S,b,T){let w=y.value,R=S+"_"+b;if(T[R]===void 0)return typeof w=="number"||typeof w=="boolean"?T[R]=w:ArrayBuffer.isView(w)?T[R]=w.slice():T[R]=w.clone(),!0;{let v=T[R];if(typeof w=="number"||typeof w=="boolean"){if(v!==w)return T[R]=w,!0}else{if(ArrayBuffer.isView(w))return!0;if(v.equals(w)===!1)return v.copy(w),!0}}return!1}function m(y){let S=y.uniforms,b=0,T=16;for(let R=0,v=S.length;R<v;R++){let E=Array.isArray(S[R])?S[R]:[S[R]];for(let L=0,C=E.length;L<C;L++){let D=E[L],H=Array.isArray(D.value)?D.value:[D.value];for(let W=0,U=H.length;W<U;W++){let z=H[W],V=_(z),$=b%T,tt=$%V.boundary,ct=$+tt;b+=tt,ct!==0&&T-ct<V.storage&&(b+=T-ct),D.__data=new Float32Array(V.storage/Float32Array.BYTES_PER_ELEMENT),D.__offset=b,b+=V.storage}}}let w=b%T;return w>0&&(b+=T-w),y.__size=b,y.__cache={},this}function _(y){let S={boundary:0,storage:0};return typeof y=="number"||typeof y=="boolean"?(S.boundary=4,S.storage=4):y.isVector2?(S.boundary=8,S.storage=8):y.isVector3||y.isColor?(S.boundary=16,S.storage=12):y.isVector4?(S.boundary=16,S.storage=16):y.isMatrix3?(S.boundary=48,S.storage=48):y.isMatrix4?(S.boundary=64,S.storage=64):y.isTexture?Ct("WebGLRenderer: Texture samplers can not be part of an uniforms group."):ArrayBuffer.isView(y)?(S.boundary=16,S.storage=y.byteLength):Ct("WebGLRenderer: Unsupported uniform value type.",y),S}function g(y){let S=y.target;S.removeEventListener("dispose",g);let b=a.indexOf(S.__bindingPointIndex);a.splice(b,1),i.deleteBuffer(s[S.id]),delete s[S.id],delete r[S.id]}function p(){for(let y in s)i.deleteBuffer(s[y]);a=[],s={},r={}}return{bind:l,update:c,dispose:p}}var gy=new Uint16Array([12469,15057,12620,14925,13266,14620,13807,14376,14323,13990,14545,13625,14713,13328,14840,12882,14931,12528,14996,12233,15039,11829,15066,11525,15080,11295,15085,10976,15082,10705,15073,10495,13880,14564,13898,14542,13977,14430,14158,14124,14393,13732,14556,13410,14702,12996,14814,12596,14891,12291,14937,11834,14957,11489,14958,11194,14943,10803,14921,10506,14893,10278,14858,9960,14484,14039,14487,14025,14499,13941,14524,13740,14574,13468,14654,13106,14743,12678,14818,12344,14867,11893,14889,11509,14893,11180,14881,10751,14852,10428,14812,10128,14765,9754,14712,9466,14764,13480,14764,13475,14766,13440,14766,13347,14769,13070,14786,12713,14816,12387,14844,11957,14860,11549,14868,11215,14855,10751,14825,10403,14782,10044,14729,9651,14666,9352,14599,9029,14967,12835,14966,12831,14963,12804,14954,12723,14936,12564,14917,12347,14900,11958,14886,11569,14878,11247,14859,10765,14828,10401,14784,10011,14727,9600,14660,9289,14586,8893,14508,8533,15111,12234,15110,12234,15104,12216,15092,12156,15067,12010,15028,11776,14981,11500,14942,11205,14902,10752,14861,10393,14812,9991,14752,9570,14682,9252,14603,8808,14519,8445,14431,8145,15209,11449,15208,11451,15202,11451,15190,11438,15163,11384,15117,11274,15055,10979,14994,10648,14932,10343,14871,9936,14803,9532,14729,9218,14645,8742,14556,8381,14461,8020,14365,7603,15273,10603,15272,10607,15267,10619,15256,10631,15231,10614,15182,10535,15118,10389,15042,10167,14963,9787,14883,9447,14800,9115,14710,8665,14615,8318,14514,7911,14411,7507,14279,7198,15314,9675,15313,9683,15309,9712,15298,9759,15277,9797,15229,9773,15166,9668,15084,9487,14995,9274,14898,8910,14800,8539,14697,8234,14590,7790,14479,7409,14367,7067,14178,6621,15337,8619,15337,8631,15333,8677,15325,8769,15305,8871,15264,8940,15202,8909,15119,8775,15022,8565,14916,8328,14804,8009,14688,7614,14569,7287,14448,6888,14321,6483,14088,6171,15350,7402,15350,7419,15347,7480,15340,7613,15322,7804,15287,7973,15229,8057,15148,8012,15046,7846,14933,7611,14810,7357,14682,7069,14552,6656,14421,6316,14251,5948,14007,5528,15356,5942,15356,5977,15353,6119,15348,6294,15332,6551,15302,6824,15249,7044,15171,7122,15070,7050,14949,6861,14818,6611,14679,6349,14538,6067,14398,5651,14189,5311,13935,4958,15359,4123,15359,4153,15356,4296,15353,4646,15338,5160,15311,5508,15263,5829,15188,6042,15088,6094,14966,6001,14826,5796,14678,5543,14527,5287,14377,4985,14133,4586,13869,4257,15360,1563,15360,1642,15358,2076,15354,2636,15341,3350,15317,4019,15273,4429,15203,4732,15105,4911,14981,4932,14836,4818,14679,4621,14517,4386,14359,4156,14083,3795,13808,3437,15360,122,15360,137,15358,285,15355,636,15344,1274,15322,2177,15281,2765,15215,3223,15120,3451,14995,3569,14846,3567,14681,3466,14511,3305,14344,3121,14037,2800,13753,2467,15360,0,15360,1,15359,21,15355,89,15346,253,15325,479,15287,796,15225,1148,15133,1492,15008,1749,14856,1882,14685,1886,14506,1783,14324,1608,13996,1398,13702,1183]),qn=null;function _y(){return qn===null&&(qn=new $a(gy,16,16,Bi,Ze),qn.name="DFG_LUT",qn.minFilter=Ge,qn.magFilter=Ge,qn.wrapS=Vn,qn.wrapT=Vn,qn.generateMipmaps=!1,qn.needsUpdate=!0),qn}var ul=class{constructor(t={}){let{canvas:e=Lf(),context:n=null,depth:s=!0,stencil:r=!1,alpha:a=!1,antialias:o=!1,premultipliedAlpha:l=!0,preserveDrawingBuffer:c=!1,powerPreference:h="default",failIfMajorPerformanceCaveat:f=!1,reversedDepthBuffer:u=!1,outputBufferType:d=vn}=t;this.isWebGLRenderer=!0;let m;if(n!==null){if(typeof WebGLRenderingContext<"u"&&n instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");m=n.getContextAttributes().alpha}else m=a;let _=d,g=new Set([Co,Eo,To]),p=new Set([vn,Fn,zs,Vs,wo,Ao]),y=new Uint32Array(4),S=new Int32Array(4),b=new P,T=null,w=null,R=[],v=[],E=null;this.domElement=e,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this.toneMapping=xn,this.toneMappingExposure=1,this.transmissionResolutionScale=1;let L=this,C=!1,D=null;this._outputColorSpace=mn;let H=0,W=0,U=null,z=-1,V=null,$=new ve,tt=new ve,ct=null,Mt=new dt(0),St=0,qt=e.width,ee=e.height,kt=1,J=null,mt=null,st=new ve(0,0,qt,ee),Rt=new ve(0,0,qt,ee),Ut=!1,It=new yr,pe=!1,Yt=!1,ne=new ge,fe=new P,Xt=new ve,Ie={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0},me=!1;function un(){return U===null?kt:1}let N=n;function Le(M,F){return e.getContext(M,F)}try{let M={alpha:!0,depth:s,stencil:r,antialias:o,premultipliedAlpha:l,preserveDrawingBuffer:c,powerPreference:h,failIfMajorPerformanceCaveat:f};if("setAttribute"in e&&e.setAttribute("data-engine",`three.js r${vo}`),e.addEventListener("webglcontextlost",j,!1),e.addEventListener("webglcontextrestored",wt,!1),e.addEventListener("webglcontextcreationerror",Ot,!1),N===null){let F="webgl2";if(N=Le(F,M),N===null)throw Le(F)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(M){throw Pt("WebGLRenderer: "+M.message),M}let Zt,he,ht,_e,A,x,O,Z,Q,et,lt,X,K,gt,vt,rt,nt,Dt,zt,$t,I,it,Y;function _t(){Zt=new wx(N),Zt.init(),I=new hy(N,Zt),he=new gx(N,Zt,t,I),ht=new ly(N,Zt),he.reversedDepthBuffer&&u&&ht.buffers.depth.setReversed(!0),_e=new Ex(N),A=new Zv,x=new cy(N,Zt,ht,A,he,I,_e),O=new Sx(L),Z=new Ig(N),it=new px(N,Z),Q=new Ax(N,Z,_e,it),et=new Rx(N,Q,Z,it,_e),Dt=new Cx(N,he,x),vt=new _x(A),lt=new Yv(L,O,Zt,he,it,vt),X=new py(L,A),K=new Jv,gt=new ny(Zt),nt=new dx(L,O,ht,et,m,l),rt=new oy(L,et,he),Y=new my(N,_e,he,ht),zt=new mx(N,Zt,_e),$t=new Tx(N,Zt,_e),_e.programs=lt.programs,L.capabilities=he,L.extensions=Zt,L.properties=A,L.renderLists=K,L.shadowMap=rt,L.state=ht,L.info=_e}_t(),_!==vn&&(E=new Ix(_,e.width,e.height,s,r));let at=new bh(L,N);this.xr=at,this.getContext=function(){return N},this.getContextAttributes=function(){return N.getContextAttributes()},this.forceContextLoss=function(){let M=Zt.get("WEBGL_lose_context");M&&M.loseContext()},this.forceContextRestore=function(){let M=Zt.get("WEBGL_lose_context");M&&M.restoreContext()},this.getPixelRatio=function(){return kt},this.setPixelRatio=function(M){M!==void 0&&(kt=M,this.setSize(qt,ee,!1))},this.getSize=function(M){return M.set(qt,ee)},this.setSize=function(M,F,G=!0){if(at.isPresenting){Ct("WebGLRenderer: Can't change size while VR device is presenting.");return}qt=M,ee=F,e.width=Math.floor(M*kt),e.height=Math.floor(F*kt),G===!0&&(e.style.width=M+"px",e.style.height=F+"px"),E!==null&&E.setSize(e.width,e.height),this.setViewport(0,0,M,F)},this.getDrawingBufferSize=function(M){return M.set(qt*kt,ee*kt).floor()},this.setDrawingBufferSize=function(M,F,G){qt=M,ee=F,kt=G,e.width=Math.floor(M*G),e.height=Math.floor(F*G),this.setViewport(0,0,M,F)},this.setEffects=function(M){if(_===vn){Pt("THREE.WebGLRenderer: setEffects() requires outputBufferType set to HalfFloatType or FloatType.");return}if(M){for(let F=0;F<M.length;F++)if(M[F].isOutputPass===!0){Ct("THREE.WebGLRenderer: OutputPass is not needed in setEffects(). Tone mapping and color space conversion are applied automatically.");break}}E.setEffects(M||[])},this.getCurrentViewport=function(M){return M.copy($)},this.getViewport=function(M){return M.copy(st)},this.setViewport=function(M,F,G,B){M.isVector4?st.set(M.x,M.y,M.z,M.w):st.set(M,F,G,B),ht.viewport($.copy(st).multiplyScalar(kt).round())},this.getScissor=function(M){return M.copy(Rt)},this.setScissor=function(M,F,G,B){M.isVector4?Rt.set(M.x,M.y,M.z,M.w):Rt.set(M,F,G,B),ht.scissor(tt.copy(Rt).multiplyScalar(kt).round())},this.getScissorTest=function(){return Ut},this.setScissorTest=function(M){ht.setScissorTest(Ut=M)},this.setOpaqueSort=function(M){J=M},this.setTransparentSort=function(M){mt=M},this.getClearColor=function(M){return M.copy(nt.getClearColor())},this.setClearColor=function(){nt.setClearColor(...arguments)},this.getClearAlpha=function(){return nt.getClearAlpha()},this.setClearAlpha=function(){nt.setClearAlpha(...arguments)},this.clear=function(M=!0,F=!0,G=!0){let B=0;if(M){let k=!1;if(U!==null){let pt=U.texture.format;k=g.has(pt)}if(k){let pt=U.texture.type,yt=p.has(pt),ft=nt.getClearColor(),bt=nt.getClearAlpha(),At=ft.r,Bt=ft.g,Ht=ft.b;yt?(y[0]=At,y[1]=Bt,y[2]=Ht,y[3]=bt,N.clearBufferuiv(N.COLOR,0,y)):(S[0]=At,S[1]=Bt,S[2]=Ht,S[3]=bt,N.clearBufferiv(N.COLOR,0,S))}else B|=N.COLOR_BUFFER_BIT}F&&(B|=N.DEPTH_BUFFER_BIT,this.state.buffers.depth.setMask(!0)),G&&(B|=N.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),B!==0&&N.clear(B)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.setNodesHandler=function(M){M.setRenderer(this),D=M},this.dispose=function(){e.removeEventListener("webglcontextlost",j,!1),e.removeEventListener("webglcontextrestored",wt,!1),e.removeEventListener("webglcontextcreationerror",Ot,!1),nt.dispose(),K.dispose(),gt.dispose(),A.dispose(),O.dispose(),et.dispose(),it.dispose(),Y.dispose(),lt.dispose(),at.dispose(),at.removeEventListener("sessionstart",xu),at.removeEventListener("sessionend",vu),$i.stop()};function j(M){M.preventDefault(),Kc("WebGLRenderer: Context Lost."),C=!0}function wt(){Kc("WebGLRenderer: Context Restored."),C=!1;let M=_e.autoReset,F=rt.enabled,G=rt.autoUpdate,B=rt.needsUpdate,k=rt.type;_t(),_e.autoReset=M,rt.enabled=F,rt.autoUpdate=G,rt.needsUpdate=B,rt.type=k}function Ot(M){Pt("WebGLRenderer: A WebGL context could not be created. Reason: ",M.statusMessage)}function be(M){let F=M.target;F.removeEventListener("dispose",be),ie(F)}function ie(M){jn(M),A.remove(M)}function jn(M){let F=A.get(M).programs;F!==void 0&&(F.forEach(function(G){lt.releaseProgram(G)}),M.isShaderMaterial&&lt.releaseShaderCache(M))}this.renderBufferDirect=function(M,F,G,B,k,pt){F===null&&(F=Ie);let yt=k.isMesh&&k.matrixWorld.determinant()<0,ft=Cm(M,F,G,B,k);ht.setMaterial(B,yt);let bt=G.index,At=1;if(B.wireframe===!0){if(bt=Q.getWireframeAttribute(G),bt===void 0)return;At=2}let Bt=G.drawRange,Ht=G.attributes.position,Tt=Bt.start*At,se=(Bt.start+Bt.count)*At;pt!==null&&(Tt=Math.max(Tt,pt.start*At),se=Math.min(se,(pt.start+pt.count)*At)),bt!==null?(Tt=Math.max(Tt,0),se=Math.min(se,bt.count)):Ht!=null&&(Tt=Math.max(Tt,0),se=Math.min(se,Ht.count));let Se=se-Tt;if(Se<0||Se===1/0)return;it.setup(k,B,ft,G,bt);let xe,oe=zt;if(bt!==null&&(xe=Z.get(bt),oe=$t,oe.setIndex(xe)),k.isMesh)B.wireframe===!0?(ht.setLineWidth(B.wireframeLinewidth*un()),oe.setMode(N.LINES)):oe.setMode(N.TRIANGLES);else if(k.isLine){let We=B.linewidth;We===void 0&&(We=1),ht.setLineWidth(We*un()),k.isLineSegments?oe.setMode(N.LINES):k.isLineLoop?oe.setMode(N.LINE_LOOP):oe.setMode(N.LINE_STRIP)}else k.isPoints?oe.setMode(N.POINTS):k.isSprite&&oe.setMode(N.TRIANGLES);if(k.isBatchedMesh)if(Zt.get("WEBGL_multi_draw"))oe.renderMultiDraw(k._multiDrawStarts,k._multiDrawCounts,k._multiDrawCount);else{let We=k._multiDrawStarts,xt=k._multiDrawCounts,fn=k._multiDrawCount,Kt=bt?Z.get(bt).bytesPerElement:1,Mn=A.get(B).currentProgram.getUniforms();for(let kn=0;kn<fn;kn++)Mn.setValue(N,"_gl_DrawID",kn),oe.render(We[kn]/Kt,xt[kn])}else if(k.isInstancedMesh)oe.renderInstances(Tt,Se,k.count);else if(G.isInstancedBufferGeometry){let We=G._maxInstanceCount!==void 0?G._maxInstanceCount:1/0,xt=Math.min(G.instanceCount,We);oe.renderInstances(Tt,Se,xt)}else oe.render(Tt,Se)};function Bn(M,F,G){M.transparent===!0&&M.side===Xn&&M.forceSinglePass===!1?(M.side=je,M.needsUpdate=!0,ca(M,F,G),M.side=ai,M.needsUpdate=!0,ca(M,F,G),M.side=Xn):ca(M,F,G)}this.compile=function(M,F,G=null){G===null&&(G=M),w=gt.get(G),w.init(F),v.push(w),G.traverseVisible(function(k){k.isLight&&k.layers.test(F.layers)&&(w.pushLight(k),k.castShadow&&w.pushShadow(k))}),M!==G&&M.traverseVisible(function(k){k.isLight&&k.layers.test(F.layers)&&(w.pushLight(k),k.castShadow&&w.pushShadow(k))}),w.setupLights();let B=new Set;return M.traverse(function(k){if(!(k.isMesh||k.isPoints||k.isLine||k.isSprite))return;let pt=k.material;if(pt)if(Array.isArray(pt))for(let yt=0;yt<pt.length;yt++){let ft=pt[yt];Bn(ft,G,k),B.add(ft)}else Bn(pt,G,k),B.add(pt)}),w=v.pop(),B},this.compileAsync=function(M,F,G=null){let B=this.compile(M,F,G);return new Promise(k=>{function pt(){if(B.forEach(function(yt){A.get(yt).currentProgram.isReady()&&B.delete(yt)}),B.size===0){k(M);return}setTimeout(pt,10)}Zt.get("KHR_parallel_shader_compile")!==null?pt():setTimeout(pt,10)})};let Ql=null;function Tm(M){Ql&&Ql(M)}function xu(){$i.stop()}function vu(){$i.start()}let $i=new ad;$i.setAnimationLoop(Tm),typeof self<"u"&&$i.setContext(self),this.setAnimationLoop=function(M){Ql=M,at.setAnimationLoop(M),M===null?$i.stop():$i.start()},at.addEventListener("sessionstart",xu),at.addEventListener("sessionend",vu),this.render=function(M,F){if(F!==void 0&&F.isCamera!==!0){Pt("WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(C===!0)return;D!==null&&D.renderStart(M,F);let G=at.enabled===!0&&at.isPresenting===!0,B=E!==null&&(U===null||G)&&E.begin(L,U);if(M.matrixWorldAutoUpdate===!0&&M.updateMatrixWorld(),F.parent===null&&F.matrixWorldAutoUpdate===!0&&F.updateMatrixWorld(),at.enabled===!0&&at.isPresenting===!0&&(E===null||E.isCompositing()===!1)&&(at.cameraAutoUpdate===!0&&at.updateCamera(F),F=at.getCamera()),M.isScene===!0&&M.onBeforeRender(L,M,F,U),w=gt.get(M,v.length),w.init(F),w.state.textureUnits=x.getTextureUnits(),v.push(w),ne.multiplyMatrices(F.projectionMatrix,F.matrixWorldInverse),It.setFromProjectionMatrix(ne,In,F.reversedDepth),Yt=this.localClippingEnabled,pe=vt.init(this.clippingPlanes,Yt),T=K.get(M,R.length),T.init(),R.push(T),at.enabled===!0&&at.isPresenting===!0){let yt=L.xr.getDepthSensingMesh();yt!==null&&tc(yt,F,-1/0,L.sortObjects)}tc(M,F,0,L.sortObjects),T.finish(),L.sortObjects===!0&&T.sort(J,mt),me=at.enabled===!1||at.isPresenting===!1||at.hasDepthSensing()===!1,me&&nt.addToRenderList(T,M),this.info.render.frame++,pe===!0&&vt.beginShadows();let k=w.state.shadowsArray;if(rt.render(k,M,F),pe===!0&&vt.endShadows(),this.info.autoReset===!0&&this.info.reset(),(B&&E.hasRenderPass())===!1){let yt=T.opaque,ft=T.transmissive;if(w.setupLights(),F.isArrayCamera){let bt=F.cameras;if(ft.length>0)for(let At=0,Bt=bt.length;At<Bt;At++){let Ht=bt[At];Mu(yt,ft,M,Ht)}me&&nt.render(M);for(let At=0,Bt=bt.length;At<Bt;At++){let Ht=bt[At];yu(T,M,Ht,Ht.viewport)}}else ft.length>0&&Mu(yt,ft,M,F),me&&nt.render(M),yu(T,M,F)}U!==null&&W===0&&(x.updateMultisampleRenderTarget(U),x.updateRenderTargetMipmap(U)),B&&E.end(L),M.isScene===!0&&M.onAfterRender(L,M,F),it.resetDefaultState(),z=-1,V=null,v.pop(),v.length>0?(w=v[v.length-1],x.setTextureUnits(w.state.textureUnits),pe===!0&&vt.setGlobalState(L.clippingPlanes,w.state.camera)):w=null,R.pop(),R.length>0?T=R[R.length-1]:T=null,D!==null&&D.renderEnd()};function tc(M,F,G,B){if(M.visible===!1)return;if(M.layers.test(F.layers)){if(M.isGroup)G=M.renderOrder;else if(M.isLOD)M.autoUpdate===!0&&M.update(F);else if(M.isLightProbeGrid)w.pushLightProbeGrid(M);else if(M.isLight)w.pushLight(M),M.castShadow&&w.pushShadow(M);else if(M.isSprite){if(!M.frustumCulled||It.intersectsSprite(M)){B&&Xt.setFromMatrixPosition(M.matrixWorld).applyMatrix4(ne);let yt=et.update(M),ft=M.material;ft.visible&&T.push(M,yt,ft,G,Xt.z,null)}}else if((M.isMesh||M.isLine||M.isPoints)&&(!M.frustumCulled||It.intersectsObject(M))){let yt=et.update(M),ft=M.material;if(B&&(M.boundingSphere!==void 0?(M.boundingSphere===null&&M.computeBoundingSphere(),Xt.copy(M.boundingSphere.center)):(yt.boundingSphere===null&&yt.computeBoundingSphere(),Xt.copy(yt.boundingSphere.center)),Xt.applyMatrix4(M.matrixWorld).applyMatrix4(ne)),Array.isArray(ft)){let bt=yt.groups;for(let At=0,Bt=bt.length;At<Bt;At++){let Ht=bt[At],Tt=ft[Ht.materialIndex];Tt&&Tt.visible&&T.push(M,yt,Tt,G,Xt.z,Ht)}}else ft.visible&&T.push(M,yt,ft,G,Xt.z,null)}}let pt=M.children;for(let yt=0,ft=pt.length;yt<ft;yt++)tc(pt[yt],F,G,B)}function yu(M,F,G,B){let{opaque:k,transmissive:pt,transparent:yt}=M;w.setupLightsView(G),pe===!0&&vt.setGlobalState(L.clippingPlanes,G),B&&ht.viewport($.copy(B)),k.length>0&&la(k,F,G),pt.length>0&&la(pt,F,G),yt.length>0&&la(yt,F,G),ht.buffers.depth.setTest(!0),ht.buffers.depth.setMask(!0),ht.buffers.color.setMask(!0),ht.setPolygonOffset(!1)}function Mu(M,F,G,B){if((G.isScene===!0?G.overrideMaterial:null)!==null)return;if(w.state.transmissionRenderTarget[B.id]===void 0){let Tt=Zt.has("EXT_color_buffer_half_float")||Zt.has("EXT_color_buffer_float");w.state.transmissionRenderTarget[B.id]=new Ne(1,1,{generateMipmaps:!0,type:Tt?Ze:vn,minFilter:Ui,samples:Math.max(4,he.samples),stencilBuffer:r,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Wt.workingColorSpace})}let pt=w.state.transmissionRenderTarget[B.id],yt=B.viewport||$;pt.setSize(yt.z*L.transmissionResolutionScale,yt.w*L.transmissionResolutionScale);let ft=L.getRenderTarget(),bt=L.getActiveCubeFace(),At=L.getActiveMipmapLevel();L.setRenderTarget(pt),L.getClearColor(Mt),St=L.getClearAlpha(),St<1&&L.setClearColor(16777215,.5),L.clear(),me&&nt.render(G);let Bt=L.toneMapping;L.toneMapping=xn;let Ht=B.viewport;if(B.viewport!==void 0&&(B.viewport=void 0),w.setupLightsView(B),pe===!0&&vt.setGlobalState(L.clippingPlanes,B),la(M,G,B),x.updateMultisampleRenderTarget(pt),x.updateRenderTargetMipmap(pt),Zt.has("WEBGL_multisampled_render_to_texture")===!1){let Tt=!1;for(let se=0,Se=F.length;se<Se;se++){let xe=F[se],{object:oe,geometry:We,material:xt,group:fn}=xe;if(xt.side===Xn&&oe.layers.test(B.layers)){let Kt=xt.side;xt.side=je,xt.needsUpdate=!0,bu(oe,G,B,We,xt,fn),xt.side=Kt,xt.needsUpdate=!0,Tt=!0}}Tt===!0&&(x.updateMultisampleRenderTarget(pt),x.updateRenderTargetMipmap(pt))}L.setRenderTarget(ft,bt,At),L.setClearColor(Mt,St),Ht!==void 0&&(B.viewport=Ht),L.toneMapping=Bt}function la(M,F,G){let B=F.isScene===!0?F.overrideMaterial:null;for(let k=0,pt=M.length;k<pt;k++){let yt=M[k],{object:ft,geometry:bt,group:At}=yt,Bt=yt.material;Bt.allowOverride===!0&&B!==null&&(Bt=B),ft.layers.test(G.layers)&&bu(ft,F,G,bt,Bt,At)}}function bu(M,F,G,B,k,pt){M.onBeforeRender(L,F,G,B,k,pt),M.modelViewMatrix.multiplyMatrices(G.matrixWorldInverse,M.matrixWorld),M.normalMatrix.getNormalMatrix(M.modelViewMatrix),k.onBeforeRender(L,F,G,B,M,pt),k.transparent===!0&&k.side===Xn&&k.forceSinglePass===!1?(k.side=je,k.needsUpdate=!0,L.renderBufferDirect(G,F,B,k,M,pt),k.side=ai,k.needsUpdate=!0,L.renderBufferDirect(G,F,B,k,M,pt),k.side=Xn):L.renderBufferDirect(G,F,B,k,M,pt),M.onAfterRender(L,F,G,B,k,pt)}function ca(M,F,G){F.isScene!==!0&&(F=Ie);let B=A.get(M),k=w.state.lights,pt=w.state.shadowsArray,yt=k.state.version,ft=lt.getParameters(M,k.state,pt,F,G,w.state.lightProbeGridArray),bt=lt.getProgramCacheKey(ft),At=B.programs;B.environment=M.isMeshStandardMaterial||M.isMeshLambertMaterial||M.isMeshPhongMaterial?F.environment:null,B.fog=F.fog;let Bt=M.isMeshStandardMaterial||M.isMeshLambertMaterial&&!M.envMap||M.isMeshPhongMaterial&&!M.envMap;B.envMap=O.get(M.envMap||B.environment,Bt),B.envMapRotation=B.environment!==null&&M.envMap===null?F.environmentRotation:M.envMapRotation,At===void 0&&(M.addEventListener("dispose",be),At=new Map,B.programs=At);let Ht=At.get(bt);if(Ht!==void 0){if(B.currentProgram===Ht&&B.lightsStateVersion===yt)return wu(M,ft),Ht}else ft.uniforms=lt.getUniforms(M),D!==null&&M.isNodeMaterial&&D.build(M,G,ft),M.onBeforeCompile(ft,L),Ht=lt.acquireProgram(ft,bt),At.set(bt,Ht),B.uniforms=ft.uniforms;let Tt=B.uniforms;return(!M.isShaderMaterial&&!M.isRawShaderMaterial||M.clipping===!0)&&(Tt.clippingPlanes=vt.uniform),wu(M,ft),B.needsLights=Pm(M),B.lightsStateVersion=yt,B.needsLights&&(Tt.ambientLightColor.value=k.state.ambient,Tt.lightProbe.value=k.state.probe,Tt.directionalLights.value=k.state.directional,Tt.directionalLightShadows.value=k.state.directionalShadow,Tt.spotLights.value=k.state.spot,Tt.spotLightShadows.value=k.state.spotShadow,Tt.rectAreaLights.value=k.state.rectArea,Tt.ltc_1.value=k.state.rectAreaLTC1,Tt.ltc_2.value=k.state.rectAreaLTC2,Tt.pointLights.value=k.state.point,Tt.pointLightShadows.value=k.state.pointShadow,Tt.hemisphereLights.value=k.state.hemi,Tt.directionalShadowMatrix.value=k.state.directionalShadowMatrix,Tt.spotLightMatrix.value=k.state.spotLightMatrix,Tt.spotLightMap.value=k.state.spotLightMap,Tt.pointShadowMatrix.value=k.state.pointShadowMatrix),B.lightProbeGrid=w.state.lightProbeGridArray.length>0,B.currentProgram=Ht,B.uniformsList=null,Ht}function Su(M){if(M.uniformsList===null){let F=M.currentProgram.getUniforms();M.uniformsList=Ws.seqWithValue(F.seq,M.uniforms)}return M.uniformsList}function wu(M,F){let G=A.get(M);G.outputColorSpace=F.outputColorSpace,G.batching=F.batching,G.batchingColor=F.batchingColor,G.instancing=F.instancing,G.instancingColor=F.instancingColor,G.instancingMorph=F.instancingMorph,G.skinning=F.skinning,G.morphTargets=F.morphTargets,G.morphNormals=F.morphNormals,G.morphColors=F.morphColors,G.morphTargetsCount=F.morphTargetsCount,G.numClippingPlanes=F.numClippingPlanes,G.numIntersection=F.numClipIntersection,G.vertexAlphas=F.vertexAlphas,G.vertexTangents=F.vertexTangents,G.toneMapping=F.toneMapping}function Em(M,F){if(M.length===0)return null;if(M.length===1)return M[0].texture!==null?M[0]:null;b.setFromMatrixPosition(F.matrixWorld);for(let G=0,B=M.length;G<B;G++){let k=M[G];if(k.texture!==null&&k.boundingBox.containsPoint(b))return k}return null}function Cm(M,F,G,B,k){F.isScene!==!0&&(F=Ie),x.resetTextureUnits();let pt=F.fog,yt=B.isMeshStandardMaterial||B.isMeshLambertMaterial||B.isMeshPhongMaterial?F.environment:null,ft=U===null?L.outputColorSpace:U.isXRRenderTarget===!0?U.texture.colorSpace:Wt.workingColorSpace,bt=B.isMeshStandardMaterial||B.isMeshLambertMaterial&&!B.envMap||B.isMeshPhongMaterial&&!B.envMap,At=O.get(B.envMap||yt,bt),Bt=B.vertexColors===!0&&!!G.attributes.color&&G.attributes.color.itemSize===4,Ht=!!G.attributes.tangent&&(!!B.normalMap||B.anisotropy>0),Tt=!!G.morphAttributes.position,se=!!G.morphAttributes.normal,Se=!!G.morphAttributes.color,xe=xn;B.toneMapped&&(U===null||U.isXRRenderTarget===!0)&&(xe=L.toneMapping);let oe=G.morphAttributes.position||G.morphAttributes.normal||G.morphAttributes.color,We=oe!==void 0?oe.length:0,xt=A.get(B),fn=w.state.lights;if(pe===!0&&(Yt===!0||M!==V)){let ue=M===V&&B.id===z;vt.setState(B,M,ue)}let Kt=!1;B.version===xt.__version?(xt.needsLights&&xt.lightsStateVersion!==fn.state.version||xt.outputColorSpace!==ft||k.isBatchedMesh&&xt.batching===!1||!k.isBatchedMesh&&xt.batching===!0||k.isBatchedMesh&&xt.batchingColor===!0&&k.colorTexture===null||k.isBatchedMesh&&xt.batchingColor===!1&&k.colorTexture!==null||k.isInstancedMesh&&xt.instancing===!1||!k.isInstancedMesh&&xt.instancing===!0||k.isSkinnedMesh&&xt.skinning===!1||!k.isSkinnedMesh&&xt.skinning===!0||k.isInstancedMesh&&xt.instancingColor===!0&&k.instanceColor===null||k.isInstancedMesh&&xt.instancingColor===!1&&k.instanceColor!==null||k.isInstancedMesh&&xt.instancingMorph===!0&&k.morphTexture===null||k.isInstancedMesh&&xt.instancingMorph===!1&&k.morphTexture!==null||xt.envMap!==At||B.fog===!0&&xt.fog!==pt||xt.numClippingPlanes!==void 0&&(xt.numClippingPlanes!==vt.numPlanes||xt.numIntersection!==vt.numIntersection)||xt.vertexAlphas!==Bt||xt.vertexTangents!==Ht||xt.morphTargets!==Tt||xt.morphNormals!==se||xt.morphColors!==Se||xt.toneMapping!==xe||xt.morphTargetsCount!==We||!!xt.lightProbeGrid!=w.state.lightProbeGridArray.length>0)&&(Kt=!0):(Kt=!0,xt.__version=B.version);let Mn=xt.currentProgram;Kt===!0&&(Mn=ca(B,F,k),D&&B.isNodeMaterial&&D.onUpdateProgram(B,Mn,xt));let kn=!1,mi=!1,_s=!1,le=Mn.getUniforms(),we=xt.uniforms;if(ht.useProgram(Mn.program)&&(kn=!0,mi=!0,_s=!0),B.id!==z&&(z=B.id,mi=!0),xt.needsLights){let ue=Em(w.state.lightProbeGridArray,k);xt.lightProbeGrid!==ue&&(xt.lightProbeGrid=ue,mi=!0)}if(kn||V!==M){ht.buffers.depth.getReversed()&&M.reversedDepth!==!0&&(M._reversedDepth=!0,M.updateProjectionMatrix()),le.setValue(N,"projectionMatrix",M.projectionMatrix),le.setValue(N,"viewMatrix",M.matrixWorldInverse);let _i=le.map.cameraPosition;_i!==void 0&&_i.setValue(N,fe.setFromMatrixPosition(M.matrixWorld)),he.logarithmicDepthBuffer&&le.setValue(N,"logDepthBufFC",2/(Math.log(M.far+1)/Math.LN2)),(B.isMeshPhongMaterial||B.isMeshToonMaterial||B.isMeshLambertMaterial||B.isMeshBasicMaterial||B.isMeshStandardMaterial||B.isShaderMaterial)&&le.setValue(N,"isOrthographic",M.isOrthographicCamera===!0),V!==M&&(V=M,mi=!0,_s=!0)}if(xt.needsLights&&(fn.state.directionalShadowMap.length>0&&le.setValue(N,"directionalShadowMap",fn.state.directionalShadowMap,x),fn.state.spotShadowMap.length>0&&le.setValue(N,"spotShadowMap",fn.state.spotShadowMap,x),fn.state.pointShadowMap.length>0&&le.setValue(N,"pointShadowMap",fn.state.pointShadowMap,x)),k.isSkinnedMesh){le.setOptional(N,k,"bindMatrix"),le.setOptional(N,k,"bindMatrixInverse");let ue=k.skeleton;ue&&(ue.boneTexture===null&&ue.computeBoneTexture(),le.setValue(N,"boneTexture",ue.boneTexture,x))}k.isBatchedMesh&&(le.setOptional(N,k,"batchingTexture"),le.setValue(N,"batchingTexture",k._matricesTexture,x),le.setOptional(N,k,"batchingIdTexture"),le.setValue(N,"batchingIdTexture",k._indirectTexture,x),le.setOptional(N,k,"batchingColorTexture"),k._colorsTexture!==null&&le.setValue(N,"batchingColorTexture",k._colorsTexture,x));let gi=G.morphAttributes;if((gi.position!==void 0||gi.normal!==void 0||gi.color!==void 0)&&Dt.update(k,G,Mn),(mi||xt.receiveShadow!==k.receiveShadow)&&(xt.receiveShadow=k.receiveShadow,le.setValue(N,"receiveShadow",k.receiveShadow)),(B.isMeshStandardMaterial||B.isMeshLambertMaterial||B.isMeshPhongMaterial)&&B.envMap===null&&F.environment!==null&&(we.envMapIntensity.value=F.environmentIntensity),we.dfgLUT!==void 0&&(we.dfgLUT.value=_y()),mi){if(le.setValue(N,"toneMappingExposure",L.toneMappingExposure),xt.needsLights&&Rm(we,_s),pt&&B.fog===!0&&X.refreshFogUniforms(we,pt),X.refreshMaterialUniforms(we,B,kt,ee,w.state.transmissionRenderTarget[M.id]),xt.needsLights&&xt.lightProbeGrid){let ue=xt.lightProbeGrid;we.probesSH.value=ue.texture,we.probesMin.value.copy(ue.boundingBox.min),we.probesMax.value.copy(ue.boundingBox.max),we.probesResolution.value.copy(ue.resolution)}Ws.upload(N,Su(xt),we,x)}if(B.isShaderMaterial&&B.uniformsNeedUpdate===!0&&(Ws.upload(N,Su(xt),we,x),B.uniformsNeedUpdate=!1),B.isSpriteMaterial&&le.setValue(N,"center",k.center),le.setValue(N,"modelViewMatrix",k.modelViewMatrix),le.setValue(N,"normalMatrix",k.normalMatrix),le.setValue(N,"modelMatrix",k.matrixWorld),B.uniformsGroups!==void 0){let ue=B.uniformsGroups;for(let _i=0,xs=ue.length;_i<xs;_i++){let Au=ue[_i];Y.update(Au,Mn),Y.bind(Au,Mn)}}return Mn}function Rm(M,F){M.ambientLightColor.needsUpdate=F,M.lightProbe.needsUpdate=F,M.directionalLights.needsUpdate=F,M.directionalLightShadows.needsUpdate=F,M.pointLights.needsUpdate=F,M.pointLightShadows.needsUpdate=F,M.spotLights.needsUpdate=F,M.spotLightShadows.needsUpdate=F,M.rectAreaLights.needsUpdate=F,M.hemisphereLights.needsUpdate=F}function Pm(M){return M.isMeshLambertMaterial||M.isMeshToonMaterial||M.isMeshPhongMaterial||M.isMeshStandardMaterial||M.isShadowMaterial||M.isShaderMaterial&&M.lights===!0}this.getActiveCubeFace=function(){return H},this.getActiveMipmapLevel=function(){return W},this.getRenderTarget=function(){return U},this.setRenderTargetTextures=function(M,F,G){let B=A.get(M);B.__autoAllocateDepthBuffer=M.resolveDepthBuffer===!1,B.__autoAllocateDepthBuffer===!1&&(B.__useRenderToTexture=!1),A.get(M.texture).__webglTexture=F,A.get(M.depthTexture).__webglTexture=B.__autoAllocateDepthBuffer?void 0:G,B.__hasExternalTextures=!0},this.setRenderTargetFramebuffer=function(M,F){let G=A.get(M);G.__webglFramebuffer=F,G.__useDefaultFramebuffer=F===void 0};let Im=N.createFramebuffer();this.setRenderTarget=function(M,F=0,G=0){U=M,H=F,W=G;let B=null,k=!1,pt=!1;if(M){let ft=A.get(M);if(ft.__useDefaultFramebuffer!==void 0){ht.bindFramebuffer(N.FRAMEBUFFER,ft.__webglFramebuffer),$.copy(M.viewport),tt.copy(M.scissor),ct=M.scissorTest,ht.viewport($),ht.scissor(tt),ht.setScissorTest(ct),z=-1;return}else if(ft.__webglFramebuffer===void 0)x.setupRenderTarget(M);else if(ft.__hasExternalTextures)x.rebindTextures(M,A.get(M.texture).__webglTexture,A.get(M.depthTexture).__webglTexture);else if(M.depthBuffer){let Bt=M.depthTexture;if(ft.__boundDepthTexture!==Bt){if(Bt!==null&&A.has(Bt)&&(M.width!==Bt.image.width||M.height!==Bt.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");x.setupDepthRenderbuffer(M)}}let bt=M.texture;(bt.isData3DTexture||bt.isDataArrayTexture||bt.isCompressedArrayTexture)&&(pt=!0);let At=A.get(M).__webglFramebuffer;M.isWebGLCubeRenderTarget?(Array.isArray(At[F])?B=At[F][G]:B=At[F],k=!0):M.samples>0&&x.useMultisampledRTT(M)===!1?B=A.get(M).__webglMultisampledFramebuffer:Array.isArray(At)?B=At[G]:B=At,$.copy(M.viewport),tt.copy(M.scissor),ct=M.scissorTest}else $.copy(st).multiplyScalar(kt).floor(),tt.copy(Rt).multiplyScalar(kt).floor(),ct=Ut;if(G!==0&&(B=Im),ht.bindFramebuffer(N.FRAMEBUFFER,B)&&ht.drawBuffers(M,B),ht.viewport($),ht.scissor(tt),ht.setScissorTest(ct),k){let ft=A.get(M.texture);N.framebufferTexture2D(N.FRAMEBUFFER,N.COLOR_ATTACHMENT0,N.TEXTURE_CUBE_MAP_POSITIVE_X+F,ft.__webglTexture,G)}else if(pt){let ft=F;for(let bt=0;bt<M.textures.length;bt++){let At=A.get(M.textures[bt]);N.framebufferTextureLayer(N.FRAMEBUFFER,N.COLOR_ATTACHMENT0+bt,At.__webglTexture,G,ft)}}else if(M!==null&&G!==0){let ft=A.get(M.texture);N.framebufferTexture2D(N.FRAMEBUFFER,N.COLOR_ATTACHMENT0,N.TEXTURE_2D,ft.__webglTexture,G)}z=-1},this.readRenderTargetPixels=function(M,F,G,B,k,pt,yt,ft=0){if(!(M&&M.isWebGLRenderTarget)){Pt("WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let bt=A.get(M).__webglFramebuffer;if(M.isWebGLCubeRenderTarget&&yt!==void 0&&(bt=bt[yt]),bt){ht.bindFramebuffer(N.FRAMEBUFFER,bt);try{let At=M.textures[ft],Bt=At.format,Ht=At.type;if(M.textures.length>1&&N.readBuffer(N.COLOR_ATTACHMENT0+ft),!he.textureFormatReadable(Bt)){Pt("WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!he.textureTypeReadable(Ht)){Pt("WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}F>=0&&F<=M.width-B&&G>=0&&G<=M.height-k&&N.readPixels(F,G,B,k,I.convert(Bt),I.convert(Ht),pt)}finally{let At=U!==null?A.get(U).__webglFramebuffer:null;ht.bindFramebuffer(N.FRAMEBUFFER,At)}}},this.readRenderTargetPixelsAsync=async function(M,F,G,B,k,pt,yt,ft=0){if(!(M&&M.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let bt=A.get(M).__webglFramebuffer;if(M.isWebGLCubeRenderTarget&&yt!==void 0&&(bt=bt[yt]),bt)if(F>=0&&F<=M.width-B&&G>=0&&G<=M.height-k){ht.bindFramebuffer(N.FRAMEBUFFER,bt);let At=M.textures[ft],Bt=At.format,Ht=At.type;if(M.textures.length>1&&N.readBuffer(N.COLOR_ATTACHMENT0+ft),!he.textureFormatReadable(Bt))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!he.textureTypeReadable(Ht))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");let Tt=N.createBuffer();N.bindBuffer(N.PIXEL_PACK_BUFFER,Tt),N.bufferData(N.PIXEL_PACK_BUFFER,pt.byteLength,N.STREAM_READ),N.readPixels(F,G,B,k,I.convert(Bt),I.convert(Ht),0);let se=U!==null?A.get(U).__webglFramebuffer:null;ht.bindFramebuffer(N.FRAMEBUFFER,se);let Se=N.fenceSync(N.SYNC_GPU_COMMANDS_COMPLETE,0);return N.flush(),await Df(N,Se,4),N.bindBuffer(N.PIXEL_PACK_BUFFER,Tt),N.getBufferSubData(N.PIXEL_PACK_BUFFER,0,pt),N.deleteBuffer(Tt),N.deleteSync(Se),pt}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")},this.copyFramebufferToTexture=function(M,F=null,G=0){let B=Math.pow(2,-G),k=Math.floor(M.image.width*B),pt=Math.floor(M.image.height*B),yt=F!==null?F.x:0,ft=F!==null?F.y:0;x.setTexture2D(M,0),N.copyTexSubImage2D(N.TEXTURE_2D,G,0,0,yt,ft,k,pt),ht.unbindTexture()};let Lm=N.createFramebuffer(),Nm=N.createFramebuffer();this.copyTextureToTexture=function(M,F,G=null,B=null,k=0,pt=0){let yt,ft,bt,At,Bt,Ht,Tt,se,Se,xe=M.isCompressedTexture?M.mipmaps[pt]:M.image;if(G!==null)yt=G.max.x-G.min.x,ft=G.max.y-G.min.y,bt=G.isBox3?G.max.z-G.min.z:1,At=G.min.x,Bt=G.min.y,Ht=G.isBox3?G.min.z:0;else{let we=Math.pow(2,-k);yt=Math.floor(xe.width*we),ft=Math.floor(xe.height*we),M.isDataArrayTexture?bt=xe.depth:M.isData3DTexture?bt=Math.floor(xe.depth*we):bt=1,At=0,Bt=0,Ht=0}B!==null?(Tt=B.x,se=B.y,Se=B.z):(Tt=0,se=0,Se=0);let oe=I.convert(F.format),We=I.convert(F.type),xt;F.isData3DTexture?(x.setTexture3D(F,0),xt=N.TEXTURE_3D):F.isDataArrayTexture||F.isCompressedArrayTexture?(x.setTexture2DArray(F,0),xt=N.TEXTURE_2D_ARRAY):(x.setTexture2D(F,0),xt=N.TEXTURE_2D),ht.activeTexture(N.TEXTURE0),ht.pixelStorei(N.UNPACK_FLIP_Y_WEBGL,F.flipY),ht.pixelStorei(N.UNPACK_PREMULTIPLY_ALPHA_WEBGL,F.premultiplyAlpha),ht.pixelStorei(N.UNPACK_ALIGNMENT,F.unpackAlignment);let fn=ht.getParameter(N.UNPACK_ROW_LENGTH),Kt=ht.getParameter(N.UNPACK_IMAGE_HEIGHT),Mn=ht.getParameter(N.UNPACK_SKIP_PIXELS),kn=ht.getParameter(N.UNPACK_SKIP_ROWS),mi=ht.getParameter(N.UNPACK_SKIP_IMAGES);ht.pixelStorei(N.UNPACK_ROW_LENGTH,xe.width),ht.pixelStorei(N.UNPACK_IMAGE_HEIGHT,xe.height),ht.pixelStorei(N.UNPACK_SKIP_PIXELS,At),ht.pixelStorei(N.UNPACK_SKIP_ROWS,Bt),ht.pixelStorei(N.UNPACK_SKIP_IMAGES,Ht);let _s=M.isDataArrayTexture||M.isData3DTexture,le=F.isDataArrayTexture||F.isData3DTexture;if(M.isDepthTexture){let we=A.get(M),gi=A.get(F),ue=A.get(we.__renderTarget),_i=A.get(gi.__renderTarget);ht.bindFramebuffer(N.READ_FRAMEBUFFER,ue.__webglFramebuffer),ht.bindFramebuffer(N.DRAW_FRAMEBUFFER,_i.__webglFramebuffer);for(let xs=0;xs<bt;xs++)_s&&(N.framebufferTextureLayer(N.READ_FRAMEBUFFER,N.COLOR_ATTACHMENT0,A.get(M).__webglTexture,k,Ht+xs),N.framebufferTextureLayer(N.DRAW_FRAMEBUFFER,N.COLOR_ATTACHMENT0,A.get(F).__webglTexture,pt,Se+xs)),N.blitFramebuffer(At,Bt,yt,ft,Tt,se,yt,ft,N.DEPTH_BUFFER_BIT,N.NEAREST);ht.bindFramebuffer(N.READ_FRAMEBUFFER,null),ht.bindFramebuffer(N.DRAW_FRAMEBUFFER,null)}else if(k!==0||M.isRenderTargetTexture||A.has(M)){let we=A.get(M),gi=A.get(F);ht.bindFramebuffer(N.READ_FRAMEBUFFER,Lm),ht.bindFramebuffer(N.DRAW_FRAMEBUFFER,Nm);for(let ue=0;ue<bt;ue++)_s?N.framebufferTextureLayer(N.READ_FRAMEBUFFER,N.COLOR_ATTACHMENT0,we.__webglTexture,k,Ht+ue):N.framebufferTexture2D(N.READ_FRAMEBUFFER,N.COLOR_ATTACHMENT0,N.TEXTURE_2D,we.__webglTexture,k),le?N.framebufferTextureLayer(N.DRAW_FRAMEBUFFER,N.COLOR_ATTACHMENT0,gi.__webglTexture,pt,Se+ue):N.framebufferTexture2D(N.DRAW_FRAMEBUFFER,N.COLOR_ATTACHMENT0,N.TEXTURE_2D,gi.__webglTexture,pt),k!==0?N.blitFramebuffer(At,Bt,yt,ft,Tt,se,yt,ft,N.COLOR_BUFFER_BIT,N.NEAREST):le?N.copyTexSubImage3D(xt,pt,Tt,se,Se+ue,At,Bt,yt,ft):N.copyTexSubImage2D(xt,pt,Tt,se,At,Bt,yt,ft);ht.bindFramebuffer(N.READ_FRAMEBUFFER,null),ht.bindFramebuffer(N.DRAW_FRAMEBUFFER,null)}else le?M.isDataTexture||M.isData3DTexture?N.texSubImage3D(xt,pt,Tt,se,Se,yt,ft,bt,oe,We,xe.data):F.isCompressedArrayTexture?N.compressedTexSubImage3D(xt,pt,Tt,se,Se,yt,ft,bt,oe,xe.data):N.texSubImage3D(xt,pt,Tt,se,Se,yt,ft,bt,oe,We,xe):M.isDataTexture?N.texSubImage2D(N.TEXTURE_2D,pt,Tt,se,yt,ft,oe,We,xe.data):M.isCompressedTexture?N.compressedTexSubImage2D(N.TEXTURE_2D,pt,Tt,se,xe.width,xe.height,oe,xe.data):N.texSubImage2D(N.TEXTURE_2D,pt,Tt,se,yt,ft,oe,We,xe);ht.pixelStorei(N.UNPACK_ROW_LENGTH,fn),ht.pixelStorei(N.UNPACK_IMAGE_HEIGHT,Kt),ht.pixelStorei(N.UNPACK_SKIP_PIXELS,Mn),ht.pixelStorei(N.UNPACK_SKIP_ROWS,kn),ht.pixelStorei(N.UNPACK_SKIP_IMAGES,mi),pt===0&&F.generateMipmaps&&N.generateMipmap(xt),ht.unbindTexture()},this.initRenderTarget=function(M){A.get(M).__webglFramebuffer===void 0&&x.setupRenderTarget(M)},this.initTexture=function(M){M.isCubeTexture?x.setTextureCube(M,0):M.isData3DTexture?x.setTexture3D(M,0):M.isDataArrayTexture||M.isCompressedArrayTexture?x.setTexture2DArray(M,0):x.setTexture2D(M,0),ht.unbindTexture()},this.resetState=function(){H=0,W=0,U=null,ht.reset(),it.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return In}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(t){this._outputColorSpace=t;let e=this.getContext();e.drawingBufferColorSpace=Wt._getDrawingBufferColorSpace(t),e.unpackColorSpace=Wt._getUnpackColorSpace()}};var qs={name:"CopyShader",uniforms:{tDiffuse:{value:null},opacity:{value:1}},vertexShader:`

		varying vec2 vUv;

		void main() {

			vUv = uv;
			gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );

		}`,fragmentShader:`

		uniform float opacity;

		uniform sampler2D tDiffuse;

		varying vec2 vUv;

		void main() {

			vec4 texel = texture2D( tDiffuse, vUv );
			gl_FragColor = opacity * texel;


		}`};var yn=class{constructor(){this.isPass=!0,this.enabled=!0,this.needsSwap=!0,this.clear=!1,this.renderToScreen=!1}setSize(){}render(){console.error("THREE.Pass: .render() must be implemented in derived pass.")}dispose(){}},xy=new as(-1,1,1,-1,0,1),Sh=class extends te{constructor(){super(),this.setAttribute("position",new Ve([-1,3,0,-1,-1,0,3,-1,0],3)),this.setAttribute("uv",new Ve([0,2,0,0,2,0],2))}},vy=new Sh,Vi=class{constructor(t){this._mesh=new rn(vy,t)}dispose(){this._mesh.geometry.dispose()}render(t){t.render(this._mesh,xy)}get material(){return this._mesh.material}set material(t){this._mesh.material=t}};var pl=class extends yn{constructor(t,e="tDiffuse"){super(),this.textureID=e,this.uniforms=null,this.material=null,t instanceof re?(this.uniforms=t.uniforms,this.material=t):t&&(this.uniforms=fi.clone(t.uniforms),this.material=new re({name:t.name!==void 0?t.name:"unspecified",defines:Object.assign({},t.defines),uniforms:this.uniforms,vertexShader:t.vertexShader,fragmentShader:t.fragmentShader})),this._fsQuad=new Vi(this.material)}render(t,e,n){this.uniforms[this.textureID]&&(this.uniforms[this.textureID].value=n.texture),this._fsQuad.material=this.material,this.renderToScreen?(t.setRenderTarget(null),this._fsQuad.render(t)):(t.setRenderTarget(e),this.clear&&t.clear(t.autoClearColor,t.autoClearDepth,t.autoClearStencil),this._fsQuad.render(t))}dispose(){this.material.dispose(),this._fsQuad.dispose()}};var Zr=class extends yn{constructor(t,e){super(),this.scene=t,this.camera=e,this.clear=!0,this.needsSwap=!1,this.inverse=!1}render(t,e,n){let s=t.getContext(),r=t.state;r.buffers.color.setMask(!1),r.buffers.depth.setMask(!1),r.buffers.color.setLocked(!0),r.buffers.depth.setLocked(!0);let a,o;this.inverse?(a=0,o=1):(a=1,o=0),r.buffers.stencil.setTest(!0),r.buffers.stencil.setOp(s.REPLACE,s.REPLACE,s.REPLACE),r.buffers.stencil.setFunc(s.ALWAYS,a,4294967295),r.buffers.stencil.setClear(o),r.buffers.stencil.setLocked(!0),t.setRenderTarget(n),this.clear&&t.clear(),t.render(this.scene,this.camera),t.setRenderTarget(e),this.clear&&t.clear(),t.render(this.scene,this.camera),r.buffers.color.setLocked(!1),r.buffers.depth.setLocked(!1),r.buffers.color.setMask(!0),r.buffers.depth.setMask(!0),r.buffers.stencil.setLocked(!1),r.buffers.stencil.setFunc(s.EQUAL,1,4294967295),r.buffers.stencil.setOp(s.KEEP,s.KEEP,s.KEEP),r.buffers.stencil.setLocked(!0)}},ml=class extends yn{constructor(){super(),this.needsSwap=!1}render(t){t.state.buffers.stencil.setLocked(!1),t.state.buffers.stencil.setTest(!1)}};var gl=class{constructor(t,e){if(this.renderer=t,this._pixelRatio=t.getPixelRatio(),e===void 0){let n=t.getSize(new Et);this._width=n.width,this._height=n.height,e=new Ne(this._width*this._pixelRatio,this._height*this._pixelRatio,{type:Ze}),e.texture.name="EffectComposer.rt1"}else this._width=e.width,this._height=e.height;this.renderTarget1=e,this.renderTarget2=e.clone(),this.renderTarget2.texture.name="EffectComposer.rt2",this.writeBuffer=this.renderTarget1,this.readBuffer=this.renderTarget2,this.renderToScreen=!0,this.passes=[],this.copyPass=new pl(qs),this.copyPass.material.blending=wn,this.timer=new Cr}swapBuffers(){let t=this.readBuffer;this.readBuffer=this.writeBuffer,this.writeBuffer=t}addPass(t){this.passes.push(t),t.setSize(this._width*this._pixelRatio,this._height*this._pixelRatio)}insertPass(t,e){this.passes.splice(e,0,t),t.setSize(this._width*this._pixelRatio,this._height*this._pixelRatio)}removePass(t){let e=this.passes.indexOf(t);e!==-1&&this.passes.splice(e,1)}isLastEnabledPass(t){for(let e=t+1;e<this.passes.length;e++)if(this.passes[e].enabled)return!1;return!0}render(t){this.timer.update(),t===void 0&&(t=this.timer.getDelta());let e=this.renderer.getRenderTarget(),n=!1;for(let s=0,r=this.passes.length;s<r;s++){let a=this.passes[s];if(a.enabled!==!1){if(a.renderToScreen=this.renderToScreen&&this.isLastEnabledPass(s),a.render(this.renderer,this.writeBuffer,this.readBuffer,t,n),a.needsSwap){if(n){let o=this.renderer.getContext(),l=this.renderer.state.buffers.stencil;l.setFunc(o.NOTEQUAL,1,4294967295),this.copyPass.render(this.renderer,this.writeBuffer,this.readBuffer,t),l.setFunc(o.EQUAL,1,4294967295)}this.swapBuffers()}Zr!==void 0&&(a instanceof Zr?n=!0:a instanceof ml&&(n=!1))}}this.renderer.setRenderTarget(e)}reset(t){if(t===void 0){let e=this.renderer.getSize(new Et);this._pixelRatio=this.renderer.getPixelRatio(),this._width=e.width,this._height=e.height,t=this.renderTarget1.clone(),t.setSize(this._width*this._pixelRatio,this._height*this._pixelRatio)}this.renderTarget1.dispose(),this.renderTarget2.dispose(),this.renderTarget1=t,this.renderTarget2=t.clone(),this.writeBuffer=this.renderTarget1,this.readBuffer=this.renderTarget2}setSize(t,e){this._width=t,this._height=e;let n=this._width*this._pixelRatio,s=this._height*this._pixelRatio;this.renderTarget1.setSize(n,s),this.renderTarget2.setSize(n,s);for(let r=0;r<this.passes.length;r++)this.passes[r].setSize(n,s)}setPixelRatio(t){this._pixelRatio=t,this.setSize(this._width,this._height)}dispose(){this.renderTarget1.dispose(),this.renderTarget2.dispose(),this.copyPass.dispose()}};var _l=class extends yn{constructor(t,e,n=null,s=null,r=null){super(),this.scene=t,this.camera=e,this.overrideMaterial=n,this.clearColor=s,this.clearAlpha=r,this.clear=!0,this.clearDepth=!1,this.needsSwap=!1,this.isRenderPass=!0,this._oldClearColor=new dt}render(t,e,n){let s=t.autoClear;t.autoClear=!1;let r,a;this.overrideMaterial!==null&&(a=this.scene.overrideMaterial,this.scene.overrideMaterial=this.overrideMaterial),this.clearColor!==null&&(t.getClearColor(this._oldClearColor),t.setClearColor(this.clearColor,t.getClearAlpha())),this.clearAlpha!==null&&(r=t.getClearAlpha(),t.setClearAlpha(this.clearAlpha)),this.clearDepth==!0&&t.clearDepth(),t.setRenderTarget(this.renderToScreen?null:n),this.clear===!0&&t.clear(t.autoClearColor,t.autoClearDepth,t.autoClearStencil),t.render(this.scene,this.camera),this.clearColor!==null&&t.setClearColor(this._oldClearColor),this.clearAlpha!==null&&t.setClearAlpha(r),this.overrideMaterial!==null&&(this.scene.overrideMaterial=a),t.autoClear=s}};var dd={name:"LuminosityHighPassShader",uniforms:{tDiffuse:{value:null},luminosityThreshold:{value:1},smoothWidth:{value:1},defaultColor:{value:new dt(0)},defaultOpacity:{value:0}},vertexShader:`

		varying vec2 vUv;

		void main() {

			vUv = uv;

			gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );

		}`,fragmentShader:`

		uniform sampler2D tDiffuse;
		uniform vec3 defaultColor;
		uniform float defaultOpacity;
		uniform float luminosityThreshold;
		uniform float smoothWidth;

		varying vec2 vUv;

		void main() {

			vec4 texel = texture2D( tDiffuse, vUv );

			float v = luminance( texel.xyz );

			vec4 outputColor = vec4( defaultColor.rgb, defaultOpacity );

			float alpha = smoothstep( luminosityThreshold, luminosityThreshold + smoothWidth, v );

			gl_FragColor = mix( outputColor, texel, alpha );

		}`};var Ys=class i extends yn{constructor(t,e=1,n,s){super(),this.strength=e,this.radius=n,this.threshold=s,this.resolution=t!==void 0?new Et(t.x,t.y):new Et(256,256),this.clearColor=new dt(0,0,0),this.needsSwap=!1,this.renderTargetsHorizontal=[],this.renderTargetsVertical=[],this.nMips=5;let r=Math.round(this.resolution.x/2),a=Math.round(this.resolution.y/2);this.renderTargetBright=new Ne(r,a,{type:Ze}),this.renderTargetBright.texture.name="UnrealBloomPass.bright",this.renderTargetBright.texture.generateMipmaps=!1;for(let h=0;h<this.nMips;h++){let f=new Ne(r,a,{type:Ze});f.texture.name="UnrealBloomPass.h"+h,f.texture.generateMipmaps=!1,this.renderTargetsHorizontal.push(f);let u=new Ne(r,a,{type:Ze});u.texture.name="UnrealBloomPass.v"+h,u.texture.generateMipmaps=!1,this.renderTargetsVertical.push(u),r=Math.round(r/2),a=Math.round(a/2)}let o=dd;this.highPassUniforms=fi.clone(o.uniforms),this.highPassUniforms.luminosityThreshold.value=s,this.highPassUniforms.smoothWidth.value=.01,this.materialHighPassFilter=new re({uniforms:this.highPassUniforms,vertexShader:o.vertexShader,fragmentShader:o.fragmentShader}),this.separableBlurMaterials=[];let l=[6,10,14,18,22];r=Math.round(this.resolution.x/2),a=Math.round(this.resolution.y/2);for(let h=0;h<this.nMips;h++)this.separableBlurMaterials.push(this._getSeparableBlurMaterial(l[h])),this.separableBlurMaterials[h].uniforms.invSize.value=new Et(1/r,1/a),r=Math.round(r/2),a=Math.round(a/2);this.compositeMaterial=this._getCompositeMaterial(this.nMips),this.compositeMaterial.uniforms.blurTexture1.value=this.renderTargetsVertical[0].texture,this.compositeMaterial.uniforms.blurTexture2.value=this.renderTargetsVertical[1].texture,this.compositeMaterial.uniforms.blurTexture3.value=this.renderTargetsVertical[2].texture,this.compositeMaterial.uniforms.blurTexture4.value=this.renderTargetsVertical[3].texture,this.compositeMaterial.uniforms.blurTexture5.value=this.renderTargetsVertical[4].texture,this.compositeMaterial.uniforms.bloomStrength.value=e,this.compositeMaterial.uniforms.bloomRadius.value=.1;let c=[1,.8,.6,.4,.2];this.compositeMaterial.uniforms.bloomFactors.value=c,this.bloomTintColors=[new P(1,1,1),new P(1,1,1),new P(1,1,1),new P(1,1,1),new P(1,1,1)],this.compositeMaterial.uniforms.bloomTintColors.value=this.bloomTintColors,this.copyUniforms=fi.clone(qs.uniforms),this.blendMaterial=new re({uniforms:this.copyUniforms,vertexShader:qs.vertexShader,fragmentShader:qs.fragmentShader,premultipliedAlpha:!0,blending:Dn,depthTest:!1,depthWrite:!1,transparent:!0}),this._oldClearColor=new dt,this._oldClearAlpha=1,this._basic=new ss,this._fsQuad=new Vi(null)}dispose(){for(let t=0;t<this.renderTargetsHorizontal.length;t++)this.renderTargetsHorizontal[t].dispose();for(let t=0;t<this.renderTargetsVertical.length;t++)this.renderTargetsVertical[t].dispose();this.renderTargetBright.dispose();for(let t=0;t<this.separableBlurMaterials.length;t++)this.separableBlurMaterials[t].dispose();this.compositeMaterial.dispose(),this.blendMaterial.dispose(),this._basic.dispose(),this._fsQuad.dispose()}setSize(t,e){let n=Math.round(t/2),s=Math.round(e/2);this.renderTargetBright.setSize(n,s);for(let r=0;r<this.nMips;r++)this.renderTargetsHorizontal[r].setSize(n,s),this.renderTargetsVertical[r].setSize(n,s),this.separableBlurMaterials[r].uniforms.invSize.value=new Et(1/n,1/s),n=Math.round(n/2),s=Math.round(s/2)}render(t,e,n,s,r){t.getClearColor(this._oldClearColor),this._oldClearAlpha=t.getClearAlpha();let a=t.autoClear;t.autoClear=!1,t.setClearColor(this.clearColor,0),r&&t.state.buffers.stencil.setTest(!1),this.renderToScreen&&(this._fsQuad.material=this._basic,this._basic.map=n.texture,t.setRenderTarget(null),t.clear(),this._fsQuad.render(t)),this.highPassUniforms.tDiffuse.value=n.texture,this.highPassUniforms.luminosityThreshold.value=this.threshold,this._fsQuad.material=this.materialHighPassFilter,t.setRenderTarget(this.renderTargetBright),t.clear(),this._fsQuad.render(t);let o=this.renderTargetBright;for(let l=0;l<this.nMips;l++)this._fsQuad.material=this.separableBlurMaterials[l],this.separableBlurMaterials[l].uniforms.colorTexture.value=o.texture,this.separableBlurMaterials[l].uniforms.direction.value=i.BlurDirectionX,t.setRenderTarget(this.renderTargetsHorizontal[l]),t.clear(),this._fsQuad.render(t),this.separableBlurMaterials[l].uniforms.colorTexture.value=this.renderTargetsHorizontal[l].texture,this.separableBlurMaterials[l].uniforms.direction.value=i.BlurDirectionY,t.setRenderTarget(this.renderTargetsVertical[l]),t.clear(),this._fsQuad.render(t),o=this.renderTargetsVertical[l];this._fsQuad.material=this.compositeMaterial,this.compositeMaterial.uniforms.bloomStrength.value=this.strength,this.compositeMaterial.uniforms.bloomRadius.value=this.radius,this.compositeMaterial.uniforms.bloomTintColors.value=this.bloomTintColors,t.setRenderTarget(this.renderTargetsHorizontal[0]),t.clear(),this._fsQuad.render(t),this._fsQuad.material=this.blendMaterial,this.copyUniforms.tDiffuse.value=this.renderTargetsHorizontal[0].texture,r&&t.state.buffers.stencil.setTest(!0),this.renderToScreen?(t.setRenderTarget(null),this._fsQuad.render(t)):(t.setRenderTarget(n),this._fsQuad.render(t)),t.setClearColor(this._oldClearColor,this._oldClearAlpha),t.autoClear=a}_getSeparableBlurMaterial(t){let e=[],n=t/3;for(let s=0;s<t;s++)e.push(.39894*Math.exp(-.5*s*s/(n*n))/n);return new re({defines:{KERNEL_RADIUS:t},uniforms:{colorTexture:{value:null},invSize:{value:new Et(.5,.5)},direction:{value:new Et(.5,.5)},gaussianCoefficients:{value:e}},vertexShader:`

				varying vec2 vUv;

				void main() {

					vUv = uv;
					gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );

				}`,fragmentShader:`

				#include <common>

				varying vec2 vUv;

				uniform sampler2D colorTexture;
				uniform vec2 invSize;
				uniform vec2 direction;
				uniform float gaussianCoefficients[KERNEL_RADIUS];

				void main() {

					float weightSum = gaussianCoefficients[0];
					vec3 diffuseSum = texture2D( colorTexture, vUv ).rgb * weightSum;

					for ( int i = 1; i < KERNEL_RADIUS; i ++ ) {

						float x = float( i );
						float w = gaussianCoefficients[i];
						vec2 uvOffset = direction * invSize * x;
						vec3 sample1 = texture2D( colorTexture, vUv + uvOffset ).rgb;
						vec3 sample2 = texture2D( colorTexture, vUv - uvOffset ).rgb;
						diffuseSum += ( sample1 + sample2 ) * w;

					}

					gl_FragColor = vec4( diffuseSum, 1.0 );

				}`})}_getCompositeMaterial(t){return new re({defines:{NUM_MIPS:t},uniforms:{blurTexture1:{value:null},blurTexture2:{value:null},blurTexture3:{value:null},blurTexture4:{value:null},blurTexture5:{value:null},bloomStrength:{value:1},bloomFactors:{value:null},bloomTintColors:{value:null},bloomRadius:{value:0}},vertexShader:`

				varying vec2 vUv;

				void main() {

					vUv = uv;
					gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );

				}`,fragmentShader:`

				varying vec2 vUv;

				uniform sampler2D blurTexture1;
				uniform sampler2D blurTexture2;
				uniform sampler2D blurTexture3;
				uniform sampler2D blurTexture4;
				uniform sampler2D blurTexture5;
				uniform float bloomStrength;
				uniform float bloomRadius;
				uniform float bloomFactors[NUM_MIPS];
				uniform vec3 bloomTintColors[NUM_MIPS];

				float lerpBloomFactor( const in float factor ) {

					float mirrorFactor = 1.2 - factor;
					return mix( factor, mirrorFactor, bloomRadius );

				}

				void main() {

					// 3.0 for backwards compatibility with previous alpha-based intensity
					vec3 bloom = 3.0 * bloomStrength * (
						lerpBloomFactor( bloomFactors[ 0 ] ) * bloomTintColors[ 0 ] * texture2D( blurTexture1, vUv ).rgb +
						lerpBloomFactor( bloomFactors[ 1 ] ) * bloomTintColors[ 1 ] * texture2D( blurTexture2, vUv ).rgb +
						lerpBloomFactor( bloomFactors[ 2 ] ) * bloomTintColors[ 2 ] * texture2D( blurTexture3, vUv ).rgb +
						lerpBloomFactor( bloomFactors[ 3 ] ) * bloomTintColors[ 3 ] * texture2D( blurTexture4, vUv ).rgb +
						lerpBloomFactor( bloomFactors[ 4 ] ) * bloomTintColors[ 4 ] * texture2D( blurTexture5, vUv ).rgb
					);

					float bloomAlpha = max( bloom.r, max( bloom.g, bloom.b ) );
					gl_FragColor = vec4( bloom, bloomAlpha );

				}`})}};Ys.BlurDirectionX=new Et(1,0);Ys.BlurDirectionY=new Et(0,1);var Kr={name:"OutputShader",uniforms:{tDiffuse:{value:null},toneMappingExposure:{value:1}},vertexShader:`
		precision highp float;

		uniform mat4 modelViewMatrix;
		uniform mat4 projectionMatrix;

		attribute vec3 position;
		attribute vec2 uv;

		varying vec2 vUv;

		void main() {

			vUv = uv;
			gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );

		}`,fragmentShader:`

		precision highp float;

		uniform sampler2D tDiffuse;

		#include <tonemapping_pars_fragment>
		#include <colorspace_pars_fragment>

		varying vec2 vUv;

		void main() {

			gl_FragColor = texture2D( tDiffuse, vUv );

			// tone mapping

			#ifdef LINEAR_TONE_MAPPING

				gl_FragColor.rgb = LinearToneMapping( gl_FragColor.rgb );

			#elif defined( REINHARD_TONE_MAPPING )

				gl_FragColor.rgb = ReinhardToneMapping( gl_FragColor.rgb );

			#elif defined( CINEON_TONE_MAPPING )

				gl_FragColor.rgb = CineonToneMapping( gl_FragColor.rgb );

			#elif defined( ACES_FILMIC_TONE_MAPPING )

				gl_FragColor.rgb = ACESFilmicToneMapping( gl_FragColor.rgb );

			#elif defined( AGX_TONE_MAPPING )

				gl_FragColor.rgb = AgXToneMapping( gl_FragColor.rgb );

			#elif defined( NEUTRAL_TONE_MAPPING )

				gl_FragColor.rgb = NeutralToneMapping( gl_FragColor.rgb );

			#elif defined( CUSTOM_TONE_MAPPING )

				gl_FragColor.rgb = CustomToneMapping( gl_FragColor.rgb );

			#endif

			// color space

			#ifdef SRGB_TRANSFER

				gl_FragColor = sRGBTransferOETF( gl_FragColor );

			#endif

		}`};var xl=class extends yn{constructor(){super(),this.isOutputPass=!0,this.uniforms=fi.clone(Kr.uniforms),this.material=new Bs({name:Kr.name,uniforms:this.uniforms,vertexShader:Kr.vertexShader,fragmentShader:Kr.fragmentShader}),this._fsQuad=new Vi(this.material),this._outputColorSpace=null,this._toneMapping=null}render(t,e,n){this.uniforms.tDiffuse.value=n.texture,this.uniforms.toneMappingExposure.value=t.toneMappingExposure,(this._outputColorSpace!==t.outputColorSpace||this._toneMapping!==t.toneMapping)&&(this._outputColorSpace=t.outputColorSpace,this._toneMapping=t.toneMapping,this.material.defines={},Wt.getTransfer(this._outputColorSpace)===jt&&(this.material.defines.SRGB_TRANSFER=""),this._toneMapping===Ir?this.material.defines.LINEAR_TONE_MAPPING="":this._toneMapping===Lr?this.material.defines.REINHARD_TONE_MAPPING="":this._toneMapping===Nr?this.material.defines.CINEON_TONE_MAPPING="":this._toneMapping===Di?this.material.defines.ACES_FILMIC_TONE_MAPPING="":this._toneMapping===Fr?this.material.defines.AGX_TONE_MAPPING="":this._toneMapping===Ur?this.material.defines.NEUTRAL_TONE_MAPPING="":this._toneMapping===Dr&&(this.material.defines.CUSTOM_TONE_MAPPING=""),this.material.needsUpdate=!0),this.renderToScreen===!0?(t.setRenderTarget(null),this._fsQuad.render(t)):(t.setRenderTarget(e),this.clear&&t.clear(t.autoClearColor,t.autoClearDepth,t.autoClearStencil),this._fsQuad.render(t))}dispose(){this.material.dispose(),this._fsQuad.dispose()}};var wh=13.200000000000001;var vl={strength:.6,radius:.4,threshold:.18};var Zn={angularSpeed:.022,elevationDeg:8,elevationPeriodS:90,radiusBreath:.04,radiusPeriodS:60,resumeDelayMs:6e3,rampUpMs:2e3},di={distancePerRadius:12,minDistance:40,maxDistance:140,azimuthOffsetRad:15*Math.PI/180,minMs:800,maxMs:1800,msPerWorldUnit:.45},yl=8e-4;function Ml(i,t){return i>.001?Math.max(t,1):1}function pd(i,t,e,n,s,r){let a=0;for(let o=0;o<s.length;o++){let l=s[o];if(!l){for(let p=0;p<r*2;p++){let y=a*3;i[y]=0,i[y+1]=0,i[y+2]=0,t[y]=0,t[y+1]=0,t[y+2]=0,e[a]=0,a++}continue}let c=l.source*3,h=l.target*3,f=n[c]??0,u=n[c+1]??0,d=n[c+2]??0,m=n[h]??0,_=n[h+1]??0,g=n[h+2]??0;for(let p=0;p<r;p++)for(let y=0;y<2;y++){let S=a*3;i[S]=f,i[S+1]=u,i[S+2]=d,t[S]=m,t[S+1]=_,t[S+2]=g,e[a]=(p+y)/r,a++}}}function Ah(i,t,e,n,s){let r=s*.32,a=0;for(let o=0;o<e.length;o++){let l=e[o];if(!l){a+=n*6;continue}let c=l.source*3,h=l.target*3,f=t[c]??0,u=t[c+1]??0,d=t[c+2]??0,m=t[h]??0,_=t[h+1]??0,g=t[h+2]??0;if(n===1||r<=0){i[a++]=f,i[a++]=u,i[a++]=d,i[a++]=m,i[a++]=_,i[a++]=g;continue}let p=(f+m)/2,y=(u+_)/2,S=(d+g)/2,b=Math.hypot(m-f,_-u,g-d),T=Math.hypot(p,y,S),w,R,v;if(T>.001)w=p/T,R=y/T,v=S/T;else{let z=m-f,V=g-d,$=Math.hypot(V,z);$>1e-6?(w=V/$,R=0,v=-z/$):(w=1,R=0,v=0)}let E=r*b,L=p+w*E,C=y+R*E,D=S+v*E,H=f,W=u,U=d;for(let z=1;z<=n;z++){let V=z/n,$=(1-V)*(1-V),tt=2*(1-V)*V,ct=V*V,Mt=$*f+tt*L+ct*m,St=$*u+tt*C+ct*_,qt=$*d+tt*D+ct*g;i[a++]=H,i[a++]=W,i[a++]=U,i[a++]=Mt,i[a++]=St,i[a++]=qt,H=Mt,W=St,U=qt}}}function Th(i){return i!==void 0&&Number.isFinite(i)?i:0}function md(i,t,e){let n=Number.isFinite(i)?Math.min(Math.max(i,0),1):i>0?1:0,s=Number.isFinite(e)&&e>0?e:1,a=(Number.isFinite(t)?Math.max(t,0):0)/s*.55,o=Math.min(Math.max((n-a)/.45,0),1);return 1-Math.pow(1-o,3)}function gd(i,t){let e=1,n=Math.min(Math.max(Math.floor(t),0),Math.floor(i.length/3));for(let s=0;s<n;s++){let r=Math.hypot(Th(i[s*3]),Th(i[s*3+1]),Th(i[s*3+2]));r>e&&(e=r)}return e}var _d=`
vec3 revealPosition(vec3 targetPosition) {
	if (uRevealActive < 0.5) return targetPosition;
	float delay = (length(targetPosition) / max(uRevealMaxRadius, 0.0001)) * ${.55.toFixed(2)};
	float localProgress = clamp((uRevealProgress - delay) / ${.45.toFixed(2)}, 0.0, 1.0);
	float scale = 1.0 - pow(1.0 - localProgress, 3.0);
	return targetPosition * scale;
}
`,xd=`
attribute float aSize;
attribute float aGhost;
attribute float aDim;
varying vec3 vColor;
varying float vGhost;
varying float vDim;
uniform float uPixelScale; // drawingBufferHeight / (2·tan(fov/2))
uniform float uSizeMul; // 控制面板「节点大小」倍率
uniform float uMaxPoint; // 设备像素钳制：穿行星团时防满屏大精灵打爆填充率（M3）
uniform float uRevealActive;
uniform float uRevealProgress;
uniform float uRevealMaxRadius;

${_d}

void main() {
	vColor = color;
	vGhost = aGhost;
	vDim = aDim;
	vec4 mv = modelViewMatrix * vec4(revealPosition(position), 1.0);
	gl_PointSize = min(aSize * uSizeMul * uPixelScale / max(-mv.z, 1.0), uMaxPoint);
	gl_Position = projectionMatrix * mv;
}
`,vd=`
varying vec3 vColor;
varying float vGhost;
varying float vDim;
uniform float uLightMode; // 0 = 深空（白热核心），1 = 晨昼（墨水圆盘 + rim）

void main() {
	vec2 uv = gl_PointCoord - 0.5;
	float d = length(uv);

	float core = smoothstep(0.18, 0.0, d) * 0.55 * (1.0 - vGhost) * (1.0 - uLightMode);
	vec3 col = mix(vColor, vec3(1.0), core);

	// 晨昼：外缘 1px 深色 rim，让节点「坐在纸上」
	float rim = smoothstep(0.40, 0.46, d) * smoothstep(0.50, 0.46, d);
	col = mix(col, col * 0.72, rim * uLightMode);

	// ams-life: aGhost marks a private point and draws it as a hollow ring
	// (Galaxy View used it for a dimmer unresolved note).
	float ring = mix(1.0, smoothstep(0.17, 0.27, d), vGhost);
	float alpha = smoothstep(0.5, 0.42, d) * ring * vDim;
	if (alpha < 0.01) discard;
	gl_FragColor = vec4(col, alpha);
}
`,by=`
attribute vec3 aSourcePosition;
attribute vec3 aTargetPosition;
attribute float aCurveT;
uniform float uLinkCurvature;
uniform float uRevealActive;
uniform float uRevealProgress;
uniform float uRevealMaxRadius;

${_d}
`,Sy=`
	vec3 source = revealPosition(aSourcePosition);
	vec3 target = revealPosition(aTargetPosition);
	vec3 midpoint = (source + target) * 0.5;
	vec3 edge = target - source;
	float edgeLength = length(edge);
	float midpointRadius = length(midpoint);
	vec3 direction;
	if (midpointRadius > 0.001) {
		direction = midpoint / midpointRadius;
	} else {
		float perpendicularLength = length(vec2(edge.z, edge.x));
		direction = perpendicularLength > 0.000001
			? vec3(edge.z / perpendicularLength, 0.0, -edge.x / perpendicularLength)
			: vec3(1.0, 0.0, 0.0);
	}
	vec3 control = midpoint + direction * (uLinkCurvature * ${.32.toFixed(2)} * edgeLength);
	float inverseT = 1.0 - aCurveT;
	vec3 curvePosition =
		inverseT * inverseT * source +
		2.0 * inverseT * aCurveT * control +
		aCurveT * aCurveT * target;
	vec3 transformed = curvePosition;
`;function yd(i,t){let e="void main() {",n="#include <begin_vertex>";if(!i.vertexShader.includes(e)||!i.vertexShader.includes(n))throw new Error("Three line shader anchors changed; reveal patch cannot be applied safely");Object.assign(i.uniforms,t),i.vertexShader=i.vertexShader.replace(e,`${by}
${e}`).replace(n,Sy)}function Rh(i){let t=2166136261;for(let e=0;e<i.length;e++)t^=i.charCodeAt(e),t=Math.imul(t,16777619);return t>>>0}function Ch(i){return Rh(i)/4294967295}function Md(i,t){let e=Ch(i),n=Ch(i+":v"),s=Ch(i+":w"),r=t*Math.cbrt(e),a=2*Math.PI*n,o=Math.acos(2*s-1);return[r*Math.sin(o)*Math.cos(a),r*Math.sin(o)*Math.sin(a),r*Math.cos(o)]}function bd(i){return 80*Math.cbrt(Math.max(i,1)/1e3)}var Ad=i=>i.tag?Ty:Ey(i.folderTop,i.unresolved);var Sd=[0,40,80,120,160,200,240,280,320],wy=new dt("#9aa4b2"),Ay=new dt("#7a8499"),Ty=new dt("#d8a94b"),wd=new Map;function Ey(i,t){if(t)return Ay;if(i==="")return wy;let e=wd.get(i);if(!e){let n=Sd[Rh(i)%Sd.length]??0;e=new dt().setHSL(n/360,.6,.6),wd.set(i,e)}return e}function Td(i,t){let e=i.clone().lerp(t,.5),n={h:0,s:0,l:0};return e.getHSL(n),e.setHSL(n.h,n.s*.4,Math.min(n.l,.35)),e}var Cy=[{count:2600,size:1.2},{count:900,size:2},{count:250,size:3}],Ed=new dt("#9da8c4"),Cd=new dt("#ffffff"),Rd=new dt("#ffe9c9"),Pd=new dt("#bfd3ff");function Id(i){let t=i>>>0;return()=>{t=t+1831565813>>>0;let e=t;return e=Math.imul(e^e>>>15,e|1),e^=e+Math.imul(e^e>>>7,e|61),((e^e>>>14)>>>0)/4294967296}}function Ph(i){for(let t of i.children){let e=t;e.geometry.dispose(),e.material.dispose()}}var bl=class{constructor(t,e){this.geometry=t;this.starCount=e;q(this,"baseColors");q(this,"attr");q(this,"active",null);q(this,"nextIn",3);this.attr=t.getAttribute("color"),this.baseColors=new Float32Array(this.attr.array)}update(t,e){if(this.active){this.active.t+=t;let n=this.active.t,s=1.6,r=this.attr.array,a=this.active.index*3,o=n>=s?1:1+2.2*Math.sin(Math.PI*n/s);r[a]=(this.baseColors[a]??1)*o,r[a+1]=(this.baseColors[a+1]??1)*o,r[a+2]=(this.baseColors[a+2]??1)*o,this.attr.needsUpdate=!0,n>=s&&(this.active=null);return}e<=.01||(this.nextIn-=t,this.nextIn<=0&&(this.active={index:Math.floor(Math.random()*this.starCount),t:0},this.nextIn=Math.min(Math.max(-Math.log(Math.random()+1e-9)*(6/e),1.5),90)))}};function Ld(i,t,e=1){let n=Math.max(Math.round(1200*t*e),1),s=Id(3108379),r=new Float32Array(n*3),a=new Float32Array(n*3);for(let h=0;h<n;h++){let f=i*(.3+.7*Math.cbrt(s())),u=2*Math.PI*s(),d=Math.acos(2*s()-1);r[h*3]=f*Math.sin(d)*Math.cos(u),r[h*3+1]=f*Math.sin(d)*Math.sin(u),r[h*3+2]=f*Math.cos(d);let m=s(),_=(m<.85?Ed.clone().lerp(Cd,s()):m<.95?Rd.clone():Pd.clone()).multiplyScalar(.75);a[h*3]=_.r,a[h*3+1]=_.g,a[h*3+2]=_.b}let o=new te;o.setAttribute("position",new Lt(r,3)),o.setAttribute("color",new Lt(a,3));let l=new ci({size:2.4,sizeAttenuation:!0,vertexColors:!0,transparent:!0,opacity:.6,depthWrite:!1}),c=new an(o,l);return c.renderOrder=-1,c.frustumCulled=!1,c}function Ih(i,t=1){let e=new si,n=Id(5340353),s=null;for(let r of Cy){let a={count:Math.max(Math.round(r.count*t),50),size:r.size},o=new Float32Array(a.count*3),l=new Float32Array(a.count*3);for(let u=0;u<a.count;u++){let d=2*Math.PI*n(),m=Math.acos(2*n()-1),_=i*(.95+.1*n());o[u*3]=_*Math.sin(m)*Math.cos(d),o[u*3+1]=_*Math.sin(m)*Math.sin(d),o[u*3+2]=_*Math.cos(m);let g=n(),p=g<.85?Ed.clone().lerp(Cd,n()):g<.95?Rd.clone():Pd.clone();a.size>=3&&n()<.03&&p.multiplyScalar(1.8),l[u*3]=p.r,l[u*3+1]=p.g,l[u*3+2]=p.b}let c=new te;c.setAttribute("position",new Lt(o,3)),c.setAttribute("color",new Lt(l,3));let h=new ci({size:a.size,sizeAttenuation:!1,vertexColors:!0,transparent:!0,opacity:.55,depthWrite:!1}),f=new an(c,h);f.renderOrder=-1,e.add(f),a.size>=3&&(s=new bl(c,a.count))}return{group:e,twinkler:s??new bl(new te().setAttribute("color",new Lt(new Float32Array(3),3)),1)}}var Lh=null;function Ry(){return Lh||(Lh=new Float64Array(2048)),Lh}function Ae(i){return i!==void 0&&Number.isFinite(i)?i:0}function Nd(i,t,e,n,s){let r=Math.min(Math.max(Math.floor(e),0),Math.floor(i.length/3),Math.floor(t.length/3));if(r===0)return{center:[0,0,0],scale:1,sourceRadius:0};let a=0,o=0,l=0,c=0;for(let d=0;d<r;d++){let m=Math.max(Ae(s?.[d]),0);a+=m,o+=Ae(i[d*3])*m,l+=Ae(i[d*3+1])*m,c+=Ae(i[d*3+2])*m}let h=a>0;if(h)o/=a,l/=a,c/=a;else{for(let d=0;d<r;d++)o+=Ae(i[d*3]),l+=Ae(i[d*3+1]),c+=Ae(i[d*3+2]);o/=r,l/=r,c/=r}let f=0;if(h){let d=0;for(let m=0;m<r;m++){if(Math.max(Ae(s?.[m]),0)<=0)continue;let _=Ae(i[m*3])-o,g=Ae(i[m*3+1])-l,p=Ae(i[m*3+2])-c,y=Math.hypot(_,g,p);y>d&&(d=y)}if(d>0){let m=Ry();m.fill(0);for(let p=0;p<r;p++){let y=Math.max(Ae(s?.[p]),0);if(y<=0)continue;let S=Ae(i[p*3])-o,b=Ae(i[p*3+1])-l,T=Ae(i[p*3+2])-c,w=Math.hypot(S,b,T),R=Math.min(Math.floor(w/d*2048),2047);m[R]=(m[R]??0)+y}let _=a*.95,g=0;for(let p=0;p<2048;p++)if(g+=m[p]??0,g>=_){f=(p+1)/2048*d;break}f===0&&(f=d)}}else for(let d=0;d<r;d++){let m=Ae(i[d*3])-o,_=Ae(i[d*3+1])-l,g=Ae(i[d*3+2])-c;f=Math.max(f,Math.hypot(m,_,g))}let u=f>n&&n>0?n/f:1;for(let d=0;d<r;d++)t[d*3]=(Ae(i[d*3])-o)*u,t[d*3+1]=(Ae(i[d*3+1])-l)*u,t[d*3+2]=(Ae(i[d*3+2])-c)*u;return{center:[o,l,c],scale:u,sourceRadius:f}}function Sl(i,t,e){let n=i*374761393+t*668265263+e*1442695|0;return n=Math.imul(n^n>>>13,1274126177),((n^n>>>16)>>>0)/4294967296}function Py(i){let t=i>>>0;return()=>{t=t+1831565813>>>0;let e=t;return e=Math.imul(e^e>>>15,e|1),e^=e+Math.imul(e^e>>>7,e|61),((e^e>>>14)>>>0)/4294967296}}var Iy=4e-4,Ly=`
attribute float aSize;
attribute vec3 aColor;
varying vec3 vColor;
uniform float uPixelScale;
uniform float uMaxPoint;

void main() {
	vColor = aColor;
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	gl_PointSize = min(aSize * uPixelScale / max(-mv.z, 1.0), uMaxPoint);
	gl_Position = projectionMatrix * mv;
}
`,Ny=`
varying vec3 vColor;
uniform float uIntensity;

void main() {
	// r: 0=中心 → 1=精灵半径；很软的高斯，让相邻云片无缝融合成雾（不是一颗颗圆斑）
	float r = length(gl_PointCoord - 0.5) * 2.0;
	float a = exp(-r * r * 2.6) - 0.0743; // r=1 处精确归零；系数偏大=中心不实、边缘更飘
	if (a < 0.003) discard;
	// 系数压到「薄如雾」：颜色 0.30 / 透明度 0.22——加色叠加下浓处仍成色，但不再有实体块感
	gl_FragColor = vec4(vColor * uIntensity * 0.30, a * uIntensity * 0.22);
}
`,Dd=6,Fd=24,Jr=Dd*Fd,Tl=class{constructor(t){q(this,"object");q(this,"radius");q(this,"scale",1);q(this,"count",0);this.radius=t;let e=new te;e.setAttribute("position",new Lt(new Float32Array(Jr*3),3)),e.setAttribute("aColor",new Lt(new Float32Array(Jr*3),3)),e.setAttribute("aSize",new Lt(new Float32Array(Jr),1)),e.setDrawRange(0,0);let n=new re({vertexShader:Ly,fragmentShader:Ny,transparent:!0,depthWrite:!1,blending:Dn,uniforms:{uPixelScale:{value:1},uMaxPoint:{value:1600},uIntensity:{value:0}}});this.object=new an(e,n),this.object.renderOrder=-1,this.object.frustumCulled=!1}setQuality(t){this.scale=t}bake(t,e){let n=Py(40503),s=this.object.geometry.getAttribute("position"),r=this.object.geometry.getAttribute("aColor"),a=this.object.geometry.getAttribute("aSize"),o=s.array,l=r.array,c=a.array,h=this.radius,f=new dt(t),u=new dt(e),d={h:0,s:0,l:0},m=new dt,_=Math.max(2,Math.round(Dd*this.scale)),g=Math.max(6,Math.round(Fd*this.scale)),p=0;for(let y=0;y<_&&p<Jr;y++){let S=2*Math.PI*n(),b=Math.acos(2*n()-1),T=h*(.7+1.7*n()),w=T*Math.sin(b)*Math.cos(S),R=T*Math.sin(b)*Math.sin(S)*.75,v=T*Math.cos(b),E=h*(.5+.5*n());m.copy(f).lerp(u,n()),m.getHSL(d),m.setHSL(d.h+(n()-.5)*.05,Math.min(d.s*.85,.9),.16+.08*n());for(let L=0;L<g&&p<Jr;L++){let C=(n()+n()+n()-1.5)*E,D=(n()+n()+n()-1.5)*E*.8,H=(n()+n()+n()-1.5)*E;o[p*3]=w+C,o[p*3+1]=R+D,o[p*3+2]=v+H;let W=n()<.25;c[p]=h*(W?1+.8*n():.4+.5*n());let U=.85+.3*n();l[p*3]=m.r*U,l[p*3+1]=m.g*U,l[p*3+2]=m.b*U,p++}}this.count=p,s.needsUpdate=!0,r.needsUpdate=!0,a.needsUpdate=!0,this.object.geometry.setDrawRange(0,p)}setPixelScale(t,e){this.object.material.uniforms.uPixelScale.value=t,this.object.material.uniforms.uMaxPoint.value=e}setIntensity(t){this.object.material.uniforms.uIntensity.value=t,this.object.visible=t>.005&&this.count>0}get visible(){return this.object.visible}update(t){this.object.rotation.y+=Iy*t}dispose(){this.object.geometry.dispose(),this.object.material.dispose()}},Dy=`
attribute float aSize;
varying vec3 vColor;
uniform float uPixelScale;
uniform float uMaxPoint;

void main() {
	vColor = color;
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	gl_PointSize = min(aSize * uPixelScale / max(-mv.z, 1.0), uMaxPoint);
	gl_Position = projectionMatrix * mv;
}
`,Fy=`
varying vec3 vColor;
uniform float uIntensity;

void main() {
	vec2 uv = gl_PointCoord - 0.5;
	float d2 = dot(uv, uv);
	float a = exp(-d2 * 10.0) - 0.0821; // 软高斯，r=0.5 处精确归零（无方形硬边）
	if (a < 0.004) discard;
	gl_FragColor = vec4(vColor * uIntensity * 0.55, a * uIntensity * 0.4);
}
`,wl=10,Al=3,El=class{constructor(){q(this,"points");q(this,"memberSamples",[]);q(this,"count",0);let t=new te;t.setAttribute("position",new Lt(new Float32Array(wl*Al*3),3)),t.setAttribute("color",new Lt(new Float32Array(wl*Al*3),3)),t.setAttribute("aSize",new Lt(new Float32Array(wl*Al),1)),t.setDrawRange(0,0);let e=new re({vertexShader:Dy,fragmentShader:Fy,vertexColors:!0,transparent:!0,depthWrite:!1,blending:Dn,uniforms:{uPixelScale:{value:1},uMaxPoint:{value:300},uIntensity:{value:0}}});this.points=new an(t,e),this.points.renderOrder=-1,this.points.frustumCulled=!1}rebuild(t,e,n){let s=t.nodes,r=s.length;if(this.memberSamples=[],r<20){this.count=0,this.points.geometry.setDrawRange(0,0);return}let a=Array.from({length:r},(g,p)=>p).sort((g,p)=>(s[p]?.degree??0)-(s[g]?.degree??0)),o=[],l=n*.5;for(let g of a.slice(0,250)){let p=e[g*3]??0,y=e[g*3+1]??0,S=e[g*3+2]??0,b=!0;for(let T of o)if(Math.hypot(p-(e[T*3]??0),y-(e[T*3+1]??0),S-(e[T*3+2]??0))<l){b=!1;break}if(b&&o.push(g),o.length>=wl)break}let c=this.points.geometry.getAttribute("position"),h=this.points.geometry.getAttribute("aSize"),f=c.array,u=h.array,d=n*.33,m=0,_=11;for(let g of o){let p=e[g*3]??0,y=e[g*3+1]??0,S=e[g*3+2]??0,b=[],T=0,w=0,R=0;for(let C=0;C<r;C++){let D=(e[C*3]??0)-p,H=(e[C*3+1]??0)-y,W=(e[C*3+2]??0)-S;D*D+H*H+W*W<d*d&&(b.push(C),T+=e[C*3]??0,w+=e[C*3+1]??0,R+=e[C*3+2]??0)}if(b.length<8)continue;T/=b.length,w/=b.length,R/=b.length;let v=0;for(let C of b)v+=((e[C*3]??0)-T)**2+((e[C*3+1]??0)-w)**2+((e[C*3+2]??0)-R)**2;let E=Math.sqrt(v/b.length),L=b.length>120?b.filter((C,D)=>D%Math.ceil(b.length/120)===0):b;for(let C=0;C<Al;C++){let D=(Sl(_,C,3)-.5)*E,H=(Sl(_,C,5)-.5)*E*.7,W=(Sl(_,C,7)-.5)*E;f[m*3]=T+D,f[m*3+1]=w+H,f[m*3+2]=R+W,u[m]=E*(1.6+.8*Sl(_,C,13)),this.memberSamples.push(L),m++}_++}this.count=m,c.needsUpdate=!0,h.needsUpdate=!0,this.points.geometry.setDrawRange(0,m)}clear(){this.count=0,this.memberSamples=[],this.points.geometry.setDrawRange(0,0)}recolor(t){if(this.count===0)return;let e=this.points.geometry.getAttribute("color"),n=e.array,s={h:0,s:0,l:0},r=new dt;for(let a=0;a<this.count;a++){let o=this.memberSamples[a]??[];r.setRGB(0,0,0);for(let l of o)r.add(t(l));o.length>0&&r.multiplyScalar(1/o.length),r.getHSL(s),r.setHSL(s.h,Math.min(s.s*1.25,1),.4),n[a*3]=r.r,n[a*3+1]=r.g,n[a*3+2]=r.b}e.needsUpdate=!0}setIntensity(t){this.points.material.uniforms.uIntensity.value=t,this.points.visible=t>.005&&this.count>0}get intensity(){return this.points.material.uniforms.uIntensity.value}setPixelScale(t,e){this.points.material.uniforms.uPixelScale.value=t,this.points.material.uniforms.uMaxPoint.value=e}dispose(){this.points.geometry.dispose(),this.points.material.dispose()}};function Ud(i,t){return Math.min(i,t)}var $r={high:{id:"high",pixelRatioCap:2,bloomAllowed:!0,starScale:1,linkSegments:8,clusterCloudsAllowed:!0,nodeCap:null,linkCap:null,hubLabels:14,neighborLabels:20,hoverThrottleMs:30},low:{id:"low",pixelRatioCap:1,bloomAllowed:!0,starScale:.4,linkSegments:6,clusterCloudsAllowed:!0,nodeCap:null,linkCap:null,hubLabels:8,neighborLabels:12,hoverThrottleMs:80},mobile:{id:"mobile",pixelRatioCap:1.5,bloomAllowed:!1,starScale:.32,linkSegments:4,clusterCloudsAllowed:!1,nodeCap:1500,linkCap:12e3,hubLabels:6,neighborLabels:8,hoverThrottleMs:null}};var jr={id:"deep-space",background:3,starfield:!0,space:!0,motes:!1,bloomEnabled:!0,lightMode:!1,nodeLightness:null,linkInk:null,linkOpacityScale:1,panelClass:"gx-theme-dark"},Nh={id:"daylight",background:16184559,starfield:!1,space:!1,motes:!0,bloomEnabled:!1,lightMode:!0,nodeLightness:.44,linkInk:"#2e2a24",linkOpacityScale:.65,panelClass:"gx-theme-light"};var Oy=.28,Rl=class{constructor(t,e){q(this,"camera");q(this,"renderer");q(this,"scene",new _r);q(this,"composer");q(this,"bloomPass");q(this,"outputPass");q(this,"renderPass");q(this,"nodePoints",null);q(this,"nodeMaterial",null);q(this,"nodeGeometry",null);q(this,"linkSegments",null);q(this,"linkGeometry",null);q(this,"linkMaterial",null);q(this,"revealLinkMaterial",null);q(this,"selSegments",null);q(this,"selGeometry",null);q(this,"selMaterial",null);q(this,"revealSelMaterial",null);q(this,"ghostSegments",null);q(this,"ghostGeometry",null);q(this,"ghostMaterial",null);q(this,"ghostLinks",[]);q(this,"selLinkIdx",[]);q(this,"selLinks",[]);q(this,"selTier1",[]);q(this,"selTier2",[]);q(this,"starfield");q(this,"twinkler");q(this,"starfieldEnabled",!0);q(this,"twinkleFreq",.5);q(this,"motes",null);q(this,"linkCurvature",0);q(this,"tierLinkSegs",8);q(this,"linkK",1);q(this,"space",{nebula:0,fieldStars:0,clusterClouds:0});q(this,"nebula",null);q(this,"clouds",null);q(this,"fieldStars",null);q(this,"fieldStarsDensity",0);q(this,"nebulaTintA","#46d4dc");q(this,"nebulaTintB","#9a7fe0");q(this,"tierCloudsAllowed",!0);q(this,"tierStarScale",1);q(this,"reveal",null);q(this,"revealActiveUniform",{value:0});q(this,"revealProgressUniform",{value:1});q(this,"revealMaxRadiusUniform",{value:1});q(this,"linkCurvatureUniform",{value:0});q(this,"data",{nodes:[],links:[]});q(this,"positions",new Float32Array(0));q(this,"renderPositions",new Float32Array(0));q(this,"nodeTargetPositions",new Float32Array(0));q(this,"fitWeights",new Float32Array(0));q(this,"sizes",new Float32Array(0));q(this,"dimCurrent",new Float32Array(0));q(this,"dimTarget",new Float32Array(0));q(this,"dimAnimating",!1);q(this,"colorFn",Ad);q(this,"tokens",jr);q(this,"tierBloomAllowed",!0);q(this,"lastW",2);q(this,"lastH",2);q(this,"baseLinkOpacity",.16);q(this,"focusActive",!1);q(this,"graphRadiusEstimate");q(this,"projVec",new P);q(this,"ghostSourceVec",new P);q(this,"ghostTargetVec",new P);q(this,"pixelScale",1);q(this,"nodeScale",1);q(this,"sizeMode","degree");this.graphRadiusEstimate=e,this.renderer=new ul({antialias:!1,alpha:!1}),this.renderer.setPixelRatio(Math.min(window.devicePixelRatio,2)),this.renderer.toneMapping=Di,this.renderer.toneMappingExposure=1.05,this.renderer.info.autoReset=!1,t.appendChild(this.renderer.domElement),this.scene.background=new dt(this.tokens.background),this.camera=new Ye(60,1,.5,5e4);let n=Ih(e*6.5);this.starfield=n.group,this.twinkler=n.twinkler,this.scene.add(this.starfield),this.composer=new gl(this.renderer),this.renderPass=new _l(this.scene,this.camera),this.bloomPass=new Ys(new Et(2,2),vl.strength,vl.radius,vl.threshold),this.outputPass=new xl,this.composer.addPass(this.renderPass),this.composer.addPass(this.bloomPass),this.composer.addPass(this.outputPass)}setColorFn(t){this.colorFn=t}setData(t,e){this.resetRevealState(),this.data=t,this.positions=e,this.disposeGraphObjects();let n=t.nodes.length;this.renderPositions=new Float32Array(n*3),this.nodeTargetPositions=new Float32Array(n*3),this.fitWeights=new Float32Array(n);let s=new Float32Array(n);this.sizes=new Float32Array(n),this.dimCurrent=new Float32Array(n).fill(1),this.dimTarget=new Float32Array(n).fill(1);for(let r=0;r<n;r++){let a=t.nodes[r];a&&(s[r]=a.unresolved?1:0,this.fitWeights[r]=a.degree,this.sizes[r]=this.computeSize(a))}this.fitPositions(),this.nodeTargetPositions.set(this.renderPositions),this.nodeGeometry=new te,this.nodeGeometry.setAttribute("position",new Lt(this.nodeTargetPositions,3).setUsage(ki)),this.nodeGeometry.setAttribute("color",new Lt(new Float32Array(n*3),3)),this.nodeGeometry.setAttribute("aSize",new Lt(this.sizes,1)),this.nodeGeometry.setAttribute("aGhost",new Lt(s,1)),this.nodeGeometry.setAttribute("aDim",new Lt(this.dimCurrent,1)),this.nodeMaterial=new re({vertexShader:xd,fragmentShader:vd,vertexColors:!0,transparent:!0,depthWrite:!1,uniforms:{uPixelScale:{value:this.pixelScale},uSizeMul:{value:this.nodeScale},uLightMode:{value:this.tokens.lightMode?1:0},uMaxPoint:{value:110*this.renderer.getPixelRatio()},uRevealActive:this.revealActiveUniform,uRevealProgress:this.revealProgressUniform,uRevealMaxRadius:this.revealMaxRadiusUniform}}),this.nodePoints=new an(this.nodeGeometry,this.nodeMaterial),this.nodePoints.renderOrder=1,this.nodePoints.frustumCulled=!1,this.scene.add(this.nodePoints),this.buildLinkLayer(),this.clouds?.clear(),this.recolor(),this.updatePositions(),this.buildSelLayer()}buildLinkLayer(){this.linkSegments&&(this.scene.remove(this.linkSegments),this.linkGeometry?.dispose(),this.linkMaterial?.dispose());let t=this.data.links.length;this.linkK=Ml(this.linkCurvature,this.tierLinkSegs),this.linkGeometry=new te,this.linkGeometry.setAttribute("position",new Lt(new Float32Array(t*this.linkK*2*3),3)),this.linkGeometry.setAttribute("color",new Lt(new Float32Array(t*this.linkK*2*3),3)),this.linkMaterial=new li({vertexColors:!0,transparent:!0,opacity:this.effectiveLinkOpacity(),depthWrite:!1}),this.linkSegments=new rs(this.linkGeometry,this.linkMaterial),this.linkSegments.renderOrder=0,this.linkSegments.frustumCulled=!1,this.scene.add(this.linkSegments)}setGhostLinks(t){this.ghostLinks=t,this.buildGhostLayer()}buildGhostLayer(){this.ghostSegments&&(this.scene.remove(this.ghostSegments),this.ghostGeometry?.dispose(),this.ghostMaterial?.dispose(),this.ghostSegments=null,this.ghostGeometry=null,this.ghostMaterial=null);let t=this.ghostLinks.length;if(t===0)return;this.ghostGeometry=new te,this.ghostGeometry.setAttribute("position",new Lt(new Float32Array(t*2*3),3));let e=new Float32Array(t*2*3),n=this.tokens.lightMode?.35:.8;for(let s=0;s<t;s++){let r=this.ghostLinks[s]?.score??.5,a=n*(.45+.55*r);for(let o=0;o<2;o++)e[(s*2+o)*3]=a,e[(s*2+o)*3+1]=a,e[(s*2+o)*3+2]=a*1.08}this.ghostGeometry.setAttribute("color",new Lt(e,3)),this.ghostMaterial=new Ar({vertexColors:!0,transparent:!0,opacity:.22,depthWrite:!1,dashSize:2.6,gapSize:3.4}),this.ghostSegments=new rs(this.ghostGeometry,this.ghostMaterial),this.ghostSegments.renderOrder=0,this.ghostSegments.frustumCulled=!1,this.scene.add(this.ghostSegments),this.updateGhostPositions()}updateGhostPositions(){if(!this.ghostGeometry||!this.ghostSegments)return;let t=this.ghostGeometry.getAttribute("position"),e=t.array;for(let n=0;n<this.ghostLinks.length;n++){let s=this.ghostLinks[n];s&&(this.displayPosition(s.source,this.ghostSourceVec),this.displayPosition(s.target,this.ghostTargetVec),e[n*6]=this.ghostSourceVec.x,e[n*6+1]=this.ghostSourceVec.y,e[n*6+2]=this.ghostSourceVec.z,e[n*6+3]=this.ghostTargetVec.x,e[n*6+4]=this.ghostTargetVec.y,e[n*6+5]=this.ghostTargetVec.z)}t.needsUpdate=!0,this.ghostSegments.computeLineDistances()}setLinkCurve(t){this.linkCurvature=t,this.linkCurvatureUniform.value=t,Ml(t,this.tierLinkSegs)!==this.linkK&&(this.buildLinkLayer(),this.recolor(),this.buildSelLayer(),this.reveal&&this.activateRevealLinkLayer(this.reveal.target)),this.reveal||this.updatePositions()}computeSize(t){switch(this.sizeMode){case"fileSize":return Math.min(Math.max(2.2*(.7+1.1*Math.cbrt(t.fileSize/4096)),1.6),wh);case"uniform":return 2.2*1.3;default:return Math.min(2.2*(1+.5*Math.sqrt(t.degree)),wh)}}setSizeMode(t){if(this.sizeMode=t,!!this.nodeGeometry){for(let e=0;e<this.data.nodes.length;e++){let n=this.data.nodes[e];n&&(this.sizes[e]=this.computeSize(n))}this.nodeGeometry.getAttribute("aSize").needsUpdate=!0}}playReveal(t=2600){let e=this.data.nodes.length;if(e===0||!this.nodeGeometry||!this.linkGeometry)return;this.resetRevealState(),this.updatePositions();let n=new Float32Array(this.renderPositions),s=gd(n,e);this.reveal={elapsedMs:0,durMs:Math.max(t,1),maxR:s,target:n},this.revealActiveUniform.value=1,this.revealProgressUniform.value=0,this.revealMaxRadiusUniform.value=s,this.activateRevealLinkLayer(n),this.activateRevealSelectionLayer(n),this.ghostMaterial&&(this.ghostMaterial.opacity=0),this.updateGhostPositions(),this.renderer.compile(this.scene,this.camera)}stepReveal(t){let e=this.reveal;if(!e)return;let n=Number.isFinite(t)?Math.max(t,0):0;e.elapsedMs+=n*1e3;let s=Math.min(e.elapsedMs/e.durMs,1);this.revealProgressUniform.value=s,this.syncRevealLinkOpacity(s),this.ghostMaterial&&(this.ghostMaterial.opacity=.22*Math.min(s*1.6,1)),this.updateGhostPositions(),s>=1&&(this.resetRevealState(),this.updatePositions(),this.refreshClusterClouds())}fillRevealAttributes(t,e,n,s){let r=n.length*s*2,a=r*3,o=t.getAttribute("aSourcePosition"),l=t.getAttribute("aTargetPosition"),c=t.getAttribute("aCurveT"),h=o?.array instanceof Float32Array&&o.array.length===a&&l?.array instanceof Float32Array&&l.array.length===a&&c?.array instanceof Float32Array&&c.array.length===r,f=h?o.array:new Float32Array(a),u=h?l.array:new Float32Array(a),d=h?c.array:new Float32Array(r);pd(f,u,d,e,n,s),h?(o.needsUpdate=!0,l.needsUpdate=!0,c.needsUpdate=!0):(t.setAttribute("aSourcePosition",new Lt(f,3)),t.setAttribute("aTargetPosition",new Lt(u,3)),t.setAttribute("aCurveT",new Lt(d,1)))}createRevealLinkMaterial(t){let e=new li({vertexColors:!0,transparent:!0,opacity:t,depthWrite:!1});return e.onBeforeCompile=n=>{yd(n,{uLinkCurvature:this.linkCurvatureUniform,uRevealActive:this.revealActiveUniform,uRevealProgress:this.revealProgressUniform,uRevealMaxRadius:this.revealMaxRadiusUniform})},e.customProgramCacheKey=()=>"galaxy-reveal-basic-v1",e}activateRevealLinkLayer(t){let e=this.linkGeometry,n=this.linkSegments;!e||!n||(this.fillRevealAttributes(e,t,this.data.links,this.linkK),this.linkCurvatureUniform.value=this.linkCurvature,this.revealLinkMaterial??=this.createRevealLinkMaterial(this.effectiveLinkOpacity()),this.revealLinkMaterial.opacity=this.effectiveLinkOpacity()*Math.min(this.revealProgressUniform.value*1.6,1),n.material=this.revealLinkMaterial)}activateRevealSelectionLayer(t){!this.selGeometry||!this.selSegments||this.selLinks.length===0||(this.fillRevealAttributes(this.selGeometry,t,this.selLinks,this.linkK),this.revealSelMaterial??=this.createRevealLinkMaterial(.85),this.revealSelMaterial.opacity=.85*Math.min(this.revealProgressUniform.value*1.6,1),this.selSegments.material=this.revealSelMaterial)}syncRevealLinkOpacity(t){let e=Math.min(Math.max(t,0)*1.6,1);this.revealLinkMaterial&&(this.revealLinkMaterial.opacity=this.effectiveLinkOpacity()*e),this.revealSelMaterial&&(this.revealSelMaterial.opacity=.85*e)}resetRevealState(){this.reveal=null,this.revealActiveUniform.value=0,this.revealProgressUniform.value=1,this.revealMaxRadiusUniform.value=1,this.linkSegments&&this.linkMaterial&&(this.linkSegments.material=this.linkMaterial),this.selSegments&&this.selMaterial&&(this.selSegments.material=this.selMaterial),this.ghostMaterial&&(this.ghostMaterial.opacity=.22)}get revealing(){return this.reveal!==null}recolor(){if(!this.nodeGeometry||!this.linkGeometry)return;let t=this.data.nodes.length,e=this.nodeGeometry.getAttribute("color"),n=e.array,s=new Array(t),r={h:0,s:0,l:0};for(let f=0;f<t;f++){let u=this.data.nodes[f];if(!u)continue;let d=this.colorFn(u).clone();this.tokens.nodeLightness!==null&&(d.getHSL(r),d=d.setHSL(r.h,r.s*.95,this.tokens.nodeLightness)),s[f]=d,n[f*3]=d.r,n[f*3+1]=d.g,n[f*3+2]=d.b}e.needsUpdate=!0;let a=this.linkGeometry.getAttribute("color"),o=a.array,l=this.tokens.linkInk?new dt(this.tokens.linkInk):null,c=new dt("#7a87a8"),h=this.linkK*2;for(let f=0;f<this.data.links.length;f++){let u=this.data.links[f];if(!u)continue;let d=l??Td(s[u.source]??c,s[u.target]??c);for(let m=0;m<h;m++)o[(f*h+m)*3]=d.r,o[(f*h+m)*3+1]=d.g,o[(f*h+m)*3+2]=d.b}a.needsUpdate=!0,this.clouds?.recolor(f=>{let u=this.data.nodes[f];return u?this.colorFn(u):c})}fitPositions(){Nd(this.positions,this.renderPositions,this.data.nodes.length,this.graphRadiusEstimate*6.2,this.fitWeights)}updatePositions(){if(!this.nodeGeometry||!this.linkGeometry||this.reveal)return;this.fitPositions();let t=this.nodeGeometry.getAttribute("position");this.nodeTargetPositions.set(this.renderPositions),t.needsUpdate=!0;let e=this.linkGeometry.getAttribute("position");Ah(e.array,this.renderPositions,this.data.links,this.linkK,this.linkCurvature),e.needsUpdate=!0,this.updateSelPositions(),this.updateGhostPositions()}setFocus(t){let e=this.data.nodes.length;this.focusActive=t!==null;for(let n=0;n<e;n++)this.dimTarget[n]=t?t(n):1;this.dimAnimating=!0,this.syncLinkOpacity()}setSelectedLinks(t,e){this.selTier1=t,this.selTier2=e,this.buildSelLayer()}buildSelLayer(){this.selLinkIdx=[...this.selTier1,...this.selTier2],this.selLinks=this.selLinkIdx.map(l=>this.data.links[l]),this.selSegments&&(this.scene.remove(this.selSegments),this.selGeometry?.dispose(),this.selMaterial?.dispose(),this.selSegments=null,this.selGeometry=null,this.selMaterial=null);let t=this.selLinkIdx.length;if(t===0)return;let e=this.selTier1.length,s=this.linkK*2,r=new Float32Array(t*s*3),a=new Float32Array(t*s*3),o={h:0,s:0,l:0};for(let l=0;l<t;l++){let c=this.data.links[this.selLinkIdx[l]??-1];if(!c)continue;let h=this.data.nodes[c.source],f=h?this.colorFn(h).clone():new dt("#9aa4b2");f.getHSL(o);let u=l>=e,d=this.tokens.lightMode?u?.34:.42:u?.46:.62,m=u?o.s*.9:Math.min(o.s*1.2,1);f.setHSL(o.h,m,d);let _=u?.55:1;for(let g=0;g<s;g++)a[(l*s+g)*3]=f.r*_,a[(l*s+g)*3+1]=f.g*_,a[(l*s+g)*3+2]=f.b*_}this.selGeometry=new te,this.selGeometry.setAttribute("position",new Lt(r,3)),this.selGeometry.setAttribute("color",new Lt(a,3)),this.selMaterial=new li({vertexColors:!0,transparent:!0,opacity:.85,depthWrite:!1}),this.selSegments=new rs(this.selGeometry,this.selMaterial),this.selSegments.renderOrder=2,this.selSegments.frustumCulled=!1,this.scene.add(this.selSegments),this.updateSelPositions(),this.reveal&&this.activateRevealSelectionLayer(this.reveal.target)}updateSelPositions(){if(!this.selGeometry||this.selLinks.length===0)return;let t=this.selGeometry.getAttribute("position");Ah(t.array,this.renderPositions,this.selLinks,this.linkK,this.linkCurvature),t.needsUpdate=!0}effectiveLinkOpacity(){let t=this.baseLinkOpacity*this.tokens.linkOpacityScale;return this.focusActive?t*.25:t}syncLinkOpacity(){let t=this.effectiveLinkOpacity();this.linkMaterial&&(this.linkMaterial.opacity=t),this.reveal?this.syncRevealLinkOpacity(this.revealProgressUniform.value):this.revealLinkMaterial&&(this.revealLinkMaterial.opacity=t)}applyTokens(t,e){this.tokens=t,this.scene.background=new dt(t.background),this.starfield.visible=t.starfield&&this.starfieldEnabled,this.syncSpace(),this.renderer.toneMapping=t.lightMode?xn:Di,this.nodeMaterial&&(this.nodeMaterial.uniforms.uLightMode.value=t.lightMode?1:0),this.bloomPass.enabled=t.bloomEnabled&&this.tierBloomAllowed&&e>.001,t.motes&&!this.motes&&this.buildMotes(),this.motes&&(this.motes.visible=t.motes),this.syncLinkOpacity(),this.recolor(),this.buildSelLayer()}get currentTokens(){return this.tokens}setSpace(t){this.space={...t},this.syncSpace()}syncSpace(){let t=this.tokens.space,e=t?this.space.nebula:0;e>.005&&!this.nebula&&(this.nebula=new Tl(this.graphRadiusEstimate*2.6),this.nebula.setQuality(this.tierStarScale),this.nebula.setPixelScale(this.pixelScale,1600*this.renderer.getPixelRatio()),this.nebula.bake(this.nebulaTintA,this.nebulaTintB),this.scene.add(this.nebula.object)),this.nebula?.setIntensity(e);let n=t?this.space.fieldStars:0;Math.abs(n-this.fieldStarsDensity)>.001&&(this.disposeFieldStars(),n>.005&&(this.fieldStars=Ld(this.graphRadiusEstimate*2.4,n,this.tierStarScale),this.scene.add(this.fieldStars)),this.fieldStarsDensity=n);let s=t&&this.tierCloudsAllowed?this.space.clusterClouds:0;s>.005&&!this.clouds&&(this.clouds=new El,this.clouds.setPixelScale(this.pixelScale,300*this.renderer.getPixelRatio()),this.scene.add(this.clouds.points),this.refreshClusterClouds()),this.clouds?.setIntensity(s)}setNebulaTint(t,e){t===this.nebulaTintA&&e===this.nebulaTintB||(this.nebulaTintA=t,this.nebulaTintB=e,this.nebula?.bake(t,e))}refreshClusterClouds(){if(!this.clouds||this.data.nodes.length===0)return;this.clouds.rebuild(this.data,this.reveal?.target??this.renderPositions,this.graphRadiusEstimate);let t=new dt("#7a87a8");this.clouds.recolor(e=>{let n=this.data.nodes[e];return n?this.colorFn(n):t}),this.clouds.setIntensity(this.tokens.space&&this.tierCloudsAllowed?this.space.clusterClouds:0)}disposeFieldStars(){this.fieldStars&&(this.fieldStars.geometry.dispose(),this.fieldStars.material.dispose(),this.scene.remove(this.fieldStars),this.fieldStars=null)}buildMotes(){let e=new Float32Array(1800),n=this.graphRadiusEstimate*2.2;for(let a=0;a<600;a++)e[a*3]=(Math.random()*2-1)*n,e[a*3+1]=(Math.random()*2-1)*n,e[a*3+2]=(Math.random()*2-1)*n;let s=new te;s.setAttribute("position",new Lt(e,3));let r=new ci({color:new dt("#d8d4cb"),size:1.6,sizeAttenuation:!0,transparent:!0,opacity:.5,depthWrite:!1});this.motes=new an(s,r),this.motes.renderOrder=-1,this.scene.add(this.motes)}render(t,e=t){this.starfield.rotation.y+=yl*t,this.starfield.visible&&this.twinkler.update(t,this.twinkleFreq),this.nebula?.visible&&this.nebula.update(t),this.fieldStars&&(this.fieldStars.rotation.y-=yl*.6*t),this.motes?.visible&&(this.motes.rotation.y-=yl*2*t),this.dimAnimating&&this.stepDim(t),this.reveal&&this.stepReveal(e),this.renderer.info.reset(),this.composer.render()}stepDim(t){let e=Math.min(t/Oy,1),n=!1;for(let s=0;s<this.dimCurrent.length;s++){let r=this.dimCurrent[s]??1,a=this.dimTarget[s]??1,o=r+(a-r)*e;this.dimCurrent[s]=Math.abs(o-a)<.005?a:o,this.dimCurrent[s]!==a&&(n=!0)}this.dimAnimating=n,this.nodeGeometry&&(this.nodeGeometry.getAttribute("aDim").needsUpdate=!0)}get drawCalls(){return this.renderer.info.render.calls}setBloomParams(t){this.bloomPass.strength=t.strength,this.bloomPass.radius=t.radius,this.bloomPass.threshold=t.threshold,this.bloomPass.enabled=this.tokens.bloomEnabled&&this.tierBloomAllowed&&t.strength>.001}getBloomStrength(){return this.bloomPass.enabled?this.bloomPass.strength:0}setBloomStrength(t){this.bloomPass.strength=t,this.bloomPass.enabled=this.tokens.bloomEnabled&&this.tierBloomAllowed&&t>.001}applyTier(t,e){this.tierBloomAllowed=t.bloomAllowed;let n=Ud(window.devicePixelRatio,t.pixelRatioCap);this.renderer.setPixelRatio(n),this.composer.setPixelRatio(n),this.bloomPass.enabled=this.tokens.bloomEnabled&&this.tierBloomAllowed&&e>.001;let s=this.starfield.visible,r=this.starfield.rotation.y;Ph(this.starfield),this.scene.remove(this.starfield);let a=Ih(this.graphRadiusEstimate*6.5,t.starScale);this.starfield=a.group,this.twinkler=a.twinkler,this.starfield.visible=s,this.starfield.rotation.y=r,this.scene.add(this.starfield),this.tierLinkSegs=t.linkSegments,this.linkGeometry&&Ml(this.linkCurvature,this.tierLinkSegs)!==this.linkK&&(this.buildLinkLayer(),this.recolor(),this.buildSelLayer(),this.reveal?this.activateRevealLinkLayer(this.reveal.target):this.updatePositions()),this.tierCloudsAllowed=t.clusterCloudsAllowed,this.tierStarScale!==t.starScale&&(this.tierStarScale=t.starScale,this.nebula&&(this.nebula.setQuality(t.starScale),this.nebula.bake(this.nebulaTintA,this.nebulaTintB))),this.fieldStarsDensity=-1,this.syncSpace(),this.resize(this.lastW,this.lastH);let o=this.nodeMaterial?.uniforms.uMaxPoint;o&&(o.value=110*this.renderer.getPixelRatio())}setLinkOpacity(t){this.baseLinkOpacity=t,this.syncLinkOpacity()}setNodeScale(t){this.nodeScale=t;let e=this.nodeMaterial?.uniforms.uSizeMul;e&&(e.value=t)}setStarfieldEnabled(t){this.starfieldEnabled=t,this.starfield.visible=t&&this.tokens.starfield}resize(t,e){if(t<2||e<2)return;this.lastW=t,this.lastH=e,this.camera.aspect=t/e,this.camera.updateProjectionMatrix(),this.renderer.setSize(t,e),this.composer.setSize(t,e),this.bloomPass.resolution.set(t,e);let n=e*this.renderer.getPixelRatio();this.pixelScale=n/(2*Math.tan(this.camera.fov/2*Math.PI/180));let s=this.nodeMaterial?.uniforms.uPixelScale;s&&(s.value=this.pixelScale),this.clouds?.setPixelScale(this.pixelScale,300*this.renderer.getPixelRatio()),this.nebula?.setPixelScale(this.pixelScale,1600*this.renderer.getPixelRatio())}displayPosition(t,e){let n=this.reveal,s=n?.target??this.renderPositions,r=s[t*3]??0,a=s[t*3+1]??0,o=s[t*3+2]??0;if(!n)return e.set(r,a,o);let l=md(this.revealProgressUniform.value,Math.hypot(r,a,o),n.maxR);return e.set(r*l,a*l,o*l)}projectNode(t,e,n){return this.displayPosition(t,this.projVec),this.projVec.project(this.camera),{x:(this.projVec.x+1)/2*e,y:(1-this.projVec.y)/2*n,behind:this.projVec.z>1}}pickNearest(t,e,n,s,r){let a=-1,o=r;for(let l=0;l<this.data.nodes.length;l++){let c=this.projectNode(l,n,s);if(c.behind)continue;let h=Math.hypot(c.x-t,c.y-e);h<o&&(o=h,a=l)}return a}nodeRadius(t){return this.sizes[t]??2.2}nodePosition(t,e){return this.displayPosition(t,e)}nodeColorHex(t){let e=this.data.nodes[t];return e?`#${this.colorFn(e).getHexString()}`:"#9aa4b2"}cameraDistanceTo(t){return this.displayPosition(t,this.projVec),this.camera.position.distanceTo(this.projVec)}disposeGraphObjects(){this.nodePoints&&this.scene.remove(this.nodePoints),this.linkSegments&&this.scene.remove(this.linkSegments),this.selSegments&&(this.scene.remove(this.selSegments),this.selGeometry?.dispose(),this.selMaterial?.dispose(),this.selSegments=null,this.selGeometry=null,this.selMaterial=null),this.ghostSegments&&(this.scene.remove(this.ghostSegments),this.ghostGeometry?.dispose(),this.ghostMaterial?.dispose(),this.ghostSegments=null,this.ghostGeometry=null,this.ghostMaterial=null),this.nodeGeometry?.dispose(),this.nodeMaterial?.dispose(),this.linkGeometry?.dispose(),this.linkMaterial?.dispose(),this.revealLinkMaterial?.dispose(),this.revealSelMaterial?.dispose(),this.nodePoints=null,this.linkSegments=null,this.nodeGeometry=null,this.linkGeometry=null,this.nodeMaterial=null,this.linkMaterial=null,this.revealLinkMaterial=null,this.revealSelMaterial=null}dispose(){this.disposeGraphObjects(),Ph(this.starfield),this.scene.remove(this.starfield),this.disposeFieldStars(),this.nebula&&(this.nebula.dispose(),this.scene.remove(this.nebula.object),this.nebula=null),this.clouds&&(this.clouds.dispose(),this.scene.remove(this.clouds.points),this.clouds=null),this.motes&&(this.motes.geometry.dispose(),this.motes.material.dispose(),this.scene.remove(this.motes),this.motes=null),this.bloomPass.dispose(),this.outputPass.dispose(),this.renderPass.dispose(),this.composer.dispose(),this.renderer.dispose();try{this.renderer.forceContextLoss()}catch{}this.renderer.domElement.remove()}};var Od={type:"change"},Fh={type:"start"},kd={type:"end"},Pl=new Ri,Bd=new Sn,By=Math.cos(70*$c.DEG2RAD),Ue=new P,on=2*Math.PI,ae={NONE:-1,ROTATE:0,DOLLY:1,PAN:2,TOUCH_ROTATE:3,TOUCH_PAN:4,TOUCH_DOLLY_PAN:5,TOUCH_DOLLY_ROTATE:6},Dh=1e-6,Il=class extends Rr{constructor(t,e=null){super(t,e),this.state=ae.NONE,this.target=new P,this.cursor=new P,this.minDistance=0,this.maxDistance=1/0,this.minZoom=0,this.maxZoom=1/0,this.minTargetRadius=0,this.maxTargetRadius=1/0,this.minPolarAngle=0,this.maxPolarAngle=Math.PI,this.minAzimuthAngle=-1/0,this.maxAzimuthAngle=1/0,this.enableDamping=!1,this.dampingFactor=.05,this.enableZoom=!0,this.zoomSpeed=1,this.enableRotate=!0,this.rotateSpeed=1,this.keyRotateSpeed=1,this.enablePan=!0,this.panSpeed=1,this.screenSpacePanning=!0,this.keyPanSpeed=7,this.zoomToCursor=!1,this.autoRotate=!1,this.autoRotateSpeed=2,this.keys={LEFT:"ArrowLeft",UP:"ArrowUp",RIGHT:"ArrowRight",BOTTOM:"ArrowDown"},this.mouseButtons={LEFT:Nn.ROTATE,MIDDLE:Nn.DOLLY,RIGHT:Nn.PAN},this.touches={ONE:Ni.ROTATE,TWO:Ni.DOLLY_PAN},this.target0=this.target.clone(),this.position0=this.object.position.clone(),this.zoom0=this.object.zoom,this._cursorStyle="auto",this._domElementKeyEvents=null,this._lastPosition=new P,this._lastQuaternion=new gn,this._lastTargetPosition=new P,this._quat=new gn().setFromUnitVectors(t.up,new P(0,1,0)),this._quatInverse=this._quat.clone().invert(),this._spherical=new Wn,this._sphericalDelta=new Wn,this._scale=1,this._panOffset=new P,this._rotateStart=new Et,this._rotateEnd=new Et,this._rotateDelta=new Et,this._panStart=new Et,this._panEnd=new Et,this._panDelta=new Et,this._dollyStart=new Et,this._dollyEnd=new Et,this._dollyDelta=new Et,this._dollyDirection=new P,this._mouse=new Et,this._performCursorZoom=!1,this._pointers=[],this._pointerPositions={},this._controlActive=!1,this._onPointerMove=zy.bind(this),this._onPointerDown=ky.bind(this),this._onPointerUp=Vy.bind(this),this._onContextMenu=Zy.bind(this),this._onMouseWheel=Wy.bind(this),this._onKeyDown=Xy.bind(this),this._onTouchStart=qy.bind(this),this._onTouchMove=Yy.bind(this),this._onMouseDown=Gy.bind(this),this._onMouseMove=Hy.bind(this),this._interceptControlDown=Ky.bind(this),this._interceptControlUp=Jy.bind(this),this.domElement!==null&&this.connect(this.domElement),this.update()}set cursorStyle(t){this._cursorStyle=t,t==="grab"?this.domElement.style.cursor="grab":this.domElement.style.cursor="auto"}get cursorStyle(){return this._cursorStyle}connect(t){super.connect(t),this.domElement.addEventListener("pointerdown",this._onPointerDown),this.domElement.addEventListener("pointercancel",this._onPointerUp),this.domElement.addEventListener("contextmenu",this._onContextMenu),this.domElement.addEventListener("wheel",this._onMouseWheel,{passive:!1}),this.domElement.getRootNode().addEventListener("keydown",this._interceptControlDown,{passive:!0,capture:!0}),this.domElement.style.touchAction="none"}disconnect(){this.domElement.removeEventListener("pointerdown",this._onPointerDown),this.domElement.ownerDocument.removeEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.removeEventListener("pointerup",this._onPointerUp),this.domElement.removeEventListener("pointercancel",this._onPointerUp),this.domElement.removeEventListener("wheel",this._onMouseWheel),this.domElement.removeEventListener("contextmenu",this._onContextMenu),this.stopListenToKeyEvents(),this.domElement.getRootNode().removeEventListener("keydown",this._interceptControlDown,{capture:!0}),this.domElement.style.touchAction=""}dispose(){this.disconnect()}getPolarAngle(){return this._spherical.phi}getAzimuthalAngle(){return this._spherical.theta}getDistance(){return this.object.position.distanceTo(this.target)}listenToKeyEvents(t){t.addEventListener("keydown",this._onKeyDown),this._domElementKeyEvents=t}stopListenToKeyEvents(){this._domElementKeyEvents!==null&&(this._domElementKeyEvents.removeEventListener("keydown",this._onKeyDown),this._domElementKeyEvents=null)}saveState(){this.target0.copy(this.target),this.position0.copy(this.object.position),this.zoom0=this.object.zoom}reset(){this.target.copy(this.target0),this.object.position.copy(this.position0),this.object.zoom=this.zoom0,this.object.updateProjectionMatrix(),this.dispatchEvent(Od),this.update(),this.state=ae.NONE}pan(t,e){this._pan(t,e),this.update()}dollyIn(t){this._dollyIn(t),this.update()}dollyOut(t){this._dollyOut(t),this.update()}rotateLeft(t){this._rotateLeft(t),this.update()}rotateUp(t){this._rotateUp(t),this.update()}update(t=null){let e=this.object.position;Ue.copy(e).sub(this.target),Ue.applyQuaternion(this._quat),this._spherical.setFromVector3(Ue),this.autoRotate&&this.state===ae.NONE&&this._rotateLeft(this._getAutoRotationAngle(t)),this.enableDamping?(this._spherical.theta+=this._sphericalDelta.theta*this.dampingFactor,this._spherical.phi+=this._sphericalDelta.phi*this.dampingFactor):(this._spherical.theta+=this._sphericalDelta.theta,this._spherical.phi+=this._sphericalDelta.phi);let n=this.minAzimuthAngle,s=this.maxAzimuthAngle;isFinite(n)&&isFinite(s)&&(n<-Math.PI?n+=on:n>Math.PI&&(n-=on),s<-Math.PI?s+=on:s>Math.PI&&(s-=on),n<=s?this._spherical.theta=Math.max(n,Math.min(s,this._spherical.theta)):this._spherical.theta=this._spherical.theta>(n+s)/2?Math.max(n,this._spherical.theta):Math.min(s,this._spherical.theta)),this._spherical.phi=Math.max(this.minPolarAngle,Math.min(this.maxPolarAngle,this._spherical.phi)),this._spherical.makeSafe(),this.enableDamping===!0?this.target.addScaledVector(this._panOffset,this.dampingFactor):this.target.add(this._panOffset),this.target.sub(this.cursor),this.target.clampLength(this.minTargetRadius,this.maxTargetRadius),this.target.add(this.cursor);let r=!1;if(this.zoomToCursor&&this._performCursorZoom||this.object.isOrthographicCamera)this._spherical.radius=this._clampDistance(this._spherical.radius);else{let a=this._spherical.radius;this._spherical.radius=this._clampDistance(this._spherical.radius*this._scale),r=a!=this._spherical.radius}if(Ue.setFromSpherical(this._spherical),Ue.applyQuaternion(this._quatInverse),e.copy(this.target).add(Ue),this.object.lookAt(this.target),this.enableDamping===!0?(this._sphericalDelta.theta*=1-this.dampingFactor,this._sphericalDelta.phi*=1-this.dampingFactor,this._panOffset.multiplyScalar(1-this.dampingFactor)):(this._sphericalDelta.set(0,0,0),this._panOffset.set(0,0,0)),this.zoomToCursor&&this._performCursorZoom){let a=null;if(this.object.isPerspectiveCamera){let o=Ue.length();a=this._clampDistance(o*this._scale);let l=o-a;this.object.position.addScaledVector(this._dollyDirection,l),this.object.updateMatrixWorld(),r=!!l}else if(this.object.isOrthographicCamera){let o=new P(this._mouse.x,this._mouse.y,0);o.unproject(this.object);let l=this.object.zoom;this.object.zoom=Math.max(this.minZoom,Math.min(this.maxZoom,this.object.zoom/this._scale)),this.object.updateProjectionMatrix(),r=l!==this.object.zoom;let c=new P(this._mouse.x,this._mouse.y,0);c.unproject(this.object),this.object.position.sub(c).add(o),this.object.updateMatrixWorld(),a=Ue.length()}else console.warn("WARNING: OrbitControls.js encountered an unknown camera type - zoom to cursor disabled."),this.zoomToCursor=!1;a!==null&&(this.screenSpacePanning?this.target.set(0,0,-1).transformDirection(this.object.matrix).multiplyScalar(a).add(this.object.position):(Pl.origin.copy(this.object.position),Pl.direction.set(0,0,-1).transformDirection(this.object.matrix),Math.abs(this.object.up.dot(Pl.direction))<By?this.object.lookAt(this.target):(Bd.setFromNormalAndCoplanarPoint(this.object.up,this.target),Pl.intersectPlane(Bd,this.target))))}else if(this.object.isOrthographicCamera){let a=this.object.zoom;this.object.zoom=Math.max(this.minZoom,Math.min(this.maxZoom,this.object.zoom/this._scale)),a!==this.object.zoom&&(this.object.updateProjectionMatrix(),r=!0)}return this._scale=1,this._performCursorZoom=!1,r||this._lastPosition.distanceToSquared(this.object.position)>Dh||8*(1-this._lastQuaternion.dot(this.object.quaternion))>Dh||this._lastTargetPosition.distanceToSquared(this.target)>Dh?(this.dispatchEvent(Od),this._lastPosition.copy(this.object.position),this._lastQuaternion.copy(this.object.quaternion),this._lastTargetPosition.copy(this.target),!0):!1}_getAutoRotationAngle(t){return t!==null?on/60*this.autoRotateSpeed*t:on/60/60*this.autoRotateSpeed}_getZoomScale(t){let e=Math.abs(t*.01);return Math.pow(.95,this.zoomSpeed*e)}_rotateLeft(t){this._sphericalDelta.theta-=t}_rotateUp(t){this._sphericalDelta.phi-=t}_panLeft(t,e){Ue.setFromMatrixColumn(e,0),Ue.multiplyScalar(-t),this._panOffset.add(Ue)}_panUp(t,e){this.screenSpacePanning===!0?Ue.setFromMatrixColumn(e,1):(Ue.setFromMatrixColumn(e,0),Ue.crossVectors(this.object.up,Ue)),Ue.multiplyScalar(t),this._panOffset.add(Ue)}_pan(t,e){let n=this.domElement;if(this.object.isPerspectiveCamera){let s=this.object.position;Ue.copy(s).sub(this.target);let r=Ue.length();r*=Math.tan(this.object.fov/2*Math.PI/180),this._panLeft(2*t*r/n.clientHeight,this.object.matrix),this._panUp(2*e*r/n.clientHeight,this.object.matrix)}else this.object.isOrthographicCamera?(this._panLeft(t*(this.object.right-this.object.left)/this.object.zoom/n.clientWidth,this.object.matrix),this._panUp(e*(this.object.top-this.object.bottom)/this.object.zoom/n.clientHeight,this.object.matrix)):(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - pan disabled."),this.enablePan=!1)}_dollyOut(t){this.object.isPerspectiveCamera||this.object.isOrthographicCamera?this._scale/=t:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),this.enableZoom=!1)}_dollyIn(t){this.object.isPerspectiveCamera||this.object.isOrthographicCamera?this._scale*=t:(console.warn("WARNING: OrbitControls.js encountered an unknown camera type - dolly/zoom disabled."),this.enableZoom=!1)}_updateZoomParameters(t,e){if(!this.zoomToCursor)return;this._performCursorZoom=!0;let n=this.domElement.getBoundingClientRect(),s=t-n.left,r=e-n.top,a=n.width,o=n.height;this._mouse.x=s/a*2-1,this._mouse.y=-(r/o)*2+1,this._dollyDirection.set(this._mouse.x,this._mouse.y,1).unproject(this.object).sub(this.object.position).normalize()}_clampDistance(t){return Math.max(this.minDistance,Math.min(this.maxDistance,t))}_handleMouseDownRotate(t){this._rotateStart.set(t.clientX,t.clientY)}_handleMouseDownDolly(t){this._updateZoomParameters(t.clientX,t.clientX),this._dollyStart.set(t.clientX,t.clientY)}_handleMouseDownPan(t){this._panStart.set(t.clientX,t.clientY)}_handleMouseMoveRotate(t){this._rotateEnd.set(t.clientX,t.clientY),this._rotateDelta.subVectors(this._rotateEnd,this._rotateStart).multiplyScalar(this.rotateSpeed);let e=this.domElement;this._rotateLeft(on*this._rotateDelta.x/e.clientHeight),this._rotateUp(on*this._rotateDelta.y/e.clientHeight),this._rotateStart.copy(this._rotateEnd),this.update()}_handleMouseMoveDolly(t){this._dollyEnd.set(t.clientX,t.clientY),this._dollyDelta.subVectors(this._dollyEnd,this._dollyStart),this._dollyDelta.y>0?this._dollyOut(this._getZoomScale(this._dollyDelta.y)):this._dollyDelta.y<0&&this._dollyIn(this._getZoomScale(this._dollyDelta.y)),this._dollyStart.copy(this._dollyEnd),this.update()}_handleMouseMovePan(t){this._panEnd.set(t.clientX,t.clientY),this._panDelta.subVectors(this._panEnd,this._panStart).multiplyScalar(this.panSpeed),this._pan(this._panDelta.x,this._panDelta.y),this._panStart.copy(this._panEnd),this.update()}_handleMouseWheel(t){this._updateZoomParameters(t.clientX,t.clientY),t.deltaY<0?this._dollyIn(this._getZoomScale(t.deltaY)):t.deltaY>0&&this._dollyOut(this._getZoomScale(t.deltaY)),this.update()}_handleKeyDown(t){let e=!1;switch(t.code){case this.keys.UP:t.ctrlKey||t.metaKey||t.shiftKey?this.enableRotate&&this._rotateUp(on*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(0,this.keyPanSpeed),e=!0;break;case this.keys.BOTTOM:t.ctrlKey||t.metaKey||t.shiftKey?this.enableRotate&&this._rotateUp(-on*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(0,-this.keyPanSpeed),e=!0;break;case this.keys.LEFT:t.ctrlKey||t.metaKey||t.shiftKey?this.enableRotate&&this._rotateLeft(on*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(this.keyPanSpeed,0),e=!0;break;case this.keys.RIGHT:t.ctrlKey||t.metaKey||t.shiftKey?this.enableRotate&&this._rotateLeft(-on*this.keyRotateSpeed/this.domElement.clientHeight):this.enablePan&&this._pan(-this.keyPanSpeed,0),e=!0;break}e&&(t.preventDefault(),this.update())}_handleTouchStartRotate(t){if(this._pointers.length===1)this._rotateStart.set(t.pageX,t.pageY);else{let e=this._getSecondPointerPosition(t),n=.5*(t.pageX+e.x),s=.5*(t.pageY+e.y);this._rotateStart.set(n,s)}}_handleTouchStartPan(t){if(this._pointers.length===1)this._panStart.set(t.pageX,t.pageY);else{let e=this._getSecondPointerPosition(t),n=.5*(t.pageX+e.x),s=.5*(t.pageY+e.y);this._panStart.set(n,s)}}_handleTouchStartDolly(t){let e=this._getSecondPointerPosition(t),n=t.pageX-e.x,s=t.pageY-e.y,r=Math.sqrt(n*n+s*s);this._dollyStart.set(0,r)}_handleTouchStartDollyPan(t){this.enableZoom&&this._handleTouchStartDolly(t),this.enablePan&&this._handleTouchStartPan(t)}_handleTouchStartDollyRotate(t){this.enableZoom&&this._handleTouchStartDolly(t),this.enableRotate&&this._handleTouchStartRotate(t)}_handleTouchMoveRotate(t){if(this._pointers.length==1)this._rotateEnd.set(t.pageX,t.pageY);else{let n=this._getSecondPointerPosition(t),s=.5*(t.pageX+n.x),r=.5*(t.pageY+n.y);this._rotateEnd.set(s,r)}this._rotateDelta.subVectors(this._rotateEnd,this._rotateStart).multiplyScalar(this.rotateSpeed);let e=this.domElement;this._rotateLeft(on*this._rotateDelta.x/e.clientHeight),this._rotateUp(on*this._rotateDelta.y/e.clientHeight),this._rotateStart.copy(this._rotateEnd)}_handleTouchMovePan(t){if(this._pointers.length===1)this._panEnd.set(t.pageX,t.pageY);else{let e=this._getSecondPointerPosition(t),n=.5*(t.pageX+e.x),s=.5*(t.pageY+e.y);this._panEnd.set(n,s)}this._panDelta.subVectors(this._panEnd,this._panStart).multiplyScalar(this.panSpeed),this._pan(this._panDelta.x,this._panDelta.y),this._panStart.copy(this._panEnd)}_handleTouchMoveDolly(t){let e=this._getSecondPointerPosition(t),n=t.pageX-e.x,s=t.pageY-e.y,r=Math.sqrt(n*n+s*s);this._dollyEnd.set(0,r),this._dollyDelta.set(0,Math.pow(this._dollyEnd.y/this._dollyStart.y,this.zoomSpeed)),this._dollyOut(this._dollyDelta.y),this._dollyStart.copy(this._dollyEnd);let a=(t.pageX+e.x)*.5,o=(t.pageY+e.y)*.5;this._updateZoomParameters(a,o)}_handleTouchMoveDollyPan(t){this.enableZoom&&this._handleTouchMoveDolly(t),this.enablePan&&this._handleTouchMovePan(t)}_handleTouchMoveDollyRotate(t){this.enableZoom&&this._handleTouchMoveDolly(t),this.enableRotate&&this._handleTouchMoveRotate(t)}_addPointer(t){this._pointers.push(t.pointerId)}_removePointer(t){delete this._pointerPositions[t.pointerId];for(let e=0;e<this._pointers.length;e++)if(this._pointers[e]==t.pointerId){this._pointers.splice(e,1);return}}_isTrackingPointer(t){for(let e=0;e<this._pointers.length;e++)if(this._pointers[e]==t.pointerId)return!0;return!1}_trackPointer(t){let e=this._pointerPositions[t.pointerId];e===void 0&&(e=new Et,this._pointerPositions[t.pointerId]=e),e.set(t.pageX,t.pageY)}_getSecondPointerPosition(t){let e=t.pointerId===this._pointers[0]?this._pointers[1]:this._pointers[0];return this._pointerPositions[e]}_customWheelEvent(t){let e=t.deltaMode,n={clientX:t.clientX,clientY:t.clientY,deltaY:t.deltaY};switch(e){case 1:n.deltaY*=16;break;case 2:n.deltaY*=100;break}return t.ctrlKey&&!this._controlActive&&(n.deltaY*=10),n}};function ky(i){this.enabled!==!1&&(this._pointers.length===0&&(this.domElement.setPointerCapture(i.pointerId),this.domElement.ownerDocument.addEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.addEventListener("pointerup",this._onPointerUp)),!this._isTrackingPointer(i)&&(this._addPointer(i),i.pointerType==="touch"?this._onTouchStart(i):this._onMouseDown(i),this._cursorStyle==="grab"&&(this.domElement.style.cursor="grabbing")))}function zy(i){this.enabled!==!1&&(i.pointerType==="touch"?this._onTouchMove(i):this._onMouseMove(i))}function Vy(i){switch(this._removePointer(i),this._pointers.length){case 0:this.domElement.releasePointerCapture(i.pointerId),this.domElement.ownerDocument.removeEventListener("pointermove",this._onPointerMove),this.domElement.ownerDocument.removeEventListener("pointerup",this._onPointerUp),this.dispatchEvent(kd),this.state=ae.NONE,this._cursorStyle==="grab"&&(this.domElement.style.cursor="grab");break;case 1:let t=this._pointers[0],e=this._pointerPositions[t];this._onTouchStart({pointerId:t,pageX:e.x,pageY:e.y});break}}function Gy(i){let t;switch(i.button){case 0:t=this.mouseButtons.LEFT;break;case 1:t=this.mouseButtons.MIDDLE;break;case 2:t=this.mouseButtons.RIGHT;break;default:t=-1}switch(t){case Nn.DOLLY:if(this.enableZoom===!1)return;this._handleMouseDownDolly(i),this.state=ae.DOLLY;break;case Nn.ROTATE:if(i.ctrlKey||i.metaKey||i.shiftKey){if(this.enablePan===!1)return;this._handleMouseDownPan(i),this.state=ae.PAN}else{if(this.enableRotate===!1)return;this._handleMouseDownRotate(i),this.state=ae.ROTATE}break;case Nn.PAN:if(i.ctrlKey||i.metaKey||i.shiftKey){if(this.enableRotate===!1)return;this._handleMouseDownRotate(i),this.state=ae.ROTATE}else{if(this.enablePan===!1)return;this._handleMouseDownPan(i),this.state=ae.PAN}break;default:this.state=ae.NONE}this.state!==ae.NONE&&this.dispatchEvent(Fh)}function Hy(i){switch(this.state){case ae.ROTATE:if(this.enableRotate===!1)return;this._handleMouseMoveRotate(i);break;case ae.DOLLY:if(this.enableZoom===!1)return;this._handleMouseMoveDolly(i);break;case ae.PAN:if(this.enablePan===!1)return;this._handleMouseMovePan(i);break}}function Wy(i){this.enabled===!1||this.enableZoom===!1||this.state!==ae.NONE||(i.preventDefault(),this.dispatchEvent(Fh),this._handleMouseWheel(this._customWheelEvent(i)),this.dispatchEvent(kd))}function Xy(i){this.enabled!==!1&&this._handleKeyDown(i)}function qy(i){switch(this._trackPointer(i),this._pointers.length){case 1:switch(this.touches.ONE){case Ni.ROTATE:if(this.enableRotate===!1)return;this._handleTouchStartRotate(i),this.state=ae.TOUCH_ROTATE;break;case Ni.PAN:if(this.enablePan===!1)return;this._handleTouchStartPan(i),this.state=ae.TOUCH_PAN;break;default:this.state=ae.NONE}break;case 2:switch(this.touches.TWO){case Ni.DOLLY_PAN:if(this.enableZoom===!1&&this.enablePan===!1)return;this._handleTouchStartDollyPan(i),this.state=ae.TOUCH_DOLLY_PAN;break;case Ni.DOLLY_ROTATE:if(this.enableZoom===!1&&this.enableRotate===!1)return;this._handleTouchStartDollyRotate(i),this.state=ae.TOUCH_DOLLY_ROTATE;break;default:this.state=ae.NONE}break;default:this.state=ae.NONE}this.state!==ae.NONE&&this.dispatchEvent(Fh)}function Yy(i){switch(this._trackPointer(i),this.state){case ae.TOUCH_ROTATE:if(this.enableRotate===!1)return;this._handleTouchMoveRotate(i),this.update();break;case ae.TOUCH_PAN:if(this.enablePan===!1)return;this._handleTouchMovePan(i),this.update();break;case ae.TOUCH_DOLLY_PAN:if(this.enableZoom===!1&&this.enablePan===!1)return;this._handleTouchMoveDollyPan(i),this.update();break;case ae.TOUCH_DOLLY_ROTATE:if(this.enableZoom===!1&&this.enableRotate===!1)return;this._handleTouchMoveDollyRotate(i),this.update();break;default:this.state=ae.NONE}}function Zy(i){this.enabled!==!1&&i.preventDefault()}function Ky(i){i.key==="Control"&&(this._controlActive=!0,this.domElement.getRootNode().addEventListener("keyup",this._interceptControlUp,{passive:!0,capture:!0}))}function Jy(i){i.key==="Control"&&(this._controlActive=!1,this.domElement.getRootNode().removeEventListener("keyup",this._interceptControlUp,{passive:!0,capture:!0}))}function Uh(i,t){if(t===null)return 0;let e=(i-t)/1e3;return Number.isFinite(e)?Math.max(e,0):0}function zd(i,t,e=.1){return Math.min(Uh(i,t),e)}function Oh(i){return Number.isFinite(i)?Math.max(i,0):0}function Bh(i,t){return Number.isFinite(i)?!Number.isFinite(t)||t<=0?1:Math.min(Math.max(i/t,0),1):i>0?1:0}function Vd(i){return i<.5?4*i*i*i:1-Math.pow(-2*i+2,3)/2}var Gd=new P(0,1,0),Hd=.6,$y=1.5,jy=4,Qy=new Set(["w","a","s","d","q","e"]),Ll=class{constructor(t,e,n){this.camera=t;this.dom=e;this.hooks=n;q(this,"cruiseEnabled",!0);q(this,"cruiseSpeed",1);q(this,"tourActive",!1);q(this,"framingElevDeg",18);q(this,"controls");q(this,"tween",null);q(this,"path",null);q(this,"pathPos",new P);q(this,"pathTan",new P);q(this,"pathTan2",new P);q(this,"pathRight",new P);q(this,"pathUp",new P);q(this,"idleMs",0);q(this,"cruiseAnchor",null);q(this,"cruiseT",0);q(this,"cruiseDir",1);q(this,"pendingDensityDir",null);q(this,"pressed",new Set);q(this,"shiftHeld",!1);q(this,"tmpOffset",new P);q(this,"tmpSph",new Wn);q(this,"tmpDir",new P);q(this,"tmpRight",new P);q(this,"disposeFns",[]);this.controls=new Il(t,e),this.controls.enableDamping=!0,this.controls.dampingFactor=.08,e.tabIndex=0,this.bindPointer(),this.bindKeys()}get target(){return this.controls.target}markInput(){this.idleMs=0,this.cruiseAnchor=null,this.tween=null,this.path=null}get onPath(){return this.path!==null}flyPath(t,e,n={}){let s=[];for(let a of t){if(!Number.isFinite(a.x)||!Number.isFinite(a.y)||!Number.isFinite(a.z))continue;let o=s[s.length-1];o&&o.distanceToSquared(a)<1e-4||s.push(a.clone())}if(s.length<2)return;let r=new Sr(s,!1,"catmullrom",.5);this.path={elapsedMs:0,durMs:Math.max(1,e),curve:r,lookMode:n.lookMode??"tangent",fixedTarget:(n.target??new P).clone(),lookAhead:n.lookAhead??60,bank:n.bank??0},n.onDone&&(this.path.onDone=n.onDone),this.tween=null,this.cruiseAnchor=null}cancelMotion(){this.path=null,this.tween=null,this.camera.up.set(0,1,0)}bindPointer(){let t=0,e=0,n=!1,s=l=>{this.dom.focus(),this.controls.mouseButtons.LEFT=l.metaKey||l.shiftKey||l.ctrlKey?Nn.PAN:Nn.ROTATE,t=l.clientX,e=l.clientY,n=!1},r=l=>{n||l.buttons===0||Math.hypot(l.clientX-t,l.clientY-e)>jy&&(n=!0,this.markInput())},a=()=>this.markInput(),o=()=>this.markInput();this.dom.addEventListener("pointerdown",s,{capture:!0}),this.dom.addEventListener("pointermove",r),this.dom.addEventListener("wheel",a,{passive:!0}),this.dom.addEventListener("touchmove",o,{passive:!0}),this.disposeFns.push(()=>{this.dom.removeEventListener("pointerdown",s,{capture:!0}),this.dom.removeEventListener("pointermove",r),this.dom.removeEventListener("wheel",a),this.dom.removeEventListener("touchmove",o)})}bindKeys(){let t=s=>{let r=s.key.toLowerCase();this.shiftHeld=s.shiftKey,Qy.has(r)?(this.pressed.add(r),this.markInput(),s.preventDefault(),s.stopPropagation()):r==="f"?(this.hooks.onFlyToSelected(),s.preventDefault()):r==="r"&&(this.hooks.onResetView(),s.preventDefault())},e=s=>{this.shiftHeld=s.shiftKey,this.pressed.delete(s.key.toLowerCase())},n=()=>this.pressed.clear();this.dom.addEventListener("keydown",t),this.dom.addEventListener("keyup",e),this.dom.addEventListener("blur",n),this.disposeFns.push(()=>{this.dom.removeEventListener("keydown",t),this.dom.removeEventListener("keyup",e),this.dom.removeEventListener("blur",n)})}applyFly(t){if(this.pressed.size===0)return!1;let e=this.camera.position.distanceTo(this.controls.target),n=Math.min(Math.max(e*.8,10),600)*(this.shiftHeld?3:1),s=this.camera.getWorldDirection(this.tmpDir);this.tmpRight.crossVectors(s,this.camera.up).normalize();let r=new P;return this.pressed.has("w")&&r.add(s),this.pressed.has("s")&&r.sub(s),this.pressed.has("d")&&r.add(this.tmpRight),this.pressed.has("a")&&r.sub(this.tmpRight),this.pressed.has("e")&&(r.y+=1),this.pressed.has("q")&&(r.y-=1),r.lengthSq()<1e-8?!1:(r.normalize().multiplyScalar(n*t),this.camera.position.add(r),this.controls.target.add(r),this.idleMs=0,!0)}setInitialFraming(t,e){this.camera.position.copy(this.framingPosition(t,e)),this.controls.target.copy(t),this.controls.update()}setFramingElev(t){this.framingElevDeg=t}framingPosition(t,e){let n=this.camera.fov*Math.PI/180,s=Math.max(e,1)/Math.sin(n/2)*$y,r=this.framingElevDeg*Math.PI/180;return new P(Math.cos(r),Math.sin(r),.35).normalize().multiplyScalar(s).add(t)}resetView(t,e,n){this.startTween(this.framingPosition(t,e),t.clone(),1200,n)}beginFocusOrbit(t){this.pendingDensityDir=t,this.cruiseAnchor=null,this.idleMs=Zn.resumeDelayMs+1}flyTo(t,e,n){let s=Math.min(Math.max(e*di.distancePerRadius,di.minDistance),di.maxDistance),r=this.camera.position.clone().sub(t);r.lengthSq()<1e-6&&r.set(0,0,1),this.tmpSph.setFromVector3(r),this.tmpSph.theta+=di.azimuthOffsetRad,this.tmpSph.radius=s;let a=t.clone().add(new P().setFromSpherical(this.tmpSph)),o=this.camera.position.distanceTo(a),l=Math.min(Math.max(di.minMs+di.msPerWorldUnit*o,di.minMs),di.maxMs);this.startTween(a,t.clone(),l,n)}startTween(t,e,n,s){this.tween={elapsedMs:0,durMs:n,fromPos:this.camera.position.clone(),toPos:t,fromTarget:this.controls.target.clone(),toTarget:e},s&&(this.tween.onDone=s)}update(t,e,n=e){let s=Oh(e),r=Oh(n),a=s*1e3;if(this.path){let l=this.path;l.elapsedMs+=a;let c=Bh(l.elapsedMs,l.durMs),h=Vd(c);try{l.curve.getPointAt(h,this.pathPos)}catch{return this.camera.up.set(0,1,0),this.path=null,l.onDone?.(),this.idleMs=0,!1}if(!Number.isFinite(this.pathPos.x)||!Number.isFinite(this.pathPos.y)||!Number.isFinite(this.pathPos.z))return this.camera.up.set(0,1,0),this.path=null,l.onDone?.(),this.idleMs=0,!1;if(this.camera.position.copy(this.pathPos),l.lookMode==="tangent")if(l.curve.getTangentAt(h,this.pathTan),this.controls.target.copy(this.pathPos).addScaledVector(this.pathTan,l.lookAhead),l.bank>0&&c<.999){l.curve.getTangentAt(Math.min(h+.02,1),this.pathTan2),this.pathRight.crossVectors(this.pathTan,Gd).normalize();let f=this.pathTan2.dot(this.pathRight),u=Math.max(Math.min(-f*l.bank*6,Hd),-Hd);this.pathUp.copy(this.pathTan).normalize(),this.camera.up.copy(Gd).applyAxisAngle(this.pathUp,u).normalize()}else this.camera.up.set(0,1,0);else this.controls.target.copy(l.fixedTarget),this.camera.up.set(0,1,0);return this.controls.update(),c>=1&&(this.camera.up.set(0,1,0),this.path=null,l.onDone?.(),this.idleMs=0),!1}if(this.tween){let l=this.tween;l.elapsedMs+=a;let c=Bh(l.elapsedMs,l.durMs),h=Vd(c);return this.camera.position.lerpVectors(l.fromPos,l.toPos,h),this.controls.target.lerpVectors(l.fromTarget,l.toTarget,h),this.controls.update(),c>=1&&(this.tween=null,l.onDone?.(),this.idleMs=0),!1}let o=this.applyFly(r);if(o||(this.idleMs+=a),!o&&(this.cruiseEnabled||this.tourActive)&&this.idleMs>Zn.resumeDelayMs){let l=Math.min(Math.max((this.idleMs-Zn.resumeDelayMs)/Zn.rampUpMs,0),1);if(!this.cruiseAnchor){if(this.cruiseAnchor=new Wn().setFromVector3(this.tmpOffset.copy(this.camera.position).sub(this.controls.target)),this.cruiseT=0,this.cruiseDir=1,this.pendingDensityDir&&this.pendingDensityDir.lengthSq()>1e-6){let m=new Wn().setFromVector3(this.pendingDensityDir).theta-this.cruiseAnchor.theta;for(;m>Math.PI;)m-=2*Math.PI;for(;m<-Math.PI;)m+=2*Math.PI;this.cruiseDir=m>=0?1:-1}this.pendingDensityDir=null}this.cruiseT+=s*l;let c=this.cruiseT,h=this.cruiseAnchor,f=Zn.elevationDeg*Math.PI/180*Math.sin(2*Math.PI*c/Zn.elevationPeriodS),u=1+Zn.radiusBreath*Math.sin(2*Math.PI*c/Zn.radiusPeriodS);return this.tmpSph.radius=h.radius*u,this.tmpSph.theta=h.theta+this.cruiseDir*Zn.angularSpeed*this.cruiseSpeed*c,this.tmpSph.phi=Math.min(Math.max(h.phi+f,.05),Math.PI-.05),this.camera.position.setFromSpherical(this.tmpSph).add(this.controls.target),this.camera.lookAt(this.controls.target),!0}return this.controls.update(),!1}dispose(){this.tween=null,this.pressed.clear();for(let t of this.disposeFns)t();this.disposeFns=[],this.controls.dispose()}};var Wd=`(()=>{function zt(t){let e=+this._x.call(null,t);return Mt(this.cover(e),e,t)}function Mt(t,e,r){if(isNaN(e))return t;var n,i=t._root,o={data:r},f=t._x0,a=t._x1,s,l,h,c,x;if(!i)return t._root=o,t;for(;i.length;)if((h=e>=(s=(f+a)/2))?f=s:a=s,n=i,!(i=i[c=+h]))return n[c]=o,t;if(l=+t._x.call(null,i.data),e===l)return o.next=i,n?n[c]=o:t._root=o,t;do n=n?n[c]=new Array(2):t._root=new Array(2),(h=e>=(s=(f+a)/2))?f=s:a=s;while((c=+h)==(x=+(l>=s)));return n[x]=i,n[c]=o,t}function bt(t){Array.isArray(t)||(t=Array.from(t));let e=t.length,r=new Float64Array(e),n=1/0,i=-1/0;for(let o=0,f;o<e;++o)isNaN(f=+this._x.call(null,t[o]))||(r[o]=f,f<n&&(n=f),f>i&&(i=f));if(n>i)return this;this.cover(n).cover(i);for(let o=0;o<e;++o)Mt(this,r[o],t[o]);return this}function kt(t){if(isNaN(t=+t))return this;var e=this._x0,r=this._x1;if(isNaN(e))r=(e=Math.floor(t))+1;else{for(var n=r-e||1,i=this._root,o,f;e>t||t>=r;)switch(f=+(t<e),o=new Array(2),o[f]=i,i=o,n*=2,f){case 0:r=e+n;break;case 1:e=r-n;break}this._root&&this._root.length&&(this._root=i)}return this._x0=e,this._x1=r,this}function It(){var t=[];return this.visit(function(e){if(!e.length)do t.push(e.data);while(e=e.next)}),t}function qt(t){return arguments.length?this.cover(+t[0][0]).cover(+t[1][0]):isNaN(this._x0)?void 0:[[this._x0],[this._x1]]}function E(t,e,r){this.node=t,this.x0=e,this.x1=r}function St(t,e){var r,n=this._x0,i,o,f=this._x1,a=[],s=this._root,l,h;for(s&&a.push(new E(s,n,f)),e==null?e=1/0:(n=t-e,f=t+e);l=a.pop();)if(!(!(s=l.node)||(i=l.x0)>f||(o=l.x1)<n))if(s.length){var c=(i+o)/2;a.push(new E(s[1],c,o),new E(s[0],i,c)),(h=+(t>=c))&&(l=a[a.length-1],a[a.length-1]=a[a.length-1-h],a[a.length-1-h]=l)}else{var x=Math.abs(t-+this._x.call(null,s.data));x<e&&(e=x,n=t-x,f=t+x,r=s.data)}return r}function Ft(t){if(isNaN(s=+this._x.call(null,t)))return this;var e,r=this._root,n,i,o,f=this._x0,a=this._x1,s,l,h,c,x;if(!r)return this;if(r.length)for(;;){if((h=s>=(l=(f+a)/2))?f=l:a=l,e=r,!(r=r[c=+h]))return this;if(!r.length)break;e[c+1&1]&&(n=e,x=c)}for(;r.data!==t;)if(i=r,!(r=r.next))return this;return(o=r.next)&&delete r.next,i?(o?i.next=o:delete i.next,this):e?(o?e[c]=o:delete e[c],(r=e[0]||e[1])&&r===(e[1]||e[0])&&!r.length&&(n?n[x]=r:this._root=r),this):(this._root=o,this)}function Pt(t){for(var e=0,r=t.length;e<r;++e)this.remove(t[e]);return this}function Wt(){return this._root}function Dt(){var t=0;return this.visit(function(e){if(!e.length)do++t;while(e=e.next)}),t}function Rt(t){var e=[],r,n=this._root,i,o,f;for(n&&e.push(new E(n,this._x0,this._x1));r=e.pop();)if(!t(n=r.node,o=r.x0,f=r.x1)&&n.length){var a=(o+f)/2;(i=n[1])&&e.push(new E(i,a,f)),(i=n[0])&&e.push(new E(i,o,a))}return this}function Et(t){var e=[],r=[],n;for(this._root&&e.push(new E(this._root,this._x0,this._x1));n=e.pop();){var i=n.node;if(i.length){var o,f=n.x0,a=n.x1,s=(f+a)/2;(o=i[0])&&e.push(new E(o,f,s)),(o=i[1])&&e.push(new E(o,s,a))}r.push(n)}for(;n=r.pop();)t(n.node,n.x0,n.x1);return this}function Bt(t){return t[0]}function Lt(t){return arguments.length?(this._x=t,this):this._x}function O(t,e){var r=new it(e??Bt,NaN,NaN);return t==null?r:r.addAll(t)}function it(t,e,r){this._x=t,this._x0=e,this._x1=r,this._root=void 0}function jt(t){for(var e={data:t.data},r=e;t=t.next;)r=r.next={data:t.data};return e}var W=O.prototype=it.prototype;W.copy=function(){var t=new it(this._x,this._x0,this._x1),e=this._root,r,n;if(!e)return t;if(!e.length)return t._root=jt(e),t;for(r=[{source:e,target:t._root=new Array(2)}];e=r.pop();)for(var i=0;i<2;++i)(n=e.source[i])&&(n.length?r.push({source:n,target:e.target[i]=new Array(2)}):e.target[i]=jt(n));return t};W.add=zt;W.addAll=bt;W.cover=kt;W.data=It;W.extent=qt;W.find=St;W.remove=Ft;W.removeAll=Pt;W.root=Wt;W.size=Dt;W.visit=Rt;W.visitAfter=Et;W.x=Lt;function Tt(t){let e=+this._x.call(null,t),r=+this._y.call(null,t);return Ot(this.cover(e,r),e,r,t)}function Ot(t,e,r,n){if(isNaN(e)||isNaN(r))return t;var i,o=t._root,f={data:n},a=t._x0,s=t._y0,l=t._x1,h=t._y1,c,x,v,p,w,y,u,g;if(!o)return t._root=f,t;for(;o.length;)if((w=e>=(c=(a+l)/2))?a=c:l=c,(y=r>=(x=(s+h)/2))?s=x:h=x,i=o,!(o=o[u=y<<1|w]))return i[u]=f,t;if(v=+t._x.call(null,o.data),p=+t._y.call(null,o.data),e===v&&r===p)return f.next=o,i?i[u]=f:t._root=f,t;do i=i?i[u]=new Array(4):t._root=new Array(4),(w=e>=(c=(a+l)/2))?a=c:l=c,(y=r>=(x=(s+h)/2))?s=x:h=x;while((u=y<<1|w)===(g=(p>=x)<<1|v>=c));return i[g]=o,i[u]=f,t}function Ct(t){var e,r,n=t.length,i,o,f=new Array(n),a=new Array(n),s=1/0,l=1/0,h=-1/0,c=-1/0;for(r=0;r<n;++r)isNaN(i=+this._x.call(null,e=t[r]))||isNaN(o=+this._y.call(null,e))||(f[r]=i,a[r]=o,i<s&&(s=i),i>h&&(h=i),o<l&&(l=o),o>c&&(c=o));if(s>h||l>c)return this;for(this.cover(s,l).cover(h,c),r=0;r<n;++r)Ot(this,f[r],a[r],t[r]);return this}function Xt(t,e){if(isNaN(t=+t)||isNaN(e=+e))return this;var r=this._x0,n=this._y0,i=this._x1,o=this._y1;if(isNaN(r))i=(r=Math.floor(t))+1,o=(n=Math.floor(e))+1;else{for(var f=i-r||1,a=this._root,s,l;r>t||t>=i||n>e||e>=o;)switch(l=(e<n)<<1|t<r,s=new Array(4),s[l]=a,a=s,f*=2,l){case 0:i=r+f,o=n+f;break;case 1:r=i-f,o=n+f;break;case 2:i=r+f,n=o-f;break;case 3:r=i-f,n=o-f;break}this._root&&this._root.length&&(this._root=a)}return this._x0=r,this._y0=n,this._x1=i,this._y1=o,this}function Yt(){var t=[];return this.visit(function(e){if(!e.length)do t.push(e.data);while(e=e.next)}),t}function Ht(t){return arguments.length?this.cover(+t[0][0],+t[0][1]).cover(+t[1][0],+t[1][1]):isNaN(this._x0)?void 0:[[this._x0,this._y0],[this._x1,this._y1]]}function q(t,e,r,n,i){this.node=t,this.x0=e,this.y0=r,this.x1=n,this.y1=i}function Qt(t,e,r){var n,i=this._x0,o=this._y0,f,a,s,l,h=this._x1,c=this._y1,x=[],v=this._root,p,w;for(v&&x.push(new q(v,i,o,h,c)),r==null?r=1/0:(i=t-r,o=e-r,h=t+r,c=e+r,r*=r);p=x.pop();)if(!(!(v=p.node)||(f=p.x0)>h||(a=p.y0)>c||(s=p.x1)<i||(l=p.y1)<o))if(v.length){var y=(f+s)/2,u=(a+l)/2;x.push(new q(v[3],y,u,s,l),new q(v[2],f,u,y,l),new q(v[1],y,a,s,u),new q(v[0],f,a,y,u)),(w=(e>=u)<<1|t>=y)&&(p=x[x.length-1],x[x.length-1]=x[x.length-1-w],x[x.length-1-w]=p)}else{var g=t-+this._x.call(null,v.data),m=e-+this._y.call(null,v.data),d=g*g+m*m;if(d<r){var _=Math.sqrt(r=d);i=t-_,o=e-_,h=t+_,c=e+_,n=v.data}}return n}function Zt(t){if(isNaN(h=+this._x.call(null,t))||isNaN(c=+this._y.call(null,t)))return this;var e,r=this._root,n,i,o,f=this._x0,a=this._y0,s=this._x1,l=this._y1,h,c,x,v,p,w,y,u;if(!r)return this;if(r.length)for(;;){if((p=h>=(x=(f+s)/2))?f=x:s=x,(w=c>=(v=(a+l)/2))?a=v:l=v,e=r,!(r=r[y=w<<1|p]))return this;if(!r.length)break;(e[y+1&3]||e[y+2&3]||e[y+3&3])&&(n=e,u=y)}for(;r.data!==t;)if(i=r,!(r=r.next))return this;return(o=r.next)&&delete r.next,i?(o?i.next=o:delete i.next,this):e?(o?e[y]=o:delete e[y],(r=e[0]||e[1]||e[2]||e[3])&&r===(e[3]||e[2]||e[1]||e[0])&&!r.length&&(n?n[u]=r:this._root=r),this):(this._root=o,this)}function Gt(t){for(var e=0,r=t.length;e<r;++e)this.remove(t[e]);return this}function Ut(){return this._root}function Jt(){var t=0;return this.visit(function(e){if(!e.length)do++t;while(e=e.next)}),t}function Kt(t){var e=[],r,n=this._root,i,o,f,a,s;for(n&&e.push(new q(n,this._x0,this._y0,this._x1,this._y1));r=e.pop();)if(!t(n=r.node,o=r.x0,f=r.y0,a=r.x1,s=r.y1)&&n.length){var l=(o+a)/2,h=(f+s)/2;(i=n[3])&&e.push(new q(i,l,h,a,s)),(i=n[2])&&e.push(new q(i,o,h,l,s)),(i=n[1])&&e.push(new q(i,l,f,a,h)),(i=n[0])&&e.push(new q(i,o,f,l,h))}return this}function Vt(t){var e=[],r=[],n;for(this._root&&e.push(new q(this._root,this._x0,this._y0,this._x1,this._y1));n=e.pop();){var i=n.node;if(i.length){var o,f=n.x0,a=n.y0,s=n.x1,l=n.y1,h=(f+s)/2,c=(a+l)/2;(o=i[0])&&e.push(new q(o,f,a,h,c)),(o=i[1])&&e.push(new q(o,h,a,s,c)),(o=i[2])&&e.push(new q(o,f,c,h,l)),(o=i[3])&&e.push(new q(o,h,c,s,l))}r.push(n)}for(;n=r.pop();)t(n.node,n.x0,n.y0,n.x1,n.y1);return this}function $t(t){return t[0]}function te(t){return arguments.length?(this._x=t,this):this._x}function ee(t){return t[1]}function re(t){return arguments.length?(this._y=t,this):this._y}function C(t,e,r){var n=new ot(e??$t,r??ee,NaN,NaN,NaN,NaN);return t==null?n:n.addAll(t)}function ot(t,e,r,n,i,o){this._x=t,this._y=e,this._x0=r,this._y0=n,this._x1=i,this._y1=o,this._root=void 0}function ne(t){for(var e={data:t.data},r=e;t=t.next;)r=r.next={data:t.data};return e}var F=C.prototype=ot.prototype;F.copy=function(){var t=new ot(this._x,this._y,this._x0,this._y0,this._x1,this._y1),e=this._root,r,n;if(!e)return t;if(!e.length)return t._root=ne(e),t;for(r=[{source:e,target:t._root=new Array(4)}];e=r.pop();)for(var i=0;i<4;++i)(n=e.source[i])&&(n.length?r.push({source:n,target:e.target[i]=new Array(4)}):e.target[i]=ne(n));return t};F.add=Tt;F.addAll=Ct;F.cover=Xt;F.data=Yt;F.extent=Ht;F.find=Qt;F.remove=Zt;F.removeAll=Gt;F.root=Ut;F.size=Jt;F.visit=Kt;F.visitAfter=Vt;F.x=te;F.y=re;function ie(t){let e=+this._x.call(null,t),r=+this._y.call(null,t),n=+this._z.call(null,t);return oe(this.cover(e,r,n),e,r,n,t)}function oe(t,e,r,n,i){if(isNaN(e)||isNaN(r)||isNaN(n))return t;var o,f=t._root,a={data:i},s=t._x0,l=t._y0,h=t._z0,c=t._x1,x=t._y1,v=t._z1,p,w,y,u,g,m,d,_,N,A,z;if(!f)return t._root=a,t;for(;f.length;)if((d=e>=(p=(s+c)/2))?s=p:c=p,(_=r>=(w=(l+x)/2))?l=w:x=w,(N=n>=(y=(h+v)/2))?h=y:v=y,o=f,!(f=f[A=N<<2|_<<1|d]))return o[A]=a,t;if(u=+t._x.call(null,f.data),g=+t._y.call(null,f.data),m=+t._z.call(null,f.data),e===u&&r===g&&n===m)return a.next=f,o?o[A]=a:t._root=a,t;do o=o?o[A]=new Array(8):t._root=new Array(8),(d=e>=(p=(s+c)/2))?s=p:c=p,(_=r>=(w=(l+x)/2))?l=w:x=w,(N=n>=(y=(h+v)/2))?h=y:v=y;while((A=N<<2|_<<1|d)===(z=(m>=y)<<2|(g>=w)<<1|u>=p));return o[z]=f,o[A]=a,t}function ae(t){Array.isArray(t)||(t=Array.from(t));let e=t.length,r=new Float64Array(e),n=new Float64Array(e),i=new Float64Array(e),o=1/0,f=1/0,a=1/0,s=-1/0,l=-1/0,h=-1/0;for(let c=0,x,v,p,w;c<e;++c)isNaN(v=+this._x.call(null,x=t[c]))||isNaN(p=+this._y.call(null,x))||isNaN(w=+this._z.call(null,x))||(r[c]=v,n[c]=p,i[c]=w,v<o&&(o=v),v>s&&(s=v),p<f&&(f=p),p>l&&(l=p),w<a&&(a=w),w>h&&(h=w));if(o>s||f>l||a>h)return this;this.cover(o,f,a).cover(s,l,h);for(let c=0;c<e;++c)oe(this,r[c],n[c],i[c],t[c]);return this}function fe(t,e,r){if(isNaN(t=+t)||isNaN(e=+e)||isNaN(r=+r))return this;var n=this._x0,i=this._y0,o=this._z0,f=this._x1,a=this._y1,s=this._z1;if(isNaN(n))f=(n=Math.floor(t))+1,a=(i=Math.floor(e))+1,s=(o=Math.floor(r))+1;else{for(var l=f-n||1,h=this._root,c,x;n>t||t>=f||i>e||e>=a||o>r||r>=s;)switch(x=(r<o)<<2|(e<i)<<1|t<n,c=new Array(8),c[x]=h,h=c,l*=2,x){case 0:f=n+l,a=i+l,s=o+l;break;case 1:n=f-l,a=i+l,s=o+l;break;case 2:f=n+l,i=a-l,s=o+l;break;case 3:n=f-l,i=a-l,s=o+l;break;case 4:f=n+l,a=i+l,o=s-l;break;case 5:n=f-l,a=i+l,o=s-l;break;case 6:f=n+l,i=a-l,o=s-l;break;case 7:n=f-l,i=a-l,o=s-l;break}this._root&&this._root.length&&(this._root=h)}return this._x0=n,this._y0=i,this._z0=o,this._x1=f,this._y1=a,this._z1=s,this}function se(){var t=[];return this.visit(function(e){if(!e.length)do t.push(e.data);while(e=e.next)}),t}function ue(t){return arguments.length?this.cover(+t[0][0],+t[0][1],+t[0][2]).cover(+t[1][0],+t[1][1],+t[1][2]):isNaN(this._x0)?void 0:[[this._x0,this._y0,this._z0],[this._x1,this._y1,this._z1]]}function M(t,e,r,n,i,o,f){this.node=t,this.x0=e,this.y0=r,this.z0=n,this.x1=i,this.y1=o,this.z1=f}function le(t,e,r,n){var i,o=this._x0,f=this._y0,a=this._z0,s,l,h,c,x,v,p=this._x1,w=this._y1,y=this._z1,u=[],g=this._root,m,d;for(g&&u.push(new M(g,o,f,a,p,w,y)),n==null?n=1/0:(o=t-n,f=e-n,a=r-n,p=t+n,w=e+n,y=r+n,n*=n);m=u.pop();)if(!(!(g=m.node)||(s=m.x0)>p||(l=m.y0)>w||(h=m.z0)>y||(c=m.x1)<o||(x=m.y1)<f||(v=m.z1)<a))if(g.length){var _=(s+c)/2,N=(l+x)/2,A=(h+v)/2;u.push(new M(g[7],_,N,A,c,x,v),new M(g[6],s,N,A,_,x,v),new M(g[5],_,l,A,c,N,v),new M(g[4],s,l,A,_,N,v),new M(g[3],_,N,h,c,x,A),new M(g[2],s,N,h,_,x,A),new M(g[1],_,l,h,c,N,A),new M(g[0],s,l,h,_,N,A)),(d=(r>=A)<<2|(e>=N)<<1|t>=_)&&(m=u[u.length-1],u[u.length-1]=u[u.length-1-d],u[u.length-1-d]=m)}else{var z=t-+this._x.call(null,g.data),D=e-+this._y.call(null,g.data),R=r-+this._z.call(null,g.data),P=z*z+D*D+R*R;if(P<n){var I=Math.sqrt(n=P);o=t-I,f=e-I,a=r-I,p=t+I,w=e+I,y=r+I,i=g.data}}return i}var Le=(t,e,r,n,i,o)=>Math.sqrt((t-n)**2+(e-i)**2+(r-o)**2);function he(t,e,r,n){let i=[],o=t-n,f=e-n,a=r-n,s=t+n,l=e+n,h=r+n;return this.visit((c,x,v,p,w,y,u)=>{if(!c.length)do{let g=c.data;Le(t,e,r,this._x(g),this._y(g),this._z(g))<=n&&i.push(g)}while(c=c.next);return x>s||v>l||p>h||w<o||y<f||u<a}),i}function ce(t){if(isNaN(x=+this._x.call(null,t))||isNaN(v=+this._y.call(null,t))||isNaN(p=+this._z.call(null,t)))return this;var e,r=this._root,n,i,o,f=this._x0,a=this._y0,s=this._z0,l=this._x1,h=this._y1,c=this._z1,x,v,p,w,y,u,g,m,d,_,N;if(!r)return this;if(r.length)for(;;){if((g=x>=(w=(f+l)/2))?f=w:l=w,(m=v>=(y=(a+h)/2))?a=y:h=y,(d=p>=(u=(s+c)/2))?s=u:c=u,e=r,!(r=r[_=d<<2|m<<1|g]))return this;if(!r.length)break;(e[_+1&7]||e[_+2&7]||e[_+3&7]||e[_+4&7]||e[_+5&7]||e[_+6&7]||e[_+7&7])&&(n=e,N=_)}for(;r.data!==t;)if(i=r,!(r=r.next))return this;return(o=r.next)&&delete r.next,i?(o?i.next=o:delete i.next,this):e?(o?e[_]=o:delete e[_],(r=e[0]||e[1]||e[2]||e[3]||e[4]||e[5]||e[6]||e[7])&&r===(e[7]||e[6]||e[5]||e[4]||e[3]||e[2]||e[1]||e[0])&&!r.length&&(n?n[N]=r:this._root=r),this):(this._root=o,this)}function pe(t){for(var e=0,r=t.length;e<r;++e)this.remove(t[e]);return this}function xe(){return this._root}function _e(){var t=0;return this.visit(function(e){if(!e.length)do++t;while(e=e.next)}),t}function ve(t){var e=[],r,n=this._root,i,o,f,a,s,l,h;for(n&&e.push(new M(n,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1));r=e.pop();)if(!t(n=r.node,o=r.x0,f=r.y0,a=r.z0,s=r.x1,l=r.y1,h=r.z1)&&n.length){var c=(o+s)/2,x=(f+l)/2,v=(a+h)/2;(i=n[7])&&e.push(new M(i,c,x,v,s,l,h)),(i=n[6])&&e.push(new M(i,o,x,v,c,l,h)),(i=n[5])&&e.push(new M(i,c,f,v,s,x,h)),(i=n[4])&&e.push(new M(i,o,f,v,c,x,h)),(i=n[3])&&e.push(new M(i,c,x,a,s,l,v)),(i=n[2])&&e.push(new M(i,o,x,a,c,l,v)),(i=n[1])&&e.push(new M(i,c,f,a,s,x,v)),(i=n[0])&&e.push(new M(i,o,f,a,c,x,v))}return this}function ye(t){var e=[],r=[],n;for(this._root&&e.push(new M(this._root,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1));n=e.pop();){var i=n.node;if(i.length){var o,f=n.x0,a=n.y0,s=n.z0,l=n.x1,h=n.y1,c=n.z1,x=(f+l)/2,v=(a+h)/2,p=(s+c)/2;(o=i[0])&&e.push(new M(o,f,a,s,x,v,p)),(o=i[1])&&e.push(new M(o,x,a,s,l,v,p)),(o=i[2])&&e.push(new M(o,f,v,s,x,h,p)),(o=i[3])&&e.push(new M(o,x,v,s,l,h,p)),(o=i[4])&&e.push(new M(o,f,a,p,x,v,c)),(o=i[5])&&e.push(new M(o,x,a,p,l,v,c)),(o=i[6])&&e.push(new M(o,f,v,p,x,h,c)),(o=i[7])&&e.push(new M(o,x,v,p,l,h,c))}r.push(n)}for(;n=r.pop();)t(n.node,n.x0,n.y0,n.z0,n.x1,n.y1,n.z1);return this}function de(t){return t[0]}function me(t){return arguments.length?(this._x=t,this):this._x}function ge(t){return t[1]}function we(t){return arguments.length?(this._y=t,this):this._y}function Ne(t){return t[2]}function Ae(t){return arguments.length?(this._z=t,this):this._z}function X(t,e,r,n){var i=new at(e??de,r??ge,n??Ne,NaN,NaN,NaN,NaN,NaN,NaN);return t==null?i:i.addAll(t)}function at(t,e,r,n,i,o,f,a,s){this._x=t,this._y=e,this._z=r,this._x0=n,this._y0=i,this._z0=o,this._x1=f,this._y1=a,this._z1=s,this._root=void 0}function ze(t){for(var e={data:t.data},r=e;t=t.next;)r=r.next={data:t.data};return e}var S=X.prototype=at.prototype;S.copy=function(){var t=new at(this._x,this._y,this._z,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1),e=this._root,r,n;if(!e)return t;if(!e.length)return t._root=ze(e),t;for(r=[{source:e,target:t._root=new Array(8)}];e=r.pop();)for(var i=0;i<8;++i)(n=e.source[i])&&(n.length?r.push({source:n,target:e.target[i]=new Array(8)}):e.target[i]=ze(n));return t};S.add=ie;S.addAll=ae;S.cover=fe;S.data=se;S.extent=ue;S.find=le;S.findAllWithinRadius=he;S.remove=ce;S.removeAll=pe;S.root=xe;S.size=_e;S.visit=ve;S.visitAfter=ye;S.x=me;S.y=we;S.z=Ae;function b(t){return function(){return t}}function B(t){return(t()-.5)*1e-6}function je(t){return t.index}function Me(t,e){var r=t.get(e);if(!r)throw new Error("node not found: "+e);return r}function ft(t){var e=je,r=x,n,i=b(30),o,f,a,s,l,h,c=1;t==null&&(t=[]);function x(u){return 1/Math.min(s[u.source.index],s[u.target.index])}function v(u){for(var g=0,m=t.length;g<c;++g)for(var d=0,_,N,A,z=0,D=0,R=0,P,I;d<m;++d)_=t[d],N=_.source,A=_.target,z=A.x+A.vx-N.x-N.vx||B(h),a>1&&(D=A.y+A.vy-N.y-N.vy||B(h)),a>2&&(R=A.z+A.vz-N.z-N.vz||B(h)),P=Math.sqrt(z*z+D*D+R*R),P=(P-o[d])/P*u*n[d],z*=P,D*=P,R*=P,A.vx-=z*(I=l[d]),a>1&&(A.vy-=D*I),a>2&&(A.vz-=R*I),N.vx+=z*(I=1-I),a>1&&(N.vy+=D*I),a>2&&(N.vz+=R*I)}function p(){if(f){var u,g=f.length,m=t.length,d=new Map(f.map((N,A)=>[e(N,A,f),N])),_;for(u=0,s=new Array(g);u<m;++u)_=t[u],_.index=u,typeof _.source!="object"&&(_.source=Me(d,_.source)),typeof _.target!="object"&&(_.target=Me(d,_.target)),s[_.source.index]=(s[_.source.index]||0)+1,s[_.target.index]=(s[_.target.index]||0)+1;for(u=0,l=new Array(m);u<m;++u)_=t[u],l[u]=s[_.source.index]/(s[_.source.index]+s[_.target.index]);n=new Array(m),w(),o=new Array(m),y()}}function w(){if(f)for(var u=0,g=t.length;u<g;++u)n[u]=+r(t[u],u,t)}function y(){if(f)for(var u=0,g=t.length;u<g;++u)o[u]=+i(t[u],u,t)}return v.initialize=function(u,...g){f=u,h=g.find(m=>typeof m=="function")||Math.random,a=g.find(m=>[1,2,3].includes(m))||2,p()},v.links=function(u){return arguments.length?(t=u,p(),v):t},v.id=function(u){return arguments.length?(e=u,v):e},v.iterations=function(u){return arguments.length?(c=+u,v):c},v.strength=function(u){return arguments.length?(r=typeof u=="function"?u:b(+u),w(),v):r},v.distance=function(u){return arguments.length?(i=typeof u=="function"?u:b(+u),y(),v):i},v}var Te={value:()=>{}};function ke(){for(var t=0,e=arguments.length,r={},n;t<e;++t){if(!(n=arguments[t]+"")||n in r||/[\\s.]/.test(n))throw new Error("illegal type: "+n);r[n]=[]}return new J(r)}function J(t){this._=t}function Oe(t,e){return t.trim().split(/^|\\s+/).map(function(r){var n="",i=r.indexOf(".");if(i>=0&&(n=r.slice(i+1),r=r.slice(0,i)),r&&!e.hasOwnProperty(r))throw new Error("unknown type: "+r);return{type:r,name:n}})}J.prototype=ke.prototype={constructor:J,on:function(t,e){var r=this._,n=Oe(t+"",r),i,o=-1,f=n.length;if(arguments.length<2){for(;++o<f;)if((i=(t=n[o]).type)&&(i=Ce(r[i],t.name)))return i;return}if(e!=null&&typeof e!="function")throw new Error("invalid callback: "+e);for(;++o<f;)if(i=(t=n[o]).type)r[i]=be(r[i],t.name,e);else if(e==null)for(i in r)r[i]=be(r[i],t.name,null);return this},copy:function(){var t={},e=this._;for(var r in e)t[r]=e[r].slice();return new J(t)},call:function(t,e){if((i=arguments.length-2)>0)for(var r=new Array(i),n=0,i,o;n<i;++n)r[n]=arguments[n+2];if(!this._.hasOwnProperty(t))throw new Error("unknown type: "+t);for(o=this._[t],n=0,i=o.length;n<i;++n)o[n].value.apply(e,r)},apply:function(t,e,r){if(!this._.hasOwnProperty(t))throw new Error("unknown type: "+t);for(var n=this._[t],i=0,o=n.length;i<o;++i)n[i].value.apply(e,r)}};function Ce(t,e){for(var r=0,n=t.length,i;r<n;++r)if((i=t[r]).name===e)return i.value}function be(t,e,r){for(var n=0,i=t.length;n<i;++n)if(t[n].name===e){t[n]=Te,t=t.slice(0,n).concat(t.slice(n+1));break}return r!=null&&t.push({name:e,value:r}),t}var st=ke;var T=0,H=0,Y=0,qe=1e3,K,Q,V=0,j=0,$=0,Z=typeof performance=="object"&&performance.now?performance:Date,Se=typeof window=="object"&&window.requestAnimationFrame?window.requestAnimationFrame.bind(window):function(t){setTimeout(t,17)};function ht(){return j||(Se(Xe),j=Z.now()+$)}function Xe(){j=0}function ut(){this._call=this._time=this._next=null}ut.prototype=tt.prototype={constructor:ut,restart:function(t,e,r){if(typeof t!="function")throw new TypeError("callback is not a function");r=(r==null?ht():+r)+(e==null?0:+e),!this._next&&Q!==this&&(Q?Q._next=this:K=this,Q=this),this._call=t,this._time=r,lt()},stop:function(){this._call&&(this._call=null,this._time=1/0,lt())}};function tt(t,e,r){var n=new ut;return n.restart(t,e,r),n}function Fe(){ht(),++T;for(var t=K,e;t;)(e=j-t._time)>=0&&t._call.call(void 0,e),t=t._next;--T}function Ie(){j=(V=Z.now())+$,T=H=0;try{Fe()}finally{T=0,He(),j=0}}function Ye(){var t=Z.now(),e=t-V;e>qe&&($-=e,V=t)}function He(){for(var t,e=K,r,n=1/0;e;)e._call?(n>e._time&&(n=e._time),t=e,e=e._next):(r=e._next,e._next=null,e=t?t._next=r:K=r);Q=t,lt(n)}function lt(t){if(!T){H&&(H=clearTimeout(H));var e=t-j;e>24?(t<1/0&&(H=setTimeout(Ie,t-Z.now()-$)),Y&&(Y=clearInterval(Y))):(Y||(V=Z.now(),Y=setInterval(Ye,qe)),T=1,Se(Ie))}}function Pe(){let t=1;return()=>(t=(1664525*t+1013904223)%4294967296)/4294967296}var We=3;function et(t){return t.x}function ct(t){return t.y}function De(t){return t.z}var Qe=10,Ze=Math.PI*(3-Math.sqrt(5)),Ge=Math.PI*20/(9+Math.sqrt(221));function pt(t,e){e=e||2;var r=Math.min(We,Math.max(1,Math.round(e))),n,i=1,o=.001,f=1-Math.pow(o,1/300),a=0,s=.6,l=new Map,h=tt(v),c=st("tick","end"),x=Pe();t==null&&(t=[]);function v(){p(),c.call("tick",n),i<o&&(h.stop(),c.call("end",n))}function p(u){var g,m=t.length,d;u===void 0&&(u=1);for(var _=0;_<u;++_)for(i+=(a-i)*f,l.forEach(function(N){N(i)}),g=0;g<m;++g)d=t[g],d.fx==null?d.x+=d.vx*=s:(d.x=d.fx,d.vx=0),r>1&&(d.fy==null?d.y+=d.vy*=s:(d.y=d.fy,d.vy=0)),r>2&&(d.fz==null?d.z+=d.vz*=s:(d.z=d.fz,d.vz=0));return n}function w(){for(var u=0,g=t.length,m;u<g;++u){if(m=t[u],m.index=u,m.fx!=null&&(m.x=m.fx),m.fy!=null&&(m.y=m.fy),m.fz!=null&&(m.z=m.fz),isNaN(m.x)||r>1&&isNaN(m.y)||r>2&&isNaN(m.z)){var d=Qe*(r>2?Math.cbrt(.5+u):r>1?Math.sqrt(.5+u):u),_=u*Ze,N=u*Ge;r===1?m.x=d:r===2?(m.x=d*Math.cos(_),m.y=d*Math.sin(_)):(m.x=d*Math.sin(_)*Math.cos(N),m.y=d*Math.cos(_),m.z=d*Math.sin(_)*Math.sin(N))}(isNaN(m.vx)||r>1&&isNaN(m.vy)||r>2&&isNaN(m.vz))&&(m.vx=0,r>1&&(m.vy=0),r>2&&(m.vz=0))}}function y(u){return u.initialize&&u.initialize(t,x,r),u}return w(),n={tick:p,restart:function(){return h.restart(v),n},stop:function(){return h.stop(),n},numDimensions:function(u){return arguments.length?(r=Math.min(We,Math.max(1,Math.round(u))),l.forEach(y),n):r},nodes:function(u){return arguments.length?(t=u,w(),l.forEach(y),n):t},alpha:function(u){return arguments.length?(i=+u,n):i},alphaMin:function(u){return arguments.length?(o=+u,n):o},alphaDecay:function(u){return arguments.length?(f=+u,n):+f},alphaTarget:function(u){return arguments.length?(a=+u,n):a},velocityDecay:function(u){return arguments.length?(s=1-u,n):1-s},randomSource:function(u){return arguments.length?(x=u,l.forEach(y),n):x},force:function(u,g){return arguments.length>1?(g==null?l.delete(u):l.set(u,y(g)),n):l.get(u)},find:function(){var u=Array.prototype.slice.call(arguments),g=u.shift()||0,m=(r>1?u.shift():null)||0,d=(r>2?u.shift():null)||0,_=u.shift()||1/0,N=0,A=t.length,z,D,R,P,I,At;for(_*=_,N=0;N<A;++N)I=t[N],z=g-I.x,D=m-(I.y||0),R=d-(I.z||0),P=z*z+D*D+R*R,P<_&&(At=I,_=P);return At},on:function(u,g){return arguments.length>1?(c.on(u,g),n):c.on(u)}}}function xt(){var t,e,r,n,i,o=b(-30),f,a=1,s=1/0,l=.81;function h(p){var w,y=t.length,u=(e===1?O(t,et):e===2?C(t,et,ct):e===3?X(t,et,ct,De):null).visitAfter(x);for(i=p,w=0;w<y;++w)r=t[w],u.visit(v)}function c(){if(t){var p,w=t.length,y;for(f=new Array(w),p=0;p<w;++p)y=t[p],f[y.index]=+o(y,p,t)}}function x(p){var w=0,y,u,g=0,m,d,_,N,A=p.length;if(A){for(m=d=_=N=0;N<A;++N)(y=p[N])&&(u=Math.abs(y.value))&&(w+=y.value,g+=u,m+=u*(y.x||0),d+=u*(y.y||0),_+=u*(y.z||0));w*=Math.sqrt(4/A),p.x=m/g,e>1&&(p.y=d/g),e>2&&(p.z=_/g)}else{y=p,y.x=y.data.x,e>1&&(y.y=y.data.y),e>2&&(y.z=y.data.z);do w+=f[y.data.index];while(y=y.next)}p.value=w}function v(p,w,y,u,g){if(!p.value)return!0;var m=[y,u,g][e-1],d=p.x-r.x,_=e>1?p.y-r.y:0,N=e>2?p.z-r.z:0,A=m-w,z=d*d+_*_+N*N;if(A*A/l<z)return z<s&&(d===0&&(d=B(n),z+=d*d),e>1&&_===0&&(_=B(n),z+=_*_),e>2&&N===0&&(N=B(n),z+=N*N),z<a&&(z=Math.sqrt(a*z)),r.vx+=d*p.value*i/z,e>1&&(r.vy+=_*p.value*i/z),e>2&&(r.vz+=N*p.value*i/z)),!0;if(p.length||z>=s)return;(p.data!==r||p.next)&&(d===0&&(d=B(n),z+=d*d),e>1&&_===0&&(_=B(n),z+=_*_),e>2&&N===0&&(N=B(n),z+=N*N),z<a&&(z=Math.sqrt(a*z)));do p.data!==r&&(A=f[p.data.index]*i/z,r.vx+=d*A,e>1&&(r.vy+=_*A),e>2&&(r.vz+=N*A));while(p=p.next)}return h.initialize=function(p,...w){t=p,n=w.find(y=>typeof y=="function")||Math.random,e=w.find(y=>[1,2,3].includes(y))||2,c()},h.strength=function(p){return arguments.length?(o=typeof p=="function"?p:b(+p),c(),h):o},h.distanceMin=function(p){return arguments.length?(a=p*p,h):Math.sqrt(a)},h.distanceMax=function(p){return arguments.length?(s=p*p,h):Math.sqrt(s)},h.theta=function(p){return arguments.length?(l=p*p,h):Math.sqrt(l)},h}function _t(t){var e=b(.1),r,n,i;typeof t!="function"&&(t=b(t==null?0:+t));function o(a){for(var s=0,l=r.length,h;s<l;++s)h=r[s],h.vx+=(i[s]-h.x)*n[s]*a}function f(){if(r){var a,s=r.length;for(n=new Array(s),i=new Array(s),a=0;a<s;++a)n[a]=isNaN(i[a]=+t(r[a],a,r))?0:+e(r[a],a,r)}}return o.initialize=function(a){r=a,f()},o.strength=function(a){return arguments.length?(e=typeof a=="function"?a:b(+a),f(),o):e},o.x=function(a){return arguments.length?(t=typeof a=="function"?a:b(+a),f(),o):t},o}function vt(t){var e=b(.1),r,n,i;typeof t!="function"&&(t=b(t==null?0:+t));function o(a){for(var s=0,l=r.length,h;s<l;++s)h=r[s],h.vy+=(i[s]-h.y)*n[s]*a}function f(){if(r){var a,s=r.length;for(n=new Array(s),i=new Array(s),a=0;a<s;++a)n[a]=isNaN(i[a]=+t(r[a],a,r))?0:+e(r[a],a,r)}}return o.initialize=function(a){r=a,f()},o.strength=function(a){return arguments.length?(e=typeof a=="function"?a:b(+a),f(),o):e},o.y=function(a){return arguments.length?(t=typeof a=="function"?a:b(+a),f(),o):t},o}function yt(t){var e=b(.1),r,n,i;typeof t!="function"&&(t=b(t==null?0:+t));function o(a){for(var s=0,l=r.length,h;s<l;++s)h=r[s],h.vz+=(i[s]-h.z)*n[s]*a}function f(){if(r){var a,s=r.length;for(n=new Array(s),i=new Array(s),a=0;a<s;++a)n[a]=isNaN(i[a]=+t(r[a],a,r))?0:+e(r[a],a,r)}}return o.initialize=function(a){r=a,f()},o.strength=function(a){return arguments.length?(e=typeof a=="function"?a:b(+a),f(),o):e},o.z=function(a){return arguments.length?(t=typeof a=="function"?a:b(+a),f(),o):t},o}function dt(t,e){let r=[],n=1,i=o=>{if(t!==0)for(let f of r){let a=f.x??0,s=f.z??0,l=Math.hypot(a,s);if(l<1e-4)continue;let h=Math.min(Math.max((e[f.index??0]||1)/n,.3),3),c=t*h*o*l/200;f.vx=(f.vx??0)-a/l*c,f.vz=(f.vz??0)-s/l*c}};return i.initialize=o=>{r=o;let f=0;for(let a of o)f+=e[a.index??0]||1;n=o.length?f/o.length:1},i}function mt(t){let e=[],r=n=>{if(t!==0)for(let i of e){let o=i.x??0,f=i.z??0,a=Math.hypot(o,f);if(a<.001)continue;let s=1/(1+a/160),l=t*n*s;i.vx=(i.vx??0)+-f/a*l*a,i.vz=(i.vz??0)+o/a*l*a}};return r.initialize=n=>{e=n},r}var Re=self,k=null,G=[],U=new Float32Array(0),gt=[],L=!0,Nt=0,nt=!1,wt=!1;function Ee(t){return e=>{let r=typeof e.source=="number"?e.source:e.source.index??0,n=typeof e.target=="number"?e.target:e.target.index??0,i=1/Math.min(U[r]??1,U[n]??1);return Math.min(i*t,1)}}function Ue(t){if(!k)return;k.force("charge")?.strength(t.charge);let e=k.force("link");e?.distance(t.linkDistance),e?.strength(Ee(t.linkStrength)),k.force("x")?.strength(t.centerPull),k.force("y")?.strength(t.centerPull+t.flatten),k.force("z")?.strength(t.centerPull),k.force("core",dt(t.coreGravity,U)),k.force("spiral",mt(t.spiral))}function rt(){wt||(wt=!0,self.setTimeout(Je,0))}function Je(){wt=!1;let t=k;if(!t||L)return;let e=Date.now();for(;Date.now()-e<12;)if(t.tick(),Nt++,t.alpha()<t.alphaMin()){L=!0;break}nt=!0,Be(),L||rt()}function Be(){if(!nt||!k)return;let t=gt.pop();if(!t)return;let e=new Float32Array(t);for(let r=0;r<G.length;r++){let n=G[r];n&&(e[r*3]=n.x,e[r*3+1]=n.y,e[r*3+2]=n.z)}nt=!1,Re.postMessage({type:"tick",buffer:t,alpha:k.alpha(),settled:L,ticks:Nt},[t])}Re.onmessage=t=>{let e=t.data;switch(e.type){case"init":{k?.stop();let r=new Float32Array(e.positions);U=new Float32Array(e.degrees);let n=new Uint32Array(e.links);G=[];for(let o=0;o<e.count;o++)G.push({x:r[o*3]??0,y:r[o*3+1]??0,z:r[o*3+2]??0});let i=[];for(let o=0;o<n.length;o+=2)i.push({source:n[o]??0,target:n[o+1]??0});k=pt(G,3).alphaDecay(1-Math.pow(.001,1/300)).velocityDecay(e.params.velocityDecay).force("link",ft(i).distance(e.params.linkDistance).strength(Ee(e.params.linkStrength))).force("charge",xt().strength(e.params.charge).distanceMax(800)).force("x",_t(0).strength(e.params.centerPull)).force("y",vt(0).strength(e.params.centerPull+e.params.flatten)).force("z",yt(0).strength(e.params.centerPull)).force("core",dt(e.params.coreGravity,U)).force("spiral",mt(e.params.spiral)).stop(),k.alpha(e.initialAlpha),gt=[e.bufA,e.bufB],Nt=0,L=e.initialAlpha<k.alphaMin(),nt=!1,L||rt();break}case"params":Ue(e.params),k&&(k.alpha(Math.max(k.alpha(),.5)),L=!1,rt());break;case"reheat":k&&(k.alpha(Math.max(k.alpha(),e.alpha)),L=!1,rt());break;case"buffer":gt.push(e.buffer),Be();break}};})();
`;var Zs=class{constructor(){q(this,"positions",new Float32Array(0));q(this,"worker",null);q(this,"url","");q(this,"dirty",!1);q(this,"settled",!0);q(this,"_ticks",0)}get ticks(){return this._ticks}init(t,e,n,s=1){this.disposeWorker(),this.positions=e,this._ticks=0,this.dirty=!1,this.url=URL.createObjectURL(new Blob([Wd],{type:"text/javascript"})),this.worker=new Worker(this.url),this.worker.onmessage=f=>{let u=f.data;if(u.type!=="tick")return;let d=new Float32Array(u.buffer);this.positions.set(d.subarray(0,this.positions.length)),this._ticks=u.ticks,this.settled=u.settled,this.dirty=!0,this.worker?.postMessage({type:"buffer",buffer:u.buffer},[u.buffer])};let r=t.nodes.length,a=new Float32Array(e),o=new Uint32Array(t.links.length*2);t.links.forEach((f,u)=>{o[u*2]=f.source,o[u*2+1]=f.target});let l=new Float32Array(r);t.nodes.forEach((f,u)=>l[u]=Math.max(f.degree,1));let c=new ArrayBuffer(r*3*4),h=new ArrayBuffer(r*3*4);this.settled=s<.001,this.worker.postMessage({type:"init",count:r,positions:a.buffer,links:o.buffer,degrees:l.buffer,params:n,initialAlpha:s,bufA:c,bufB:h},[a.buffer,o.buffer,l.buffer,c,h])}step(){let t=this.dirty;return this.dirty=!1,t}isSettled(){return this.settled}reheat(t=.3){this.settled=!1,this.worker?.postMessage({type:"reheat",alpha:t})}updateParams(t){this.settled=!1,this.worker?.postMessage({type:"params",params:t})}disposeWorker(){this.worker&&(this.worker.onmessage=null,this.worker.terminate()),this.worker=null,this.url&&(URL.revokeObjectURL(this.url),this.url="")}dispose(){this.disposeWorker(),this.settled=!0,this.dirty=!1}};function Xd(i){let t=+this._x.call(null,i);return qd(this.cover(t),t,i)}function qd(i,t,e){if(isNaN(t))return i;var n,s=i._root,r={data:e},a=i._x0,o=i._x1,l,c,h,f,u;if(!s)return i._root=r,i;for(;s.length;)if((h=t>=(l=(a+o)/2))?a=l:o=l,n=s,!(s=s[f=+h]))return n[f]=r,i;if(c=+i._x.call(null,s.data),t===c)return r.next=s,n?n[f]=r:i._root=r,i;do n=n?n[f]=new Array(2):i._root=new Array(2),(h=t>=(l=(a+o)/2))?a=l:o=l;while((f=+h)==(u=+(c>=l)));return n[u]=s,n[f]=r,i}function Yd(i){Array.isArray(i)||(i=Array.from(i));let t=i.length,e=new Float64Array(t),n=1/0,s=-1/0;for(let r=0,a;r<t;++r)isNaN(a=+this._x.call(null,i[r]))||(e[r]=a,a<n&&(n=a),a>s&&(s=a));if(n>s)return this;this.cover(n).cover(s);for(let r=0;r<t;++r)qd(this,e[r],i[r]);return this}function Zd(i){if(isNaN(i=+i))return this;var t=this._x0,e=this._x1;if(isNaN(t))e=(t=Math.floor(i))+1;else{for(var n=e-t||1,s=this._root,r,a;t>i||i>=e;)switch(a=+(i<t),r=new Array(2),r[a]=s,s=r,n*=2,a){case 0:e=t+n;break;case 1:t=e-n;break}this._root&&this._root.length&&(this._root=s)}return this._x0=t,this._x1=e,this}function Kd(){var i=[];return this.visit(function(t){if(!t.length)do i.push(t.data);while(t=t.next)}),i}function Jd(i){return arguments.length?this.cover(+i[0][0]).cover(+i[1][0]):isNaN(this._x0)?void 0:[[this._x0],[this._x1]]}function Tn(i,t,e){this.node=i,this.x0=t,this.x1=e}function $d(i,t){var e,n=this._x0,s,r,a=this._x1,o=[],l=this._root,c,h;for(l&&o.push(new Tn(l,n,a)),t==null?t=1/0:(n=i-t,a=i+t);c=o.pop();)if(!(!(l=c.node)||(s=c.x0)>a||(r=c.x1)<n))if(l.length){var f=(s+r)/2;o.push(new Tn(l[1],f,r),new Tn(l[0],s,f)),(h=+(i>=f))&&(c=o[o.length-1],o[o.length-1]=o[o.length-1-h],o[o.length-1-h]=c)}else{var u=Math.abs(i-+this._x.call(null,l.data));u<t&&(t=u,n=i-u,a=i+u,e=l.data)}return e}function jd(i){if(isNaN(l=+this._x.call(null,i)))return this;var t,e=this._root,n,s,r,a=this._x0,o=this._x1,l,c,h,f,u;if(!e)return this;if(e.length)for(;;){if((h=l>=(c=(a+o)/2))?a=c:o=c,t=e,!(e=e[f=+h]))return this;if(!e.length)break;t[f+1&1]&&(n=t,u=f)}for(;e.data!==i;)if(s=e,!(e=e.next))return this;return(r=e.next)&&delete e.next,s?(r?s.next=r:delete s.next,this):t?(r?t[f]=r:delete t[f],(e=t[0]||t[1])&&e===(t[1]||t[0])&&!e.length&&(n?n[u]=e:this._root=e),this):(this._root=r,this)}function Qd(i){for(var t=0,e=i.length;t<e;++t)this.remove(i[t]);return this}function tp(){return this._root}function ep(){var i=0;return this.visit(function(t){if(!t.length)do++i;while(t=t.next)}),i}function np(i){var t=[],e,n=this._root,s,r,a;for(n&&t.push(new Tn(n,this._x0,this._x1));e=t.pop();)if(!i(n=e.node,r=e.x0,a=e.x1)&&n.length){var o=(r+a)/2;(s=n[1])&&t.push(new Tn(s,o,a)),(s=n[0])&&t.push(new Tn(s,r,o))}return this}function ip(i){var t=[],e=[],n;for(this._root&&t.push(new Tn(this._root,this._x0,this._x1));n=t.pop();){var s=n.node;if(s.length){var r,a=n.x0,o=n.x1,l=(a+o)/2;(r=s[0])&&t.push(new Tn(r,a,l)),(r=s[1])&&t.push(new Tn(r,l,o))}e.push(n)}for(;n=e.pop();)i(n.node,n.x0,n.x1);return this}function sp(i){return i[0]}function rp(i){return arguments.length?(this._x=i,this):this._x}function Qr(i,t){var e=new kh(t??sp,NaN,NaN);return i==null?e:e.addAll(i)}function kh(i,t,e){this._x=i,this._x0=t,this._x1=e,this._root=void 0}function ap(i){for(var t={data:i.data},e=t;i=i.next;)e=e.next={data:i.data};return t}var ln=Qr.prototype=kh.prototype;ln.copy=function(){var i=new kh(this._x,this._x0,this._x1),t=this._root,e,n;if(!t)return i;if(!t.length)return i._root=ap(t),i;for(e=[{source:t,target:i._root=new Array(2)}];t=e.pop();)for(var s=0;s<2;++s)(n=t.source[s])&&(n.length?e.push({source:n,target:t.target[s]=new Array(2)}):t.target[s]=ap(n));return i};ln.add=Xd;ln.addAll=Yd;ln.cover=Zd;ln.data=Kd;ln.extent=Jd;ln.find=$d;ln.remove=jd;ln.removeAll=Qd;ln.root=tp;ln.size=ep;ln.visit=np;ln.visitAfter=ip;ln.x=rp;function op(i){let t=+this._x.call(null,i),e=+this._y.call(null,i);return lp(this.cover(t,e),t,e,i)}function lp(i,t,e,n){if(isNaN(t)||isNaN(e))return i;var s,r=i._root,a={data:n},o=i._x0,l=i._y0,c=i._x1,h=i._y1,f,u,d,m,_,g,p,y;if(!r)return i._root=a,i;for(;r.length;)if((_=t>=(f=(o+c)/2))?o=f:c=f,(g=e>=(u=(l+h)/2))?l=u:h=u,s=r,!(r=r[p=g<<1|_]))return s[p]=a,i;if(d=+i._x.call(null,r.data),m=+i._y.call(null,r.data),t===d&&e===m)return a.next=r,s?s[p]=a:i._root=a,i;do s=s?s[p]=new Array(4):i._root=new Array(4),(_=t>=(f=(o+c)/2))?o=f:c=f,(g=e>=(u=(l+h)/2))?l=u:h=u;while((p=g<<1|_)===(y=(m>=u)<<1|d>=f));return s[y]=r,s[p]=a,i}function cp(i){var t,e,n=i.length,s,r,a=new Array(n),o=new Array(n),l=1/0,c=1/0,h=-1/0,f=-1/0;for(e=0;e<n;++e)isNaN(s=+this._x.call(null,t=i[e]))||isNaN(r=+this._y.call(null,t))||(a[e]=s,o[e]=r,s<l&&(l=s),s>h&&(h=s),r<c&&(c=r),r>f&&(f=r));if(l>h||c>f)return this;for(this.cover(l,c).cover(h,f),e=0;e<n;++e)lp(this,a[e],o[e],i[e]);return this}function hp(i,t){if(isNaN(i=+i)||isNaN(t=+t))return this;var e=this._x0,n=this._y0,s=this._x1,r=this._y1;if(isNaN(e))s=(e=Math.floor(i))+1,r=(n=Math.floor(t))+1;else{for(var a=s-e||1,o=this._root,l,c;e>i||i>=s||n>t||t>=r;)switch(c=(t<n)<<1|i<e,l=new Array(4),l[c]=o,o=l,a*=2,c){case 0:s=e+a,r=n+a;break;case 1:e=s-a,r=n+a;break;case 2:s=e+a,n=r-a;break;case 3:e=s-a,n=r-a;break}this._root&&this._root.length&&(this._root=o)}return this._x0=e,this._y0=n,this._x1=s,this._y1=r,this}function up(){var i=[];return this.visit(function(t){if(!t.length)do i.push(t.data);while(t=t.next)}),i}function fp(i){return arguments.length?this.cover(+i[0][0],+i[0][1]).cover(+i[1][0],+i[1][1]):isNaN(this._x0)?void 0:[[this._x0,this._y0],[this._x1,this._y1]]}function ke(i,t,e,n,s){this.node=i,this.x0=t,this.y0=e,this.x1=n,this.y1=s}function dp(i,t,e){var n,s=this._x0,r=this._y0,a,o,l,c,h=this._x1,f=this._y1,u=[],d=this._root,m,_;for(d&&u.push(new ke(d,s,r,h,f)),e==null?e=1/0:(s=i-e,r=t-e,h=i+e,f=t+e,e*=e);m=u.pop();)if(!(!(d=m.node)||(a=m.x0)>h||(o=m.y0)>f||(l=m.x1)<s||(c=m.y1)<r))if(d.length){var g=(a+l)/2,p=(o+c)/2;u.push(new ke(d[3],g,p,l,c),new ke(d[2],a,p,g,c),new ke(d[1],g,o,l,p),new ke(d[0],a,o,g,p)),(_=(t>=p)<<1|i>=g)&&(m=u[u.length-1],u[u.length-1]=u[u.length-1-_],u[u.length-1-_]=m)}else{var y=i-+this._x.call(null,d.data),S=t-+this._y.call(null,d.data),b=y*y+S*S;if(b<e){var T=Math.sqrt(e=b);s=i-T,r=t-T,h=i+T,f=t+T,n=d.data}}return n}function pp(i){if(isNaN(h=+this._x.call(null,i))||isNaN(f=+this._y.call(null,i)))return this;var t,e=this._root,n,s,r,a=this._x0,o=this._y0,l=this._x1,c=this._y1,h,f,u,d,m,_,g,p;if(!e)return this;if(e.length)for(;;){if((m=h>=(u=(a+l)/2))?a=u:l=u,(_=f>=(d=(o+c)/2))?o=d:c=d,t=e,!(e=e[g=_<<1|m]))return this;if(!e.length)break;(t[g+1&3]||t[g+2&3]||t[g+3&3])&&(n=t,p=g)}for(;e.data!==i;)if(s=e,!(e=e.next))return this;return(r=e.next)&&delete e.next,s?(r?s.next=r:delete s.next,this):t?(r?t[g]=r:delete t[g],(e=t[0]||t[1]||t[2]||t[3])&&e===(t[3]||t[2]||t[1]||t[0])&&!e.length&&(n?n[p]=e:this._root=e),this):(this._root=r,this)}function mp(i){for(var t=0,e=i.length;t<e;++t)this.remove(i[t]);return this}function gp(){return this._root}function _p(){var i=0;return this.visit(function(t){if(!t.length)do++i;while(t=t.next)}),i}function xp(i){var t=[],e,n=this._root,s,r,a,o,l;for(n&&t.push(new ke(n,this._x0,this._y0,this._x1,this._y1));e=t.pop();)if(!i(n=e.node,r=e.x0,a=e.y0,o=e.x1,l=e.y1)&&n.length){var c=(r+o)/2,h=(a+l)/2;(s=n[3])&&t.push(new ke(s,c,h,o,l)),(s=n[2])&&t.push(new ke(s,r,h,c,l)),(s=n[1])&&t.push(new ke(s,c,a,o,h)),(s=n[0])&&t.push(new ke(s,r,a,c,h))}return this}function vp(i){var t=[],e=[],n;for(this._root&&t.push(new ke(this._root,this._x0,this._y0,this._x1,this._y1));n=t.pop();){var s=n.node;if(s.length){var r,a=n.x0,o=n.y0,l=n.x1,c=n.y1,h=(a+l)/2,f=(o+c)/2;(r=s[0])&&t.push(new ke(r,a,o,h,f)),(r=s[1])&&t.push(new ke(r,h,o,l,f)),(r=s[2])&&t.push(new ke(r,a,f,h,c)),(r=s[3])&&t.push(new ke(r,h,f,l,c))}e.push(n)}for(;n=e.pop();)i(n.node,n.x0,n.y0,n.x1,n.y1);return this}function yp(i){return i[0]}function Mp(i){return arguments.length?(this._x=i,this):this._x}function bp(i){return i[1]}function Sp(i){return arguments.length?(this._y=i,this):this._y}function ta(i,t,e){var n=new zh(t??yp,e??bp,NaN,NaN,NaN,NaN);return i==null?n:n.addAll(i)}function zh(i,t,e,n,s,r){this._x=i,this._y=t,this._x0=e,this._y0=n,this._x1=s,this._y1=r,this._root=void 0}function wp(i){for(var t={data:i.data},e=t;i=i.next;)e=e.next={data:i.data};return t}var Qe=ta.prototype=zh.prototype;Qe.copy=function(){var i=new zh(this._x,this._y,this._x0,this._y0,this._x1,this._y1),t=this._root,e,n;if(!t)return i;if(!t.length)return i._root=wp(t),i;for(e=[{source:t,target:i._root=new Array(4)}];t=e.pop();)for(var s=0;s<4;++s)(n=t.source[s])&&(n.length?e.push({source:n,target:t.target[s]=new Array(4)}):t.target[s]=wp(n));return i};Qe.add=op;Qe.addAll=cp;Qe.cover=hp;Qe.data=up;Qe.extent=fp;Qe.find=dp;Qe.remove=pp;Qe.removeAll=mp;Qe.root=gp;Qe.size=_p;Qe.visit=xp;Qe.visitAfter=vp;Qe.x=Mp;Qe.y=Sp;function Ap(i){let t=+this._x.call(null,i),e=+this._y.call(null,i),n=+this._z.call(null,i);return Tp(this.cover(t,e,n),t,e,n,i)}function Tp(i,t,e,n,s){if(isNaN(t)||isNaN(e)||isNaN(n))return i;var r,a=i._root,o={data:s},l=i._x0,c=i._y0,h=i._z0,f=i._x1,u=i._y1,d=i._z1,m,_,g,p,y,S,b,T,w,R,v;if(!a)return i._root=o,i;for(;a.length;)if((b=t>=(m=(l+f)/2))?l=m:f=m,(T=e>=(_=(c+u)/2))?c=_:u=_,(w=n>=(g=(h+d)/2))?h=g:d=g,r=a,!(a=a[R=w<<2|T<<1|b]))return r[R]=o,i;if(p=+i._x.call(null,a.data),y=+i._y.call(null,a.data),S=+i._z.call(null,a.data),t===p&&e===y&&n===S)return o.next=a,r?r[R]=o:i._root=o,i;do r=r?r[R]=new Array(8):i._root=new Array(8),(b=t>=(m=(l+f)/2))?l=m:f=m,(T=e>=(_=(c+u)/2))?c=_:u=_,(w=n>=(g=(h+d)/2))?h=g:d=g;while((R=w<<2|T<<1|b)===(v=(S>=g)<<2|(y>=_)<<1|p>=m));return r[v]=a,r[R]=o,i}function Ep(i){Array.isArray(i)||(i=Array.from(i));let t=i.length,e=new Float64Array(t),n=new Float64Array(t),s=new Float64Array(t),r=1/0,a=1/0,o=1/0,l=-1/0,c=-1/0,h=-1/0;for(let f=0,u,d,m,_;f<t;++f)isNaN(d=+this._x.call(null,u=i[f]))||isNaN(m=+this._y.call(null,u))||isNaN(_=+this._z.call(null,u))||(e[f]=d,n[f]=m,s[f]=_,d<r&&(r=d),d>l&&(l=d),m<a&&(a=m),m>c&&(c=m),_<o&&(o=_),_>h&&(h=_));if(r>l||a>c||o>h)return this;this.cover(r,a,o).cover(l,c,h);for(let f=0;f<t;++f)Tp(this,e[f],n[f],s[f],i[f]);return this}function Cp(i,t,e){if(isNaN(i=+i)||isNaN(t=+t)||isNaN(e=+e))return this;var n=this._x0,s=this._y0,r=this._z0,a=this._x1,o=this._y1,l=this._z1;if(isNaN(n))a=(n=Math.floor(i))+1,o=(s=Math.floor(t))+1,l=(r=Math.floor(e))+1;else{for(var c=a-n||1,h=this._root,f,u;n>i||i>=a||s>t||t>=o||r>e||e>=l;)switch(u=(e<r)<<2|(t<s)<<1|i<n,f=new Array(8),f[u]=h,h=f,c*=2,u){case 0:a=n+c,o=s+c,l=r+c;break;case 1:n=a-c,o=s+c,l=r+c;break;case 2:a=n+c,s=o-c,l=r+c;break;case 3:n=a-c,s=o-c,l=r+c;break;case 4:a=n+c,o=s+c,r=l-c;break;case 5:n=a-c,o=s+c,r=l-c;break;case 6:a=n+c,s=o-c,r=l-c;break;case 7:n=a-c,s=o-c,r=l-c;break}this._root&&this._root.length&&(this._root=h)}return this._x0=n,this._y0=s,this._z0=r,this._x1=a,this._y1=o,this._z1=l,this}function Rp(){var i=[];return this.visit(function(t){if(!t.length)do i.push(t.data);while(t=t.next)}),i}function Pp(i){return arguments.length?this.cover(+i[0][0],+i[0][1],+i[0][2]).cover(+i[1][0],+i[1][1],+i[1][2]):isNaN(this._x0)?void 0:[[this._x0,this._y0,this._z0],[this._x1,this._y1,this._z1]]}function Qt(i,t,e,n,s,r,a){this.node=i,this.x0=t,this.y0=e,this.z0=n,this.x1=s,this.y1=r,this.z1=a}function Ip(i,t,e,n){var s,r=this._x0,a=this._y0,o=this._z0,l,c,h,f,u,d,m=this._x1,_=this._y1,g=this._z1,p=[],y=this._root,S,b;for(y&&p.push(new Qt(y,r,a,o,m,_,g)),n==null?n=1/0:(r=i-n,a=t-n,o=e-n,m=i+n,_=t+n,g=e+n,n*=n);S=p.pop();)if(!(!(y=S.node)||(l=S.x0)>m||(c=S.y0)>_||(h=S.z0)>g||(f=S.x1)<r||(u=S.y1)<a||(d=S.z1)<o))if(y.length){var T=(l+f)/2,w=(c+u)/2,R=(h+d)/2;p.push(new Qt(y[7],T,w,R,f,u,d),new Qt(y[6],l,w,R,T,u,d),new Qt(y[5],T,c,R,f,w,d),new Qt(y[4],l,c,R,T,w,d),new Qt(y[3],T,w,h,f,u,R),new Qt(y[2],l,w,h,T,u,R),new Qt(y[1],T,c,h,f,w,R),new Qt(y[0],l,c,h,T,w,R)),(b=(e>=R)<<2|(t>=w)<<1|i>=T)&&(S=p[p.length-1],p[p.length-1]=p[p.length-1-b],p[p.length-1-b]=S)}else{var v=i-+this._x.call(null,y.data),E=t-+this._y.call(null,y.data),L=e-+this._z.call(null,y.data),C=v*v+E*E+L*L;if(C<n){var D=Math.sqrt(n=C);r=i-D,a=t-D,o=e-D,m=i+D,_=t+D,g=e+D,s=y.data}}return s}var eM=(i,t,e,n,s,r)=>Math.sqrt((i-n)**2+(t-s)**2+(e-r)**2);function Lp(i,t,e,n){let s=[],r=i-n,a=t-n,o=e-n,l=i+n,c=t+n,h=e+n;return this.visit((f,u,d,m,_,g,p)=>{if(!f.length)do{let y=f.data;eM(i,t,e,this._x(y),this._y(y),this._z(y))<=n&&s.push(y)}while(f=f.next);return u>l||d>c||m>h||_<r||g<a||p<o}),s}function Np(i){if(isNaN(u=+this._x.call(null,i))||isNaN(d=+this._y.call(null,i))||isNaN(m=+this._z.call(null,i)))return this;var t,e=this._root,n,s,r,a=this._x0,o=this._y0,l=this._z0,c=this._x1,h=this._y1,f=this._z1,u,d,m,_,g,p,y,S,b,T,w;if(!e)return this;if(e.length)for(;;){if((y=u>=(_=(a+c)/2))?a=_:c=_,(S=d>=(g=(o+h)/2))?o=g:h=g,(b=m>=(p=(l+f)/2))?l=p:f=p,t=e,!(e=e[T=b<<2|S<<1|y]))return this;if(!e.length)break;(t[T+1&7]||t[T+2&7]||t[T+3&7]||t[T+4&7]||t[T+5&7]||t[T+6&7]||t[T+7&7])&&(n=t,w=T)}for(;e.data!==i;)if(s=e,!(e=e.next))return this;return(r=e.next)&&delete e.next,s?(r?s.next=r:delete s.next,this):t?(r?t[T]=r:delete t[T],(e=t[0]||t[1]||t[2]||t[3]||t[4]||t[5]||t[6]||t[7])&&e===(t[7]||t[6]||t[5]||t[4]||t[3]||t[2]||t[1]||t[0])&&!e.length&&(n?n[w]=e:this._root=e),this):(this._root=r,this)}function Dp(i){for(var t=0,e=i.length;t<e;++t)this.remove(i[t]);return this}function Fp(){return this._root}function Up(){var i=0;return this.visit(function(t){if(!t.length)do++i;while(t=t.next)}),i}function Op(i){var t=[],e,n=this._root,s,r,a,o,l,c,h;for(n&&t.push(new Qt(n,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1));e=t.pop();)if(!i(n=e.node,r=e.x0,a=e.y0,o=e.z0,l=e.x1,c=e.y1,h=e.z1)&&n.length){var f=(r+l)/2,u=(a+c)/2,d=(o+h)/2;(s=n[7])&&t.push(new Qt(s,f,u,d,l,c,h)),(s=n[6])&&t.push(new Qt(s,r,u,d,f,c,h)),(s=n[5])&&t.push(new Qt(s,f,a,d,l,u,h)),(s=n[4])&&t.push(new Qt(s,r,a,d,f,u,h)),(s=n[3])&&t.push(new Qt(s,f,u,o,l,c,d)),(s=n[2])&&t.push(new Qt(s,r,u,o,f,c,d)),(s=n[1])&&t.push(new Qt(s,f,a,o,l,u,d)),(s=n[0])&&t.push(new Qt(s,r,a,o,f,u,d))}return this}function Bp(i){var t=[],e=[],n;for(this._root&&t.push(new Qt(this._root,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1));n=t.pop();){var s=n.node;if(s.length){var r,a=n.x0,o=n.y0,l=n.z0,c=n.x1,h=n.y1,f=n.z1,u=(a+c)/2,d=(o+h)/2,m=(l+f)/2;(r=s[0])&&t.push(new Qt(r,a,o,l,u,d,m)),(r=s[1])&&t.push(new Qt(r,u,o,l,c,d,m)),(r=s[2])&&t.push(new Qt(r,a,d,l,u,h,m)),(r=s[3])&&t.push(new Qt(r,u,d,l,c,h,m)),(r=s[4])&&t.push(new Qt(r,a,o,m,u,d,f)),(r=s[5])&&t.push(new Qt(r,u,o,m,c,d,f)),(r=s[6])&&t.push(new Qt(r,a,d,m,u,h,f)),(r=s[7])&&t.push(new Qt(r,u,d,m,c,h,f))}e.push(n)}for(;n=e.pop();)i(n.node,n.x0,n.y0,n.z0,n.x1,n.y1,n.z1);return this}function kp(i){return i[0]}function zp(i){return arguments.length?(this._x=i,this):this._x}function Vp(i){return i[1]}function Gp(i){return arguments.length?(this._y=i,this):this._y}function Hp(i){return i[2]}function Wp(i){return arguments.length?(this._z=i,this):this._z}function ea(i,t,e,n){var s=new Vh(t??kp,e??Vp,n??Hp,NaN,NaN,NaN,NaN,NaN,NaN);return i==null?s:s.addAll(i)}function Vh(i,t,e,n,s,r,a,o,l){this._x=i,this._y=t,this._z=e,this._x0=n,this._y0=s,this._z0=r,this._x1=a,this._y1=o,this._z1=l,this._root=void 0}function Xp(i){for(var t={data:i.data},e=t;i=i.next;)e=e.next={data:i.data};return t}var He=ea.prototype=Vh.prototype;He.copy=function(){var i=new Vh(this._x,this._y,this._z,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1),t=this._root,e,n;if(!t)return i;if(!t.length)return i._root=Xp(t),i;for(e=[{source:t,target:i._root=new Array(8)}];t=e.pop();)for(var s=0;s<8;++s)(n=t.source[s])&&(n.length?e.push({source:n,target:t.target[s]=new Array(8)}):t.target[s]=Xp(n));return i};He.add=Ap;He.addAll=Ep;He.cover=Cp;He.data=Rp;He.extent=Pp;He.find=Ip;He.findAllWithinRadius=Lp;He.remove=Np;He.removeAll=Dp;He.root=Fp;He.size=Up;He.visit=Op;He.visitAfter=Bp;He.x=zp;He.y=Gp;He.z=Wp;function ye(i){return function(){return i}}function On(i){return(i()-.5)*1e-6}function nM(i){return i.index}function qp(i,t){var e=i.get(t);if(!e)throw new Error("node not found: "+t);return e}function Gh(i){var t=nM,e=u,n,s=ye(30),r,a,o,l,c,h,f=1;i==null&&(i=[]);function u(p){return 1/Math.min(l[p.source.index],l[p.target.index])}function d(p){for(var y=0,S=i.length;y<f;++y)for(var b=0,T,w,R,v=0,E=0,L=0,C,D;b<S;++b)T=i[b],w=T.source,R=T.target,v=R.x+R.vx-w.x-w.vx||On(h),o>1&&(E=R.y+R.vy-w.y-w.vy||On(h)),o>2&&(L=R.z+R.vz-w.z-w.vz||On(h)),C=Math.sqrt(v*v+E*E+L*L),C=(C-r[b])/C*p*n[b],v*=C,E*=C,L*=C,R.vx-=v*(D=c[b]),o>1&&(R.vy-=E*D),o>2&&(R.vz-=L*D),w.vx+=v*(D=1-D),o>1&&(w.vy+=E*D),o>2&&(w.vz+=L*D)}function m(){if(a){var p,y=a.length,S=i.length,b=new Map(a.map((w,R)=>[t(w,R,a),w])),T;for(p=0,l=new Array(y);p<S;++p)T=i[p],T.index=p,typeof T.source!="object"&&(T.source=qp(b,T.source)),typeof T.target!="object"&&(T.target=qp(b,T.target)),l[T.source.index]=(l[T.source.index]||0)+1,l[T.target.index]=(l[T.target.index]||0)+1;for(p=0,c=new Array(S);p<S;++p)T=i[p],c[p]=l[T.source.index]/(l[T.source.index]+l[T.target.index]);n=new Array(S),_(),r=new Array(S),g()}}function _(){if(a)for(var p=0,y=i.length;p<y;++p)n[p]=+e(i[p],p,i)}function g(){if(a)for(var p=0,y=i.length;p<y;++p)r[p]=+s(i[p],p,i)}return d.initialize=function(p,...y){a=p,h=y.find(S=>typeof S=="function")||Math.random,o=y.find(S=>[1,2,3].includes(S))||2,m()},d.links=function(p){return arguments.length?(i=p,m(),d):i},d.id=function(p){return arguments.length?(t=p,d):t},d.iterations=function(p){return arguments.length?(f=+p,d):f},d.strength=function(p){return arguments.length?(e=typeof p=="function"?p:ye(+p),_(),d):e},d.distance=function(p){return arguments.length?(s=typeof p=="function"?p:ye(+p),g(),d):s},d}var iM={value:()=>{}};function Zp(){for(var i=0,t=arguments.length,e={},n;i<t;++i){if(!(n=arguments[i]+"")||n in e||/[\s.]/.test(n))throw new Error("illegal type: "+n);e[n]=[]}return new Nl(e)}function Nl(i){this._=i}function sM(i,t){return i.trim().split(/^|\s+/).map(function(e){var n="",s=e.indexOf(".");if(s>=0&&(n=e.slice(s+1),e=e.slice(0,s)),e&&!t.hasOwnProperty(e))throw new Error("unknown type: "+e);return{type:e,name:n}})}Nl.prototype=Zp.prototype={constructor:Nl,on:function(i,t){var e=this._,n=sM(i+"",e),s,r=-1,a=n.length;if(arguments.length<2){for(;++r<a;)if((s=(i=n[r]).type)&&(s=rM(e[s],i.name)))return s;return}if(t!=null&&typeof t!="function")throw new Error("invalid callback: "+t);for(;++r<a;)if(s=(i=n[r]).type)e[s]=Yp(e[s],i.name,t);else if(t==null)for(s in e)e[s]=Yp(e[s],i.name,null);return this},copy:function(){var i={},t=this._;for(var e in t)i[e]=t[e].slice();return new Nl(i)},call:function(i,t){if((s=arguments.length-2)>0)for(var e=new Array(s),n=0,s,r;n<s;++n)e[n]=arguments[n+2];if(!this._.hasOwnProperty(i))throw new Error("unknown type: "+i);for(r=this._[i],n=0,s=r.length;n<s;++n)r[n].value.apply(t,e)},apply:function(i,t,e){if(!this._.hasOwnProperty(i))throw new Error("unknown type: "+i);for(var n=this._[i],s=0,r=n.length;s<r;++s)n[s].value.apply(t,e)}};function rM(i,t){for(var e=0,n=i.length,s;e<n;++e)if((s=i[e]).name===t)return s.value}function Yp(i,t,e){for(var n=0,s=i.length;n<s;++n)if(i[n].name===t){i[n]=iM,i=i.slice(0,n).concat(i.slice(n+1));break}return e!=null&&i.push({name:t,value:e}),i}var Hh=Zp;var Ks=0,ia=0,na=0,Jp=1e3,Dl,sa,Fl=0,hs=0,Ul=0,ra=typeof performance=="object"&&performance.now?performance:Date,$p=typeof window=="object"&&window.requestAnimationFrame?window.requestAnimationFrame.bind(window):function(i){setTimeout(i,17)};function qh(){return hs||($p(aM),hs=ra.now()+Ul)}function aM(){hs=0}function Wh(){this._call=this._time=this._next=null}Wh.prototype=Ol.prototype={constructor:Wh,restart:function(i,t,e){if(typeof i!="function")throw new TypeError("callback is not a function");e=(e==null?qh():+e)+(t==null?0:+t),!this._next&&sa!==this&&(sa?sa._next=this:Dl=this,sa=this),this._call=i,this._time=e,Xh()},stop:function(){this._call&&(this._call=null,this._time=1/0,Xh())}};function Ol(i,t,e){var n=new Wh;return n.restart(i,t,e),n}function jp(){qh(),++Ks;for(var i=Dl,t;i;)(t=hs-i._time)>=0&&i._call.call(void 0,t),i=i._next;--Ks}function Kp(){hs=(Fl=ra.now())+Ul,Ks=ia=0;try{jp()}finally{Ks=0,lM(),hs=0}}function oM(){var i=ra.now(),t=i-Fl;t>Jp&&(Ul-=t,Fl=i)}function lM(){for(var i,t=Dl,e,n=1/0;t;)t._call?(n>t._time&&(n=t._time),i=t,t=t._next):(e=t._next,t._next=null,t=i?i._next=e:Dl=e);sa=i,Xh(n)}function Xh(i){if(!Ks){ia&&(ia=clearTimeout(ia));var t=i-hs;t>24?(i<1/0&&(ia=setTimeout(Kp,i-ra.now()-Ul)),na&&(na=clearInterval(na))):(na||(Fl=ra.now(),na=setInterval(oM,Jp)),Ks=1,$p(Kp))}}function Qp(){let i=1;return()=>(i=(1664525*i+1013904223)%4294967296)/4294967296}var tm=3;function Bl(i){return i.x}function Yh(i){return i.y}function em(i){return i.z}var cM=10,hM=Math.PI*(3-Math.sqrt(5)),uM=Math.PI*20/(9+Math.sqrt(221));function Zh(i,t){t=t||2;var e=Math.min(tm,Math.max(1,Math.round(t))),n,s=1,r=.001,a=1-Math.pow(r,1/300),o=0,l=.6,c=new Map,h=Ol(d),f=Hh("tick","end"),u=Qp();i==null&&(i=[]);function d(){m(),f.call("tick",n),s<r&&(h.stop(),f.call("end",n))}function m(p){var y,S=i.length,b;p===void 0&&(p=1);for(var T=0;T<p;++T)for(s+=(o-s)*a,c.forEach(function(w){w(s)}),y=0;y<S;++y)b=i[y],b.fx==null?b.x+=b.vx*=l:(b.x=b.fx,b.vx=0),e>1&&(b.fy==null?b.y+=b.vy*=l:(b.y=b.fy,b.vy=0)),e>2&&(b.fz==null?b.z+=b.vz*=l:(b.z=b.fz,b.vz=0));return n}function _(){for(var p=0,y=i.length,S;p<y;++p){if(S=i[p],S.index=p,S.fx!=null&&(S.x=S.fx),S.fy!=null&&(S.y=S.fy),S.fz!=null&&(S.z=S.fz),isNaN(S.x)||e>1&&isNaN(S.y)||e>2&&isNaN(S.z)){var b=cM*(e>2?Math.cbrt(.5+p):e>1?Math.sqrt(.5+p):p),T=p*hM,w=p*uM;e===1?S.x=b:e===2?(S.x=b*Math.cos(T),S.y=b*Math.sin(T)):(S.x=b*Math.sin(T)*Math.cos(w),S.y=b*Math.cos(T),S.z=b*Math.sin(T)*Math.sin(w))}(isNaN(S.vx)||e>1&&isNaN(S.vy)||e>2&&isNaN(S.vz))&&(S.vx=0,e>1&&(S.vy=0),e>2&&(S.vz=0))}}function g(p){return p.initialize&&p.initialize(i,u,e),p}return _(),n={tick:m,restart:function(){return h.restart(d),n},stop:function(){return h.stop(),n},numDimensions:function(p){return arguments.length?(e=Math.min(tm,Math.max(1,Math.round(p))),c.forEach(g),n):e},nodes:function(p){return arguments.length?(i=p,_(),c.forEach(g),n):i},alpha:function(p){return arguments.length?(s=+p,n):s},alphaMin:function(p){return arguments.length?(r=+p,n):r},alphaDecay:function(p){return arguments.length?(a=+p,n):+a},alphaTarget:function(p){return arguments.length?(o=+p,n):o},velocityDecay:function(p){return arguments.length?(l=1-p,n):1-l},randomSource:function(p){return arguments.length?(u=p,c.forEach(g),n):u},force:function(p,y){return arguments.length>1?(y==null?c.delete(p):c.set(p,g(y)),n):c.get(p)},find:function(){var p=Array.prototype.slice.call(arguments),y=p.shift()||0,S=(e>1?p.shift():null)||0,b=(e>2?p.shift():null)||0,T=p.shift()||1/0,w=0,R=i.length,v,E,L,C,D,H;for(T*=T,w=0;w<R;++w)D=i[w],v=y-D.x,E=S-(D.y||0),L=b-(D.z||0),C=v*v+E*E+L*L,C<T&&(H=D,T=C);return H},on:function(p,y){return arguments.length>1?(f.on(p,y),n):f.on(p)}}}function Kh(){var i,t,e,n,s,r=ye(-30),a,o=1,l=1/0,c=.81;function h(m){var _,g=i.length,p=(t===1?Qr(i,Bl):t===2?ta(i,Bl,Yh):t===3?ea(i,Bl,Yh,em):null).visitAfter(u);for(s=m,_=0;_<g;++_)e=i[_],p.visit(d)}function f(){if(i){var m,_=i.length,g;for(a=new Array(_),m=0;m<_;++m)g=i[m],a[g.index]=+r(g,m,i)}}function u(m){var _=0,g,p,y=0,S,b,T,w,R=m.length;if(R){for(S=b=T=w=0;w<R;++w)(g=m[w])&&(p=Math.abs(g.value))&&(_+=g.value,y+=p,S+=p*(g.x||0),b+=p*(g.y||0),T+=p*(g.z||0));_*=Math.sqrt(4/R),m.x=S/y,t>1&&(m.y=b/y),t>2&&(m.z=T/y)}else{g=m,g.x=g.data.x,t>1&&(g.y=g.data.y),t>2&&(g.z=g.data.z);do _+=a[g.data.index];while(g=g.next)}m.value=_}function d(m,_,g,p,y){if(!m.value)return!0;var S=[g,p,y][t-1],b=m.x-e.x,T=t>1?m.y-e.y:0,w=t>2?m.z-e.z:0,R=S-_,v=b*b+T*T+w*w;if(R*R/c<v)return v<l&&(b===0&&(b=On(n),v+=b*b),t>1&&T===0&&(T=On(n),v+=T*T),t>2&&w===0&&(w=On(n),v+=w*w),v<o&&(v=Math.sqrt(o*v)),e.vx+=b*m.value*s/v,t>1&&(e.vy+=T*m.value*s/v),t>2&&(e.vz+=w*m.value*s/v)),!0;if(m.length||v>=l)return;(m.data!==e||m.next)&&(b===0&&(b=On(n),v+=b*b),t>1&&T===0&&(T=On(n),v+=T*T),t>2&&w===0&&(w=On(n),v+=w*w),v<o&&(v=Math.sqrt(o*v)));do m.data!==e&&(R=a[m.data.index]*s/v,e.vx+=b*R,t>1&&(e.vy+=T*R),t>2&&(e.vz+=w*R));while(m=m.next)}return h.initialize=function(m,..._){i=m,n=_.find(g=>typeof g=="function")||Math.random,t=_.find(g=>[1,2,3].includes(g))||2,f()},h.strength=function(m){return arguments.length?(r=typeof m=="function"?m:ye(+m),f(),h):r},h.distanceMin=function(m){return arguments.length?(o=m*m,h):Math.sqrt(o)},h.distanceMax=function(m){return arguments.length?(l=m*m,h):Math.sqrt(l)},h.theta=function(m){return arguments.length?(c=m*m,h):Math.sqrt(c)},h}function Jh(i){var t=ye(.1),e,n,s;typeof i!="function"&&(i=ye(i==null?0:+i));function r(o){for(var l=0,c=e.length,h;l<c;++l)h=e[l],h.vx+=(s[l]-h.x)*n[l]*o}function a(){if(e){var o,l=e.length;for(n=new Array(l),s=new Array(l),o=0;o<l;++o)n[o]=isNaN(s[o]=+i(e[o],o,e))?0:+t(e[o],o,e)}}return r.initialize=function(o){e=o,a()},r.strength=function(o){return arguments.length?(t=typeof o=="function"?o:ye(+o),a(),r):t},r.x=function(o){return arguments.length?(i=typeof o=="function"?o:ye(+o),a(),r):i},r}function $h(i){var t=ye(.1),e,n,s;typeof i!="function"&&(i=ye(i==null?0:+i));function r(o){for(var l=0,c=e.length,h;l<c;++l)h=e[l],h.vy+=(s[l]-h.y)*n[l]*o}function a(){if(e){var o,l=e.length;for(n=new Array(l),s=new Array(l),o=0;o<l;++o)n[o]=isNaN(s[o]=+i(e[o],o,e))?0:+t(e[o],o,e)}}return r.initialize=function(o){e=o,a()},r.strength=function(o){return arguments.length?(t=typeof o=="function"?o:ye(+o),a(),r):t},r.y=function(o){return arguments.length?(i=typeof o=="function"?o:ye(+o),a(),r):i},r}function jh(i){var t=ye(.1),e,n,s;typeof i!="function"&&(i=ye(i==null?0:+i));function r(o){for(var l=0,c=e.length,h;l<c;++l)h=e[l],h.vz+=(s[l]-h.z)*n[l]*o}function a(){if(e){var o,l=e.length;for(n=new Array(l),s=new Array(l),o=0;o<l;++o)n[o]=isNaN(s[o]=+i(e[o],o,e))?0:+t(e[o],o,e)}}return r.initialize=function(o){e=o,a()},r.strength=function(o){return arguments.length?(t=typeof o=="function"?o:ye(+o),a(),r):t},r.z=function(o){return arguments.length?(i=typeof o=="function"?o:ye(+o),a(),r):i},r}function Qh(i,t){let e=[],n=1,s=r=>{if(i!==0)for(let a of e){let o=a.x??0,l=a.z??0,c=Math.hypot(o,l);if(c<1e-4)continue;let h=Math.min(Math.max((t[a.index??0]||1)/n,.3),3),f=i*h*r*c/200;a.vx=(a.vx??0)-o/c*f,a.vz=(a.vz??0)-l/c*f}};return s.initialize=r=>{e=r;let a=0;for(let o of r)a+=t[o.index??0]||1;n=r.length?a/r.length:1},s}function tu(i){let t=[],e=n=>{if(i!==0)for(let s of t){let r=s.x??0,a=s.z??0,o=Math.hypot(r,a);if(o<.001)continue;let l=1/(1+o/160),c=i*n*l;s.vx=(s.vx??0)+-a/o*c*o,s.vz=(s.vz??0)+r/o*c*o}};return e.initialize=n=>{t=n},e}var Js=class{constructor(){q(this,"positions",new Float32Array(0));q(this,"sim",null);q(this,"simNodes",[]);q(this,"degrees",[]);q(this,"settled",!0);q(this,"_ticks",0)}get ticks(){return this._ticks}init(t,e,n,s=1){this.dispose(),this.positions=e,this.degrees=t.nodes.map(a=>Math.max(a.degree,1)),this.simNodes=t.nodes.map((a,o)=>({x:e[o*3]??0,y:e[o*3+1]??0,z:e[o*3+2]??0}));let r=t.links.map(a=>({source:a.source,target:a.target}));this.sim=Zh(this.simNodes,3).alphaDecay(1-Math.pow(.001,1/300)).velocityDecay(n.velocityDecay).force("link",Gh(r).distance(n.linkDistance).strength(this.linkStrengthFn(n.linkStrength))).force("charge",Kh().strength(n.charge).distanceMax(800)).force("x",Jh(0).strength(n.centerPull)).force("y",$h(0).strength(n.centerPull+n.flatten)).force("z",jh(0).strength(n.centerPull)).force("core",Qh(n.coreGravity,this.degrees)).force("spiral",tu(n.spiral)).stop(),this.sim.alpha(s),this._ticks=0,this.settled=!1}linkStrengthFn(t){let e=this.degrees;return n=>{let s=typeof n.source=="number"?n.source:n.source.index??0,r=typeof n.target=="number"?n.target:n.target.index??0,a=1/Math.min(e[s]??1,e[r]??1);return Math.min(a*t,1)}}updateParams(t){let e=this.sim;if(!e)return;e.force("charge")?.strength(t.charge);let n=e.force("link");n?.distance(t.linkDistance),n?.strength(this.linkStrengthFn(t.linkStrength)),e.force("x")?.strength(t.centerPull),e.force("y")?.strength(t.centerPull+t.flatten),e.force("z")?.strength(t.centerPull),e.force("core",Qh(t.coreGravity,this.degrees)),e.force("spiral",tu(t.spiral)),this.reheat(.5)}step(){let t=this.sim;if(!t||this.settled)return!1;t.tick(),this._ticks++;let e=this.positions,n=this.simNodes;for(let s=0;s<n.length;s++){let r=n[s];r&&(e[s*3]=r.x,e[s*3+1]=r.y,e[s*3+2]=r.z)}return t.alpha()<t.alphaMin()&&(this.settled=!0),!this.settled}isSettled(){return this.settled}reheat(t=.3){this.sim&&(this.sim.alpha(Math.max(this.sim.alpha(),t)),this.settled=!1)}dispose(){this.sim?.stop(),this.sim=null,this.simNodes=[],this.settled=!0}};function nm(i){let t=i.nodes.length,e=i.links.length,n=new Int32Array(t+1);for(let o of i.links)n[o.source+1]=(n[o.source+1]??0)+1,n[o.target+1]=(n[o.target+1]??0)+1;for(let o=0;o<t;o++)n[o+1]=(n[o+1]??0)+(n[o]??0);let s=new Int32Array(2*e),r=new Int32Array(2*e),a=new Int32Array(t);for(let o=0;o<t;o++)a[o]=n[o]??0;for(let o=0;o<e;o++){let l=i.links[o];if(!l)continue;let c=l.source,h=l.target,f=a[c]??0;s[f]=h,r[f]=o,a[c]=f+1;let u=a[h]??0;s[u]=c,r[u]=o,a[h]=u+1}return{offset:n,neighbor:s,linkOf:r}}function eu(i,t,e){let n=new Map([[t,0]]),s=[],r=[],a=[t];for(let o=1;o<=e;o++){let l=[];for(let c of a){let h=i.offset[c]??0,f=i.offset[c+1]??0;for(let u=h;u<f;u++){let d=i.neighbor[u]??0,m=i.linkOf[u]??0,_=n.get(d);o===1?s.push(m):(_===void 0||_===2)&&r.push(m),_===void 0&&(n.set(d,o),o<e&&l.push(d))}}a=l}return{depthOf:n,linkTier1:s,linkTier2:r}}var ot=i=>document.getElementById(i),tn=new URLSearchParams(location.search),ql=86400,En={bloom:{strength:.35,radius:.35,threshold:.22},linkOpacity:.16,linkCurve:.35,twinkle:.5,nodeSize:1.35,space:{nebula:.35,fieldStars:.25,clusterClouds:.3},frameElevDeg:50},iu={charge:-170,linkDistance:55,linkStrength:1.1,centerPull:.05,flatten:.55,coreGravity:.1,spiral:.02,velocityDecay:.6},Hi={lit:1,near:1,rest:.12,turnRest:.07},ps={window:"窗口",person:"人",memory:"记忆",event:"事件",note:"本子"},tr={link:"联想",origin:"出处",about:"跟谁有关",impression:"印象"},Kn=[{key:"social",name:"想说话",c:"#ff8a1f"},{key:"curiosity",name:"好奇",c:"#54c08b"},{key:"boredom",name:"无聊",c:"#9a958c"},{key:"seen",name:"想被看见",c:"#f2c14e"},{key:"talked",name:"说多了",c:"#9b7bf6"},{key:"stress",name:"压力",c:"#e5533d"},{key:"valence",name:"心情",c:"#5b8def"}],im=[28,200,120,330,50,170,280,90,0,230,150,300],$n=new dt("#efe7d2"),ou=new dt("#ffc861"),lu=new dt("#7d7f88"),cn=null,er="sample",fs=null,us=null,Te=new Map,$s=new Map,Ee={nodes:[],links:[]},Je=new Map,cu=null,en=[],Hl=new Map,Nt=null,hn=null,Me=null,Qs=80,nr=300,ds=$r.high,aa={},kl=null,Jt={kinds:new Set(Object.keys(ps)),edges:new Set(Object.keys(tr)),win:"",vis:"all",from:24,to:0},ce=-1,Pe=-1,hu=0,qi=null,hm=-1,su=-1,ze=!0,ms=!0,Yl=!1,ru=!1,Yi=new Map,Wl=new Map;function fM(){let i=null;try{i=window.AstrBotPluginView||window.AstrBotPluginPage||window.astrbotPluginView||null}catch{i=null}try{!i&&window.parent&&window.parent!==window&&(i=window.parent.AstrBotPluginView||window.parent.AstrBotPluginPage||null)}catch{i=null}let t=!1;try{t=!!(window.parent&&window.parent!==window)}catch{t=!1}return i&&t?i:null}var uu=i=>i&&i.data!==void 0?i.data:i;async function dM(){if(us=fM(),us)try{let i=await Promise.race([us.ready(),new Promise(e=>setTimeout(()=>e(null),3e3))]);!tn.get("theme")&&!_u("bio_theme")&&i&&(ms=!!i.isDark);let t=uu(await Promise.race([us.apiGet("page/brain",{}),new Promise((e,n)=>setTimeout(()=>n(new Error("timeout")),8e3))]));if(t&&Array.isArray(t.nodes))return er="live",t}catch{}return fs=window.BrainSample.make({n:Number(tn.get("n"))||900}),er=us?"sample-embedded":"sample",fs.graph}async function pM(i){if(er==="live")try{return uu(await us.apiGet("page/brain/node",{id:i}))}catch(t){return{error:"没取到："+(t&&t.message||t)}}return fs&&fs.details[i]||null}async function mM(i){if(er==="live")try{let e=uu(await us.apiGet("page/brain/search",{q:i}));return Array.isArray(e)?e:e&&e.ids||[]}catch{return[]}let t=[];if(!fs)return t;for(let e in fs.details){let n=fs.details[e];((n.text||"").includes(i)||(n.title||"").includes(i))&&t.push(e)}return t}function gM(i){cn=i,aa=Object.assign({},i.body||{}),Te=new Map;for(let r of i.nodes||[])r&&r.id&&ps[r.kind]&&!Te.has(r.id)&&Te.set(r.id,r);cn.edges=(i.edges||[]).filter(r=>tr[r.kind]&&Te.has(r.s)&&Te.has(r.t)&&r.s!==r.t),cn.turns=i.turns||[],$s=new Map;for(let r of cn.edges)($s.get(r.s)||$s.set(r.s,[]).get(r.s)).push({other:r.t,kind:r.kind,w:Number(r.w)||1}),($s.get(r.t)||$s.set(r.t,[]).get(r.t)).push({other:r.s,kind:r.kind,w:Number(r.w)||1});let t=[...Te.values()].filter(r=>r.kind==="window"&&r.sub!=="private").sort((r,a)=>(a.w||0)-(r.w||0)),e=[...Te.values()].filter(r=>r.kind==="window"&&r.sub==="private");t.forEach((r,a)=>Yi.set(r.id,new dt().setHSL(im[a%im.length]/360,.66,.6))),e.forEach((r,a)=>Yi.set(r.id,new dt().setHSL((236+a*11%44)/360,.32,.74)));let n=i.now||Date.now()/1e3,s=1;for(let r of Te.values())r.ts&&(s=Math.max(s,Math.ceil((n-r.ts)/ql)));Jt.from=s,Jt.to=0;for(let r of["tFrom","tTo"])ot(r).max=String(s)}function _M(i){if(!Jt.kinds.has(i.kind))return!1;if(Jt.vis!=="all"){if(i.kind==="window"){if(i.sub==="private"!=(Jt.vis==="private"))return!1}else if(i.vis&&i.vis!==Jt.vis)return!1}if(i.ts&&i.kind!=="person"&&i.kind!=="window"){let t=((cn.now||Date.now()/1e3)-i.ts)/ql;if(t>Jt.from+1e-4||t<Jt.to-1e-4)return!1}return!0}function xM(){if(!Me)return;let i=Me.positions;Ee.nodes.forEach((t,e)=>Hl.set(t.id,[i[e*3],i[e*3+1],i[e*3+2]]))}function um(i){xM();let t=[...Te.values()].filter(_M);if(ds.nodeCap&&t.length>ds.nodeCap){let a=t.filter(l=>l.kind==="window"||l.kind==="person"),o=t.filter(l=>l.kind!=="window"&&l.kind!=="person").sort((l,c)=>(c.w||0)-(l.w||0));t=a.concat(o.slice(0,Math.max(0,ds.nodeCap-a.length)))}en=t,Je=new Map(t.map((a,o)=>[a.id,o]));let e=t.map(a=>({id:a.id,name:a.label||a.id,folderTop:a.where||a.id,degree:0,inDegree:0,outDegree:0,fileSize:0,tags:[],unresolved:a.vis==="private"&&a.kind!=="window",tag:!1})),n=[];for(let a of cn.edges){if(!Jt.edges.has(a.kind))continue;let o=Je.get(a.s),l=Je.get(a.t);o===void 0||l===void 0||(n.push({source:o,target:l,kind:a.kind}),e[o].degree++,e[l].degree++,e[o].outDegree++,e[l].inDegree++)}Ee={nodes:e,links:n},cu=nm(Ee);let s=bd(e.length),r=new Float32Array(e.length*3);t.forEach((a,o)=>{let l=Hl.get(a.id);if(!l){let c=Md(a.id,s),h=a.where&&Hl.get(a.where);l=h?[h[0]+c[0]*.25,h[1]+c[1]*.25,h[2]+c[2]*.25]:c}r.set(l,o*3)}),i&&(Qs=s*1.6),Nt||bM(),Nt.setData(Ee,r),vM(Ee,r,i?1:Hl.size?.3:1),ce=-1,hm=-1,Zl(),Zi(),MM()}function vM(i,t,e){Me?.dispose();let n=tn.get("settle")==="1";try{Me=n?new Js:new Zs,Me.init(i,t,iu,e)}catch{Me=new Js,Me.init(i,t,iu,e)}if(n){for(;Me.step(););Nt.updatePositions()}fm=performance.now()}var fm=0;function yM(i){if(!(Me instanceof Zs)||Me.ticks>0||Me.isSettled()||i-fm<2e3)return;let t=Me.positions;Me.dispose(),Me=new Js,Me.init(Ee,t,iu,1)}function dm(i){let t=Wl.get(i.id);if(t)return t;let e=Te.get(i.id);if(!e||e.kind==="person")return $n;let n=Yi.get(e.kind==="window"?e.id:e.where)||Yi.values().next().value||$n;return e.kind==="event"?n.clone().offsetHSL(0,.05,.08):e.kind==="note"?n.clone().offsetHSL(0,-.1,.16):n}function Zl(){Nt.setColorFn(dm),Nt.recolor()}function pm(i){let t=new Set,e=Je.get(i);if(e===void 0)return t;t.add(e);for(let n=0;n<en.length;n++)en[n].where===i&&t.add(n);return Ee.links.forEach(n=>{n.kind==="impression"&&(n.source===e||n.target===e)&&t.add(n.source===e?n.target:n.source),n.kind==="about"&&en[n.source].where===i&&t.add(n.target)}),t}function Zi(){if(!Nt)return;if(Pe>=0){vm(performance.now(),!0);return}let i=null,t=[];if(ce>=0){let e=eu(cu,ce,1);i=n=>e.depthOf.has(n)?Hi.lit:Hi.rest,t=e.linkTier1}else if(qi)i=e=>qi.has(e)?Hi.lit:Hi.rest;else if(Jt.win){let e=pm(Jt.win);i=s=>e.has(s)?Hi.lit:Hi.rest;let n=Je.get(Jt.win);Ee.links.forEach((s,r)=>{(s.source===n||s.target===n)&&t.push(r)})}Nt.setFocus(i),Nt.setSelectedLinks(t,[])}function MM(){ot("statLine").textContent="显示 "+Ee.nodes.length+" / "+Te.size+" 颗星 · "+Ee.links.length+" 条线"}function bM(){let i=ot("galaxy");Nt=new Rl(i,Qs),hn=new Ll(Nt.camera,Nt.renderer.domElement,{onFlyToSelected:()=>{ce>=0&&hn.flyTo(pi(ce),Nt.nodeRadius(ce))},onResetView:()=>oa()}),hn.setFramingElev(En.frameElevDeg),Nt.setBloomParams(En.bloom),Nt.setNodeScale(En.nodeSize),Nt.setLinkOpacity(En.linkOpacity),Nt.setLinkCurve(En.linkCurve),Nt.setSizeMode("degree"),Nt.setStarfieldEnabled(!0),Nt.setNebulaTint("#46d4dc","#9a7fe0"),Nt.setSpace(En.space),Nt.twinkleFreq=ze?En.twinkle:0,Nt.applyTier(ds,En.bloom.strength),Nt.applyTokens(ms?jr:Nh,En.bloom.strength),Ki.build(),gs.build(),du.build()}var Jn=new P,mm=[],pi=(i,t=new P)=>Nt.nodePosition(i,t);function gm(){let i=Ee.nodes.length;if(!i)return{center:new P,radius:Qs};let t=new P;for(let s=0;s<i;s++)t.add(pi(s,Jn));t.divideScalar(i);let e=new Float64Array(i);for(let s=0;s<i;s++)e[s]=pi(s,Jn).distanceTo(t);e.sort();let n=Math.max(e[Math.min(i-1,Math.floor(i*.95))]||Qs,Qs*.3);return nr=n,{center:t,radius:n}}function oa(){let i=gm();hn.resetView(i.center,i.radius*.8,()=>hn.beginFocusOrbit(null))}function _m(i){if(!i.length)return;let t=new P;for(let s of i)t.add(pi(s,Jn));t.divideScalar(i.length);let e=i.map(s=>pi(s,Jn).distanceTo(t)).sort((s,r)=>s-r),n=e[Math.min(e.length-1,Math.floor(e.length*.85))]||0;hn.resetView(t,Math.max(n*.75,nr*.12),()=>hn.beginFocusOrbit(null))}function xm(){let i=ot("galaxy");Nt?.resize(i.clientWidth,i.clientHeight),zl=i.clientHeight*(Nt?Nt.renderer.getPixelRatio():1)/(2*Math.tan((Nt?Nt.camera.fov:60)/2*Math.PI/180)),Ki.setPixelScale(zl),gs.setPixelScale(zl),du.setPixelScale(zl)}var zl=1,SM=`
attribute float aSize; attribute float aAlpha; attribute vec3 aColor;
varying float vAlpha; varying vec3 vColor; uniform float uPixelScale;
void main() { vAlpha = aAlpha; vColor = aColor;
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	gl_PointSize = min(aSize * uPixelScale / max(-mv.z, 1.0), 220.0);
	gl_Position = projectionMatrix * mv; }`,wM=`
varying float vAlpha; varying vec3 vColor; uniform float uLight;
void main() { float d = length(gl_PointCoord - 0.5);
	float halo = smoothstep(0.5, 0.0, d); float core = smoothstep(0.16, 0.0, d);
	float a = (halo * halo * 0.9 + core) * vAlpha; if (a < 0.01) discard;
	if (uLight > 0.5) { gl_FragColor = vec4(mix(vColor, vColor * 0.7, core), min(a, 1.0)); return; }   // on paper: plain ink
	vec3 col = mix(vColor, vec3(1.0), core * 0.7);
	gl_FragColor = vec4(col * a, a); }`;function fu(i){let t=new te;t.setAttribute("position",new Lt(new Float32Array(i*3),3).setUsage(ki)),t.setAttribute("aSize",new Lt(new Float32Array(i),1).setUsage(ki)),t.setAttribute("aAlpha",new Lt(new Float32Array(i),1).setUsage(ki)),t.setAttribute("aColor",new Lt(new Float32Array(i*3),3).setUsage(ki));let e=new re({vertexShader:SM,fragmentShader:wM,transparent:!0,depthWrite:!1,blending:ms?Dn:Gn,uniforms:{uPixelScale:{value:1},uLight:{value:ms?0:1}}}),n=new an(t,e);return mm.push(e),n.frustumCulled=!1,n.renderOrder=3,Nt.scene.add(n),n}var Ki={pts:null,pos:[],build(){this.pts=fu(Kn.length);let i=this.pts.geometry.getAttribute("aColor");Kn.forEach((t,e)=>{let n=new dt(t.c);i.setXYZ(e,n.r,n.g,n.b),this.pos.push(new P)})},setPixelScale(i){this.pts&&(this.pts.material.uniforms.uPixelScale.value=i)},value(i){let t=Number(aa[Kn[i].key]);return Number.isFinite(t)||(t=0),Kn[i].key==="valence"?t:Math.max(0,Math.min(1,t))},update(i){if(!this.pts)return;let t=this.pts.geometry,e=t.getAttribute("position"),n=t.getAttribute("aSize"),s=t.getAttribute("aAlpha"),r=t.getAttribute("aColor"),a=nr*.24;Kn.forEach((o,l)=>{let c=l/Kn.length*Math.PI*2;this.pos[l].set(Math.cos(c)*a,0,Math.sin(c)*a),e.setXYZ(l,this.pos[l].x,0,this.pos[l].z);let h=this.value(l);if(o.key==="valence"){let u=new dt(h>=0?"#f2c14e":"#5b8def");r.setXYZ(l,u.r,u.g,u.b),h=Math.min(1,Math.abs(h))}let f=ze?1+Math.sin(i/1e3*(.8+h*1.6)+l)*(.05+h*.08):1;n.setX(l,nr*(.08+h*.16)*f),s.setX(l,(ms?.35:.55)+h*.65)}),e.needsUpdate=n.needsUpdate=s.needsUpdate=r.needsUpdate=!0}},du={pts:null,max:48,build(){this.pts=fu(this.max)},setPixelScale(i){this.pts&&(this.pts.material.uniforms.uPixelScale.value=i)},update(i){if(!this.pts)return;let t=this.pts.geometry,e=t.getAttribute("position"),n=t.getAttribute("aSize"),s=t.getAttribute("aAlpha"),r=t.getAttribute("aColor"),a=[];if(Pe>=0){let{rec:o,held:l}=jl(),c=(o.length+3)*Wi+2200,h=ze?(i-hu)%c:c;o.forEach((f,u)=>{if(h<u*Wi)return;let d=ze?Math.max(0,1-(h-u*Wi)/900):0;a.push([f,ou,.05*(1+d*1.6),.9])}),l.forEach(f=>a.push([f,lu,.04,.55]))}else if(ce>=0&&a.push([ce,new dt(1,1,1),.045*(ze?1+Math.sin(i/300)*.12:1),.7]),qi)for(let o of qi){if(a.length>=this.max)break;a.push([o,new dt("#ffb14d"),.03,.6])}for(let o=0;o<this.max;o++){let l=a[o];if(!l){s.setX(o,0);continue}pi(l[0],Jn),e.setXYZ(o,Jn.x,Jn.y,Jn.z),n.setX(o,nr*l[2]),s.setX(o,l[3]),r.setXYZ(o,l[1].r,l[1].g,l[1].b)}e.needsUpdate=n.needsUpdate=s.needsUpdate=r.needsUpdate=!0}},gs={pts:null,list:[],max:64,build(){this.pts=fu(this.max)},setPixelScale(i){this.pts&&(this.pts.material.uniforms.uPixelScale.value=i)},emit(i,t,e,n,s){this.list.length<this.max&&this.list.push({a:i,b:t,color:e,t0:performance.now(),dur:n,big:s})},ambient(i){if(!(!ze||Pe>=0||!Ee.links.length||this.list.length>24||Math.random()>.3))for(let t=0;t<6;t++){let e=Ee.links[Math.floor(Math.random()*Ee.links.length)];if(e.kind!=="link"&&Math.random()<.75||ce>=0&&e.source!==ce&&e.target!==ce)continue;let n=Math.random()<.5,s=dm(Ee.nodes[n?e.source:e.target]).clone().lerp(new dt(1,1,1),.35);this.emit(n?e.source:e.target,n?e.target:e.source,s,1300+Math.random()*1200,!1);break}},update(i){if(!this.pts)return;this.list=this.list.filter(l=>i-l.t0<l.dur&&l.a<Ee.nodes.length&&l.b<Ee.nodes.length);let t=this.pts.geometry,e=t.getAttribute("position"),n=t.getAttribute("aSize"),s=t.getAttribute("aAlpha"),r=t.getAttribute("aColor"),a=new P,o=new P;for(let l=0;l<this.max;l++){let c=this.list[l];if(!c){s.setX(l,0);continue}let h=Math.max(0,Math.min(1,(i-c.t0)/c.dur));AM(pi(c.a,a),pi(c.b,o),h,e,l),n.setX(l,nr*(c.big?.03:.016)),s.setX(l,Math.sin(h*Math.PI)*(c.big?1:.8)),r.setXYZ(l,c.color.r,c.color.g,c.color.b)}e.needsUpdate=n.needsUpdate=s.needsUpdate=r.needsUpdate=!0}};function AM(i,t,e,n,s){let r=(i.x+t.x)/2,a=(i.y+t.y)/2,o=(i.z+t.z)/2,l=i.distanceTo(t),c=Math.hypot(r,a,o)||1,h=En.linkCurve*.32*l,f=r+r/c*h,u=a+a/c*h,d=o+o/c*h,m=(1-e)*(1-e),_=2*(1-e)*e,g=e*e;n.setXYZ(s,m*i.x+_*f+g*t.x,m*i.y+_*u+g*t.y,m*i.z+_*d+g*t.z)}var Wi=600,Kl=-1;function jl(){let i=cn.turns[Pe],t=(i.recalled||[]).map(s=>Je.get(s)).filter(s=>s!==void 0),e=(i.held||[]).map(s=>Je.get(s)).filter(s=>s!==void 0),n=(i.path||[]).map(s=>[Je.get(s[0]),Je.get(s[1])]).filter(s=>s[0]!==void 0&&s[1]!==void 0);return{tr:i,rec:t,held:e,path:n,where:Je.get(i.where)}}function vm(i,t){if(Pe<0)return;let{rec:e,held:n,path:s,where:r}=jl(),a=(e.length+3)*Wi+2200,o=ze?(i-hu)%a:a,l=Math.min(e.length,Math.floor(o/Wi)+1);if(l!==Kl||t){Kl=l;let c=new Set(e.slice(0,l)),h=new Set(n);Nt.setFocus(d=>c.has(d)||d===r?Hi.lit:h.has(d)?.9:Hi.turnRest);let f=new Set(s.map(([d,m])=>d+":"+m).concat(s.map(([d,m])=>m+":"+d))),u=[];Ee.links.forEach((d,m)=>{f.has(d.source+":"+d.target)&&u.push(m)}),Nt.setSelectedLinks(u,[])}ze&&s.forEach(([c,h],f)=>{let u=(f+.5)*Wi;o>=u&&o-u<40&&!gs.list.some(d=>d.a===c&&d.b===h&&i-d.t0<Wi)&&gs.emit(c,h,n.includes(h)?lu:ou,Wi*1.4,!0)})}function Xi(i){let t=cn.turns||[];if(i>=t.length&&(i=t.length-1),i>=0&&Pe<0&&(kl=aa),i<0&&Pe>=0&&kl&&(aa=kl),Pe=i,Wl=new Map,i>=0){ce=-1,ot("drawer").hidden=!0;let{tr:n,rec:s,held:r,where:a}=jl();for(let l of s)Wl.set(Ee.nodes[l].id,ou);for(let l of r)Wl.set(Ee.nodes[l].id,lu);n.body&&(aa=Object.assign({},kl,n.body)),hu=performance.now(),Kl=-1,gs.list=[];let o=(n.recalled||[]).length+(n.held||[]).length-s.length-r.length;ot("turnHint").textContent=pu(n.ts)+" 在"+Ji(n.where)+"：想起 "+(n.recalled||[]).length+" 条（金色，按顺序亮），"+((n.held||[]).length?(n.held||[]).length+" 条她知道但在这里没说（灰的）。":"没有被挡下的。")+(n.body?" 中间的核是那一刻的身体。":"")+(o?"（有 "+o+" 条被筛掉了）":""),Zl(),_m(s.concat(r,a===void 0?[]:[a]))}else ot("turnHint").textContent="点一轮看她这次想起了谁。金色的是想起的，灰的是她知道、但在这里没说的。",Zl();ym();let e=ot("turnList").querySelector("li.on");e&&e.scrollIntoView&&e.scrollIntoView({block:"nearest",inline:"nearest"}),Zi()}function ym(){let i=cn.turns||[];if(!i.length){ot("turnList").innerHTML='<li class="more">还没有记录。她被叫到一次，这里就多一轮。</li>';return}ot("turnList").innerHTML=i.map((t,e)=>'<li data-turn="'+e+'"'+(e===Pe?' class="on"':"")+">"+Re(pu(t.ts))+" · "+Re(Ji(t.where)||"?")+"<small>想起 "+(t.recalled||[]).length+" · 没说 "+(t.held||[]).length+"</small></li>").join("")}var Jl=new Map;function sm(i,t,e,n,s){let r=Jl.get(i);r||(r=document.createElement("div"),r.className="lbl3",ot("labels").appendChild(r),Jl.set(i,r)),r.textContent!==t&&(r.textContent=t),r.className="lbl3 "+(s||""),r.style.transform="translate("+Math.round(e)+"px,"+Math.round(n)+"px)",r.dataset.seen="1"}function TM(){let i=ot("galaxy"),t=i.clientWidth,e=i.clientHeight;for(let l of Jl.values())l.dataset.seen="";let n=(l,c,h,f,u)=>{let d=Nt.projectNode(c,t,e);d.behind||d.x<-40||d.y<-20||d.x>t+40||d.y>e+20||sm(l,h,d.x,d.y+(u||10),f)},s=Pe>=0,r=s?jl():null,a=Jt.win?Je.get(Jt.win):void 0;if(Ee.nodes.forEach((l,c)=>{if(en[c].kind!=="window")return;let h=s&&c!==r.where||ce>=0&&c!==ce&&!EM(c)||a!==void 0&&c!==a;n("w"+c,c,l.name,"win"+(h?" faded":""),12)}),ce>=0&&en[ce].kind!=="window"&&n("sel",ce,en[ce].label,"sel",10),s){let{rec:l,held:c}=r;l.slice(0,Kl).forEach((h,f)=>n("r"+f,h,f+1+" · "+en[h].label+(en[h].where!==cn.turns[Pe].where?"（"+Ji(en[h].where)+"）":""),"lit",-22)),c.forEach((h,f)=>n("h"+f,h,"没说 · "+en[h].label+"（"+Ji(en[h].where)+"）","held",-22))}if(qi&&!s&&ce<0){let l=0;for(let c of qi){if(l++>15)break;n("q"+c,c,en[c].label,"hit",10)}}let o=Nt.camera;Ki.pos.forEach((l,c)=>{let h=Jn.copy(l).project(o);if(h.z>1)return;let f=Ki.value(c),u=Kn[c].key==="valence"?(f>=0?"+":"−")+Math.round(Math.abs(f)*100):Math.round(f*100);sm("c"+c,Kn[c].name+" "+u+"%",(h.x+1)/2*t,(1-h.y)/2*e+14,"core")});for(let l of Jl.values())l.style.display=l.dataset.seen?"":"none"}var Vl=null;function EM(i){return(!Vl||Vl.sel!==ce)&&(Vl={sel:ce,set:eu(cu,ce,1).depthOf}),Vl.set.has(i)}function Re(i){return String(i??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}var pu=i=>{if(!i)return"";let t=new Date(i*1e3),e=n=>String(n).padStart(2,"0");return t.getMonth()+1+"-"+e(t.getDate())+" "+e(t.getHours())+":"+e(t.getMinutes())},mu=i=>{if(!i)return"";let t=(cn.now||Date.now()/1e3)-i;return t<3600?Math.max(1,Math.round(t/60))+" 分钟前":t<ql?Math.round(t/3600)+" 小时前":Math.round(t/ql)+" 天前"},Mm=i=>ps[i.kind]+(i.kind==="window"?i.sub==="private"?" · 私聊":" · 群":""),Ji=i=>{let t=Te.get(i);return t?t.label:""},bm=i=>[Mm(i),i.label,i.where?Ji(i.where):"",mu(i.ts)].filter(Boolean).join(" · "),js=i=>"#"+i.getHexString(),$l=null;async function Sm(i){$l=i.id,ot("drawer").hidden=!1,ot("dKind").textContent=Mm(i)+(i.cat&&i.cat!==i.label?" · "+i.cat:""),ot("dTitle").textContent=i.label||i.id;let t=[];i.ts&&t.push(["时间",Re(pu(i.ts)+"（"+mu(i.ts)+"）")]),i.where&&t.push(["窗口",'<a data-go="'+Re(i.where)+'">'+Re(Ji(i.where))+"</a>"]),i.vis&&t.push(["分寸",i.vis==="private"?"私下（空心）":"公开"]),i.kind==="memory"&&t.push(["分量",Math.round((i.w||0)*100)+"%"]),i.kind==="note"&&i.self&&t.push(["","她写给自己的"]),t.push(["编号",Re(i.id)]),ot("dMeta").innerHTML=t.map(([r,a])=>"<dt>"+Re(r)+"</dt><dd>"+a+"</dd>").join(""),ot("dBody").innerHTML='<span class="muted">取内容…</span>',RM(i);let e=await pM(i.id);if($l!==i.id)return;if(!e){ot("dBody").innerHTML='<span class="muted">没有更多内容。</span>';return}if(e.error){ot("dBody").innerHTML='<span class="muted">'+Re(e.error)+"</span>";return}let n="";e.title&&(ot("dTitle").textContent=e.title),e.text&&(n+='<div class="text">'+Re(e.text)+"</div>"),Array.isArray(e.lines)&&e.lines.length&&(n+="<dl>"+e.lines.map(([r,a])=>"<dt>"+Re(r)+"</dt><dd>"+Re(a)+"</dd>").join("")+"</dl>"),e.qq&&(n+='<div class="reveal"><button class="btn" id="qqBtn">显示 QQ 号</button> <span id="qqVal"></span></div>'),ot("dBody").innerHTML=n||'<span class="muted">没有更多内容。</span>';let s=ot("qqBtn");s&&(s.onclick=()=>{ot("qqVal").textContent=e.qq,s.remove()})}function CM(i){$l="core:"+i;let t=Kn[i],e=Ki.value(i);ot("drawer").hidden=!1,ot("dKind").textContent="身体",ot("dTitle").textContent=t.name,ot("dMeta").innerHTML="<dt>现在</dt><dd>"+(t.key==="valence"?(e>=0?"偏好 ":"偏低 ")+Math.round(Math.abs(e)*100):Math.round(e*100))+"%</dd><dt>说明</dt><dd>身体里的一样，只有数，不存话。越大越亮，数越高。</dd>",ot("dBody").innerHTML="",ot("dLinks").innerHTML=""}function RM(i){let t={};for(let n of $s.get(i.id)||[])(t[n.kind]=t[n.kind]||[]).push(n);let e='<div class="d-links">';for(let n of Object.keys(tr)){let s=t[n];if(s){s.sort((r,a)=>a.w-r.w),e+="<h3>"+tr[n]+" · "+s.length+"</h3><ul>";for(let r of s.slice(0,40)){let a=Te.get(r.other),o=a.kind==="person"?$n:Yi.get(a.kind==="window"?a.id:a.where)||$n;e+='<li data-id="'+Re(a.id)+'"><span class="dot'+(a.vis==="private"&&a.kind!=="window"?" ring":"")+'" style="--c:'+js(o)+'"></span>'+Re(bm(a))+(Je.has(a.id)?"":' <span class="muted">（筛掉了）</span>')+"</li>"}s.length>40&&(e+='<li class="more">还有 '+(s.length-40)+" 个</li>"),e+="</ul>"}}ot("dLinks").innerHTML=e+"</div>"}function Gi(i,t){if(su=-1,i<0){ce=-1,$l=null,ot("drawer").hidden=!0,Zi();return}Pe>=0&&Xi(-1),ce=i,Zi(),Sm(en[i]),t&&hn.flyTo(pi(i),Nt.nodeRadius(i),()=>hn.beginFocusOrbit(null))}function au(i,t){let e=Je.get(i);e!==void 0?Gi(e,t):Te.has(i)&&(ce=-1,Zi(),Sm(Te.get(i)))}var rm=0;function gu(){let i=ot("q").value.trim();if(clearTimeout(rm),!i){qi=null,ot("hits").innerHTML="",Zi();return}rm=setTimeout(async()=>{let t=new Set,e=i.toLowerCase();for(let s of Te.values())[s.id,s.label,s.cat,ps[s.kind],s.where?Ji(s.where):""].join(" ").toLowerCase().includes(e)&&t.add(s.id);for(let s of await mM(i))Te.has(s)&&t.add(s);if(ot("q").value.trim()!==i)return;qi=new Set([...t].map(s=>Je.get(s)).filter(s=>s!==void 0));let n=[...t].filter(s=>Je.has(s)).slice(0,60);ot("hits").innerHTML=(n.length?"":'<li class="more">没找到（或被筛掉了）</li>')+n.map(s=>{let r=Te.get(s),a=r.kind==="person"?$n:Yi.get(r.kind==="window"?r.id:r.where)||$n;return'<li data-id="'+Re(s)+'"><span class="dot" style="--c:'+js(a)+'"></span>'+Re(r.label)+(r.where?" · "+Re(Ji(r.where)):"")+'<span class="k">'+Re(mu(r.ts)||ps[r.kind])+"</span></li>"}).join("")+(t.size>n.length?'<li class="more">共 '+t.size+" 个，图上都亮着</li>":""),Zi()},200)}function _u(i){try{return localStorage.getItem(i)||""}catch{return""}}function am(i,t){try{localStorage.setItem(i,t)}catch{}}function Xl(i){ms=i,document.documentElement.dataset.theme=i?"dark":"light",ot("themeBtn").textContent=i?"浅色":"深色",Nt&&(Nt.applyTokens(i?jr:Nh,En.bloom.strength),Zl(),Zi());for(let t of mm)t.blending=i?Dn:Gn,t.uniforms.uLight.value=i?0:1,t.needsUpdate=!0}function PM(){let i=tn.get("theme");if(i==="dark"||i==="light")return Xl(i==="dark");let t=_u("bio_theme");if(t==="dark"||t==="light")return Xl(t==="dark");Xl(!0)}function IM(){let i={},t={};for(let a of Te.values())i[a.kind]=(i[a.kind]||0)+1;for(let a of cn.edges)t[a.kind]=(t[a.kind]||0)+1;let e={window:"#ff8a1f",person:js($n),memory:"#8cacc4",event:"#f2c14e",note:"#a78bfa"};ot("kindBoxes").innerHTML=Object.keys(ps).map(a=>'<label><input type="checkbox" data-kind="'+a+'"'+(Jt.kinds.has(a)?" checked":"")+' /><span class="chip" style="background:'+e[a]+'"></span>'+ps[a]+' <span class="n">'+(i[a]||0)+"</span></label>").join(""),ot("edgeBoxes").innerHTML=Object.keys(tr).map(a=>'<label><input type="checkbox" data-edge="'+a+'"'+(Jt.edges.has(a)?" checked":"")+" />"+tr[a]+' <span class="n">'+(t[a]||0)+"</span></label>").join("");let n=[...Te.values()].filter(a=>a.kind==="window"),s={};for(let a of Te.values())a.where&&(s[a.where]=(s[a.where]||0)+1);let r=a=>'<option value="'+Re(a.id)+'">'+Re(a.label)+"（"+(s[a.id]||0)+"）</option>";ot("winSel").innerHTML='<option value="">全部窗口</option><optgroup label="群">'+n.filter(a=>a.sub!=="private").map(r).join("")+'</optgroup><optgroup label="私聊">'+n.filter(a=>a.sub==="private").map(r).join("")+"</optgroup>",ot("legendWins").innerHTML=n.filter(a=>a.sub!=="private").slice(0,12).map(a=>'<span><i style="background:'+js(Yi.get(a.id))+'"></i>'+Re(a.label)+"</span>").join("")+'<span><i class="ring" style="--c:'+js(Yi.get(n.find(a=>a.sub==="private")?.id)||$n)+'"></i>私聊（空心）</span><span><i style="background:'+js($n)+'"></i>人</span>',ot("tFrom").value=String(Jt.from),ot("tTo").value=String(Jt.to),wm()}function wm(){ot("timeText").textContent=Jt.to===0?"最近 "+Jt.from+" 天":Jt.from+"–"+Jt.to+" 天前"}var om=0;function Gl(){clearTimeout(om),om=setTimeout(()=>{let i=Pe;Pe=-1,um(!1),ru=!1,Yl=i>=0,i>=0&&Xi(i),gu()},120)}function LM(){ot("kindBoxes").addEventListener("change",a=>{let o=a.target.dataset.kind;o&&(a.target.checked?Jt.kinds.add(o):Jt.kinds.delete(o),Gl())}),ot("edgeBoxes").addEventListener("change",a=>{let o=a.target.dataset.edge;o&&(a.target.checked?Jt.edges.add(o):Jt.edges.delete(o),Gl())}),ot("winSel").addEventListener("change",()=>{Jt.win=ot("winSel").value,Gi(-1),Je.get(Jt.win)!==void 0?_m([...pm(Jt.win)]):oa()}),ot("visSeg").addEventListener("click",a=>{let o=a.target.dataset.vis;if(o){Jt.vis=o;for(let l of ot("visSeg").children)l.classList.toggle("on",l.dataset.vis===o);Gl()}});let i=()=>{let a=Number(ot("tFrom").value),o=Number(ot("tTo").value);o>a&&(document.activeElement===ot("tFrom")?o=a:a=o,ot("tFrom").value=a,ot("tTo").value=o),Jt.from=a,Jt.to=o,wm(),Gl()};ot("tFrom").addEventListener("input",i),ot("tTo").addEventListener("input",i),ot("q").addEventListener("input",gu);let t=a=>{let o=a.target.closest("[data-id]");o&&au(o.dataset.id,!0)};ot("hits").addEventListener("click",t),ot("dLinks").addEventListener("click",t),ot("dMeta").addEventListener("click",a=>{let o=a.target.closest("[data-go]");o&&au(o.dataset.go,!0)}),ot("drawerClose").addEventListener("click",()=>Gi(-1)),ot("turnList").addEventListener("click",a=>{let o=a.target.closest("[data-turn]");o&&Xi(Number(o.dataset.turn))}),ot("turnPrev").addEventListener("click",()=>Xi(Pe<=0?cn.turns.length-1:Pe-1)),ot("turnNext").addEventListener("click",()=>Xi(Pe+1>=cn.turns.length?0:Pe+1)),ot("turnOff").addEventListener("click",()=>{Xi(-1),oa()}),ot("fitBtn").addEventListener("click",()=>{Gi(-1),oa()}),ot("motionBtn").addEventListener("click",()=>{ze=!ze,ot("motionBtn").classList.toggle("on",ze),am("brain_motion",ze?"1":"0"),hn.cruiseEnabled=ze,Nt.twinkleFreq=ze?En.twinkle:0}),ot("themeBtn").addEventListener("click",()=>{let a=!ms;Xl(a),am("bio_theme",a?"dark":"light")}),ot("panelBtn").addEventListener("click",()=>ot("side").classList.toggle("open")),window.addEventListener("resize",xm),window.addEventListener("keydown",a=>{a.target&&/INPUT|SELECT|TEXTAREA/.test(a.target.tagName)||(a.key==="Escape"?Pe>=0?Xi(-1):Gi(-1):a.key==="ArrowRight"?ot("turnNext").click():a.key==="ArrowLeft"&&ot("turnPrev").click())});let e=Nt.renderer.domElement,n=0,s=0;e.addEventListener("pointerdown",a=>{n=a.clientX,s=a.clientY}),e.addEventListener("pointerup",a=>{if(a.button!==0||a.ctrlKey||a.metaKey||a.shiftKey||Math.hypot(a.clientX-n,a.clientY-s)>5)return;let o=e.getBoundingClientRect(),l=a.clientX-o.left,c=a.clientY-o.top,h=lm(l,c,o.width,o.height);if(h>=0){Gi(-1),su=h,CM(h);return}let f=Nt.pickNearest(l,c,o.width,o.height,14);f>=0?Gi(f,!0):(ce>=0||su>=0)&&Gi(-1)});let r=!1;e.addEventListener("pointermove",a=>{ds.hoverThrottleMs===null||r||a.buttons||(r=!0,setTimeout(()=>{r=!1;let o=e.getBoundingClientRect(),l=a.clientX-o.left,c=a.clientY-o.top,h=lm(l,c,o.width,o.height),f=h>=0?-1:Nt.pickNearest(l,c,o.width,o.height,10);hm=f;let u=ot("tip");h>=0||f>=0?(u.textContent=h>=0?Kn[h].name+" · "+Math.round(Math.abs(Ki.value(h))*100)+"%":bm(en[f]),u.hidden=!1,u.style.left=Math.min(o.width-u.offsetWidth-8,l+14)+"px",u.style.top=c+14+"px",e.style.cursor="pointer"):(u.hidden=!0,e.style.cursor="")},ds.hoverThrottleMs))}),e.addEventListener("pointerleave",()=>{ot("tip").hidden=!0})}function lm(i,t,e,n){let s=-1,r=22;return Ki.pos.forEach((a,o)=>{let l=Jn.copy(a).project(Nt.camera);if(l.z>1)return;let c=Math.hypot((l.x+1)/2*e-i,(1-l.y)/2*n-t);c<r&&(r=c,s=o)}),s}var NM=tn.get("debug")==="1",cm=0,nu=null;function Am(i){let t=Uh(i,nu),e=zd(i,nu);nu=i,yM(i),Me.step()&&Nt.updatePositions(),Me.isSettled()&&!ru&&(ru=!0,Nt.refreshClusterClouds(),ot("loading").style.display="none",Yl||(Yl=!0,Pe<0&&ce<0&&!Jt.win&&oa()));try{hn.update(i,t,e)}catch{hn.cancelMotion()}vm(i),gs.ambient(i),gs.update(i),Ki.update(i),du.update(i),Nt.render(e,t),TM(),NM&&cm++%30===0&&(ot("statLine").dataset.debug=(Me instanceof Zs?"worker":"main")+" ticks="+Me.ticks+" settled="+Me.isSettled()+" frames="+cm),requestAnimationFrame(Am)}async function DM(){PM(),ze=_u("brain_motion")!=="0"&&!(window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches),tn.get("motion")==="0"&&(ze=!1),ot("motionBtn").classList.toggle("on",ze);let i=window.matchMedia&&window.matchMedia("(pointer: coarse)").matches;ds=$r[tn.get("tier")]||(i||window.innerWidth<820?$r.mobile:$r.high);let t=await dM();if(er!=="live"){let n=ot("sourceBadge");n.hidden=!1,er==="sample-embedded"&&(n.textContent="示例数据（编造）· 接口还没接上")}gM(t),IM(),um(!0),hn.cruiseEnabled=ze,xm();let e=gm();hn.setInitialFraming(e.center,Me.isSettled()?e.radius*.8:Math.max(e.radius,Qs*2.4)),Me.isSettled()&&(Yl=!0),LM(),ym(),tn.get("win")&&(ot("winSel").value=tn.get("win"),ot("winSel").dispatchEvent(new Event("change"))),tn.get("sel")&&au(tn.get("sel"),!0),tn.get("turn")&&Xi(Number(tn.get("turn"))-1),tn.get("q")&&(ot("q").value=tn.get("q"),gu()),requestAnimationFrame(Am)}DM();})();
/*! Bundled license information:

three/build/three.core.js:
three/build/three.module.js:
  (**
   * @license
   * Copyright 2010-2026 Three.js Authors
   * SPDX-License-Identifier: MIT
   *)
*/
