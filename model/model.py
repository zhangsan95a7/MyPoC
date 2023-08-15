
# 请勿删除该文件
# 请将该文件复制到poc目录下进行编辑测试

# requests模块已重写为Requests，如果不使用重写的Requests模块，则不能使用--proxy参数
from lib.request.requests_new import Requests

# 下面为主函数，不要修改函数名
def main(target):
	
	uri = "/exec.php?cmd=echo success" # 注意uri首字符必须带“/”
	url = target+uri
	headers = {}
	data = "" # post请求加上该参数

	request = Requests()
	response = Requests.get(url, headers=headers, timeout=3, verify=False)

	# 判断是否执行成功，成功返回True，否则返回False
	if "success" in response.text:
		return True
	else:
		return False