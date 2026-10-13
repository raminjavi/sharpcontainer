import sys,subprocess,math
from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,H=map(int,sys.argv[1:3]);out=sys.argv[3];FPS=30;T=21.0
F='/usr/share/fonts/truetype/sand-box/google/Inter/Inter-VariableFont_opsz,wght.ttf'
def font(sz,w='Bold'):
    f=ImageFont.truetype(F,sz)
    try:f.set_variation_by_name(w)
    except Exception:pass
    return f
V=H>W; S=min(W,H)/1080
BG=(18,20,24);RED=(214,34,40);WH=(255,255,255);GR=(170,176,186)
I={k:Image.open('/workspace/flx/video/src/'+k+'.jpg').convert('RGB') for k in ['hero-sharps-container','wall-cabinet-t46wm','r-series-r07','y-series-y01','container-dms-f02','t-series-t3','t-series-t46c']}
def ease(x):x=max(0,min(1,x));return x*x*(3-2*x)
def card(img,box,z,fx=.5,fy=.5,a=1):
    x0,y0,w,h=box;iw,ih=img.size
    s=max(w/iw,h/ih)*z;cw,ch=w/s,h/s
    l=(iw-cw)*fx;t=(ih-ch)*fy
    c=img.resize((w,h),Image.LANCZOS,box=(l,t,l+cw,t+ch))
    return c
def fit(img,w,h):
    iw,ih=img.size;s=min(w/iw,h/ih);return img.resize((int(iw*s),int(ih*s)),Image.LANCZOS)
def text(d,xy,s,sz,col,w='Bold',anchor='la',a=1):
    if a<=0:return
    col=tuple(int(BG[i]+(col[i]-BG[i])*a) for i in range(3))
    d.text(xy,s,font=font(int(sz*S),w),fill=col,anchor=anchor)
def fade(t,t0,t1,d=.35):return ease((t-t0)/d)*ease((t1-t)/d)
def panel(fr,img,box,z,fx=.5,fy=.5):
    c=card(img,box,z,fx,fy);m=Image.new('L',c.size,0);ImageDraw.Draw(m).rounded_rectangle([0,0,c.size[0]-1,c.size[1]-1],int(28*S),fill=255)
    fr.paste(c,box[:2],m)
