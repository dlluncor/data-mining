import subprocess, re, sys

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
    def warning(txt):
        return TextDecorator.WARNING + txt + TextDecorator.ENDC

def upload_file(ip, local_path, remote_path):
    cmd = "scp -i /Users/haoran/.ssh/bonjoy-team.pem %s ubuntu@%s:%s " % (local_path, ip, remote_path)
    execute_cmd(cmd)

def create_remote_cmd(ip, cmds):
    return "ssh -X -i /Users/haoran/.ssh/bonjoy-team.pem ubuntu@%s '%s'" % (ip, ';'.join(cmds))

def execute_remote_cmds(ip, cmds):
    cmd = create_remote_cmd(ip, cmds)
    return execute_cmd(cmd)

def execute_cmd(cmd):
    try:
        print(cmd)
        output = subprocess.check_output(cmd, shell=True)
        return output
    except subprocess.CalledProcessError as e:
        print e

def check_status(machine,show_err_count=False):
    is_missed = machine.get('missed', False)
    machine_id = machine['id']
    ip = machine['ip']
    cmds = [
        'ps aux | grep [r]uby',
        'free | head -n 2',
        'wc -l data-mining/renters/price_engine/data/%s' %  ('missed_full_3_%s.csv' % machine_id if is_missed == True else 'origin_data_set/full_crosses_renters_0921212303_%s.csv' % machine_id),
        'tail data-mining/renters/price_engine/data/status_full_0921212303_3_%s.log | grep HITTING' % machine_id,

        'printf "last-success: "',
        r'echo -n `tail -n 1 data-mining/renters/price_engine/data/success_full_0921212303_3_%s.log | cut -c7-9 | tr -d "," | tr -d "\""`' % machine_id,
        'printf " count: "',
        'wc -l data-mining/renters/price_engine/data/success_full_0921212303_3_%s.log | cut -d " " -f 1' % machine_id,

        'printf "last-error: "',
        r'echo -n `tail -n 1 data-mining/renters/price_engine/data/error_full_0921212303_3_%s.log | cut -c7-9 | tr -d "," | tr -d "\""`' % machine_id,
        'printf " count: "',
        'wc -l data-mining/renters/price_engine/data/error_full_0921212303_3_%s.log | cut -d " " -f 1' % machine_id,

        'wc -l data-mining/renters/price_engine/data/%s' % ('error_missed_full_3_%s.log' % machine_id if is_missed else 'error_full_0921212303_2_%s.log' % machine_id)
    ]
    if not show_err_count:
        cmd = create_remote_cmd(ip, cmds[:-1])
        try:
            output = subprocess.check_output(cmd, shell=True)
            header = ">>>> [%s] %s" % (machine_id, ip)
            if re.search('ruby browser_robot.rb', output):
                print(TextDecorator.sucess(header))
            else:
                print(TextDecorator.fail(header))

            print output
        except subprocess.CalledProcessError as e:
            print e

    else:
        process_cmd = create_remote_cmd(ip, [cmds[0]])
        total_count_cmd = create_remote_cmd(ip, [cmds[1]])
        err_count_cmd = create_remote_cmd(ip, [cmds[3]])
        progress_cmd = create_remote_cmd(ip, [cmds[2]])

        try:
            process_output = subprocess.check_output(process_cmd, shell=True)
            header = ">>>> [%s] %s" % (machine_id, ip)
            if re.search('ruby browser_robot.rb', process_output):
                print(TextDecorator.sucess(header))
            else:
                print(TextDecorator.fail(header))

            total_output = subprocess.check_output(total_count_cmd, shell=True)
            m = re.search('^(\d+)', total_output)
            if m:
                sys.stdout.write("total: %s " % m.group(1))

            err_output = subprocess.check_output(err_count_cmd, shell=True)
            m = re.search('^(\d+)', err_output)
            if m:
                print(TextDecorator.warning("err: %s" % m.group(1)))
            else:
                print("")

            progress_output = subprocess.check_output(progress_cmd, shell=True)
            print(progress_output)

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

def start_scripting(machine):
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
        "nohup ruby browser_robot.rb 'data/origin_data_set/full_crosses_renters_0921212303_%s.csv' 'full_0921212303_3_%s' 0 > /dev/null 2>&1 &" % (machine_id, machine_id),
    ]
    execute_remote_cmds(ip, cmds)

def reboot_machine(machine):
    ip = machine['ip']
    execute_remote_cmds(ip, ['sudo reboot'])

def restart_task(machine):
    pass

def resume_task(machine):
    pass

machines = [
    {'id': 0,  'ip': '52.88.233.117'},# 'missed': True},
    {'id': 1,  'ip': '52.11.189.158'},# 'missed': True},
    {'id': 2,  'ip': '52.88.226.131'},# 'missed': True},
    {'id': 3,  'ip': '52.27.101.36'},# 'missed': True},
    {'id': 4,  'ip': '52.89.19.195'} ,# 'missed': True},
    {'id': 5,  'ip': '52.88.52.137'} ,# 'missed': True},
    {'id': 6,  'ip': '52.24.245.42'} ,# 'missed': True},
    {'id': 7,  'ip': '52.25.250.151'},# 'missed': True},
    {'id': 8,  'ip': '52.88.193.187'},# 'missed': True},
    {'id': 9,  'ip': '52.88.8.172'}  ,# 'missed': True},
    {'id': 10, 'ip': '52.88.252.120'},# 'missed': True},
    {'id': 11, 'ip': '52.89.3.92'}   ,# 'missed': True},
    {'id': 12, 'ip': '52.88.149.7'}  ,#
    {'id': 13, 'ip': '52.88.119.125'},# 'missed': True},
    {'id': 14, 'ip': '52.24.188.108'},# 'missed': True},
    {'id': 15, 'ip': '52.88.4.226'}, # 'missed': True},
]
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", help="id of the machine to operate. signle id or multiple ids delimit by comma.")
    parser.add_argument("-a", "--action", help="[init | check | resume | reboot | restart] Action need to be executed. Signle action or multiple actions delimit by comma.")
    args = parser.parse_args()
    #if sys.argv[1] == 'true':
    #    init_remote_env(machines, sys.argv[2], sys.argv[3])
    #    start_scripting(machines)
    #    pass
    #check_machine_statues(machines)
    if args.id is None:
        sys.exit("Sorry fail to execute. Please give the machine ids to operate")

    if args.action is None:
        sys.exit("Sorry fail to execute. Please give the actions to operate")

    action_funcs = {
        'init': init_remote_env,
        'check': check_status,
        'resume': resume_task,
        'reboot': reboot_machine,
        'restart': restart_task
    }
    if args.id == 'all':
        target_machines = machines
    else:
        ids = args.id.split(',')
        target_machines = [machine for machine in machines if str(machine['id']) in ids]

    actions = args.action.split(',')
    for machine in target_machines:
        for name in actions:
            action_funcs[name](machine)
