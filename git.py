import os
import json
import subprocess

def cwd():
    '''
    获取当前地址
    '''
    current_dir = os.getcwd()
    return current_dir


def git_init(current_dir):
    '''
    判断是否初始化仓库
    若没有有则初始化
    current_dir : 当前文件夹地址
    '''
    if not os.path.isdir(os.path.join(current_dir, '.git')):
        subprocess.run(['git', 'init', current_dir])


def load_config(config_file):
    '''
    从config.json文件加载配置
    如果文件不存在或解析错误，返回空字典
    '''
    config = {}
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            pass
    return config


def user_selection(config):
    '''
    用户选择配置
    返回选择的服务和配置键
    '''
    choices = []
    print('==========================================')
    print("请选择用户配置:")
    for service in config:
        for user_key in config[service]:
            choices.append((service, user_key))
            username = config[service][user_key]['username']
            print(f"{len(choices)}. {service}. {user_key}. {username}")
    print('==========================================')
    while True:
        try:
            choice = int(input("请输入选择的编号: "))
            if 1 <= choice <= len(choices):
                selected_choice = choices[choice - 1]
                return selected_choice
            else:
                print("无效的选择，请重新输入编号。")
        except ValueError:
            print("无效的选择，请重新输入编号。")


def get_user_data(config, service, selected_key):
    '''
    根据选择的配置键获取用户数据
    返回用户名、邮箱、远程仓库名称和地址
    '''
    username = config[service][selected_key]['username']
    email = config[service][selected_key]['email']
    remote_name = config[service][selected_key]['remote_name']
    remote_url = config[service][selected_key]['remote_url']
    return username, email, remote_name, remote_url



def add_files_to_stage():
    '''
    添加文件到缓存区
    '''
    subprocess.run(['git', 'add', '.'])


def set_branch(branch_name):
    '''
    判断是否存在分支
    若没有则创建分支
    '''
    branches = subprocess.run(['git', 'branch', '--list', branch_name], capture_output=True, text=True)
    if branch_name not in branches.stdout:
        subprocess.run(['git', 'branch', branch_name])
    subprocess.run(['git', 'checkout', branch_name])


def commit(commit_message):
    '''
    提交保存
    '''
    subprocess.run(['git', 'commit', '-m', commit_message])


def check_remote_config_exists(remote_name, remote_url):
    '''
    判断远程仓库是否存在
    不存在则创建
    '''
    remotes = subprocess.run(['git', 'remote'], capture_output=True, text=True).stdout.splitlines()
    if remote_name not in remotes:
        subprocess.run(['git', 'remote', 'add', remote_name, remote_url])
        print('==========================================')
        print(f"远程仓库配置 '{remote_name}' 创建成功。")
    else:
        print('==========================================')
        print(f"远程仓库配置 '{remote_name}' 已存在，跳过创建。")


def upload_to_github(remote_name, branch_name):
    '''
    提交到GitHub
    '''
    subprocess.run(['git', 'push', remote_name, branch_name])

def _print(service, selected_key, username, email, remote_name, remote_url):
    print('==========================================')
    print(service + '\n' + selected_key + '\n' + username + '\n' + email + '\n' + remote_name + '\n' + remote_url)
    print('==========================================')


def main():
    current_dir = cwd()
    CONFIG_FILE = 'Git_Data/config.json'
    branch_name = 'main'
    commit_message = input("请输入提交备注: ")

    # 1. 初始化仓库
    git_init(current_dir)

    # 2. 读取用户配置
    config = load_config(CONFIG_FILE)

    # 3. 用户选择配置
    service, selected_key = user_selection(config)

    # 4. 获取用户数据
    username, email, remote_name, remote_url = get_user_data(config, service, selected_key)

    # 5. 添加文件到缓存区
    add_files_to_stage()

    # 6. 提交保存
    commit(commit_message)

    # 7. 设定分支
    set_branch(branch_name)

    # 8. 检查并创建远程仓库配置
    # _print(service, selected_key, username, email, remote_name, remote_url)
    check_remote_config_exists(remote_name, remote_url)

    # 9. 提交到GitHub
    _print(service, selected_key, username, email, remote_name, remote_url)
    upload_to_github(remote_name, branch_name)


if __name__ == '__main__':
    main()

