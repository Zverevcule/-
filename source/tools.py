"""Workshop SVG illustrations for San3a: pegboard tools, gear, wrench-and-nut badge, done mark, screw."""
import math

# Every pegboard tool lives in viewBox 0 0 120 210 and hangs from a peg at (60, 22).
HOLE = (60, 22, 5.2)


def rrect(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return (f"M{x+r} {y}H{x+w-r}A{r} {r} 0 0 1 {x+w} {y+r}V{y+h-r}A{r} {r} 0 0 1 {x+w-r} {y+h}"
            f"H{x+r}A{r} {r} 0 0 1 {x} {y+h-r}V{y+r}A{r} {r} 0 0 1 {x+r} {y}Z")


def circ(cx, cy, r):
    return f"M{cx-r} {cy}A{r} {r} 0 1 0 {cx+r} {cy}A{r} {r} 0 1 0 {cx-r} {cy}Z"


def hole():
    return circ(*HOLE)


def with_hole(d):
    return f'{d}{hole()}'


def P(cls, d, extra=""):
    return f'<path class="{cls}" d="{d}"{extra}/>'


def R(cls, x, y, w, h, r=0, extra=""):
    return f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"{extra}/>'


def C(cls, cx, cy, r, extra=""):
    return f'<circle class="{cls}" cx="{cx}" cy="{cy}" r="{r}"{extra}/>'


EO = ' fill-rule="evenodd"'

# ---------------------------------------------------------------- tools

def pipe_wrench():  # plumbing
    g = []
    g.append(P("t-green", with_hole(rrect(49, 10, 22, 118, 11)), EO))
    for y in (46, 58, 70, 82, 94, 106):
        g.append(R("t-green-d", 52, y, 16, 3, 1.5, ' opacity=".55"'))
    g.append(R("t-steel", 53, 124, 14, 22))
    g.append(R("t-steel-d", 42, 140, 34, 22, 4))
    g.append(R("t-brass", 44, 146, 30, 10, 3))
    for x in (49, 55, 61, 67):
        g.append(R("t-brass-d", x, 146, 2, 10))
    g.append(P("t-steel", "M54 160H68V199Q68 205 62 205H30Q25 205 25 200V194Q25 189 30 189H54Z"))
    g.append(P("t-steel-l", "M30 167H60V178H30Q25 178 25 173V172Q25 167 30 167Z"))
    for x in range(30, 54, 5):  # teeth
        g.append(P("t-steel-d", f"M{x} 178l2.5 3 2.5-3Z"))
        g.append(P("t-steel-d", f"M{x} 189l2.5-3 2.5 3Z"))
    return "".join(g)


def screwdriver():  # electric
    g = []
    g.append(P("t-green", with_hole(rrect(44, 10, 32, 80, 15)), EO))
    for x in (51, 58, 65):
        g.append(R("t-green-d", x, 36, 4, 46, 2, ' opacity=".55"'))
    g.append(R("t-mint", 47, 86, 26, 12, 4))
    g.append(R("t-steel", 56, 96, 8, 82))
    g.append(R("t-steel-l", 56, 96, 3, 82))
    g.append(P("t-steel-d", "M55 176H65L68 194H52Z"))
    g.append(R("t-steel-d", 52, 194, 16, 5, 1))
    return "".join(g)


def gauge():  # AC
    g = []
    g.append(P("t-steel-d", with_hole(circ(60, 22, 10)), EO))
    g.append(R("t-steel", 57, 30, 6, 16))
    g.append(C("t-green", 60, 84, 38))
    g.append(C("t-paper", 60, 84, 31))
    ticks = []
    for i in range(11):
        a = math.radians(-225 + i * 27)
        r1, r2 = (24, 29) if i % 5 else (21, 29)
        ticks.append(f"M{60+r1*math.cos(a):.1f} {84+r1*math.sin(a):.1f}L{60+r2*math.cos(a):.1f} {84+r2*math.sin(a):.1f}")
    g.append(f'<path d="{"".join(ticks)}" class="s-ink" stroke-width="1.6" fill="none" stroke-linecap="round"/>')
    # coloured arcs: mint (low) brass (high)
    def arc(a0, a1, r):
        x0, y0 = 60 + r * math.cos(math.radians(a0)), 84 + r * math.sin(math.radians(a0))
        x1, y1 = 60 + r * math.cos(math.radians(a1)), 84 + r * math.sin(math.radians(a1))
        return f"M{x0:.1f} {y0:.1f}A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}"
    g.append(f'<path d="{arc(-225, -120, 27)}" class="s-mint" stroke-width="3" fill="none"/>')
    g.append(f'<path d="{arc(-30, 45, 27)}" class="s-brass" stroke-width="3" fill="none"/>')
    g.append('<g class="needle"><path d="M60 84L60 60" class="s-ink" stroke-width="2.4" stroke-linecap="round"/></g>')
    g.append(C("t-ink", 60, 84, 4))
    g.append(R("t-brass", 54, 120, 12, 12, 2))
    g.append('<path d="M60 132C60 160 30 150 33 174C36 197 80 198 82 178" fill="none" class="s-mint" stroke-width="7" stroke-linecap="round"/>')
    g.append(R("t-brass-d", 77, 170, 10, 12, 2))
    return "".join(g)


def multimeter():  # appliances
    g = []
    g.append(P("t-brass", with_hole(rrect(30, 12, 60, 118, 12)), EO))
    g.append(R("t-ink", 36, 34, 48, 88, 7))
    g.append(R("t-mint-p", 41, 40, 38, 20, 3))
    g.append('<text x="60" y="55" text-anchor="middle" font-size="13" font-weight="700" font-family="monospace" class="t-ink">230</text>')
    g.append(C("t-steel", 60, 87, 15))
    g.append(C("t-steel-l", 60, 87, 9))
    g.append(R("t-ink", 58.5, 74, 3, 13, 1.5))
    for a in range(0, 360, 45):
        r = math.radians(a)
        g.append(C("t-steel-l", round(60 + 20 * math.cos(r), 1), round(87 + 20 * math.sin(r), 1), 1.4))
    g.append(C("t-steel-d", 48, 112, 4.5))
    g.append(C("t-brass", 72, 112, 4.5))
    g.append('<path d="M48 116C44 146 54 160 46 186" fill="none" class="s-ink" stroke-width="3.5" stroke-linecap="round"/>')
    g.append('<path d="M72 116C78 146 66 164 74 190" fill="none" class="s-green" stroke-width="3.5" stroke-linecap="round"/>')
    g.append(R("t-ink", 42, 184, 8, 18, 3))
    g.append(R("t-green", 70, 188, 8, 18, 3))
    return "".join(g)


def spray():  # pest control & filters
    g = []
    g.append(P("t-green", with_hole("M40 12H74Q82 12 82 20V44H40Z"), EO))
    g.append(R("t-green-d", 82, 22, 12, 9, 2))
    g.append('<g class="puff">' + C("t-mint", 100, 22, 2.4) + C("t-mint", 104, 28, 1.8) + C("t-mint", 99, 31, 1.6) + "</g>")
    g.append(P("t-green-d", "M44 44Q36 62 46 76L52 73Q45 62 51 46Z"))
    g.append(R("t-steel-d", 50, 44, 22, 14, 3))
    g.append(P("t-mint-p", "M48 58H74Q86 70 86 86V188Q86 200 74 200H48Q36 200 36 188V86Q36 70 48 58Z"))
    g.append(P("t-brass", "M36 128H86V188Q86 200 74 200H48Q36 200 36 188Z", ' opacity=".7"'))
    g.append(R("t-paper", 44, 104, 34, 46, 4))
    g.append(R("t-green", 50, 114, 22, 4, 2))
    g.append(R("t-line", 50, 124, 22, 3, 1.5))
    g.append(R("t-line", 50, 132, 16, 3, 1.5))
    return "".join(g)


def roller():  # painting
    g = []
    g.append(P("t-green", with_hole(rrect(48, 10, 24, 72, 12)), EO))
    g.append(R("t-mint", 49, 78, 22, 9, 3))
    g.append('<path d="M60 87V114H102V151H94" fill="none" class="s-steel" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>')
    g.append(R("t-brass", 20, 136, 76, 32, 9))
    for x in range(26, 92, 7):
        g.append(R("t-brass-d", x, 138, 2, 28, 1, ' opacity=".45"'))
    g.append(R("t-steel-d", 16, 142, 6, 20, 2))
    g.append(R("t-steel-d", 94, 142, 6, 20, 2))
    g.append(P("t-brass", "M40 168Q42 178 38 184Q34 178 36 168Z"))
    return "".join(g)


def hammer():  # carpentry
    g = []
    g.append(P("t-brass", with_hole(rrect(52, 10, 16, 146, 8)), EO))
    g.append(R("t-green", 52, 34, 16, 50, 6))
    for y in (44, 54, 64, 74):
        g.append(R("t-green-d", 52, y, 16, 3, 1, ' opacity=".5"'))
    g.append(P("t-steel-d", "M26 150H86Q92 150 92 156V174Q92 180 86 180H26Z"))
    g.append(P("t-steel", "M90 154Q110 160 116 182Q104 172 90 174Z"))
    g.append(R("t-steel-l", 14, 148, 14, 34, 3))
    g.append(R("t-steel", 30, 154, 54, 4, 2, ' opacity=".6"'))
    return "".join(g)


def spanner():  # heaters & gas
    g = []
    g.append(P("t-steel", circ(60, 22, 20) + circ(60, 22, 9.5), EO))
    g.append(R("t-steel", 51, 38, 18, 122))
    g.append(R("t-steel-d", 55.5, 58, 9, 88, 4.5, ' opacity=".55"'))
    yc, R0, w = 176, 23, 9
    yi = yc + math.sqrt(R0 * R0 - w * w)
    jaw = (f"M{60-w} {yi:.2f}L{60-w} {yc-4}A{w} {w} 0 0 1 {60+w} {yc-4}L{60+w} {yi:.2f}"
           f"A{R0} {R0} 0 1 0 {60-w} {yi:.2f}Z")
    g.append(P("t-steel", jaw))
    g.append(C("t-steel-l", 52, 160, 2.2, ' opacity=".8"'))
    return "".join(g)


def clipboard():  # B2B
    g = []
    g.append(R("t-brass", 26, 28, 68, 160, 8))
    g.append(R("t-paper", 34, 44, 52, 134, 3))
    g.append(P("t-steel-d", with_hole(rrect(42, 12, 36, 30, 7)), EO))
    g.append(R("t-steel", 46, 34, 28, 8, 3))
    for i, y in enumerate((62, 84, 106, 128, 150)):
        g.append(R("t-line", 54, y - 2, 26, 4, 2))
        if i < 3:
            g.append(f'<path d="M40 {y}l4 4 7-8" fill="none" class="s-green" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            g.append(R("t-line", 40, y - 5, 10, 10, 2))
    return "".join(g)


def mop():  # home cleaning
    g = []
    g.append(P("t-steel-d", with_hole(circ(60, 22, 10)), EO))
    g.append(R("t-green", 55, 30, 10, 112, 5))
    g.append(R("t-green-d", 55, 40, 10, 26, 5, ' opacity=".55"'))
    g.append(R("t-steel", 49, 138, 22, 12, 4))
    g.append(R("t-brass", 34, 147, 52, 12, 5))
    strands = "".join(
        f'<path d="M{x} 157q{-3 if i % 2 else 3} 22 {1 if i % 2 else -1} 44" class="{"s-mint" if i % 3 == 0 else "s-mintp"}" stroke-width="5.5" stroke-linecap="round" fill="none"/>'
        for i, x in enumerate(range(38, 86, 6)))
    g.append(f'<g class="strands">{strands}</g>')
    return "".join(g)


TOOLS = {
    "plumbing": pipe_wrench, "electric": screwdriver, "ac": gauge, "appliances": multimeter,
    "cleaning": mop, "pest": spray, "painting": roller, "carpentry": hammer, "heaters": spanner, "b2b": clipboard,
}


def peg_svg(key, cls="peg-tool"):
    """Tool hanging from a fixed peg; the inner <g class="swing"> rotates around the peg."""
    peg = C("t-steel-d", 60, 22, 4.4) + C("t-steel-l", 58.8, 20.8, 1.5)
    return (f'<svg class="{cls}" viewBox="0 0 120 210" aria-hidden="true" focusable="false">'
            f'<g class="swing">{TOOLS[key]()}</g>{peg}</svg>')


def small_tool_svg(key):
    return (f'<svg viewBox="0 0 120 210" aria-hidden="true" focusable="false">{TOOLS[key]()}'
            f'{C("t-steel-d", 60, 22, 4.4)}</svg>')

# ---------------------------------------------------------------- gear, nut, marks

def gear_svg(teeth=12, r_out=72, r_in=61, cx=75, cy=75):
    pts = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a = i * step
        for da, r in ((-0.30, r_in), (-0.17, r_out), (0.17, r_out), (0.30, r_in)):
            pts.append(f"{cx + r * math.cos(a + da * step * 1.6):.1f},{cy + r * math.sin(a + da * step * 1.6):.1f}")
    poly = " ".join(pts)
    return (f'<svg viewBox="0 0 150 150" aria-hidden="true" focusable="false">'
            f'<polygon points="{poly}" fill="rgba(198,138,69,.16)" stroke="#C68A45" stroke-width="2.5" stroke-linejoin="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="rgba(233,183,127,.45)" stroke-width="1.5" stroke-dasharray="3 5"/>'
            f'</svg>')


def nut_badge_svg():
    nx, ny = 24, 30          # nut centre = pivot
    hx = nx + 7              # wrench head centre
    R0, w = 14, 8.3
    xm = hx - math.sqrt(R0 * R0 - w * w)
    hexpts = " ".join(f"{nx + 9.5 * math.cos(math.radians(a)):.2f},{ny + 9.5 * math.sin(math.radians(a)):.2f}" for a in range(0, 360, 60))
    jaw = (f"M{xm:.2f} {ny-w}L{nx+9.5} {ny-w}L{nx+9.5} {ny+w}L{xm:.2f} {ny+w}A{R0} {R0} 0 1 0 {xm:.2f} {ny-w}Z")
    return ('<svg class="nut-svg" viewBox="0 0 72 72" aria-hidden="true" focusable="false">'
            f'<g class="nut"><polygon points="{hexpts}" class="t-brass"/><circle cx="{nx}" cy="{ny}" r="3.6" class="t-brass-d"/></g>'
            f'<g transform="rotate(32 {nx} {ny})"><g class="wr">'
            f'<path d="{jaw}" class="t-steel-d"/>'
            f'<rect x="{hx+9}" y="{ny-3.8}" width="34" height="7.6" rx="3.8" class="t-steel-d"/>'
            f'<rect x="{hx+21}" y="{ny-4.8}" width="23" height="9.6" rx="4.8" class="t-green"/>'
            '</g></g></svg>')


def done_mark_svg():
    hexpts = " ".join(f"{46 + 38 * math.cos(math.radians(a)):.1f},{46 + 38 * math.sin(math.radians(a)):.1f}" for a in range(30, 390, 60))
    return ('<svg class="done-mark" viewBox="0 0 92 92" aria-hidden="true" focusable="false">'
            f'<polygon class="hex" points="{hexpts}"/><path class="ck" d="M30 47l11 11 21-23"/></svg>')


SCREW = ('<svg class="screw" viewBox="0 0 20 20" aria-hidden="true" focusable="false">'
         '<circle cx="10" cy="10" r="8.5" fill="currentColor"/>'
         '<path d="M6 10h8M10 6v8" stroke="#1B1F1C" stroke-width="2" stroke-linecap="round"/></svg>')

TICK = ('<svg class="tick" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
        '<circle cx="12" cy="12" r="10.5"/><path d="M7.5 12.5l3 3 6-6.5"/></svg>')
