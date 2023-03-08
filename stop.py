from swarmrobot import SwarmRobot

# checks if the motors are coupled up correctly

if __name__ == '__main__':
    print('stopping all...')
    SwarmRobot().stop_all()
    print('done...')
