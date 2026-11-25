from pathlib import Path
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2200
PAPER = "#f7f2e7"
INK = "#1a1a1a"
RED = "#c0392b"
BLUE = "#1f3a5f"
GREEN = "#73b83f"
PALE_GREEN = "#dcebc9"
MUTED = "#5c5a55"
WHITE = "#ffffff"


def load_font(size, bold=False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


FONT_16 = load_font(16)
FONT_17 = load_font(17)
FONT_18 = load_font(18)
FONT_20 = load_font(20)
FONT_21 = load_font(21, True)
FONT_22 = load_font(22, True)
FONT_24 = load_font(24, True)
FONT_28 = load_font(28, True)
FONT_36 = load_font(36, True)
FONT_76 = load_font(76, True)
FONT_88 = load_font(88, True)

REGIONS = [
    ("EUROPE", "rocket", [
        ("NATO VOWS SPACE DEFENCE", "After reports Russia readies a nuclear-armed satellite."),
        ("EU'S 22ND SANCTIONS PACK", "Targets Russian banks, crypto platforms and sports teams."),
        ("UKRAINE SINKS RUSSIAN SHIP", "Warship sunk off Libya; 2 Libyan soldiers killed."),
        ("KYIV HITS FINLAND GULF SHIP", "Zelensky confirms strike on Russian cargo ship."),
        ("RUSSIAN JETS ENTER K-ADIZ", "South Korea reports jets in its air defence zone."),
        ("WILLIAM HOME BREAK-IN", "Two men arrested after Anmer Hall break-in."),
    ]),
    ("ASIA-PACIFIC", "chart", [
        ("SHENZHOU-24 LIFTS OFF", "First foreign astronaut joins the Tiangong crew."),
        ("BANGLADESH WAGE WIN +36%", "Garment workers win minimum wage rise after protests."),
        ("MINERS TRAPPED IN INDONESIA", "Dozens stuck in a 100-metre-deep mine after rains."),
        ("SOLOMONS PICK AUSTRALIA", "Security pact names Australia top partner, signed 25 Nov."),
        ("PYONGYANG EXPELS SWISS", "Envoy Sylvain Astier out; office ordered shut in 48 hours."),
        ("KOREA MINISTER QUITS", "Education chief resigns over exam cheating scandal."),
        ("INDIA BLOCKS 'COCKROACH' CHIEF", "Drive leader stopped from flying to London."),
    ]),
    ("MIDDLE EAST", "gavel", [
        ("SAUDI STRIKES HODEIDAH", "Coalition hits Yemen port; Houthis threaten Jeddah."),
        ("TANKER HIT IN HORMUZ", "3 ships hit Monday; Brent +2.3% Tuesday, slips Wednesday."),
        ("GAZA STRIKES KILL 7", "Israeli strikes kill a senior security official."),
        ("WHO: END CUBA FUEL BLOCKADE", "Director urges US to lift the fuel blockade."),
        ("IRAN VOWS 'ALL MEANS'", "Tehran vows to counter US blockade; fertiliser down 40%."),
    ]),
    ("AFRICA", "leaf", [
        ("EBOLA: VIOLENCE RISES", "Attacks on women and girls surge in Congo."),
        ("REBELS RETREAT IN E. CONGO", "Group pulls back after heavy clashes."),
        ("SENEGAL REGAINS CAN TITLE", "CAS returns 2025 African crown, 10 months on."),
        ("VANTARA-MADAGASCAR PACT", "10-year wildlife conservation deal signed."),
    ]),
    ("AMERICAS", "handshake", [
        ("CARTAGENA HOSTAGES FREED", "All 25–30 freed after failed cash-truck robbery."),
        ("PLANE CRASH KILLS 6", "Small plane down in Gulf of Mexico, including 2 children."),
        ("ABREGO GARCIA LEAVES US", "Deportation battle ends as he flies to Spain."),
        ("FORT HOOD SURVIVORS BARRED", "Denied execution attendance for Nidal Hasan."),
        ("THOMAS MARKLE CHARGED", "Indicted in US over abuse material."),
        ("TRUMP TARIFFS ON 16 NATIONS", "New levies planned after trade probe."),
    ]),
    ("MARKETS & TECH", "chart", [
        ("HUANG RETURNS TO NVIDIA", "Unanimous board vote; Trump brokered it; +30% then -5%."),
        ("DOW TOPS 50,000", "Dow +0.85% to 50,018.70; S&P -0.50%; Nasdaq -1.48%."),
        ("AI STAFF FEAR UNSAFE MODELS", "Anthropic and OpenAI workers warn of unreleased models."),
        ("SPACEX-TESLA $3.5T TIE-UP", "5-member group advances mega-merger; Broadcom patches 23 flaws."),
    ]),
    ("SCIENCE & CLIMATE", "leaf", [
        ("QIANFAN RIVALS STARLINK", "China's satellite mega-constellation answers SpaceX."),
        ("MISS UNIVERSE MAKES HISTORY", "Miss Puerto Rico wins, first mother to take the crown."),
        ("HUAWEI GUILTY", "US court: stole trade secrets, cleared of racketeering."),
    ]),
]


def fit_text(draw, text, font, max_width):
    if draw.textlength(text, font=font) <= max_width:
        return text
    shortened = text
    while shortened and draw.textlength(shortened + "…", font=font) > max_width:
        shortened = shortened[:-1]
    return shortened.rstrip() + "…"


def draw_icon(draw, cx, cy, kind, size=30):
    x0, y0 = cx - size // 2, cy - size // 2
    x1, y1 = x0 + size, y0 + size
    color = RED if kind in ("gavel", "handshake") else BLUE
    if kind == "rocket":
        draw.ellipse((cx - 7, y0 + 1, cx + 7, y0 + 22), fill=color)
        draw.polygon([(cx - 6, y0 + 10), (x0 + 1, y0 + 24), (cx - 5, y0 + 21)], fill=RED)
        draw.polygon([(cx + 6, y0 + 10), (x1 - 1, y0 + 24), (cx + 5, y0 + 21)], fill=RED)
        draw.ellipse((cx - 3, y0 + 7, cx + 3, y0 + 13), fill=PAPER)
        draw.polygon([(cx - 4, y0 + 22), (cx, y1), (cx + 4, y0 + 22)], fill="#e39a37")
    elif kind == "chart":
        draw.line((x0 + 2, y1 - 2, x0 + 2, y0 + 2, x1 - 1, y0 + 2), fill=color, width=2)
        points = [(x0 + 5, y1 - 7), (x0 + 12, y0 + 17), (x0 + 18, y0 + 20), (x1 - 4, y0 + 5)]
        draw.line(points, fill=GREEN, width=4, joint="curve")
        draw.polygon([(x1 - 5, y0 + 3), (x1 - 1, y0 + 4), (x1 - 4, y0 + 9)], fill=GREEN)
    elif kind == "gavel":
        draw.line((cx - 7, cy + 7, cx + 7, cy - 7), fill=color, width=6)
        draw.line((cx - 11, cy + 12, cx + 7, cy + 12), fill=color, width=3)
        draw.line((cx - 9, cy + 14, cx + 10, cy + 14), fill=color, width=2)
        draw.line((cx - 11, cy - 11, cx - 5, cy - 5), fill=color, width=7)
        draw.line((cx + 2, cy - 18, cx + 8, cy - 12), fill=color, width=7)
    elif kind == "leaf":
        draw.ellipse((x0 + 4, y0 + 2, x1 - 3, y1 - 3), fill=GREEN)
        draw.line((cx - 7, cy + 8, cx + 7, cy - 8), fill=BLUE, width=2)
        draw.line((cx, cy, cx + 7, cy + 2), fill=BLUE, width=2)
    elif kind == "handshake":
        draw.line((x0 + 1, cy - 2, cx - 6, cy + 2, cx, cy + 8, cx + 6, cy + 1, x1 - 1, cy - 3), fill=color, width=5, joint="curve")
        draw.line((x0 + 1, cy - 2, x0 + 5, cy - 9), fill=BLUE, width=4)
        draw.line((x1 - 1, cy - 3, x1 - 5, cy - 10), fill=BLUE, width=4)
    else:
        draw.ellipse((x0 + 5, y0 + 5, x1 - 5, y1 - 5), fill=color)


def draw_story(draw, x, y, width, headline, detail, icon_kind, row_height=50):
    draw_icon(draw, x + 21, y + row_height // 2, icon_kind, 27)
    text_x = x + 48
    text_width = width - 57
    head = fit_text(draw, headline, FONT_20, text_width)
    detail_line = fit_text(draw, detail, FONT_16, text_width)
    draw.text((text_x, y + 3), head, font=FONT_20, fill=INK)
    draw.text((text_x, y + 27), detail_line, font=FONT_16, fill=MUTED)
    draw.line((text_x, y + row_height - 1, x + width - 3, y + row_height - 1), fill="#d8d1c3", width=1)


def draw_region(draw, box, name, stories, icon_kind, row_height):
    x, y, width, height = box
    header_h = 38
    draw.rectangle((x, y, x + width, y + header_h), fill=BLUE)
    draw.text((x + 13, y + 5), name, font=FONT_24, fill=WHITE)
    count_label = f"{len(stories)} STORIES"
    count_w = draw.textlength(count_label, font=FONT_16)
    draw.text((x + width - count_w - 12, y + 11), count_label, font=FONT_16, fill=WHITE)
    story_y = y + header_h + 3
    for headline, detail in stories:
        draw_story(draw, x + 1, story_y, width - 2, headline, detail, icon_kind, row_height)
        story_y += row_height


def draw_masthead(draw):
    draw.text((55, 25), "THE WORLD IN ONE DAY", font=FONT_76, fill=INK)
    draw.text((60, 112), "Wednesday, 25 November 2026", font=FONT_28, fill=BLUE)
    right_note = "35 stories · 7 regions"
    note_w = draw.textlength(right_note, font=FONT_24)
    draw.text((1545 - note_w, 120), right_note, font=FONT_24, fill=INK)
    draw.rectangle((55, 158, 1545, 165), fill=RED)


def draw_hero(draw):
    left, top, right, bottom = 55, 178, 1545, 590
    draw.rectangle((left, top, right, bottom), fill="#eee8da", outline="#bcb4a5", width=2)
    draw.text((82, 190), "BREAKING · THE CEO IS BACK", font=FONT_18, fill=RED)

    chip_box = (920, 218, 1200, 425)
    draw.rectangle(chip_box, fill="#204e35", outline=INK, width=5)
    draw.rectangle((945, 242, 1175, 401), fill=GREEN, outline="#173b2b", width=4)
    for x in range(958, 1160, 27):
        for y in range(255, 390, 27):
            tone = "#a8d76f" if ((x // 27 + y // 27) % 2 == 0) else "#5f9f43"
            draw.rectangle((x, y, x + 18, y + 18), fill=tone)
    draw.rectangle((1000, 285, 1120, 357), fill="#173b2b", outline=PAPER, width=3)
    draw.text((1018, 302), "NVIDIA", font=FONT_24, fill=WHITE)
    for x in range(936, 1190, 28):
        draw.line((x, 208, x, 218), fill=INK, width=4)
        draw.line((x, 425, x, 435), fill=INK, width=4)
    for y in range(230, 420, 28):
        draw.line((910, y, 920, y), fill=INK, width=4)
        draw.line((1200, y, 1210, y), fill=INK, width=4)

    draw.line((1228, 412, 1228, 239, 1518, 239), fill=INK, width=3)
    chart_points = [(1245, 390), (1290, 355), (1330, 363), (1370, 310), (1410, 284), (1450, 253), (1490, 218), (1520, 245)]
    draw.line(chart_points, fill=RED, width=8, joint="curve")
    draw.polygon([(1520, 245), (1496, 238), (1511, 260)], fill=RED)
    draw.text((1250, 252), "+30%", font=FONT_22, fill=BLUE)
    draw.text((1420, 395), "−5%", font=FONT_20, fill=RED)

    draw.ellipse((270, 236, 370, 336), fill="#d5a77e", outline=INK, width=3)
    draw.arc((268, 224, 373, 330), 188, 350, fill=INK, width=13)
    draw.rectangle((300, 326, 340, 354), fill="#c8946d")
    draw.polygon([(221, 414), (244, 354), (290, 333), (350, 333), (397, 355), (419, 414)], fill="#161819", outline=INK)
    draw.line((300, 346, 320, 414), fill="#55595a", width=5)
    draw.line((347, 347, 328, 414), fill="#55595a", width=5)
    draw.line((285, 368, 257, 401), fill="#303536", width=5)
    draw.line((362, 368, 391, 401), fill="#303536", width=5)
    draw.text((208, 420), "JENSEN HUANG", font=FONT_16, fill=INK)
    draw.text((452, 294), "11 DAYS", font=FONT_28, fill=RED)
    draw.text((452, 330), "away from the helm", font=FONT_18, fill=INK)
    draw.line((560, 360, 830, 360), fill="#8a887f", width=2)
    draw.polygon([(830, 360), (815, 352), (815, 368)], fill="#8a887f")
    draw.text((640, 292), "UNANIMOUS BOARD VOTE", font=FONT_16, fill=BLUE)

    headline = "HUANG IS BACK — NVIDIA'S $3 TRILLION COMEBACK"
    hero_font = load_font(44, True)
    draw.text((82, 452), fit_text(draw, headline, hero_font, 1430), font=hero_font, fill=INK)
    subhead = "Board unanimously reinstates Jensen Huang 11 days after he quit — Trump brokered it. Shares +30% Monday, -5% Tuesday."
    sub_font = load_font(20)
    draw.text((84, 519), fit_text(draw, subhead, sub_font, 1430), font=sub_font, fill=INK)


def draw_footer(draw):
    y = 2070
    draw.rectangle((55, y, 1545, y + 96), fill="#e9e2d3", outline="#bcb4a5", width=1)
    draw.rectangle((55, y, 1545, y + 5), fill=RED)
    draw.text((75, y + 18), "ONE YEAR AFTER TAI PO — Hong Kong fire survivors struggle with loss and a lingering sense of injustice.", font=FONT_17, fill=INK)
    draw.text((75, y + 57), "Sources: wire reports and official statements, 25 November 2026.", font=FONT_16, fill=MUTED)


def main():
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    draw_masthead(draw)
    draw_hero(draw)

    column_w = 720
    left_x, right_x = 55, 825
    draw_region(draw, (left_x, 610, column_w, 414), *REGIONS[0][::2], REGIONS[0][1], 51)
    draw_region(draw, (right_x, 610, column_w, 414), REGIONS[1][0], REGIONS[1][2], REGIONS[1][1], 51)
    draw_region(draw, (left_x, 1035, column_w, 333), REGIONS[2][0], REGIONS[2][2], REGIONS[2][1], 56)
    draw_region(draw, (right_x, 1035, column_w, 333), REGIONS[3][0], REGIONS[3][2], REGIONS[3][1], 56)
    draw_region(draw, (left_x, 1375, column_w, 375), REGIONS[4][0], REGIONS[4][2], REGIONS[4][1], 55)
    draw_region(draw, (right_x, 1375, column_w, 375), REGIONS[5][0], REGIONS[5][2], REGIONS[5][1], 55)
    draw_region(draw, (55, 1760, 1490, 280), REGIONS[6][0], REGIONS[6][2], REGIONS[6][1], 67)
    draw_footer(draw)

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "entry.png"
    image.save(output_path, format="PNG", optimize=False)
    print(f"Wrote {output_path}: {image.width}x{image.height}, {output_path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
