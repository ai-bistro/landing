from PIL import Image, ImageDraw, ImageFont
import math

# --- Configuration ---
W, H = 1200, 1200
PADDING = 100

# Colors - dark professional palette
NAVY = (18, 22, 36)         # Deep navy background
CHARCOAL = (35, 40, 55)     # Slightly lighter
WARM_WHITE = (245, 240, 232) # Warm cream/white
ACCENT = (200, 160, 90)      # Warm gold accent
ACCENT_DIM = (160, 125, 70)  # Dimmer gold

FONTS_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts"

# --- Create images ---
# Main logo (square, dark background)
img = Image.new("RGBA", (W, H), NAVY)
draw = ImageDraw.Draw(img)

# Load fonts
font_display = ImageFont.truetype(f"{FONTS_DIR}/YoungSerif-Regular.ttf", 130)
font_sub = ImageFont.truetype(f"{FONTS_DIR}/InstrumentSans-Regular.ttf", 36)
font_tagline = ImageFont.truetype(f"{FONTS_DIR}/InstrumentSans-Regular.ttf", 28)
font_icon_large = ImageFont.truetype(f"{FONTS_DIR}/YoungSerif-Regular.ttf", 180)
font_small = ImageFont.truetype(f"{FONTS_DIR}/DMMono-Regular.ttf", 22)

cx, cy = W // 2, H // 2

# --- Draw the cloche (serving dome) icon ---
# This is the key visual: a serving cloche that subtly incorporates neural network / data nodes

cloche_cy = cy - 80  # center of cloche area
cloche_rx = 180       # horizontal radius
cloche_ry = 120       # vertical radius

# Draw the dome as a series of arcs
# Dome outline
dome_points = []
for angle in range(180, 361):
    rad = math.radians(angle)
    x = cx + cloche_rx * math.cos(rad)
    y = cloche_cy + cloche_ry * math.sin(rad)
    dome_points.append((x, y))

# Draw dome with thick line
for i in range(len(dome_points) - 1):
    draw.line([dome_points[i], dome_points[i+1]], fill=WARM_WHITE, width=4)

# Flat base line of the dome
base_y = cloche_cy
draw.line([(cx - cloche_rx - 30, base_y), (cx + cloche_rx + 30, base_y)], fill=WARM_WHITE, width=4)

# Small handle on top
handle_y = cloche_cy - cloche_ry
draw.ellipse([cx - 18, handle_y - 18, cx + 18, handle_y + 18], fill=ACCENT, outline=WARM_WHITE, width=3)

# --- Neural network nodes inside the dome ---
# Place nodes in an organic pattern inside the dome
import random
random.seed(42)

nodes = []
# Layer 1 (top, fewer)
layer1_y = cloche_cy - 70
for i, xoff in enumerate([-55, 0, 55]):
    nodes.append((cx + xoff, layer1_y, 10))

# Layer 2 (middle)
layer2_y = cloche_cy - 25
for i, xoff in enumerate([-90, -30, 30, 90]):
    nodes.append((cx + xoff, layer2_y, 8))

# Draw connections (subtle)
for i, (x1, y1, r1) in enumerate(nodes):
    for j, (x2, y2, r2) in enumerate(nodes):
        if i < j:
            dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
            if dist < 160:
                # Opacity based on distance
                alpha = max(40, int(120 - dist * 0.6))
                draw.line([(x1, y1), (x2, y2)], fill=(*ACCENT_DIM, alpha), width=2)

# Draw nodes
for x, y, r in nodes:
    draw.ellipse([x-r, y-r, x+r, y+r], fill=ACCENT, outline=WARM_WHITE, width=2)

# --- Steam rising from the cloche (data streams) ---
# Three wavy lines of "steam" made of small dots/dashes
for stream_offset in [-40, 0, 40]:
    sx = cx + stream_offset
    for step in range(8):
        sy = cloche_cy - cloche_ry - 40 - step * 18
        wobble = math.sin(step * 0.8 + stream_offset * 0.05) * 12
        dot_r = max(2, 5 - step * 0.4)
        alpha = max(30, 180 - step * 20)
        draw.ellipse(
            [sx + wobble - dot_r, sy - dot_r, sx + wobble + dot_r, sy + dot_r],
            fill=(*ACCENT, alpha)
        )

# --- Typography ---
# "AI" text
ai_text = "AI"
ai_bbox = draw.textbbox((0, 0), ai_text, font=font_display)
ai_w = ai_bbox[2] - ai_bbox[0]

