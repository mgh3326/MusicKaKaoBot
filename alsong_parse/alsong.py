import html

import requests


def get_tag(xml, tag_start, tag_end):
    start = xml.find(tag_start)
    end = xml.find(tag_end)
    if start == -1 or end == -1:
        return [-1, -1]  # error
    return xml[start + len(tag_start):end], end + len(tag_end)


def get_song_blocks(xml):
    signature = "strLyric"

    start = "<" + signature + ">"
    end = "</" + signature + ">"
    tag, idx = get_tag(xml, start, end)
    return tag


def parse(title, artist):
    #
    # title = "트와이스"
    # artist = "Heart shaker"
    url = "http://lyrics.alsong.co.kr/alsongwebservice/service1.asmx"
    xml = '<?xml version="1.0" encoding="UTF-8"?><SOAP-ENV:Envelope ' \
          'xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" ' \
          'xmlns:SOAP-ENC="http://www.w3.org/2003/05/soap-encoding" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ' \
          'xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:ns2="ALSongWebServer/Service1Soap" ' \
          'xmlns:ns1="ALSongWebServer" xmlns:ns3="ALSongWebServer/Service1Soap12"><SOAP-ENV:Body><ns1:GetResembleLyric2' \
          '><ns1:stQuery><ns1:strTitle>' + title + "</ns1:strTitle><ns1:strArtistName>" + artist + \
          "</ns1:strArtistName><ns1:nCurPage>0</ns1:nCurPage></ns1:stQuery></ns1:GetResembleLyric2></SOAP-ENV:Body></SOAP" \
          "-ENV:Envelope>"
    sess = requests.Session()
    sess.headers.update({"Content-Type": "text/xml;charset=utf-8"})

    tag_blocks = get_song_blocks(html.unescape(sess.post(url, data=xml.encode("utf-8")).text))

    tag_blocks = tag_blocks.replace('<br>', '\n')
    return tag_blocks
