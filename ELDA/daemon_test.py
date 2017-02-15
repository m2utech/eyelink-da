import os, sys

def daemon():
        try:
          pid = os.fork()

          if pid > 0:
            print 'PID: %d' % pid
            sys.exit()

        except OSError as error:
          print 'Unable to fork. Error: %d (%s)' % (error.errno, error.strerror)
          sys.exit()

        doTask()

def doTask():
        "new session create"
        os.setsid()

        os.open("/dev/null", os.O_RDWR)
        os.dup(0)
        os.dup(0)

        while True:
          pass

if __name__ == '__main__':
        daemon()