# "BISTRO" text
bistro_text = "BISTRO"
bistro_bbox = draw.textbbox((0, 0), bistro_text, font=font_display)
bistro_w = bistro_bbox[2] - bistro_bbox[0]

# Total width and positioning
total_text_w = ai_w + 30 + bistro_w  # 30px gap
text_x = (W - total_text_w) // 2
text_y = cy + 100

# Draw "AI" in accent color
draw.text((text_x, text_y), ai_text, fill=ACCENT, font=font_display)

# Draw "BISTRO" in warm white
draw.text((text_x + ai_w + 30, text_y), bistro_text, fill=WARM_WHITE, font=font_display)

# --- Tagline ---
tagline = "serving intelligent solutions"
tag_bbox = draw.textbbox((0, 0), tagline, font=font_tagline)
tag_w = tag_bbox[2] - tag_bbox[0]
tag_y = text_y + 150

# Decorative line before and after tagline
line_w = 60
line_y = tag_y + 14
tag_total = tag_w + line_w * 2 + 40
tag_start_x = (W - tag_total) // 2

draw.line([(tag_start_x, line_y), (tag_start_x + line_w, line_y)], fill=ACCENT_DIM, width=1)
draw.text(((W - tag_w) // 2, tag_y), tagline, fill=(*WARM_WHITE, 180), font=font_tagline)
draw.line([(W - tag_start_x - line_w, line_y), (W - tag_start_x, line_y)], fill=ACCENT_DIM, width=1)

# --- Subtle corner accents ---
corner_len = 40
corner_w = 2
margin = 60
# Top-left
draw.line([(margin, margin), (margin + corner_len, margin)], fill=ACCENT_DIM, width=corner_w)
draw.line([(margin, margin), (margin, margin + corner_len)], fill=ACCENT_DIM, width=corner_w)
# Top-right
draw.line([(W - margin, margin), (W - margin - corner_len, margin)], fill=ACCENT_DIM, width=corner_w)
draw.line([(W - margin, margin), (W - margin, margin + corner_len)], fill=ACCENT_DIM, width=corner_w)
# Bottom-left
draw.line([(margin, H - margin), (margin + corner_len, H - margin)], fill=ACCENT_DIM, width=corner_w)
draw.line([(margin, H - margin), (margin, H - margin - corner_len)], fill=ACCENT_DIM, width=corner_w)
# Bottom-right
draw.line([(W - margin, H - margin), (W - margin - corner_len, H - margin)], fill=ACCENT_DIM, width=corner_w)
draw.line([(W - margin, H - margin), (W - margin, H - margin - corner_len)], fill=ACCENT_DIM, width=corner_w)

# Save main logo
img.save("/home/claude/ai_bistro_logo_full.png", "PNG")
print("Full logo saved")

# --- Create icon version (just cloche + AI BISTRO, no tagline) ---
icon_size = 512
icon = Image.new("RGBA", (icon_size, icon_size), NAVY)
icon_draw = ImageDraw.Draw(icon)

# Scale everything down for icon
scale = icon_size / W
# Paste a cropped/scaled version
# Instead, create a simpler icon version

# Simple icon: cloche with nodes, compact text
icx, icy = icon_size // 2, icon_size // 2 - 40
irx, iry = 85, 60

# Dome
icon_dome_points = []
for angle in range(180, 361):
    rad = math.radians(angle)
    x = icx + irx * math.cos(rad)
    y = icy + iry * math.sin(rad)
    icon_dome_points.append((x, y))

for i in range(len(icon_dome_points) - 1):
    icon_draw.line([icon_dome_points[i], icon_dome_points[i+1]], fill=WARM_WHITE, width=3)

icon_draw.line([(icx - irx - 15, icy), (icx + irx + 15, icy)], fill=WARM_WHITE, width=3)

# Handle
handle_iy = icy - iry
icon_draw.ellipse([icx - 10, handle_iy - 10, icx + 10, handle_iy + 10], fill=ACCENT, outline=WARM_WHITE, width=2)

# Nodes inside (simplified)
for xoff, yoff in [(-30, -35), (0, -40), (30, -35), (-45, -10), (-15, -10), (15, -10), (45, -10)]:
    nx, ny = icx + xoff, icy + yoff
    icon_draw.ellipse([nx-5, ny-5, nx+5, ny+5], fill=ACCENT, outline=WARM_WHITE, width=1)

# Connections
node_positions = [(icx-30, icy-35), (icx, icy-40), (icx+30, icy-35),
                  (icx-45, icy-10), (icx-15, icy-10), (icx+15, icy-10), (icx+45, icy-10)]
for i, (x1, y1) in enumerate(node_positions):
    for j, (x2, y2) in enumerate(node_positions):
        if i < j and math.sqrt((x2-x1)**2 + (y2-y1)**2) < 80:
            icon_draw.line([(x1, y1), (x2, y2)], fill=(*ACCENT_DIM, 100), width=1)

# Steam dots
for soff in [-20, 0, 20]:
    for step in range(4):
        sy = icy - iry - 20 - step * 12
        wobble = math.sin(step * 0.8 + soff * 0.05) * 8
        dr = max(1.5, 3 - step * 0.5)
        icon_draw.ellipse([icx+soff+wobble-dr, sy-dr, icx+soff+wobble+dr, sy+dr],
                         fill=(*ACCENT, max(30, 150 - step * 30)))

# Text
icon_font = ImageFont.truetype(f"{FONTS_DIR}/YoungSerif-Regular.ttf", 62)
icon_font_sub = ImageFont.truetype(f"{FONTS_DIR}/InstrumentSans-Regular.ttf", 18)

ai_bb = icon_draw.textbbox((0, 0), "AI", font=icon_font)
bi_bb = icon_draw.textbbox((0, 0), "BISTRO", font=icon_font)
ai_iw = ai_bb[2] - ai_bb[0]
bi_iw = bi_bb[2] - bi_bb[0]
total_iw = ai_iw + 15 + bi_iw
ix_start = (icon_size - total_iw) // 2
iy_text = icy + 75

icon_draw.text((ix_start, iy_text), "AI", fill=ACCENT, font=icon_font)
icon_draw.text((ix_start + ai_iw + 15, iy_text), "BISTRO", fill=WARM_WHITE, font=icon_font)

icon.save("/home/claude/ai_bistro_icon_512.png", "PNG")
print("Icon saved")

# --- Create transparent logo version for website ---
web_logo = Image.new("RGBA", (800, 200), (0, 0, 0, 0))
web_draw = ImageDraw.Draw(web_logo)

web_font = ImageFont.truetype(f"{FONTS_DIR}/YoungSerif-Regular.ttf", 80)
web_font_tag = ImageFont.truetype(f"{FONTS_DIR}/InstrumentSans-Regular.ttf", 20)

# Mini cloche on the left
wcx, wcy = 90, 100
wrx, wry = 45, 32

web_dome_pts = []
for angle in range(180, 361):
    rad = math.radians(angle)
    x = wcx + wrx * math.cos(rad)
    y = wcy + wry * math.sin(rad)
    web_dome_pts.append((x, y))

for i in range(len(web_dome_pts) - 1):
    web_draw.line([web_dome_pts[i], web_dome_pts[i+1]], fill=WARM_WHITE, width=3)
web_draw.line([(wcx - wrx - 8, wcy), (wcx + wrx + 8, wcy)], fill=WARM_WHITE, width=3)

# Handle
web_draw.ellipse([wcx-6, wcy-wry-6, wcx+6, wcy-wry+6], fill=ACCENT, outline=WARM_WHITE, width=2)

# Small nodes
for xo, yo in [(-15, -15), (0, -18), (15, -15), (-22, -3), (0, -3), (22, -3)]:
    web_draw.ellipse([wcx+xo-3, wcy+yo-3, wcx+xo+3, wcy+yo+3], fill=ACCENT)

# Text next to icon
text_start_x = 160
ai_bb2 = web_draw.textbbox((0, 0), "AI", font=web_font)
ai_w2 = ai_bb2[2] - ai_bb2[0]
web_draw.text((text_start_x, 45), "AI", fill=ACCENT, font=web_font)
web_draw.text((text_start_x + ai_w2 + 18, 45), "BISTRO", fill=WARM_WHITE, font=web_font)

# Tagline below
tag_bb2 = web_draw.textbbox((0, 0), "serving intelligent solutions", font=web_font_tag)
web_draw.text((text_start_x + 5, 135), "serving intelligent solutions", fill=(*WARM_WHITE, 160), font=web_font_tag)

web_logo.save("/home/claude/ai_bistro_logo_horizontal.png", "PNG")
print("Horizontal logo saved")

print("\nAll logo variants created!")
