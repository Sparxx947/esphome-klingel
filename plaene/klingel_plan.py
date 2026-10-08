import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["svg.fonttype"]="none"; matplotlib.rcParams["font.family"]="DejaVu Sans"
from matplotlib.patches import Rectangle, Circle, Polygon, FancyArrowPatch
fig=plt.figure(figsize=(8.27,5.4)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,210); ax.set_ylim(0,137); ax.axis("off")
L=dict(color="black",lw=1.3)
def line(*p,**k): ax.plot([a[0] for a in p],[a[1] for a in p],**{**L,**k})
def dot(x,y): ax.add_patch(Circle((x,y),0.9,color="black"))
T=lambda x,y,s,**k: ax.text(x,y,s,**{"fontsize":8.5,**k})
# Gemeinsamer Rueckleiter links unten, Etagenadern links
yB=12
line((12,yB),(118,yB),lw=1.8); T(12,yB-6,"Gong-Rückleiter (gemeinsam, per Messung bestimmen)",fontsize=8)
for i,(y,name,pin) in enumerate(((112,"Etage 2","D7"),(78,"Etage 1","D6"),(44,"Erdgeschoss","D5"))):
    T(2,y+2.5,name,fontsize=9,fontweight="bold"); T(2,y-3,"Etagenader",fontsize=7)
    line((24,y),(32,y)); ax.add_patch(Rectangle((32,y-2.2),12,4.4,fill=False,lw=1.3)); T(33,y+4,"1 kΩ",fontsize=8,fontweight="bold")
    line((44,y),(58,y)); dot(52,y)
    # Optokoppler-Gehaeuse
    ax.add_patch(Rectangle((58,y-13),40,22,fill=False,lw=1.4,ls="--")); T(66,y+10.5,"PC817",fontsize=8.5,fontweight="bold")
    # LED senkrecht: Anode oben (Pin1), Kathode unten (Pin2)
    lx=66; line((58,y),(lx,y),(lx,y-2)); ax.add_patch(Polygon([(lx-3,y-2),(lx+3,y-2),(lx,y-7)],closed=True,fill=False,lw=1.3)); line((lx-3,y-7.3),(lx+3,y-7.3)); line((lx,y-7.3),(lx,y-11),(58,y-11))
    T(59.5,y+1,"1",fontsize=6.5); T(59.5,y-10,"2",fontsize=6.5)
    for d in (0,2.5): ax.add_patch(FancyArrowPatch((lx+3,y-4+d),(lx+9,y-2+d),arrowstyle="-|>",mutation_scale=7,color="crimson",lw=1))
    # Transistor
    tx=84; line((tx,y-1),(tx,y-9)); line((tx,y-3),(92,y+1),(98,y+1)); line((tx,y-7),(92,y-11),(98,y-11))
    ax.add_patch(FancyArrowPatch((tx+3,y-8.5),(92,y-11),arrowstyle="-|>",mutation_scale=7,color="black",lw=1))
    T(94.5,y+2.3,"4",fontsize=6.5); T(94.5,y-9.7,"3",fontsize=6.5)
    # Pin 2 zum Rueckleiter, Diode antiparallel zwischen Pin1-Knoten und Pin2-Leitung
    line((52,y),(52,y-2)); ax.add_patch(Polygon([(49,y-7),(55,y-7),(52,y-2.3)],closed=True,fill=False,lw=1.3)); line((49,y-2),(55,y-2)); line((52,y-7),(52,y-11)); dot(52,y-11)
    T(36,y-7.5,"1N4007",fontsize=7); 
    line((52,y-11),(48,y-11),(48,y-15)); 
    line((48,y-15),(48,yB) if i==2 else (48,y-15)); 
    # Ausgang
    line((98,y+1),(152,y+1)); T(154,y,f"{pin}",fontsize=10,fontweight="bold")
    line((98,y-11),(132,y-11),(132,yB+8)); dot(132,yB+8) if True else None
# vertikale Rueckleiter-Schiene bei x=48
line((48,112-15),(48,yB)); dot(48,yB)
for y in (112,78,44): dot(48,y-15)
# GND-Schiene Ausgang
line((132,yB+8),(172,yB+8),(172,30),lw=1.4); T(174,33,"G",fontsize=10,fontweight="bold")
# D1 mini
ax.add_patch(Rectangle((152,30),40,92,fill=False,lw=1.5)); T(165,115,"D1 mini",fontsize=10,fontweight="bold")
T(165,108,"Pull-up intern",fontsize=7.5); T(165,100,"USB-Netzteil",fontsize=7.5); T(165,94,"(Verteiler)",fontsize=7)


fig.savefig("doku/klingel_plan.svg",transparent=True); fig.savefig("kl.png",dpi=80)
