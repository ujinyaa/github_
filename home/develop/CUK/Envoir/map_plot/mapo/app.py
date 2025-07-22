from flask import Flask, render_template
import webbrowser
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Flask는 templates 폴더에서 HTML 파일을 찾습니다
    return render_template('mapo_cctv_location_map.html')

if __name__ == '__main__':
    # 브라우저 자동 실행
    webbrowser.open("http://127.0.0.1:5002")
    
    # 서버 실행 (5002 포트에서 실행)
    app.run(debug=True, port=5002)
