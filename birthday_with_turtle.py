
import turtle
import random
import math

# --- CONFIGURATION ---
BIRTHDAY_NAME = "Maida Islam"
FPS = 30
FRAME_DELAY = 1000 // FPS

# Colors
NIGHT_COLOR = "#050515"
STAR_COLORS = ["#ffffff", "#fff4e6", "#e6f2ff", "#ffffe6"]

FIREWORK_COLORS = [
    "#ff0055", "#aa00ff", "#00eeff",
    "#ffd700", "#ff3300", "#00ffaa", "#ff99cc"
]

BALLOON_COLORS = [
    "#ff4d4d", "#4d79ff", "#ffcc00",
    "#33cc33", "#cc33ff", "#ff9933"
]

# --- TEXT CONFIGURATION ---
target_text_1 = "HAPPY BIRTHDAY!"
target_text_2 = f"Happy Birthday, {BIRTHDAY_NAME}!"

target_text_3 = (
    "তোমার জীবনে আসুক নতুন নতুন আনন্দ,\n"
    "পূরণ হোক মনের সব ইচ্ছে,\n"
    "আর প্রতিটি সকাল নিয়ে আসুক নতুন সম্ভাবনা।"
)

# Text positions
TEXT_1_Y = 150
TEXT_2_Y = 180
TEXT_3_Y = 110

# --- SETUP SCREEN ---
screen = turtle.Screen()
screen.setup(width=1.0, height=1.0)
screen.bgcolor(NIGHT_COLOR)
screen.title(f"Happy Birthday, {BIRTHDAY_NAME}!")
screen.tracer(0)

# --- PENS ---
static_pen = turtle.Turtle()
static_pen.hideturtle()
static_pen.speed(0)

dynamic_pen = turtle.Turtle()
dynamic_pen.hideturtle()
dynamic_pen.speed(0)
dynamic_pen.penup()

text_pen = turtle.Turtle()
text_pen.hideturtle()
text_pen.speed(0)
text_pen.penup()

# --- CLASSES ---

class Star:
    def __init__(self):
        self.x = random.randint(
            -screen.window_width() // 2,
            screen.window_width() // 2
        )

        self.y = random.randint(
            -screen.window_height() // 2,
            screen.window_height() // 2
        )

        self.size = random.uniform(1, 3)
        self.color = random.choice(STAR_COLORS)
        self.blink_speed = random.uniform(0.05, 0.15)
        self.brightness = random.uniform(0, 2 * math.pi)

    def draw(self, pen):
        self.brightness += self.blink_speed

        current_size = self.size * (
            0.5 + 0.5 * math.sin(self.brightness)
        )

        pen.goto(self.x, self.y)
        pen.dot(current_size, self.color)


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 10)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = 255
        self.decay = random.uniform(3, 8)
        self.gravity = -0.15
        self.size = random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.vy += self.gravity
        self.y += self.vy
        self.life -= self.decay

    def draw(self, pen):
        if self.life > 0:
            pen.goto(self.x, self.y)
            pen.dot(self.size, self.color)


class Firework:
    def __init__(self):
        self.x = random.randint(
            -screen.window_width() // 2 + 100,
            screen.window_width() // 2 - 100
        )

        self.y = random.randint(
            0,
            screen.window_height() // 2 - 50
        )

        self.color = random.choice(FIREWORK_COLORS)

        self.particles = [
            Particle(self.x, self.y, self.color)
            for _ in range(40)
        ]

    def update(self):
        for p in self.particles:
            p.update()

        self.particles = [
            p for p in self.particles if p.life > 0
        ]

    def draw(self, pen):
        for p in self.particles:
            p.draw(pen)


class Balloon:
    def __init__(self):
        self.x = random.randint(
            -screen.window_width() // 2,
            screen.window_width() // 2
        )

        self.y = -screen.window_height() // 2 - 50

        self.color = random.choice(BALLOON_COLORS)
        self.speed_y = random.uniform(2, 4)

        self.wobble_speed = random.uniform(0.05, 0.1)
        self.wobble_offset = random.uniform(0, 2 * math.pi)

        self.size = random.uniform(30, 45)

    def update(self):
        self.y += self.speed_y
        self.wobble_offset += self.wobble_speed

    def draw(self, pen):
        current_x = self.x + math.sin(
            self.wobble_offset
        ) * 20

        # Balloon string
        pen.goto(current_x, self.y)
        pen.color("white")
        pen.pendown()
        pen.setheading(-90)
        pen.forward(self.size * 1.5)
        pen.penup()

        # Balloon body
        pen.goto(current_x, self.y)
        pen.dot(self.size, self.color)


# --- STATIC ASSETS (CAKE) ---

candles = []


def draw_rectangle(pen, x, y, width, height, color):
    pen.penup()
    pen.goto(x - width / 2, y)
    pen.pendown()

    pen.color(color)
    pen.begin_fill()

    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)

    pen.end_fill()
    pen.penup()


