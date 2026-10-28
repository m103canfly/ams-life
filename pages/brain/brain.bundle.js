/* ams-life brain map (AGPL-3.0). Built by tools/brain/build.mjs; source in tools/brain/src/. Third-party licenses: licenses/. */
(()=>{var Cm=Object.defineProperty;var Rm=(i,t,e)=>t in i?Cm(i,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):i[t]=e;var Q=(i,t,e)=>Rm(i,typeof t!="symbol"?t+"":t,e);var po="184";var Nu=0,Tc=1,Du=2;var gr=1,Fu=2,Ns=3,ei=0,$e=1,zn=2,vn=0,On=1,Tn=2,Ec=3,Cc=4,Uu=5;var Mi=100,Ou=101,Bu=102,ku=103,zu=104,Vu=200,Gu=201,Hu=202,Wu=203,Pa=204,Ia=205,Xu=206,qu=207,Yu=208,Zu=209,Ju=210,$u=211,Ku=212,ju=213,Qu=214,La=0,Na=1,Da=2,ts=3,Fa=4,Ua=5,Oa=6,Ba=7,Rc=0,tf=1,ef=2,pn=0,_r=1,xr=2,vr=3,Ci=4,yr=5,Mr=6,br=7;var Pc=300,Ri=301,ss=302,mo=303,go=304,Sr=306,ka=1e3,Un=1001,za=1002,Oe=1003,nf=1004;var wr=1005;var ze=1006,_o=1007;var Pi=1008;var mn=1009,Ic=1010,Lc=1011,Ds=1012,xo=1013,En=1014,Cn=1015,qe=1016,vo=1017,yo=1018,Fs=1020,Nc=35902,Dc=35899,Fc=1021,Uc=1022,yn=1023,Bn=1026,Ii=1027,Oc=1028,Mo=1029,Li=1030,bo=1031;var So=1033,Ar=33776,Tr=33777,Er=33778,Cr=33779,wo=35840,Ao=35841,To=35842,Eo=35843,Co=36196,Ro=37492,Po=37496,Io=37488,Lo=37489,Rr=37490,No=37491,Do=37808,Fo=37809,Uo=37810,Oo=37811,Bo=37812,ko=37813,zo=37814,Vo=37815,Go=37816,Ho=37817,Wo=37818,Xo=37819,qo=37820,Yo=37821,Zo=36492,Jo=36494,$o=36495,Ko=36283,jo=36284,Pr=36285,Qo=36286;var js=2300,Va=2301,Ra=2302,_c=2303,xc=2400,vc=2401,yc=2402;var sf=3200;var Bc=0,rf=1,ai="",fn="srgb",Qs="srgb-linear",tr="linear",Kt="srgb";var Qi=7680;var Mc=519,af=512,of=513,lf=514,tl=515,cf=516,hf=517,el=518,uf=519,bc=35044,Ni=35048;var kc="300 es",An=2e3,er=2001;function Pm(i){for(let t=i.length-1;t>=0;--t)if(i[t]>=65535)return!0;return!1}function Im(i){return ArrayBuffer.isView(i)&&!(i instanceof DataView)}function nr(i){return document.createElementNS("http://www.w3.org/1999/xhtml",i)}function ff(){let i=nr("canvas");return i.style.display="block",i}var cu={},Es=null;function zc(...i){let t="THREE."+i.shift();Es?Es("log",t,...i):console.log(t,...i)}function df(i){let t=i[0];if(typeof t=="string"&&t.startsWith("TSL:")){let e=i[1];e&&e.isStackTrace?i[0]+=" "+e.getLocation():i[1]='Stack trace not available. Enable "THREE.Node.captureStackTrace" to capture stack traces.'}return i}function Et(...i){i=df(i);let t="THREE."+i.shift();if(Es)Es("warn",t,...i);else{let e=i[0];e&&e.isStackTrace?console.warn(e.getError(t)):console.warn(t,...i)}}function Rt(...i){i=df(i);let t="THREE."+i.shift();if(Es)Es("error",t,...i);else{let e=i[0];e&&e.isStackTrace?console.error(e.getError(t)):console.error(t,...i)}}function Ga(...i){let t=i.join(" ");t in cu||(cu[t]=!0,Et(...i))}function pf(i,t,e){return new Promise(function(n,s){function r(){switch(i.clientWaitSync(t,i.SYNC_FLUSH_COMMANDS_BIT,0)){case i.WAIT_FAILED:s();break;case i.TIMEOUT_EXPIRED:setTimeout(r,e);break;default:n()}}setTimeout(r,e)})}var mf={[La]:Na,[Da]:Oa,[Fa]:Ba,[ts]:Ua,[Na]:La,[Oa]:Da,[Ba]:Fa,[Ua]:ts},kn=class{addEventListener(t,e){this._listeners===void 0&&(this._listeners={});let n=this._listeners;n[t]===void 0&&(n[t]=[]),n[t].indexOf(e)===-1&&n[t].push(e)}hasEventListener(t,e){let n=this._listeners;return n===void 0?!1:n[t]!==void 0&&n[t].indexOf(e)!==-1}removeEventListener(t,e){let n=this._listeners;if(n===void 0)return;let s=n[t];if(s!==void 0){let r=s.indexOf(e);r!==-1&&s.splice(r,1)}}dispatchEvent(t){let e=this._listeners;if(e===void 0)return;let n=e[t.type];if(n!==void 0){t.target=this;let s=n.slice(0);for(let r=0,a=s.length;r<a;r++)s[r].call(this,t);t.target=null}}},He=["00","01","02","03","04","05","06","07","08","09","0a","0b","0c","0d","0e","0f","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","40","41","42","43","44","45","46","47","48","49","4a","4b","4c","4d","4e","4f","50","51","52","53","54","55","56","57","58","59","5a","5b","5c","5d","5e","5f","60","61","62","63","64","65","66","67","68","69","6a","6b","6c","6d","6e","6f","70","71","72","73","74","75","76","77","78","79","7a","7b","7c","7d","7e","7f","80","81","82","83","84","85","86","87","88","89","8a","8b","8c","8d","8e","8f","90","91","92","93","94","95","96","97","98","99","9a","9b","9c","9d","9e","9f","a0","a1","a2","a3","a4","a5","a6","a7","a8","a9","aa","ab","ac","ad","ae","af","b0","b1","b2","b3","b4","b5","b6","b7","b8","b9","ba","bb","bc","bd","be","bf","c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","ca","cb","cc","cd","ce","cf","d0","d1","d2","d3","d4","d5","d6","d7","d8","d9","da","db","dc","dd","de","df","e0","e1","e2","e3","e4","e5","e6","e7","e8","e9","ea","eb","ec","ed","ee","ef","f0","f1","f2","f3","f4","f5","f6","f7","f8","f9","fa","fb","fc","fd","fe","ff"];var Yl=Math.PI/180,Ha=180/Math.PI;function Ir(){let i=Math.random()*4294967295|0,t=Math.random()*4294967295|0,e=Math.random()*4294967295|0,n=Math.random()*4294967295|0;return(He[i&255]+He[i>>8&255]+He[i>>16&255]+He[i>>24&255]+"-"+He[t&255]+He[t>>8&255]+"-"+He[t>>16&15|64]+He[t>>24&255]+"-"+He[e&63|128]+He[e>>8&255]+"-"+He[e>>16&255]+He[e>>24&255]+He[n&255]+He[n>>8&255]+He[n>>16&255]+He[n>>24&255]).toLowerCase()}function Zt(i,t,e){return Math.max(t,Math.min(e,i))}function Lm(i,t){return(i%t+t)%t}function Zl(i,t,e){return(1-e)*i+e*t}function qs(i,t){switch(t.constructor){case Float32Array:return i;case Uint32Array:return i/4294967295;case Uint16Array:return i/65535;case Uint8Array:return i/255;case Int32Array:return Math.max(i/2147483647,-1);case Int16Array:return Math.max(i/32767,-1);case Int8Array:return Math.max(i/127,-1);default:throw new Error("Invalid component type.")}}function tn(i,t){switch(t.constructor){case Float32Array:return i;case Uint32Array:return Math.round(i*4294967295);case Uint16Array:return Math.round(i*65535);case Uint8Array:return Math.round(i*255);case Int32Array:return Math.round(i*2147483647);case Int16Array:return Math.round(i*32767);case Int8Array:return Math.round(i*127);default:throw new Error("Invalid component type.")}}var Xc=class Xc{constructor(t=0,e=0){this.x=t,this.y=e}get width(){return this.x}set width(t){this.x=t}get height(){return this.y}set height(t){this.y=t}set(t,e){return this.x=t,this.y=e,this}setScalar(t){return this.x=t,this.y=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y)}copy(t){return this.x=t.x,this.y=t.y,this}add(t){return this.x+=t.x,this.y+=t.y,this}addScalar(t){return this.x+=t,this.y+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this}subScalar(t){return this.x-=t,this.y-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this}multiply(t){return this.x*=t.x,this.y*=t.y,this}multiplyScalar(t){return this.x*=t,this.y*=t,this}divide(t){return this.x/=t.x,this.y/=t.y,this}divideScalar(t){return this.multiplyScalar(1/t)}applyMatrix3(t){let e=this.x,n=this.y,s=t.elements;return this.x=s[0]*e+s[3]*n+s[6],this.y=s[1]*e+s[4]*n+s[7],this}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this}clamp(t,e){return this.x=Zt(this.x,t.x,e.x),this.y=Zt(this.y,t.y,e.y),this}clampScalar(t,e){return this.x=Zt(this.x,t,e),this.y=Zt(this.y,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(Zt(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this}negate(){return this.x=-this.x,this.y=-this.y,this}dot(t){return this.x*t.x+this.y*t.y}cross(t){return this.x*t.y-this.y*t.x}lengthSq(){return this.x*this.x+this.y*this.y}length(){return Math.sqrt(this.x*this.x+this.y*this.y)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)}normalize(){return this.divideScalar(this.length()||1)}angle(){return Math.atan2(-this.y,-this.x)+Math.PI}angleTo(t){let e=Math.sqrt(this.lengthSq()*t.lengthSq());if(e===0)return Math.PI/2;let n=this.dot(t)/e;return Math.acos(Zt(n,-1,1))}distanceTo(t){return Math.sqrt(this.distanceToSquared(t))}distanceToSquared(t){let e=this.x-t.x,n=this.y-t.y;return e*e+n*n}manhattanDistanceTo(t){return Math.abs(this.x-t.x)+Math.abs(this.y-t.y)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this}equals(t){return t.x===this.x&&t.y===this.y}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this}rotateAround(t,e){let n=Math.cos(e),s=Math.sin(e),r=this.x-t.x,a=this.y-t.y;return this.x=r*n-a*s+t.x,this.y=r*s+a*n+t.y,this}random(){return this.x=Math.random(),this.y=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y}};Xc.prototype.isVector2=!0;var Ut=Xc,en=class{constructor(t=0,e=0,n=0,s=1){this.isQuaternion=!0,this._x=t,this._y=e,this._z=n,this._w=s}static slerpFlat(t,e,n,s,r,a,o){let l=n[s+0],c=n[s+1],h=n[s+2],f=n[s+3],u=r[a+0],p=r[a+1],g=r[a+2],x=r[a+3];if(f!==x||l!==u||c!==p||h!==g){let m=l*u+c*p+h*g+f*x;m<0&&(u=-u,p=-p,g=-g,x=-x,m=-m);let d=1-o;if(m<.9995){let y=Math.acos(m),S=Math.sin(y);d=Math.sin(d*y)/S,o=Math.sin(o*y)/S,l=l*d+u*o,c=c*d+p*o,h=h*d+g*o,f=f*d+x*o}else{l=l*d+u*o,c=c*d+p*o,h=h*d+g*o,f=f*d+x*o;let y=1/Math.sqrt(l*l+c*c+h*h+f*f);l*=y,c*=y,h*=y,f*=y}}t[e]=l,t[e+1]=c,t[e+2]=h,t[e+3]=f}static multiplyQuaternionsFlat(t,e,n,s,r,a){let o=n[s],l=n[s+1],c=n[s+2],h=n[s+3],f=r[a],u=r[a+1],p=r[a+2],g=r[a+3];return t[e]=o*g+h*f+l*p-c*u,t[e+1]=l*g+h*u+c*f-o*p,t[e+2]=c*g+h*p+o*u-l*f,t[e+3]=h*g-o*f-l*u-c*p,t}get x(){return this._x}set x(t){this._x=t,this._onChangeCallback()}get y(){return this._y}set y(t){this._y=t,this._onChangeCallback()}get z(){return this._z}set z(t){this._z=t,this._onChangeCallback()}get w(){return this._w}set w(t){this._w=t,this._onChangeCallback()}set(t,e,n,s){return this._x=t,this._y=e,this._z=n,this._w=s,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._w)}copy(t){return this._x=t.x,this._y=t.y,this._z=t.z,this._w=t.w,this._onChangeCallback(),this}setFromEuler(t,e=!0){let n=t._x,s=t._y,r=t._z,a=t._order,o=Math.cos,l=Math.sin,c=o(n/2),h=o(s/2),f=o(r/2),u=l(n/2),p=l(s/2),g=l(r/2);switch(a){case"XYZ":this._x=u*h*f+c*p*g,this._y=c*p*f-u*h*g,this._z=c*h*g+u*p*f,this._w=c*h*f-u*p*g;break;case"YXZ":this._x=u*h*f+c*p*g,this._y=c*p*f-u*h*g,this._z=c*h*g-u*p*f,this._w=c*h*f+u*p*g;break;case"ZXY":this._x=u*h*f-c*p*g,this._y=c*p*f+u*h*g,this._z=c*h*g+u*p*f,this._w=c*h*f-u*p*g;break;case"ZYX":this._x=u*h*f-c*p*g,this._y=c*p*f+u*h*g,this._z=c*h*g-u*p*f,this._w=c*h*f+u*p*g;break;case"YZX":this._x=u*h*f+c*p*g,this._y=c*p*f+u*h*g,this._z=c*h*g-u*p*f,this._w=c*h*f-u*p*g;break;case"XZY":this._x=u*h*f-c*p*g,this._y=c*p*f-u*h*g,this._z=c*h*g+u*p*f,this._w=c*h*f+u*p*g;break;default:Et("Quaternion: .setFromEuler() encountered an unknown order: "+a)}return e===!0&&this._onChangeCallback(),this}setFromAxisAngle(t,e){let n=e/2,s=Math.sin(n);return this._x=t.x*s,this._y=t.y*s,this._z=t.z*s,this._w=Math.cos(n),this._onChangeCallback(),this}setFromRotationMatrix(t){let e=t.elements,n=e[0],s=e[4],r=e[8],a=e[1],o=e[5],l=e[9],c=e[2],h=e[6],f=e[10],u=n+o+f;if(u>0){let p=.5/Math.sqrt(u+1);this._w=.25/p,this._x=(h-l)*p,this._y=(r-c)*p,this._z=(a-s)*p}else if(n>o&&n>f){let p=2*Math.sqrt(1+n-o-f);this._w=(h-l)/p,this._x=.25*p,this._y=(s+a)/p,this._z=(r+c)/p}else if(o>f){let p=2*Math.sqrt(1+o-n-f);this._w=(r-c)/p,this._x=(s+a)/p,this._y=.25*p,this._z=(l+h)/p}else{let p=2*Math.sqrt(1+f-n-o);this._w=(a-s)/p,this._x=(r+c)/p,this._y=(l+h)/p,this._z=.25*p}return this._onChangeCallback(),this}setFromUnitVectors(t,e){let n=t.dot(e)+1;return n<1e-8?(n=0,Math.abs(t.x)>Math.abs(t.z)?(this._x=-t.y,this._y=t.x,this._z=0,this._w=n):(this._x=0,this._y=-t.z,this._z=t.y,this._w=n)):(this._x=t.y*e.z-t.z*e.y,this._y=t.z*e.x-t.x*e.z,this._z=t.x*e.y-t.y*e.x,this._w=n),this.normalize()}angleTo(t){return 2*Math.acos(Math.abs(Zt(this.dot(t),-1,1)))}rotateTowards(t,e){let n=this.angleTo(t);if(n===0)return this;let s=Math.min(1,e/n);return this.slerp(t,s),this}identity(){return this.set(0,0,0,1)}invert(){return this.conjugate()}conjugate(){return this._x*=-1,this._y*=-1,this._z*=-1,this._onChangeCallback(),this}dot(t){return this._x*t._x+this._y*t._y+this._z*t._z+this._w*t._w}lengthSq(){return this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w}length(){return Math.sqrt(this._x*this._x+this._y*this._y+this._z*this._z+this._w*this._w)}normalize(){let t=this.length();return t===0?(this._x=0,this._y=0,this._z=0,this._w=1):(t=1/t,this._x=this._x*t,this._y=this._y*t,this._z=this._z*t,this._w=this._w*t),this._onChangeCallback(),this}multiply(t){return this.multiplyQuaternions(this,t)}premultiply(t){return this.multiplyQuaternions(t,this)}multiplyQuaternions(t,e){let n=t._x,s=t._y,r=t._z,a=t._w,o=e._x,l=e._y,c=e._z,h=e._w;return this._x=n*h+a*o+s*c-r*l,this._y=s*h+a*l+r*o-n*c,this._z=r*h+a*c+n*l-s*o,this._w=a*h-n*o-s*l-r*c,this._onChangeCallback(),this}slerp(t,e){let n=t._x,s=t._y,r=t._z,a=t._w,o=this.dot(t);o<0&&(n=-n,s=-s,r=-r,a=-a,o=-o);let l=1-e;if(o<.9995){let c=Math.acos(o),h=Math.sin(c);l=Math.sin(l*c)/h,e=Math.sin(e*c)/h,this._x=this._x*l+n*e,this._y=this._y*l+s*e,this._z=this._z*l+r*e,this._w=this._w*l+a*e,this._onChangeCallback()}else this._x=this._x*l+n*e,this._y=this._y*l+s*e,this._z=this._z*l+r*e,this._w=this._w*l+a*e,this.normalize();return this}slerpQuaternions(t,e,n){return this.copy(t).slerp(e,n)}random(){let t=2*Math.PI*Math.random(),e=2*Math.PI*Math.random(),n=Math.random(),s=Math.sqrt(1-n),r=Math.sqrt(n);return this.set(s*Math.sin(t),s*Math.cos(t),r*Math.sin(e),r*Math.cos(e))}equals(t){return t._x===this._x&&t._y===this._y&&t._z===this._z&&t._w===this._w}fromArray(t,e=0){return this._x=t[e],this._y=t[e+1],this._z=t[e+2],this._w=t[e+3],this._onChangeCallback(),this}toArray(t=[],e=0){return t[e]=this._x,t[e+1]=this._y,t[e+2]=this._z,t[e+3]=this._w,t}fromBufferAttribute(t,e){return this._x=t.getX(e),this._y=t.getY(e),this._z=t.getZ(e),this._w=t.getW(e),this._onChangeCallback(),this}toJSON(){return this.toArray()}_onChange(t){return this._onChangeCallback=t,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._w}},qc=class qc{constructor(t=0,e=0,n=0){this.x=t,this.y=e,this.z=n}set(t,e,n){return n===void 0&&(n=this.z),this.x=t,this.y=e,this.z=n,this}setScalar(t){return this.x=t,this.y=t,this.z=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setZ(t){return this.z=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;case 2:this.z=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;case 2:return this.z;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y,this.z)}copy(t){return this.x=t.x,this.y=t.y,this.z=t.z,this}add(t){return this.x+=t.x,this.y+=t.y,this.z+=t.z,this}addScalar(t){return this.x+=t,this.y+=t,this.z+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this.z=t.z+e.z,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this.z+=t.z*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this.z-=t.z,this}subScalar(t){return this.x-=t,this.y-=t,this.z-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this.z=t.z-e.z,this}multiply(t){return this.x*=t.x,this.y*=t.y,this.z*=t.z,this}multiplyScalar(t){return this.x*=t,this.y*=t,this.z*=t,this}multiplyVectors(t,e){return this.x=t.x*e.x,this.y=t.y*e.y,this.z=t.z*e.z,this}applyEuler(t){return this.applyQuaternion(hu.setFromEuler(t))}applyAxisAngle(t,e){return this.applyQuaternion(hu.setFromAxisAngle(t,e))}applyMatrix3(t){let e=this.x,n=this.y,s=this.z,r=t.elements;return this.x=r[0]*e+r[3]*n+r[6]*s,this.y=r[1]*e+r[4]*n+r[7]*s,this.z=r[2]*e+r[5]*n+r[8]*s,this}applyNormalMatrix(t){return this.applyMatrix3(t).normalize()}applyMatrix4(t){let e=this.x,n=this.y,s=this.z,r=t.elements,a=1/(r[3]*e+r[7]*n+r[11]*s+r[15]);return this.x=(r[0]*e+r[4]*n+r[8]*s+r[12])*a,this.y=(r[1]*e+r[5]*n+r[9]*s+r[13])*a,this.z=(r[2]*e+r[6]*n+r[10]*s+r[14])*a,this}applyQuaternion(t){let e=this.x,n=this.y,s=this.z,r=t.x,a=t.y,o=t.z,l=t.w,c=2*(a*s-o*n),h=2*(o*e-r*s),f=2*(r*n-a*e);return this.x=e+l*c+a*f-o*h,this.y=n+l*h+o*c-r*f,this.z=s+l*f+r*h-a*c,this}project(t){return this.applyMatrix4(t.matrixWorldInverse).applyMatrix4(t.projectionMatrix)}unproject(t){return this.applyMatrix4(t.projectionMatrixInverse).applyMatrix4(t.matrixWorld)}transformDirection(t){let e=this.x,n=this.y,s=this.z,r=t.elements;return this.x=r[0]*e+r[4]*n+r[8]*s,this.y=r[1]*e+r[5]*n+r[9]*s,this.z=r[2]*e+r[6]*n+r[10]*s,this.normalize()}divide(t){return this.x/=t.x,this.y/=t.y,this.z/=t.z,this}divideScalar(t){return this.multiplyScalar(1/t)}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this.z=Math.min(this.z,t.z),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this.z=Math.max(this.z,t.z),this}clamp(t,e){return this.x=Zt(this.x,t.x,e.x),this.y=Zt(this.y,t.y,e.y),this.z=Zt(this.z,t.z,e.z),this}clampScalar(t,e){return this.x=Zt(this.x,t,e),this.y=Zt(this.y,t,e),this.z=Zt(this.z,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(Zt(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this}dot(t){return this.x*t.x+this.y*t.y+this.z*t.z}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)}normalize(){return this.divideScalar(this.length()||1)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this.z+=(t.z-this.z)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this.z=t.z+(e.z-t.z)*n,this}cross(t){return this.crossVectors(this,t)}crossVectors(t,e){let n=t.x,s=t.y,r=t.z,a=e.x,o=e.y,l=e.z;return this.x=s*l-r*o,this.y=r*a-n*l,this.z=n*o-s*a,this}projectOnVector(t){let e=t.lengthSq();if(e===0)return this.set(0,0,0);let n=t.dot(this)/e;return this.copy(t).multiplyScalar(n)}projectOnPlane(t){return Jl.copy(this).projectOnVector(t),this.sub(Jl)}reflect(t){return this.sub(Jl.copy(t).multiplyScalar(2*this.dot(t)))}angleTo(t){let e=Math.sqrt(this.lengthSq()*t.lengthSq());if(e===0)return Math.PI/2;let n=this.dot(t)/e;return Math.acos(Zt(n,-1,1))}distanceTo(t){return Math.sqrt(this.distanceToSquared(t))}distanceToSquared(t){let e=this.x-t.x,n=this.y-t.y,s=this.z-t.z;return e*e+n*n+s*s}manhattanDistanceTo(t){return Math.abs(this.x-t.x)+Math.abs(this.y-t.y)+Math.abs(this.z-t.z)}setFromSpherical(t){return this.setFromSphericalCoords(t.radius,t.phi,t.theta)}setFromSphericalCoords(t,e,n){let s=Math.sin(e)*t;return this.x=s*Math.sin(n),this.y=Math.cos(e)*t,this.z=s*Math.cos(n),this}setFromCylindrical(t){return this.setFromCylindricalCoords(t.radius,t.theta,t.y)}setFromCylindricalCoords(t,e,n){return this.x=t*Math.sin(e),this.y=n,this.z=t*Math.cos(e),this}setFromMatrixPosition(t){let e=t.elements;return this.x=e[12],this.y=e[13],this.z=e[14],this}setFromMatrixScale(t){let e=this.setFromMatrixColumn(t,0).length(),n=this.setFromMatrixColumn(t,1).length(),s=this.setFromMatrixColumn(t,2).length();return this.x=e,this.y=n,this.z=s,this}setFromMatrixColumn(t,e){return this.fromArray(t.elements,e*4)}setFromMatrix3Column(t,e){return this.fromArray(t.elements,e*3)}setFromEuler(t){return this.x=t._x,this.y=t._y,this.z=t._z,this}setFromColor(t){return this.x=t.r,this.y=t.g,this.z=t.b,this}equals(t){return t.x===this.x&&t.y===this.y&&t.z===this.z}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this.z=t[e+2],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t[e+2]=this.z,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this.z=t.getZ(e),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this}randomDirection(){let t=Math.random()*Math.PI*2,e=Math.random()*2-1,n=Math.sqrt(1-e*e);return this.x=n*Math.cos(t),this.y=e,this.z=n*Math.sin(t),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z}};qc.prototype.isVector3=!0;var D=qc,Jl=new D,hu=new en,Yc=class Yc{constructor(t,e,n,s,r,a,o,l,c){this.elements=[1,0,0,0,1,0,0,0,1],t!==void 0&&this.set(t,e,n,s,r,a,o,l,c)}set(t,e,n,s,r,a,o,l,c){let h=this.elements;return h[0]=t,h[1]=s,h[2]=o,h[3]=e,h[4]=r,h[5]=l,h[6]=n,h[7]=a,h[8]=c,this}identity(){return this.set(1,0,0,0,1,0,0,0,1),this}copy(t){let e=this.elements,n=t.elements;return e[0]=n[0],e[1]=n[1],e[2]=n[2],e[3]=n[3],e[4]=n[4],e[5]=n[5],e[6]=n[6],e[7]=n[7],e[8]=n[8],this}extractBasis(t,e,n){return t.setFromMatrix3Column(this,0),e.setFromMatrix3Column(this,1),n.setFromMatrix3Column(this,2),this}setFromMatrix4(t){let e=t.elements;return this.set(e[0],e[4],e[8],e[1],e[5],e[9],e[2],e[6],e[10]),this}multiply(t){return this.multiplyMatrices(this,t)}premultiply(t){return this.multiplyMatrices(t,this)}multiplyMatrices(t,e){let n=t.elements,s=e.elements,r=this.elements,a=n[0],o=n[3],l=n[6],c=n[1],h=n[4],f=n[7],u=n[2],p=n[5],g=n[8],x=s[0],m=s[3],d=s[6],y=s[1],S=s[4],b=s[7],T=s[2],w=s[5],R=s[8];return r[0]=a*x+o*y+l*T,r[3]=a*m+o*S+l*w,r[6]=a*d+o*b+l*R,r[1]=c*x+h*y+f*T,r[4]=c*m+h*S+f*w,r[7]=c*d+h*b+f*R,r[2]=u*x+p*y+g*T,r[5]=u*m+p*S+g*w,r[8]=u*d+p*b+g*R,this}multiplyScalar(t){let e=this.elements;return e[0]*=t,e[3]*=t,e[6]*=t,e[1]*=t,e[4]*=t,e[7]*=t,e[2]*=t,e[5]*=t,e[8]*=t,this}determinant(){let t=this.elements,e=t[0],n=t[1],s=t[2],r=t[3],a=t[4],o=t[5],l=t[6],c=t[7],h=t[8];return e*a*h-e*o*c-n*r*h+n*o*l+s*r*c-s*a*l}invert(){let t=this.elements,e=t[0],n=t[1],s=t[2],r=t[3],a=t[4],o=t[5],l=t[6],c=t[7],h=t[8],f=h*a-o*c,u=o*l-h*r,p=c*r-a*l,g=e*f+n*u+s*p;if(g===0)return this.set(0,0,0,0,0,0,0,0,0);let x=1/g;return t[0]=f*x,t[1]=(s*c-h*n)*x,t[2]=(o*n-s*a)*x,t[3]=u*x,t[4]=(h*e-s*l)*x,t[5]=(s*r-o*e)*x,t[6]=p*x,t[7]=(n*l-c*e)*x,t[8]=(a*e-n*r)*x,this}transpose(){let t,e=this.elements;return t=e[1],e[1]=e[3],e[3]=t,t=e[2],e[2]=e[6],e[6]=t,t=e[5],e[5]=e[7],e[7]=t,this}getNormalMatrix(t){return this.setFromMatrix4(t).invert().transpose()}transposeIntoArray(t){let e=this.elements;return t[0]=e[0],t[1]=e[3],t[2]=e[6],t[3]=e[1],t[4]=e[4],t[5]=e[7],t[6]=e[2],t[7]=e[5],t[8]=e[8],this}setUvTransform(t,e,n,s,r,a,o){let l=Math.cos(r),c=Math.sin(r);return this.set(n*l,n*c,-n*(l*a+c*o)+a+t,-s*c,s*l,-s*(-c*a+l*o)+o+e,0,0,1),this}scale(t,e){return this.premultiply($l.makeScale(t,e)),this}rotate(t){return this.premultiply($l.makeRotation(-t)),this}translate(t,e){return this.premultiply($l.makeTranslation(t,e)),this}makeTranslation(t,e){return t.isVector2?this.set(1,0,t.x,0,1,t.y,0,0,1):this.set(1,0,t,0,1,e,0,0,1),this}makeRotation(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,-n,0,n,e,0,0,0,1),this}makeScale(t,e){return this.set(t,0,0,0,e,0,0,0,1),this}equals(t){let e=this.elements,n=t.elements;for(let s=0;s<9;s++)if(e[s]!==n[s])return!1;return!0}fromArray(t,e=0){for(let n=0;n<9;n++)this.elements[n]=t[n+e];return this}toArray(t=[],e=0){let n=this.elements;return t[e]=n[0],t[e+1]=n[1],t[e+2]=n[2],t[e+3]=n[3],t[e+4]=n[4],t[e+5]=n[5],t[e+6]=n[6],t[e+7]=n[7],t[e+8]=n[8],t}clone(){return new this.constructor().fromArray(this.elements)}};Yc.prototype.isMatrix3=!0;var Dt=Yc,$l=new Dt,uu=new Dt().set(.4123908,.3575843,.1804808,.212639,.7151687,.0721923,.0193308,.1191948,.9505322),fu=new Dt().set(3.2409699,-1.5373832,-.4986108,-.9692436,1.8759675,.0415551,.0556301,-.203977,1.0569715);function Nm(){let i={enabled:!0,workingColorSpace:Qs,spaces:{},convert:function(s,r,a){return this.enabled===!1||r===a||!r||!a||(this.spaces[r].transfer===Kt&&(s.r=ti(s.r),s.g=ti(s.g),s.b=ti(s.b)),this.spaces[r].primaries!==this.spaces[a].primaries&&(s.applyMatrix3(this.spaces[r].toXYZ),s.applyMatrix3(this.spaces[a].fromXYZ)),this.spaces[a].transfer===Kt&&(s.r=Ts(s.r),s.g=Ts(s.g),s.b=Ts(s.b))),s},workingToColorSpace:function(s,r){return this.convert(s,this.workingColorSpace,r)},colorSpaceToWorking:function(s,r){return this.convert(s,r,this.workingColorSpace)},getPrimaries:function(s){return this.spaces[s].primaries},getTransfer:function(s){return s===ai?tr:this.spaces[s].transfer},getToneMappingMode:function(s){return this.spaces[s].outputColorSpaceConfig.toneMappingMode||"standard"},getLuminanceCoefficients:function(s,r=this.workingColorSpace){return s.fromArray(this.spaces[r].luminanceCoefficients)},define:function(s){Object.assign(this.spaces,s)},_getMatrix:function(s,r,a){return s.copy(this.spaces[r].toXYZ).multiply(this.spaces[a].fromXYZ)},_getDrawingBufferColorSpace:function(s){return this.spaces[s].outputColorSpaceConfig.drawingBufferColorSpace},_getUnpackColorSpace:function(s=this.workingColorSpace){return this.spaces[s].workingColorSpaceConfig.unpackColorSpace},fromWorkingColorSpace:function(s,r){return Ga("ColorManagement: .fromWorkingColorSpace() has been renamed to .workingToColorSpace()."),i.workingToColorSpace(s,r)},toWorkingColorSpace:function(s,r){return Ga("ColorManagement: .toWorkingColorSpace() has been renamed to .colorSpaceToWorking()."),i.colorSpaceToWorking(s,r)}},t=[.64,.33,.3,.6,.15,.06],e=[.2126,.7152,.0722],n=[.3127,.329];return i.define({[Qs]:{primaries:t,whitePoint:n,transfer:tr,toXYZ:uu,fromXYZ:fu,luminanceCoefficients:e,workingColorSpaceConfig:{unpackColorSpace:fn},outputColorSpaceConfig:{drawingBufferColorSpace:fn}},[fn]:{primaries:t,whitePoint:n,transfer:Kt,toXYZ:uu,fromXYZ:fu,luminanceCoefficients:e,outputColorSpaceConfig:{drawingBufferColorSpace:fn}}}),i}var Ht=Nm();function ti(i){return i<.04045?i*.0773993808:Math.pow(i*.9478672986+.0521327014,2.4)}function Ts(i){return i<.0031308?i*12.92:1.055*Math.pow(i,.41666)-.055}var ps,Wa=class{static getDataURL(t,e="image/png"){if(/^data:/i.test(t.src)||typeof HTMLCanvasElement>"u")return t.src;let n;if(t instanceof HTMLCanvasElement)n=t;else{ps===void 0&&(ps=nr("canvas")),ps.width=t.width,ps.height=t.height;let s=ps.getContext("2d");t instanceof ImageData?s.putImageData(t,0,0):s.drawImage(t,0,0,t.width,t.height),n=ps}return n.toDataURL(e)}static sRGBToLinear(t){if(typeof HTMLImageElement<"u"&&t instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&t instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&t instanceof ImageBitmap){let e=nr("canvas");e.width=t.width,e.height=t.height;let n=e.getContext("2d");n.drawImage(t,0,0,t.width,t.height);let s=n.getImageData(0,0,t.width,t.height),r=s.data;for(let a=0;a<r.length;a++)r[a]=ti(r[a]/255)*255;return n.putImageData(s,0,0),e}else if(t.data){let e=t.data.slice(0);for(let n=0;n<e.length;n++)e instanceof Uint8Array||e instanceof Uint8ClampedArray?e[n]=Math.floor(ti(e[n]/255)*255):e[n]=ti(e[n]);return{data:e,width:t.width,height:t.height}}else return Et("ImageUtils.sRGBToLinear(): Unsupported image type. No color space conversion applied."),t}},Dm=0,Cs=class{constructor(t=null){this.isSource=!0,Object.defineProperty(this,"id",{value:Dm++}),this.uuid=Ir(),this.data=t,this.dataReady=!0,this.version=0}getSize(t){let e=this.data;return typeof HTMLVideoElement<"u"&&e instanceof HTMLVideoElement?t.set(e.videoWidth,e.videoHeight,0):typeof VideoFrame<"u"&&e instanceof VideoFrame?t.set(e.displayWidth,e.displayHeight,0):e!==null?t.set(e.width,e.height,e.depth||0):t.set(0,0,0),t}set needsUpdate(t){t===!0&&this.version++}toJSON(t){let e=t===void 0||typeof t=="string";if(!e&&t.images[this.uuid]!==void 0)return t.images[this.uuid];let n={uuid:this.uuid,url:""},s=this.data;if(s!==null){let r;if(Array.isArray(s)){r=[];for(let a=0,o=s.length;a<o;a++)s[a].isDataTexture?r.push(Kl(s[a].image)):r.push(Kl(s[a]))}else r=Kl(s);n.url=r}return e||(t.images[this.uuid]=n),n}};function Kl(i){return typeof HTMLImageElement<"u"&&i instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&i instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&i instanceof ImageBitmap?Wa.getDataURL(i):i.data?{data:Array.from(i.data),width:i.width,height:i.height,type:i.data.constructor.name}:(Et("Texture: Unable to serialize Texture."),{})}var Fm=0,jl=new D,nn=class i extends kn{constructor(t=i.DEFAULT_IMAGE,e=i.DEFAULT_MAPPING,n=Un,s=Un,r=ze,a=Pi,o=yn,l=mn,c=i.DEFAULT_ANISOTROPY,h=ai){super(),this.isTexture=!0,Object.defineProperty(this,"id",{value:Fm++}),this.uuid=Ir(),this.name="",this.source=new Cs(t),this.mipmaps=[],this.mapping=e,this.channel=0,this.wrapS=n,this.wrapT=s,this.magFilter=r,this.minFilter=a,this.anisotropy=c,this.format=o,this.internalFormat=null,this.type=l,this.offset=new Ut(0,0),this.repeat=new Ut(1,1),this.center=new Ut(0,0),this.rotation=0,this.matrixAutoUpdate=!0,this.matrix=new Dt,this.generateMipmaps=!0,this.premultiplyAlpha=!1,this.flipY=!0,this.unpackAlignment=4,this.colorSpace=h,this.userData={},this.updateRanges=[],this.version=0,this.onUpdate=null,this.renderTarget=null,this.isRenderTargetTexture=!1,this.isArrayTexture=!!(t&&t.depth&&t.depth>1),this.pmremVersion=0,this.normalized=!1}get width(){return this.source.getSize(jl).x}get height(){return this.source.getSize(jl).y}get depth(){return this.source.getSize(jl).z}get image(){return this.source.data}set image(t){this.source.data=t}updateMatrix(){this.matrix.setUvTransform(this.offset.x,this.offset.y,this.repeat.x,this.repeat.y,this.rotation,this.center.x,this.center.y)}addUpdateRange(t,e){this.updateRanges.push({start:t,count:e})}clearUpdateRanges(){this.updateRanges.length=0}clone(){return new this.constructor().copy(this)}copy(t){return this.name=t.name,this.source=t.source,this.mipmaps=t.mipmaps.slice(0),this.mapping=t.mapping,this.channel=t.channel,this.wrapS=t.wrapS,this.wrapT=t.wrapT,this.magFilter=t.magFilter,this.minFilter=t.minFilter,this.anisotropy=t.anisotropy,this.format=t.format,this.internalFormat=t.internalFormat,this.type=t.type,this.normalized=t.normalized,this.offset.copy(t.offset),this.repeat.copy(t.repeat),this.center.copy(t.center),this.rotation=t.rotation,this.matrixAutoUpdate=t.matrixAutoUpdate,this.matrix.copy(t.matrix),this.generateMipmaps=t.generateMipmaps,this.premultiplyAlpha=t.premultiplyAlpha,this.flipY=t.flipY,this.unpackAlignment=t.unpackAlignment,this.colorSpace=t.colorSpace,this.renderTarget=t.renderTarget,this.isRenderTargetTexture=t.isRenderTargetTexture,this.isArrayTexture=t.isArrayTexture,this.userData=JSON.parse(JSON.stringify(t.userData)),this.needsUpdate=!0,this}setValues(t){for(let e in t){let n=t[e];if(n===void 0){Et(`Texture.setValues(): parameter '${e}' has value of undefined.`);continue}let s=this[e];if(s===void 0){Et(`Texture.setValues(): property '${e}' does not exist.`);continue}s&&n&&s.isVector2&&n.isVector2||s&&n&&s.isVector3&&n.isVector3||s&&n&&s.isMatrix3&&n.isMatrix3?s.copy(n):this[e]=n}}toJSON(t){let e=t===void 0||typeof t=="string";if(!e&&t.textures[this.uuid]!==void 0)return t.textures[this.uuid];let n={metadata:{version:4.7,type:"Texture",generator:"Texture.toJSON"},uuid:this.uuid,name:this.name,image:this.source.toJSON(t).uuid,mapping:this.mapping,channel:this.channel,repeat:[this.repeat.x,this.repeat.y],offset:[this.offset.x,this.offset.y],center:[this.center.x,this.center.y],rotation:this.rotation,wrap:[this.wrapS,this.wrapT],format:this.format,internalFormat:this.internalFormat,type:this.type,normalized:this.normalized,colorSpace:this.colorSpace,minFilter:this.minFilter,magFilter:this.magFilter,anisotropy:this.anisotropy,flipY:this.flipY,generateMipmaps:this.generateMipmaps,premultiplyAlpha:this.premultiplyAlpha,unpackAlignment:this.unpackAlignment};return Object.keys(this.userData).length>0&&(n.userData=this.userData),e||(t.textures[this.uuid]=n),n}dispose(){this.dispatchEvent({type:"dispose"})}transformUv(t){if(this.mapping!==Pc)return t;if(t.applyMatrix3(this.matrix),t.x<0||t.x>1)switch(this.wrapS){case ka:t.x=t.x-Math.floor(t.x);break;case Un:t.x=t.x<0?0:1;break;case za:Math.abs(Math.floor(t.x)%2)===1?t.x=Math.ceil(t.x)-t.x:t.x=t.x-Math.floor(t.x);break}if(t.y<0||t.y>1)switch(this.wrapT){case ka:t.y=t.y-Math.floor(t.y);break;case Un:t.y=t.y<0?0:1;break;case za:Math.abs(Math.floor(t.y)%2)===1?t.y=Math.ceil(t.y)-t.y:t.y=t.y-Math.floor(t.y);break}return this.flipY&&(t.y=1-t.y),t}set needsUpdate(t){t===!0&&(this.version++,this.source.needsUpdate=!0)}set needsPMREMUpdate(t){t===!0&&this.pmremVersion++}};nn.DEFAULT_IMAGE=null;nn.DEFAULT_MAPPING=Pc;nn.DEFAULT_ANISOTROPY=1;var Zc=class Zc{constructor(t=0,e=0,n=0,s=1){this.x=t,this.y=e,this.z=n,this.w=s}get width(){return this.z}set width(t){this.z=t}get height(){return this.w}set height(t){this.w=t}set(t,e,n,s){return this.x=t,this.y=e,this.z=n,this.w=s,this}setScalar(t){return this.x=t,this.y=t,this.z=t,this.w=t,this}setX(t){return this.x=t,this}setY(t){return this.y=t,this}setZ(t){return this.z=t,this}setW(t){return this.w=t,this}setComponent(t,e){switch(t){case 0:this.x=e;break;case 1:this.y=e;break;case 2:this.z=e;break;case 3:this.w=e;break;default:throw new Error("index is out of range: "+t)}return this}getComponent(t){switch(t){case 0:return this.x;case 1:return this.y;case 2:return this.z;case 3:return this.w;default:throw new Error("index is out of range: "+t)}}clone(){return new this.constructor(this.x,this.y,this.z,this.w)}copy(t){return this.x=t.x,this.y=t.y,this.z=t.z,this.w=t.w!==void 0?t.w:1,this}add(t){return this.x+=t.x,this.y+=t.y,this.z+=t.z,this.w+=t.w,this}addScalar(t){return this.x+=t,this.y+=t,this.z+=t,this.w+=t,this}addVectors(t,e){return this.x=t.x+e.x,this.y=t.y+e.y,this.z=t.z+e.z,this.w=t.w+e.w,this}addScaledVector(t,e){return this.x+=t.x*e,this.y+=t.y*e,this.z+=t.z*e,this.w+=t.w*e,this}sub(t){return this.x-=t.x,this.y-=t.y,this.z-=t.z,this.w-=t.w,this}subScalar(t){return this.x-=t,this.y-=t,this.z-=t,this.w-=t,this}subVectors(t,e){return this.x=t.x-e.x,this.y=t.y-e.y,this.z=t.z-e.z,this.w=t.w-e.w,this}multiply(t){return this.x*=t.x,this.y*=t.y,this.z*=t.z,this.w*=t.w,this}multiplyScalar(t){return this.x*=t,this.y*=t,this.z*=t,this.w*=t,this}applyMatrix4(t){let e=this.x,n=this.y,s=this.z,r=this.w,a=t.elements;return this.x=a[0]*e+a[4]*n+a[8]*s+a[12]*r,this.y=a[1]*e+a[5]*n+a[9]*s+a[13]*r,this.z=a[2]*e+a[6]*n+a[10]*s+a[14]*r,this.w=a[3]*e+a[7]*n+a[11]*s+a[15]*r,this}divide(t){return this.x/=t.x,this.y/=t.y,this.z/=t.z,this.w/=t.w,this}divideScalar(t){return this.multiplyScalar(1/t)}setAxisAngleFromQuaternion(t){this.w=2*Math.acos(t.w);let e=Math.sqrt(1-t.w*t.w);return e<1e-4?(this.x=1,this.y=0,this.z=0):(this.x=t.x/e,this.y=t.y/e,this.z=t.z/e),this}setAxisAngleFromRotationMatrix(t){let e,n,s,r,l=t.elements,c=l[0],h=l[4],f=l[8],u=l[1],p=l[5],g=l[9],x=l[2],m=l[6],d=l[10];if(Math.abs(h-u)<.01&&Math.abs(f-x)<.01&&Math.abs(g-m)<.01){if(Math.abs(h+u)<.1&&Math.abs(f+x)<.1&&Math.abs(g+m)<.1&&Math.abs(c+p+d-3)<.1)return this.set(1,0,0,0),this;e=Math.PI;let S=(c+1)/2,b=(p+1)/2,T=(d+1)/2,w=(h+u)/4,R=(f+x)/4,v=(g+m)/4;return S>b&&S>T?S<.01?(n=0,s=.707106781,r=.707106781):(n=Math.sqrt(S),s=w/n,r=R/n):b>T?b<.01?(n=.707106781,s=0,r=.707106781):(s=Math.sqrt(b),n=w/s,r=v/s):T<.01?(n=.707106781,s=.707106781,r=0):(r=Math.sqrt(T),n=R/r,s=v/r),this.set(n,s,r,e),this}let y=Math.sqrt((m-g)*(m-g)+(f-x)*(f-x)+(u-h)*(u-h));return Math.abs(y)<.001&&(y=1),this.x=(m-g)/y,this.y=(f-x)/y,this.z=(u-h)/y,this.w=Math.acos((c+p+d-1)/2),this}setFromMatrixPosition(t){let e=t.elements;return this.x=e[12],this.y=e[13],this.z=e[14],this.w=e[15],this}min(t){return this.x=Math.min(this.x,t.x),this.y=Math.min(this.y,t.y),this.z=Math.min(this.z,t.z),this.w=Math.min(this.w,t.w),this}max(t){return this.x=Math.max(this.x,t.x),this.y=Math.max(this.y,t.y),this.z=Math.max(this.z,t.z),this.w=Math.max(this.w,t.w),this}clamp(t,e){return this.x=Zt(this.x,t.x,e.x),this.y=Zt(this.y,t.y,e.y),this.z=Zt(this.z,t.z,e.z),this.w=Zt(this.w,t.w,e.w),this}clampScalar(t,e){return this.x=Zt(this.x,t,e),this.y=Zt(this.y,t,e),this.z=Zt(this.z,t,e),this.w=Zt(this.w,t,e),this}clampLength(t,e){let n=this.length();return this.divideScalar(n||1).multiplyScalar(Zt(n,t,e))}floor(){return this.x=Math.floor(this.x),this.y=Math.floor(this.y),this.z=Math.floor(this.z),this.w=Math.floor(this.w),this}ceil(){return this.x=Math.ceil(this.x),this.y=Math.ceil(this.y),this.z=Math.ceil(this.z),this.w=Math.ceil(this.w),this}round(){return this.x=Math.round(this.x),this.y=Math.round(this.y),this.z=Math.round(this.z),this.w=Math.round(this.w),this}roundToZero(){return this.x=Math.trunc(this.x),this.y=Math.trunc(this.y),this.z=Math.trunc(this.z),this.w=Math.trunc(this.w),this}negate(){return this.x=-this.x,this.y=-this.y,this.z=-this.z,this.w=-this.w,this}dot(t){return this.x*t.x+this.y*t.y+this.z*t.z+this.w*t.w}lengthSq(){return this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w}length(){return Math.sqrt(this.x*this.x+this.y*this.y+this.z*this.z+this.w*this.w)}manhattanLength(){return Math.abs(this.x)+Math.abs(this.y)+Math.abs(this.z)+Math.abs(this.w)}normalize(){return this.divideScalar(this.length()||1)}setLength(t){return this.normalize().multiplyScalar(t)}lerp(t,e){return this.x+=(t.x-this.x)*e,this.y+=(t.y-this.y)*e,this.z+=(t.z-this.z)*e,this.w+=(t.w-this.w)*e,this}lerpVectors(t,e,n){return this.x=t.x+(e.x-t.x)*n,this.y=t.y+(e.y-t.y)*n,this.z=t.z+(e.z-t.z)*n,this.w=t.w+(e.w-t.w)*n,this}equals(t){return t.x===this.x&&t.y===this.y&&t.z===this.z&&t.w===this.w}fromArray(t,e=0){return this.x=t[e],this.y=t[e+1],this.z=t[e+2],this.w=t[e+3],this}toArray(t=[],e=0){return t[e]=this.x,t[e+1]=this.y,t[e+2]=this.z,t[e+3]=this.w,t}fromBufferAttribute(t,e){return this.x=t.getX(e),this.y=t.getY(e),this.z=t.getZ(e),this.w=t.getW(e),this}random(){return this.x=Math.random(),this.y=Math.random(),this.z=Math.random(),this.w=Math.random(),this}*[Symbol.iterator](){yield this.x,yield this.y,yield this.z,yield this.w}};Zc.prototype.isVector4=!0;var ye=Zc,Xa=class extends kn{constructor(t=1,e=1,n={}){super(),n=Object.assign({generateMipmaps:!1,internalFormat:null,minFilter:ze,depthBuffer:!0,stencilBuffer:!1,resolveDepthBuffer:!0,resolveStencilBuffer:!0,depthTexture:null,samples:0,count:1,depth:1,multiview:!1},n),this.isRenderTarget=!0,this.width=t,this.height=e,this.depth=n.depth,this.scissor=new ye(0,0,t,e),this.scissorTest=!1,this.viewport=new ye(0,0,t,e),this.textures=[];let s={width:t,height:e,depth:n.depth},r=new nn(s),a=n.count;for(let o=0;o<a;o++)this.textures[o]=r.clone(),this.textures[o].isRenderTargetTexture=!0,this.textures[o].renderTarget=this;this._setTextureOptions(n),this.depthBuffer=n.depthBuffer,this.stencilBuffer=n.stencilBuffer,this.resolveDepthBuffer=n.resolveDepthBuffer,this.resolveStencilBuffer=n.resolveStencilBuffer,this._depthTexture=null,this.depthTexture=n.depthTexture,this.samples=n.samples,this.multiview=n.multiview}_setTextureOptions(t={}){let e={minFilter:ze,generateMipmaps:!1,flipY:!1,internalFormat:null};t.mapping!==void 0&&(e.mapping=t.mapping),t.wrapS!==void 0&&(e.wrapS=t.wrapS),t.wrapT!==void 0&&(e.wrapT=t.wrapT),t.wrapR!==void 0&&(e.wrapR=t.wrapR),t.magFilter!==void 0&&(e.magFilter=t.magFilter),t.minFilter!==void 0&&(e.minFilter=t.minFilter),t.format!==void 0&&(e.format=t.format),t.type!==void 0&&(e.type=t.type),t.anisotropy!==void 0&&(e.anisotropy=t.anisotropy),t.colorSpace!==void 0&&(e.colorSpace=t.colorSpace),t.flipY!==void 0&&(e.flipY=t.flipY),t.generateMipmaps!==void 0&&(e.generateMipmaps=t.generateMipmaps),t.internalFormat!==void 0&&(e.internalFormat=t.internalFormat);for(let n=0;n<this.textures.length;n++)this.textures[n].setValues(e)}get texture(){return this.textures[0]}set texture(t){this.textures[0]=t}set depthTexture(t){this._depthTexture!==null&&(this._depthTexture.renderTarget=null),t!==null&&(t.renderTarget=this),this._depthTexture=t}get depthTexture(){return this._depthTexture}setSize(t,e,n=1){if(this.width!==t||this.height!==e||this.depth!==n){this.width=t,this.height=e,this.depth=n;for(let s=0,r=this.textures.length;s<r;s++)this.textures[s].image.width=t,this.textures[s].image.height=e,this.textures[s].image.depth=n,this.textures[s].isData3DTexture!==!0&&(this.textures[s].isArrayTexture=this.textures[s].image.depth>1);this.dispose()}this.viewport.set(0,0,t,e),this.scissor.set(0,0,t,e)}clone(){return new this.constructor().copy(this)}copy(t){this.width=t.width,this.height=t.height,this.depth=t.depth,this.scissor.copy(t.scissor),this.scissorTest=t.scissorTest,this.viewport.copy(t.viewport),this.textures.length=0;for(let e=0,n=t.textures.length;e<n;e++){this.textures[e]=t.textures[e].clone(),this.textures[e].isRenderTargetTexture=!0,this.textures[e].renderTarget=this;let s=Object.assign({},t.textures[e].image);this.textures[e].source=new Cs(s)}return this.depthBuffer=t.depthBuffer,this.stencilBuffer=t.stencilBuffer,this.resolveDepthBuffer=t.resolveDepthBuffer,this.resolveStencilBuffer=t.resolveStencilBuffer,t.depthTexture!==null&&(this.depthTexture=t.depthTexture.clone()),this.samples=t.samples,this.multiview=t.multiview,this}dispose(){this.dispatchEvent({type:"dispose"})}},Le=class extends Xa{constructor(t=1,e=1,n={}){super(t,e,n),this.isWebGLRenderTarget=!0}},ir=class extends nn{constructor(t=null,e=1,n=1,s=1){super(null),this.isDataArrayTexture=!0,this.image={data:t,width:e,height:n,depth:s},this.magFilter=Oe,this.minFilter=Oe,this.wrapR=Un,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1,this.layerUpdates=new Set}addLayerUpdate(t){this.layerUpdates.add(t)}clearLayerUpdates(){this.layerUpdates.clear()}};var qa=class extends nn{constructor(t=null,e=1,n=1,s=1){super(null),this.isData3DTexture=!0,this.image={data:t,width:e,height:n,depth:s},this.magFilter=Oe,this.minFilter=Oe,this.wrapR=Un,this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}};var fo=class fo{constructor(t,e,n,s,r,a,o,l,c,h,f,u,p,g,x,m){this.elements=[1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1],t!==void 0&&this.set(t,e,n,s,r,a,o,l,c,h,f,u,p,g,x,m)}set(t,e,n,s,r,a,o,l,c,h,f,u,p,g,x,m){let d=this.elements;return d[0]=t,d[4]=e,d[8]=n,d[12]=s,d[1]=r,d[5]=a,d[9]=o,d[13]=l,d[2]=c,d[6]=h,d[10]=f,d[14]=u,d[3]=p,d[7]=g,d[11]=x,d[15]=m,this}identity(){return this.set(1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1),this}clone(){return new fo().fromArray(this.elements)}copy(t){let e=this.elements,n=t.elements;return e[0]=n[0],e[1]=n[1],e[2]=n[2],e[3]=n[3],e[4]=n[4],e[5]=n[5],e[6]=n[6],e[7]=n[7],e[8]=n[8],e[9]=n[9],e[10]=n[10],e[11]=n[11],e[12]=n[12],e[13]=n[13],e[14]=n[14],e[15]=n[15],this}copyPosition(t){let e=this.elements,n=t.elements;return e[12]=n[12],e[13]=n[13],e[14]=n[14],this}setFromMatrix3(t){let e=t.elements;return this.set(e[0],e[3],e[6],0,e[1],e[4],e[7],0,e[2],e[5],e[8],0,0,0,0,1),this}extractBasis(t,e,n){return this.determinant()===0?(t.set(1,0,0),e.set(0,1,0),n.set(0,0,1),this):(t.setFromMatrixColumn(this,0),e.setFromMatrixColumn(this,1),n.setFromMatrixColumn(this,2),this)}makeBasis(t,e,n){return this.set(t.x,e.x,n.x,0,t.y,e.y,n.y,0,t.z,e.z,n.z,0,0,0,0,1),this}extractRotation(t){if(t.determinant()===0)return this.identity();let e=this.elements,n=t.elements,s=1/ms.setFromMatrixColumn(t,0).length(),r=1/ms.setFromMatrixColumn(t,1).length(),a=1/ms.setFromMatrixColumn(t,2).length();return e[0]=n[0]*s,e[1]=n[1]*s,e[2]=n[2]*s,e[3]=0,e[4]=n[4]*r,e[5]=n[5]*r,e[6]=n[6]*r,e[7]=0,e[8]=n[8]*a,e[9]=n[9]*a,e[10]=n[10]*a,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,this}makeRotationFromEuler(t){let e=this.elements,n=t.x,s=t.y,r=t.z,a=Math.cos(n),o=Math.sin(n),l=Math.cos(s),c=Math.sin(s),h=Math.cos(r),f=Math.sin(r);if(t.order==="XYZ"){let u=a*h,p=a*f,g=o*h,x=o*f;e[0]=l*h,e[4]=-l*f,e[8]=c,e[1]=p+g*c,e[5]=u-x*c,e[9]=-o*l,e[2]=x-u*c,e[6]=g+p*c,e[10]=a*l}else if(t.order==="YXZ"){let u=l*h,p=l*f,g=c*h,x=c*f;e[0]=u+x*o,e[4]=g*o-p,e[8]=a*c,e[1]=a*f,e[5]=a*h,e[9]=-o,e[2]=p*o-g,e[6]=x+u*o,e[10]=a*l}else if(t.order==="ZXY"){let u=l*h,p=l*f,g=c*h,x=c*f;e[0]=u-x*o,e[4]=-a*f,e[8]=g+p*o,e[1]=p+g*o,e[5]=a*h,e[9]=x-u*o,e[2]=-a*c,e[6]=o,e[10]=a*l}else if(t.order==="ZYX"){let u=a*h,p=a*f,g=o*h,x=o*f;e[0]=l*h,e[4]=g*c-p,e[8]=u*c+x,e[1]=l*f,e[5]=x*c+u,e[9]=p*c-g,e[2]=-c,e[6]=o*l,e[10]=a*l}else if(t.order==="YZX"){let u=a*l,p=a*c,g=o*l,x=o*c;e[0]=l*h,e[4]=x-u*f,e[8]=g*f+p,e[1]=f,e[5]=a*h,e[9]=-o*h,e[2]=-c*h,e[6]=p*f+g,e[10]=u-x*f}else if(t.order==="XZY"){let u=a*l,p=a*c,g=o*l,x=o*c;e[0]=l*h,e[4]=-f,e[8]=c*h,e[1]=u*f+x,e[5]=a*h,e[9]=p*f-g,e[2]=g*f-p,e[6]=o*h,e[10]=x*f+u}return e[3]=0,e[7]=0,e[11]=0,e[12]=0,e[13]=0,e[14]=0,e[15]=1,this}makeRotationFromQuaternion(t){return this.compose(Um,t,Om)}lookAt(t,e,n){let s=this.elements;return hn.subVectors(t,e),hn.lengthSq()===0&&(hn.z=1),hn.normalize(),pi.crossVectors(n,hn),pi.lengthSq()===0&&(Math.abs(n.z)===1?hn.x+=1e-4:hn.z+=1e-4,hn.normalize(),pi.crossVectors(n,hn)),pi.normalize(),ra.crossVectors(hn,pi),s[0]=pi.x,s[4]=ra.x,s[8]=hn.x,s[1]=pi.y,s[5]=ra.y,s[9]=hn.y,s[2]=pi.z,s[6]=ra.z,s[10]=hn.z,this}multiply(t){return this.multiplyMatrices(this,t)}premultiply(t){return this.multiplyMatrices(t,this)}multiplyMatrices(t,e){let n=t.elements,s=e.elements,r=this.elements,a=n[0],o=n[4],l=n[8],c=n[12],h=n[1],f=n[5],u=n[9],p=n[13],g=n[2],x=n[6],m=n[10],d=n[14],y=n[3],S=n[7],b=n[11],T=n[15],w=s[0],R=s[4],v=s[8],E=s[12],I=s[1],C=s[5],N=s[9],H=s[13],W=s[2],U=s[6],z=s[10],V=s[14],$=s[3],tt=s[7],ct=s[11],Mt=s[15];return r[0]=a*w+o*I+l*W+c*$,r[4]=a*R+o*C+l*U+c*tt,r[8]=a*v+o*N+l*z+c*ct,r[12]=a*E+o*H+l*V+c*Mt,r[1]=h*w+f*I+u*W+p*$,r[5]=h*R+f*C+u*U+p*tt,r[9]=h*v+f*N+u*z+p*ct,r[13]=h*E+f*H+u*V+p*Mt,r[2]=g*w+x*I+m*W+d*$,r[6]=g*R+x*C+m*U+d*tt,r[10]=g*v+x*N+m*z+d*ct,r[14]=g*E+x*H+m*V+d*Mt,r[3]=y*w+S*I+b*W+T*$,r[7]=y*R+S*C+b*U+T*tt,r[11]=y*v+S*N+b*z+T*ct,r[15]=y*E+S*H+b*V+T*Mt,this}multiplyScalar(t){let e=this.elements;return e[0]*=t,e[4]*=t,e[8]*=t,e[12]*=t,e[1]*=t,e[5]*=t,e[9]*=t,e[13]*=t,e[2]*=t,e[6]*=t,e[10]*=t,e[14]*=t,e[3]*=t,e[7]*=t,e[11]*=t,e[15]*=t,this}determinant(){let t=this.elements,e=t[0],n=t[4],s=t[8],r=t[12],a=t[1],o=t[5],l=t[9],c=t[13],h=t[2],f=t[6],u=t[10],p=t[14],g=t[3],x=t[7],m=t[11],d=t[15],y=l*p-c*u,S=o*p-c*f,b=o*u-l*f,T=a*p-c*h,w=a*u-l*h,R=a*f-o*h;return e*(x*y-m*S+d*b)-n*(g*y-m*T+d*w)+s*(g*S-x*T+d*R)-r*(g*b-x*w+m*R)}transpose(){let t=this.elements,e;return e=t[1],t[1]=t[4],t[4]=e,e=t[2],t[2]=t[8],t[8]=e,e=t[6],t[6]=t[9],t[9]=e,e=t[3],t[3]=t[12],t[12]=e,e=t[7],t[7]=t[13],t[13]=e,e=t[11],t[11]=t[14],t[14]=e,this}setPosition(t,e,n){let s=this.elements;return t.isVector3?(s[12]=t.x,s[13]=t.y,s[14]=t.z):(s[12]=t,s[13]=e,s[14]=n),this}invert(){let t=this.elements,e=t[0],n=t[1],s=t[2],r=t[3],a=t[4],o=t[5],l=t[6],c=t[7],h=t[8],f=t[9],u=t[10],p=t[11],g=t[12],x=t[13],m=t[14],d=t[15],y=e*o-n*a,S=e*l-s*a,b=e*c-r*a,T=n*l-s*o,w=n*c-r*o,R=s*c-r*l,v=h*x-f*g,E=h*m-u*g,I=h*d-p*g,C=f*m-u*x,N=f*d-p*x,H=u*d-p*m,W=y*H-S*N+b*C+T*I-w*E+R*v;if(W===0)return this.set(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);let U=1/W;return t[0]=(o*H-l*N+c*C)*U,t[1]=(s*N-n*H-r*C)*U,t[2]=(x*R-m*w+d*T)*U,t[3]=(u*w-f*R-p*T)*U,t[4]=(l*I-a*H-c*E)*U,t[5]=(e*H-s*I+r*E)*U,t[6]=(m*b-g*R-d*S)*U,t[7]=(h*R-u*b+p*S)*U,t[8]=(a*N-o*I+c*v)*U,t[9]=(n*I-e*N-r*v)*U,t[10]=(g*w-x*b+d*y)*U,t[11]=(f*b-h*w-p*y)*U,t[12]=(o*E-a*C-l*v)*U,t[13]=(e*C-n*E+s*v)*U,t[14]=(x*S-g*T-m*y)*U,t[15]=(h*T-f*S+u*y)*U,this}scale(t){let e=this.elements,n=t.x,s=t.y,r=t.z;return e[0]*=n,e[4]*=s,e[8]*=r,e[1]*=n,e[5]*=s,e[9]*=r,e[2]*=n,e[6]*=s,e[10]*=r,e[3]*=n,e[7]*=s,e[11]*=r,this}getMaxScaleOnAxis(){let t=this.elements,e=t[0]*t[0]+t[1]*t[1]+t[2]*t[2],n=t[4]*t[4]+t[5]*t[5]+t[6]*t[6],s=t[8]*t[8]+t[9]*t[9]+t[10]*t[10];return Math.sqrt(Math.max(e,n,s))}makeTranslation(t,e,n){return t.isVector3?this.set(1,0,0,t.x,0,1,0,t.y,0,0,1,t.z,0,0,0,1):this.set(1,0,0,t,0,1,0,e,0,0,1,n,0,0,0,1),this}makeRotationX(t){let e=Math.cos(t),n=Math.sin(t);return this.set(1,0,0,0,0,e,-n,0,0,n,e,0,0,0,0,1),this}makeRotationY(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,0,n,0,0,1,0,0,-n,0,e,0,0,0,0,1),this}makeRotationZ(t){let e=Math.cos(t),n=Math.sin(t);return this.set(e,-n,0,0,n,e,0,0,0,0,1,0,0,0,0,1),this}makeRotationAxis(t,e){let n=Math.cos(e),s=Math.sin(e),r=1-n,a=t.x,o=t.y,l=t.z,c=r*a,h=r*o;return this.set(c*a+n,c*o-s*l,c*l+s*o,0,c*o+s*l,h*o+n,h*l-s*a,0,c*l-s*o,h*l+s*a,r*l*l+n,0,0,0,0,1),this}makeScale(t,e,n){return this.set(t,0,0,0,0,e,0,0,0,0,n,0,0,0,0,1),this}makeShear(t,e,n,s,r,a){return this.set(1,n,r,0,t,1,a,0,e,s,1,0,0,0,0,1),this}compose(t,e,n){let s=this.elements,r=e._x,a=e._y,o=e._z,l=e._w,c=r+r,h=a+a,f=o+o,u=r*c,p=r*h,g=r*f,x=a*h,m=a*f,d=o*f,y=l*c,S=l*h,b=l*f,T=n.x,w=n.y,R=n.z;return s[0]=(1-(x+d))*T,s[1]=(p+b)*T,s[2]=(g-S)*T,s[3]=0,s[4]=(p-b)*w,s[5]=(1-(u+d))*w,s[6]=(m+y)*w,s[7]=0,s[8]=(g+S)*R,s[9]=(m-y)*R,s[10]=(1-(u+x))*R,s[11]=0,s[12]=t.x,s[13]=t.y,s[14]=t.z,s[15]=1,this}decompose(t,e,n){let s=this.elements;t.x=s[12],t.y=s[13],t.z=s[14];let r=this.determinant();if(r===0)return n.set(1,1,1),e.identity(),this;let a=ms.set(s[0],s[1],s[2]).length(),o=ms.set(s[4],s[5],s[6]).length(),l=ms.set(s[8],s[9],s[10]).length();r<0&&(a=-a),bn.copy(this);let c=1/a,h=1/o,f=1/l;return bn.elements[0]*=c,bn.elements[1]*=c,bn.elements[2]*=c,bn.elements[4]*=h,bn.elements[5]*=h,bn.elements[6]*=h,bn.elements[8]*=f,bn.elements[9]*=f,bn.elements[10]*=f,e.setFromRotationMatrix(bn),n.x=a,n.y=o,n.z=l,this}makePerspective(t,e,n,s,r,a,o=An,l=!1){let c=this.elements,h=2*r/(e-t),f=2*r/(n-s),u=(e+t)/(e-t),p=(n+s)/(n-s),g,x;if(l)g=r/(a-r),x=a*r/(a-r);else if(o===An)g=-(a+r)/(a-r),x=-2*a*r/(a-r);else if(o===er)g=-a/(a-r),x=-a*r/(a-r);else throw new Error("THREE.Matrix4.makePerspective(): Invalid coordinate system: "+o);return c[0]=h,c[4]=0,c[8]=u,c[12]=0,c[1]=0,c[5]=f,c[9]=p,c[13]=0,c[2]=0,c[6]=0,c[10]=g,c[14]=x,c[3]=0,c[7]=0,c[11]=-1,c[15]=0,this}makeOrthographic(t,e,n,s,r,a,o=An,l=!1){let c=this.elements,h=2/(e-t),f=2/(n-s),u=-(e+t)/(e-t),p=-(n+s)/(n-s),g,x;if(l)g=1/(a-r),x=a/(a-r);else if(o===An)g=-2/(a-r),x=-(a+r)/(a-r);else if(o===er)g=-1/(a-r),x=-r/(a-r);else throw new Error("THREE.Matrix4.makeOrthographic(): Invalid coordinate system: "+o);return c[0]=h,c[4]=0,c[8]=0,c[12]=u,c[1]=0,c[5]=f,c[9]=0,c[13]=p,c[2]=0,c[6]=0,c[10]=g,c[14]=x,c[3]=0,c[7]=0,c[11]=0,c[15]=1,this}equals(t){let e=this.elements,n=t.elements;for(let s=0;s<16;s++)if(e[s]!==n[s])return!1;return!0}fromArray(t,e=0){for(let n=0;n<16;n++)this.elements[n]=t[n+e];return this}toArray(t=[],e=0){let n=this.elements;return t[e]=n[0],t[e+1]=n[1],t[e+2]=n[2],t[e+3]=n[3],t[e+4]=n[4],t[e+5]=n[5],t[e+6]=n[6],t[e+7]=n[7],t[e+8]=n[8],t[e+9]=n[9],t[e+10]=n[10],t[e+11]=n[11],t[e+12]=n[12],t[e+13]=n[13],t[e+14]=n[14],t[e+15]=n[15],t}};fo.prototype.isMatrix4=!0;var ve=fo,ms=new D,bn=new ve,Um=new D(0,0,0),Om=new D(1,1,1),pi=new D,ra=new D,hn=new D,du=new ve,pu=new en,bi=class i{constructor(t=0,e=0,n=0,s=i.DEFAULT_ORDER){this.isEuler=!0,this._x=t,this._y=e,this._z=n,this._order=s}get x(){return this._x}set x(t){this._x=t,this._onChangeCallback()}get y(){return this._y}set y(t){this._y=t,this._onChangeCallback()}get z(){return this._z}set z(t){this._z=t,this._onChangeCallback()}get order(){return this._order}set order(t){this._order=t,this._onChangeCallback()}set(t,e,n,s=this._order){return this._x=t,this._y=e,this._z=n,this._order=s,this._onChangeCallback(),this}clone(){return new this.constructor(this._x,this._y,this._z,this._order)}copy(t){return this._x=t._x,this._y=t._y,this._z=t._z,this._order=t._order,this._onChangeCallback(),this}setFromRotationMatrix(t,e=this._order,n=!0){let s=t.elements,r=s[0],a=s[4],o=s[8],l=s[1],c=s[5],h=s[9],f=s[2],u=s[6],p=s[10];switch(e){case"XYZ":this._y=Math.asin(Zt(o,-1,1)),Math.abs(o)<.9999999?(this._x=Math.atan2(-h,p),this._z=Math.atan2(-a,r)):(this._x=Math.atan2(u,c),this._z=0);break;case"YXZ":this._x=Math.asin(-Zt(h,-1,1)),Math.abs(h)<.9999999?(this._y=Math.atan2(o,p),this._z=Math.atan2(l,c)):(this._y=Math.atan2(-f,r),this._z=0);break;case"ZXY":this._x=Math.asin(Zt(u,-1,1)),Math.abs(u)<.9999999?(this._y=Math.atan2(-f,p),this._z=Math.atan2(-a,c)):(this._y=0,this._z=Math.atan2(l,r));break;case"ZYX":this._y=Math.asin(-Zt(f,-1,1)),Math.abs(f)<.9999999?(this._x=Math.atan2(u,p),this._z=Math.atan2(l,r)):(this._x=0,this._z=Math.atan2(-a,c));break;case"YZX":this._z=Math.asin(Zt(l,-1,1)),Math.abs(l)<.9999999?(this._x=Math.atan2(-h,c),this._y=Math.atan2(-f,r)):(this._x=0,this._y=Math.atan2(o,p));break;case"XZY":this._z=Math.asin(-Zt(a,-1,1)),Math.abs(a)<.9999999?(this._x=Math.atan2(u,c),this._y=Math.atan2(o,r)):(this._x=Math.atan2(-h,p),this._y=0);break;default:Et("Euler: .setFromRotationMatrix() encountered an unknown order: "+e)}return this._order=e,n===!0&&this._onChangeCallback(),this}setFromQuaternion(t,e,n){return du.makeRotationFromQuaternion(t),this.setFromRotationMatrix(du,e,n)}setFromVector3(t,e=this._order){return this.set(t.x,t.y,t.z,e)}reorder(t){return pu.setFromEuler(this),this.setFromQuaternion(pu,t)}equals(t){return t._x===this._x&&t._y===this._y&&t._z===this._z&&t._order===this._order}fromArray(t){return this._x=t[0],this._y=t[1],this._z=t[2],t[3]!==void 0&&(this._order=t[3]),this._onChangeCallback(),this}toArray(t=[],e=0){return t[e]=this._x,t[e+1]=this._y,t[e+2]=this._z,t[e+3]=this._order,t}_onChange(t){return this._onChangeCallback=t,this}_onChangeCallback(){}*[Symbol.iterator](){yield this._x,yield this._y,yield this._z,yield this._order}};bi.DEFAULT_ORDER="XYZ";var sr=class{constructor(){this.mask=1}set(t){this.mask=(1<<t|0)>>>0}enable(t){this.mask|=1<<t|0}enableAll(){this.mask=-1}toggle(t){this.mask^=1<<t|0}disable(t){this.mask&=~(1<<t|0)}disableAll(){this.mask=0}test(t){return(this.mask&t.mask)!==0}isEnabled(t){return(this.mask&(1<<t|0))!==0}},Bm=0,mu=new D,gs=new en,Zn=new ve,aa=new D,Ys=new D,km=new D,zm=new en,gu=new D(1,0,0),_u=new D(0,1,0),xu=new D(0,0,1),vu={type:"added"},Vm={type:"removed"},_s={type:"childadded",child:null},Ql={type:"childremoved",child:null},sn=class i extends kn{constructor(){super(),this.isObject3D=!0,Object.defineProperty(this,"id",{value:Bm++}),this.uuid=Ir(),this.name="",this.type="Object3D",this.parent=null,this.children=[],this.up=i.DEFAULT_UP.clone();let t=new D,e=new bi,n=new en,s=new D(1,1,1);function r(){n.setFromEuler(e,!1)}function a(){e.setFromQuaternion(n,void 0,!1)}e._onChange(r),n._onChange(a),Object.defineProperties(this,{position:{configurable:!0,enumerable:!0,value:t},rotation:{configurable:!0,enumerable:!0,value:e},quaternion:{configurable:!0,enumerable:!0,value:n},scale:{configurable:!0,enumerable:!0,value:s},modelViewMatrix:{value:new ve},normalMatrix:{value:new Dt}}),this.matrix=new ve,this.matrixWorld=new ve,this.matrixAutoUpdate=i.DEFAULT_MATRIX_AUTO_UPDATE,this.matrixWorldAutoUpdate=i.DEFAULT_MATRIX_WORLD_AUTO_UPDATE,this.matrixWorldNeedsUpdate=!1,this.layers=new sr,this.visible=!0,this.castShadow=!1,this.receiveShadow=!1,this.frustumCulled=!0,this.renderOrder=0,this.animations=[],this.customDepthMaterial=void 0,this.customDistanceMaterial=void 0,this.static=!1,this.userData={},this.pivot=null}onBeforeShadow(){}onAfterShadow(){}onBeforeRender(){}onAfterRender(){}applyMatrix4(t){this.matrixAutoUpdate&&this.updateMatrix(),this.matrix.premultiply(t),this.matrix.decompose(this.position,this.quaternion,this.scale)}applyQuaternion(t){return this.quaternion.premultiply(t),this}setRotationFromAxisAngle(t,e){this.quaternion.setFromAxisAngle(t,e)}setRotationFromEuler(t){this.quaternion.setFromEuler(t,!0)}setRotationFromMatrix(t){this.quaternion.setFromRotationMatrix(t)}setRotationFromQuaternion(t){this.quaternion.copy(t)}rotateOnAxis(t,e){return gs.setFromAxisAngle(t,e),this.quaternion.multiply(gs),this}rotateOnWorldAxis(t,e){return gs.setFromAxisAngle(t,e),this.quaternion.premultiply(gs),this}rotateX(t){return this.rotateOnAxis(gu,t)}rotateY(t){return this.rotateOnAxis(_u,t)}rotateZ(t){return this.rotateOnAxis(xu,t)}translateOnAxis(t,e){return mu.copy(t).applyQuaternion(this.quaternion),this.position.add(mu.multiplyScalar(e)),this}translateX(t){return this.translateOnAxis(gu,t)}translateY(t){return this.translateOnAxis(_u,t)}translateZ(t){return this.translateOnAxis(xu,t)}localToWorld(t){return this.updateWorldMatrix(!0,!1),t.applyMatrix4(this.matrixWorld)}worldToLocal(t){return this.updateWorldMatrix(!0,!1),t.applyMatrix4(Zn.copy(this.matrixWorld).invert())}lookAt(t,e,n){t.isVector3?aa.copy(t):aa.set(t,e,n);let s=this.parent;this.updateWorldMatrix(!0,!1),Ys.setFromMatrixPosition(this.matrixWorld),this.isCamera||this.isLight?Zn.lookAt(Ys,aa,this.up):Zn.lookAt(aa,Ys,this.up),this.quaternion.setFromRotationMatrix(Zn),s&&(Zn.extractRotation(s.matrixWorld),gs.setFromRotationMatrix(Zn),this.quaternion.premultiply(gs.invert()))}add(t){if(arguments.length>1){for(let e=0;e<arguments.length;e++)this.add(arguments[e]);return this}return t===this?(Rt("Object3D.add: object can't be added as a child of itself.",t),this):(t&&t.isObject3D?(t.removeFromParent(),t.parent=this,this.children.push(t),t.dispatchEvent(vu),_s.child=t,this.dispatchEvent(_s),_s.child=null):Rt("Object3D.add: object not an instance of THREE.Object3D.",t),this)}remove(t){if(arguments.length>1){for(let n=0;n<arguments.length;n++)this.remove(arguments[n]);return this}let e=this.children.indexOf(t);return e!==-1&&(t.parent=null,this.children.splice(e,1),t.dispatchEvent(Vm),Ql.child=t,this.dispatchEvent(Ql),Ql.child=null),this}removeFromParent(){let t=this.parent;return t!==null&&t.remove(this),this}clear(){return this.remove(...this.children)}attach(t){return this.updateWorldMatrix(!0,!1),Zn.copy(this.matrixWorld).invert(),t.parent!==null&&(t.parent.updateWorldMatrix(!0,!1),Zn.multiply(t.parent.matrixWorld)),t.applyMatrix4(Zn),t.removeFromParent(),t.parent=this,this.children.push(t),t.updateWorldMatrix(!1,!0),t.dispatchEvent(vu),_s.child=t,this.dispatchEvent(_s),_s.child=null,this}getObjectById(t){return this.getObjectByProperty("id",t)}getObjectByName(t){return this.getObjectByProperty("name",t)}getObjectByProperty(t,e){if(this[t]===e)return this;for(let n=0,s=this.children.length;n<s;n++){let a=this.children[n].getObjectByProperty(t,e);if(a!==void 0)return a}}getObjectsByProperty(t,e,n=[]){this[t]===e&&n.push(this);let s=this.children;for(let r=0,a=s.length;r<a;r++)s[r].getObjectsByProperty(t,e,n);return n}getWorldPosition(t){return this.updateWorldMatrix(!0,!1),t.setFromMatrixPosition(this.matrixWorld)}getWorldQuaternion(t){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Ys,t,km),t}getWorldScale(t){return this.updateWorldMatrix(!0,!1),this.matrixWorld.decompose(Ys,zm,t),t}getWorldDirection(t){this.updateWorldMatrix(!0,!1);let e=this.matrixWorld.elements;return t.set(e[8],e[9],e[10]).normalize()}raycast(){}traverse(t){t(this);let e=this.children;for(let n=0,s=e.length;n<s;n++)e[n].traverse(t)}traverseVisible(t){if(this.visible===!1)return;t(this);let e=this.children;for(let n=0,s=e.length;n<s;n++)e[n].traverseVisible(t)}traverseAncestors(t){let e=this.parent;e!==null&&(t(e),e.traverseAncestors(t))}updateMatrix(){this.matrix.compose(this.position,this.quaternion,this.scale);let t=this.pivot;if(t!==null){let e=t.x,n=t.y,s=t.z,r=this.matrix.elements;r[12]+=e-r[0]*e-r[4]*n-r[8]*s,r[13]+=n-r[1]*e-r[5]*n-r[9]*s,r[14]+=s-r[2]*e-r[6]*n-r[10]*s}this.matrixWorldNeedsUpdate=!0}updateMatrixWorld(t){this.matrixAutoUpdate&&this.updateMatrix(),(this.matrixWorldNeedsUpdate||t)&&(this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),this.matrixWorldNeedsUpdate=!1,t=!0);let e=this.children;for(let n=0,s=e.length;n<s;n++)e[n].updateMatrixWorld(t)}updateWorldMatrix(t,e){let n=this.parent;if(t===!0&&n!==null&&n.updateWorldMatrix(!0,!1),this.matrixAutoUpdate&&this.updateMatrix(),this.matrixWorldAutoUpdate===!0&&(this.parent===null?this.matrixWorld.copy(this.matrix):this.matrixWorld.multiplyMatrices(this.parent.matrixWorld,this.matrix)),e===!0){let s=this.children;for(let r=0,a=s.length;r<a;r++)s[r].updateWorldMatrix(!1,!0)}}toJSON(t){let e=t===void 0||typeof t=="string",n={};e&&(t={geometries:{},materials:{},textures:{},images:{},shapes:{},skeletons:{},animations:{},nodes:{}},n.metadata={version:4.7,type:"Object",generator:"Object3D.toJSON"});let s={};s.uuid=this.uuid,s.type=this.type,this.name!==""&&(s.name=this.name),this.castShadow===!0&&(s.castShadow=!0),this.receiveShadow===!0&&(s.receiveShadow=!0),this.visible===!1&&(s.visible=!1),this.frustumCulled===!1&&(s.frustumCulled=!1),this.renderOrder!==0&&(s.renderOrder=this.renderOrder),this.static!==!1&&(s.static=this.static),Object.keys(this.userData).length>0&&(s.userData=this.userData),s.layers=this.layers.mask,s.matrix=this.matrix.toArray(),s.up=this.up.toArray(),this.pivot!==null&&(s.pivot=this.pivot.toArray()),this.matrixAutoUpdate===!1&&(s.matrixAutoUpdate=!1),this.morphTargetDictionary!==void 0&&(s.morphTargetDictionary=Object.assign({},this.morphTargetDictionary)),this.morphTargetInfluences!==void 0&&(s.morphTargetInfluences=this.morphTargetInfluences.slice()),this.isInstancedMesh&&(s.type="InstancedMesh",s.count=this.count,s.instanceMatrix=this.instanceMatrix.toJSON(),this.instanceColor!==null&&(s.instanceColor=this.instanceColor.toJSON())),this.isBatchedMesh&&(s.type="BatchedMesh",s.perObjectFrustumCulled=this.perObjectFrustumCulled,s.sortObjects=this.sortObjects,s.drawRanges=this._drawRanges,s.reservedRanges=this._reservedRanges,s.geometryInfo=this._geometryInfo.map(o=>({...o,boundingBox:o.boundingBox?o.boundingBox.toJSON():void 0,boundingSphere:o.boundingSphere?o.boundingSphere.toJSON():void 0})),s.instanceInfo=this._instanceInfo.map(o=>({...o})),s.availableInstanceIds=this._availableInstanceIds.slice(),s.availableGeometryIds=this._availableGeometryIds.slice(),s.nextIndexStart=this._nextIndexStart,s.nextVertexStart=this._nextVertexStart,s.geometryCount=this._geometryCount,s.maxInstanceCount=this._maxInstanceCount,s.maxVertexCount=this._maxVertexCount,s.maxIndexCount=this._maxIndexCount,s.geometryInitialized=this._geometryInitialized,s.matricesTexture=this._matricesTexture.toJSON(t),s.indirectTexture=this._indirectTexture.toJSON(t),this._colorsTexture!==null&&(s.colorsTexture=this._colorsTexture.toJSON(t)),this.boundingSphere!==null&&(s.boundingSphere=this.boundingSphere.toJSON()),this.boundingBox!==null&&(s.boundingBox=this.boundingBox.toJSON()));function r(o,l){return o[l.uuid]===void 0&&(o[l.uuid]=l.toJSON(t)),l.uuid}if(this.isScene)this.background&&(this.background.isColor?s.background=this.background.toJSON():this.background.isTexture&&(s.background=this.background.toJSON(t).uuid)),this.environment&&this.environment.isTexture&&this.environment.isRenderTargetTexture!==!0&&(s.environment=this.environment.toJSON(t).uuid);else if(this.isMesh||this.isLine||this.isPoints){s.geometry=r(t.geometries,this.geometry);let o=this.geometry.parameters;if(o!==void 0&&o.shapes!==void 0){let l=o.shapes;if(Array.isArray(l))for(let c=0,h=l.length;c<h;c++){let f=l[c];r(t.shapes,f)}else r(t.shapes,l)}}if(this.isSkinnedMesh&&(s.bindMode=this.bindMode,s.bindMatrix=this.bindMatrix.toArray(),this.skeleton!==void 0&&(r(t.skeletons,this.skeleton),s.skeleton=this.skeleton.uuid)),this.material!==void 0)if(Array.isArray(this.material)){let o=[];for(let l=0,c=this.material.length;l<c;l++)o.push(r(t.materials,this.material[l]));s.material=o}else s.material=r(t.materials,this.material);if(this.children.length>0){s.children=[];for(let o=0;o<this.children.length;o++)s.children.push(this.children[o].toJSON(t).object)}if(this.animations.length>0){s.animations=[];for(let o=0;o<this.animations.length;o++){let l=this.animations[o];s.animations.push(r(t.animations,l))}}if(e){let o=a(t.geometries),l=a(t.materials),c=a(t.textures),h=a(t.images),f=a(t.shapes),u=a(t.skeletons),p=a(t.animations),g=a(t.nodes);o.length>0&&(n.geometries=o),l.length>0&&(n.materials=l),c.length>0&&(n.textures=c),h.length>0&&(n.images=h),f.length>0&&(n.shapes=f),u.length>0&&(n.skeletons=u),p.length>0&&(n.animations=p),g.length>0&&(n.nodes=g)}return n.object=s,n;function a(o){let l=[];for(let c in o){let h=o[c];delete h.metadata,l.push(h)}return l}}clone(t){return new this.constructor().copy(this,t)}copy(t,e=!0){if(this.name=t.name,this.up.copy(t.up),this.position.copy(t.position),this.rotation.order=t.rotation.order,this.quaternion.copy(t.quaternion),this.scale.copy(t.scale),this.pivot=t.pivot!==null?t.pivot.clone():null,this.matrix.copy(t.matrix),this.matrixWorld.copy(t.matrixWorld),this.matrixAutoUpdate=t.matrixAutoUpdate,this.matrixWorldAutoUpdate=t.matrixWorldAutoUpdate,this.matrixWorldNeedsUpdate=t.matrixWorldNeedsUpdate,this.layers.mask=t.layers.mask,this.visible=t.visible,this.castShadow=t.castShadow,this.receiveShadow=t.receiveShadow,this.frustumCulled=t.frustumCulled,this.renderOrder=t.renderOrder,this.static=t.static,this.animations=t.animations.slice(),this.userData=JSON.parse(JSON.stringify(t.userData)),e===!0)for(let n=0;n<t.children.length;n++){let s=t.children[n];this.add(s.clone())}return this}};sn.DEFAULT_UP=new D(0,1,0);sn.DEFAULT_MATRIX_AUTO_UPDATE=!0;sn.DEFAULT_MATRIX_WORLD_AUTO_UPDATE=!0;var Qn=class extends sn{constructor(){super(),this.isGroup=!0,this.type="Group"}},Gm={type:"move"},Rs=class{constructor(){this._targetRay=null,this._grip=null,this._hand=null}getHandSpace(){return this._hand===null&&(this._hand=new Qn,this._hand.matrixAutoUpdate=!1,this._hand.visible=!1,this._hand.joints={},this._hand.inputState={pinching:!1}),this._hand}getTargetRaySpace(){return this._targetRay===null&&(this._targetRay=new Qn,this._targetRay.matrixAutoUpdate=!1,this._targetRay.visible=!1,this._targetRay.hasLinearVelocity=!1,this._targetRay.linearVelocity=new D,this._targetRay.hasAngularVelocity=!1,this._targetRay.angularVelocity=new D),this._targetRay}getGripSpace(){return this._grip===null&&(this._grip=new Qn,this._grip.matrixAutoUpdate=!1,this._grip.visible=!1,this._grip.hasLinearVelocity=!1,this._grip.linearVelocity=new D,this._grip.hasAngularVelocity=!1,this._grip.angularVelocity=new D,this._grip.eventsEnabled=!1),this._grip}dispatchEvent(t){return this._targetRay!==null&&this._targetRay.dispatchEvent(t),this._grip!==null&&this._grip.dispatchEvent(t),this._hand!==null&&this._hand.dispatchEvent(t),this}connect(t){if(t&&t.hand){let e=this._hand;if(e)for(let n of t.hand.values())this._getHandJoint(e,n)}return this.dispatchEvent({type:"connected",data:t}),this}disconnect(t){return this.dispatchEvent({type:"disconnected",data:t}),this._targetRay!==null&&(this._targetRay.visible=!1),this._grip!==null&&(this._grip.visible=!1),this._hand!==null&&(this._hand.visible=!1),this}update(t,e,n){let s=null,r=null,a=null,o=this._targetRay,l=this._grip,c=this._hand;if(t&&e.session.visibilityState!=="visible-blurred"){if(c&&t.hand){a=!0;for(let x of t.hand.values()){let m=e.getJointPose(x,n),d=this._getHandJoint(c,x);m!==null&&(d.matrix.fromArray(m.transform.matrix),d.matrix.decompose(d.position,d.rotation,d.scale),d.matrixWorldNeedsUpdate=!0,d.jointRadius=m.radius),d.visible=m!==null}let h=c.joints["index-finger-tip"],f=c.joints["thumb-tip"],u=h.position.distanceTo(f.position),p=.02,g=.005;c.inputState.pinching&&u>p+g?(c.inputState.pinching=!1,this.dispatchEvent({type:"pinchend",handedness:t.handedness,target:this})):!c.inputState.pinching&&u<=p-g&&(c.inputState.pinching=!0,this.dispatchEvent({type:"pinchstart",handedness:t.handedness,target:this}))}else l!==null&&t.gripSpace&&(r=e.getPose(t.gripSpace,n),r!==null&&(l.matrix.fromArray(r.transform.matrix),l.matrix.decompose(l.position,l.rotation,l.scale),l.matrixWorldNeedsUpdate=!0,r.linearVelocity?(l.hasLinearVelocity=!0,l.linearVelocity.copy(r.linearVelocity)):l.hasLinearVelocity=!1,r.angularVelocity?(l.hasAngularVelocity=!0,l.angularVelocity.copy(r.angularVelocity)):l.hasAngularVelocity=!1,l.eventsEnabled&&l.dispatchEvent({type:"gripUpdated",data:t,target:this})));o!==null&&(s=e.getPose(t.targetRaySpace,n),s===null&&r!==null&&(s=r),s!==null&&(o.matrix.fromArray(s.transform.matrix),o.matrix.decompose(o.position,o.rotation,o.scale),o.matrixWorldNeedsUpdate=!0,s.linearVelocity?(o.hasLinearVelocity=!0,o.linearVelocity.copy(s.linearVelocity)):o.hasLinearVelocity=!1,s.angularVelocity?(o.hasAngularVelocity=!0,o.angularVelocity.copy(s.angularVelocity)):o.hasAngularVelocity=!1,this.dispatchEvent(Gm)))}return o!==null&&(o.visible=s!==null),l!==null&&(l.visible=r!==null),c!==null&&(c.visible=a!==null),this}_getHandJoint(t,e){if(t.joints[e.jointName]===void 0){let n=new Qn;n.matrixAutoUpdate=!1,n.visible=!1,t.joints[e.jointName]=n,t.add(n)}return t.joints[e.jointName]}},gf={aliceblue:15792383,antiquewhite:16444375,aqua:65535,aquamarine:8388564,azure:15794175,beige:16119260,bisque:16770244,black:0,blanchedalmond:16772045,blue:255,blueviolet:9055202,brown:10824234,burlywood:14596231,cadetblue:6266528,chartreuse:8388352,chocolate:13789470,coral:16744272,cornflowerblue:6591981,cornsilk:16775388,crimson:14423100,cyan:65535,darkblue:139,darkcyan:35723,darkgoldenrod:12092939,darkgray:11119017,darkgreen:25600,darkgrey:11119017,darkkhaki:12433259,darkmagenta:9109643,darkolivegreen:5597999,darkorange:16747520,darkorchid:10040012,darkred:9109504,darksalmon:15308410,darkseagreen:9419919,darkslateblue:4734347,darkslategray:3100495,darkslategrey:3100495,darkturquoise:52945,darkviolet:9699539,deeppink:16716947,deepskyblue:49151,dimgray:6908265,dimgrey:6908265,dodgerblue:2003199,firebrick:11674146,floralwhite:16775920,forestgreen:2263842,fuchsia:16711935,gainsboro:14474460,ghostwhite:16316671,gold:16766720,goldenrod:14329120,gray:8421504,green:32768,greenyellow:11403055,grey:8421504,honeydew:15794160,hotpink:16738740,indianred:13458524,indigo:4915330,ivory:16777200,khaki:15787660,lavender:15132410,lavenderblush:16773365,lawngreen:8190976,lemonchiffon:16775885,lightblue:11393254,lightcoral:15761536,lightcyan:14745599,lightgoldenrodyellow:16448210,lightgray:13882323,lightgreen:9498256,lightgrey:13882323,lightpink:16758465,lightsalmon:16752762,lightseagreen:2142890,lightskyblue:8900346,lightslategray:7833753,lightslategrey:7833753,lightsteelblue:11584734,lightyellow:16777184,lime:65280,limegreen:3329330,linen:16445670,magenta:16711935,maroon:8388608,mediumaquamarine:6737322,mediumblue:205,mediumorchid:12211667,mediumpurple:9662683,mediumseagreen:3978097,mediumslateblue:8087790,mediumspringgreen:64154,mediumturquoise:4772300,mediumvioletred:13047173,midnightblue:1644912,mintcream:16121850,mistyrose:16770273,moccasin:16770229,navajowhite:16768685,navy:128,oldlace:16643558,olive:8421376,olivedrab:7048739,orange:16753920,orangered:16729344,orchid:14315734,palegoldenrod:15657130,palegreen:10025880,paleturquoise:11529966,palevioletred:14381203,papayawhip:16773077,peachpuff:16767673,peru:13468991,pink:16761035,plum:14524637,powderblue:11591910,purple:8388736,rebeccapurple:6697881,red:16711680,rosybrown:12357519,royalblue:4286945,saddlebrown:9127187,salmon:16416882,sandybrown:16032864,seagreen:3050327,seashell:16774638,sienna:10506797,silver:12632256,skyblue:8900331,slateblue:6970061,slategray:7372944,slategrey:7372944,snow:16775930,springgreen:65407,steelblue:4620980,tan:13808780,teal:32896,thistle:14204888,tomato:16737095,turquoise:4251856,violet:15631086,wheat:16113331,white:16777215,whitesmoke:16119285,yellow:16776960,yellowgreen:10145074},mi={h:0,s:0,l:0},oa={h:0,s:0,l:0};function tc(i,t,e){return e<0&&(e+=1),e>1&&(e-=1),e<1/6?i+(t-i)*6*e:e<1/2?t:e<2/3?i+(t-i)*6*(2/3-e):i}var ut=class{constructor(t,e,n){return this.isColor=!0,this.r=1,this.g=1,this.b=1,this.set(t,e,n)}set(t,e,n){if(e===void 0&&n===void 0){let s=t;s&&s.isColor?this.copy(s):typeof s=="number"?this.setHex(s):typeof s=="string"&&this.setStyle(s)}else this.setRGB(t,e,n);return this}setScalar(t){return this.r=t,this.g=t,this.b=t,this}setHex(t,e=fn){return t=Math.floor(t),this.r=(t>>16&255)/255,this.g=(t>>8&255)/255,this.b=(t&255)/255,Ht.colorSpaceToWorking(this,e),this}setRGB(t,e,n,s=Ht.workingColorSpace){return this.r=t,this.g=e,this.b=n,Ht.colorSpaceToWorking(this,s),this}setHSL(t,e,n,s=Ht.workingColorSpace){if(t=Lm(t,1),e=Zt(e,0,1),n=Zt(n,0,1),e===0)this.r=this.g=this.b=n;else{let r=n<=.5?n*(1+e):n+e-n*e,a=2*n-r;this.r=tc(a,r,t+1/3),this.g=tc(a,r,t),this.b=tc(a,r,t-1/3)}return Ht.colorSpaceToWorking(this,s),this}setStyle(t,e=fn){function n(r){r!==void 0&&parseFloat(r)<1&&Et("Color: Alpha component of "+t+" will be ignored.")}let s;if(s=/^(\w+)\(([^\)]*)\)/.exec(t)){let r,a=s[1],o=s[2];switch(a){case"rgb":case"rgba":if(r=/^\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(r[4]),this.setRGB(Math.min(255,parseInt(r[1],10))/255,Math.min(255,parseInt(r[2],10))/255,Math.min(255,parseInt(r[3],10))/255,e);if(r=/^\s*(\d+)\%\s*,\s*(\d+)\%\s*,\s*(\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(r[4]),this.setRGB(Math.min(100,parseInt(r[1],10))/100,Math.min(100,parseInt(r[2],10))/100,Math.min(100,parseInt(r[3],10))/100,e);break;case"hsl":case"hsla":if(r=/^\s*(\d*\.?\d+)\s*,\s*(\d*\.?\d+)\%\s*,\s*(\d*\.?\d+)\%\s*(?:,\s*(\d*\.?\d+)\s*)?$/.exec(o))return n(r[4]),this.setHSL(parseFloat(r[1])/360,parseFloat(r[2])/100,parseFloat(r[3])/100,e);break;default:Et("Color: Unknown color model "+t)}}else if(s=/^\#([A-Fa-f\d]+)$/.exec(t)){let r=s[1],a=r.length;if(a===3)return this.setRGB(parseInt(r.charAt(0),16)/15,parseInt(r.charAt(1),16)/15,parseInt(r.charAt(2),16)/15,e);if(a===6)return this.setHex(parseInt(r,16),e);Et("Color: Invalid hex color "+t)}else if(t&&t.length>0)return this.setColorName(t,e);return this}setColorName(t,e=fn){let n=gf[t.toLowerCase()];return n!==void 0?this.setHex(n,e):Et("Color: Unknown color "+t),this}clone(){return new this.constructor(this.r,this.g,this.b)}copy(t){return this.r=t.r,this.g=t.g,this.b=t.b,this}copySRGBToLinear(t){return this.r=ti(t.r),this.g=ti(t.g),this.b=ti(t.b),this}copyLinearToSRGB(t){return this.r=Ts(t.r),this.g=Ts(t.g),this.b=Ts(t.b),this}convertSRGBToLinear(){return this.copySRGBToLinear(this),this}convertLinearToSRGB(){return this.copyLinearToSRGB(this),this}getHex(t=fn){return Ht.workingToColorSpace(We.copy(this),t),Math.round(Zt(We.r*255,0,255))*65536+Math.round(Zt(We.g*255,0,255))*256+Math.round(Zt(We.b*255,0,255))}getHexString(t=fn){return("000000"+this.getHex(t).toString(16)).slice(-6)}getHSL(t,e=Ht.workingColorSpace){Ht.workingToColorSpace(We.copy(this),e);let n=We.r,s=We.g,r=We.b,a=Math.max(n,s,r),o=Math.min(n,s,r),l,c,h=(o+a)/2;if(o===a)l=0,c=0;else{let f=a-o;switch(c=h<=.5?f/(a+o):f/(2-a-o),a){case n:l=(s-r)/f+(s<r?6:0);break;case s:l=(r-n)/f+2;break;case r:l=(n-s)/f+4;break}l/=6}return t.h=l,t.s=c,t.l=h,t}getRGB(t,e=Ht.workingColorSpace){return Ht.workingToColorSpace(We.copy(this),e),t.r=We.r,t.g=We.g,t.b=We.b,t}getStyle(t=fn){Ht.workingToColorSpace(We.copy(this),t);let e=We.r,n=We.g,s=We.b;return t!==fn?`color(${t} ${e.toFixed(3)} ${n.toFixed(3)} ${s.toFixed(3)})`:`rgb(${Math.round(e*255)},${Math.round(n*255)},${Math.round(s*255)})`}offsetHSL(t,e,n){return this.getHSL(mi),this.setHSL(mi.h+t,mi.s+e,mi.l+n)}add(t){return this.r+=t.r,this.g+=t.g,this.b+=t.b,this}addColors(t,e){return this.r=t.r+e.r,this.g=t.g+e.g,this.b=t.b+e.b,this}addScalar(t){return this.r+=t,this.g+=t,this.b+=t,this}sub(t){return this.r=Math.max(0,this.r-t.r),this.g=Math.max(0,this.g-t.g),this.b=Math.max(0,this.b-t.b),this}multiply(t){return this.r*=t.r,this.g*=t.g,this.b*=t.b,this}multiplyScalar(t){return this.r*=t,this.g*=t,this.b*=t,this}lerp(t,e){return this.r+=(t.r-this.r)*e,this.g+=(t.g-this.g)*e,this.b+=(t.b-this.b)*e,this}lerpColors(t,e,n){return this.r=t.r+(e.r-t.r)*n,this.g=t.g+(e.g-t.g)*n,this.b=t.b+(e.b-t.b)*n,this}lerpHSL(t,e){this.getHSL(mi),t.getHSL(oa);let n=Zl(mi.h,oa.h,e),s=Zl(mi.s,oa.s,e),r=Zl(mi.l,oa.l,e);return this.setHSL(n,s,r),this}setFromVector3(t){return this.r=t.x,this.g=t.y,this.b=t.z,this}applyMatrix3(t){let e=this.r,n=this.g,s=this.b,r=t.elements;return this.r=r[0]*e+r[3]*n+r[6]*s,this.g=r[1]*e+r[4]*n+r[7]*s,this.b=r[2]*e+r[5]*n+r[8]*s,this}equals(t){return t.r===this.r&&t.g===this.g&&t.b===this.b}fromArray(t,e=0){return this.r=t[e],this.g=t[e+1],this.b=t[e+2],this}toArray(t=[],e=0){return t[e]=this.r,t[e+1]=this.g,t[e+2]=this.b,t}fromBufferAttribute(t,e){return this.r=t.getX(e),this.g=t.getY(e),this.b=t.getZ(e),this}toJSON(){return this.getHex()}*[Symbol.iterator](){yield this.r,yield this.g,yield this.b}},We=new ut;ut.NAMES=gf;var rr=class extends sn{constructor(){super(),this.isScene=!0,this.type="Scene",this.background=null,this.environment=null,this.fog=null,this.backgroundBlurriness=0,this.backgroundIntensity=1,this.backgroundRotation=new bi,this.environmentIntensity=1,this.environmentRotation=new bi,this.overrideMaterial=null,typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}copy(t,e){return super.copy(t,e),t.background!==null&&(this.background=t.background.clone()),t.environment!==null&&(this.environment=t.environment.clone()),t.fog!==null&&(this.fog=t.fog.clone()),this.backgroundBlurriness=t.backgroundBlurriness,this.backgroundIntensity=t.backgroundIntensity,this.backgroundRotation.copy(t.backgroundRotation),this.environmentIntensity=t.environmentIntensity,this.environmentRotation.copy(t.environmentRotation),t.overrideMaterial!==null&&(this.overrideMaterial=t.overrideMaterial.clone()),this.matrixAutoUpdate=t.matrixAutoUpdate,this}toJSON(t){let e=super.toJSON(t);return this.fog!==null&&(e.object.fog=this.fog.toJSON()),this.backgroundBlurriness>0&&(e.object.backgroundBlurriness=this.backgroundBlurriness),this.backgroundIntensity!==1&&(e.object.backgroundIntensity=this.backgroundIntensity),e.object.backgroundRotation=this.backgroundRotation.toArray(),this.environmentIntensity!==1&&(e.object.environmentIntensity=this.environmentIntensity),e.object.environmentRotation=this.environmentRotation.toArray(),e}},Sn=new D,Jn=new D,ec=new D,$n=new D,xs=new D,vs=new D,yu=new D,nc=new D,ic=new D,sc=new D,rc=new ye,ac=new ye,oc=new ye,yi=class i{constructor(t=new D,e=new D,n=new D){this.a=t,this.b=e,this.c=n}static getNormal(t,e,n,s){s.subVectors(n,e),Sn.subVectors(t,e),s.cross(Sn);let r=s.lengthSq();return r>0?s.multiplyScalar(1/Math.sqrt(r)):s.set(0,0,0)}static getBarycoord(t,e,n,s,r){Sn.subVectors(s,e),Jn.subVectors(n,e),ec.subVectors(t,e);let a=Sn.dot(Sn),o=Sn.dot(Jn),l=Sn.dot(ec),c=Jn.dot(Jn),h=Jn.dot(ec),f=a*c-o*o;if(f===0)return r.set(0,0,0),null;let u=1/f,p=(c*l-o*h)*u,g=(a*h-o*l)*u;return r.set(1-p-g,g,p)}static containsPoint(t,e,n,s){return this.getBarycoord(t,e,n,s,$n)===null?!1:$n.x>=0&&$n.y>=0&&$n.x+$n.y<=1}static getInterpolation(t,e,n,s,r,a,o,l){return this.getBarycoord(t,e,n,s,$n)===null?(l.x=0,l.y=0,"z"in l&&(l.z=0),"w"in l&&(l.w=0),null):(l.setScalar(0),l.addScaledVector(r,$n.x),l.addScaledVector(a,$n.y),l.addScaledVector(o,$n.z),l)}static getInterpolatedAttribute(t,e,n,s,r,a){return rc.setScalar(0),ac.setScalar(0),oc.setScalar(0),rc.fromBufferAttribute(t,e),ac.fromBufferAttribute(t,n),oc.fromBufferAttribute(t,s),a.setScalar(0),a.addScaledVector(rc,r.x),a.addScaledVector(ac,r.y),a.addScaledVector(oc,r.z),a}static isFrontFacing(t,e,n,s){return Sn.subVectors(n,e),Jn.subVectors(t,e),Sn.cross(Jn).dot(s)<0}set(t,e,n){return this.a.copy(t),this.b.copy(e),this.c.copy(n),this}setFromPointsAndIndices(t,e,n,s){return this.a.copy(t[e]),this.b.copy(t[n]),this.c.copy(t[s]),this}setFromAttributeAndIndices(t,e,n,s){return this.a.fromBufferAttribute(t,e),this.b.fromBufferAttribute(t,n),this.c.fromBufferAttribute(t,s),this}clone(){return new this.constructor().copy(this)}copy(t){return this.a.copy(t.a),this.b.copy(t.b),this.c.copy(t.c),this}getArea(){return Sn.subVectors(this.c,this.b),Jn.subVectors(this.a,this.b),Sn.cross(Jn).length()*.5}getMidpoint(t){return t.addVectors(this.a,this.b).add(this.c).multiplyScalar(1/3)}getNormal(t){return i.getNormal(this.a,this.b,this.c,t)}getPlane(t){return t.setFromCoplanarPoints(this.a,this.b,this.c)}getBarycoord(t,e){return i.getBarycoord(t,this.a,this.b,this.c,e)}getInterpolation(t,e,n,s,r){return i.getInterpolation(t,this.a,this.b,this.c,e,n,s,r)}containsPoint(t){return i.containsPoint(t,this.a,this.b,this.c)}isFrontFacing(t){return i.isFrontFacing(this.a,this.b,this.c,t)}intersectsBox(t){return t.intersectsTriangle(this)}closestPointToPoint(t,e){let n=this.a,s=this.b,r=this.c,a,o;xs.subVectors(s,n),vs.subVectors(r,n),nc.subVectors(t,n);let l=xs.dot(nc),c=vs.dot(nc);if(l<=0&&c<=0)return e.copy(n);ic.subVectors(t,s);let h=xs.dot(ic),f=vs.dot(ic);if(h>=0&&f<=h)return e.copy(s);let u=l*f-h*c;if(u<=0&&l>=0&&h<=0)return a=l/(l-h),e.copy(n).addScaledVector(xs,a);sc.subVectors(t,r);let p=xs.dot(sc),g=vs.dot(sc);if(g>=0&&p<=g)return e.copy(r);let x=p*c-l*g;if(x<=0&&c>=0&&g<=0)return o=c/(c-g),e.copy(n).addScaledVector(vs,o);let m=h*g-p*f;if(m<=0&&f-h>=0&&p-g>=0)return yu.subVectors(r,s),o=(f-h)/(f-h+(p-g)),e.copy(s).addScaledVector(yu,o);let d=1/(m+x+u);return a=x*d,o=u*d,e.copy(n).addScaledVector(xs,a).addScaledVector(vs,o)}equals(t){return t.a.equals(this.a)&&t.b.equals(this.b)&&t.c.equals(this.c)}},Si=class{constructor(t=new D(1/0,1/0,1/0),e=new D(-1/0,-1/0,-1/0)){this.isBox3=!0,this.min=t,this.max=e}set(t,e){return this.min.copy(t),this.max.copy(e),this}setFromArray(t){this.makeEmpty();for(let e=0,n=t.length;e<n;e+=3)this.expandByPoint(wn.fromArray(t,e));return this}setFromBufferAttribute(t){this.makeEmpty();for(let e=0,n=t.count;e<n;e++)this.expandByPoint(wn.fromBufferAttribute(t,e));return this}setFromPoints(t){this.makeEmpty();for(let e=0,n=t.length;e<n;e++)this.expandByPoint(t[e]);return this}setFromCenterAndSize(t,e){let n=wn.copy(e).multiplyScalar(.5);return this.min.copy(t).sub(n),this.max.copy(t).add(n),this}setFromObject(t,e=!1){return this.makeEmpty(),this.expandByObject(t,e)}clone(){return new this.constructor().copy(this)}copy(t){return this.min.copy(t.min),this.max.copy(t.max),this}makeEmpty(){return this.min.x=this.min.y=this.min.z=1/0,this.max.x=this.max.y=this.max.z=-1/0,this}isEmpty(){return this.max.x<this.min.x||this.max.y<this.min.y||this.max.z<this.min.z}getCenter(t){return this.isEmpty()?t.set(0,0,0):t.addVectors(this.min,this.max).multiplyScalar(.5)}getSize(t){return this.isEmpty()?t.set(0,0,0):t.subVectors(this.max,this.min)}expandByPoint(t){return this.min.min(t),this.max.max(t),this}expandByVector(t){return this.min.sub(t),this.max.add(t),this}expandByScalar(t){return this.min.addScalar(-t),this.max.addScalar(t),this}expandByObject(t,e=!1){t.updateWorldMatrix(!1,!1);let n=t.geometry;if(n!==void 0){let r=n.getAttribute("position");if(e===!0&&r!==void 0&&t.isInstancedMesh!==!0)for(let a=0,o=r.count;a<o;a++)t.isMesh===!0?t.getVertexPosition(a,wn):wn.fromBufferAttribute(r,a),wn.applyMatrix4(t.matrixWorld),this.expandByPoint(wn);else t.boundingBox!==void 0?(t.boundingBox===null&&t.computeBoundingBox(),la.copy(t.boundingBox)):(n.boundingBox===null&&n.computeBoundingBox(),la.copy(n.boundingBox)),la.applyMatrix4(t.matrixWorld),this.union(la)}let s=t.children;for(let r=0,a=s.length;r<a;r++)this.expandByObject(s[r],e);return this}containsPoint(t){return t.x>=this.min.x&&t.x<=this.max.x&&t.y>=this.min.y&&t.y<=this.max.y&&t.z>=this.min.z&&t.z<=this.max.z}containsBox(t){return this.min.x<=t.min.x&&t.max.x<=this.max.x&&this.min.y<=t.min.y&&t.max.y<=this.max.y&&this.min.z<=t.min.z&&t.max.z<=this.max.z}getParameter(t,e){return e.set((t.x-this.min.x)/(this.max.x-this.min.x),(t.y-this.min.y)/(this.max.y-this.min.y),(t.z-this.min.z)/(this.max.z-this.min.z))}intersectsBox(t){return t.max.x>=this.min.x&&t.min.x<=this.max.x&&t.max.y>=this.min.y&&t.min.y<=this.max.y&&t.max.z>=this.min.z&&t.min.z<=this.max.z}intersectsSphere(t){return this.clampPoint(t.center,wn),wn.distanceToSquared(t.center)<=t.radius*t.radius}intersectsPlane(t){let e,n;return t.normal.x>0?(e=t.normal.x*this.min.x,n=t.normal.x*this.max.x):(e=t.normal.x*this.max.x,n=t.normal.x*this.min.x),t.normal.y>0?(e+=t.normal.y*this.min.y,n+=t.normal.y*this.max.y):(e+=t.normal.y*this.max.y,n+=t.normal.y*this.min.y),t.normal.z>0?(e+=t.normal.z*this.min.z,n+=t.normal.z*this.max.z):(e+=t.normal.z*this.max.z,n+=t.normal.z*this.min.z),e<=-t.constant&&n>=-t.constant}intersectsTriangle(t){if(this.isEmpty())return!1;this.getCenter(Zs),ca.subVectors(this.max,Zs),ys.subVectors(t.a,Zs),Ms.subVectors(t.b,Zs),bs.subVectors(t.c,Zs),gi.subVectors(Ms,ys),_i.subVectors(bs,Ms),Ji.subVectors(ys,bs);let e=[0,-gi.z,gi.y,0,-_i.z,_i.y,0,-Ji.z,Ji.y,gi.z,0,-gi.x,_i.z,0,-_i.x,Ji.z,0,-Ji.x,-gi.y,gi.x,0,-_i.y,_i.x,0,-Ji.y,Ji.x,0];return!lc(e,ys,Ms,bs,ca)||(e=[1,0,0,0,1,0,0,0,1],!lc(e,ys,Ms,bs,ca))?!1:(ha.crossVectors(gi,_i),e=[ha.x,ha.y,ha.z],lc(e,ys,Ms,bs,ca))}clampPoint(t,e){return e.copy(t).clamp(this.min,this.max)}distanceToPoint(t){return this.clampPoint(t,wn).distanceTo(t)}getBoundingSphere(t){return this.isEmpty()?t.makeEmpty():(this.getCenter(t.center),t.radius=this.getSize(wn).length()*.5),t}intersect(t){return this.min.max(t.min),this.max.min(t.max),this.isEmpty()&&this.makeEmpty(),this}union(t){return this.min.min(t.min),this.max.max(t.max),this}applyMatrix4(t){return this.isEmpty()?this:(Kn[0].set(this.min.x,this.min.y,this.min.z).applyMatrix4(t),Kn[1].set(this.min.x,this.min.y,this.max.z).applyMatrix4(t),Kn[2].set(this.min.x,this.max.y,this.min.z).applyMatrix4(t),Kn[3].set(this.min.x,this.max.y,this.max.z).applyMatrix4(t),Kn[4].set(this.max.x,this.min.y,this.min.z).applyMatrix4(t),Kn[5].set(this.max.x,this.min.y,this.max.z).applyMatrix4(t),Kn[6].set(this.max.x,this.max.y,this.min.z).applyMatrix4(t),Kn[7].set(this.max.x,this.max.y,this.max.z).applyMatrix4(t),this.setFromPoints(Kn),this)}translate(t){return this.min.add(t),this.max.add(t),this}equals(t){return t.min.equals(this.min)&&t.max.equals(this.max)}toJSON(){return{min:this.min.toArray(),max:this.max.toArray()}}fromJSON(t){return this.min.fromArray(t.min),this.max.fromArray(t.max),this}},Kn=[new D,new D,new D,new D,new D,new D,new D,new D],wn=new D,la=new Si,ys=new D,Ms=new D,bs=new D,gi=new D,_i=new D,Ji=new D,Zs=new D,ca=new D,ha=new D,$i=new D;function lc(i,t,e,n,s){for(let r=0,a=i.length-3;r<=a;r+=3){$i.fromArray(i,r);let o=s.x*Math.abs($i.x)+s.y*Math.abs($i.y)+s.z*Math.abs($i.z),l=t.dot($i),c=e.dot($i),h=n.dot($i);if(Math.max(-Math.max(l,c,h),Math.min(l,c,h))>o)return!1}return!0}var Ce=new D,ua=new Ut,Hm=0,Lt=class extends kn{constructor(t,e,n=!1){if(super(),Array.isArray(t))throw new TypeError("THREE.BufferAttribute: array should be a Typed Array.");this.isBufferAttribute=!0,Object.defineProperty(this,"id",{value:Hm++}),this.name="",this.array=t,this.itemSize=e,this.count=t!==void 0?t.length/e:0,this.normalized=n,this.usage=bc,this.updateRanges=[],this.gpuType=Cn,this.version=0}onUploadCallback(){}set needsUpdate(t){t===!0&&this.version++}setUsage(t){return this.usage=t,this}addUpdateRange(t,e){this.updateRanges.push({start:t,count:e})}clearUpdateRanges(){this.updateRanges.length=0}copy(t){return this.name=t.name,this.array=new t.array.constructor(t.array),this.itemSize=t.itemSize,this.count=t.count,this.normalized=t.normalized,this.usage=t.usage,this.gpuType=t.gpuType,this}copyAt(t,e,n){t*=this.itemSize,n*=e.itemSize;for(let s=0,r=this.itemSize;s<r;s++)this.array[t+s]=e.array[n+s];return this}copyArray(t){return this.array.set(t),this}applyMatrix3(t){if(this.itemSize===2)for(let e=0,n=this.count;e<n;e++)ua.fromBufferAttribute(this,e),ua.applyMatrix3(t),this.setXY(e,ua.x,ua.y);else if(this.itemSize===3)for(let e=0,n=this.count;e<n;e++)Ce.fromBufferAttribute(this,e),Ce.applyMatrix3(t),this.setXYZ(e,Ce.x,Ce.y,Ce.z);return this}applyMatrix4(t){for(let e=0,n=this.count;e<n;e++)Ce.fromBufferAttribute(this,e),Ce.applyMatrix4(t),this.setXYZ(e,Ce.x,Ce.y,Ce.z);return this}applyNormalMatrix(t){for(let e=0,n=this.count;e<n;e++)Ce.fromBufferAttribute(this,e),Ce.applyNormalMatrix(t),this.setXYZ(e,Ce.x,Ce.y,Ce.z);return this}transformDirection(t){for(let e=0,n=this.count;e<n;e++)Ce.fromBufferAttribute(this,e),Ce.transformDirection(t),this.setXYZ(e,Ce.x,Ce.y,Ce.z);return this}set(t,e=0){return this.array.set(t,e),this}getComponent(t,e){let n=this.array[t*this.itemSize+e];return this.normalized&&(n=qs(n,this.array)),n}setComponent(t,e,n){return this.normalized&&(n=tn(n,this.array)),this.array[t*this.itemSize+e]=n,this}getX(t){let e=this.array[t*this.itemSize];return this.normalized&&(e=qs(e,this.array)),e}setX(t,e){return this.normalized&&(e=tn(e,this.array)),this.array[t*this.itemSize]=e,this}getY(t){let e=this.array[t*this.itemSize+1];return this.normalized&&(e=qs(e,this.array)),e}setY(t,e){return this.normalized&&(e=tn(e,this.array)),this.array[t*this.itemSize+1]=e,this}getZ(t){let e=this.array[t*this.itemSize+2];return this.normalized&&(e=qs(e,this.array)),e}setZ(t,e){return this.normalized&&(e=tn(e,this.array)),this.array[t*this.itemSize+2]=e,this}getW(t){let e=this.array[t*this.itemSize+3];return this.normalized&&(e=qs(e,this.array)),e}setW(t,e){return this.normalized&&(e=tn(e,this.array)),this.array[t*this.itemSize+3]=e,this}setXY(t,e,n){return t*=this.itemSize,this.normalized&&(e=tn(e,this.array),n=tn(n,this.array)),this.array[t+0]=e,this.array[t+1]=n,this}setXYZ(t,e,n,s){return t*=this.itemSize,this.normalized&&(e=tn(e,this.array),n=tn(n,this.array),s=tn(s,this.array)),this.array[t+0]=e,this.array[t+1]=n,this.array[t+2]=s,this}setXYZW(t,e,n,s,r){return t*=this.itemSize,this.normalized&&(e=tn(e,this.array),n=tn(n,this.array),s=tn(s,this.array),r=tn(r,this.array)),this.array[t+0]=e,this.array[t+1]=n,this.array[t+2]=s,this.array[t+3]=r,this}onUpload(t){return this.onUploadCallback=t,this}clone(){return new this.constructor(this.array,this.itemSize).copy(this)}toJSON(){let t={itemSize:this.itemSize,type:this.array.constructor.name,array:Array.from(this.array),normalized:this.normalized};return this.name!==""&&(t.name=this.name),this.usage!==bc&&(t.usage=this.usage),t}dispose(){this.dispatchEvent({type:"dispose"})}};var ar=class extends Lt{constructor(t,e,n){super(new Uint16Array(t),e,n)}};var or=class extends Lt{constructor(t,e,n){super(new Uint32Array(t),e,n)}};var ke=class extends Lt{constructor(t,e,n){super(new Float32Array(t),e,n)}},Wm=new Si,Js=new D,cc=new D,wi=class{constructor(t=new D,e=-1){this.isSphere=!0,this.center=t,this.radius=e}set(t,e){return this.center.copy(t),this.radius=e,this}setFromPoints(t,e){let n=this.center;e!==void 0?n.copy(e):Wm.setFromPoints(t).getCenter(n);let s=0;for(let r=0,a=t.length;r<a;r++)s=Math.max(s,n.distanceToSquared(t[r]));return this.radius=Math.sqrt(s),this}copy(t){return this.center.copy(t.center),this.radius=t.radius,this}isEmpty(){return this.radius<0}makeEmpty(){return this.center.set(0,0,0),this.radius=-1,this}containsPoint(t){return t.distanceToSquared(this.center)<=this.radius*this.radius}distanceToPoint(t){return t.distanceTo(this.center)-this.radius}intersectsSphere(t){let e=this.radius+t.radius;return t.center.distanceToSquared(this.center)<=e*e}intersectsBox(t){return t.intersectsSphere(this)}intersectsPlane(t){return Math.abs(t.distanceToPoint(this.center))<=this.radius}clampPoint(t,e){let n=this.center.distanceToSquared(t);return e.copy(t),n>this.radius*this.radius&&(e.sub(this.center).normalize(),e.multiplyScalar(this.radius).add(this.center)),e}getBoundingBox(t){return this.isEmpty()?(t.makeEmpty(),t):(t.set(this.center,this.center),t.expandByScalar(this.radius),t)}applyMatrix4(t){return this.center.applyMatrix4(t),this.radius=this.radius*t.getMaxScaleOnAxis(),this}translate(t){return this.center.add(t),this}expandByPoint(t){if(this.isEmpty())return this.center.copy(t),this.radius=0,this;Js.subVectors(t,this.center);let e=Js.lengthSq();if(e>this.radius*this.radius){let n=Math.sqrt(e),s=(n-this.radius)*.5;this.center.addScaledVector(Js,s/n),this.radius+=s}return this}union(t){return t.isEmpty()?this:this.isEmpty()?(this.copy(t),this):(this.center.equals(t.center)===!0?this.radius=Math.max(this.radius,t.radius):(cc.subVectors(t.center,this.center).setLength(t.radius),this.expandByPoint(Js.copy(t.center).add(cc)),this.expandByPoint(Js.copy(t.center).sub(cc))),this)}equals(t){return t.center.equals(this.center)&&t.radius===this.radius}clone(){return new this.constructor().copy(this)}toJSON(){return{radius:this.radius,center:this.center.toArray()}}fromJSON(t){return this.radius=t.radius,this.center.fromArray(t.center),this}},Xm=0,xn=new ve,hc=new sn,Ss=new D,un=new Si,$s=new Si,Ue=new D,Qt=class i extends kn{constructor(){super(),this.isBufferGeometry=!0,Object.defineProperty(this,"id",{value:Xm++}),this.uuid=Ir(),this.name="",this.type="BufferGeometry",this.index=null,this.indirect=null,this.indirectOffset=0,this.attributes={},this.morphAttributes={},this.morphTargetsRelative=!1,this.groups=[],this.boundingBox=null,this.boundingSphere=null,this.drawRange={start:0,count:1/0},this.userData={}}getIndex(){return this.index}setIndex(t){return Array.isArray(t)?this.index=new(Pm(t)?or:ar)(t,1):this.index=t,this}setIndirect(t,e=0){return this.indirect=t,this.indirectOffset=e,this}getIndirect(){return this.indirect}getAttribute(t){return this.attributes[t]}setAttribute(t,e){return this.attributes[t]=e,this}deleteAttribute(t){return delete this.attributes[t],this}hasAttribute(t){return this.attributes[t]!==void 0}addGroup(t,e,n=0){this.groups.push({start:t,count:e,materialIndex:n})}clearGroups(){this.groups=[]}setDrawRange(t,e){this.drawRange.start=t,this.drawRange.count=e}applyMatrix4(t){let e=this.attributes.position;e!==void 0&&(e.applyMatrix4(t),e.needsUpdate=!0);let n=this.attributes.normal;if(n!==void 0){let r=new Dt().getNormalMatrix(t);n.applyNormalMatrix(r),n.needsUpdate=!0}let s=this.attributes.tangent;return s!==void 0&&(s.transformDirection(t),s.needsUpdate=!0),this.boundingBox!==null&&this.computeBoundingBox(),this.boundingSphere!==null&&this.computeBoundingSphere(),this}applyQuaternion(t){return xn.makeRotationFromQuaternion(t),this.applyMatrix4(xn),this}rotateX(t){return xn.makeRotationX(t),this.applyMatrix4(xn),this}rotateY(t){return xn.makeRotationY(t),this.applyMatrix4(xn),this}rotateZ(t){return xn.makeRotationZ(t),this.applyMatrix4(xn),this}translate(t,e,n){return xn.makeTranslation(t,e,n),this.applyMatrix4(xn),this}scale(t,e,n){return xn.makeScale(t,e,n),this.applyMatrix4(xn),this}lookAt(t){return hc.lookAt(t),hc.updateMatrix(),this.applyMatrix4(hc.matrix),this}center(){return this.computeBoundingBox(),this.boundingBox.getCenter(Ss).negate(),this.translate(Ss.x,Ss.y,Ss.z),this}setFromPoints(t){let e=this.getAttribute("position");if(e===void 0){let n=[];for(let s=0,r=t.length;s<r;s++){let a=t[s];n.push(a.x,a.y,a.z||0)}this.setAttribute("position",new ke(n,3))}else{let n=Math.min(t.length,e.count);for(let s=0;s<n;s++){let r=t[s];e.setXYZ(s,r.x,r.y,r.z||0)}t.length>e.count&&Et("BufferGeometry: Buffer size too small for points data. Use .dispose() and create a new geometry."),e.needsUpdate=!0}return this}computeBoundingBox(){this.boundingBox===null&&(this.boundingBox=new Si);let t=this.attributes.position,e=this.morphAttributes.position;if(t&&t.isGLBufferAttribute){Rt("BufferGeometry.computeBoundingBox(): GLBufferAttribute requires a manual bounding box.",this),this.boundingBox.set(new D(-1/0,-1/0,-1/0),new D(1/0,1/0,1/0));return}if(t!==void 0){if(this.boundingBox.setFromBufferAttribute(t),e)for(let n=0,s=e.length;n<s;n++){let r=e[n];un.setFromBufferAttribute(r),this.morphTargetsRelative?(Ue.addVectors(this.boundingBox.min,un.min),this.boundingBox.expandByPoint(Ue),Ue.addVectors(this.boundingBox.max,un.max),this.boundingBox.expandByPoint(Ue)):(this.boundingBox.expandByPoint(un.min),this.boundingBox.expandByPoint(un.max))}}else this.boundingBox.makeEmpty();(isNaN(this.boundingBox.min.x)||isNaN(this.boundingBox.min.y)||isNaN(this.boundingBox.min.z))&&Rt('BufferGeometry.computeBoundingBox(): Computed min/max have NaN values. The "position" attribute is likely to have NaN values.',this)}computeBoundingSphere(){this.boundingSphere===null&&(this.boundingSphere=new wi);let t=this.attributes.position,e=this.morphAttributes.position;if(t&&t.isGLBufferAttribute){Rt("BufferGeometry.computeBoundingSphere(): GLBufferAttribute requires a manual bounding sphere.",this),this.boundingSphere.set(new D,1/0);return}if(t){let n=this.boundingSphere.center;if(un.setFromBufferAttribute(t),e)for(let r=0,a=e.length;r<a;r++){let o=e[r];$s.setFromBufferAttribute(o),this.morphTargetsRelative?(Ue.addVectors(un.min,$s.min),un.expandByPoint(Ue),Ue.addVectors(un.max,$s.max),un.expandByPoint(Ue)):(un.expandByPoint($s.min),un.expandByPoint($s.max))}un.getCenter(n);let s=0;for(let r=0,a=t.count;r<a;r++)Ue.fromBufferAttribute(t,r),s=Math.max(s,n.distanceToSquared(Ue));if(e)for(let r=0,a=e.length;r<a;r++){let o=e[r],l=this.morphTargetsRelative;for(let c=0,h=o.count;c<h;c++)Ue.fromBufferAttribute(o,c),l&&(Ss.fromBufferAttribute(t,c),Ue.add(Ss)),s=Math.max(s,n.distanceToSquared(Ue))}this.boundingSphere.radius=Math.sqrt(s),isNaN(this.boundingSphere.radius)&&Rt('BufferGeometry.computeBoundingSphere(): Computed radius is NaN. The "position" attribute is likely to have NaN values.',this)}}computeTangents(){let t=this.index,e=this.attributes;if(t===null||e.position===void 0||e.normal===void 0||e.uv===void 0){Rt("BufferGeometry: .computeTangents() failed. Missing required attributes (index, position, normal or uv)");return}let n=e.position,s=e.normal,r=e.uv;this.hasAttribute("tangent")===!1&&this.setAttribute("tangent",new Lt(new Float32Array(4*n.count),4));let a=this.getAttribute("tangent"),o=[],l=[];for(let v=0;v<n.count;v++)o[v]=new D,l[v]=new D;let c=new D,h=new D,f=new D,u=new Ut,p=new Ut,g=new Ut,x=new D,m=new D;function d(v,E,I){c.fromBufferAttribute(n,v),h.fromBufferAttribute(n,E),f.fromBufferAttribute(n,I),u.fromBufferAttribute(r,v),p.fromBufferAttribute(r,E),g.fromBufferAttribute(r,I),h.sub(c),f.sub(c),p.sub(u),g.sub(u);let C=1/(p.x*g.y-g.x*p.y);isFinite(C)&&(x.copy(h).multiplyScalar(g.y).addScaledVector(f,-p.y).multiplyScalar(C),m.copy(f).multiplyScalar(p.x).addScaledVector(h,-g.x).multiplyScalar(C),o[v].add(x),o[E].add(x),o[I].add(x),l[v].add(m),l[E].add(m),l[I].add(m))}let y=this.groups;y.length===0&&(y=[{start:0,count:t.count}]);for(let v=0,E=y.length;v<E;++v){let I=y[v],C=I.start,N=I.count;for(let H=C,W=C+N;H<W;H+=3)d(t.getX(H+0),t.getX(H+1),t.getX(H+2))}let S=new D,b=new D,T=new D,w=new D;function R(v){T.fromBufferAttribute(s,v),w.copy(T);let E=o[v];S.copy(E),S.sub(T.multiplyScalar(T.dot(E))).normalize(),b.crossVectors(w,E);let C=b.dot(l[v])<0?-1:1;a.setXYZW(v,S.x,S.y,S.z,C)}for(let v=0,E=y.length;v<E;++v){let I=y[v],C=I.start,N=I.count;for(let H=C,W=C+N;H<W;H+=3)R(t.getX(H+0)),R(t.getX(H+1)),R(t.getX(H+2))}}computeVertexNormals(){let t=this.index,e=this.getAttribute("position");if(e!==void 0){let n=this.getAttribute("normal");if(n===void 0)n=new Lt(new Float32Array(e.count*3),3),this.setAttribute("normal",n);else for(let u=0,p=n.count;u<p;u++)n.setXYZ(u,0,0,0);let s=new D,r=new D,a=new D,o=new D,l=new D,c=new D,h=new D,f=new D;if(t)for(let u=0,p=t.count;u<p;u+=3){let g=t.getX(u+0),x=t.getX(u+1),m=t.getX(u+2);s.fromBufferAttribute(e,g),r.fromBufferAttribute(e,x),a.fromBufferAttribute(e,m),h.subVectors(a,r),f.subVectors(s,r),h.cross(f),o.fromBufferAttribute(n,g),l.fromBufferAttribute(n,x),c.fromBufferAttribute(n,m),o.add(h),l.add(h),c.add(h),n.setXYZ(g,o.x,o.y,o.z),n.setXYZ(x,l.x,l.y,l.z),n.setXYZ(m,c.x,c.y,c.z)}else for(let u=0,p=e.count;u<p;u+=3)s.fromBufferAttribute(e,u+0),r.fromBufferAttribute(e,u+1),a.fromBufferAttribute(e,u+2),h.subVectors(a,r),f.subVectors(s,r),h.cross(f),n.setXYZ(u+0,h.x,h.y,h.z),n.setXYZ(u+1,h.x,h.y,h.z),n.setXYZ(u+2,h.x,h.y,h.z);this.normalizeNormals(),n.needsUpdate=!0}}normalizeNormals(){let t=this.attributes.normal;for(let e=0,n=t.count;e<n;e++)Ue.fromBufferAttribute(t,e),Ue.normalize(),t.setXYZ(e,Ue.x,Ue.y,Ue.z)}toNonIndexed(){function t(o,l){let c=o.array,h=o.itemSize,f=o.normalized,u=new c.constructor(l.length*h),p=0,g=0;for(let x=0,m=l.length;x<m;x++){o.isInterleavedBufferAttribute?p=l[x]*o.data.stride+o.offset:p=l[x]*h;for(let d=0;d<h;d++)u[g++]=c[p++]}return new Lt(u,h,f)}if(this.index===null)return Et("BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed."),this;let e=new i,n=this.index.array,s=this.attributes;for(let o in s){let l=s[o],c=t(l,n);e.setAttribute(o,c)}let r=this.morphAttributes;for(let o in r){let l=[],c=r[o];for(let h=0,f=c.length;h<f;h++){let u=c[h],p=t(u,n);l.push(p)}e.morphAttributes[o]=l}e.morphTargetsRelative=this.morphTargetsRelative;let a=this.groups;for(let o=0,l=a.length;o<l;o++){let c=a[o];e.addGroup(c.start,c.count,c.materialIndex)}return e}toJSON(){let t={metadata:{version:4.7,type:"BufferGeometry",generator:"BufferGeometry.toJSON"}};if(t.uuid=this.uuid,t.type=this.type,this.name!==""&&(t.name=this.name),Object.keys(this.userData).length>0&&(t.userData=this.userData),this.parameters!==void 0){let l=this.parameters;for(let c in l)l[c]!==void 0&&(t[c]=l[c]);return t}t.data={attributes:{}};let e=this.index;e!==null&&(t.data.index={type:e.array.constructor.name,array:Array.prototype.slice.call(e.array)});let n=this.attributes;for(let l in n){let c=n[l];t.data.attributes[l]=c.toJSON(t.data)}let s={},r=!1;for(let l in this.morphAttributes){let c=this.morphAttributes[l],h=[];for(let f=0,u=c.length;f<u;f++){let p=c[f];h.push(p.toJSON(t.data))}h.length>0&&(s[l]=h,r=!0)}r&&(t.data.morphAttributes=s,t.data.morphTargetsRelative=this.morphTargetsRelative);let a=this.groups;a.length>0&&(t.data.groups=JSON.parse(JSON.stringify(a)));let o=this.boundingSphere;return o!==null&&(t.data.boundingSphere=o.toJSON()),t}clone(){return new this.constructor().copy(this)}copy(t){this.index=null,this.attributes={},this.morphAttributes={},this.groups=[],this.boundingBox=null,this.boundingSphere=null;let e={};this.name=t.name;let n=t.index;n!==null&&this.setIndex(n.clone());let s=t.attributes;for(let c in s){let h=s[c];this.setAttribute(c,h.clone(e))}let r=t.morphAttributes;for(let c in r){let h=[],f=r[c];for(let u=0,p=f.length;u<p;u++)h.push(f[u].clone(e));this.morphAttributes[c]=h}this.morphTargetsRelative=t.morphTargetsRelative;let a=t.groups;for(let c=0,h=a.length;c<h;c++){let f=a[c];this.addGroup(f.start,f.count,f.materialIndex)}let o=t.boundingBox;o!==null&&(this.boundingBox=o.clone());let l=t.boundingSphere;return l!==null&&(this.boundingSphere=l.clone()),this.drawRange.start=t.drawRange.start,this.drawRange.count=t.drawRange.count,this.userData=t.userData,this}dispose(){this.dispatchEvent({type:"dispose"})}};var qm=0,ni=class extends kn{constructor(){super(),this.isMaterial=!0,Object.defineProperty(this,"id",{value:qm++}),this.uuid=Ir(),this.name="",this.type="Material",this.blending=On,this.side=ei,this.vertexColors=!1,this.opacity=1,this.transparent=!1,this.alphaHash=!1,this.blendSrc=Pa,this.blendDst=Ia,this.blendEquation=Mi,this.blendSrcAlpha=null,this.blendDstAlpha=null,this.blendEquationAlpha=null,this.blendColor=new ut(0,0,0),this.blendAlpha=0,this.depthFunc=ts,this.depthTest=!0,this.depthWrite=!0,this.stencilWriteMask=255,this.stencilFunc=Mc,this.stencilRef=0,this.stencilFuncMask=255,this.stencilFail=Qi,this.stencilZFail=Qi,this.stencilZPass=Qi,this.stencilWrite=!1,this.clippingPlanes=null,this.clipIntersection=!1,this.clipShadows=!1,this.shadowSide=null,this.colorWrite=!0,this.precision=null,this.polygonOffset=!1,this.polygonOffsetFactor=0,this.polygonOffsetUnits=0,this.dithering=!1,this.alphaToCoverage=!1,this.premultipliedAlpha=!1,this.forceSinglePass=!1,this.allowOverride=!0,this.visible=!0,this.toneMapped=!0,this.userData={},this.version=0,this._alphaTest=0}get alphaTest(){return this._alphaTest}set alphaTest(t){this._alphaTest>0!=t>0&&this.version++,this._alphaTest=t}onBeforeRender(){}onBeforeCompile(){}customProgramCacheKey(){return this.onBeforeCompile.toString()}setValues(t){if(t!==void 0)for(let e in t){let n=t[e];if(n===void 0){Et(`Material: parameter '${e}' has value of undefined.`);continue}let s=this[e];if(s===void 0){Et(`Material: '${e}' is not a property of THREE.${this.type}.`);continue}s&&s.isColor?s.set(n):s&&s.isVector3&&n&&n.isVector3?s.copy(n):this[e]=n}}toJSON(t){let e=t===void 0||typeof t=="string";e&&(t={textures:{},images:{}});let n={metadata:{version:4.7,type:"Material",generator:"Material.toJSON"}};n.uuid=this.uuid,n.type=this.type,this.name!==""&&(n.name=this.name),this.color&&this.color.isColor&&(n.color=this.color.getHex()),this.roughness!==void 0&&(n.roughness=this.roughness),this.metalness!==void 0&&(n.metalness=this.metalness),this.sheen!==void 0&&(n.sheen=this.sheen),this.sheenColor&&this.sheenColor.isColor&&(n.sheenColor=this.sheenColor.getHex()),this.sheenRoughness!==void 0&&(n.sheenRoughness=this.sheenRoughness),this.emissive&&this.emissive.isColor&&(n.emissive=this.emissive.getHex()),this.emissiveIntensity!==void 0&&this.emissiveIntensity!==1&&(n.emissiveIntensity=this.emissiveIntensity),this.specular&&this.specular.isColor&&(n.specular=this.specular.getHex()),this.specularIntensity!==void 0&&(n.specularIntensity=this.specularIntensity),this.specularColor&&this.specularColor.isColor&&(n.specularColor=this.specularColor.getHex()),this.shininess!==void 0&&(n.shininess=this.shininess),this.clearcoat!==void 0&&(n.clearcoat=this.clearcoat),this.clearcoatRoughness!==void 0&&(n.clearcoatRoughness=this.clearcoatRoughness),this.clearcoatMap&&this.clearcoatMap.isTexture&&(n.clearcoatMap=this.clearcoatMap.toJSON(t).uuid),this.clearcoatRoughnessMap&&this.clearcoatRoughnessMap.isTexture&&(n.clearcoatRoughnessMap=this.clearcoatRoughnessMap.toJSON(t).uuid),this.clearcoatNormalMap&&this.clearcoatNormalMap.isTexture&&(n.clearcoatNormalMap=this.clearcoatNormalMap.toJSON(t).uuid,n.clearcoatNormalScale=this.clearcoatNormalScale.toArray()),this.sheenColorMap&&this.sheenColorMap.isTexture&&(n.sheenColorMap=this.sheenColorMap.toJSON(t).uuid),this.sheenRoughnessMap&&this.sheenRoughnessMap.isTexture&&(n.sheenRoughnessMap=this.sheenRoughnessMap.toJSON(t).uuid),this.dispersion!==void 0&&(n.dispersion=this.dispersion),this.iridescence!==void 0&&(n.iridescence=this.iridescence),this.iridescenceIOR!==void 0&&(n.iridescenceIOR=this.iridescenceIOR),this.iridescenceThicknessRange!==void 0&&(n.iridescenceThicknessRange=this.iridescenceThicknessRange),this.iridescenceMap&&this.iridescenceMap.isTexture&&(n.iridescenceMap=this.iridescenceMap.toJSON(t).uuid),this.iridescenceThicknessMap&&this.iridescenceThicknessMap.isTexture&&(n.iridescenceThicknessMap=this.iridescenceThicknessMap.toJSON(t).uuid),this.anisotropy!==void 0&&(n.anisotropy=this.anisotropy),this.anisotropyRotation!==void 0&&(n.anisotropyRotation=this.anisotropyRotation),this.anisotropyMap&&this.anisotropyMap.isTexture&&(n.anisotropyMap=this.anisotropyMap.toJSON(t).uuid),this.map&&this.map.isTexture&&(n.map=this.map.toJSON(t).uuid),this.matcap&&this.matcap.isTexture&&(n.matcap=this.matcap.toJSON(t).uuid),this.alphaMap&&this.alphaMap.isTexture&&(n.alphaMap=this.alphaMap.toJSON(t).uuid),this.lightMap&&this.lightMap.isTexture&&(n.lightMap=this.lightMap.toJSON(t).uuid,n.lightMapIntensity=this.lightMapIntensity),this.aoMap&&this.aoMap.isTexture&&(n.aoMap=this.aoMap.toJSON(t).uuid,n.aoMapIntensity=this.aoMapIntensity),this.bumpMap&&this.bumpMap.isTexture&&(n.bumpMap=this.bumpMap.toJSON(t).uuid,n.bumpScale=this.bumpScale),this.normalMap&&this.normalMap.isTexture&&(n.normalMap=this.normalMap.toJSON(t).uuid,n.normalMapType=this.normalMapType,n.normalScale=this.normalScale.toArray()),this.displacementMap&&this.displacementMap.isTexture&&(n.displacementMap=this.displacementMap.toJSON(t).uuid,n.displacementScale=this.displacementScale,n.displacementBias=this.displacementBias),this.roughnessMap&&this.roughnessMap.isTexture&&(n.roughnessMap=this.roughnessMap.toJSON(t).uuid),this.metalnessMap&&this.metalnessMap.isTexture&&(n.metalnessMap=this.metalnessMap.toJSON(t).uuid),this.emissiveMap&&this.emissiveMap.isTexture&&(n.emissiveMap=this.emissiveMap.toJSON(t).uuid),this.specularMap&&this.specularMap.isTexture&&(n.specularMap=this.specularMap.toJSON(t).uuid),this.specularIntensityMap&&this.specularIntensityMap.isTexture&&(n.specularIntensityMap=this.specularIntensityMap.toJSON(t).uuid),this.specularColorMap&&this.specularColorMap.isTexture&&(n.specularColorMap=this.specularColorMap.toJSON(t).uuid),this.envMap&&this.envMap.isTexture&&(n.envMap=this.envMap.toJSON(t).uuid,this.combine!==void 0&&(n.combine=this.combine)),this.envMapRotation!==void 0&&(n.envMapRotation=this.envMapRotation.toArray()),this.envMapIntensity!==void 0&&(n.envMapIntensity=this.envMapIntensity),this.reflectivity!==void 0&&(n.reflectivity=this.reflectivity),this.refractionRatio!==void 0&&(n.refractionRatio=this.refractionRatio),this.gradientMap&&this.gradientMap.isTexture&&(n.gradientMap=this.gradientMap.toJSON(t).uuid),this.transmission!==void 0&&(n.transmission=this.transmission),this.transmissionMap&&this.transmissionMap.isTexture&&(n.transmissionMap=this.transmissionMap.toJSON(t).uuid),this.thickness!==void 0&&(n.thickness=this.thickness),this.thicknessMap&&this.thicknessMap.isTexture&&(n.thicknessMap=this.thicknessMap.toJSON(t).uuid),this.attenuationDistance!==void 0&&this.attenuationDistance!==1/0&&(n.attenuationDistance=this.attenuationDistance),this.attenuationColor!==void 0&&(n.attenuationColor=this.attenuationColor.getHex()),this.size!==void 0&&(n.size=this.size),this.shadowSide!==null&&(n.shadowSide=this.shadowSide),this.sizeAttenuation!==void 0&&(n.sizeAttenuation=this.sizeAttenuation),this.blending!==On&&(n.blending=this.blending),this.side!==ei&&(n.side=this.side),this.vertexColors===!0&&(n.vertexColors=!0),this.opacity<1&&(n.opacity=this.opacity),this.transparent===!0&&(n.transparent=!0),this.blendSrc!==Pa&&(n.blendSrc=this.blendSrc),this.blendDst!==Ia&&(n.blendDst=this.blendDst),this.blendEquation!==Mi&&(n.blendEquation=this.blendEquation),this.blendSrcAlpha!==null&&(n.blendSrcAlpha=this.blendSrcAlpha),this.blendDstAlpha!==null&&(n.blendDstAlpha=this.blendDstAlpha),this.blendEquationAlpha!==null&&(n.blendEquationAlpha=this.blendEquationAlpha),this.blendColor&&this.blendColor.isColor&&(n.blendColor=this.blendColor.getHex()),this.blendAlpha!==0&&(n.blendAlpha=this.blendAlpha),this.depthFunc!==ts&&(n.depthFunc=this.depthFunc),this.depthTest===!1&&(n.depthTest=this.depthTest),this.depthWrite===!1&&(n.depthWrite=this.depthWrite),this.colorWrite===!1&&(n.colorWrite=this.colorWrite),this.stencilWriteMask!==255&&(n.stencilWriteMask=this.stencilWriteMask),this.stencilFunc!==Mc&&(n.stencilFunc=this.stencilFunc),this.stencilRef!==0&&(n.stencilRef=this.stencilRef),this.stencilFuncMask!==255&&(n.stencilFuncMask=this.stencilFuncMask),this.stencilFail!==Qi&&(n.stencilFail=this.stencilFail),this.stencilZFail!==Qi&&(n.stencilZFail=this.stencilZFail),this.stencilZPass!==Qi&&(n.stencilZPass=this.stencilZPass),this.stencilWrite===!0&&(n.stencilWrite=this.stencilWrite),this.rotation!==void 0&&this.rotation!==0&&(n.rotation=this.rotation),this.polygonOffset===!0&&(n.polygonOffset=!0),this.polygonOffsetFactor!==0&&(n.polygonOffsetFactor=this.polygonOffsetFactor),this.polygonOffsetUnits!==0&&(n.polygonOffsetUnits=this.polygonOffsetUnits),this.linewidth!==void 0&&this.linewidth!==1&&(n.linewidth=this.linewidth),this.dashSize!==void 0&&(n.dashSize=this.dashSize),this.gapSize!==void 0&&(n.gapSize=this.gapSize),this.scale!==void 0&&(n.scale=this.scale),this.dithering===!0&&(n.dithering=!0),this.alphaTest>0&&(n.alphaTest=this.alphaTest),this.alphaHash===!0&&(n.alphaHash=!0),this.alphaToCoverage===!0&&(n.alphaToCoverage=!0),this.premultipliedAlpha===!0&&(n.premultipliedAlpha=!0),this.forceSinglePass===!0&&(n.forceSinglePass=!0),this.allowOverride===!1&&(n.allowOverride=!1),this.wireframe===!0&&(n.wireframe=!0),this.wireframeLinewidth>1&&(n.wireframeLinewidth=this.wireframeLinewidth),this.wireframeLinecap!=="round"&&(n.wireframeLinecap=this.wireframeLinecap),this.wireframeLinejoin!=="round"&&(n.wireframeLinejoin=this.wireframeLinejoin),this.flatShading===!0&&(n.flatShading=!0),this.visible===!1&&(n.visible=!1),this.toneMapped===!1&&(n.toneMapped=!1),this.fog===!1&&(n.fog=!1),Object.keys(this.userData).length>0&&(n.userData=this.userData);function s(r){let a=[];for(let o in r){let l=r[o];delete l.metadata,a.push(l)}return a}if(e){let r=s(t.textures),a=s(t.images);r.length>0&&(n.textures=r),a.length>0&&(n.images=a)}return n}clone(){return new this.constructor().copy(this)}copy(t){this.name=t.name,this.blending=t.blending,this.side=t.side,this.vertexColors=t.vertexColors,this.opacity=t.opacity,this.transparent=t.transparent,this.blendSrc=t.blendSrc,this.blendDst=t.blendDst,this.blendEquation=t.blendEquation,this.blendSrcAlpha=t.blendSrcAlpha,this.blendDstAlpha=t.blendDstAlpha,this.blendEquationAlpha=t.blendEquationAlpha,this.blendColor.copy(t.blendColor),this.blendAlpha=t.blendAlpha,this.depthFunc=t.depthFunc,this.depthTest=t.depthTest,this.depthWrite=t.depthWrite,this.stencilWriteMask=t.stencilWriteMask,this.stencilFunc=t.stencilFunc,this.stencilRef=t.stencilRef,this.stencilFuncMask=t.stencilFuncMask,this.stencilFail=t.stencilFail,this.stencilZFail=t.stencilZFail,this.stencilZPass=t.stencilZPass,this.stencilWrite=t.stencilWrite;let e=t.clippingPlanes,n=null;if(e!==null){let s=e.length;n=new Array(s);for(let r=0;r!==s;++r)n[r]=e[r].clone()}return this.clippingPlanes=n,this.clipIntersection=t.clipIntersection,this.clipShadows=t.clipShadows,this.shadowSide=t.shadowSide,this.colorWrite=t.colorWrite,this.precision=t.precision,this.polygonOffset=t.polygonOffset,this.polygonOffsetFactor=t.polygonOffsetFactor,this.polygonOffsetUnits=t.polygonOffsetUnits,this.dithering=t.dithering,this.alphaTest=t.alphaTest,this.alphaHash=t.alphaHash,this.alphaToCoverage=t.alphaToCoverage,this.premultipliedAlpha=t.premultipliedAlpha,this.forceSinglePass=t.forceSinglePass,this.allowOverride=t.allowOverride,this.visible=t.visible,this.toneMapped=t.toneMapped,this.userData=JSON.parse(JSON.stringify(t.userData)),this}dispose(){this.dispatchEvent({type:"dispose"})}set needsUpdate(t){t===!0&&this.version++}};var jn=new D,uc=new D,fa=new D,xi=new D,fc=new D,da=new D,dc=new D,Ps=class{constructor(t=new D,e=new D(0,0,-1)){this.origin=t,this.direction=e}set(t,e){return this.origin.copy(t),this.direction.copy(e),this}copy(t){return this.origin.copy(t.origin),this.direction.copy(t.direction),this}at(t,e){return e.copy(this.origin).addScaledVector(this.direction,t)}lookAt(t){return this.direction.copy(t).sub(this.origin).normalize(),this}recast(t){return this.origin.copy(this.at(t,jn)),this}closestPointToPoint(t,e){e.subVectors(t,this.origin);let n=e.dot(this.direction);return n<0?e.copy(this.origin):e.copy(this.origin).addScaledVector(this.direction,n)}distanceToPoint(t){return Math.sqrt(this.distanceSqToPoint(t))}distanceSqToPoint(t){let e=jn.subVectors(t,this.origin).dot(this.direction);return e<0?this.origin.distanceToSquared(t):(jn.copy(this.origin).addScaledVector(this.direction,e),jn.distanceToSquared(t))}distanceSqToSegment(t,e,n,s){uc.copy(t).add(e).multiplyScalar(.5),fa.copy(e).sub(t).normalize(),xi.copy(this.origin).sub(uc);let r=t.distanceTo(e)*.5,a=-this.direction.dot(fa),o=xi.dot(this.direction),l=-xi.dot(fa),c=xi.lengthSq(),h=Math.abs(1-a*a),f,u,p,g;if(h>0)if(f=a*l-o,u=a*o-l,g=r*h,f>=0)if(u>=-g)if(u<=g){let x=1/h;f*=x,u*=x,p=f*(f+a*u+2*o)+u*(a*f+u+2*l)+c}else u=r,f=Math.max(0,-(a*u+o)),p=-f*f+u*(u+2*l)+c;else u=-r,f=Math.max(0,-(a*u+o)),p=-f*f+u*(u+2*l)+c;else u<=-g?(f=Math.max(0,-(-a*r+o)),u=f>0?-r:Math.min(Math.max(-r,-l),r),p=-f*f+u*(u+2*l)+c):u<=g?(f=0,u=Math.min(Math.max(-r,-l),r),p=u*(u+2*l)+c):(f=Math.max(0,-(a*r+o)),u=f>0?r:Math.min(Math.max(-r,-l),r),p=-f*f+u*(u+2*l)+c);else u=a>0?-r:r,f=Math.max(0,-(a*u+o)),p=-f*f+u*(u+2*l)+c;return n&&n.copy(this.origin).addScaledVector(this.direction,f),s&&s.copy(uc).addScaledVector(fa,u),p}intersectSphere(t,e){jn.subVectors(t.center,this.origin);let n=jn.dot(this.direction),s=jn.dot(jn)-n*n,r=t.radius*t.radius;if(s>r)return null;let a=Math.sqrt(r-s),o=n-a,l=n+a;return l<0?null:o<0?this.at(l,e):this.at(o,e)}intersectsSphere(t){return t.radius<0?!1:this.distanceSqToPoint(t.center)<=t.radius*t.radius}distanceToPlane(t){let e=t.normal.dot(this.direction);if(e===0)return t.distanceToPoint(this.origin)===0?0:null;let n=-(this.origin.dot(t.normal)+t.constant)/e;return n>=0?n:null}intersectPlane(t,e){let n=this.distanceToPlane(t);return n===null?null:this.at(n,e)}intersectsPlane(t){let e=t.distanceToPoint(this.origin);return e===0||t.normal.dot(this.direction)*e<0}intersectBox(t,e){let n,s,r,a,o,l,c=1/this.direction.x,h=1/this.direction.y,f=1/this.direction.z,u=this.origin;return c>=0?(n=(t.min.x-u.x)*c,s=(t.max.x-u.x)*c):(n=(t.max.x-u.x)*c,s=(t.min.x-u.x)*c),h>=0?(r=(t.min.y-u.y)*h,a=(t.max.y-u.y)*h):(r=(t.max.y-u.y)*h,a=(t.min.y-u.y)*h),n>a||r>s||((r>n||isNaN(n))&&(n=r),(a<s||isNaN(s))&&(s=a),f>=0?(o=(t.min.z-u.z)*f,l=(t.max.z-u.z)*f):(o=(t.max.z-u.z)*f,l=(t.min.z-u.z)*f),n>l||o>s)||((o>n||n!==n)&&(n=o),(l<s||s!==s)&&(s=l),s<0)?null:this.at(n>=0?n:s,e)}intersectsBox(t){return this.intersectBox(t,jn)!==null}intersectTriangle(t,e,n,s,r){fc.subVectors(e,t),da.subVectors(n,t),dc.crossVectors(fc,da);let a=this.direction.dot(dc),o;if(a>0){if(s)return null;o=1}else if(a<0)o=-1,a=-a;else return null;xi.subVectors(this.origin,t);let l=o*this.direction.dot(da.crossVectors(xi,da));if(l<0)return null;let c=o*this.direction.dot(fc.cross(xi));if(c<0||l+c>a)return null;let h=-o*xi.dot(dc);return h<0?null:this.at(h/a,r)}applyMatrix4(t){return this.origin.applyMatrix4(t),this.direction.transformDirection(t),this}equals(t){return t.origin.equals(this.origin)&&t.direction.equals(this.direction)}clone(){return new this.constructor().copy(this)}},es=class extends ni{constructor(t){super(),this.isMeshBasicMaterial=!0,this.type="MeshBasicMaterial",this.color=new ut(16777215),this.map=null,this.lightMap=null,this.lightMapIntensity=1,this.aoMap=null,this.aoMapIntensity=1,this.specularMap=null,this.alphaMap=null,this.envMap=null,this.envMapRotation=new bi,this.combine=Rc,this.reflectivity=1,this.refractionRatio=.98,this.wireframe=!1,this.wireframeLinewidth=1,this.wireframeLinecap="round",this.wireframeLinejoin="round",this.fog=!0,this.setValues(t)}copy(t){return super.copy(t),this.color.copy(t.color),this.map=t.map,this.lightMap=t.lightMap,this.lightMapIntensity=t.lightMapIntensity,this.aoMap=t.aoMap,this.aoMapIntensity=t.aoMapIntensity,this.specularMap=t.specularMap,this.alphaMap=t.alphaMap,this.envMap=t.envMap,this.envMapRotation.copy(t.envMapRotation),this.combine=t.combine,this.reflectivity=t.reflectivity,this.refractionRatio=t.refractionRatio,this.wireframe=t.wireframe,this.wireframeLinewidth=t.wireframeLinewidth,this.wireframeLinecap=t.wireframeLinecap,this.wireframeLinejoin=t.wireframeLinejoin,this.fog=t.fog,this}},Mu=new ve,Ki=new Ps,pa=new wi,bu=new D,ma=new D,ga=new D,_a=new D,pc=new D,xa=new D,Su=new D,va=new D,rn=class extends sn{constructor(t=new Qt,e=new es){super(),this.isMesh=!0,this.type="Mesh",this.geometry=t,this.material=e,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.count=1,this.updateMorphTargets()}copy(t,e){return super.copy(t,e),t.morphTargetInfluences!==void 0&&(this.morphTargetInfluences=t.morphTargetInfluences.slice()),t.morphTargetDictionary!==void 0&&(this.morphTargetDictionary=Object.assign({},t.morphTargetDictionary)),this.material=Array.isArray(t.material)?t.material.slice():t.material,this.geometry=t.geometry,this}updateMorphTargets(){let e=this.geometry.morphAttributes,n=Object.keys(e);if(n.length>0){let s=e[n[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,a=s.length;r<a;r++){let o=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=r}}}}getVertexPosition(t,e){let n=this.geometry,s=n.attributes.position,r=n.morphAttributes.position,a=n.morphTargetsRelative;e.fromBufferAttribute(s,t);let o=this.morphTargetInfluences;if(r&&o){xa.set(0,0,0);for(let l=0,c=r.length;l<c;l++){let h=o[l],f=r[l];h!==0&&(pc.fromBufferAttribute(f,t),a?xa.addScaledVector(pc,h):xa.addScaledVector(pc.sub(e),h))}e.add(xa)}return e}raycast(t,e){let n=this.geometry,s=this.material,r=this.matrixWorld;s!==void 0&&(n.boundingSphere===null&&n.computeBoundingSphere(),pa.copy(n.boundingSphere),pa.applyMatrix4(r),Ki.copy(t.ray).recast(t.near),!(pa.containsPoint(Ki.origin)===!1&&(Ki.intersectSphere(pa,bu)===null||Ki.origin.distanceToSquared(bu)>(t.far-t.near)**2))&&(Mu.copy(r).invert(),Ki.copy(t.ray).applyMatrix4(Mu),!(n.boundingBox!==null&&Ki.intersectsBox(n.boundingBox)===!1)&&this._computeIntersections(t,e,Ki)))}_computeIntersections(t,e,n){let s,r=this.geometry,a=this.material,o=r.index,l=r.attributes.position,c=r.attributes.uv,h=r.attributes.uv1,f=r.attributes.normal,u=r.groups,p=r.drawRange;if(o!==null)if(Array.isArray(a))for(let g=0,x=u.length;g<x;g++){let m=u[g],d=a[m.materialIndex],y=Math.max(m.start,p.start),S=Math.min(o.count,Math.min(m.start+m.count,p.start+p.count));for(let b=y,T=S;b<T;b+=3){let w=o.getX(b),R=o.getX(b+1),v=o.getX(b+2);s=ya(this,d,t,n,c,h,f,w,R,v),s&&(s.faceIndex=Math.floor(b/3),s.face.materialIndex=m.materialIndex,e.push(s))}}else{let g=Math.max(0,p.start),x=Math.min(o.count,p.start+p.count);for(let m=g,d=x;m<d;m+=3){let y=o.getX(m),S=o.getX(m+1),b=o.getX(m+2);s=ya(this,a,t,n,c,h,f,y,S,b),s&&(s.faceIndex=Math.floor(m/3),e.push(s))}}else if(l!==void 0)if(Array.isArray(a))for(let g=0,x=u.length;g<x;g++){let m=u[g],d=a[m.materialIndex],y=Math.max(m.start,p.start),S=Math.min(l.count,Math.min(m.start+m.count,p.start+p.count));for(let b=y,T=S;b<T;b+=3){let w=b,R=b+1,v=b+2;s=ya(this,d,t,n,c,h,f,w,R,v),s&&(s.faceIndex=Math.floor(b/3),s.face.materialIndex=m.materialIndex,e.push(s))}}else{let g=Math.max(0,p.start),x=Math.min(l.count,p.start+p.count);for(let m=g,d=x;m<d;m+=3){let y=m,S=m+1,b=m+2;s=ya(this,a,t,n,c,h,f,y,S,b),s&&(s.faceIndex=Math.floor(m/3),e.push(s))}}}};function Ym(i,t,e,n,s,r,a,o){let l;if(t.side===$e?l=n.intersectTriangle(a,r,s,!0,o):l=n.intersectTriangle(s,r,a,t.side===ei,o),l===null)return null;va.copy(o),va.applyMatrix4(i.matrixWorld);let c=e.ray.origin.distanceTo(va);return c<e.near||c>e.far?null:{distance:c,point:va.clone(),object:i}}function ya(i,t,e,n,s,r,a,o,l,c){i.getVertexPosition(o,ma),i.getVertexPosition(l,ga),i.getVertexPosition(c,_a);let h=Ym(i,t,e,n,ma,ga,_a,Su);if(h){let f=new D;yi.getBarycoord(Su,ma,ga,_a,f),s&&(h.uv=yi.getInterpolatedAttribute(s,o,l,c,f,new Ut)),r&&(h.uv1=yi.getInterpolatedAttribute(r,o,l,c,f,new Ut)),a&&(h.normal=yi.getInterpolatedAttribute(a,o,l,c,f,new D),h.normal.dot(n.direction)>0&&h.normal.multiplyScalar(-1));let u={a:o,b:l,c,normal:new D,materialIndex:0};yi.getNormal(ma,ga,_a,u.normal),h.face=u,h.barycoord=f}return h}var Ya=class extends nn{constructor(t=null,e=1,n=1,s,r,a,o,l,c=Oe,h=Oe,f,u){super(null,a,o,l,c,h,s,r,f,u),this.isDataTexture=!0,this.image={data:t,width:e,height:n},this.generateMipmaps=!1,this.flipY=!1,this.unpackAlignment=1}};var mc=new D,Zm=new D,Jm=new Dt,Fn=class{constructor(t=new D(1,0,0),e=0){this.isPlane=!0,this.normal=t,this.constant=e}set(t,e){return this.normal.copy(t),this.constant=e,this}setComponents(t,e,n,s){return this.normal.set(t,e,n),this.constant=s,this}setFromNormalAndCoplanarPoint(t,e){return this.normal.copy(t),this.constant=-e.dot(this.normal),this}setFromCoplanarPoints(t,e,n){let s=mc.subVectors(n,e).cross(Zm.subVectors(t,e)).normalize();return this.setFromNormalAndCoplanarPoint(s,t),this}copy(t){return this.normal.copy(t.normal),this.constant=t.constant,this}normalize(){let t=1/this.normal.length();return this.normal.multiplyScalar(t),this.constant*=t,this}negate(){return this.constant*=-1,this.normal.negate(),this}distanceToPoint(t){return this.normal.dot(t)+this.constant}distanceToSphere(t){return this.distanceToPoint(t.center)-t.radius}projectPoint(t,e){return e.copy(t).addScaledVector(this.normal,-this.distanceToPoint(t))}intersectLine(t,e,n=!0){let s=t.delta(mc),r=this.normal.dot(s);if(r===0)return this.distanceToPoint(t.start)===0?e.copy(t.start):null;let a=-(t.start.dot(this.normal)+this.constant)/r;return n===!0&&(a<0||a>1)?null:e.copy(t.start).addScaledVector(s,a)}intersectsLine(t){let e=this.distanceToPoint(t.start),n=this.distanceToPoint(t.end);return e<0&&n>0||n<0&&e>0}intersectsBox(t){return t.intersectsPlane(this)}intersectsSphere(t){return t.intersectsPlane(this)}coplanarPoint(t){return t.copy(this.normal).multiplyScalar(-this.constant)}applyMatrix4(t,e){let n=e||Jm.getNormalMatrix(t),s=this.coplanarPoint(mc).applyMatrix4(t),r=this.normal.applyMatrix3(n).normalize();return this.constant=-s.dot(r),this}translate(t){return this.constant-=t.dot(this.normal),this}equals(t){return t.normal.equals(this.normal)&&t.constant===this.constant}clone(){return new this.constructor().copy(this)}},ji=new wi,$m=new Ut(.5,.5),Ma=new D,lr=class{constructor(t=new Fn,e=new Fn,n=new Fn,s=new Fn,r=new Fn,a=new Fn){this.planes=[t,e,n,s,r,a]}set(t,e,n,s,r,a){let o=this.planes;return o[0].copy(t),o[1].copy(e),o[2].copy(n),o[3].copy(s),o[4].copy(r),o[5].copy(a),this}copy(t){let e=this.planes;for(let n=0;n<6;n++)e[n].copy(t.planes[n]);return this}setFromProjectionMatrix(t,e=An,n=!1){let s=this.planes,r=t.elements,a=r[0],o=r[1],l=r[2],c=r[3],h=r[4],f=r[5],u=r[6],p=r[7],g=r[8],x=r[9],m=r[10],d=r[11],y=r[12],S=r[13],b=r[14],T=r[15];if(s[0].setComponents(c-a,p-h,d-g,T-y).normalize(),s[1].setComponents(c+a,p+h,d+g,T+y).normalize(),s[2].setComponents(c+o,p+f,d+x,T+S).normalize(),s[3].setComponents(c-o,p-f,d-x,T-S).normalize(),n)s[4].setComponents(l,u,m,b).normalize(),s[5].setComponents(c-l,p-u,d-m,T-b).normalize();else if(s[4].setComponents(c-l,p-u,d-m,T-b).normalize(),e===An)s[5].setComponents(c+l,p+u,d+m,T+b).normalize();else if(e===er)s[5].setComponents(l,u,m,b).normalize();else throw new Error("THREE.Frustum.setFromProjectionMatrix(): Invalid coordinate system: "+e);return this}intersectsObject(t){if(t.boundingSphere!==void 0)t.boundingSphere===null&&t.computeBoundingSphere(),ji.copy(t.boundingSphere).applyMatrix4(t.matrixWorld);else{let e=t.geometry;e.boundingSphere===null&&e.computeBoundingSphere(),ji.copy(e.boundingSphere).applyMatrix4(t.matrixWorld)}return this.intersectsSphere(ji)}intersectsSprite(t){ji.center.set(0,0,0);let e=$m.distanceTo(t.center);return ji.radius=.7071067811865476+e,ji.applyMatrix4(t.matrixWorld),this.intersectsSphere(ji)}intersectsSphere(t){let e=this.planes,n=t.center,s=-t.radius;for(let r=0;r<6;r++)if(e[r].distanceToPoint(n)<s)return!1;return!0}intersectsBox(t){let e=this.planes;for(let n=0;n<6;n++){let s=e[n];if(Ma.x=s.normal.x>0?t.max.x:t.min.x,Ma.y=s.normal.y>0?t.max.y:t.min.y,Ma.z=s.normal.z>0?t.max.z:t.min.z,s.distanceToPoint(Ma)<0)return!1}return!0}containsPoint(t){let e=this.planes;for(let n=0;n<6;n++)if(e[n].distanceToPoint(t)<0)return!1;return!0}clone(){return new this.constructor().copy(this)}};var ii=class extends ni{constructor(t){super(),this.isLineBasicMaterial=!0,this.type="LineBasicMaterial",this.color=new ut(16777215),this.map=null,this.linewidth=1,this.linecap="round",this.linejoin="round",this.fog=!0,this.setValues(t)}copy(t){return super.copy(t),this.color.copy(t.color),this.map=t.map,this.linewidth=t.linewidth,this.linecap=t.linecap,this.linejoin=t.linejoin,this.fog=t.fog,this}},Za=new D,Ja=new D,wu=new ve,Ks=new Ps,ba=new wi,gc=new D,Au=new D,$a=class extends sn{constructor(t=new Qt,e=new ii){super(),this.isLine=!0,this.type="Line",this.geometry=t,this.material=e,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(t,e){return super.copy(t,e),this.material=Array.isArray(t.material)?t.material.slice():t.material,this.geometry=t.geometry,this}computeLineDistances(){let t=this.geometry;if(t.index===null){let e=t.attributes.position,n=[0];for(let s=1,r=e.count;s<r;s++)Za.fromBufferAttribute(e,s-1),Ja.fromBufferAttribute(e,s),n[s]=n[s-1],n[s]+=Za.distanceTo(Ja);t.setAttribute("lineDistance",new ke(n,1))}else Et("Line.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}raycast(t,e){let n=this.geometry,s=this.matrixWorld,r=t.params.Line.threshold,a=n.drawRange;if(n.boundingSphere===null&&n.computeBoundingSphere(),ba.copy(n.boundingSphere),ba.applyMatrix4(s),ba.radius+=r,t.ray.intersectsSphere(ba)===!1)return;wu.copy(s).invert(),Ks.copy(t.ray).applyMatrix4(wu);let o=r/((this.scale.x+this.scale.y+this.scale.z)/3),l=o*o,c=this.isLineSegments?2:1,h=n.index,u=n.attributes.position;if(h!==null){let p=Math.max(0,a.start),g=Math.min(h.count,a.start+a.count);for(let x=p,m=g-1;x<m;x+=c){let d=h.getX(x),y=h.getX(x+1),S=Sa(this,t,Ks,l,d,y,x);S&&e.push(S)}if(this.isLineLoop){let x=h.getX(g-1),m=h.getX(p),d=Sa(this,t,Ks,l,x,m,g-1);d&&e.push(d)}}else{let p=Math.max(0,a.start),g=Math.min(u.count,a.start+a.count);for(let x=p,m=g-1;x<m;x+=c){let d=Sa(this,t,Ks,l,x,x+1,x);d&&e.push(d)}if(this.isLineLoop){let x=Sa(this,t,Ks,l,g-1,p,g-1);x&&e.push(x)}}}updateMorphTargets(){let e=this.geometry.morphAttributes,n=Object.keys(e);if(n.length>0){let s=e[n[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,a=s.length;r<a;r++){let o=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=r}}}}};function Sa(i,t,e,n,s,r,a){let o=i.geometry.attributes.position;if(Za.fromBufferAttribute(o,s),Ja.fromBufferAttribute(o,r),e.distanceSqToSegment(Za,Ja,gc,Au)>n)return;gc.applyMatrix4(i.matrixWorld);let c=t.ray.origin.distanceTo(gc);if(!(c<t.near||c>t.far))return{distance:c,point:Au.clone().applyMatrix4(i.matrixWorld),index:a,face:null,faceIndex:null,barycoord:null,object:i}}var Tu=new D,Eu=new D,ns=class extends $a{constructor(t,e){super(t,e),this.isLineSegments=!0,this.type="LineSegments"}computeLineDistances(){let t=this.geometry;if(t.index===null){let e=t.attributes.position,n=[];for(let s=0,r=e.count;s<r;s+=2)Tu.fromBufferAttribute(e,s),Eu.fromBufferAttribute(e,s+1),n[s]=s===0?0:n[s-1],n[s+1]=n[s]+Tu.distanceTo(Eu);t.setAttribute("lineDistance",new ke(n,1))}else Et("LineSegments.computeLineDistances(): Computation only possible with non-indexed BufferGeometry.");return this}};var si=class extends ni{constructor(t){super(),this.isPointsMaterial=!0,this.type="PointsMaterial",this.color=new ut(16777215),this.map=null,this.alphaMap=null,this.size=1,this.sizeAttenuation=!0,this.fog=!0,this.setValues(t)}copy(t){return super.copy(t),this.color.copy(t.color),this.map=t.map,this.alphaMap=t.alphaMap,this.size=t.size,this.sizeAttenuation=t.sizeAttenuation,this.fog=t.fog,this}},Cu=new ve,Sc=new Ps,wa=new wi,Aa=new D,an=class extends sn{constructor(t=new Qt,e=new si){super(),this.isPoints=!0,this.type="Points",this.geometry=t,this.material=e,this.morphTargetDictionary=void 0,this.morphTargetInfluences=void 0,this.updateMorphTargets()}copy(t,e){return super.copy(t,e),this.material=Array.isArray(t.material)?t.material.slice():t.material,this.geometry=t.geometry,this}raycast(t,e){let n=this.geometry,s=this.matrixWorld,r=t.params.Points.threshold,a=n.drawRange;if(n.boundingSphere===null&&n.computeBoundingSphere(),wa.copy(n.boundingSphere),wa.applyMatrix4(s),wa.radius+=r,t.ray.intersectsSphere(wa)===!1)return;Cu.copy(s).invert(),Sc.copy(t.ray).applyMatrix4(Cu);let o=r/((this.scale.x+this.scale.y+this.scale.z)/3),l=o*o,c=n.index,f=n.attributes.position;if(c!==null){let u=Math.max(0,a.start),p=Math.min(c.count,a.start+a.count);for(let g=u,x=p;g<x;g++){let m=c.getX(g);Aa.fromBufferAttribute(f,m),Ru(Aa,m,l,s,t,e,this)}}else{let u=Math.max(0,a.start),p=Math.min(f.count,a.start+a.count);for(let g=u,x=p;g<x;g++)Aa.fromBufferAttribute(f,g),Ru(Aa,g,l,s,t,e,this)}}updateMorphTargets(){let e=this.geometry.morphAttributes,n=Object.keys(e);if(n.length>0){let s=e[n[0]];if(s!==void 0){this.morphTargetInfluences=[],this.morphTargetDictionary={};for(let r=0,a=s.length;r<a;r++){let o=s[r].name||String(r);this.morphTargetInfluences.push(0),this.morphTargetDictionary[o]=r}}}}};function Ru(i,t,e,n,s,r,a){let o=Sc.distanceSqToPoint(i);if(o<e){let l=new D;Sc.closestPointToPoint(i,l),l.applyMatrix4(n);let c=s.ray.origin.distanceTo(l);if(c<s.near||c>s.far)return;r.push({distance:c,distanceToRay:Math.sqrt(o),point:l,index:t,face:null,faceIndex:null,barycoord:null,object:a})}}var cr=class extends nn{constructor(t=[],e=Ri,n,s,r,a,o,l,c,h){super(t,e,n,s,r,a,o,l,c,h),this.isCubeTexture=!0,this.flipY=!1}get images(){return this.image}set images(t){this.image=t}};var ri=class extends nn{constructor(t,e,n=En,s,r,a,o=Oe,l=Oe,c,h=Bn,f=1){if(h!==Bn&&h!==Ii)throw new Error("DepthTexture format must be either THREE.DepthFormat or THREE.DepthStencilFormat");let u={width:t,height:e,depth:f};super(u,s,r,a,o,l,h,n,c),this.isDepthTexture=!0,this.flipY=!1,this.generateMipmaps=!1,this.compareFunction=null}copy(t){return super.copy(t),this.source=new Cs(Object.assign({},t.image)),this.compareFunction=t.compareFunction,this}toJSON(t){let e=super.toJSON(t);return this.compareFunction!==null&&(e.compareFunction=this.compareFunction),e}},Ka=class extends ri{constructor(t,e=En,n=Ri,s,r,a=Oe,o=Oe,l,c=Bn){let h={width:t,height:t,depth:1},f=[h,h,h,h,h,h];super(t,t,e,n,s,r,a,o,l,c),this.image=f,this.isCubeDepthTexture=!0,this.isCubeTexture=!0}get images(){return this.image}set images(t){this.image=t}},hr=class extends nn{constructor(t=null){super(),this.sourceTexture=t,this.isExternalTexture=!0}copy(t){return super.copy(t),this.sourceTexture=t.sourceTexture,this}},Is=class i extends Qt{constructor(t=1,e=1,n=1,s=1,r=1,a=1){super(),this.type="BoxGeometry",this.parameters={width:t,height:e,depth:n,widthSegments:s,heightSegments:r,depthSegments:a};let o=this;s=Math.floor(s),r=Math.floor(r),a=Math.floor(a);let l=[],c=[],h=[],f=[],u=0,p=0;g("z","y","x",-1,-1,n,e,t,a,r,0),g("z","y","x",1,-1,n,e,-t,a,r,1),g("x","z","y",1,1,t,n,e,s,a,2),g("x","z","y",1,-1,t,n,-e,s,a,3),g("x","y","z",1,-1,t,e,n,s,r,4),g("x","y","z",-1,-1,t,e,-n,s,r,5),this.setIndex(l),this.setAttribute("position",new ke(c,3)),this.setAttribute("normal",new ke(h,3)),this.setAttribute("uv",new ke(f,2));function g(x,m,d,y,S,b,T,w,R,v,E){let I=b/R,C=T/v,N=b/2,H=T/2,W=w/2,U=R+1,z=v+1,V=0,$=0,tt=new D;for(let ct=0;ct<z;ct++){let Mt=ct*C-H;for(let St=0;St<U;St++){let Xt=St*I-N;tt[x]=Xt*y,tt[m]=Mt*S,tt[d]=W,c.push(tt.x,tt.y,tt.z),tt[x]=0,tt[m]=0,tt[d]=w>0?1:-1,h.push(tt.x,tt.y,tt.z),f.push(St/R),f.push(1-ct/v),V+=1}}for(let ct=0;ct<v;ct++)for(let Mt=0;Mt<R;Mt++){let St=u+Mt+U*ct,Xt=u+Mt+U*(ct+1),te=u+(Mt+1)+U*(ct+1),kt=u+(Mt+1)+U*ct;l.push(St,Xt,kt),l.push(Xt,te,kt),$+=6}o.addGroup(p,$,E),p+=$,u+=V}}copy(t){return super.copy(t),this.parameters=Object.assign({},t.parameters),this}static fromJSON(t){return new i(t.width,t.height,t.depth,t.widthSegments,t.heightSegments,t.depthSegments)}};var ur=class i extends Qt{constructor(t=1,e=1,n=1,s=1){super(),this.type="PlaneGeometry",this.parameters={width:t,height:e,widthSegments:n,heightSegments:s};let r=t/2,a=e/2,o=Math.floor(n),l=Math.floor(s),c=o+1,h=l+1,f=t/o,u=e/l,p=[],g=[],x=[],m=[];for(let d=0;d<h;d++){let y=d*u-a;for(let S=0;S<c;S++){let b=S*f-r;g.push(b,-y,0),x.push(0,0,1),m.push(S/o),m.push(1-d/l)}}for(let d=0;d<l;d++)for(let y=0;y<o;y++){let S=y+c*d,b=y+c*(d+1),T=y+1+c*(d+1),w=y+1+c*d;p.push(S,b,w),p.push(b,T,w)}this.setIndex(p),this.setAttribute("position",new ke(g,3)),this.setAttribute("normal",new ke(x,3)),this.setAttribute("uv",new ke(m,2))}copy(t){return super.copy(t),this.parameters=Object.assign({},t.parameters),this}static fromJSON(t){return new i(t.width,t.height,t.widthSegments,t.heightSegments)}};function rs(i){let t={};for(let e in i){t[e]={};for(let n in i[e]){let s=i[e][n];if(Pu(s))s.isRenderTargetTexture?(Et("UniformsUtils: Textures of render targets cannot be cloned via cloneUniforms() or mergeUniforms()."),t[e][n]=null):t[e][n]=s.clone();else if(Array.isArray(s))if(Pu(s[0])){let r=[];for(let a=0,o=s.length;a<o;a++)r[a]=s[a].clone();t[e][n]=r}else t[e][n]=s.slice();else t[e][n]=s}}return t}function Ye(i){let t={};for(let e=0;e<i.length;e++){let n=rs(i[e]);for(let s in n)t[s]=n[s]}return t}function Pu(i){return i&&(i.isColor||i.isMatrix3||i.isMatrix4||i.isVector2||i.isVector3||i.isVector4||i.isTexture||i.isQuaternion)}function Km(i){let t=[];for(let e=0;e<i.length;e++)t.push(i[e].clone());return t}function Vc(i){let t=i.getRenderTarget();return t===null?i.outputColorSpace:t.isXRRenderTarget===!0?t.texture.colorSpace:Ht.workingColorSpace}var oi={clone:rs,merge:Ye},jm=`void main() {
	gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
}`,Qm=`void main() {
	gl_FragColor = vec4( 1.0, 0.0, 0.0, 1.0 );
}`,se=class extends ni{constructor(t){super(),this.isShaderMaterial=!0,this.type="ShaderMaterial",this.defines={},this.uniforms={},this.uniformsGroups=[],this.vertexShader=jm,this.fragmentShader=Qm,this.linewidth=1,this.wireframe=!1,this.wireframeLinewidth=1,this.fog=!1,this.lights=!1,this.clipping=!1,this.forceSinglePass=!0,this.extensions={clipCullDistance:!1,multiDraw:!1},this.defaultAttributeValues={color:[1,1,1],uv:[0,0],uv1:[0,0]},this.index0AttributeName=void 0,this.uniformsNeedUpdate=!1,this.glslVersion=null,t!==void 0&&this.setValues(t)}copy(t){return super.copy(t),this.fragmentShader=t.fragmentShader,this.vertexShader=t.vertexShader,this.uniforms=rs(t.uniforms),this.uniformsGroups=Km(t.uniformsGroups),this.defines=Object.assign({},t.defines),this.wireframe=t.wireframe,this.wireframeLinewidth=t.wireframeLinewidth,this.fog=t.fog,this.lights=t.lights,this.clipping=t.clipping,this.extensions=Object.assign({},t.extensions),this.glslVersion=t.glslVersion,this.defaultAttributeValues=Object.assign({},t.defaultAttributeValues),this.index0AttributeName=t.index0AttributeName,this.uniformsNeedUpdate=t.uniformsNeedUpdate,this}toJSON(t){let e=super.toJSON(t);e.glslVersion=this.glslVersion,e.uniforms={};for(let s in this.uniforms){let a=this.uniforms[s].value;a&&a.isTexture?e.uniforms[s]={type:"t",value:a.toJSON(t).uuid}:a&&a.isColor?e.uniforms[s]={type:"c",value:a.getHex()}:a&&a.isVector2?e.uniforms[s]={type:"v2",value:a.toArray()}:a&&a.isVector3?e.uniforms[s]={type:"v3",value:a.toArray()}:a&&a.isVector4?e.uniforms[s]={type:"v4",value:a.toArray()}:a&&a.isMatrix3?e.uniforms[s]={type:"m3",value:a.toArray()}:a&&a.isMatrix4?e.uniforms[s]={type:"m4",value:a.toArray()}:e.uniforms[s]={value:a}}Object.keys(this.defines).length>0&&(e.defines=this.defines),e.vertexShader=this.vertexShader,e.fragmentShader=this.fragmentShader,e.lights=this.lights,e.clipping=this.clipping;let n={};for(let s in this.extensions)this.extensions[s]===!0&&(n[s]=!0);return Object.keys(n).length>0&&(e.extensions=n),e}},Ls=class extends se{constructor(t){super(t),this.isRawShaderMaterial=!0,this.type="RawShaderMaterial"}};var ja=class extends ni{constructor(t){super(),this.isMeshDepthMaterial=!0,this.type="MeshDepthMaterial",this.depthPacking=sf,this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.wireframe=!1,this.wireframeLinewidth=1,this.setValues(t)}copy(t){return super.copy(t),this.depthPacking=t.depthPacking,this.map=t.map,this.alphaMap=t.alphaMap,this.displacementMap=t.displacementMap,this.displacementScale=t.displacementScale,this.displacementBias=t.displacementBias,this.wireframe=t.wireframe,this.wireframeLinewidth=t.wireframeLinewidth,this}},Qa=class extends ni{constructor(t){super(),this.isMeshDistanceMaterial=!0,this.type="MeshDistanceMaterial",this.map=null,this.alphaMap=null,this.displacementMap=null,this.displacementScale=1,this.displacementBias=0,this.setValues(t)}copy(t){return super.copy(t),this.map=t.map,this.alphaMap=t.alphaMap,this.displacementMap=t.displacementMap,this.displacementScale=t.displacementScale,this.displacementBias=t.displacementBias,this}};var fr=class extends ii{constructor(t){super(),this.isLineDashedMaterial=!0,this.type="LineDashedMaterial",this.scale=1,this.dashSize=3,this.gapSize=1,this.setValues(t)}copy(t){return super.copy(t),this.scale=t.scale,this.dashSize=t.dashSize,this.gapSize=t.gapSize,this}};function Ta(i,t){return!i||i.constructor===t?i:typeof t.BYTES_PER_ELEMENT=="number"?new t(i):Array.prototype.slice.call(i)}var Ai=class{constructor(t,e,n,s){this.parameterPositions=t,this._cachedIndex=0,this.resultBuffer=s!==void 0?s:new e.constructor(n),this.sampleValues=e,this.valueSize=n,this.settings=null,this.DefaultSettings_={}}evaluate(t){let e=this.parameterPositions,n=this._cachedIndex,s=e[n],r=e[n-1];n:{t:{let a;e:{i:if(!(t<s)){for(let o=n+2;;){if(s===void 0){if(t<r)break i;return n=e.length,this._cachedIndex=n,this.copySampleValue_(n-1)}if(n===o)break;if(r=s,s=e[++n],t<s)break t}a=e.length;break e}if(!(t>=r)){let o=e[1];t<o&&(n=2,r=o);for(let l=n-2;;){if(r===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(n===l)break;if(s=r,r=e[--n-1],t>=r)break t}a=n,n=0;break e}break n}for(;n<a;){let o=n+a>>>1;t<e[o]?a=o:n=o+1}if(s=e[n],r=e[n-1],r===void 0)return this._cachedIndex=0,this.copySampleValue_(0);if(s===void 0)return n=e.length,this._cachedIndex=n,this.copySampleValue_(n-1)}this._cachedIndex=n,this.intervalChanged_(n,r,s)}return this.interpolate_(n,r,t,s)}getSettings_(){return this.settings||this.DefaultSettings_}copySampleValue_(t){let e=this.resultBuffer,n=this.sampleValues,s=this.valueSize,r=t*s;for(let a=0;a!==s;++a)e[a]=n[r+a];return e}interpolate_(){throw new Error("call to abstract method")}intervalChanged_(){}},to=class extends Ai{constructor(t,e,n,s){super(t,e,n,s),this._weightPrev=-0,this._offsetPrev=-0,this._weightNext=-0,this._offsetNext=-0,this.DefaultSettings_={endingStart:xc,endingEnd:xc}}intervalChanged_(t,e,n){let s=this.parameterPositions,r=t-2,a=t+1,o=s[r],l=s[a];if(o===void 0)switch(this.getSettings_().endingStart){case vc:r=t,o=2*e-n;break;case yc:r=s.length-2,o=e+s[r]-s[r+1];break;default:r=t,o=n}if(l===void 0)switch(this.getSettings_().endingEnd){case vc:a=t,l=2*n-e;break;case yc:a=1,l=n+s[1]-s[0];break;default:a=t-1,l=e}let c=(n-e)*.5,h=this.valueSize;this._weightPrev=c/(e-o),this._weightNext=c/(l-n),this._offsetPrev=r*h,this._offsetNext=a*h}interpolate_(t,e,n,s){let r=this.resultBuffer,a=this.sampleValues,o=this.valueSize,l=t*o,c=l-o,h=this._offsetPrev,f=this._offsetNext,u=this._weightPrev,p=this._weightNext,g=(n-e)/(s-e),x=g*g,m=x*g,d=-u*m+2*u*x-u*g,y=(1+u)*m+(-1.5-2*u)*x+(-.5+u)*g+1,S=(-1-p)*m+(1.5+p)*x+.5*g,b=p*m-p*x;for(let T=0;T!==o;++T)r[T]=d*a[h+T]+y*a[c+T]+S*a[l+T]+b*a[f+T];return r}},eo=class extends Ai{constructor(t,e,n,s){super(t,e,n,s)}interpolate_(t,e,n,s){let r=this.resultBuffer,a=this.sampleValues,o=this.valueSize,l=t*o,c=l-o,h=(n-e)/(s-e),f=1-h;for(let u=0;u!==o;++u)r[u]=a[c+u]*f+a[l+u]*h;return r}},no=class extends Ai{constructor(t,e,n,s){super(t,e,n,s)}interpolate_(t){return this.copySampleValue_(t-1)}},io=class extends Ai{interpolate_(t,e,n,s){let r=this.resultBuffer,a=this.sampleValues,o=this.valueSize,l=t*o,c=l-o,h=this.settings||this.DefaultSettings_,f=h.inTangents,u=h.outTangents;if(!f||!u){let x=(n-e)/(s-e),m=1-x;for(let d=0;d!==o;++d)r[d]=a[c+d]*m+a[l+d]*x;return r}let p=o*2,g=t-1;for(let x=0;x!==o;++x){let m=a[c+x],d=a[l+x],y=g*p+x*2,S=u[y],b=u[y+1],T=t*p+x*2,w=f[T],R=f[T+1],v=(n-e)/(s-e),E,I,C,N,H;for(let W=0;W<8;W++){E=v*v,I=E*v,C=1-v,N=C*C,H=N*C;let z=H*e+3*N*v*S+3*C*E*w+I*s-n;if(Math.abs(z)<1e-10)break;let V=3*N*(S-e)+6*C*v*(w-S)+3*E*(s-w);if(Math.abs(V)<1e-10)break;v=v-z/V,v=Math.max(0,Math.min(1,v))}r[x]=H*m+3*N*v*b+3*C*E*R+I*d}return r}},dn=class{constructor(t,e,n,s){if(t===void 0)throw new Error("THREE.KeyframeTrack: track name is undefined");if(e===void 0||e.length===0)throw new Error("THREE.KeyframeTrack: no keyframes in track named "+t);this.name=t,this.times=Ta(e,this.TimeBufferType),this.values=Ta(n,this.ValueBufferType),this.setInterpolation(s||this.DefaultInterpolation)}static toJSON(t){let e=t.constructor,n;if(e.toJSON!==this.toJSON)n=e.toJSON(t);else{n={name:t.name,times:Ta(t.times,Array),values:Ta(t.values,Array)};let s=t.getInterpolation();s!==t.DefaultInterpolation&&(n.interpolation=s)}return n.type=t.ValueTypeName,n}InterpolantFactoryMethodDiscrete(t){return new no(this.times,this.values,this.getValueSize(),t)}InterpolantFactoryMethodLinear(t){return new eo(this.times,this.values,this.getValueSize(),t)}InterpolantFactoryMethodSmooth(t){return new to(this.times,this.values,this.getValueSize(),t)}InterpolantFactoryMethodBezier(t){let e=new io(this.times,this.values,this.getValueSize(),t);return this.settings&&(e.settings=this.settings),e}setInterpolation(t){let e;switch(t){case js:e=this.InterpolantFactoryMethodDiscrete;break;case Va:e=this.InterpolantFactoryMethodLinear;break;case Ra:e=this.InterpolantFactoryMethodSmooth;break;case _c:e=this.InterpolantFactoryMethodBezier;break}if(e===void 0){let n="unsupported interpolation for "+this.ValueTypeName+" keyframe track named "+this.name;if(this.createInterpolant===void 0)if(t!==this.DefaultInterpolation)this.setInterpolation(this.DefaultInterpolation);else throw new Error(n);return Et("KeyframeTrack:",n),this}return this.createInterpolant=e,this}getInterpolation(){switch(this.createInterpolant){case this.InterpolantFactoryMethodDiscrete:return js;case this.InterpolantFactoryMethodLinear:return Va;case this.InterpolantFactoryMethodSmooth:return Ra;case this.InterpolantFactoryMethodBezier:return _c}}getValueSize(){return this.values.length/this.times.length}shift(t){if(t!==0){let e=this.times;for(let n=0,s=e.length;n!==s;++n)e[n]+=t}return this}scale(t){if(t!==1){let e=this.times;for(let n=0,s=e.length;n!==s;++n)e[n]*=t}return this}trim(t,e){let n=this.times,s=n.length,r=0,a=s-1;for(;r!==s&&n[r]<t;)++r;for(;a!==-1&&n[a]>e;)--a;if(++a,r!==0||a!==s){r>=a&&(a=Math.max(a,1),r=a-1);let o=this.getValueSize();this.times=n.slice(r,a),this.values=this.values.slice(r*o,a*o)}return this}validate(){let t=!0,e=this.getValueSize();e-Math.floor(e)!==0&&(Rt("KeyframeTrack: Invalid value size in track.",this),t=!1);let n=this.times,s=this.values,r=n.length;r===0&&(Rt("KeyframeTrack: Track is empty.",this),t=!1);let a=null;for(let o=0;o!==r;o++){let l=n[o];if(typeof l=="number"&&isNaN(l)){Rt("KeyframeTrack: Time is not a valid number.",this,o,l),t=!1;break}if(a!==null&&a>l){Rt("KeyframeTrack: Out of order keys.",this,o,l,a),t=!1;break}a=l}if(s!==void 0&&Im(s))for(let o=0,l=s.length;o!==l;++o){let c=s[o];if(isNaN(c)){Rt("KeyframeTrack: Value is not a valid number.",this,o,c),t=!1;break}}return t}optimize(){let t=this.times.slice(),e=this.values.slice(),n=this.getValueSize(),s=this.getInterpolation()===Ra,r=t.length-1,a=1;for(let o=1;o<r;++o){let l=!1,c=t[o],h=t[o+1];if(c!==h&&(o!==1||c!==t[0]))if(s)l=!0;else{let f=o*n,u=f-n,p=f+n;for(let g=0;g!==n;++g){let x=e[f+g];if(x!==e[u+g]||x!==e[p+g]){l=!0;break}}}if(l){if(o!==a){t[a]=t[o];let f=o*n,u=a*n;for(let p=0;p!==n;++p)e[u+p]=e[f+p]}++a}}if(r>0){t[a]=t[r];for(let o=r*n,l=a*n,c=0;c!==n;++c)e[l+c]=e[o+c];++a}return a!==t.length?(this.times=t.slice(0,a),this.values=e.slice(0,a*n)):(this.times=t,this.values=e),this}clone(){let t=this.times.slice(),e=this.values.slice(),n=this.constructor,s=new n(this.name,t,e);return s.createInterpolant=this.createInterpolant,s}};dn.prototype.ValueTypeName="";dn.prototype.TimeBufferType=Float32Array;dn.prototype.ValueBufferType=Float32Array;dn.prototype.DefaultInterpolation=Va;var Ti=class extends dn{constructor(t,e,n){super(t,e,n)}};Ti.prototype.ValueTypeName="bool";Ti.prototype.ValueBufferType=Array;Ti.prototype.DefaultInterpolation=js;Ti.prototype.InterpolantFactoryMethodLinear=void 0;Ti.prototype.InterpolantFactoryMethodSmooth=void 0;var so=class extends dn{constructor(t,e,n,s){super(t,e,n,s)}};so.prototype.ValueTypeName="color";var ro=class extends dn{constructor(t,e,n,s){super(t,e,n,s)}};ro.prototype.ValueTypeName="number";var ao=class extends Ai{constructor(t,e,n,s){super(t,e,n,s)}interpolate_(t,e,n,s){let r=this.resultBuffer,a=this.sampleValues,o=this.valueSize,l=(n-e)/(s-e),c=t*o;for(let h=c+o;c!==h;c+=4)en.slerpFlat(r,0,a,c-o,a,c,l);return r}},dr=class extends dn{constructor(t,e,n,s){super(t,e,n,s)}InterpolantFactoryMethodLinear(t){return new ao(this.times,this.values,this.getValueSize(),t)}};dr.prototype.ValueTypeName="quaternion";dr.prototype.InterpolantFactoryMethodSmooth=void 0;var Ei=class extends dn{constructor(t,e,n){super(t,e,n)}};Ei.prototype.ValueTypeName="string";Ei.prototype.ValueBufferType=Array;Ei.prototype.DefaultInterpolation=js;Ei.prototype.InterpolantFactoryMethodLinear=void 0;Ei.prototype.InterpolantFactoryMethodSmooth=void 0;var oo=class extends dn{constructor(t,e,n,s){super(t,e,n,s)}};oo.prototype.ValueTypeName="vector";var lo=class{constructor(t,e,n){let s=this,r=!1,a=0,o=0,l,c=[];this.onStart=void 0,this.onLoad=t,this.onProgress=e,this.onError=n,this._abortController=null,this.itemStart=function(h){o++,r===!1&&s.onStart!==void 0&&s.onStart(h,a,o),r=!0},this.itemEnd=function(h){a++,s.onProgress!==void 0&&s.onProgress(h,a,o),a===o&&(r=!1,s.onLoad!==void 0&&s.onLoad())},this.itemError=function(h){s.onError!==void 0&&s.onError(h)},this.resolveURL=function(h){return l?l(h):h},this.setURLModifier=function(h){return l=h,this},this.addHandler=function(h,f){return c.push(h,f),this},this.removeHandler=function(h){let f=c.indexOf(h);return f!==-1&&c.splice(f,2),this},this.getHandler=function(h){for(let f=0,u=c.length;f<u;f+=2){let p=c[f],g=c[f+1];if(p.global&&(p.lastIndex=0),p.test(h))return g}return null},this.abort=function(){return this.abortController.abort(),this._abortController=null,this}}get abortController(){return this._abortController||(this._abortController=new AbortController),this._abortController}},_f=new lo,co=class{constructor(t){this.manager=t!==void 0?t:_f,this.crossOrigin="anonymous",this.withCredentials=!1,this.path="",this.resourcePath="",this.requestHeader={},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}load(){}loadAsync(t,e){let n=this;return new Promise(function(s,r){n.load(t,s,e,r)})}parse(){}setCrossOrigin(t){return this.crossOrigin=t,this}setWithCredentials(t){return this.withCredentials=t,this}setPath(t){return this.path=t,this}setResourcePath(t){return this.resourcePath=t,this}setRequestHeader(t){return this.requestHeader=t,this}abort(){return this}};co.DEFAULT_MATERIAL_NAME="__DEFAULT";var Ea=new D,Ca=new en,Dn=new D,pr=class extends sn{constructor(){super(),this.isCamera=!0,this.type="Camera",this.matrixWorldInverse=new ve,this.projectionMatrix=new ve,this.projectionMatrixInverse=new ve,this.coordinateSystem=An,this._reversedDepth=!1}get reversedDepth(){return this._reversedDepth}copy(t,e){return super.copy(t,e),this.matrixWorldInverse.copy(t.matrixWorldInverse),this.projectionMatrix.copy(t.projectionMatrix),this.projectionMatrixInverse.copy(t.projectionMatrixInverse),this.coordinateSystem=t.coordinateSystem,this}getWorldDirection(t){return super.getWorldDirection(t).negate()}updateMatrixWorld(t){super.updateMatrixWorld(t),this.matrixWorld.decompose(Ea,Ca,Dn),Dn.x===1&&Dn.y===1&&Dn.z===1?this.matrixWorldInverse.copy(this.matrixWorld).invert():this.matrixWorldInverse.compose(Ea,Ca,Dn.set(1,1,1)).invert()}updateWorldMatrix(t,e){super.updateWorldMatrix(t,e),this.matrixWorld.decompose(Ea,Ca,Dn),Dn.x===1&&Dn.y===1&&Dn.z===1?this.matrixWorldInverse.copy(this.matrixWorld).invert():this.matrixWorldInverse.compose(Ea,Ca,Dn.set(1,1,1)).invert()}clone(){return new this.constructor().copy(this)}},vi=new D,Iu=new Ut,Lu=new Ut,Xe=class extends pr{constructor(t=50,e=1,n=.1,s=2e3){super(),this.isPerspectiveCamera=!0,this.type="PerspectiveCamera",this.fov=t,this.zoom=1,this.near=n,this.far=s,this.focus=10,this.aspect=e,this.view=null,this.filmGauge=35,this.filmOffset=0,this.updateProjectionMatrix()}copy(t,e){return super.copy(t,e),this.fov=t.fov,this.zoom=t.zoom,this.near=t.near,this.far=t.far,this.focus=t.focus,this.aspect=t.aspect,this.view=t.view===null?null:Object.assign({},t.view),this.filmGauge=t.filmGauge,this.filmOffset=t.filmOffset,this}setFocalLength(t){let e=.5*this.getFilmHeight()/t;this.fov=Ha*2*Math.atan(e),this.updateProjectionMatrix()}getFocalLength(){let t=Math.tan(Yl*.5*this.fov);return .5*this.getFilmHeight()/t}getEffectiveFOV(){return Ha*2*Math.atan(Math.tan(Yl*.5*this.fov)/this.zoom)}getFilmWidth(){return this.filmGauge*Math.min(this.aspect,1)}getFilmHeight(){return this.filmGauge/Math.max(this.aspect,1)}getViewBounds(t,e,n){vi.set(-1,-1,.5).applyMatrix4(this.projectionMatrixInverse),e.set(vi.x,vi.y).multiplyScalar(-t/vi.z),vi.set(1,1,.5).applyMatrix4(this.projectionMatrixInverse),n.set(vi.x,vi.y).multiplyScalar(-t/vi.z)}getViewSize(t,e){return this.getViewBounds(t,Iu,Lu),e.subVectors(Lu,Iu)}setViewOffset(t,e,n,s,r,a){this.aspect=t/e,this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=t,this.view.fullHeight=e,this.view.offsetX=n,this.view.offsetY=s,this.view.width=r,this.view.height=a,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let t=this.near,e=t*Math.tan(Yl*.5*this.fov)/this.zoom,n=2*e,s=this.aspect*n,r=-.5*s,a=this.view;if(this.view!==null&&this.view.enabled){let l=a.fullWidth,c=a.fullHeight;r+=a.offsetX*s/l,e-=a.offsetY*n/c,s*=a.width/l,n*=a.height/c}let o=this.filmOffset;o!==0&&(r+=t*o/this.getFilmWidth()),this.projectionMatrix.makePerspective(r,r+s,e,e-n,t,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(t){let e=super.toJSON(t);return e.object.fov=this.fov,e.object.zoom=this.zoom,e.object.near=this.near,e.object.far=this.far,e.object.focus=this.focus,e.object.aspect=this.aspect,this.view!==null&&(e.object.view=Object.assign({},this.view)),e.object.filmGauge=this.filmGauge,e.object.filmOffset=this.filmOffset,e}};var is=class extends pr{constructor(t=-1,e=1,n=1,s=-1,r=.1,a=2e3){super(),this.isOrthographicCamera=!0,this.type="OrthographicCamera",this.zoom=1,this.view=null,this.left=t,this.right=e,this.top=n,this.bottom=s,this.near=r,this.far=a,this.updateProjectionMatrix()}copy(t,e){return super.copy(t,e),this.left=t.left,this.right=t.right,this.top=t.top,this.bottom=t.bottom,this.near=t.near,this.far=t.far,this.zoom=t.zoom,this.view=t.view===null?null:Object.assign({},t.view),this}setViewOffset(t,e,n,s,r,a){this.view===null&&(this.view={enabled:!0,fullWidth:1,fullHeight:1,offsetX:0,offsetY:0,width:1,height:1}),this.view.enabled=!0,this.view.fullWidth=t,this.view.fullHeight=e,this.view.offsetX=n,this.view.offsetY=s,this.view.width=r,this.view.height=a,this.updateProjectionMatrix()}clearViewOffset(){this.view!==null&&(this.view.enabled=!1),this.updateProjectionMatrix()}updateProjectionMatrix(){let t=(this.right-this.left)/(2*this.zoom),e=(this.top-this.bottom)/(2*this.zoom),n=(this.right+this.left)/2,s=(this.top+this.bottom)/2,r=n-t,a=n+t,o=s+e,l=s-e;if(this.view!==null&&this.view.enabled){let c=(this.right-this.left)/this.view.fullWidth/this.zoom,h=(this.top-this.bottom)/this.view.fullHeight/this.zoom;r+=c*this.view.offsetX,a=r+c*this.view.width,o-=h*this.view.offsetY,l=o-h*this.view.height}this.projectionMatrix.makeOrthographic(r,a,o,l,this.near,this.far,this.coordinateSystem,this.reversedDepth),this.projectionMatrixInverse.copy(this.projectionMatrix).invert()}toJSON(t){let e=super.toJSON(t);return e.object.zoom=this.zoom,e.object.left=this.left,e.object.right=this.right,e.object.top=this.top,e.object.bottom=this.bottom,e.object.near=this.near,e.object.far=this.far,this.view!==null&&(e.object.view=Object.assign({},this.view)),e}};var ws=-90,As=1,ho=class extends sn{constructor(t,e,n){super(),this.type="CubeCamera",this.renderTarget=n,this.coordinateSystem=null,this.activeMipmapLevel=0;let s=new Xe(ws,As,t,e);s.layers=this.layers,this.add(s);let r=new Xe(ws,As,t,e);r.layers=this.layers,this.add(r);let a=new Xe(ws,As,t,e);a.layers=this.layers,this.add(a);let o=new Xe(ws,As,t,e);o.layers=this.layers,this.add(o);let l=new Xe(ws,As,t,e);l.layers=this.layers,this.add(l);let c=new Xe(ws,As,t,e);c.layers=this.layers,this.add(c)}updateCoordinateSystem(){let t=this.coordinateSystem,e=this.children.concat(),[n,s,r,a,o,l]=e;for(let c of e)this.remove(c);if(t===An)n.up.set(0,1,0),n.lookAt(1,0,0),s.up.set(0,1,0),s.lookAt(-1,0,0),r.up.set(0,0,-1),r.lookAt(0,1,0),a.up.set(0,0,1),a.lookAt(0,-1,0),o.up.set(0,1,0),o.lookAt(0,0,1),l.up.set(0,1,0),l.lookAt(0,0,-1);else if(t===er)n.up.set(0,-1,0),n.lookAt(-1,0,0),s.up.set(0,-1,0),s.lookAt(1,0,0),r.up.set(0,0,1),r.lookAt(0,1,0),a.up.set(0,0,-1),a.lookAt(0,-1,0),o.up.set(0,-1,0),o.lookAt(0,0,1),l.up.set(0,-1,0),l.lookAt(0,0,-1);else throw new Error("THREE.CubeCamera.updateCoordinateSystem(): Invalid coordinate system: "+t);for(let c of e)this.add(c),c.updateMatrixWorld()}update(t,e){this.parent===null&&this.updateMatrixWorld();let{renderTarget:n,activeMipmapLevel:s}=this;this.coordinateSystem!==t.coordinateSystem&&(this.coordinateSystem=t.coordinateSystem,this.updateCoordinateSystem());let[r,a,o,l,c,h]=this.children,f=t.getRenderTarget(),u=t.getActiveCubeFace(),p=t.getActiveMipmapLevel(),g=t.xr.enabled;t.xr.enabled=!1;let x=n.texture.generateMipmaps;n.texture.generateMipmaps=!1;let m=!1;t.isWebGLRenderer===!0?m=t.state.buffers.depth.getReversed():m=t.reversedDepthBuffer,t.setRenderTarget(n,0,s),m&&t.autoClear===!1&&t.clearDepth(),t.render(e,r),t.setRenderTarget(n,1,s),m&&t.autoClear===!1&&t.clearDepth(),t.render(e,a),t.setRenderTarget(n,2,s),m&&t.autoClear===!1&&t.clearDepth(),t.render(e,o),t.setRenderTarget(n,3,s),m&&t.autoClear===!1&&t.clearDepth(),t.render(e,l),t.setRenderTarget(n,4,s),m&&t.autoClear===!1&&t.clearDepth(),t.render(e,c),n.texture.generateMipmaps=x,t.setRenderTarget(n,5,s),m&&t.autoClear===!1&&t.clearDepth(),t.render(e,h),t.setRenderTarget(f,u,p),t.xr.enabled=g,n.texture.needsPMREMUpdate=!0}},uo=class extends Xe{constructor(t=[]){super(),this.isArrayCamera=!0,this.isMultiViewCamera=!1,this.cameras=t}},mr=class{constructor(){this._previousTime=0,this._currentTime=0,this._startTime=performance.now(),this._delta=0,this._elapsed=0,this._timescale=1,this._document=null,this._pageVisibilityHandler=null}connect(t){this._document=t,t.hidden!==void 0&&(this._pageVisibilityHandler=tg.bind(this),t.addEventListener("visibilitychange",this._pageVisibilityHandler,!1))}disconnect(){this._pageVisibilityHandler!==null&&(this._document.removeEventListener("visibilitychange",this._pageVisibilityHandler),this._pageVisibilityHandler=null),this._document=null}getDelta(){return this._delta/1e3}getElapsed(){return this._elapsed/1e3}getTimescale(){return this._timescale}setTimescale(t){return this._timescale=t,this}reset(){return this._currentTime=performance.now()-this._startTime,this}dispose(){this.disconnect()}update(t){return this._pageVisibilityHandler!==null&&this._document.hidden===!0?this._delta=0:(this._previousTime=this._currentTime,this._currentTime=(t!==void 0?t:performance.now())-this._startTime,this._delta=(this._currentTime-this._previousTime)*this._timescale,this._elapsed+=this._delta),this}};function tg(){this._document.hidden===!1&&this.reset()}var Gc="\\[\\]\\.:\\/",eg=new RegExp("["+Gc+"]","g"),Hc="[^"+Gc+"]",ng="[^"+Gc.replace("\\.","")+"]",ig=/((?:WC+[\/:])*)/.source.replace("WC",Hc),sg=/(WCOD+)?/.source.replace("WCOD",ng),rg=/(?:\.(WC+)(?:\[(.+)\])?)?/.source.replace("WC",Hc),ag=/\.(WC+)(?:\[(.+)\])?/.source.replace("WC",Hc),og=new RegExp("^"+ig+sg+rg+ag+"$"),lg=["material","materials","bones","map"],wc=class{constructor(t,e,n){let s=n||fe.parseTrackName(e);this._targetGroup=t,this._bindings=t.subscribe_(e,s)}getValue(t,e){this.bind();let n=this._targetGroup.nCachedObjects_,s=this._bindings[n];s!==void 0&&s.getValue(t,e)}setValue(t,e){let n=this._bindings;for(let s=this._targetGroup.nCachedObjects_,r=n.length;s!==r;++s)n[s].setValue(t,e)}bind(){let t=this._bindings;for(let e=this._targetGroup.nCachedObjects_,n=t.length;e!==n;++e)t[e].bind()}unbind(){let t=this._bindings;for(let e=this._targetGroup.nCachedObjects_,n=t.length;e!==n;++e)t[e].unbind()}},fe=class i{constructor(t,e,n){this.path=e,this.parsedPath=n||i.parseTrackName(e),this.node=i.findNode(t,this.parsedPath.nodeName),this.rootNode=t,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}static create(t,e,n){return t&&t.isAnimationObjectGroup?new i.Composite(t,e,n):new i(t,e,n)}static sanitizeNodeName(t){return t.replace(/\s/g,"_").replace(eg,"")}static parseTrackName(t){let e=og.exec(t);if(e===null)throw new Error("PropertyBinding: Cannot parse trackName: "+t);let n={nodeName:e[2],objectName:e[3],objectIndex:e[4],propertyName:e[5],propertyIndex:e[6]},s=n.nodeName&&n.nodeName.lastIndexOf(".");if(s!==void 0&&s!==-1){let r=n.nodeName.substring(s+1);lg.indexOf(r)!==-1&&(n.nodeName=n.nodeName.substring(0,s),n.objectName=r)}if(n.propertyName===null||n.propertyName.length===0)throw new Error("PropertyBinding: can not parse propertyName from trackName: "+t);return n}static findNode(t,e){if(e===void 0||e===""||e==="."||e===-1||e===t.name||e===t.uuid)return t;if(t.skeleton){let n=t.skeleton.getBoneByName(e);if(n!==void 0)return n}if(t.children){let n=function(r){for(let a=0;a<r.length;a++){let o=r[a];if(o.name===e||o.uuid===e)return o;let l=n(o.children);if(l)return l}return null},s=n(t.children);if(s)return s}return null}_getValue_unavailable(){}_setValue_unavailable(){}_getValue_direct(t,e){t[e]=this.targetObject[this.propertyName]}_getValue_array(t,e){let n=this.resolvedProperty;for(let s=0,r=n.length;s!==r;++s)t[e++]=n[s]}_getValue_arrayElement(t,e){t[e]=this.resolvedProperty[this.propertyIndex]}_getValue_toArray(t,e){this.resolvedProperty.toArray(t,e)}_setValue_direct(t,e){this.targetObject[this.propertyName]=t[e]}_setValue_direct_setNeedsUpdate(t,e){this.targetObject[this.propertyName]=t[e],this.targetObject.needsUpdate=!0}_setValue_direct_setMatrixWorldNeedsUpdate(t,e){this.targetObject[this.propertyName]=t[e],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_array(t,e){let n=this.resolvedProperty;for(let s=0,r=n.length;s!==r;++s)n[s]=t[e++]}_setValue_array_setNeedsUpdate(t,e){let n=this.resolvedProperty;for(let s=0,r=n.length;s!==r;++s)n[s]=t[e++];this.targetObject.needsUpdate=!0}_setValue_array_setMatrixWorldNeedsUpdate(t,e){let n=this.resolvedProperty;for(let s=0,r=n.length;s!==r;++s)n[s]=t[e++];this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_arrayElement(t,e){this.resolvedProperty[this.propertyIndex]=t[e]}_setValue_arrayElement_setNeedsUpdate(t,e){this.resolvedProperty[this.propertyIndex]=t[e],this.targetObject.needsUpdate=!0}_setValue_arrayElement_setMatrixWorldNeedsUpdate(t,e){this.resolvedProperty[this.propertyIndex]=t[e],this.targetObject.matrixWorldNeedsUpdate=!0}_setValue_fromArray(t,e){this.resolvedProperty.fromArray(t,e)}_setValue_fromArray_setNeedsUpdate(t,e){this.resolvedProperty.fromArray(t,e),this.targetObject.needsUpdate=!0}_setValue_fromArray_setMatrixWorldNeedsUpdate(t,e){this.resolvedProperty.fromArray(t,e),this.targetObject.matrixWorldNeedsUpdate=!0}_getValue_unbound(t,e){this.bind(),this.getValue(t,e)}_setValue_unbound(t,e){this.bind(),this.setValue(t,e)}bind(){let t=this.node,e=this.parsedPath,n=e.objectName,s=e.propertyName,r=e.propertyIndex;if(t||(t=i.findNode(this.rootNode,e.nodeName),this.node=t),this.getValue=this._getValue_unavailable,this.setValue=this._setValue_unavailable,!t){Et("PropertyBinding: No target node found for track: "+this.path+".");return}if(n){let c=e.objectIndex;switch(n){case"materials":if(!t.material){Rt("PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!t.material.materials){Rt("PropertyBinding: Can not bind to material.materials as node.material does not have a materials array.",this);return}t=t.material.materials;break;case"bones":if(!t.skeleton){Rt("PropertyBinding: Can not bind to bones as node does not have a skeleton.",this);return}t=t.skeleton.bones;for(let h=0;h<t.length;h++)if(t[h].name===c){c=h;break}break;case"map":if("map"in t){t=t.map;break}if(!t.material){Rt("PropertyBinding: Can not bind to material as node does not have a material.",this);return}if(!t.material.map){Rt("PropertyBinding: Can not bind to material.map as node.material does not have a map.",this);return}t=t.material.map;break;default:if(t[n]===void 0){Rt("PropertyBinding: Can not bind to objectName of node undefined.",this);return}t=t[n]}if(c!==void 0){if(t[c]===void 0){Rt("PropertyBinding: Trying to bind to objectIndex of objectName, but is undefined.",this,t);return}t=t[c]}}let a=t[s];if(a===void 0){let c=e.nodeName;Rt("PropertyBinding: Trying to update property for track: "+c+"."+s+" but it wasn't found.",t);return}let o=this.Versioning.None;this.targetObject=t,t.isMaterial===!0?o=this.Versioning.NeedsUpdate:t.isObject3D===!0&&(o=this.Versioning.MatrixWorldNeedsUpdate);let l=this.BindingType.Direct;if(r!==void 0){if(s==="morphTargetInfluences"){if(!t.geometry){Rt("PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.",this);return}if(!t.geometry.morphAttributes){Rt("PropertyBinding: Can not bind to morphTargetInfluences because node does not have a geometry.morphAttributes.",this);return}t.morphTargetDictionary[r]!==void 0&&(r=t.morphTargetDictionary[r])}l=this.BindingType.ArrayElement,this.resolvedProperty=a,this.propertyIndex=r}else a.fromArray!==void 0&&a.toArray!==void 0?(l=this.BindingType.HasFromToArray,this.resolvedProperty=a):Array.isArray(a)?(l=this.BindingType.EntireArray,this.resolvedProperty=a):this.propertyName=s;this.getValue=this.GetterByBindingType[l],this.setValue=this.SetterByBindingTypeAndVersioning[l][o]}unbind(){this.node=null,this.getValue=this._getValue_unbound,this.setValue=this._setValue_unbound}};fe.Composite=wc;fe.prototype.BindingType={Direct:0,EntireArray:1,ArrayElement:2,HasFromToArray:3};fe.prototype.Versioning={None:0,NeedsUpdate:1,MatrixWorldNeedsUpdate:2};fe.prototype.GetterByBindingType=[fe.prototype._getValue_direct,fe.prototype._getValue_array,fe.prototype._getValue_arrayElement,fe.prototype._getValue_toArray];fe.prototype.SetterByBindingTypeAndVersioning=[[fe.prototype._setValue_direct,fe.prototype._setValue_direct_setNeedsUpdate,fe.prototype._setValue_direct_setMatrixWorldNeedsUpdate],[fe.prototype._setValue_array,fe.prototype._setValue_array_setNeedsUpdate,fe.prototype._setValue_array_setMatrixWorldNeedsUpdate],[fe.prototype._setValue_arrayElement,fe.prototype._setValue_arrayElement_setNeedsUpdate,fe.prototype._setValue_arrayElement_setMatrixWorldNeedsUpdate],[fe.prototype._setValue_fromArray,fe.prototype._setValue_fromArray_setNeedsUpdate,fe.prototype._setValue_fromArray_setMatrixWorldNeedsUpdate]];var aM=new Float32Array(1);var Jc=class Jc{constructor(t,e,n,s){this.elements=[1,0,0,1],t!==void 0&&this.set(t,e,n,s)}identity(){return this.set(1,0,0,1),this}fromArray(t,e=0){for(let n=0;n<4;n++)this.elements[n]=t[n+e];return this}set(t,e,n,s){let r=this.elements;return r[0]=t,r[2]=e,r[1]=n,r[3]=s,this}};Jc.prototype.isMatrix2=!0;var Ac=Jc;function Wc(i,t,e,n){let s=cg(n);switch(e){case Fc:return i*t;case Oc:return i*t/s.components*s.byteLength;case Mo:return i*t/s.components*s.byteLength;case Li:return i*t*2/s.components*s.byteLength;case bo:return i*t*2/s.components*s.byteLength;case Uc:return i*t*3/s.components*s.byteLength;case yn:return i*t*4/s.components*s.byteLength;case So:return i*t*4/s.components*s.byteLength;case Ar:case Tr:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*8;case Er:case Cr:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*16;case Ao:case Eo:return Math.max(i,16)*Math.max(t,8)/4;case wo:case To:return Math.max(i,8)*Math.max(t,8)/2;case Co:case Ro:case Io:case Lo:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*8;case Po:case Rr:case No:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*16;case Do:return Math.floor((i+3)/4)*Math.floor((t+3)/4)*16;case Fo:return Math.floor((i+4)/5)*Math.floor((t+3)/4)*16;case Uo:return Math.floor((i+4)/5)*Math.floor((t+4)/5)*16;case Oo:return Math.floor((i+5)/6)*Math.floor((t+4)/5)*16;case Bo:return Math.floor((i+5)/6)*Math.floor((t+5)/6)*16;case ko:return Math.floor((i+7)/8)*Math.floor((t+4)/5)*16;case zo:return Math.floor((i+7)/8)*Math.floor((t+5)/6)*16;case Vo:return Math.floor((i+7)/8)*Math.floor((t+7)/8)*16;case Go:return Math.floor((i+9)/10)*Math.floor((t+4)/5)*16;case Ho:return Math.floor((i+9)/10)*Math.floor((t+5)/6)*16;case Wo:return Math.floor((i+9)/10)*Math.floor((t+7)/8)*16;case Xo:return Math.floor((i+9)/10)*Math.floor((t+9)/10)*16;case qo:return Math.floor((i+11)/12)*Math.floor((t+9)/10)*16;case Yo:return Math.floor((i+11)/12)*Math.floor((t+11)/12)*16;case Zo:case Jo:case $o:return Math.ceil(i/4)*Math.ceil(t/4)*16;case Ko:case jo:return Math.ceil(i/4)*Math.ceil(t/4)*8;case Pr:case Qo:return Math.ceil(i/4)*Math.ceil(t/4)*16}throw new Error(`Unable to determine texture byte length for ${e} format.`)}function cg(i){switch(i){case mn:case Ic:return{byteLength:1,components:1};case Ds:case Lc:case qe:return{byteLength:2,components:1};case vo:case yo:return{byteLength:2,components:4};case En:case xo:case Cn:return{byteLength:4,components:1};case Nc:case Dc:return{byteLength:4,components:3}}throw new Error(`Unknown texture type ${i}.`)}typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("register",{detail:{revision:po}}));typeof window<"u"&&(window.__THREE__?Et("WARNING: Multiple instances of Three.js being imported."):window.__THREE__=po);function zf(){let i=null,t=!1,e=null,n=null;function s(r,a){e(r,a),n=i.requestAnimationFrame(s)}return{start:function(){t!==!0&&e!==null&&i!==null&&(n=i.requestAnimationFrame(s),t=!0)},stop:function(){i!==null&&i.cancelAnimationFrame(n),t=!1},setAnimationLoop:function(r){e=r},setContext:function(r){i=r}}}function hg(i){let t=new WeakMap;function e(o,l){let c=o.array,h=o.usage,f=c.byteLength,u=i.createBuffer();i.bindBuffer(l,u),i.bufferData(l,c,h),o.onUploadCallback();let p;if(c instanceof Float32Array)p=i.FLOAT;else if(typeof Float16Array<"u"&&c instanceof Float16Array)p=i.HALF_FLOAT;else if(c instanceof Uint16Array)o.isFloat16BufferAttribute?p=i.HALF_FLOAT:p=i.UNSIGNED_SHORT;else if(c instanceof Int16Array)p=i.SHORT;else if(c instanceof Uint32Array)p=i.UNSIGNED_INT;else if(c instanceof Int32Array)p=i.INT;else if(c instanceof Int8Array)p=i.BYTE;else if(c instanceof Uint8Array)p=i.UNSIGNED_BYTE;else if(c instanceof Uint8ClampedArray)p=i.UNSIGNED_BYTE;else throw new Error("THREE.WebGLAttributes: Unsupported buffer data format: "+c);return{buffer:u,type:p,bytesPerElement:c.BYTES_PER_ELEMENT,version:o.version,size:f}}function n(o,l,c){let h=l.array,f=l.updateRanges;if(i.bindBuffer(c,o),f.length===0)i.bufferSubData(c,0,h);else{f.sort((p,g)=>p.start-g.start);let u=0;for(let p=1;p<f.length;p++){let g=f[u],x=f[p];x.start<=g.start+g.count+1?g.count=Math.max(g.count,x.start+x.count-g.start):(++u,f[u]=x)}f.length=u+1;for(let p=0,g=f.length;p<g;p++){let x=f[p];i.bufferSubData(c,x.start*h.BYTES_PER_ELEMENT,h,x.start,x.count)}l.clearUpdateRanges()}l.onUploadCallback()}function s(o){return o.isInterleavedBufferAttribute&&(o=o.data),t.get(o)}function r(o){o.isInterleavedBufferAttribute&&(o=o.data);let l=t.get(o);l&&(i.deleteBuffer(l.buffer),t.delete(o))}function a(o,l){if(o.isInterleavedBufferAttribute&&(o=o.data),o.isGLBufferAttribute){let h=t.get(o);(!h||h.version<o.version)&&t.set(o,{buffer:o.buffer,type:o.type,bytesPerElement:o.elementSize,version:o.version});return}let c=t.get(o);if(c===void 0)t.set(o,e(o,l));else if(c.version<o.version){if(c.size!==o.array.byteLength)throw new Error("THREE.WebGLAttributes: The size of the buffer attribute's array buffer does not match the original size. Resizing buffer attributes is not supported.");n(c.buffer,o,l),c.version=o.version}}return{get:s,remove:r,update:a}}var ug=`#ifdef USE_ALPHAHASH
	if ( diffuseColor.a < getAlphaHashThreshold( vPosition ) ) discard;
#endif`,fg=`#ifdef USE_ALPHAHASH
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
#endif`,dg=`#ifdef USE_ALPHAMAP
	diffuseColor.a *= texture2D( alphaMap, vAlphaMapUv ).g;
#endif`,pg=`#ifdef USE_ALPHAMAP
	uniform sampler2D alphaMap;
#endif`,mg=`#ifdef USE_ALPHATEST
	#ifdef ALPHA_TO_COVERAGE
	diffuseColor.a = smoothstep( alphaTest, alphaTest + fwidth( diffuseColor.a ), diffuseColor.a );
	if ( diffuseColor.a == 0.0 ) discard;
	#else
	if ( diffuseColor.a < alphaTest ) discard;
	#endif
#endif`,gg=`#ifdef USE_ALPHATEST
	uniform float alphaTest;
#endif`,_g=`#ifdef USE_AOMAP
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
#endif`,xg=`#ifdef USE_AOMAP
	uniform sampler2D aoMap;
	uniform float aoMapIntensity;
#endif`,vg=`#ifdef USE_BATCHING
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
#endif`,yg=`#ifdef USE_BATCHING
	mat4 batchingMatrix = getBatchingMatrix( getIndirectIndex( gl_DrawID ) );
#endif`,Mg=`vec3 transformed = vec3( position );
#ifdef USE_ALPHAHASH
	vPosition = vec3( position );
#endif`,bg=`vec3 objectNormal = vec3( normal );
#ifdef USE_TANGENT
	vec3 objectTangent = vec3( tangent.xyz );
#endif`,Sg=`float G_BlinnPhong_Implicit( ) {
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
} // validated`,wg=`#ifdef USE_IRIDESCENCE
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
#endif`,Ag=`#ifdef USE_BUMPMAP
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
#endif`,Tg=`#if NUM_CLIPPING_PLANES > 0
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
#endif`,Eg=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
	uniform vec4 clippingPlanes[ NUM_CLIPPING_PLANES ];
#endif`,Cg=`#if NUM_CLIPPING_PLANES > 0
	varying vec3 vClipPosition;
#endif`,Rg=`#if NUM_CLIPPING_PLANES > 0
	vClipPosition = - mvPosition.xyz;
#endif`,Pg=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA )
	diffuseColor *= vColor;
#endif`,Ig=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA )
	varying vec4 vColor;
#endif`,Lg=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
	varying vec4 vColor;
#endif`,Ng=`#if defined( USE_COLOR ) || defined( USE_COLOR_ALPHA ) || defined( USE_INSTANCING_COLOR ) || defined( USE_BATCHING_COLOR )
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
#endif`,Dg=`#define PI 3.141592653589793
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
} // validated`,Fg=`#ifdef ENVMAP_TYPE_CUBE_UV
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
#endif`,Ug=`vec3 transformedNormal = objectNormal;
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
#endif`,Og=`#ifdef USE_DISPLACEMENTMAP
	uniform sampler2D displacementMap;
	uniform float displacementScale;
	uniform float displacementBias;
#endif`,Bg=`#ifdef USE_DISPLACEMENTMAP
	transformed += normalize( objectNormal ) * ( texture2D( displacementMap, vDisplacementMapUv ).x * displacementScale + displacementBias );
#endif`,kg=`#ifdef USE_EMISSIVEMAP
	vec4 emissiveColor = texture2D( emissiveMap, vEmissiveMapUv );
	#ifdef DECODE_VIDEO_TEXTURE_EMISSIVE
		emissiveColor = sRGBTransferEOTF( emissiveColor );
	#endif
	totalEmissiveRadiance *= emissiveColor.rgb;
#endif`,zg=`#ifdef USE_EMISSIVEMAP
	uniform sampler2D emissiveMap;
#endif`,Vg="gl_FragColor = linearToOutputTexel( gl_FragColor );",Gg=`vec4 LinearTransferOETF( in vec4 value ) {
	return value;
}
vec4 sRGBTransferEOTF( in vec4 value ) {
	return vec4( mix( pow( value.rgb * 0.9478672986 + vec3( 0.0521327014 ), vec3( 2.4 ) ), value.rgb * 0.0773993808, vec3( lessThanEqual( value.rgb, vec3( 0.04045 ) ) ) ), value.a );
}
vec4 sRGBTransferOETF( in vec4 value ) {
	return vec4( mix( pow( value.rgb, vec3( 0.41666 ) ) * 1.055 - vec3( 0.055 ), value.rgb * 12.92, vec3( lessThanEqual( value.rgb, vec3( 0.0031308 ) ) ) ), value.a );
}`,Hg=`#ifdef USE_ENVMAP
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
#endif`,Wg=`#ifdef USE_ENVMAP
	uniform float envMapIntensity;
	uniform mat3 envMapRotation;
	#ifdef ENVMAP_TYPE_CUBE
		uniform samplerCube envMap;
	#else
		uniform sampler2D envMap;
	#endif
#endif`,Xg=`#ifdef USE_ENVMAP
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
#endif`,qg=`#ifdef USE_ENVMAP
	#if defined( USE_BUMPMAP ) || defined( USE_NORMALMAP ) || defined( PHONG ) || defined( LAMBERT )
		#define ENV_WORLDPOS
	#endif
	#ifdef ENV_WORLDPOS
		
		varying vec3 vWorldPosition;
	#else
		varying vec3 vReflect;
		uniform float refractionRatio;
	#endif
#endif`,Yg=`#ifdef USE_ENVMAP
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
#endif`,Zg=`#ifdef USE_FOG
	vFogDepth = - mvPosition.z;
#endif`,Jg=`#ifdef USE_FOG
	varying float vFogDepth;
#endif`,$g=`#ifdef USE_FOG
	#ifdef FOG_EXP2
		float fogFactor = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
	#else
		float fogFactor = smoothstep( fogNear, fogFar, vFogDepth );
	#endif
	gl_FragColor.rgb = mix( gl_FragColor.rgb, fogColor, fogFactor );
#endif`,Kg=`#ifdef USE_FOG
	uniform vec3 fogColor;
	varying float vFogDepth;
	#ifdef FOG_EXP2
		uniform float fogDensity;
	#else
		uniform float fogNear;
		uniform float fogFar;
	#endif
#endif`,jg=`#ifdef USE_GRADIENTMAP
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
}`,Qg=`#ifdef USE_LIGHTMAP
	uniform sampler2D lightMap;
	uniform float lightMapIntensity;
#endif`,t0=`LambertMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularStrength = specularStrength;`,e0=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Lambert`,n0=`uniform bool receiveShadow;
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
#include <lightprobes_pars_fragment>`,i0=`#ifdef USE_ENVMAP
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
#endif`,s0=`ToonMaterial material;
material.diffuseColor = diffuseColor.rgb;`,r0=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_Toon`,a0=`BlinnPhongMaterial material;
material.diffuseColor = diffuseColor.rgb;
material.specularColor = specular;
material.specularShininess = shininess;
material.specularStrength = specularStrength;`,o0=`varying vec3 vViewPosition;
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
#define RE_IndirectDiffuse		RE_IndirectDiffuse_BlinnPhong`,l0=`PhysicalMaterial material;
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
#endif`,c0=`uniform sampler2D dfgLUT;
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
}`,h0=`
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
#endif`,u0=`#if defined( RE_IndirectDiffuse )
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
#endif`,f0=`#if defined( RE_IndirectDiffuse )
	#if defined( LAMBERT ) || defined( PHONG )
		irradiance += iblIrradiance;
	#endif
	RE_IndirectDiffuse( irradiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif
#if defined( RE_IndirectSpecular )
	RE_IndirectSpecular( radiance, iblIrradiance, clearcoatRadiance, geometryPosition, geometryNormal, geometryViewDir, geometryClearcoatNormal, material, reflectedLight );
#endif`,d0=`#ifdef USE_LIGHT_PROBES_GRID
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
#endif`,p0=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	gl_FragDepth = vIsPerspective == 0.0 ? gl_FragCoord.z : log2( vFragDepth ) * logDepthBufFC * 0.5;
#endif`,m0=`#if defined( USE_LOGARITHMIC_DEPTH_BUFFER )
	uniform float logDepthBufFC;
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,g0=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	varying float vFragDepth;
	varying float vIsPerspective;
#endif`,_0=`#ifdef USE_LOGARITHMIC_DEPTH_BUFFER
	vFragDepth = 1.0 + gl_Position.w;
	vIsPerspective = float( isPerspectiveMatrix( projectionMatrix ) );
#endif`,x0=`#ifdef USE_MAP
	vec4 sampledDiffuseColor = texture2D( map, vMapUv );
	#ifdef DECODE_VIDEO_TEXTURE
		sampledDiffuseColor = sRGBTransferEOTF( sampledDiffuseColor );
	#endif
	diffuseColor *= sampledDiffuseColor;
#endif`,v0=`#ifdef USE_MAP
	uniform sampler2D map;
#endif`,y0=`#if defined( USE_MAP ) || defined( USE_ALPHAMAP )
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
#endif`,M0=`#if defined( USE_POINTS_UV )
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
#endif`,b0=`float metalnessFactor = metalness;
#ifdef USE_METALNESSMAP
	vec4 texelMetalness = texture2D( metalnessMap, vMetalnessMapUv );
	metalnessFactor *= texelMetalness.b;
#endif`,S0=`#ifdef USE_METALNESSMAP
	uniform sampler2D metalnessMap;
#endif`,w0=`#ifdef USE_INSTANCING_MORPH
	float morphTargetInfluences[ MORPHTARGETS_COUNT ];
	float morphTargetBaseInfluence = texelFetch( morphTexture, ivec2( 0, gl_InstanceID ), 0 ).r;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		morphTargetInfluences[i] =  texelFetch( morphTexture, ivec2( i + 1, gl_InstanceID ), 0 ).r;
	}
#endif`,A0=`#if defined( USE_MORPHCOLORS )
	vColor *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		#if defined( USE_COLOR_ALPHA )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ) * morphTargetInfluences[ i ];
		#elif defined( USE_COLOR )
			if ( morphTargetInfluences[ i ] != 0.0 ) vColor += getMorph( gl_VertexID, i, 2 ).rgb * morphTargetInfluences[ i ];
		#endif
	}
#endif`,T0=`#ifdef USE_MORPHNORMALS
	objectNormal *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) objectNormal += getMorph( gl_VertexID, i, 1 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,E0=`#ifdef USE_MORPHTARGETS
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
#endif`,C0=`#ifdef USE_MORPHTARGETS
	transformed *= morphTargetBaseInfluence;
	for ( int i = 0; i < MORPHTARGETS_COUNT; i ++ ) {
		if ( morphTargetInfluences[ i ] != 0.0 ) transformed += getMorph( gl_VertexID, i, 0 ).xyz * morphTargetInfluences[ i ];
	}
#endif`,R0=`float faceDirection = gl_FrontFacing ? 1.0 : - 1.0;
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
vec3 nonPerturbedNormal = normal;`,P0=`#ifdef USE_NORMALMAP_OBJECTSPACE
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
#endif`,I0=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,L0=`#ifndef FLAT_SHADED
	varying vec3 vNormal;
	#ifdef USE_TANGENT
		varying vec3 vTangent;
		varying vec3 vBitangent;
	#endif
#endif`,N0=`#ifndef FLAT_SHADED
	vNormal = normalize( transformedNormal );
	#ifdef USE_TANGENT
		vTangent = normalize( transformedTangent );
		vBitangent = normalize( cross( vNormal, vTangent ) * tangent.w );
	#endif
#endif`,D0=`#ifdef USE_NORMALMAP
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
#endif`,F0=`#ifdef USE_CLEARCOAT
	vec3 clearcoatNormal = nonPerturbedNormal;
#endif`,U0=`#ifdef USE_CLEARCOAT_NORMALMAP
	vec3 clearcoatMapN = texture2D( clearcoatNormalMap, vClearcoatNormalMapUv ).xyz * 2.0 - 1.0;
	clearcoatMapN.xy *= clearcoatNormalScale;
	clearcoatNormal = normalize( tbn2 * clearcoatMapN );
#endif`,O0=`#ifdef USE_CLEARCOATMAP
	uniform sampler2D clearcoatMap;
#endif
#ifdef USE_CLEARCOAT_NORMALMAP
	uniform sampler2D clearcoatNormalMap;
	uniform vec2 clearcoatNormalScale;
#endif
#ifdef USE_CLEARCOAT_ROUGHNESSMAP
	uniform sampler2D clearcoatRoughnessMap;
#endif`,B0=`#ifdef USE_IRIDESCENCEMAP
	uniform sampler2D iridescenceMap;
#endif
#ifdef USE_IRIDESCENCE_THICKNESSMAP
	uniform sampler2D iridescenceThicknessMap;
#endif`,k0=`#ifdef OPAQUE
diffuseColor.a = 1.0;
#endif
#ifdef USE_TRANSMISSION
diffuseColor.a *= material.transmissionAlpha;
#endif
gl_FragColor = vec4( outgoingLight, diffuseColor.a );`,z0=`vec3 packNormalToRGB( const in vec3 normal ) {
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
}`,V0=`#ifdef PREMULTIPLIED_ALPHA
	gl_FragColor.rgb *= gl_FragColor.a;
#endif`,G0=`vec4 mvPosition = vec4( transformed, 1.0 );
#ifdef USE_BATCHING
	mvPosition = batchingMatrix * mvPosition;
#endif
#ifdef USE_INSTANCING
	mvPosition = instanceMatrix * mvPosition;
#endif
mvPosition = modelViewMatrix * mvPosition;
gl_Position = projectionMatrix * mvPosition;`,H0=`#ifdef DITHERING
	gl_FragColor.rgb = dithering( gl_FragColor.rgb );
#endif`,W0=`#ifdef DITHERING
	vec3 dithering( vec3 color ) {
		float grid_position = rand( gl_FragCoord.xy );
		vec3 dither_shift_RGB = vec3( 0.25 / 255.0, -0.25 / 255.0, 0.25 / 255.0 );
		dither_shift_RGB = mix( 2.0 * dither_shift_RGB, -2.0 * dither_shift_RGB, grid_position );
		return color + dither_shift_RGB;
	}
#endif`,X0=`float roughnessFactor = roughness;
#ifdef USE_ROUGHNESSMAP
	vec4 texelRoughness = texture2D( roughnessMap, vRoughnessMapUv );
	roughnessFactor *= texelRoughness.g;
#endif`,q0=`#ifdef USE_ROUGHNESSMAP
	uniform sampler2D roughnessMap;
#endif`,Y0=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,Z0=`#if NUM_SPOT_LIGHT_COORDS > 0
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
#endif`,J0=`#if ( defined( USE_SHADOWMAP ) && ( NUM_DIR_LIGHT_SHADOWS > 0 || NUM_POINT_LIGHT_SHADOWS > 0 ) ) || ( NUM_SPOT_LIGHT_COORDS > 0 )
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
#endif`,$0=`float getShadowMask() {
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
}`,K0=`#ifdef USE_SKINNING
	mat4 boneMatX = getBoneMatrix( skinIndex.x );
	mat4 boneMatY = getBoneMatrix( skinIndex.y );
	mat4 boneMatZ = getBoneMatrix( skinIndex.z );
	mat4 boneMatW = getBoneMatrix( skinIndex.w );
#endif`,j0=`#ifdef USE_SKINNING
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
#endif`,Q0=`#ifdef USE_SKINNING
	vec4 skinVertex = bindMatrix * vec4( transformed, 1.0 );
	vec4 skinned = vec4( 0.0 );
	skinned += boneMatX * skinVertex * skinWeight.x;
	skinned += boneMatY * skinVertex * skinWeight.y;
	skinned += boneMatZ * skinVertex * skinWeight.z;
	skinned += boneMatW * skinVertex * skinWeight.w;
	transformed = ( bindMatrixInverse * skinned ).xyz;
#endif`,t_=`#ifdef USE_SKINNING
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
#endif`,e_=`float specularStrength;
#ifdef USE_SPECULARMAP
	vec4 texelSpecular = texture2D( specularMap, vSpecularMapUv );
	specularStrength = texelSpecular.r;
#else
	specularStrength = 1.0;
#endif`,n_=`#ifdef USE_SPECULARMAP
	uniform sampler2D specularMap;
#endif`,i_=`#if defined( TONE_MAPPING )
	gl_FragColor.rgb = toneMapping( gl_FragColor.rgb );
#endif`,s_=`#ifndef saturate
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
vec3 CustomToneMapping( vec3 color ) { return color; }`,r_=`#ifdef USE_TRANSMISSION
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
#endif`,a_=`#ifdef USE_TRANSMISSION
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
#endif`,o_=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,l_=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,c_=`#if defined( USE_UV ) || defined( USE_ANISOTROPY )
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
#endif`,h_=`#if defined( USE_ENVMAP ) || defined( DISTANCE ) || defined ( USE_SHADOWMAP ) || defined ( USE_TRANSMISSION ) || NUM_SPOT_LIGHT_COORDS > 0
	vec4 worldPosition = vec4( transformed, 1.0 );
	#ifdef USE_BATCHING
		worldPosition = batchingMatrix * worldPosition;
	#endif
	#ifdef USE_INSTANCING
		worldPosition = instanceMatrix * worldPosition;
	#endif
	worldPosition = modelMatrix * worldPosition;
#endif`,u_=`varying vec2 vUv;
uniform mat3 uvTransform;
void main() {
	vUv = ( uvTransform * vec3( uv, 1 ) ).xy;
	gl_Position = vec4( position.xy, 1.0, 1.0 );
}`,f_=`uniform sampler2D t2D;
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
}`,d_=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,p_=`#ifdef ENVMAP_TYPE_CUBE
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
}`,m_=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
	gl_Position.z = gl_Position.w;
}`,g_=`uniform samplerCube tCube;
uniform float tFlip;
uniform float opacity;
varying vec3 vWorldDirection;
void main() {
	vec4 texColor = textureCube( tCube, vec3( tFlip * vWorldDirection.x, vWorldDirection.yz ) );
	gl_FragColor = texColor;
	gl_FragColor.a *= opacity;
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,__=`#include <common>
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
}`,x_=`#if DEPTH_PACKING == 3200
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
}`,v_=`#define DISTANCE
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
}`,y_=`#define DISTANCE
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
}`,M_=`varying vec3 vWorldDirection;
#include <common>
void main() {
	vWorldDirection = transformDirection( position, modelMatrix );
	#include <begin_vertex>
	#include <project_vertex>
}`,b_=`uniform sampler2D tEquirect;
varying vec3 vWorldDirection;
#include <common>
void main() {
	vec3 direction = normalize( vWorldDirection );
	vec2 sampleUV = equirectUv( direction );
	gl_FragColor = texture2D( tEquirect, sampleUV );
	#include <tonemapping_fragment>
	#include <colorspace_fragment>
}`,S_=`uniform float scale;
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
}`,w_=`uniform vec3 diffuse;
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
}`,A_=`#include <common>
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
}`,T_=`uniform vec3 diffuse;
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
}`,E_=`#define LAMBERT
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
}`,C_=`#define LAMBERT
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
}`,R_=`#define MATCAP
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
}`,P_=`#define MATCAP
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
}`,I_=`#define NORMAL
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
}`,L_=`#define NORMAL
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
}`,N_=`#define PHONG
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
}`,D_=`#define PHONG
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
}`,F_=`#define STANDARD
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
}`,U_=`#define STANDARD
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
}`,O_=`#define TOON
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
}`,B_=`#define TOON
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
}`,k_=`uniform float size;
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
}`,z_=`uniform vec3 diffuse;
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
}`,V_=`#include <common>
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
}`,G_=`uniform vec3 color;
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
}`,H_=`uniform float rotation;
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
}`,W_=`uniform vec3 diffuse;
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
}`,Vt={alphahash_fragment:ug,alphahash_pars_fragment:fg,alphamap_fragment:dg,alphamap_pars_fragment:pg,alphatest_fragment:mg,alphatest_pars_fragment:gg,aomap_fragment:_g,aomap_pars_fragment:xg,batching_pars_vertex:vg,batching_vertex:yg,begin_vertex:Mg,beginnormal_vertex:bg,bsdfs:Sg,iridescence_fragment:wg,bumpmap_pars_fragment:Ag,clipping_planes_fragment:Tg,clipping_planes_pars_fragment:Eg,clipping_planes_pars_vertex:Cg,clipping_planes_vertex:Rg,color_fragment:Pg,color_pars_fragment:Ig,color_pars_vertex:Lg,color_vertex:Ng,common:Dg,cube_uv_reflection_fragment:Fg,defaultnormal_vertex:Ug,displacementmap_pars_vertex:Og,displacementmap_vertex:Bg,emissivemap_fragment:kg,emissivemap_pars_fragment:zg,colorspace_fragment:Vg,colorspace_pars_fragment:Gg,envmap_fragment:Hg,envmap_common_pars_fragment:Wg,envmap_pars_fragment:Xg,envmap_pars_vertex:qg,envmap_physical_pars_fragment:i0,envmap_vertex:Yg,fog_vertex:Zg,fog_pars_vertex:Jg,fog_fragment:$g,fog_pars_fragment:Kg,gradientmap_pars_fragment:jg,lightmap_pars_fragment:Qg,lights_lambert_fragment:t0,lights_lambert_pars_fragment:e0,lights_pars_begin:n0,lights_toon_fragment:s0,lights_toon_pars_fragment:r0,lights_phong_fragment:a0,lights_phong_pars_fragment:o0,lights_physical_fragment:l0,lights_physical_pars_fragment:c0,lights_fragment_begin:h0,lights_fragment_maps:u0,lights_fragment_end:f0,lightprobes_pars_fragment:d0,logdepthbuf_fragment:p0,logdepthbuf_pars_fragment:m0,logdepthbuf_pars_vertex:g0,logdepthbuf_vertex:_0,map_fragment:x0,map_pars_fragment:v0,map_particle_fragment:y0,map_particle_pars_fragment:M0,metalnessmap_fragment:b0,metalnessmap_pars_fragment:S0,morphinstance_vertex:w0,morphcolor_vertex:A0,morphnormal_vertex:T0,morphtarget_pars_vertex:E0,morphtarget_vertex:C0,normal_fragment_begin:R0,normal_fragment_maps:P0,normal_pars_fragment:I0,normal_pars_vertex:L0,normal_vertex:N0,normalmap_pars_fragment:D0,clearcoat_normal_fragment_begin:F0,clearcoat_normal_fragment_maps:U0,clearcoat_pars_fragment:O0,iridescence_pars_fragment:B0,opaque_fragment:k0,packing:z0,premultiplied_alpha_fragment:V0,project_vertex:G0,dithering_fragment:H0,dithering_pars_fragment:W0,roughnessmap_fragment:X0,roughnessmap_pars_fragment:q0,shadowmap_pars_fragment:Y0,shadowmap_pars_vertex:Z0,shadowmap_vertex:J0,shadowmask_pars_fragment:$0,skinbase_vertex:K0,skinning_pars_vertex:j0,skinning_vertex:Q0,skinnormal_vertex:t_,specularmap_fragment:e_,specularmap_pars_fragment:n_,tonemapping_fragment:i_,tonemapping_pars_fragment:s_,transmission_fragment:r_,transmission_pars_fragment:a_,uv_pars_fragment:o_,uv_pars_vertex:l_,uv_vertex:c_,worldpos_vertex:h_,background_vert:u_,background_frag:f_,backgroundCube_vert:d_,backgroundCube_frag:p_,cube_vert:m_,cube_frag:g_,depth_vert:__,depth_frag:x_,distance_vert:v_,distance_frag:y_,equirect_vert:M_,equirect_frag:b_,linedashed_vert:S_,linedashed_frag:w_,meshbasic_vert:A_,meshbasic_frag:T_,meshlambert_vert:E_,meshlambert_frag:C_,meshmatcap_vert:R_,meshmatcap_frag:P_,meshnormal_vert:I_,meshnormal_frag:L_,meshphong_vert:N_,meshphong_frag:D_,meshphysical_vert:F_,meshphysical_frag:U_,meshtoon_vert:O_,meshtoon_frag:B_,points_vert:k_,points_frag:z_,shadow_vert:V_,shadow_frag:G_,sprite_vert:H_,sprite_frag:W_},ft={common:{diffuse:{value:new ut(16777215)},opacity:{value:1},map:{value:null},mapTransform:{value:new Dt},alphaMap:{value:null},alphaMapTransform:{value:new Dt},alphaTest:{value:0}},specularmap:{specularMap:{value:null},specularMapTransform:{value:new Dt}},envmap:{envMap:{value:null},envMapRotation:{value:new Dt},reflectivity:{value:1},ior:{value:1.5},refractionRatio:{value:.98},dfgLUT:{value:null}},aomap:{aoMap:{value:null},aoMapIntensity:{value:1},aoMapTransform:{value:new Dt}},lightmap:{lightMap:{value:null},lightMapIntensity:{value:1},lightMapTransform:{value:new Dt}},bumpmap:{bumpMap:{value:null},bumpMapTransform:{value:new Dt},bumpScale:{value:1}},normalmap:{normalMap:{value:null},normalMapTransform:{value:new Dt},normalScale:{value:new Ut(1,1)}},displacementmap:{displacementMap:{value:null},displacementMapTransform:{value:new Dt},displacementScale:{value:1},displacementBias:{value:0}},emissivemap:{emissiveMap:{value:null},emissiveMapTransform:{value:new Dt}},metalnessmap:{metalnessMap:{value:null},metalnessMapTransform:{value:new Dt}},roughnessmap:{roughnessMap:{value:null},roughnessMapTransform:{value:new Dt}},gradientmap:{gradientMap:{value:null}},fog:{fogDensity:{value:25e-5},fogNear:{value:1},fogFar:{value:2e3},fogColor:{value:new ut(16777215)}},lights:{ambientLightColor:{value:[]},lightProbe:{value:[]},directionalLights:{value:[],properties:{direction:{},color:{}}},directionalLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},directionalShadowMatrix:{value:[]},spotLights:{value:[],properties:{color:{},position:{},direction:{},distance:{},coneCos:{},penumbraCos:{},decay:{}}},spotLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{}}},spotLightMap:{value:[]},spotLightMatrix:{value:[]},pointLights:{value:[],properties:{color:{},position:{},decay:{},distance:{}}},pointLightShadows:{value:[],properties:{shadowIntensity:1,shadowBias:{},shadowNormalBias:{},shadowRadius:{},shadowMapSize:{},shadowCameraNear:{},shadowCameraFar:{}}},pointShadowMatrix:{value:[]},hemisphereLights:{value:[],properties:{direction:{},skyColor:{},groundColor:{}}},rectAreaLights:{value:[],properties:{color:{},position:{},width:{},height:{}}},ltc_1:{value:null},ltc_2:{value:null},probesSH:{value:null},probesMin:{value:new D},probesMax:{value:new D},probesResolution:{value:new D}},points:{diffuse:{value:new ut(16777215)},opacity:{value:1},size:{value:1},scale:{value:1},map:{value:null},alphaMap:{value:null},alphaMapTransform:{value:new Dt},alphaTest:{value:0},uvTransform:{value:new Dt}},sprite:{diffuse:{value:new ut(16777215)},opacity:{value:1},center:{value:new Ut(.5,.5)},rotation:{value:0},map:{value:null},mapTransform:{value:new Dt},alphaMap:{value:null},alphaMapTransform:{value:new Dt},alphaTest:{value:0}}},Gn={basic:{uniforms:Ye([ft.common,ft.specularmap,ft.envmap,ft.aomap,ft.lightmap,ft.fog]),vertexShader:Vt.meshbasic_vert,fragmentShader:Vt.meshbasic_frag},lambert:{uniforms:Ye([ft.common,ft.specularmap,ft.envmap,ft.aomap,ft.lightmap,ft.emissivemap,ft.bumpmap,ft.normalmap,ft.displacementmap,ft.fog,ft.lights,{emissive:{value:new ut(0)},envMapIntensity:{value:1}}]),vertexShader:Vt.meshlambert_vert,fragmentShader:Vt.meshlambert_frag},phong:{uniforms:Ye([ft.common,ft.specularmap,ft.envmap,ft.aomap,ft.lightmap,ft.emissivemap,ft.bumpmap,ft.normalmap,ft.displacementmap,ft.fog,ft.lights,{emissive:{value:new ut(0)},specular:{value:new ut(1118481)},shininess:{value:30},envMapIntensity:{value:1}}]),vertexShader:Vt.meshphong_vert,fragmentShader:Vt.meshphong_frag},standard:{uniforms:Ye([ft.common,ft.envmap,ft.aomap,ft.lightmap,ft.emissivemap,ft.bumpmap,ft.normalmap,ft.displacementmap,ft.roughnessmap,ft.metalnessmap,ft.fog,ft.lights,{emissive:{value:new ut(0)},roughness:{value:1},metalness:{value:0},envMapIntensity:{value:1}}]),vertexShader:Vt.meshphysical_vert,fragmentShader:Vt.meshphysical_frag},toon:{uniforms:Ye([ft.common,ft.aomap,ft.lightmap,ft.emissivemap,ft.bumpmap,ft.normalmap,ft.displacementmap,ft.gradientmap,ft.fog,ft.lights,{emissive:{value:new ut(0)}}]),vertexShader:Vt.meshtoon_vert,fragmentShader:Vt.meshtoon_frag},matcap:{uniforms:Ye([ft.common,ft.bumpmap,ft.normalmap,ft.displacementmap,ft.fog,{matcap:{value:null}}]),vertexShader:Vt.meshmatcap_vert,fragmentShader:Vt.meshmatcap_frag},points:{uniforms:Ye([ft.points,ft.fog]),vertexShader:Vt.points_vert,fragmentShader:Vt.points_frag},dashed:{uniforms:Ye([ft.common,ft.fog,{scale:{value:1},dashSize:{value:1},totalSize:{value:2}}]),vertexShader:Vt.linedashed_vert,fragmentShader:Vt.linedashed_frag},depth:{uniforms:Ye([ft.common,ft.displacementmap]),vertexShader:Vt.depth_vert,fragmentShader:Vt.depth_frag},normal:{uniforms:Ye([ft.common,ft.bumpmap,ft.normalmap,ft.displacementmap,{opacity:{value:1}}]),vertexShader:Vt.meshnormal_vert,fragmentShader:Vt.meshnormal_frag},sprite:{uniforms:Ye([ft.sprite,ft.fog]),vertexShader:Vt.sprite_vert,fragmentShader:Vt.sprite_frag},background:{uniforms:{uvTransform:{value:new Dt},t2D:{value:null},backgroundIntensity:{value:1}},vertexShader:Vt.background_vert,fragmentShader:Vt.background_frag},backgroundCube:{uniforms:{envMap:{value:null},backgroundBlurriness:{value:0},backgroundIntensity:{value:1},backgroundRotation:{value:new Dt}},vertexShader:Vt.backgroundCube_vert,fragmentShader:Vt.backgroundCube_frag},cube:{uniforms:{tCube:{value:null},tFlip:{value:-1},opacity:{value:1}},vertexShader:Vt.cube_vert,fragmentShader:Vt.cube_frag},equirect:{uniforms:{tEquirect:{value:null}},vertexShader:Vt.equirect_vert,fragmentShader:Vt.equirect_frag},distance:{uniforms:Ye([ft.common,ft.displacementmap,{referencePosition:{value:new D},nearDistance:{value:1},farDistance:{value:1e3}}]),vertexShader:Vt.distance_vert,fragmentShader:Vt.distance_frag},shadow:{uniforms:Ye([ft.lights,ft.fog,{color:{value:new ut(0)},opacity:{value:1}}]),vertexShader:Vt.shadow_vert,fragmentShader:Vt.shadow_frag}};Gn.physical={uniforms:Ye([Gn.standard.uniforms,{clearcoat:{value:0},clearcoatMap:{value:null},clearcoatMapTransform:{value:new Dt},clearcoatNormalMap:{value:null},clearcoatNormalMapTransform:{value:new Dt},clearcoatNormalScale:{value:new Ut(1,1)},clearcoatRoughness:{value:0},clearcoatRoughnessMap:{value:null},clearcoatRoughnessMapTransform:{value:new Dt},dispersion:{value:0},iridescence:{value:0},iridescenceMap:{value:null},iridescenceMapTransform:{value:new Dt},iridescenceIOR:{value:1.3},iridescenceThicknessMinimum:{value:100},iridescenceThicknessMaximum:{value:400},iridescenceThicknessMap:{value:null},iridescenceThicknessMapTransform:{value:new Dt},sheen:{value:0},sheenColor:{value:new ut(0)},sheenColorMap:{value:null},sheenColorMapTransform:{value:new Dt},sheenRoughness:{value:1},sheenRoughnessMap:{value:null},sheenRoughnessMapTransform:{value:new Dt},transmission:{value:0},transmissionMap:{value:null},transmissionMapTransform:{value:new Dt},transmissionSamplerSize:{value:new Ut},transmissionSamplerMap:{value:null},thickness:{value:0},thicknessMap:{value:null},thicknessMapTransform:{value:new Dt},attenuationDistance:{value:0},attenuationColor:{value:new ut(0)},specularColor:{value:new ut(1,1,1)},specularColorMap:{value:null},specularColorMapTransform:{value:new Dt},specularIntensity:{value:1},specularIntensityMap:{value:null},specularIntensityMapTransform:{value:new Dt},anisotropyVector:{value:new Ut},anisotropyMap:{value:null},anisotropyMapTransform:{value:new Dt}}]),vertexShader:Vt.meshphysical_vert,fragmentShader:Vt.meshphysical_frag};var nl={r:0,b:0,g:0},X_=new ve,Vf=new Dt;Vf.set(-1,0,0,0,1,0,0,0,1);function q_(i,t,e,n,s,r){let a=new ut(0),o=s===!0?0:1,l,c,h=null,f=0,u=null;function p(y){let S=y.isScene===!0?y.background:null;if(S&&S.isTexture){let b=y.backgroundBlurriness>0;S=t.get(S,b)}return S}function g(y){let S=!1,b=p(y);b===null?m(a,o):b&&b.isColor&&(m(b,1),S=!0);let T=i.xr.getEnvironmentBlendMode();T==="additive"?e.buffers.color.setClear(0,0,0,1,r):T==="alpha-blend"&&e.buffers.color.setClear(0,0,0,0,r),(i.autoClear||S)&&(e.buffers.depth.setTest(!0),e.buffers.depth.setMask(!0),e.buffers.color.setMask(!0),i.clear(i.autoClearColor,i.autoClearDepth,i.autoClearStencil))}function x(y,S){let b=p(S);b&&(b.isCubeTexture||b.mapping===Sr)?(c===void 0&&(c=new rn(new Is(1,1,1),new se({name:"BackgroundCubeMaterial",uniforms:rs(Gn.backgroundCube.uniforms),vertexShader:Gn.backgroundCube.vertexShader,fragmentShader:Gn.backgroundCube.fragmentShader,side:$e,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),c.geometry.deleteAttribute("normal"),c.geometry.deleteAttribute("uv"),c.onBeforeRender=function(T,w,R){this.matrixWorld.copyPosition(R.matrixWorld)},Object.defineProperty(c.material,"envMap",{get:function(){return this.uniforms.envMap.value}}),n.update(c)),c.material.uniforms.envMap.value=b,c.material.uniforms.backgroundBlurriness.value=S.backgroundBlurriness,c.material.uniforms.backgroundIntensity.value=S.backgroundIntensity,c.material.uniforms.backgroundRotation.value.setFromMatrix4(X_.makeRotationFromEuler(S.backgroundRotation)).transpose(),b.isCubeTexture&&b.isRenderTargetTexture===!1&&c.material.uniforms.backgroundRotation.value.premultiply(Vf),c.material.toneMapped=Ht.getTransfer(b.colorSpace)!==Kt,(h!==b||f!==b.version||u!==i.toneMapping)&&(c.material.needsUpdate=!0,h=b,f=b.version,u=i.toneMapping),c.layers.enableAll(),y.unshift(c,c.geometry,c.material,0,0,null)):b&&b.isTexture&&(l===void 0&&(l=new rn(new ur(2,2),new se({name:"BackgroundMaterial",uniforms:rs(Gn.background.uniforms),vertexShader:Gn.background.vertexShader,fragmentShader:Gn.background.fragmentShader,side:ei,depthTest:!1,depthWrite:!1,fog:!1,allowOverride:!1})),l.geometry.deleteAttribute("normal"),Object.defineProperty(l.material,"map",{get:function(){return this.uniforms.t2D.value}}),n.update(l)),l.material.uniforms.t2D.value=b,l.material.uniforms.backgroundIntensity.value=S.backgroundIntensity,l.material.toneMapped=Ht.getTransfer(b.colorSpace)!==Kt,b.matrixAutoUpdate===!0&&b.updateMatrix(),l.material.uniforms.uvTransform.value.copy(b.matrix),(h!==b||f!==b.version||u!==i.toneMapping)&&(l.material.needsUpdate=!0,h=b,f=b.version,u=i.toneMapping),l.layers.enableAll(),y.unshift(l,l.geometry,l.material,0,0,null))}function m(y,S){y.getRGB(nl,Vc(i)),e.buffers.color.setClear(nl.r,nl.g,nl.b,S,r)}function d(){c!==void 0&&(c.geometry.dispose(),c.material.dispose(),c=void 0),l!==void 0&&(l.geometry.dispose(),l.material.dispose(),l=void 0)}return{getClearColor:function(){return a},setClearColor:function(y,S=1){a.set(y),o=S,m(a,o)},getClearAlpha:function(){return o},setClearAlpha:function(y){o=y,m(a,o)},render:g,addToRenderList:x,dispose:d}}function Y_(i,t){let e=i.getParameter(i.MAX_VERTEX_ATTRIBS),n={},s=u(null),r=s,a=!1;function o(C,N,H,W,U){let z=!1,V=f(C,W,H,N);r!==V&&(r=V,c(r.object)),z=p(C,W,H,U),z&&g(C,W,H,U),U!==null&&t.update(U,i.ELEMENT_ARRAY_BUFFER),(z||a)&&(a=!1,b(C,N,H,W),U!==null&&i.bindBuffer(i.ELEMENT_ARRAY_BUFFER,t.get(U).buffer))}function l(){return i.createVertexArray()}function c(C){return i.bindVertexArray(C)}function h(C){return i.deleteVertexArray(C)}function f(C,N,H,W){let U=W.wireframe===!0,z=n[N.id];z===void 0&&(z={},n[N.id]=z);let V=C.isInstancedMesh===!0?C.id:0,$=z[V];$===void 0&&($={},z[V]=$);let tt=$[H.id];tt===void 0&&(tt={},$[H.id]=tt);let ct=tt[U];return ct===void 0&&(ct=u(l()),tt[U]=ct),ct}function u(C){let N=[],H=[],W=[];for(let U=0;U<e;U++)N[U]=0,H[U]=0,W[U]=0;return{geometry:null,program:null,wireframe:!1,newAttributes:N,enabledAttributes:H,attributeDivisors:W,object:C,attributes:{},index:null}}function p(C,N,H,W){let U=r.attributes,z=N.attributes,V=0,$=H.getAttributes();for(let tt in $)if($[tt].location>=0){let Mt=U[tt],St=z[tt];if(St===void 0&&(tt==="instanceMatrix"&&C.instanceMatrix&&(St=C.instanceMatrix),tt==="instanceColor"&&C.instanceColor&&(St=C.instanceColor)),Mt===void 0||Mt.attribute!==St||St&&Mt.data!==St.data)return!0;V++}return r.attributesNum!==V||r.index!==W}function g(C,N,H,W){let U={},z=N.attributes,V=0,$=H.getAttributes();for(let tt in $)if($[tt].location>=0){let Mt=z[tt];Mt===void 0&&(tt==="instanceMatrix"&&C.instanceMatrix&&(Mt=C.instanceMatrix),tt==="instanceColor"&&C.instanceColor&&(Mt=C.instanceColor));let St={};St.attribute=Mt,Mt&&Mt.data&&(St.data=Mt.data),U[tt]=St,V++}r.attributes=U,r.attributesNum=V,r.index=W}function x(){let C=r.newAttributes;for(let N=0,H=C.length;N<H;N++)C[N]=0}function m(C){d(C,0)}function d(C,N){let H=r.newAttributes,W=r.enabledAttributes,U=r.attributeDivisors;H[C]=1,W[C]===0&&(i.enableVertexAttribArray(C),W[C]=1),U[C]!==N&&(i.vertexAttribDivisor(C,N),U[C]=N)}function y(){let C=r.newAttributes,N=r.enabledAttributes;for(let H=0,W=N.length;H<W;H++)N[H]!==C[H]&&(i.disableVertexAttribArray(H),N[H]=0)}function S(C,N,H,W,U,z,V){V===!0?i.vertexAttribIPointer(C,N,H,U,z):i.vertexAttribPointer(C,N,H,W,U,z)}function b(C,N,H,W){x();let U=W.attributes,z=H.getAttributes(),V=N.defaultAttributeValues;for(let $ in z){let tt=z[$];if(tt.location>=0){let ct=U[$];if(ct===void 0&&($==="instanceMatrix"&&C.instanceMatrix&&(ct=C.instanceMatrix),$==="instanceColor"&&C.instanceColor&&(ct=C.instanceColor)),ct!==void 0){let Mt=ct.normalized,St=ct.itemSize,Xt=t.get(ct);if(Xt===void 0)continue;let te=Xt.buffer,kt=Xt.type,J=Xt.bytesPerElement,mt=kt===i.INT||kt===i.UNSIGNED_INT||ct.gpuType===xo;if(ct.isInterleavedBufferAttribute){let rt=ct.data,Ct=rt.stride,Ft=ct.offset;if(rt.isInstancedInterleavedBuffer){for(let Pt=0;Pt<tt.locationSize;Pt++)d(tt.location+Pt,rt.meshPerAttribute);C.isInstancedMesh!==!0&&W._maxInstanceCount===void 0&&(W._maxInstanceCount=rt.meshPerAttribute*rt.count)}else for(let Pt=0;Pt<tt.locationSize;Pt++)m(tt.location+Pt);i.bindBuffer(i.ARRAY_BUFFER,te);for(let Pt=0;Pt<tt.locationSize;Pt++)S(tt.location+Pt,St/tt.locationSize,kt,Mt,Ct*J,(Ft+St/tt.locationSize*Pt)*J,mt)}else{if(ct.isInstancedBufferAttribute){for(let rt=0;rt<tt.locationSize;rt++)d(tt.location+rt,ct.meshPerAttribute);C.isInstancedMesh!==!0&&W._maxInstanceCount===void 0&&(W._maxInstanceCount=ct.meshPerAttribute*ct.count)}else for(let rt=0;rt<tt.locationSize;rt++)m(tt.location+rt);i.bindBuffer(i.ARRAY_BUFFER,te);for(let rt=0;rt<tt.locationSize;rt++)S(tt.location+rt,St/tt.locationSize,kt,Mt,St*J,St/tt.locationSize*rt*J,mt)}}else if(V!==void 0){let Mt=V[$];if(Mt!==void 0)switch(Mt.length){case 2:i.vertexAttrib2fv(tt.location,Mt);break;case 3:i.vertexAttrib3fv(tt.location,Mt);break;case 4:i.vertexAttrib4fv(tt.location,Mt);break;default:i.vertexAttrib1fv(tt.location,Mt)}}}}y()}function T(){E();for(let C in n){let N=n[C];for(let H in N){let W=N[H];for(let U in W){let z=W[U];for(let V in z)h(z[V].object),delete z[V];delete W[U]}}delete n[C]}}function w(C){if(n[C.id]===void 0)return;let N=n[C.id];for(let H in N){let W=N[H];for(let U in W){let z=W[U];for(let V in z)h(z[V].object),delete z[V];delete W[U]}}delete n[C.id]}function R(C){for(let N in n){let H=n[N];for(let W in H){let U=H[W];if(U[C.id]===void 0)continue;let z=U[C.id];for(let V in z)h(z[V].object),delete z[V];delete U[C.id]}}}function v(C){for(let N in n){let H=n[N],W=C.isInstancedMesh===!0?C.id:0,U=H[W];if(U!==void 0){for(let z in U){let V=U[z];for(let $ in V)h(V[$].object),delete V[$];delete U[z]}delete H[W],Object.keys(H).length===0&&delete n[N]}}}function E(){I(),a=!0,r!==s&&(r=s,c(r.object))}function I(){s.geometry=null,s.program=null,s.wireframe=!1}return{setup:o,reset:E,resetDefaultState:I,dispose:T,releaseStatesOfGeometry:w,releaseStatesOfObject:v,releaseStatesOfProgram:R,initAttributes:x,enableAttribute:m,disableUnusedAttributes:y}}function Z_(i,t,e){let n;function s(l){n=l}function r(l,c){i.drawArrays(n,l,c),e.update(c,n,1)}function a(l,c,h){h!==0&&(i.drawArraysInstanced(n,l,c,h),e.update(c,n,h))}function o(l,c,h){if(h===0)return;t.get("WEBGL_multi_draw").multiDrawArraysWEBGL(n,l,0,c,0,h);let u=0;for(let p=0;p<h;p++)u+=c[p];e.update(u,n,1)}this.setMode=s,this.render=r,this.renderInstances=a,this.renderMultiDraw=o}function J_(i,t,e,n){let s;function r(){if(s!==void 0)return s;if(t.has("EXT_texture_filter_anisotropic")===!0){let R=t.get("EXT_texture_filter_anisotropic");s=i.getParameter(R.MAX_TEXTURE_MAX_ANISOTROPY_EXT)}else s=0;return s}function a(R){return!(R!==yn&&n.convert(R)!==i.getParameter(i.IMPLEMENTATION_COLOR_READ_FORMAT))}function o(R){let v=R===qe&&(t.has("EXT_color_buffer_half_float")||t.has("EXT_color_buffer_float"));return!(R!==mn&&n.convert(R)!==i.getParameter(i.IMPLEMENTATION_COLOR_READ_TYPE)&&R!==Cn&&!v)}function l(R){if(R==="highp"){if(i.getShaderPrecisionFormat(i.VERTEX_SHADER,i.HIGH_FLOAT).precision>0&&i.getShaderPrecisionFormat(i.FRAGMENT_SHADER,i.HIGH_FLOAT).precision>0)return"highp";R="mediump"}return R==="mediump"&&i.getShaderPrecisionFormat(i.VERTEX_SHADER,i.MEDIUM_FLOAT).precision>0&&i.getShaderPrecisionFormat(i.FRAGMENT_SHADER,i.MEDIUM_FLOAT).precision>0?"mediump":"lowp"}let c=e.precision!==void 0?e.precision:"highp",h=l(c);h!==c&&(Et("WebGLRenderer:",c,"not supported, using",h,"instead."),c=h);let f=e.logarithmicDepthBuffer===!0,u=e.reversedDepthBuffer===!0&&t.has("EXT_clip_control");e.reversedDepthBuffer===!0&&u===!1&&Et("WebGLRenderer: Unable to use reversed depth buffer due to missing EXT_clip_control extension. Fallback to default depth buffer.");let p=i.getParameter(i.MAX_TEXTURE_IMAGE_UNITS),g=i.getParameter(i.MAX_VERTEX_TEXTURE_IMAGE_UNITS),x=i.getParameter(i.MAX_TEXTURE_SIZE),m=i.getParameter(i.MAX_CUBE_MAP_TEXTURE_SIZE),d=i.getParameter(i.MAX_VERTEX_ATTRIBS),y=i.getParameter(i.MAX_VERTEX_UNIFORM_VECTORS),S=i.getParameter(i.MAX_VARYING_VECTORS),b=i.getParameter(i.MAX_FRAGMENT_UNIFORM_VECTORS),T=i.getParameter(i.MAX_SAMPLES),w=i.getParameter(i.SAMPLES);return{isWebGL2:!0,getMaxAnisotropy:r,getMaxPrecision:l,textureFormatReadable:a,textureTypeReadable:o,precision:c,logarithmicDepthBuffer:f,reversedDepthBuffer:u,maxTextures:p,maxVertexTextures:g,maxTextureSize:x,maxCubemapSize:m,maxAttributes:d,maxVertexUniforms:y,maxVaryings:S,maxFragmentUniforms:b,maxSamples:T,samples:w}}function $_(i){let t=this,e=null,n=0,s=!1,r=!1,a=new Fn,o=new Dt,l={value:null,needsUpdate:!1};this.uniform=l,this.numPlanes=0,this.numIntersection=0,this.init=function(f,u){let p=f.length!==0||u||n!==0||s;return s=u,n=f.length,p},this.beginShadows=function(){r=!0,h(null)},this.endShadows=function(){r=!1},this.setGlobalState=function(f,u){e=h(f,u,0)},this.setState=function(f,u,p){let g=f.clippingPlanes,x=f.clipIntersection,m=f.clipShadows,d=i.get(f);if(!s||g===null||g.length===0||r&&!m)r?h(null):c();else{let y=r?0:n,S=y*4,b=d.clippingState||null;l.value=b,b=h(g,u,S,p);for(let T=0;T!==S;++T)b[T]=e[T];d.clippingState=b,this.numIntersection=x?this.numPlanes:0,this.numPlanes+=y}};function c(){l.value!==e&&(l.value=e,l.needsUpdate=n>0),t.numPlanes=n,t.numIntersection=0}function h(f,u,p,g){let x=f!==null?f.length:0,m=null;if(x!==0){if(m=l.value,g!==!0||m===null){let d=p+x*4,y=u.matrixWorldInverse;o.getNormalMatrix(y),(m===null||m.length<d)&&(m=new Float32Array(d));for(let S=0,b=p;S!==x;++S,b+=4)a.copy(f[S]).applyMatrix4(y,o),a.normal.toArray(m,b),m[b+3]=a.constant}l.value=m,l.needsUpdate=!0}return t.numPlanes=x,t.numIntersection=0,m}}var Di=4,xf=[.125,.215,.35,.446,.526,.582],as=20,K_=256,Lr=new is,vf=new ut,$c=null,Kc=0,jc=0,Qc=!1,j_=new D,sl=class{constructor(t){this._renderer=t,this._pingPongRenderTarget=null,this._lodMax=0,this._cubeSize=0,this._sizeLods=[],this._sigmas=[],this._lodMeshes=[],this._backgroundBox=null,this._cubemapMaterial=null,this._equirectMaterial=null,this._blurMaterial=null,this._ggxMaterial=null}fromScene(t,e=0,n=.1,s=100,r={}){let{size:a=256,position:o=j_}=r;$c=this._renderer.getRenderTarget(),Kc=this._renderer.getActiveCubeFace(),jc=this._renderer.getActiveMipmapLevel(),Qc=this._renderer.xr.enabled,this._renderer.xr.enabled=!1,this._setSize(a);let l=this._allocateTargets();return l.depthBuffer=!0,this._sceneToCubeUV(t,n,s,l,o),e>0&&this._blur(l,0,0,e),this._applyPMREM(l),this._cleanup(l),l}fromEquirectangular(t,e=null){return this._fromTexture(t,e)}fromCubemap(t,e=null){return this._fromTexture(t,e)}compileCubemapShader(){this._cubemapMaterial===null&&(this._cubemapMaterial=bf(),this._compileMaterial(this._cubemapMaterial))}compileEquirectangularShader(){this._equirectMaterial===null&&(this._equirectMaterial=Mf(),this._compileMaterial(this._equirectMaterial))}dispose(){this._dispose(),this._cubemapMaterial!==null&&this._cubemapMaterial.dispose(),this._equirectMaterial!==null&&this._equirectMaterial.dispose(),this._backgroundBox!==null&&(this._backgroundBox.geometry.dispose(),this._backgroundBox.material.dispose())}_setSize(t){this._lodMax=Math.floor(Math.log2(t)),this._cubeSize=Math.pow(2,this._lodMax)}_dispose(){this._blurMaterial!==null&&this._blurMaterial.dispose(),this._ggxMaterial!==null&&this._ggxMaterial.dispose(),this._pingPongRenderTarget!==null&&this._pingPongRenderTarget.dispose();for(let t=0;t<this._lodMeshes.length;t++)this._lodMeshes[t].geometry.dispose()}_cleanup(t){this._renderer.setRenderTarget($c,Kc,jc),this._renderer.xr.enabled=Qc,t.scissorTest=!1,Us(t,0,0,t.width,t.height)}_fromTexture(t,e){t.mapping===Ri||t.mapping===ss?this._setSize(t.image.length===0?16:t.image[0].width||t.image[0].image.width):this._setSize(t.image.width/4),$c=this._renderer.getRenderTarget(),Kc=this._renderer.getActiveCubeFace(),jc=this._renderer.getActiveMipmapLevel(),Qc=this._renderer.xr.enabled,this._renderer.xr.enabled=!1;let n=e||this._allocateTargets();return this._textureToCubeUV(t,n),this._applyPMREM(n),this._cleanup(n),n}_allocateTargets(){let t=3*Math.max(this._cubeSize,112),e=4*this._cubeSize,n={magFilter:ze,minFilter:ze,generateMipmaps:!1,type:qe,format:yn,colorSpace:Qs,depthBuffer:!1},s=yf(t,e,n);if(this._pingPongRenderTarget===null||this._pingPongRenderTarget.width!==t||this._pingPongRenderTarget.height!==e){this._pingPongRenderTarget!==null&&this._dispose(),this._pingPongRenderTarget=yf(t,e,n);let{_lodMax:r}=this;({lodMeshes:this._lodMeshes,sizeLods:this._sizeLods,sigmas:this._sigmas}=Q_(r)),this._blurMaterial=ex(r,t,e),this._ggxMaterial=tx(r,t,e)}return s}_compileMaterial(t){let e=new rn(new Qt,t);this._renderer.compile(e,Lr)}_sceneToCubeUV(t,e,n,s,r){let l=new Xe(90,1,e,n),c=[1,-1,1,1,1,1],h=[1,1,1,-1,-1,-1],f=this._renderer,u=f.autoClear,p=f.toneMapping;f.getClearColor(vf),f.toneMapping=pn,f.autoClear=!1,f.state.buffers.depth.getReversed()&&(f.setRenderTarget(s),f.clearDepth(),f.setRenderTarget(null)),this._backgroundBox===null&&(this._backgroundBox=new rn(new Is,new es({name:"PMREM.Background",side:$e,depthWrite:!1,depthTest:!1})));let x=this._backgroundBox,m=x.material,d=!1,y=t.background;y?y.isColor&&(m.color.copy(y),t.background=null,d=!0):(m.color.copy(vf),d=!0);for(let S=0;S<6;S++){let b=S%3;b===0?(l.up.set(0,c[S],0),l.position.set(r.x,r.y,r.z),l.lookAt(r.x+h[S],r.y,r.z)):b===1?(l.up.set(0,0,c[S]),l.position.set(r.x,r.y,r.z),l.lookAt(r.x,r.y+h[S],r.z)):(l.up.set(0,c[S],0),l.position.set(r.x,r.y,r.z),l.lookAt(r.x,r.y,r.z+h[S]));let T=this._cubeSize;Us(s,b*T,S>2?T:0,T,T),f.setRenderTarget(s),d&&f.render(x,l),f.render(t,l)}f.toneMapping=p,f.autoClear=u,t.background=y}_textureToCubeUV(t,e){let n=this._renderer,s=t.mapping===Ri||t.mapping===ss;s?(this._cubemapMaterial===null&&(this._cubemapMaterial=bf()),this._cubemapMaterial.uniforms.flipEnvMap.value=t.isRenderTargetTexture===!1?-1:1):this._equirectMaterial===null&&(this._equirectMaterial=Mf());let r=s?this._cubemapMaterial:this._equirectMaterial,a=this._lodMeshes[0];a.material=r;let o=r.uniforms;o.envMap.value=t;let l=this._cubeSize;Us(e,0,0,3*l,2*l),n.setRenderTarget(e),n.render(a,Lr)}_applyPMREM(t){let e=this._renderer,n=e.autoClear;e.autoClear=!1;let s=this._lodMeshes.length;for(let r=1;r<s;r++)this._applyGGXFilter(t,r-1,r);e.autoClear=n}_applyGGXFilter(t,e,n){let s=this._renderer,r=this._pingPongRenderTarget,a=this._ggxMaterial,o=this._lodMeshes[n];o.material=a;let l=a.uniforms,c=n/(this._lodMeshes.length-1),h=e/(this._lodMeshes.length-1),f=Math.sqrt(c*c-h*h),u=0+c*1.25,p=f*u,{_lodMax:g}=this,x=this._sizeLods[n],m=3*x*(n>g-Di?n-g+Di:0),d=4*(this._cubeSize-x);l.envMap.value=t.texture,l.roughness.value=p,l.mipInt.value=g-e,Us(r,m,d,3*x,2*x),s.setRenderTarget(r),s.render(o,Lr),l.envMap.value=r.texture,l.roughness.value=0,l.mipInt.value=g-n,Us(t,m,d,3*x,2*x),s.setRenderTarget(t),s.render(o,Lr)}_blur(t,e,n,s,r){let a=this._pingPongRenderTarget;this._halfBlur(t,a,e,n,s,"latitudinal",r),this._halfBlur(a,t,n,n,s,"longitudinal",r)}_halfBlur(t,e,n,s,r,a,o){let l=this._renderer,c=this._blurMaterial;a!=="latitudinal"&&a!=="longitudinal"&&Rt("blur direction must be either latitudinal or longitudinal!");let h=3,f=this._lodMeshes[s];f.material=c;let u=c.uniforms,p=this._sizeLods[n]-1,g=isFinite(r)?Math.PI/(2*p):2*Math.PI/(2*as-1),x=r/g,m=isFinite(r)?1+Math.floor(h*x):as;m>as&&Et(`sigmaRadians, ${r}, is too large and will clip, as it requested ${m} samples when the maximum is set to ${as}`);let d=[],y=0;for(let R=0;R<as;++R){let v=R/x,E=Math.exp(-v*v/2);d.push(E),R===0?y+=E:R<m&&(y+=2*E)}for(let R=0;R<d.length;R++)d[R]=d[R]/y;u.envMap.value=t.texture,u.samples.value=m,u.weights.value=d,u.latitudinal.value=a==="latitudinal",o&&(u.poleAxis.value=o);let{_lodMax:S}=this;u.dTheta.value=g,u.mipInt.value=S-n;let b=this._sizeLods[s],T=3*b*(s>S-Di?s-S+Di:0),w=4*(this._cubeSize-b);Us(e,T,w,3*b,2*b),l.setRenderTarget(e),l.render(f,Lr)}};function Q_(i){let t=[],e=[],n=[],s=i,r=i-Di+1+xf.length;for(let a=0;a<r;a++){let o=Math.pow(2,s);t.push(o);let l=1/o;a>i-Di?l=xf[a-i+Di-1]:a===0&&(l=0),e.push(l);let c=1/(o-2),h=-c,f=1+c,u=[h,h,f,h,f,f,h,h,f,f,h,f],p=6,g=6,x=3,m=2,d=1,y=new Float32Array(x*g*p),S=new Float32Array(m*g*p),b=new Float32Array(d*g*p);for(let w=0;w<p;w++){let R=w%3*2/3-1,v=w>2?0:-1,E=[R,v,0,R+2/3,v,0,R+2/3,v+1,0,R,v,0,R+2/3,v+1,0,R,v+1,0];y.set(E,x*g*w),S.set(u,m*g*w);let I=[w,w,w,w,w,w];b.set(I,d*g*w)}let T=new Qt;T.setAttribute("position",new Lt(y,x)),T.setAttribute("uv",new Lt(S,m)),T.setAttribute("faceIndex",new Lt(b,d)),n.push(new rn(T,null)),s>Di&&s--}return{lodMeshes:n,sizeLods:t,sigmas:e}}function yf(i,t,e){let n=new Le(i,t,e);return n.texture.mapping=Sr,n.texture.name="PMREM.cubeUv",n.scissorTest=!0,n}function Us(i,t,e,n,s){i.viewport.set(t,e,n,s),i.scissor.set(t,e,n,s)}function tx(i,t,e){return new se({name:"PMREMGGXConvolution",defines:{GGX_SAMPLES:K_,CUBEUV_TEXEL_WIDTH:1/t,CUBEUV_TEXEL_HEIGHT:1/e,CUBEUV_MAX_MIP:`${i}.0`},uniforms:{envMap:{value:null},roughness:{value:0},mipInt:{value:0}},vertexShader:ol(),fragmentShader:`

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
		`,blending:vn,depthTest:!1,depthWrite:!1})}function ex(i,t,e){let n=new Float32Array(as),s=new D(0,1,0);return new se({name:"SphericalGaussianBlur",defines:{n:as,CUBEUV_TEXEL_WIDTH:1/t,CUBEUV_TEXEL_HEIGHT:1/e,CUBEUV_MAX_MIP:`${i}.0`},uniforms:{envMap:{value:null},samples:{value:1},weights:{value:n},latitudinal:{value:!1},dTheta:{value:0},mipInt:{value:0},poleAxis:{value:s}},vertexShader:ol(),fragmentShader:`

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
		`,blending:vn,depthTest:!1,depthWrite:!1})}function Mf(){return new se({name:"EquirectangularToCubeUV",uniforms:{envMap:{value:null}},vertexShader:ol(),fragmentShader:`

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
		`,blending:vn,depthTest:!1,depthWrite:!1})}function bf(){return new se({name:"CubemapToCubeUV",uniforms:{envMap:{value:null},flipEnvMap:{value:-1}},vertexShader:ol(),fragmentShader:`

			precision mediump float;
			precision mediump int;

			uniform float flipEnvMap;

			varying vec3 vOutputDirection;

			uniform samplerCube envMap;

			void main() {

				gl_FragColor = textureCube( envMap, vec3( flipEnvMap * vOutputDirection.x, vOutputDirection.yz ) );

			}
		`,blending:vn,depthTest:!1,depthWrite:!1})}function ol(){return`

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
	`}var rl=class extends Le{constructor(t=1,e={}){super(t,t,e),this.isWebGLCubeRenderTarget=!0;let n={width:t,height:t,depth:1},s=[n,n,n,n,n,n];this.texture=new cr(s),this._setTextureOptions(e),this.texture.isRenderTargetTexture=!0}fromEquirectangularTexture(t,e){this.texture.type=e.type,this.texture.colorSpace=e.colorSpace,this.texture.generateMipmaps=e.generateMipmaps,this.texture.minFilter=e.minFilter,this.texture.magFilter=e.magFilter;let n={uniforms:{tEquirect:{value:null}},vertexShader:`

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
			`},s=new Is(5,5,5),r=new se({name:"CubemapFromEquirect",uniforms:rs(n.uniforms),vertexShader:n.vertexShader,fragmentShader:n.fragmentShader,side:$e,blending:vn});r.uniforms.tEquirect.value=e;let a=new rn(s,r),o=e.minFilter;return e.minFilter===Pi&&(e.minFilter=ze),new ho(1,10,this).update(t,a),e.minFilter=o,a.geometry.dispose(),a.material.dispose(),this}clear(t,e=!0,n=!0,s=!0){let r=t.getRenderTarget();for(let a=0;a<6;a++)t.setRenderTarget(this,a),t.clear(e,n,s);t.setRenderTarget(r)}};function nx(i){let t=new WeakMap,e=new WeakMap,n=null;function s(u,p=!1){return u==null?null:p?a(u):r(u)}function r(u){if(u&&u.isTexture){let p=u.mapping;if(p===mo||p===go)if(t.has(u)){let g=t.get(u).texture;return o(g,u.mapping)}else{let g=u.image;if(g&&g.height>0){let x=new rl(g.height);return x.fromEquirectangularTexture(i,u),t.set(u,x),u.addEventListener("dispose",c),o(x.texture,u.mapping)}else return null}}return u}function a(u){if(u&&u.isTexture){let p=u.mapping,g=p===mo||p===go,x=p===Ri||p===ss;if(g||x){let m=e.get(u),d=m!==void 0?m.texture.pmremVersion:0;if(u.isRenderTargetTexture&&u.pmremVersion!==d)return n===null&&(n=new sl(i)),m=g?n.fromEquirectangular(u,m):n.fromCubemap(u,m),m.texture.pmremVersion=u.pmremVersion,e.set(u,m),m.texture;if(m!==void 0)return m.texture;{let y=u.image;return g&&y&&y.height>0||x&&y&&l(y)?(n===null&&(n=new sl(i)),m=g?n.fromEquirectangular(u):n.fromCubemap(u),m.texture.pmremVersion=u.pmremVersion,e.set(u,m),u.addEventListener("dispose",h),m.texture):null}}}return u}function o(u,p){return p===mo?u.mapping=Ri:p===go&&(u.mapping=ss),u}function l(u){let p=0,g=6;for(let x=0;x<g;x++)u[x]!==void 0&&p++;return p===g}function c(u){let p=u.target;p.removeEventListener("dispose",c);let g=t.get(p);g!==void 0&&(t.delete(p),g.dispose())}function h(u){let p=u.target;p.removeEventListener("dispose",h);let g=e.get(p);g!==void 0&&(e.delete(p),g.dispose())}function f(){t=new WeakMap,e=new WeakMap,n!==null&&(n.dispose(),n=null)}return{get:s,dispose:f}}function ix(i){let t={};function e(n){if(t[n]!==void 0)return t[n];let s=i.getExtension(n);return t[n]=s,s}return{has:function(n){return e(n)!==null},init:function(){e("EXT_color_buffer_float"),e("WEBGL_clip_cull_distance"),e("OES_texture_float_linear"),e("EXT_color_buffer_half_float"),e("WEBGL_multisampled_render_to_texture"),e("WEBGL_render_shared_exponent")},get:function(n){let s=e(n);return s===null&&Ga("WebGLRenderer: "+n+" extension not supported."),s}}}function sx(i,t,e,n){let s={},r=new WeakMap;function a(f){let u=f.target;u.index!==null&&t.remove(u.index);for(let g in u.attributes)t.remove(u.attributes[g]);u.removeEventListener("dispose",a),delete s[u.id];let p=r.get(u);p&&(t.remove(p),r.delete(u)),n.releaseStatesOfGeometry(u),u.isInstancedBufferGeometry===!0&&delete u._maxInstanceCount,e.memory.geometries--}function o(f,u){return s[u.id]===!0||(u.addEventListener("dispose",a),s[u.id]=!0,e.memory.geometries++),u}function l(f){let u=f.attributes;for(let p in u)t.update(u[p],i.ARRAY_BUFFER)}function c(f){let u=[],p=f.index,g=f.attributes.position,x=0;if(g===void 0)return;if(p!==null){let y=p.array;x=p.version;for(let S=0,b=y.length;S<b;S+=3){let T=y[S+0],w=y[S+1],R=y[S+2];u.push(T,w,w,R,R,T)}}else{let y=g.array;x=g.version;for(let S=0,b=y.length/3-1;S<b;S+=3){let T=S+0,w=S+1,R=S+2;u.push(T,w,w,R,R,T)}}let m=new(g.count>=65535?or:ar)(u,1);m.version=x;let d=r.get(f);d&&t.remove(d),r.set(f,m)}function h(f){let u=r.get(f);if(u){let p=f.index;p!==null&&u.version<p.version&&c(f)}else c(f);return r.get(f)}return{get:o,update:l,getWireframeAttribute:h}}function rx(i,t,e){let n;function s(f){n=f}let r,a;function o(f){r=f.type,a=f.bytesPerElement}function l(f,u){i.drawElements(n,u,r,f*a),e.update(u,n,1)}function c(f,u,p){p!==0&&(i.drawElementsInstanced(n,u,r,f*a,p),e.update(u,n,p))}function h(f,u,p){if(p===0)return;t.get("WEBGL_multi_draw").multiDrawElementsWEBGL(n,u,0,r,f,0,p);let x=0;for(let m=0;m<p;m++)x+=u[m];e.update(x,n,1)}this.setMode=s,this.setIndex=o,this.render=l,this.renderInstances=c,this.renderMultiDraw=h}function ax(i){let t={geometries:0,textures:0},e={frame:0,calls:0,triangles:0,points:0,lines:0};function n(r,a,o){switch(e.calls++,a){case i.TRIANGLES:e.triangles+=o*(r/3);break;case i.LINES:e.lines+=o*(r/2);break;case i.LINE_STRIP:e.lines+=o*(r-1);break;case i.LINE_LOOP:e.lines+=o*r;break;case i.POINTS:e.points+=o*r;break;default:Rt("WebGLInfo: Unknown draw mode:",a);break}}function s(){e.calls=0,e.triangles=0,e.points=0,e.lines=0}return{memory:t,render:e,programs:null,autoReset:!0,reset:s,update:n}}function ox(i,t,e){let n=new WeakMap,s=new ye;function r(a,o,l){let c=a.morphTargetInfluences,h=o.morphAttributes.position||o.morphAttributes.normal||o.morphAttributes.color,f=h!==void 0?h.length:0,u=n.get(o);if(u===void 0||u.count!==f){let E=function(){R.dispose(),n.delete(o),o.removeEventListener("dispose",E)};u!==void 0&&u.texture.dispose();let p=o.morphAttributes.position!==void 0,g=o.morphAttributes.normal!==void 0,x=o.morphAttributes.color!==void 0,m=o.morphAttributes.position||[],d=o.morphAttributes.normal||[],y=o.morphAttributes.color||[],S=0;p===!0&&(S=1),g===!0&&(S=2),x===!0&&(S=3);let b=o.attributes.position.count*S,T=1;b>t.maxTextureSize&&(T=Math.ceil(b/t.maxTextureSize),b=t.maxTextureSize);let w=new Float32Array(b*T*4*f),R=new ir(w,b,T,f);R.type=Cn,R.needsUpdate=!0;let v=S*4;for(let I=0;I<f;I++){let C=m[I],N=d[I],H=y[I],W=b*T*4*I;for(let U=0;U<C.count;U++){let z=U*v;p===!0&&(s.fromBufferAttribute(C,U),w[W+z+0]=s.x,w[W+z+1]=s.y,w[W+z+2]=s.z,w[W+z+3]=0),g===!0&&(s.fromBufferAttribute(N,U),w[W+z+4]=s.x,w[W+z+5]=s.y,w[W+z+6]=s.z,w[W+z+7]=0),x===!0&&(s.fromBufferAttribute(H,U),w[W+z+8]=s.x,w[W+z+9]=s.y,w[W+z+10]=s.z,w[W+z+11]=H.itemSize===4?s.w:1)}}u={count:f,texture:R,size:new Ut(b,T)},n.set(o,u),o.addEventListener("dispose",E)}if(a.isInstancedMesh===!0&&a.morphTexture!==null)l.getUniforms().setValue(i,"morphTexture",a.morphTexture,e);else{let p=0;for(let x=0;x<c.length;x++)p+=c[x];let g=o.morphTargetsRelative?1:1-p;l.getUniforms().setValue(i,"morphTargetBaseInfluence",g),l.getUniforms().setValue(i,"morphTargetInfluences",c)}l.getUniforms().setValue(i,"morphTargetsTexture",u.texture,e),l.getUniforms().setValue(i,"morphTargetsTextureSize",u.size)}return{update:r}}function lx(i,t,e,n,s){let r=new WeakMap;function a(c){let h=s.render.frame,f=c.geometry,u=t.get(c,f);if(r.get(u)!==h&&(t.update(u),r.set(u,h)),c.isInstancedMesh&&(c.hasEventListener("dispose",l)===!1&&c.addEventListener("dispose",l),r.get(c)!==h&&(e.update(c.instanceMatrix,i.ARRAY_BUFFER),c.instanceColor!==null&&e.update(c.instanceColor,i.ARRAY_BUFFER),r.set(c,h))),c.isSkinnedMesh){let p=c.skeleton;r.get(p)!==h&&(p.update(),r.set(p,h))}return u}function o(){r=new WeakMap}function l(c){let h=c.target;h.removeEventListener("dispose",l),n.releaseStatesOfObject(h),e.remove(h.instanceMatrix),h.instanceColor!==null&&e.remove(h.instanceColor)}return{update:a,dispose:o}}var cx={[_r]:"LINEAR_TONE_MAPPING",[xr]:"REINHARD_TONE_MAPPING",[vr]:"CINEON_TONE_MAPPING",[Ci]:"ACES_FILMIC_TONE_MAPPING",[Mr]:"AGX_TONE_MAPPING",[br]:"NEUTRAL_TONE_MAPPING",[yr]:"CUSTOM_TONE_MAPPING"};function hx(i,t,e,n,s){let r=new Le(t,e,{type:i,depthBuffer:n,stencilBuffer:s,depthTexture:n?new ri(t,e):void 0}),a=new Le(t,e,{type:qe,depthBuffer:!1,stencilBuffer:!1}),o=new Qt;o.setAttribute("position",new ke([-1,3,0,-1,-1,0,3,-1,0],3)),o.setAttribute("uv",new ke([0,2,0,0,2,0],2));let l=new Ls({uniforms:{tDiffuse:{value:null}},vertexShader:`
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
			}`,depthTest:!1,depthWrite:!1}),c=new rn(o,l),h=new is(-1,1,1,-1,0,1),f=null,u=null,p=!1,g,x=null,m=[],d=!1;this.setSize=function(y,S){r.setSize(y,S),a.setSize(y,S);for(let b=0;b<m.length;b++){let T=m[b];T.setSize&&T.setSize(y,S)}},this.setEffects=function(y){m=y,d=m.length>0&&m[0].isRenderPass===!0;let S=r.width,b=r.height;for(let T=0;T<m.length;T++){let w=m[T];w.setSize&&w.setSize(S,b)}},this.begin=function(y,S){if(p||y.toneMapping===pn&&m.length===0)return!1;if(x=S,S!==null){let b=S.width,T=S.height;(r.width!==b||r.height!==T)&&this.setSize(b,T)}return d===!1&&y.setRenderTarget(r),g=y.toneMapping,y.toneMapping=pn,!0},this.hasRenderPass=function(){return d},this.end=function(y,S){y.toneMapping=g,p=!0;let b=r,T=a;for(let w=0;w<m.length;w++){let R=m[w];if(R.enabled!==!1&&(R.render(y,T,b,S),R.needsSwap!==!1)){let v=b;b=T,T=v}}if(f!==y.outputColorSpace||u!==y.toneMapping){f=y.outputColorSpace,u=y.toneMapping,l.defines={},Ht.getTransfer(f)===Kt&&(l.defines.SRGB_TRANSFER="");let w=cx[u];w&&(l.defines[w]=""),l.needsUpdate=!0}l.uniforms.tDiffuse.value=b.texture,y.setRenderTarget(x),y.render(c,h),x=null,p=!1},this.isCompositing=function(){return p},this.dispose=function(){r.depthTexture&&r.depthTexture.dispose(),r.dispose(),a.dispose(),o.dispose(),l.dispose()}}var Gf=new nn,nh=new ri(1,1),Hf=new ir,Wf=new qa,Xf=new cr,Sf=[],wf=[],Af=new Float32Array(16),Tf=new Float32Array(9),Ef=new Float32Array(4);function Bs(i,t,e){let n=i[0];if(n<=0||n>0)return i;let s=t*e,r=Sf[s];if(r===void 0&&(r=new Float32Array(s),Sf[s]=r),t!==0){n.toArray(r,0);for(let a=1,o=0;a!==t;++a)o+=e,i[a].toArray(r,o)}return r}function Ne(i,t){if(i.length!==t.length)return!1;for(let e=0,n=i.length;e<n;e++)if(i[e]!==t[e])return!1;return!0}function De(i,t){for(let e=0,n=t.length;e<n;e++)i[e]=t[e]}function ll(i,t){let e=wf[t];e===void 0&&(e=new Int32Array(t),wf[t]=e);for(let n=0;n!==t;++n)e[n]=i.allocateTextureUnit();return e}function ux(i,t){let e=this.cache;e[0]!==t&&(i.uniform1f(this.addr,t),e[0]=t)}function fx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y)&&(i.uniform2f(this.addr,t.x,t.y),e[0]=t.x,e[1]=t.y);else{if(Ne(e,t))return;i.uniform2fv(this.addr,t),De(e,t)}}function dx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z)&&(i.uniform3f(this.addr,t.x,t.y,t.z),e[0]=t.x,e[1]=t.y,e[2]=t.z);else if(t.r!==void 0)(e[0]!==t.r||e[1]!==t.g||e[2]!==t.b)&&(i.uniform3f(this.addr,t.r,t.g,t.b),e[0]=t.r,e[1]=t.g,e[2]=t.b);else{if(Ne(e,t))return;i.uniform3fv(this.addr,t),De(e,t)}}function px(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z||e[3]!==t.w)&&(i.uniform4f(this.addr,t.x,t.y,t.z,t.w),e[0]=t.x,e[1]=t.y,e[2]=t.z,e[3]=t.w);else{if(Ne(e,t))return;i.uniform4fv(this.addr,t),De(e,t)}}function mx(i,t){let e=this.cache,n=t.elements;if(n===void 0){if(Ne(e,t))return;i.uniformMatrix2fv(this.addr,!1,t),De(e,t)}else{if(Ne(e,n))return;Ef.set(n),i.uniformMatrix2fv(this.addr,!1,Ef),De(e,n)}}function gx(i,t){let e=this.cache,n=t.elements;if(n===void 0){if(Ne(e,t))return;i.uniformMatrix3fv(this.addr,!1,t),De(e,t)}else{if(Ne(e,n))return;Tf.set(n),i.uniformMatrix3fv(this.addr,!1,Tf),De(e,n)}}function _x(i,t){let e=this.cache,n=t.elements;if(n===void 0){if(Ne(e,t))return;i.uniformMatrix4fv(this.addr,!1,t),De(e,t)}else{if(Ne(e,n))return;Af.set(n),i.uniformMatrix4fv(this.addr,!1,Af),De(e,n)}}function xx(i,t){let e=this.cache;e[0]!==t&&(i.uniform1i(this.addr,t),e[0]=t)}function vx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y)&&(i.uniform2i(this.addr,t.x,t.y),e[0]=t.x,e[1]=t.y);else{if(Ne(e,t))return;i.uniform2iv(this.addr,t),De(e,t)}}function yx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z)&&(i.uniform3i(this.addr,t.x,t.y,t.z),e[0]=t.x,e[1]=t.y,e[2]=t.z);else{if(Ne(e,t))return;i.uniform3iv(this.addr,t),De(e,t)}}function Mx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z||e[3]!==t.w)&&(i.uniform4i(this.addr,t.x,t.y,t.z,t.w),e[0]=t.x,e[1]=t.y,e[2]=t.z,e[3]=t.w);else{if(Ne(e,t))return;i.uniform4iv(this.addr,t),De(e,t)}}function bx(i,t){let e=this.cache;e[0]!==t&&(i.uniform1ui(this.addr,t),e[0]=t)}function Sx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y)&&(i.uniform2ui(this.addr,t.x,t.y),e[0]=t.x,e[1]=t.y);else{if(Ne(e,t))return;i.uniform2uiv(this.addr,t),De(e,t)}}function wx(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z)&&(i.uniform3ui(this.addr,t.x,t.y,t.z),e[0]=t.x,e[1]=t.y,e[2]=t.z);else{if(Ne(e,t))return;i.uniform3uiv(this.addr,t),De(e,t)}}function Ax(i,t){let e=this.cache;if(t.x!==void 0)(e[0]!==t.x||e[1]!==t.y||e[2]!==t.z||e[3]!==t.w)&&(i.uniform4ui(this.addr,t.x,t.y,t.z,t.w),e[0]=t.x,e[1]=t.y,e[2]=t.z,e[3]=t.w);else{if(Ne(e,t))return;i.uniform4uiv(this.addr,t),De(e,t)}}function Tx(i,t,e){let n=this.cache,s=e.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s);let r;this.type===i.SAMPLER_2D_SHADOW?(nh.compareFunction=e.isReversedDepthBuffer()?el:tl,r=nh):r=Gf,e.setTexture2D(t||r,s)}function Ex(i,t,e){let n=this.cache,s=e.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),e.setTexture3D(t||Wf,s)}function Cx(i,t,e){let n=this.cache,s=e.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),e.setTextureCube(t||Xf,s)}function Rx(i,t,e){let n=this.cache,s=e.allocateTextureUnit();n[0]!==s&&(i.uniform1i(this.addr,s),n[0]=s),e.setTexture2DArray(t||Hf,s)}function Px(i){switch(i){case 5126:return ux;case 35664:return fx;case 35665:return dx;case 35666:return px;case 35674:return mx;case 35675:return gx;case 35676:return _x;case 5124:case 35670:return xx;case 35667:case 35671:return vx;case 35668:case 35672:return yx;case 35669:case 35673:return Mx;case 5125:return bx;case 36294:return Sx;case 36295:return wx;case 36296:return Ax;case 35678:case 36198:case 36298:case 36306:case 35682:return Tx;case 35679:case 36299:case 36307:return Ex;case 35680:case 36300:case 36308:case 36293:return Cx;case 36289:case 36303:case 36311:case 36292:return Rx}}function Ix(i,t){i.uniform1fv(this.addr,t)}function Lx(i,t){let e=Bs(t,this.size,2);i.uniform2fv(this.addr,e)}function Nx(i,t){let e=Bs(t,this.size,3);i.uniform3fv(this.addr,e)}function Dx(i,t){let e=Bs(t,this.size,4);i.uniform4fv(this.addr,e)}function Fx(i,t){let e=Bs(t,this.size,4);i.uniformMatrix2fv(this.addr,!1,e)}function Ux(i,t){let e=Bs(t,this.size,9);i.uniformMatrix3fv(this.addr,!1,e)}function Ox(i,t){let e=Bs(t,this.size,16);i.uniformMatrix4fv(this.addr,!1,e)}function Bx(i,t){i.uniform1iv(this.addr,t)}function kx(i,t){i.uniform2iv(this.addr,t)}function zx(i,t){i.uniform3iv(this.addr,t)}function Vx(i,t){i.uniform4iv(this.addr,t)}function Gx(i,t){i.uniform1uiv(this.addr,t)}function Hx(i,t){i.uniform2uiv(this.addr,t)}function Wx(i,t){i.uniform3uiv(this.addr,t)}function Xx(i,t){i.uniform4uiv(this.addr,t)}function qx(i,t,e){let n=this.cache,s=t.length,r=ll(e,s);Ne(n,r)||(i.uniform1iv(this.addr,r),De(n,r));let a;this.type===i.SAMPLER_2D_SHADOW?a=nh:a=Gf;for(let o=0;o!==s;++o)e.setTexture2D(t[o]||a,r[o])}function Yx(i,t,e){let n=this.cache,s=t.length,r=ll(e,s);Ne(n,r)||(i.uniform1iv(this.addr,r),De(n,r));for(let a=0;a!==s;++a)e.setTexture3D(t[a]||Wf,r[a])}function Zx(i,t,e){let n=this.cache,s=t.length,r=ll(e,s);Ne(n,r)||(i.uniform1iv(this.addr,r),De(n,r));for(let a=0;a!==s;++a)e.setTextureCube(t[a]||Xf,r[a])}function Jx(i,t,e){let n=this.cache,s=t.length,r=ll(e,s);Ne(n,r)||(i.uniform1iv(this.addr,r),De(n,r));for(let a=0;a!==s;++a)e.setTexture2DArray(t[a]||Hf,r[a])}function $x(i){switch(i){case 5126:return Ix;case 35664:return Lx;case 35665:return Nx;case 35666:return Dx;case 35674:return Fx;case 35675:return Ux;case 35676:return Ox;case 5124:case 35670:return Bx;case 35667:case 35671:return kx;case 35668:case 35672:return zx;case 35669:case 35673:return Vx;case 5125:return Gx;case 36294:return Hx;case 36295:return Wx;case 36296:return Xx;case 35678:case 36198:case 36298:case 36306:case 35682:return qx;case 35679:case 36299:case 36307:return Yx;case 35680:case 36300:case 36308:case 36293:return Zx;case 36289:case 36303:case 36311:case 36292:return Jx}}var ih=class{constructor(t,e,n){this.id=t,this.addr=n,this.cache=[],this.type=e.type,this.setValue=Px(e.type)}},sh=class{constructor(t,e,n){this.id=t,this.addr=n,this.cache=[],this.type=e.type,this.size=e.size,this.setValue=$x(e.type)}},rh=class{constructor(t){this.id=t,this.seq=[],this.map={}}setValue(t,e,n){let s=this.seq;for(let r=0,a=s.length;r!==a;++r){let o=s[r];o.setValue(t,e[o.id],n)}}},th=/(\w+)(\])?(\[|\.)?/g;function Cf(i,t){i.seq.push(t),i.map[t.id]=t}function Kx(i,t,e){let n=i.name,s=n.length;for(th.lastIndex=0;;){let r=th.exec(n),a=th.lastIndex,o=r[1],l=r[2]==="]",c=r[3];if(l&&(o=o|0),c===void 0||c==="["&&a+2===s){Cf(e,c===void 0?new ih(o,i,t):new sh(o,i,t));break}else{let f=e.map[o];f===void 0&&(f=new rh(o),Cf(e,f)),e=f}}}var Os=class{constructor(t,e){this.seq=[],this.map={};let n=t.getProgramParameter(e,t.ACTIVE_UNIFORMS);for(let a=0;a<n;++a){let o=t.getActiveUniform(e,a),l=t.getUniformLocation(e,o.name);Kx(o,l,this)}let s=[],r=[];for(let a of this.seq)a.type===t.SAMPLER_2D_SHADOW||a.type===t.SAMPLER_CUBE_SHADOW||a.type===t.SAMPLER_2D_ARRAY_SHADOW?s.push(a):r.push(a);s.length>0&&(this.seq=s.concat(r))}setValue(t,e,n,s){let r=this.map[e];r!==void 0&&r.setValue(t,n,s)}setOptional(t,e,n){let s=e[n];s!==void 0&&this.setValue(t,n,s)}static upload(t,e,n,s){for(let r=0,a=e.length;r!==a;++r){let o=e[r],l=n[o.id];l.needsUpdate!==!1&&o.setValue(t,l.value,s)}}static seqWithValue(t,e){let n=[];for(let s=0,r=t.length;s!==r;++s){let a=t[s];a.id in e&&n.push(a)}return n}};function Rf(i,t,e){let n=i.createShader(t);return i.shaderSource(n,e),i.compileShader(n),n}var jx=37297,Qx=0;function tv(i,t){let e=i.split(`
`),n=[],s=Math.max(t-6,0),r=Math.min(t+6,e.length);for(let a=s;a<r;a++){let o=a+1;n.push(`${o===t?">":" "} ${o}: ${e[a]}`)}return n.join(`
`)}var Pf=new Dt;function ev(i){Ht._getMatrix(Pf,Ht.workingColorSpace,i);let t=`mat3( ${Pf.elements.map(e=>e.toFixed(4))} )`;switch(Ht.getTransfer(i)){case tr:return[t,"LinearTransferOETF"];case Kt:return[t,"sRGBTransferOETF"];default:return Et("WebGLProgram: Unsupported color space: ",i),[t,"LinearTransferOETF"]}}function If(i,t,e){let n=i.getShaderParameter(t,i.COMPILE_STATUS),r=(i.getShaderInfoLog(t)||"").trim();if(n&&r==="")return"";let a=/ERROR: 0:(\d+)/.exec(r);if(a){let o=parseInt(a[1]);return e.toUpperCase()+`

`+r+`

`+tv(i.getShaderSource(t),o)}else return r}function nv(i,t){let e=ev(t);return[`vec4 ${i}( vec4 value ) {`,`	return ${e[1]}( vec4( value.rgb * ${e[0]}, value.a ) );`,"}"].join(`
`)}var iv={[_r]:"Linear",[xr]:"Reinhard",[vr]:"Cineon",[Ci]:"ACESFilmic",[Mr]:"AgX",[br]:"Neutral",[yr]:"Custom"};function sv(i,t){let e=iv[t];return e===void 0?(Et("WebGLProgram: Unsupported toneMapping:",t),"vec3 "+i+"( vec3 color ) { return LinearToneMapping( color ); }"):"vec3 "+i+"( vec3 color ) { return "+e+"ToneMapping( color ); }"}var il=new D;function rv(){Ht.getLuminanceCoefficients(il);let i=il.x.toFixed(4),t=il.y.toFixed(4),e=il.z.toFixed(4);return["float luminance( const in vec3 rgb ) {",`	const vec3 weights = vec3( ${i}, ${t}, ${e} );`,"	return dot( weights, rgb );","}"].join(`
`)}function av(i){return[i.extensionClipCullDistance?"#extension GL_ANGLE_clip_cull_distance : require":"",i.extensionMultiDraw?"#extension GL_ANGLE_multi_draw : require":""].filter(Dr).join(`
`)}function ov(i){let t=[];for(let e in i){let n=i[e];n!==!1&&t.push("#define "+e+" "+n)}return t.join(`
`)}function lv(i,t){let e={},n=i.getProgramParameter(t,i.ACTIVE_ATTRIBUTES);for(let s=0;s<n;s++){let r=i.getActiveAttrib(t,s),a=r.name,o=1;r.type===i.FLOAT_MAT2&&(o=2),r.type===i.FLOAT_MAT3&&(o=3),r.type===i.FLOAT_MAT4&&(o=4),e[a]={type:r.type,location:i.getAttribLocation(t,a),locationSize:o}}return e}function Dr(i){return i!==""}function Lf(i,t){let e=t.numSpotLightShadows+t.numSpotLightMaps-t.numSpotLightShadowsWithMaps;return i.replace(/NUM_DIR_LIGHTS/g,t.numDirLights).replace(/NUM_SPOT_LIGHTS/g,t.numSpotLights).replace(/NUM_SPOT_LIGHT_MAPS/g,t.numSpotLightMaps).replace(/NUM_SPOT_LIGHT_COORDS/g,e).replace(/NUM_RECT_AREA_LIGHTS/g,t.numRectAreaLights).replace(/NUM_POINT_LIGHTS/g,t.numPointLights).replace(/NUM_HEMI_LIGHTS/g,t.numHemiLights).replace(/NUM_DIR_LIGHT_SHADOWS/g,t.numDirLightShadows).replace(/NUM_SPOT_LIGHT_SHADOWS_WITH_MAPS/g,t.numSpotLightShadowsWithMaps).replace(/NUM_SPOT_LIGHT_SHADOWS/g,t.numSpotLightShadows).replace(/NUM_POINT_LIGHT_SHADOWS/g,t.numPointLightShadows)}function Nf(i,t){return i.replace(/NUM_CLIPPING_PLANES/g,t.numClippingPlanes).replace(/UNION_CLIPPING_PLANES/g,t.numClippingPlanes-t.numClipIntersection)}var cv=/^[ \t]*#include +<([\w\d./]+)>/gm;function ah(i){return i.replace(cv,uv)}var hv=new Map;function uv(i,t){let e=Vt[t];if(e===void 0){let n=hv.get(t);if(n!==void 0)e=Vt[n],Et('WebGLRenderer: Shader chunk "%s" has been deprecated. Use "%s" instead.',t,n);else throw new Error("Can not resolve #include <"+t+">")}return ah(e)}var fv=/#pragma unroll_loop_start\s+for\s*\(\s*int\s+i\s*=\s*(\d+)\s*;\s*i\s*<\s*(\d+)\s*;\s*i\s*\+\+\s*\)\s*{([\s\S]+?)}\s+#pragma unroll_loop_end/g;function Df(i){return i.replace(fv,dv)}function dv(i,t,e,n){let s="";for(let r=parseInt(t);r<parseInt(e);r++)s+=n.replace(/\[\s*i\s*\]/g,"[ "+r+" ]").replace(/UNROLLED_LOOP_INDEX/g,r);return s}function Ff(i){let t=`precision ${i.precision} float;
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
#define LOW_PRECISION`),t}var pv={[gr]:"SHADOWMAP_TYPE_PCF",[Ns]:"SHADOWMAP_TYPE_VSM"};function mv(i){return pv[i.shadowMapType]||"SHADOWMAP_TYPE_BASIC"}var gv={[Ri]:"ENVMAP_TYPE_CUBE",[ss]:"ENVMAP_TYPE_CUBE",[Sr]:"ENVMAP_TYPE_CUBE_UV"};function _v(i){return i.envMap===!1?"ENVMAP_TYPE_CUBE":gv[i.envMapMode]||"ENVMAP_TYPE_CUBE"}var xv={[ss]:"ENVMAP_MODE_REFRACTION"};function vv(i){return i.envMap===!1?"ENVMAP_MODE_REFLECTION":xv[i.envMapMode]||"ENVMAP_MODE_REFLECTION"}var yv={[Rc]:"ENVMAP_BLENDING_MULTIPLY",[tf]:"ENVMAP_BLENDING_MIX",[ef]:"ENVMAP_BLENDING_ADD"};function Mv(i){return i.envMap===!1?"ENVMAP_BLENDING_NONE":yv[i.combine]||"ENVMAP_BLENDING_NONE"}function bv(i){let t=i.envMapCubeUVHeight;if(t===null)return null;let e=Math.log2(t)-2,n=1/t;return{texelWidth:1/(3*Math.max(Math.pow(2,e),7*16)),texelHeight:n,maxMip:e}}function Sv(i,t,e,n){let s=i.getContext(),r=e.defines,a=e.vertexShader,o=e.fragmentShader,l=mv(e),c=_v(e),h=vv(e),f=Mv(e),u=bv(e),p=av(e),g=ov(r),x=s.createProgram(),m,d,y=e.glslVersion?"#version "+e.glslVersion+`
`:"";e.isRawShaderMaterial?(m=["#define SHADER_TYPE "+e.shaderType,"#define SHADER_NAME "+e.shaderName,g].filter(Dr).join(`
`),m.length>0&&(m+=`
`),d=["#define SHADER_TYPE "+e.shaderType,"#define SHADER_NAME "+e.shaderName,g].filter(Dr).join(`
`),d.length>0&&(d+=`
`)):(m=[Ff(e),"#define SHADER_TYPE "+e.shaderType,"#define SHADER_NAME "+e.shaderName,g,e.extensionClipCullDistance?"#define USE_CLIP_DISTANCE":"",e.batching?"#define USE_BATCHING":"",e.batchingColor?"#define USE_BATCHING_COLOR":"",e.instancing?"#define USE_INSTANCING":"",e.instancingColor?"#define USE_INSTANCING_COLOR":"",e.instancingMorph?"#define USE_INSTANCING_MORPH":"",e.useFog&&e.fog?"#define USE_FOG":"",e.useFog&&e.fogExp2?"#define FOG_EXP2":"",e.map?"#define USE_MAP":"",e.envMap?"#define USE_ENVMAP":"",e.envMap?"#define "+h:"",e.lightMap?"#define USE_LIGHTMAP":"",e.aoMap?"#define USE_AOMAP":"",e.bumpMap?"#define USE_BUMPMAP":"",e.normalMap?"#define USE_NORMALMAP":"",e.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",e.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",e.displacementMap?"#define USE_DISPLACEMENTMAP":"",e.emissiveMap?"#define USE_EMISSIVEMAP":"",e.anisotropy?"#define USE_ANISOTROPY":"",e.anisotropyMap?"#define USE_ANISOTROPYMAP":"",e.clearcoatMap?"#define USE_CLEARCOATMAP":"",e.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",e.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",e.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",e.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",e.specularMap?"#define USE_SPECULARMAP":"",e.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",e.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",e.roughnessMap?"#define USE_ROUGHNESSMAP":"",e.metalnessMap?"#define USE_METALNESSMAP":"",e.alphaMap?"#define USE_ALPHAMAP":"",e.alphaHash?"#define USE_ALPHAHASH":"",e.transmission?"#define USE_TRANSMISSION":"",e.transmissionMap?"#define USE_TRANSMISSIONMAP":"",e.thicknessMap?"#define USE_THICKNESSMAP":"",e.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",e.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",e.mapUv?"#define MAP_UV "+e.mapUv:"",e.alphaMapUv?"#define ALPHAMAP_UV "+e.alphaMapUv:"",e.lightMapUv?"#define LIGHTMAP_UV "+e.lightMapUv:"",e.aoMapUv?"#define AOMAP_UV "+e.aoMapUv:"",e.emissiveMapUv?"#define EMISSIVEMAP_UV "+e.emissiveMapUv:"",e.bumpMapUv?"#define BUMPMAP_UV "+e.bumpMapUv:"",e.normalMapUv?"#define NORMALMAP_UV "+e.normalMapUv:"",e.displacementMapUv?"#define DISPLACEMENTMAP_UV "+e.displacementMapUv:"",e.metalnessMapUv?"#define METALNESSMAP_UV "+e.metalnessMapUv:"",e.roughnessMapUv?"#define ROUGHNESSMAP_UV "+e.roughnessMapUv:"",e.anisotropyMapUv?"#define ANISOTROPYMAP_UV "+e.anisotropyMapUv:"",e.clearcoatMapUv?"#define CLEARCOATMAP_UV "+e.clearcoatMapUv:"",e.clearcoatNormalMapUv?"#define CLEARCOAT_NORMALMAP_UV "+e.clearcoatNormalMapUv:"",e.clearcoatRoughnessMapUv?"#define CLEARCOAT_ROUGHNESSMAP_UV "+e.clearcoatRoughnessMapUv:"",e.iridescenceMapUv?"#define IRIDESCENCEMAP_UV "+e.iridescenceMapUv:"",e.iridescenceThicknessMapUv?"#define IRIDESCENCE_THICKNESSMAP_UV "+e.iridescenceThicknessMapUv:"",e.sheenColorMapUv?"#define SHEEN_COLORMAP_UV "+e.sheenColorMapUv:"",e.sheenRoughnessMapUv?"#define SHEEN_ROUGHNESSMAP_UV "+e.sheenRoughnessMapUv:"",e.specularMapUv?"#define SPECULARMAP_UV "+e.specularMapUv:"",e.specularColorMapUv?"#define SPECULAR_COLORMAP_UV "+e.specularColorMapUv:"",e.specularIntensityMapUv?"#define SPECULAR_INTENSITYMAP_UV "+e.specularIntensityMapUv:"",e.transmissionMapUv?"#define TRANSMISSIONMAP_UV "+e.transmissionMapUv:"",e.thicknessMapUv?"#define THICKNESSMAP_UV "+e.thicknessMapUv:"",e.vertexTangents&&e.flatShading===!1?"#define USE_TANGENT":"",e.vertexNormals?"#define HAS_NORMAL":"",e.vertexColors?"#define USE_COLOR":"",e.vertexAlphas?"#define USE_COLOR_ALPHA":"",e.vertexUv1s?"#define USE_UV1":"",e.vertexUv2s?"#define USE_UV2":"",e.vertexUv3s?"#define USE_UV3":"",e.pointsUvs?"#define USE_POINTS_UV":"",e.flatShading?"#define FLAT_SHADED":"",e.skinning?"#define USE_SKINNING":"",e.morphTargets?"#define USE_MORPHTARGETS":"",e.morphNormals&&e.flatShading===!1?"#define USE_MORPHNORMALS":"",e.morphColors?"#define USE_MORPHCOLORS":"",e.morphTargetsCount>0?"#define MORPHTARGETS_TEXTURE_STRIDE "+e.morphTextureStride:"",e.morphTargetsCount>0?"#define MORPHTARGETS_COUNT "+e.morphTargetsCount:"",e.doubleSided?"#define DOUBLE_SIDED":"",e.flipSided?"#define FLIP_SIDED":"",e.shadowMapEnabled?"#define USE_SHADOWMAP":"",e.shadowMapEnabled?"#define "+l:"",e.sizeAttenuation?"#define USE_SIZEATTENUATION":"",e.numLightProbes>0?"#define USE_LIGHT_PROBES":"",e.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",e.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 modelMatrix;","uniform mat4 modelViewMatrix;","uniform mat4 projectionMatrix;","uniform mat4 viewMatrix;","uniform mat3 normalMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;","#ifdef USE_INSTANCING","	attribute mat4 instanceMatrix;","#endif","#ifdef USE_INSTANCING_COLOR","	attribute vec3 instanceColor;","#endif","#ifdef USE_INSTANCING_MORPH","	uniform sampler2D morphTexture;","#endif","attribute vec3 position;","attribute vec3 normal;","attribute vec2 uv;","#ifdef USE_UV1","	attribute vec2 uv1;","#endif","#ifdef USE_UV2","	attribute vec2 uv2;","#endif","#ifdef USE_UV3","	attribute vec2 uv3;","#endif","#ifdef USE_TANGENT","	attribute vec4 tangent;","#endif","#if defined( USE_COLOR_ALPHA )","	attribute vec4 color;","#elif defined( USE_COLOR )","	attribute vec3 color;","#endif","#ifdef USE_SKINNING","	attribute vec4 skinIndex;","	attribute vec4 skinWeight;","#endif",`
`].filter(Dr).join(`
`),d=[Ff(e),"#define SHADER_TYPE "+e.shaderType,"#define SHADER_NAME "+e.shaderName,g,e.useFog&&e.fog?"#define USE_FOG":"",e.useFog&&e.fogExp2?"#define FOG_EXP2":"",e.alphaToCoverage?"#define ALPHA_TO_COVERAGE":"",e.map?"#define USE_MAP":"",e.matcap?"#define USE_MATCAP":"",e.envMap?"#define USE_ENVMAP":"",e.envMap?"#define "+c:"",e.envMap?"#define "+h:"",e.envMap?"#define "+f:"",u?"#define CUBEUV_TEXEL_WIDTH "+u.texelWidth:"",u?"#define CUBEUV_TEXEL_HEIGHT "+u.texelHeight:"",u?"#define CUBEUV_MAX_MIP "+u.maxMip+".0":"",e.lightMap?"#define USE_LIGHTMAP":"",e.aoMap?"#define USE_AOMAP":"",e.bumpMap?"#define USE_BUMPMAP":"",e.normalMap?"#define USE_NORMALMAP":"",e.normalMapObjectSpace?"#define USE_NORMALMAP_OBJECTSPACE":"",e.normalMapTangentSpace?"#define USE_NORMALMAP_TANGENTSPACE":"",e.packedNormalMap?"#define USE_PACKED_NORMALMAP":"",e.emissiveMap?"#define USE_EMISSIVEMAP":"",e.anisotropy?"#define USE_ANISOTROPY":"",e.anisotropyMap?"#define USE_ANISOTROPYMAP":"",e.clearcoat?"#define USE_CLEARCOAT":"",e.clearcoatMap?"#define USE_CLEARCOATMAP":"",e.clearcoatRoughnessMap?"#define USE_CLEARCOAT_ROUGHNESSMAP":"",e.clearcoatNormalMap?"#define USE_CLEARCOAT_NORMALMAP":"",e.dispersion?"#define USE_DISPERSION":"",e.iridescence?"#define USE_IRIDESCENCE":"",e.iridescenceMap?"#define USE_IRIDESCENCEMAP":"",e.iridescenceThicknessMap?"#define USE_IRIDESCENCE_THICKNESSMAP":"",e.specularMap?"#define USE_SPECULARMAP":"",e.specularColorMap?"#define USE_SPECULAR_COLORMAP":"",e.specularIntensityMap?"#define USE_SPECULAR_INTENSITYMAP":"",e.roughnessMap?"#define USE_ROUGHNESSMAP":"",e.metalnessMap?"#define USE_METALNESSMAP":"",e.alphaMap?"#define USE_ALPHAMAP":"",e.alphaTest?"#define USE_ALPHATEST":"",e.alphaHash?"#define USE_ALPHAHASH":"",e.sheen?"#define USE_SHEEN":"",e.sheenColorMap?"#define USE_SHEEN_COLORMAP":"",e.sheenRoughnessMap?"#define USE_SHEEN_ROUGHNESSMAP":"",e.transmission?"#define USE_TRANSMISSION":"",e.transmissionMap?"#define USE_TRANSMISSIONMAP":"",e.thicknessMap?"#define USE_THICKNESSMAP":"",e.vertexTangents&&e.flatShading===!1?"#define USE_TANGENT":"",e.vertexColors||e.instancingColor?"#define USE_COLOR":"",e.vertexAlphas||e.batchingColor?"#define USE_COLOR_ALPHA":"",e.vertexUv1s?"#define USE_UV1":"",e.vertexUv2s?"#define USE_UV2":"",e.vertexUv3s?"#define USE_UV3":"",e.pointsUvs?"#define USE_POINTS_UV":"",e.gradientMap?"#define USE_GRADIENTMAP":"",e.flatShading?"#define FLAT_SHADED":"",e.doubleSided?"#define DOUBLE_SIDED":"",e.flipSided?"#define FLIP_SIDED":"",e.shadowMapEnabled?"#define USE_SHADOWMAP":"",e.shadowMapEnabled?"#define "+l:"",e.premultipliedAlpha?"#define PREMULTIPLIED_ALPHA":"",e.numLightProbes>0?"#define USE_LIGHT_PROBES":"",e.numLightProbeGrids>0?"#define USE_LIGHT_PROBES_GRID":"",e.decodeVideoTexture?"#define DECODE_VIDEO_TEXTURE":"",e.decodeVideoTextureEmissive?"#define DECODE_VIDEO_TEXTURE_EMISSIVE":"",e.logarithmicDepthBuffer?"#define USE_LOGARITHMIC_DEPTH_BUFFER":"",e.reversedDepthBuffer?"#define USE_REVERSED_DEPTH_BUFFER":"","uniform mat4 viewMatrix;","uniform vec3 cameraPosition;","uniform bool isOrthographic;",e.toneMapping!==pn?"#define TONE_MAPPING":"",e.toneMapping!==pn?Vt.tonemapping_pars_fragment:"",e.toneMapping!==pn?sv("toneMapping",e.toneMapping):"",e.dithering?"#define DITHERING":"",e.opaque?"#define OPAQUE":"",Vt.colorspace_pars_fragment,nv("linearToOutputTexel",e.outputColorSpace),rv(),e.useDepthPacking?"#define DEPTH_PACKING "+e.depthPacking:"",`
`].filter(Dr).join(`
`)),a=ah(a),a=Lf(a,e),a=Nf(a,e),o=ah(o),o=Lf(o,e),o=Nf(o,e),a=Df(a),o=Df(o),e.isRawShaderMaterial!==!0&&(y=`#version 300 es
`,m=[p,"#define attribute in","#define varying out","#define texture2D texture"].join(`
`)+`
`+m,d=["#define varying in",e.glslVersion===kc?"":"layout(location = 0) out highp vec4 pc_fragColor;",e.glslVersion===kc?"":"#define gl_FragColor pc_fragColor","#define gl_FragDepthEXT gl_FragDepth","#define texture2D texture","#define textureCube texture","#define texture2DProj textureProj","#define texture2DLodEXT textureLod","#define texture2DProjLodEXT textureProjLod","#define textureCubeLodEXT textureLod","#define texture2DGradEXT textureGrad","#define texture2DProjGradEXT textureProjGrad","#define textureCubeGradEXT textureGrad"].join(`
`)+`
`+d);let S=y+m+a,b=y+d+o,T=Rf(s,s.VERTEX_SHADER,S),w=Rf(s,s.FRAGMENT_SHADER,b);s.attachShader(x,T),s.attachShader(x,w),e.index0AttributeName!==void 0?s.bindAttribLocation(x,0,e.index0AttributeName):e.morphTargets===!0&&s.bindAttribLocation(x,0,"position"),s.linkProgram(x);function R(C){if(i.debug.checkShaderErrors){let N=s.getProgramInfoLog(x)||"",H=s.getShaderInfoLog(T)||"",W=s.getShaderInfoLog(w)||"",U=N.trim(),z=H.trim(),V=W.trim(),$=!0,tt=!0;if(s.getProgramParameter(x,s.LINK_STATUS)===!1)if($=!1,typeof i.debug.onShaderError=="function")i.debug.onShaderError(s,x,T,w);else{let ct=If(s,T,"vertex"),Mt=If(s,w,"fragment");Rt("THREE.WebGLProgram: Shader Error "+s.getError()+" - VALIDATE_STATUS "+s.getProgramParameter(x,s.VALIDATE_STATUS)+`

Material Name: `+C.name+`
Material Type: `+C.type+`

Program Info Log: `+U+`
`+ct+`
`+Mt)}else U!==""?Et("WebGLProgram: Program Info Log:",U):(z===""||V==="")&&(tt=!1);tt&&(C.diagnostics={runnable:$,programLog:U,vertexShader:{log:z,prefix:m},fragmentShader:{log:V,prefix:d}})}s.deleteShader(T),s.deleteShader(w),v=new Os(s,x),E=lv(s,x)}let v;this.getUniforms=function(){return v===void 0&&R(this),v};let E;this.getAttributes=function(){return E===void 0&&R(this),E};let I=e.rendererExtensionParallelShaderCompile===!1;return this.isReady=function(){return I===!1&&(I=s.getProgramParameter(x,jx)),I},this.destroy=function(){n.releaseStatesOfProgram(this),s.deleteProgram(x),this.program=void 0},this.type=e.shaderType,this.name=e.shaderName,this.id=Qx++,this.cacheKey=t,this.usedTimes=1,this.program=x,this.vertexShader=T,this.fragmentShader=w,this}var wv=0,oh=class{constructor(){this.shaderCache=new Map,this.materialCache=new Map}update(t){let e=t.vertexShader,n=t.fragmentShader,s=this._getShaderStage(e),r=this._getShaderStage(n),a=this._getShaderCacheForMaterial(t);return a.has(s)===!1&&(a.add(s),s.usedTimes++),a.has(r)===!1&&(a.add(r),r.usedTimes++),this}remove(t){let e=this.materialCache.get(t);for(let n of e)n.usedTimes--,n.usedTimes===0&&this.shaderCache.delete(n.code);return this.materialCache.delete(t),this}getVertexShaderID(t){return this._getShaderStage(t.vertexShader).id}getFragmentShaderID(t){return this._getShaderStage(t.fragmentShader).id}dispose(){this.shaderCache.clear(),this.materialCache.clear()}_getShaderCacheForMaterial(t){let e=this.materialCache,n=e.get(t);return n===void 0&&(n=new Set,e.set(t,n)),n}_getShaderStage(t){let e=this.shaderCache,n=e.get(t);return n===void 0&&(n=new lh(t),e.set(t,n)),n}},lh=class{constructor(t){this.id=wv++,this.code=t,this.usedTimes=0}};function Av(i){return i===Li||i===Rr||i===Pr}function Tv(i,t,e,n,s,r){let a=new sr,o=new oh,l=new Set,c=[],h=new Map,f=n.logarithmicDepthBuffer,u=n.precision,p={MeshDepthMaterial:"depth",MeshDistanceMaterial:"distance",MeshNormalMaterial:"normal",MeshBasicMaterial:"basic",MeshLambertMaterial:"lambert",MeshPhongMaterial:"phong",MeshToonMaterial:"toon",MeshStandardMaterial:"physical",MeshPhysicalMaterial:"physical",MeshMatcapMaterial:"matcap",LineBasicMaterial:"basic",LineDashedMaterial:"dashed",PointsMaterial:"points",ShadowMaterial:"shadow",SpriteMaterial:"sprite"};function g(v){return l.add(v),v===0?"uv":`uv${v}`}function x(v,E,I,C,N,H){let W=C.fog,U=N.geometry,z=v.isMeshStandardMaterial||v.isMeshLambertMaterial||v.isMeshPhongMaterial?C.environment:null,V=v.isMeshStandardMaterial||v.isMeshLambertMaterial&&!v.envMap||v.isMeshPhongMaterial&&!v.envMap,$=t.get(v.envMap||z,V),tt=$&&$.mapping===Sr?$.image.height:null,ct=p[v.type];v.precision!==null&&(u=n.getMaxPrecision(v.precision),u!==v.precision&&Et("WebGLProgram.getParameters:",v.precision,"not supported, using",u,"instead."));let Mt=U.morphAttributes.position||U.morphAttributes.normal||U.morphAttributes.color,St=Mt!==void 0?Mt.length:0,Xt=0;U.morphAttributes.position!==void 0&&(Xt=1),U.morphAttributes.normal!==void 0&&(Xt=2),U.morphAttributes.color!==void 0&&(Xt=3);let te,kt,J,mt;if(ct){let Ot=Gn[ct];te=Ot.vertexShader,kt=Ot.fragmentShader}else te=v.vertexShader,kt=v.fragmentShader,o.update(v),J=o.getVertexShaderID(v),mt=o.getFragmentShaderID(v);let rt=i.getRenderTarget(),Ct=i.state.buffers.depth.getReversed(),Ft=N.isInstancedMesh===!0,Pt=N.isBatchedMesh===!0,pe=!!v.map,qt=!!v.matcap,ee=!!$,ue=!!v.aoMap,Wt=!!v.lightMap,Pe=!!v.bumpMap,me=!!v.normalMap,ln=!!v.displacementMap,L=!!v.emissiveMap,Ie=!!v.metalnessMap,Yt=!!v.roughnessMap,ce=v.anisotropy>0,ht=v.clearcoat>0,_e=v.dispersion>0,A=v.iridescence>0,_=v.sheen>0,O=v.transmission>0,Y=ce&&!!v.anisotropyMap,j=ht&&!!v.clearcoatMap,et=ht&&!!v.clearcoatNormalMap,lt=ht&&!!v.clearcoatRoughnessMap,X=A&&!!v.iridescenceMap,Z=A&&!!v.iridescenceThicknessMap,gt=_&&!!v.sheenColorMap,vt=_&&!!v.sheenRoughnessMap,at=!!v.specularMap,nt=!!v.specularColorMap,Nt=!!v.specularIntensityMap,zt=O&&!!v.transmissionMap,$t=O&&!!v.thicknessMap,P=!!v.gradientMap,it=!!v.alphaMap,q=v.alphaTest>0,_t=!!v.alphaHash,ot=!!v.extensions,K=pn;v.toneMapped&&(rt===null||rt.isXRRenderTarget===!0)&&(K=i.toneMapping);let wt={shaderID:ct,shaderType:v.type,shaderName:v.name,vertexShader:te,fragmentShader:kt,defines:v.defines,customVertexShaderID:J,customFragmentShaderID:mt,isRawShaderMaterial:v.isRawShaderMaterial===!0,glslVersion:v.glslVersion,precision:u,batching:Pt,batchingColor:Pt&&N._colorsTexture!==null,instancing:Ft,instancingColor:Ft&&N.instanceColor!==null,instancingMorph:Ft&&N.morphTexture!==null,outputColorSpace:rt===null?i.outputColorSpace:rt.isXRRenderTarget===!0?rt.texture.colorSpace:Ht.workingColorSpace,alphaToCoverage:!!v.alphaToCoverage,map:pe,matcap:qt,envMap:ee,envMapMode:ee&&$.mapping,envMapCubeUVHeight:tt,aoMap:ue,lightMap:Wt,bumpMap:Pe,normalMap:me,displacementMap:ln,emissiveMap:L,normalMapObjectSpace:me&&v.normalMapType===rf,normalMapTangentSpace:me&&v.normalMapType===Bc,packedNormalMap:me&&v.normalMapType===Bc&&Av(v.normalMap.format),metalnessMap:Ie,roughnessMap:Yt,anisotropy:ce,anisotropyMap:Y,clearcoat:ht,clearcoatMap:j,clearcoatNormalMap:et,clearcoatRoughnessMap:lt,dispersion:_e,iridescence:A,iridescenceMap:X,iridescenceThicknessMap:Z,sheen:_,sheenColorMap:gt,sheenRoughnessMap:vt,specularMap:at,specularColorMap:nt,specularIntensityMap:Nt,transmission:O,transmissionMap:zt,thicknessMap:$t,gradientMap:P,opaque:v.transparent===!1&&v.blending===On&&v.alphaToCoverage===!1,alphaMap:it,alphaTest:q,alphaHash:_t,combine:v.combine,mapUv:pe&&g(v.map.channel),aoMapUv:ue&&g(v.aoMap.channel),lightMapUv:Wt&&g(v.lightMap.channel),bumpMapUv:Pe&&g(v.bumpMap.channel),normalMapUv:me&&g(v.normalMap.channel),displacementMapUv:ln&&g(v.displacementMap.channel),emissiveMapUv:L&&g(v.emissiveMap.channel),metalnessMapUv:Ie&&g(v.metalnessMap.channel),roughnessMapUv:Yt&&g(v.roughnessMap.channel),anisotropyMapUv:Y&&g(v.anisotropyMap.channel),clearcoatMapUv:j&&g(v.clearcoatMap.channel),clearcoatNormalMapUv:et&&g(v.clearcoatNormalMap.channel),clearcoatRoughnessMapUv:lt&&g(v.clearcoatRoughnessMap.channel),iridescenceMapUv:X&&g(v.iridescenceMap.channel),iridescenceThicknessMapUv:Z&&g(v.iridescenceThicknessMap.channel),sheenColorMapUv:gt&&g(v.sheenColorMap.channel),sheenRoughnessMapUv:vt&&g(v.sheenRoughnessMap.channel),specularMapUv:at&&g(v.specularMap.channel),specularColorMapUv:nt&&g(v.specularColorMap.channel),specularIntensityMapUv:Nt&&g(v.specularIntensityMap.channel),transmissionMapUv:zt&&g(v.transmissionMap.channel),thicknessMapUv:$t&&g(v.thicknessMap.channel),alphaMapUv:it&&g(v.alphaMap.channel),vertexTangents:!!U.attributes.tangent&&(me||ce),vertexNormals:!!U.attributes.normal,vertexColors:v.vertexColors,vertexAlphas:v.vertexColors===!0&&!!U.attributes.color&&U.attributes.color.itemSize===4,pointsUvs:N.isPoints===!0&&!!U.attributes.uv&&(pe||it),fog:!!W,useFog:v.fog===!0,fogExp2:!!W&&W.isFogExp2,flatShading:v.wireframe===!1&&(v.flatShading===!0||U.attributes.normal===void 0&&me===!1&&(v.isMeshLambertMaterial||v.isMeshPhongMaterial||v.isMeshStandardMaterial||v.isMeshPhysicalMaterial)),sizeAttenuation:v.sizeAttenuation===!0,logarithmicDepthBuffer:f,reversedDepthBuffer:Ct,skinning:N.isSkinnedMesh===!0,morphTargets:U.morphAttributes.position!==void 0,morphNormals:U.morphAttributes.normal!==void 0,morphColors:U.morphAttributes.color!==void 0,morphTargetsCount:St,morphTextureStride:Xt,numDirLights:E.directional.length,numPointLights:E.point.length,numSpotLights:E.spot.length,numSpotLightMaps:E.spotLightMap.length,numRectAreaLights:E.rectArea.length,numHemiLights:E.hemi.length,numDirLightShadows:E.directionalShadowMap.length,numPointLightShadows:E.pointShadowMap.length,numSpotLightShadows:E.spotShadowMap.length,numSpotLightShadowsWithMaps:E.numSpotLightShadowsWithMaps,numLightProbes:E.numLightProbes,numLightProbeGrids:H.length,numClippingPlanes:r.numPlanes,numClipIntersection:r.numIntersection,dithering:v.dithering,shadowMapEnabled:i.shadowMap.enabled&&I.length>0,shadowMapType:i.shadowMap.type,toneMapping:K,decodeVideoTexture:pe&&v.map.isVideoTexture===!0&&Ht.getTransfer(v.map.colorSpace)===Kt,decodeVideoTextureEmissive:L&&v.emissiveMap.isVideoTexture===!0&&Ht.getTransfer(v.emissiveMap.colorSpace)===Kt,premultipliedAlpha:v.premultipliedAlpha,doubleSided:v.side===zn,flipSided:v.side===$e,useDepthPacking:v.depthPacking>=0,depthPacking:v.depthPacking||0,index0AttributeName:v.index0AttributeName,extensionClipCullDistance:ot&&v.extensions.clipCullDistance===!0&&e.has("WEBGL_clip_cull_distance"),extensionMultiDraw:(ot&&v.extensions.multiDraw===!0||Pt)&&e.has("WEBGL_multi_draw"),rendererExtensionParallelShaderCompile:e.has("KHR_parallel_shader_compile"),customProgramCacheKey:v.customProgramCacheKey()};return wt.vertexUv1s=l.has(1),wt.vertexUv2s=l.has(2),wt.vertexUv3s=l.has(3),l.clear(),wt}function m(v){let E=[];if(v.shaderID?E.push(v.shaderID):(E.push(v.customVertexShaderID),E.push(v.customFragmentShaderID)),v.defines!==void 0)for(let I in v.defines)E.push(I),E.push(v.defines[I]);return v.isRawShaderMaterial===!1&&(d(E,v),y(E,v),E.push(i.outputColorSpace)),E.push(v.customProgramCacheKey),E.join()}function d(v,E){v.push(E.precision),v.push(E.outputColorSpace),v.push(E.envMapMode),v.push(E.envMapCubeUVHeight),v.push(E.mapUv),v.push(E.alphaMapUv),v.push(E.lightMapUv),v.push(E.aoMapUv),v.push(E.bumpMapUv),v.push(E.normalMapUv),v.push(E.displacementMapUv),v.push(E.emissiveMapUv),v.push(E.metalnessMapUv),v.push(E.roughnessMapUv),v.push(E.anisotropyMapUv),v.push(E.clearcoatMapUv),v.push(E.clearcoatNormalMapUv),v.push(E.clearcoatRoughnessMapUv),v.push(E.iridescenceMapUv),v.push(E.iridescenceThicknessMapUv),v.push(E.sheenColorMapUv),v.push(E.sheenRoughnessMapUv),v.push(E.specularMapUv),v.push(E.specularColorMapUv),v.push(E.specularIntensityMapUv),v.push(E.transmissionMapUv),v.push(E.thicknessMapUv),v.push(E.combine),v.push(E.fogExp2),v.push(E.sizeAttenuation),v.push(E.morphTargetsCount),v.push(E.morphAttributeCount),v.push(E.numDirLights),v.push(E.numPointLights),v.push(E.numSpotLights),v.push(E.numSpotLightMaps),v.push(E.numHemiLights),v.push(E.numRectAreaLights),v.push(E.numDirLightShadows),v.push(E.numPointLightShadows),v.push(E.numSpotLightShadows),v.push(E.numSpotLightShadowsWithMaps),v.push(E.numLightProbes),v.push(E.shadowMapType),v.push(E.toneMapping),v.push(E.numClippingPlanes),v.push(E.numClipIntersection),v.push(E.depthPacking)}function y(v,E){a.disableAll(),E.instancing&&a.enable(0),E.instancingColor&&a.enable(1),E.instancingMorph&&a.enable(2),E.matcap&&a.enable(3),E.envMap&&a.enable(4),E.normalMapObjectSpace&&a.enable(5),E.normalMapTangentSpace&&a.enable(6),E.clearcoat&&a.enable(7),E.iridescence&&a.enable(8),E.alphaTest&&a.enable(9),E.vertexColors&&a.enable(10),E.vertexAlphas&&a.enable(11),E.vertexUv1s&&a.enable(12),E.vertexUv2s&&a.enable(13),E.vertexUv3s&&a.enable(14),E.vertexTangents&&a.enable(15),E.anisotropy&&a.enable(16),E.alphaHash&&a.enable(17),E.batching&&a.enable(18),E.dispersion&&a.enable(19),E.batchingColor&&a.enable(20),E.gradientMap&&a.enable(21),E.packedNormalMap&&a.enable(22),E.vertexNormals&&a.enable(23),v.push(a.mask),a.disableAll(),E.fog&&a.enable(0),E.useFog&&a.enable(1),E.flatShading&&a.enable(2),E.logarithmicDepthBuffer&&a.enable(3),E.reversedDepthBuffer&&a.enable(4),E.skinning&&a.enable(5),E.morphTargets&&a.enable(6),E.morphNormals&&a.enable(7),E.morphColors&&a.enable(8),E.premultipliedAlpha&&a.enable(9),E.shadowMapEnabled&&a.enable(10),E.doubleSided&&a.enable(11),E.flipSided&&a.enable(12),E.useDepthPacking&&a.enable(13),E.dithering&&a.enable(14),E.transmission&&a.enable(15),E.sheen&&a.enable(16),E.opaque&&a.enable(17),E.pointsUvs&&a.enable(18),E.decodeVideoTexture&&a.enable(19),E.decodeVideoTextureEmissive&&a.enable(20),E.alphaToCoverage&&a.enable(21),E.numLightProbeGrids>0&&a.enable(22),v.push(a.mask)}function S(v){let E=p[v.type],I;if(E){let C=Gn[E];I=oi.clone(C.uniforms)}else I=v.uniforms;return I}function b(v,E){let I=h.get(E);return I!==void 0?++I.usedTimes:(I=new Sv(i,E,v,s),c.push(I),h.set(E,I)),I}function T(v){if(--v.usedTimes===0){let E=c.indexOf(v);c[E]=c[c.length-1],c.pop(),h.delete(v.cacheKey),v.destroy()}}function w(v){o.remove(v)}function R(){o.dispose()}return{getParameters:x,getProgramCacheKey:m,getUniforms:S,acquireProgram:b,releaseProgram:T,releaseShaderCache:w,programs:c,dispose:R}}function Ev(){let i=new WeakMap;function t(a){return i.has(a)}function e(a){let o=i.get(a);return o===void 0&&(o={},i.set(a,o)),o}function n(a){i.delete(a)}function s(a,o,l){i.get(a)[o]=l}function r(){i=new WeakMap}return{has:t,get:e,remove:n,update:s,dispose:r}}function Cv(i,t){return i.groupOrder!==t.groupOrder?i.groupOrder-t.groupOrder:i.renderOrder!==t.renderOrder?i.renderOrder-t.renderOrder:i.material.id!==t.material.id?i.material.id-t.material.id:i.materialVariant!==t.materialVariant?i.materialVariant-t.materialVariant:i.z!==t.z?i.z-t.z:i.id-t.id}function Uf(i,t){return i.groupOrder!==t.groupOrder?i.groupOrder-t.groupOrder:i.renderOrder!==t.renderOrder?i.renderOrder-t.renderOrder:i.z!==t.z?t.z-i.z:i.id-t.id}function Of(){let i=[],t=0,e=[],n=[],s=[];function r(){t=0,e.length=0,n.length=0,s.length=0}function a(u){let p=0;return u.isInstancedMesh&&(p+=2),u.isSkinnedMesh&&(p+=1),p}function o(u,p,g,x,m,d){let y=i[t];return y===void 0?(y={id:u.id,object:u,geometry:p,material:g,materialVariant:a(u),groupOrder:x,renderOrder:u.renderOrder,z:m,group:d},i[t]=y):(y.id=u.id,y.object=u,y.geometry=p,y.material=g,y.materialVariant=a(u),y.groupOrder=x,y.renderOrder=u.renderOrder,y.z=m,y.group=d),t++,y}function l(u,p,g,x,m,d){let y=o(u,p,g,x,m,d);g.transmission>0?n.push(y):g.transparent===!0?s.push(y):e.push(y)}function c(u,p,g,x,m,d){let y=o(u,p,g,x,m,d);g.transmission>0?n.unshift(y):g.transparent===!0?s.unshift(y):e.unshift(y)}function h(u,p){e.length>1&&e.sort(u||Cv),n.length>1&&n.sort(p||Uf),s.length>1&&s.sort(p||Uf)}function f(){for(let u=t,p=i.length;u<p;u++){let g=i[u];if(g.id===null)break;g.id=null,g.object=null,g.geometry=null,g.material=null,g.group=null}}return{opaque:e,transmissive:n,transparent:s,init:r,push:l,unshift:c,finish:f,sort:h}}function Rv(){let i=new WeakMap;function t(n,s){let r=i.get(n),a;return r===void 0?(a=new Of,i.set(n,[a])):s>=r.length?(a=new Of,r.push(a)):a=r[s],a}function e(){i=new WeakMap}return{get:t,dispose:e}}function Pv(){let i={};return{get:function(t){if(i[t.id]!==void 0)return i[t.id];let e;switch(t.type){case"DirectionalLight":e={direction:new D,color:new ut};break;case"SpotLight":e={position:new D,direction:new D,color:new ut,distance:0,coneCos:0,penumbraCos:0,decay:0};break;case"PointLight":e={position:new D,color:new ut,distance:0,decay:0};break;case"HemisphereLight":e={direction:new D,skyColor:new ut,groundColor:new ut};break;case"RectAreaLight":e={color:new ut,position:new D,halfWidth:new D,halfHeight:new D};break}return i[t.id]=e,e}}}function Iv(){let i={};return{get:function(t){if(i[t.id]!==void 0)return i[t.id];let e;switch(t.type){case"DirectionalLight":e={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ut};break;case"SpotLight":e={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ut};break;case"PointLight":e={shadowIntensity:1,shadowBias:0,shadowNormalBias:0,shadowRadius:1,shadowMapSize:new Ut,shadowCameraNear:1,shadowCameraFar:1e3};break}return i[t.id]=e,e}}}var Lv=0;function Nv(i,t){return(t.castShadow?2:0)-(i.castShadow?2:0)+(t.map?1:0)-(i.map?1:0)}function Dv(i){let t=new Pv,e=Iv(),n={version:0,hash:{directionalLength:-1,pointLength:-1,spotLength:-1,rectAreaLength:-1,hemiLength:-1,numDirectionalShadows:-1,numPointShadows:-1,numSpotShadows:-1,numSpotMaps:-1,numLightProbes:-1},ambient:[0,0,0],probe:[],directional:[],directionalShadow:[],directionalShadowMap:[],directionalShadowMatrix:[],spot:[],spotLightMap:[],spotShadow:[],spotShadowMap:[],spotLightMatrix:[],rectArea:[],rectAreaLTC1:null,rectAreaLTC2:null,point:[],pointShadow:[],pointShadowMap:[],pointShadowMatrix:[],hemi:[],numSpotLightShadowsWithMaps:0,numLightProbes:0};for(let c=0;c<9;c++)n.probe.push(new D);let s=new D,r=new ve,a=new ve;function o(c){let h=0,f=0,u=0;for(let E=0;E<9;E++)n.probe[E].set(0,0,0);let p=0,g=0,x=0,m=0,d=0,y=0,S=0,b=0,T=0,w=0,R=0;c.sort(Nv);for(let E=0,I=c.length;E<I;E++){let C=c[E],N=C.color,H=C.intensity,W=C.distance,U=null;if(C.shadow&&C.shadow.map&&(C.shadow.map.texture.format===Li?U=C.shadow.map.texture:U=C.shadow.map.depthTexture||C.shadow.map.texture),C.isAmbientLight)h+=N.r*H,f+=N.g*H,u+=N.b*H;else if(C.isLightProbe){for(let z=0;z<9;z++)n.probe[z].addScaledVector(C.sh.coefficients[z],H);R++}else if(C.isDirectionalLight){let z=t.get(C);if(z.color.copy(C.color).multiplyScalar(C.intensity),C.castShadow){let V=C.shadow,$=e.get(C);$.shadowIntensity=V.intensity,$.shadowBias=V.bias,$.shadowNormalBias=V.normalBias,$.shadowRadius=V.radius,$.shadowMapSize=V.mapSize,n.directionalShadow[p]=$,n.directionalShadowMap[p]=U,n.directionalShadowMatrix[p]=C.shadow.matrix,y++}n.directional[p]=z,p++}else if(C.isSpotLight){let z=t.get(C);z.position.setFromMatrixPosition(C.matrixWorld),z.color.copy(N).multiplyScalar(H),z.distance=W,z.coneCos=Math.cos(C.angle),z.penumbraCos=Math.cos(C.angle*(1-C.penumbra)),z.decay=C.decay,n.spot[x]=z;let V=C.shadow;if(C.map&&(n.spotLightMap[T]=C.map,T++,V.updateMatrices(C),C.castShadow&&w++),n.spotLightMatrix[x]=V.matrix,C.castShadow){let $=e.get(C);$.shadowIntensity=V.intensity,$.shadowBias=V.bias,$.shadowNormalBias=V.normalBias,$.shadowRadius=V.radius,$.shadowMapSize=V.mapSize,n.spotShadow[x]=$,n.spotShadowMap[x]=U,b++}x++}else if(C.isRectAreaLight){let z=t.get(C);z.color.copy(N).multiplyScalar(H),z.halfWidth.set(C.width*.5,0,0),z.halfHeight.set(0,C.height*.5,0),n.rectArea[m]=z,m++}else if(C.isPointLight){let z=t.get(C);if(z.color.copy(C.color).multiplyScalar(C.intensity),z.distance=C.distance,z.decay=C.decay,C.castShadow){let V=C.shadow,$=e.get(C);$.shadowIntensity=V.intensity,$.shadowBias=V.bias,$.shadowNormalBias=V.normalBias,$.shadowRadius=V.radius,$.shadowMapSize=V.mapSize,$.shadowCameraNear=V.camera.near,$.shadowCameraFar=V.camera.far,n.pointShadow[g]=$,n.pointShadowMap[g]=U,n.pointShadowMatrix[g]=C.shadow.matrix,S++}n.point[g]=z,g++}else if(C.isHemisphereLight){let z=t.get(C);z.skyColor.copy(C.color).multiplyScalar(H),z.groundColor.copy(C.groundColor).multiplyScalar(H),n.hemi[d]=z,d++}}m>0&&(i.has("OES_texture_float_linear")===!0?(n.rectAreaLTC1=ft.LTC_FLOAT_1,n.rectAreaLTC2=ft.LTC_FLOAT_2):(n.rectAreaLTC1=ft.LTC_HALF_1,n.rectAreaLTC2=ft.LTC_HALF_2)),n.ambient[0]=h,n.ambient[1]=f,n.ambient[2]=u;let v=n.hash;(v.directionalLength!==p||v.pointLength!==g||v.spotLength!==x||v.rectAreaLength!==m||v.hemiLength!==d||v.numDirectionalShadows!==y||v.numPointShadows!==S||v.numSpotShadows!==b||v.numSpotMaps!==T||v.numLightProbes!==R)&&(n.directional.length=p,n.spot.length=x,n.rectArea.length=m,n.point.length=g,n.hemi.length=d,n.directionalShadow.length=y,n.directionalShadowMap.length=y,n.pointShadow.length=S,n.pointShadowMap.length=S,n.spotShadow.length=b,n.spotShadowMap.length=b,n.directionalShadowMatrix.length=y,n.pointShadowMatrix.length=S,n.spotLightMatrix.length=b+T-w,n.spotLightMap.length=T,n.numSpotLightShadowsWithMaps=w,n.numLightProbes=R,v.directionalLength=p,v.pointLength=g,v.spotLength=x,v.rectAreaLength=m,v.hemiLength=d,v.numDirectionalShadows=y,v.numPointShadows=S,v.numSpotShadows=b,v.numSpotMaps=T,v.numLightProbes=R,n.version=Lv++)}function l(c,h){let f=0,u=0,p=0,g=0,x=0,m=h.matrixWorldInverse;for(let d=0,y=c.length;d<y;d++){let S=c[d];if(S.isDirectionalLight){let b=n.directional[f];b.direction.setFromMatrixPosition(S.matrixWorld),s.setFromMatrixPosition(S.target.matrixWorld),b.direction.sub(s),b.direction.transformDirection(m),f++}else if(S.isSpotLight){let b=n.spot[p];b.position.setFromMatrixPosition(S.matrixWorld),b.position.applyMatrix4(m),b.direction.setFromMatrixPosition(S.matrixWorld),s.setFromMatrixPosition(S.target.matrixWorld),b.direction.sub(s),b.direction.transformDirection(m),p++}else if(S.isRectAreaLight){let b=n.rectArea[g];b.position.setFromMatrixPosition(S.matrixWorld),b.position.applyMatrix4(m),a.identity(),r.copy(S.matrixWorld),r.premultiply(m),a.extractRotation(r),b.halfWidth.set(S.width*.5,0,0),b.halfHeight.set(0,S.height*.5,0),b.halfWidth.applyMatrix4(a),b.halfHeight.applyMatrix4(a),g++}else if(S.isPointLight){let b=n.point[u];b.position.setFromMatrixPosition(S.matrixWorld),b.position.applyMatrix4(m),u++}else if(S.isHemisphereLight){let b=n.hemi[x];b.direction.setFromMatrixPosition(S.matrixWorld),b.direction.transformDirection(m),x++}}}return{setup:o,setupView:l,state:n}}function Bf(i){let t=new Dv(i),e=[],n=[],s=[];function r(u){f.camera=u,e.length=0,n.length=0,s.length=0}function a(u){e.push(u)}function o(u){n.push(u)}function l(u){s.push(u)}function c(){t.setup(e)}function h(u){t.setupView(e,u)}let f={lightsArray:e,shadowsArray:n,lightProbeGridArray:s,camera:null,lights:t,transmissionRenderTarget:{},textureUnits:0};return{init:r,state:f,setupLights:c,setupLightsView:h,pushLight:a,pushShadow:o,pushLightProbeGrid:l}}function Fv(i){let t=new WeakMap;function e(s,r=0){let a=t.get(s),o;return a===void 0?(o=new Bf(i),t.set(s,[o])):r>=a.length?(o=new Bf(i),a.push(o)):o=a[r],o}function n(){t=new WeakMap}return{get:e,dispose:n}}var Uv=`void main() {
	gl_Position = vec4( position, 1.0 );
}`,Ov=`uniform sampler2D shadow_pass;
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
}`,Bv=[new D(1,0,0),new D(-1,0,0),new D(0,1,0),new D(0,-1,0),new D(0,0,1),new D(0,0,-1)],kv=[new D(0,-1,0),new D(0,-1,0),new D(0,0,1),new D(0,0,-1),new D(0,-1,0),new D(0,-1,0)],kf=new ve,Nr=new D,eh=new D;function zv(i,t,e){let n=new lr,s=new Ut,r=new Ut,a=new ye,o=new ja,l=new Qa,c={},h=e.maxTextureSize,f={[ei]:$e,[$e]:ei,[zn]:zn},u=new se({defines:{VSM_SAMPLES:8},uniforms:{shadow_pass:{value:null},resolution:{value:new Ut},radius:{value:4}},vertexShader:Uv,fragmentShader:Ov}),p=u.clone();p.defines.HORIZONTAL_PASS=1;let g=new Qt;g.setAttribute("position",new Lt(new Float32Array([-1,-1,.5,3,-1,.5,-1,3,.5]),3));let x=new rn(g,u),m=this;this.enabled=!1,this.autoUpdate=!0,this.needsUpdate=!1,this.type=gr;let d=this.type;this.render=function(w,R,v){if(m.enabled===!1||m.autoUpdate===!1&&m.needsUpdate===!1||w.length===0)return;this.type===Fu&&(Et("WebGLShadowMap: PCFSoftShadowMap has been deprecated. Using PCFShadowMap instead."),this.type=gr);let E=i.getRenderTarget(),I=i.getActiveCubeFace(),C=i.getActiveMipmapLevel(),N=i.state;N.setBlending(vn),N.buffers.depth.getReversed()===!0?N.buffers.color.setClear(0,0,0,0):N.buffers.color.setClear(1,1,1,1),N.buffers.depth.setTest(!0),N.setScissorTest(!1);let H=d!==this.type;H&&R.traverse(function(W){W.material&&(Array.isArray(W.material)?W.material.forEach(U=>U.needsUpdate=!0):W.material.needsUpdate=!0)});for(let W=0,U=w.length;W<U;W++){let z=w[W],V=z.shadow;if(V===void 0){Et("WebGLShadowMap:",z,"has no shadow.");continue}if(V.autoUpdate===!1&&V.needsUpdate===!1)continue;s.copy(V.mapSize);let $=V.getFrameExtents();s.multiply($),r.copy(V.mapSize),(s.x>h||s.y>h)&&(s.x>h&&(r.x=Math.floor(h/$.x),s.x=r.x*$.x,V.mapSize.x=r.x),s.y>h&&(r.y=Math.floor(h/$.y),s.y=r.y*$.y,V.mapSize.y=r.y));let tt=i.state.buffers.depth.getReversed();if(V.camera._reversedDepth=tt,V.map===null||H===!0){if(V.map!==null&&(V.map.depthTexture!==null&&(V.map.depthTexture.dispose(),V.map.depthTexture=null),V.map.dispose()),this.type===Ns){if(z.isPointLight){Et("WebGLShadowMap: VSM shadow maps are not supported for PointLights. Use PCF or BasicShadowMap instead.");continue}V.map=new Le(s.x,s.y,{format:Li,type:qe,minFilter:ze,magFilter:ze,generateMipmaps:!1}),V.map.texture.name=z.name+".shadowMap",V.map.depthTexture=new ri(s.x,s.y,Cn),V.map.depthTexture.name=z.name+".shadowMapDepth",V.map.depthTexture.format=Bn,V.map.depthTexture.compareFunction=null,V.map.depthTexture.minFilter=Oe,V.map.depthTexture.magFilter=Oe}else z.isPointLight?(V.map=new rl(s.x),V.map.depthTexture=new Ka(s.x,En)):(V.map=new Le(s.x,s.y),V.map.depthTexture=new ri(s.x,s.y,En)),V.map.depthTexture.name=z.name+".shadowMap",V.map.depthTexture.format=Bn,this.type===gr?(V.map.depthTexture.compareFunction=tt?el:tl,V.map.depthTexture.minFilter=ze,V.map.depthTexture.magFilter=ze):(V.map.depthTexture.compareFunction=null,V.map.depthTexture.minFilter=Oe,V.map.depthTexture.magFilter=Oe);V.camera.updateProjectionMatrix()}let ct=V.map.isWebGLCubeRenderTarget?6:1;for(let Mt=0;Mt<ct;Mt++){if(V.map.isWebGLCubeRenderTarget)i.setRenderTarget(V.map,Mt),i.clear();else{Mt===0&&(i.setRenderTarget(V.map),i.clear());let St=V.getViewport(Mt);a.set(r.x*St.x,r.y*St.y,r.x*St.z,r.y*St.w),N.viewport(a)}if(z.isPointLight){let St=V.camera,Xt=V.matrix,te=z.distance||St.far;te!==St.far&&(St.far=te,St.updateProjectionMatrix()),Nr.setFromMatrixPosition(z.matrixWorld),St.position.copy(Nr),eh.copy(St.position),eh.add(Bv[Mt]),St.up.copy(kv[Mt]),St.lookAt(eh),St.updateMatrixWorld(),Xt.makeTranslation(-Nr.x,-Nr.y,-Nr.z),kf.multiplyMatrices(St.projectionMatrix,St.matrixWorldInverse),V._frustum.setFromProjectionMatrix(kf,St.coordinateSystem,St.reversedDepth)}else V.updateMatrices(z);n=V.getFrustum(),b(R,v,V.camera,z,this.type)}V.isPointLightShadow!==!0&&this.type===Ns&&y(V,v),V.needsUpdate=!1}d=this.type,m.needsUpdate=!1,i.setRenderTarget(E,I,C)};function y(w,R){let v=t.update(x);u.defines.VSM_SAMPLES!==w.blurSamples&&(u.defines.VSM_SAMPLES=w.blurSamples,p.defines.VSM_SAMPLES=w.blurSamples,u.needsUpdate=!0,p.needsUpdate=!0),w.mapPass===null&&(w.mapPass=new Le(s.x,s.y,{format:Li,type:qe})),u.uniforms.shadow_pass.value=w.map.depthTexture,u.uniforms.resolution.value=w.mapSize,u.uniforms.radius.value=w.radius,i.setRenderTarget(w.mapPass),i.clear(),i.renderBufferDirect(R,null,v,u,x,null),p.uniforms.shadow_pass.value=w.mapPass.texture,p.uniforms.resolution.value=w.mapSize,p.uniforms.radius.value=w.radius,i.setRenderTarget(w.map),i.clear(),i.renderBufferDirect(R,null,v,p,x,null)}function S(w,R,v,E){let I=null,C=v.isPointLight===!0?w.customDistanceMaterial:w.customDepthMaterial;if(C!==void 0)I=C;else if(I=v.isPointLight===!0?l:o,i.localClippingEnabled&&R.clipShadows===!0&&Array.isArray(R.clippingPlanes)&&R.clippingPlanes.length!==0||R.displacementMap&&R.displacementScale!==0||R.alphaMap&&R.alphaTest>0||R.map&&R.alphaTest>0||R.alphaToCoverage===!0){let N=I.uuid,H=R.uuid,W=c[N];W===void 0&&(W={},c[N]=W);let U=W[H];U===void 0&&(U=I.clone(),W[H]=U,R.addEventListener("dispose",T)),I=U}if(I.visible=R.visible,I.wireframe=R.wireframe,E===Ns?I.side=R.shadowSide!==null?R.shadowSide:R.side:I.side=R.shadowSide!==null?R.shadowSide:f[R.side],I.alphaMap=R.alphaMap,I.alphaTest=R.alphaToCoverage===!0?.5:R.alphaTest,I.map=R.map,I.clipShadows=R.clipShadows,I.clippingPlanes=R.clippingPlanes,I.clipIntersection=R.clipIntersection,I.displacementMap=R.displacementMap,I.displacementScale=R.displacementScale,I.displacementBias=R.displacementBias,I.wireframeLinewidth=R.wireframeLinewidth,I.linewidth=R.linewidth,v.isPointLight===!0&&I.isMeshDistanceMaterial===!0){let N=i.properties.get(I);N.light=v}return I}function b(w,R,v,E,I){if(w.visible===!1)return;if(w.layers.test(R.layers)&&(w.isMesh||w.isLine||w.isPoints)&&(w.castShadow||w.receiveShadow&&I===Ns)&&(!w.frustumCulled||n.intersectsObject(w))){w.modelViewMatrix.multiplyMatrices(v.matrixWorldInverse,w.matrixWorld);let H=t.update(w),W=w.material;if(Array.isArray(W)){let U=H.groups;for(let z=0,V=U.length;z<V;z++){let $=U[z],tt=W[$.materialIndex];if(tt&&tt.visible){let ct=S(w,tt,E,I);w.onBeforeShadow(i,w,R,v,H,ct,$),i.renderBufferDirect(v,null,H,ct,w,$),w.onAfterShadow(i,w,R,v,H,ct,$)}}}else if(W.visible){let U=S(w,W,E,I);w.onBeforeShadow(i,w,R,v,H,U,null),i.renderBufferDirect(v,null,H,U,w,null),w.onAfterShadow(i,w,R,v,H,U,null)}}let N=w.children;for(let H=0,W=N.length;H<W;H++)b(N[H],R,v,E,I)}function T(w){w.target.removeEventListener("dispose",T);for(let v in c){let E=c[v],I=w.target.uuid;I in E&&(E[I].dispose(),delete E[I])}}}function Vv(i,t){function e(){let P=!1,it=new ye,q=null,_t=new ye(0,0,0,0);return{setMask:function(ot){q!==ot&&!P&&(i.colorMask(ot,ot,ot,ot),q=ot)},setLocked:function(ot){P=ot},setClear:function(ot,K,wt,Ot,Se){Se===!0&&(ot*=Ot,K*=Ot,wt*=Ot),it.set(ot,K,wt,Ot),_t.equals(it)===!1&&(i.clearColor(ot,K,wt,Ot),_t.copy(it))},reset:function(){P=!1,q=null,_t.set(-1,0,0,0)}}}function n(){let P=!1,it=!1,q=null,_t=null,ot=null;return{setReversed:function(K){if(it!==K){let wt=t.get("EXT_clip_control");K?wt.clipControlEXT(wt.LOWER_LEFT_EXT,wt.ZERO_TO_ONE_EXT):wt.clipControlEXT(wt.LOWER_LEFT_EXT,wt.NEGATIVE_ONE_TO_ONE_EXT),it=K;let Ot=ot;ot=null,this.setClear(Ot)}},getReversed:function(){return it},setTest:function(K){K?rt(i.DEPTH_TEST):Ct(i.DEPTH_TEST)},setMask:function(K){q!==K&&!P&&(i.depthMask(K),q=K)},setFunc:function(K){if(it&&(K=mf[K]),_t!==K){switch(K){case La:i.depthFunc(i.NEVER);break;case Na:i.depthFunc(i.ALWAYS);break;case Da:i.depthFunc(i.LESS);break;case ts:i.depthFunc(i.LEQUAL);break;case Fa:i.depthFunc(i.EQUAL);break;case Ua:i.depthFunc(i.GEQUAL);break;case Oa:i.depthFunc(i.GREATER);break;case Ba:i.depthFunc(i.NOTEQUAL);break;default:i.depthFunc(i.LEQUAL)}_t=K}},setLocked:function(K){P=K},setClear:function(K){ot!==K&&(ot=K,it&&(K=1-K),i.clearDepth(K))},reset:function(){P=!1,q=null,_t=null,ot=null,it=!1}}}function s(){let P=!1,it=null,q=null,_t=null,ot=null,K=null,wt=null,Ot=null,Se=null;return{setTest:function(ne){P||(ne?rt(i.STENCIL_TEST):Ct(i.STENCIL_TEST))},setMask:function(ne){it!==ne&&!P&&(i.stencilMask(ne),it=ne)},setFunc:function(ne,Yn,Ln){(q!==ne||_t!==Yn||ot!==Ln)&&(i.stencilFunc(ne,Yn,Ln),q=ne,_t=Yn,ot=Ln)},setOp:function(ne,Yn,Ln){(K!==ne||wt!==Yn||Ot!==Ln)&&(i.stencilOp(ne,Yn,Ln),K=ne,wt=Yn,Ot=Ln)},setLocked:function(ne){P=ne},setClear:function(ne){Se!==ne&&(i.clearStencil(ne),Se=ne)},reset:function(){P=!1,it=null,q=null,_t=null,ot=null,K=null,wt=null,Ot=null,Se=null}}}let r=new e,a=new n,o=new s,l=new WeakMap,c=new WeakMap,h={},f={},u={},p=new WeakMap,g=[],x=null,m=!1,d=null,y=null,S=null,b=null,T=null,w=null,R=null,v=new ut(0,0,0),E=0,I=!1,C=null,N=null,H=null,W=null,U=null,z=i.getParameter(i.MAX_COMBINED_TEXTURE_IMAGE_UNITS),V=!1,$=0,tt=i.getParameter(i.VERSION);tt.indexOf("WebGL")!==-1?($=parseFloat(/^WebGL (\d)/.exec(tt)[1]),V=$>=1):tt.indexOf("OpenGL ES")!==-1&&($=parseFloat(/^OpenGL ES (\d)/.exec(tt)[1]),V=$>=2);let ct=null,Mt={},St=i.getParameter(i.SCISSOR_BOX),Xt=i.getParameter(i.VIEWPORT),te=new ye().fromArray(St),kt=new ye().fromArray(Xt);function J(P,it,q,_t){let ot=new Uint8Array(4),K=i.createTexture();i.bindTexture(P,K),i.texParameteri(P,i.TEXTURE_MIN_FILTER,i.NEAREST),i.texParameteri(P,i.TEXTURE_MAG_FILTER,i.NEAREST);for(let wt=0;wt<q;wt++)P===i.TEXTURE_3D||P===i.TEXTURE_2D_ARRAY?i.texImage3D(it,0,i.RGBA,1,1,_t,0,i.RGBA,i.UNSIGNED_BYTE,ot):i.texImage2D(it+wt,0,i.RGBA,1,1,0,i.RGBA,i.UNSIGNED_BYTE,ot);return K}let mt={};mt[i.TEXTURE_2D]=J(i.TEXTURE_2D,i.TEXTURE_2D,1),mt[i.TEXTURE_CUBE_MAP]=J(i.TEXTURE_CUBE_MAP,i.TEXTURE_CUBE_MAP_POSITIVE_X,6),mt[i.TEXTURE_2D_ARRAY]=J(i.TEXTURE_2D_ARRAY,i.TEXTURE_2D_ARRAY,1,1),mt[i.TEXTURE_3D]=J(i.TEXTURE_3D,i.TEXTURE_3D,1,1),r.setClear(0,0,0,1),a.setClear(1),o.setClear(0),rt(i.DEPTH_TEST),a.setFunc(ts),Pe(!1),me(Tc),rt(i.CULL_FACE),ue(vn);function rt(P){h[P]!==!0&&(i.enable(P),h[P]=!0)}function Ct(P){h[P]!==!1&&(i.disable(P),h[P]=!1)}function Ft(P,it){return u[P]!==it?(i.bindFramebuffer(P,it),u[P]=it,P===i.DRAW_FRAMEBUFFER&&(u[i.FRAMEBUFFER]=it),P===i.FRAMEBUFFER&&(u[i.DRAW_FRAMEBUFFER]=it),!0):!1}function Pt(P,it){let q=g,_t=!1;if(P){q=p.get(it),q===void 0&&(q=[],p.set(it,q));let ot=P.textures;if(q.length!==ot.length||q[0]!==i.COLOR_ATTACHMENT0){for(let K=0,wt=ot.length;K<wt;K++)q[K]=i.COLOR_ATTACHMENT0+K;q.length=ot.length,_t=!0}}else q[0]!==i.BACK&&(q[0]=i.BACK,_t=!0);_t&&i.drawBuffers(q)}function pe(P){return x!==P?(i.useProgram(P),x=P,!0):!1}let qt={[Mi]:i.FUNC_ADD,[Ou]:i.FUNC_SUBTRACT,[Bu]:i.FUNC_REVERSE_SUBTRACT};qt[ku]=i.MIN,qt[zu]=i.MAX;let ee={[Vu]:i.ZERO,[Gu]:i.ONE,[Hu]:i.SRC_COLOR,[Pa]:i.SRC_ALPHA,[Ju]:i.SRC_ALPHA_SATURATE,[Yu]:i.DST_COLOR,[Xu]:i.DST_ALPHA,[Wu]:i.ONE_MINUS_SRC_COLOR,[Ia]:i.ONE_MINUS_SRC_ALPHA,[Zu]:i.ONE_MINUS_DST_COLOR,[qu]:i.ONE_MINUS_DST_ALPHA,[$u]:i.CONSTANT_COLOR,[Ku]:i.ONE_MINUS_CONSTANT_COLOR,[ju]:i.CONSTANT_ALPHA,[Qu]:i.ONE_MINUS_CONSTANT_ALPHA};function ue(P,it,q,_t,ot,K,wt,Ot,Se,ne){if(P===vn){m===!0&&(Ct(i.BLEND),m=!1);return}if(m===!1&&(rt(i.BLEND),m=!0),P!==Uu){if(P!==d||ne!==I){if((y!==Mi||T!==Mi)&&(i.blendEquation(i.FUNC_ADD),y=Mi,T=Mi),ne)switch(P){case On:i.blendFuncSeparate(i.ONE,i.ONE_MINUS_SRC_ALPHA,i.ONE,i.ONE_MINUS_SRC_ALPHA);break;case Tn:i.blendFunc(i.ONE,i.ONE);break;case Ec:i.blendFuncSeparate(i.ZERO,i.ONE_MINUS_SRC_COLOR,i.ZERO,i.ONE);break;case Cc:i.blendFuncSeparate(i.DST_COLOR,i.ONE_MINUS_SRC_ALPHA,i.ZERO,i.ONE);break;default:Rt("WebGLState: Invalid blending: ",P);break}else switch(P){case On:i.blendFuncSeparate(i.SRC_ALPHA,i.ONE_MINUS_SRC_ALPHA,i.ONE,i.ONE_MINUS_SRC_ALPHA);break;case Tn:i.blendFuncSeparate(i.SRC_ALPHA,i.ONE,i.ONE,i.ONE);break;case Ec:Rt("WebGLState: SubtractiveBlending requires material.premultipliedAlpha = true");break;case Cc:Rt("WebGLState: MultiplyBlending requires material.premultipliedAlpha = true");break;default:Rt("WebGLState: Invalid blending: ",P);break}S=null,b=null,w=null,R=null,v.set(0,0,0),E=0,d=P,I=ne}return}ot=ot||it,K=K||q,wt=wt||_t,(it!==y||ot!==T)&&(i.blendEquationSeparate(qt[it],qt[ot]),y=it,T=ot),(q!==S||_t!==b||K!==w||wt!==R)&&(i.blendFuncSeparate(ee[q],ee[_t],ee[K],ee[wt]),S=q,b=_t,w=K,R=wt),(Ot.equals(v)===!1||Se!==E)&&(i.blendColor(Ot.r,Ot.g,Ot.b,Se),v.copy(Ot),E=Se),d=P,I=!1}function Wt(P,it){P.side===zn?Ct(i.CULL_FACE):rt(i.CULL_FACE);let q=P.side===$e;it&&(q=!q),Pe(q),P.blending===On&&P.transparent===!1?ue(vn):ue(P.blending,P.blendEquation,P.blendSrc,P.blendDst,P.blendEquationAlpha,P.blendSrcAlpha,P.blendDstAlpha,P.blendColor,P.blendAlpha,P.premultipliedAlpha),a.setFunc(P.depthFunc),a.setTest(P.depthTest),a.setMask(P.depthWrite),r.setMask(P.colorWrite);let _t=P.stencilWrite;o.setTest(_t),_t&&(o.setMask(P.stencilWriteMask),o.setFunc(P.stencilFunc,P.stencilRef,P.stencilFuncMask),o.setOp(P.stencilFail,P.stencilZFail,P.stencilZPass)),L(P.polygonOffset,P.polygonOffsetFactor,P.polygonOffsetUnits),P.alphaToCoverage===!0?rt(i.SAMPLE_ALPHA_TO_COVERAGE):Ct(i.SAMPLE_ALPHA_TO_COVERAGE)}function Pe(P){C!==P&&(P?i.frontFace(i.CW):i.frontFace(i.CCW),C=P)}function me(P){P!==Nu?(rt(i.CULL_FACE),P!==N&&(P===Tc?i.cullFace(i.BACK):P===Du?i.cullFace(i.FRONT):i.cullFace(i.FRONT_AND_BACK))):Ct(i.CULL_FACE),N=P}function ln(P){P!==H&&(V&&i.lineWidth(P),H=P)}function L(P,it,q){P?(rt(i.POLYGON_OFFSET_FILL),(W!==it||U!==q)&&(W=it,U=q,a.getReversed()&&(it=-it),i.polygonOffset(it,q))):Ct(i.POLYGON_OFFSET_FILL)}function Ie(P){P?rt(i.SCISSOR_TEST):Ct(i.SCISSOR_TEST)}function Yt(P){P===void 0&&(P=i.TEXTURE0+z-1),ct!==P&&(i.activeTexture(P),ct=P)}function ce(P,it,q){q===void 0&&(ct===null?q=i.TEXTURE0+z-1:q=ct);let _t=Mt[q];_t===void 0&&(_t={type:void 0,texture:void 0},Mt[q]=_t),(_t.type!==P||_t.texture!==it)&&(ct!==q&&(i.activeTexture(q),ct=q),i.bindTexture(P,it||mt[P]),_t.type=P,_t.texture=it)}function ht(){let P=Mt[ct];P!==void 0&&P.type!==void 0&&(i.bindTexture(P.type,null),P.type=void 0,P.texture=void 0)}function _e(){try{i.compressedTexImage2D(...arguments)}catch(P){Rt("WebGLState:",P)}}function A(){try{i.compressedTexImage3D(...arguments)}catch(P){Rt("WebGLState:",P)}}function _(){try{i.texSubImage2D(...arguments)}catch(P){Rt("WebGLState:",P)}}function O(){try{i.texSubImage3D(...arguments)}catch(P){Rt("WebGLState:",P)}}function Y(){try{i.compressedTexSubImage2D(...arguments)}catch(P){Rt("WebGLState:",P)}}function j(){try{i.compressedTexSubImage3D(...arguments)}catch(P){Rt("WebGLState:",P)}}function et(){try{i.texStorage2D(...arguments)}catch(P){Rt("WebGLState:",P)}}function lt(){try{i.texStorage3D(...arguments)}catch(P){Rt("WebGLState:",P)}}function X(){try{i.texImage2D(...arguments)}catch(P){Rt("WebGLState:",P)}}function Z(){try{i.texImage3D(...arguments)}catch(P){Rt("WebGLState:",P)}}function gt(P){return f[P]!==void 0?f[P]:i.getParameter(P)}function vt(P,it){f[P]!==it&&(i.pixelStorei(P,it),f[P]=it)}function at(P){te.equals(P)===!1&&(i.scissor(P.x,P.y,P.z,P.w),te.copy(P))}function nt(P){kt.equals(P)===!1&&(i.viewport(P.x,P.y,P.z,P.w),kt.copy(P))}function Nt(P,it){let q=c.get(it);q===void 0&&(q=new WeakMap,c.set(it,q));let _t=q.get(P);_t===void 0&&(_t=i.getUniformBlockIndex(it,P.name),q.set(P,_t))}function zt(P,it){let _t=c.get(it).get(P);l.get(it)!==_t&&(i.uniformBlockBinding(it,_t,P.__bindingPointIndex),l.set(it,_t))}function $t(){i.disable(i.BLEND),i.disable(i.CULL_FACE),i.disable(i.DEPTH_TEST),i.disable(i.POLYGON_OFFSET_FILL),i.disable(i.SCISSOR_TEST),i.disable(i.STENCIL_TEST),i.disable(i.SAMPLE_ALPHA_TO_COVERAGE),i.blendEquation(i.FUNC_ADD),i.blendFunc(i.ONE,i.ZERO),i.blendFuncSeparate(i.ONE,i.ZERO,i.ONE,i.ZERO),i.blendColor(0,0,0,0),i.colorMask(!0,!0,!0,!0),i.clearColor(0,0,0,0),i.depthMask(!0),i.depthFunc(i.LESS),a.setReversed(!1),i.clearDepth(1),i.stencilMask(4294967295),i.stencilFunc(i.ALWAYS,0,4294967295),i.stencilOp(i.KEEP,i.KEEP,i.KEEP),i.clearStencil(0),i.cullFace(i.BACK),i.frontFace(i.CCW),i.polygonOffset(0,0),i.activeTexture(i.TEXTURE0),i.bindFramebuffer(i.FRAMEBUFFER,null),i.bindFramebuffer(i.DRAW_FRAMEBUFFER,null),i.bindFramebuffer(i.READ_FRAMEBUFFER,null),i.useProgram(null),i.lineWidth(1),i.scissor(0,0,i.canvas.width,i.canvas.height),i.viewport(0,0,i.canvas.width,i.canvas.height),i.pixelStorei(i.PACK_ALIGNMENT,4),i.pixelStorei(i.UNPACK_ALIGNMENT,4),i.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,!1),i.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,!1),i.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,i.BROWSER_DEFAULT_WEBGL),i.pixelStorei(i.PACK_ROW_LENGTH,0),i.pixelStorei(i.PACK_SKIP_PIXELS,0),i.pixelStorei(i.PACK_SKIP_ROWS,0),i.pixelStorei(i.UNPACK_ROW_LENGTH,0),i.pixelStorei(i.UNPACK_IMAGE_HEIGHT,0),i.pixelStorei(i.UNPACK_SKIP_PIXELS,0),i.pixelStorei(i.UNPACK_SKIP_ROWS,0),i.pixelStorei(i.UNPACK_SKIP_IMAGES,0),h={},f={},ct=null,Mt={},u={},p=new WeakMap,g=[],x=null,m=!1,d=null,y=null,S=null,b=null,T=null,w=null,R=null,v=new ut(0,0,0),E=0,I=!1,C=null,N=null,H=null,W=null,U=null,te.set(0,0,i.canvas.width,i.canvas.height),kt.set(0,0,i.canvas.width,i.canvas.height),r.reset(),a.reset(),o.reset()}return{buffers:{color:r,depth:a,stencil:o},enable:rt,disable:Ct,bindFramebuffer:Ft,drawBuffers:Pt,useProgram:pe,setBlending:ue,setMaterial:Wt,setFlipSided:Pe,setCullFace:me,setLineWidth:ln,setPolygonOffset:L,setScissorTest:Ie,activeTexture:Yt,bindTexture:ce,unbindTexture:ht,compressedTexImage2D:_e,compressedTexImage3D:A,texImage2D:X,texImage3D:Z,pixelStorei:vt,getParameter:gt,updateUBOMapping:Nt,uniformBlockBinding:zt,texStorage2D:et,texStorage3D:lt,texSubImage2D:_,texSubImage3D:O,compressedTexSubImage2D:Y,compressedTexSubImage3D:j,scissor:at,viewport:nt,reset:$t}}function Gv(i,t,e,n,s,r,a){let o=t.has("WEBGL_multisampled_render_to_texture")?t.get("WEBGL_multisampled_render_to_texture"):null,l=typeof navigator>"u"?!1:/OculusBrowser/g.test(navigator.userAgent),c=new Ut,h=new WeakMap,f=new Set,u,p=new WeakMap,g=!1;try{g=typeof OffscreenCanvas<"u"&&new OffscreenCanvas(1,1).getContext("2d")!==null}catch{}function x(A,_){return g?new OffscreenCanvas(A,_):nr("canvas")}function m(A,_,O){let Y=1,j=_e(A);if((j.width>O||j.height>O)&&(Y=O/Math.max(j.width,j.height)),Y<1)if(typeof HTMLImageElement<"u"&&A instanceof HTMLImageElement||typeof HTMLCanvasElement<"u"&&A instanceof HTMLCanvasElement||typeof ImageBitmap<"u"&&A instanceof ImageBitmap||typeof VideoFrame<"u"&&A instanceof VideoFrame){let et=Math.floor(Y*j.width),lt=Math.floor(Y*j.height);u===void 0&&(u=x(et,lt));let X=_?x(et,lt):u;return X.width=et,X.height=lt,X.getContext("2d").drawImage(A,0,0,et,lt),Et("WebGLRenderer: Texture has been resized from ("+j.width+"x"+j.height+") to ("+et+"x"+lt+")."),X}else return"data"in A&&Et("WebGLRenderer: Image in DataTexture is too big ("+j.width+"x"+j.height+")."),A;return A}function d(A){return A.generateMipmaps}function y(A){i.generateMipmap(A)}function S(A){return A.isWebGLCubeRenderTarget?i.TEXTURE_CUBE_MAP:A.isWebGL3DRenderTarget?i.TEXTURE_3D:A.isWebGLArrayRenderTarget||A.isCompressedArrayTexture?i.TEXTURE_2D_ARRAY:i.TEXTURE_2D}function b(A,_,O,Y,j,et=!1){if(A!==null){if(i[A]!==void 0)return i[A];Et("WebGLRenderer: Attempt to use non-existing WebGL internal format '"+A+"'")}let lt;Y&&(lt=t.get("EXT_texture_norm16"),lt||Et("WebGLRenderer: Unable to use normalized textures without EXT_texture_norm16 extension"));let X=_;if(_===i.RED&&(O===i.FLOAT&&(X=i.R32F),O===i.HALF_FLOAT&&(X=i.R16F),O===i.UNSIGNED_BYTE&&(X=i.R8),O===i.UNSIGNED_SHORT&&lt&&(X=lt.R16_EXT),O===i.SHORT&&lt&&(X=lt.R16_SNORM_EXT)),_===i.RED_INTEGER&&(O===i.UNSIGNED_BYTE&&(X=i.R8UI),O===i.UNSIGNED_SHORT&&(X=i.R16UI),O===i.UNSIGNED_INT&&(X=i.R32UI),O===i.BYTE&&(X=i.R8I),O===i.SHORT&&(X=i.R16I),O===i.INT&&(X=i.R32I)),_===i.RG&&(O===i.FLOAT&&(X=i.RG32F),O===i.HALF_FLOAT&&(X=i.RG16F),O===i.UNSIGNED_BYTE&&(X=i.RG8),O===i.UNSIGNED_SHORT&&lt&&(X=lt.RG16_EXT),O===i.SHORT&&lt&&(X=lt.RG16_SNORM_EXT)),_===i.RG_INTEGER&&(O===i.UNSIGNED_BYTE&&(X=i.RG8UI),O===i.UNSIGNED_SHORT&&(X=i.RG16UI),O===i.UNSIGNED_INT&&(X=i.RG32UI),O===i.BYTE&&(X=i.RG8I),O===i.SHORT&&(X=i.RG16I),O===i.INT&&(X=i.RG32I)),_===i.RGB_INTEGER&&(O===i.UNSIGNED_BYTE&&(X=i.RGB8UI),O===i.UNSIGNED_SHORT&&(X=i.RGB16UI),O===i.UNSIGNED_INT&&(X=i.RGB32UI),O===i.BYTE&&(X=i.RGB8I),O===i.SHORT&&(X=i.RGB16I),O===i.INT&&(X=i.RGB32I)),_===i.RGBA_INTEGER&&(O===i.UNSIGNED_BYTE&&(X=i.RGBA8UI),O===i.UNSIGNED_SHORT&&(X=i.RGBA16UI),O===i.UNSIGNED_INT&&(X=i.RGBA32UI),O===i.BYTE&&(X=i.RGBA8I),O===i.SHORT&&(X=i.RGBA16I),O===i.INT&&(X=i.RGBA32I)),_===i.RGB&&(O===i.UNSIGNED_SHORT&&lt&&(X=lt.RGB16_EXT),O===i.SHORT&&lt&&(X=lt.RGB16_SNORM_EXT),O===i.UNSIGNED_INT_5_9_9_9_REV&&(X=i.RGB9_E5),O===i.UNSIGNED_INT_10F_11F_11F_REV&&(X=i.R11F_G11F_B10F)),_===i.RGBA){let Z=et?tr:Ht.getTransfer(j);O===i.FLOAT&&(X=i.RGBA32F),O===i.HALF_FLOAT&&(X=i.RGBA16F),O===i.UNSIGNED_BYTE&&(X=Z===Kt?i.SRGB8_ALPHA8:i.RGBA8),O===i.UNSIGNED_SHORT&&lt&&(X=lt.RGBA16_EXT),O===i.SHORT&&lt&&(X=lt.RGBA16_SNORM_EXT),O===i.UNSIGNED_SHORT_4_4_4_4&&(X=i.RGBA4),O===i.UNSIGNED_SHORT_5_5_5_1&&(X=i.RGB5_A1)}return(X===i.R16F||X===i.R32F||X===i.RG16F||X===i.RG32F||X===i.RGBA16F||X===i.RGBA32F)&&t.get("EXT_color_buffer_float"),X}function T(A,_){let O;return A?_===null||_===En||_===Fs?O=i.DEPTH24_STENCIL8:_===Cn?O=i.DEPTH32F_STENCIL8:_===Ds&&(O=i.DEPTH24_STENCIL8,Et("DepthTexture: 16 bit depth attachment is not supported with stencil. Using 24-bit attachment.")):_===null||_===En||_===Fs?O=i.DEPTH_COMPONENT24:_===Cn?O=i.DEPTH_COMPONENT32F:_===Ds&&(O=i.DEPTH_COMPONENT16),O}function w(A,_){return d(A)===!0||A.isFramebufferTexture&&A.minFilter!==Oe&&A.minFilter!==ze?Math.log2(Math.max(_.width,_.height))+1:A.mipmaps!==void 0&&A.mipmaps.length>0?A.mipmaps.length:A.isCompressedTexture&&Array.isArray(A.image)?_.mipmaps.length:1}function R(A){let _=A.target;_.removeEventListener("dispose",R),E(_),_.isVideoTexture&&h.delete(_),_.isHTMLTexture&&f.delete(_)}function v(A){let _=A.target;_.removeEventListener("dispose",v),C(_)}function E(A){let _=n.get(A);if(_.__webglInit===void 0)return;let O=A.source,Y=p.get(O);if(Y){let j=Y[_.__cacheKey];j.usedTimes--,j.usedTimes===0&&I(A),Object.keys(Y).length===0&&p.delete(O)}n.remove(A)}function I(A){let _=n.get(A);i.deleteTexture(_.__webglTexture);let O=A.source,Y=p.get(O);delete Y[_.__cacheKey],a.memory.textures--}function C(A){let _=n.get(A);if(A.depthTexture&&(A.depthTexture.dispose(),n.remove(A.depthTexture)),A.isWebGLCubeRenderTarget)for(let Y=0;Y<6;Y++){if(Array.isArray(_.__webglFramebuffer[Y]))for(let j=0;j<_.__webglFramebuffer[Y].length;j++)i.deleteFramebuffer(_.__webglFramebuffer[Y][j]);else i.deleteFramebuffer(_.__webglFramebuffer[Y]);_.__webglDepthbuffer&&i.deleteRenderbuffer(_.__webglDepthbuffer[Y])}else{if(Array.isArray(_.__webglFramebuffer))for(let Y=0;Y<_.__webglFramebuffer.length;Y++)i.deleteFramebuffer(_.__webglFramebuffer[Y]);else i.deleteFramebuffer(_.__webglFramebuffer);if(_.__webglDepthbuffer&&i.deleteRenderbuffer(_.__webglDepthbuffer),_.__webglMultisampledFramebuffer&&i.deleteFramebuffer(_.__webglMultisampledFramebuffer),_.__webglColorRenderbuffer)for(let Y=0;Y<_.__webglColorRenderbuffer.length;Y++)_.__webglColorRenderbuffer[Y]&&i.deleteRenderbuffer(_.__webglColorRenderbuffer[Y]);_.__webglDepthRenderbuffer&&i.deleteRenderbuffer(_.__webglDepthRenderbuffer)}let O=A.textures;for(let Y=0,j=O.length;Y<j;Y++){let et=n.get(O[Y]);et.__webglTexture&&(i.deleteTexture(et.__webglTexture),a.memory.textures--),n.remove(O[Y])}n.remove(A)}let N=0;function H(){N=0}function W(){return N}function U(A){N=A}function z(){let A=N;return A>=s.maxTextures&&Et("WebGLTextures: Trying to use "+A+" texture units while this GPU supports only "+s.maxTextures),N+=1,A}function V(A){let _=[];return _.push(A.wrapS),_.push(A.wrapT),_.push(A.wrapR||0),_.push(A.magFilter),_.push(A.minFilter),_.push(A.anisotropy),_.push(A.internalFormat),_.push(A.format),_.push(A.type),_.push(A.generateMipmaps),_.push(A.premultiplyAlpha),_.push(A.flipY),_.push(A.unpackAlignment),_.push(A.colorSpace),_.join()}function $(A,_){let O=n.get(A);if(A.isVideoTexture&&ce(A),A.isRenderTargetTexture===!1&&A.isExternalTexture!==!0&&A.version>0&&O.__version!==A.version){let Y=A.image;if(Y===null)Et("WebGLRenderer: Texture marked for update but no image data found.");else if(Y.complete===!1)Et("WebGLRenderer: Texture marked for update but image is incomplete");else{Ct(O,A,_);return}}else A.isExternalTexture&&(O.__webglTexture=A.sourceTexture?A.sourceTexture:null);e.bindTexture(i.TEXTURE_2D,O.__webglTexture,i.TEXTURE0+_)}function tt(A,_){let O=n.get(A);if(A.isRenderTargetTexture===!1&&A.version>0&&O.__version!==A.version){Ct(O,A,_);return}else A.isExternalTexture&&(O.__webglTexture=A.sourceTexture?A.sourceTexture:null);e.bindTexture(i.TEXTURE_2D_ARRAY,O.__webglTexture,i.TEXTURE0+_)}function ct(A,_){let O=n.get(A);if(A.isRenderTargetTexture===!1&&A.version>0&&O.__version!==A.version){Ct(O,A,_);return}e.bindTexture(i.TEXTURE_3D,O.__webglTexture,i.TEXTURE0+_)}function Mt(A,_){let O=n.get(A);if(A.isCubeDepthTexture!==!0&&A.version>0&&O.__version!==A.version){Ft(O,A,_);return}e.bindTexture(i.TEXTURE_CUBE_MAP,O.__webglTexture,i.TEXTURE0+_)}let St={[ka]:i.REPEAT,[Un]:i.CLAMP_TO_EDGE,[za]:i.MIRRORED_REPEAT},Xt={[Oe]:i.NEAREST,[nf]:i.NEAREST_MIPMAP_NEAREST,[wr]:i.NEAREST_MIPMAP_LINEAR,[ze]:i.LINEAR,[_o]:i.LINEAR_MIPMAP_NEAREST,[Pi]:i.LINEAR_MIPMAP_LINEAR},te={[af]:i.NEVER,[uf]:i.ALWAYS,[of]:i.LESS,[tl]:i.LEQUAL,[lf]:i.EQUAL,[el]:i.GEQUAL,[cf]:i.GREATER,[hf]:i.NOTEQUAL};function kt(A,_){if(_.type===Cn&&t.has("OES_texture_float_linear")===!1&&(_.magFilter===ze||_.magFilter===_o||_.magFilter===wr||_.magFilter===Pi||_.minFilter===ze||_.minFilter===_o||_.minFilter===wr||_.minFilter===Pi)&&Et("WebGLRenderer: Unable to use linear filtering with floating point textures. OES_texture_float_linear not supported on this device."),i.texParameteri(A,i.TEXTURE_WRAP_S,St[_.wrapS]),i.texParameteri(A,i.TEXTURE_WRAP_T,St[_.wrapT]),(A===i.TEXTURE_3D||A===i.TEXTURE_2D_ARRAY)&&i.texParameteri(A,i.TEXTURE_WRAP_R,St[_.wrapR]),i.texParameteri(A,i.TEXTURE_MAG_FILTER,Xt[_.magFilter]),i.texParameteri(A,i.TEXTURE_MIN_FILTER,Xt[_.minFilter]),_.compareFunction&&(i.texParameteri(A,i.TEXTURE_COMPARE_MODE,i.COMPARE_REF_TO_TEXTURE),i.texParameteri(A,i.TEXTURE_COMPARE_FUNC,te[_.compareFunction])),t.has("EXT_texture_filter_anisotropic")===!0){if(_.magFilter===Oe||_.minFilter!==wr&&_.minFilter!==Pi||_.type===Cn&&t.has("OES_texture_float_linear")===!1)return;if(_.anisotropy>1||n.get(_).__currentAnisotropy){let O=t.get("EXT_texture_filter_anisotropic");i.texParameterf(A,O.TEXTURE_MAX_ANISOTROPY_EXT,Math.min(_.anisotropy,s.getMaxAnisotropy())),n.get(_).__currentAnisotropy=_.anisotropy}}}function J(A,_){let O=!1;A.__webglInit===void 0&&(A.__webglInit=!0,_.addEventListener("dispose",R));let Y=_.source,j=p.get(Y);j===void 0&&(j={},p.set(Y,j));let et=V(_);if(et!==A.__cacheKey){j[et]===void 0&&(j[et]={texture:i.createTexture(),usedTimes:0},a.memory.textures++,O=!0),j[et].usedTimes++;let lt=j[A.__cacheKey];lt!==void 0&&(j[A.__cacheKey].usedTimes--,lt.usedTimes===0&&I(_)),A.__cacheKey=et,A.__webglTexture=j[et].texture}return O}function mt(A,_,O){return Math.floor(Math.floor(A/O)/_)}function rt(A,_,O,Y){let et=A.updateRanges;if(et.length===0)e.texSubImage2D(i.TEXTURE_2D,0,0,0,_.width,_.height,O,Y,_.data);else{et.sort((vt,at)=>vt.start-at.start);let lt=0;for(let vt=1;vt<et.length;vt++){let at=et[lt],nt=et[vt],Nt=at.start+at.count,zt=mt(nt.start,_.width,4),$t=mt(at.start,_.width,4);nt.start<=Nt+1&&zt===$t&&mt(nt.start+nt.count-1,_.width,4)===zt?at.count=Math.max(at.count,nt.start+nt.count-at.start):(++lt,et[lt]=nt)}et.length=lt+1;let X=e.getParameter(i.UNPACK_ROW_LENGTH),Z=e.getParameter(i.UNPACK_SKIP_PIXELS),gt=e.getParameter(i.UNPACK_SKIP_ROWS);e.pixelStorei(i.UNPACK_ROW_LENGTH,_.width);for(let vt=0,at=et.length;vt<at;vt++){let nt=et[vt],Nt=Math.floor(nt.start/4),zt=Math.ceil(nt.count/4),$t=Nt%_.width,P=Math.floor(Nt/_.width),it=zt,q=1;e.pixelStorei(i.UNPACK_SKIP_PIXELS,$t),e.pixelStorei(i.UNPACK_SKIP_ROWS,P),e.texSubImage2D(i.TEXTURE_2D,0,$t,P,it,q,O,Y,_.data)}A.clearUpdateRanges(),e.pixelStorei(i.UNPACK_ROW_LENGTH,X),e.pixelStorei(i.UNPACK_SKIP_PIXELS,Z),e.pixelStorei(i.UNPACK_SKIP_ROWS,gt)}}function Ct(A,_,O){let Y=i.TEXTURE_2D;(_.isDataArrayTexture||_.isCompressedArrayTexture)&&(Y=i.TEXTURE_2D_ARRAY),_.isData3DTexture&&(Y=i.TEXTURE_3D);let j=J(A,_),et=_.source;e.bindTexture(Y,A.__webglTexture,i.TEXTURE0+O);let lt=n.get(et);if(et.version!==lt.__version||j===!0){if(e.activeTexture(i.TEXTURE0+O),(typeof ImageBitmap<"u"&&_.image instanceof ImageBitmap)===!1){let q=Ht.getPrimaries(Ht.workingColorSpace),_t=_.colorSpace===ai?null:Ht.getPrimaries(_.colorSpace),ot=_.colorSpace===ai||q===_t?i.NONE:i.BROWSER_DEFAULT_WEBGL;e.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,_.flipY),e.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,_.premultiplyAlpha),e.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,ot)}e.pixelStorei(i.UNPACK_ALIGNMENT,_.unpackAlignment);let Z=m(_.image,!1,s.maxTextureSize);Z=ht(_,Z);let gt=r.convert(_.format,_.colorSpace),vt=r.convert(_.type),at=b(_.internalFormat,gt,vt,_.normalized,_.colorSpace,_.isVideoTexture);kt(Y,_);let nt,Nt=_.mipmaps,zt=_.isVideoTexture!==!0,$t=lt.__version===void 0||j===!0,P=et.dataReady,it=w(_,Z);if(_.isDepthTexture)at=T(_.format===Ii,_.type),$t&&(zt?e.texStorage2D(i.TEXTURE_2D,1,at,Z.width,Z.height):e.texImage2D(i.TEXTURE_2D,0,at,Z.width,Z.height,0,gt,vt,null));else if(_.isDataTexture)if(Nt.length>0){zt&&$t&&e.texStorage2D(i.TEXTURE_2D,it,at,Nt[0].width,Nt[0].height);for(let q=0,_t=Nt.length;q<_t;q++)nt=Nt[q],zt?P&&e.texSubImage2D(i.TEXTURE_2D,q,0,0,nt.width,nt.height,gt,vt,nt.data):e.texImage2D(i.TEXTURE_2D,q,at,nt.width,nt.height,0,gt,vt,nt.data);_.generateMipmaps=!1}else zt?($t&&e.texStorage2D(i.TEXTURE_2D,it,at,Z.width,Z.height),P&&rt(_,Z,gt,vt)):e.texImage2D(i.TEXTURE_2D,0,at,Z.width,Z.height,0,gt,vt,Z.data);else if(_.isCompressedTexture)if(_.isCompressedArrayTexture){zt&&$t&&e.texStorage3D(i.TEXTURE_2D_ARRAY,it,at,Nt[0].width,Nt[0].height,Z.depth);for(let q=0,_t=Nt.length;q<_t;q++)if(nt=Nt[q],_.format!==yn)if(gt!==null)if(zt){if(P)if(_.layerUpdates.size>0){let ot=Wc(nt.width,nt.height,_.format,_.type);for(let K of _.layerUpdates){let wt=nt.data.subarray(K*ot/nt.data.BYTES_PER_ELEMENT,(K+1)*ot/nt.data.BYTES_PER_ELEMENT);e.compressedTexSubImage3D(i.TEXTURE_2D_ARRAY,q,0,0,K,nt.width,nt.height,1,gt,wt)}_.clearLayerUpdates()}else e.compressedTexSubImage3D(i.TEXTURE_2D_ARRAY,q,0,0,0,nt.width,nt.height,Z.depth,gt,nt.data)}else e.compressedTexImage3D(i.TEXTURE_2D_ARRAY,q,at,nt.width,nt.height,Z.depth,0,nt.data,0,0);else Et("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()");else zt?P&&e.texSubImage3D(i.TEXTURE_2D_ARRAY,q,0,0,0,nt.width,nt.height,Z.depth,gt,vt,nt.data):e.texImage3D(i.TEXTURE_2D_ARRAY,q,at,nt.width,nt.height,Z.depth,0,gt,vt,nt.data)}else{zt&&$t&&e.texStorage2D(i.TEXTURE_2D,it,at,Nt[0].width,Nt[0].height);for(let q=0,_t=Nt.length;q<_t;q++)nt=Nt[q],_.format!==yn?gt!==null?zt?P&&e.compressedTexSubImage2D(i.TEXTURE_2D,q,0,0,nt.width,nt.height,gt,nt.data):e.compressedTexImage2D(i.TEXTURE_2D,q,at,nt.width,nt.height,0,nt.data):Et("WebGLRenderer: Attempt to load unsupported compressed texture format in .uploadTexture()"):zt?P&&e.texSubImage2D(i.TEXTURE_2D,q,0,0,nt.width,nt.height,gt,vt,nt.data):e.texImage2D(i.TEXTURE_2D,q,at,nt.width,nt.height,0,gt,vt,nt.data)}else if(_.isDataArrayTexture)if(zt){if($t&&e.texStorage3D(i.TEXTURE_2D_ARRAY,it,at,Z.width,Z.height,Z.depth),P)if(_.layerUpdates.size>0){let q=Wc(Z.width,Z.height,_.format,_.type);for(let _t of _.layerUpdates){let ot=Z.data.subarray(_t*q/Z.data.BYTES_PER_ELEMENT,(_t+1)*q/Z.data.BYTES_PER_ELEMENT);e.texSubImage3D(i.TEXTURE_2D_ARRAY,0,0,0,_t,Z.width,Z.height,1,gt,vt,ot)}_.clearLayerUpdates()}else e.texSubImage3D(i.TEXTURE_2D_ARRAY,0,0,0,0,Z.width,Z.height,Z.depth,gt,vt,Z.data)}else e.texImage3D(i.TEXTURE_2D_ARRAY,0,at,Z.width,Z.height,Z.depth,0,gt,vt,Z.data);else if(_.isData3DTexture)zt?($t&&e.texStorage3D(i.TEXTURE_3D,it,at,Z.width,Z.height,Z.depth),P&&e.texSubImage3D(i.TEXTURE_3D,0,0,0,0,Z.width,Z.height,Z.depth,gt,vt,Z.data)):e.texImage3D(i.TEXTURE_3D,0,at,Z.width,Z.height,Z.depth,0,gt,vt,Z.data);else if(_.isFramebufferTexture){if($t)if(zt)e.texStorage2D(i.TEXTURE_2D,it,at,Z.width,Z.height);else{let q=Z.width,_t=Z.height;for(let ot=0;ot<it;ot++)e.texImage2D(i.TEXTURE_2D,ot,at,q,_t,0,gt,vt,null),q>>=1,_t>>=1}}else if(_.isHTMLTexture){if("texElementImage2D"in i){let q=i.canvas;if(q.hasAttribute("layoutsubtree")||q.setAttribute("layoutsubtree","true"),Z.parentNode!==q){q.appendChild(Z),f.add(_),q.onpaint=Ot=>{let Se=Ot.changedElements;for(let ne of f)Se.includes(ne.image)&&(ne.needsUpdate=!0)},q.requestPaint();return}let _t=0,ot=i.RGBA,K=i.RGBA,wt=i.UNSIGNED_BYTE;i.texElementImage2D(i.TEXTURE_2D,_t,ot,K,wt,Z),i.texParameteri(i.TEXTURE_2D,i.TEXTURE_MIN_FILTER,i.LINEAR),i.texParameteri(i.TEXTURE_2D,i.TEXTURE_WRAP_S,i.CLAMP_TO_EDGE),i.texParameteri(i.TEXTURE_2D,i.TEXTURE_WRAP_T,i.CLAMP_TO_EDGE)}}else if(Nt.length>0){if(zt&&$t){let q=_e(Nt[0]);e.texStorage2D(i.TEXTURE_2D,it,at,q.width,q.height)}for(let q=0,_t=Nt.length;q<_t;q++)nt=Nt[q],zt?P&&e.texSubImage2D(i.TEXTURE_2D,q,0,0,gt,vt,nt):e.texImage2D(i.TEXTURE_2D,q,at,gt,vt,nt);_.generateMipmaps=!1}else if(zt){if($t){let q=_e(Z);e.texStorage2D(i.TEXTURE_2D,it,at,q.width,q.height)}P&&e.texSubImage2D(i.TEXTURE_2D,0,0,0,gt,vt,Z)}else e.texImage2D(i.TEXTURE_2D,0,at,gt,vt,Z);d(_)&&y(Y),lt.__version=et.version,_.onUpdate&&_.onUpdate(_)}A.__version=_.version}function Ft(A,_,O){if(_.image.length!==6)return;let Y=J(A,_),j=_.source;e.bindTexture(i.TEXTURE_CUBE_MAP,A.__webglTexture,i.TEXTURE0+O);let et=n.get(j);if(j.version!==et.__version||Y===!0){e.activeTexture(i.TEXTURE0+O);let lt=Ht.getPrimaries(Ht.workingColorSpace),X=_.colorSpace===ai?null:Ht.getPrimaries(_.colorSpace),Z=_.colorSpace===ai||lt===X?i.NONE:i.BROWSER_DEFAULT_WEBGL;e.pixelStorei(i.UNPACK_FLIP_Y_WEBGL,_.flipY),e.pixelStorei(i.UNPACK_PREMULTIPLY_ALPHA_WEBGL,_.premultiplyAlpha),e.pixelStorei(i.UNPACK_ALIGNMENT,_.unpackAlignment),e.pixelStorei(i.UNPACK_COLORSPACE_CONVERSION_WEBGL,Z);let gt=_.isCompressedTexture||_.image[0].isCompressedTexture,vt=_.image[0]&&_.image[0].isDataTexture,at=[];for(let K=0;K<6;K++)!gt&&!vt?at[K]=m(_.image[K],!0,s.maxCubemapSize):at[K]=vt?_.image[K].image:_.image[K],at[K]=ht(_,at[K]);let nt=at[0],Nt=r.convert(_.format,_.colorSpace),zt=r.convert(_.type),$t=b(_.internalFormat,Nt,zt,_.normalized,_.colorSpace),P=_.isVideoTexture!==!0,it=et.__version===void 0||Y===!0,q=j.dataReady,_t=w(_,nt);kt(i.TEXTURE_CUBE_MAP,_);let ot;if(gt){P&&it&&e.texStorage2D(i.TEXTURE_CUBE_MAP,_t,$t,nt.width,nt.height);for(let K=0;K<6;K++){ot=at[K].mipmaps;for(let wt=0;wt<ot.length;wt++){let Ot=ot[wt];_.format!==yn?Nt!==null?P?q&&e.compressedTexSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,wt,0,0,Ot.width,Ot.height,Nt,Ot.data):e.compressedTexImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,wt,$t,Ot.width,Ot.height,0,Ot.data):Et("WebGLRenderer: Attempt to load unsupported compressed texture format in .setTextureCube()"):P?q&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,wt,0,0,Ot.width,Ot.height,Nt,zt,Ot.data):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,wt,$t,Ot.width,Ot.height,0,Nt,zt,Ot.data)}}}else{if(ot=_.mipmaps,P&&it){ot.length>0&&_t++;let K=_e(at[0]);e.texStorage2D(i.TEXTURE_CUBE_MAP,_t,$t,K.width,K.height)}for(let K=0;K<6;K++)if(vt){P?q&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,0,0,0,at[K].width,at[K].height,Nt,zt,at[K].data):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,0,$t,at[K].width,at[K].height,0,Nt,zt,at[K].data);for(let wt=0;wt<ot.length;wt++){let Se=ot[wt].image[K].image;P?q&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,wt+1,0,0,Se.width,Se.height,Nt,zt,Se.data):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,wt+1,$t,Se.width,Se.height,0,Nt,zt,Se.data)}}else{P?q&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,0,0,0,Nt,zt,at[K]):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,0,$t,Nt,zt,at[K]);for(let wt=0;wt<ot.length;wt++){let Ot=ot[wt];P?q&&e.texSubImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,wt+1,0,0,Nt,zt,Ot.image[K]):e.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+K,wt+1,$t,Nt,zt,Ot.image[K])}}}d(_)&&y(i.TEXTURE_CUBE_MAP),et.__version=j.version,_.onUpdate&&_.onUpdate(_)}A.__version=_.version}function Pt(A,_,O,Y,j,et){let lt=r.convert(O.format,O.colorSpace),X=r.convert(O.type),Z=b(O.internalFormat,lt,X,O.normalized,O.colorSpace),gt=n.get(_),vt=n.get(O);if(vt.__renderTarget=_,!gt.__hasExternalTextures){let at=Math.max(1,_.width>>et),nt=Math.max(1,_.height>>et);j===i.TEXTURE_3D||j===i.TEXTURE_2D_ARRAY?e.texImage3D(j,et,Z,at,nt,_.depth,0,lt,X,null):e.texImage2D(j,et,Z,at,nt,0,lt,X,null)}e.bindFramebuffer(i.FRAMEBUFFER,A),Yt(_)?o.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,Y,j,vt.__webglTexture,0,Ie(_)):(j===i.TEXTURE_2D||j>=i.TEXTURE_CUBE_MAP_POSITIVE_X&&j<=i.TEXTURE_CUBE_MAP_NEGATIVE_Z)&&i.framebufferTexture2D(i.FRAMEBUFFER,Y,j,vt.__webglTexture,et),e.bindFramebuffer(i.FRAMEBUFFER,null)}function pe(A,_,O){if(i.bindRenderbuffer(i.RENDERBUFFER,A),_.depthBuffer){let Y=_.depthTexture,j=Y&&Y.isDepthTexture?Y.type:null,et=T(_.stencilBuffer,j),lt=_.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;Yt(_)?o.renderbufferStorageMultisampleEXT(i.RENDERBUFFER,Ie(_),et,_.width,_.height):O?i.renderbufferStorageMultisample(i.RENDERBUFFER,Ie(_),et,_.width,_.height):i.renderbufferStorage(i.RENDERBUFFER,et,_.width,_.height),i.framebufferRenderbuffer(i.FRAMEBUFFER,lt,i.RENDERBUFFER,A)}else{let Y=_.textures;for(let j=0;j<Y.length;j++){let et=Y[j],lt=r.convert(et.format,et.colorSpace),X=r.convert(et.type),Z=b(et.internalFormat,lt,X,et.normalized,et.colorSpace);Yt(_)?o.renderbufferStorageMultisampleEXT(i.RENDERBUFFER,Ie(_),Z,_.width,_.height):O?i.renderbufferStorageMultisample(i.RENDERBUFFER,Ie(_),Z,_.width,_.height):i.renderbufferStorage(i.RENDERBUFFER,Z,_.width,_.height)}}i.bindRenderbuffer(i.RENDERBUFFER,null)}function qt(A,_,O){let Y=_.isWebGLCubeRenderTarget===!0;if(e.bindFramebuffer(i.FRAMEBUFFER,A),!(_.depthTexture&&_.depthTexture.isDepthTexture))throw new Error("renderTarget.depthTexture must be an instance of THREE.DepthTexture");let j=n.get(_.depthTexture);if(j.__renderTarget=_,(!j.__webglTexture||_.depthTexture.image.width!==_.width||_.depthTexture.image.height!==_.height)&&(_.depthTexture.image.width=_.width,_.depthTexture.image.height=_.height,_.depthTexture.needsUpdate=!0),Y){if(j.__webglInit===void 0&&(j.__webglInit=!0,_.depthTexture.addEventListener("dispose",R)),j.__webglTexture===void 0){j.__webglTexture=i.createTexture(),e.bindTexture(i.TEXTURE_CUBE_MAP,j.__webglTexture),kt(i.TEXTURE_CUBE_MAP,_.depthTexture);let gt=r.convert(_.depthTexture.format),vt=r.convert(_.depthTexture.type),at;_.depthTexture.format===Bn?at=i.DEPTH_COMPONENT24:_.depthTexture.format===Ii&&(at=i.DEPTH24_STENCIL8);for(let nt=0;nt<6;nt++)i.texImage2D(i.TEXTURE_CUBE_MAP_POSITIVE_X+nt,0,at,_.width,_.height,0,gt,vt,null)}}else $(_.depthTexture,0);let et=j.__webglTexture,lt=Ie(_),X=Y?i.TEXTURE_CUBE_MAP_POSITIVE_X+O:i.TEXTURE_2D,Z=_.depthTexture.format===Ii?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;if(_.depthTexture.format===Bn)Yt(_)?o.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,Z,X,et,0,lt):i.framebufferTexture2D(i.FRAMEBUFFER,Z,X,et,0);else if(_.depthTexture.format===Ii)Yt(_)?o.framebufferTexture2DMultisampleEXT(i.FRAMEBUFFER,Z,X,et,0,lt):i.framebufferTexture2D(i.FRAMEBUFFER,Z,X,et,0);else throw new Error("Unknown depthTexture format")}function ee(A){let _=n.get(A),O=A.isWebGLCubeRenderTarget===!0;if(_.__boundDepthTexture!==A.depthTexture){let Y=A.depthTexture;if(_.__depthDisposeCallback&&_.__depthDisposeCallback(),Y){let j=()=>{delete _.__boundDepthTexture,delete _.__depthDisposeCallback,Y.removeEventListener("dispose",j)};Y.addEventListener("dispose",j),_.__depthDisposeCallback=j}_.__boundDepthTexture=Y}if(A.depthTexture&&!_.__autoAllocateDepthBuffer)if(O)for(let Y=0;Y<6;Y++)qt(_.__webglFramebuffer[Y],A,Y);else{let Y=A.texture.mipmaps;Y&&Y.length>0?qt(_.__webglFramebuffer[0],A,0):qt(_.__webglFramebuffer,A,0)}else if(O){_.__webglDepthbuffer=[];for(let Y=0;Y<6;Y++)if(e.bindFramebuffer(i.FRAMEBUFFER,_.__webglFramebuffer[Y]),_.__webglDepthbuffer[Y]===void 0)_.__webglDepthbuffer[Y]=i.createRenderbuffer(),pe(_.__webglDepthbuffer[Y],A,!1);else{let j=A.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,et=_.__webglDepthbuffer[Y];i.bindRenderbuffer(i.RENDERBUFFER,et),i.framebufferRenderbuffer(i.FRAMEBUFFER,j,i.RENDERBUFFER,et)}}else{let Y=A.texture.mipmaps;if(Y&&Y.length>0?e.bindFramebuffer(i.FRAMEBUFFER,_.__webglFramebuffer[0]):e.bindFramebuffer(i.FRAMEBUFFER,_.__webglFramebuffer),_.__webglDepthbuffer===void 0)_.__webglDepthbuffer=i.createRenderbuffer(),pe(_.__webglDepthbuffer,A,!1);else{let j=A.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,et=_.__webglDepthbuffer;i.bindRenderbuffer(i.RENDERBUFFER,et),i.framebufferRenderbuffer(i.FRAMEBUFFER,j,i.RENDERBUFFER,et)}}e.bindFramebuffer(i.FRAMEBUFFER,null)}function ue(A,_,O){let Y=n.get(A);_!==void 0&&Pt(Y.__webglFramebuffer,A,A.texture,i.COLOR_ATTACHMENT0,i.TEXTURE_2D,0),O!==void 0&&ee(A)}function Wt(A){let _=A.texture,O=n.get(A),Y=n.get(_);A.addEventListener("dispose",v);let j=A.textures,et=A.isWebGLCubeRenderTarget===!0,lt=j.length>1;if(lt||(Y.__webglTexture===void 0&&(Y.__webglTexture=i.createTexture()),Y.__version=_.version,a.memory.textures++),et){O.__webglFramebuffer=[];for(let X=0;X<6;X++)if(_.mipmaps&&_.mipmaps.length>0){O.__webglFramebuffer[X]=[];for(let Z=0;Z<_.mipmaps.length;Z++)O.__webglFramebuffer[X][Z]=i.createFramebuffer()}else O.__webglFramebuffer[X]=i.createFramebuffer()}else{if(_.mipmaps&&_.mipmaps.length>0){O.__webglFramebuffer=[];for(let X=0;X<_.mipmaps.length;X++)O.__webglFramebuffer[X]=i.createFramebuffer()}else O.__webglFramebuffer=i.createFramebuffer();if(lt)for(let X=0,Z=j.length;X<Z;X++){let gt=n.get(j[X]);gt.__webglTexture===void 0&&(gt.__webglTexture=i.createTexture(),a.memory.textures++)}if(A.samples>0&&Yt(A)===!1){O.__webglMultisampledFramebuffer=i.createFramebuffer(),O.__webglColorRenderbuffer=[],e.bindFramebuffer(i.FRAMEBUFFER,O.__webglMultisampledFramebuffer);for(let X=0;X<j.length;X++){let Z=j[X];O.__webglColorRenderbuffer[X]=i.createRenderbuffer(),i.bindRenderbuffer(i.RENDERBUFFER,O.__webglColorRenderbuffer[X]);let gt=r.convert(Z.format,Z.colorSpace),vt=r.convert(Z.type),at=b(Z.internalFormat,gt,vt,Z.normalized,Z.colorSpace,A.isXRRenderTarget===!0),nt=Ie(A);i.renderbufferStorageMultisample(i.RENDERBUFFER,nt,at,A.width,A.height),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+X,i.RENDERBUFFER,O.__webglColorRenderbuffer[X])}i.bindRenderbuffer(i.RENDERBUFFER,null),A.depthBuffer&&(O.__webglDepthRenderbuffer=i.createRenderbuffer(),pe(O.__webglDepthRenderbuffer,A,!0)),e.bindFramebuffer(i.FRAMEBUFFER,null)}}if(et){e.bindTexture(i.TEXTURE_CUBE_MAP,Y.__webglTexture),kt(i.TEXTURE_CUBE_MAP,_);for(let X=0;X<6;X++)if(_.mipmaps&&_.mipmaps.length>0)for(let Z=0;Z<_.mipmaps.length;Z++)Pt(O.__webglFramebuffer[X][Z],A,_,i.COLOR_ATTACHMENT0,i.TEXTURE_CUBE_MAP_POSITIVE_X+X,Z);else Pt(O.__webglFramebuffer[X],A,_,i.COLOR_ATTACHMENT0,i.TEXTURE_CUBE_MAP_POSITIVE_X+X,0);d(_)&&y(i.TEXTURE_CUBE_MAP),e.unbindTexture()}else if(lt){for(let X=0,Z=j.length;X<Z;X++){let gt=j[X],vt=n.get(gt),at=i.TEXTURE_2D;(A.isWebGL3DRenderTarget||A.isWebGLArrayRenderTarget)&&(at=A.isWebGL3DRenderTarget?i.TEXTURE_3D:i.TEXTURE_2D_ARRAY),e.bindTexture(at,vt.__webglTexture),kt(at,gt),Pt(O.__webglFramebuffer,A,gt,i.COLOR_ATTACHMENT0+X,at,0),d(gt)&&y(at)}e.unbindTexture()}else{let X=i.TEXTURE_2D;if((A.isWebGL3DRenderTarget||A.isWebGLArrayRenderTarget)&&(X=A.isWebGL3DRenderTarget?i.TEXTURE_3D:i.TEXTURE_2D_ARRAY),e.bindTexture(X,Y.__webglTexture),kt(X,_),_.mipmaps&&_.mipmaps.length>0)for(let Z=0;Z<_.mipmaps.length;Z++)Pt(O.__webglFramebuffer[Z],A,_,i.COLOR_ATTACHMENT0,X,Z);else Pt(O.__webglFramebuffer,A,_,i.COLOR_ATTACHMENT0,X,0);d(_)&&y(X),e.unbindTexture()}A.depthBuffer&&ee(A)}function Pe(A){let _=A.textures;for(let O=0,Y=_.length;O<Y;O++){let j=_[O];if(d(j)){let et=S(A),lt=n.get(j).__webglTexture;e.bindTexture(et,lt),y(et),e.unbindTexture()}}}let me=[],ln=[];function L(A){if(A.samples>0){if(Yt(A)===!1){let _=A.textures,O=A.width,Y=A.height,j=i.COLOR_BUFFER_BIT,et=A.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT,lt=n.get(A),X=_.length>1;if(X)for(let gt=0;gt<_.length;gt++)e.bindFramebuffer(i.FRAMEBUFFER,lt.__webglMultisampledFramebuffer),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+gt,i.RENDERBUFFER,null),e.bindFramebuffer(i.FRAMEBUFFER,lt.__webglFramebuffer),i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0+gt,i.TEXTURE_2D,null,0);e.bindFramebuffer(i.READ_FRAMEBUFFER,lt.__webglMultisampledFramebuffer);let Z=A.texture.mipmaps;Z&&Z.length>0?e.bindFramebuffer(i.DRAW_FRAMEBUFFER,lt.__webglFramebuffer[0]):e.bindFramebuffer(i.DRAW_FRAMEBUFFER,lt.__webglFramebuffer);for(let gt=0;gt<_.length;gt++){if(A.resolveDepthBuffer&&(A.depthBuffer&&(j|=i.DEPTH_BUFFER_BIT),A.stencilBuffer&&A.resolveStencilBuffer&&(j|=i.STENCIL_BUFFER_BIT)),X){i.framebufferRenderbuffer(i.READ_FRAMEBUFFER,i.COLOR_ATTACHMENT0,i.RENDERBUFFER,lt.__webglColorRenderbuffer[gt]);let vt=n.get(_[gt]).__webglTexture;i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0,i.TEXTURE_2D,vt,0)}i.blitFramebuffer(0,0,O,Y,0,0,O,Y,j,i.NEAREST),l===!0&&(me.length=0,ln.length=0,me.push(i.COLOR_ATTACHMENT0+gt),A.depthBuffer&&A.resolveDepthBuffer===!1&&(me.push(et),ln.push(et),i.invalidateFramebuffer(i.DRAW_FRAMEBUFFER,ln)),i.invalidateFramebuffer(i.READ_FRAMEBUFFER,me))}if(e.bindFramebuffer(i.READ_FRAMEBUFFER,null),e.bindFramebuffer(i.DRAW_FRAMEBUFFER,null),X)for(let gt=0;gt<_.length;gt++){e.bindFramebuffer(i.FRAMEBUFFER,lt.__webglMultisampledFramebuffer),i.framebufferRenderbuffer(i.FRAMEBUFFER,i.COLOR_ATTACHMENT0+gt,i.RENDERBUFFER,lt.__webglColorRenderbuffer[gt]);let vt=n.get(_[gt]).__webglTexture;e.bindFramebuffer(i.FRAMEBUFFER,lt.__webglFramebuffer),i.framebufferTexture2D(i.DRAW_FRAMEBUFFER,i.COLOR_ATTACHMENT0+gt,i.TEXTURE_2D,vt,0)}e.bindFramebuffer(i.DRAW_FRAMEBUFFER,lt.__webglMultisampledFramebuffer)}else if(A.depthBuffer&&A.resolveDepthBuffer===!1&&l){let _=A.stencilBuffer?i.DEPTH_STENCIL_ATTACHMENT:i.DEPTH_ATTACHMENT;i.invalidateFramebuffer(i.DRAW_FRAMEBUFFER,[_])}}}function Ie(A){return Math.min(s.maxSamples,A.samples)}function Yt(A){let _=n.get(A);return A.samples>0&&t.has("WEBGL_multisampled_render_to_texture")===!0&&_.__useRenderToTexture!==!1}function ce(A){let _=a.render.frame;h.get(A)!==_&&(h.set(A,_),A.update())}function ht(A,_){let O=A.colorSpace,Y=A.format,j=A.type;return A.isCompressedTexture===!0||A.isVideoTexture===!0||O!==Qs&&O!==ai&&(Ht.getTransfer(O)===Kt?(Y!==yn||j!==mn)&&Et("WebGLTextures: sRGB encoded textures have to use RGBAFormat and UnsignedByteType."):Rt("WebGLTextures: Unsupported texture color space:",O)),_}function _e(A){return typeof HTMLImageElement<"u"&&A instanceof HTMLImageElement?(c.width=A.naturalWidth||A.width,c.height=A.naturalHeight||A.height):typeof VideoFrame<"u"&&A instanceof VideoFrame?(c.width=A.displayWidth,c.height=A.displayHeight):(c.width=A.width,c.height=A.height),c}this.allocateTextureUnit=z,this.resetTextureUnits=H,this.getTextureUnits=W,this.setTextureUnits=U,this.setTexture2D=$,this.setTexture2DArray=tt,this.setTexture3D=ct,this.setTextureCube=Mt,this.rebindTextures=ue,this.setupRenderTarget=Wt,this.updateRenderTargetMipmap=Pe,this.updateMultisampleRenderTarget=L,this.setupDepthRenderbuffer=ee,this.setupFrameBufferTexture=Pt,this.useMultisampledRTT=Yt,this.isReversedDepthBuffer=function(){return e.buffers.depth.getReversed()}}function Hv(i,t){function e(n,s=ai){let r,a=Ht.getTransfer(s);if(n===mn)return i.UNSIGNED_BYTE;if(n===vo)return i.UNSIGNED_SHORT_4_4_4_4;if(n===yo)return i.UNSIGNED_SHORT_5_5_5_1;if(n===Nc)return i.UNSIGNED_INT_5_9_9_9_REV;if(n===Dc)return i.UNSIGNED_INT_10F_11F_11F_REV;if(n===Ic)return i.BYTE;if(n===Lc)return i.SHORT;if(n===Ds)return i.UNSIGNED_SHORT;if(n===xo)return i.INT;if(n===En)return i.UNSIGNED_INT;if(n===Cn)return i.FLOAT;if(n===qe)return i.HALF_FLOAT;if(n===Fc)return i.ALPHA;if(n===Uc)return i.RGB;if(n===yn)return i.RGBA;if(n===Bn)return i.DEPTH_COMPONENT;if(n===Ii)return i.DEPTH_STENCIL;if(n===Oc)return i.RED;if(n===Mo)return i.RED_INTEGER;if(n===Li)return i.RG;if(n===bo)return i.RG_INTEGER;if(n===So)return i.RGBA_INTEGER;if(n===Ar||n===Tr||n===Er||n===Cr)if(a===Kt)if(r=t.get("WEBGL_compressed_texture_s3tc_srgb"),r!==null){if(n===Ar)return r.COMPRESSED_SRGB_S3TC_DXT1_EXT;if(n===Tr)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT1_EXT;if(n===Er)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT3_EXT;if(n===Cr)return r.COMPRESSED_SRGB_ALPHA_S3TC_DXT5_EXT}else return null;else if(r=t.get("WEBGL_compressed_texture_s3tc"),r!==null){if(n===Ar)return r.COMPRESSED_RGB_S3TC_DXT1_EXT;if(n===Tr)return r.COMPRESSED_RGBA_S3TC_DXT1_EXT;if(n===Er)return r.COMPRESSED_RGBA_S3TC_DXT3_EXT;if(n===Cr)return r.COMPRESSED_RGBA_S3TC_DXT5_EXT}else return null;if(n===wo||n===Ao||n===To||n===Eo)if(r=t.get("WEBGL_compressed_texture_pvrtc"),r!==null){if(n===wo)return r.COMPRESSED_RGB_PVRTC_4BPPV1_IMG;if(n===Ao)return r.COMPRESSED_RGB_PVRTC_2BPPV1_IMG;if(n===To)return r.COMPRESSED_RGBA_PVRTC_4BPPV1_IMG;if(n===Eo)return r.COMPRESSED_RGBA_PVRTC_2BPPV1_IMG}else return null;if(n===Co||n===Ro||n===Po||n===Io||n===Lo||n===Rr||n===No)if(r=t.get("WEBGL_compressed_texture_etc"),r!==null){if(n===Co||n===Ro)return a===Kt?r.COMPRESSED_SRGB8_ETC2:r.COMPRESSED_RGB8_ETC2;if(n===Po)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ETC2_EAC:r.COMPRESSED_RGBA8_ETC2_EAC;if(n===Io)return r.COMPRESSED_R11_EAC;if(n===Lo)return r.COMPRESSED_SIGNED_R11_EAC;if(n===Rr)return r.COMPRESSED_RG11_EAC;if(n===No)return r.COMPRESSED_SIGNED_RG11_EAC}else return null;if(n===Do||n===Fo||n===Uo||n===Oo||n===Bo||n===ko||n===zo||n===Vo||n===Go||n===Ho||n===Wo||n===Xo||n===qo||n===Yo)if(r=t.get("WEBGL_compressed_texture_astc"),r!==null){if(n===Do)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_4x4_KHR:r.COMPRESSED_RGBA_ASTC_4x4_KHR;if(n===Fo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_5x4_KHR:r.COMPRESSED_RGBA_ASTC_5x4_KHR;if(n===Uo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_5x5_KHR:r.COMPRESSED_RGBA_ASTC_5x5_KHR;if(n===Oo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_6x5_KHR:r.COMPRESSED_RGBA_ASTC_6x5_KHR;if(n===Bo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_6x6_KHR:r.COMPRESSED_RGBA_ASTC_6x6_KHR;if(n===ko)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x5_KHR:r.COMPRESSED_RGBA_ASTC_8x5_KHR;if(n===zo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x6_KHR:r.COMPRESSED_RGBA_ASTC_8x6_KHR;if(n===Vo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_8x8_KHR:r.COMPRESSED_RGBA_ASTC_8x8_KHR;if(n===Go)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x5_KHR:r.COMPRESSED_RGBA_ASTC_10x5_KHR;if(n===Ho)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x6_KHR:r.COMPRESSED_RGBA_ASTC_10x6_KHR;if(n===Wo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x8_KHR:r.COMPRESSED_RGBA_ASTC_10x8_KHR;if(n===Xo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_10x10_KHR:r.COMPRESSED_RGBA_ASTC_10x10_KHR;if(n===qo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_12x10_KHR:r.COMPRESSED_RGBA_ASTC_12x10_KHR;if(n===Yo)return a===Kt?r.COMPRESSED_SRGB8_ALPHA8_ASTC_12x12_KHR:r.COMPRESSED_RGBA_ASTC_12x12_KHR}else return null;if(n===Zo||n===Jo||n===$o)if(r=t.get("EXT_texture_compression_bptc"),r!==null){if(n===Zo)return a===Kt?r.COMPRESSED_SRGB_ALPHA_BPTC_UNORM_EXT:r.COMPRESSED_RGBA_BPTC_UNORM_EXT;if(n===Jo)return r.COMPRESSED_RGB_BPTC_SIGNED_FLOAT_EXT;if(n===$o)return r.COMPRESSED_RGB_BPTC_UNSIGNED_FLOAT_EXT}else return null;if(n===Ko||n===jo||n===Pr||n===Qo)if(r=t.get("EXT_texture_compression_rgtc"),r!==null){if(n===Ko)return r.COMPRESSED_RED_RGTC1_EXT;if(n===jo)return r.COMPRESSED_SIGNED_RED_RGTC1_EXT;if(n===Pr)return r.COMPRESSED_RED_GREEN_RGTC2_EXT;if(n===Qo)return r.COMPRESSED_SIGNED_RED_GREEN_RGTC2_EXT}else return null;return n===Fs?i.UNSIGNED_INT_24_8:i[n]!==void 0?i[n]:null}return{convert:e}}var Wv=`
void main() {

	gl_Position = vec4( position, 1.0 );

}`,Xv=`
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

}`,ch=class{constructor(){this.texture=null,this.mesh=null,this.depthNear=0,this.depthFar=0}init(t,e){if(this.texture===null){let n=new hr(t.texture);(t.depthNear!==e.depthNear||t.depthFar!==e.depthFar)&&(this.depthNear=t.depthNear,this.depthFar=t.depthFar),this.texture=n}}getMesh(t){if(this.texture!==null&&this.mesh===null){let e=t.cameras[0].viewport,n=new se({vertexShader:Wv,fragmentShader:Xv,uniforms:{depthColor:{value:this.texture},depthWidth:{value:e.z},depthHeight:{value:e.w}}});this.mesh=new rn(new ur(20,20),n)}return this.mesh}reset(){this.texture=null,this.mesh=null}getDepthTexture(){return this.texture}},hh=class extends kn{constructor(t,e){super();let n=this,s=null,r=1,a=null,o="local-floor",l=1,c=null,h=null,f=null,u=null,p=null,g=null,x=typeof XRWebGLBinding<"u",m=new ch,d={},y=e.getContextAttributes(),S=null,b=null,T=[],w=[],R=new Ut,v=null,E=new Xe;E.viewport=new ye;let I=new Xe;I.viewport=new ye;let C=[E,I],N=new uo,H=null,W=null;this.cameraAutoUpdate=!0,this.enabled=!1,this.isPresenting=!1,this.getController=function(J){let mt=T[J];return mt===void 0&&(mt=new Rs,T[J]=mt),mt.getTargetRaySpace()},this.getControllerGrip=function(J){let mt=T[J];return mt===void 0&&(mt=new Rs,T[J]=mt),mt.getGripSpace()},this.getHand=function(J){let mt=T[J];return mt===void 0&&(mt=new Rs,T[J]=mt),mt.getHandSpace()};function U(J){let mt=w.indexOf(J.inputSource);if(mt===-1)return;let rt=T[mt];rt!==void 0&&(rt.update(J.inputSource,J.frame,c||a),rt.dispatchEvent({type:J.type,data:J.inputSource}))}function z(){s.removeEventListener("select",U),s.removeEventListener("selectstart",U),s.removeEventListener("selectend",U),s.removeEventListener("squeeze",U),s.removeEventListener("squeezestart",U),s.removeEventListener("squeezeend",U),s.removeEventListener("end",z),s.removeEventListener("inputsourceschange",V);for(let J=0;J<T.length;J++){let mt=w[J];mt!==null&&(w[J]=null,T[J].disconnect(mt))}H=null,W=null,m.reset();for(let J in d)delete d[J];t.setRenderTarget(S),p=null,u=null,f=null,s=null,b=null,kt.stop(),n.isPresenting=!1,t.setPixelRatio(v),t.setSize(R.width,R.height,!1),n.dispatchEvent({type:"sessionend"})}this.setFramebufferScaleFactor=function(J){r=J,n.isPresenting===!0&&Et("WebXRManager: Cannot change framebuffer scale while presenting.")},this.setReferenceSpaceType=function(J){o=J,n.isPresenting===!0&&Et("WebXRManager: Cannot change reference space type while presenting.")},this.getReferenceSpace=function(){return c||a},this.setReferenceSpace=function(J){c=J},this.getBaseLayer=function(){return u!==null?u:p},this.getBinding=function(){return f===null&&x&&(f=new XRWebGLBinding(s,e)),f},this.getFrame=function(){return g},this.getSession=function(){return s},this.setSession=async function(J){if(s=J,s!==null){if(S=t.getRenderTarget(),s.addEventListener("select",U),s.addEventListener("selectstart",U),s.addEventListener("selectend",U),s.addEventListener("squeeze",U),s.addEventListener("squeezestart",U),s.addEventListener("squeezeend",U),s.addEventListener("end",z),s.addEventListener("inputsourceschange",V),y.xrCompatible!==!0&&await e.makeXRCompatible(),v=t.getPixelRatio(),t.getSize(R),x&&"createProjectionLayer"in XRWebGLBinding.prototype){let rt=null,Ct=null,Ft=null;y.depth&&(Ft=y.stencil?e.DEPTH24_STENCIL8:e.DEPTH_COMPONENT24,rt=y.stencil?Ii:Bn,Ct=y.stencil?Fs:En);let Pt={colorFormat:e.RGBA8,depthFormat:Ft,scaleFactor:r};f=this.getBinding(),u=f.createProjectionLayer(Pt),s.updateRenderState({layers:[u]}),t.setPixelRatio(1),t.setSize(u.textureWidth,u.textureHeight,!1),b=new Le(u.textureWidth,u.textureHeight,{format:yn,type:mn,depthTexture:new ri(u.textureWidth,u.textureHeight,Ct,void 0,void 0,void 0,void 0,void 0,void 0,rt),stencilBuffer:y.stencil,colorSpace:t.outputColorSpace,samples:y.antialias?4:0,resolveDepthBuffer:u.ignoreDepthValues===!1,resolveStencilBuffer:u.ignoreDepthValues===!1})}else{let rt={antialias:y.antialias,alpha:!0,depth:y.depth,stencil:y.stencil,framebufferScaleFactor:r};p=new XRWebGLLayer(s,e,rt),s.updateRenderState({baseLayer:p}),t.setPixelRatio(1),t.setSize(p.framebufferWidth,p.framebufferHeight,!1),b=new Le(p.framebufferWidth,p.framebufferHeight,{format:yn,type:mn,colorSpace:t.outputColorSpace,stencilBuffer:y.stencil,resolveDepthBuffer:p.ignoreDepthValues===!1,resolveStencilBuffer:p.ignoreDepthValues===!1})}b.isXRRenderTarget=!0,this.setFoveation(l),c=null,a=await s.requestReferenceSpace(o),kt.setContext(s),kt.start(),n.isPresenting=!0,n.dispatchEvent({type:"sessionstart"})}},this.getEnvironmentBlendMode=function(){if(s!==null)return s.environmentBlendMode},this.getDepthTexture=function(){return m.getDepthTexture()};function V(J){for(let mt=0;mt<J.removed.length;mt++){let rt=J.removed[mt],Ct=w.indexOf(rt);Ct>=0&&(w[Ct]=null,T[Ct].disconnect(rt))}for(let mt=0;mt<J.added.length;mt++){let rt=J.added[mt],Ct=w.indexOf(rt);if(Ct===-1){for(let Pt=0;Pt<T.length;Pt++)if(Pt>=w.length){w.push(rt),Ct=Pt;break}else if(w[Pt]===null){w[Pt]=rt,Ct=Pt;break}if(Ct===-1)break}let Ft=T[Ct];Ft&&Ft.connect(rt)}}let $=new D,tt=new D;function ct(J,mt,rt){$.setFromMatrixPosition(mt.matrixWorld),tt.setFromMatrixPosition(rt.matrixWorld);let Ct=$.distanceTo(tt),Ft=mt.projectionMatrix.elements,Pt=rt.projectionMatrix.elements,pe=Ft[14]/(Ft[10]-1),qt=Ft[14]/(Ft[10]+1),ee=(Ft[9]+1)/Ft[5],ue=(Ft[9]-1)/Ft[5],Wt=(Ft[8]-1)/Ft[0],Pe=(Pt[8]+1)/Pt[0],me=pe*Wt,ln=pe*Pe,L=Ct/(-Wt+Pe),Ie=L*-Wt;if(mt.matrixWorld.decompose(J.position,J.quaternion,J.scale),J.translateX(Ie),J.translateZ(L),J.matrixWorld.compose(J.position,J.quaternion,J.scale),J.matrixWorldInverse.copy(J.matrixWorld).invert(),Ft[10]===-1)J.projectionMatrix.copy(mt.projectionMatrix),J.projectionMatrixInverse.copy(mt.projectionMatrixInverse);else{let Yt=pe+L,ce=qt+L,ht=me-Ie,_e=ln+(Ct-Ie),A=ee*qt/ce*Yt,_=ue*qt/ce*Yt;J.projectionMatrix.makePerspective(ht,_e,A,_,Yt,ce),J.projectionMatrixInverse.copy(J.projectionMatrix).invert()}}function Mt(J,mt){mt===null?J.matrixWorld.copy(J.matrix):J.matrixWorld.multiplyMatrices(mt.matrixWorld,J.matrix),J.matrixWorldInverse.copy(J.matrixWorld).invert()}this.updateCamera=function(J){if(s===null)return;let mt=J.near,rt=J.far;m.texture!==null&&(m.depthNear>0&&(mt=m.depthNear),m.depthFar>0&&(rt=m.depthFar)),N.near=I.near=E.near=mt,N.far=I.far=E.far=rt,(H!==N.near||W!==N.far)&&(s.updateRenderState({depthNear:N.near,depthFar:N.far}),H=N.near,W=N.far),N.layers.mask=J.layers.mask|6,E.layers.mask=N.layers.mask&-5,I.layers.mask=N.layers.mask&-3;let Ct=J.parent,Ft=N.cameras;Mt(N,Ct);for(let Pt=0;Pt<Ft.length;Pt++)Mt(Ft[Pt],Ct);Ft.length===2?ct(N,E,I):N.projectionMatrix.copy(E.projectionMatrix),St(J,N,Ct)};function St(J,mt,rt){rt===null?J.matrix.copy(mt.matrixWorld):(J.matrix.copy(rt.matrixWorld),J.matrix.invert(),J.matrix.multiply(mt.matrixWorld)),J.matrix.decompose(J.position,J.quaternion,J.scale),J.updateMatrixWorld(!0),J.projectionMatrix.copy(mt.projectionMatrix),J.projectionMatrixInverse.copy(mt.projectionMatrixInverse),J.isPerspectiveCamera&&(J.fov=Ha*2*Math.atan(1/J.projectionMatrix.elements[5]),J.zoom=1)}this.getCamera=function(){return N},this.getFoveation=function(){if(!(u===null&&p===null))return l},this.setFoveation=function(J){l=J,u!==null&&(u.fixedFoveation=J),p!==null&&p.fixedFoveation!==void 0&&(p.fixedFoveation=J)},this.hasDepthSensing=function(){return m.texture!==null},this.getDepthSensingMesh=function(){return m.getMesh(N)},this.getCameraTexture=function(J){return d[J]};let Xt=null;function te(J,mt){if(h=mt.getViewerPose(c||a),g=mt,h!==null){let rt=h.views;p!==null&&(t.setRenderTargetFramebuffer(b,p.framebuffer),t.setRenderTarget(b));let Ct=!1;rt.length!==N.cameras.length&&(N.cameras.length=0,Ct=!0);for(let qt=0;qt<rt.length;qt++){let ee=rt[qt],ue=null;if(p!==null)ue=p.getViewport(ee);else{let Pe=f.getViewSubImage(u,ee);ue=Pe.viewport,qt===0&&(t.setRenderTargetTextures(b,Pe.colorTexture,Pe.depthStencilTexture),t.setRenderTarget(b))}let Wt=C[qt];Wt===void 0&&(Wt=new Xe,Wt.layers.enable(qt),Wt.viewport=new ye,C[qt]=Wt),Wt.matrix.fromArray(ee.transform.matrix),Wt.matrix.decompose(Wt.position,Wt.quaternion,Wt.scale),Wt.projectionMatrix.fromArray(ee.projectionMatrix),Wt.projectionMatrixInverse.copy(Wt.projectionMatrix).invert(),Wt.viewport.set(ue.x,ue.y,ue.width,ue.height),qt===0&&(N.matrix.copy(Wt.matrix),N.matrix.decompose(N.position,N.quaternion,N.scale)),Ct===!0&&N.cameras.push(Wt)}let Ft=s.enabledFeatures;if(Ft&&Ft.includes("depth-sensing")&&s.depthUsage=="gpu-optimized"&&x){f=n.getBinding();let qt=f.getDepthInformation(rt[0]);qt&&qt.isValid&&qt.texture&&m.init(qt,s.renderState)}if(Ft&&Ft.includes("camera-access")&&x){t.state.unbindTexture(),f=n.getBinding();for(let qt=0;qt<rt.length;qt++){let ee=rt[qt].camera;if(ee){let ue=d[ee];ue||(ue=new hr,d[ee]=ue);let Wt=f.getCameraImage(ee);ue.sourceTexture=Wt}}}}for(let rt=0;rt<T.length;rt++){let Ct=w[rt],Ft=T[rt];Ct!==null&&Ft!==void 0&&Ft.update(Ct,mt,c||a)}Xt&&Xt(J,mt),mt.detectedPlanes&&n.dispatchEvent({type:"planesdetected",data:mt}),g=null}let kt=new zf;kt.setAnimationLoop(te),this.setAnimationLoop=function(J){Xt=J},this.dispose=function(){}}},qv=new ve,qf=new Dt;qf.set(-1,0,0,0,1,0,0,0,1);function Yv(i,t){function e(m,d){m.matrixAutoUpdate===!0&&m.updateMatrix(),d.value.copy(m.matrix)}function n(m,d){d.color.getRGB(m.fogColor.value,Vc(i)),d.isFog?(m.fogNear.value=d.near,m.fogFar.value=d.far):d.isFogExp2&&(m.fogDensity.value=d.density)}function s(m,d,y,S,b){d.isNodeMaterial?d.uniformsNeedUpdate=!1:d.isMeshBasicMaterial?r(m,d):d.isMeshLambertMaterial?(r(m,d),d.envMap&&(m.envMapIntensity.value=d.envMapIntensity)):d.isMeshToonMaterial?(r(m,d),f(m,d)):d.isMeshPhongMaterial?(r(m,d),h(m,d),d.envMap&&(m.envMapIntensity.value=d.envMapIntensity)):d.isMeshStandardMaterial?(r(m,d),u(m,d),d.isMeshPhysicalMaterial&&p(m,d,b)):d.isMeshMatcapMaterial?(r(m,d),g(m,d)):d.isMeshDepthMaterial?r(m,d):d.isMeshDistanceMaterial?(r(m,d),x(m,d)):d.isMeshNormalMaterial?r(m,d):d.isLineBasicMaterial?(a(m,d),d.isLineDashedMaterial&&o(m,d)):d.isPointsMaterial?l(m,d,y,S):d.isSpriteMaterial?c(m,d):d.isShadowMaterial?(m.color.value.copy(d.color),m.opacity.value=d.opacity):d.isShaderMaterial&&(d.uniformsNeedUpdate=!1)}function r(m,d){m.opacity.value=d.opacity,d.color&&m.diffuse.value.copy(d.color),d.emissive&&m.emissive.value.copy(d.emissive).multiplyScalar(d.emissiveIntensity),d.map&&(m.map.value=d.map,e(d.map,m.mapTransform)),d.alphaMap&&(m.alphaMap.value=d.alphaMap,e(d.alphaMap,m.alphaMapTransform)),d.bumpMap&&(m.bumpMap.value=d.bumpMap,e(d.bumpMap,m.bumpMapTransform),m.bumpScale.value=d.bumpScale,d.side===$e&&(m.bumpScale.value*=-1)),d.normalMap&&(m.normalMap.value=d.normalMap,e(d.normalMap,m.normalMapTransform),m.normalScale.value.copy(d.normalScale),d.side===$e&&m.normalScale.value.negate()),d.displacementMap&&(m.displacementMap.value=d.displacementMap,e(d.displacementMap,m.displacementMapTransform),m.displacementScale.value=d.displacementScale,m.displacementBias.value=d.displacementBias),d.emissiveMap&&(m.emissiveMap.value=d.emissiveMap,e(d.emissiveMap,m.emissiveMapTransform)),d.specularMap&&(m.specularMap.value=d.specularMap,e(d.specularMap,m.specularMapTransform)),d.alphaTest>0&&(m.alphaTest.value=d.alphaTest);let y=t.get(d),S=y.envMap,b=y.envMapRotation;S&&(m.envMap.value=S,m.envMapRotation.value.setFromMatrix4(qv.makeRotationFromEuler(b)).transpose(),S.isCubeTexture&&S.isRenderTargetTexture===!1&&m.envMapRotation.value.premultiply(qf),m.reflectivity.value=d.reflectivity,m.ior.value=d.ior,m.refractionRatio.value=d.refractionRatio),d.lightMap&&(m.lightMap.value=d.lightMap,m.lightMapIntensity.value=d.lightMapIntensity,e(d.lightMap,m.lightMapTransform)),d.aoMap&&(m.aoMap.value=d.aoMap,m.aoMapIntensity.value=d.aoMapIntensity,e(d.aoMap,m.aoMapTransform))}function a(m,d){m.diffuse.value.copy(d.color),m.opacity.value=d.opacity,d.map&&(m.map.value=d.map,e(d.map,m.mapTransform))}function o(m,d){m.dashSize.value=d.dashSize,m.totalSize.value=d.dashSize+d.gapSize,m.scale.value=d.scale}function l(m,d,y,S){m.diffuse.value.copy(d.color),m.opacity.value=d.opacity,m.size.value=d.size*y,m.scale.value=S*.5,d.map&&(m.map.value=d.map,e(d.map,m.uvTransform)),d.alphaMap&&(m.alphaMap.value=d.alphaMap,e(d.alphaMap,m.alphaMapTransform)),d.alphaTest>0&&(m.alphaTest.value=d.alphaTest)}function c(m,d){m.diffuse.value.copy(d.color),m.opacity.value=d.opacity,m.rotation.value=d.rotation,d.map&&(m.map.value=d.map,e(d.map,m.mapTransform)),d.alphaMap&&(m.alphaMap.value=d.alphaMap,e(d.alphaMap,m.alphaMapTransform)),d.alphaTest>0&&(m.alphaTest.value=d.alphaTest)}function h(m,d){m.specular.value.copy(d.specular),m.shininess.value=Math.max(d.shininess,1e-4)}function f(m,d){d.gradientMap&&(m.gradientMap.value=d.gradientMap)}function u(m,d){m.metalness.value=d.metalness,d.metalnessMap&&(m.metalnessMap.value=d.metalnessMap,e(d.metalnessMap,m.metalnessMapTransform)),m.roughness.value=d.roughness,d.roughnessMap&&(m.roughnessMap.value=d.roughnessMap,e(d.roughnessMap,m.roughnessMapTransform)),d.envMap&&(m.envMapIntensity.value=d.envMapIntensity)}function p(m,d,y){m.ior.value=d.ior,d.sheen>0&&(m.sheenColor.value.copy(d.sheenColor).multiplyScalar(d.sheen),m.sheenRoughness.value=d.sheenRoughness,d.sheenColorMap&&(m.sheenColorMap.value=d.sheenColorMap,e(d.sheenColorMap,m.sheenColorMapTransform)),d.sheenRoughnessMap&&(m.sheenRoughnessMap.value=d.sheenRoughnessMap,e(d.sheenRoughnessMap,m.sheenRoughnessMapTransform))),d.clearcoat>0&&(m.clearcoat.value=d.clearcoat,m.clearcoatRoughness.value=d.clearcoatRoughness,d.clearcoatMap&&(m.clearcoatMap.value=d.clearcoatMap,e(d.clearcoatMap,m.clearcoatMapTransform)),d.clearcoatRoughnessMap&&(m.clearcoatRoughnessMap.value=d.clearcoatRoughnessMap,e(d.clearcoatRoughnessMap,m.clearcoatRoughnessMapTransform)),d.clearcoatNormalMap&&(m.clearcoatNormalMap.value=d.clearcoatNormalMap,e(d.clearcoatNormalMap,m.clearcoatNormalMapTransform),m.clearcoatNormalScale.value.copy(d.clearcoatNormalScale),d.side===$e&&m.clearcoatNormalScale.value.negate())),d.dispersion>0&&(m.dispersion.value=d.dispersion),d.iridescence>0&&(m.iridescence.value=d.iridescence,m.iridescenceIOR.value=d.iridescenceIOR,m.iridescenceThicknessMinimum.value=d.iridescenceThicknessRange[0],m.iridescenceThicknessMaximum.value=d.iridescenceThicknessRange[1],d.iridescenceMap&&(m.iridescenceMap.value=d.iridescenceMap,e(d.iridescenceMap,m.iridescenceMapTransform)),d.iridescenceThicknessMap&&(m.iridescenceThicknessMap.value=d.iridescenceThicknessMap,e(d.iridescenceThicknessMap,m.iridescenceThicknessMapTransform))),d.transmission>0&&(m.transmission.value=d.transmission,m.transmissionSamplerMap.value=y.texture,m.transmissionSamplerSize.value.set(y.width,y.height),d.transmissionMap&&(m.transmissionMap.value=d.transmissionMap,e(d.transmissionMap,m.transmissionMapTransform)),m.thickness.value=d.thickness,d.thicknessMap&&(m.thicknessMap.value=d.thicknessMap,e(d.thicknessMap,m.thicknessMapTransform)),m.attenuationDistance.value=d.attenuationDistance,m.attenuationColor.value.copy(d.attenuationColor)),d.anisotropy>0&&(m.anisotropyVector.value.set(d.anisotropy*Math.cos(d.anisotropyRotation),d.anisotropy*Math.sin(d.anisotropyRotation)),d.anisotropyMap&&(m.anisotropyMap.value=d.anisotropyMap,e(d.anisotropyMap,m.anisotropyMapTransform))),m.specularIntensity.value=d.specularIntensity,m.specularColor.value.copy(d.specularColor),d.specularColorMap&&(m.specularColorMap.value=d.specularColorMap,e(d.specularColorMap,m.specularColorMapTransform)),d.specularIntensityMap&&(m.specularIntensityMap.value=d.specularIntensityMap,e(d.specularIntensityMap,m.specularIntensityMapTransform))}function g(m,d){d.matcap&&(m.matcap.value=d.matcap)}function x(m,d){let y=t.get(d).light;m.referencePosition.value.setFromMatrixPosition(y.matrixWorld),m.nearDistance.value=y.shadow.camera.near,m.farDistance.value=y.shadow.camera.far}return{refreshFogUniforms:n,refreshMaterialUniforms:s}}function Zv(i,t,e,n){let s={},r={},a=[],o=i.getParameter(i.MAX_UNIFORM_BUFFER_BINDINGS);function l(y,S){let b=S.program;n.uniformBlockBinding(y,b)}function c(y,S){let b=s[y.id];b===void 0&&(g(y),b=h(y),s[y.id]=b,y.addEventListener("dispose",m));let T=S.program;n.updateUBOMapping(y,T);let w=t.render.frame;r[y.id]!==w&&(u(y),r[y.id]=w)}function h(y){let S=f();y.__bindingPointIndex=S;let b=i.createBuffer(),T=y.__size,w=y.usage;return i.bindBuffer(i.UNIFORM_BUFFER,b),i.bufferData(i.UNIFORM_BUFFER,T,w),i.bindBuffer(i.UNIFORM_BUFFER,null),i.bindBufferBase(i.UNIFORM_BUFFER,S,b),b}function f(){for(let y=0;y<o;y++)if(a.indexOf(y)===-1)return a.push(y),y;return Rt("WebGLRenderer: Maximum number of simultaneously usable uniforms groups reached."),0}function u(y){let S=s[y.id],b=y.uniforms,T=y.__cache;i.bindBuffer(i.UNIFORM_BUFFER,S);for(let w=0,R=b.length;w<R;w++){let v=Array.isArray(b[w])?b[w]:[b[w]];for(let E=0,I=v.length;E<I;E++){let C=v[E];if(p(C,w,E,T)===!0){let N=C.__offset,H=Array.isArray(C.value)?C.value:[C.value],W=0;for(let U=0;U<H.length;U++){let z=H[U],V=x(z);typeof z=="number"||typeof z=="boolean"?(C.__data[0]=z,i.bufferSubData(i.UNIFORM_BUFFER,N+W,C.__data)):z.isMatrix3?(C.__data[0]=z.elements[0],C.__data[1]=z.elements[1],C.__data[2]=z.elements[2],C.__data[3]=0,C.__data[4]=z.elements[3],C.__data[5]=z.elements[4],C.__data[6]=z.elements[5],C.__data[7]=0,C.__data[8]=z.elements[6],C.__data[9]=z.elements[7],C.__data[10]=z.elements[8],C.__data[11]=0):ArrayBuffer.isView(z)?C.__data.set(new z.constructor(z.buffer,z.byteOffset,C.__data.length)):(z.toArray(C.__data,W),W+=V.storage/Float32Array.BYTES_PER_ELEMENT)}i.bufferSubData(i.UNIFORM_BUFFER,N,C.__data)}}}i.bindBuffer(i.UNIFORM_BUFFER,null)}function p(y,S,b,T){let w=y.value,R=S+"_"+b;if(T[R]===void 0)return typeof w=="number"||typeof w=="boolean"?T[R]=w:ArrayBuffer.isView(w)?T[R]=w.slice():T[R]=w.clone(),!0;{let v=T[R];if(typeof w=="number"||typeof w=="boolean"){if(v!==w)return T[R]=w,!0}else{if(ArrayBuffer.isView(w))return!0;if(v.equals(w)===!1)return v.copy(w),!0}}return!1}function g(y){let S=y.uniforms,b=0,T=16;for(let R=0,v=S.length;R<v;R++){let E=Array.isArray(S[R])?S[R]:[S[R]];for(let I=0,C=E.length;I<C;I++){let N=E[I],H=Array.isArray(N.value)?N.value:[N.value];for(let W=0,U=H.length;W<U;W++){let z=H[W],V=x(z),$=b%T,tt=$%V.boundary,ct=$+tt;b+=tt,ct!==0&&T-ct<V.storage&&(b+=T-ct),N.__data=new Float32Array(V.storage/Float32Array.BYTES_PER_ELEMENT),N.__offset=b,b+=V.storage}}}let w=b%T;return w>0&&(b+=T-w),y.__size=b,y.__cache={},this}function x(y){let S={boundary:0,storage:0};return typeof y=="number"||typeof y=="boolean"?(S.boundary=4,S.storage=4):y.isVector2?(S.boundary=8,S.storage=8):y.isVector3||y.isColor?(S.boundary=16,S.storage=12):y.isVector4?(S.boundary=16,S.storage=16):y.isMatrix3?(S.boundary=48,S.storage=48):y.isMatrix4?(S.boundary=64,S.storage=64):y.isTexture?Et("WebGLRenderer: Texture samplers can not be part of an uniforms group."):ArrayBuffer.isView(y)?(S.boundary=16,S.storage=y.byteLength):Et("WebGLRenderer: Unsupported uniform value type.",y),S}function m(y){let S=y.target;S.removeEventListener("dispose",m);let b=a.indexOf(S.__bindingPointIndex);a.splice(b,1),i.deleteBuffer(s[S.id]),delete s[S.id],delete r[S.id]}function d(){for(let y in s)i.deleteBuffer(s[y]);a=[],s={},r={}}return{bind:l,update:c,dispose:d}}var Jv=new Uint16Array([12469,15057,12620,14925,13266,14620,13807,14376,14323,13990,14545,13625,14713,13328,14840,12882,14931,12528,14996,12233,15039,11829,15066,11525,15080,11295,15085,10976,15082,10705,15073,10495,13880,14564,13898,14542,13977,14430,14158,14124,14393,13732,14556,13410,14702,12996,14814,12596,14891,12291,14937,11834,14957,11489,14958,11194,14943,10803,14921,10506,14893,10278,14858,9960,14484,14039,14487,14025,14499,13941,14524,13740,14574,13468,14654,13106,14743,12678,14818,12344,14867,11893,14889,11509,14893,11180,14881,10751,14852,10428,14812,10128,14765,9754,14712,9466,14764,13480,14764,13475,14766,13440,14766,13347,14769,13070,14786,12713,14816,12387,14844,11957,14860,11549,14868,11215,14855,10751,14825,10403,14782,10044,14729,9651,14666,9352,14599,9029,14967,12835,14966,12831,14963,12804,14954,12723,14936,12564,14917,12347,14900,11958,14886,11569,14878,11247,14859,10765,14828,10401,14784,10011,14727,9600,14660,9289,14586,8893,14508,8533,15111,12234,15110,12234,15104,12216,15092,12156,15067,12010,15028,11776,14981,11500,14942,11205,14902,10752,14861,10393,14812,9991,14752,9570,14682,9252,14603,8808,14519,8445,14431,8145,15209,11449,15208,11451,15202,11451,15190,11438,15163,11384,15117,11274,15055,10979,14994,10648,14932,10343,14871,9936,14803,9532,14729,9218,14645,8742,14556,8381,14461,8020,14365,7603,15273,10603,15272,10607,15267,10619,15256,10631,15231,10614,15182,10535,15118,10389,15042,10167,14963,9787,14883,9447,14800,9115,14710,8665,14615,8318,14514,7911,14411,7507,14279,7198,15314,9675,15313,9683,15309,9712,15298,9759,15277,9797,15229,9773,15166,9668,15084,9487,14995,9274,14898,8910,14800,8539,14697,8234,14590,7790,14479,7409,14367,7067,14178,6621,15337,8619,15337,8631,15333,8677,15325,8769,15305,8871,15264,8940,15202,8909,15119,8775,15022,8565,14916,8328,14804,8009,14688,7614,14569,7287,14448,6888,14321,6483,14088,6171,15350,7402,15350,7419,15347,7480,15340,7613,15322,7804,15287,7973,15229,8057,15148,8012,15046,7846,14933,7611,14810,7357,14682,7069,14552,6656,14421,6316,14251,5948,14007,5528,15356,5942,15356,5977,15353,6119,15348,6294,15332,6551,15302,6824,15249,7044,15171,7122,15070,7050,14949,6861,14818,6611,14679,6349,14538,6067,14398,5651,14189,5311,13935,4958,15359,4123,15359,4153,15356,4296,15353,4646,15338,5160,15311,5508,15263,5829,15188,6042,15088,6094,14966,6001,14826,5796,14678,5543,14527,5287,14377,4985,14133,4586,13869,4257,15360,1563,15360,1642,15358,2076,15354,2636,15341,3350,15317,4019,15273,4429,15203,4732,15105,4911,14981,4932,14836,4818,14679,4621,14517,4386,14359,4156,14083,3795,13808,3437,15360,122,15360,137,15358,285,15355,636,15344,1274,15322,2177,15281,2765,15215,3223,15120,3451,14995,3569,14846,3567,14681,3466,14511,3305,14344,3121,14037,2800,13753,2467,15360,0,15360,1,15359,21,15355,89,15346,253,15325,479,15287,796,15225,1148,15133,1492,15008,1749,14856,1882,14685,1886,14506,1783,14324,1608,13996,1398,13702,1183]),Vn=null;function $v(){return Vn===null&&(Vn=new Ya(Jv,16,16,Li,qe),Vn.name="DFG_LUT",Vn.minFilter=ze,Vn.magFilter=ze,Vn.wrapS=Un,Vn.wrapT=Un,Vn.generateMipmaps=!1,Vn.needsUpdate=!0),Vn}var al=class{constructor(t={}){let{canvas:e=ff(),context:n=null,depth:s=!0,stencil:r=!1,alpha:a=!1,antialias:o=!1,premultipliedAlpha:l=!0,preserveDrawingBuffer:c=!1,powerPreference:h="default",failIfMajorPerformanceCaveat:f=!1,reversedDepthBuffer:u=!1,outputBufferType:p=mn}=t;this.isWebGLRenderer=!0;let g;if(n!==null){if(typeof WebGLRenderingContext<"u"&&n instanceof WebGLRenderingContext)throw new Error("THREE.WebGLRenderer: WebGL 1 is not supported since r163.");g=n.getContextAttributes().alpha}else g=a;let x=p,m=new Set([So,bo,Mo]),d=new Set([mn,En,Ds,Fs,vo,yo]),y=new Uint32Array(4),S=new Int32Array(4),b=new D,T=null,w=null,R=[],v=[],E=null;this.domElement=e,this.debug={checkShaderErrors:!0,onShaderError:null},this.autoClear=!0,this.autoClearColor=!0,this.autoClearDepth=!0,this.autoClearStencil=!0,this.sortObjects=!0,this.clippingPlanes=[],this.localClippingEnabled=!1,this.toneMapping=pn,this.toneMappingExposure=1,this.transmissionResolutionScale=1;let I=this,C=!1,N=null;this._outputColorSpace=fn;let H=0,W=0,U=null,z=-1,V=null,$=new ye,tt=new ye,ct=null,Mt=new ut(0),St=0,Xt=e.width,te=e.height,kt=1,J=null,mt=null,rt=new ye(0,0,Xt,te),Ct=new ye(0,0,Xt,te),Ft=!1,Pt=new lr,pe=!1,qt=!1,ee=new ve,ue=new D,Wt=new ye,Pe={background:null,fog:null,environment:null,overrideMaterial:null,isScene:!0},me=!1;function ln(){return U===null?kt:1}let L=n;function Ie(M,F){return e.getContext(M,F)}try{let M={alpha:!0,depth:s,stencil:r,antialias:o,premultipliedAlpha:l,preserveDrawingBuffer:c,powerPreference:h,failIfMajorPerformanceCaveat:f};if("setAttribute"in e&&e.setAttribute("data-engine",`three.js r${po}`),e.addEventListener("webglcontextlost",K,!1),e.addEventListener("webglcontextrestored",wt,!1),e.addEventListener("webglcontextcreationerror",Ot,!1),L===null){let F="webgl2";if(L=Ie(F,M),L===null)throw Ie(F)?new Error("Error creating WebGL context with your selected attributes."):new Error("Error creating WebGL context.")}}catch(M){throw Rt("WebGLRenderer: "+M.message),M}let Yt,ce,ht,_e,A,_,O,Y,j,et,lt,X,Z,gt,vt,at,nt,Nt,zt,$t,P,it,q;function _t(){Yt=new ix(L),Yt.init(),P=new Hv(L,Yt),ce=new J_(L,Yt,t,P),ht=new Vv(L,Yt),ce.reversedDepthBuffer&&u&&ht.buffers.depth.setReversed(!0),_e=new ax(L),A=new Ev,_=new Gv(L,Yt,ht,A,ce,P,_e),O=new nx(I),Y=new hg(L),it=new Y_(L,Y),j=new sx(L,Y,_e,it),et=new lx(L,j,Y,it,_e),Nt=new ox(L,ce,_),vt=new $_(A),lt=new Tv(I,O,Yt,ce,it,vt),X=new Yv(I,A),Z=new Rv,gt=new Fv(Yt),nt=new q_(I,O,ht,et,g,l),at=new zv(I,et,ce),q=new Zv(L,_e,ce,ht),zt=new Z_(L,Yt,_e),$t=new rx(L,Yt,_e),_e.programs=lt.programs,I.capabilities=ce,I.extensions=Yt,I.properties=A,I.renderLists=Z,I.shadowMap=at,I.state=ht,I.info=_e}_t(),x!==mn&&(E=new hx(x,e.width,e.height,s,r));let ot=new hh(I,L);this.xr=ot,this.getContext=function(){return L},this.getContextAttributes=function(){return L.getContextAttributes()},this.forceContextLoss=function(){let M=Yt.get("WEBGL_lose_context");M&&M.loseContext()},this.forceContextRestore=function(){let M=Yt.get("WEBGL_lose_context");M&&M.restoreContext()},this.getPixelRatio=function(){return kt},this.setPixelRatio=function(M){M!==void 0&&(kt=M,this.setSize(Xt,te,!1))},this.getSize=function(M){return M.set(Xt,te)},this.setSize=function(M,F,G=!0){if(ot.isPresenting){Et("WebGLRenderer: Can't change size while VR device is presenting.");return}Xt=M,te=F,e.width=Math.floor(M*kt),e.height=Math.floor(F*kt),G===!0&&(e.style.width=M+"px",e.style.height=F+"px"),E!==null&&E.setSize(e.width,e.height),this.setViewport(0,0,M,F)},this.getDrawingBufferSize=function(M){return M.set(Xt*kt,te*kt).floor()},this.setDrawingBufferSize=function(M,F,G){Xt=M,te=F,kt=G,e.width=Math.floor(M*G),e.height=Math.floor(F*G),this.setViewport(0,0,M,F)},this.setEffects=function(M){if(x===mn){Rt("THREE.WebGLRenderer: setEffects() requires outputBufferType set to HalfFloatType or FloatType.");return}if(M){for(let F=0;F<M.length;F++)if(M[F].isOutputPass===!0){Et("THREE.WebGLRenderer: OutputPass is not needed in setEffects(). Tone mapping and color space conversion are applied automatically.");break}}E.setEffects(M||[])},this.getCurrentViewport=function(M){return M.copy($)},this.getViewport=function(M){return M.copy(rt)},this.setViewport=function(M,F,G,B){M.isVector4?rt.set(M.x,M.y,M.z,M.w):rt.set(M,F,G,B),ht.viewport($.copy(rt).multiplyScalar(kt).round())},this.getScissor=function(M){return M.copy(Ct)},this.setScissor=function(M,F,G,B){M.isVector4?Ct.set(M.x,M.y,M.z,M.w):Ct.set(M,F,G,B),ht.scissor(tt.copy(Ct).multiplyScalar(kt).round())},this.getScissorTest=function(){return Ft},this.setScissorTest=function(M){ht.setScissorTest(Ft=M)},this.setOpaqueSort=function(M){J=M},this.setTransparentSort=function(M){mt=M},this.getClearColor=function(M){return M.copy(nt.getClearColor())},this.setClearColor=function(){nt.setClearColor(...arguments)},this.getClearAlpha=function(){return nt.getClearAlpha()},this.setClearAlpha=function(){nt.setClearAlpha(...arguments)},this.clear=function(M=!0,F=!0,G=!0){let B=0;if(M){let k=!1;if(U!==null){let pt=U.texture.format;k=m.has(pt)}if(k){let pt=U.texture.type,yt=d.has(pt),dt=nt.getClearColor(),bt=nt.getClearAlpha(),At=dt.r,Bt=dt.g,Gt=dt.b;yt?(y[0]=At,y[1]=Bt,y[2]=Gt,y[3]=bt,L.clearBufferuiv(L.COLOR,0,y)):(S[0]=At,S[1]=Bt,S[2]=Gt,S[3]=bt,L.clearBufferiv(L.COLOR,0,S))}else B|=L.COLOR_BUFFER_BIT}F&&(B|=L.DEPTH_BUFFER_BIT,this.state.buffers.depth.setMask(!0)),G&&(B|=L.STENCIL_BUFFER_BIT,this.state.buffers.stencil.setMask(4294967295)),B!==0&&L.clear(B)},this.clearColor=function(){this.clear(!0,!1,!1)},this.clearDepth=function(){this.clear(!1,!0,!1)},this.clearStencil=function(){this.clear(!1,!1,!0)},this.setNodesHandler=function(M){M.setRenderer(this),N=M},this.dispose=function(){e.removeEventListener("webglcontextlost",K,!1),e.removeEventListener("webglcontextrestored",wt,!1),e.removeEventListener("webglcontextcreationerror",Ot,!1),nt.dispose(),Z.dispose(),gt.dispose(),A.dispose(),O.dispose(),et.dispose(),it.dispose(),q.dispose(),lt.dispose(),ot.dispose(),ot.removeEventListener("sessionstart",eu),ot.removeEventListener("sessionend",nu),Zi.stop()};function K(M){M.preventDefault(),zc("WebGLRenderer: Context Lost."),C=!0}function wt(){zc("WebGLRenderer: Context Restored."),C=!1;let M=_e.autoReset,F=at.enabled,G=at.autoUpdate,B=at.needsUpdate,k=at.type;_t(),_e.autoReset=M,at.enabled=F,at.autoUpdate=G,at.needsUpdate=B,at.type=k}function Ot(M){Rt("WebGLRenderer: A WebGL context could not be created. Reason: ",M.statusMessage)}function Se(M){let F=M.target;F.removeEventListener("dispose",Se),ne(F)}function ne(M){Yn(M),A.remove(M)}function Yn(M){let F=A.get(M).programs;F!==void 0&&(F.forEach(function(G){lt.releaseProgram(G)}),M.isShaderMaterial&&lt.releaseShaderCache(M))}this.renderBufferDirect=function(M,F,G,B,k,pt){F===null&&(F=Pe);let yt=k.isMesh&&k.matrixWorld.determinant()<0,dt=bm(M,F,G,B,k);ht.setMaterial(B,yt);let bt=G.index,At=1;if(B.wireframe===!0){if(bt=j.getWireframeAttribute(G),bt===void 0)return;At=2}let Bt=G.drawRange,Gt=G.attributes.position,Tt=Bt.start*At,ie=(Bt.start+Bt.count)*At;pt!==null&&(Tt=Math.max(Tt,pt.start*At),ie=Math.min(ie,(pt.start+pt.count)*At)),bt!==null?(Tt=Math.max(Tt,0),ie=Math.min(ie,bt.count)):Gt!=null&&(Tt=Math.max(Tt,0),ie=Math.min(ie,Gt.count));let we=ie-Tt;if(we<0||we===1/0)return;it.setup(k,B,dt,G,bt);let xe,ae=zt;if(bt!==null&&(xe=Y.get(bt),ae=$t,ae.setIndex(xe)),k.isMesh)B.wireframe===!0?(ht.setLineWidth(B.wireframeLinewidth*ln()),ae.setMode(L.LINES)):ae.setMode(L.TRIANGLES);else if(k.isLine){let Ge=B.linewidth;Ge===void 0&&(Ge=1),ht.setLineWidth(Ge*ln()),k.isLineSegments?ae.setMode(L.LINES):k.isLineLoop?ae.setMode(L.LINE_LOOP):ae.setMode(L.LINE_STRIP)}else k.isPoints?ae.setMode(L.POINTS):k.isSprite&&ae.setMode(L.TRIANGLES);if(k.isBatchedMesh)if(Yt.get("WEBGL_multi_draw"))ae.renderMultiDraw(k._multiDrawStarts,k._multiDrawCounts,k._multiDrawCount);else{let Ge=k._multiDrawStarts,xt=k._multiDrawCounts,cn=k._multiDrawCount,Jt=bt?Y.get(bt).bytesPerElement:1,_n=A.get(B).currentProgram.getUniforms();for(let Nn=0;Nn<cn;Nn++)_n.setValue(L,"_gl_DrawID",Nn),ae.render(Ge[Nn]/Jt,xt[Nn])}else if(k.isInstancedMesh)ae.renderInstances(Tt,we,k.count);else if(G.isInstancedBufferGeometry){let Ge=G._maxInstanceCount!==void 0?G._maxInstanceCount:1/0,xt=Math.min(G.instanceCount,Ge);ae.renderInstances(Tt,we,xt)}else ae.render(Tt,we)};function Ln(M,F,G){M.transparent===!0&&M.side===zn&&M.forceSinglePass===!1?(M.side=$e,M.needsUpdate=!0,sa(M,F,G),M.side=ei,M.needsUpdate=!0,sa(M,F,G),M.side=zn):sa(M,F,G)}this.compile=function(M,F,G=null){G===null&&(G=M),w=gt.get(G),w.init(F),v.push(w),G.traverseVisible(function(k){k.isLight&&k.layers.test(F.layers)&&(w.pushLight(k),k.castShadow&&w.pushShadow(k))}),M!==G&&M.traverseVisible(function(k){k.isLight&&k.layers.test(F.layers)&&(w.pushLight(k),k.castShadow&&w.pushShadow(k))}),w.setupLights();let B=new Set;return M.traverse(function(k){if(!(k.isMesh||k.isPoints||k.isLine||k.isSprite))return;let pt=k.material;if(pt)if(Array.isArray(pt))for(let yt=0;yt<pt.length;yt++){let dt=pt[yt];Ln(dt,G,k),B.add(dt)}else Ln(pt,G,k),B.add(pt)}),w=v.pop(),B},this.compileAsync=function(M,F,G=null){let B=this.compile(M,F,G);return new Promise(k=>{function pt(){if(B.forEach(function(yt){A.get(yt).currentProgram.isReady()&&B.delete(yt)}),B.size===0){k(M);return}setTimeout(pt,10)}Yt.get("KHR_parallel_shader_compile")!==null?pt():setTimeout(pt,10)})};let Xl=null;function ym(M){Xl&&Xl(M)}function eu(){Zi.stop()}function nu(){Zi.start()}let Zi=new zf;Zi.setAnimationLoop(ym),typeof self<"u"&&Zi.setContext(self),this.setAnimationLoop=function(M){Xl=M,ot.setAnimationLoop(M),M===null?Zi.stop():Zi.start()},ot.addEventListener("sessionstart",eu),ot.addEventListener("sessionend",nu),this.render=function(M,F){if(F!==void 0&&F.isCamera!==!0){Rt("WebGLRenderer.render: camera is not an instance of THREE.Camera.");return}if(C===!0)return;N!==null&&N.renderStart(M,F);let G=ot.enabled===!0&&ot.isPresenting===!0,B=E!==null&&(U===null||G)&&E.begin(I,U);if(M.matrixWorldAutoUpdate===!0&&M.updateMatrixWorld(),F.parent===null&&F.matrixWorldAutoUpdate===!0&&F.updateMatrixWorld(),ot.enabled===!0&&ot.isPresenting===!0&&(E===null||E.isCompositing()===!1)&&(ot.cameraAutoUpdate===!0&&ot.updateCamera(F),F=ot.getCamera()),M.isScene===!0&&M.onBeforeRender(I,M,F,U),w=gt.get(M,v.length),w.init(F),w.state.textureUnits=_.getTextureUnits(),v.push(w),ee.multiplyMatrices(F.projectionMatrix,F.matrixWorldInverse),Pt.setFromProjectionMatrix(ee,An,F.reversedDepth),qt=this.localClippingEnabled,pe=vt.init(this.clippingPlanes,qt),T=Z.get(M,R.length),T.init(),R.push(T),ot.enabled===!0&&ot.isPresenting===!0){let yt=I.xr.getDepthSensingMesh();yt!==null&&ql(yt,F,-1/0,I.sortObjects)}ql(M,F,0,I.sortObjects),T.finish(),I.sortObjects===!0&&T.sort(J,mt),me=ot.enabled===!1||ot.isPresenting===!1||ot.hasDepthSensing()===!1,me&&nt.addToRenderList(T,M),this.info.render.frame++,pe===!0&&vt.beginShadows();let k=w.state.shadowsArray;if(at.render(k,M,F),pe===!0&&vt.endShadows(),this.info.autoReset===!0&&this.info.reset(),(B&&E.hasRenderPass())===!1){let yt=T.opaque,dt=T.transmissive;if(w.setupLights(),F.isArrayCamera){let bt=F.cameras;if(dt.length>0)for(let At=0,Bt=bt.length;At<Bt;At++){let Gt=bt[At];su(yt,dt,M,Gt)}me&&nt.render(M);for(let At=0,Bt=bt.length;At<Bt;At++){let Gt=bt[At];iu(T,M,Gt,Gt.viewport)}}else dt.length>0&&su(yt,dt,M,F),me&&nt.render(M),iu(T,M,F)}U!==null&&W===0&&(_.updateMultisampleRenderTarget(U),_.updateRenderTargetMipmap(U)),B&&E.end(I),M.isScene===!0&&M.onAfterRender(I,M,F),it.resetDefaultState(),z=-1,V=null,v.pop(),v.length>0?(w=v[v.length-1],_.setTextureUnits(w.state.textureUnits),pe===!0&&vt.setGlobalState(I.clippingPlanes,w.state.camera)):w=null,R.pop(),R.length>0?T=R[R.length-1]:T=null,N!==null&&N.renderEnd()};function ql(M,F,G,B){if(M.visible===!1)return;if(M.layers.test(F.layers)){if(M.isGroup)G=M.renderOrder;else if(M.isLOD)M.autoUpdate===!0&&M.update(F);else if(M.isLightProbeGrid)w.pushLightProbeGrid(M);else if(M.isLight)w.pushLight(M),M.castShadow&&w.pushShadow(M);else if(M.isSprite){if(!M.frustumCulled||Pt.intersectsSprite(M)){B&&Wt.setFromMatrixPosition(M.matrixWorld).applyMatrix4(ee);let yt=et.update(M),dt=M.material;dt.visible&&T.push(M,yt,dt,G,Wt.z,null)}}else if((M.isMesh||M.isLine||M.isPoints)&&(!M.frustumCulled||Pt.intersectsObject(M))){let yt=et.update(M),dt=M.material;if(B&&(M.boundingSphere!==void 0?(M.boundingSphere===null&&M.computeBoundingSphere(),Wt.copy(M.boundingSphere.center)):(yt.boundingSphere===null&&yt.computeBoundingSphere(),Wt.copy(yt.boundingSphere.center)),Wt.applyMatrix4(M.matrixWorld).applyMatrix4(ee)),Array.isArray(dt)){let bt=yt.groups;for(let At=0,Bt=bt.length;At<Bt;At++){let Gt=bt[At],Tt=dt[Gt.materialIndex];Tt&&Tt.visible&&T.push(M,yt,Tt,G,Wt.z,Gt)}}else dt.visible&&T.push(M,yt,dt,G,Wt.z,null)}}let pt=M.children;for(let yt=0,dt=pt.length;yt<dt;yt++)ql(pt[yt],F,G,B)}function iu(M,F,G,B){let{opaque:k,transmissive:pt,transparent:yt}=M;w.setupLightsView(G),pe===!0&&vt.setGlobalState(I.clippingPlanes,G),B&&ht.viewport($.copy(B)),k.length>0&&ia(k,F,G),pt.length>0&&ia(pt,F,G),yt.length>0&&ia(yt,F,G),ht.buffers.depth.setTest(!0),ht.buffers.depth.setMask(!0),ht.buffers.color.setMask(!0),ht.setPolygonOffset(!1)}function su(M,F,G,B){if((G.isScene===!0?G.overrideMaterial:null)!==null)return;if(w.state.transmissionRenderTarget[B.id]===void 0){let Tt=Yt.has("EXT_color_buffer_half_float")||Yt.has("EXT_color_buffer_float");w.state.transmissionRenderTarget[B.id]=new Le(1,1,{generateMipmaps:!0,type:Tt?qe:mn,minFilter:Pi,samples:Math.max(4,ce.samples),stencilBuffer:r,resolveDepthBuffer:!1,resolveStencilBuffer:!1,colorSpace:Ht.workingColorSpace})}let pt=w.state.transmissionRenderTarget[B.id],yt=B.viewport||$;pt.setSize(yt.z*I.transmissionResolutionScale,yt.w*I.transmissionResolutionScale);let dt=I.getRenderTarget(),bt=I.getActiveCubeFace(),At=I.getActiveMipmapLevel();I.setRenderTarget(pt),I.getClearColor(Mt),St=I.getClearAlpha(),St<1&&I.setClearColor(16777215,.5),I.clear(),me&&nt.render(G);let Bt=I.toneMapping;I.toneMapping=pn;let Gt=B.viewport;if(B.viewport!==void 0&&(B.viewport=void 0),w.setupLightsView(B),pe===!0&&vt.setGlobalState(I.clippingPlanes,B),ia(M,G,B),_.updateMultisampleRenderTarget(pt),_.updateRenderTargetMipmap(pt),Yt.has("WEBGL_multisampled_render_to_texture")===!1){let Tt=!1;for(let ie=0,we=F.length;ie<we;ie++){let xe=F[ie],{object:ae,geometry:Ge,material:xt,group:cn}=xe;if(xt.side===zn&&ae.layers.test(B.layers)){let Jt=xt.side;xt.side=$e,xt.needsUpdate=!0,ru(ae,G,B,Ge,xt,cn),xt.side=Jt,xt.needsUpdate=!0,Tt=!0}}Tt===!0&&(_.updateMultisampleRenderTarget(pt),_.updateRenderTargetMipmap(pt))}I.setRenderTarget(dt,bt,At),I.setClearColor(Mt,St),Gt!==void 0&&(B.viewport=Gt),I.toneMapping=Bt}function ia(M,F,G){let B=F.isScene===!0?F.overrideMaterial:null;for(let k=0,pt=M.length;k<pt;k++){let yt=M[k],{object:dt,geometry:bt,group:At}=yt,Bt=yt.material;Bt.allowOverride===!0&&B!==null&&(Bt=B),dt.layers.test(G.layers)&&ru(dt,F,G,bt,Bt,At)}}function ru(M,F,G,B,k,pt){M.onBeforeRender(I,F,G,B,k,pt),M.modelViewMatrix.multiplyMatrices(G.matrixWorldInverse,M.matrixWorld),M.normalMatrix.getNormalMatrix(M.modelViewMatrix),k.onBeforeRender(I,F,G,B,M,pt),k.transparent===!0&&k.side===zn&&k.forceSinglePass===!1?(k.side=$e,k.needsUpdate=!0,I.renderBufferDirect(G,F,B,k,M,pt),k.side=ei,k.needsUpdate=!0,I.renderBufferDirect(G,F,B,k,M,pt),k.side=zn):I.renderBufferDirect(G,F,B,k,M,pt),M.onAfterRender(I,F,G,B,k,pt)}function sa(M,F,G){F.isScene!==!0&&(F=Pe);let B=A.get(M),k=w.state.lights,pt=w.state.shadowsArray,yt=k.state.version,dt=lt.getParameters(M,k.state,pt,F,G,w.state.lightProbeGridArray),bt=lt.getProgramCacheKey(dt),At=B.programs;B.environment=M.isMeshStandardMaterial||M.isMeshLambertMaterial||M.isMeshPhongMaterial?F.environment:null,B.fog=F.fog;let Bt=M.isMeshStandardMaterial||M.isMeshLambertMaterial&&!M.envMap||M.isMeshPhongMaterial&&!M.envMap;B.envMap=O.get(M.envMap||B.environment,Bt),B.envMapRotation=B.environment!==null&&M.envMap===null?F.environmentRotation:M.envMapRotation,At===void 0&&(M.addEventListener("dispose",Se),At=new Map,B.programs=At);let Gt=At.get(bt);if(Gt!==void 0){if(B.currentProgram===Gt&&B.lightsStateVersion===yt)return ou(M,dt),Gt}else dt.uniforms=lt.getUniforms(M),N!==null&&M.isNodeMaterial&&N.build(M,G,dt),M.onBeforeCompile(dt,I),Gt=lt.acquireProgram(dt,bt),At.set(bt,Gt),B.uniforms=dt.uniforms;let Tt=B.uniforms;return(!M.isShaderMaterial&&!M.isRawShaderMaterial||M.clipping===!0)&&(Tt.clippingPlanes=vt.uniform),ou(M,dt),B.needsLights=wm(M),B.lightsStateVersion=yt,B.needsLights&&(Tt.ambientLightColor.value=k.state.ambient,Tt.lightProbe.value=k.state.probe,Tt.directionalLights.value=k.state.directional,Tt.directionalLightShadows.value=k.state.directionalShadow,Tt.spotLights.value=k.state.spot,Tt.spotLightShadows.value=k.state.spotShadow,Tt.rectAreaLights.value=k.state.rectArea,Tt.ltc_1.value=k.state.rectAreaLTC1,Tt.ltc_2.value=k.state.rectAreaLTC2,Tt.pointLights.value=k.state.point,Tt.pointLightShadows.value=k.state.pointShadow,Tt.hemisphereLights.value=k.state.hemi,Tt.directionalShadowMatrix.value=k.state.directionalShadowMatrix,Tt.spotLightMatrix.value=k.state.spotLightMatrix,Tt.spotLightMap.value=k.state.spotLightMap,Tt.pointShadowMatrix.value=k.state.pointShadowMatrix),B.lightProbeGrid=w.state.lightProbeGridArray.length>0,B.currentProgram=Gt,B.uniformsList=null,Gt}function au(M){if(M.uniformsList===null){let F=M.currentProgram.getUniforms();M.uniformsList=Os.seqWithValue(F.seq,M.uniforms)}return M.uniformsList}function ou(M,F){let G=A.get(M);G.outputColorSpace=F.outputColorSpace,G.batching=F.batching,G.batchingColor=F.batchingColor,G.instancing=F.instancing,G.instancingColor=F.instancingColor,G.instancingMorph=F.instancingMorph,G.skinning=F.skinning,G.morphTargets=F.morphTargets,G.morphNormals=F.morphNormals,G.morphColors=F.morphColors,G.morphTargetsCount=F.morphTargetsCount,G.numClippingPlanes=F.numClippingPlanes,G.numIntersection=F.numClipIntersection,G.vertexAlphas=F.vertexAlphas,G.vertexTangents=F.vertexTangents,G.toneMapping=F.toneMapping}function Mm(M,F){if(M.length===0)return null;if(M.length===1)return M[0].texture!==null?M[0]:null;b.setFromMatrixPosition(F.matrixWorld);for(let G=0,B=M.length;G<B;G++){let k=M[G];if(k.texture!==null&&k.boundingBox.containsPoint(b))return k}return null}function bm(M,F,G,B,k){F.isScene!==!0&&(F=Pe),_.resetTextureUnits();let pt=F.fog,yt=B.isMeshStandardMaterial||B.isMeshLambertMaterial||B.isMeshPhongMaterial?F.environment:null,dt=U===null?I.outputColorSpace:U.isXRRenderTarget===!0?U.texture.colorSpace:Ht.workingColorSpace,bt=B.isMeshStandardMaterial||B.isMeshLambertMaterial&&!B.envMap||B.isMeshPhongMaterial&&!B.envMap,At=O.get(B.envMap||yt,bt),Bt=B.vertexColors===!0&&!!G.attributes.color&&G.attributes.color.itemSize===4,Gt=!!G.attributes.tangent&&(!!B.normalMap||B.anisotropy>0),Tt=!!G.morphAttributes.position,ie=!!G.morphAttributes.normal,we=!!G.morphAttributes.color,xe=pn;B.toneMapped&&(U===null||U.isXRRenderTarget===!0)&&(xe=I.toneMapping);let ae=G.morphAttributes.position||G.morphAttributes.normal||G.morphAttributes.color,Ge=ae!==void 0?ae.length:0,xt=A.get(B),cn=w.state.lights;if(pe===!0&&(qt===!0||M!==V)){let he=M===V&&B.id===z;vt.setState(B,M,he)}let Jt=!1;B.version===xt.__version?(xt.needsLights&&xt.lightsStateVersion!==cn.state.version||xt.outputColorSpace!==dt||k.isBatchedMesh&&xt.batching===!1||!k.isBatchedMesh&&xt.batching===!0||k.isBatchedMesh&&xt.batchingColor===!0&&k.colorTexture===null||k.isBatchedMesh&&xt.batchingColor===!1&&k.colorTexture!==null||k.isInstancedMesh&&xt.instancing===!1||!k.isInstancedMesh&&xt.instancing===!0||k.isSkinnedMesh&&xt.skinning===!1||!k.isSkinnedMesh&&xt.skinning===!0||k.isInstancedMesh&&xt.instancingColor===!0&&k.instanceColor===null||k.isInstancedMesh&&xt.instancingColor===!1&&k.instanceColor!==null||k.isInstancedMesh&&xt.instancingMorph===!0&&k.morphTexture===null||k.isInstancedMesh&&xt.instancingMorph===!1&&k.morphTexture!==null||xt.envMap!==At||B.fog===!0&&xt.fog!==pt||xt.numClippingPlanes!==void 0&&(xt.numClippingPlanes!==vt.numPlanes||xt.numIntersection!==vt.numIntersection)||xt.vertexAlphas!==Bt||xt.vertexTangents!==Gt||xt.morphTargets!==Tt||xt.morphNormals!==ie||xt.morphColors!==we||xt.toneMapping!==xe||xt.morphTargetsCount!==Ge||!!xt.lightProbeGrid!=w.state.lightProbeGridArray.length>0)&&(Jt=!0):(Jt=!0,xt.__version=B.version);let _n=xt.currentProgram;Jt===!0&&(_n=sa(B,F,k),N&&B.isNodeMaterial&&N.onUpdateProgram(B,_n,xt));let Nn=!1,ui=!1,fs=!1,oe=_n.getUniforms(),Ae=xt.uniforms;if(ht.useProgram(_n.program)&&(Nn=!0,ui=!0,fs=!0),B.id!==z&&(z=B.id,ui=!0),xt.needsLights){let he=Mm(w.state.lightProbeGridArray,k);xt.lightProbeGrid!==he&&(xt.lightProbeGrid=he,ui=!0)}if(Nn||V!==M){ht.buffers.depth.getReversed()&&M.reversedDepth!==!0&&(M._reversedDepth=!0,M.updateProjectionMatrix()),oe.setValue(L,"projectionMatrix",M.projectionMatrix),oe.setValue(L,"viewMatrix",M.matrixWorldInverse);let di=oe.map.cameraPosition;di!==void 0&&di.setValue(L,ue.setFromMatrixPosition(M.matrixWorld)),ce.logarithmicDepthBuffer&&oe.setValue(L,"logDepthBufFC",2/(Math.log(M.far+1)/Math.LN2)),(B.isMeshPhongMaterial||B.isMeshToonMaterial||B.isMeshLambertMaterial||B.isMeshBasicMaterial||B.isMeshStandardMaterial||B.isShaderMaterial)&&oe.setValue(L,"isOrthographic",M.isOrthographicCamera===!0),V!==M&&(V=M,ui=!0,fs=!0)}if(xt.needsLights&&(cn.state.directionalShadowMap.length>0&&oe.setValue(L,"directionalShadowMap",cn.state.directionalShadowMap,_),cn.state.spotShadowMap.length>0&&oe.setValue(L,"spotShadowMap",cn.state.spotShadowMap,_),cn.state.pointShadowMap.length>0&&oe.setValue(L,"pointShadowMap",cn.state.pointShadowMap,_)),k.isSkinnedMesh){oe.setOptional(L,k,"bindMatrix"),oe.setOptional(L,k,"bindMatrixInverse");let he=k.skeleton;he&&(he.boneTexture===null&&he.computeBoneTexture(),oe.setValue(L,"boneTexture",he.boneTexture,_))}k.isBatchedMesh&&(oe.setOptional(L,k,"batchingTexture"),oe.setValue(L,"batchingTexture",k._matricesTexture,_),oe.setOptional(L,k,"batchingIdTexture"),oe.setValue(L,"batchingIdTexture",k._indirectTexture,_),oe.setOptional(L,k,"batchingColorTexture"),k._colorsTexture!==null&&oe.setValue(L,"batchingColorTexture",k._colorsTexture,_));let fi=G.morphAttributes;if((fi.position!==void 0||fi.normal!==void 0||fi.color!==void 0)&&Nt.update(k,G,_n),(ui||xt.receiveShadow!==k.receiveShadow)&&(xt.receiveShadow=k.receiveShadow,oe.setValue(L,"receiveShadow",k.receiveShadow)),(B.isMeshStandardMaterial||B.isMeshLambertMaterial||B.isMeshPhongMaterial)&&B.envMap===null&&F.environment!==null&&(Ae.envMapIntensity.value=F.environmentIntensity),Ae.dfgLUT!==void 0&&(Ae.dfgLUT.value=$v()),ui){if(oe.setValue(L,"toneMappingExposure",I.toneMappingExposure),xt.needsLights&&Sm(Ae,fs),pt&&B.fog===!0&&X.refreshFogUniforms(Ae,pt),X.refreshMaterialUniforms(Ae,B,kt,te,w.state.transmissionRenderTarget[M.id]),xt.needsLights&&xt.lightProbeGrid){let he=xt.lightProbeGrid;Ae.probesSH.value=he.texture,Ae.probesMin.value.copy(he.boundingBox.min),Ae.probesMax.value.copy(he.boundingBox.max),Ae.probesResolution.value.copy(he.resolution)}Os.upload(L,au(xt),Ae,_)}if(B.isShaderMaterial&&B.uniformsNeedUpdate===!0&&(Os.upload(L,au(xt),Ae,_),B.uniformsNeedUpdate=!1),B.isSpriteMaterial&&oe.setValue(L,"center",k.center),oe.setValue(L,"modelViewMatrix",k.modelViewMatrix),oe.setValue(L,"normalMatrix",k.normalMatrix),oe.setValue(L,"modelMatrix",k.matrixWorld),B.uniformsGroups!==void 0){let he=B.uniformsGroups;for(let di=0,ds=he.length;di<ds;di++){let lu=he[di];q.update(lu,_n),q.bind(lu,_n)}}return _n}function Sm(M,F){M.ambientLightColor.needsUpdate=F,M.lightProbe.needsUpdate=F,M.directionalLights.needsUpdate=F,M.directionalLightShadows.needsUpdate=F,M.pointLights.needsUpdate=F,M.pointLightShadows.needsUpdate=F,M.spotLights.needsUpdate=F,M.spotLightShadows.needsUpdate=F,M.rectAreaLights.needsUpdate=F,M.hemisphereLights.needsUpdate=F}function wm(M){return M.isMeshLambertMaterial||M.isMeshToonMaterial||M.isMeshPhongMaterial||M.isMeshStandardMaterial||M.isShadowMaterial||M.isShaderMaterial&&M.lights===!0}this.getActiveCubeFace=function(){return H},this.getActiveMipmapLevel=function(){return W},this.getRenderTarget=function(){return U},this.setRenderTargetTextures=function(M,F,G){let B=A.get(M);B.__autoAllocateDepthBuffer=M.resolveDepthBuffer===!1,B.__autoAllocateDepthBuffer===!1&&(B.__useRenderToTexture=!1),A.get(M.texture).__webglTexture=F,A.get(M.depthTexture).__webglTexture=B.__autoAllocateDepthBuffer?void 0:G,B.__hasExternalTextures=!0},this.setRenderTargetFramebuffer=function(M,F){let G=A.get(M);G.__webglFramebuffer=F,G.__useDefaultFramebuffer=F===void 0};let Am=L.createFramebuffer();this.setRenderTarget=function(M,F=0,G=0){U=M,H=F,W=G;let B=null,k=!1,pt=!1;if(M){let dt=A.get(M);if(dt.__useDefaultFramebuffer!==void 0){ht.bindFramebuffer(L.FRAMEBUFFER,dt.__webglFramebuffer),$.copy(M.viewport),tt.copy(M.scissor),ct=M.scissorTest,ht.viewport($),ht.scissor(tt),ht.setScissorTest(ct),z=-1;return}else if(dt.__webglFramebuffer===void 0)_.setupRenderTarget(M);else if(dt.__hasExternalTextures)_.rebindTextures(M,A.get(M.texture).__webglTexture,A.get(M.depthTexture).__webglTexture);else if(M.depthBuffer){let Bt=M.depthTexture;if(dt.__boundDepthTexture!==Bt){if(Bt!==null&&A.has(Bt)&&(M.width!==Bt.image.width||M.height!==Bt.image.height))throw new Error("WebGLRenderTarget: Attached DepthTexture is initialized to the incorrect size.");_.setupDepthRenderbuffer(M)}}let bt=M.texture;(bt.isData3DTexture||bt.isDataArrayTexture||bt.isCompressedArrayTexture)&&(pt=!0);let At=A.get(M).__webglFramebuffer;M.isWebGLCubeRenderTarget?(Array.isArray(At[F])?B=At[F][G]:B=At[F],k=!0):M.samples>0&&_.useMultisampledRTT(M)===!1?B=A.get(M).__webglMultisampledFramebuffer:Array.isArray(At)?B=At[G]:B=At,$.copy(M.viewport),tt.copy(M.scissor),ct=M.scissorTest}else $.copy(rt).multiplyScalar(kt).floor(),tt.copy(Ct).multiplyScalar(kt).floor(),ct=Ft;if(G!==0&&(B=Am),ht.bindFramebuffer(L.FRAMEBUFFER,B)&&ht.drawBuffers(M,B),ht.viewport($),ht.scissor(tt),ht.setScissorTest(ct),k){let dt=A.get(M.texture);L.framebufferTexture2D(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_CUBE_MAP_POSITIVE_X+F,dt.__webglTexture,G)}else if(pt){let dt=F;for(let bt=0;bt<M.textures.length;bt++){let At=A.get(M.textures[bt]);L.framebufferTextureLayer(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0+bt,At.__webglTexture,G,dt)}}else if(M!==null&&G!==0){let dt=A.get(M.texture);L.framebufferTexture2D(L.FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,dt.__webglTexture,G)}z=-1},this.readRenderTargetPixels=function(M,F,G,B,k,pt,yt,dt=0){if(!(M&&M.isWebGLRenderTarget)){Rt("WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");return}let bt=A.get(M).__webglFramebuffer;if(M.isWebGLCubeRenderTarget&&yt!==void 0&&(bt=bt[yt]),bt){ht.bindFramebuffer(L.FRAMEBUFFER,bt);try{let At=M.textures[dt],Bt=At.format,Gt=At.type;if(M.textures.length>1&&L.readBuffer(L.COLOR_ATTACHMENT0+dt),!ce.textureFormatReadable(Bt)){Rt("WebGLRenderer.readRenderTargetPixels: renderTarget is not in RGBA or implementation defined format.");return}if(!ce.textureTypeReadable(Gt)){Rt("WebGLRenderer.readRenderTargetPixels: renderTarget is not in UnsignedByteType or implementation defined type.");return}F>=0&&F<=M.width-B&&G>=0&&G<=M.height-k&&L.readPixels(F,G,B,k,P.convert(Bt),P.convert(Gt),pt)}finally{let At=U!==null?A.get(U).__webglFramebuffer:null;ht.bindFramebuffer(L.FRAMEBUFFER,At)}}},this.readRenderTargetPixelsAsync=async function(M,F,G,B,k,pt,yt,dt=0){if(!(M&&M.isWebGLRenderTarget))throw new Error("THREE.WebGLRenderer.readRenderTargetPixels: renderTarget is not THREE.WebGLRenderTarget.");let bt=A.get(M).__webglFramebuffer;if(M.isWebGLCubeRenderTarget&&yt!==void 0&&(bt=bt[yt]),bt)if(F>=0&&F<=M.width-B&&G>=0&&G<=M.height-k){ht.bindFramebuffer(L.FRAMEBUFFER,bt);let At=M.textures[dt],Bt=At.format,Gt=At.type;if(M.textures.length>1&&L.readBuffer(L.COLOR_ATTACHMENT0+dt),!ce.textureFormatReadable(Bt))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in RGBA or implementation defined format.");if(!ce.textureTypeReadable(Gt))throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: renderTarget is not in UnsignedByteType or implementation defined type.");let Tt=L.createBuffer();L.bindBuffer(L.PIXEL_PACK_BUFFER,Tt),L.bufferData(L.PIXEL_PACK_BUFFER,pt.byteLength,L.STREAM_READ),L.readPixels(F,G,B,k,P.convert(Bt),P.convert(Gt),0);let ie=U!==null?A.get(U).__webglFramebuffer:null;ht.bindFramebuffer(L.FRAMEBUFFER,ie);let we=L.fenceSync(L.SYNC_GPU_COMMANDS_COMPLETE,0);return L.flush(),await pf(L,we,4),L.bindBuffer(L.PIXEL_PACK_BUFFER,Tt),L.getBufferSubData(L.PIXEL_PACK_BUFFER,0,pt),L.deleteBuffer(Tt),L.deleteSync(we),pt}else throw new Error("THREE.WebGLRenderer.readRenderTargetPixelsAsync: requested read bounds are out of range.")},this.copyFramebufferToTexture=function(M,F=null,G=0){let B=Math.pow(2,-G),k=Math.floor(M.image.width*B),pt=Math.floor(M.image.height*B),yt=F!==null?F.x:0,dt=F!==null?F.y:0;_.setTexture2D(M,0),L.copyTexSubImage2D(L.TEXTURE_2D,G,0,0,yt,dt,k,pt),ht.unbindTexture()};let Tm=L.createFramebuffer(),Em=L.createFramebuffer();this.copyTextureToTexture=function(M,F,G=null,B=null,k=0,pt=0){let yt,dt,bt,At,Bt,Gt,Tt,ie,we,xe=M.isCompressedTexture?M.mipmaps[pt]:M.image;if(G!==null)yt=G.max.x-G.min.x,dt=G.max.y-G.min.y,bt=G.isBox3?G.max.z-G.min.z:1,At=G.min.x,Bt=G.min.y,Gt=G.isBox3?G.min.z:0;else{let Ae=Math.pow(2,-k);yt=Math.floor(xe.width*Ae),dt=Math.floor(xe.height*Ae),M.isDataArrayTexture?bt=xe.depth:M.isData3DTexture?bt=Math.floor(xe.depth*Ae):bt=1,At=0,Bt=0,Gt=0}B!==null?(Tt=B.x,ie=B.y,we=B.z):(Tt=0,ie=0,we=0);let ae=P.convert(F.format),Ge=P.convert(F.type),xt;F.isData3DTexture?(_.setTexture3D(F,0),xt=L.TEXTURE_3D):F.isDataArrayTexture||F.isCompressedArrayTexture?(_.setTexture2DArray(F,0),xt=L.TEXTURE_2D_ARRAY):(_.setTexture2D(F,0),xt=L.TEXTURE_2D),ht.activeTexture(L.TEXTURE0),ht.pixelStorei(L.UNPACK_FLIP_Y_WEBGL,F.flipY),ht.pixelStorei(L.UNPACK_PREMULTIPLY_ALPHA_WEBGL,F.premultiplyAlpha),ht.pixelStorei(L.UNPACK_ALIGNMENT,F.unpackAlignment);let cn=ht.getParameter(L.UNPACK_ROW_LENGTH),Jt=ht.getParameter(L.UNPACK_IMAGE_HEIGHT),_n=ht.getParameter(L.UNPACK_SKIP_PIXELS),Nn=ht.getParameter(L.UNPACK_SKIP_ROWS),ui=ht.getParameter(L.UNPACK_SKIP_IMAGES);ht.pixelStorei(L.UNPACK_ROW_LENGTH,xe.width),ht.pixelStorei(L.UNPACK_IMAGE_HEIGHT,xe.height),ht.pixelStorei(L.UNPACK_SKIP_PIXELS,At),ht.pixelStorei(L.UNPACK_SKIP_ROWS,Bt),ht.pixelStorei(L.UNPACK_SKIP_IMAGES,Gt);let fs=M.isDataArrayTexture||M.isData3DTexture,oe=F.isDataArrayTexture||F.isData3DTexture;if(M.isDepthTexture){let Ae=A.get(M),fi=A.get(F),he=A.get(Ae.__renderTarget),di=A.get(fi.__renderTarget);ht.bindFramebuffer(L.READ_FRAMEBUFFER,he.__webglFramebuffer),ht.bindFramebuffer(L.DRAW_FRAMEBUFFER,di.__webglFramebuffer);for(let ds=0;ds<bt;ds++)fs&&(L.framebufferTextureLayer(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,A.get(M).__webglTexture,k,Gt+ds),L.framebufferTextureLayer(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,A.get(F).__webglTexture,pt,we+ds)),L.blitFramebuffer(At,Bt,yt,dt,Tt,ie,yt,dt,L.DEPTH_BUFFER_BIT,L.NEAREST);ht.bindFramebuffer(L.READ_FRAMEBUFFER,null),ht.bindFramebuffer(L.DRAW_FRAMEBUFFER,null)}else if(k!==0||M.isRenderTargetTexture||A.has(M)){let Ae=A.get(M),fi=A.get(F);ht.bindFramebuffer(L.READ_FRAMEBUFFER,Tm),ht.bindFramebuffer(L.DRAW_FRAMEBUFFER,Em);for(let he=0;he<bt;he++)fs?L.framebufferTextureLayer(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,Ae.__webglTexture,k,Gt+he):L.framebufferTexture2D(L.READ_FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,Ae.__webglTexture,k),oe?L.framebufferTextureLayer(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,fi.__webglTexture,pt,we+he):L.framebufferTexture2D(L.DRAW_FRAMEBUFFER,L.COLOR_ATTACHMENT0,L.TEXTURE_2D,fi.__webglTexture,pt),k!==0?L.blitFramebuffer(At,Bt,yt,dt,Tt,ie,yt,dt,L.COLOR_BUFFER_BIT,L.NEAREST):oe?L.copyTexSubImage3D(xt,pt,Tt,ie,we+he,At,Bt,yt,dt):L.copyTexSubImage2D(xt,pt,Tt,ie,At,Bt,yt,dt);ht.bindFramebuffer(L.READ_FRAMEBUFFER,null),ht.bindFramebuffer(L.DRAW_FRAMEBUFFER,null)}else oe?M.isDataTexture||M.isData3DTexture?L.texSubImage3D(xt,pt,Tt,ie,we,yt,dt,bt,ae,Ge,xe.data):F.isCompressedArrayTexture?L.compressedTexSubImage3D(xt,pt,Tt,ie,we,yt,dt,bt,ae,xe.data):L.texSubImage3D(xt,pt,Tt,ie,we,yt,dt,bt,ae,Ge,xe):M.isDataTexture?L.texSubImage2D(L.TEXTURE_2D,pt,Tt,ie,yt,dt,ae,Ge,xe.data):M.isCompressedTexture?L.compressedTexSubImage2D(L.TEXTURE_2D,pt,Tt,ie,xe.width,xe.height,ae,xe.data):L.texSubImage2D(L.TEXTURE_2D,pt,Tt,ie,yt,dt,ae,Ge,xe);ht.pixelStorei(L.UNPACK_ROW_LENGTH,cn),ht.pixelStorei(L.UNPACK_IMAGE_HEIGHT,Jt),ht.pixelStorei(L.UNPACK_SKIP_PIXELS,_n),ht.pixelStorei(L.UNPACK_SKIP_ROWS,Nn),ht.pixelStorei(L.UNPACK_SKIP_IMAGES,ui),pt===0&&F.generateMipmaps&&L.generateMipmap(xt),ht.unbindTexture()},this.initRenderTarget=function(M){A.get(M).__webglFramebuffer===void 0&&_.setupRenderTarget(M)},this.initTexture=function(M){M.isCubeTexture?_.setTextureCube(M,0):M.isData3DTexture?_.setTexture3D(M,0):M.isDataArrayTexture||M.isCompressedArrayTexture?_.setTexture2DArray(M,0):_.setTexture2D(M,0),ht.unbindTexture()},this.resetState=function(){H=0,W=0,U=null,ht.reset(),it.reset()},typeof __THREE_DEVTOOLS__<"u"&&__THREE_DEVTOOLS__.dispatchEvent(new CustomEvent("observe",{detail:this}))}get coordinateSystem(){return An}get outputColorSpace(){return this._outputColorSpace}set outputColorSpace(t){this._outputColorSpace=t;let e=this.getContext();e.drawingBufferColorSpace=Ht._getDrawingBufferColorSpace(t),e.unpackColorSpace=Ht._getUnpackColorSpace()}};var ks={name:"CopyShader",uniforms:{tDiffuse:{value:null},opacity:{value:1}},vertexShader:`

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


		}`};var gn=class{constructor(){this.isPass=!0,this.enabled=!0,this.needsSwap=!0,this.clear=!1,this.renderToScreen=!1}setSize(){}render(){console.error("THREE.Pass: .render() must be implemented in derived pass.")}dispose(){}},Kv=new is(-1,1,1,-1,0,1),uh=class extends Qt{constructor(){super(),this.setAttribute("position",new ke([-1,3,0,-1,-1,0,3,-1,0],3)),this.setAttribute("uv",new ke([0,2,0,0,2,0],2))}},jv=new uh,Fi=class{constructor(t){this._mesh=new rn(jv,t)}dispose(){this._mesh.geometry.dispose()}render(t){t.render(this._mesh,Kv)}get material(){return this._mesh.material}set material(t){this._mesh.material=t}};var cl=class extends gn{constructor(t,e="tDiffuse"){super(),this.textureID=e,this.uniforms=null,this.material=null,t instanceof se?(this.uniforms=t.uniforms,this.material=t):t&&(this.uniforms=oi.clone(t.uniforms),this.material=new se({name:t.name!==void 0?t.name:"unspecified",defines:Object.assign({},t.defines),uniforms:this.uniforms,vertexShader:t.vertexShader,fragmentShader:t.fragmentShader})),this._fsQuad=new Fi(this.material)}render(t,e,n){this.uniforms[this.textureID]&&(this.uniforms[this.textureID].value=n.texture),this._fsQuad.material=this.material,this.renderToScreen?(t.setRenderTarget(null),this._fsQuad.render(t)):(t.setRenderTarget(e),this.clear&&t.clear(t.autoClearColor,t.autoClearDepth,t.autoClearStencil),this._fsQuad.render(t))}dispose(){this.material.dispose(),this._fsQuad.dispose()}};var Fr=class extends gn{constructor(t,e){super(),this.scene=t,this.camera=e,this.clear=!0,this.needsSwap=!1,this.inverse=!1}render(t,e,n){let s=t.getContext(),r=t.state;r.buffers.color.setMask(!1),r.buffers.depth.setMask(!1),r.buffers.color.setLocked(!0),r.buffers.depth.setLocked(!0);let a,o;this.inverse?(a=0,o=1):(a=1,o=0),r.buffers.stencil.setTest(!0),r.buffers.stencil.setOp(s.REPLACE,s.REPLACE,s.REPLACE),r.buffers.stencil.setFunc(s.ALWAYS,a,4294967295),r.buffers.stencil.setClear(o),r.buffers.stencil.setLocked(!0),t.setRenderTarget(n),this.clear&&t.clear(),t.render(this.scene,this.camera),t.setRenderTarget(e),this.clear&&t.clear(),t.render(this.scene,this.camera),r.buffers.color.setLocked(!1),r.buffers.depth.setLocked(!1),r.buffers.color.setMask(!0),r.buffers.depth.setMask(!0),r.buffers.stencil.setLocked(!1),r.buffers.stencil.setFunc(s.EQUAL,1,4294967295),r.buffers.stencil.setOp(s.KEEP,s.KEEP,s.KEEP),r.buffers.stencil.setLocked(!0)}},hl=class extends gn{constructor(){super(),this.needsSwap=!1}render(t){t.state.buffers.stencil.setLocked(!1),t.state.buffers.stencil.setTest(!1)}};var ul=class{constructor(t,e){if(this.renderer=t,this._pixelRatio=t.getPixelRatio(),e===void 0){let n=t.getSize(new Ut);this._width=n.width,this._height=n.height,e=new Le(this._width*this._pixelRatio,this._height*this._pixelRatio,{type:qe}),e.texture.name="EffectComposer.rt1"}else this._width=e.width,this._height=e.height;this.renderTarget1=e,this.renderTarget2=e.clone(),this.renderTarget2.texture.name="EffectComposer.rt2",this.writeBuffer=this.renderTarget1,this.readBuffer=this.renderTarget2,this.renderToScreen=!0,this.passes=[],this.copyPass=new cl(ks),this.copyPass.material.blending=vn,this.timer=new mr}swapBuffers(){let t=this.readBuffer;this.readBuffer=this.writeBuffer,this.writeBuffer=t}addPass(t){this.passes.push(t),t.setSize(this._width*this._pixelRatio,this._height*this._pixelRatio)}insertPass(t,e){this.passes.splice(e,0,t),t.setSize(this._width*this._pixelRatio,this._height*this._pixelRatio)}removePass(t){let e=this.passes.indexOf(t);e!==-1&&this.passes.splice(e,1)}isLastEnabledPass(t){for(let e=t+1;e<this.passes.length;e++)if(this.passes[e].enabled)return!1;return!0}render(t){this.timer.update(),t===void 0&&(t=this.timer.getDelta());let e=this.renderer.getRenderTarget(),n=!1;for(let s=0,r=this.passes.length;s<r;s++){let a=this.passes[s];if(a.enabled!==!1){if(a.renderToScreen=this.renderToScreen&&this.isLastEnabledPass(s),a.render(this.renderer,this.writeBuffer,this.readBuffer,t,n),a.needsSwap){if(n){let o=this.renderer.getContext(),l=this.renderer.state.buffers.stencil;l.setFunc(o.NOTEQUAL,1,4294967295),this.copyPass.render(this.renderer,this.writeBuffer,this.readBuffer,t),l.setFunc(o.EQUAL,1,4294967295)}this.swapBuffers()}Fr!==void 0&&(a instanceof Fr?n=!0:a instanceof hl&&(n=!1))}}this.renderer.setRenderTarget(e)}reset(t){if(t===void 0){let e=this.renderer.getSize(new Ut);this._pixelRatio=this.renderer.getPixelRatio(),this._width=e.width,this._height=e.height,t=this.renderTarget1.clone(),t.setSize(this._width*this._pixelRatio,this._height*this._pixelRatio)}this.renderTarget1.dispose(),this.renderTarget2.dispose(),this.renderTarget1=t,this.renderTarget2=t.clone(),this.writeBuffer=this.renderTarget1,this.readBuffer=this.renderTarget2}setSize(t,e){this._width=t,this._height=e;let n=this._width*this._pixelRatio,s=this._height*this._pixelRatio;this.renderTarget1.setSize(n,s),this.renderTarget2.setSize(n,s);for(let r=0;r<this.passes.length;r++)this.passes[r].setSize(n,s)}setPixelRatio(t){this._pixelRatio=t,this.setSize(this._width,this._height)}dispose(){this.renderTarget1.dispose(),this.renderTarget2.dispose(),this.copyPass.dispose()}};var fl=class extends gn{constructor(t,e,n=null,s=null,r=null){super(),this.scene=t,this.camera=e,this.overrideMaterial=n,this.clearColor=s,this.clearAlpha=r,this.clear=!0,this.clearDepth=!1,this.needsSwap=!1,this.isRenderPass=!0,this._oldClearColor=new ut}render(t,e,n){let s=t.autoClear;t.autoClear=!1;let r,a;this.overrideMaterial!==null&&(a=this.scene.overrideMaterial,this.scene.overrideMaterial=this.overrideMaterial),this.clearColor!==null&&(t.getClearColor(this._oldClearColor),t.setClearColor(this.clearColor,t.getClearAlpha())),this.clearAlpha!==null&&(r=t.getClearAlpha(),t.setClearAlpha(this.clearAlpha)),this.clearDepth==!0&&t.clearDepth(),t.setRenderTarget(this.renderToScreen?null:n),this.clear===!0&&t.clear(t.autoClearColor,t.autoClearDepth,t.autoClearStencil),t.render(this.scene,this.camera),this.clearColor!==null&&t.setClearColor(this._oldClearColor),this.clearAlpha!==null&&t.setClearAlpha(r),this.overrideMaterial!==null&&(this.scene.overrideMaterial=a),t.autoClear=s}};var Yf={name:"LuminosityHighPassShader",uniforms:{tDiffuse:{value:null},luminosityThreshold:{value:1},smoothWidth:{value:1},defaultColor:{value:new ut(0)},defaultOpacity:{value:0}},vertexShader:`

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

		}`};var zs=class i extends gn{constructor(t,e=1,n,s){super(),this.strength=e,this.radius=n,this.threshold=s,this.resolution=t!==void 0?new Ut(t.x,t.y):new Ut(256,256),this.clearColor=new ut(0,0,0),this.needsSwap=!1,this.renderTargetsHorizontal=[],this.renderTargetsVertical=[],this.nMips=5;let r=Math.round(this.resolution.x/2),a=Math.round(this.resolution.y/2);this.renderTargetBright=new Le(r,a,{type:qe}),this.renderTargetBright.texture.name="UnrealBloomPass.bright",this.renderTargetBright.texture.generateMipmaps=!1;for(let h=0;h<this.nMips;h++){let f=new Le(r,a,{type:qe});f.texture.name="UnrealBloomPass.h"+h,f.texture.generateMipmaps=!1,this.renderTargetsHorizontal.push(f);let u=new Le(r,a,{type:qe});u.texture.name="UnrealBloomPass.v"+h,u.texture.generateMipmaps=!1,this.renderTargetsVertical.push(u),r=Math.round(r/2),a=Math.round(a/2)}let o=Yf;this.highPassUniforms=oi.clone(o.uniforms),this.highPassUniforms.luminosityThreshold.value=s,this.highPassUniforms.smoothWidth.value=.01,this.materialHighPassFilter=new se({uniforms:this.highPassUniforms,vertexShader:o.vertexShader,fragmentShader:o.fragmentShader}),this.separableBlurMaterials=[];let l=[6,10,14,18,22];r=Math.round(this.resolution.x/2),a=Math.round(this.resolution.y/2);for(let h=0;h<this.nMips;h++)this.separableBlurMaterials.push(this._getSeparableBlurMaterial(l[h])),this.separableBlurMaterials[h].uniforms.invSize.value=new Ut(1/r,1/a),r=Math.round(r/2),a=Math.round(a/2);this.compositeMaterial=this._getCompositeMaterial(this.nMips),this.compositeMaterial.uniforms.blurTexture1.value=this.renderTargetsVertical[0].texture,this.compositeMaterial.uniforms.blurTexture2.value=this.renderTargetsVertical[1].texture,this.compositeMaterial.uniforms.blurTexture3.value=this.renderTargetsVertical[2].texture,this.compositeMaterial.uniforms.blurTexture4.value=this.renderTargetsVertical[3].texture,this.compositeMaterial.uniforms.blurTexture5.value=this.renderTargetsVertical[4].texture,this.compositeMaterial.uniforms.bloomStrength.value=e,this.compositeMaterial.uniforms.bloomRadius.value=.1;let c=[1,.8,.6,.4,.2];this.compositeMaterial.uniforms.bloomFactors.value=c,this.bloomTintColors=[new D(1,1,1),new D(1,1,1),new D(1,1,1),new D(1,1,1),new D(1,1,1)],this.compositeMaterial.uniforms.bloomTintColors.value=this.bloomTintColors,this.copyUniforms=oi.clone(ks.uniforms),this.blendMaterial=new se({uniforms:this.copyUniforms,vertexShader:ks.vertexShader,fragmentShader:ks.fragmentShader,premultipliedAlpha:!0,blending:Tn,depthTest:!1,depthWrite:!1,transparent:!0}),this._oldClearColor=new ut,this._oldClearAlpha=1,this._basic=new es,this._fsQuad=new Fi(null)}dispose(){for(let t=0;t<this.renderTargetsHorizontal.length;t++)this.renderTargetsHorizontal[t].dispose();for(let t=0;t<this.renderTargetsVertical.length;t++)this.renderTargetsVertical[t].dispose();this.renderTargetBright.dispose();for(let t=0;t<this.separableBlurMaterials.length;t++)this.separableBlurMaterials[t].dispose();this.compositeMaterial.dispose(),this.blendMaterial.dispose(),this._basic.dispose(),this._fsQuad.dispose()}setSize(t,e){let n=Math.round(t/2),s=Math.round(e/2);this.renderTargetBright.setSize(n,s);for(let r=0;r<this.nMips;r++)this.renderTargetsHorizontal[r].setSize(n,s),this.renderTargetsVertical[r].setSize(n,s),this.separableBlurMaterials[r].uniforms.invSize.value=new Ut(1/n,1/s),n=Math.round(n/2),s=Math.round(s/2)}render(t,e,n,s,r){t.getClearColor(this._oldClearColor),this._oldClearAlpha=t.getClearAlpha();let a=t.autoClear;t.autoClear=!1,t.setClearColor(this.clearColor,0),r&&t.state.buffers.stencil.setTest(!1),this.renderToScreen&&(this._fsQuad.material=this._basic,this._basic.map=n.texture,t.setRenderTarget(null),t.clear(),this._fsQuad.render(t)),this.highPassUniforms.tDiffuse.value=n.texture,this.highPassUniforms.luminosityThreshold.value=this.threshold,this._fsQuad.material=this.materialHighPassFilter,t.setRenderTarget(this.renderTargetBright),t.clear(),this._fsQuad.render(t);let o=this.renderTargetBright;for(let l=0;l<this.nMips;l++)this._fsQuad.material=this.separableBlurMaterials[l],this.separableBlurMaterials[l].uniforms.colorTexture.value=o.texture,this.separableBlurMaterials[l].uniforms.direction.value=i.BlurDirectionX,t.setRenderTarget(this.renderTargetsHorizontal[l]),t.clear(),this._fsQuad.render(t),this.separableBlurMaterials[l].uniforms.colorTexture.value=this.renderTargetsHorizontal[l].texture,this.separableBlurMaterials[l].uniforms.direction.value=i.BlurDirectionY,t.setRenderTarget(this.renderTargetsVertical[l]),t.clear(),this._fsQuad.render(t),o=this.renderTargetsVertical[l];this._fsQuad.material=this.compositeMaterial,this.compositeMaterial.uniforms.bloomStrength.value=this.strength,this.compositeMaterial.uniforms.bloomRadius.value=this.radius,this.compositeMaterial.uniforms.bloomTintColors.value=this.bloomTintColors,t.setRenderTarget(this.renderTargetsHorizontal[0]),t.clear(),this._fsQuad.render(t),this._fsQuad.material=this.blendMaterial,this.copyUniforms.tDiffuse.value=this.renderTargetsHorizontal[0].texture,r&&t.state.buffers.stencil.setTest(!0),this.renderToScreen?(t.setRenderTarget(null),this._fsQuad.render(t)):(t.setRenderTarget(n),this._fsQuad.render(t)),t.setClearColor(this._oldClearColor,this._oldClearAlpha),t.autoClear=a}_getSeparableBlurMaterial(t){let e=[],n=t/3;for(let s=0;s<t;s++)e.push(.39894*Math.exp(-.5*s*s/(n*n))/n);return new se({defines:{KERNEL_RADIUS:t},uniforms:{colorTexture:{value:null},invSize:{value:new Ut(.5,.5)},direction:{value:new Ut(.5,.5)},gaussianCoefficients:{value:e}},vertexShader:`

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

				}`})}_getCompositeMaterial(t){return new se({defines:{NUM_MIPS:t},uniforms:{blurTexture1:{value:null},blurTexture2:{value:null},blurTexture3:{value:null},blurTexture4:{value:null},blurTexture5:{value:null},bloomStrength:{value:1},bloomFactors:{value:null},bloomTintColors:{value:null},bloomRadius:{value:0}},vertexShader:`

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

				}`})}};zs.BlurDirectionX=new Ut(1,0);zs.BlurDirectionY=new Ut(0,1);var Ur={name:"OutputShader",uniforms:{tDiffuse:{value:null},toneMappingExposure:{value:1}},vertexShader:`
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

		}`};var dl=class extends gn{constructor(){super(),this.isOutputPass=!0,this.uniforms=oi.clone(Ur.uniforms),this.material=new Ls({name:Ur.name,uniforms:this.uniforms,vertexShader:Ur.vertexShader,fragmentShader:Ur.fragmentShader}),this._fsQuad=new Fi(this.material),this._outputColorSpace=null,this._toneMapping=null}render(t,e,n){this.uniforms.tDiffuse.value=n.texture,this.uniforms.toneMappingExposure.value=t.toneMappingExposure,(this._outputColorSpace!==t.outputColorSpace||this._toneMapping!==t.toneMapping)&&(this._outputColorSpace=t.outputColorSpace,this._toneMapping=t.toneMapping,this.material.defines={},Ht.getTransfer(this._outputColorSpace)===Kt&&(this.material.defines.SRGB_TRANSFER=""),this._toneMapping===_r?this.material.defines.LINEAR_TONE_MAPPING="":this._toneMapping===xr?this.material.defines.REINHARD_TONE_MAPPING="":this._toneMapping===vr?this.material.defines.CINEON_TONE_MAPPING="":this._toneMapping===Ci?this.material.defines.ACES_FILMIC_TONE_MAPPING="":this._toneMapping===Mr?this.material.defines.AGX_TONE_MAPPING="":this._toneMapping===br?this.material.defines.NEUTRAL_TONE_MAPPING="":this._toneMapping===yr&&(this.material.defines.CUSTOM_TONE_MAPPING=""),this.material.needsUpdate=!0),this.renderToScreen===!0?(t.setRenderTarget(null),this._fsQuad.render(t)):(t.setRenderTarget(e),this.clear&&t.clear(t.autoClearColor,t.autoClearDepth,t.autoClearStencil),this._fsQuad.render(t))}dispose(){this.material.dispose(),this._fsQuad.dispose()}};var fh=13.200000000000001;var pl={strength:.6,radius:.4,threshold:.18};var m1={distancePerRadius:12,minDistance:40,maxDistance:140,azimuthOffsetRad:15*Math.PI/180,minMs:800,maxMs:1800,msPerWorldUnit:.45},ml=8e-4;function gl(i,t){return i>.001?Math.max(t,1):1}function Zf(i,t,e,n,s,r){let a=0;for(let o=0;o<s.length;o++){let l=s[o];if(!l){for(let d=0;d<r*2;d++){let y=a*3;i[y]=0,i[y+1]=0,i[y+2]=0,t[y]=0,t[y+1]=0,t[y+2]=0,e[a]=0,a++}continue}let c=l.source*3,h=l.target*3,f=n[c]??0,u=n[c+1]??0,p=n[c+2]??0,g=n[h]??0,x=n[h+1]??0,m=n[h+2]??0;for(let d=0;d<r;d++)for(let y=0;y<2;y++){let S=a*3;i[S]=f,i[S+1]=u,i[S+2]=p,t[S]=g,t[S+1]=x,t[S+2]=m,e[a]=(d+y)/r,a++}}}function dh(i,t,e,n,s){let r=s*.32,a=0;for(let o=0;o<e.length;o++){let l=e[o];if(!l){a+=n*6;continue}let c=l.source*3,h=l.target*3,f=t[c]??0,u=t[c+1]??0,p=t[c+2]??0,g=t[h]??0,x=t[h+1]??0,m=t[h+2]??0;if(n===1||r<=0){i[a++]=f,i[a++]=u,i[a++]=p,i[a++]=g,i[a++]=x,i[a++]=m;continue}let d=(f+g)/2,y=(u+x)/2,S=(p+m)/2,b=Math.hypot(g-f,x-u,m-p),T=Math.hypot(d,y,S),w,R,v;if(T>.001)w=d/T,R=y/T,v=S/T;else{let z=g-f,V=m-p,$=Math.hypot(V,z);$>1e-6?(w=V/$,R=0,v=-z/$):(w=1,R=0,v=0)}let E=r*b,I=d+w*E,C=y+R*E,N=S+v*E,H=f,W=u,U=p;for(let z=1;z<=n;z++){let V=z/n,$=(1-V)*(1-V),tt=2*(1-V)*V,ct=V*V,Mt=$*f+tt*I+ct*g,St=$*u+tt*C+ct*x,Xt=$*p+tt*N+ct*m;i[a++]=H,i[a++]=W,i[a++]=U,i[a++]=Mt,i[a++]=St,i[a++]=Xt,H=Mt,W=St,U=Xt}}}function ph(i){return i!==void 0&&Number.isFinite(i)?i:0}function Jf(i,t,e){let n=Number.isFinite(i)?Math.min(Math.max(i,0),1):i>0?1:0,s=Number.isFinite(e)&&e>0?e:1,a=(Number.isFinite(t)?Math.max(t,0):0)/s*.55,o=Math.min(Math.max((n-a)/.45,0),1);return 1-Math.pow(1-o,3)}function $f(i,t){let e=1,n=Math.min(Math.max(Math.floor(t),0),Math.floor(i.length/3));for(let s=0;s<n;s++){let r=Math.hypot(ph(i[s*3]),ph(i[s*3+1]),ph(i[s*3+2]));r>e&&(e=r)}return e}var Kf=`
vec3 revealPosition(vec3 targetPosition) {
	if (uRevealActive < 0.5) return targetPosition;
	float delay = (length(targetPosition) / max(uRevealMaxRadius, 0.0001)) * ${.55.toFixed(2)};
	float localProgress = clamp((uRevealProgress - delay) / ${.45.toFixed(2)}, 0.0, 1.0);
	float scale = 1.0 - pow(1.0 - localProgress, 3.0);
	return targetPosition * scale;
}
`,jf=`
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

${Kf}

void main() {
	vColor = color;
	vGhost = aGhost;
	vDim = aDim;
	vec4 mv = modelViewMatrix * vec4(revealPosition(position), 1.0);
	gl_PointSize = min(aSize * uSizeMul * uPixelScale / max(-mv.z, 1.0), uMaxPoint);
	gl_Position = projectionMatrix * mv;
}
`,Qf=`
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
`,ey=`
attribute vec3 aSourcePosition;
attribute vec3 aTargetPosition;
attribute float aCurveT;
uniform float uLinkCurvature;
uniform float uRevealActive;
uniform float uRevealProgress;
uniform float uRevealMaxRadius;

${Kf}
`,ny=`
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
`;function td(i,t){let e="void main() {",n="#include <begin_vertex>";if(!i.vertexShader.includes(e)||!i.vertexShader.includes(n))throw new Error("Three line shader anchors changed; reveal patch cannot be applied safely");Object.assign(i.uniforms,t),i.vertexShader=i.vertexShader.replace(e,`${ey}
${e}`).replace(n,ny)}function _h(i){let t=2166136261;for(let e=0;e<i.length;e++)t^=i.charCodeAt(e),t=Math.imul(t,16777619);return t>>>0}function gh(i){return _h(i)/4294967295}function ed(i,t){let e=gh(i),n=gh(i+":v"),s=gh(i+":w"),r=t*Math.cbrt(e),a=2*Math.PI*n,o=Math.acos(2*s-1);return[r*Math.sin(o)*Math.cos(a),r*Math.sin(o)*Math.sin(a),r*Math.cos(o)]}function nd(i){return 80*Math.cbrt(Math.max(i,1)/1e3)}var rd=i=>i.tag?ry:ay(i.folderTop,i.unresolved);var id=[0,40,80,120,160,200,240,280,320],iy=new ut("#9aa4b2"),sy=new ut("#7a8499"),ry=new ut("#d8a94b"),sd=new Map;function ay(i,t){if(t)return sy;if(i==="")return iy;let e=sd.get(i);if(!e){let n=id[_h(i)%id.length]??0;e=new ut().setHSL(n/360,.6,.6),sd.set(i,e)}return e}function ad(i,t){let e=i.clone().lerp(t,.5),n={h:0,s:0,l:0};return e.getHSL(n),e.setHSL(n.h,n.s*.4,Math.min(n.l,.35)),e}var oy=[{count:2600,size:1.2},{count:900,size:2},{count:250,size:3}],od=new ut("#9da8c4"),ld=new ut("#ffffff"),cd=new ut("#ffe9c9"),hd=new ut("#bfd3ff");function ud(i){let t=i>>>0;return()=>{t=t+1831565813>>>0;let e=t;return e=Math.imul(e^e>>>15,e|1),e^=e+Math.imul(e^e>>>7,e|61),((e^e>>>14)>>>0)/4294967296}}function xh(i){for(let t of i.children){let e=t;e.geometry.dispose(),e.material.dispose()}}var _l=class{constructor(t,e){this.geometry=t;this.starCount=e;Q(this,"baseColors");Q(this,"attr");Q(this,"active",null);Q(this,"nextIn",3);this.attr=t.getAttribute("color"),this.baseColors=new Float32Array(this.attr.array)}update(t,e){if(this.active){this.active.t+=t;let n=this.active.t,s=1.6,r=this.attr.array,a=this.active.index*3,o=n>=s?1:1+2.2*Math.sin(Math.PI*n/s);r[a]=(this.baseColors[a]??1)*o,r[a+1]=(this.baseColors[a+1]??1)*o,r[a+2]=(this.baseColors[a+2]??1)*o,this.attr.needsUpdate=!0,n>=s&&(this.active=null);return}e<=.01||(this.nextIn-=t,this.nextIn<=0&&(this.active={index:Math.floor(Math.random()*this.starCount),t:0},this.nextIn=Math.min(Math.max(-Math.log(Math.random()+1e-9)*(6/e),1.5),90)))}};function fd(i,t,e=1){let n=Math.max(Math.round(1200*t*e),1),s=ud(3108379),r=new Float32Array(n*3),a=new Float32Array(n*3);for(let h=0;h<n;h++){let f=i*(.3+.7*Math.cbrt(s())),u=2*Math.PI*s(),p=Math.acos(2*s()-1);r[h*3]=f*Math.sin(p)*Math.cos(u),r[h*3+1]=f*Math.sin(p)*Math.sin(u),r[h*3+2]=f*Math.cos(p);let g=s(),x=(g<.85?od.clone().lerp(ld,s()):g<.95?cd.clone():hd.clone()).multiplyScalar(.75);a[h*3]=x.r,a[h*3+1]=x.g,a[h*3+2]=x.b}let o=new Qt;o.setAttribute("position",new Lt(r,3)),o.setAttribute("color",new Lt(a,3));let l=new si({size:2.4,sizeAttenuation:!0,vertexColors:!0,transparent:!0,opacity:.6,depthWrite:!1}),c=new an(o,l);return c.renderOrder=-1,c.frustumCulled=!1,c}function vh(i,t=1){let e=new Qn,n=ud(5340353),s=null;for(let r of oy){let a={count:Math.max(Math.round(r.count*t),50),size:r.size},o=new Float32Array(a.count*3),l=new Float32Array(a.count*3);for(let u=0;u<a.count;u++){let p=2*Math.PI*n(),g=Math.acos(2*n()-1),x=i*(.95+.1*n());o[u*3]=x*Math.sin(g)*Math.cos(p),o[u*3+1]=x*Math.sin(g)*Math.sin(p),o[u*3+2]=x*Math.cos(g);let m=n(),d=m<.85?od.clone().lerp(ld,n()):m<.95?cd.clone():hd.clone();a.size>=3&&n()<.03&&d.multiplyScalar(1.8),l[u*3]=d.r,l[u*3+1]=d.g,l[u*3+2]=d.b}let c=new Qt;c.setAttribute("position",new Lt(o,3)),c.setAttribute("color",new Lt(l,3));let h=new si({size:a.size,sizeAttenuation:!1,vertexColors:!0,transparent:!0,opacity:.55,depthWrite:!1}),f=new an(c,h);f.renderOrder=-1,e.add(f),a.size>=3&&(s=new _l(c,a.count))}return{group:e,twinkler:s??new _l(new Qt().setAttribute("color",new Lt(new Float32Array(3),3)),1)}}var yh=null;function ly(){return yh||(yh=new Float64Array(2048)),yh}function Te(i){return i!==void 0&&Number.isFinite(i)?i:0}function dd(i,t,e,n,s){let r=Math.min(Math.max(Math.floor(e),0),Math.floor(i.length/3),Math.floor(t.length/3));if(r===0)return{center:[0,0,0],scale:1,sourceRadius:0};let a=0,o=0,l=0,c=0;for(let p=0;p<r;p++){let g=Math.max(Te(s?.[p]),0);a+=g,o+=Te(i[p*3])*g,l+=Te(i[p*3+1])*g,c+=Te(i[p*3+2])*g}let h=a>0;if(h)o/=a,l/=a,c/=a;else{for(let p=0;p<r;p++)o+=Te(i[p*3]),l+=Te(i[p*3+1]),c+=Te(i[p*3+2]);o/=r,l/=r,c/=r}let f=0;if(h){let p=0;for(let g=0;g<r;g++){if(Math.max(Te(s?.[g]),0)<=0)continue;let x=Te(i[g*3])-o,m=Te(i[g*3+1])-l,d=Te(i[g*3+2])-c,y=Math.hypot(x,m,d);y>p&&(p=y)}if(p>0){let g=ly();g.fill(0);for(let d=0;d<r;d++){let y=Math.max(Te(s?.[d]),0);if(y<=0)continue;let S=Te(i[d*3])-o,b=Te(i[d*3+1])-l,T=Te(i[d*3+2])-c,w=Math.hypot(S,b,T),R=Math.min(Math.floor(w/p*2048),2047);g[R]=(g[R]??0)+y}let x=a*.95,m=0;for(let d=0;d<2048;d++)if(m+=g[d]??0,m>=x){f=(d+1)/2048*p;break}f===0&&(f=p)}}else for(let p=0;p<r;p++){let g=Te(i[p*3])-o,x=Te(i[p*3+1])-l,m=Te(i[p*3+2])-c;f=Math.max(f,Math.hypot(g,x,m))}let u=f>n&&n>0?n/f:1;for(let p=0;p<r;p++)t[p*3]=(Te(i[p*3])-o)*u,t[p*3+1]=(Te(i[p*3+1])-l)*u,t[p*3+2]=(Te(i[p*3+2])-c)*u;return{center:[o,l,c],scale:u,sourceRadius:f}}function xl(i,t,e){let n=i*374761393+t*668265263+e*1442695|0;return n=Math.imul(n^n>>>13,1274126177),((n^n>>>16)>>>0)/4294967296}function cy(i){let t=i>>>0;return()=>{t=t+1831565813>>>0;let e=t;return e=Math.imul(e^e>>>15,e|1),e^=e+Math.imul(e^e>>>7,e|61),((e^e>>>14)>>>0)/4294967296}}var hy=4e-4,uy=`
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
`,fy=`
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
`,pd=6,md=24,Or=pd*md,Ml=class{constructor(t){Q(this,"object");Q(this,"radius");Q(this,"scale",1);Q(this,"count",0);this.radius=t;let e=new Qt;e.setAttribute("position",new Lt(new Float32Array(Or*3),3)),e.setAttribute("aColor",new Lt(new Float32Array(Or*3),3)),e.setAttribute("aSize",new Lt(new Float32Array(Or),1)),e.setDrawRange(0,0);let n=new se({vertexShader:uy,fragmentShader:fy,transparent:!0,depthWrite:!1,blending:Tn,uniforms:{uPixelScale:{value:1},uMaxPoint:{value:1600},uIntensity:{value:0}}});this.object=new an(e,n),this.object.renderOrder=-1,this.object.frustumCulled=!1}setQuality(t){this.scale=t}bake(t,e){let n=cy(40503),s=this.object.geometry.getAttribute("position"),r=this.object.geometry.getAttribute("aColor"),a=this.object.geometry.getAttribute("aSize"),o=s.array,l=r.array,c=a.array,h=this.radius,f=new ut(t),u=new ut(e),p={h:0,s:0,l:0},g=new ut,x=Math.max(2,Math.round(pd*this.scale)),m=Math.max(6,Math.round(md*this.scale)),d=0;for(let y=0;y<x&&d<Or;y++){let S=2*Math.PI*n(),b=Math.acos(2*n()-1),T=h*(.7+1.7*n()),w=T*Math.sin(b)*Math.cos(S),R=T*Math.sin(b)*Math.sin(S)*.75,v=T*Math.cos(b),E=h*(.5+.5*n());g.copy(f).lerp(u,n()),g.getHSL(p),g.setHSL(p.h+(n()-.5)*.05,Math.min(p.s*.85,.9),.16+.08*n());for(let I=0;I<m&&d<Or;I++){let C=(n()+n()+n()-1.5)*E,N=(n()+n()+n()-1.5)*E*.8,H=(n()+n()+n()-1.5)*E;o[d*3]=w+C,o[d*3+1]=R+N,o[d*3+2]=v+H;let W=n()<.25;c[d]=h*(W?1+.8*n():.4+.5*n());let U=.85+.3*n();l[d*3]=g.r*U,l[d*3+1]=g.g*U,l[d*3+2]=g.b*U,d++}}this.count=d,s.needsUpdate=!0,r.needsUpdate=!0,a.needsUpdate=!0,this.object.geometry.setDrawRange(0,d)}setPixelScale(t,e){this.object.material.uniforms.uPixelScale.value=t,this.object.material.uniforms.uMaxPoint.value=e}setIntensity(t){this.object.material.uniforms.uIntensity.value=t,this.object.visible=t>.005&&this.count>0}get visible(){return this.object.visible}update(t){this.object.rotation.y+=hy*t}dispose(){this.object.geometry.dispose(),this.object.material.dispose()}},dy=`
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
`,py=`
varying vec3 vColor;
uniform float uIntensity;

void main() {
	vec2 uv = gl_PointCoord - 0.5;
	float d2 = dot(uv, uv);
	float a = exp(-d2 * 10.0) - 0.0821; // 软高斯，r=0.5 处精确归零（无方形硬边）
	if (a < 0.004) discard;
	gl_FragColor = vec4(vColor * uIntensity * 0.55, a * uIntensity * 0.4);
}
`,vl=10,yl=3,bl=class{constructor(){Q(this,"points");Q(this,"memberSamples",[]);Q(this,"count",0);let t=new Qt;t.setAttribute("position",new Lt(new Float32Array(vl*yl*3),3)),t.setAttribute("color",new Lt(new Float32Array(vl*yl*3),3)),t.setAttribute("aSize",new Lt(new Float32Array(vl*yl),1)),t.setDrawRange(0,0);let e=new se({vertexShader:dy,fragmentShader:py,vertexColors:!0,transparent:!0,depthWrite:!1,blending:Tn,uniforms:{uPixelScale:{value:1},uMaxPoint:{value:300},uIntensity:{value:0}}});this.points=new an(t,e),this.points.renderOrder=-1,this.points.frustumCulled=!1}rebuild(t,e,n){let s=t.nodes,r=s.length;if(this.memberSamples=[],r<20){this.count=0,this.points.geometry.setDrawRange(0,0);return}let a=Array.from({length:r},(m,d)=>d).sort((m,d)=>(s[d]?.degree??0)-(s[m]?.degree??0)),o=[],l=n*.5;for(let m of a.slice(0,250)){let d=e[m*3]??0,y=e[m*3+1]??0,S=e[m*3+2]??0,b=!0;for(let T of o)if(Math.hypot(d-(e[T*3]??0),y-(e[T*3+1]??0),S-(e[T*3+2]??0))<l){b=!1;break}if(b&&o.push(m),o.length>=vl)break}let c=this.points.geometry.getAttribute("position"),h=this.points.geometry.getAttribute("aSize"),f=c.array,u=h.array,p=n*.33,g=0,x=11;for(let m of o){let d=e[m*3]??0,y=e[m*3+1]??0,S=e[m*3+2]??0,b=[],T=0,w=0,R=0;for(let C=0;C<r;C++){let N=(e[C*3]??0)-d,H=(e[C*3+1]??0)-y,W=(e[C*3+2]??0)-S;N*N+H*H+W*W<p*p&&(b.push(C),T+=e[C*3]??0,w+=e[C*3+1]??0,R+=e[C*3+2]??0)}if(b.length<8)continue;T/=b.length,w/=b.length,R/=b.length;let v=0;for(let C of b)v+=((e[C*3]??0)-T)**2+((e[C*3+1]??0)-w)**2+((e[C*3+2]??0)-R)**2;let E=Math.sqrt(v/b.length),I=b.length>120?b.filter((C,N)=>N%Math.ceil(b.length/120)===0):b;for(let C=0;C<yl;C++){let N=(xl(x,C,3)-.5)*E,H=(xl(x,C,5)-.5)*E*.7,W=(xl(x,C,7)-.5)*E;f[g*3]=T+N,f[g*3+1]=w+H,f[g*3+2]=R+W,u[g]=E*(1.6+.8*xl(x,C,13)),this.memberSamples.push(I),g++}x++}this.count=g,c.needsUpdate=!0,h.needsUpdate=!0,this.points.geometry.setDrawRange(0,g)}clear(){this.count=0,this.memberSamples=[],this.points.geometry.setDrawRange(0,0)}recolor(t){if(this.count===0)return;let e=this.points.geometry.getAttribute("color"),n=e.array,s={h:0,s:0,l:0},r=new ut;for(let a=0;a<this.count;a++){let o=this.memberSamples[a]??[];r.setRGB(0,0,0);for(let l of o)r.add(t(l));o.length>0&&r.multiplyScalar(1/o.length),r.getHSL(s),r.setHSL(s.h,Math.min(s.s*1.25,1),.4),n[a*3]=r.r,n[a*3+1]=r.g,n[a*3+2]=r.b}e.needsUpdate=!0}setIntensity(t){this.points.material.uniforms.uIntensity.value=t,this.points.visible=t>.005&&this.count>0}get intensity(){return this.points.material.uniforms.uIntensity.value}setPixelScale(t,e){this.points.material.uniforms.uPixelScale.value=t,this.points.material.uniforms.uMaxPoint.value=e}dispose(){this.points.geometry.dispose(),this.points.material.dispose()}};function gd(i,t){return Math.min(i,t)}var Br={high:{id:"high",pixelRatioCap:2,bloomAllowed:!0,starScale:1,linkSegments:8,clusterCloudsAllowed:!0,nodeCap:null,linkCap:null,hubLabels:14,neighborLabels:20,hoverThrottleMs:30},low:{id:"low",pixelRatioCap:1,bloomAllowed:!0,starScale:.4,linkSegments:6,clusterCloudsAllowed:!0,nodeCap:null,linkCap:null,hubLabels:8,neighborLabels:12,hoverThrottleMs:80},mobile:{id:"mobile",pixelRatioCap:1.5,bloomAllowed:!1,starScale:.32,linkSegments:4,clusterCloudsAllowed:!1,nodeCap:1500,linkCap:12e3,hubLabels:6,neighborLabels:8,hoverThrottleMs:null}};var kr={id:"deep-space",background:3,starfield:!0,space:!0,motes:!1,bloomEnabled:!0,lightMode:!1,nodeLightness:null,linkInk:null,linkOpacityScale:1,panelClass:"gx-theme-dark"},Mh={id:"daylight",background:16184559,starfield:!1,space:!1,motes:!0,bloomEnabled:!1,lightMode:!0,nodeLightness:.44,linkInk:"#2e2a24",linkOpacityScale:.65,panelClass:"gx-theme-light"};var gy=.28,wl=class{constructor(t,e){Q(this,"camera");Q(this,"renderer");Q(this,"scene",new rr);Q(this,"composer");Q(this,"bloomPass");Q(this,"outputPass");Q(this,"renderPass");Q(this,"nodePoints",null);Q(this,"nodeMaterial",null);Q(this,"nodeGeometry",null);Q(this,"linkSegments",null);Q(this,"linkGeometry",null);Q(this,"linkMaterial",null);Q(this,"revealLinkMaterial",null);Q(this,"selSegments",null);Q(this,"selGeometry",null);Q(this,"selMaterial",null);Q(this,"revealSelMaterial",null);Q(this,"ghostSegments",null);Q(this,"ghostGeometry",null);Q(this,"ghostMaterial",null);Q(this,"ghostLinks",[]);Q(this,"selLinkIdx",[]);Q(this,"selLinks",[]);Q(this,"selTier1",[]);Q(this,"selTier2",[]);Q(this,"starfield");Q(this,"twinkler");Q(this,"starfieldEnabled",!0);Q(this,"twinkleFreq",.5);Q(this,"motes",null);Q(this,"linkCurvature",0);Q(this,"tierLinkSegs",8);Q(this,"linkK",1);Q(this,"space",{nebula:0,fieldStars:0,clusterClouds:0});Q(this,"nebula",null);Q(this,"clouds",null);Q(this,"fieldStars",null);Q(this,"fieldStarsDensity",0);Q(this,"nebulaTintA","#46d4dc");Q(this,"nebulaTintB","#9a7fe0");Q(this,"tierCloudsAllowed",!0);Q(this,"tierStarScale",1);Q(this,"reveal",null);Q(this,"revealActiveUniform",{value:0});Q(this,"revealProgressUniform",{value:1});Q(this,"revealMaxRadiusUniform",{value:1});Q(this,"linkCurvatureUniform",{value:0});Q(this,"data",{nodes:[],links:[]});Q(this,"positions",new Float32Array(0));Q(this,"renderPositions",new Float32Array(0));Q(this,"nodeTargetPositions",new Float32Array(0));Q(this,"fitWeights",new Float32Array(0));Q(this,"sizes",new Float32Array(0));Q(this,"dimCurrent",new Float32Array(0));Q(this,"dimTarget",new Float32Array(0));Q(this,"dimAnimating",!1);Q(this,"colorFn",rd);Q(this,"tokens",kr);Q(this,"tierBloomAllowed",!0);Q(this,"lastW",2);Q(this,"lastH",2);Q(this,"baseLinkOpacity",.16);Q(this,"focusActive",!1);Q(this,"graphRadiusEstimate");Q(this,"projVec",new D);Q(this,"ghostSourceVec",new D);Q(this,"ghostTargetVec",new D);Q(this,"pixelScale",1);Q(this,"nodeScale",1);Q(this,"sizeMode","degree");this.graphRadiusEstimate=e,this.renderer=new al({antialias:!1,alpha:!1}),this.renderer.setPixelRatio(Math.min(window.devicePixelRatio,2)),this.renderer.toneMapping=Ci,this.renderer.toneMappingExposure=1.05,this.renderer.info.autoReset=!1,t.appendChild(this.renderer.domElement),this.scene.background=new ut(this.tokens.background),this.camera=new Xe(60,1,.5,5e4);let n=vh(e*6.5);this.starfield=n.group,this.twinkler=n.twinkler,this.scene.add(this.starfield),this.composer=new ul(this.renderer),this.renderPass=new fl(this.scene,this.camera),this.bloomPass=new zs(new Ut(2,2),pl.strength,pl.radius,pl.threshold),this.outputPass=new dl,this.composer.addPass(this.renderPass),this.composer.addPass(this.bloomPass),this.composer.addPass(this.outputPass)}setColorFn(t){this.colorFn=t}setData(t,e){this.resetRevealState(),this.data=t,this.positions=e,this.disposeGraphObjects();let n=t.nodes.length;this.renderPositions=new Float32Array(n*3),this.nodeTargetPositions=new Float32Array(n*3),this.fitWeights=new Float32Array(n);let s=new Float32Array(n);this.sizes=new Float32Array(n),this.dimCurrent=new Float32Array(n).fill(1),this.dimTarget=new Float32Array(n).fill(1);for(let r=0;r<n;r++){let a=t.nodes[r];a&&(s[r]=a.unresolved?1:0,this.fitWeights[r]=a.degree,this.sizes[r]=this.computeSize(a))}this.fitPositions(),this.nodeTargetPositions.set(this.renderPositions),this.nodeGeometry=new Qt,this.nodeGeometry.setAttribute("position",new Lt(this.nodeTargetPositions,3).setUsage(Ni)),this.nodeGeometry.setAttribute("color",new Lt(new Float32Array(n*3),3)),this.nodeGeometry.setAttribute("aSize",new Lt(this.sizes,1)),this.nodeGeometry.setAttribute("aGhost",new Lt(s,1)),this.nodeGeometry.setAttribute("aDim",new Lt(this.dimCurrent,1)),this.nodeMaterial=new se({vertexShader:jf,fragmentShader:Qf,vertexColors:!0,transparent:!0,depthWrite:!1,uniforms:{uPixelScale:{value:this.pixelScale},uSizeMul:{value:this.nodeScale},uLightMode:{value:this.tokens.lightMode?1:0},uMaxPoint:{value:110*this.renderer.getPixelRatio()},uRevealActive:this.revealActiveUniform,uRevealProgress:this.revealProgressUniform,uRevealMaxRadius:this.revealMaxRadiusUniform}}),this.nodePoints=new an(this.nodeGeometry,this.nodeMaterial),this.nodePoints.renderOrder=1,this.nodePoints.frustumCulled=!1,this.scene.add(this.nodePoints),this.buildLinkLayer(),this.clouds?.clear(),this.recolor(),this.updatePositions(),this.buildSelLayer()}buildLinkLayer(){this.linkSegments&&(this.scene.remove(this.linkSegments),this.linkGeometry?.dispose(),this.linkMaterial?.dispose());let t=this.data.links.length;this.linkK=gl(this.linkCurvature,this.tierLinkSegs),this.linkGeometry=new Qt,this.linkGeometry.setAttribute("position",new Lt(new Float32Array(t*this.linkK*2*3),3)),this.linkGeometry.setAttribute("color",new Lt(new Float32Array(t*this.linkK*2*3),3)),this.linkMaterial=new ii({vertexColors:!0,transparent:!0,opacity:this.effectiveLinkOpacity(),depthWrite:!1}),this.linkSegments=new ns(this.linkGeometry,this.linkMaterial),this.linkSegments.renderOrder=0,this.linkSegments.frustumCulled=!1,this.scene.add(this.linkSegments)}setGhostLinks(t){this.ghostLinks=t,this.buildGhostLayer()}buildGhostLayer(){this.ghostSegments&&(this.scene.remove(this.ghostSegments),this.ghostGeometry?.dispose(),this.ghostMaterial?.dispose(),this.ghostSegments=null,this.ghostGeometry=null,this.ghostMaterial=null);let t=this.ghostLinks.length;if(t===0)return;this.ghostGeometry=new Qt,this.ghostGeometry.setAttribute("position",new Lt(new Float32Array(t*2*3),3));let e=new Float32Array(t*2*3),n=this.tokens.lightMode?.35:.8;for(let s=0;s<t;s++){let r=this.ghostLinks[s]?.score??.5,a=n*(.45+.55*r);for(let o=0;o<2;o++)e[(s*2+o)*3]=a,e[(s*2+o)*3+1]=a,e[(s*2+o)*3+2]=a*1.08}this.ghostGeometry.setAttribute("color",new Lt(e,3)),this.ghostMaterial=new fr({vertexColors:!0,transparent:!0,opacity:.22,depthWrite:!1,dashSize:2.6,gapSize:3.4}),this.ghostSegments=new ns(this.ghostGeometry,this.ghostMaterial),this.ghostSegments.renderOrder=0,this.ghostSegments.frustumCulled=!1,this.scene.add(this.ghostSegments),this.updateGhostPositions()}updateGhostPositions(){if(!this.ghostGeometry||!this.ghostSegments)return;let t=this.ghostGeometry.getAttribute("position"),e=t.array;for(let n=0;n<this.ghostLinks.length;n++){let s=this.ghostLinks[n];s&&(this.displayPosition(s.source,this.ghostSourceVec),this.displayPosition(s.target,this.ghostTargetVec),e[n*6]=this.ghostSourceVec.x,e[n*6+1]=this.ghostSourceVec.y,e[n*6+2]=this.ghostSourceVec.z,e[n*6+3]=this.ghostTargetVec.x,e[n*6+4]=this.ghostTargetVec.y,e[n*6+5]=this.ghostTargetVec.z)}t.needsUpdate=!0,this.ghostSegments.computeLineDistances()}setLinkCurve(t){this.linkCurvature=t,this.linkCurvatureUniform.value=t,gl(t,this.tierLinkSegs)!==this.linkK&&(this.buildLinkLayer(),this.recolor(),this.buildSelLayer(),this.reveal&&this.activateRevealLinkLayer(this.reveal.target)),this.reveal||this.updatePositions()}computeSize(t){switch(this.sizeMode){case"fileSize":return Math.min(Math.max(2.2*(.7+1.1*Math.cbrt(t.fileSize/4096)),1.6),fh);case"uniform":return 2.2*1.3;default:return Math.min(2.2*(1+.5*Math.sqrt(t.degree)),fh)}}setSizeMode(t){if(this.sizeMode=t,!!this.nodeGeometry){for(let e=0;e<this.data.nodes.length;e++){let n=this.data.nodes[e];n&&(this.sizes[e]=this.computeSize(n))}this.nodeGeometry.getAttribute("aSize").needsUpdate=!0}}playReveal(t=2600){let e=this.data.nodes.length;if(e===0||!this.nodeGeometry||!this.linkGeometry)return;this.resetRevealState(),this.updatePositions();let n=new Float32Array(this.renderPositions),s=$f(n,e);this.reveal={elapsedMs:0,durMs:Math.max(t,1),maxR:s,target:n},this.revealActiveUniform.value=1,this.revealProgressUniform.value=0,this.revealMaxRadiusUniform.value=s,this.activateRevealLinkLayer(n),this.activateRevealSelectionLayer(n),this.ghostMaterial&&(this.ghostMaterial.opacity=0),this.updateGhostPositions(),this.renderer.compile(this.scene,this.camera)}stepReveal(t){let e=this.reveal;if(!e)return;let n=Number.isFinite(t)?Math.max(t,0):0;e.elapsedMs+=n*1e3;let s=Math.min(e.elapsedMs/e.durMs,1);this.revealProgressUniform.value=s,this.syncRevealLinkOpacity(s),this.ghostMaterial&&(this.ghostMaterial.opacity=.22*Math.min(s*1.6,1)),this.updateGhostPositions(),s>=1&&(this.resetRevealState(),this.updatePositions(),this.refreshClusterClouds())}fillRevealAttributes(t,e,n,s){let r=n.length*s*2,a=r*3,o=t.getAttribute("aSourcePosition"),l=t.getAttribute("aTargetPosition"),c=t.getAttribute("aCurveT"),h=o?.array instanceof Float32Array&&o.array.length===a&&l?.array instanceof Float32Array&&l.array.length===a&&c?.array instanceof Float32Array&&c.array.length===r,f=h?o.array:new Float32Array(a),u=h?l.array:new Float32Array(a),p=h?c.array:new Float32Array(r);Zf(f,u,p,e,n,s),h?(o.needsUpdate=!0,l.needsUpdate=!0,c.needsUpdate=!0):(t.setAttribute("aSourcePosition",new Lt(f,3)),t.setAttribute("aTargetPosition",new Lt(u,3)),t.setAttribute("aCurveT",new Lt(p,1)))}createRevealLinkMaterial(t){let e=new ii({vertexColors:!0,transparent:!0,opacity:t,depthWrite:!1});return e.onBeforeCompile=n=>{td(n,{uLinkCurvature:this.linkCurvatureUniform,uRevealActive:this.revealActiveUniform,uRevealProgress:this.revealProgressUniform,uRevealMaxRadius:this.revealMaxRadiusUniform})},e.customProgramCacheKey=()=>"galaxy-reveal-basic-v1",e}activateRevealLinkLayer(t){let e=this.linkGeometry,n=this.linkSegments;!e||!n||(this.fillRevealAttributes(e,t,this.data.links,this.linkK),this.linkCurvatureUniform.value=this.linkCurvature,this.revealLinkMaterial??=this.createRevealLinkMaterial(this.effectiveLinkOpacity()),this.revealLinkMaterial.opacity=this.effectiveLinkOpacity()*Math.min(this.revealProgressUniform.value*1.6,1),n.material=this.revealLinkMaterial)}activateRevealSelectionLayer(t){!this.selGeometry||!this.selSegments||this.selLinks.length===0||(this.fillRevealAttributes(this.selGeometry,t,this.selLinks,this.linkK),this.revealSelMaterial??=this.createRevealLinkMaterial(.85),this.revealSelMaterial.opacity=.85*Math.min(this.revealProgressUniform.value*1.6,1),this.selSegments.material=this.revealSelMaterial)}syncRevealLinkOpacity(t){let e=Math.min(Math.max(t,0)*1.6,1);this.revealLinkMaterial&&(this.revealLinkMaterial.opacity=this.effectiveLinkOpacity()*e),this.revealSelMaterial&&(this.revealSelMaterial.opacity=.85*e)}resetRevealState(){this.reveal=null,this.revealActiveUniform.value=0,this.revealProgressUniform.value=1,this.revealMaxRadiusUniform.value=1,this.linkSegments&&this.linkMaterial&&(this.linkSegments.material=this.linkMaterial),this.selSegments&&this.selMaterial&&(this.selSegments.material=this.selMaterial),this.ghostMaterial&&(this.ghostMaterial.opacity=.22)}get revealing(){return this.reveal!==null}recolor(){if(!this.nodeGeometry||!this.linkGeometry)return;let t=this.data.nodes.length,e=this.nodeGeometry.getAttribute("color"),n=e.array,s=new Array(t),r={h:0,s:0,l:0};for(let f=0;f<t;f++){let u=this.data.nodes[f];if(!u)continue;let p=this.colorFn(u).clone();this.tokens.nodeLightness!==null&&(p.getHSL(r),p=p.setHSL(r.h,r.s*.95,this.tokens.nodeLightness)),s[f]=p,n[f*3]=p.r,n[f*3+1]=p.g,n[f*3+2]=p.b}e.needsUpdate=!0;let a=this.linkGeometry.getAttribute("color"),o=a.array,l=this.tokens.linkInk?new ut(this.tokens.linkInk):null,c=new ut("#7a87a8"),h=this.linkK*2;for(let f=0;f<this.data.links.length;f++){let u=this.data.links[f];if(!u)continue;let p=l??ad(s[u.source]??c,s[u.target]??c);for(let g=0;g<h;g++)o[(f*h+g)*3]=p.r,o[(f*h+g)*3+1]=p.g,o[(f*h+g)*3+2]=p.b}a.needsUpdate=!0,this.clouds?.recolor(f=>{let u=this.data.nodes[f];return u?this.colorFn(u):c})}fitPositions(){dd(this.positions,this.renderPositions,this.data.nodes.length,this.graphRadiusEstimate*6.2,this.fitWeights)}updatePositions(){if(!this.nodeGeometry||!this.linkGeometry||this.reveal)return;this.fitPositions();let t=this.nodeGeometry.getAttribute("position");this.nodeTargetPositions.set(this.renderPositions),t.needsUpdate=!0;let e=this.linkGeometry.getAttribute("position");dh(e.array,this.renderPositions,this.data.links,this.linkK,this.linkCurvature),e.needsUpdate=!0,this.updateSelPositions(),this.updateGhostPositions()}setFocus(t){let e=this.data.nodes.length;this.focusActive=t!==null;for(let n=0;n<e;n++)this.dimTarget[n]=t?t(n):1;this.dimAnimating=!0,this.syncLinkOpacity()}setSelectedLinks(t,e){this.selTier1=t,this.selTier2=e,this.buildSelLayer()}buildSelLayer(){this.selLinkIdx=[...this.selTier1,...this.selTier2],this.selLinks=this.selLinkIdx.map(l=>this.data.links[l]),this.selSegments&&(this.scene.remove(this.selSegments),this.selGeometry?.dispose(),this.selMaterial?.dispose(),this.selSegments=null,this.selGeometry=null,this.selMaterial=null);let t=this.selLinkIdx.length;if(t===0)return;let e=this.selTier1.length,s=this.linkK*2,r=new Float32Array(t*s*3),a=new Float32Array(t*s*3),o={h:0,s:0,l:0};for(let l=0;l<t;l++){let c=this.data.links[this.selLinkIdx[l]??-1];if(!c)continue;let h=this.data.nodes[c.source],f=h?this.colorFn(h).clone():new ut("#9aa4b2");f.getHSL(o);let u=l>=e,p=this.tokens.lightMode?u?.34:.42:u?.46:.62,g=u?o.s*.9:Math.min(o.s*1.2,1);f.setHSL(o.h,g,p);let x=u?.55:1;for(let m=0;m<s;m++)a[(l*s+m)*3]=f.r*x,a[(l*s+m)*3+1]=f.g*x,a[(l*s+m)*3+2]=f.b*x}this.selGeometry=new Qt,this.selGeometry.setAttribute("position",new Lt(r,3)),this.selGeometry.setAttribute("color",new Lt(a,3)),this.selMaterial=new ii({vertexColors:!0,transparent:!0,opacity:.85,depthWrite:!1}),this.selSegments=new ns(this.selGeometry,this.selMaterial),this.selSegments.renderOrder=2,this.selSegments.frustumCulled=!1,this.scene.add(this.selSegments),this.updateSelPositions(),this.reveal&&this.activateRevealSelectionLayer(this.reveal.target)}updateSelPositions(){if(!this.selGeometry||this.selLinks.length===0)return;let t=this.selGeometry.getAttribute("position");dh(t.array,this.renderPositions,this.selLinks,this.linkK,this.linkCurvature),t.needsUpdate=!0}effectiveLinkOpacity(){let t=this.baseLinkOpacity*this.tokens.linkOpacityScale;return this.focusActive?t*.25:t}syncLinkOpacity(){let t=this.effectiveLinkOpacity();this.linkMaterial&&(this.linkMaterial.opacity=t),this.reveal?this.syncRevealLinkOpacity(this.revealProgressUniform.value):this.revealLinkMaterial&&(this.revealLinkMaterial.opacity=t)}applyTokens(t,e){this.tokens=t,this.scene.background=new ut(t.background),this.starfield.visible=t.starfield&&this.starfieldEnabled,this.syncSpace(),this.renderer.toneMapping=t.lightMode?pn:Ci,this.nodeMaterial&&(this.nodeMaterial.uniforms.uLightMode.value=t.lightMode?1:0),this.bloomPass.enabled=t.bloomEnabled&&this.tierBloomAllowed&&e>.001,t.motes&&!this.motes&&this.buildMotes(),this.motes&&(this.motes.visible=t.motes),this.syncLinkOpacity(),this.recolor(),this.buildSelLayer()}get currentTokens(){return this.tokens}setSpace(t){this.space={...t},this.syncSpace()}syncSpace(){let t=this.tokens.space,e=t?this.space.nebula:0;e>.005&&!this.nebula&&(this.nebula=new Ml(this.graphRadiusEstimate*2.6),this.nebula.setQuality(this.tierStarScale),this.nebula.setPixelScale(this.pixelScale,1600*this.renderer.getPixelRatio()),this.nebula.bake(this.nebulaTintA,this.nebulaTintB),this.scene.add(this.nebula.object)),this.nebula?.setIntensity(e);let n=t?this.space.fieldStars:0;Math.abs(n-this.fieldStarsDensity)>.001&&(this.disposeFieldStars(),n>.005&&(this.fieldStars=fd(this.graphRadiusEstimate*2.4,n,this.tierStarScale),this.scene.add(this.fieldStars)),this.fieldStarsDensity=n);let s=t&&this.tierCloudsAllowed?this.space.clusterClouds:0;s>.005&&!this.clouds&&(this.clouds=new bl,this.clouds.setPixelScale(this.pixelScale,300*this.renderer.getPixelRatio()),this.scene.add(this.clouds.points),this.refreshClusterClouds()),this.clouds?.setIntensity(s)}setNebulaTint(t,e){t===this.nebulaTintA&&e===this.nebulaTintB||(this.nebulaTintA=t,this.nebulaTintB=e,this.nebula?.bake(t,e))}refreshClusterClouds(){if(!this.clouds||this.data.nodes.length===0)return;this.clouds.rebuild(this.data,this.reveal?.target??this.renderPositions,this.graphRadiusEstimate);let t=new ut("#7a87a8");this.clouds.recolor(e=>{let n=this.data.nodes[e];return n?this.colorFn(n):t}),this.clouds.setIntensity(this.tokens.space&&this.tierCloudsAllowed?this.space.clusterClouds:0)}disposeFieldStars(){this.fieldStars&&(this.fieldStars.geometry.dispose(),this.fieldStars.material.dispose(),this.scene.remove(this.fieldStars),this.fieldStars=null)}buildMotes(){let e=new Float32Array(1800),n=this.graphRadiusEstimate*2.2;for(let a=0;a<600;a++)e[a*3]=(Math.random()*2-1)*n,e[a*3+1]=(Math.random()*2-1)*n,e[a*3+2]=(Math.random()*2-1)*n;let s=new Qt;s.setAttribute("position",new Lt(e,3));let r=new si({color:new ut("#d8d4cb"),size:1.6,sizeAttenuation:!0,transparent:!0,opacity:.5,depthWrite:!1});this.motes=new an(s,r),this.motes.renderOrder=-1,this.scene.add(this.motes)}render(t,e=t){this.starfield.rotation.y+=ml*t,this.starfield.visible&&this.twinkler.update(t,this.twinkleFreq),this.nebula?.visible&&this.nebula.update(t),this.fieldStars&&(this.fieldStars.rotation.y-=ml*.6*t),this.motes?.visible&&(this.motes.rotation.y-=ml*2*t),this.dimAnimating&&this.stepDim(t),this.reveal&&this.stepReveal(e),this.renderer.info.reset(),this.composer.render()}stepDim(t){let e=Math.min(t/gy,1),n=!1;for(let s=0;s<this.dimCurrent.length;s++){let r=this.dimCurrent[s]??1,a=this.dimTarget[s]??1,o=r+(a-r)*e;this.dimCurrent[s]=Math.abs(o-a)<.005?a:o,this.dimCurrent[s]!==a&&(n=!0)}this.dimAnimating=n,this.nodeGeometry&&(this.nodeGeometry.getAttribute("aDim").needsUpdate=!0)}get drawCalls(){return this.renderer.info.render.calls}setBloomParams(t){this.bloomPass.strength=t.strength,this.bloomPass.radius=t.radius,this.bloomPass.threshold=t.threshold,this.bloomPass.enabled=this.tokens.bloomEnabled&&this.tierBloomAllowed&&t.strength>.001}getBloomStrength(){return this.bloomPass.enabled?this.bloomPass.strength:0}setBloomStrength(t){this.bloomPass.strength=t,this.bloomPass.enabled=this.tokens.bloomEnabled&&this.tierBloomAllowed&&t>.001}applyTier(t,e){this.tierBloomAllowed=t.bloomAllowed;let n=gd(window.devicePixelRatio,t.pixelRatioCap);this.renderer.setPixelRatio(n),this.composer.setPixelRatio(n),this.bloomPass.enabled=this.tokens.bloomEnabled&&this.tierBloomAllowed&&e>.001;let s=this.starfield.visible,r=this.starfield.rotation.y;xh(this.starfield),this.scene.remove(this.starfield);let a=vh(this.graphRadiusEstimate*6.5,t.starScale);this.starfield=a.group,this.twinkler=a.twinkler,this.starfield.visible=s,this.starfield.rotation.y=r,this.scene.add(this.starfield),this.tierLinkSegs=t.linkSegments,this.linkGeometry&&gl(this.linkCurvature,this.tierLinkSegs)!==this.linkK&&(this.buildLinkLayer(),this.recolor(),this.buildSelLayer(),this.reveal?this.activateRevealLinkLayer(this.reveal.target):this.updatePositions()),this.tierCloudsAllowed=t.clusterCloudsAllowed,this.tierStarScale!==t.starScale&&(this.tierStarScale=t.starScale,this.nebula&&(this.nebula.setQuality(t.starScale),this.nebula.bake(this.nebulaTintA,this.nebulaTintB))),this.fieldStarsDensity=-1,this.syncSpace(),this.resize(this.lastW,this.lastH);let o=this.nodeMaterial?.uniforms.uMaxPoint;o&&(o.value=110*this.renderer.getPixelRatio())}setLinkOpacity(t){this.baseLinkOpacity=t,this.syncLinkOpacity()}setNodeScale(t){this.nodeScale=t;let e=this.nodeMaterial?.uniforms.uSizeMul;e&&(e.value=t)}setStarfieldEnabled(t){this.starfieldEnabled=t,this.starfield.visible=t&&this.tokens.starfield}resize(t,e){if(t<2||e<2)return;this.lastW=t,this.lastH=e,this.camera.aspect=t/e,this.camera.updateProjectionMatrix(),this.renderer.setSize(t,e),this.composer.setSize(t,e),this.bloomPass.resolution.set(t,e);let n=e*this.renderer.getPixelRatio();this.pixelScale=n/(2*Math.tan(this.camera.fov/2*Math.PI/180));let s=this.nodeMaterial?.uniforms.uPixelScale;s&&(s.value=this.pixelScale),this.clouds?.setPixelScale(this.pixelScale,300*this.renderer.getPixelRatio()),this.nebula?.setPixelScale(this.pixelScale,1600*this.renderer.getPixelRatio())}displayPosition(t,e){let n=this.reveal,s=n?.target??this.renderPositions,r=s[t*3]??0,a=s[t*3+1]??0,o=s[t*3+2]??0;if(!n)return e.set(r,a,o);let l=Jf(this.revealProgressUniform.value,Math.hypot(r,a,o),n.maxR);return e.set(r*l,a*l,o*l)}projectNode(t,e,n){return this.displayPosition(t,this.projVec),this.projVec.project(this.camera),{x:(this.projVec.x+1)/2*e,y:(1-this.projVec.y)/2*n,behind:this.projVec.z>1}}pickNearest(t,e,n,s,r){let a=-1,o=r;for(let l=0;l<this.data.nodes.length;l++){let c=this.projectNode(l,n,s);if(c.behind)continue;let h=Math.hypot(c.x-t,c.y-e);h<o&&(o=h,a=l)}return a}nodeRadius(t){return this.sizes[t]??2.2}nodePosition(t,e){return this.displayPosition(t,e)}nodeColorHex(t){let e=this.data.nodes[t];return e?`#${this.colorFn(e).getHexString()}`:"#9aa4b2"}cameraDistanceTo(t){return this.displayPosition(t,this.projVec),this.camera.position.distanceTo(this.projVec)}disposeGraphObjects(){this.nodePoints&&this.scene.remove(this.nodePoints),this.linkSegments&&this.scene.remove(this.linkSegments),this.selSegments&&(this.scene.remove(this.selSegments),this.selGeometry?.dispose(),this.selMaterial?.dispose(),this.selSegments=null,this.selGeometry=null,this.selMaterial=null),this.ghostSegments&&(this.scene.remove(this.ghostSegments),this.ghostGeometry?.dispose(),this.ghostMaterial?.dispose(),this.ghostSegments=null,this.ghostGeometry=null,this.ghostMaterial=null),this.nodeGeometry?.dispose(),this.nodeMaterial?.dispose(),this.linkGeometry?.dispose(),this.linkMaterial?.dispose(),this.revealLinkMaterial?.dispose(),this.revealSelMaterial?.dispose(),this.nodePoints=null,this.linkSegments=null,this.nodeGeometry=null,this.linkGeometry=null,this.nodeMaterial=null,this.linkMaterial=null,this.revealLinkMaterial=null,this.revealSelMaterial=null}dispose(){this.disposeGraphObjects(),xh(this.starfield),this.scene.remove(this.starfield),this.disposeFieldStars(),this.nebula&&(this.nebula.dispose(),this.scene.remove(this.nebula.object),this.nebula=null),this.clouds&&(this.clouds.dispose(),this.scene.remove(this.clouds.points),this.clouds=null),this.motes&&(this.motes.geometry.dispose(),this.motes.material.dispose(),this.scene.remove(this.motes),this.motes=null),this.bloomPass.dispose(),this.outputPass.dispose(),this.renderPass.dispose(),this.composer.dispose(),this.renderer.dispose();try{this.renderer.forceContextLoss()}catch{}this.renderer.domElement.remove()}};var _d=`(()=>{function zt(t){let e=+this._x.call(null,t);return bt(this.cover(e),e,t)}function bt(t,e,r){if(isNaN(e))return t;var n,i=t._root,o={data:r},f=t._x0,a=t._x1,s,l,h,c,x;if(!i)return t._root=o,t;for(;i.length;)if((h=e>=(s=(f+a)/2))?f=s:a=s,n=i,!(i=i[c=+h]))return n[c]=o,t;if(l=+t._x.call(null,i.data),e===l)return o.next=i,n?n[c]=o:t._root=o,t;do n=n?n[c]=new Array(2):t._root=new Array(2),(h=e>=(s=(f+a)/2))?f=s:a=s;while((c=+h)==(x=+(l>=s)));return n[x]=i,n[c]=o,t}function kt(t){Array.isArray(t)||(t=Array.from(t));let e=t.length,r=new Float64Array(e),n=1/0,i=-1/0;for(let o=0,f;o<e;++o)isNaN(f=+this._x.call(null,t[o]))||(r[o]=f,f<n&&(n=f),f>i&&(i=f));if(n>i)return this;this.cover(n).cover(i);for(let o=0;o<e;++o)bt(this,r[o],t[o]);return this}function St(t){if(isNaN(t=+t))return this;var e=this._x0,r=this._x1;if(isNaN(e))r=(e=Math.floor(t))+1;else{for(var n=r-e||1,i=this._root,o,f;e>t||t>=r;)switch(f=+(t<e),o=new Array(2),o[f]=i,i=o,n*=2,f){case 0:r=e+n;break;case 1:e=r-n;break}this._root&&this._root.length&&(this._root=i)}return this._x0=e,this._x1=r,this}function It(){var t=[];return this.visit(function(e){if(!e.length)do t.push(e.data);while(e=e.next)}),t}function qt(t){return arguments.length?this.cover(+t[0][0]).cover(+t[1][0]):isNaN(this._x0)?void 0:[[this._x0],[this._x1]]}function R(t,e,r){this.node=t,this.x0=e,this.x1=r}function Ft(t,e){var r,n=this._x0,i,o,f=this._x1,a=[],s=this._root,l,h;for(s&&a.push(new R(s,n,f)),e==null?e=1/0:(n=t-e,f=t+e);l=a.pop();)if(!(!(s=l.node)||(i=l.x0)>f||(o=l.x1)<n))if(s.length){var c=(i+o)/2;a.push(new R(s[1],c,o),new R(s[0],i,c)),(h=+(t>=c))&&(l=a[a.length-1],a[a.length-1]=a[a.length-1-h],a[a.length-1-h]=l)}else{var x=Math.abs(t-+this._x.call(null,s.data));x<e&&(e=x,n=t-x,f=t+x,r=s.data)}return r}function Pt(t){if(isNaN(s=+this._x.call(null,t)))return this;var e,r=this._root,n,i,o,f=this._x0,a=this._x1,s,l,h,c,x;if(!r)return this;if(r.length)for(;;){if((h=s>=(l=(f+a)/2))?f=l:a=l,e=r,!(r=r[c=+h]))return this;if(!r.length)break;e[c+1&1]&&(n=e,x=c)}for(;r.data!==t;)if(i=r,!(r=r.next))return this;return(o=r.next)&&delete r.next,i?(o?i.next=o:delete i.next,this):e?(o?e[c]=o:delete e[c],(r=e[0]||e[1])&&r===(e[1]||e[0])&&!r.length&&(n?n[x]=r:this._root=r),this):(this._root=o,this)}function Wt(t){for(var e=0,r=t.length;e<r;++e)this.remove(t[e]);return this}function Bt(){return this._root}function Dt(){var t=0;return this.visit(function(e){if(!e.length)do++t;while(e=e.next)}),t}function Rt(t){var e=[],r,n=this._root,i,o,f;for(n&&e.push(new R(n,this._x0,this._x1));r=e.pop();)if(!t(n=r.node,o=r.x0,f=r.x1)&&n.length){var a=(o+f)/2;(i=n[1])&&e.push(new R(i,a,f)),(i=n[0])&&e.push(new R(i,o,a))}return this}function Et(t){var e=[],r=[],n;for(this._root&&e.push(new R(this._root,this._x0,this._x1));n=e.pop();){var i=n.node;if(i.length){var o,f=n.x0,a=n.x1,s=(f+a)/2;(o=i[0])&&e.push(new R(o,f,s)),(o=i[1])&&e.push(new R(o,s,a))}r.push(n)}for(;n=r.pop();)t(n.node,n.x0,n.x1);return this}function Lt(t){return t[0]}function Tt(t){return arguments.length?(this._x=t,this):this._x}function O(t,e){var r=new it(e??Lt,NaN,NaN);return t==null?r:r.addAll(t)}function it(t,e,r){this._x=t,this._x0=e,this._x1=r,this._root=void 0}function jt(t){for(var e={data:t.data},r=e;t=t.next;)r=r.next={data:t.data};return e}var W=O.prototype=it.prototype;W.copy=function(){var t=new it(this._x,this._x0,this._x1),e=this._root,r,n;if(!e)return t;if(!e.length)return t._root=jt(e),t;for(r=[{source:e,target:t._root=new Array(2)}];e=r.pop();)for(var i=0;i<2;++i)(n=e.source[i])&&(n.length?r.push({source:n,target:e.target[i]=new Array(2)}):e.target[i]=jt(n));return t};W.add=zt;W.addAll=kt;W.cover=St;W.data=It;W.extent=qt;W.find=Ft;W.remove=Pt;W.removeAll=Wt;W.root=Bt;W.size=Dt;W.visit=Rt;W.visitAfter=Et;W.x=Tt;function Ot(t){let e=+this._x.call(null,t),r=+this._y.call(null,t);return Ct(this.cover(e,r),e,r,t)}function Ct(t,e,r,n){if(isNaN(e)||isNaN(r))return t;var i,o=t._root,f={data:n},a=t._x0,s=t._y0,l=t._x1,h=t._y1,c,x,y,p,w,v,u,g;if(!o)return t._root=f,t;for(;o.length;)if((w=e>=(c=(a+l)/2))?a=c:l=c,(v=r>=(x=(s+h)/2))?s=x:h=x,i=o,!(o=o[u=v<<1|w]))return i[u]=f,t;if(y=+t._x.call(null,o.data),p=+t._y.call(null,o.data),e===y&&r===p)return f.next=o,i?i[u]=f:t._root=f,t;do i=i?i[u]=new Array(4):t._root=new Array(4),(w=e>=(c=(a+l)/2))?a=c:l=c,(v=r>=(x=(s+h)/2))?s=x:h=x;while((u=v<<1|w)===(g=(p>=x)<<1|y>=c));return i[g]=o,i[u]=f,t}function Xt(t){var e,r,n=t.length,i,o,f=new Array(n),a=new Array(n),s=1/0,l=1/0,h=-1/0,c=-1/0;for(r=0;r<n;++r)isNaN(i=+this._x.call(null,e=t[r]))||isNaN(o=+this._y.call(null,e))||(f[r]=i,a[r]=o,i<s&&(s=i),i>h&&(h=i),o<l&&(l=o),o>c&&(c=o));if(s>h||l>c)return this;for(this.cover(s,l).cover(h,c),r=0;r<n;++r)Ct(this,f[r],a[r],t[r]);return this}function Yt(t,e){if(isNaN(t=+t)||isNaN(e=+e))return this;var r=this._x0,n=this._y0,i=this._x1,o=this._y1;if(isNaN(r))i=(r=Math.floor(t))+1,o=(n=Math.floor(e))+1;else{for(var f=i-r||1,a=this._root,s,l;r>t||t>=i||n>e||e>=o;)switch(l=(e<n)<<1|t<r,s=new Array(4),s[l]=a,a=s,f*=2,l){case 0:i=r+f,o=n+f;break;case 1:r=i-f,o=n+f;break;case 2:i=r+f,n=o-f;break;case 3:r=i-f,n=o-f;break}this._root&&this._root.length&&(this._root=a)}return this._x0=r,this._y0=n,this._x1=i,this._y1=o,this}function Ht(){var t=[];return this.visit(function(e){if(!e.length)do t.push(e.data);while(e=e.next)}),t}function Qt(t){return arguments.length?this.cover(+t[0][0],+t[0][1]).cover(+t[1][0],+t[1][1]):isNaN(this._x0)?void 0:[[this._x0,this._y0],[this._x1,this._y1]]}function I(t,e,r,n,i){this.node=t,this.x0=e,this.y0=r,this.x1=n,this.y1=i}function Zt(t,e,r){var n,i=this._x0,o=this._y0,f,a,s,l,h=this._x1,c=this._y1,x=[],y=this._root,p,w;for(y&&x.push(new I(y,i,o,h,c)),r==null?r=1/0:(i=t-r,o=e-r,h=t+r,c=e+r,r*=r);p=x.pop();)if(!(!(y=p.node)||(f=p.x0)>h||(a=p.y0)>c||(s=p.x1)<i||(l=p.y1)<o))if(y.length){var v=(f+s)/2,u=(a+l)/2;x.push(new I(y[3],v,u,s,l),new I(y[2],f,u,v,l),new I(y[1],v,a,s,u),new I(y[0],f,a,v,u)),(w=(e>=u)<<1|t>=v)&&(p=x[x.length-1],x[x.length-1]=x[x.length-1-w],x[x.length-1-w]=p)}else{var g=t-+this._x.call(null,y.data),d=e-+this._y.call(null,y.data),m=g*g+d*d;if(m<r){var _=Math.sqrt(r=m);i=t-_,o=e-_,h=t+_,c=e+_,n=y.data}}return n}function Gt(t){if(isNaN(h=+this._x.call(null,t))||isNaN(c=+this._y.call(null,t)))return this;var e,r=this._root,n,i,o,f=this._x0,a=this._y0,s=this._x1,l=this._y1,h,c,x,y,p,w,v,u;if(!r)return this;if(r.length)for(;;){if((p=h>=(x=(f+s)/2))?f=x:s=x,(w=c>=(y=(a+l)/2))?a=y:l=y,e=r,!(r=r[v=w<<1|p]))return this;if(!r.length)break;(e[v+1&3]||e[v+2&3]||e[v+3&3])&&(n=e,u=v)}for(;r.data!==t;)if(i=r,!(r=r.next))return this;return(o=r.next)&&delete r.next,i?(o?i.next=o:delete i.next,this):e?(o?e[v]=o:delete e[v],(r=e[0]||e[1]||e[2]||e[3])&&r===(e[3]||e[2]||e[1]||e[0])&&!r.length&&(n?n[u]=r:this._root=r),this):(this._root=o,this)}function Ut(t){for(var e=0,r=t.length;e<r;++e)this.remove(t[e]);return this}function Jt(){return this._root}function Kt(){var t=0;return this.visit(function(e){if(!e.length)do++t;while(e=e.next)}),t}function Vt(t){var e=[],r,n=this._root,i,o,f,a,s;for(n&&e.push(new I(n,this._x0,this._y0,this._x1,this._y1));r=e.pop();)if(!t(n=r.node,o=r.x0,f=r.y0,a=r.x1,s=r.y1)&&n.length){var l=(o+a)/2,h=(f+s)/2;(i=n[3])&&e.push(new I(i,l,h,a,s)),(i=n[2])&&e.push(new I(i,o,h,l,s)),(i=n[1])&&e.push(new I(i,l,f,a,h)),(i=n[0])&&e.push(new I(i,o,f,l,h))}return this}function $t(t){var e=[],r=[],n;for(this._root&&e.push(new I(this._root,this._x0,this._y0,this._x1,this._y1));n=e.pop();){var i=n.node;if(i.length){var o,f=n.x0,a=n.y0,s=n.x1,l=n.y1,h=(f+s)/2,c=(a+l)/2;(o=i[0])&&e.push(new I(o,f,a,h,c)),(o=i[1])&&e.push(new I(o,h,a,s,c)),(o=i[2])&&e.push(new I(o,f,c,h,l)),(o=i[3])&&e.push(new I(o,h,c,s,l))}r.push(n)}for(;n=r.pop();)t(n.node,n.x0,n.y0,n.x1,n.y1);return this}function te(t){return t[0]}function ee(t){return arguments.length?(this._x=t,this):this._x}function re(t){return t[1]}function ne(t){return arguments.length?(this._y=t,this):this._y}function C(t,e,r){var n=new ot(e??te,r??re,NaN,NaN,NaN,NaN);return t==null?n:n.addAll(t)}function ot(t,e,r,n,i,o){this._x=t,this._y=e,this._x0=r,this._y0=n,this._x1=i,this._y1=o,this._root=void 0}function ie(t){for(var e={data:t.data},r=e;t=t.next;)r=r.next={data:t.data};return e}var F=C.prototype=ot.prototype;F.copy=function(){var t=new ot(this._x,this._y,this._x0,this._y0,this._x1,this._y1),e=this._root,r,n;if(!e)return t;if(!e.length)return t._root=ie(e),t;for(r=[{source:e,target:t._root=new Array(4)}];e=r.pop();)for(var i=0;i<4;++i)(n=e.source[i])&&(n.length?r.push({source:n,target:e.target[i]=new Array(4)}):e.target[i]=ie(n));return t};F.add=Ot;F.addAll=Xt;F.cover=Yt;F.data=Ht;F.extent=Qt;F.find=Zt;F.remove=Gt;F.removeAll=Ut;F.root=Jt;F.size=Kt;F.visit=Vt;F.visitAfter=$t;F.x=ee;F.y=ne;function oe(t){let e=+this._x.call(null,t),r=+this._y.call(null,t),n=+this._z.call(null,t);return ae(this.cover(e,r,n),e,r,n,t)}function ae(t,e,r,n,i){if(isNaN(e)||isNaN(r)||isNaN(n))return t;var o,f=t._root,a={data:i},s=t._x0,l=t._y0,h=t._z0,c=t._x1,x=t._y1,y=t._z1,p,w,v,u,g,d,m,_,N,A,M;if(!f)return t._root=a,t;for(;f.length;)if((m=e>=(p=(s+c)/2))?s=p:c=p,(_=r>=(w=(l+x)/2))?l=w:x=w,(N=n>=(v=(h+y)/2))?h=v:y=v,o=f,!(f=f[A=N<<2|_<<1|m]))return o[A]=a,t;if(u=+t._x.call(null,f.data),g=+t._y.call(null,f.data),d=+t._z.call(null,f.data),e===u&&r===g&&n===d)return a.next=f,o?o[A]=a:t._root=a,t;do o=o?o[A]=new Array(8):t._root=new Array(8),(m=e>=(p=(s+c)/2))?s=p:c=p,(_=r>=(w=(l+x)/2))?l=w:x=w,(N=n>=(v=(h+y)/2))?h=v:y=v;while((A=N<<2|_<<1|m)===(M=(d>=v)<<2|(g>=w)<<1|u>=p));return o[M]=f,o[A]=a,t}function fe(t){Array.isArray(t)||(t=Array.from(t));let e=t.length,r=new Float64Array(e),n=new Float64Array(e),i=new Float64Array(e),o=1/0,f=1/0,a=1/0,s=-1/0,l=-1/0,h=-1/0;for(let c=0,x,y,p,w;c<e;++c)isNaN(y=+this._x.call(null,x=t[c]))||isNaN(p=+this._y.call(null,x))||isNaN(w=+this._z.call(null,x))||(r[c]=y,n[c]=p,i[c]=w,y<o&&(o=y),y>s&&(s=y),p<f&&(f=p),p>l&&(l=p),w<a&&(a=w),w>h&&(h=w));if(o>s||f>l||a>h)return this;this.cover(o,f,a).cover(s,l,h);for(let c=0;c<e;++c)ae(this,r[c],n[c],i[c],t[c]);return this}function se(t,e,r){if(isNaN(t=+t)||isNaN(e=+e)||isNaN(r=+r))return this;var n=this._x0,i=this._y0,o=this._z0,f=this._x1,a=this._y1,s=this._z1;if(isNaN(n))f=(n=Math.floor(t))+1,a=(i=Math.floor(e))+1,s=(o=Math.floor(r))+1;else{for(var l=f-n||1,h=this._root,c,x;n>t||t>=f||i>e||e>=a||o>r||r>=s;)switch(x=(r<o)<<2|(e<i)<<1|t<n,c=new Array(8),c[x]=h,h=c,l*=2,x){case 0:f=n+l,a=i+l,s=o+l;break;case 1:n=f-l,a=i+l,s=o+l;break;case 2:f=n+l,i=a-l,s=o+l;break;case 3:n=f-l,i=a-l,s=o+l;break;case 4:f=n+l,a=i+l,o=s-l;break;case 5:n=f-l,a=i+l,o=s-l;break;case 6:f=n+l,i=a-l,o=s-l;break;case 7:n=f-l,i=a-l,o=s-l;break}this._root&&this._root.length&&(this._root=h)}return this._x0=n,this._y0=i,this._z0=o,this._x1=f,this._y1=a,this._z1=s,this}function le(){var t=[];return this.visit(function(e){if(!e.length)do t.push(e.data);while(e=e.next)}),t}function ue(t){return arguments.length?this.cover(+t[0][0],+t[0][1],+t[0][2]).cover(+t[1][0],+t[1][1],+t[1][2]):isNaN(this._x0)?void 0:[[this._x0,this._y0,this._z0],[this._x1,this._y1,this._z1]]}function z(t,e,r,n,i,o,f){this.node=t,this.x0=e,this.y0=r,this.z0=n,this.x1=i,this.y1=o,this.z1=f}function he(t,e,r,n){var i,o=this._x0,f=this._y0,a=this._z0,s,l,h,c,x,y,p=this._x1,w=this._y1,v=this._z1,u=[],g=this._root,d,m;for(g&&u.push(new z(g,o,f,a,p,w,v)),n==null?n=1/0:(o=t-n,f=e-n,a=r-n,p=t+n,w=e+n,v=r+n,n*=n);d=u.pop();)if(!(!(g=d.node)||(s=d.x0)>p||(l=d.y0)>w||(h=d.z0)>v||(c=d.x1)<o||(x=d.y1)<f||(y=d.z1)<a))if(g.length){var _=(s+c)/2,N=(l+x)/2,A=(h+y)/2;u.push(new z(g[7],_,N,A,c,x,y),new z(g[6],s,N,A,_,x,y),new z(g[5],_,l,A,c,N,y),new z(g[4],s,l,A,_,N,y),new z(g[3],_,N,h,c,x,A),new z(g[2],s,N,h,_,x,A),new z(g[1],_,l,h,c,N,A),new z(g[0],s,l,h,_,N,A)),(m=(r>=A)<<2|(e>=N)<<1|t>=_)&&(d=u[u.length-1],u[u.length-1]=u[u.length-1-m],u[u.length-1-m]=d)}else{var M=t-+this._x.call(null,g.data),B=e-+this._y.call(null,g.data),D=r-+this._z.call(null,g.data),P=M*M+B*B+D*D;if(P<n){var S=Math.sqrt(n=P);o=t-S,f=e-S,a=r-S,p=t+S,w=e+S,v=r+S,i=g.data}}return i}var Oe=(t,e,r,n,i,o)=>Math.sqrt((t-n)**2+(e-i)**2+(r-o)**2);function ce(t,e,r,n){let i=[],o=t-n,f=e-n,a=r-n,s=t+n,l=e+n,h=r+n;return this.visit((c,x,y,p,w,v,u)=>{if(!c.length)do{let g=c.data;Oe(t,e,r,this._x(g),this._y(g),this._z(g))<=n&&i.push(g)}while(c=c.next);return x>s||y>l||p>h||w<o||v<f||u<a}),i}function pe(t){if(isNaN(x=+this._x.call(null,t))||isNaN(y=+this._y.call(null,t))||isNaN(p=+this._z.call(null,t)))return this;var e,r=this._root,n,i,o,f=this._x0,a=this._y0,s=this._z0,l=this._x1,h=this._y1,c=this._z1,x,y,p,w,v,u,g,d,m,_,N;if(!r)return this;if(r.length)for(;;){if((g=x>=(w=(f+l)/2))?f=w:l=w,(d=y>=(v=(a+h)/2))?a=v:h=v,(m=p>=(u=(s+c)/2))?s=u:c=u,e=r,!(r=r[_=m<<2|d<<1|g]))return this;if(!r.length)break;(e[_+1&7]||e[_+2&7]||e[_+3&7]||e[_+4&7]||e[_+5&7]||e[_+6&7]||e[_+7&7])&&(n=e,N=_)}for(;r.data!==t;)if(i=r,!(r=r.next))return this;return(o=r.next)&&delete r.next,i?(o?i.next=o:delete i.next,this):e?(o?e[_]=o:delete e[_],(r=e[0]||e[1]||e[2]||e[3]||e[4]||e[5]||e[6]||e[7])&&r===(e[7]||e[6]||e[5]||e[4]||e[3]||e[2]||e[1]||e[0])&&!r.length&&(n?n[N]=r:this._root=r),this):(this._root=o,this)}function xe(t){for(var e=0,r=t.length;e<r;++e)this.remove(t[e]);return this}function _e(){return this._root}function ye(){var t=0;return this.visit(function(e){if(!e.length)do++t;while(e=e.next)}),t}function ve(t){var e=[],r,n=this._root,i,o,f,a,s,l,h;for(n&&e.push(new z(n,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1));r=e.pop();)if(!t(n=r.node,o=r.x0,f=r.y0,a=r.z0,s=r.x1,l=r.y1,h=r.z1)&&n.length){var c=(o+s)/2,x=(f+l)/2,y=(a+h)/2;(i=n[7])&&e.push(new z(i,c,x,y,s,l,h)),(i=n[6])&&e.push(new z(i,o,x,y,c,l,h)),(i=n[5])&&e.push(new z(i,c,f,y,s,x,h)),(i=n[4])&&e.push(new z(i,o,f,y,c,x,h)),(i=n[3])&&e.push(new z(i,c,x,a,s,l,y)),(i=n[2])&&e.push(new z(i,o,x,a,c,l,y)),(i=n[1])&&e.push(new z(i,c,f,a,s,x,y)),(i=n[0])&&e.push(new z(i,o,f,a,c,x,y))}return this}function me(t){var e=[],r=[],n;for(this._root&&e.push(new z(this._root,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1));n=e.pop();){var i=n.node;if(i.length){var o,f=n.x0,a=n.y0,s=n.z0,l=n.x1,h=n.y1,c=n.z1,x=(f+l)/2,y=(a+h)/2,p=(s+c)/2;(o=i[0])&&e.push(new z(o,f,a,s,x,y,p)),(o=i[1])&&e.push(new z(o,x,a,s,l,y,p)),(o=i[2])&&e.push(new z(o,f,y,s,x,h,p)),(o=i[3])&&e.push(new z(o,x,y,s,l,h,p)),(o=i[4])&&e.push(new z(o,f,a,p,x,y,c)),(o=i[5])&&e.push(new z(o,x,a,p,l,y,c)),(o=i[6])&&e.push(new z(o,f,y,p,x,h,c)),(o=i[7])&&e.push(new z(o,x,y,p,l,h,c))}r.push(n)}for(;n=r.pop();)t(n.node,n.x0,n.y0,n.z0,n.x1,n.y1,n.z1);return this}function de(t){return t[0]}function ge(t){return arguments.length?(this._x=t,this):this._x}function we(t){return t[1]}function Ne(t){return arguments.length?(this._y=t,this):this._y}function Ae(t){return t[2]}function Me(t){return arguments.length?(this._z=t,this):this._z}function X(t,e,r,n){var i=new at(e??de,r??we,n??Ae,NaN,NaN,NaN,NaN,NaN,NaN);return t==null?i:i.addAll(t)}function at(t,e,r,n,i,o,f,a,s){this._x=t,this._y=e,this._z=r,this._x0=n,this._y0=i,this._z0=o,this._x1=f,this._y1=a,this._z1=s,this._root=void 0}function ze(t){for(var e={data:t.data},r=e;t=t.next;)r=r.next={data:t.data};return e}var q=X.prototype=at.prototype;q.copy=function(){var t=new at(this._x,this._y,this._z,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1),e=this._root,r,n;if(!e)return t;if(!e.length)return t._root=ze(e),t;for(r=[{source:e,target:t._root=new Array(8)}];e=r.pop();)for(var i=0;i<8;++i)(n=e.source[i])&&(n.length?r.push({source:n,target:e.target[i]=new Array(8)}):e.target[i]=ze(n));return t};q.add=oe;q.addAll=fe;q.cover=se;q.data=le;q.extent=ue;q.find=he;q.findAllWithinRadius=ce;q.remove=pe;q.removeAll=xe;q.root=_e;q.size=ye;q.visit=ve;q.visitAfter=me;q.x=ge;q.y=Ne;q.z=Me;function b(t){return function(){return t}}function E(t){return(t()-.5)*1e-6}function Ce(t){return t.index}function be(t,e){var r=t.get(e);if(!r)throw new Error("node not found: "+e);return r}function ft(t){var e=Ce,r=x,n,i=b(30),o,f,a,s,l,h,c=1;t==null&&(t=[]);function x(u){return 1/Math.min(s[u.source.index],s[u.target.index])}function y(u){for(var g=0,d=t.length;g<c;++g)for(var m=0,_,N,A,M=0,B=0,D=0,P,S;m<d;++m)_=t[m],N=_.source,A=_.target,M=A.x+A.vx-N.x-N.vx||E(h),a>1&&(B=A.y+A.vy-N.y-N.vy||E(h)),a>2&&(D=A.z+A.vz-N.z-N.vz||E(h)),P=Math.sqrt(M*M+B*B+D*D),P=(P-o[m])/P*u*n[m],M*=P,B*=P,D*=P,A.vx-=M*(S=l[m]),a>1&&(A.vy-=B*S),a>2&&(A.vz-=D*S),N.vx+=M*(S=1-S),a>1&&(N.vy+=B*S),a>2&&(N.vz+=D*S)}function p(){if(f){var u,g=f.length,d=t.length,m=new Map(f.map((N,A)=>[e(N,A,f),N])),_;for(u=0,s=new Array(g);u<d;++u)_=t[u],_.index=u,typeof _.source!="object"&&(_.source=be(m,_.source)),typeof _.target!="object"&&(_.target=be(m,_.target)),s[_.source.index]=(s[_.source.index]||0)+1,s[_.target.index]=(s[_.target.index]||0)+1;for(u=0,l=new Array(d);u<d;++u)_=t[u],l[u]=s[_.source.index]/(s[_.source.index]+s[_.target.index]);n=new Array(d),w(),o=new Array(d),v()}}function w(){if(f)for(var u=0,g=t.length;u<g;++u)n[u]=+r(t[u],u,t)}function v(){if(f)for(var u=0,g=t.length;u<g;++u)o[u]=+i(t[u],u,t)}return y.initialize=function(u,...g){f=u,h=g.find(d=>typeof d=="function")||Math.random,a=g.find(d=>[1,2,3].includes(d))||2,p()},y.links=function(u){return arguments.length?(t=u,p(),y):t},y.id=function(u){return arguments.length?(e=u,y):e},y.iterations=function(u){return arguments.length?(c=+u,y):c},y.strength=function(u){return arguments.length?(r=typeof u=="function"?u:b(+u),w(),y):r},y.distance=function(u){return arguments.length?(i=typeof u=="function"?u:b(+u),v(),y):i},y}var Xe={value:()=>{}};function Se(){for(var t=0,e=arguments.length,r={},n;t<e;++t){if(!(n=arguments[t]+"")||n in r||/[\\s.]/.test(n))throw new Error("illegal type: "+n);r[n]=[]}return new J(r)}function J(t){this._=t}function Ye(t,e){return t.trim().split(/^|\\s+/).map(function(r){var n="",i=r.indexOf(".");if(i>=0&&(n=r.slice(i+1),r=r.slice(0,i)),r&&!e.hasOwnProperty(r))throw new Error("unknown type: "+r);return{type:r,name:n}})}J.prototype=Se.prototype={constructor:J,on:function(t,e){var r=this._,n=Ye(t+"",r),i,o=-1,f=n.length;if(arguments.length<2){for(;++o<f;)if((i=(t=n[o]).type)&&(i=He(r[i],t.name)))return i;return}if(e!=null&&typeof e!="function")throw new Error("invalid callback: "+e);for(;++o<f;)if(i=(t=n[o]).type)r[i]=ke(r[i],t.name,e);else if(e==null)for(i in r)r[i]=ke(r[i],t.name,null);return this},copy:function(){var t={},e=this._;for(var r in e)t[r]=e[r].slice();return new J(t)},call:function(t,e){if((i=arguments.length-2)>0)for(var r=new Array(i),n=0,i,o;n<i;++n)r[n]=arguments[n+2];if(!this._.hasOwnProperty(t))throw new Error("unknown type: "+t);for(o=this._[t],n=0,i=o.length;n<i;++n)o[n].value.apply(e,r)},apply:function(t,e,r){if(!this._.hasOwnProperty(t))throw new Error("unknown type: "+t);for(var n=this._[t],i=0,o=n.length;i<o;++i)n[i].value.apply(e,r)}};function He(t,e){for(var r=0,n=t.length,i;r<n;++r)if((i=t[r]).name===e)return i.value}function ke(t,e,r){for(var n=0,i=t.length;n<i;++n)if(t[n].name===e){t[n]=Xe,t=t.slice(0,n).concat(t.slice(n+1));break}return r!=null&&t.push({name:e,value:r}),t}var st=Se;var j=0,H=0,Y=0,qe=1e3,K,Q,V=0,T=0,$=0,Z=typeof performance=="object"&&performance.now?performance:Date,Fe=typeof window=="object"&&window.requestAnimationFrame?window.requestAnimationFrame.bind(window):function(t){setTimeout(t,17)};function ht(){return T||(Fe(Qe),T=Z.now()+$)}function Qe(){T=0}function lt(){this._call=this._time=this._next=null}lt.prototype=tt.prototype={constructor:lt,restart:function(t,e,r){if(typeof t!="function")throw new TypeError("callback is not a function");r=(r==null?ht():+r)+(e==null?0:+e),!this._next&&Q!==this&&(Q?Q._next=this:K=this,Q=this),this._call=t,this._time=r,ut()},stop:function(){this._call&&(this._call=null,this._time=1/0,ut())}};function tt(t,e,r){var n=new lt;return n.restart(t,e,r),n}function Pe(){ht(),++j;for(var t=K,e;t;)(e=T-t._time)>=0&&t._call.call(void 0,e),t=t._next;--j}function Ie(){T=(V=Z.now())+$,j=H=0;try{Pe()}finally{j=0,Ge(),T=0}}function Ze(){var t=Z.now(),e=t-V;e>qe&&($-=e,V=t)}function Ge(){for(var t,e=K,r,n=1/0;e;)e._call?(n>e._time&&(n=e._time),t=e,e=e._next):(r=e._next,e._next=null,e=t?t._next=r:K=r);Q=t,ut(n)}function ut(t){if(!j){H&&(H=clearTimeout(H));var e=t-T;e>24?(t<1/0&&(H=setTimeout(Ie,t-Z.now()-$)),Y&&(Y=clearInterval(Y))):(Y||(V=Z.now(),Y=setInterval(Ze,qe)),j=1,Fe(Ie))}}function We(){let t=1;return()=>(t=(1664525*t+1013904223)%4294967296)/4294967296}var Be=3;function et(t){return t.x}function ct(t){return t.y}function De(t){return t.z}var Ue=10,Je=Math.PI*(3-Math.sqrt(5)),Ke=Math.PI*20/(9+Math.sqrt(221));function pt(t,e){e=e||2;var r=Math.min(Be,Math.max(1,Math.round(e))),n,i=1,o=.001,f=1-Math.pow(o,1/300),a=0,s=.6,l=new Map,h=tt(y),c=st("tick","end"),x=We();t==null&&(t=[]);function y(){p(),c.call("tick",n),i<o&&(h.stop(),c.call("end",n))}function p(u){var g,d=t.length,m;u===void 0&&(u=1);for(var _=0;_<u;++_)for(i+=(a-i)*f,l.forEach(function(N){N(i)}),g=0;g<d;++g)m=t[g],m.fx==null?m.x+=m.vx*=s:(m.x=m.fx,m.vx=0),r>1&&(m.fy==null?m.y+=m.vy*=s:(m.y=m.fy,m.vy=0)),r>2&&(m.fz==null?m.z+=m.vz*=s:(m.z=m.fz,m.vz=0));return n}function w(){for(var u=0,g=t.length,d;u<g;++u){if(d=t[u],d.index=u,d.fx!=null&&(d.x=d.fx),d.fy!=null&&(d.y=d.fy),d.fz!=null&&(d.z=d.fz),isNaN(d.x)||r>1&&isNaN(d.y)||r>2&&isNaN(d.z)){var m=Ue*(r>2?Math.cbrt(.5+u):r>1?Math.sqrt(.5+u):u),_=u*Je,N=u*Ke;r===1?d.x=m:r===2?(d.x=m*Math.cos(_),d.y=m*Math.sin(_)):(d.x=m*Math.sin(_)*Math.cos(N),d.y=m*Math.cos(_),d.z=m*Math.sin(_)*Math.sin(N))}(isNaN(d.vx)||r>1&&isNaN(d.vy)||r>2&&isNaN(d.vz))&&(d.vx=0,r>1&&(d.vy=0),r>2&&(d.vz=0))}}function v(u){return u.initialize&&u.initialize(t,x,r),u}return w(),n={tick:p,restart:function(){return h.restart(y),n},stop:function(){return h.stop(),n},numDimensions:function(u){return arguments.length?(r=Math.min(Be,Math.max(1,Math.round(u))),l.forEach(v),n):r},nodes:function(u){return arguments.length?(t=u,w(),l.forEach(v),n):t},alpha:function(u){return arguments.length?(i=+u,n):i},alphaMin:function(u){return arguments.length?(o=+u,n):o},alphaDecay:function(u){return arguments.length?(f=+u,n):+f},alphaTarget:function(u){return arguments.length?(a=+u,n):a},velocityDecay:function(u){return arguments.length?(s=1-u,n):1-s},randomSource:function(u){return arguments.length?(x=u,l.forEach(v),n):x},force:function(u,g){return arguments.length>1?(g==null?l.delete(u):l.set(u,v(g)),n):l.get(u)},find:function(){var u=Array.prototype.slice.call(arguments),g=u.shift()||0,d=(r>1?u.shift():null)||0,m=(r>2?u.shift():null)||0,_=u.shift()||1/0,N=0,A=t.length,M,B,D,P,S,Mt;for(_*=_,N=0;N<A;++N)S=t[N],M=g-S.x,B=d-(S.y||0),D=m-(S.z||0),P=M*M+B*B+D*D,P<_&&(Mt=S,_=P);return Mt},on:function(u,g){return arguments.length>1?(c.on(u,g),n):c.on(u)}}}function xt(){var t,e,r,n,i,o=b(-30),f,a=1,s=1/0,l=.81;function h(p){var w,v=t.length,u=(e===1?O(t,et):e===2?C(t,et,ct):e===3?X(t,et,ct,De):null).visitAfter(x);for(i=p,w=0;w<v;++w)r=t[w],u.visit(y)}function c(){if(t){var p,w=t.length,v;for(f=new Array(w),p=0;p<w;++p)v=t[p],f[v.index]=+o(v,p,t)}}function x(p){var w=0,v,u,g=0,d,m,_,N,A=p.length;if(A){for(d=m=_=N=0;N<A;++N)(v=p[N])&&(u=Math.abs(v.value))&&(w+=v.value,g+=u,d+=u*(v.x||0),m+=u*(v.y||0),_+=u*(v.z||0));w*=Math.sqrt(4/A),p.x=d/g,e>1&&(p.y=m/g),e>2&&(p.z=_/g)}else{v=p,v.x=v.data.x,e>1&&(v.y=v.data.y),e>2&&(v.z=v.data.z);do w+=f[v.data.index];while(v=v.next)}p.value=w}function y(p,w,v,u,g){if(!p.value)return!0;var d=[v,u,g][e-1],m=p.x-r.x,_=e>1?p.y-r.y:0,N=e>2?p.z-r.z:0,A=d-w,M=m*m+_*_+N*N;if(A*A/l<M)return M<s&&(m===0&&(m=E(n),M+=m*m),e>1&&_===0&&(_=E(n),M+=_*_),e>2&&N===0&&(N=E(n),M+=N*N),M<a&&(M=Math.sqrt(a*M)),r.vx+=m*p.value*i/M,e>1&&(r.vy+=_*p.value*i/M),e>2&&(r.vz+=N*p.value*i/M)),!0;if(p.length||M>=s)return;(p.data!==r||p.next)&&(m===0&&(m=E(n),M+=m*m),e>1&&_===0&&(_=E(n),M+=_*_),e>2&&N===0&&(N=E(n),M+=N*N),M<a&&(M=Math.sqrt(a*M)));do p.data!==r&&(A=f[p.data.index]*i/M,r.vx+=m*A,e>1&&(r.vy+=_*A),e>2&&(r.vz+=N*A));while(p=p.next)}return h.initialize=function(p,...w){t=p,n=w.find(v=>typeof v=="function")||Math.random,e=w.find(v=>[1,2,3].includes(v))||2,c()},h.strength=function(p){return arguments.length?(o=typeof p=="function"?p:b(+p),c(),h):o},h.distanceMin=function(p){return arguments.length?(a=p*p,h):Math.sqrt(a)},h.distanceMax=function(p){return arguments.length?(s=p*p,h):Math.sqrt(s)},h.theta=function(p){return arguments.length?(l=p*p,h):Math.sqrt(l)},h}function _t(t){var e=b(.1),r,n,i;typeof t!="function"&&(t=b(t==null?0:+t));function o(a){for(var s=0,l=r.length,h;s<l;++s)h=r[s],h.vx+=(i[s]-h.x)*n[s]*a}function f(){if(r){var a,s=r.length;for(n=new Array(s),i=new Array(s),a=0;a<s;++a)n[a]=isNaN(i[a]=+t(r[a],a,r))?0:+e(r[a],a,r)}}return o.initialize=function(a){r=a,f()},o.strength=function(a){return arguments.length?(e=typeof a=="function"?a:b(+a),f(),o):e},o.x=function(a){return arguments.length?(t=typeof a=="function"?a:b(+a),f(),o):t},o}function yt(t){var e=b(.1),r,n,i;typeof t!="function"&&(t=b(t==null?0:+t));function o(a){for(var s=0,l=r.length,h;s<l;++s)h=r[s],h.vy+=(i[s]-h.y)*n[s]*a}function f(){if(r){var a,s=r.length;for(n=new Array(s),i=new Array(s),a=0;a<s;++a)n[a]=isNaN(i[a]=+t(r[a],a,r))?0:+e(r[a],a,r)}}return o.initialize=function(a){r=a,f()},o.strength=function(a){return arguments.length?(e=typeof a=="function"?a:b(+a),f(),o):e},o.y=function(a){return arguments.length?(t=typeof a=="function"?a:b(+a),f(),o):t},o}function vt(t){var e=b(.1),r,n,i;typeof t!="function"&&(t=b(t==null?0:+t));function o(a){for(var s=0,l=r.length,h;s<l;++s)h=r[s],h.vz+=(i[s]-h.z)*n[s]*a}function f(){if(r){var a,s=r.length;for(n=new Array(s),i=new Array(s),a=0;a<s;++a)n[a]=isNaN(i[a]=+t(r[a],a,r))?0:+e(r[a],a,r)}}return o.initialize=function(a){r=a,f()},o.strength=function(a){return arguments.length?(e=typeof a=="function"?a:b(+a),f(),o):e},o.z=function(a){return arguments.length?(t=typeof a=="function"?a:b(+a),f(),o):t},o}function mt(t,e){let r=[],n=1,i=o=>{if(t!==0)for(let f of r){let a=f.x??0,s=f.z??0,l=Math.hypot(a,s);if(l<1e-4)continue;let h=Math.min(Math.max((e[f.index??0]||1)/n,.3),3),c=t*h*o*l/200;f.vx=(f.vx??0)-a/l*c,f.vz=(f.vz??0)-s/l*c}};return i.initialize=o=>{r=o;let f=0;for(let a of o)f+=e[a.index??0]||1;n=o.length?f/o.length:1},i}function dt(t){let e=[],r=n=>{if(t!==0)for(let i of e){let o=i.x??0,f=i.z??0,a=Math.hypot(o,f);if(a<.001)continue;let s=1/(1+a/160),l=t*n*s;i.vx=(i.vx??0)+-f/a*l*a,i.vz=(i.vz??0)+o/a*l*a}};return r.initialize=n=>{e=n},r}function gt(t,e){let r=[],n=i=>{if(!(!(t>0)||!e))for(let o of r){let f=o.x||0,a=o.y||0,s=o.z||0,l=Math.hypot(f,a,s);if(l<=t||l<1e-6)continue;let h=e*i*(l-t)/l;o.vx=(o.vx||0)-f*h,o.vy=(o.vy||0)-a*h,o.vz=(o.vz||0)-s*h}};return n.initialize=i=>{r=i},n}function Re(t,e){return(t||0)*e*.42}var zi={perScreen:1.25*Math.PI,damping:1.5,stopBelow:.015,resumeMs:4e3,rampMs:2500,auto:.06};var Le=self,k=null,G=[],U=new Float32Array(0),Ee=new Float32Array(0),wt=[],L=!0,At=0,nt=!1,Nt=!1;function Te(t){return e=>{let r=typeof e.source=="number"?e.source:e.source.index??0,n=typeof e.target=="number"?e.target:e.target.index??0,i=1/Math.min(U[r]??1,U[n]??1);return Math.min(i*t,1)}}function Ve(t){if(!k)return;k.force("charge")?.strength(t.charge);let e=k.force("link");e?.distance(t.linkDistance),e?.strength(Te(t.linkStrength)),k.force("x")?.strength(t.centerPull+(t.sidePull??0)),k.force("y")?.strength(t.centerPull+t.flatten),k.force("z")?.strength(t.centerPull),k.force("core",mt(t.coreGravity,U)),k.force("spiral",dt(t.spiral)),k.force("ball",gt(t.ball??0,t.ballStrength??0))}function rt(){Nt||(Nt=!0,self.setTimeout($e,0))}function $e(){Nt=!1;let t=k;if(!t||L)return;let e=Date.now();for(;Date.now()-e<12;)if(t.tick(),At++,t.alpha()<t.alphaMin()){L=!0;break}nt=!0,je(),L||rt()}function je(){if(!nt||!k)return;let t=wt.pop();if(!t)return;let e=new Float32Array(t);for(let r=0;r<G.length;r++){let n=G[r];n&&(e[r*3]=n.x,e[r*3+1]=n.y,e[r*3+2]=n.z)}nt=!1,Le.postMessage({type:"tick",buffer:t,alpha:k.alpha(),settled:L,ticks:At},[t])}Le.onmessage=t=>{let e=t.data;switch(e.type){case"init":{k?.stop();let r=new Float32Array(e.positions);U=new Float32Array(e.degrees),Ee=e.sides?new Float32Array(e.sides):new Float32Array(e.count);let n=new Uint32Array(e.links);G=[];for(let o=0;o<e.count;o++)G.push({x:r[o*3]??0,y:r[o*3+1]??0,z:r[o*3+2]??0});let i=[];for(let o=0;o<n.length;o+=2)i.push({source:n[o]??0,target:n[o+1]??0});k=pt(G,3).alphaDecay(1-Math.pow(.001,1/300)).velocityDecay(e.params.velocityDecay).force("link",ft(i).distance(e.params.linkDistance).strength(Te(e.params.linkStrength))).force("charge",xt().strength(e.params.charge).distanceMax(800)).force("x",_t((o,f)=>Re(Ee[f]??0,e.params.ball??0)).strength(e.params.centerPull+(e.params.sidePull??0))).force("y",yt(0).strength(e.params.centerPull+e.params.flatten)).force("z",vt(0).strength(e.params.centerPull)).force("core",mt(e.params.coreGravity,U)).force("spiral",dt(e.params.spiral)).force("ball",gt(e.params.ball??0,e.params.ballStrength??0)).stop(),k.alpha(e.initialAlpha),wt=[e.bufA,e.bufB],At=0,L=e.initialAlpha<k.alphaMin(),nt=!1,L||rt();break}case"params":Ve(e.params),k&&(k.alpha(Math.max(k.alpha(),.5)),L=!1,rt());break;case"reheat":k&&(k.alpha(Math.max(k.alpha(),e.alpha)),L=!1,rt());break;case"buffer":wt.push(e.buffer),je();break}};})();
`;var Vs=class{constructor(){Q(this,"positions",new Float32Array(0));Q(this,"worker",null);Q(this,"url","");Q(this,"dirty",!1);Q(this,"settled",!0);Q(this,"_ticks",0)}get ticks(){return this._ticks}init(t,e,n,s=1){this.disposeWorker(),this.positions=e,this._ticks=0,this.dirty=!1,this.url=URL.createObjectURL(new Blob([_d],{type:"text/javascript"})),this.worker=new Worker(this.url),this.worker.onmessage=u=>{let p=u.data;if(p.type!=="tick")return;let g=new Float32Array(p.buffer);this.positions.set(g.subarray(0,this.positions.length)),this._ticks=p.ticks,this.settled=p.settled,this.dirty=!0,this.worker?.postMessage({type:"buffer",buffer:p.buffer},[p.buffer])};let r=t.nodes.length,a=new Float32Array(e),o=new Uint32Array(t.links.length*2);t.links.forEach((u,p)=>{o[p*2]=u.source,o[p*2+1]=u.target});let l=new Float32Array(r);t.nodes.forEach((u,p)=>l[p]=Math.max(u.degree,1));let c=new Float32Array(r);t.nodes.forEach((u,p)=>c[p]=u.side??0);let h=new ArrayBuffer(r*3*4),f=new ArrayBuffer(r*3*4);this.settled=s<.001,this.worker.postMessage({type:"init",count:r,positions:a.buffer,links:o.buffer,degrees:l.buffer,sides:c.buffer,params:n,initialAlpha:s,bufA:h,bufB:f},[a.buffer,o.buffer,l.buffer,c.buffer,h,f])}step(){let t=this.dirty;return this.dirty=!1,t}isSettled(){return this.settled}reheat(t=.3){this.settled=!1,this.worker?.postMessage({type:"reheat",alpha:t})}updateParams(t){this.settled=!1,this.worker?.postMessage({type:"params",params:t})}disposeWorker(){this.worker&&(this.worker.onmessage=null,this.worker.terminate()),this.worker=null,this.url&&(URL.revokeObjectURL(this.url),this.url="")}dispose(){this.disposeWorker(),this.settled=!0,this.dirty=!1}};function xd(i){let t=+this._x.call(null,i);return vd(this.cover(t),t,i)}function vd(i,t,e){if(isNaN(t))return i;var n,s=i._root,r={data:e},a=i._x0,o=i._x1,l,c,h,f,u;if(!s)return i._root=r,i;for(;s.length;)if((h=t>=(l=(a+o)/2))?a=l:o=l,n=s,!(s=s[f=+h]))return n[f]=r,i;if(c=+i._x.call(null,s.data),t===c)return r.next=s,n?n[f]=r:i._root=r,i;do n=n?n[f]=new Array(2):i._root=new Array(2),(h=t>=(l=(a+o)/2))?a=l:o=l;while((f=+h)==(u=+(c>=l)));return n[u]=s,n[f]=r,i}function yd(i){Array.isArray(i)||(i=Array.from(i));let t=i.length,e=new Float64Array(t),n=1/0,s=-1/0;for(let r=0,a;r<t;++r)isNaN(a=+this._x.call(null,i[r]))||(e[r]=a,a<n&&(n=a),a>s&&(s=a));if(n>s)return this;this.cover(n).cover(s);for(let r=0;r<t;++r)vd(this,e[r],i[r]);return this}function Md(i){if(isNaN(i=+i))return this;var t=this._x0,e=this._x1;if(isNaN(t))e=(t=Math.floor(i))+1;else{for(var n=e-t||1,s=this._root,r,a;t>i||i>=e;)switch(a=+(i<t),r=new Array(2),r[a]=s,s=r,n*=2,a){case 0:e=t+n;break;case 1:t=e-n;break}this._root&&this._root.length&&(this._root=s)}return this._x0=t,this._x1=e,this}function bd(){var i=[];return this.visit(function(t){if(!t.length)do i.push(t.data);while(t=t.next)}),i}function Sd(i){return arguments.length?this.cover(+i[0][0]).cover(+i[1][0]):isNaN(this._x0)?void 0:[[this._x0],[this._x1]]}function Mn(i,t,e){this.node=i,this.x0=t,this.x1=e}function wd(i,t){var e,n=this._x0,s,r,a=this._x1,o=[],l=this._root,c,h;for(l&&o.push(new Mn(l,n,a)),t==null?t=1/0:(n=i-t,a=i+t);c=o.pop();)if(!(!(l=c.node)||(s=c.x0)>a||(r=c.x1)<n))if(l.length){var f=(s+r)/2;o.push(new Mn(l[1],f,r),new Mn(l[0],s,f)),(h=+(i>=f))&&(c=o[o.length-1],o[o.length-1]=o[o.length-1-h],o[o.length-1-h]=c)}else{var u=Math.abs(i-+this._x.call(null,l.data));u<t&&(t=u,n=i-u,a=i+u,e=l.data)}return e}function Ad(i){if(isNaN(l=+this._x.call(null,i)))return this;var t,e=this._root,n,s,r,a=this._x0,o=this._x1,l,c,h,f,u;if(!e)return this;if(e.length)for(;;){if((h=l>=(c=(a+o)/2))?a=c:o=c,t=e,!(e=e[f=+h]))return this;if(!e.length)break;t[f+1&1]&&(n=t,u=f)}for(;e.data!==i;)if(s=e,!(e=e.next))return this;return(r=e.next)&&delete e.next,s?(r?s.next=r:delete s.next,this):t?(r?t[f]=r:delete t[f],(e=t[0]||t[1])&&e===(t[1]||t[0])&&!e.length&&(n?n[u]=e:this._root=e),this):(this._root=r,this)}function Td(i){for(var t=0,e=i.length;t<e;++t)this.remove(i[t]);return this}function Ed(){return this._root}function Cd(){var i=0;return this.visit(function(t){if(!t.length)do++i;while(t=t.next)}),i}function Rd(i){var t=[],e,n=this._root,s,r,a;for(n&&t.push(new Mn(n,this._x0,this._x1));e=t.pop();)if(!i(n=e.node,r=e.x0,a=e.x1)&&n.length){var o=(r+a)/2;(s=n[1])&&t.push(new Mn(s,o,a)),(s=n[0])&&t.push(new Mn(s,r,o))}return this}function Pd(i){var t=[],e=[],n;for(this._root&&t.push(new Mn(this._root,this._x0,this._x1));n=t.pop();){var s=n.node;if(s.length){var r,a=n.x0,o=n.x1,l=(a+o)/2;(r=s[0])&&t.push(new Mn(r,a,l)),(r=s[1])&&t.push(new Mn(r,l,o))}e.push(n)}for(;n=e.pop();)i(n.node,n.x0,n.x1);return this}function Id(i){return i[0]}function Ld(i){return arguments.length?(this._x=i,this):this._x}function zr(i,t){var e=new bh(t??Id,NaN,NaN);return i==null?e:e.addAll(i)}function bh(i,t,e){this._x=i,this._x0=t,this._x1=e,this._root=void 0}function Nd(i){for(var t={data:i.data},e=t;i=i.next;)e=e.next={data:i.data};return t}var on=zr.prototype=bh.prototype;on.copy=function(){var i=new bh(this._x,this._x0,this._x1),t=this._root,e,n;if(!t)return i;if(!t.length)return i._root=Nd(t),i;for(e=[{source:t,target:i._root=new Array(2)}];t=e.pop();)for(var s=0;s<2;++s)(n=t.source[s])&&(n.length?e.push({source:n,target:t.target[s]=new Array(2)}):t.target[s]=Nd(n));return i};on.add=xd;on.addAll=yd;on.cover=Md;on.data=bd;on.extent=Sd;on.find=wd;on.remove=Ad;on.removeAll=Td;on.root=Ed;on.size=Cd;on.visit=Rd;on.visitAfter=Pd;on.x=Ld;function Dd(i){let t=+this._x.call(null,i),e=+this._y.call(null,i);return Fd(this.cover(t,e),t,e,i)}function Fd(i,t,e,n){if(isNaN(t)||isNaN(e))return i;var s,r=i._root,a={data:n},o=i._x0,l=i._y0,c=i._x1,h=i._y1,f,u,p,g,x,m,d,y;if(!r)return i._root=a,i;for(;r.length;)if((x=t>=(f=(o+c)/2))?o=f:c=f,(m=e>=(u=(l+h)/2))?l=u:h=u,s=r,!(r=r[d=m<<1|x]))return s[d]=a,i;if(p=+i._x.call(null,r.data),g=+i._y.call(null,r.data),t===p&&e===g)return a.next=r,s?s[d]=a:i._root=a,i;do s=s?s[d]=new Array(4):i._root=new Array(4),(x=t>=(f=(o+c)/2))?o=f:c=f,(m=e>=(u=(l+h)/2))?l=u:h=u;while((d=m<<1|x)===(y=(g>=u)<<1|p>=f));return s[y]=r,s[d]=a,i}function Ud(i){var t,e,n=i.length,s,r,a=new Array(n),o=new Array(n),l=1/0,c=1/0,h=-1/0,f=-1/0;for(e=0;e<n;++e)isNaN(s=+this._x.call(null,t=i[e]))||isNaN(r=+this._y.call(null,t))||(a[e]=s,o[e]=r,s<l&&(l=s),s>h&&(h=s),r<c&&(c=r),r>f&&(f=r));if(l>h||c>f)return this;for(this.cover(l,c).cover(h,f),e=0;e<n;++e)Fd(this,a[e],o[e],i[e]);return this}function Od(i,t){if(isNaN(i=+i)||isNaN(t=+t))return this;var e=this._x0,n=this._y0,s=this._x1,r=this._y1;if(isNaN(e))s=(e=Math.floor(i))+1,r=(n=Math.floor(t))+1;else{for(var a=s-e||1,o=this._root,l,c;e>i||i>=s||n>t||t>=r;)switch(c=(t<n)<<1|i<e,l=new Array(4),l[c]=o,o=l,a*=2,c){case 0:s=e+a,r=n+a;break;case 1:e=s-a,r=n+a;break;case 2:s=e+a,n=r-a;break;case 3:e=s-a,n=r-a;break}this._root&&this._root.length&&(this._root=o)}return this._x0=e,this._y0=n,this._x1=s,this._y1=r,this}function Bd(){var i=[];return this.visit(function(t){if(!t.length)do i.push(t.data);while(t=t.next)}),i}function kd(i){return arguments.length?this.cover(+i[0][0],+i[0][1]).cover(+i[1][0],+i[1][1]):isNaN(this._x0)?void 0:[[this._x0,this._y0],[this._x1,this._y1]]}function Be(i,t,e,n,s){this.node=i,this.x0=t,this.y0=e,this.x1=n,this.y1=s}function zd(i,t,e){var n,s=this._x0,r=this._y0,a,o,l,c,h=this._x1,f=this._y1,u=[],p=this._root,g,x;for(p&&u.push(new Be(p,s,r,h,f)),e==null?e=1/0:(s=i-e,r=t-e,h=i+e,f=t+e,e*=e);g=u.pop();)if(!(!(p=g.node)||(a=g.x0)>h||(o=g.y0)>f||(l=g.x1)<s||(c=g.y1)<r))if(p.length){var m=(a+l)/2,d=(o+c)/2;u.push(new Be(p[3],m,d,l,c),new Be(p[2],a,d,m,c),new Be(p[1],m,o,l,d),new Be(p[0],a,o,m,d)),(x=(t>=d)<<1|i>=m)&&(g=u[u.length-1],u[u.length-1]=u[u.length-1-x],u[u.length-1-x]=g)}else{var y=i-+this._x.call(null,p.data),S=t-+this._y.call(null,p.data),b=y*y+S*S;if(b<e){var T=Math.sqrt(e=b);s=i-T,r=t-T,h=i+T,f=t+T,n=p.data}}return n}function Vd(i){if(isNaN(h=+this._x.call(null,i))||isNaN(f=+this._y.call(null,i)))return this;var t,e=this._root,n,s,r,a=this._x0,o=this._y0,l=this._x1,c=this._y1,h,f,u,p,g,x,m,d;if(!e)return this;if(e.length)for(;;){if((g=h>=(u=(a+l)/2))?a=u:l=u,(x=f>=(p=(o+c)/2))?o=p:c=p,t=e,!(e=e[m=x<<1|g]))return this;if(!e.length)break;(t[m+1&3]||t[m+2&3]||t[m+3&3])&&(n=t,d=m)}for(;e.data!==i;)if(s=e,!(e=e.next))return this;return(r=e.next)&&delete e.next,s?(r?s.next=r:delete s.next,this):t?(r?t[m]=r:delete t[m],(e=t[0]||t[1]||t[2]||t[3])&&e===(t[3]||t[2]||t[1]||t[0])&&!e.length&&(n?n[d]=e:this._root=e),this):(this._root=r,this)}function Gd(i){for(var t=0,e=i.length;t<e;++t)this.remove(i[t]);return this}function Hd(){return this._root}function Wd(){var i=0;return this.visit(function(t){if(!t.length)do++i;while(t=t.next)}),i}function Xd(i){var t=[],e,n=this._root,s,r,a,o,l;for(n&&t.push(new Be(n,this._x0,this._y0,this._x1,this._y1));e=t.pop();)if(!i(n=e.node,r=e.x0,a=e.y0,o=e.x1,l=e.y1)&&n.length){var c=(r+o)/2,h=(a+l)/2;(s=n[3])&&t.push(new Be(s,c,h,o,l)),(s=n[2])&&t.push(new Be(s,r,h,c,l)),(s=n[1])&&t.push(new Be(s,c,a,o,h)),(s=n[0])&&t.push(new Be(s,r,a,c,h))}return this}function qd(i){var t=[],e=[],n;for(this._root&&t.push(new Be(this._root,this._x0,this._y0,this._x1,this._y1));n=t.pop();){var s=n.node;if(s.length){var r,a=n.x0,o=n.y0,l=n.x1,c=n.y1,h=(a+l)/2,f=(o+c)/2;(r=s[0])&&t.push(new Be(r,a,o,h,f)),(r=s[1])&&t.push(new Be(r,h,o,l,f)),(r=s[2])&&t.push(new Be(r,a,f,h,c)),(r=s[3])&&t.push(new Be(r,h,f,l,c))}e.push(n)}for(;n=e.pop();)i(n.node,n.x0,n.y0,n.x1,n.y1);return this}function Yd(i){return i[0]}function Zd(i){return arguments.length?(this._x=i,this):this._x}function Jd(i){return i[1]}function $d(i){return arguments.length?(this._y=i,this):this._y}function Vr(i,t,e){var n=new Sh(t??Yd,e??Jd,NaN,NaN,NaN,NaN);return i==null?n:n.addAll(i)}function Sh(i,t,e,n,s,r){this._x=i,this._y=t,this._x0=e,this._y0=n,this._x1=s,this._y1=r,this._root=void 0}function Kd(i){for(var t={data:i.data},e=t;i=i.next;)e=e.next={data:i.data};return t}var Ke=Vr.prototype=Sh.prototype;Ke.copy=function(){var i=new Sh(this._x,this._y,this._x0,this._y0,this._x1,this._y1),t=this._root,e,n;if(!t)return i;if(!t.length)return i._root=Kd(t),i;for(e=[{source:t,target:i._root=new Array(4)}];t=e.pop();)for(var s=0;s<4;++s)(n=t.source[s])&&(n.length?e.push({source:n,target:t.target[s]=new Array(4)}):t.target[s]=Kd(n));return i};Ke.add=Dd;Ke.addAll=Ud;Ke.cover=Od;Ke.data=Bd;Ke.extent=kd;Ke.find=zd;Ke.remove=Vd;Ke.removeAll=Gd;Ke.root=Hd;Ke.size=Wd;Ke.visit=Xd;Ke.visitAfter=qd;Ke.x=Zd;Ke.y=$d;function jd(i){let t=+this._x.call(null,i),e=+this._y.call(null,i),n=+this._z.call(null,i);return Qd(this.cover(t,e,n),t,e,n,i)}function Qd(i,t,e,n,s){if(isNaN(t)||isNaN(e)||isNaN(n))return i;var r,a=i._root,o={data:s},l=i._x0,c=i._y0,h=i._z0,f=i._x1,u=i._y1,p=i._z1,g,x,m,d,y,S,b,T,w,R,v;if(!a)return i._root=o,i;for(;a.length;)if((b=t>=(g=(l+f)/2))?l=g:f=g,(T=e>=(x=(c+u)/2))?c=x:u=x,(w=n>=(m=(h+p)/2))?h=m:p=m,r=a,!(a=a[R=w<<2|T<<1|b]))return r[R]=o,i;if(d=+i._x.call(null,a.data),y=+i._y.call(null,a.data),S=+i._z.call(null,a.data),t===d&&e===y&&n===S)return o.next=a,r?r[R]=o:i._root=o,i;do r=r?r[R]=new Array(8):i._root=new Array(8),(b=t>=(g=(l+f)/2))?l=g:f=g,(T=e>=(x=(c+u)/2))?c=x:u=x,(w=n>=(m=(h+p)/2))?h=m:p=m;while((R=w<<2|T<<1|b)===(v=(S>=m)<<2|(y>=x)<<1|d>=g));return r[v]=a,r[R]=o,i}function tp(i){Array.isArray(i)||(i=Array.from(i));let t=i.length,e=new Float64Array(t),n=new Float64Array(t),s=new Float64Array(t),r=1/0,a=1/0,o=1/0,l=-1/0,c=-1/0,h=-1/0;for(let f=0,u,p,g,x;f<t;++f)isNaN(p=+this._x.call(null,u=i[f]))||isNaN(g=+this._y.call(null,u))||isNaN(x=+this._z.call(null,u))||(e[f]=p,n[f]=g,s[f]=x,p<r&&(r=p),p>l&&(l=p),g<a&&(a=g),g>c&&(c=g),x<o&&(o=x),x>h&&(h=x));if(r>l||a>c||o>h)return this;this.cover(r,a,o).cover(l,c,h);for(let f=0;f<t;++f)Qd(this,e[f],n[f],s[f],i[f]);return this}function ep(i,t,e){if(isNaN(i=+i)||isNaN(t=+t)||isNaN(e=+e))return this;var n=this._x0,s=this._y0,r=this._z0,a=this._x1,o=this._y1,l=this._z1;if(isNaN(n))a=(n=Math.floor(i))+1,o=(s=Math.floor(t))+1,l=(r=Math.floor(e))+1;else{for(var c=a-n||1,h=this._root,f,u;n>i||i>=a||s>t||t>=o||r>e||e>=l;)switch(u=(e<r)<<2|(t<s)<<1|i<n,f=new Array(8),f[u]=h,h=f,c*=2,u){case 0:a=n+c,o=s+c,l=r+c;break;case 1:n=a-c,o=s+c,l=r+c;break;case 2:a=n+c,s=o-c,l=r+c;break;case 3:n=a-c,s=o-c,l=r+c;break;case 4:a=n+c,o=s+c,r=l-c;break;case 5:n=a-c,o=s+c,r=l-c;break;case 6:a=n+c,s=o-c,r=l-c;break;case 7:n=a-c,s=o-c,r=l-c;break}this._root&&this._root.length&&(this._root=h)}return this._x0=n,this._y0=s,this._z0=r,this._x1=a,this._y1=o,this._z1=l,this}function np(){var i=[];return this.visit(function(t){if(!t.length)do i.push(t.data);while(t=t.next)}),i}function ip(i){return arguments.length?this.cover(+i[0][0],+i[0][1],+i[0][2]).cover(+i[1][0],+i[1][1],+i[1][2]):isNaN(this._x0)?void 0:[[this._x0,this._y0,this._z0],[this._x1,this._y1,this._z1]]}function jt(i,t,e,n,s,r,a){this.node=i,this.x0=t,this.y0=e,this.z0=n,this.x1=s,this.y1=r,this.z1=a}function sp(i,t,e,n){var s,r=this._x0,a=this._y0,o=this._z0,l,c,h,f,u,p,g=this._x1,x=this._y1,m=this._z1,d=[],y=this._root,S,b;for(y&&d.push(new jt(y,r,a,o,g,x,m)),n==null?n=1/0:(r=i-n,a=t-n,o=e-n,g=i+n,x=t+n,m=e+n,n*=n);S=d.pop();)if(!(!(y=S.node)||(l=S.x0)>g||(c=S.y0)>x||(h=S.z0)>m||(f=S.x1)<r||(u=S.y1)<a||(p=S.z1)<o))if(y.length){var T=(l+f)/2,w=(c+u)/2,R=(h+p)/2;d.push(new jt(y[7],T,w,R,f,u,p),new jt(y[6],l,w,R,T,u,p),new jt(y[5],T,c,R,f,w,p),new jt(y[4],l,c,R,T,w,p),new jt(y[3],T,w,h,f,u,R),new jt(y[2],l,w,h,T,u,R),new jt(y[1],T,c,h,f,w,R),new jt(y[0],l,c,h,T,w,R)),(b=(e>=R)<<2|(t>=w)<<1|i>=T)&&(S=d[d.length-1],d[d.length-1]=d[d.length-1-b],d[d.length-1-b]=S)}else{var v=i-+this._x.call(null,y.data),E=t-+this._y.call(null,y.data),I=e-+this._z.call(null,y.data),C=v*v+E*E+I*I;if(C<n){var N=Math.sqrt(n=C);r=i-N,a=t-N,o=e-N,g=i+N,x=t+N,m=e+N,s=y.data}}return s}var xy=(i,t,e,n,s,r)=>Math.sqrt((i-n)**2+(t-s)**2+(e-r)**2);function rp(i,t,e,n){let s=[],r=i-n,a=t-n,o=e-n,l=i+n,c=t+n,h=e+n;return this.visit((f,u,p,g,x,m,d)=>{if(!f.length)do{let y=f.data;xy(i,t,e,this._x(y),this._y(y),this._z(y))<=n&&s.push(y)}while(f=f.next);return u>l||p>c||g>h||x<r||m<a||d<o}),s}function ap(i){if(isNaN(u=+this._x.call(null,i))||isNaN(p=+this._y.call(null,i))||isNaN(g=+this._z.call(null,i)))return this;var t,e=this._root,n,s,r,a=this._x0,o=this._y0,l=this._z0,c=this._x1,h=this._y1,f=this._z1,u,p,g,x,m,d,y,S,b,T,w;if(!e)return this;if(e.length)for(;;){if((y=u>=(x=(a+c)/2))?a=x:c=x,(S=p>=(m=(o+h)/2))?o=m:h=m,(b=g>=(d=(l+f)/2))?l=d:f=d,t=e,!(e=e[T=b<<2|S<<1|y]))return this;if(!e.length)break;(t[T+1&7]||t[T+2&7]||t[T+3&7]||t[T+4&7]||t[T+5&7]||t[T+6&7]||t[T+7&7])&&(n=t,w=T)}for(;e.data!==i;)if(s=e,!(e=e.next))return this;return(r=e.next)&&delete e.next,s?(r?s.next=r:delete s.next,this):t?(r?t[T]=r:delete t[T],(e=t[0]||t[1]||t[2]||t[3]||t[4]||t[5]||t[6]||t[7])&&e===(t[7]||t[6]||t[5]||t[4]||t[3]||t[2]||t[1]||t[0])&&!e.length&&(n?n[w]=e:this._root=e),this):(this._root=r,this)}function op(i){for(var t=0,e=i.length;t<e;++t)this.remove(i[t]);return this}function lp(){return this._root}function cp(){var i=0;return this.visit(function(t){if(!t.length)do++i;while(t=t.next)}),i}function hp(i){var t=[],e,n=this._root,s,r,a,o,l,c,h;for(n&&t.push(new jt(n,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1));e=t.pop();)if(!i(n=e.node,r=e.x0,a=e.y0,o=e.z0,l=e.x1,c=e.y1,h=e.z1)&&n.length){var f=(r+l)/2,u=(a+c)/2,p=(o+h)/2;(s=n[7])&&t.push(new jt(s,f,u,p,l,c,h)),(s=n[6])&&t.push(new jt(s,r,u,p,f,c,h)),(s=n[5])&&t.push(new jt(s,f,a,p,l,u,h)),(s=n[4])&&t.push(new jt(s,r,a,p,f,u,h)),(s=n[3])&&t.push(new jt(s,f,u,o,l,c,p)),(s=n[2])&&t.push(new jt(s,r,u,o,f,c,p)),(s=n[1])&&t.push(new jt(s,f,a,o,l,u,p)),(s=n[0])&&t.push(new jt(s,r,a,o,f,u,p))}return this}function up(i){var t=[],e=[],n;for(this._root&&t.push(new jt(this._root,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1));n=t.pop();){var s=n.node;if(s.length){var r,a=n.x0,o=n.y0,l=n.z0,c=n.x1,h=n.y1,f=n.z1,u=(a+c)/2,p=(o+h)/2,g=(l+f)/2;(r=s[0])&&t.push(new jt(r,a,o,l,u,p,g)),(r=s[1])&&t.push(new jt(r,u,o,l,c,p,g)),(r=s[2])&&t.push(new jt(r,a,p,l,u,h,g)),(r=s[3])&&t.push(new jt(r,u,p,l,c,h,g)),(r=s[4])&&t.push(new jt(r,a,o,g,u,p,f)),(r=s[5])&&t.push(new jt(r,u,o,g,c,p,f)),(r=s[6])&&t.push(new jt(r,a,p,g,u,h,f)),(r=s[7])&&t.push(new jt(r,u,p,g,c,h,f))}e.push(n)}for(;n=e.pop();)i(n.node,n.x0,n.y0,n.z0,n.x1,n.y1,n.z1);return this}function fp(i){return i[0]}function dp(i){return arguments.length?(this._x=i,this):this._x}function pp(i){return i[1]}function mp(i){return arguments.length?(this._y=i,this):this._y}function gp(i){return i[2]}function _p(i){return arguments.length?(this._z=i,this):this._z}function Gr(i,t,e,n){var s=new wh(t??fp,e??pp,n??gp,NaN,NaN,NaN,NaN,NaN,NaN);return i==null?s:s.addAll(i)}function wh(i,t,e,n,s,r,a,o,l){this._x=i,this._y=t,this._z=e,this._x0=n,this._y0=s,this._z0=r,this._x1=a,this._y1=o,this._z1=l,this._root=void 0}function xp(i){for(var t={data:i.data},e=t;i=i.next;)e=e.next={data:i.data};return t}var Ve=Gr.prototype=wh.prototype;Ve.copy=function(){var i=new wh(this._x,this._y,this._z,this._x0,this._y0,this._z0,this._x1,this._y1,this._z1),t=this._root,e,n;if(!t)return i;if(!t.length)return i._root=xp(t),i;for(e=[{source:t,target:i._root=new Array(8)}];t=e.pop();)for(var s=0;s<8;++s)(n=t.source[s])&&(n.length?e.push({source:n,target:t.target[s]=new Array(8)}):t.target[s]=xp(n));return i};Ve.add=jd;Ve.addAll=tp;Ve.cover=ep;Ve.data=np;Ve.extent=ip;Ve.find=sp;Ve.findAllWithinRadius=rp;Ve.remove=ap;Ve.removeAll=op;Ve.root=lp;Ve.size=cp;Ve.visit=hp;Ve.visitAfter=up;Ve.x=dp;Ve.y=mp;Ve.z=_p;function Me(i){return function(){return i}}function Rn(i){return(i()-.5)*1e-6}function vy(i){return i.index}function vp(i,t){var e=i.get(t);if(!e)throw new Error("node not found: "+t);return e}function Ah(i){var t=vy,e=u,n,s=Me(30),r,a,o,l,c,h,f=1;i==null&&(i=[]);function u(d){return 1/Math.min(l[d.source.index],l[d.target.index])}function p(d){for(var y=0,S=i.length;y<f;++y)for(var b=0,T,w,R,v=0,E=0,I=0,C,N;b<S;++b)T=i[b],w=T.source,R=T.target,v=R.x+R.vx-w.x-w.vx||Rn(h),o>1&&(E=R.y+R.vy-w.y-w.vy||Rn(h)),o>2&&(I=R.z+R.vz-w.z-w.vz||Rn(h)),C=Math.sqrt(v*v+E*E+I*I),C=(C-r[b])/C*d*n[b],v*=C,E*=C,I*=C,R.vx-=v*(N=c[b]),o>1&&(R.vy-=E*N),o>2&&(R.vz-=I*N),w.vx+=v*(N=1-N),o>1&&(w.vy+=E*N),o>2&&(w.vz+=I*N)}function g(){if(a){var d,y=a.length,S=i.length,b=new Map(a.map((w,R)=>[t(w,R,a),w])),T;for(d=0,l=new Array(y);d<S;++d)T=i[d],T.index=d,typeof T.source!="object"&&(T.source=vp(b,T.source)),typeof T.target!="object"&&(T.target=vp(b,T.target)),l[T.source.index]=(l[T.source.index]||0)+1,l[T.target.index]=(l[T.target.index]||0)+1;for(d=0,c=new Array(S);d<S;++d)T=i[d],c[d]=l[T.source.index]/(l[T.source.index]+l[T.target.index]);n=new Array(S),x(),r=new Array(S),m()}}function x(){if(a)for(var d=0,y=i.length;d<y;++d)n[d]=+e(i[d],d,i)}function m(){if(a)for(var d=0,y=i.length;d<y;++d)r[d]=+s(i[d],d,i)}return p.initialize=function(d,...y){a=d,h=y.find(S=>typeof S=="function")||Math.random,o=y.find(S=>[1,2,3].includes(S))||2,g()},p.links=function(d){return arguments.length?(i=d,g(),p):i},p.id=function(d){return arguments.length?(t=d,p):t},p.iterations=function(d){return arguments.length?(f=+d,p):f},p.strength=function(d){return arguments.length?(e=typeof d=="function"?d:Me(+d),x(),p):e},p.distance=function(d){return arguments.length?(s=typeof d=="function"?d:Me(+d),m(),p):s},p}var yy={value:()=>{}};function Mp(){for(var i=0,t=arguments.length,e={},n;i<t;++i){if(!(n=arguments[i]+"")||n in e||/[\s.]/.test(n))throw new Error("illegal type: "+n);e[n]=[]}return new Al(e)}function Al(i){this._=i}function My(i,t){return i.trim().split(/^|\s+/).map(function(e){var n="",s=e.indexOf(".");if(s>=0&&(n=e.slice(s+1),e=e.slice(0,s)),e&&!t.hasOwnProperty(e))throw new Error("unknown type: "+e);return{type:e,name:n}})}Al.prototype=Mp.prototype={constructor:Al,on:function(i,t){var e=this._,n=My(i+"",e),s,r=-1,a=n.length;if(arguments.length<2){for(;++r<a;)if((s=(i=n[r]).type)&&(s=by(e[s],i.name)))return s;return}if(t!=null&&typeof t!="function")throw new Error("invalid callback: "+t);for(;++r<a;)if(s=(i=n[r]).type)e[s]=yp(e[s],i.name,t);else if(t==null)for(s in e)e[s]=yp(e[s],i.name,null);return this},copy:function(){var i={},t=this._;for(var e in t)i[e]=t[e].slice();return new Al(i)},call:function(i,t){if((s=arguments.length-2)>0)for(var e=new Array(s),n=0,s,r;n<s;++n)e[n]=arguments[n+2];if(!this._.hasOwnProperty(i))throw new Error("unknown type: "+i);for(r=this._[i],n=0,s=r.length;n<s;++n)r[n].value.apply(t,e)},apply:function(i,t,e){if(!this._.hasOwnProperty(i))throw new Error("unknown type: "+i);for(var n=this._[i],s=0,r=n.length;s<r;++s)n[s].value.apply(t,e)}};function by(i,t){for(var e=0,n=i.length,s;e<n;++e)if((s=i[e]).name===t)return s.value}function yp(i,t,e){for(var n=0,s=i.length;n<s;++n)if(i[n].name===t){i[n]=yy,i=i.slice(0,n).concat(i.slice(n+1));break}return e!=null&&i.push({name:t,value:e}),i}var Th=Mp;var Gs=0,Wr=0,Hr=0,Sp=1e3,Tl,Xr,El=0,os=0,Cl=0,qr=typeof performance=="object"&&performance.now?performance:Date,wp=typeof window=="object"&&window.requestAnimationFrame?window.requestAnimationFrame.bind(window):function(i){setTimeout(i,17)};function Rh(){return os||(wp(Sy),os=qr.now()+Cl)}function Sy(){os=0}function Eh(){this._call=this._time=this._next=null}Eh.prototype=Rl.prototype={constructor:Eh,restart:function(i,t,e){if(typeof i!="function")throw new TypeError("callback is not a function");e=(e==null?Rh():+e)+(t==null?0:+t),!this._next&&Xr!==this&&(Xr?Xr._next=this:Tl=this,Xr=this),this._call=i,this._time=e,Ch()},stop:function(){this._call&&(this._call=null,this._time=1/0,Ch())}};function Rl(i,t,e){var n=new Eh;return n.restart(i,t,e),n}function Ap(){Rh(),++Gs;for(var i=Tl,t;i;)(t=os-i._time)>=0&&i._call.call(void 0,t),i=i._next;--Gs}function bp(){os=(El=qr.now())+Cl,Gs=Wr=0;try{Ap()}finally{Gs=0,Ay(),os=0}}function wy(){var i=qr.now(),t=i-El;t>Sp&&(Cl-=t,El=i)}function Ay(){for(var i,t=Tl,e,n=1/0;t;)t._call?(n>t._time&&(n=t._time),i=t,t=t._next):(e=t._next,t._next=null,t=i?i._next=e:Tl=e);Xr=i,Ch(n)}function Ch(i){if(!Gs){Wr&&(Wr=clearTimeout(Wr));var t=i-os;t>24?(i<1/0&&(Wr=setTimeout(bp,i-qr.now()-Cl)),Hr&&(Hr=clearInterval(Hr))):(Hr||(El=qr.now(),Hr=setInterval(wy,Sp)),Gs=1,wp(bp))}}function Tp(){let i=1;return()=>(i=(1664525*i+1013904223)%4294967296)/4294967296}var Ep=3;function Pl(i){return i.x}function Ph(i){return i.y}function Cp(i){return i.z}var Ty=10,Ey=Math.PI*(3-Math.sqrt(5)),Cy=Math.PI*20/(9+Math.sqrt(221));function Ih(i,t){t=t||2;var e=Math.min(Ep,Math.max(1,Math.round(t))),n,s=1,r=.001,a=1-Math.pow(r,1/300),o=0,l=.6,c=new Map,h=Rl(p),f=Th("tick","end"),u=Tp();i==null&&(i=[]);function p(){g(),f.call("tick",n),s<r&&(h.stop(),f.call("end",n))}function g(d){var y,S=i.length,b;d===void 0&&(d=1);for(var T=0;T<d;++T)for(s+=(o-s)*a,c.forEach(function(w){w(s)}),y=0;y<S;++y)b=i[y],b.fx==null?b.x+=b.vx*=l:(b.x=b.fx,b.vx=0),e>1&&(b.fy==null?b.y+=b.vy*=l:(b.y=b.fy,b.vy=0)),e>2&&(b.fz==null?b.z+=b.vz*=l:(b.z=b.fz,b.vz=0));return n}function x(){for(var d=0,y=i.length,S;d<y;++d){if(S=i[d],S.index=d,S.fx!=null&&(S.x=S.fx),S.fy!=null&&(S.y=S.fy),S.fz!=null&&(S.z=S.fz),isNaN(S.x)||e>1&&isNaN(S.y)||e>2&&isNaN(S.z)){var b=Ty*(e>2?Math.cbrt(.5+d):e>1?Math.sqrt(.5+d):d),T=d*Ey,w=d*Cy;e===1?S.x=b:e===2?(S.x=b*Math.cos(T),S.y=b*Math.sin(T)):(S.x=b*Math.sin(T)*Math.cos(w),S.y=b*Math.cos(T),S.z=b*Math.sin(T)*Math.sin(w))}(isNaN(S.vx)||e>1&&isNaN(S.vy)||e>2&&isNaN(S.vz))&&(S.vx=0,e>1&&(S.vy=0),e>2&&(S.vz=0))}}function m(d){return d.initialize&&d.initialize(i,u,e),d}return x(),n={tick:g,restart:function(){return h.restart(p),n},stop:function(){return h.stop(),n},numDimensions:function(d){return arguments.length?(e=Math.min(Ep,Math.max(1,Math.round(d))),c.forEach(m),n):e},nodes:function(d){return arguments.length?(i=d,x(),c.forEach(m),n):i},alpha:function(d){return arguments.length?(s=+d,n):s},alphaMin:function(d){return arguments.length?(r=+d,n):r},alphaDecay:function(d){return arguments.length?(a=+d,n):+a},alphaTarget:function(d){return arguments.length?(o=+d,n):o},velocityDecay:function(d){return arguments.length?(l=1-d,n):1-l},randomSource:function(d){return arguments.length?(u=d,c.forEach(m),n):u},force:function(d,y){return arguments.length>1?(y==null?c.delete(d):c.set(d,m(y)),n):c.get(d)},find:function(){var d=Array.prototype.slice.call(arguments),y=d.shift()||0,S=(e>1?d.shift():null)||0,b=(e>2?d.shift():null)||0,T=d.shift()||1/0,w=0,R=i.length,v,E,I,C,N,H;for(T*=T,w=0;w<R;++w)N=i[w],v=y-N.x,E=S-(N.y||0),I=b-(N.z||0),C=v*v+E*E+I*I,C<T&&(H=N,T=C);return H},on:function(d,y){return arguments.length>1?(f.on(d,y),n):f.on(d)}}}function Lh(){var i,t,e,n,s,r=Me(-30),a,o=1,l=1/0,c=.81;function h(g){var x,m=i.length,d=(t===1?zr(i,Pl):t===2?Vr(i,Pl,Ph):t===3?Gr(i,Pl,Ph,Cp):null).visitAfter(u);for(s=g,x=0;x<m;++x)e=i[x],d.visit(p)}function f(){if(i){var g,x=i.length,m;for(a=new Array(x),g=0;g<x;++g)m=i[g],a[m.index]=+r(m,g,i)}}function u(g){var x=0,m,d,y=0,S,b,T,w,R=g.length;if(R){for(S=b=T=w=0;w<R;++w)(m=g[w])&&(d=Math.abs(m.value))&&(x+=m.value,y+=d,S+=d*(m.x||0),b+=d*(m.y||0),T+=d*(m.z||0));x*=Math.sqrt(4/R),g.x=S/y,t>1&&(g.y=b/y),t>2&&(g.z=T/y)}else{m=g,m.x=m.data.x,t>1&&(m.y=m.data.y),t>2&&(m.z=m.data.z);do x+=a[m.data.index];while(m=m.next)}g.value=x}function p(g,x,m,d,y){if(!g.value)return!0;var S=[m,d,y][t-1],b=g.x-e.x,T=t>1?g.y-e.y:0,w=t>2?g.z-e.z:0,R=S-x,v=b*b+T*T+w*w;if(R*R/c<v)return v<l&&(b===0&&(b=Rn(n),v+=b*b),t>1&&T===0&&(T=Rn(n),v+=T*T),t>2&&w===0&&(w=Rn(n),v+=w*w),v<o&&(v=Math.sqrt(o*v)),e.vx+=b*g.value*s/v,t>1&&(e.vy+=T*g.value*s/v),t>2&&(e.vz+=w*g.value*s/v)),!0;if(g.length||v>=l)return;(g.data!==e||g.next)&&(b===0&&(b=Rn(n),v+=b*b),t>1&&T===0&&(T=Rn(n),v+=T*T),t>2&&w===0&&(w=Rn(n),v+=w*w),v<o&&(v=Math.sqrt(o*v)));do g.data!==e&&(R=a[g.data.index]*s/v,e.vx+=b*R,t>1&&(e.vy+=T*R),t>2&&(e.vz+=w*R));while(g=g.next)}return h.initialize=function(g,...x){i=g,n=x.find(m=>typeof m=="function")||Math.random,t=x.find(m=>[1,2,3].includes(m))||2,f()},h.strength=function(g){return arguments.length?(r=typeof g=="function"?g:Me(+g),f(),h):r},h.distanceMin=function(g){return arguments.length?(o=g*g,h):Math.sqrt(o)},h.distanceMax=function(g){return arguments.length?(l=g*g,h):Math.sqrt(l)},h.theta=function(g){return arguments.length?(c=g*g,h):Math.sqrt(c)},h}function Nh(i){var t=Me(.1),e,n,s;typeof i!="function"&&(i=Me(i==null?0:+i));function r(o){for(var l=0,c=e.length,h;l<c;++l)h=e[l],h.vx+=(s[l]-h.x)*n[l]*o}function a(){if(e){var o,l=e.length;for(n=new Array(l),s=new Array(l),o=0;o<l;++o)n[o]=isNaN(s[o]=+i(e[o],o,e))?0:+t(e[o],o,e)}}return r.initialize=function(o){e=o,a()},r.strength=function(o){return arguments.length?(t=typeof o=="function"?o:Me(+o),a(),r):t},r.x=function(o){return arguments.length?(i=typeof o=="function"?o:Me(+o),a(),r):i},r}function Dh(i){var t=Me(.1),e,n,s;typeof i!="function"&&(i=Me(i==null?0:+i));function r(o){for(var l=0,c=e.length,h;l<c;++l)h=e[l],h.vy+=(s[l]-h.y)*n[l]*o}function a(){if(e){var o,l=e.length;for(n=new Array(l),s=new Array(l),o=0;o<l;++o)n[o]=isNaN(s[o]=+i(e[o],o,e))?0:+t(e[o],o,e)}}return r.initialize=function(o){e=o,a()},r.strength=function(o){return arguments.length?(t=typeof o=="function"?o:Me(+o),a(),r):t},r.y=function(o){return arguments.length?(i=typeof o=="function"?o:Me(+o),a(),r):i},r}function Fh(i){var t=Me(.1),e,n,s;typeof i!="function"&&(i=Me(i==null?0:+i));function r(o){for(var l=0,c=e.length,h;l<c;++l)h=e[l],h.vz+=(s[l]-h.z)*n[l]*o}function a(){if(e){var o,l=e.length;for(n=new Array(l),s=new Array(l),o=0;o<l;++o)n[o]=isNaN(s[o]=+i(e[o],o,e))?0:+t(e[o],o,e)}}return r.initialize=function(o){e=o,a()},r.strength=function(o){return arguments.length?(t=typeof o=="function"?o:Me(+o),a(),r):t},r.z=function(o){return arguments.length?(i=typeof o=="function"?o:Me(+o),a(),r):i},r}function Uh(i,t){let e=[],n=1,s=r=>{if(i!==0)for(let a of e){let o=a.x??0,l=a.z??0,c=Math.hypot(o,l);if(c<1e-4)continue;let h=Math.min(Math.max((t[a.index??0]||1)/n,.3),3),f=i*h*r*c/200;a.vx=(a.vx??0)-o/c*f,a.vz=(a.vz??0)-l/c*f}};return s.initialize=r=>{e=r;let a=0;for(let o of r)a+=t[o.index??0]||1;n=r.length?a/r.length:1},s}function Oh(i){let t=[],e=n=>{if(i!==0)for(let s of t){let r=s.x??0,a=s.z??0,o=Math.hypot(r,a);if(o<.001)continue;let l=1/(1+o/160),c=i*n*l;s.vx=(s.vx??0)+-a/o*c*o,s.vz=(s.vz??0)+r/o*c*o}};return e.initialize=n=>{t=n},e}function Rp(i){return 26*Math.cbrt(Math.max(i,50))}function Pp(i,t){let e=[],n=s=>{if(!(!(i>0)||!t))for(let r of e){let a=r.x||0,o=r.y||0,l=r.z||0,c=Math.hypot(a,o,l);if(c<=i||c<1e-6)continue;let h=t*s*(c-i)/c;r.vx=(r.vx||0)-a*h,r.vy=(r.vy||0)-o*h,r.vz=(r.vz||0)-l*h}};return n.initialize=s=>{e=s},n}function Ip(i,t){return(i||0)*t*.42}var li={perScreen:1.25*Math.PI,damping:1.5,stopBelow:.015,resumeMs:4e3,rampMs:2500,auto:.06};function Lp(i,t,e){let n=li.perScreen/Math.max(200,e||0);return{yaw:-i*n,pitch:-t*n}}function Np(i,t){let e=i*Math.exp(-li.damping*Math.max(0,t));return Math.abs(e)<li.stopBelow?0:e}function Dp(i,t){return!t||i<li.resumeMs?0:li.auto*Math.min(1,(i-li.resumeMs)/li.rampMs)}var Hs=class{constructor(){Q(this,"positions",new Float32Array(0));Q(this,"sim",null);Q(this,"simNodes",[]);Q(this,"degrees",[]);Q(this,"settled",!0);Q(this,"_ticks",0)}get ticks(){return this._ticks}init(t,e,n,s=1){this.dispose(),this.positions=e,this.degrees=t.nodes.map(a=>Math.max(a.degree,1)),this.simNodes=t.nodes.map((a,o)=>({x:e[o*3]??0,y:e[o*3+1]??0,z:e[o*3+2]??0}));let r=t.links.map(a=>({source:a.source,target:a.target}));this.sim=Ih(this.simNodes,3).alphaDecay(1-Math.pow(.001,1/300)).velocityDecay(n.velocityDecay).force("link",Ah(r).distance(n.linkDistance).strength(this.linkStrengthFn(n.linkStrength))).force("charge",Lh().strength(n.charge).distanceMax(800)).force("x",Nh((a,o)=>Ip(t.nodes[o]?.side??0,n.ball??0)).strength(n.centerPull+(n.sidePull??0))).force("y",Dh(0).strength(n.centerPull+n.flatten)).force("z",Fh(0).strength(n.centerPull)).force("core",Uh(n.coreGravity,this.degrees)).force("spiral",Oh(n.spiral)).force("ball",Pp(n.ball??0,n.ballStrength??0)).stop(),this.sim.alpha(s),this._ticks=0,this.settled=!1}linkStrengthFn(t){let e=this.degrees;return n=>{let s=typeof n.source=="number"?n.source:n.source.index??0,r=typeof n.target=="number"?n.target:n.target.index??0,a=1/Math.min(e[s]??1,e[r]??1);return Math.min(a*t,1)}}updateParams(t){let e=this.sim;if(!e)return;e.force("charge")?.strength(t.charge);let n=e.force("link");n?.distance(t.linkDistance),n?.strength(this.linkStrengthFn(t.linkStrength)),e.force("x")?.strength(t.centerPull),e.force("y")?.strength(t.centerPull+t.flatten),e.force("z")?.strength(t.centerPull),e.force("core",Uh(t.coreGravity,this.degrees)),e.force("spiral",Oh(t.spiral)),this.reheat(.5)}step(){let t=this.sim;if(!t||this.settled)return!1;t.tick(),this._ticks++;let e=this.positions,n=this.simNodes;for(let s=0;s<n.length;s++){let r=n[s];r&&(e[s*3]=r.x,e[s*3+1]=r.y,e[s*3+2]=r.z)}return t.alpha()<t.alphaMin()&&(this.settled=!0),!this.settled}isSettled(){return this.settled}reheat(t=.3){this.sim&&(this.sim.alpha(Math.max(this.sim.alpha(),t)),this.settled=!1)}dispose(){this.sim?.stop(),this.sim=null,this.simNodes=[],this.settled=!0}};function Fp(i){let t=i.nodes.length,e=i.links.length,n=new Int32Array(t+1);for(let o of i.links)n[o.source+1]=(n[o.source+1]??0)+1,n[o.target+1]=(n[o.target+1]??0)+1;for(let o=0;o<t;o++)n[o+1]=(n[o+1]??0)+(n[o]??0);let s=new Int32Array(2*e),r=new Int32Array(2*e),a=new Int32Array(t);for(let o=0;o<t;o++)a[o]=n[o]??0;for(let o=0;o<e;o++){let l=i.links[o];if(!l)continue;let c=l.source,h=l.target,f=a[c]??0;s[f]=h,r[f]=o,a[c]=f+1;let u=a[h]??0;s[u]=c,r[u]=o,a[h]=u+1}return{offset:n,neighbor:s,linkOf:r}}function Up(i,t,e){let n=new Map([[t,0]]),s=[],r=[],a=[t];for(let o=1;o<=e;o++){let l=[];for(let c of a){let h=i.offset[c]??0,f=i.offset[c+1]??0;for(let u=h;u<f;u++){let p=i.neighbor[u]??0,g=i.linkOf[u]??0,x=n.get(p);o===1?s.push(g):(x===void 0||x===2)&&r.push(g),x===void 0&&(n.set(p,o),o<e&&l.push(p))}}a=l}return{depthOf:n,linkTier1:s,linkTier2:r}}function Bh(i,t){if(t===null)return 0;let e=(i-t)/1e3;return Number.isFinite(e)?Math.max(e,0):0}function Op(i,t,e=.1){return Math.min(Bh(i,t),e)}var Ry=1100,Py=i=>i<.5?4*i*i*i:1-Math.pow(-2*i+2,3)/2,Il=class{constructor(t,e){this.camera=t,this.dom=e,this.target=new D,this.autoEnabled=!0,this.spinAxis=new D(0,1,0),this.spinSpeed=0,this.idleMs=li.resumeMs,this.tween=null,this.pointers=new Map,this.minDist=5,this.maxDist=5e4,this.q=new en,this.tmp=new D,this.right=new D,this.bind()}distanceFor(t){let e=this.camera.fov*Math.PI/180,n=Math.max(.3,Math.min(1,this.camera.aspect||1));return Math.max(t,1)/Math.sin(e/2)*1.25/n}setInitial(t,e){this.target.copy(t);let n=this.camera.position.clone().sub(t);n.lengthSq()<1e-6&&n.set(.35,.45,1),this.camera.position.copy(t).add(n.normalize().multiplyScalar(this.distanceFor(e))),this.camera.lookAt(this.target)}frame(t,e,n){let s=this.camera.position.clone().sub(this.target),r=s.clone().normalize(),a=r.clone();if(n){let o=t.clone().sub(n);o.lengthSq()>1e-6&&(a=o.normalize())}this.tween={t0:performance.now(),fromTarget:this.target.clone(),toTarget:t.clone(),fromDist:s.length(),toDist:this.distanceFor(e),turn:new en().setFromUnitVectors(r,a),fromDir:r,fromUp:this.camera.up.clone()},this.spinSpeed=0,this.idleMs=0}turn(t,e){if(!e)return;this.q.setFromAxisAngle(t,e);let n=this.camera.position.clone().sub(this.target).applyQuaternion(this.q);this.camera.up.applyQuaternion(this.q),this.camera.position.copy(this.target).add(n),this.camera.lookAt(this.target)}screenAxes(){let t=this.tmp.copy(this.target).sub(this.camera.position).normalize();this.right.copy(t).cross(this.camera.up).normalize();let e=this.right.clone().cross(t).normalize();return{right:this.right.clone(),up:e}}dragBy(t,e,n){let{yaw:s,pitch:r}=Lp(t,e,this.dom.clientHeight),{right:a,up:o}=this.screenAxes(),l=o.multiplyScalar(s).add(a.multiplyScalar(r)),c=l.length();if(c<1e-9)return;let h=l.normalize();this.turn(h,c);let f=c/Math.max(n,1/240);this.spinSpeed>0&&h.dot(this.spinAxis)<0&&(this.spinSpeed=0),this.spinAxis.lerp(h,.5).normalize(),this.spinSpeed=this.spinSpeed*.4+f*.6}zoomBy(t){let e=this.camera.position.clone().sub(this.target),n=Math.max(this.minDist,Math.min(this.maxDist,e.length()*t));this.camera.position.copy(this.target).add(e.setLength(n))}bind(){let t=this.dom,e=0,n=0;t.addEventListener("pointerdown",r=>{t.setPointerCapture?.(r.pointerId),this.pointers.set(r.pointerId,{x:r.clientX,y:r.clientY}),this.spinSpeed=0,this.tween=null,this.idleMs=0,this.held=!0,e=performance.now(),this.pointers.size===2&&(n=this.pinchDistance())}),t.addEventListener("pointermove",r=>{let a=this.pointers.get(r.pointerId);if(!a)return;let o=performance.now();if(this.pointers.size===1&&this.dragBy(r.clientX-a.x,r.clientY-a.y,(o-e)/1e3),a.x=r.clientX,a.y=r.clientY,this.pointers.size===2){let l=this.pinchDistance();n>0&&l>0&&this.zoomBy(n/l),n=l}e=o,this.idleMs=0});let s=r=>{this.pointers.delete(r.pointerId),this.pointers.size===0&&(this.held=!1,performance.now()-e>90&&(this.spinSpeed=0)),n=0};t.addEventListener("pointerup",s),t.addEventListener("pointercancel",s),t.addEventListener("wheel",r=>{r.preventDefault(),this.zoomBy(Math.exp(r.deltaY*.0012)),this.spinSpeed=0,this.idleMs=0,this.tween=null},{passive:!1})}pinchDistance(){let[t,e]=[...this.pointers.values()];return t&&e?Math.hypot(t.x-e.x,t.y-e.y):0}update(t){let e=Math.max(0,Math.min(t,.1));if(this.tween){let s=this.tween,r=Math.min(1,(performance.now()-s.t0)/Ry),a=Py(r),o=new en().slerp(s.turn,a);this.target.lerpVectors(s.fromTarget,s.toTarget,a);let l=s.fromDist+(s.toDist-s.fromDist)*a;this.camera.up.copy(s.fromUp).applyQuaternion(o),this.camera.position.copy(this.target).add(s.fromDir.clone().applyQuaternion(o).multiplyScalar(l)),this.camera.lookAt(this.target),r>=1&&(this.tween=null);return}if(this.held)return;if(this.spinSpeed>0){this.turn(this.spinAxis,this.spinSpeed*e),this.spinSpeed=Np(this.spinSpeed,e),this.idleMs=0;return}this.idleMs+=e*1e3;let n=Dp(this.idleMs,this.autoEnabled);n>0&&this.turn(this.camera.up.clone().normalize(),n*e)}};var Iy="ams-life.brain/1",Bp={timeoutMs:8e3,maxParts:200},Ly=i=>i&&i.data!==void 0&&i.status!==void 0?i.data:i;function Ny(i,t){return Promise.race([i,new Promise((e,n)=>setTimeout(()=>n(new Error("超时")),t))])}async function kp(i,t,e){let n=await Ny(i("page/brain",t),e);if(n&&n.status==="error")throw new Error(n.message||"接口出错");let s=Ly(n);if(s&&s.stale){let r=new Error("数据更新了");throw r.stale=!0,r}return s}async function zp(i,t){let e=t&&t.timeoutMs||Bp.timeoutMs;for(let n=0;n<2;n++){let s=await kp(i,{},e);if(!s||s.schema!==Iy||!Array.isArray(s.nodes))throw new Error("不是她的数据");let r=Object.assign({},s,{nodes:s.nodes.slice(),edges:(s.edges||[]).slice()}),a=Math.min(Bp.maxParts,Math.max(1,Number(s.parts)||1));try{for(let o=1;o<a;o++){let l=await kp(i,{part:o,snap:s.snap},e);r.nodes.push(...l.nodes||[]),r.edges.push(...l.edges||[])}}catch(o){if(o.stale&&n===0)continue;throw o}return delete r.part,delete r.parts,delete r.snap,r}throw new Error("数据一直在变")}function Vp(i,t){return i?"示例数据（编造）· 接口没连上"+(t?"："+t:""):"示例数据（编造）· 不是从 AstrBot 后台打开的"}var Pn={step:600,hold:1800,fade:1600,rest:900};function Gp(i){return i===!0}function Hp(i){let t=new Map;return i.forEach((e,n)=>{t.set(e.source+":"+e.target,n),t.set(e.target+":"+e.source,n)}),t}function Wp(i,t,e){let n=new Set(e),s=[];for(let[r,a]of t){if(n.has(r)||n.has(a))continue;let o=i.get(r+":"+a);o!==void 0&&!s.some(l=>l.line===o)&&s.push({a:r,b:a,line:o})}return s}function Dy(i){return Math.max(1,i)*Pn.step+Pn.hold+Pn.fade+Pn.rest}function Xp(i,t,e,n){if(!n)return{lit:t,lines:i.map(l=>l.line),alpha:1,done:!1};let s=Math.min(t,Math.floor(e/Pn.step)+1),r=Math.max(1,t)*Pn.step+Pn.hold,a=e<=r?1:Math.max(0,1-(e-r)/Pn.fade),o=a>0?i.filter((l,c)=>e>=(c+.5)*Pn.step).map(l=>l.line):[];return{lit:s,lines:o,alpha:a,done:e>=Dy(t)}}function Ll(i,t){let e=[],n=[];return i.forEach((s,r)=>{s.source!==t&&s.target!==t||(n.push(r),s.kind==="link"&&e.push(r))}),e.length?e:n}var st=i=>document.getElementById(i),Ze=new URLSearchParams(location.search),Bl=86400,In={bloom:{strength:.35,radius:.35,threshold:.22},linkOpacity:.16,linkCurve:.35,twinkle:.5,nodeSize:1.35,space:{nebula:.35,fieldStars:.25,clusterClouds:.3},frameElevDeg:50},tm={charge:-170,linkDistance:55,linkStrength:1.1,centerPull:.02,flatten:0,coreGravity:0,spiral:0,velocityDecay:.6,ball:0,ballStrength:.6,sidePull:.05},ls=tm,Oi={lit:1,near:1,rest:.12,turnRest:.07},cs={window:"窗口",person:"人",memory:"记忆",event:"事件",note:"本子"},Qr={link:"联想",origin:"出处",about:"跟谁有关",impression:"印象"},Hn=[{key:"social",name:"想说话",c:"#ff8a1f"},{key:"curiosity",name:"好奇",c:"#54c08b"},{key:"boredom",name:"无聊",c:"#9a958c"},{key:"seen",name:"想被看见",c:"#f2c14e"},{key:"talked",name:"说多了",c:"#9b7bf6"},{key:"stress",name:"压力",c:"#e5533d"},{key:"valence",name:"心情",c:"#5b8def"}],qp=[28,200,120,330,50,170,280,90,0,230,150,300],Xn=new ut("#efe7d2"),Xh=new ut("#ffc861"),em=new ut("#7d7f88"),Je=null,hs="sample",qn=null,Bi=null,nm="",be=new Map,Ws=new Map,le={nodes:[],links:[]},Qe=new Map,im=null,je=[],Fl=new Map,It=null,zi=null,ge=null,Jr=80,us=300,ki=Br.high,$r={},Nl=null,re={kinds:new Set(Object.keys(cs)),win:"",vis:"all",from:24,to:0},de=-1,Ee=-1,qh=0,Vi=null,sm=-1,Vh=-1,Fe=!0,Gi=!0,kl=!1,Gh=!1,ta=!1,rm=new Map,Hi=new Map,Ul=new Map;function Uy(){let i=null;try{i=window.AstrBotPluginView||window.AstrBotPluginPage||window.astrbotPluginView||null}catch{i=null}try{!i&&window.parent&&window.parent!==window&&(i=window.parent.AstrBotPluginView||window.parent.AstrBotPluginPage||null)}catch{i=null}let t=!1;try{t=!!(window.parent&&window.parent!==window)}catch{t=!1}return i&&t?i:null}var Yh=i=>i&&i.data!==void 0?i.data:i;async function Oy(){if(Bi=Uy(),Bi)try{let i=await Promise.race([Bi.ready(),new Promise(e=>setTimeout(()=>e(null),3e3))]);!Ze.get("theme")&&!tu("bio_theme")&&i&&(Gi=!!i.isDark);let t=await zp((e,n)=>Bi.apiGet(e,n));return hs="live",t}catch(i){nm=String(i&&i.message||i||"").slice(0,60)}return qn=window.BrainSample.make({n:Number(Ze.get("n"))||900}),hs=Bi?"sample-embedded":"sample",qn.graph}async function By(i){if(hs==="live")try{let e=await Bi.apiGet("page/brain/node",{id:i});return e&&e.status==="error"?{error:e.message||"没取到"}:Yh(e)}catch(e){return{error:"没取到："+(e&&e.message||e)}}let t=qn&&qn.details[i];return t?Object.assign({},t,{qq:void 0,has_qq:!!t.qq}):null}async function ky(i){if(hs==="live")try{let t=await Bi.apiGet("page/brain/node",{id:i,reveal:"qq"});return(Yh(t)||{}).qq||"没取到"}catch{return"没取到"}return qn&&qn.details[i]&&qn.details[i].qq||""}async function zy(i){if(hs==="live")try{let e=Yh(await Bi.apiGet("page/brain/search",{q:i}));return Array.isArray(e)?e:e&&e.ids||[]}catch{return[]}let t=[];if(!qn)return t;for(let e in qn.details){let n=qn.details[e];((n.text||"").includes(i)||(n.title||"").includes(i))&&t.push(e)}return t}function Vy(i){Je=i,$r=Object.assign({},i.body||{}),be=new Map;for(let r of i.nodes||[])r&&r.id&&cs[r.kind]&&!be.has(r.id)&&be.set(r.id,r);Je.edges=(i.edges||[]).filter(r=>Qr[r.kind]&&be.has(r.s)&&be.has(r.t)&&r.s!==r.t),Je.turns=i.turns||[],Ws=new Map;for(let r of Je.edges)(Ws.get(r.s)||Ws.set(r.s,[]).get(r.s)).push({other:r.t,kind:r.kind,w:Number(r.w)||1}),(Ws.get(r.t)||Ws.set(r.t,[]).get(r.t)).push({other:r.s,kind:r.kind,w:Number(r.w)||1});let t=[...be.values()].filter(r=>r.kind==="window"&&r.sub!=="private").sort((r,a)=>(a.w||0)-(r.w||0)),e=[...be.values()].filter(r=>r.kind==="window"&&r.sub==="private");t.forEach((r,a)=>Hi.set(r.id,new ut().setHSL(qp[a%qp.length]/360,.66,.6))),e.forEach((r,a)=>Hi.set(r.id,new ut().setHSL((236+a*11%44)/360,.32,.74)));let n=i.now||Date.now()/1e3,s=1;for(let r of be.values())r.ts&&(s=Math.max(s,Math.ceil((n-r.ts)/Bl)));re.from=s,re.to=0;for(let r of["tFrom","tTo"])st(r).max=String(s)}function Gy(i){if(!re.kinds.has(i.kind))return!1;if(re.vis!=="all"){if(i.kind==="window"){if(i.sub==="private"!=(re.vis==="private"))return!1}else if(i.vis&&i.vis!==re.vis)return!1}if(i.ts&&i.kind!=="person"&&i.kind!=="window"){let t=((Je.now||Date.now()/1e3)-i.ts)/Bl;if(t>re.from+1e-4||t<re.to-1e-4)return!1}return!0}function Hy(){if(!ge)return;let i=ge.positions;le.nodes.forEach((t,e)=>Fl.set(t.id,[i[e*3],i[e*3+1],i[e*3+2]]))}function am(i){Hy();let t=[...be.values()].filter(Gy);if(ki.nodeCap&&t.length>ki.nodeCap){let o=t.filter(c=>c.kind==="window"||c.kind==="person"),l=t.filter(c=>c.kind!=="window"&&c.kind!=="person").sort((c,h)=>(h.w||0)-(c.w||0));t=o.concat(l.slice(0,Math.max(0,ki.nodeCap-o.length)))}je=t,Qe=new Map(t.map((o,l)=>[o.id,l]));let e=o=>{if(o.kind==="person")return 0;let l=o.kind==="window"?o:be.get(o.where);return l&&l.sub==="private"?1:-1},n=t.map(o=>({id:o.id,name:o.label||o.id,folderTop:o.where||o.id,degree:0,inDegree:0,outDegree:0,fileSize:0,tags:[],unresolved:o.vis==="private"&&o.kind!=="window",tag:!1,side:e(o)})),s=[];for(let o of Je.edges){let l=Qe.get(o.s),c=Qe.get(o.t);l===void 0||c===void 0||(s.push({source:l,target:c,kind:o.kind}),n[l].degree++,n[c].degree++,n[l].outDegree++,n[c].inDegree++)}le={nodes:n,links:s},im=Fp(le),rm=Hp(s);let r=nd(n.length);ls=Object.assign({},tm,{ball:Rp(n.length)});let a=new Float32Array(n.length*3);t.forEach((o,l)=>{let c=Fl.get(o.id);if(!c){let h=ed(o.id,ls.ball*.8);h[0]+=n[l].side*ls.ball*.3;let f=o.where&&Fl.get(o.where);c=f?[f[0]+h[0]*.25,f[1]+h[1]*.25,f[2]+h[2]*.25]:h}a.set(c,l*3)}),i&&(Jr=r*1.6),It||Yy(),It.setData(le,a),Wy(le,a,i?1:Fl.size?.3:1),de=-1,sm=-1,zl(),Wi(),qy()}function Wy(i,t,e){ge?.dispose();let n=Ze.get("settle")==="1";try{ge=n?new Hs:new Vs,ge.init(i,t,ls,e)}catch{ge=new Hs,ge.init(i,t,ls,e)}if(n){for(;ge.step(););It.updatePositions()}om=performance.now()}var om=0;function Xy(i){if(!(ge instanceof Vs)||ge.ticks>0||ge.isSettled()||i-om<2e3)return;let t=ge.positions;ge.dispose(),ge=new Hs,ge.init(le,t,ls,1)}function Zh(i){let t=Ul.get(i.id);if(t)return t;let e=be.get(i.id);if(!e||e.kind==="person")return Xn;let n=Hi.get(e.kind==="window"?e.id:e.where)||Hi.values().next().value||Xn;return e.kind==="event"?n.clone().offsetHSL(0,.05,.08):e.kind==="note"?n.clone().offsetHSL(0,-.1,.16):n}function zl(){It.setColorFn(Zh),It.recolor()}function lm(i){let t=new Set,e=Qe.get(i);if(e===void 0)return t;t.add(e);for(let n=0;n<je.length;n++)je[n].where===i&&t.add(n);return le.links.forEach(n=>{n.kind==="impression"&&(n.source===e||n.target===e)&&t.add(n.source===e?n.target:n.source),n.kind==="about"&&je[n.source].where===i&&t.add(n.target)}),t}function Wi(){if(!It)return;if(Ee>=0){dm(performance.now(),!0);return}let i=null,t=[];if(de>=0){t=Ll(le.links,de);let e=new Set([de]);for(let n of t)e.add(le.links[n].source),e.add(le.links[n].target);i=n=>e.has(n)?Oi.lit:Oi.rest}else if(Vi)i=e=>Vi.has(e)?Oi.lit:Oi.rest;else if(re.win){let e=lm(re.win);i=n=>e.has(n)?Oi.lit:Oi.rest}It.setFocus(i),It.setSelectedLinks(t,[]),cm(1)}function cm(i){It.selMaterial&&(It.selMaterial.opacity=.85*i)}function qy(){st("statLine").textContent="显示 "+le.nodes.length+" / "+be.size+" 颗星 · "+le.links.length+" 条关系"}function Yy(){let i=st("galaxy");It=new wl(i,Jr),zi=new Il(It.camera,It.renderer.domElement),It.setBloomParams(In.bloom),It.setNodeScale(In.nodeSize*(ki.id==="mobile"?1.9:1)),It.setLinkOpacity(In.linkOpacity),It.setLinkCurve(In.linkCurve),It.setSizeMode("degree"),It.setStarfieldEnabled(!0),It.setNebulaTint("#46d4dc","#9a7fe0"),It.setSpace(In.space),It.twinkleFreq=Fe?In.twinkle:0,It.applyTier(ki,In.bloom.strength),It.applyTokens(Gi?kr:Mh,In.bloom.strength),qi.build(),hi.build(),$h.build(),na.build()}var Wn=new D,hm=[],Xi=(i,t=new D)=>It.nodePosition(i,t);function um(){let i=le.nodes.length;if(!i)return{center:new D,radius:Jr};let t=new D;for(let s=0;s<i;s++)t.add(Xi(s,Wn));t.divideScalar(i);let e=new Float64Array(i);for(let s=0;s<i;s++)e[s]=Xi(s,Wn).distanceTo(t);e.sort();let n=Math.max(e[Math.min(i-1,Math.floor(i*.98))]||Jr,Jr*.3);return us=n,ea.copy(t),{center:t,radius:n}}var ea=new D;function Zr(){let i=um();na.place(i.center,i.radius),zi.frame(i.center,i.radius*1.08,null)}function Jh(i){if(!i.length)return;let t=new D;for(let n of i)t.add(Xi(n,Wn));t.divideScalar(i.length);let e=0;for(let n of i)e=Math.max(e,Xi(n,Wn).distanceTo(t));zi.frame(t,Math.max(e*1.1,us*.35),ea)}function fm(){let i=st("galaxy");It?.resize(i.clientWidth,i.clientHeight),Yr=i.clientHeight*(It?It.renderer.getPixelRatio():1)/(2*Math.tan((It?It.camera.fov:60)/2*Math.PI/180)),qi.setPixelScale(Yr),hi.setPixelScale(Yr),$h.setPixelScale(Yr),na.setPixelScale(Yr)}var Yr=1,Zy=`
attribute float aSize; attribute float aAlpha; attribute vec3 aColor;
varying float vAlpha; varying vec3 vColor; uniform float uPixelScale;
void main() { vAlpha = aAlpha; vColor = aColor;
	vec4 mv = modelViewMatrix * vec4(position, 1.0);
	gl_PointSize = min(aSize * uPixelScale / max(-mv.z, 1.0), 220.0);
	gl_Position = projectionMatrix * mv; }`,Jy=`
varying float vAlpha; varying vec3 vColor; uniform float uLight; uniform float uFade;
void main() { float d = length(gl_PointCoord - 0.5);
	float halo = smoothstep(0.5, 0.0, d); float core = smoothstep(0.16, 0.0, d);
	float a = (halo * halo * 0.9 + core) * vAlpha * uFade; if (a < 0.01) discard;
	if (uLight > 0.5) { gl_FragColor = vec4(mix(vColor, vColor * 0.7, core), min(a, 1.0)); return; }   // on paper: plain ink
	vec3 col = mix(vColor, vec3(1.0), core * 0.7);
	gl_FragColor = vec4(col * a, a); }`;function Hl(i){let t=new Qt;t.setAttribute("position",new Lt(new Float32Array(i*3),3).setUsage(Ni)),t.setAttribute("aSize",new Lt(new Float32Array(i),1).setUsage(Ni)),t.setAttribute("aAlpha",new Lt(new Float32Array(i),1).setUsage(Ni)),t.setAttribute("aColor",new Lt(new Float32Array(i*3),3).setUsage(Ni));let e=new se({vertexShader:Zy,fragmentShader:Jy,transparent:!0,depthWrite:!1,blending:Gi?Tn:On,uniforms:{uPixelScale:{value:1},uLight:{value:Gi?0:1},uFade:{value:1}}}),n=new an(t,e);return hm.push(e),n.frustumCulled=!1,n.renderOrder=3,It.scene.add(n),n}var qi={pts:null,pos:[],build(){this.pts=Hl(Hn.length);let i=this.pts.geometry.getAttribute("aColor");Hn.forEach((t,e)=>{let n=new ut(t.c);i.setXYZ(e,n.r,n.g,n.b),this.pos.push(new D)})},setPixelScale(i){this.pts&&(this.pts.material.uniforms.uPixelScale.value=i)},value(i){let t=Number($r[Hn[i].key]);return Number.isFinite(t)||(t=0),Hn[i].key==="valence"?t:Math.max(0,Math.min(1,t))},update(i){if(!this.pts)return;let t=this.pts.geometry,e=t.getAttribute("position"),n=t.getAttribute("aSize"),s=t.getAttribute("aAlpha"),r=t.getAttribute("aColor"),a=us*.24;Hn.forEach((o,l)=>{let c=l/Hn.length*Math.PI*2;this.pos[l].set(Math.cos(c)*a,0,Math.sin(c)*a),this.pos[l].add(ea),e.setXYZ(l,this.pos[l].x,this.pos[l].y,this.pos[l].z);let h=this.value(l);if(o.key==="valence"){let u=new ut(h>=0?"#f2c14e":"#5b8def");r.setXYZ(l,u.r,u.g,u.b),h=Math.min(1,Math.abs(h))}let f=Fe?1+Math.sin(i/1e3*(.8+h*1.6)+l)*(.05+h*.08):1;n.setX(l,us*(.08+h*.16)*f),s.setX(l,(Gi?.35:.55)+h*.65)}),e.needsUpdate=n.needsUpdate=s.needsUpdate=r.needsUpdate=!0}},$h={pts:null,max:48,build(){this.pts=Hl(this.max)},setPixelScale(i){this.pts&&(this.pts.material.uniforms.uPixelScale.value=i)},update(i){if(!this.pts)return;let t=this.pts.geometry,e=t.getAttribute("position"),n=t.getAttribute("aSize"),s=t.getAttribute("aAlpha"),r=t.getAttribute("aColor"),a=[];if(Ee>=0){let{rec:o,held:l}=Wl(),c=i-qh;o.forEach((h,f)=>{if(Fe&&c<f*Kr)return;let u=Fe?Math.max(0,1-(c-f*Kr)/900):0;a.push([h,Xh,.05*(1+u*1.6),.9])}),l.forEach(h=>a.push([h,em,.04,.55]))}else if(de>=0&&a.push([de,new ut(1,1,1),.045*(Fe?1+Math.sin(i/300)*.12:1),.7]),Vi)for(let o of Vi){if(a.length>=this.max)break;a.push([o,new ut("#ffb14d"),.03,.6])}for(let o=0;o<this.max;o++){let l=a[o];if(!l){s.setX(o,0);continue}Xi(l[0],Wn),e.setXYZ(o,Wn.x,Wn.y,Wn.z),n.setX(o,us*l[2]),s.setX(o,l[3]),r.setXYZ(o,l[1].r,l[1].g,l[1].b)}e.needsUpdate=n.needsUpdate=s.needsUpdate=r.needsUpdate=!0}},na={pts:null,count:900,build(){this.pts=Hl(this.count);let i=this.pts.geometry.getAttribute("aColor"),t=this.pts.geometry.getAttribute("aAlpha");for(let e=0;e<this.count;e++)i.setXYZ(e,.72,.8,1),t.setX(e,0)},setPixelScale(i){this.pts&&(this.pts.material.uniforms.uPixelScale.value=i)},radius:0,update(){if(!this.pts||!this.radius)return;let i=It.camera.position.distanceTo(ea);this.pts.material.uniforms.uFade.value=Math.max(0,Math.min(1,(i-this.radius*1.6)/(this.radius*.8)))},place(i,t){if(this.radius=t,!this.pts)return;let e=this.pts.geometry,n=e.getAttribute("position"),s=e.getAttribute("aSize"),r=e.getAttribute("aAlpha"),a=Math.PI*(3-Math.sqrt(5)),o=11,l=()=>(o=o*16807%2147483647,o/2147483647);for(let c=0;c<this.count;c++){let h=1-(c+.5)/this.count*2,f=Math.sqrt(1-h*h),u=c*a,p=t*(1.06+(l()-.5)*.05);n.setXYZ(c,i.x+Math.cos(u)*f*p,i.y+h*p,i.z+Math.sin(u)*f*p),s.setX(c,t*(.016+l()*.02)),r.setX(c,(Gi?.3:.4)+l()*.3)}n.needsUpdate=s.needsUpdate=r.needsUpdate=!0}},hi={pts:null,list:[],max:64,build(){this.pts=Hl(this.max)},setPixelScale(i){this.pts&&(this.pts.material.uniforms.uPixelScale.value=i)},emit(i,t,e,n,s){this.list.length<this.max&&this.list.push({a:i,b:t,color:e,t0:performance.now(),dur:n,big:s})},ambient(i){if(!(!ta||!Fe||Ee>=0||!le.links.length||this.list.length>24||Math.random()>.3))for(let t=0;t<6;t++){let e=le.links[Math.floor(Math.random()*le.links.length)];if(e.kind!=="link"&&Math.random()<.75||de>=0&&e.source!==de&&e.target!==de)continue;let n=Math.random()<.5,s=Zh(le.nodes[n?e.source:e.target]).clone().lerp(new ut(1,1,1),.35);this.emit(n?e.source:e.target,n?e.target:e.source,s,1300+Math.random()*1200,!1);break}},update(i){if(!this.pts)return;this.list=this.list.filter(l=>i-l.t0<l.dur&&l.a<le.nodes.length&&l.b<le.nodes.length);let t=this.pts.geometry,e=t.getAttribute("position"),n=t.getAttribute("aSize"),s=t.getAttribute("aAlpha"),r=t.getAttribute("aColor"),a=new D,o=new D;for(let l=0;l<this.max;l++){let c=this.list[l];if(!c){s.setX(l,0);continue}let h=Math.max(0,Math.min(1,(i-c.t0)/c.dur));$y(Xi(c.a,a),Xi(c.b,o),h,e,l),n.setX(l,us*(c.big?.03:.016)),s.setX(l,Math.sin(h*Math.PI)*(c.big?1:.8)),r.setXYZ(l,c.color.r,c.color.g,c.color.b)}e.needsUpdate=n.needsUpdate=s.needsUpdate=r.needsUpdate=!0}};function $y(i,t,e,n,s){let r=(i.x+t.x)/2,a=(i.y+t.y)/2,o=(i.z+t.z)/2,l=i.distanceTo(t),c=Math.hypot(r,a,o)||1,h=In.linkCurve*.32*l,f=r+r/c*h,u=a+a/c*h,p=o+o/c*h,g=(1-e)*(1-e),x=2*(1-e)*e,m=e*e;n.setXYZ(s,g*i.x+x*f+m*t.x,g*i.y+x*u+m*t.y,g*i.z+x*p+m*t.z)}var Kr=Pn.step,Vl=-1,Hh=-1;function Wl(){let i=Je.turns[Ee],t=(i.recalled||[]).map(s=>Qe.get(s)).filter(s=>s!==void 0),e=(i.held||[]).map(s=>Qe.get(s)).filter(s=>s!==void 0),n=(i.path||[]).map(s=>[Qe.get(s[0]),Qe.get(s[1])]).filter(s=>s[0]!==void 0&&s[1]!==void 0);return{tr:i,rec:t,held:e,path:n,where:Qe.get(i.where)}}function dm(i,t){if(Ee<0)return;let{rec:e,held:n,path:s,where:r}=Wl(),a=Wp(rm,s,n),o=i-qh,l=Xp(a,e.length,o,Fe);if(l.done&&!t&&Je.turns.length>1){ci((Ee+1)%Je.turns.length);return}if(l.lit!==Vl||l.lines.length!==Hh||t){Vl=l.lit,Hh=l.lines.length;let c=new Set(e.slice(0,l.lit)),h=new Set(n);It.setFocus(f=>c.has(f)||f===r?Oi.lit:h.has(f)?.9:Oi.turnRest),It.setSelectedLinks(l.lines,[])}cm(l.alpha),Fe&&a.forEach(({a:c,b:h},f)=>{let u=(f+.5)*Kr;o>=u&&o-u<60&&!hi.list.some(p=>p.a===c&&p.b===h&&i-p.t0<Kr)&&hi.emit(c,h,Xh,Kr*1.4,!0)})}function ci(i){let t=Je.turns||[];if(i>=t.length&&(i=t.length-1),i>=0&&Ee<0&&(Nl=$r),i<0&&Ee>=0&&Nl&&($r=Nl),Ee=i,Ul=new Map,i>=0){de=-1,st("drawer").hidden=!0;let{tr:n,rec:s,held:r,where:a}=Wl();for(let l of s)Ul.set(le.nodes[l].id,Xh);for(let l of r)Ul.set(le.nodes[l].id,em);n.body&&($r=Object.assign({},Nl,n.body)),qh=performance.now(),Vl=-1,Hh=-1,hi.list=[];let o=(n.recalled||[]).length+(n.held||[]).length-s.length-r.length;st("turnHint").textContent=Kh(n.ts)+" 在"+Yi(n.where)+"：想起 "+(n.recalled||[]).length+" 条（金色，按顺序亮，顺着线想过去），"+((n.held||[]).length?(n.held||[]).length+" 条她知道但在这里没说（灰的）。":"没有被挡下的。")+(n.body?" 中间的核是那一刻的身体。":"")+(o?"（有 "+o+" 条被筛掉了）":""),zl(),Jh(s.concat(a===void 0?[]:[a]))}else st("turnHint").textContent="点一轮看她这次想起了谁。平常星之间不连线，她想起来时才连。",zl();pm();let e=st("turnList").querySelector("li.on");e&&e.scrollIntoView&&e.scrollIntoView({block:"nearest",inline:"nearest"}),Wi()}function pm(){let i=Je.turns||[];if(!i.length){st("turnList").innerHTML='<li class="more">还没有记录。她被叫到一次，这里就多一轮。</li>';return}st("turnList").innerHTML=i.map((t,e)=>'<li data-turn="'+e+'"'+(e===Ee?' class="on"':"")+">"+Re(Kh(t.ts))+" · "+Re(Yi(t.where)||"?")+"<small>想起 "+(t.recalled||[]).length+" · 没说 "+(t.held||[]).length+"</small></li>").join("")}var Gl=new Map;function Yp(i,t,e,n,s){let r=Gl.get(i);r||(r=document.createElement("div"),r.className="lbl3",st("labels").appendChild(r),Gl.set(i,r)),r.textContent!==t&&(r.textContent=t),r.className="lbl3 "+(s||""),r.style.transform="translate("+Math.round(e)+"px,"+Math.round(n)+"px)",r.dataset.seen="1"}function Ky(){let i=st("galaxy"),t=i.clientWidth,e=i.clientHeight;for(let l of Gl.values())l.dataset.seen="";let n=(l,c,h,f,u)=>{let p=It.projectNode(c,t,e);p.behind||p.x<-40||p.y<-20||p.x>t+40||p.y>e+20||Yp(l,h,p.x,p.y+(u||10),f)},s=Ee>=0,r=s?Wl():null,a=re.win?Qe.get(re.win):void 0;if(le.nodes.forEach((l,c)=>{if(je[c].kind!=="window")return;let h=s&&c!==r.where||de>=0&&c!==de&&!jy(c)||a!==void 0&&c!==a;n("w"+c,c,l.name,"win"+(h?" faded":""),12)}),de>=0&&je[de].kind!=="window"&&n("sel",de,je[de].label,"sel",10),s){let{rec:l,held:c}=r;l.slice(0,Vl).forEach((h,f)=>n("r"+f,h,f+1+" · "+je[h].label+(je[h].where!==Je.turns[Ee].where?"（"+Yi(je[h].where)+"）":""),"lit",-22)),c.forEach((h,f)=>n("h"+f,h,"没说 · "+je[h].label+"（"+Yi(je[h].where)+"）","held",-22))}if(Vi&&!s&&de<0){let l=0;for(let c of Vi){if(l++>15)break;n("q"+c,c,je[c].label,"hit",10)}}let o=It.camera;t>=600&&qi.pos.forEach((l,c)=>{let h=Wn.copy(l).project(o);if(h.z>1)return;let f=qi.value(c),u=Hn[c].key==="valence"?(f>=0?"+":"−")+Math.round(Math.abs(f)*100):Math.round(f*100);Yp("c"+c,Hn[c].name+" "+u+"%",(h.x+1)/2*t,(1-h.y)/2*e+14,"core")});for(let l of Gl.values())l.style.display=l.dataset.seen?"":"none"}var Dl=null;function jy(i){return(!Dl||Dl.sel!==de)&&(Dl={sel:de,set:Up(im,de,1).depthOf}),Dl.set.has(i)}function Re(i){return String(i??"").replace(/[&<>"']/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"})[t])}var Kh=i=>{if(!i)return"";let t=new Date(i*1e3),e=n=>String(n).padStart(2,"0");return t.getMonth()+1+"-"+e(t.getDate())+" "+e(t.getHours())+":"+e(t.getMinutes())},jh=i=>{if(!i)return"";let t=(Je.now||Date.now()/1e3)-i;return t<3600?Math.max(1,Math.round(t/60))+" 分钟前":t<Bl?Math.round(t/3600)+" 小时前":Math.round(t/Bl)+" 天前"},mm=i=>cs[i.kind]+(i.kind==="window"?i.sub==="private"?" · 私聊":" · 群":""),Yi=i=>{let t=be.get(i);return t?t.label:""},gm=i=>[mm(i),i.label,i.where?Yi(i.where):"",jh(i.ts)].filter(Boolean).join(" · "),Xs=i=>"#"+i.getHexString(),jr=null;async function _m(i){jr=i.id,st("drawer").hidden=!1,st("dKind").textContent=mm(i)+(i.cat&&i.cat!==i.label?" · "+i.cat:""),st("dTitle").textContent=i.label||i.id;let t=[];i.ts&&t.push(["时间",Re(Kh(i.ts)+"（"+jh(i.ts)+"）")]),i.where&&t.push(["窗口",'<a data-go="'+Re(i.where)+'">'+Re(Yi(i.where))+"</a>"]),i.vis&&t.push(["分寸",i.vis==="private"?"私下（空心）":"公开"]),i.kind==="memory"&&t.push(["分量",Math.round((i.w||0)*100)+"%"]),i.kind==="note"&&i.self&&t.push(["","她写给自己的"]),t.push(["编号",Re(i.id)]),st("dMeta").innerHTML=t.map(([r,a])=>"<dt>"+Re(r)+"</dt><dd>"+a+"</dd>").join(""),st("dBody").innerHTML='<span class="muted">取内容…</span>',tM(i);let e=await By(i.id);if(jr!==i.id)return;if(!e){st("dBody").innerHTML='<span class="muted">没有更多内容。</span>';return}if(e.error){st("dBody").innerHTML='<span class="muted">'+Re(e.error)+"</span>";return}let n="";e.title&&(st("dTitle").textContent=e.title),e.text&&(n+='<div class="text">'+Re(e.text)+"</div>"),Array.isArray(e.lines)&&e.lines.length&&(n+="<dl>"+e.lines.map(([r,a])=>"<dt>"+Re(r)+"</dt><dd>"+Re(a)+"</dd>").join("")+"</dl>"),e.has_qq&&(n+='<div class="reveal"><button class="btn" id="qqBtn">显示 QQ 号</button> <span id="qqVal"></span></div>'),st("dBody").innerHTML=n||'<span class="muted">没有更多内容。</span>';let s=st("qqBtn");s&&(s.onclick=async()=>{s.disabled=!0;let r=await ky(i.id);jr===i.id&&(st("qqVal").textContent=r,s.remove())})}function Qy(i){jr="core:"+i;let t=Hn[i],e=qi.value(i);st("drawer").hidden=!1,st("dKind").textContent="身体",st("dTitle").textContent=t.name,st("dMeta").innerHTML="<dt>现在</dt><dd>"+(t.key==="valence"?(e>=0?"偏好 ":"偏低 ")+Math.round(Math.abs(e)*100):Math.round(e*100))+"%</dd><dt>说明</dt><dd>身体里的一样，只有数，不存话。越大越亮，数越高。</dd>",st("dBody").innerHTML="",st("dLinks").innerHTML=""}function tM(i){let t={};for(let n of Ws.get(i.id)||[])(t[n.kind]=t[n.kind]||[]).push(n);let e='<div class="d-links">';for(let n of Object.keys(Qr)){let s=t[n];if(s){s.sort((r,a)=>a.w-r.w),e+="<h3>"+Qr[n]+" · "+s.length+"</h3><ul>";for(let r of s.slice(0,40)){let a=be.get(r.other),o=a.kind==="person"?Xn:Hi.get(a.kind==="window"?a.id:a.where)||Xn;e+='<li data-id="'+Re(a.id)+'"><span class="dot'+(a.vis==="private"&&a.kind!=="window"?" ring":"")+'" style="--c:'+Xs(o)+'"></span>'+Re(gm(a))+(Qe.has(a.id)?"":' <span class="muted">（筛掉了）</span>')+"</li>"}s.length>40&&(e+='<li class="more">还有 '+(s.length-40)+" 个</li>"),e+="</ul>"}}st("dLinks").innerHTML=e+"</div>"}function Ui(i,t){if(Vh=-1,i<0){de=-1,jr=null,st("drawer").hidden=!0,Wi();return}if(Ee>=0&&ci(-1),de=i,Wi(),Fe)for(let e of Ll(le.links,i)){let n=le.links[e],s=n.source===i?n.target:n.source;hi.emit(i,s,Zh(le.nodes[s]).clone().lerp(new ut(1,1,1),.4),1200,!1)}if(_m(je[i]),t){let e=[i];for(let n of Ll(le.links,i)){let s=le.links[n];e.push(s.source===i?s.target:s.source)}e.length>1?Jh(e):zi.frame(Xi(i),us*.15,ea)}}function Wh(i,t){let e=Qe.get(i);e!==void 0?Ui(e,t):be.has(i)&&(de=-1,Wi(),_m(be.get(i)))}var Zp=0;function Qh(){let i=st("q").value.trim();if(clearTimeout(Zp),!i){Vi=null,st("hits").innerHTML="",Wi();return}Zp=setTimeout(async()=>{let t=new Set,e=i.toLowerCase();for(let s of be.values())[s.id,s.label,s.cat,cs[s.kind],s.where?Yi(s.where):""].join(" ").toLowerCase().includes(e)&&t.add(s.id);for(let s of await zy(i))be.has(s)&&t.add(s);if(st("q").value.trim()!==i)return;Vi=new Set([...t].map(s=>Qe.get(s)).filter(s=>s!==void 0));let n=[...t].filter(s=>Qe.has(s)).slice(0,60);st("hits").innerHTML=(n.length?"":'<li class="more">没找到（或被筛掉了）</li>')+n.map(s=>{let r=be.get(s),a=r.kind==="person"?Xn:Hi.get(r.kind==="window"?r.id:r.where)||Xn;return'<li data-id="'+Re(s)+'"><span class="dot" style="--c:'+Xs(a)+'"></span>'+Re(r.label)+(r.where?" · "+Re(Yi(r.where)):"")+'<span class="k">'+Re(jh(r.ts)||cs[r.kind])+"</span></li>"}).join("")+(t.size>n.length?'<li class="more">共 '+t.size+" 个，图上都亮着</li>":""),Wi()},200)}function tu(i){try{return localStorage.getItem(i)||""}catch{return""}}function Jp(i,t){try{localStorage.setItem(i,t)}catch{}}function Ol(i){Gi=i,document.documentElement.dataset.theme=i?"dark":"light",st("themeBtn").textContent=i?"浅色":"深色",It&&(It.applyTokens(i?kr:Mh,In.bloom.strength),zl(),Wi());for(let t of hm)t.blending=i?Tn:On,t.uniforms.uLight.value=i?0:1,t.needsUpdate=!0}function eM(){let i=Ze.get("theme");if(i==="dark"||i==="light")return Ol(i==="dark");let t=tu("bio_theme");if(t==="dark"||t==="light")return Ol(t==="dark");Ol(!0)}function nM(){let i={},t={};for(let a of be.values())i[a.kind]=(i[a.kind]||0)+1;for(let a of Je.edges)t[a.kind]=(t[a.kind]||0)+1;let e={window:"#ff8a1f",person:Xs(Xn),memory:"#8cacc4",event:"#f2c14e",note:"#a78bfa"};st("kindBoxes").innerHTML=Object.keys(cs).map(a=>'<label><input type="checkbox" data-kind="'+a+'"'+(re.kinds.has(a)?" checked":"")+' /><span class="chip" style="background:'+e[a]+'"></span>'+cs[a]+' <span class="n">'+(i[a]||0)+"</span></label>").join(""),st("lineCount").textContent=Object.keys(Qr).map(a=>Qr[a]+" "+(t[a]||0)).join(" · "),st("allLines").checked=ta;let n=[...be.values()].filter(a=>a.kind==="window"),s={};for(let a of be.values())a.where&&(s[a.where]=(s[a.where]||0)+1);let r=a=>'<option value="'+Re(a.id)+'">'+Re(a.label)+"（"+(s[a.id]||0)+"）</option>";st("winSel").innerHTML='<option value="">全部窗口</option><optgroup label="群">'+n.filter(a=>a.sub!=="private").map(r).join("")+'</optgroup><optgroup label="私聊">'+n.filter(a=>a.sub==="private").map(r).join("")+"</optgroup>",st("legendWins").innerHTML=n.filter(a=>a.sub!=="private").slice(0,12).map(a=>'<span><i style="background:'+Xs(Hi.get(a.id))+'"></i>'+Re(a.label)+"</span>").join("")+'<span><i class="ring" style="--c:'+Xs(Hi.get(n.find(a=>a.sub==="private")?.id)||Xn)+'"></i>私聊（空心）</span><span><i style="background:'+Xs(Xn)+'"></i>人</span>',st("tFrom").value=String(re.from),st("tTo").value=String(re.to),xm()}function xm(){st("timeText").textContent=re.to===0?"最近 "+re.from+" 天":re.from+"–"+re.to+" 天前"}var $p=0;function kh(){clearTimeout($p),$p=setTimeout(()=>{let i=Ee;Ee=-1,am(!1),Gh=!1,kl=i>=0,i>=0&&ci(i),Qh()},120)}function iM(){st("kindBoxes").addEventListener("change",a=>{let o=a.target.dataset.kind;o&&(a.target.checked?re.kinds.add(o):re.kinds.delete(o),kh())}),st("allLines").addEventListener("change",()=>{ta=st("allLines").checked,hi.list=[]}),st("winSel").addEventListener("change",()=>{re.win=st("winSel").value,Ui(-1),Qe.get(re.win)!==void 0?Jh([...lm(re.win)]):Zr()}),st("visSeg").addEventListener("click",a=>{let o=a.target.dataset.vis;if(o){re.vis=o;for(let l of st("visSeg").children)l.classList.toggle("on",l.dataset.vis===o);kh()}});let i=()=>{let a=Number(st("tFrom").value),o=Number(st("tTo").value);o>a&&(document.activeElement===st("tFrom")?o=a:a=o,st("tFrom").value=a,st("tTo").value=o),re.from=a,re.to=o,xm(),kh()};st("tFrom").addEventListener("input",i),st("tTo").addEventListener("input",i),st("q").addEventListener("input",Qh);let t=a=>{let o=a.target.closest("[data-id]");o&&Wh(o.dataset.id,!0)};st("hits").addEventListener("click",t),st("dLinks").addEventListener("click",t),st("dMeta").addEventListener("click",a=>{let o=a.target.closest("[data-go]");o&&Wh(o.dataset.go,!0)}),st("drawerClose").addEventListener("click",()=>Ui(-1)),st("turnList").addEventListener("click",a=>{let o=a.target.closest("[data-turn]");o&&ci(Number(o.dataset.turn))}),st("turnPrev").addEventListener("click",()=>ci(Ee<=0?Je.turns.length-1:Ee-1)),st("turnNext").addEventListener("click",()=>ci(Ee+1>=Je.turns.length?0:Ee+1)),st("turnOff").addEventListener("click",()=>{ci(-1),Zr()}),st("fitBtn").addEventListener("click",()=>{Ui(-1),Zr()}),st("motionBtn").addEventListener("click",()=>{Fe=!Fe,st("motionBtn").classList.toggle("on",Fe),Jp("brain_motion",Fe?"1":"0"),zi.autoEnabled=Fe,It.twinkleFreq=Fe?In.twinkle:0}),st("themeBtn").addEventListener("click",()=>{let a=!Gi;Ol(a),Jp("bio_theme",a?"dark":"light")}),st("panelBtn").addEventListener("click",()=>st("side").classList.toggle("open")),window.addEventListener("resize",fm),window.addEventListener("keydown",a=>{a.target&&/INPUT|SELECT|TEXTAREA/.test(a.target.tagName)||(a.key==="Escape"?Ee>=0?ci(-1):Ui(-1):a.key==="ArrowRight"?st("turnNext").click():a.key==="ArrowLeft"?st("turnPrev").click():(a.key==="r"||a.key==="R")&&Zr())});let e=It.renderer.domElement,n=0,s=0;e.addEventListener("pointerdown",a=>{n=a.clientX,s=a.clientY}),e.addEventListener("pointerup",a=>{if(a.button!==0||a.ctrlKey||a.metaKey||a.shiftKey||Math.hypot(a.clientX-n,a.clientY-s)>5)return;let o=e.getBoundingClientRect(),l=a.clientX-o.left,c=a.clientY-o.top,h=Kp(l,c,o.width,o.height);if(h>=0){Ui(-1),Vh=h,Qy(h);return}let f=It.pickNearest(l,c,o.width,o.height,14);f>=0?Ui(f,!0):(de>=0||Vh>=0)&&Ui(-1)});let r=!1;e.addEventListener("pointermove",a=>{ki.hoverThrottleMs===null||r||a.buttons||(r=!0,setTimeout(()=>{r=!1;let o=e.getBoundingClientRect(),l=a.clientX-o.left,c=a.clientY-o.top,h=Kp(l,c,o.width,o.height),f=h>=0?-1:It.pickNearest(l,c,o.width,o.height,10);sm=f;let u=st("tip");h>=0||f>=0?(u.textContent=h>=0?Hn[h].name+" · "+Math.round(Math.abs(qi.value(h))*100)+"%":gm(je[f]),u.hidden=!1,u.style.left=Math.min(o.width-u.offsetWidth-8,l+14)+"px",u.style.top=c+14+"px",e.style.cursor="pointer"):(u.hidden=!0,e.style.cursor="")},ki.hoverThrottleMs))}),e.addEventListener("pointerleave",()=>{st("tip").hidden=!0})}function Kp(i,t,e,n){let s=-1,r=22;return qi.pos.forEach((a,o)=>{let l=Wn.copy(a).project(It.camera);if(l.z>1)return;let c=Math.hypot((l.x+1)/2*e-i,(1-l.y)/2*n-t);c<r&&(r=c,s=o)}),s}var sM=Ze.get("debug")==="1",jp=0,zh=null;function vm(i){let t=Bh(i,zh),e=Op(i,zh);zh=i,Xy(i),ge.step()&&It.updatePositions(),ge.isSettled()&&!Gh&&(Gh=!0,It.refreshClusterClouds(),st("loading").style.display="none",kl||(kl=!0,Ee<0&&de<0&&!re.win&&Zr())),zi.update(e),dm(i),hi.ambient(i),hi.update(i),qi.update(i),$h.update(i),na.update(),It.linkSegments&&(It.linkSegments.visible=Gp(ta)),It.render(e,t),Ky(),sM&&jp++%30===0&&(st("statLine").dataset.debug=(ge instanceof Vs?"worker":"main")+" ticks="+ge.ticks+" settled="+ge.isSettled()+" frames="+jp),requestAnimationFrame(vm)}async function Qp(){eM(),Fe=tu("brain_motion")!=="0"&&!(window.matchMedia&&window.matchMedia("(prefers-reduced-motion: reduce)").matches),Ze.get("motion")==="0"&&(Fe=!1),Ze.get("lines")==="all"&&(ta=!0),st("motionBtn").classList.toggle("on",Fe);let i=window.matchMedia&&window.matchMedia("(pointer: coarse)").matches;ki=Br[Ze.get("tier")]||(i||window.innerWidth<820?Br.mobile:Br.high);let t=await Oy();if(hs!=="live"){let n=st("sourceBadge");n.hidden=!1,n.textContent=Vp(hs==="sample-embedded",nm)}Vy(t),nM(),am(!0),zi.autoEnabled=Fe,fm();let e=um();zi.setInitial(e.center,ge.isSettled()?e.radius*1.08:Math.max(e.radius,ls.ball)*1.08),ge.isSettled()&&na.place(e.center,e.radius),ge.isSettled()&&(kl=!0),iM(),pm(),Ze.get("win")&&(st("winSel").value=Ze.get("win"),st("winSel").dispatchEvent(new Event("change"))),Ze.get("sel")&&Wh(Ze.get("sel"),!0),Ze.get("turn")&&ci(Number(Ze.get("turn"))-1),Ze.get("q")&&(st("q").value=Ze.get("q"),Qh()),requestAnimationFrame(vm)}document.readyState==="loading"?document.addEventListener("DOMContentLoaded",Qp,{once:!0}):Qp();})();
/*! Bundled license information:

three/build/three.core.js:
three/build/three.module.js:
  (**
   * @license
   * Copyright 2010-2026 Three.js Authors
   * SPDX-License-Identifier: MIT
   *)
*/
