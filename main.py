# Space Invaders - Part 10
# Sound (MacOSX / Linux Only)
# Python 2.7 on Mac
import turtle
import os
import math
import random


def menu():
	option = input('''--Selecione a diiculdade --
	[1] Fácil
	[2] Médio
	[3] Difícil
	''')

	global PLAYER_SPEED
	global NUMBER_OF_ENEMIES
	global ENEMY_SPEED
	global BULLET_SPEED

	if option == "1":
		PLAYER_SPEED = 20
		NUMBER_OF_ENEMIES = 5
		ENEMY_SPEED = 2
		BULLET_SPEED = 30

	if option == "2":
		PLAYER_SPEED = 19
		NUMBER_OF_ENEMIES = 5
		ENEMY_SPEED = 5
		BULLET_SPEED = 28

	if option == "3":
		PLAYER_SPEED = 18
		NUMBER_OF_ENEMIES = 5
		ENEMY_SPEED = 10
		BULLET_SPEED = 25


menu()

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")
wn.bgpic("space_invaders_background.gif")

# Register the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
	border_pen.fd(600)
	border_pen.lt(90)
border_pen.hideturtle()

# Set the score to 0
score = 0

# Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

playerspeed = PLAYER_SPEED

# Choose a number of enemies
number_of_enemies = NUMBER_OF_ENEMIES
# Create an empty list of enemies
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
	# Create the enemy
	enemies.append(turtle.Turtle())

for enemy in enemies:
	enemy.color("red")
	enemy.shape("invader.gif")
	enemy.penup()
	enemy.speed(0)
	x = random.randint(-200, 200)
	y = random.randint(100, 250)
	enemy.setposition(x, y)

enemyspeed = ENEMY_SPEED

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = BULLET_SPEED

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"


# Move the player left and right
def move_left():
	x = player.xcor()
	x -= playerspeed
	if x < -280:
		x = - 280
	player.setx(x)


def move_right():
	x = player.xcor()
	x += playerspeed
	if x > 280:
		x = 280
	player.setx(x)


def move_up():
	y = player.ycor()
	y += playerspeed
	if y > -25:
		y = -25
	player.sety(y)


def move_down():
	y = player.ycor()
	y -= playerspeed
	if y < -280:
		y = -280
	player.sety(y)


def fire_bullet():
	# Declare bulletstate as a global if it needs to be changed
	global bulletstate
	if bulletstate == "ready":
		# os.system("afplay laser.wav&")
		bulletstate = "fire"
		# Move the bullet to the just above the player
		x = player.xcor()
		y = player.ycor() + 10
		bullet.setposition(x, y)
		bullet.showturtle()


def is_collision(t1, t2):
	distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
	if distance < 15:
		return True
	else:
		return False


# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(move_up, "Up")
turtle.onkey(move_down, "Down")
turtle.onkey(fire_bullet, "space")

# Main game loop
conditon = True
while conditon:

	for enemy in enemies:
		# Move the enemy
		x = enemy.xcor()
		x += enemyspeed
		enemy.setx(x)

		# Move the enemy back and down
		if enemy.xcor() > 280:
			# Move all enemies down
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			# Change enemy direction
			enemyspeed *= -1

		if enemy.xcor() < -280:
			# Move all enemies down
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			# Change enemy direction
			enemyspeed *= -1

		# Check for a collision between the bullet and the enemy
		if is_collision(bullet, enemy):
			# os.system("afplay explosion.wav&")
			# Reset the bullet
			bullet.hideturtle()
			bulletstate = "ready"
			bullet.setposition(0, -400)
			# Reset the enemy
			x = random.randint(-200, 200)
			y = random.randint(100, 250)
			enemy.setposition(x, y)
			# Update the score
			score += 10
			scorestring = "Score: %s" % score
			score_pen.clear()
			score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

		if is_collision(player, enemy):
			# os.system("afplay explosion.wav&")
			enemyspeed = 0
			player.hideturtle()
			enemy.hideturtle()
			print("Game Over")
			conditon = False

		if enemy.ycor() <= -280:
			enemyspeed = 0
			player.hideturtle()
			enemy.hideturtle()
			print("Game Over")
			conditon = False

	# Move the bullet
	if bulletstate == "fire":
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)

	# Check to see if the bullet has gone to the top
	if bullet.ycor() > 275:
		bullet.hideturtle()
		bulletstate = "ready"

