class Header_Processing:
	def __init__(kimin, *argument):
		kimin.ua, kimin.cookie = argument[0], argument[1]
		kimin.header = {
			"Accept": "*/*",
			"Accept-Language": "en-US,en;q=0.5",
			"Host": "chat.openai.com",
			"User-Agent": kimin.ua,
			"Connection": "keep-alive",
			"Cookie":kimin.cookie,
			"Sec-Fetch-Dest": "empty",
			"Sec-Fetch-Mode": "cors",
			"Sec-Fetch-Site": "same-origin",
			"TE": "trailers"
			}
	def Session_Header(kimin):
		kimin.header['Referer'], kimin.header['If-None-Match'] = "https://chat.openai.com/", 'W/"77g3j8q5vd1br"'
		return kimin.header
	
	def Api_Header(kimin, x):
		kimin.header['Referer'], kimin.header['Authorization'], kimin.header['OAI-Device-Id'], kimin.header['OAI-Language'] = "https://chat.openai.com/", f'Bearer {x}', kimin.cookie.split("oai-did=")[-1].split(";")[0], 'en-US' 
		return kimin.header
	
	def Chat_ReqHeader(kimin, x):
		kimin.header['Origin'] = "https://chat.openai.com/"
		return kimin.header
	
	def Convertasion_Header(kimin, x):
		kimin.header['OpenAI-Sentinel-Chat-Requirements-Token'] = x
		return kimin.header
