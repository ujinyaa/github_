import random
import json
import math
from tqdm import tqdm
import os

# --- 설정 (Constants) ---
OUTPUT_JSONL = "artlang_annotated_pairs.jsonl"
TARGET_PAIRS = 4000
MIN_TOKENS = 6
MAX_TOKENS = 25

# --- 🎯 1. Zipf 분포 상수 ---
ZIPF_ALPHA = 1.07

# --- 🎯 2. 문법 규칙 상수 (Pro Final Fix) ---
PLURAL_NOUN_PROB = 0.3
# 🚨 오류 수정: PLURAL_RULES와 PLURAL_WEIGHTS 분리
PLURAL_RULES = {"regular": "-ka", "irreg1": "-po", "irreg2": "-lee"}
PLURAL_WEIGHTS = {"regular": 0.7, "irreg1": 0.15, "irreg2": 0.15}

# 형용사 1-6개 (PP로 길이 확장)
ADJ_COUNTS = [0, 1, 2, 3, 4, 5, 6]
ADJ_PROBS =  [0.10, 0.30, 0.25, 0.15, 0.10, 0.05, 0.05]

ADV_PROB = 0.6
ADJ_PLURAL_RULE = "-z"

# 전치사구(PP) 도입 (퀘냐 방법론: 격)
PREPOSITION_PROB = 0.6

# --- 어휘 정의 ---
NOUNS = {"pleck": "m", "vode": "f", "klim": "m", "zuna": "f", "brip": "m", "lorf": "f", "niff": "m", "glim": "f"}
ADJECTIVES = {"trois": {"m": "troise", "f": "troiso"}, "neim": {"m": "neime", "f": "neimo"},
              "peli": {"m": "pelie", "f": "pelio"}, "glok": {"m": "gloke", "f": "gloko"}}
ARTICLES = {"m": "li", "f": "lu"}
VERBS = ["klin", "nim", "yab", "praz", "flig", "droz"]
ADVERBS = ["noyka", "zayma", "dema", "vogo"]
PREPOSITIONS = ["er", "ko", "po", "in"]


# --- 🎯 1. Zipf 샘플러 구현 ---
class ZipfianSampler:
    def __init__(self, vocab: list, alpha: float = 1.07):
        self.vocab = vocab
        self.ranks = list(range(1, len(vocab) + 1))
        self.weights = [1 / (rank ** alpha) for rank in self.ranks]

    def sample(self) -> str:
        return random.choices(self.vocab, weights=self.weights, k=1)[0]


# --- 품사별 샘플러 초기화 ---
NOUN_SAMPLER = ZipfianSampler(list(NOUNS.keys()), ZIPF_ALPHA)
ADJ_SAMPLER = ZipfianSampler(list(ADJECTIVES.keys()), ZIPF_ALPHA)
VERB_SAMPLER = ZipfianSampler(list(VERBS), ZIPF_ALPHA)
ADV_SAMPLER = ZipfianSampler(list(ADVERBS), ZIPF_ALPHA)
PREP_SAMPLER = ZipfianSampler(PREPOSITIONS, ZIPF_ALPHA)


# --- 🎯 2 & 3. NP 생성기 (오류 수정: PLURAL_PROBS 관련) ---
def make_np():
    """
    역할: 인공어 명사구(NP) 생성 [N (Adj*1-6) Art]
    수정: PLURAL_PROBS 관련 TypeError 해결
    """
    # 1. 명사 선택 (Zipf)
    noun_base = NOUN_SAMPLER.sample()
    gender = NOUNS[noun_base]

    # 2. 복수 적용 (파라미터화)
    is_plural = random.random() < PLURAL_NOUN_PROB
    noun = noun_base
    plural_type = None
    if is_plural:
        # 🚨 오류 수정 부분: PLURAL_WEIGHTS 사용으로 변경
        plural_type = random.choices(
            list(PLURAL_WEIGHTS.keys()),
            weights=list(PLURAL_WEIGHTS.values()),
            k=1
        )[0]
        noun += PLURAL_RULES[plural_type]

    np_tokens = [noun]
    adj_stems = []

    # 3. 형용사 추가 (1-6개, 가중치 적용, 문법 일관성 수정)
    num_adjectives = random.choices(ADJ_COUNTS, weights=ADJ_PROBS, k=1)[0]

    for _ in range(num_adjectives):
        adj_stem = ADJ_SAMPLER.sample()

        # 3a. 성(Gender) 일치
        adj_token = ADJECTIVES[adj_stem][gender]

        # 3b. 수(Number) 일치
        if is_plural:
            adj_token += ADJ_PLURAL_RULE

        np_tokens.append(adj_token)
        adj_stems.append(adj_stem)

    # 4. 관사 추가 (필수)
    np_tokens.append(ARTICLES[gender])

    meta = {
        "base": noun_base,
        "gender": gender,
        "is_plural": is_plural,
        "plural_type": plural_type,
        "adj": adj_stems
    }
    return np_tokens, meta


