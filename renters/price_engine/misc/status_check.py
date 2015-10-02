import subprocess, re, sys, time

class TextDecorator(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def sucess(txt):
        return TextDecorator.OKGREEN + txt + TextDecorator.ENDC

    @staticmethod
    def fail(txt):
        return TextDecorator.FAIL + txt + TextDecorator.ENDC

    @staticmethod
    def warn(txt):
        return TextDecorator.WARNING + txt + TextDecorator.ENDC

def upload_file(ip, local_path, remote_path):
    cmd = "scp -i ~/.ssh/bonjoy-team.pem %s ubuntu@%s:%s " % (local_path, ip, remote_path)
    execute_cmd(cmd)

def create_remote_cmd(ip, cmds):
    return "ssh -X -i ~/.ssh/bonjoy-team.pem ubuntu@%s '%s'" % (ip, ';'.join(cmds))

def execute_remote_cmds(ip, cmds):
    cmd = create_remote_cmd(ip, cmds)
    return execute_cmd(cmd)

def execute_cmd(cmd):
    print(cmd)
    try:
        output = subprocess.check_output(cmd, shell=True)
        return output
    except subprocess.CalledProcessError as e:
        print e

def get_last_success_id_cmd(machine, use_origin=False):
    cmd = r'FILE_PATH=data-mining/renters/price_engine/data/new_data_set/success_%s.log; test -e $FILE_PATH && echo -n `tail -n 1 $FILE_PATH | cut -c7-9 | tr -d "," | tr -d "\""`' % get_tag(machine)
    if machine.get('handle_missed', False) and not use_origin:
        cmd = r'FILE_PATH=data-mining/renters/price_engine/data/new_data_set/success_%s.log; test -e $FILE_PATH && echo -n `tail -n 1 $FILE_PATH | cut -c7-9 | tr -d "," | tr -d "\""`' % get_tag(machine)

    return [cmd]

def get_last_error_id_cmd(machine, use_origin=False):
    cmd = r'FILE_PATH=data-mining/renters/price_engine/data/new_data_set/error_%s.log; test -e $FILE_PATH && echo -n `tail -n 1 $FILE_PATH | cut -c7-9 | tr -d "," | tr -d "\""`' % get_tag(machine)
    if machine.get('handle_missed', False) and not use_origin:
        cmd = r'FILE_PATH=data-mining/renters/price_engine/data/new_data_set/error_%s.log; test -e $FILE_PATH && echo -n `tail -n 1 $FILE_PATH | cut -c7-9 | tr -d "," | tr -d "\""`' % get_tag(machine)

    return [cmd]

def get_total_count_cmd(machine, use_origin=False):
    cmd = r'wc -l data-mining/renters/price_engine/data/new_data_set/full_crosses_renters_%s.csv | cut -d " " -f 1' % machine['id']
    if machine.get('handle_missed', False) and not use_origin:
        cmd = r'wc -l data-mining/renters/price_engine/data/new_data_set/missed_full_%s.csv | cut -d " " -f 1' % machine['id']

    return [cmd]

def get_data_path(machine):
    if machine.get('handle_missed', False):
        return 'data/missed_full_%s.csv' % machine['id']
    return 'data/new_data_set/full_crosses_renters_%s.csv' % machine['id']

def get_tag(machine):
    if machine.get('handle_missed', False):
        return 'missed_full_%s' % machine['id']
    return 'full_%s' % machine['id']

def generate_missed_data_set(machine):
    print("generating missed data set")
    ip = machine['ip']
    machine_id = machine['id']
    upload_file(ip, '~/extract_samples_from_error_file.py', '~/data-mining/renters/price_engine/misc/extract_samples_from_error_file.py')
    execute_remote_cmds(ip, [
        'cd data-mining/renters/price_engine',
        'python misc/extract_samples_from_error_file.py %s %s' % ('data/error_full_%s.log' % machine_id, 'data/missed_full_%s.csv' % machine_id)
    ])

def check_status(machine):
    machine_id = machine['id']
    ip = machine['ip']

    if machine.get('finished', False):
        print(TextDecorator.warn(">>>> [%s] %s FINISHED" % (machine_id, ip)))
        return

    cmds = [
        'ps aux | grep [r]uby',
        'free | head -n 2',

        'printf "total: "'
    ] + get_total_count_cmd(machine) + [
        'tail data-mining/renters/price_engine/data/status_%s.log | grep HITTING' % get_tag(machine),

        'printf "last-success: "',
    ] + get_last_success_id_cmd(machine) + [
        'printf " count: "',
        'wc -l data-mining/renters/price_engine/data/success_%s.log | cut -d " " -f 1' % get_tag(machine),

        'printf "last-error: "',
    ] + get_last_error_id_cmd(machine) + [
        'printf " count: "',
        'wc -l data-mining/renters/price_engine/data/error_%s.log | cut -d " " -f 1' % get_tag(machine),
    ]
    cmd = create_remote_cmd(ip, cmds)
    try:
        output = subprocess.check_output(cmd, shell=True)
        header = ">>>> [%s] %s" % (machine_id, ip)
        if re.search('ruby browser_robot.rb', output):
            print(TextDecorator.sucess(header))
        else:
            print(TextDecorator.fail(header))
            print("the script stopped. Trying to restart.")
            resume_task(machine)

        print output
    except subprocess.CalledProcessError as e:
        print e

def init_remote_env(machine, name, passwd):
    ip = machine['ip']
    machine_id = machine['id']
    print("[%s] init env" % machine_id)
    upload_file(ip, '~/locale', '~/locale')
    upload_file(ip, '~/Xwrapper.config', '~/Xwrapper.config')
    cmds = [
        'rm -rf data-mining',
        'git clone https://%s:%s@github.com/bonjoylabs/data-mining' % (name, passwd),
        'sudo cp /etc/default/locale /etc/default/locale.default',
        'sudo cp ~/locale /etc/default/locale',
        'sudo cp /etc/X11/Xwrapper.config /etc/X11/Xwrapper.config.default',
        'sudo cp ~/Xwrapper.config /etc/X11/Xwrapper.config'
    ]
    execute_remote_cmds(ip, cmds)

def start_scripting(machine, offset=0):
    ip = machine['ip']
    machine_id = machine['id']
    print("[%s] start script" % machine_id)
    print("Check if X server is running")
    output = execute_remote_cmds(ip, ['pidof X'])
    if output is None:
        print("start X server")
        output = execute_remote_cmds(ip, ['export DISPLAY=:0.0', 'nohup startx > /dev/null 2>&1 &'])
    else:
        print("X server is already running")
    cmds = [
        'export DISPLAY=:0.0',
        'cd ~/data-mining/renters/price_engine',
        "nohup ruby browser_robot.rb '%s' '%s' %s > /dev/null 2>&1 &" % (get_data_path(machine), get_tag(machine), offset),
    ]
    execute_remote_cmds(ip, cmds)

def reboot_machine(machine):
    ip = machine['ip']
    execute_remote_cmds(ip, ['sudo reboot'])

def restart_task(machine):
    pass

def resume_task(machine):
    print("resume [%s]" % machine['id'])
    #update_machine_status([machine])

    if machine.get('finished', False):
        print("[%d] is fnished. Do not need to resume" % machine['id'])
        return

    reboot_machine(machine)
    print("rebooting ... waiting for 60s")
    time.sleep(60)

    if machine.get('handle_missed', False):
        print(">> Handle Missed Data Set")
    else:
        print(">> Handle Original Data Set")

    offset = execute_remote_cmds(machine['ip'], get_last_success_id_cmd(machine)) or 0
    print("get last success id ", offset)

    #if machine.get('handle_missed', False):
    #    generate_missed_data_set(machine)

    start_scripting(machine, offset)

def update_machine_status(machines):
    print("update machine status ...")
    for machine in machines:
        if not machine.get('finished', False) and is_machine_finish_origin_data(machine):
            machine['handle_missed'] = True

        if not machine.get('finished', False) and is_machine_finish_missed_data(machine):
            machine['finished'] = True

def is_machine_finish_origin_data(machine):
    ip = machine['ip']
    machine_id = machine['id']

    total_count = execute_remote_cmds(ip, get_total_count_cmd(machine, True)) or '0'
    success_id = execute_remote_cmds(ip, get_last_success_id_cmd(machine, True)) or '0'
    error_id = execute_remote_cmds(ip, get_last_error_id_cmd(machine, True)) or '0'

    if int(success_id.strip()) + 1 == int(total_count.strip()) or int(error_id.strip()) + 1 == int(total_count.strip()):
        return True
    return False

def is_machine_finish_missed_data(machine):
    ip = machine['ip']
    machine_id = machine['id']

    if not machine.get('handle_missed', False):
        return False

    total_count = execute_remote_cmds(ip, get_total_count_cmd(machine)) or '0'
    success_id = execute_remote_cmds(ip, get_last_success_id_cmd(machine)) or '0'
    error_id = execute_remote_cmds(ip, get_last_error_id_cmd(machine)) or '0'

    if int(success_id.strip()) + 1 == int(total_count.strip()) or int(error_id.strip()) + 1 == int(total_count.strip()):
        return True
    return False

machines = [
    {'id': 0,  'ip': '54.148.44.40'},
    {'id': 1,  'ip': '52.26.4.236'},
    {'id': 2,  'ip': '52.26.49.136'},
    {'id': 3,  'ip': '52.88.205.83'} ,
    {'id': 4,  'ip': '52.89.202.119'} ,
]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", help="id of the machine to operate. signle id or multiple ids delimit by comma.")
    parser.add_argument("-a", "--action", help="[init | check | resume | reboot | restart] Action need to be executed. Signle action or multiple actions delimit by comma.")
    parser.add_argument("-l", "--loop", help="[forever | N] repeat the action for specific time")
    args = parser.parse_args()

    if args.id is None:
        sys.exit("Sorry fail to execute. Please give the machine ids to operate")

    if args.action is None:
        sys.exit("Sorry fail to execute. Please give the actions to operate")

    action_funcs = {
        'init': init_remote_env,
        'check': check_status,
        'resume': resume_task,
        'reboot': reboot_machine,
        'restart': restart_task,
        'start': start_scripting,
        'test': is_machine_finish_origin_data
    }

    if args.id == 'all':
        target_machines = machines
    else:
        ids = args.id.split(',')
        target_machines = [machine for machine in machines if str(machine['id']) in ids]

    #update_machine_status(target_machines)
    actions = args.action.split(',')

    for name in actions:
        if name == 'init':
            import getpass
            username = raw_input("Please input Github account.\nUsername:")
            password = getpass.getpass()
        for machine in target_machines:
            if name == 'init':
                action_funcs[name](machine, username, password)
            else:
                action_funcs[name](machine)

    if args.action == 'check' and args.loop == 'forever':
        print("Loop forever")
        while True:
            for machine in target_machines:
                for name in actions:
                    action_funcs[name](machine)
            # run check every 5min
            print("waiting for 5m ...")
            time.sleep(300)
