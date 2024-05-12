import time


class BandwidthMeter:
    def __init__(self):
        self.bytes_read = 0
        self.start = 0
        self.cancelled = False
        self.last_read = 0

    def write(self, data):
        self.last_read = time.time()
        bytes_written = len(data)
        self.bytes_read += bytes_written
        if not self.start:
            self.start = self.last_read
        return bytes_written

    def bandwidth(self):
        delta_secs = time.time() - self.start
        bytes_per_sec = self.bytes_read / delta_secs
        return bytes_per_sec

    def duration(self):
        return time.time() - self.start


def async_copy(
    index,
    primary_bandwidth_reader: BandwidthMeter,
    reader,
):
    bytes_written = 0
    try:
        while True:
            if primary_bandwidth_reader.cancelled:
                return {"index": index, "bytes_written": bytes_written, "err": None}
            data = reader.read(1024)
            if not data:
                break
            bytes_written += len(data)
            primary_bandwidth_reader.write(data)
    except Exception as e:
        return {"index": index, "bytes_written": bytes_written, "err": e}
    return {"index": index, "bytes_written": bytes_written, "err": None}


