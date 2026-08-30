import pygame
import math
import random

pygame.init()

# ============================================================
# WINDOW
# ============================================================

WIDTH = 1000
HEIGHT = 1000
CX = WIDTH // 2
CY = HEIGHT // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Floral Pookalam")
clock = pygame.time.Clock()

random.seed(24)

# ============================================================
# COLORS
# ============================================================

BACKGROUND = (232, 219, 198)

DARK_PURPLE = (48, 18, 43)
DEEP_PURPLE = (77, 22, 69)

MAROON = (106, 26, 26)
RED = (150, 39, 31)
DARK_RED = (89, 20, 22)

ORANGE = (238, 103, 15)
LIGHT_ORANGE = (255, 143, 25)

YELLOW = (244, 189, 28)
LIGHT_YELLOW = (255, 222, 72)

WHITE = (252, 248, 232)
CREAM = (239, 228, 205)

PURPLE = (103, 31, 117)
LIGHT_PURPLE = (153, 75, 164)

PINK = (224, 117, 150)
LIGHT_PINK = (244, 154, 179)
DARK_PINK = (185, 73, 112)

GREEN = (61, 104, 39)
LIGHT_GREEN = (103, 144, 58)
DARK_GREEN = (35, 70, 27)

BROWN = (104, 60, 34)
DARK_BROWN = (53, 30, 20)

GOLD = (228, 176, 33)

# ============================================================
# HELPERS
# ============================================================

def clamp(v):
    return max(0, min(255, int(v)))

def lighter(c, amount):
    return (
        clamp(c[0] + amount),
        clamp(c[1] + amount),
        clamp(c[2] + amount)
    )

def darker(c, amount):
    return (
        clamp(c[0] - amount),
        clamp(c[1] - amount),
        clamp(c[2] - amount)
    )

def polar(radius, angle_deg):
    a = math.radians(angle_deg)
    return (
        CX + math.cos(a) * radius,
        CY + math.sin(a) * radius
    )

def point_radius_angle(x, y):
    dx = x - CX
    dy = y - CY
    r = math.hypot(dx, dy)
    a = (math.degrees(math.atan2(dy, dx)) + 360) % 360
    return r, a

# ============================================================
# PETAL / LEAF SPRITES
# ============================================================

