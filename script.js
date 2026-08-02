// ===============================
// RACEBOX MVP
// PART 1
// ===============================

const speedEl=document.getElementById("speed");
const timerEl=document.getElementById("timer");
const distanceEl=document.getElementById("distance");
const topSpeedEl=document.getElementById("topSpeed");
const statusEl=document.getElementById("status");
const accuracyEl=document.getElementById("accuracy");

const r60=document.getElementById("r60");
const r100=document.getElementById("r100");
const r200=document.getElementById("r200");
const r400=document.getElementById("r400");
const r500=document.getElementById("r500");

const resetBtn=document.getElementById("resetBtn");

let running=false;
let startTime=0;
let timerFrame=null;

let totalDistance=0;
let topSpeed=0;

let lastLat=null;
let lastLng=null;

const result={
60:false,
100:false,
200:false,
400:false,
500:false
};

function haversine(lat1,lon1,lat2,lon2){

const R=6371000;

const dLat=(lat2-lat1)*Math.PI/180;
const dLon=(lon2-lon1)*Math.PI/180;

const a=
Math.sin(dLat/2)**2+
Math.cos(lat1*Math.PI/180)*
Math.cos(lat2*Math.PI/180)*
Math.sin(dLon/2)**2;

return R*2*Math.atan2(Math.sqrt(a),Math.sqrt(1-a));

}

function updateTimer(){

if(!running)return;

const t=performance.now()-startTime;

const m=Math.floor(t/60000);
const s=Math.floor((t%60000)/1000);
const ms=Math.floor(t%1000);

timerEl.textContent=
String(m).padStart(2,"0")+
":"+
String(s).padStart(2,"0")+
"."+
String(ms).padStart(3,"0");

timerFrame=requestAnimationFrame(updateTimer);

}

function startRun(){

if(running)return;

running=true;

startTime=performance.now();

statusEl.textContent="RUNNING";

updateTimer();

}

function finishRun(){

running=false;

cancelAnimationFrame(timerFrame);

statusEl.textContent="FINISHED";

saveHistory();

}

function resetRun(){

running=false;

cancelAnimationFrame(timerFrame);

timerEl.textContent="00:00.000";
speedEl.textContent="0";
distanceEl.textContent="0.0 m";
topSpeedEl.textContent="0 km/h";
accuracyEl.textContent="-";
statusEl.textContent="READY";

totalDistance=0;
topSpeed=0;

lastLat=null;
lastLng=null;

r60.textContent="--";
r100.textContent="--";
r200.textContent="--";
r400.textContent="--";
r500.textContent="--";

result[60]=false;
result[100]=false;
result[200]=false;
result[400]=false;
result[500]=false;

}

resetBtn.onclick=resetRun;

// ===============================
// RACEBOX MVP
// PART 2 - GPS ENGINE
// ===============================

function checkDistance(time){

if(totalDistance>=60&&!result[60]){

result[60]=true;
r60.textContent=time.toFixed(3)+" s";

}

if(totalDistance>=100&&!result[100]){

result[100]=true;
r100.textContent=time.toFixed(3)+" s";

}

if(totalDistance>=200&&!result[200]){

result[200]=true;
r200.textContent=time.toFixed(3)+" s";

}

if(totalDistance>=400&&!result[400]){

result[400]=true;
r400.textContent=time.toFixed(3)+" s";

}

if(totalDistance>=500&&!result[500]){

result[500]=true;
r500.textContent=time.toFixed(3)+" s";

finishRun();

}

}

if(!navigator.geolocation){

alert("Browser tidak mendukung GPS.");

}else{

navigator.geolocation.watchPosition(

(position)=>{

const c=position.coords;

accuracyEl.textContent="± "+Math.round(c.accuracy)+" m";

let speed=0;

if(c.speed!==null){

speed=c.speed*3.6;

}

speedEl.textContent=Math.round(speed);

if(speed>topSpeed){

topSpeed=speed;

topSpeedEl.textContent=Math.round(topSpeed)+" km/h";

}

if(speed>=3&&!running){

startRun();

}

if(lastLat!==null){

const d=haversine(

lastLat,
lastLng,
c.latitude,
c.longitude

);

if(d>1&&d<40){

totalDistance+=d;

distanceEl.textContent=totalDistance.toFixed(1)+" m";

if(running){

const sec=(performance.now()-startTime)/1000;

checkDistance(sec);

}

}

}

lastLat=c.latitude;
lastLng=c.longitude;

},

(error)=>{

console.log(error);

alert("GPS Error : "+error.message);

},

{

enableHighAccuracy:true,
maximumAge:0,
timeout:10000

}

);

}

// ===============================
// RACEBOX MVP
// PART 3 - AUTO STOP & FILTER
// ===============================

let speedHistory=[];

function smoothSpeed(speed){

speedHistory.push(speed);

if(speedHistory.length>5){

speedHistory.shift();

}

let total=0;

for(const s of speedHistory){

total+=s;

}

return total/speedHistory.length;

}

let stopCounter=0;

function updateStatus(speed){

if(!running)return;

if(speed<1){

stopCounter++;

}else{

stopCounter=0;

}

if(stopCounter>=5){

finishRun();

}

}

function updateGPS(position){

const c=position.coords;

let speed=0;

if(c.speed!=null){

speed=c.speed*3.6;

}

speed=smoothSpeed(speed);

speedEl.textContent=Math.round(speed);

updateStatus(speed);

if(speed>topSpeed){

topSpeed=speed;

topSpeedEl.textContent=Math.round(topSpeed)+" km/h";

}

accuracyEl.textContent="± "+Math.round(c.accuracy)+" m";

if(speed>=3&&!running){

startRun();

}

if(lastLat!=null){

const d=haversine(

lastLat,
lastLng,
c.latitude,
c.longitude

);

if(d>1&&d<40){

totalDistance+=d;

distanceEl.textContent=totalDistance.toFixed(1)+" m";

if(running){

const sec=(performance.now()-startTime)/1000;

checkDistance(sec);

}

}

}

lastLat=c.latitude;
lastLng=c.longitude;

}

//=============================
// HISTORY
//=============================

const historyList=document.getElementById("historyList");

let historyData=[];

function saveHistory(){

const now=new Date();

historyData.unshift({

date:now.toLocaleDateString(),

time:now.toLocaleTimeString(),

m60:r60.textContent,

m100:r100.textContent,

m200:r200.textContent,

m400:r400.textContent,

m500:r500.textContent,

top:topSpeedEl.textContent,

distance:distanceEl.textContent

});

localStorage.setItem(

"raceboxHistory",

JSON.stringify(historyData)

);

renderHistory();

}

function renderHistory(){

historyData=

JSON.parse(

localStorage.getItem("raceboxHistory")

)||[];

historyList.innerHTML="";

if(historyData.length==0){

historyList.innerHTML="<p>Belum ada data.</p>";

return;

}

historyData.forEach((item,index)=>{

historyList.innerHTML+=`

<div class="history-item">

<b>#${index+1}</b><br>

📅 ${item.date}<br>

🕒 ${item.time}<br><br>

60 m : ${item.m60}<br>

100 m : ${item.m100}<br>

200 m : ${item.m200}<br>

400 m : ${item.m400}<br>

500 m : ${item.m500}<br><br>

🚀 ${item.top}<br>

📍 ${item.distance}

</div>

`;

});

}

renderHistory();