import requests
import os

# 设置请求头，模拟浏览器访问以避免被拒绝
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 获取原始URL列表
sub_all_clash_url = 'https://raw.githubusercontent.com/GameAutoScript/collectSub/main/sub/sub_all_clash.txt'
try:
    response = requests.get(sub_all_clash_url, headers=headers, timeout=10)
    response.raise_for_status()
    urls = response.text.splitlines()
    print(f"成功获取到 {len(urls)} 个URL")
except Exception as e:
    print(f"获取URL列表失败: {e}")
    exit()

# 收集所有网页内容
output_filename = 'combined_content.txt'
with open(output_filename, 'w', encoding='utf-8') as out_file:
    for index, url in enumerate(urls, 1):
        try:
            print(f"正在处理 ({index}/{len(urls)})：{url}")
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            
            # 自动检测编码（更可靠的方式）
            resp.encoding = resp.apparent_encoding
            
            # 写入分隔标识和内容
            out_file.write(f"\n\n{'=' * 50}\n")
            out_file.write(f"# 来源URL: {url}\n")
            out_file.write(f"{'=' * 50}\n\n")
            out_file.write(resp.text)
        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
        except Exception as e:
            print(f"处理时发生未知错误: {e}")

print(f"所有内容已保存到 {output_filename}")

# 在原有代码最后追加以下内容
if os.getenv('GITHUB_ACTIONS') == 'true':
    print("检测到在GitHub Actions环境中运行，自动提交结果...")
    os.system('git config --global user.name "GitHub Actions"')
    os.system('git config --global user.email "actions@github.com"')
    os.system('git add combined_content.txt')
    os.system('git commit -m "Auto update collected content"')
    os.system('git push')