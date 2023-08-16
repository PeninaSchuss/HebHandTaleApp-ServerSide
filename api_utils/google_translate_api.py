import requests

url = "https://google-translate1.p.rapidapi.com/language/translate/v2"


def translate_word(word_to_translate, target_language):
    payload = {
        "q": word_to_translate,
        "target": target_language,
        "source": "he"
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "cb66237962msh072cf932d6327eep1b0f92jsnc07647de39d9",  # Replace this with your actual API key
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers, verify=False)

    # Check if the request was successful
    if response.status_code == 200:
        try:
            data = response.json()["data"]
            # source_word = data["translations"][0]["q"]
            translation = data["translations"][0]["translatedText"]
            # print("Source word:", source_word)
            print("Translation:", translation)
            return data["translations"][0]["translatedText"]
        except KeyError as e:
            print("Error parsing response:", e)
    else:
        print("Translation failed. Status code:", response.status_code)

    return response
