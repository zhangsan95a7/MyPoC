from argparse import ArgumentParser
from lib.core import result_save
import os
import re
import importlib
import threading
from datetime import datetime
import json



class NewArgumentParser(ArgumentParser):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# 添加一个自定义组，名称为 "Options"
		self._optionals.title = 'Help Options'


class MyPoC:
	def __init__(self):
		# 创建一个线程锁和计数器
		self.progress_lock = threading.Lock()
		
		# 已测试URL数量
		self.current_target_count = 0

		# 存在漏洞URL个数
		self.vul_count = 0
		
		# 测试结果
		self.results = {}


	def get_pocs(self):
		pocs = []
		for dir_name in os.listdir("./poc/"):
			if os.path.isdir(os.path.join("./poc/", dir_name)):
				pocs.append(dir_name)

		return pocs


	def poc_laod(self):

		poc = []

		all_pocs = self.get_pocs()

		if self.args.poc:
			poc = [self.args.poc]

		elif self.args.poc_fuzz == "all":
			poc = all_pocs

		else:
			# 通过关键词匹配poc进行测试
			for poc_keyword in self.args.poc_fuzz.split("|"):
				for poc_tmp in all_pocs:
					if any(re.finditer(poc_keyword, poc_tmp, re.IGNORECASE)) and poc_tmp not in poc:
						poc.append(poc_tmp)

		return poc


	def poc_update(self):
		print("功能待完善")


	def poc_search(self,keyword):
		# 搜索结果中被命中的关键词高亮显示
		print(f"POC搜索结果:	关键词 {keyword}")
		print("-----------------------------------")
		pocs = self.get_pocs()
		for poc in pocs:
			if keyword.lower() in poc.lower():
				matches = re.finditer(keyword, poc, re.IGNORECASE)

				results = ""
				prev_end = 0

				for match in matches:
					start, end = match.span()
					results += poc[prev_end:start] + "\033[31m" + poc[start:end] + "\033[0m"
					prev_end = end

				results += poc[prev_end:]

				print(results)


	def poc_show(self):
		pocs = self.get_pocs()
		print(f"POC列表:    总计 {len(pocs)}")
		print("-----------------------------------")
		for poc in pocs:
			print(poc)


	def get_args(self):
		parser = NewArgumentParser()

		poc = parser.add_argument_group("POC Options")


		# POC参数
		poc.add_argument("-p", "--poc", dest="poc", help="指定POC名称，eg: -p pocname")

		poc.add_argument("--poc-search", dest="poc_search", help="模糊搜索POC，eg: --poc-search=RCE")# 实现不区分大小写

		poc.add_argument("--poc-list", dest="poc_list", action="store_true", help="输出所有POC")

		poc.add_argument("--poc-fuzz", dest="poc_fuzz", help='批量测试，通过关键词匹配poc进行测试，支持多个关键词，eg: --poc-fuzz="OA|SQL" 或 --poc-fuzz=all 进行全量POC测试')

		poc.add_argument("--poc-update", dest="poc_update", action="store_true", help="更新POC库")

		poc.add_argument("--poc-info", dest="poc_info",  help='获取POC详情，eg: --poc-info="pocname"')


		# Target参数
		target = parser.add_argument_group("Target Options")

		target.add_argument("-u", "--url", dest="url", help='指定目标url，eg: -u "https://example.com"')

		target.add_argument("-f", "--file", dest="target_file", help="指定目标文件，eg: -f targets.txt")


		# 其他参数
		other = parser.add_argument_group("Other Options")

		other.add_argument("--thread", dest="thread", type=int, help="设置最大线程数，默认为5，eg: --thread=10")

		other.add_argument("--out-put", dest="filetype", help='指定保存结果的文件类型，支持txt，html，excel，可同时输出多种类型，eg: --out-put="txt|html|excel"')

		other.add_argument("--proxy", dest="proxy", help='设置代理，eg: --proxy="http://127.0.0.1:8080"')

		other.add_argument("--time-out", dest="time", type=int, help='设置响应超时，默认为3s，eg: --time-out=5')


		# 返回命令行参数
		return parser.parse_args()


	def payloading(self,poc,target):

		try:
			vul, POC_RETURN = importlib.import_module("poc."+poc+"."+poc).payload(target=target)
		except:
			vul = False

		with self.progress_lock:

			self.current_target_count += 1

			if vul:

				self.vul_count += 1
				self.results[target][poc] = POC_RETURN
				print(f"\033[0;31;40m[!]  Progress: {self.current_target_count}/{self.total}  vul: {self.vul_count}  {target}   存在  {poc}\033[0m")
			
			else:
				print(f"[*]  Progress: {self.current_target_count}/{self.total}  vul: {self.vul_count}  {target}   不存在  {poc}")


	def config_update(self,action):

		config_file =  open("./config/config.json", "r+", encoding="utf-8")
		config = json.load(config_file)

		if self.args.proxy:
			if action == "change":
				config["proxy"] = self.args.proxy
			elif action == "recover":
				config["proxy"] = ""

		if self.args.time:
			if action == "change":
				config["timeout"] = self.args.time
			elif action == "recover":
				config["timeout"] = 3

		config_file.seek(0)# 将文件读写位置移动到文件开头
		json.dump(config, config_file, indent=4, ensure_ascii=False)
		config_file.truncate()# 截断文件，以确保不包含旧的内容


	def mypoc(self):

		start_time = datetime.now()

		self.args = self.get_args()

		if not self.args.poc_search and not self.args.poc_list and not self.args.poc_update and not self.args.poc_info:

			if not self.args.poc and not self.args.poc_fuzz:
				print("未指定POC")
				return

			if not self.args.url and not self.args.target_file:
				print("未指定目标URL")
				return

			if self.args.url and self.args.target_file:
				print("不能同时出现 -u -f 参数")

		elif self.args.poc_search:
			self.poc_search(self.args.poc_search)
			return

		elif self.args.poc_list:
			self.poc_show()
			return

		elif self.args.poc_update:
			self.poc_update()
			return

		elif self.args.poc_info:
			try:
				
				introduce, reference_link = importlib.import_module("poc."+self.args.poc_info+"."+self.args.poc_info).poc_description()
				
				print("介绍：\n{}\n\n参考链接：\n{}".format(introduce, '\n'.join(reference_link)))

			except:
				print("获取POC详情失败")

			return

		if self.args.url:
			Targets = [self.args.url]
		else:
			Targets = list(filter(None, open(self.args.target_file, "r", encoding="utf-8").read().split("\n")))


		if self.args.thread:
			max_threads = self.args.thread
		else:
			max_threads = 5

		self.targets = len(Targets)

		self.pocs = self.poc_laod()

		self.total = self.targets * len(self.pocs)

		if self.pocs == []:
			print("未找到POC")
			return

		self.config_update(action="change")

		# 创建线程并启动，控制最大线程数
		threads = []

		for Target in Targets:
			self.results[Target] = {}
			for poc in self.pocs:
				while threading.active_count() >= max_threads:
					pass  # 等待，直到线程数小于最大线程数

				thread = threading.Thread(target=self.payloading, args=(poc, Target))
				threads.append(thread)
				thread.start()

		# 等待所有线程结束
		for thread in threads:
			thread.join()

		stop_time = datetime.now()
		delta = stop_time - start_time
		minutes, seconds = divmod(delta.total_seconds(), 60)

		print(f"\n测试URL: {self.targets}  测试POC: {len(self.pocs)}  漏洞个数: {self.vul_count}  耗时: {int(minutes)}分{int(seconds)}秒")

		self.config_update(action="recover")

		if self.args.filetype:
			
			result_save.Result_save(self.results,self.args.filetype)



if __name__ == '__main__':

	print("""
  ███╗   ███╗██╗   ██╗██████╗  ██████╗  ██████╗
  ████╗ ████║╚██╗ ██╔╝██╔══██╗██╔═══██╗██╔════╝
  ██╔████╔██║ ╚████╔╝ ██████╔╝██║   ██║██║     
  ██║╚██╔╝██║  ╚██╔╝  ██╔═══╝ ██║   ██║██║     
  ██║ ╚═╝ ██║   ██║   ██║     ╚██████╔╝╚██████╗
  ╚═╝     ╚═╝   ╚═╝   ╚═╝      ╚═════╝  ╚═════╝                                             
  """)

	MYPOC = MyPoC()
	MYPOC.mypoc()
