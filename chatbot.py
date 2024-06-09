import pandas as pd


def levenshtein_distance(s1, s2):
    # s1이 s2보다 짧으면 s1과 s2의 위치를 바꾸고 함수를 다시 호출
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # s2가 비어있다면, s1의 길이를 반환
    if len(s2) == 0:
        return len(s1)

    # s2의 길이에 1을 더한 만큼의 초기 거리 배열 생성, 이 배열은 s2의 각 문자에 대한 거리 저장
    distances = range(len(s2) + 1)

    for i, c1 in enumerate(s1):
        # 새로운 행을 시작할 때 첫 번째 원소는 i + 1로 설정, 이는 s1의 i번째 문자까지 고려한 거리
        current_row = [i + 1]

        for j, c2 in enumerate(s2):
            # 삽입, 삭제, 치환 비용 계산
            insertions = distances[j + 1] + 1  # s2에 새 문자 삽입
            deletions = current_row[j] + 1  # s1에서 문자 삭제
            substitutions = distances[j] + (c1 != c2)  # s1의 문자를 s2의 문자로 치환

            # 계산된 비용 중 최소값을 현재 행에 추가
            current_row.append(min(insertions, deletions, substitutions))

        # 완성된 현재 행을 거리 배열로 업데이트, 다음 문자 비교를 위한 준비
        distances = current_row

    # 모든 계산을 마친 후 마지막 원소가 s1과 s2의 최종 레벤슈타인 거리
    return distances[-1]


class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data["Q"].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data["A"].tolist()  # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def find_best_answer(self, input_sentence):
        # 최소 거리를 무한대로 초기화
        min_distance = float("inf")
        # 가장 적합한 질문의 인덱스를 저장할 변수 초기화
        best_match_index = 0

        # 모든 질문에 대해 반복
        for i, question in enumerate(self.questions):
            # 입력된 문장과 각 질문 사이의 레벤슈타인 거리 계산
            distance = levenshtein_distance(input_sentence, question)

            # 현재 거리가 이전 최소 거리보다 작으면 업데이트
            if distance < min_distance:
                min_distance = distance
                best_match_index = i

        # 가장 거리가 짧은 질문에 해당하는 답변 반환
        return self.answers[best_match_index]


# CSV 파일 경로를 지정하세요.
filepath = "C:/Users/sangs/Desktop/24.06.09 final/chatbot/ChatbotData.csv"

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input("You: ")
    if input_sentence.lower() == "종료":
        break
    response = chatbot.find_best_answer(input_sentence)
    print("Chatbot:", response)