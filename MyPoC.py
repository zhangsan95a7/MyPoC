from argparse import ArgumentParser
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
		self.current_count = 0

		self.vul_count = 0
		self.results = []


	def get_pocs(self):
		poc_files = os.listdir("./poc/")
		pocs = []
		for file_name in poc_files:
			if os.path.isfile(os.path.join("./poc/", file_name)):
				pocs.append(os.path.splitext(file_name)[0])

		return pocs



	def poc_search(self,keyword):
		# 搜索结果中被命中的关键词高亮显示
		print("POC搜索结果:	关键词 "+keyword)
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
		print("POC列表:    总计 "+str(len(pocs)))
		print("-----------------------------------")
		for poc in pocs:
			print(poc)


	def get_args(self):
		parser = NewArgumentParser()

		poc = parser.add_argument_group("POC Options")


		# POC参数
		poc.add_argument("-p", "--poc", dest="poc", help="指定POC名称，eg: -p 某某某RCE")

		poc.add_argument("--poc-search", dest="poc_search", help="搜索POC，eg: --poc-search=RCE")# 实现不区别大小写

		poc.add_argument("--poc-list", dest="poc_list", help="输出所有POC")

		poc.add_argument("--poc-fuzz", dest="poc_fuzz", help="批量测试，通过关键词匹配poc进行测试，支持多个关键词，eg: --poc-fuzz=OA|SQL 或 --poc-fuzz=all 进行全量POC测试")

		poc.add_argument("--poc-update", dest="poc_update", help="更新POC库")


		# Target参数
		target = parser.add_argument_group("Target Options")

		target.add_argument("-u", "--url", dest="url", help='指定目标url，eg: -u "https://example.com"')

		target.add_argument("-f", "--file", dest="target_file", help="指定目标文件，eg: -f targets.txt")


		# 其他参数
		other = parser.add_argument_group("Other Options")

		other.add_argument("--thread", dest="thread", type=int, help="设置最大线程数，默认为5，eg: --thread=10")

		other.add_argument("--out-put", dest="filetype", help="指定保存结果的文件类型，支持txt，html，excel，可同时输出多种类型，eg: --out-put=txt|html|excel")

		other.add_argument("--proxy", dest="proxy", help='设置代理，eg: --proxy="http://127.0.0.1:8080"')

		other.add_argument("--time-out", dest="time", type=int, help='设置响应超时，默认为3s，eg: --time-out=5')


		# 返回命令行参数
		return parser.parse_args()


	def payloading(self,poc,target,total):

		try:
			vul = importlib.import_module("poc."+poc).payload(target=target)
		except:
			vul = False

		with self.progress_lock:

			self.current_count += 1

			if vul:
				self.vul_count += 1
				self.results.append({target:poc})
				print("\033[0;31;40m[!]  Progress: "+str(self.current_count)+"/"+str(total)+"  vul: "+str(self.vul_count)+"  "+target+"   存在  "+poc+"\033[0m")
			
			else:
				print("[*]  Progress: "+str(self.current_count)+"/"+str(total)+"  vul: "+str(self.vul_count)+"  "+target+"   不存在  "+poc)


	def result_save(self):
		
		print("\n正在保存...")

		current_path = os.getcwd()
		current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S").split(" ")

		# 构建文件夹和文件路径
		folder_path = os.path.join("results", current_time[0])
		

		# 创建文件夹（如果不存在）
		os.makedirs(folder_path, exist_ok=True)

		if "txt" in self.args.filetype:
			
			file_path = os.path.join(folder_path, f"{current_time[1]}.txt")
			
			results = [list(result.keys())[0] for result in self.results]

			with open(file_path, "w") as file:
				file.write("\n".join(results))
			
			print("测试结果已保存至: "+file_path+"  (txt类型只保存验证成功的URL)")


		if "html" in self.args.filetype:
			pass

		if "excel" in self.args.filetype:
			pass


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

		if not self.args.poc_search and not self.args.poc_list:

			if not self.args.poc:
				print("缺少 -p 参数")
				return

			if not self.args.url and not self.args.target_file:
				print("缺少 -u 参数，或缺少 -f 参数")
				return

			if self.args.url and self.args.target_file:
				print("不能同时出现 -u -f 参数")

		elif self.args.poc_search:
			self.poc_search(self.args.poc_search)
			return

		elif self.args.poc_list:
			self.poc_show()
			return

		if self.args.url:
			Targets = [self.args.url]
		else:
			Targets = list(filter(None, open(self.args.target_file, "r", encoding="utf-8").read().split("\n")))


		if self.args.thread:
			max_threads = self.args.thread
		else:
			max_threads = 5

		total = len(Targets)

		if self.args.poc not in self.get_pocs():
			print("不存在poc: "+self.args.poc)
			return

		self.config_update(action="change")

		# 创建线程并启动，控制最大线程数
		threads = []
		for Target in Targets:
			
			while threading.active_count() >= max_threads:
				pass  # 等待，直到线程数小于最大线程数

			thread = threading.Thread(target=self.payloading, args=(self.args.poc, Target, total))
			threads.append(thread)
			thread.start()

		# 等待所有线程结束
		for thread in threads:
			thread.join()

		stop_time = datetime.now()
		delta = stop_time - start_time
		minutes, seconds = divmod(delta.total_seconds(), 60)

		print(f"\n测试URL: {total}  漏洞URL: {self.vul_count}  耗时: {int(minutes)}分{int(seconds)}秒")

		self.config_update(action="recover")

		if self.args.filetype:
			
			self.result_save()


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
