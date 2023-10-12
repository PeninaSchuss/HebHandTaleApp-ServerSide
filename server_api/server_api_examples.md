#### Examples of calling the functions found in the server_api.py file using Windows power shell (but can also be done in other ways too - through chrome, postman, etc.):
1) Calling the recognize_word_by_content route:
   1) open a new Windows PowerShell.
   2) run the following commands:
   ```$imagePath = "path to the image"```
    ```imageContent = [System.IO.File]::ReadAllBytes($imagePath)```
    ```$base64Image = [System.Convert]::ToBase64String($imageContent)```
    ```$headers = @{"Content-Type" = "application/octet-stream"}```
    ```$url = "http://localhost:5000/recognize_word_by_content"```
    ```$body = [System.Text.Encoding]::UTF8.GetBytes($base64Image)```
    ```response = Invoke-RestMethod -Method Post -Uri $url -Headers $headers -Body $body```
    ```$response```
   The output received is the identified word from the image, followed by 10 words similar to it.
2) Calling the translate_word_with_google_api route:
   1) open a new Windows PowerShell.
   2) run the following command:
   ```curl "http://127.0.0.1:5000/translate_word_with_google_api/מילה/en/English"```  (replace the word "מילה" with the Hebrew word you want to translate)
   3) The output received is a path of an audio file of the translation of the word, and the translation word.