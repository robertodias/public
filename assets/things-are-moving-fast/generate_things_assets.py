from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.join(os.path.dirname(__file__))
# ensure directory
os.makedirs(OUT_DIR, exist_ok=True)

# Try to load a TTF font
def get_font(size, bold=False):
    possible = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for p in possible:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()

# Colors (Neo-Minimal Startup)
BG = (11,15,26)  # dark navy
CYAN = (0,229,255)  # electric cyan
CORAL = (255,107,107)  # soft coral
WHITE = (245,247,250)
TAG_FILL = (255,255,255,200)

TAG_TEXT = "Beto Dias"

# helper to draw bottom-left tag on image (Pillow)
def draw_tag(draw, W, H):
    font = get_font(16)
    padding = 16
    text_w, text_h = draw.textbbox((0,0), TAG_TEXT, font=font)[2:]
    x = padding
    y = H - padding - text_h
    # translucent rounded rect bg
    rect_w = text_w + 12
    rect_h = text_h + 8
    rect = [x-6, y-4, x-6+rect_w, y-4+rect_h]
    draw.rounded_rectangle(rect, radius=6, fill=(255,255,255,24))
    draw.text((x, y), TAG_TEXT, font=font, fill=(255,255,255,200))

# Save PNG and @2x versions

def save_png_and_2x(img, name, size):
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    # @2x
    w,h = size
    img2 = img.resize((w*2, h*2), Image.LANCZOS)
    path2 = os.path.join(OUT_DIR, name.replace('.png','@2x.png'))
    img2.save(path2)
    return path, path2

# 1) cover_modern
W,H = 1200,630
cover = Image.new('RGBA',(W,H),BG)
d = ImageDraw.Draw(cover)
font_title = get_font(56)
font_sub = get_font(22)

# background geometric shapes
for i,(x,y,w,h,angle,col) in enumerate([
    (60,40,540,420,0,CYAN),
    (520,90,640,420,0,CORAL),
]):
    for b in range(4):
        bbox = [x-b*10, y-b*10, x+w+b*10, y+h+b*10]
        d.rounded_rectangle(bbox, radius=40+b*4, outline=col)

# diagonal accent lines
for i in range(-400, W+400, 80):
    d.line([(i,0),(i-200,H)], fill=(20,30,40), width=2)

# Title
title = "Things Are Moving Fast"
subtitle = "Generative UI, MCP Apps, and the New Standards Race"

