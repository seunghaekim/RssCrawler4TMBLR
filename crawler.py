import feedparser, re, urllib, sys, os, json
from urllib.parse import urlparse, urljoin

class RSSCRWLR4TMBLR:
    def __init__(self):
        try:
            with open('config.json') as config_raw:
                self.config = json.load(config_raw)
                config_raw.close()
                downloadFolder = os.path.join(
                    os.path.abspath(__file__),
                    self.config['downloadFolderName'] + '/'
                )
                if not os.path.isdir(self.config['downloadFolderName']):
                    try:
                        os.makedirs(self.config['downloadFolderName'])
                    except OSError as e:
                        print(e)
                self.config['downloadPath'] = downloadFolder

        except FileNotFoundError as e:
            with open('config.json', 'w') as write_config:
                default_config = {
                    'rssList': [
                        'https://tragedygirlsmovie.tumblr.com/'
                    ],
                    'downloadFolderName': 'tmblr'
                }
                write_config.write(json.dumps(default_config))
                write_config.close()
                print('file wirte done, restart this program')
        except:
            return None

    def readFeed(self):
        for rss in self.config['rssList']:
            feed = feedparser.parse(rss)
            if len(feed) < 0:
                print('there is no content to download on %s' % rss)
                continue
            else:
                print('download start from %s, count: %d' % (rss, len(feed)))
                entries = feed['entries']
                for entry in entries:
                    downloadset = []
                    downloadset.extend(self.imageExtractor(entry['summary_detail']['value']))
                    downloadset.extend(self.videoExtractor(entry['summary_detail']['value']))
                    for download in downloadset:
                        self.downloader(download)

    def imageExtractor(self, subject):
        imgRe = re.compile('\<img src=\"(.+?)\"\/?\>')
        if imgRe.search(subject) != None:
            return list(map(lambda x: {'url': x, 'filename': urlparse(x).path.split('/')[-1]}, imgRe.findall(subject)))
        else:
            return []

    def videoExtractor(self, subject):
        # \<source src=\"(.+?)\" ?type=\"(.+?)\"\>
        videoRe = re.compile('\<source src=\"(.+?)\" ?type=\"(.+?)\"\>')
        if videoRe.search(subject) != None:
            path = lambda x: urlparse(x).path.split('/')[-1]
            ext = lambda x: x.split('/')[-1]
            url = lambda x: urljoin('https://vt.tumblr.com/', x)
            filename = lambda path, ext: '.'.join([path, ext])

            return list( map( lambda x: { 'url': url(x), 'filename': filename(path(x[0]), ext(x[1])) }, videoRe.findall(subject) ) )
            # videoPrefix = "https://vt.tumblr.com/"
            # videoBody = videoRe.search(subject).group(5)
            # try:
            #     videoBodySurFix = "_" + videoRe.search(subject).group(7)
            # except TypeError:
            #     videoBodySurFix = ""
            # videoType = "." + videoRe.search(subject).group(9)
            # videoSurFix = "#_=_"
            # videoUrl = videoPrefix + videoBody + videoBodySurFix + videoType + videoSurFix
            # videoFile = videoBody + videoType
            # return {
            #     'url': videoUrl,
            #     'filename': videoFile
            # }
        else:
            return []

    def downloader(self, downloadDict):
        if downloadDict is False:
            return None

        afile = os.path.join(self.config['downloadFolderName'], downloadDict['filename']);
        if os.path.isfile(afile) is False:
            try:
                urllib.request.urlretrieve(downloadDict['url'], afile)
                print('%s download successed' % downloadDict['filename'])
            except OSError as e:
                print(e)
                return None
            except UnicodeEncodeError as e:
                # print(e)
                print(downloadDict['filename'])
                return None
        else:
            print('%s is already exists' % downloadDict['filename'])


rsscrwr = RSSCRWLR4TMBLR()
# test = '<img src="https://78.media.tumblr.com/a90ecb4f7417a844564d4d125361f9f1/tumblr_os38kp6Q1V1w69jrdo1_500.jpg"/><br/> <br/><img src="https://78.media.tumblr.com/a14f51850cccf3f49495a30871dada25/tumblr_os38kp6Q1V1w69jrdo2_500.jpg"/><br/> <br/><img src="https://78.media.tumblr.com/aa688d83172db1a3c02484cb6c2e8e0c/tumblr_os38kp6Q1V1w69jrdo3_500.jpg"/><br/> <br/><img src="https://78.media.tumblr.com/c58c11a9f5d92ba5e359dd1e0aa7b52c/tumblr_os38kp6Q1V1w69jrdo4_500.jpg"/><br/> <br/><img src="https://78.media.tumblr.com/a9e795b1f0338ff436d4f5ad9e5b9b35/tumblr_os38kp6Q1V1w69jrdo5_500.jpg"/><br/> <br/><img src="https://78.media.tumblr.com/4f6a0b1228ff9e58f1de46afc9657a87/tumblr_os38kp6Q1V1w69jrdo6_500.jpg"/><br/> <br/><img src="https://78.media.tumblr.com/18e043edb619583347ee384592b233e6/tumblr_os38kp6Q1V1w69jrdo7_500.jpg"/><br/> <br/><p>大吊的援交JK少女<br/>'
rsscrwr.readFeed()
