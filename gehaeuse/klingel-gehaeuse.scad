// Tuerklingel: Gehaeuse fuer Minilötplatine 45 x 39 (3 x PC817 + 1N4007 + 1 kΩ) und Wemos D1 mini
// Stand 11.10.2026 — Notiz project_ha_klingel.  Innenraum (Holznische neben der Abzweigdose) → PLA reicht.
//
// TEIL = "box" | "deckel" | "zusammen" | "schnitt" | "alle"
//
// Aufteilung: links die Klingelseite (Lochraster, Kabel der Abzweigdose kommt LINKS rein),
//             rechts die ESP-Seite (D1 mini, USB-Stecker kommt RECHTS rein) — wie auf der Platine getrennt.
//
// ANNAHMEN (abgeleitet, nicht gemessen) — ★ vor dem Druck nachmessen:
//   lr_l x lr_b        Minilötplatine 44,12 x 38,74 — GEMESSEN 11.10.
//   d1_l x d1_b        D1 mini 34,2 x 25,6 — GEMESSEN 11.10.
//   usb_stecker        Umspritzung Micro-USB 10,8 x 7,2 — GEMESSEN 11.10.
//   kabel_d            4 Einzellitzen à 1,38 mm — GEMESSEN 11.10.
//
// BESTÜCKUNGSREGELN, damit nichts auf eine Auflage trifft (Lehre 07.10., Optolink-Gehaeuse):
//   - Lochraster liegt NUR auf 4 Eckstützen (je ec x ec mm) → die 2 x 2 Eckloecher jeder Ecke NICHT belegen.
//     Unterseite: Loetstellen frei, Beinchen auf ≤ 2 mm kürzen (Freiraum darunter = stuetz_h).
//   - D1 mini MIT Stiftleisten, Dupont-Stecker zeigen NACH OBEN (Bauhoehe 25 mm, gemessen 11.10.). Er liegt nur mit dem
//     ANTENNEN-Ende auf einem Sockel zwischen den Stiftleisten-Reihen (dort ist die Unterseite bauartbedingt frei); das USB-Ende trägt der
//     eingesteckte Stecker in der Wandöffnung. Mit einem Tropfen Heißkleber auf dem Sockel fixieren.
//   - Bauteilhöhe über dem Lochraster max. ~10 mm (PC817 ~4,6, 1N4007 liegend ~3, Widerstand ~2,5).
// Druck: Box auf dem Boden, Deckel mit der Platte nach unten (TEIL="deckel" dreht ihn), 0,2 mm, ohne Stützen.
// Deckel: 4 Blechschrauben 3 x 12 (oder 2,9 x 13) in die Eckdome.

TEIL = "alle";
$fn = 48;

// ---------- Platinen ----------
lr_l = 44.12; lr_b = 38.74; lr_t = 1.6;    // Lochraster, gemessen 11.10.
d1_l = 34.2; d1_b = 25.6;  d1_t = 1.0;     // ★ D1 mini
sp   = 0.8;                                // Spiel rundum

// ---------- Gehaeuse ----------
w      = 2.2;    // Wand
bo     = 2.0;    // Boden
d1_bauhoehe = 25;     // D1 mit Stiftleisten + Dupont-Steckern NACH OBEN: Platinen-Unterseite bis Steckeroberkante (gemessen 11.10.)
biege  = 4;      // Luft ueber den Steckern, damit die Litzen umbiegen koennen
d1_h = 6;             // D1 liegt 6 mm ueber dem Boden (Lochraster 4): Stecker-Umspritzung bleibt ueber dem Boden,
                      // auch wenn die USB-Buchse auf der Platinen-UNTERseite sitzt
ih     = d1_h + d1_bauhoehe + biege;   // = 35
stuetz_h = 4;    // Freiraum unter beiden Platinen
gap_m  = 8;      // Platz zwischen Lochraster und D1 fuer die 4 Verbindungsadern
gap_l  = 10;     // links: Kabeleinfuehrung + Zugentlastung VOR dem Lochraster (nicht darunter)
il = gap_l + lr_l + sp + gap_m + d1_l + 1.0;  // rechts nur 1 mm: USB-Buchse sitzt bündig an der Platinenkante
ib = lr_b + 2*sp;
al = il + 2*w;  ab = ib + 2*w;
dom_d = 7;  dom_loch = 2.5;  schraub_t = 12;   // Vorbohrung 2,5 fuer 3er Blechschraube
dom_rest = 2;    // Boden bleibt unter der Vorbohrung stehen (Loch geht NICHT durch den Boden)

