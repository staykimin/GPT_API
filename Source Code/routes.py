from flask import request
from kimin.core_executor import Execute
import datetime, os, json, time

with open('server_config.min', 'r', encoding='UTF-8') as dataku:
	cfg = json.loads(dataku.read())

def Date_2_Date(data, format='%d-%m-%Y %H:%M:%S'):
	return datetime.datetime.fromisoformat(data.replace('Z', '+00:00')).strftime(format)

def Config(**parameter):
	if parameter['mode'].lower() == 'get':
		with open(parameter['path'], 'r', encoding='UTF-8') as dataku:
			return json.loads(dataku.read())
	elif parameter['mode'].lower() == 'set':
		with open(parameter['path'], 'w', encoding='UTF-8') as dataku:
			json.dump(parameter['data'], dataku, indent=4)
			return True

def Get_User(**parameter):
	return parameter['executor'].User_Info(parameter['access_token'])

def Get_Plan(**parameter):
	return parameter['executor'].Plan_Info(parameter['access_token'])

def User_Info(sin, session):
	hasil = {'status':True}
	user = Get_User(executor=sin, access_token=session['accessToken'])
	if 'error' in user:
		hasil['status'] = False
		hasil['data'] = user['error']['message']
	else:
		plan = Get_Plan(executor=sin, access_token=session['accessToken'])
		hasil['data'] = {
			'nama':user['name'], 
			'email':user['email'], 
			'expired_session':Date_2_Date(session['expires']),
			'phone':user['phone_number'],
			'plan':plan['account_plan']['subscription_plan'],
			'active_plan':plan['account_plan']['is_paid_subscription_active'],
			'expired_plan':plan['account_plan']['subscription_expires_at_timestamp'],
			'role_account':plan['account_plan']['account_user_role']
			}
	
	return hasil

def Get_Chat(**parameter):
	return parameter['executor'].Get_Convertasion(parameter['access_token'])

def Chat_Info(sin, session):
	hasil = {}
	chat = Get_Chat(executor=sin, access_token=session['accessToken'])
	hasil['data'] = [{"judul":i['title'], 'id_chat':i['id'], 'created_at':Date_2_Date(i['create_time']), 'update_at':Date_2_Date(i['update_time'])} for i in chat['items']]
	return hasil

def API(mode):
	path = cfg['user_config']
	config = Config(path=path, mode='get')
	sin = Execute(ua=config['ua'], cookie=config['cookie'])
	session = sin.Session()
	config['cookie'] = sin.cookie
	Config(path=path, mode='set', data=config)
	user = User_Info(sin, session)
	if mode == 'user_info':
		return user
	
	elif mode == 'get_chat':
		chat = Chat_Info(sin, session)
		return chat
	
	elif mode == 'delete_chat':
		id = request.form['id_chat']
		respon = sin.Delete_Chat(session['accessToken'], id)
		return respon
		
	elif mode == 'new_chat':
		text = request.form['text']
		promt = sin.Get_Promt(session['accessToken'])
		promt = [i['description'] for i in promt['items']]
		if 'promt' in request.form:
			promt = [request.form['promt']]
		
		chat_req = sin.Get_Chat_Req(session['accessToken'])
		if 'id_chat' is request.form:
			x = sin.Chat(chat_token=chat_req['token'], promt=promt, text=[text], id=request.form['id_chat'])
		else:
			x = sin.Chat(chat_token=chat_req['token'], promt=promt, text=[text])
		
		while True:
			respon = sin.Get_Respon(session['accessToken'], x['conversation_id'])
			if respon[-1]['end_turn']:
				y = '\n'.join(respon[-1]['content']['parts'])
				id = x['conversation_id']
				return {"id_chat":id, 
					'data':[
						{'role':'user', 'text':text},
						{'role':respon[-1]['author']['role'], 'text':y}
						]
					}
			time.sleep(1)
