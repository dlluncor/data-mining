import logging, os, re, subprocess, sys, time
logging.basicConfig(format='%(message)s', level=logging.DEBUG)

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
    def success(txt):
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
    return "ssh -i ~/.ssh/bonjoy-team.pem ubuntu@%s '%s'" % (ip, ';'.join(cmds))

def execute_remote_cmds(ip, cmds):
    cmd = create_remote_cmd(ip, cmds)
    return execute_cmd(cmd)

def execute_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True)
        return output
    except subprocess.CalledProcessError as e:
        print("Oooops error!")
        print e

def reboot_machine(machine):
    ip = machine['ip']
    execute_remote_cmds(ip, ['sudo reboot'])

def restart_service(machine):
    ip = machine['ip']
    execute_remote_cmds(ip, ['sudo restart renters'])

def deploy(machine, name, passwd):
    logging.info(TextDecorator.success("Deploying ..."))
    ip = machine['ip']

    cmds = [
        'cd /u/app/data-mining',
        'printf ">>>> Update Codes\n"',
        'git pull --rebase https://%s:%s@github.com/bonjoylabs/data-mining master' % (name, passwd),
        'git log -1',
        'printf "\n>>>> Restart service\n"',
        'sudo restart renters',
    ]
    out = execute_remote_cmds(ip, cmds)
    logging.info(out)
    logging.info(TextDecorator.success("Deployment is finished."))

def fresh_deploy(machine, name, passwd):
    logging.info(TextDecorator.success("Fresh Deploying ..."))
    ip = machine['ip']

    cmds = [
        'sudo stop renters'
        'rm -rf /u/app/data-mining',
        'cd /u/app/',
        'git clone https://%s:%s@github.com/bonjoylabs/data-mining' % (name, passwd),
        'cd /u/app/data-mining/renters/service',
        'sudo pip install -r requirements.txt'
        'sudo start renters'
    ]
    execute_remote_cmds(ip, cmds)
    logging.info(TextDecorator.success("Deployment is finished."))

def show_logs(machine, lines=20):
    ip = machine['ip']
    execute_remote_cmds(ip, ['sudo tail -n %s /var/log/upstart/renters.log' % lines])

machines = [
    {'id': 0,  'ip': '52.89.174.57'},
]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", help="[deploy | fresh_deploy | reboot | restart | logs] Action need to be executed")
    args = parser.parse_args()

    if args.action is None:
        print("Sorry fail to execute. Please give the action to operate")
        sys.exit(parser.print_help())

    action_funcs = {
        'deploy': deploy,
        'fresh_deploy': fresh_deploy,
        'reboot': reboot_machine,
        'restart': restart_service,
        'logs': show_logs,
    }

    for machine in machines:
        if args.action == 'deploy' or args.action == 'fresh_deploy':
            import getpass

            user = raw_input('Please input your github account.\nUsername: ')
            passwd = getpass.getpass()
            action_funcs[args.action](machine, user, passwd)
        else:
            action_funcs[args.action](machine)
