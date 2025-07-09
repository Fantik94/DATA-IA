import os
import shutil
import datetime

def backup_files(source_dir, backup_dir):
    """Backup files from source directory to backup directory"""
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'backup_{timestamp}')
    shutil.copytree(source_dir, backup_path)
    return backup_path

def main():
    source = './'
    backup = './backups'
    try:
        backup_files(source, backup)
        print(f'Backup successful to {backup}')
    except Exception as e:
        print(f'Backup failed: {e}')

if __name__ == '__main__':
    main()