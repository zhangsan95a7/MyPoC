
# 请勿删除该文件
# 请将该文件复制到poc目录下进行编辑测试

# requests模块已重写为Requests，如果不使用重写的Requests模块，则不能使用--proxy参数
from lib.request.requests_new import Requests


# 下面为主函数，不要修改函数名
def payload(target):
	
	uri = "/exec.php?cmd=echo success" # 注意uri首字符必须带“/”
	url = target+uri
	headers = {}
	data = "" # post请求加上该参数

	response = Requests().get(url, headers=headers, timeout=3, verify=False).text

	POC_RETURN = "success"

	# 判断是否执行成功，成功返回True，否则返回False
	if "Script Output" in response:
		return True, POC_RETURN
	else:
		return False, POC_RETURN


# 添加POC详情，方便使用者更容易地复现，比如POC介绍、复现的参考链接
def poc_description():
	
	# 介绍（漏洞原理、修复建议等）
	introduce = """该漏洞是..."""

	# 参考链接，可放多个
	reference_link = ["https://www.example.com"]

	return introduce, reference_link

