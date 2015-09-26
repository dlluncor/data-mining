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

def check_machine_statues(machines,show_err_count=False):
    for machine in machines:
        is_missed = machine.get('missed', False)
        machine_id = machine['id']
        ip = machine['ip']
        cmds = [
            'ps aux | grep [r]uby',
            'wc -l data-mining/renters/%s' %  ('data/missed_full_%s.csv' % machine_id if is_missed == True else 'full_crosses_renters_0921212303_%s.csv' % machine_id),
            'tail data-mining/renters/data/out_full_%s_0921212303.log | grep HITTING' % machine_id,
            'wc -l data-mining/renters/data/%s' % ('data/error_missed_full_%s.log' % machine_id if is_missed else 'error_full_0921212303_2_%s.log' % machine_id)
        ]
        if not show_err_count:
            cmd = create_remote_cmd(ip, cmds[:3])
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

def init_remote_env(machines, name, passwd):
    for machine in machines:
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
        break

def start_scripting(machines):
    for machine in machines:
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
            'cd ~/data-mining/renters/price_engine',
            "nohup ruby browser_robot.rb 'data/origin_data_set/full_crosses_renters_0921212303_%s.csv' 'full_0921212303_3_%s' 0 >> data/out_full_3_%s.log > /dev/null 2>&1 &" % (machine_id, machine_id, machine_id)
        ]
        output = execute_remote_cmds(ip, cmds)
        print(output)
        break

machines = [
    {'id': 1,  'ip': '52.11.189.158'},# 'missed': True},
    {'id': 0,  'ip': '52.88.233.117'},# 'missed': True},

    {'id': 2,  'ip': '52.88.226.131'},# 'missed': True},
    {'id': 3,  'ip': '52.11.249.176'},# 'missed': True},
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
    {'id': 14, 'ip': '52.88.152.120'},# 'missed': True},
    {'id': 15, 'ip': '52.27.163.93'}, # 'missed': True},
]
if __name__ == '__main__':
    if sys.argv[1] == 'true':
        #init_remote_env(machines, sys.argv[2], sys.argv[3])
        start_scripting(machines)
    #check_machine_statues(machines)
