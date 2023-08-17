from datetime import datetime
import importlib
import os
import re



def file_save(file_path, file_text):
	
	with open(file_path, "w") as file:
		file.write(file_text)

	if file_path.split(".")[-1] == "txt":

		print(f"测试结果已保存至: {file_path}  (只保存验证成功的URL)")

	elif file_path.split(".")[-1] == "html":
		print(f"测试结果已保存至: {file_path}  (只保存验证成功的URL)")

	elif file_path.split(".")[-1] == "html":
		print(f"测试结果已保存至: {file_path}")


def type_txt(results, file_path, current_time):

	file_text = ""

	for url, poc_list in results.items():
		if poc_list:
			file_text += '{}\n{}\n\n'.format(url, '\n'.join('\t' + poc for poc in poc_list))

	file_save(file_path, file_text)


def type_html(results, file_path, current_time):

	html = ""

	HTML = open("C:/Users/zhangsan9527/Desktop/MyPoC/config/results model.html", "r", encoding="utf-8").read()

	REFERENCE_link = ""

	for url, poc_list in results.items():

		URL = f'  <li class="item">\n	<div class="link" onclick="toggleAllDetails(this)">\n	  <span class="arrow">▼</span>\n	  {url}\n	</div>\n'

		POC_DESCRIPTION = ""

		for poc, POC_RETURN in poc_list.items():

			if poc:

				INTRODUCE, reference_link = importlib.import_module("poc."+poc+"."+poc).poc_description()

				REFERENCE_link = ""

				POC = f'	  <div class="details" onclick="togglebtn(this)">\n		 <span class="btn">▼</span>\n	   {poc}\n	  </div>\n'

				POC_DES = f'		<div class="description-box">\n		  <p><strong>测试结果：</strong></p>\n		  <p>{POC_RETURN}</p>\n		  <br>\n		  <p><strong>介绍：</strong></p>\n		  <p>{INTRODUCE}\n		  </p>\n		  <br>\n		  <p><strong>参考链接：</strong></p>\n'

				for ref_link in reference_link:

					REFERENCE_link += f'		  <p><a href="{ref_link}" target="_blank">{ref_link}</a></p>\n'

				POC_DESCRIPTION += f'{POC}{POC_DES}{REFERENCE_link}		</div>\n'

			html += f'{URL}	<div class="details-container">\n{POC_DESCRIPTION}	</div>\n\n  </li>\n'

	file_text = re.sub(r'  <li class="item">(.*?)  </li>', html, HTML, flags=re.DOTALL)

	file_save(file_path, file_text)



def type_excel():
	print("功能待完善")


def Result_save(results,filetype):
	
	print("\n正在保存...")

	current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S").split(" ")

	# 构建文件夹和文件路径
	folder_path = os.path.join("results", current_time[0])
	
	# 创建文件夹（如果不存在）
	os.makedirs(folder_path, exist_ok=True)

	if "txt" in filetype:
		
		file_path = os.path.join(folder_path, f"{current_time[1]}.txt")
		
		type_txt(results, file_path, current_time)

	if "html" in filetype:
		
		file_path = os.path.join(folder_path, f"{current_time[1]}.html")

		type_html(results, file_path, current_time)

	if "excel" in filetype:
		
		file_path = os.path.join(folder_path, f"{current_time[1]}.xlsx")

		type_excel()