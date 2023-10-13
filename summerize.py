import os
import win32com.client
import requests

def read_outlook_files(directory):
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    emails = []
    for file in os.listdir(directory):
        if file.endswith(".msg"):
            message = outlook.OpenSharedItem(os.path.join(directory, file))
            emails.append(message.Body)
    return emails

def summarize_and_categorize(emails, openai_api_key):
    summaries = []
    for email in emails:
        response = requests.post(
            "https://api.openai.com/v1/completions",
            headers={"Authorization": f"Bearer {openai_api_key}"},
            json={
                "model": "gpt-4",
                "prompt": email,
                "max_tokens": 250,
                "temperature": 0.7
            }
        )
        if response.status_code == 200:
            data = response.json()
            print(data)  # Print the entire data dictionary
            if 'choices' in data:
                summary = data['choices'][0]['text'].strip()
                summaries.append(summary)
            else:
                print("No 'choices' key in response data")
        else:
            print(f"API request failed with status code {response.status_code}")
    return summaries


directory = r"C:\Users\dean.yang\Desktop\AI CHAT DATA"
openai_api_key = "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"
emails = read_outlook_files(directory)
summaries = summarize_and_categorize(emails, openai_api_key)
print(summaries)
print("--------------------------------------------------------------------------------------------------")
