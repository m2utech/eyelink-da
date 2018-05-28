import sys
import psutil
from subprocess import Popen

cmd1 = 'python3.5'
cmd2 = 'efsl_main.py'
cmd3 = 'efsl_scheduler.py'


def start():
    for process in psutil.process_iter():
        if process.cmdline() == [cmd1, cmd2] or process.cmdline() == [cmd1, cmd3]:
            print("pid {}, {} already exist. Daemon already running ?".format(process.pid, process.cmdline()[1]))
            sys.exit(0)

    print("start {} and {} for daemon service".format(cmd2, cmd3))
    Popen([cmd1, cmd2])
    Popen([cmd1, cmd3])


def stop():
    print("stop the daemon ...")
    for process in psutil.process_iter():
        if process.cmdline() == [cmd1, cmd2] or process.cmdline() == [cmd1, cmd3]:
            print("stopped {}".format(process.cmdline()[1]))
            process.terminate()


def restart():
    for process in psutil.process_iter():
        if process.cmdline() == [cmd1, cmd2] or process.cmdline() == [cmd1, cmd3]:
            process.terminate()
    print("restart {} and {} for daemon service".format(cmd2, cmd3))
    Popen([cmd1, cmd2])
    Popen([cmd1, cmd3])


if __name__ == '__main__':
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            # logger.info("Started daemon for {} ...".format(product['productName']))
            start()
        elif 'stop' == sys.argv[1]:
            # logger.info("Stopped daemon for {} ...".format(product['productName']))
            stop()
        elif 'restart' == sys.argv[1]:
            # logger.info("Restarted daemon for {} ...".format(product['productName']))
            restart()
        else:
            print("unknown command")
            print("usage: %s start|stop|restart" % sys.argv[0])
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)