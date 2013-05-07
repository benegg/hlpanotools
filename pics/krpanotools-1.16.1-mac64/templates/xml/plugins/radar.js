/* krpanoJS 1.16.1 radar plugin (build 2013-03-30) */
var krpanoplugin=function(){function z(){var j=k,f=e/2;if(q){var c=a.getmouse(!0);c.x*=e/Number(d.width);c.y*=e/Number(d.height);c=180*Math.atan2(c.y-f,c.x-f)/Math.PI;c-=p;null==l?l=c-h.view.hlookat:h.view.hlookat=c-l}var c=(p+r-90+h.view.hlookat)*Math.PI/180,b=0.5*h.view.fov*Math.PI/180;s&&(b=-b);if(0.01<Math.abs(c-w)||0.02<Math.abs(b-x))w=c,x=b,g=!0;g&&(g=!1,j.clearRect(0,0,e,e),j.fillStyle="rgba("+(m>>16&255)+","+(m>>8&255)+","+(m&255)+","+t+")",j.strokeStyle="rgba("+(n>>16&255)+","+(n>>8&255)+
","+(n&255)+","+u+")",j.lineWidth=v,j.beginPath(),j.moveTo(f,f),j.arc(f,f,f,c-b,c+b),j.fill())}var h=null,a=null,d=null,k=null,e=256,p=0,r=90,s=!1,m=16777215,n=16777215,t=0.5,u=0.3,v=0,q=!1,l=null,g=!0,y=null,w=0,x=0;this.registerplugin=function(j,f,c){h=j;a=c;"1.0.8.14">h.version||"2011-03-30">h.build?(h.trace(3,"radar plugin - too old krpano version (min. 1.0.8.14)"),a=h=null):(a.registerattribute("heading",0,function(b){p=Number(b);g=!0},function(){return p}),a.registerattribute("headingoffset",
90,function(b){r=Number(b);g=!0},function(){return r}),a.registerattribute("invert",!1,function(b){s="true"==String(b).toLowerCase();g=!0},function(){return s}),a.registerattribute("fillcolor",16777215,function(b){m=parseInt(b);g=!0},function(){return m}),a.registerattribute("linecolor",16777215,function(b){n=parseInt(b);g=!0},function(){return n}),a.registerattribute("fillalpha",0.5,function(b){t=Number(b);g=!0},function(){return t}),a.registerattribute("linealpha",0.3,function(b){u=Number(b);g=
!0},function(){return u}),a.registerattribute("linewidth",0,function(b){v=Number(b);g=!0},function(){return v}),a.handcursor=!1,a.ondown=function(){q=!0;l=null},a.onup=function(){q=!1;l=null},a.registercontentsize(e,e),d=document.createElement("canvas"),d.width=e,d.height=e,d.style.width="100%",d.style.height="100%",d.onselectstart=function(){return!1},a.sprite.appendChild(d),k=d.getContext("2d"),y=setInterval(z,1E3/30))};this.unloadplugin=function(){h&&a&&(clearInterval(y),a.sprite.removeChild(d),
h=a=d=k=null)};this.hittest=function(a,d){return k.isPointInPath(a,d)};this.onresize=function(a,f){e=Math.max(a,f);d.width=a;d.height=f;k.scale(a/e,f/e);g=!0;return!1}};
