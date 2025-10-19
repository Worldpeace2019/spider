import requests
import json
import os
import time

key_words = input("请输入关键字:  ")
pages = int(input("请输入页数:  "))

# 定义保存文件夹路径
save_dir = "baidu_img"
os.makedirs(save_dir, exist_ok=True)

# 显示保存路径信息
current_dir = os.getcwd()
full_save_path = os.path.join(current_dir, save_dir)
print(f"\n图片将保存到: {full_save_path}\n")

success_count = 0
fail_count = 0

for page in range(pages):
    base_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&logid=6479461037240569120&ipn=rj&ct=201326592&is=&fp=result&fr=&word=cat&queryWord=cat&cl=2&lm=&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn=1&rn=30&gsm=3c&1717504898319='
    url, payload_string = base_url.split('?')
    payload = {word.split('=')[0]: word.split('=')[1] for word in payload_string.split('&')}
    payload["word"] = payload["queryWord"] = key_words
    payload["pn"] = str(page * 30 + 1)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"}

    session = requests.Session()
    response = session.get(url)
    cookies = session.cookies.get_dict()
    re = requests.get(url=url, headers=headers, cookies=cookies, params=payload)

    data_raw = re.text.replace("'", "\"")
    data = json.loads(data_raw)
    imgs = data["data"][:-1]

    for index, li in enumerate(imgs, start=1):
        img = li["thumbURL"]
        file_name = f"{index + page * 30}.jpg"
        file_path = os.path.join(save_dir, file_name)

        print(f"正在下载 {index + page * 30}.jpg: {img}")
        try:
            response = requests.get(img, headers=headers, timeout=10)
            response.raise_for_status()  # 检查请求是否成功

            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"✔ 已保存到 {file_path}")
            success_count += 1
        except Exception as e:
            print(f"✘ 下载失败: {e}")
            fail_count += 1

        time.sleep(1)  # 避免请求过快

# 显示下载统计信息
print(f"\n下载完成！共尝试下载 {success_count + fail_count} 张图片")
print(f"成功: {success_count} 张")
print(f"失败: {fail_count} 张")
print(f"图片保存位置: {full_save_path}")