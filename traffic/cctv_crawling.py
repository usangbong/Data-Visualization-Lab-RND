import json
import requests
import subprocess

def video(channel):
  source = ''
  url = 'https://map.naver.com/v5/api/cctv/list?channel=' + channel
  data = requests.get(url).json()

  for cctv in data['message']['result']['cctvList']:
    if cctv['channel'] == int(channel):
      liveParam = cctv['liveEncryptedString']
      if liveParam is None:
        liveParam = cctv['encryptedString']

      url = 'http://cctvsec.ktict.co.kr/' + channel + '/' + liveParam

      headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Host': 'cctvsec.ktict.co.kr',
        'Set-Fetch-Dest': 'empty',
        'Set-Fetch-Mode': 'cors',
        'Set-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
      }
      response = requests.get(url, headers = headers)
      source = response.url

      return source

# 어린이대공원 CCTV
source = video('6237')

result = subprocess.Popen(['ffmpeg', '-i', source, '-t', '10', '-c', 'copy', 'test.ts'], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
out, err = result.communicate()
exitcode = result.returncode
if exitcode != 0:
    print(exitcode, out.decode('utf8'), err.decode('utf8'))
else:
    print('Completed')