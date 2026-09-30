from PIL import Image, ImageDraw, ImageFont
import math, os, subprocess, shutil
W,H,FPS,DUR=960,540,24,15
OUT="media"; os.makedirs(OUT,exist_ok=True)
MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"; BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
def F(n,b=False): return ImageFont.truetype(BOLD if b else MONO,n)
HEAD=F(25,1); SUB=F(13); T=F(15); B=F(13); S=F(10); XS=F(9)
BG=(7,11,14); GRID=(27,38,44); WHITE=(235,241,240); LIME=(214,255,69); CYAN=(104,225,209); RED=(255,105,105); MUTED=(135,150,155); PANEL=(13,20,24)
def e(x): x=max(0,min(1,x)); return x*x*(3-2*x)
def tx(d,p,s,f=B,c=WHITE,a=None): d.text(p,s,font=f,fill=c,anchor=a)
def rr(d,b,r=8,fill=PANEL,outline=(52,65,72),w=2): d.rounded_rectangle(b,r,fill=fill,outline=outline,width=w)
def ln(d,a,b,c=LIME,w=3): d.line([a,b],fill=c,width=w)
def ar(d,a,b,c=LIME,w=3):
    ln(d,a,b,c,w); q=math.atan2(b[1]-a[1],b[0]-a[0]); L=11
    d.polygon([b,(b[0]-L*math.cos(q-.5),b[1]-L*math.sin(q-.5)),(b[0]-L*math.cos(q+.5),b[1]-L*math.sin(q+.5))],fill=c)
def base(title,sub,t):
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    for x in range(0,W,60): ln(d,(x,0),(x,H),GRID,1)
    for y in range(0,H,60): ln(d,(0,y),(W,y),GRID,1)
    tx(d,(35,30),title,HEAD,LIME); tx(d,(35,58),sub,SUB,CYAN); tx(d,(925,32),f"{t:04.1f}s",SUB,MUTED,"ra"); rr(d,(30,90,930,505),12); return im,d
def video(name,fn):
    fr=f"/tmp/{name}_frames"; shutil.rmtree(fr,ignore_errors=True); os.makedirs(fr)
    for i in range(FPS*DUR): fn(i/FPS).save(f"{fr}/{i:04d}.png")
    out=f"{OUT}/{name}.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",f"{fr}/%04d.png","-c:v","libx264","-pix_fmt","yuv420p","-crf","22","-preset","fast","-movflags","+faststart",out],check=True)
    shutil.rmtree(fr)
def morphle(t):
    im,d=base("MORPHLE","MICROSCOPE → OPENCV → ERROR → PID → 3-AXIS GANTRY",t)
    rr(d,(55,135,245,300)); tx(d,(150,160),"MICROSCOPE",T,CYAN,"ma"); d.rectangle((85,185,215,265),outline=CYAN,width=2)
    cx=150+55*math.sin(t*.9) if t<4 else 150; cy=225+20*math.sin(t*1.2) if t<4 else 225; d.ellipse((cx-18,cy-18,cx+18,cy+18),outline=LIME,width=3)
    rr(d,(285,135,500,300)); tx(d,(392,160),"OpenCV",T,CYAN,"ma"); target=392+(35*(1-e((t-3)/3)) if 3<t<6 else (0 if t>=6 else 35)); d.rectangle((315,180,470,265),outline=(55,70,78),width=2); d.ellipse((target-20,200,target+20,240),outline=LIME,width=3); ln(d,(target-30,220),(target+30,220),LIME,2); ln(d,(target,190),(target,250),LIME,2)
    rr(d,(540,135,700,300)); tx(d,(620,160),"ERROR",T,CYAN,"ma"); ex=40 if t<6 else max(0,40*(1-e((t-6)/3))); d.ellipse((565,195,635,265),outline=(50,63,70),width=2); d.ellipse((630+ex-5,215,630+ex+5,225),fill=RED); ln(d,(600,230),(630+ex,220),RED,3); tx(d,(620,275),f"dx = {int(ex)} px",S,WHITE,"ma")
    rr(d,(735,135,905,300)); tx(d,(820,160),"PID",T,CYAN,"ma"); tx(d,(755,195),"P · error",B); tx(d,(755,220),"I · history",B); tx(d,(755,245),"D · rate",B)
    rr(d,(285,350,905,470)); tx(d,(595,375),"3-AXIS CARTESIAN STAGE",T,CYAN,"ma"); q=e((t-9)/4) if t>9 else 0; gx=500+85*q; ln(d,(330,420),(860,420),(60,75,82),8); d.rectangle((gx-35,392,gx+35,438),fill=(22,33,39),outline=LIME,width=2); tx(d,(gx,415),"X/Y/Z",S,WHITE,"mm"); tx(d,(55,495),"CAPTURE → CENTROID → dx/dy → PID → GANTRY MOVE → FEEDBACK",XS,MUTED); return im
