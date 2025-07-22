from flask import Flask, render_template
import webbrowser
import os

app = Flask(__name__)

@app.route('/')
def home():

    return render_template('은평구자체_지도.html')

if __name__ == '__main__':
    # 브라우저 자동 실행 (선택)
    webbrowser.open("http://127.0.0.1:5001")
    
    # 서버 실행
    app.run(debug=True, port=5001)
