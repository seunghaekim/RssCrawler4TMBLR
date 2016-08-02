import feedparser, re, urllib, sys, os

# finding images and videos from img tag
imgRe = re.compile(r"(\<img src=\")(\S+(\/(\S+\.(jpg|gif|png))))(\"\/\>)")
videoRe = re.compile(r"(\<source src\=\")((https?\:\/+([a-z0-9\.\_]+\/)+)(tumblr_[\S]{17})(\/?([0-9]{3})?))(\" type\=\"video\/(\S{3,4})\"\>)")
def downloader(url, fileName):
    downloadFolder = 'e:\\Users\\joeaney\\Pictures\\tumblr\\'
    fileName = downloadFolder + fileName
    urllib.request.urlretrieve(url, fileName)

def tmbrVideoAddress(source, option):
    vre = re.compile(r"(\<source src\=\")((https?\:\/+([a-z0-9\.\_]+\/)+)(tumblr_[\S]{17})(\/?([0-9]{3})?))(\" type\=\"video\/(\S{3,4})\"\>)")
    vdPrefix = "https://vt.tumblr.com/"
    vdBody = vre.search(source).group(5)
    try:
        vdBodySurFix = "_" + vre.search(source).group(7)
    except TypeError:
        vdBodySurFix = ""
    vdType = "." + vre.search(source).group(9)
    vdSurFix = "#_=_"
    videoUrl = vdPrefix + vdBody + vdBodySurFix + vdType + vdSurFix
    videoFile = vdBody + vdType
    if option == "url":
        return(videoUrl)
    elif option == "file":
        return(videoFile)

with open("feedList.txt", "r") as f:
    feeds = f.readlines()

downloadedCount = 0
passedCount = 0
for line in feeds:
    line = line.strip()
    d = feedparser.parse(line + 'rss')
    dEntry = d['entries']
    print(line)
    for entry in dEntry:
        try:
            descript = entry['summary_detail']['value']
            # finding images from img tag
            if imgRe.search(descript) != None:
                # continue
                url = imgRe.search(descript).group(2)
                files = imgRe.search(descript).group(4)
                print(files)
                try:
                    downloader(url, files)
                    downloadedCount = downloadedCount + 1
                except OSError:
                    print(url)
                    continue
            elif videoRe.search(descript) != None:
                url = tmbrVideoAddress(descript, 'url')
                files = tmbrVideoAddress(descript, 'file')
                print(files)
                try:
                    downloader(url, files)
                except urllib.error.HTTPError:
                    print(url)
                    continue
            else:
                passedCount = passedCount + 1
        except KeyError:
            pass

print("downloaded: %s   passed: %s" % (downloadedCount, passedCount))
