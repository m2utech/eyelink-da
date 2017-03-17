import daemon
import daemon.pidfile


def start_daemon():

	print("Start daemon for EyeLink in python")

	with daemon.DaemonContext():
		while True:
			import elda_main


if __name__ == '__main__':
	start_daemon()
