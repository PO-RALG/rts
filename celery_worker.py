import os
import subprocess

if __name__ == '__main__':
    # Activate the virtual environment
    venv_dir = os.path.join(os.getcwd(), '.venv')  # Assuming the virtual environment is named '.venv'
    venv_python = os.path.join(venv_dir, 'bin', 'python')
    venv_celery = os.path.join(venv_dir, 'bin', 'celery')

    # Start the Celery worker
    command = [venv_python, venv_celery, '-A', 'app', 'worker', '--loglevel=info']
    celery_worker_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = celery_worker_process.communicate()
    print(stdout.decode())
    print(stderr.decode())