def stm(t):
    im,d=base("STM32F401 USART1","WIRE → PERIPHERAL → ISR → RING BUFFER → CRC → APPLICATION",t)
    rr(d,(55,130,400,250)); tx(d,(75,150),"UART RX WIRE",T,CYAN); bits=[1,0,1,1,0,0,1,0,1,1,0,1]; pts=[]
    for j,b in enumerate(bits): x=75+j*25; y=205 if b else 180; pts += [(x,y),(x+25,y)]
    d.line(pts,fill=LIME,width=3); tx(d,(75,230),"START | DATA | STOP",S,MUTED)
    rr(d,(445,130,650,250)); tx(d,(547,155),"STM32F401",T,CYAN,"ma"); tx(d,(547,190),"USART1",F(20,1),WHITE,"ma"); tx(d,(547,220),"BRR · UE · RE · TE",S,MUTED,"ma"); ar(d,(400,205),(445,205))
    rr(d,(690,130,900,250)); tx(d,(795,155),"RX INTERRUPT",T,CYAN,"ma"); d.rectangle((715,185,875,220),outline=LIME,width=2); tx(d,(795,203),"RXNE → ISR → DR",S,WHITE,"mm")
    rr(d,(250,285,680,405)); tx(d,(465,310),"CIRCULAR RX BUFFER",T,CYAN,"ma"); ptr=min(7,max(0,int((t-4)*1.2)))
    for j in range(8):
        x=280+j*48; d.rectangle((x,335,x+38,370),fill=LIME if 4<t<9 and j<=ptr else (30,43,48),outline=(70,85,92))
        if j<=ptr: tx(d,(x+19,352),f"{0x41+j:02X}",S,(8,12,14),"mm")
    rr(d,(705,285,900,405)); tx(d,(802,310),"FRAME CHECK",T,CYAN,"ma"); tx(d,(802,345),"AA | LEN | DATA",S); tx(d,(802,370),"CRC-32 ✓",S,LIME)
    rr(d,(430,430,700,475)); tx(d,(565,453),"APPLICATION MESSAGE QUEUE",S,WHITE,"mm"); tx(d,(55,495),"BARE-METAL DATA PATH · NO HAL",XS,MUTED); return im
