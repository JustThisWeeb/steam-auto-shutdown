import psutil
from time import sleep
import os
from datetime import datetime
from PIL import ImageGrab


def get_steam_process(): #this just gets the current steam process' pid and returns it.
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() == 'steam.exe':
            return psutil.Process(process.info['pid'])
    return None

def check_steam_activity(process):
    initial_io = process.io_counters()
    initial_net = psutil.net_io_counters()

    sleep(4)

    final_io = process.io_counters()
    final_net = psutil.net_io_counters()

    read_bytes = final_io.read_bytes - initial_io.read_bytes
    write_bytes = final_io.write_bytes - initial_io.write_bytes
    net_bytes_sent = final_net.bytes_sent - initial_net.bytes_sent
    net_bytes_recv = final_net.bytes_recv - initial_net.bytes_recv

    return {
        'read_bytes': read_bytes,
        'write_bytes': write_bytes,
        'net_bytes_sent': net_bytes_sent,
        'net_bytes_recv': net_bytes_recv
    }

def main_steam(shutdown, screenshot):
    print("Steam it is")
    print(f"{'shutdown' if shutdown else 'restart'} it is")
    print(f"{'screenshot' if screenshot else 'no screenshot'} it is")
    while True:
        steam_process = get_steam_process()
        if steam_process:
            activity = check_steam_activity(steam_process)
            if activity['write_bytes'] > 0 and activity['net_bytes_recv'] > 0:
                print("Steam seems to still be downloading or installing something")
                continue
            else:
                if screenshot:
                    make_screenshot()
                print("Steam seems to have stopped with the download of the game... Shutting down")
                if shutdown:
                    sleep(1)
                    os.system("shutdown /s /t 0")
                    print("Shut down")
                else:
                    sleep(1)
                    os.system("shutdown /r /t 0")
                    print("Restarted")
        else:
            print("Steam process not found... exiting.")
            sleep(3)
            exit()






def get_epic_games_process(): #same as the steam equivalent
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'].lower() in ['epicgameslauncher.exe', 'epicgameslauncher']:
            return psutil.Process(process.info['pid'])
    return None

def check_epic_games_activity(process): #check the current epic games process' usage
    initial_io = process.io_counters()
    initial_net = psutil.net_io_counters()

    sleep(4)

    final_io = process.io_counters()
    final_net = psutil.net_io_counters()

    read_bytes = final_io.read_bytes - initial_io.read_bytes
    write_bytes = final_io.write_bytes - initial_io.write_bytes
    net_bytes_sent = final_net.bytes_sent - initial_net.bytes_sent
    net_bytes_recv = final_net.bytes_recv - initial_net.bytes_recv

    return {
        'read_bytes': read_bytes,
        'write_bytes': write_bytes,
        'net_bytes_sent': net_bytes_sent,
        'net_bytes_recv': net_bytes_recv
    }

def main_epic(shutdown, screenshot): #main epic function.
    print("Epic games it is...")
    print(f"{'shutdown' if shutdown else 'restart'} it is")
    print(f"{'screenshot' if screenshot else 'no screenshot'} it is")
    while True:
        epic_games_process = get_epic_games_process()
        if epic_games_process:
            activity = check_epic_games_activity(epic_games_process)
            if activity['write_bytes'] > 0 and activity['net_bytes_recv'] > 0:
                print("Epic seems to still be installing or updating something.")
                continue
            else:
                if screenshot:
                    make_screenshot()
                print("Epic games seems to have stopped with the download of the game... Shutting down")
                if shutdown:
                    os.system("shutdown /s /t 0")
                else:
                    os.system("shutdown /r /t 0")
        else:
            print("epic process not found... exiting.")
            sleep(3)
            exit()

def check_general_activity(): #this just has to check the general system activity instead of a specific process' so
    initial_disk_io = psutil.disk_io_counters()
    initial_net_io = psutil.net_io_counters()

    sleep(10)


    current_disk_io = psutil.disk_io_counters()
    current_net_io = psutil.net_io_counters()

    read_bytes = current_disk_io.read_bytes - initial_disk_io.read_bytes
    write_bytes = current_disk_io.write_bytes - initial_disk_io.write_bytes
    net_bytes_sent = current_net_io.bytes_sent - initial_net_io.bytes_sent
    net_bytes_recv = current_net_io.bytes_recv - initial_net_io.bytes_recv

    return {
        'read_bytes': read_bytes,
        'write_bytes': write_bytes,
        'net_bytes_sent': net_bytes_sent,
        'net_bytes_recv': net_bytes_recv
    }

def main_general(shutdown, screenshot): # the main general actions.
    print("General it is...")
    print(f"{'shutdown' if shutdown else 'restart'} it is")
    print(f"{'screenshot' if screenshot else 'no screenshot'} it is")
    while True:
        activity = check_general_activity()
        if activity['write_bytes'] > 10 * (1024 * 1024) and activity['net_bytes_recv'] > 10 * (1024 * 1024):
            print("updating or installing.")
            continue
        else:
            if screenshot:
                make_screenshot()
            print("The system doesn't seem to be installing anything in general. exiting")
            sleep(2)
            if shutdown:
                os.system("shutdown /s /t 0")
            else:
                os.system("shutdown /r /t 0")

def make_screenshot():
    print("Making screenshot.")
    if "Restart Screenshots" not in os.listdir():
        os.mkdir("Restart Screenshots")
    current_time_list = "-".join(str(datetime.now()).split(".")[0].split(":")).split(" ")
    current_time = current_time_list[1] + "-" + current_time_list[0]
    screenshot = ImageGrab.grab(all_screens=True)
    screenshot.save(f"{os.getcwd()}\\Restart Screenshots\\{current_time}.png")
    print(f"Screenshot saved as {current_time}.png")
    sleep(1)
    return 0

print("""
------------------------------------------------------------------------------------------------------------------------
                                    Automatic Shutdown by jtw
------------------------------------------------------------------------------------------------------------------------
    This script basically just automatically shuts down your system after steam, epic games or games from another source
    finish installing or updating. It's quite useful I'd say. There is no real usage here. 
    Just type in what you want to monitor (general should work for both steam and epic games as well) and then if you
    want to restart your system or simply shut it down. 
    

""")
task_to_monitor = input("Task (steam, epic, general): ").lower()
shut_or_res = input("Shutdown or restart: ").lower()
shutdown = True
if shut_or_res != "shutdown":
    shutdown = False

screenshot_in = input(f"Wanna screenshot the screen right before {'shutdown' if shut_or_res else 'restart'}? [y, n]: ")
screenshot = False
if screenshot_in == "y":
    screenshot = True


if task_to_monitor == "steam":
    main_steam(shutdown, screenshot)
elif "epic" in task_to_monitor:
    main_epic(shutdown, screenshot)
else:
    main_general(shutdown, screenshot)


