import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = int(os.environ.get("PORT", 8080))

HTML = r'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Toll Plaza Management System</title>
<style>
*{box-sizing:border-box}
:root{--bg:#06152d;--panel:#08264a;--line:#145080;--text:#eaf4ff;--muted:#a9c3df}
body{margin:0;background:var(--bg);color:var(--text);font:14px Arial,sans-serif}
header{height:68px;background:#06234a;border-bottom:1px solid #174d7d;display:flex;align-items:center;justify-content:space-between;padding:0 22px;gap:15px}
.brand{display:flex;align-items:center;gap:14px}.logo{font-size:36px;color:#dceeff}
h1{font-size:21px;margin:0;font-weight:600}.subtitle{font-size:12px;color:#c3d8ee;margin-top:5px}
.topright{display:flex;align-items:center;gap:22px;white-space:nowrap}
.online{color:#42efa0}.topitem{border-left:1px solid #24496e;padding-left:20px}
.app{display:grid;grid-template-columns:235px minmax(0,1fr);min-height:calc(100vh - 68px)}
aside{background:#061c38;border-right:1px solid #17436b;padding:18px 10px;display:flex;flex-direction:column}
.nav{padding:13px 14px;border-radius:5px;margin-bottom:5px;color:#d8e9fa;display:flex;gap:13px;align-items:center}
.nav.active{background:#087fc4;border-left:4px solid #80d9ff}.nav .ico{font-size:20px;width:25px}
.sys{margin-top:auto;border:1px solid #17466f;border-radius:6px;padding:13px}
.sys h3{font-size:14px;margin:0 0 13px}.sysrow{display:flex;justify-content:space-between;gap:5px;font-size:12px;margin:12px 0;color:#c4d8ee}
.ok{color:#4ff1a2}.version{margin:25px 10px 4px;color:#b4c7dc;font-size:12px}
main{min-width:0;padding:18px 20px}
.stats{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:13px;margin-bottom:16px}
.stat{height:117px;border:1px solid #1671b1;border-radius:6px;background:#07386c;display:flex;align-items:center;padding:14px;gap:13px;min-width:0}
.stat:nth-child(2){background:#00634f;border-color:#098f70}.stat:nth-child(3){background:#6b1735;border-color:#a8324b}
.stat:nth-child(4){background:#3d208a;border-color:#6745bc}.stat:nth-child(5){background:#005c70;border-color:#087f9c}
.staticon{width:49px;height:49px;flex-shrink:0;border-radius:50%;background:#e5f5ff;color:#0783bd;display:grid;place-items:center;font-size:27px}
.stat:nth-child(2) .staticon{color:#008b65}.stat:nth-child(3) .staticon{color:#e12b42}
.stat:nth-child(4) .staticon{color:#7048d8}.stat:nth-child(5) .staticon{color:#008ba4}
.statlabel{font-size:14px;white-space:nowrap}.statnum{font-size:27px;font-weight:bold;margin:6px 0 4px;white-space:nowrap}
.statfoot{font-size:12px;color:#d6e8f7;white-space:nowrap}.up{color:#50ffad}
.plaza{border:1px solid #1b5d8b;border-radius:6px;background:#102d48;padding:3px;margin-bottom:15px}
.plazatitle{text-align:center;background:#0755a2;border:1px solid #2485ca;padding:6px;font-weight:bold;font-size:17px;letter-spacing:1px}
.lanes{display:grid;grid-template-columns:repeat(8,minmax(0,1fr));gap:5px;padding:5px}
.lane{min-width:0;background:#0a2a49;border:1px solid #315a78;border-radius:4px;overflow:hidden}
.lanehead{text-align:center;background:#102e4e;padding:8px 2px 5px;font-size:14px;font-weight:bold}
.gatebadge{display:block;margin:6px auto 0;width:62%;padding:5px 0;border-radius:4px;color:#fff;font-size:11px;background:#05a965}
.gatebadge.closed{background:#e32f37}
.road{height:177px;position:relative;overflow:hidden;background:linear-gradient(#82b5d2 0%,#b8d6e4 45%,#49535a 46%,#303b43 100%);border-top:3px solid #bacbd5;border-bottom:3px solid #d5dce1}
.skyline{position:absolute;bottom:49px;left:0;width:100%;height:36px;background:linear-gradient(160deg,transparent 30%,#47794d 31% 45%,transparent 46%),linear-gradient(20deg,transparent 25%,#528451 26% 48%,transparent 49%)}
.roadmark{position:absolute;left:0;right:0;bottom:27px;border-top:2px dashed #eee}
.roadarrow{position:absolute;left:4px;top:5px;color:#fff;font-size:18px;text-shadow:0 1px 2px #333}
.tollbooth{position:absolute;right:4px;top:53px;width:25px;height:60px;background:#163c5b;border:2px solid #9ab8cc}
.tollbooth:before{content:"";position:absolute;top:10px;left:3px;right:3px;height:15px;background:#6e9db8}
.camera{position:absolute;top:38px;left:12px;font-size:13px;color:#12283b}
.barrier{position:absolute;right:19%;top:78px;width:55px;height:6px;background:repeating-linear-gradient(90deg,#f33 0 9px,#fff 9px 18px);border:1px solid #eee;border-radius:2px;transform-origin:right center;transform:rotate(0);z-index:5;transition:transform .5s}
.barrier.open{transform:rotate(85deg)}
.car{
 position:absolute;
 left:-30%;
 bottom:20px;
 font-size:75px;
 z-index:4;
 line-height:1;
 transform:scaleX(-1);
}
.car.approach{
 animation:approach 3s linear forwards;
}
.car.pass{
 animation:pass 2.7s linear forwards;
}
@keyframes approach{
 from{left:-30%}
 to{left:43%}
}
@keyframes pass{
 from{left:43%}
 to{left:120%}
}
.light{
 position:absolute;
 right:3px;
 top:119px;
 background:#111b25;
 border:1px solid #8795a2;
 border-radius:4px;
 padding:3px;
 display:flex;
 gap:3px;
 z-index:6;
}
.bulb{
 width:8px;
 height:8px;
 border-radius:50%;
 background:#3c454e;
}
.bulb.red.on{
 background:#ff3030;
 box-shadow:0 0 6px red;
}
.bulb.green.on{
 background:#18ef75;
 box-shadow:0 0 6px #18ef75;
}
.lanedata{padding:9px 5px;background:#0b2b4b;text-align:center;min-height:115px}

.ufd{margin-top:9px;padding:8px 5px;background:#020b13;border:1px solid #24c9a0;border-radius:5px;color:#5dffca;text-align:center;font-family:monospace}
.ufd-title{font-size:10px;letter-spacing:1px;color:#8bb5c8}
.ufd-class{font-size:13px;font-weight:bold;margin:5px 0}
.ufd-amount{font-size:20px;font-weight:bold;color:#fff}
.ufd-status{font-size:11px;margin-top:4px;color:#54ff9a}

.plate{font-family:monospace;font-size:clamp(11px,1vw,14px);font-weight:bold;margin:2px 0 7px;overflow-wrap:anywhere}
.detail{font-size:12px;margin:5px 0;color:#e0edfa}.amount{font-size:14px;font-weight:bold;color:#42f2a1;margin-top:8px}
.bottom{display:grid;grid-template-columns:1.35fr 1fr 1.25fr;gap:13px}
.panel{border:1px solid #18517c;border-radius:6px;background:#082747;overflow:hidden;min-width:0}
.panelhead{padding:13px 14px;border-bottom:1px solid #20567e;display:flex;justify-content:space-between;font-size:15px;font-weight:bold}
.panelhead span{font-size:12px;color:#70caff;font-weight:normal}
table{border-collapse:collapse;width:100%;font-size:11px}
th,td{text-align:left;padding:9px 7px;border-bottom:1px solid #163d60;white-space:nowrap}
th{background:#0b3156;color:#c6dcf0;font-weight:normal}
tr:nth-child(even){background:#0b2e50}
.status{background:#078c63;padding:4px 7px;border-radius:3px;color:#fff}
.status.denied{background:#d52f3b}
.paycontent{padding:15px}
.payrow{display:flex;align-items:center;gap:18px;justify-content:center;padding:4px 0 13px}
.donut{width:118px;height:118px;border-radius:50%;background:conic-gradient(#19cf83 0 97.2%,#ffbd24 97.2% 98.2%,#f43e3e 98.2% 100%);display:grid;place-items:center;flex-shrink:0}
.donutinner{background:#092747;width:79px;height:79px;border-radius:50%;display:grid;place-content:center;text-align:center;font-size:12px}
.donutinner b{font-size:19px}.legend{font-size:12px;line-height:2.2}
.dot{display:inline-block;width:11px;height:11px;border-radius:50%;margin-right:8px}
.distribution{border-top:1px solid #1b5077;padding-top:12px}
.distribution h4{margin:0 0 10px;font-size:13px}
.barline{display:grid;grid-template-columns:80px 1fr 29px;gap:7px;align-items:center;font-size:11px;margin:11px 0}
.track{height:11px;background:#173d5f;border-radius:3px;overflow:hidden}.fill{height:100%;background:#08a8e8;border-radius:3px}
.fill.f2{background:#27c989}.fill.f3{background:#e9a91c}.fill.f4{background:#8246e8}
.event{display:grid;grid-template-columns:52px 32px 1fr 1.2fr;gap:5px;padding:11px 9px;border-bottom:1px solid #153d60;font-size:11px;align-items:center}
.event:nth-child(even){background:#0b2e50}
.eventhead{background:#0b3156;color:#c6dcf0}
.bullet{color:#3deca4;font-size:16px}
@media(max-width:1400px){.app{grid-template-columns:190px minmax(0,1fr)}main{padding:12px}.stats{grid-template-columns:repeat(3,minmax(0,1fr))}.lanes{grid-template-columns:repeat(4,minmax(0,1fr))}.bottom{grid-template-columns:1fr 1fr}.panel:last-child{grid-column:1/-1}}
@media(max-width:850px){.app{grid-template-columns:1fr}aside{display:none}.topright{font-size:11px;gap:8px}.topitem{padding-left:8px}.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.bottom{grid-template-columns:1fr}.panel:last-child{grid-column:auto}}
@media(max-width:500px){header{padding:10px;height:auto;align-items:flex-start}.topright{display:none}h1{font-size:16px}.stats{grid-template-columns:1fr 1fr}.stat{padding:8px;gap:7px;height:100px}.staticon{width:32px;height:32px;font-size:18px}.statnum{font-size:19px}.statlabel{font-size:11px}.lanes{grid-template-columns:repeat(2,minmax(0,1fr))}.event{font-size:10px}}

/* Enlarged Traffic Light and UFD Display */
.light {
    padding: 6px !important;
    gap: 6px !important;
    border-radius: 7px !important;
}
.bulb {
    width: 16px !important;
    height: 16px !important;
}
.bulb.red.on,
.bulb.green.on {
    box-shadow: 0 0 10px currentColor !important;
}
.ufd {
    padding: 12px 8px !important;
    margin-top: 12px !important;
}
.ufd-title {
    font-size: 13px !important;
}
.ufd-class {
    font-size: 18px !important;
}
.ufd-amount {
    font-size: 25px !important;
}
.ufd-status {
    font-size: 14px !important;
}

</style>
</head>
<body>
<header>
 <div class="brand"><div class="logo">â™œ</div><div><h1>Toll Plaza Management System</h1><div class="subtitle">8 Lane | FASTag | AVC | ANPR | Real-time Monitoring</div></div></div>
 <div class="topright"><span class="online">â— System Online</span><span class="topitem">28-06-2025&nbsp; 10:24 AM</span><span class="topitem" id="user-label">â™Ÿ Guest</span><button id="login-btn" class="topitem" style="background:#087fc4;color:white;border:0;padding:9px 14px;border-radius:4px;cursor:pointer">Login</button><button id="logout-btn" class="topitem" style="background:#8d2636;color:white;border:0;padding:9px 14px;border-radius:4px;cursor:pointer">Logout</button></div>
</header>
<div class="app">
<aside>
 <div class="nav active"><span class="ico">âŒ‚</span>Dashboard</div>
 <div class="nav"><span class="ico">ðŸš¦</span>Lane Monitoring</div>
 <div class="nav"><span class="ico">â–¤</span>Transactions</div>
 <div class="nav"><span class="ico">â—†</span>FASTag Management</div>
 <div class="nav"><span class="ico">â–£</span>AVC &amp; ANPR</div>
 <div class="nav"><span class="ico">ðŸš˜</span>AVCC</div>
 <div class="nav"><span class="ico">â–¥</span>Reports</div>
 <div class="nav"><span class="ico">âš™</span>Devices</div>
 <div class="nav"><span class="ico">âš™</span>Settings</div>
 <div class="nav"><span class="ico">ðŸ‘¤</span>User Management</div>
 <div class="nav"><span class="ico">ðŸ–¥</span>UFD Display</div>
 <div class="sys"><h3>System Status</h3>
  <div class="sysrow"><span>ðŸŸ¢ API Server</span><span class="ok">Connected</span></div>
  <div class="sysrow"><span>ðŸŸ¢ MySQL Database</span><span class="ok">Connected</span></div>
  <div class="sysrow"><span>ðŸŸ¢ Camera (ANPR)</span><span class="ok">Online</span></div>
  <div class="sysrow"><span>ðŸŸ¢ AVC System</span><span class="ok">Online</span></div>
  <div class="sysrow"><span>ðŸŸ¢ Lane Controllers</span><span class="ok">Online</span></div>
  <div class="sysrow"><span>ðŸŸ¢ Network</span><span class="ok">OK</span></div>
 </div>
 <div class="version">Toll Plaza v1.0<br><br>Created by<br><b>Vivek Yadav</b></div>
</aside>
<main>
 <div class="stats">
  <div class="stat"><div class="staticon">ðŸš˜</div><div><div class="statlabel">Total Vehicles</div><div class="statnum" id="kpi-total">1,248</div><div class="statfoot"><span class="up">â†‘ 12%</span> (vs yesterday)</div></div></div>
  <div class="stat"><div class="staticon">âœ“</div><div><div class="statlabel">Approved</div><div class="statnum" id="kpi-approved">1,213</div><div class="statfoot"><span class="up">â†‘ 14%</span> (vs yesterday)</div></div></div>
  <div class="stat"><div class="staticon">âœ•</div><div><div class="statlabel">Declined</div><div class="statnum" id="kpi-declined">35</div><div class="statfoot">â†“ 8% (vs yesterday)</div></div></div>
  <div class="stat"><div class="staticon">â‚¹</div><div><div class="statlabel">Total Toll Revenue</div><div class="statnum" id="kpi-revenue">â‚¹ 3,74,650</div><div class="statfoot"><span class="up">â†‘ 16%</span> (vs yesterday)</div></div></div>
  <div class="stat"><div class="staticon">ðŸ›£</div><div><div class="statlabel">Active Lanes</div><div class="statnum">8 / 8</div><div class="statfoot">All Lanes Operational</div></div></div>
 </div>
 <section class="plaza">
  <div class="plazatitle">TOLL PLAZA - 8 LANE</div>
  <div class="lanes" id="lanes"></div>
 </section>
 <div class="bottom">
  <section class="panel"><div class="panelhead">Recent Transactions <span>View All</span></div>
   <table><thead><tr><th>#</th><th>Time</th><th>Lane</th><th>Vehicle No.</th><th>Class</th><th>Amount</th><th>Status</th></tr></thead>
   <tbody>
   <tr><td>1</td><td>10:23:45</td><td>3</td><td>HR26DK9012</td><td>1</td><td>â‚¹80</td><td><span class="status">Approved</span></td></tr>
   <tr><td>2</td><td>10:22:31</td><td>2</td><td>DL8CA5678</td><td>2</td><td>â‚¹120</td><td><span class="status">Approved</span></td></tr>
   <tr><td>3</td><td>10:21:17</td><td>7</td><td>UP32KL1122</td><td>1</td><td>â‚¹80</td><td><span class="status">Approved</span></td></tr>
   <tr><td>4</td><td>10:19:56</td><td>1</td><td>UP16AB1234</td><td>1</td><td>â‚¹80</td><td><span class="status">Approved</span></td></tr>
   <tr><td>5</td><td>10:18:40</td><td>5</td><td>RJ14GD7890</td><td>4</td><td>â‚¹570</td><td><span class="status">Approved</span></td></tr>
   <tr><td>6</td><td>10:17:22</td><td>8</td><td>MH12AB3456</td><td>2</td><td>â‚¹120</td><td><span class="status">Approved</span></td></tr>
   <tr><td>7</td><td>10:15:03</td><td>4</td><td>PB10EF3456</td><td>3</td><td>â‚¹320</td><td><span class="status">Approved</span></td></tr>
   <tr><td>8</td><td>10:13:17</td><td>6</td><td>--</td><td>--</td><td>â‚¹0</td><td><span class="status denied">Declined</span></td></tr>
   </tbody></table>
  </section>
  <section class="panel"><div class="panelhead">FASTag / Payment Status</div>
   <div class="paycontent"><div class="payrow"><div class="donut"><div class="donutinner"><b>1,248</b>Total</div></div>
   <div class="legend"><div><i class="dot" style="background:#19cf83"></i>Successful&nbsp; 1,213 (97.2%)</div>
   <div><i class="dot" style="background:#ffbd24"></i>Pending&nbsp; 12 (1.0%)</div>
   <div><i class="dot" style="background:#f43e3e"></i>Failed&nbsp; 23 (1.8%)</div></div></div>
   <div class="distribution"><h4>Vehicle Class Distribution</h4>
    <div class="barline"><span>Class 1 (Car)</span><div class="track"><div class="fill" style="width:62%"></div></div><span>62%</span></div>
    <div class="barline"><span>Class 2 (LCV)</span><div class="track"><div class="fill f2" style="width:18%"></div></div><span>18%</span></div>
    <div class="barline"><span>Class 3 (Bus)</span><div class="track"><div class="fill f3" style="width:8%"></div></div><span>8%</span></div>
    <div class="barline"><span>Class 4 (Truck)</span><div class="track"><div class="fill f4" style="width:12%"></div></div><span>12%</span></div>
   </div></div>
  </section>
  <section class="panel"><div class="panelhead">Recent Events / Alerts <span>View All</span></div>
   <div class="event eventhead"><span>Time</span><span>Lane</span><span>Event</span><span>Details</span></div>
   <div class="event"><span>10:23</span><span>3</span><span>â— Payment Success</span><span>FASTag: ******1234</span></div>
   <div class="event"><span>10:22</span><span>2</span><span>â— Vehicle Detected</span><span>DL8CA5678 (Class 2)</span></div>
   <div class="event"><span>10:21</span><span>6</span><span>â— Lane Closed</span><span>Maintenance Mode</span></div>
   <div class="event"><span>10:17</span><span>7</span><span>â— Payment Success</span><span>FASTag: ******1122</span></div>
   <div class="event"><span>10:15</span><span>1</span><span>â— ANPR Capture</span><span>UP16AB1234</span></div>
   <div class="event"><span>10:18</span><span>5</span><span>â— Payment Success</span><span>FASTag: ******7890</span></div>
   <div class="event"><span>10:17</span><span>8</span><span>â— Vehicle Detected</span><span>MH12AB3456 (Class 2)</span></div>
   <div class="event"><span>10:15</span><span>4</span><span>â— Payment Success</span><span>FASTag: ******3456</span></div>
  </section>
 </div>
</main>
</div>
<script>
const data=[
 {no:"UP16AB1234",cls:"Car (Class 1)",ax:2,amt:80,open:true,car:"ðŸš™"},
 {no:"DL8CA5678",cls:"LCV (Class 2)",ax:2,amt:120,open:true,car:"ðŸš™"},
 {no:"HR26DK9012",cls:"Car (Class 1)",ax:2,amt:80,open:true,car:"ðŸš—"},
 {no:"PB10EF3456",cls:"Bus (Class 3)",ax:2,amt:320,open:true,car:"ðŸšŒ"},
 {no:"RJ14GD7890",cls:"Truck (Class 4)",ax:4,amt:570,open:true,car:"ðŸšš"},
 {no:"--",cls:"No Vehicle",ax:"-",amt:0,open:false,car:""},
 {no:"UP32KL1122",cls:"Car (Class 1)",ax:2,amt:80,open:true,car:"ðŸš—"},
 {no:"MH12AB3456",cls:"LCV (Class 2)",ax:2,amt:120,open:true,car:"ðŸš™"}
];
data.forEach((d,i)=>{
 d.payMode = d.open ? ["FASTag","Cash","UPI","Card"][i%4] : "N/A";
});
data.forEach((d,i)=>{
 d.payMode = d.open ? ["FASTag","Cash","UPI","Card"][i%4] : "N/A";
});
const root=document.getElementById("lanes");
data.forEach((d,i)=>{
 const n=i+1;
 root.insertAdjacentHTML("beforeend",`
 <div class="lane">
  <div class="lanehead">LANE ${n}<span class="gatebadge ${d.open?"":"closed"}" id="gate${n}">${d.open?"OPEN":"CLOSED"}</span></div>
  <div class="road">
   <div class="skyline"></div><div class="roadarrow">â†’</div><div class="roadmark"></div>
   <div class="camera">ðŸ“¹</div><div class="tollbooth"></div>
   <div class="barrier ${d.open?"open":"closed"}" id="barrier${n}"></div>
   <div class="light"><span class="bulb red ${d.open?"":"on"}" id="red${n}"></span><span class="bulb green ${d.open?"on":""}" id="green${n}"></span></div>
   <div class="car" id="car${n}">${d.car}</div>
  </div>
  <div class="lanedata">
   <div class="plate">${d.no}</div><div class="detail">${d.cls}</div>
   <div class="detail">Axles: ${d.ax}</div><div class="amount">â‚¹ ${Number(d.amt).toFixed(2)}</div>
   <div class="ufd">
    <div class="ufd-title">USER FARE DISPLAY</div>
    <div class="ufd-class">${d.cls}</div>
    <div style="font-size:12px;margin:4px 0">Payment: ${d.payMode || "FASTag"}</div>
    <div class="ufd-amount">â‚¹ ${Number(d.amt).toFixed(2)}</div>
    <div class="ufd-status">${d.open?"PAYMENT APPROVED":"LANE CLOSED"}</div>
   </div>
  </div>
 </div>`);
});

/* DEMO KPI UPDATE */
let demoTotal = 1248;
let demoApproved = 1213;
let demoDeclined = 35;
let demoRevenue = 374650;

function recordDemoVehicle(vehicle) {
  demoTotal++;
  demoApproved++;
  demoRevenue += Number(vehicle.amt || 0);

  const totalEl = document.getElementById("kpi-total");
  const approvedEl = document.getElementById("kpi-approved");
  const declinedEl = document.getElementById("kpi-declined");
  const revenueEl = document.getElementById("kpi-revenue");

  if (totalEl) totalEl.textContent = demoTotal.toLocaleString("en-IN");
  if (approvedEl) approvedEl.textContent = demoApproved.toLocaleString("en-IN");
  if (declinedEl) declinedEl.textContent = demoDeclined.toLocaleString("en-IN");
  if (revenueEl) revenueEl.textContent =
    "â‚¹ " + demoRevenue.toLocaleString("en-IN");
}

/* Continuous demo cycle: lane 6 remains closed. */
data.forEach((d,i)=>{
 if(!d.open)return;

 const laneNo=i+1;
 const car=document.getElementById("car"+laneNo);
 const barrier=document.getElementById("barrier"+laneNo);
 const gate=document.getElementById("gate"+laneNo);
 const red=document.getElementById("red"+laneNo);
 const green=document.getElementById("green"+laneNo);

 function setGate(isOpen){
   barrier.classList.toggle("open",isOpen);
   gate.textContent=isOpen?"OPEN":"CLOSED";
   gate.classList.toggle("closed",!isOpen);
   red.classList.toggle("on",!isOpen);
   green.classList.toggle("on",isOpen);
 }

 function runCycle(){
   if(!document.body.contains(car))return;

   // Vehicle approaches the closed barrier
   car.style.left="-30%";
   car.classList.remove("pass");
   setGate(false);

   void car.offsetWidth;
   car.classList.add("approach");

   // Vehicle reaches barrier; open it and let vehicle pass
   setTimeout(()=>{
     car.classList.remove("approach");
     car.style.left="43%";
     setGate(true);

     void car.offsetWidth;
     car.classList.add("pass");

     // After vehicle passes, close barrier and repeat
     setTimeout(()=>{
       recordDemoVehicle(d);
       car.classList.remove("pass");
       car.style.left="-30%";
       setGate(false);
       setTimeout(runCycle,1200);
     },2800);
   },3000);
 }

 setTimeout(runCycle,i*450);
});

/* MENU_NAVIGATION_PATCH_START */
(function(){
 const main=document.querySelector("main");
 const navs=[...document.querySelectorAll("aside .nav")];
 if(!main || navs.length<8) return;

 const dashboardHTML=main.innerHTML;
 const pages={
 "Lane Monitoring":`
   <h2>ðŸš¦ Lane Monitoring</h2>
   <p>8-lane live demo monitoring. Lane 6 is in maintenance mode.</p>
   <div class="panel" style="padding:18px">
   <h3>Lane Status</h3>
   <table><thead><tr><th>Lane</th><th>Vehicle</th><th>Status</th><th>Control</th></tr></thead>
   <tbody>${Array.from({length:8},(_,i)=>`<tr><td>Lane ${i+1}</td><td>${i===5?"--":"Demo vehicle"}</td><td>${i===5?"Maintenance":"Monitoring"}</td><td><button data-lane="${i+1}" class="lane-toggle">${i===5?"Enable":"Disable"}</button></td></tr>`).join("")}</tbody></table>
   </div>`,
 "Transactions":`
   <h2>â–¤ Transactions</h2><div class="panel" style="padding:16px">
   <input id="txsearch" placeholder="Search vehicle number..." style="padding:10px;width:min(100%,360px);margin-bottom:12px">
   <div style="overflow:auto"><table id="txtable"><thead><tr><th>#</th><th>Time</th><th>Lane</th><th>Vehicle No.</th><th>Class</th><th>Amount</th><th>Status</th></tr></thead>
   <tbody>${[...document.querySelectorAll(".bottom tbody tr")].map(r=>r.outerHTML).join("")}</tbody></table></div></div>`,
 "FASTag Management":`
   <h2>â—† FASTag Management</h2><div class="panel" style="padding:18px">
   <p>Demo FASTag lookup</p><label>Vehicle / FASTag number</label><br>
   <input id="taginput" placeholder="Enter vehicle or tag number" style="padding:10px;margin:10px 0;width:min(100%,360px)">
   <button id="tagcheck">Check Tag</button><p id="tagresult">Enter a number to check the demo record.</p>
   <hr><p>Successful: 1,213 | Pending: 12 | Failed: 23</p></div>`,
 "AVC & ANPR":`
   <h2>â–£ AVC & ANPR</h2><div class="panel" style="padding:18px">
   <p>Demo vehicle classification and number-plate recognition.</p>
   <label>Lane</label> <select id="anprlane">${Array.from({length:8},(_,i)=>`<option>${i+1}</option>`).join("")}</select>
   <label>Vehicle class</label><select id="anprclass"><option>Car (Class 1)</option><option>LCV (Class 2)</option><option>Bus (Class 3)</option><option>Truck (Class 4)</option></select>
   <label>Vehicle number</label><input id="anprno" value="UP16AB1234">
   <br><label>Mode of Payment</label>
   <select id="anprpayment">
    <option>FASTag</option><option>Cash</option><option>UPI</option><option>Card</option>
   </select>
   <button id="anprsave">Simulate Detection</button><p id="anprresult"></p></div>`,
 "Reports":`
   <h2>â–¥ Reports</h2><div class="panel" style="padding:18px">
   <p>Demo summary based on the dashboard figures.</p>
   <p>Total Vehicles: <b>1,248</b></p><p>Approved: <b>1,213</b></p>
   <p>Declined: <b>35</b></p><p>Total Revenue: <b>â‚¹ 3,74,650</b></p>
   <button id="downloadreport">Download CSV Report</button></div>`,
 "Devices":`
   <h2>âš™ Devices</h2><div class="panel" style="padding:18px">
   <table><thead><tr><th>Device</th><th>Status</th><th>Action</th></tr></thead><tbody>
   ${["API Server","MySQL Database","ANPR Camera","AVC System","AVCC Device","Lane Controllers","Network"].map(x=>`<tr><td>${x}</td><td><span class="status">Demo Online</span></td><td><button class="device-check">Check</button></td></tr>`).join("")}
   </tbody></table><p id="device-result"></p></div>`,
 "User Management":`
   <h2>ðŸ‘¤ User Management</h2>
   <div class="panel" style="padding:18px">
    <h3>Add New User</h3>
    <form id="userform">
     <label>Full Name</label><br>
     <input id="newname" required placeholder="Enter full name" style="padding:10px;margin:7px 0;width:min(100%,360px)"><br>
     <label>Username</label><br>
     <input id="newusername" required placeholder="Enter username" style="padding:10px;margin:7px 0;width:min(100%,360px)"><br>
     <label>Role</label><br>
     <select id="newrole" style="padding:10px;margin:7px 0">
      <option>Operator</option><option>Supervisor</option><option>Administrator</option>
     </select><br>
     <label>Password (demo only)</label><br>
     <input id="newpassword" type="password" required placeholder="Enter password" style="padding:10px;margin:7px 0;width:min(100%,360px)"><br>
     <button type="submit" style="padding:10px 16px;margin-top:8px">Add User</button>
    </form>
    <p id="userresult"></p>
    <h3>Users</h3>
    <div style="overflow:auto"><table id="usertable">
     <thead><tr><th>Name</th><th>Username</th><th>Role</th><th>Action</th></tr></thead>
     <tbody><tr><td>Admin</td><td>admin</td><td>Administrator</td><td>Default demo user</td></tr></tbody>
    </table></div>
    <p style="color:#ffcf76">Demo only: users are not saved to a database. Do not use real passwords here.</p>
   </div>`,
 "UFD Display":`
   <h2>ðŸ–¥ User Fare Display (UFD)</h2>
   <p>Lane-wise demo fare information shown to the vehicle driver.</p>
   <div class="panel" style="padding:16px;overflow:auto">
    <table><thead><tr><th>Lane</th><th>Vehicle Class</th><th>Axles</th><th>Toll Fare</th><th>Payment Mode</th><th>UFD Status</th></tr></thead>
    <tbody>${data.map((d,i)=>`<tr><td>Lane ${i+1}</td><td>${d.cls}</td><td>${d.ax}</td><td>â‚¹ ${Number(d.amt).toFixed(2)}</td><td>${d.payMode || "FASTag"}</td><td>${d.open?"Demo: Approved":"Lane Closed"}</td></tr>`).join("")}</tbody></table>
   </div>
   <p style="color:#ffcf76">This is a software preview. Physical UFD hardware is not connected.</p>`,
 "AVCC":`
   <h2>ðŸš˜ AVCC - Automatic Vehicle Classification</h2>
   <p>Lane-wise vehicle classification demo.</p>
   <div class="panel" style="padding:16px;overflow:auto">
    <table><thead><tr><th>Lane</th><th>Vehicle Number</th><th>Classification</th><th>Axles</th><th>Fare</th><th>Status</th></tr></thead>
    <tbody>${data.map((d,i)=>`<tr><td>Lane ${i+1}</td><td id="avcc-plate-${i+1}">${d.no}</td><td>${d.cls}</td><td>${d.ax}</td><td>â‚¹ ${Number(d.amt).toFixed(2)}</td><td id="avcc-status-${i+1}">${d.open?"Demo: Classified":"Lane Closed"}</td></tr>`).join("")}</tbody></table>
   </div>
   <p style="color:#ffcf76">AVCC hardware se live data abhi connected nahi hai.</p>`,
 "Settings":`
   <h2>âš™ Settings</h2><div class="panel" style="padding:18px">
   <label>Plaza Name</label><br><input id="plazaname" value="TOLL PLAZA" style="padding:9px;margin:8px 0">
   <br><label>Demo cycle speed</label><br><select id="cyclespeed"><option value="normal">Normal</option><option value="fast">Fast</option></select>
   <br><button id="savesettings" style="margin-top:12px">Save Settings</button><p id="settingresult"></p></div>`
 };

 function showPage(name){
   navs.forEach(n=>n.classList.toggle("active",n.textContent.trim().replace(/\s+/g," ").includes(name)));
   if(name==="Dashboard"){main.innerHTML=dashboardHTML;return;}
   main.innerHTML=pages[name]||dashboardHTML;
   if(name==="Transactions"){
     const inp=document.getElementById("txsearch");
     inp.oninput=()=>[...document.querySelectorAll("#txtable tbody tr")].forEach(r=>r.style.display=r.textContent.toLowerCase().includes(inp.value.toLowerCase())?"":"none");
   }
   if(name==="FASTag Management"){
     document.getElementById("tagcheck").onclick=()=>{
       const v=document.getElementById("taginput").value.trim();
       document.getElementById("tagresult").textContent=v?(v.toUpperCase().includes("BAD")?"Demo status: Failed":"Demo status: Tag record found (simulated)"):"Please enter a number.";
     };
   }
   if(name==="AVC & ANPR"){
     document.getElementById("anprsave").onclick=()=>{
       const no=document.getElementById("anprno").value.trim().toUpperCase();
       document.getElementById("anprresult").textContent=no?`Demo detection: Lane ${document.getElementById("anprlane").value} | ${no} | ${document.getElementById("anprclass").value} | Payment: ${document.getElementById("anprpayment").value}`:"Enter a vehicle number.";
     };
   }
   if(name==="AVCC"){
     let tick=0;
     const timer=setInterval(()=>{
       const table=document.getElementById("avcc-status-1");
       if(!table){
         clearInterval(timer);
         return;
       }
       tick++;
       data.forEach((d,i)=>{
         const lane=i+1;
         const status=document.getElementById("avcc-status-"+lane);
         const plate=document.getElementById("avcc-plate-"+lane);
         const barrier=document.getElementById("barrier"+lane);

         if(!status)return;
         if(!d.open){
           status.textContent="Lane Closed / Maintenance";
         } else if(barrier && barrier.classList.contains("open")){
           status.textContent="Vehicle Passing | Demo";
         } else if(tick%3===0){
           status.textContent="Vehicle Detected | Demo";
         } else if(tick%3===1){
           status.textContent="AVCC Classifying | Demo";
         } else {
           status.textContent="Waiting for Vehicle";
         }

         if(plate && d.no==="--" && d.open){
           plate.textContent="DEMO-"+String(1000+lane+tick).slice(-4);
         }
       });
     },1000);
   }
   if(name==="Reports"){
     document.getElementById("downloadreport").onclick=()=>{
       const csv="Metric,Value\nTotal Vehicles,1248\nApproved,1213\nDeclined,35\nTotal Toll Revenue,374650\n";
       const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([csv],{type:"text/csv"}));a.download="toll-report.csv";a.click();URL.revokeObjectURL(a.href);
     };
   }
   if(name==="Devices"){
     document.querySelectorAll(".device-check").forEach(b=>b.onclick=()=>document.getElementById("device-result").textContent="Demo status only â€” real device connectivity is not configured.");
   }
   if(name==="User Management"){
     const form=document.getElementById("userform");
     form.onsubmit=(e)=>{
       e.preventDefault();
       const nameValue=document.getElementById("newname").value.trim();
       const username=document.getElementById("newusername").value.trim();
       const role=document.getElementById("newrole").value;
       const password=document.getElementById("newpassword").value;
       if(!nameValue||!username||!password)return;
       const tbody=document.querySelector("#usertable tbody");
       if([...tbody.rows].some(r=>r.cells[1].textContent.toLowerCase()===username.toLowerCase())){
         document.getElementById("userresult").textContent="Username already exists.";
         return;
       }
       const row=tbody.insertRow();
       [nameValue,username,role].forEach(v=>row.insertCell().textContent=v);
       row.insertCell().textContent="Added (demo)";
       document.getElementById("userresult").textContent="User added in this page (demo only).";
       form.reset();
     };
   }
   if(name==="Settings"){
     document.getElementById("savesettings").onclick=()=>{
       const title=document.getElementById("plazaname").value.trim()||"TOLL PLAZA";
       document.querySelector(".plazatitle")?.replaceChildren(document.createTextNode(title+" - 8 LANE"));
       document.getElementById("settingresult").textContent="Settings applied to this page.";
     };
   }
   if(name==="Lane Monitoring"){
     document.querySelectorAll(".lane-toggle").forEach(b=>b.onclick=()=>{
       const row=b.closest("tr");
       const disabled=b.textContent==="Disable";
       b.textContent=disabled?"Enable":"Disable";
       row.cells[2].textContent=disabled?"Disabled (demo)":"Monitoring (demo)";
     });
   }
 }

 navs.forEach(n=>{
   n.style.cursor="pointer";
   n.onclick=()=>{
     const t=n.textContent.trim().replace(/\s+/g," ");
     const name=["Dashboard","Lane Monitoring","Transactions","FASTag Management","AVC & ANPR","AVCC","Reports","Devices","Settings","User Management","UFD Display"].find(x=>t.includes(x));
     if(name)showPage(name);
   };
 });
})();
/* MENU_NAVIGATION_PATCH_END */


/* DEMO LOGIN / LOGOUT */
(function(){
 const loginBtn=document.getElementById("login-btn");
 const logoutBtn=document.getElementById("logout-btn");
 const label=document.getElementById("user-label");
 if(!loginBtn || !logoutBtn || !label) return;

 loginBtn.onclick=()=>{
   const username=prompt("Demo Login - Username:");
   if(username===null)return;
   const password=prompt("Password:");
   if(password===null)return;

   if(username.trim()==="admin" && password==="admin123"){
     label.textContent="â™Ÿ Admin";
     alert("Demo login successful. Welcome, Vivek Yadav!");
   } else {
     alert("Invalid demo credentials.");
   }
 };

 logoutBtn.onclick=()=>{
   label.textContent="â™Ÿ Guest";
   alert("Logged out from demo display.");
 };
})();

</script>
</body>
</html>'''

from http.server import BaseHTTPRequestHandler, HTTPServer
from http import cookies
import secrets
import urllib.parse

PORT = int(os.environ.get("PORT", 8080))

USERNAME = "admin"
PASSWORD = "admin123"

SESSIONS = set()

LOGIN_HTML = r'''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Toll Plaza Login</title>
<style>
*{box-sizing:border-box}
body{
margin:0;
min-height:100vh;
display:flex;
align-items:center;
justify-content:center;
background:#06152d;
color:#eaf4ff;
font-family:Arial,sans-serif
}
.login-box{
width:min(420px,92%);
background:#082747;
border:1px solid #1671b1;
border-radius:10px;
padding:30px;
box-shadow:0 15px 50px rgba(0,0,0,.45)
}
.logo{text-align:center;font-size:48px;margin-bottom:8px}
h1{text-align:center;margin:0;font-size:22px}
.subtitle{text-align:center;color:#a9c3df;font-size:13px;margin:8px 0 25px}
label{display:block;margin:14px 0 6px;color:#cfe3f7}
input{
width:100%;
padding:12px;
border-radius:5px;
border:1px solid #28638e;
background:#061a32;
color:white;
outline:none
}
button{
width:100%;
margin-top:20px;
padding:12px;
border:0;
border-radius:5px;
background:#087fc4;
color:white;
font-size:15px;
cursor:pointer
}
.error{
background:#6e1e2c;
border:1px solid #c83d50;
color:#ffd9de;
padding:10px;
border-radius:5px;
margin-bottom:15px;
text-align:center
}
.footer{text-align:center;color:#7997b5;font-size:11px;margin-top:20px}
</style>
</head>
<body>
<div class="login-box">
<div class="logo">♜</div>
<h1>Toll Plaza Management System</h1>
<div class="subtitle">Secure Administrator Login</div>
{ERROR}
<form method="POST" action="/login">
<label>Username</label>
<input type="text" name="username" autocomplete="username" required autofocus>
<label>Password</label>
<input type="password" name="password" autocomplete="current-password" required>
<button type="submit">Login</button>
</form>
<div class="footer">Toll Plaza v1.0</div>
</div>
</body>
</html>
'''

def make_session():
    token = secrets.token_urlsafe(32)
    SESSIONS.add(token)
    return token

def get_session(handler):
    header = handler.headers.get("Cookie", "")

    if not header:
        return None

    jar = cookies.SimpleCookie()

    try:
        jar.load(header)
    except:
        return None

    if "session" not in jar:
        return None

    token = jar["session"].value

    if token in SESSIONS:
        return token

    return None


class Handler(BaseHTTPRequestHandler):

    def send_html(self, body, status=200, headers=None):

        data = body.encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(data))
        )

        if headers:
            for key, value in headers:
                self.send_header(key, value)

        self.end_headers()
        self.wfile.write(data)

    def redirect(self, location, headers=None):

        self.send_response(302)
        self.send_header("Location", location)

        if headers:
            for key, value in headers:
                self.send_header(key, value)

        self.end_headers()

    def show_login(self, error=""):

        error_html = ""

        if error:
            safe = (
                error
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
            )

            error_html = f'<div class="error">{safe}</div>'

        page = LOGIN_HTML.replace(
            "{ERROR}",
            error_html
        )

        self.send_html(page)

    def do_GET(self):

        if self.path == "/logout":

            session = get_session(self)

            if session:
                SESSIONS.discard(session)

            self.redirect(
                "/",
                [
                    (
                        "Set-Cookie",
                        "session=deleted; "
                        "Path=/; "
                        "Max-Age=0; "
                        "HttpOnly; "
                        "SameSite=Lax"
                    )
                ]
            )

            return

        session = get_session(self)

        if not session:
            self.show_login()
            return

        if self.path in ("/", "/index.html"):

            self.send_html(HTML)

            return

        self.send_error(404)

    def do_POST(self):

        if self.path != "/login":
            self.send_error(404)
            return

        try:
            length = int(
                self.headers.get(
                    "Content-Length",
                    "0"
                )
            )

            raw = self.rfile.read(length)

            form = urllib.parse.parse_qs(
                raw.decode("utf-8")
            )

        except Exception:
            self.show_login("Invalid request.")
            return

        username = form.get(
            "username",
            [""]
        )[0].strip()

        password = form.get(
            "password",
            [""]
        )[0]

        if (
            secrets.compare_digest(
                username,
                USERNAME
            )
            and
            secrets.compare_digest(
                password,
                PASSWORD
            )
        ):

            session = make_session()

            self.redirect(
                "/",
                [
                    (
                        "Set-Cookie",
                        f"session={session}; "
                        "Path=/; "
                        "HttpOnly; "
                        "SameSite=Lax"
                    )
                ]
            )

            print(
                "[LOGIN] Successful:",
                self.client_address[0]
            )

        else:

            print(
                "[LOGIN] Failed:",
                self.client_address[0]
            )

            self.show_login(
                "Invalid username or password."
            )

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":

    print("=" * 60)
    print("TOLL PLAZA MANAGEMENT SYSTEM")
    print("=" * 60)
    print("Server   : http://0.0.0.0:")
    print("Username : admin")
    print("Password : admin123")
    print("=" * 60)

    HTTPServer(
        ("0.0.0.0", PORT),
        Handler
    ).serve_forever()






