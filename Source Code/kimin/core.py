import json, os, datetime, platform, time
from kimin.core_executor import Execute
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

def Date_2_Date(data, format='%d-%m-%Y %H:%M:%S'):
	return datetime.datetime.fromisoformat(data.replace('Z', '+00:00')).strftime(format)

class Server:
	def __init__(kimin, config):
		from kiminv4.core_server import Set_Server
		from flask_cors import CORS
		config_path = "server_config.min"
		with open(config_path, 'r', encoding='UTF-8') as dataku:
			cfg = json.loads(dataku.read())
		
		cfg['user_config'] = config
		with open(config_path, 'w', encoding='UTF-8') as dataku:
			json.dump(cfg, dataku, indent=4)
		
		x = Set_Server(config_path)
		
		server = x.Server()
		CORS(server)
		
		x.Routes(server)
		x.Run(server)

class Client:
	def __init__(kimin, config):
		kimin.path_config = config
	
	def Config(kimin, **parameter):
		if parameter['mode'].lower() == 'get':
			with open(parameter['path'], 'r', encoding='UTF-8') as dataku:
				return json.loads(dataku.read())
		elif parameter['mode'].lower() == 'set':
			with open(parameter['path'], 'w', encoding='UTF-8') as dataku:
				json.dump(parameter['data'], dataku, indent=4)
				return True
	
	def Get_User(kimin, **parameter):
		return parameter['executor'].User_Info(parameter['access_token'])
	
	def Get_Plan(kimin, **parameter):
		return parameter['executor'].Plan_Info(parameter['access_token'])
	
	def Get_Chat(kimin, **parameter):
		return parameter['executor'].Get_Convertasion(parameter['access_token'])
	
	def User_Info(kimin, sin, session):
		user = kimin.Get_User(executor=sin, access_token=session['accessToken'])
		if 'error' in user:
			print(f"{Fore.RED}[*] {user['error']['message']}")
			return False, None
		plan = kimin.Get_Plan(executor=sin, access_token=session['accessToken'])
		print(f"{Fore.LIGHTYELLOW_EX}============== User Information ==============")
		print(f"[*]{Fore.LIGHTGREEN_EX} Nama            : {user['name']}")
		print(f"[*]{Fore.LIGHTGREEN_EX} Email           : {user['email']}")
		print(f"[*]{Fore.LIGHTGREEN_EX} Expired Session : {Date_2_Date(session['expires'])}")
		print(f"[*]{Fore.LIGHTGREEN_EX} Phone           : {user['phone_number']}")
		print(f"[*]{Fore.LIGHTGREEN_EX} Plan            : {plan['account_plan']['subscription_plan']}")
		print(f"[*]{Fore.LIGHTGREEN_EX} Active Plan     : {plan['account_plan']['is_paid_subscription_active']}")
		print(f"[*]{Fore.LIGHTGREEN_EX} Expired Plan    : {plan['account_plan']['subscription_expires_at_timestamp']}")
		print(f"[*]{Fore.LIGHTGREEN_EX} Role Account    : {plan['account_plan']['account_user_role']}")
		print(f"{Fore.LIGHTYELLOW_EX}==============================================")
		return True, {"email":user['email'], "phone":user['phone_number']}
	
	def Chat_Info(kimin, sin, session):
		chat = kimin.Get_Chat(executor=sin, access_token=session['accessToken'])
		print(f"\n{Fore.LIGHTBLUE_EX}============== History Chat ==================")
		for i in chat['items']:
			print(f"{Fore.LIGHTYELLOW_EX}---------------------------------------------")
			print(f"{Fore.LIGHTGREEN_EX}[*] Judul : {i['title']}")
			print(f"{Fore.LIGHTGREEN_EX}[*] ID    : {i['id']}")
			print(f"{Fore.LIGHTGREEN_EX}[*] Create: {Date_2_Date(i['create_time'])}")
			print(f"{Fore.LIGHTGREEN_EX}[*] Update: {Date_2_Date(i['update_time'])}")
			print(f"{Fore.LIGHTYELLOW_EX}---------------------------------------------", end='\r')
		print(f"{Fore.LIGHTYELLOW_EX}---------------------------------------------")
		print(f"{Fore.LIGHTBLUE_EX}==============================================")
		return chat
	
	def Device_Type(kimin):
		return platform.system()
	
	def Banner(kimin):
		print(f"{Fore.LIGHTBLUE_EX}==============================================")
		print(f"{Fore.LIGHTGREEN_EX}           CHAT GPT FREE API                 ")
		print(f"\n\n{Fore.LIGHTGREEN_EX}version   : 1.0                             ")
		print(f"{Fore.LIGHTGREEN_EX}Created By: Kimin                           ")
		print(f"{Fore.LIGHTGREEN_EX}Facebook  : https://www.facebook.com/staykimin")
		print(f"{Fore.LIGHTBLUE_EX}==============================================\n\n")
	
	def Run(kimin):
		config = kimin.Config(path=kimin.path_config, mode='get')
		sin = Execute(ua=config['ua'], cookie=config['cookie'])
		session = sin.Session()
		config['cookie'] = sin.cookie
		kimin.Config(path=kimin.path_config, mode='set', data=config)
		device = kimin.Device_Type()
		if device.lower() == 'windows':
			os.system('cls')
		else:
			os.system('clear')
	
		while True:
			if device.lower() == 'windows':
				os.system('cls')
			else:
				os.system('clear')
			kimin.Banner()
			user = kimin.User_Info(sin, session)
			if not user[0]:
				break
			print(f"\n{Fore.LIGHTYELLOW_EX}============== Menu ========================")
			print(f"{Fore.LIGHTGREEN_EX}[1] New Chat")
			print(f"{Fore.LIGHTGREEN_EX}[2] Select Chat")
			print(f"{Fore.LIGHTGREEN_EX}[3] Delete Chat")
			print(f"{Fore.LIGHTGREEN_EX}[0] Exit")
			print(f"{Fore.LIGHTYELLOW_EX}==============================================")
			menu = input("[*] Nomor Menu Yang Dipilih : ")
			if menu.isnumeric():
				menu = int(menu)
				if menu == 2 or menu == 3:
					if device.lower() == 'windows':
						os.system('cls')
					else:
						os.system('clear')
					kimin.Banner()
					chat = kimin.Chat_Info(sin, session)
					print(f"\n{Fore.LIGHTYELLOW_EX}============== Chat Selection ==============")
					for i in chat['items']:
						print(f"[*]{Fore.LIGHTGREEN_EX}[{chat['items'].index(i)+1}] -> {i['id']}")
					print(f"[*]{Fore.LIGHTGREEN_EX}[0] -> Back")		
					print(f"{Fore.LIGHTYELLOW_EX}==============================================")
					if menu == 2:
						text = "[*] Nomor Chat Yang Akan Dipilih : "
					elif menu == 3:
						text = "[*] Nomor Chat Yang Akan Hapus : "
					mode = input(text)
					if mode.isnumeric():
						mode = int(mode)
						if menu == 2 and mode <= len(chat['items']):
							if not mode == 0:
								if device.lower() == 'windows':
									os.system('cls')
								else:
									os.system('clear')
								kimin.Banner()
								respon, tmp_id = sin.Get_Respon(session['accessToken'], chat['items'][mode-1]['id']), []
								for i in respon:
									tmp_id.append(i['id'])
									role = i['author']['role'] 
									text = "\n".join(i['content']['parts'])
									print(f"{role} : {text}")
								
								while True:
									config = kimin.Config(path=kimin.path_config, mode='get')
									sin = Execute(ua=config['ua'], cookie=config['cookie'])
									session = sin.Session()
									config['cookie'] = sin.cookie
									kimin.Config(path=kimin.path_config, mode='set', data=config)
									text = input("[*] Your Convertasion Ketik 0 Untuk Kembali : ")
									if text == "0":
										break
									else:
										promt = input("Masukkan Promt Jika Ada & Tekan Enter Jika Tidak : ")
										if promt == "":
											promt = sin.Get_Promt(session['accessToken'])
											promt = [i['description'] for i in promt['items']]
										else:
											promt = [promt]
										chat_req = sin.Get_Chat_Req(session['accessToken'])
										x = sin.Chat(chat_token=chat_req['token'], promt=promt, text=[text], id=chat['items'][mode-1]['id']) 
										while True:
											respon = sin.Get_Respon(session['accessToken'], chat['items'][mode-1]['id'])
											if not respon[-1]['id'] in tmp_id and respon[-1]['end_turn']:
												y = '\n'.join(respon[-1]['content']['parts'])
												print(f"user : {text}")
												print(f"{respon[-1]['author']['role']} : {y}")
												break
											time.sleep(1)
						
						elif menu == 3 and mode <= len(chat['items']):
							if not mode == 0:
								respon = sin.Delete_Chat(session['accessToken'], chat['items'][mode-1]['id'])
								print(respon)
								input("[*] Tekan ENTER Untuk Kembali!")
				elif menu == 1:
					if device.lower() == 'windows':
						os.system('cls')
					else:
						os.system('clear')
					kimin.Banner()
					tmp_id = []
					id = None
					while True:
						config = kimin.Config(path=kimin.path_config, mode='get')
						sin = Execute(ua=config['ua'], cookie=config['cookie'])
						session = sin.Session()
						config['cookie'] = sin.cookie
						kimin.Config(path=kimin.path_config, mode='set', data=config)
						text = input("\r[*] Your Convertasion Ketik 0 Untuk Kembali : ")
						if text == "0":
							break
						else:
							promt = input("\rMasukkan Promt Jika Ada & Tekan Enter Jika Tidak : ")
							if promt == "":
								promt = sin.Get_Promt(session['accessToken'])
								promt = [i['description'] for i in promt['items']]
							else:
								promt = [promt]
							chat_req = sin.Get_Chat_Req(session['accessToken'])
							if id is None:
								x = sin.Chat(chat_token=chat_req['token'], promt=promt, text=[text])
							else:
								x = sin.Chat(chat_token=chat_req['token'], promt=promt, text=[text], id=id)
							while True:
								respon = sin.Get_Respon(session['accessToken'], x['conversation_id'])
								if not respon[-1]['id'] in tmp_id and respon[-1]['end_turn']:
									y = '\n'.join(respon[-1]['content']['parts'])
									id = x['conversation_id']
									print(f"user : {text}")
									print(f"{respon[-1]['author']['role']} : {y}")
									break
								time.sleep(1)
				elif menu == 0:
					break
			
			else:
				print(f"{Fore.RED}[*] Hanya Menerima Inputan Berupa Nomor/Angka Saja")
				input("[*] Tekan ENTER Untuk Kembali!")
			