# --- 전치사구(PP) 생성기 ---
def make_pp():
    """
    역할: 전치사구(PP) 생성 [Prep NP]
    """
    prep_token = [PREP_SAMPLER.sample()]

    np_tokens, meta_np = make_np()

    pp_tokens = prep_token + np_tokens

    meta = {"prep": prep_token[0], "np": meta_np}
    return pp_tokens, meta


# --- 문장 생성기 ( PP 추가) ---
def make_sentence_pair():
    """
    역할: SOV(ok)와 SVO(violation) 문장 쌍 생성
    수정: 40% 확률로 PP(전치사구)를 동사 앞에 추가
    """
    # 1. 주어(S), 목적어(O) 생성
    np_s_tokens, meta_s = make_np()
    while True:
        np_o_tokens, meta_o = make_np()
        if meta_s["base"] != meta_o["base"]:
            break

    # 2. 동사(V) 생성 (Zipf)
    verb_token = [VERB_SAMPLER.sample()]

    # 3. 부사(ADV) 생성
    adv_token = []
    meta_adv = None
    if random.random() < ADV_PROB:
        adv_token = [ADV_SAMPLER.sample()]
        meta_adv = adv_token[0]

    # 4. 전치사구(PP) 생성
    pp_token = []
    meta_pp = None
    if random.random() < PREPOSITION_PROB:
        pp_token, meta_pp = make_pp()

    # 5. 'ok' (SOV) 문장 생성
    # 구조: [NP_S] [NP_O] [PP] [V] [ADV] -> 최대 27토큰까지 생성 가능 (25토큰 목표 충족)
    ok_tokens = np_s_tokens + np_o_tokens + pp_token + verb_token + adv_token
    ok_text = " ".join(ok_tokens)
    ok_meta = {
        "structure": "S-O-PP-V-ADV" if pp_token and adv_token else (
            "S-O-PP-V" if pp_token else ("S-O-V-ADV" if adv_token else "S-O-V")),
        "s": meta_s, "o": meta_o, "pp": meta_pp, "adv": meta_adv
    }

    # 6. 'violation' (SVO) 문장 생성
    # 구조: [NP_S] [V] [NP_O] [PP] [ADV]
    vio_tokens = np_s_tokens + verb_token + np_o_tokens + pp_token + adv_token
    vio_text = " ".join(vio_tokens)
    vio_meta = {
        "structure": "S-V-O-PP-ADV" if pp_token and adv_token else (
            "S-V-O-PP" if pp_token else ("S-V-O-ADV" if adv_token else "S-V-O")),
        "s": meta_s, "o": meta_o, "pp": meta_pp, "adv": meta_adv
    }

    return (ok_text, ok_meta, ok_tokens), (vio_text, vio_meta, vio_tokens)


# --- 파일 로드 (get_existing_pair_count) ---
def get_existing_pair_count(filepath: str) -> int:
    if not os.path.exists(filepath):
        return 0
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            line_count = sum(1 for _ in f)
        return line_count // 2
    except Exception as e:
        print(f"Warning: Could not read existing file {filepath}. Overwriting. Error: {e}")
        return 0


# --- 메인 함수 (main) ---
def main():
    existing_pairs = get_existing_pair_count(OUTPUT_JSONL)
    pairs_to_generate = TARGET_PAIRS - existing_pairs

    if pairs_to_generate <= 0:
        print(f"Target of {TARGET_PAIRS} pairs already met or exceeded.")
        return

    print(f"Found {existing_pairs} existing pairs. Generating {pairs_to_generate} new pairs...")

    with open(OUTPUT_JSONL, "a", encoding="utf-8") as f_out:
        pbar = tqdm(desc="Generating Artificial Language (SOV) pairs", total=pairs_to_generate)

        generated_count = 0
        while generated_count < pairs_to_generate:
            (ok_text, ok_meta, ok_tokens), (vio_text, vio_meta, vio_tokens) = make_sentence_pair()

            # MAX_TOKENS=25 필터가 작동하여 23~25토큰 문장을 안정적으로 확보합니다.
            if not (MIN_TOKENS <= len(ok_tokens) <= MAX_TOKENS):
                continue

            pair_id_num = existing_pairs + generated_count + 1
            pair_id = f"art_{pair_id_num:06d}"

            ok_entry = {
                "id": f"{pair_id}_ok", "pair_id": pair_id, "text": ok_text, "label": "ok",
                "meta": {**ok_meta, "length": len(ok_tokens), "language": "artificial"}
            }
            vio_entry = {
                "id": f"{pair_id}_vi", "pair_id": pair_id, "text": vio_text, "label": "violation",
                "meta": {**vio_meta, "length": len(vio_tokens), "language": "artificial"}
            }

            f_out.write(json.dumps(ok_entry, ensure_ascii=False) + "\n")
            f_out.write(json.dumps(vio_entry, ensure_ascii=False) + "\n")
            f_out.flush()

            generated_count += 1
            pbar.update(1)

        pbar.close()

    print(f"Generation complete. Total pairs in file: {existing_pairs + generated_count}")


if __name__ == "__main__":
    main()