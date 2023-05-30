import os
from shutil import copy2
from glob import iglob

# List all files int the directory
home_url = os.path.expanduser("~")
github_url = os.path.join(home_url, 'github')
project_url = os.path.join(github_url, 'tools_settings')


def copy_bash():
    """ Copy the bash files """
    # Copy bash related files
    src_url = os.path.join(project_url, "git_bash", ".*")
    if not os.path.isdir(src_url):
        print(f"{src_url} : Invalid Path")

    print(f'Searching for files ...{src_url}')
    for file in iglob(src_url):
        print(file)
        # Copy git bash files
        copy2(file, home_url)


def setup_nvim():
    """ Setup Nvim enviornment """
    # Set env variable
    xdg_path = os.path.join(home_url, "AppData/Local")
    if not os.environ["XDG_CONFIG_HOME"]:
        os.environ["XDG_CONFIG_HOME"] = os.path.join(home_url, "AppData/Local")
        os.environ["XDG_DATA_HOME"] = os.path.join(home_url, "AppData/Local")

    # Install nvim plugins
    command = "pip3 install pynvim"
    os.system(command)

    # Create Vundle
    destn_url = os.path.join(xdg_path, "nvim", "bundle")

    if not os.path.isdir(src_url):
        os.mkdir(destn_url)

    os.chdir(destn_url)
    command = "git clone https://github.com/VundleVim/Vundle.vim.git"
    os.system(command)

    # Copy the files
    src_url = os.path.join(project_url, "nvim", "nvim", "*")
    for filename in iglob(src_url, recursive=True):
        copy2(filename, destn_url)


def install_fonts():
    """ Install the fonts """
    os.chdir(github_url)
    command = "git clone https://github.com/powerline/fonts.git --depth=1"
    os.system(command)


if __name__ == '__main__':
    # copy_bash()
    setup_nvim()
