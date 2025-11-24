모델 파트는 명시적 학습(Explicit) 과 암시적 학습(Implicit) 조건에서
GPT 기반 언어모델이 문법 규칙을 어떻게 내재화하고 일반화하는지를 비교하기 위해 수행되었다.
실험은 E1 (Fine-tuning Efficiency) 와 E2 (Grammaticality Judgment) 두 단계로 구성된다.

1. 데이터 나누기 
   ## 데이터 경로 : C:\Users\User\PycharmProjects\CUK_NL_team3\data\split_data
   ## 원본 데이터 : train_aria_explicit.jsonl, train_aria_implicit.jsonl
   두 파일을 각각 train : valid : test = 8 : 1 : 1 비율로 분할하여 저장하였다.

2. E1 실험 - Fine-Tuning & PPL 
   ## 사용 데이터셋
   - Explicit (명시적 학습) : train_explicit.jsonl, val_explicit.jsonl
   → 프롬프트 구성:
      [RULES] (EXPLICIT_RULE_CARD_A/B/C 중 선택. SOV 규칙 등 명시)
      [EXAMPLE] (정답/오답 예시)
      [INPUT] (실제 인공어 문장)
   - Implicit (암시적 학습) : train_implicit.jsonl, val_implicit.jsonl
   → 프롬프트 구성:
      [EXAMPLE] (예시만 제공)
      [INPUT] (실제 인공어 문장, 규칙 카드 생략)
   - 학습 경로 : C:\Users\User\PycharmProjects\CUK_NL_team3\scripts\train.py
   ## 실험 목적
   - 동일한 GPT-2 아키텍처에서 explicit/implicit 조건별로 각각 fine-tuning을 수행한다.
   - 두 조건 간 PPL(perplexity) 하락 속도와 수렴 패턴을 비교한다.
   ## 결과 확인
   - 학습 로그 및 곡선은 TensorBoard에서 시각화한다. 
   - 결과 그래프 저장 경로: C:\Users\User\PycharmProjects\CUK_NL_team3\E1_aria_test2

   ## 일차적 파인튜닝 내용 요약
   - train에 대해 explicit, implicit 학습 모두 lr과 loss가 줄어드는 것을 텐서보드로 확인할 수 있다.

3. E2 실험
   ## 사용 데이터셋
   - Explicit (명시적 학습) : test_aral.jsonl
   - Implicit (암시적 학습) : test_aral.jsonl
   - 실행 경로 : C:\Users\User\PycharmProjects\CUK_NL_team3\scripts\eval.py
   ## 실험 목적 
   - 명시적/암시적 조건에서 학습한 모델의 일반화 성능·문법 판별 능력을 정확도, PLL GAP, ECE 지표로 평가한다.
   - 두 조건의 결과를 정량적으로 비교해, 규칙 제시 유무가 모델의 문법 판단 및 신뢰 calibration에 미치는 영향을 분석한다
   - "text" 가 있으면 그 문자열을 반환, 없으면 "sentence" 있으면 반환, 둘다 없으면 빈 문자열 반환 
   ## 1. PPL ACCURACY : 전체 쌍 중 정답 비율을 Accuracy (ACC) 로 계산한다.
   - 실험 결과
      explicit : 0.935223
      implicit : 0.940621 
   - 분석 
     1. 두 모델 모두 93% 이상의 높은 정확도를 보인다. 
     2. 암시적 학습이 명시적 학습에 비해 정확도가 근소하게 더 높으나, 통계적으로는 큰 차이가 없다.
     3. 명시적 규칙을 제시하지 않아도 충분한 generalized 문법 추론 성능을 보인다. 

   ## 2. MEAN_PPL_GAP : 모델이 정상 문장과 위반 문장 사이 확신(PLL log likelihood)의 평균 차이
   - 실험 결과
      explicit : 0.857383 
      implicit : 0.990131 
   - 분석 
     1. 암시적 모델의 평균 gap이 더 크며, 실제로 위반/정상 구분의 확신이 더 강함. 
     2. 암시적 조건에서도 반복 학습을 통해 패턴/위반 감지가 잘 학습됨을 확인할 수 있음.
     3. gap 값은 문법 추론의 신뢰도 역할
   
   ## 3. ECE : 모델의 예측 확신과 실제 정답 일치율 차이(=칼리브레이션 오류
   - 실험 결과
      explicit : 0.235325
      implicit : 0.220281
   - 분석 
     1. 두 조건 모두 낮은 ECE(0.2대)로, 예측 확신이 실제 결과와 잘 맞음(잘 칼리브레이션됨).
     2. 암시적 모델이 오히려 ECE가 조금 더 낮아 예측 신뢰와 실제 정답 일치가 더 좋게 조정됨.
     3. 이는 암시적/명시적 모두 실험 환경에서 신뢰 calibration이 효과적임을 시사.

## 최종 결과 
eval 완료된 implicit, explicit 에 대한 텐서보드를 확인해보면 loss가 제각각인걸 확인할 수 있다. 
이런 현상은 test_aral.jsonl이 train 데이터셋이랑 달라서 발생한 현상이거나 혹은 조건으로 문장을 쪼개서 분석하는데 있어서 차이가 존재해서 나는 문제들이다.

