import feedparser, re, urllib, sys, os, json

class RSSCRWLR4TMBLR:
    def __init__(self):
        try:
            with open('config.json') as config_raw:
                self.config = json.load(config_raw)
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
        except:
            return None

    def readFeed(self):
        for rss in self.config['rssList']:
            feed = feedparser.parse(rss)
            entries = feed['entries']
            for entry in entries:
                self.downloader(
                    self.imageExtractor(entry['summary_detail']['value'])
                )
                self.downloader(
                    self.videoExtractor(entry['summary_detail']['value'])
                )

    def imageExtractor(self, subject):
        imgRe = re.compile(r"(\<img src=\")(\S+(\/(\S+\.(jpg|gif|png))))(\"\/\>)")
        if imgRe.search(subject) != None:
            return {
                'url': imgRe.search(subject).group(2),
                'filename': imgRe.search(subject).group(4)
                }
        else:
            return False

    def videoExtractor(self, subject):
        videoRe = re.compile(r"(\<source src\=\")((https?\:\/+([a-z0-9\.\_]+\/)+)(tumblr_[\S]{17})(\/?([0-9]{3})?))(\" type\=\"video\/(\S{3,4})\"\>)")
        if videoRe.search(subject) != None:
            videoPrefix = "https://vt.tumblr.com/"
            videoBody = videoRe.search(subject).group(5)
            try:
                videoBodySurFix = "_" + videoRe.search(subject).group(7)
            except TypeError:
                videoBodySurFix = ""
            videoType = "." + videoRe.search(subject).group(9)
            videoSurFix = "#_=_"
            videoUrl = videoPrefix + videoBody + videoBodySurFix + videoType + videoSurFix
            videoFile = videoBody + videoType
            return {
                'url': videoUrl,
                'filename': videoFile
            }
        else:
            return False

    def downloader(self, downloadDict):
        if downloadDict is False:
            return None

        afile = os.path.join(self.config['downloadFolderName'], downloadDict['filename']);
        if os.path.isfile(afile) is False:
            try:
                urllib.request.urlretrieve(downloadDict['url'], afile)
            except OSError as e:
                print(e)
                return None
        else:
            print('%s is already exists' % downloadDict['filename'])


rsscrwr = RSSCRWLR4TMBLR()
rsscrwr.readFeed();
