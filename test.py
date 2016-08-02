import feedparser, re, urllib, sys, os

# finding images and videos from img tag
imgRe = re.compile(r"(\<img src=\")(\S+(\/(\S+\.(jpg|gif|png))))(\"\/\>)")
videoRe = re.compile(r"(\<source src\=\")((http?s\:\/+([a-z0-9\.\_]+\/)+)(tumblr_[\S]{17})(\/?([0-9]{3})?))(\" type\=\"video\/(\S{3,4})\"\>)")

def downloader(url, fileName):
    downloadFolder = 'e:\\Users\\joeaney\\Pictures\\tumblr\\'
    fileName = downloadFolder + fileName
    urllib.request.urlretrieve(url, fileName)

feedsA = """
<video id='embed-579d5af8ca87b150489018' class='crt-video crt-skin-default' width='400' height='225' poster='http://media.tumblr.com/tumblr_o6er3aL42r1uhimfv_frame1.jpg' preload='none' muted data-crt-video data-crt-options='{"autoheight":null,"duration":206,"hdUrl":"http:\/\/mmmmmancunts.tumblr.com\/video_file\/148073895158\/tumblr_o6er3aL42r1uhimfv","filmstrip":{"url":"http:\/\/38.media.tumblr.com\/previews\/tumblr_o6er3aL42r1uhimfv_filmstrip.jpg","width":"200","height":"112"}}' > <source src="http://mmmmmancunts.tumblr.com/video_file/148073895158/tumblr_o6er3aL42r1uhimfv/480" type="video/mp4"> </video> <br/><br/>
"""

feedsB = """
<video id='embed-579d52d4cc15a919466611' class='crt-video crt-skin-default' width='400' height='210' poster='https://31.media.tumblr.com/tumblr_o5eonb4ngS1tg2m6x_frame1.jpg' preload='none' muted data-crt-video data-crt-options='{"autoheight":null,"duration":152,"hdUrl":false,"filmstrip":{"url":"https:\/\/38.media.tumblr.com\/previews\/tumblr_o5eonb4ngS1tg2m6x_filmstrip.jpg","width":"200","height":"105"}}' > <source src="https://mygirllovesperm.tumblr.com/video_file/147870624850/tumblr_o5eonb4ngS1tg2m6x" type="video/mp4"> </video> <br/><br/><p>Source: mygirllovesperm.tumblr.com</p>
"""

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

vdFile = tmbrVideoAddress(feedsA, "file")
vdUrl = tmbrVideoAddress(feedsA, "url")
print(vdFile, vdUrl)
downloadedCount = 0
passedCount = 0
