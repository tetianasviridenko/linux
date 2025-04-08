import os
import sys
def my_system(command):
    pid = os.fork()
    if pid == 0:
        try:
            os.execvp(command[0],command)
        except Exception as e:
             print(f'Помилка виконання команди: {e}', file=sys.stderr)
             os._exit(1)
    else:
        pid,status = os.wait()
        if os.WIFEXITED(status):
            return os.WEXITSTATUS(status)
        else:
            return -1
exit_code = my_system(['ls','-l'])
print(f'Команда завершилася з кодом: {exit_code}')

