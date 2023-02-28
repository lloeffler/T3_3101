import time

from botlib.bot import Bot

# switched ports B and C

def right1(bot):
    bot.drive_steer(0.25)
    time.sleep(0.5)

def right2(bot):
    bot.drive_steer(0.5)
    time.sleep(0.5)

def right3(bot):
    bot.drive_steer(0.75)
    time.sleep(0.5)

def right4(bot):
    bot.drive_steer(1)
    time.sleep(0.5)

def left1(bot):
    bot.drive_steer(-0.25)
    time.sleep(0.5)

def left2(bot):
    bot.drive_steer(-0.5)
    time.sleep(0.5)

def left3(bot):
    bot.drive_steer(-0.75)
    time.sleep(0.5)

def left4(bot):
    bot.drive_steer(-1)
    time.sleep(0.5)

def straight(bot):
    bot.drive_steer(0)
    time.sleep(0.5)

def drive(bot, dspeed):
    print("enter how long to drive with power:")
    print(dspeed)
    sec = input(">")
    bot.drive_power(dspeed)
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
    return 20

def set_speed():
    return int(input("enter speed between -100 and +100\nx equals 1 cm per second\n>"))

def help():
    print("commands:\n")
    print("right1 -> right steer 0.25\n")
    print("right2 -> right steer 0.5\n")
    print("right3 -> right steer 0.75\n")
    print("right4 -> right steer 1\n")
    print("left1 -> left steer 0.25\n")
    print("left2 -> left steer 0.5\n")
    print("left3 -> left steer 0.75\n")
    print("left4 -> left steer 1\n")
    print("straight -> steer straight\n")
    print("drive -> enter time to drive in seconds to drive\n")
    print("set_speed -> enter new driving speed\n")
    print("reset -> resets speed and steering\n")
    print("end -> quits programm\n")
    print("help -> prints this help\n")

bot = Bot()

speed = 20

bot.calibrate()

bot.drive_steer(0)

help()

user_input = input("enter something\n>")

while user_input != "end":
    if user_input == "right1":
        right1(bot=bot)
    if user_input == "right2":
        right2(bot=bot)
    if user_input == "right3":
        right3(bot=bot)
    if user_input == "right4":
        right4(bot=bot)
    if user_input == "left1":
        left1(bot=bot)
    if user_input == "left2":
        left2(bot=bot)
    if user_input == "left3":
        left3(bot=bot)
    if user_input == "left4":
        left4(bot=bot)
    if user_input == "forward":
        drive(bot=bot, dspeed=speed)
    if user_input == "reset":
        speed = reset(bot=bot)
    if user_input == "set_speed":
        speed = set_speed()
    if user_input == "help":
        help()
    if user_input == "straight":
        straight(bot=bot)
    user_input = input("enter something\n>")