// Lage der Platinen (Innenraum beginnt bei x=0, y=0, z=bo)
lr_x0 = gap_l;        lr_y0 = sp;
d1_x0 = il - 1.0 - d1_l;  d1_y0 = (ib - d1_b)/2;

ec = 5.5;             // Eckstütze: Platine hat in jeder Ecke ein grosses Befestigungsloch (ohne Pads) → Stütze traegt den Rand drumherum
sockel_l = 6;         // D1-Sockel unter dem Antennen-Ende (Antennenende = links, zur Platinenmitte hin)
sockel_b = 16;

// Kabel/Stecker
kabel_d = 4.5;        // 4 Einzellitzen à 1,38 mm (gemessen 11.10.) → Buendel ~3,3 mm
kabel_z = 6;          // Achshöhe der Kabeleinfuehrung über dem Boden
usb_stecker = [10.8, 7.2];  // gemessen
usb_versatz = 1.8;    // Buchsenmitte liegt ~1,8 mm ober- ODER unterhalb der Platinenmitte (Seite unbekannt)
usb_b = usb_stecker[0] + 1.7;                      // 12,5
usb_h = usb_stecker[1] + 2*usb_versatz + 0.8;      // 11,6: deckt Buchse oben UND unten, je 0,4 Luft
usb_z = bo + d1_h + d1_t/2;   // Platinenmitte des D1
usb_frei = 9.5;       // Mitte unter der Buchse frei (Micro-USB-Buchse ~7,5 breit + Luft)
usb_stuetze_b = 4.5;  // je Stuetze → aussen bis ±9,25 von der Mitte; Stiftleisten-Loetstellen beginnen bei ~±10,4
usb_stuetze_l = 4;    // ab der USB-Kante nach innen

// Wandbefestigung (Holz): 2 Laschen an den Stirnseiten unten? Dort sind Kabel → Laschen an den LÄNGSseiten
lasche_l = 12; lasche_b = 12; lasche_t = 3; lasche_loch = 4.4;  // Spax 4 (Linsenkopf)

// Schraubsaeulen IN den Innenecken (6 x 6). Frueher Dome aussen per hull() → hull fuellte ALLE Waende auf 6,5 mm auf
// und die Durchbrueche endeten blind (11.10.). Jetzt: Aussenwand ueberall w = 2,2.
saeule = 6;  saeule_loch = 1.9;   // Lochmitte 1,9 mm von der Innenecke → ≥ 2,7 mm Material rundum
function dome() = [for (x=[saeule_loch, il-saeule_loch], y=[saeule_loch, ib-saeule_loch]) [x,y]];
function saeulen() = [for (x=[0, il-saeule], y=[0, ib-saeule]) [x,y]];

module aussen(h) {
    hull() for (x=[-w+3, il+w-3], y=[-w+3, ib+w-3]) translate([x,y,0]) cylinder(r=3, h=h);
}