d.text((80, H//2 - 60), title, font=font_title, fill=WHITE)
d.text((80, H//2 - 6), subtitle, font=font_sub, fill=(220,224,229))

# Tag
draw_tag(d,W,H)

# Save cover PNG and @2x
cover_path, cover_2x = save_png_and_2x(cover, 'cover_modern.png', (W,H))

# cover without title
cover_notitle = cover.copy()
# erase title area by redrawing background patterns roughly
c = Image.new('RGBA',(W,H),BG)
d2 = ImageDraw.Draw(c)
for i,(x,y,w,h,angle,col) in enumerate([
    (60,40,540,420,0,CYAN),
    (520,90,640,420,0,CORAL),
]):
    for b in range(4):
        bbox = [x-b*10, y-b*10, x+w+b*10, y+h+b*10]
        d2.rounded_rectangle(bbox, radius=40+b*4, outline=col)
for i in range(-400, W+400, 80):
    d2.line([(i,0),(i-200,H)], fill=(20,30,40), width=2)
# composite tag
c_draw = ImageDraw.Draw(c)
draw_tag(c_draw,W,H)
cover_notitle.save(os.path.join(OUT_DIR,'cover_modern_notitle.png'))

# SVG for cover
svg_cover = f'''<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0b0f1a" />
  <g fill="none" stroke="#00E5FF" stroke-width="3">
    <rect x="60" y="40" width="540" height="420" rx="40"/>
  </g>
  <g fill="none" stroke="#FF6B6B" stroke-width="3">
    <rect x="520" y="90" width="640" height="420" rx="40"/>
  </g>
  <text x="80" y="280" fill="#F5F7FA" font-family="Inter, Arial, sans-serif" font-size="48">Things Are Moving Fast</text>
  <text x="80" y="320" fill="#DCE0E5" font-family="Inter, Arial, sans-serif" font-size="20">Generative UI, MCP Apps, and the New Standards Race</text>
  <rect x="16" y="590" width="120" height="28" rx="6" fill="rgba(255,255,255,0.08)" />
  <text x="24" y="610" fill="rgba(255,255,255,0.85)" font-family="Inter, Arial, sans-serif" font-size="16">Beto Dias</text>
</svg>'''

with open(os.path.join(OUT_DIR,'cover_modern.svg'),'w') as f:
    f.write(svg_cover)

# also save a @2x explicitly for cover (2400x1260) already created above as cover_modern@2x.png
# But ensure path name matches desired: cover_modern@2x.png was created by save_png_and_2x

# 2) diagram_flow (1200x800)
W2,H2 = 1200,800
img = Image.new('RGBA',(W2,H2),BG)
di = ImageDraw.Draw(img)
font_lbl = get_font(22)
font_title = get_font(28)

# boxes positions
mx = 80
my = 200
bw = 240
bh = 84
gap = 60
labels = ['Model','Generative UI\nRenderer','MCP Host','MCP Apps\n(composable modules)']
boxes = []
for i,lab in enumerate(labels):
    x = mx + i*(bw+gap)
    y = my
    di.rounded_rectangle([x,y,x+bw,y+bh], radius=12, outline=WHITE, width=2)
    # icon
    icx = x+30
    icy = y+bh//2
    di.ellipse([icx-18,icy-18,icx+18,icy+18], outline=CYAN, width=3)
    # text
    di.multiline_text((x+70,y+10), lab, font=font_lbl, fill=WHITE, spacing=4)
    boxes.append((x,y,bw,bh))

# arrows
for i in range(len(boxes)-1):
    ax,ay,aw,ah = boxes[i]
    bx,by,bw2,bh2 = boxes[i+1]
    start = (ax+aw, ay+ah//2)
    end = (bx, by+bh2//2)
    di.line([start,end], fill=CYAN, width=4)
    ex,ey = end
    di.polygon([(ex,ey),(ex-12,ey-6),(ex-12,ey+6)], fill=CYAN)

# Agent box above
agent_x = mx + (bw+gap)
agent_y = my - 180
di.rounded_rectangle([agent_x,agent_y,agent_x+bw,agent_y+bh], radius=12, outline=WHITE, width=2)
di.multiline_text((agent_x+70,agent_y+10), 'Agent (A2UI)\norchestrator', font=font_lbl, fill=WHITE)
# arrows from agent to model and to MCP Apps
start = (agent_x+10+bw//2, agent_y+bh)
end1 = (boxes[0][0]+20, boxes[0][1]+boxes[0][3]//2)
end2 = (boxes[-1][0]+boxes[-1][2]-10, boxes[-1][1]+boxes[-1][3]//2)
di.line([start,end1], fill=CORAL, width=3)
di.line([start,end2], fill=CORAL, width=3)

# title
di.text((mx, my-80), 'Architecture / Flow', font=font_title, fill=WHITE)

# tag
draw_tag(di,W2,H2)

img.save(os.path.join(OUT_DIR,'diagram_flow.png'))
# save @2x
img.resize((W2*2,H2*2), Image.LANCZOS).save(os.path.join(OUT_DIR,'diagram_flow@2x.png'))

# create simple SVG for diagram
svg_diag = f'''<svg width="1200" height="800" viewBox="0 0 1200 800" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0b0f1a" />
  <text x="80" y="140" fill="#F5F7FA" font-family="Inter, Arial, sans-serif" font-size="28">Architecture / Flow</text>
  <g stroke="#F5F7FA" fill="none" stroke-width="2">
    <rect x="80" y="200" width="240" height="84" rx="12"/>
    <rect x="380" y="200" width="240" height="84" rx="12"/>
    <rect x="680" y="200" width="240" height="84" rx="12"/>
    <rect x="980" y="200" width="240" height="84" rx="12"/>
  </g>
  <g fill="none" stroke="#00E5FF" stroke-width="4">
    <path d="M320 242 L380 242" />
    <path d="M620 242 L680 242" />
    <path d="M920 242 L980 242" />
  </g>
  <rect x="320" y="20" width="240" height="84" rx="12" stroke="#F5F7FA" fill="none" />
  <line x1="440" y1="104" x2="100" y2="242" stroke="#FF6B6B" stroke-width="3" />
  <line x1="440" y1="104" x2="1120" y2="242" stroke="#FF6B6B" stroke-width="3" />
  <rect x="16" y="760" width="120" height="28" rx="6" fill="rgba(255,255,255,0.08)" />
  <text x="24" y="780" fill="rgba(255,255,255,0.85)" font-family="Inter, Arial, sans-serif" font-size="16">Beto Dias</text>
</svg>'''

with open(os.path.join(OUT_DIR,'diagram_flow.svg'),'w') as f:
    f.write(svg_diag)

# 3) action_list (1200x630) 3-panel
W3,H3 = 1200,630
al = Image.new('RGBA',(W3,H3),BG)
d3 = ImageDraw.Draw(al)
font_h = get_font(26)
font_s = get_font(20)
# three panels
panel_w = (W3 - 4*40)//3
px = 40
for i,(title_txt, color) in enumerate([('Generate UI',CYAN),('Compose App',CORAL),('Deploy to Host',WHITE) ]):
    x = px + i*(panel_w+40)
    d3.rounded_rectangle([x,80,x+panel_w, H3-120], radius=16, outline=(255,255,255,24), width=2, fill=(0,0,0,0))
    # icon circle
    cx = x + 60
    cy = 180
    d3.ellipse([cx-34,cy-34,cx+34,cy+34], fill=color)
    # title
    d3.text((x+120, cy-14), title_txt, font=font_h, fill=WHITE)
    # short label
    d3.text((x+40, cy+44), 'Quick actions to convert ideas into running interfaces', font=font_s, fill=(200,205,210))

# tag
draw_tag(d3,W3,H3)

al.save(os.path.join(OUT_DIR,'action_list.png'))
al.resize((W3*2,H3*2), Image.LANCZOS).save(os.path.join(OUT_DIR,'action_list@2x.png'))

# svg for action_list
svg_al = f'''<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0b0f1a" />
  <g font-family="Inter, Arial, sans-serif">
    <rect x="40" y="80" width="340" height="430" rx="16" stroke="rgba(255,255,255,0.09)" fill="none" />
    <rect x="440" y="80" width="340" height="430" rx="16" stroke="rgba(255,255,255,0.09)" fill="none" />
    <rect x="840" y="80" width="340" height="430" rx="16" stroke="rgba(255,255,255,0.09)" fill="none" />
    <circle cx="100" cy="180" r="34" fill="#00E5FF" />
    <text x="160" y="188" fill="#F5F7FA" font-size="26">Generate UI</text>
    <circle cx="500" cy="180" r="34" fill="#FF6B6B" />
    <text x="560" y="188" fill="#F5F7FA" font-size="26">Compose App</text>
    <circle cx="900" cy="180" r="34" fill="#F5F7FA" />
    <text x="960" y="188" fill="#F5F7FA" font-size="26">Deploy to Host</text>
  </g>
  <rect x="16" y="594" width="120" height="28" rx="6" fill="rgba(255,255,255,0.08)" />
  <text x="24" y="614" fill="rgba(255,255,255,0.85)" font-family="Inter, Arial, sans-serif" font-size="16">Beto Dias</text>
</svg>'''
with open(os.path.join(OUT_DIR,'action_list.svg'),'w') as f:
    f.write(svg_al)

# 4) action_agent (split-screen)
W4,H4 = 1200,630
aa = Image.new('RGBA',(W4,H4),BG)
d4 = ImageDraw.Draw(aa)
# left half: A2UI agent orchestration
d4.rectangle([0,0,W4//2,H4], fill=None, outline=None)
d4.text((60,60), 'Model-driven Agents (A2UI)', font=get_font(30), fill=WHITE)
d4.text((60,110), 'Autonomous orchestration, real-time rendering', font=get_font(18), fill=(200,205,210))
# right half: MCP Apps
d4.text((W4//2 + 60,60), 'MCP Apps', font=get_font(30), fill=WHITE)
d4.text((W4//2 + 60,110), 'Composable app modules hosted by MCP', font=get_font(18), fill=(200,205,210))
# divider
d4.line([(W4//2,40),(W4//2,H4-40)], fill=(255,255,255,20), width=2)
# small visuals
# left: flow circles
for i in range(4):
    cx = 140 + i*60
    cy = 260
    d4.ellipse([cx-22,cy-22,cx+22,cy+22], outline=CYAN, width=3)
    d4.line([(cx+22,cy),(cx+60,cy)], fill=CYAN, width=3)
# right: module cards
for i in range(3):
    rx = W4//2 + 80
    ry = 220 + i*90
    d4.rounded_rectangle([rx,ry,rx+420,ry+64], radius=10, outline=WHITE, width=2)
    d4.text((rx+16,ry+18), f'Module {i+1}', font=get_font(18), fill=WHITE)

# tag
draw_tag(d4,W4,H4)

aa.save(os.path.join(OUT_DIR,'action_agent.png'))
aa.resize((W4*2,H4*2), Image.LANCZOS).save(os.path.join(OUT_DIR,'action_agent@2x.png'))

# svg for action_agent
svg_agent = f'''<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0b0f1a" />
  <line x1="600" y1="40" x2="600" y2="590" stroke="rgba(255,255,255,0.08)" stroke-width="2" />
  <text x="60" y="60" fill="#F5F7FA" font-family="Inter, Arial, sans-serif" font-size="30">Model-driven Agents (A2UI)</text>
  <text x="660" y="60" fill="#F5F7FA" font-family="Inter, Arial, sans-serif" font-size="30">MCP Apps</text>
  <rect x="16" y="594" width="120" height="28" rx="6" fill="rgba(255,255,255,0.08)" />
  <text x="24" y="614" fill="rgba(255,255,255,0.85)" font-family="Inter, Arial, sans-serif" font-size="16">Beto Dias</text>
</svg>'''
with open(os.path.join(OUT_DIR,'action_agent.svg'),'w') as f:
    f.write(svg_agent)

# 5) action_endstate (metrics)
W5,H5 = 1200,630
es = Image.new('RGBA',(W5,H5),BG)
d5 = ImageDraw.Draw(es)
# three metric cards
mx = 80
for i,(label,val) in enumerate([('Speed','+3.2x'),('Conversions','+18%'),('Automation','>70%')]):
    x = mx + i*360
    d5.rounded_rectangle([x,120,x+320,360], radius=12, outline=WHITE, width=2)
    d5.text((x+24,160), val, font=get_font(44), fill=CYAN)
    d5.text((x+24,220), label, font=get_font(20), fill=(200,205,210))
# small description
d5.text((80,420), 'Tangible business outcomes from combining Generative UI and composable apps', font=get_font(20), fill=(200,205,210))

# tag
draw_tag(d5,W5,H5)

es.save(os.path.join(OUT_DIR,'action_endstate.png'))
es.resize((W5*2,H5*2), Image.LANCZOS).save(os.path.join(OUT_DIR,'action_endstate@2x.png'))

svg_es = f'''<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#0b0f1a" />
  <g font-family="Inter, Arial, sans-serif">
    <rect x="80" y="120" width="320" height="240" rx="12" stroke="#F5F7FA" fill="none" />
    <rect x="440" y="120" width="320" height="240" rx="12" stroke="#F5F7FA" fill="none" />
    <rect x="800" y="120" width="320" height="240" rx="12" stroke="#F5F7FA" fill="none" />
    <text x="104" y="180" fill="#00E5FF" font-size="44">+3.2x</text>
    <text x="104" y="230" fill="#F5F7FA" font-size="20">Speed</text>
    <text x="464" y="180" fill="#00E5FF" font-size="44">+18%</text>
    <text x="464" y="230" fill="#F5F7FA" font-size="20">Conversions</text>
    <text x="824" y="180" fill="#00E5FF" font-size="44">>70%</text>
    <text x="824" y="230" fill="#F5F7FA" font-size="20">Automation</text>
  </g>
  <rect x="16" y="594" width="120" height="28" rx="6" fill="rgba(255,255,255,0.08)" />
  <text x="24" y="614" fill="rgba(255,255,255,0.85)" font-family="Inter, Arial, sans-serif" font-size="16">Beto Dias</text>
</svg>'''
with open(os.path.join(OUT_DIR,'action_endstate.svg'),'w') as f:
    f.write(svg_es)

print('Generated assets in', OUT_DIR)
