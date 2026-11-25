# news-image-20261124, Tuesday 24 November 2026 — deterministic front page, PIL only.
import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; OUT=os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR','out'),'entry.png')
def F(s,b=False,ser=False):
    p='/usr/share/fonts/truetype/dejavu/'+('DejaVuSerif-Bold.ttf' if ser else 'DejaVuSans-Bold.ttf' if b else 'DejaVuSans.ttf')
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def wrap(t,f,mw):
    ws=[]
    for w in t.split(' '):
        if not ws: ws.append(w)
        elif f.getlength(ws[-1]+' '+w)<=mw: ws[-1]+=' '+w
        else: ws.append(w)
    return ws
def para(d,x,y,t,f,mw,fill=(20,20,20),lh=None):
    lh=lh or int(f.size*1.25)
    for ln in wrap(t,f,mw): d.text((x,y),ln,font=f,fill=fill); y+=lh
    return y
def chip(d,x,y,s,c):
    f=F(7,True); w=int(f.getlength(s))+10; d.rounded_rectangle([x,y,x+w,y+13],2,fill=c); d.text((x+5,y+2),s,font=f,fill=(255,255,255)); return x+w+4
def bar(d,x,y,w,h,fill): d.rectangle([x,y,x+w,y+h],fill=fill)
def sky(d,x,y,w,h,c1,c2):
    for i in range(h): d.line([(x,y+i),(x+w,y+i)],fill=tuple(int(c1[j]+(c2[j]-c1[j])*i/max(1,h)) for j in range(3)))
def tower(d,x,y,w,h):
    d.rectangle([x+w*0.35,y+h*0.25,x+w*0.65,y+h],fill=(40,60,110)); d.polygon([(x+w*0.35,y+h*0.25),(x+w*0.5,y),(x+w*0.65,y+h*0.25)],fill=(60,90,160))
    for r in range(6):
        yy=y+h*0.3+r*h*0.11
        for c in range(3): d.rectangle([x+w*0.38+c*w*0.09,yy,x+w*0.43+c*w*0.09,yy+4],fill=(255,220,120))
    d.ellipse([x+w*0.72,y+h*0.15,x+w*0.88,y+h*0.31],fill=(255,150,40)); d.ellipse([x+w*0.78,y+h*0.21,x+w*0.82,y+h*0.25],fill=(255,220,120))
def drone(d,x,y,s=1):
    d.ellipse([x-14*s,y-4,x+14*s,y+4],fill=(30,30,30)); d.ellipse([x-4,y-3,x+4,y+3],fill=(200,40,40)); d.line([(x-16*s,y-6),(x-8,y-2)],fill=(30,30,30),width=2); d.line([(x+8,y-2),(x+16*s,y-6)],fill=(30,30,30),width=2)
