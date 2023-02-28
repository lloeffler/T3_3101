import time

from botlib.bot import Bot

def right_1(bot):
    bot.drive_steer(0.25)
    time.sleep(0.5)

def right_2(bot):
    bot.drive_steer(0.5)
    time.sleep(0.5)

def right_3(bot):
    bot.drive_steer(0.75)
    time.sleep(0.5)

def right_4(bot):
    bot.drive_steer(1)
    time.sleep(0.5)

def forward(bot, speed):
    sec = input("enter how long to drive with power 10")
    bot.drive_power(speed)
    time.sleep(int(sec))
    bot.drive_power(0)
    time.sleep(0.5)

def reset(bot):
    bot.drive_power(0)
    time.sleep(0.5)
    bot.stop_all()
    time.sleep(0.5)
    bot.drive_steer(0.25)
    time.sleep(0.5)

def set_speed():
    return int(input("enter speed between -100 and +100"))

bot = Bot()

speed = 10

bot.calibrate()

bot.drive_steer(0)

user_input = input("enter something")

while user_input is not "end":
    if user_input is "right_1":
        right_1(bot=bot)
    if user_input is "right_2":
        right_2(bot=bot)
    if user_input is "right_3":
        right_3(bot=bot)
    if user_input is "right_4":
        right_4(bot=bot)
    if user_input is "forward":
        forward(bot=bot, speed=speed)
    if user_input is "reset":
        reset(bot=bot)
    if user_input is "set_speed":
        speed = set_speed()
    user_input = input("enter something")