def make_ellipse_petal(color, width, height):
    surf = pygame.Surface((height * 3, height * 3), pygame.SRCALPHA)
    cx = surf.get_width() // 2
    cy = surf.get_height() // 2

    pygame.draw.ellipse(
        surf,
        (0, 0, 0, 35),
        (cx - width // 2 + 1, cy - height // 2 + 2, width, height)
    )

    pygame.draw.ellipse(
        surf,
        color,
        (cx - width // 2, cy - height // 2, width, height)
    )

    pygame.draw.ellipse(
        surf,
        lighter(color, 35),
        (
            cx - max(1, width // 7),
            cy - height // 3,
            max(2, width // 3),
            max(3, height // 2)
        )
    )

    return surf


def make_leaf_sprite(color, width=9, height=25):
    surf = pygame.Surface((height * 3, height * 3), pygame.SRCALPHA)
    cx = surf.get_width() // 2
    cy = surf.get_height() // 2

    pts = [
        (cx, cy - height // 2),
        (cx + width // 2, cy),
        (cx, cy + height // 2),
        (cx - width // 2, cy),
    ]

    pygame.draw.polygon(surf, color, pts)
    pygame.draw.line(
        surf,
        lighter(color, 35),
        (cx, cy - height // 2 + 2),
        (cx, cy + height // 2 - 2),
        1
    )

    return surf


def blit_rotated(surface, sprite, x, y, angle, scale=1.0):
    transformed = pygame.transform.rotozoom(sprite, angle, scale)
    rect = transformed.get_rect(center=(int(x), int(y)))
    surface.blit(transformed, rect)

# ============================================================
# FLOWER HEADS
# ============================================================

def create_marigold(base_color, size=30):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size // 2
    cy = size // 2

    pygame.draw.circle(
        surf,
        (0, 0, 0, 26),
        (cx + 1, cy + 2),
        int(size * 0.42)
    )

    layers = [
        (18, size * 0.31, 8, 4),
        (14, size * 0.23, 7, 4),
        (11, size * 0.15, 6, 3),
        (8,  size * 0.08, 5, 3),
    ]

    for layer_no, (count, radius, ph, pw) in enumerate(layers):
        shade = darker(base_color, layer_no * 5)
        pet = make_ellipse_petal(shade, pw, ph)
        offset = random.uniform(0, 360)

        for i in range(count):
            ang = i * 360 / count + offset + random.uniform(-8, 8)
            a = math.radians(ang)
            rr = radius + random.uniform(-1.5, 1.5)

            px = cx + math.cos(a) * rr
            py = cy + math.sin(a) * rr

            blit_rotated(
                surf,
                pet,
                px,
                py,
                ang + 90,
                random.uniform(0.82, 1.12)
            )

    pygame.draw.circle(
        surf,
        darker(base_color, 20),
        (cx, cy),
        max(2, size // 15)
    )

    return surf


def create_jasmine(size=27):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size // 2
    cy = size // 2

    pet = make_ellipse_petal(
        random.choice([WHITE, CREAM]),
        max(5, int(size * 0.22)),
        max(11, int(size * 0.48))
    )

    for i in range(5):
        ang = i * 72 + random.uniform(-3, 3)
        a = math.radians(ang)
        rr = size * 0.16
        px = cx + math.cos(a) * rr
        py = cy + math.sin(a) * rr
        blit_rotated(surf, pet, px, py, ang + 90, 1.0)

    pygame.draw.circle(
        surf,
        GOLD,
        (cx, cy),
        max(2, int(size * 0.08))
    )

    return surf


def create_chrysanthemum(base_color, size=30):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size // 2
    cy = size // 2

    for layer in range(4):
        count = 14 + layer * 3
        radius = size * (0.30 - layer * 0.055)
        color = lighter(base_color, layer * 10)

        pet = make_ellipse_petal(
            color,
            max(3, int(size * 0.10)),
            max(9, int(size * 0.34))
        )

        for i in range(count):
            ang = i * 360 / count + random.uniform(-5, 5)
            a = math.radians(ang)
            px = cx + math.cos(a) * radius
            py = cy + math.sin(a) * radius

            blit_rotated(
                surf,
                pet,
                px,
                py,
                ang + 90,
                random.uniform(0.88, 1.06)
            )

    pygame.draw.circle(
        surf,
        darker(base_color, 15),
        (cx, cy),
        max(2, size // 14)
    )

    return surf


def create_leaf_cluster(size=28):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size // 2
    cy = size // 2

    for i in range(7):
        ang = i * 360 / 7 + random.uniform(-8, 8)
        a = math.radians(ang)
        rr = size * 0.14

        px = cx + math.cos(a) * rr
        py = cy + math.sin(a) * rr

        color = random.choice([GREEN, LIGHT_GREEN, DARK_GREEN])
        leaf = make_leaf_sprite(
            color,
            max(5, int(size * 0.20)),
            max(12, int(size * 0.52))
        )

        blit_rotated(surf, leaf, px, py, ang + 90, 1.0)

    return surf

# ============================================================
# FLOWER LIBRARY
# ============================================================

FLOWERS = {
    "dark": [],
    "red": [],
    "orange": [],
    "yellow": [],
    "white": [],
    "purple": [],
    "pink": [],
    "green": [],
}

for _ in range(9):
    FLOWERS["dark"].append(
        create_chrysanthemum(
            random.choice([DARK_PURPLE, DEEP_PURPLE]),
            random.randint(25, 31)
        )
    )

    FLOWERS["red"].append(
        create_marigold(
            random.choice([RED, MAROON, DARK_RED]),
            random.randint(27, 33)
        )
    )

    FLOWERS["orange"].append(
        create_marigold(
            random.choice([ORANGE, LIGHT_ORANGE]),
            random.randint(27, 34)
        )
    )

    FLOWERS["yellow"].append(
        create_marigold(
            random.choice([YELLOW, LIGHT_YELLOW]),
            random.randint(27, 34)
        )
    )

    FLOWERS["white"].append(
        create_jasmine(random.randint(24, 29))
    )

    FLOWERS["purple"].append(
        create_chrysanthemum(
            random.choice([PURPLE, LIGHT_PURPLE]),
            random.randint(26, 32)
        )
    )

    FLOWERS["pink"].append(
        create_chrysanthemum(
            random.choice([PINK, LIGHT_PINK, DARK_PINK]),
            random.randint(25, 31)
        )
    )

    FLOWERS["green"].append(
        create_leaf_cluster(random.randint(24, 30))
    )


def place_flower(surface, x, y, flower_type, scale=1.0):
    sprite = random.choice(FLOWERS[flower_type])

    transformed = pygame.transform.rotozoom(
        sprite,
        random.uniform(-18, 18),
        scale * random.uniform(0.88, 1.10)
    )

    rect = transformed.get_rect(center=(int(x), int(y)))
    surface.blit(transformed, rect)

# ============================================================
# PETAL-SHAPED OUTER EDGE
# ============================================================

OUTER_PETALS = 18

def outer_radius(angle_deg):
    theta = math.radians(angle_deg * OUTER_PETALS)

    # 0 at valley, 1 at petal tip
    lobe = (math.cos(theta) + 1) / 2

    # sharper petal tips
    lobe = lobe ** 3.0

    return 375 + 82 * lobe

# ============================================================
# COLOR REGION LOGIC
# ============================================================

def region_for_point(x, y):
    r, angle = point_radius_angle(x, y)
    edge = outer_radius(angle)

    if r > edge:
        return None

    # PURPLE FLOWER EDGE
    if r > edge - 24:
        return "purple"

    # OUTER PETAL REGION
    if r > 330:
        phase = (angle * OUTER_PETALS / 360.0) % 1.0
        center_dist = abs(phase - 0.5)

        if r > 372:
            if center_dist < 0.14:
                return "white"
            elif center_dist < 0.28:
                return "yellow"
            elif center_dist < 0.40:
                return "orange"
            return "red"

        if center_dist < 0.15:
            return "yellow"
        elif center_dist < 0.30:
            return "orange"
        elif center_dist < 0.42:
            return "red"
        return "purple"

    # WHITE SEPARATOR
    if 310 < r <= 330:
        return "white"

    # INNER ORANGE/YELLOW RING
    if 225 < r <= 310:
        section = angle % 30
        d = abs(section - 15)

        if d < 3.3:
            return "white"
        elif d < 6.5:
            return "yellow"
        elif d < 10.5:
            return "orange"
        else:
            return "red"

    # WHITE INNER RING
    if 205 < r <= 225:
        return "white"

    # PINK CENTRE
    if r <= 205:
        return "pink"

    return None

# ============================================================
# BUILD DENSE FLOWER CARPET
# ============================================================

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(BACKGROUND)

# NOTE:
# There is NO giant purple circle behind the design anymore.

spacing_x = 10
spacing_y = 8

row = 0

for y in range(CY - 460, CY + 461, spacing_y):
    x_offset = 0 if row % 2 == 0 else spacing_x // 2

    for x in range(CX - 460 + x_offset, CX + 461, spacing_x):
        flower_type = region_for_point(x, y)

        if flower_type is None:
            continue

        place_flower(
            canvas,
            x + random.uniform(-2.2, 2.2),
            y + random.uniform(-2.2, 2.2),
            flower_type,
            random.uniform(0.58, 0.74)
        )

    row += 1

# ============================================================
# EXTRA PURPLE FLOWERS ON OUTER PETAL TIPS
# ============================================================

for i in range(OUTER_PETALS):
    angle = i * 360 / OUTER_PETALS
    tip_radius = outer_radius(angle) - 10

    x, y = polar(tip_radius, angle)
    place_flower(canvas, x, y, "purple", 0.88)

    for offset in [-5, -3, 3, 5]:
        x, y = polar(tip_radius - 12, angle + offset)
        place_flower(canvas, x, y, "purple", 0.72)

    for offset in [-6, -3, 0, 3, 6]:
        x, y = polar(tip_radius - 25, angle + offset)
        place_flower(canvas, x, y, "purple", 0.64)

# ============================================================
# CLEAN WHITE FLOWER RINGS
# ============================================================

for radius in (320, 215):
    count = int((2 * math.pi * radius) / 10)

    for i in range(count):
        ang = i * 360 / count
        x, y = polar(radius, ang)
        place_flower(canvas, x, y, "white", 0.52)

# ============================================================
# PURPLE TEARDROP CLUSTERS
# ============================================================

def add_purple_teardrop(angle_deg, radius=265):
    for row in range(8):
        t = row / 7
        rr = radius + (t - 0.5) * 40
        half_width = 10 * (1 - abs(t - 0.5) * 2)

        for _ in range(3):
            side = random.uniform(-half_width, half_width)
            a = angle_deg + side * 0.18
            x, y = polar(rr, a)

            place_flower(
                canvas,
                x,
                y,
                "purple",
                random.uniform(0.40, 0.52)
            )

for i in range(12):
    add_purple_teardrop(i * 30 + 15)

# ============================================================
# RE-COVER CENTRE IN PINK FLOWERS
# ============================================================

for y in range(CY - 195, CY + 196, 9):
    for x in range(CX - 195, CX + 196, 9):
        if (x - CX) ** 2 + (y - CY) ** 2 <= 195 ** 2:
            place_flower(
                canvas,
                x + random.uniform(-2, 2),
                y + random.uniform(-2, 2),
                "pink",
                random.uniform(0.44, 0.56)
            )

# ============================================================
# COCONUT TREE
# ============================================================

trunk_points = []

for i in range(24):
    t = i / 23

    y = CY + 70 - t * 155
    x = CX - 28 + math.sin(t * 1.8) * 22

    trunk_points.append((x, y))

    pygame.draw.circle(
        canvas,
        DARK_BROWN,
        (int(x), int(y)),
        8
    )

    pygame.draw.circle(
        canvas,
        BROWN,
        (int(x - 2), int(y - 2)),
        5
    )

tree_x, tree_y = trunk_points[-1]

# coconuts
for dx, dy in [(-9, 6), (0, 2), (9, 6), (2, 12)]:
    pygame.draw.circle(
        canvas,
        DARK_BROWN,
        (int(tree_x + dx), int(tree_y + dy)),
        7
    )

    pygame.draw.circle(
        canvas,
        BROWN,
        (int(tree_x + dx - 1), int(tree_y + dy - 1)),
        5
    )


def draw_palm_frond(start_x, start_y, angle_deg, length=82, bend=22):
    points = []

    for i in range(13):
        t = i / 12
        a = math.radians(angle_deg)

        x = start_x + math.cos(a) * length * t
        y = start_y + math.sin(a) * length * t + bend * t * t

        points.append((x, y))

    pygame.draw.lines(
        canvas,
        DARK_GREEN,
        False,
        [(int(x), int(y)) for x, y in points],
        3
    )

    leaf_sprite = make_leaf_sprite(LIGHT_GREEN, 6, 20)

    for i in range(3, 12):
        x, y = points[i]
        stem_angle = angle_deg + i * 0.5

        for side in (-1, 1):
            leaf_angle = stem_angle + side * 62

            blit_rotated(
                canvas,
                leaf_sprite,
                x,
                y,
                leaf_angle,
                random.uniform(0.72, 0.95)
            )


for ang in (188, 205, 222, 240, 258, 278, 298, 318, 338, 354):
    draw_palm_frond(
        tree_x,
        tree_y,
        ang,
        random.randint(70, 88),
        random.randint(12, 25)
    )

# ============================================================
# BIGGER FLOWER BOAT
# ============================================================

boat_y = CY + 88

for i in range(190):
    t = i / 189 * 2 - 1

    x = CX + t * 180
    curve = 48 * (1 - t * t)
    y = boat_y + curve

    for row_offset in (0, 7, 14, 21, 28, 35):
        place_flower(
            canvas,
            x + random.uniform(-1.5, 1.5),
            y + row_offset,
            "red" if row_offset > 2 else "dark",
            0.42
        )

# raised pointed ends
for side in (-1, 1):
    base_x = CX + side * 176

    for step in range(15):
        x = base_x + side * step * 2.1
        y = boat_y + 10 - step * 6

        place_flower(
            canvas,
            x,
            y,
            "red",
            0.44
        )

# yellow flower chain
for i in range(23):
    t = i / 22 * 2 - 1

    x = CX + t * 145
    curve = 37 * (1 - t * t)
    y = boat_y + curve + 7

    place_flower(
        canvas,
        x,
        y,
        "yellow",
        0.40
    )

# ============================================================
# LOTUS FLOWERS BELOW BOAT
# ============================================================

def draw_lotus(x, y, scale=1.0):
    leaf = make_leaf_sprite(DARK_GREEN, 10, 24)

    for ang in (225, 260, 300, 335):
        blit_rotated(
            canvas,
            leaf,
            x + math.cos(math.radians(ang)) * 8,
            y + math.sin(math.radians(ang)) * 5,
            ang,
            0.7 * scale
        )

    pet = make_ellipse_petal(LIGHT_PINK, 8, 18)
    pet2 = make_ellipse_petal(PINK, 8, 18)

    for ang in (210, 240, 270, 300, 330):
        a = math.radians(ang)
        px = x + math.cos(a) * 8 * scale
        py = y + math.sin(a) * 5 * scale
        blit_rotated(canvas, pet, px, py, ang + 90, scale)

    for ang in (235, 270, 305):
        a = math.radians(ang)
        px = x + math.cos(a) * 4 * scale
        py = y + math.sin(a) * 3 * scale
        blit_rotated(canvas, pet2, px, py, ang + 90, 0.9 * scale)

    pygame.draw.circle(
        canvas,
        GOLD,
        (int(x), int(y)),
        max(2, int(3 * scale))
    )


draw_lotus(CX - 105, CY + 170, 0.90)
draw_lotus(CX - 55, CY + 185, 0.78)
draw_lotus(CX + 5, CY + 185, 0.82)
draw_lotus(CX + 65, CY + 178, 0.76)
draw_lotus(CX + 115, CY + 160, 0.72)

# ============================================================
# DISPLAY
# ============================================================

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()