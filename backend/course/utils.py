import openai

openai.api_key = "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"


def chat_with_gpt3(messages):
    print("gpt called", messages)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 使用 GPT-3.5 Turbo，或其他适当的模型
        messages=messages
    )
    content = response.choices[0].message['content']
    print("gpt response", content)
    return content


# 场景1: 回答论坛问题
def answer_forum_question(question):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": question}
    ]
    return chat_with_gpt3(messages)


def generate_study_plan(course_name_list):
    course_name_list = ','.join(course_name_list)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user",
         "content": f"""Given the courses {course_name_list}, briefly list a study plan and some recommended courses in bullet points. Limit to 5 points for each."""}
    ]
    return chat_with_gpt3(messages)
