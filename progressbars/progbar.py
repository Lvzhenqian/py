import requests
import progressbar


requests.packages.urllib3.disable_warnings()

url = "http://dldir1.qq.com/qqfile/qq/QQ8.9.3/21159/QQ8.9.3.exe"

response = requests.request(method="GET", url=url, stream=True, data=None, headers=None)

save_path = r'd:/qq.exe'

total_length = int(response.headers.get("Content-Length"))
with open(save_path, 'wb') as f:
    # widgets = ['Processed: ', progressbar.Counter(), ' lines (', progressbar.Timer(), ')']
    # pbar = progressbar.ProgressBar(widgets=widgets)
    # for chunk in pbar((i for i in response.iter_content(chunk_size=1))):
    #     if chunk:
    #         f.write(chunk)
    #         f.flush()

    widgets = ['Progress: ', progressbar.Percentage(), ' ',
               progressbar.Bar(marker='#', left='[', right=']'),
               ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
    for chunk in response.iter_content(chunk_size=1):
        if chunk:
            f.write(chunk)
            f.flush()
        pbar.update(len(chunk) + 1)
    pbar.finish()