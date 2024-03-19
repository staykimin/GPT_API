import requests
class Driver:
	def __init__(kimin, **parameter):
		kimin.parameter = parameter
	
	def Execute(kimin):
		hasil = {'status':False}
		try:
			if kimin.parameter['method'].lower() == 'get':
				respon = requests.request(kimin.parameter['method'], kimin.parameter['url'], headers=kimin.parameter.get('header', {}))
			elif kimin.parameter['method'].lower() == 'post' or 'patch':
				if kimin.parameter['data_type'].lower() == 'json':
					respon = requests.request(kimin.parameter['method'], kimin.parameter['url'], headers=kimin.parameter.get('header', {}), json=kimin.parameter['data'])
				elif kimin.parameter['data_type'].lower() == 'form':
					respon = requests.request(kimin.parameter['method'], kimin.parameter['url'], headers=kimin.parameter.get('header', {}), data=kimin.parameter['data'])
			hasil['status'], hasil['data'], hasil['status_code'], hasil['respon']= True, respon.text, respon.status_code, respon
		except requests.Timeout:
			hasil['data'] = "Timeout"
		except requests.RequestException as e:
			hasil['data'] = 'Tidak Dapat Terhubung Ke Server'
		
		return hasil