def building(d,x,y,w,h,c=(150,40,40)):
    d.rectangle([x,y,x+w,y+h],fill=c); d.rectangle([x,y-8,x+w*0.7,y],fill=(120,30,30))
    for r in range(3):
        for cc in range(4): d.rectangle([x+4+cc*(w-8)//4,y+6+r*(h-12)//3,x+4+cc*(w-8)//4+6,y+10+r*(h-12)//3],fill=(255,230,150))
def court(d,x,y,w,h):
    d.rectangle([x,y+h*0.55,x+w,y+h],fill=(210,200,180)); d.polygon([(x,y+h*0.55),(x+w/2,y),(x+w,y+h*0.55)],fill=(140,40,40))
    for c in range(5): d.rectangle([x+8+c*(w-16)//5,y+h*0.6,x+14+c*(w-16)//5,y+h*0.85],fill=(255,255,255))
def gavel(d,x,y):
    d.line([(x,y+18),(x+26,y-8)],fill=(90,60,20),width=4); d.rectangle([x+18,y-14,x+38,y-2],fill=(90,60,20)); d.ellipse([x+2,y+16,x+22,y+24],fill=(120,80,30))
CONT=[ [(-168,66),(-140,70),(-120,71),(-95,80),(-80,73),(-65,60),(-55,52),(-60,45),(-75,35),(-80,25),(-90,20),(-105,20),(-115,30),(-125,40),(-125,49),(-145,60)], [(-80,10),(-70,12),(-60,5),(-50,0),(-40,-5),(-35,-10),(-40,-20),(-50,-30),(-60,-40),(-70,-50),(-75,-35),(-80,-20),(-80,-5)], [(-10,36),(-5,44),(0,50),(-2,58),(5,60),(10,58),(18,56),(21,55),(28,60),(30,70),(40,68),(45,60),(40,50),(30,45),(23,40),(18,40),(12,44),(3,43),(-9,43)], [(-17,15),(-10,30),(0,36),(10,37),(20,32),(32,31),(35,28),(40,15),(48,11),(51,10),(45,0),(40,-10),(35,-20),(30,-30),(20,-35),(15,-30),(12,-18),(9,-5),(9,4),(-8,5)], [(40,68),(60,70),(80,73),(100,77),(120,73),(140,72),(160,70),(178,66),(170,60),(160,55),(142,50),(140,40),(130,35),(122,30),(110,20),(105,10),(100,8),(95,15),(90,22),(80,15),(75,8),(70,20),(60,25),(55,26),(50,30),(45,30),(40,36)], [(113,-22),(114,-30),(115,-35),(125,-32),(130,-32),(135,-35),(140,-38),(150,-37),(153,-27),(146,-19),(142,-11),(135,-12),(130,-13),(122,-14)] ]
PINS=[(1,24.7,46.7),(2,31.2,121.5),(3,40.7,-74.0),(4,47.8,35.2),(5,14.7,-17.4),(6,26.5,56.3),(7,40.7,-74.0),(8,47.7,-122.1),(9,39.8,30.5),(10,10.4,-75.5),(11,12.8,45.0),(12,13.0,44.9),(13,39.8,98.5)]
OFF={3:(0,-16),7:(10,10),11:(-14,-12),12:(14,10)}
REG=[('Europe',9,'#1f4e79'),('Middle East',8,'#8b1a1a'),('Asia',8,'#b7791f'),('Africa',2,'#2e6b34'),('Americas',7,'#5b2d8e'),('World/Space',4,'#0e7c7b')]
UTC=[('02:15','NATO space defence'),('08:16','Hanoi blast'),('10:42','Saudi strikes'),('14:27','Riyadh tower hit'),('16:51','Houthis near Aden'),('18:58','Hormuz attack'),('20:41','Huawei guilty')]
NUM=[('11','hurt, Riyadh'),('9','killed, Ukraine'),('50,018','Dow, first 50k'),('+8.99%','Taiex record'),('25','killed, Yemen'),('26','Cikande toll')]
HERO=[('1 · RIYADH · MIDDLE EAST','CONFIRMED','#2e6b34','Houthi drone hits Riyadh tallest tower again, 11 hurt','A Houthi drone hit the PIF tower, the tallest in Riyadh, for the second time in a week. At least 11 people were hurt: 2 Saudi, 2 Indian, 3 Nepali and 4 Egyptian. (Saudi officials · AP)'),('2 · SHANGHAI · ASIA','OFFICIAL','#1f4e79','China probes Shanghai party chief Chen Jining','Chen Jining, 62, the Shanghai party chief, is under investigation for serious violations. He is the fourth Politburo member to fall in a probe this year. (CCDI)'),('3 · NEW YORK · US / TECH','CONFIRMED','#2e6b34','Huawei guilty on 10 of 12 counts','A US federal jury found Huawei guilty on 10 of 12 counts, including trade-secret theft and bank fraud. It was cleared of racketeering. Sentencing is in Sep 2027. (US court)')]
CARDS=[('4 · ZAPORIZHZHIA · EUROPE','REPORTED','#5b6b7a','Russian attacks kill 9 across Ukraine in a day','Russia launched 96 drones; 73 were shot down or jammed. Nine people were killed and 81 hurt. (Ukrainian officials)'),('5 · CAS · AFRICA / SPORT','OFFICIAL','#1f4e79','CAS hands Senegal back the AFCON title','CAS gave the Africa Cup title back to Senegal after Morocco forfeited 3-0, so Senegal won 1-0. (CAS)'),('6 · HORMUZ · MIDDLE EAST','REPORTED','#5b6b7a','IRGC attacks container ship in Hormuz','An IRGC attack hit a container ship in Hormuz at 18:58 UTC, disabling navigation near Khasab, Oman. (UKMTO)'),('7 · NEW YORK · MARKETS','CONFIRMED','#2e6b34','Dow closes above 50,000 for the first time','The Dow closed at 50,018, its first finish above 50,000. The Taiex hit a record, up 8.99%, while the Nasdaq fell 1.5%. (Market close)'),('8 · REDMOND · TECH','REPORTED','#5b6b7a',"Microsoft declares 'Code Red' after historic outage",'After a 24-hour outage on 12-13 Nov, Microsoft set a one-hour global recovery target, with five workstreams and AI diagnosis. (Reuters)'),('9 · ESKISEHIR · EUROPE','REPORTED','#5b6b7a','Turkish military helicopter crash kills 5','A Turkish military AS-532 helicopter crashed in Eskisehir, killing five people on board. (Turkish officials)'),('10 · CARTAGENA · AMERICAS','REPORTED','#5b6b7a','Supermarket hostages: 25 held in Cartagena','Twenty-five people were held hostage in a Cartagena supermarket, and five elderly women were freed. (Colombian officials)'),('11 · ADEN · MIDDLE EAST','REPORTED','#5b6b7a','Houthis advance within 60 km of Aden','Houthi forces advanced to within 60 km of Aden, Yemen, in the latest push south. (Wires)'),('12 · LAHJ · MIDDLE EAST','REPORTED','#5b6b7a','Saudi strikes kill 25, wound 6 in Yemen','Saudi strikes on a bus and truck in Wadi Maabaq, Lahj, killed or left missing 25 people and wounded six. (Yemeni officials)'),('13 · JIUQUAN · SPACE','OFFICIAL','#1f4e79','China names first foreign astronaut for Tiangong','China named the Shenzhou-24 crew: Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali of Pakistan, the first foreigner on Tiangong. (CMSA)')]
ALSO=[('14 Ankara','Haftar visits Turkey for the first time.'),('15 London','UK sanctions Houthis + 4 officials.'),('16 Villavicencio','Car bomb injures 23.'),('17 Gaza','Israel kills Hamas security chief.'),('18 Baghdad','Iraq orders control of Kurdish oilfields.'),('19 Gaza','Meningitis alert: 272 cases in Oct.'),('20 DR Congo','Missing Cessna 208, 4 aboard.'),('21 Hanoi','Hot-pot blast kills at least 6.'),('22 Gulf of Finland','Ukraine hits Russian ship Sparta II.'),('23 Kuala Lumpur','Malaysia to return migrants to Myanmar.'),('24 Ulleungdo','S. Korea shelter as jets enter ADIZ.'),('25 Dhaka','Hasina plans return 16 Dec.'),('26 The Hague','14 nations back ICJ Myanmar ruling.'),('27 Jakarta','Indonesia nominates 2 VP candidates.'),('28 Beijing','China sentences Ma to death for spying.'),('29 Brussels','NATO vows defence vs space threat.'),('30 Mexico City','El Chapo Isidro held Fri 20 Nov; US drone aided capture.'),('31 San Salvador','Bukele names 3 soldiers killed in Haiti.'),('32 Ottawa','Pentagon rebukes Canada: only 41.9% of air fleet ready.'),('33 Washington','US adds Megaspeed to trade blacklist.'),('34 Kyiv','Zelensky urges talks soon.'),('35 Ras Al Khaimah','Bus-truck crash kills 13.'),('36 London','England record 5,258 heat deaths.'),('37 Kourou','Ariane 6 lofts 36 Amazon satellites.'),('38 Cikande','Factory-fire toll rises to 26.')]
def scene(d,x,y,w,h,k):
    if k==0:
        sky(d,x,y,w,h,(15,25,55),(70,40,70)); d.rectangle([x,y+h-22,x+w,y+h],fill=(25,25,35))
        for bx in range(5): d.rectangle([x+8+bx*22,y+h-52-(bx%3)*12,x+24+bx*22,y+h-22],fill=(50,55,90))
        tower(d,x+w*0.32,y+6,w*0.36,h*0.62); drone(d,x+w*0.78,y+22); d.ellipse([x+w*0.62,y+h*0.42,x+w*0.72,y+h*0.52],fill=(255,180,60)); d.ellipse([x+w*0.66,y+h*0.46,x+w*0.68,y+h*0.48],fill=(255,240,180))
    elif k==1:
        sky(d,x,y,w,h,(120,30,30),(240,200,160)); building(d,x+10,y+28,54,52); building(d,x+72,y+18,54,62,(90,30,30)); d.rectangle([x+140,y+34,x+192,y+80],fill=(200,180,140)); d.rectangle([x+150,y+44,x+182,y+70],fill=(255,255,255)); d.line([(x+150,y+52),(x+182,y+52)],fill=(150,40,40),width=2); d.line([(x+150,y+58),(x+178,y+58)],fill=(150,40,40),width=2); d.rectangle([x+210,y+52,x+280,y+78],fill=(255,255,255)); d.line([(x+216,y+60),(x+274,y+60)],fill=(30,30,30),width=2); d.line([(x+216,y+68),(x+268,y+68)],fill=(30,30,30),width=2)
    elif k==2:
        sky(d,x,y,w,h,(30,50,100),(180,200,230)); court(d,x+60,y+18,w-120,h-30); d.rectangle([x+16,y+h-28,x+w-16,y+h-12],fill=(120,90,50)); gavel(d,x+w-58,y+h-58); d.rectangle([x+16,y+22,x+60,y+40],fill=(200,40,40)); d.text((x+20,y+24),'HUAWEI',font=F(8,True),fill=(255,255,255))
    else:
        sky(d,x,y,w,h,(25,45,80),(90,130,170)); d.rectangle([x,y+h-14,x+w,y+h],fill=(40,40,50)); d.ellipse([x+w*0.3,y+6,x+w*0.5,y+22],fill=(255,220,120)); d.rectangle([x+6,y+h-26,x+32,y+h-14],fill=(180,60,40)); d.rectangle([x+w-32,y+h-26,x+w-6,y+h-14],fill=(60,120,70))
img=Image.new('RGB',(W,H),(250,244,230)); d=ImageDraw.Draw(img); d.rectangle([0,0,W-1,H-1],outline=(150,30,30),width=3)
d.text((14,8),'THE WORLD ON ONE DAY',font=F(10,True),fill=(170,30,30)); d.text((1010,8),'38 STORIES · 6 REGIONS · 13 FIELDS',font=F(10,True),fill=(170,30,30),anchor='ra')
d.text((14,24),'Tuesday 24 November 2026',font=F(30,True,True),fill=(15,15,15)); d.text((1010,34),'ONE DAY OF WORLD NEWS, ONE PICTURE',font=F(9,True),fill=(90,90,90),anchor='ra')
para(d,14,60,'Riyadh tower hit again  ·  Shanghai party chief probed  ·  Huawei guilty on 10 of 12 counts.',F(11,False,True),996,(170,30,30))
rx=14
for name,n,c in REG:
    w=int(996*n/38); d.rectangle([rx,80,rx+w-2,98],fill=c); d.text((rx+6,83),f'{name} {n}',font=F(9,True),fill=(255,255,255)); rx+=w
d.text((14,104),'THE DAY IN UTC',font=F(9,True),fill=(170,30,30))
ux=14
for t,s in UTC:
    d.text((ux,118),t,font=F(9,True),fill=(15,15,15)); d.text((ux+36,119),s,font=F(7),fill=(40,40,40)); ux+=142
d.line([(14,134),(1010,134)],fill=(170,30,30),width=1); d.text((14,140),'THE DAY IN NUMBERS',font=F(9,True),fill=(170,30,30))
nx=14
for v,lab in NUM:
    vf=F(16,True); d.text((nx,150),v,font=vf,fill=(15,15,15)); d.text((nx+int(vf.getlength(v))+5,157),lab,font=F(7),fill=(60,60,60)); nx+=166
for i,(kick,clab,cc,head,deck) in enumerate(HERO):
    x=14+i*336; d.rectangle([x,166,x+324,366],outline=(120,120,120),width=1,fill=(255,255,255)); scene(d,x+1,167,322,92,i); d.text((x+6,264),kick,font=F(8,True),fill=(170,30,30)); chip(d,x+240,262,clab,cc); para(d,x+6,280,head,F(13,True,True),312,(15,15,15)); para(d,x+6,322,deck,F(9),312,(35,35,35))
for i,(kick,clab,cc,head,deck) in enumerate(CARDS):
    r,c=i//5,i%5; x=14+c*199; y=372+r*120; d.rectangle([x,y,x+191,y+114],outline=(120,120,120),width=1,fill=(255,255,255)); scene(d,x+1,y+1,189,34,3+i%3); d.text((x+5,y+38),kick,font=F(7,True),fill=(170,30,30)); chip(d,x+132,y+37,clab,cc); para(d,x+5,y+54,head,F(9,True),181,(15,15,15)); para(d,x+5,y+76,deck,F(8),181,(40,40,40))
d.text((14,616),'WORLD MAP — PINS 1-13',font=F(9,True),fill=(170,30,30)); d.text((516,616),'ALSO ON TUESDAY 24 NOVEMBER — 25 MORE STORIES',font=F(9,True),fill=(170,30,30))
mx,my,mw,mh=14,632,490,168; d.rectangle([mx,my,mx+mw,my+mh],outline=(100,100,100),width=1,fill=(205,225,240))
def proj(lon,lat): return mx+(lon+180)/360*mw, my+(75-lat)/130*mh
for poly in CONT:
    pts=[proj(lon,lat) for lon,lat in poly]; d.polygon(pts,fill=(190,205,170),outline=(90,110,80))
for n,lat,lon in PINS:
    bx,by=proj(lon,lat); dx,dy=OFF.get(n,(0,0)); px,py=bx+dx,by+dy
    if (dx,dy)!=(0,0): d.line([(bx,by),(px,py)],fill=(170,30,30),width=1)
    d.ellipse([px-8,py-8,px+8,py+8],fill=(180,30,30),outline=(255,255,255),width=1); d.text((px,py),str(n),font=F(8,True),fill=(255,255,255),anchor='mm')
for i,(city,txt) in enumerate(ALSO):
    col=i//13; row=i%13; x=516+col*248; y=632+row*13; d.text((x,y),f'{city}: {txt}',font=F(7),fill=(25,25,25))
d.rectangle([14,806,1010,930],outline=(170,30,30),width=2,fill=(255,240,235)); d.text((22,812),'DATE CHECK',font=F(11,True),fill=(170,30,30))
para(d,22,830,'Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC.',F(9,True),976,(15,15,15))
para(d,22,852,'LEFT OUT (not 24 Nov): Hormuz mine claims, 4 tankers (23 Nov); Huang returns as Nvidia CEO (23 Nov); EU 22nd sanctions package (23 Nov); COP31 ends with no deal (22 Nov); corvette Merkury sinks (22 Nov); El Chapo Isidro arrested (Fri 20 Nov); Cikande factory fire starts (Sat 21 Nov); Trump hush-money appeal ruling (23 Nov); ATP Finals (22 Nov); Las Vegas GP (21 Nov).',F(8),976,(40,40,40))
para(d,22,896,'NOT YET: Shenzhou-24 launch (Wed 25 Nov 00:18 UTC); MPR session to pick VP (11 Dec); Huawei sentencing (Sep 2027); Hasina returns to Bangladesh (16 Dec); COP32 final decision and venue (not yet set).',F(8),976,(40,40,40))
para(d,14,938,'Sources: dailysummaryof.com/world/2026-11-24 · Reuters · AP · UKMTO · CCDI · CAS · CMSA · US court · Saudi officials · wires. CONFIRMED = 2+ outlets · OFFICIAL = on record · REPORTED = one outlet · CLAIM = one side claims it.',F(8),996,(50,50,50))
para(d,14,972,'Scenes are drawn illustrations, not photographs. Map drawn from real latitude and longitude (equirectangular). Pin 8 Redmond is on the US west coast; pins 3 and 7 share New York and are offset with leader lines.',F(8),996,(50,50,50))
d.text((14,998),'news-image-20261124 · Tuesday 24 November 2026',font=F(8),fill=(100,100,100))
os.makedirs(os.path.dirname(OUT) or '.',exist_ok=True); img.save(OUT)
print(OUT, os.path.getsize(OUT))
