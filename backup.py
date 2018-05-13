import os
import tarfile
import time
import yaml
from shutil import copy2 as copyfile


CONFIG_FILE = "config.yml"


# Reads the configuration from the defined configuration file (in yaml format).
def read_configs():
    stream = open(CONFIG_FILE)
    streamed_configs = yaml.safe_load_all(stream)
    configs = []

    for idx, value in enumerate(streamed_configs):
        config = {
            'source': value['source'],
            'target':  value['target']
        }

        if 'archive' in value:
            config['archive'] = value['archive']

        if 'max-history' in value:
            config['max_history'] = value['max-history']

        configs.append(config)

    stream.close()
    return configs


# Processes the backups as read from the configuration.
def backup_all():
    print 'Reading configurations from disk...'
    configs = read_configs()
    print 'Found ', len(configs), ' configurations:'

    for config in configs:
        print ' * from ', config['source'], ' to ', config['target']

    print 'Executing...'

    for config in configs:
        backup(config['source'], config['target'],
               config['archive'] if 'archive' in config else False,
               config['max_history'] if 'max_history' in config else 0)


# Processes a single backup configuration.
def backup(source, target, archive=False, max_history=0):
    if os.path.exists(source):

        if archive is True:
            archive_files(source, target, max_history)
        else:
            copy_files(source, target)

    else:
        print 'Source directory', source, ' not found, ignoring...'


# Checks if a given path exists, if not creates it.
def check_path(path):
    if not os.path.exists(path):
        print 'Target directory not found, creating...'
        os.makedirs(path)


# Copies all the files and directories from a source dir to a target dir. If file already exists and has same
# modification date, then it ignores it, as it didn't change.
def copy_files(source, target):
    check_path(target)
    for filename in os.listdir(source):
        print 'Filename:',filename
        source_file = os.path.join(source, filename)
        print 'Found ', source_file
        if os.path.isfile(source_file):
            target_file = os.path.join(target, filename)
            try:
                if os.path.exists(target_file) and str(os.stat(source_file).st_mtime) == str(
                        os.stat(target_file).st_mtime):
                    print 'File up to date, ignoring...'
                else:
                    copyfile(source_file, target_file)
                    print 'File ', source_file, 'copied.'
            except OSError as error:
                print 'ERROR: ', error
        else:
            copy_files(source_file, os.path.join(target, filename))


# Function that builds the archive name to be used.
def get_archive_name(source):
    basename = os.path.basename(source)
    return basename + '_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.tar.gz'


# Creates a tar archive with the directory contents, placing it inside the target directory.
def archive_files(source, target, max_history=0):
    filename = os.path.join(target, get_archive_name(source))
    print 'Creating archive', filename

    with tarfile.open(filename, 'w:gz') as tar:
        tar.add(source, arcname=os.path.basename(source))

    print 'Archive created.'
    if max_history > 0:
        clean_dir(target, max_history)


# Cleans up a directory by leaving only the defined number of artifacts.
def clean_dir(dir_name, max_history):
    files = os.listdir(dir_name)
    files.sort(key=lambda x: os.stat(os.path.join(dir_name, x)).st_mtime, reverse=True)

    for file_name in files[max_history:]:
        os.remove(os.path.join(dir_name, file_name))
    print 'Removed', len(files[max_history:]), 'old versions.'


# Executes the backup process.
backup_all()
