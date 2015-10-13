import csv, datetime, json, logging, os.path, re, subprocess, sys, time
from collections import OrderedDict

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

machines = [
    {'id': 0,  'ip': '54.186.155.71'},# 'filename': 'error_no_crosses.json', 'tag': 'missed'},
    {'id': 1,  'ip': '52.88.54.115'},# 'filename': 'error_no_crosses.json', 'tag': 'missed'}  ,
    #{'id': 2,  'ip': '52.26.49.136'} ,
    #{'id': 3,  'ip': '52.88.205.83'} ,
    #{'id': 4,  'ip': '52.89.202.119'},
]

dataset = {
    'local_path': 'data/new_data_set',
    'remote_path': '~/data-mining/renters/price_engine/data/new_data_set',
    'filename': 'no_crosses_renters_all.csv',
    'tag': 'no_crosses',
}

class TextDecorator(object):
    """
    Display text in different colors on Terminal
    """
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

def split_dataset(machines):
    path = dataset['local_path']
    filename = dataset['filename']
    dataset_file_path = "%s/%s" % (path, filename)
    if not os.path.exists(dataset_file_path):
        logging.error(TextDecorator.fail("Fail to find dataset file: %s" % dataset_file_path))
        return

    with open(dataset_file_path, 'r') as reader:
        lines = reader.readlines()

        samples = [json.dumps(OrderedDict([('id', idx), ('data', item.strip().split(','))])) for idx, item in enumerate(lines)]
        # Drop the header
        samples = samples[1:]
        for machine in machines:
            tag = get_tag(machine)
            items = samples[int(machine['id'])::len(machines)]
            with open("%s/%s" % (path, get_data_filename(machine)), 'w') as writer:
                for item in items:
                    writer.write(item + "\n")

def upload_file(ip, local_path, remote_path):
    cmd = "scp -i ~/.ssh/bonjoy-team.pem %s ubuntu@%s:%s " % (local_path, ip, remote_path)
    execute_cmd(cmd)

def download_file(ip, local_path, remote_path):
    cmd = "scp -i ~/.ssh/bonjoy-team.pem ubuntu@%s:%s %s" % (ip, remote_path, local_path)
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

def get_last_id_cmd(machine, state):
    tag = get_tag(machine)
    filepath = get_remote_result_filepath(state, machine)
    cmd = r'FILE_PATH={path}; test -e $FILE_PATH && echo -n `tail -n 1 $FILE_PATH | cut -c7-9 | tr -d "," | tr -d "\""`'.format(path=filepath)

    return [cmd]

def get_total_count_cmd(machine):
    cmd = r'wc -l {path}/{filename} | cut -d " " -f 1'.format(path=dataset['remote_path'], filename=get_data_filename(machine))
    return [cmd]

def get_tag(machine):
    return machine.get('tag', None) or dataset['tag']

def get_data_filename(machine):
    if machine.get('filename', None):
        return machine['filename']

    tag = get_tag(machine)
    return "%s_%s.json" % (tag, machine['id'])

def check_status(machine):
    machine_id = machine['id']
    ip = machine['ip']

    cmds = [
        'ps aux | grep [r]uby',
        'free | head -n 2',

        'printf "total: "'
    ] + get_total_count_cmd(machine) + [
        'FILE_PATH={filepath}; test -e $FILE_PATH && tail $FILE_PATH  | grep HITTING'.format(filepath=get_remote_result_filepath('status', machine, 'log')),

        'printf "last-success-id: "',
    ] + get_last_id_cmd(machine, 'success') + [
        'printf " count: "',
        'FILE_PATH={filepath}; test -e $FILE_PATH && wc -l $FILE_PATH | cut -d " " -f 1'.format(filepath=get_remote_result_filepath('success', machine)),

        'printf "last-error-id: "',
    ] + get_last_id_cmd(machine, 'error') + [
        'printf " count: "',
        'FILE_PATH={filepath}; test -e $FILE_PATH && wc -l $FILE_PATH | cut -d " " -f 1'.format(filepath=get_remote_result_filepath('error', machine)),

        'printf "\nFiles under %s:\n"' % dataset['remote_path'],
        'ls %s' % dataset['remote_path']
    ]
    cmd = create_remote_cmd(ip, cmds)
    try:
        output = subprocess.check_output(cmd, shell=True)
        header = ">>>> [%s] %s" % (machine_id, ip)
        if re.search('ruby browser_robot.rb', output):
            logging.info(TextDecorator.sucess(header))
        elif re.search('end.%s' % get_tag(machine), output):
            logging.info(TextDecorator.warn(header) + " FINISHED")
        elif re.search('start.%s' % get_tag(machine), output):
            logging.info(TextDecorator.fail(header))
            logging.info("the script stopped. Trying to restart.")
            resume_task(machine)
        else:
            logging.info(TextDecorator.fail(header))
            logging.info(TextDecorator.warn("The task seems not STARTED. Please start it before check"))
        print output
    except subprocess.CalledProcessError as e:
        print e

