/* krpano 1.16.4 scrollarea plugin (build 2013-06-05) */
var krpanoplugin=function(){function L(a){return"boolean"==typeof a?a:0<="yesontrue1".indexOf(String(a).toLowerCase())}function r(a,b,c,f,e){var d=null;e=(!0===e?"remove":"add")+"EventListener";var g=E.browser.events;if(g.touch&&("down"==b?d=g.touchstart:"move"==b?d=g.touchmove:"up"==b&&(d=g.touchend),E.ie&&!1==g.mouse&&("over"==b?d="MSPointerOver":"out"==b&&(d="MSPointerOut")),d))a[e](d,c,f);if(g.mouse&&("down"==b?d="mousedown":"move"==b?d="mousemove":"up"==b?d="mouseup":"over"==b?d="mouseover":
"out"==b&&(d="mouseout"),d))a[e](d,c,f)}function M(){if(c){var a=c.sprite.parentNode;if(a&&(a=a.kobject))a.maskchildren=!0,a.poschanged&&a.updatepluginpos(),N=a,m=a.pixelwidth,n=a.pixelheight,isNaN(m)&&(m=0),isNaN(n)&&(n=0),C=0<m||0<n}}function F(a){a=void 0===a?!1:a;1==(h&1)?c.x!=e&&(c.x=e,a=!0):e=0;2==(h&2)?c.y!=d&&(c.y=d,a=!0):d=0;if(a&&c&&c.onscroll){if(C){a=m-u;var b=n-v,t=e,f=d;isNaN(t)&&(t=0);isNaN(f)&&(f=0);t+=a*p;f+=b*q;c.woverflow=-a;c.hoverflow=-b;c.loverflow=Math.round((-t+A*a)*x);c.roverflow=
Math.round((+t-(1-A)*a)*x);c.toverflow=Math.round((-f+B*b)*y);c.boverflow=Math.round((+f-(1-B)*b)*y)}l.call(c.onscroll,c)}}function S(a){for(;0<s.length&&!(100>=a-s[0].time);)s.shift()}function G(){M();var a=String(c.align).toLowerCase();if(""==a||"null"==a)a="lefttop";y=x=1;q=p=0.5;B=A=0;0<=a.indexOf("left")&&(p=A=0,x=1);0<=a.indexOf("top")&&(q=B=0,y=1);0<=a.indexOf("right")&&(A=1,p=0,x=-1);0<=a.indexOf("bottom")&&(B=1,q=0,y=-1)}function T(a){G();s=[];if(!1==O)w=!1;else{r(window,"up",U,!0);r(window,
"move",V,!0);var b=l.stagescale,c=a.changedTouches&&0<a.changedTouches.length?a.changedTouches[0]:a;a=c.pageX/b;b=c.pageY/b;w=!1;H=a;I=b;return!1}}function W(a){if(!(void 0!==a.pointerType&&4!=a.pointerType)&&P&&(G(),!1!=C&&(a=n-v,0>m-u||0>a)))D=!0,r(c.sprite,"move",X,!0),r(c.sprite,"out",Y,!0)}function X(){if(D&&!1==w&&N){var a=N.getmouse();J(a.x/m*c.pixelwidth,a.y/n*c.pixelheight,!0)}}function Y(){r(c.sprite,"move",X,!0,!0);r(c.sprite,"out",Y,!0,!0);D=!1}function V(a){var b=l.stagescale,t=a.changedTouches&&
0<a.changedTouches.length?a.changedTouches[0]:a,f=t.pageX/b,b=t.pageY/b;if(!1==w&&(h&1&&5<Math.abs(f-H)||h&2&&5<Math.abs(b-I)))z&&(g=j=0,z=!1),null!=k&&(clearInterval(k),k=null),w=!0,D=!1,H=f,I=b,e=Number(c.x),d=Number(c.y),isNaN(Q)&&(e=0),isNaN(R)&&(d=0),Q=e,R=d;w&&(a=a.timeStamp,S(a),s.push({time:a,x:f,y:b}),e=Q+(f-H)*x,d=R+(b-I)*y,f=-(u-m),a=-(v-n),e+=f*p,d+=a*q,e=0<f?e-(e-f*p)/2:e-(0<e?e:e<f?e-f:0)/2,d=0<a?d-(d-a*q)/2:d-(0<d?d:d<a?d-a:0)/2,e-=f*p,d-=a*q,F());return!1}function U(a){r(window,"up",
U,!0,!0);r(window,"move",V,!0,!0);if(w){S(a.timeStamp);if(1<s.length){a=s[0];var b=s[s.length-1],c=b.y-a.y,d=(b.time-a.time)/15;j=(b.x-a.x)/d*x;g=c/d*y}else g=j=0;k=setInterval(K,1E3/60);w=!1}}function da(){setTimeout(function(){M();F(!0);null==k&&(k=setInterval(K,1E3/60))},100)}function K(){e+=j;d+=g;j*=Z;g*=Z;var a=0,b=0,c=-(u-m),f=-(v-n);e+=c*p;d+=f*q;0<c?a=e-c*p:z?a=e-$:e<c?a=e-c:0<e&&(a=e);0.1>a*a&&(a=0);0<f?b=d-f*q:z?b=d-aa:d<f?b=d-f:0<d&&(b=d);0.1>b*b&&(b=0);e-=c*p;d-=f*q;0==(h&1)&&(j=a=0);
0==(h&2)&&(g=b=0);0!=a&&(a*=-1,j=0>=a*j?j+a*ba:a*ca);0!=b&&(b*=-1,g=0>=b*g?g+b*ba:b*ca);0==a&&(0==b&&0.05>Math.sqrt(j*j+g*g))&&(z=!1,g=j=0,clearInterval(k),k=null);F()}function J(a,b,c){G();if(!1==C)setTimeout(function(){J(a,b,c)},10);else{a=Number(a);isNaN(a)&&(a=0);b=Number(b);isNaN(b)&&(b=0);var f=m-u,g=n-v;a=A*u+a*x;b=B*v+b*y;a*=-1;b*=-1;a+=m/2;0<a&&(a=0);a<f&&(a=f);b+=n/2;0<b&&(b=0);b<g&&(b=g);!0===c?(z=!0,$=a,aa=b,null==k&&(k=setInterval(K,1E3/60))):(f=-(u-m),g=-(v-n),a=0>f?a-f*p:0,b=0>g?b-
g*q:0,e=a,d=b,F())}}function ea(a,b){J(a,b,!0)}function fa(){null!=k&&(clearInterval(k),k=null);D=w=!1;s=[];g=j=0;z=!1}function ga(a,b){z=!1;a=Number(a);isNaN(a)&&(a=0);b=Number(b);isNaN(b)&&(b=0);G();if(!1!=C){var c=m-u,f=n-v,h=!1;0>c&&(e+=c*p,0<a&&0>e?(h=!0,j+=a):0>a&&e>c&&(h=!0,j+=a),e-=c*p);0>f&&(d+=f*q,0<b&&0>d?(h=!0,g+=b):0>b&&d>f&&(h=!0,g+=b),d-=f*q);h&&null==k&&(k=setInterval(K,1E3/60))}}var l=null,c=null,E=null,h=3,u=0,v=0,C=!1,N=null,m=0,n=0,z=!1,$=0,aa=0,x=1,y=1,p=0,q=0,A=0,B=0,Z=0.95,
ba=0.08,ca=0.15,O=!0,w=!1,H=0,I=0,e=0,d=0,Q=0,R=0,k=null,s=[],j=0,g=0,D=!1,P=!1;this.registerplugin=function(a,b,d){l=a;c=d;"1.16">l.version?(l.trace(3,"Scrollarea Plugin - too old krpano version (min. version 1.16)"),c=l=null):(E=l.device,c.registerattribute("direction","all",function(a){a=String(a).toLowerCase();h=0;h|=1*(0<=a.indexOf("h"));h|=2*(0<=a.indexOf("v"));h|=3*(0<=a.indexOf("all"))},function(){return 3==(h&3)?"all":1==(h&1)?"h":"v"}),c.registerattribute("onscroll",null),c.registerattribute("woverflow",
0),c.registerattribute("hoverflow",0),c.registerattribute("loverflow",0),c.registerattribute("roverflow",0),c.registerattribute("toverflow",0),c.registerattribute("boverflow",0),c.registerattribute("draggable",!0,function(a){O=L(a)},function(){return O}),c.registerattribute("onhover_autoscrolling",!1,function(a){P=L(a)},function(){return P}),c.registerattribute("csshardwareacceleration","auto"),c.setcenter=J,c.scrolltocenter=ea,c.stopscrolling=fa,c.scrollby=ga,!0==L(c.csshardwareacceleration)&&(c.sprite.style[E.browser.css.transform+
"Style"]="preserve-3d"),r(c.sprite,"down",T,!0),r(c.sprite,"over",W,!0),l.set("events["+c.name+"_scrollarea].keep",!0),l.set("events["+c.name+"_scrollarea].onresize",da))};this.onresize=function(a,b){if(!l)return!1;u=a;v=b;M();return!1};this.unloadplugin=function(){l&&c&&(l.set("events["+c.name+"_scrollarea].name",null),null!=k&&(clearInterval(k),k=null),r(c.sprite,"down",T,!0,!0),r(c.sprite,"over",W,!0,!0));l=c=null}};
