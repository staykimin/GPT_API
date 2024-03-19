import requests, json, uuid
from .core_header import Header_Processing
from .core_driver import Driver

class Execute(Header_Processing):
	def __init__(kimin, **parameter):
		kimin.parameter = parameter
		kimin.base_url = 'https://chat.openai.com'
		super().__init__(parameter['ua'], parameter['cookie'])
		
	def Session(kimin):
		data = Driver(
			method='get', 
			url =f"{kimin.base_url}/api/auth/session",
			header=kimin.header,
			).Execute()
		if data['status']:
			tmp = [f"{i}={data['respon'].cookies.get_dict()[i]}" for i in data['respon'].cookies.get_dict()]
			kimin.cookie = "; ".join(tmp)
			return json.loads(data['data'])
		else:
			return data
	
	def User_Info(kimin, access_token):
		data = Driver(
			method='get', 
			url =f"{kimin.base_url}/backend-api/me",
			header=kimin.Api_Header(access_token),
			).Execute()
		if data['status']:
			return json.loads(data['data'])
		else:
			return data
	
	def Plan_Info(kimin, access_token):
		data = Driver(
			method='get',
			url=f'{kimin.base_url}/backend-api/accounts/check',
			header=kimin.Api_Header(access_token)
			).Execute()
		if data['status']:
			return json.loads(data['data'])
		else:
			return data
	
	def Get_Convertasion(kimin, access_token):
		data = Driver(
			method='get', 
			url =f"{kimin.base_url}/backend-api/conversations",
			header=kimin.Api_Header(access_token),
			).Execute()
		if data['status']:
			return json.loads(data['data'])
		else:
			return data
	
	def Get_Chat_Req(kimin, access_token):
		data = {'conversation_mode_kind':"primary_assistant"}
		data = Driver(
			method='post', 
			url =f"{kimin.base_url}/backend-api/sentinel/chat-requirements",
			header=kimin.Api_Header(access_token),
			data_type='json',
			data=data
			).Execute()
		if data['status']:
			return json.loads(data['data'])
		else:
			return data
	
	def Socket_Token(kimin, access_token):
		data = {}
		data = Driver(
			method='post', 
			url =f"{kimin.base_url}/backend-api/register-websocket",
			header=kimin.Api_Header(access_token),
			data_type='json',
			data=data
			).Execute()
		if data['status']:
			return json.loads(data['data'])
		else:
			return data
	
	def Get_Promt(kimin, access_token):
		data = Driver(
			method='get', 
			url =f"{kimin.base_url}/backend-api/prompt_library/?limit=4&offset=0",
			header=kimin.Api_Header(access_token),
			).Execute()
		if data['status']:
			return json.loads(data['data'])
		else:
			return data
	
	def Get_Respon(kimin, access_token, id):
		data = Driver(
			method='get',
			url=f"{kimin.base_url}/backend-api/conversation/{id}",
			header=kimin.Api_Header(access_token),
			).Execute()
		if data['status']:
			respon = json.loads(data['data'])
			respon = [respon['mapping'][i]['message'] for i in respon['mapping']]
			respon = [i for i in respon if not i is None and not i['author']['role'] == 'system']
			return respon
		else:
			return data
	
	def Delete_Chat(kimin, access_token, id):
		data = Driver(
			method='patch',
			url=f"{kimin.base_url}/backend-api/conversation/{id}",
			header=kimin.Api_Header(access_token),
			data_type='json',
			data={"is_visible":False}
			).Execute()
		if data['status']:
			return json.loads(data['data'])
		else:
			return data
	
	def Chat(kimin, **parameter):
		data = {
				"action":"next",
				"messages":[
						{
							"id":str(uuid.uuid4()),
							"author":{"role":"user"},
							"content":{
								"content_type":"text",
								"parts":parameter['text'],
								},
							"metadata":{}
								
						}
					],
				"model":"text-davinci-002-render-sha",
				"timezone_offset_min": -420,
				"parent_message_id":str(uuid.uuid4()),
				"websocket_request_id":str(uuid.uuid4()),
				"suggestions":parameter['promt'],
				"history_and_training_disabled": False,
				"conversation_mode": {
					"kind": "primary_assistant"
					},
				"force_paragen": False,
				"force_rate_limit": False
			}
		if 'id' in parameter:
			data['conversation_id'] = parameter['id']
		
		data = Driver(
			method='post', 
			url =f"{kimin.base_url}/backend-api/conversation",
			header=kimin.Convertasion_Header(parameter['chat_token']),
			data_type='json',
			data=data
			).Execute()
		
		if data['status']:
			return json.loads(data['data'])
		else:
			return data