def pref(t):
    im,d=base("PreFRTOS","TELEMETRY → 500ms WINDOW → RF / XGBOOST → PREDICTION → WARNING",t)
    rr(d,(55,130,420,360)); tx(d,(75,152),"LIVE TELEMETRY",T,CYAN); d.rectangle((75,185,400,330),fill=(8,14,17),outline=(45,58,65)); vals=[.28,.32,.30,.35,.31,.39,.36,.42,.40,.46,.44,.51,.48,.55,.52,.60,.58,.68,.64,.76,.70,.86]; d.line([(85+j*14,315-v*105) for j,v in enumerate(vals)],fill=CYAN,width=3); q=e((t-2)/4) if t>2 else 0; wx=90+q*220; d.rectangle((wx,195,wx+115,320),outline=LIME,width=3); tx(d,(235,342),"10 samples = previous 500 ms",S,MUTED,"ma")
    rr(d,(470,130,700,300)); tx(d,(585,155),"MODEL",T,CYAN,"ma"); tx(d,(500,195),"Random Forest",B); tx(d,(500,225),"XGBoost",B); score=max(0,min(1,(t-7)/3)); d.rectangle((500,250,665,260),fill=(35,48,54)); d.rectangle((500,250,500+165*score,260),fill=LIME); tx(d,(585,278),f"P(failure) = {score:.2f}",S,MUTED,"ma")
    rr(d,(735,130,900,300)); tx(d,(817,155),"PREDICTION",T,CYAN,"ma"); p=.15 if t<9 else min(1,(t-9)/2); d.arc((760,175,875,290),-90,-90+360*p,fill=LIME,width=8); tx(d,(817,230),"WARNING" if p>.65 else "MONITORING",B,LIME if p>.65 else WHITE,"ma"); 
    if t>11: d.rectangle((735,330,900,385),fill=(45,18,18),outline=RED,width=2); tx(d,(817,350),"FAILURE EVENT",B,RED,"ma")
    rr(d,(470,330,700,385)); tx(d,(585,350),f"prediction timestamp {t:05.2f}s",S,WHITE,"ma"); tx(d,(55,495),"PREDICT BEFORE FAILURE · TIMESTAMPED WARNING",XS,MUTED); return im
def heap(t):
    im,d=base("CUSTOM HEAP ALLOCATOR","malloc → FIRST-FIT → SPLIT → free() → COALESCE",t); rr(d,(65,135,895,230)); tx(d,(80,155),"HEAP BLOCKS",T,CYAN); blocks=[("FREE",110),("USED",140),("FREE",190),("FREE",170),("USED",110),("FREE",175)]; x=80
    for name,w in blocks: d.rectangle((x,180,x+w,215),fill=(20,38,43) if name=="FREE" else (37,48,53),outline=LIME if name=="FREE" else (70,82,88),width=2); tx(d,(x+w/2,198),name,S,LIME if name=="FREE" else MUTED,"mm"); x+=w
    rr(d,(65,260,260,350)); tx(d,(162,282),"malloc(64)",F(18,1),LIME,"ma"); tx(d,(162,315),"request",S,MUTED,"ma"); ar(d,(260,305),(350,305)); rr(d,(350,255,620,350)); tx(d,(485,280),"FIRST-FIT SEARCH",T,CYAN,"ma"); scan=e((t-2)/3) if t>2 else 0; d.rectangle((380,305,590,330),fill=(8,14,17),outline=(55,68,75)); d.rectangle((380,305,380+145*scan,330),fill=(32,52,58),outline=LIME)
    rr(d,(650,255,900,350)); tx(d,(775,280),"SPLIT BLOCK",T,CYAN,"ma"); d.rectangle((680,305,770,330),fill=(31,49,54),outline=LIME); d.rectangle((770,305,865,330),fill=(17,26,30),outline=(65,78,85)); tx(d,(725,318),"64 B",S,WHITE,"mm"); tx(d,(817,318),"FREE",S,MUTED,"mm"); rr(d,(250,385,710,465)); tx(d,(480,408),"free() → COALESCE ADJACENT BLOCKS",T,CYAN,"ma"); tx(d,(55,495),"MEMORY IS MANAGED AS REAL BLOCKS, NOT A BLACK BOX",XS,MUTED); return im
