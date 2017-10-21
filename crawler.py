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
        imgRe = re.compile('\<img src=\"(.+?)\" ?\/?\>')
        if imgRe.search(subject) != None:
            return list(map(lambda x: {'url': x, 'filename': urlparse(x).path.split('/')[-1]}, imgRe.findall(subject)))
        else:
            return []

    def pathProcessor(self, subject, videotype):
        try:
            videotype = videotype.split('/')[-1]
        except AttributeError:
            videotype = videotype[0].split('/')[-1]
        a = re.findall('(tumblr_.+)\/([\d]+)', urlparse(subject).path)
        b = re.findall('(tumblr_.+)', urlparse(subject).path)
        if len(a):
            return {
                'url': urljoin('https://vt.tumblr.com/', '.'.join(['_'.join(a[0]), videotype])) + '#_=_',
                'filename': '.'.join(['_'.join(a[0]), videotype])
            }
        else:
            return {
                'url': urljoin('https://vt.tumblr.com/', '.'.join([b[0], videotype])) + '#_=_',
                'filename': '.'.join([b[0], videotype])
            }

    def videoExtractor(self, subject):
        videoRe = re.compile('\<source src=\"(.+?)\" ?type=\"(.+?)\" ?\/?\>')
        if videoRe.search(subject) != None:
            return list(map(lambda x: self.pathProcessor(x[0], x[1]), videoRe.findall(subject)))
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
                print(downloadDict['filename'])
                return None
            except urllib.error.HTTPError as e:
                print(e, downloadDict)

        else:
            # print('%s is already exists' % downloadDict['filename'])
            pass


rsscrwr = RSSCRWLR4TMBLR()
rsscrwr.readFeed()
