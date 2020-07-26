from datetime import datetime
import vk_api
import time
import sched
import paramiko


scheduler = sched.scheduler(time.time, time.sleep)

current_status = 0


def do_session():
    vk_session = vk_api.VkApi('+79859458929', 'штудук001')
    vk_session.auth()
    return vk_session


def get_info(vk):
    users = vk.users.get(user_ids='3917431', fields=['online'])
    return users[0]


def do_status(vk):
    global current_status
    ts = int(time.time())
    libreoffice_epoch = (ts + 60 * 60 * 3) / (60 * 60 * 24) + 25569
    date_time_obj = datetime.now()
    info = get_info(vk)
    status = info['online']
    line = "{}, {}, {}, {}\n".format(ts, status, libreoffice_epoch, 1 if 'online_mobile' in info else 0)
    print(line)
    with open("onlines/{}.csv".format(date_time_obj.strftime("%Y-%m-%d")), "a+") as f:
        f.write(line)
    if current_status != status and status == 1:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect("owner", username="igor", password="1")
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("notify-send \"Надежда онлайн\"")
    current_status = status
    schedule(vk)


def schedule(vk):
    scheduler.enter(60, 1, do_status, {vk})


def init():
    session = do_session()
    vk = session.get_api()
    schedule(vk)
    scheduler.run()


if __name__ == '__main__':
    init()