module box() {
    difference() {
        union() {
            aussen(bo + ih);
            // Laschen (je zwei pro Längsseite)
            for (x=[il*0.2, il*0.8], s=[-1,1])
                translate([x - lasche_l/2, s<0 ? -w - lasche_b + 0.5 : ib + w - 0.5, 0])
                    difference() {
                        cube([lasche_l, lasche_b, lasche_t]);
                        translate([lasche_l/2, s<0 ? lasche_b/2 - 0.5 : lasche_b/2 + 0.5, -1]) cylinder(d=lasche_loch, h=lasche_t+2);
                    }
        }
        // Innenraum ohne die 4 Ecksaeulen
        translate([0, 0, bo]) difference() {
            cube([il, ib, ih + 1]);
            for (q=saeulen()) translate([q[0], q[1], -1]) cube([saeule, saeule, ih + 3]);
        }
        // Deckel-Schraubloecher in den Domen: von oben, schraub_t tief, Boden bleibt
        for (p=dome()) translate([p[0], p[1], max(dom_rest, bo + ih - schraub_t)]) cylinder(d=dom_loch, h=schraub_t + 1);
        // Kabel von der Abzweigdose: linke Stirnwand, Mitte, knapp über Platinenebene
        translate([-w - 5, ib/2, bo + kabel_z]) rotate([0, 90, 0]) cylinder(d=kabel_d, h=w + 6);   // geht sicher durch die Wand
        // USB-Stecker: rechte Stirnwand, vor der D1-Buchse
        translate([il - 1, d1_y0 + d1_b/2 - usb_b/2, usb_z - usb_h/2]) cube([w + 6, usb_b, usb_h]);   // geht sicher durch die Wand
    }
    // Eckstuetzen Lochraster
    for (x=[lr_x0, lr_x0 + lr_l - ec], y=[lr_y0, lr_y0 + lr_b - ec])
        translate([x, y, bo]) cube([ec, ec, stuetz_h]);
    // Anschlaege links und rechts neben (nicht unter) dem Lochraster, 1,5 mm ueber Platinenoberkante; in y fuehren die Waende
    for (x=[lr_x0 - 0.3 - 1.6, lr_x0 + lr_l + 0.3], y=[lr_y0, lr_y0 + lr_b - ec]) translate([x, y, bo]) cube([1.6, ec, stuetz_h + lr_t + 1.5]);
    // D1-Sockel unter dem Antennen-Ende + seitliche Fuehrungen neben (nicht unter) der Platine
    translate([d1_x0, d1_y0 + d1_b/2 - sockel_b/2, bo]) cube([sockel_l, sockel_b, d1_h]);
    for (y=[d1_y0 - 0.4 - 1.6, d1_y0 + d1_b + 0.4]) translate([d1_x0, y, bo]) cube([sockel_l, 1.6, d1_h + d1_t + 1.5]);
    // USB-Ende (11.10.: lag sonst schief): zwei Stuetzen NEBEN der Buchse, Mitte frei (Buchse kann unten sitzen),
    // aussen frei fuer die Loetstellen der Stiftleisten (Reihen bei ±11,43 mm von der Mitte).
    for (sy=[-1,1]) translate([il - 1 - usb_stuetze_l, d1_y0 + d1_b/2 + (sy>0 ? usb_frei/2 : -usb_frei/2 - usb_stuetze_b), bo])
        cube([usb_stuetze_l, usb_stuetze_b, d1_h]);
    // Zugentlastung: Kabelbinder-Steg hinter der Kabeleinfuehrung (Kabel unter dem Steg durch, Binder drumherum)
    // Zwei Pfosten links/rechts der Kabelachse, Kabel laeuft dazwischen; Binder um Pfosten + Kabel, liegt komplett in gap_l
    zx = 3;
    for (y=[ib/2 - kabel_d/2 - 2.5, ib/2 + kabel_d/2 + 0.5]) translate([zx, y, bo]) cube([3, 2, kabel_z + kabel_d/2]);
}

module deckel() {
    t = 2.0; lip_h = 3; lip_w = 1.2; lsp = 0.3;
    difference() {
        aussen(t);
        for (p=dome()) translate([p[0], p[1], -1]) cylinder(d=3.4, h=t + 2);
    }
    // Lippe nach innen, an den Ecksaeulen ausgespart
    translate([0, 0, -lip_h]) difference() {
        translate([lsp, lsp, 0]) cube([il - 2*lsp, ib - 2*lsp, lip_h]);
        translate([lsp + lip_w, lsp + lip_w, -1]) cube([il - 2*lsp - 2*lip_w, ib - 2*lsp - 2*lip_w, lip_h + 2]);
        for (q=saeulen()) translate([q[0] - lsp, q[1] - lsp, -1]) cube([saeule + 2*lsp, saeule + 2*lsp, lip_h + 2]);
    }
    // Niederhalter auf die 4 Lochraster-Ecken (genau ueber den Eckstuetzen, 0,3 mm Vorspannung)
    nh = ih - stuetz_h - lr_t + 0.3;
    for (x=[lr_x0, lr_x0 + lr_l - ec], y=[lr_y0, lr_y0 + lr_b - ec])
        translate([x, y, -nh]) cube([ec, ec, nh]);
}

if (TEIL=="box") box();
if (TEIL=="deckel") rotate([180,0,0]) deckel();
if (TEIL=="zusammen") { box(); %translate([0,0,bo+ih]) deckel(); }
if (TEIL=="schnitt") difference() { union() { box(); translate([0,0,bo+ih]) deckel(); } translate([-50, ib/2, -20]) cube([200, 100, 100]); }
if (TEIL=="alle") { box(); translate([0, ab + 30, 0]) rotate([180,0,0]) translate([0,-ib,0]) deckel(); }
