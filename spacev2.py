import turtle
import os
import math
import random

turtle.register_shape("player.gif")
turtle.register_shape("invader.gif")


class TurtleFactory:
    @staticmethod
    def create_turtle(color, shape, position=(0, 0), heading=90, speed=0, size=None):
        turtle_obj = turtle.Turtle()
        turtle_obj.color(color)
        turtle_obj.shape(shape)
        turtle_obj.penup()
        turtle_obj.speed(speed)
        turtle_obj.setposition(position)
        turtle_obj.setheading(heading)
        
        if size:
            turtle_obj.shapesize(size[0], size[1])

        return turtle_obj


class Player:
    def __init__(self):
        self.turtle = TurtleFactory.create_turtle("blue", "player.gif", position=(0, -250), size=(1, 1))
        self.speed = 15

    def move_left(self):
        x = self.turtle.xcor()
        x -= self.speed
        if x < -280:
            x = -280
        self.turtle.setx(x)

    def move_right(self):
        x = self.turtle.xcor()
        x += self.speed
        if x > 280:
            x = 280
        self.turtle.setx(x)


class Enemy:
    def __init__(self, position):
        self.turtle = TurtleFactory.create_turtle("red", "invader.gif", position=position)
        self.speed = 0

    def move(self, speed):
        x = self.turtle.xcor()
        x += speed
        self.turtle.setx(x)


class Bullet:
    def __init__(self):
        self.turtle = TurtleFactory.create_turtle("yellow", "triangle", size=(0.5, 0.5))
        self.speed = 20
        self.state = "ready"
        
    def fire(self):
        os.system("afplay laser.wav&")
        self.state = "fire"
        x = player.turtle.xcor()
        y = player.turtle.ycor()
        self.turtle.setposition(x, y + 10)
        self.turtle.showturtle()


def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    return distance < 15


if __name__ == "__main__":
    wn = turtle.Screen()
    wn.bgcolor("black")
    wn.title("Space Invaders")
    wn.bgpic("space_invaders_background.gif")

    TurtleFactory.create_turtle("white", "blank", position=(-300, -300), speed=0, size=None)

    score_pen = TurtleFactory.create_turtle("white", "blank", position=(-290, 280), speed=0, size=None)
    score_pen.hideturtle()

    player = Player()

    number_of_enemies = 5
    enemies = [Enemy(position=(random.randint(-200, 200), random.randint(100, 250))) for _ in range(number_of_enemies)]
    enemyspeed = 2

    bullet = Bullet()

    turtle.listen()
    turtle.onkey(player.move_left, "Left")
    turtle.onkey(player.move_right, "Right")
    turtle.onkey(bullet.fire, "space")

    score = 0

    while True:
        for enemy in enemies:
            enemy.move(enemyspeed)

            if enemy.turtle.xcor() > 280 or enemy.turtle.xcor() < -280:
                for e in enemies:
                    y = e.turtle.ycor()
                    y -= 40
                    e.turtle.sety(y)
                enemyspeed *= -1

            if is_collision(bullet.turtle, enemy.turtle):
                os.system("afplay explosion.wav&")
                bullet.turtle.hideturtle()
                bullet.state = "ready"
                bullet.turtle.setposition(0, -400)
                enemy.turtle.setposition(random.randint(-200, 200), random.randint(100, 250))
                score += 10
                score_pen.clear()
                score_pen.write("Score: %s" % score, False, align="left", font=("Arial", 14, "normal"))

            if is_collision(player.turtle, enemy.turtle):
                os.system("afplay explosion.wav&")
                player.turtle.hideturtle()
                enemy.turtle.hideturtle()
                print("Game Over")
                break

        if bullet.state == "fire":
            y = bullet.turtle.ycor()
            y += bullet.speed
            bullet.turtle.sety(y)

        if bullet.turtle.ycor() > 275:
            bullet.turtle.hideturtle()
            bullet.state = "ready"