def draw_cake():

    # Base Plate
    draw_rectangle(
        static_pen, 0, -200, 300, 10, "#d9d9d9"
    )

    # Bottom Layer
    draw_rectangle(
        static_pen, 0, -190, 240, 70, "#ff99cc"
    )

    for i in range(-100, 110, 20):
        static_pen.goto(i, -155)
        static_pen.dot(10, "#ffffff")

    # Middle Layer
    draw_rectangle(
        static_pen, 0, -120, 180, 60, "#ff66a3"
    )

    for i in range(-70, 80, 20):
        static_pen.goto(i, -90)
        static_pen.dot(8, "#ffffff")

    # Top Layer
    draw_rectangle(
        static_pen, 0, -60, 120, 50, "#ff3377"
    )

    # Candles
    candle_x_positions = [-40, 0, 40]

    for cx in candle_x_positions:

        # Candle body
        draw_rectangle(
            static_pen, cx, -10, 10, 30, "#ffffff"
        )

        # Candle stripes
        draw_rectangle(
            static_pen, cx, 0, 10, 5, "#ff0000"
        )

        draw_rectangle(
            static_pen, cx, 10, 10, 5, "#ff0000"
        )

        candles.append((cx, 25))


# --- GLOBALS & STATE MACHINE ---

stars = []
fireworks = []
balloons = []

frame_count = 0
state = "INIT"

display_text = ""
display_text_2 = ""
display_text_3 = ""

text_2_index = 0
text_3_index = 0


# --- ANIMATION LOOP ---

def animate():

    global frame_count, state, display_text
    global display_text_2, display_text_3
    global text_2_index, text_3_index

    dynamic_pen.clear()

    # 1. MANAGE STARS

    if len(stars) < 150 and frame_count % 2 == 0:
        stars.append(Star())

    for star in stars:
        star.draw(dynamic_pen)

    # 2. MANAGE BALLOONS

    if frame_count > 60 and frame_count % 30 == 0:

        if random.random() > 0.3:
            balloons.append(Balloon())

    for balloon in balloons:
        balloon.update()
        balloon.draw(dynamic_pen)

    balloons[:] = [
        b for b in balloons
        if b.y - b.size < screen.window_height() // 2
    ]

    # 3. MANAGE FIREWORKS

    if frame_count > 150 and frame_count % random.randint(20, 60) == 0:
        fireworks.append(Firework())

    for fw in fireworks:
        fw.update()
        fw.draw(dynamic_pen)

    fireworks[:] = [
        fw for fw in fireworks
        if len(fw.particles) > 0
    ]

    # 4. FLICKERING CANDLE FLAMES

    if frame_count > 100:

        for cx, cy in candles:

            dynamic_pen.goto(
                cx,
                cy + random.uniform(-2, 2)
            )

            flame_size = random.uniform(8, 12)

            dynamic_pen.dot(
                flame_size, "#ffcc00"
            )

            dynamic_pen.goto(
                cx,
                cy - 2 + random.uniform(-1, 1)
            )

            dynamic_pen.dot(
                flame_size * 0.6, "#ff6600"
            )

    # 5. TEXT CHOREOGRAPHY

    if frame_count == 100:

        draw_cake()
        state = "TEXT_1"

    # =================================
    # TEXT 1 - HAPPY BIRTHDAY!
    # =================================

    if state == "TEXT_1":

        text_pen.clear()

        # Letter by letter animation
        if frame_count % 4 == 0 and len(display_text) < len(target_text_1):

            display_text += target_text_1[len(display_text)]

        text_pen.goto(0, TEXT_1_Y)
        text_pen.color("#ffd700")

        text_pen.write(
            display_text,
            align="center",
            font=("Arial", 48, "bold")
        )

        if len(display_text) == len(target_text_1) and frame_count > 300:

            state = "TEXT_2"
            display_text_2 = ""
            text_2_index = 0
            text_pen.clear()

    # =================================
    # TEXT 2 - PERSONALIZED BIRTHDAY
    # =================================

    elif state == "TEXT_2":

        text_pen.clear()

        # Letter by letter animation
        if frame_count % 3 == 0 and text_2_index < len(target_text_2):

            display_text_2 += target_text_2[text_2_index]
            text_2_index += 1

        text_pen.goto(0, TEXT_2_Y)
        text_pen.color("#00ffff")

        text_pen.write(
            display_text_2,
            align="center",
            font=("Arial", 40, "bold")
        )

        if text_2_index == len(target_text_2) and frame_count > 550:

            state = "TEXT_3"
            display_text_3 = ""
            text_3_index = 0
            text_pen.clear()

    # =================================
    # TEXT 3 - SPECIAL BIRTHDAY WISH
    # =================================

    elif state == "TEXT_3":

        text_pen.clear()

        # Keep TEXT 2 visible
        text_pen.goto(0, TEXT_2_Y)
        text_pen.color("#00ffff")

        text_pen.write(
            target_text_2,
            align="center",
            font=("Arial", 40, "bold")
        )

        # Letter by letter animation
        if frame_count % 3 == 0 and text_3_index < len(target_text_3):

            display_text_3 += target_text_3[text_3_index]
            text_3_index += 1

        # Draw Bengali text line by line
        lines = display_text_3.split("\n")

        for i, line in enumerate(lines):

            text_pen.goto(
                0,
                TEXT_3_Y - (i * 35)
            )

            text_pen.color("#ffb3ff")

            text_pen.write(
                line,
                align="center",
                font=("Nirmala UI", 20, "normal")
            )

    # UPDATE SCREEN

    screen.update()

    frame_count += 1

    screen.ontimer(
        animate,
        FRAME_DELAY
    )


# --- START ANIMATION ---

animate()

turtle.done()
