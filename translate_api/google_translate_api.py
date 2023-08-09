import requests

url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

payload = {
    "q": "שלום",
    "target": "en",
    "source": "he"
}

headers = {
    "content-type": "application/x-www-form-urlencoded",
    "Accept-Encoding": "application/gzip",
    "X-RapidAPI-Key": "2e310832a1mshc3c3095fad92cf2p13d8e8jsn272f97d004bf",  # Replace this with your actual API key
    "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
}

response = requests.post(url, data=payload, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    try:
        data = response.json()["data"]
        # source_word = data["translations"][0]["q"]
        translation = data["translations"][0]["translatedText"]
        # print("Source word:", source_word)
        print("Translation:", translation)
    except KeyError as e:
        print("Error parsing response:", e)
else:
    print("Translation failed. Status code:", response.status_code)