from flask import Flask, request, jsonify
from time import sleep
import telepot
from alsong_parse import alsong
from m_net_parse.m_net import Mnet


app = Flask(__name__)


@app.route('/keyboard')
def Keyboard():
    dataSend = {
        "type": "buttons",
        "buttons": ["시작하기", "도움말"]
    }

    return jsonify(dataSend)


@app.route('/message', methods=['POST'])
def Message():
    dataReceive = request.get_json()
    content = dataReceive['content']

    if content == u"시작하기":
        dataSend = {
            "message": {
                "text": "노래 검색을 자유롭게 해주세요"
            }
        }
    elif content == u"도움말":
        dataSend = {
            "message": {
                "text": "노래 검색을 자유롭게 해주세요"
            }
        }

    else:
        var = Mnet(content)
        if var.mComment == "":
            alsong_lyric = alsong.parse(var.mTitle, var.mArtist)
            dataSend = {

                "message": {
                    "text": "제목 : " + var.mTitle + "\n가수 : " + var.mArtist + "\n앨범 : " + var.mAlbum + "\n가사\n" + alsong_lyric,
                    "photo": {
                        "url": var.mImagePath,
                        "width": 400,
                        "height": 400
                    }
                }
            }
        else:
            if var.mTitle == "":
                dataSend = {

                    "message": {
                        "text": "검색 결과가 없습니다."

                    }
                }
            else:
                dataSend = {

                    "message": {
                        "text": "제목 : " + var.mTitle + "\n가수 : " + var.mArtist + "\n앨범 : " + var.mAlbum + "\n가사\n" + var.mLyric,
                        "photo": {
                            "url": var.mImagePath,
                            "width": 400,
                            "height": 400
                        }
                    }
                }

    return jsonify(dataSend)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