def tcp(t):
    im,d=base("TCP FILE TRANSFER","CLIENT → TCP BYTE STREAM → FRAMING → SERVER → DISK",t); rr(d,(55,150,230,310)); tx(d,(142,178),"CLIENT",F(18,1),CYAN,"ma"); tx(d,(142,215),"hello.txt",B,WHITE,"ma"); tx(d,(142,245),"178 bytes",S,MUTED,"ma"); rr(d,(730,150,905,310)); tx(d,(817,178),"SERVER",F(18,1),CYAN,"ma"); tx(d,(817,215),"recv_exactly()",B); tx(d,(817,245),"write → disk",S,MUTED,"ma"); ln(d,(230,230),(730,230),(48,61,68),10)
    phase=min(1,max(0,(t-1)/10)); px=230+500*min(1,phase*1.15); d.rounded_rectangle((px-48,205,px+48,255),8,fill=(17,37,43),outline=CYAN,width=2); tx(d,(px,218),"META",S,CYAN,"ma"); tx(d,(px,238),"name + size",XS,WHITE,"ma")
    for j in range(5): q=max(0,min(1,(t-3-j*.8)/6)); x=250+q*430; d.rounded_rectangle((x-35,275,x+35,315),6,fill=(24,43,32),outline=LIME,width=2); tx(d,(x,295),f"C{j+1}",S,WHITE,"mm")
    rr(d,(270,350,690,430)); tx(d,(480,375),"TCP RECEIVER LOOP",T,CYAN,"ma"); tx(d,(480,405),"partial recv() → keep reading until expected bytes arrive",S,WHITE,"ma"); tx(d,(55,495),f"FILE PROGRESS · {min(100,max(0,int((t-3)/9*100)))}%",XS,LIME); return im
def igv(t):
    im,d=base("INTELLIGENT GROUND VEHICLE","CAMERA + LiDAR → JETSON ORIN → ROS 2 → PLANNER → MOTORS",t); rr(d,(55,135,380,405)); tx(d,(75,158),"SENSORS",T,CYAN)
    for x,y,w,h in [(100,220,45,80),(210,185,55,55),(285,260,45,85)]: d.rectangle((x,y,x+w,y+h),fill=(25,32,36),outline=(70,82,88))
    for ang in [-.8,-.4,0,.4,.8]: ln(d,(190,345),(190+125*math.cos(ang),345-125*math.sin(ang)),CYAN,2)
    d.ellipse((180,335,200,355),fill=LIME); tx(d,(75,385),"camera + LiDAR",S,MUTED); rr(d,(420,145,620,260)); tx(d,(520,170),"JETSON ORIN",T,CYAN,"ma"); tx(d,(520,205),"OpenCV + ROS 2",B,WHITE,"ma"); ar(d,(380,250),(420,205)); rr(d,(660,145,875,260)); tx(d,(767,170),"PLANNER",T,CYAN,"ma"); tx(d,(767,205),"free-space",B); tx(d,(767,232),"path + velocity",B); ar(d,(620,205),(660,205))
    rr(d,(420,300,875,405)); tx(d,(645,325),"LOCAL MAP / PATH",T,CYAN,"ma"); path=[(455,370),(540,365),(600,330),(675,350),(760,345),(835,365)]; d.line(path,fill=LIME,width=4); q=e((t-7)/6) if t>7 else 0; rx,ry=path[min(5,int(q*5))]; d.rounded_rectangle((rx-28,ry-18,rx+28,ry+18),8,fill=(24,34,39),outline=LIME,width=2); tx(d,(rx,ry),"IGV",S,WHITE,"mm"); rr(d,(720,430,875,475)); tx(d,(797,452),"ARDUINO / PWM",S,CYAN,"mm"); tx(d,(55,495),"PERCEPTION → PLANNING → LOW-LEVEL CONTROL → MOTOR MOTION",XS,MUTED); return im
