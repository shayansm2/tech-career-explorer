from time import sleep

def check_till_true(function):
    while not function():
        print('result is false so I will sleep for 1 min.')
        sleep(60)
    return True