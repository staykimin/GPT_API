from kimin.core import Client, Server
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Chat GPT Free API')
	parser.add_argument('--cookie', '-c', help='Path File Cookie', required=True)
	parser.add_argument('--mode', '-m', choices=['server', 'client'], default='client', help="Mode Yang Akan Digunakan, Dimana\n"
		" server = Menggunakan Endpoint Untuk Interaksi\n"
		" client = Tanpa Endpoint Untuk Interaksi\n")
	args = parser.parse_args()
	if args.mode == 'server':
		Server(args.cookie)
	elif args.mode == 'client':
		Client(args.cookie).Run()