def slam(t):
    im,d=base("ROS 2 SLAM + NAV2","LASER SCAN → MAP + POSE → NAV2 PLANNER → CONTROLLER",t); rr(d,(55,135,575,430)); tx(d,(75,158),"LIVE OCCUPANCY MAP",T,CYAN); walls=[(95,200,400,218),(95,200,113,350),(95,332,305,350),(305,270,323,350),(305,270,485,288),(485,185,503,290),(390,185,503,203)]
    for b in walls:d.rectangle(b,fill=(50,62,68))
    q=e((t-1)/5) if t>1 else 0; rx=145+210*q; ry=315-70*q; d.ellipse((rx-10,ry-10,rx+10,ry+10),fill=LIME)
    for ang in [-1.1,-.65,-.2,.25,.7,1.1]: ln(d,(rx,ry),(rx+90*math.cos(ang),ry-90*math.sin(ang)),CYAN,2)
    path=[(145,315),(210,300),(270,275),(330,260),(395,220),(455,205)]; d.line(path,fill=LIME,width=3); tx(d,(75,390),"scan updates map while pose is estimated",S,MUTED); rr(d,(620,135,900,430)); tx(d,(760,158),"NAVIGATION STACK",T,CYAN,"ma")
    for label,y in [("SLAM Toolbox",205),("Map + Pose",260),("Nav2 Planner",315),("Controller",370)]: d.rounded_rectangle((650,y,870,y+38),6,fill=(18,29,34),outline=LIME if label=="Nav2 Planner" else (52,66,73),width=2); tx(d,(760,y+19),label,S,WHITE,"mm")
    tx(d,(55,495),"BUILD MAP → LOCALIZE → PLAN → CONTROL → MOVE",XS,MUTED); return im
def sahas(t):
    im,d=base("SAAHAS 2.0","RTK FOLLOW → DESCENT → VISION LOCK → PRECISION LANDING",t); rr(d,(55,135,245,285)); tx(d,(150,160),"RTK GNSS",T,CYAN,"ma"); tx(d,(150,200),"BASE → ROVER",B,WHITE,"ma"); tx(d,(150,235),"centimeter-level position",S,LIME,"ma"); rr(d,(55,315,245,430)); tx(d,(150,340),"MAVLink",T,CYAN,"ma"); tx(d,(150,375),"FC ↔ Raspberry Pi",B,WHITE,"ma"); rr(d,(285,135,900,430)); tx(d,(592,160),"AUTONOMOUS RECOVERY",T,CYAN,"ma")
    platx=730 if t<10 else 610; platy=370; d.rounded_rectangle((platx-105,platy-28,platx+105,platy+28),10,fill=(20,30,35),outline=CYAN,width=3); tx(d,(platx,platy),"MOVING PLATFORM",S,WHITE,"mm")
    if t<3: dx,dy=400,205
    elif t<6: q=e((t-3)/3); dx,dy=400+190*q,205+45*q
    elif t<10: q=e((t-6)/4); dx,dy=590+20*math.sin(q*math.pi),250+100*q
    else: q=e((t-10)/5); dx,dy=610,350-10*q
    d.line([(dx,dy+20),(platx,platy-28)],fill=LIME if t>=6 else CYAN,width=3); d.polygon([(dx-25,dy),(dx,dy-18),(dx+25,dy),(dx,dy+18)],fill=(25,35,41),outline=LIME); d.ellipse((dx-5,dy-5,dx+5,dy+5),fill=LIME)
    if t>=6: sz=25; d.rectangle((platx-sz,platy-sz,platx+sz,platy+sz),outline=LIME,width=3); ln(d,(platx-38,platy),(platx+38,platy),LIME,2); ln(d,(platx,platy-38),(platx,platy+38),LIME,2)
    phase="RTK FOLLOW" if t<3 else "CONTROLLED DESCENT" if t<6 else "VISION LOCK" if t<10 else "PRECISION LANDING"; tx(d,(300,460),phase,F(17,1),LIME,"lm"); tx(d,(55,495),"GLOBAL NAVIGATION → LOCAL VISION → CLOSED-LOOP RECOVERY",XS,MUTED); return im
for n,f in [("morphle",morphle),("stm32_usart",stm),("prefrtos",pref),("heap_allocator",heap),("tcp_file_transfer",tcp),("igv",igv),("ros2_slam",slam),("sahas",sahas)]: video(n,f)
