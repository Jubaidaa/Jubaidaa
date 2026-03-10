from PIL import Image, ImageDraw, ImageFont
import random, os

BASE_CHARSET = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%.+?')
BLOCK_CHARS  = [chr(0x2588)] * 6 + [chr(0x2592)] * 5
CHARSET_FULL  = BASE_CHARSET + BLOCK_CHARS
CHARSET_CLEAN = BASE_CHARSET

COLOR = (148, 201, 228)   # #94c9e4
BG    = (13, 17, 23)      # GitHub dark background
SHUFFLE_MS      = 45
SCRAMBLE_FRAMES = 55      # ~2.5s reveal per line
PAUSE_FRAMES    = int(0.5 * 1000 / 45)   # ~11 frames pause between lines
HOLD_FRAMES     = int(8.0 * 1000 / 45)   # ~178 frames hold
BLOCK_RATIO     = 0.2     # block chars only in first 20% of frames

LINE1 = '_Noah.Matthieu.Abi.Chahla_'
LINE2 = '_5.years.of.Coding.Experience_' # to change as the years go by

FONT_PATH = 'C:/Windows/Fonts/cour.ttf'
FONT_SIZE = 22
W, H = 620, 90

font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

def text_size(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0], bb[3] - bb[1]

def render_frame(line1_chars, line2_chars):
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    tw1, th1 = text_size(d, LINE1, font)
    tw2, th2 = text_size(d, LINE2, font)
    x1 = (W - tw1) // 2
    x2 = (W - tw2) // 2
    y1 = (H // 2) - th1 - 4
    y2 = (H // 2) + 4
    d.text((x1, y1), ''.join(line1_chars), font=font, fill=COLOR)
    d.text((x2, y2), ''.join(line2_chars), font=font, fill=COLOR)
    return img

def get_char(target, char_idx, total_chars, frame, total_frames):
    # Left-to-right staggered reveal: char i locks in at its proportional frame
    lock_frame = int((char_idx + 1) / total_chars * total_frames)
    if frame >= lock_frame:
        return target
    if frame < int(total_frames * BLOCK_RATIO):
        return random.choice(CHARSET_FULL)
    else:
        return random.choice(CHARSET_CLEAN)

frames = []
durations = []

# Phase 1: Line 1 reveal
placeholder2 = [' '] * len(LINE2)
for f in range(SCRAMBLE_FRAMES):
    c1 = [get_char(LINE1[i], i, len(LINE1), f, SCRAMBLE_FRAMES) for i in range(len(LINE1))]
    frames.append(render_frame(c1, placeholder2))
    durations.append(SHUFFLE_MS)

# Phase 2: Pause — line 1 final, line 2 shuffling
final1 = list(LINE1)
for f in range(PAUSE_FRAMES):
    c2 = [random.choice(CHARSET_CLEAN) for _ in range(len(LINE2))]
    frames.append(render_frame(final1, c2))
    durations.append(SHUFFLE_MS)

# Phase 3: Line 2 reveal
for f in range(SCRAMBLE_FRAMES):
    c2 = [get_char(LINE2[i], i, len(LINE2), f, SCRAMBLE_FRAMES) for i in range(len(LINE2))]
    frames.append(render_frame(final1, c2))
    durations.append(SHUFFLE_MS)

# Phase 4: Hold
hold_frame = render_frame(list(LINE1), list(LINE2))
for _ in range(HOLD_FRAMES):
    frames.append(hold_frame)
    durations.append(SHUFFLE_MS)

out_path = 'photos/header.gif'
frames[0].save(out_path, save_all=True, append_images=frames[1:], loop=0, duration=durations, optimize=False)
print(f"Done: {len(frames)} frames, {sum(durations)/1000:.1f}s, {os.path.getsize(out_path)//1024}KB")
