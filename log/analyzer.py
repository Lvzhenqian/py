import threading,os,re,datetime

o = re.compile(r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) .* \[(?P<time>.*)\] "(?P<method>\w+) (?P<url>[^\s]*) (?P<version>[\w|/\.\d]*)" (?P<status>\d{3}) (?P<length>\d+) "(?P<referer>[^\s]*)" "(?P<ua>.*)"')


def read_log(path):
    offset = 0
    event = threading.Event()
    while not event.is_set():
        with open(path) as f:
            if offset > os.stat(path).st_size:
                offset = 0
            f.seek(offset)
            yield from f
        offset = f.tell()
        event.wait(0.1)

def parse(path):

    for line in read_log(path):
        m = o.search(line.rstrip('\n'))
        if m:
            data = m.groupdict()
            data['time'] = datetime.datetime.strptime(data['time'], '%d/%b/%Y:%H:%M:%S %z')
            return data

def agg(path,interval=10):
    count = 0
    traffic = 0
    error = 0
    start = datetime.datetime.now()
    for line in parse(path):
        item = parse(line)
        count += 1
        traffic += int(item['length'])
        if int(item['status']) >= 300:
            error += 1
        currrent = datetime.datetime.now()
        if (currrent -start).total_seconds() >= interval:
            error_rate = error / count

            start = currrent
            count = 0
            traffic = 0
            error = 0

def send():
    pass