def init_remote_machine(machine, name, passwd):
    ip = machine['ip']
    machine_id = machine['id']
    tag = get_tag(machine)

    data_filename = get_data_filename(machine)
    logging.info("[%s] init env" % machine_id)
    upload_file(ip, 'misc/locale', '~/locale')
    upload_file(ip, 'misc/Xwrapper.config', '~/Xwrapper.config')

    cmds = [
        'rm -rf data-mining',
        'git clone https://%s:%s@github.com/bonjoylabs/data-mining' % (name, passwd),
        'sudo cp /etc/default/locale /etc/default/locale.default',
        'sudo cp ~/locale /etc/default/locale',
        'sudo cp /etc/X11/Xwrapper.config /etc/X11/Xwrapper.config.default',
        'sudo cp ~/Xwrapper.config /etc/X11/Xwrapper.config',
    ]
    execute_remote_cmds(ip, cmds)
    # Upload data file
    upload_file(ip, '%s/%s' % (dataset['local_path'], data_filename), '%s/%s' % (dataset['remote_path'], data_filename))
    reboot_machine(machine)
    print("Rebooting [{id}] ... ".format(**machine))

def start_scripting(machine, offset=0):
    ip = machine['ip']
    machine_id = machine['id']
    tag = get_tag(machine)
    logging.info("[%s] start script" % machine_id)
    logging.info("Check if X server is running")
    output = execute_remote_cmds(ip, ['pidof X'])
    if output is None:
        print("start X server")
        output = execute_remote_cmds(ip, ['export DISPLAY=:0.0', 'nohup startx > /dev/null 2>&1 &'])
    else:
        print("X server is already running")
    cmds = [
        'export DISPLAY=:0.0',
        'cd ~/data-mining/renters/price_engine',
        "nohup ruby browser_robot.rb '%s' '%s' '%s' '%s' %s > /dev/null 2>&1 &" % (dataset['remote_path'], get_data_filename(machine), tag, 'json', offset),
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

    offset = execute_remote_cmds(machine['ip'], get_last_id_cmd(machine, 'success')) or 0
    print("get last success id ", offset)

    #if machine.get('handle_missed', False):
    #    generate_missed_data_set(machine)

    start_scripting(machine, offset)

def get_remote_result_filepath(filetype, machine, ext='json', tag=None):
    tag = tag or get_tag(machine)
    filename = '%s_%s.%s' % (filetype, tag, ext)
    return "{path}/{filename}".format(path=dataset['remote_path'], filename=filename)

def get_local_result_filepath(filetype, machine, ext='json', tag=None):
    tag = tag or get_tag(machine)
    filename = '%s_%s_%s.%s' % (filetype, tag, machine['id'], ext)
    return "{path}/{filename}".format(path=dataset['local_path'], filename=filename)

def pull_data_files(machine, tags):
    ip = machine['ip']
    remote_path = dataset['remote_path']
    local_path = dataset['local_path']
    print(tags)
    for tag in tags:
        files = [{
            'remote_filepath': get_remote_result_filepath('success', machine, 'json', tag),
            'local_filepath': get_local_result_filepath('success', machine, 'json', tag),
        }, {
            'remote_filepath': get_remote_result_filepath('error', machine, 'json', tag),
            'local_filepath': get_local_result_filepath('error', machine, 'json', tag),
        },{
            'remote_filepath': get_remote_result_filepath('status', machine, 'log', tag),
            'local_filepath': get_local_result_filepath('status', machine, 'log', tag),
        }]
        for f in files:
            download_file(ip, f['local_filepath'], f['remote_filepath'])

def merge_result_files(machines, tags):
    samples= []
    for tag in tags:
        for machine in machines:
            for state in ['success']:
                filepath = get_local_result_filepath(state, machine, tag=tag)
                if os.path.exists(filepath):
                    with open(filepath) as reader:
                        for line in reader:
                            sample = json.loads(line)
                            samples.append(sample)

    with open("%s/final_result.csv" % dataset['local_path'], 'wb') as fout:
        writer = csv.writer(fout)
        writer.writerow(['Insurance Type', 'Zip code', 'First name', 'Last name', 'Date of birth', 'Gender', 'Address', 'City', 'State', 'Auto insurance coverage?', 'Property Type', '# units', '# unrelated roommates', '# property losses in last 3 years', 'Phone number', 'Email address', 'Fire Sprinkler System?', 'Central Fire & Burglar Alarm?', 'Local Fire / Smoke Alarm?', 'Home Security?', 'Non Smoking Household?', 'Local Burglar Alarm?', 'Unusual hazards?', 'Dogs that bite?', 'Run a business from home?', 'Start date', 'Personal property worth', 'Loss of use', 'Medical payments', 'Personal liability', 'Farmers Identity Protection', 'Deductible', 'Policy number', 'Timestamp (seconds)', 'Policy price', 'Name of agent', 'Address of agent', 'Elancer Name'])
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for sample in sorted(samples, key=lambda x: int(x['id'])):
            row = sample['data']
            (insurance_type, zip_code, first_name, last_name, dob,
            gender, address, city, state, has_auto_insurance_coverage,
            property_type, unit_count, unrelated_roommates_count, roommate_names, property_losses_count, phone_number,
            email, has_fire_sprinkler_system, has_center_fire_burglar_alarm, has_local_fire_smoke_alarm,
            has_home_security, is_non_smoking_household, has_local_burglar_alarm, has_unusual_hazards,
            has_bite_dog, is_running_bussiness, start_date, personal_property_value,
            loss_of_use, medical_payment, personal_liability, farmers_identity_protection,
            deductible, policy_price, annual_policy_price, agent_name, agent_address, agent_phone_number,
            policy_number) = row
            writer.writerow([insurance_type, zip_code, first_name, last_name, dob,
                            gender, address, city, state, has_auto_insurance_coverage,
                            property_type, unit_count, unrelated_roommates_count, property_losses_count, phone_number,
                            email, has_fire_sprinkler_system, has_center_fire_burglar_alarm, has_local_fire_smoke_alarm,
                            has_home_security, is_non_smoking_household, has_local_burglar_alarm, has_unusual_hazards,
                            has_bite_dog, is_running_bussiness, start_date, personal_property_value,
                            loss_of_use, medical_payment, personal_liability, farmers_identity_protection,
                            deductible, policy_number, timestamp, policy_price,
                            agent_name, agent_address, 'haoran'])


def test(machine):
    output = execute_remote_cmds(machine['ip'], ['ls /tmp/'])
    print(output)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--id", help="id of the machine to operate. signle id or multiple ids delimit by comma.")
    parser.add_argument("-a", "--action", help="[init | check | pull | resume | reboot | restart] Action need to be executed. Signle action or multiple actions delimit by comma.")
    parser.add_argument("-l", "--loop", help="[forever | N] repeat the action for specific time")
    parser.add_argument("-t", "--tags", help="tags of data files to download, only for pull ")
    args = parser.parse_args()

    if args.id is None:
        sys.exit("Sorry fail to execute. Please give the machine ids to operate")

    if args.action is None:
        sys.exit("Sorry fail to execute. Please give the actions to operate")

    action_funcs = {
        'init': init_remote_machine,
        'check': check_status,
        'resume': resume_task,
        'reboot': reboot_machine,
        'restart': restart_task,
        'start': start_scripting,
        'merge': merge_result_files
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
            logging.info("Split data set into %s files" % len(machines))
            split_dataset(machines)
            username = raw_input("Please input Github account.\nUsername:")
            password = getpass.getpass()

        if args.action == 'pull' or args.action == 'merge':
            if args.tags is None:
                logging.error("Please specify the tags of the file you want to download")
                sys.exit("FAIL")

            tags = args.tags.split(',')

        if name == 'merge':
            merge_result_files(target_machines, tags)
            sys.exit()

        for machine in target_machines:
            if name == 'init':
                action_funcs[name](machine, username, password)
            elif name == 'pull':
                pull_data_files(machine, tags)
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
