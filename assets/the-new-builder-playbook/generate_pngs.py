from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.dirname(__file__)

# Try common fonts
def load_font(size, bold=False):
    candidates = [
        "/Library/Fonts/Inter-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def rounded_rect(draw, xy, radius, fill):
    x1,y1,x2,y2 = xy
    draw.rectangle([x1+radius, y1, x2-radius, y2], fill=fill)
    draw.rectangle([x1, y1+radius, x2, y2-radius], fill=fill)
    # corners
    draw.pieslice([x1, y1, x1+2*radius, y1+2*radius], 180, 270, fill=fill)
    draw.pieslice([x2-2*radius, y1, x2, y1+2*radius], 270, 360, fill=fill)
    draw.pieslice([x1, y2-2*radius, x1+2*radius, y2], 90, 180, fill=fill)
    draw.pieslice([x2-2*radius, y2-2*radius, x2, y2], 0, 90, fill=fill)


def save_png(img, name):
    path = os.path.join(OUT_DIR, name)
    img.save(path)
    print('WROTE', path)


def draw_cover(img, title=True):
    w,h = img.size
    draw = ImageDraw.Draw(img)
    bg = (247,247,246)
    cyan = (0,211,255)
    coral = (255,111,97)
    navy = (11,37,69)

    # background already filled
    # muted rectangle
    rounded_rect(draw, (64,64,64+420,64+420), 24, (11,37,69,20))
    # circle
    draw.ellipse((980-84,160-84,980+84,160+84), fill=cyan)
    # coral rect
    rounded_rect(draw, (840,360,840+220,360+120), 12, coral)
    # frame line
    draw.rectangle((120,110,120+720,110+420), outline=(230,238,247))

    if title:
        f_title = load_font(40,bold=True)
        f_sub = load_font(18)
        draw.text((96,220), "The New Builder Playbook for AI First Development", font=f_title, fill=navy)
        draw.text((96,260), "How to push and thrive as one new builder", font=f_sub, fill=navy)
        draw.rectangle((96,300,96+280,300+8), fill=cyan)
        draw.rectangle((392,300,392+140,300+8), fill=coral)
    # tag
    f_tag = load_font(16)
    tag_col = (11,37,69,153)
    tag_img = Image.new('RGBA', img.size, (0,0,0,0))
    tdraw = ImageDraw.Draw(tag_img)
    tdraw.text((24,h-24), "Beto Dias", font=f_tag, fill=tag_col)
    img.alpha_composite(tag_img)


def draw_diagram(img):
    w,h = img.size
    draw = ImageDraw.Draw(img)
    cyan = (0,211,255)
    coral = (255,111,97)
    navy = (11,37,69)

    rounded_rect(draw, (80,140,80+300,140+160), 12, (11,37,69,15))
    f_label = load_font(18,bold=True)
    f_small = load_font(14)
    draw.text((120,180), "Model-powered IDEs", font=f_label, fill=navy)
    draw.text((120,208), "Code suggestions · LLM code actions", font=f_small, fill=navy)

    rounded_rect(draw, (460,80,460+280,80+240), 12, (11,37,69,15))
    draw.text((500,140), "Agent Loop", font=f_label, fill=navy)
    draw.text((500,168), "Plan → Act → Observe", font=f_small, fill=navy)
    draw.ellipse((600-46,240-46,600+46,240+46), fill=(0,211,255,32))

    rounded_rect(draw, (820,140,820+300,140+160), 12, (11,37,69,15))
    draw.text((860,180), "Publishing & Measurement", font=f_label, fill=navy)
    draw.text((860,208), "Metrics · A/B · Telemetry", font=f_small, fill=navy)

    # arrows
    draw.line((380,220,460,220), fill=cyan, width=6)
    draw.line((740,220,820,220), fill=cyan, width=6)

    # supporting icons
    rounded_rect(draw, (120,340,120+120,340+80), 8, (0,211,255,32))
    draw.text((140,387), "Data", font=f_small, fill=navy)
    rounded_rect(draw, (460,360,460+120,360+80), 8, (255,111,97,32))
    draw.text((480,407), "Tools", font=f_small, fill=navy)

    # tag
    f_tag = load_font(16)
    t_img = Image.new('RGBA', img.size, (0,0,0,0))
    td = ImageDraw.Draw(t_img)
    td.text((24,h-20), "Beto Dias", font=f_tag, fill=(11,37,69,153))
    img.alpha_composite(t_img)


def draw_action_list(img):
    w,h = img.size
    draw = ImageDraw.Draw(img)
    cyan = (0,211,255)
    navy = (11,37,69)
    f_title = load_font(34,bold=True)
    f_item = load_font(20)
    draw.text((96,96), "Quick Actions", font=f_title, fill=navy)
    items = [
        "Sketch problem & core metric",
        "Build a small model-in-the-loop prototype",
        "Automate tests and checks",
        "Measure, iterate, ship",
    ]
    y = 140
    for it in items:
        draw.ellipse((96, y, 96+36, y+36), fill=cyan)
        draw.text((150, y+8), it, font=f_item, fill=navy)
        y += 56
    rounded_rect(draw, (760,120,760+320,120+320), 20, (0,211,255,20))
    f_tag = load_font(16)
    t_img = Image.new('RGBA', img.size, (0,0,0,0))
    td = ImageDraw.Draw(t_img)
    td.text((24,h-24), "Beto Dias", font=f_tag, fill=(11,37,69,153))
    img.alpha_composite(t_img)


def draw_action_agent(img):
    w,h = img.size
    draw = ImageDraw.Draw(img)
    cyan = (0,211,255)
    coral = (255,111,97)
    navy = (11,37,69)
    f_title = load_font(32,bold=True)
    f_label = load_font(16,bold=True)
    draw.text((96,96), "Agent-assisted Builder Workflow", font=f_title, fill=navy)

    rounded_rect(draw, (96,140,96+440,140+320), 12, (0,211,255,20))
    draw.text((120,180), "Code", font=f_label, fill=navy)
    draw.text((120,210), "Live suggestions · refactors", font=load_font(14), fill=navy)

    rounded_rect(draw, (560,200,560+280,200+180), 12, (255,111,97,20))
    draw.text((584,240), "Tests", font=f_label, fill=navy)
    draw.text((584,268), "Auto-checks · unit & integration", font=load_font(14), fill=navy)

    rounded_rect(draw, (880,240,880+180,240+120), 12, (0,211,255,15))
    draw.text((896,280), "Deploy", font=f_label, fill=navy)
    draw.text((896,308), "Preview · Canary", font=load_font(14), fill=navy)

    # arrows
    draw.line((536,300,560,300), fill=cyan, width=6)
    draw.line((840,300,880,300), fill=cyan, width=6)

    # assistant avatar
    draw.ellipse((520-28,380-28,520+28,380+28), fill=(0,211,255,36))
    draw.text((556,386), "Agent", font=load_font(14), fill=navy)

    f_tag = load_font(16)
    t_img = Image.new('RGBA', img.size, (0,0,0,0))
    td = ImageDraw.Draw(t_img)
    td.text((24,h-24), "Beto Dias", font=f_tag, fill=(11,37,69,153))
    img.alpha_composite(t_img)


def draw_action_endstate(img):
    w,h = img.size
    draw = ImageDraw.Draw(img)
    cyan = (0,211,255)
    coral = (255,111,97)
    navy = (11,37,69)
    draw.text((96,96), "End States", font=load_font(34,bold=True), fill=navy)
    # three boxes
    rounded_rect(draw, (96,140,96+320,140+120), 12, (0,211,255,20))
    draw.text((120,184), "Speed", font=load_font(20,bold=True), fill=navy)
    draw.text((120,216), "Faster experiments & shipping", font=load_font(14), fill=navy)

    rounded_rect(draw, (456,140,456+320,140+120), 12, (255,111,97,20))
    draw.text((480,184), "Quality", font=load_font(20,bold=True), fill=navy)
    draw.text((480,216), "More reliable outputs", font=load_font(14), fill=navy)

    rounded_rect(draw, (816,140,816+320,140+120), 12, (11,37,69,15))
    draw.text((840,184), "Collaboration", font=load_font(20,bold=True), fill=navy)
    draw.text((840,216), "Shared context & workflows", font=load_font(14), fill=navy)

    f_tag = load_font(16)
    t_img = Image.new('RGBA', img.size, (0,0,0,0))
    td = ImageDraw.Draw(t_img)
    td.text((24,h-24), "Beto Dias", font=f_tag, fill=(11,37,69,153))
    img.alpha_composite(t_img)


if __name__ == '__main__':
    specs = [
        ('cover.png', 1200, 630, 'cover'),
        ('cover_notitle.png', 1200, 630, 'cover_notitle'),
        ('diagram_flow.png', 1200, 800, 'diagram'),
        ('action_list.png', 1200, 630, 'action_list'),
        ('action_agent.png', 1200, 630, 'action_agent'),
        ('action_endstate.png', 1200, 630, 'action_endstate'),
    ]
    for name,w,h,kind in specs:
        img = Image.new('RGBA', (w,h), (247,247,246))
        if kind == 'cover':
            draw_cover(img, title=True)
        elif kind == 'cover_notitle':
            draw_cover(img, title=False)
        elif kind == 'diagram':
            img = Image.new('RGBA', (w,h), (251,251,250))
            draw_diagram(img)
        elif kind == 'action_list':
            img = Image.new('RGBA', (w,h), (251,251,250))
            draw_action_list(img)
        elif kind == 'action_agent':
            img = Image.new('RGBA', (w,h), (248,248,247))
            draw_action_agent(img)
        elif kind == 'action_endstate':
            img = Image.new('RGBA', (w,h), (251,251,251))
            draw_action_endstate(img)
        save_png(img, name)
        # save @2x
        hi = img.resize((w*2, h*2), Image.LANCZOS)
        save_png(hi, name.replace('.png','@2x.png'))

    print('Done')
