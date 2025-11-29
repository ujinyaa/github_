1. 텐서보드 저장은 log 파일 아래 explicit,implict 학습 별로 train,eval 결과 있습니다
2. plot_learning_curves.py 돌린 내용은 results 파일 안에 그래프에 나와있습니다
3. evaluate_methods2.py 돌린 결과 cmd 내용은 log 파일 안에 explicit,implict 학습 별로 있습니다.
evaluate_methods2.py 돌릴때 출력되는 grammer_error_detection 내용도 log 파일 안에 있습니다.
예시 문장으로는 dev_explicit의 첫번째 예시문장을 이용해서 정합, 비정합으로 조건 맞추어서 넣었습니다.
# Case A: 기본적인 SVO 어순
    good_sent = "vode pelio pelio lu blig-ka troise-z clome-z miske-z li klin"
    bad_sent = "vode pelio pelio lu klin blig-ka troise-z clome-z miske-z li"  # 규칙 위반 예시
