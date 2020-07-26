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


def get_status(vk):
    users = vk.users.get(user_ids='3917431', fields=['online'])
    return users[0]['online']


def do_status(vk):
    global current_status
    ts = time.time()
    date_time_obj = datetime.now()
    status = get_status(vk)
    line = "{},{}\n".format(int(ts), status)
    print(line)
    # with open("onlines/{}.csv".format(date_time_obj.strftime("%Y-%m-%d")), "a+") as f:
    #     f.write(line)
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
    do_status(do_session().get_api())
    print(1)

