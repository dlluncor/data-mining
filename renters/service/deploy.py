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

def reboot_machine(machine):
    ip = machine['ip']
    execute_remote_cmds(ip, ['sudo reboot'])

def restart_service(machine):
    ip = machine['ip']
    execute_remote_cmds(ip, ['sudo restart renters'])

def deploy(machine, name, passwd):
    ip = machine['ip']
    if name is None or passwd is None:
        print("Please provide name and password. quit.")
        print("Usage: NAME=xxx;PASSWD=xxx;python delpoy -i all -a deploy")
        return
    cmds = [
        'cd data-mining',
        'git pull --rebase https://%s:%s@github.com/bonjoylabs/data-mining master' % (name, passwd),
        'sudo restart renters'
    ]
    execute_remote_cmds(ip, cmds)

def fresh_deploy(machine, name, passwd):
    ip = machine['ip']
    if name is None or passwd is None:
        print("Please provide name and password. quit.")
        print("Usage: NAME=xxx;PASSWD=xxx;python fresh_deploy -i all -a deploy")
        return

    cmds = [
        'rm -rf data-mining',
        'git clone https://%s:%s@github.com/bonjoylabs/data-mining' % (name, passwd),
        'sudo restart renters'
    ]
    execute_remote_cmds(ip, cmds)

def show_errors(machine, lines=20):
    ip = machine['ip']
    execute_remote_cmds(ip, ['sudo tail -n %s /var/log/renters.log' % lines])

machines = [
    {'id': 0,  'ip': '52.89.174.57'},
]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", help="id of the machine to operate. signle id or multiple ids delimit by comma or all for all servers.")
    parser.add_argument("-a", "--action", help="[deploy | fresh_deploy | reboot | restart | show_errors] Action need to be executed")
    args = parser.parse_args()

    if args.id is None:
        print("Sorry fail to execute. Please give the machine ids to operate")
        sys.exit(parser.print_help())

    if args.action is None:
        print("Sorry fail to execute. Please give the actions to operate")
        sys.exit(parser.print_help())

    action_funcs = {
        'deploy': deploy,
        'fresh_deploy': fresh_deploy,
        'reboot': reboot_machine,
        'restart': restart_service,
        'show_errors': show_errors,
    }

    if args.id == 'all':
        target_machines = machines
    else:
        ids = args.id.split(',')
        target_machines = [machine for machine in machines if str(machine['id']) in ids]

    for machine in target_machines:
        if args.action == 'deploy' or args.action == 'fresh_deploy':
            name = sys.get_env('NAME', None)
            passwd = sys.get_env('PASSWD', None)
            action_funcs[action](machine, name, passwd)
        else:
            action_funcs[action](machine)
