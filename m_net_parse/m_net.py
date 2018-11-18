import urllib
from urllib.parse import quote
from urllib.request import urlopen
import json
import codecs


# searchName = "바나나 알러지 원숭이"


#
# m_net_parse(input())
class Mnet:
    mTitle = ""
    mArtist = ""
    mAlbum = ""
    mYear = ""
    # mTrack = ""
    mGenre = ""
    mComment = ""
    mImagePath = ""
    mLyric = ""

    # 초기자(initializer)

    def __init__(self, search_name):
        # self.* : 인스턴스변수

        self.m_net(search_name)

    # 메서드
    def m_net(self, search_name):
        url = 'http://search.api.mnet.com/search/totalweb?q=' + quote(search_name) + '&sort=r'

        req = urllib.request.Request(url)

        r = urllib.request.urlopen(req).read()
        reader = codecs.getreader("utf-8")

        cont = json.loads(r.decode('utf-8'))
        if cont["resultCode"] == "S0000":
            if cont["info"]["songcnt"] != 0:
                self.mTitle = cont["data"]["songlist"][0]["songnm"]
                self.mAlbum = cont["data"]["songlist"][0]["albumnm"]
                self.mArtist = cont["data"]["songlist"][0]["ARTIST_NMS"]
                self.mGenre = cont["data"]["songlist"][0]["genrenm"]
                self.mYear = cont["data"]["songlist"][0]["releaseymd"]
                if len(cont["data"]["lyriclist"]) != 0:
                    self.mLyric = cont["data"]["lyriclist"][0]["lyrics"]
                album_id = cont["data"]["songlist"][0]["albumid"]
                if len(album_id) == 7:
                    image_path = "http://cmsimg.mnet.com/clipimage/album/480/00" + album_id[0] + "/" + (
                        album_id[1:4]) + "/" + album_id + ".jpg"
                else:
                    image_path = "http://cmsimg.mnet.com/clipimage/album/480/000/" + (
                        album_id[0:3]) + "/" + album_id + ".jpg"
                self.mImagePath = image_path
            else:
                if cont["info"]["tvcnt"] != 0:
                    self.m_net(cont["data"]["tvlist"][0]["mvtitle"])
                else:
                    self.mComment = "검색 결과가 없습니다."
        else:
            self.mComment = "실패 했습니다."