def frame(t):
    fr=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(fr)
    M=int(70*S)
    # layout: image area & text area
    if V: ib=(M,int(H*.37),W-2*M,int(H*.47)); tx,ty=M,int(H*.08)
    else: ib=(int(W*.47),M,int(W*.53)-M,H-2*M); tx,ty=M+20,int(H*.22)
    def head(lines,t0,t1,sub=None,szz=84):
        a=fade(t,t0,t1);y=ty
        d.rectangle([tx,y,tx+int(90*S),y+int(10*S)],fill=RED);y+=int(40*S)
        for i,l in enumerate(lines):
            aa=fade(t,t0+.1*i,t1);dy=int((1-ease((t-t0-.1*i)/.4))*30*S)
            text(d,(tx,y+dy),l,szz,WH,'Bold',a=aa);y+=int(szz*1.18*S)
        if sub:
            y+=int(20*S)
            for i,l in enumerate(sub):
                aa=fade(t,t0+.35+.25*i,t1)
                text(d,(tx,y),l,46,GR if not l.startswith('•') else WH,'Medium',a=aa);y+=int(64*S)
    def env(t0,t1):return fade(t,t0,t1,.4)
    if t<3.5:
        panel(fr,I['hero-sharps-container'],ib,1.0+0.12*t/3.5,.5,.4)
        head(['Inspection-ready','stations start here.'],0.2,3.5)
    elif t<7.5:
        u=(t-3.5)/4;panel(fr,I['hero-sharps-container'],ib,1.15+.35*u,.75,.35)
        head(['Built for the','sharps you use.'],3.5,7.5,['• Puncture- & leak-resistant','• Clear fill line','• Lockable lid'])
    elif t<11.5:
        u=(t-7.5)/4;x0,y0,w,h=ib;d.rounded_rectangle([x0,y0,x0+w,y0+h],int(28*S),fill=WH)
        ks=['r-series-r07','y-series-y01','container-dms-f02','t-series-t3']
        cw,ch=w//2,h//2
        for i,k in enumerate(ks):
            a=ease((t-7.6-.2*i)/.4)
            if a<=0:continue
            im=fit(I[k],int(cw*.82*(0.94+.06*u)),int(ch*.82*(0.94+.06*u)))
            px=x0+(i%2)*cw+(cw-im.size[0])//2;py=y0+(i//2)*ch+(ch-im.size[1])//2+int((1-a)*30*S)
            fr.paste(im,(px,py))
        head(['Sizes from','0.7 to 5 L.'],7.5,11.5,['Red and yellow options.','Travel, station or shared room.'])
    elif t<14.5:
        u=(t-11.5)/3;x0,y0,w,h=ib;d.rounded_rectangle([x0,y0,x0+w,y0+h],int(28*S),fill=WH)
        im=fit(I['wall-cabinet-t46wm'],int(w*.9*(1+.06*u)),int(h*.9*(1+.06*u)))
        fr.paste(im,(x0+(w-im.size[0])//2,y0+(h-im.size[1])//2))
        head(['Lockable wall','cabinet: T4.6WM.'],11.5,14.5,['Mount it. Lock it. Done.'])
    elif t<17.2:
        u=(t-14.5)/2.7
        panel(fr,I['hero-sharps-container'],ib,1.05+.1*u,.3,.5)
        ov=Image.new('RGB',(ib[2],ib[3]),BG);m=Image.new('L',ov.size,0);ImageDraw.Draw(m).rounded_rectangle([0,0,ov.size[0]-1,ov.size[1]-1],int(28*S),fill=120);fr.paste(ov,ib[:2],m)
        head(['Based in Ontario.','Delivery across','Canada.'],14.5,17.2)
    else:
        a=fade(t,17.2,T+1);cx=W//2;y=int(H*(.30 if V else .12))
        im=fit(I['hero-sharps-container'],int(W*(.62 if V else .30)),int(H*(.26 if V else .26)))
        if a>0:
            sc=fr.copy();sc.paste(im,(cx-im.size[0]//2,y));fr=Image.blend(fr,sc,a);d=ImageDraw.Draw(fr)
        y+=im.size[1]+int(70*S)
        text(d,(cx,y),'Sharp Container',96,WH,'ExtraBold','ma',a);y+=int(110*S)
        text(d,(cx,y),'by Felix',52,GR,'Medium','ma',a);y+=int(110*S)
        b=ease((t-17.7)/.4)
        if b>0:
            bw,bh=int(470*S),int(110*S);d.rounded_rectangle([cx-bw//2,y,cx+bw//2,y+bh],bh//2,fill=tuple(int(BG[i]+(RED[i]-BG[i])*b) for i in range(3)))
            text(d,(cx,y+bh//2),'Get a quote',54,WH,'Bold','mm',b)
        y+=int(160*S);text(d,(cx,y),'info@felixtrument.ca',50,WH,'Medium','ma',ease((t-18)/.4))
    # brand tag
    if t<17.2: text(d,((W-M) if V else tx,H-int(30*S)),'Sharp Container by Felix',30,GR,'Medium','rs' if V else 'ls')
    return fr
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-preset','slow','-crf','26','-maxrate','1.6M','-bufsize','3M','-pix_fmt','yuv420p','-movflags','+faststart',out],stdin=subprocess.PIPE)
for n in range(int(T*FPS)):
    t=n/FPS;f=frame(t);p.stdin.write(f.tobytes())
    if n==int(1.5*FPS):f.save(out.replace('.mp4','-f1.png'))
    if n==int(19.5*FPS):f.save(out.replace('.mp4','-f6.png'))
p.stdin.close();p.wait()
