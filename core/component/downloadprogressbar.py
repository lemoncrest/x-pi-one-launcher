import pygame
try:
    from urllib2 import urlopen # Python2
except ImportError:
    from urllib.request import urlopen # Python3
    pass
from core.component.progressbar import ProgressBar
from core.constants import WINDOW_SIZE


class DownloadProgressBar():

    def __init__(self,surface):
        self.surface = surface

    def init(self):
        self.lastFramed = 0.0
        margin = 50
        self.progressbar = ProgressBar(width=WINDOW_SIZE[0] - margin, height=30, surface=self.surface, x=0, y=50,
                                       margin=margin, centeredText=True)

    def downloadProgressBar(self, remote):
        self.init() #TODO check this one
        response = urlopen(remote)
        self.progressbar.updateProgressBar()  # first frame
        pygame.display.flip()
        self.lastFramed = 0
        content = self.chunk_read(response, report_hook=self.chunk_report)
        self.progressbar.updateProgressBar()  # last frame
        pygame.display.flip()
        return content

    def chunk_report(self, bytes_so_far, chunk_size, total_size):
        percent = float(bytes_so_far) / total_size
        progress = round(percent * 100, 2)
        # print("Downloaded %d of %d bytes (%0.2f%%)" % (bytes_so_far, total_size, progress))
        # print(str(progress/100))
        if float(self.lastFramed + 0.0015) < progress / 100 or progress >= 100:
            self.lastFramed = self.progressbar.progress
            self.progressbar.updateProgressBar()
            pygame.display.flip()
        # less frames, better times, it's not necessary refresh all time, CPU is gold for interpreter
        self.progressbar.progress = progress / 100

    def chunk_read(self, response, chunk_size=8192, report_hook=None):
        try:
            total_size = response.info().getheader('Content-Length').strip()
        except:
            total_size = response.headers['Content-Length']
            pass
        total_size = int(total_size)
        bytes_so_far = 0
        total = bytearray()
        while 1:
            chunk = response.read(chunk_size)

            total += chunk

            bytes_so_far += len(chunk)

            if not chunk:
                break

            if report_hook:
                report_hook(bytes_so_far, chunk_size, total_size)

        return total.decode("utf-8")  # bytes_so_far
