import requests
import json
import os
import sys
import urllib3

# 禁用 SSL 错误警告输出
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Requests(requests.Session):
	def __init__(self, proxy=None, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if sys.platform == "win32":

			current_path = os.getcwd().split("\\")

		elif sys.platform == "linux":

			current_path = os.getcwd().split("/")

		with open("/".join(current_path)+"/config/config.json", "r") as config_file:
			self.config = json.load(config_file)


	def request(self, method, url, *args, **kwargs):

		kwargs["proxies"] = {"http": self.config["proxy"], "https": self.config["proxy"]}
		kwargs["verify"] = False
		kwargs["verify"] = self.config["timeout"]
		
		return super().request(method, url, *args, **kwargs)
