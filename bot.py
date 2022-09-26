import telebot
import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
bot = telebot.TeleBot('api_key')

@bot.message_handler(content_types=['photo'])
def get_image_messages(message):
    print ('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print ('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print ('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
   
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    result = recognize("image.jpg")
    print(result)

    if result:
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, "Не вижу тут цифры")

def recognize(digit_photo):
    img = cv2.imread(digit_photo)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=6)

    invert = 255 - cv2.GaussianBlur(close, (3,3), 0)
    data = pytesseract.image_to_string(invert, config='--psm 6 -c tessedit_char_whitelist=0123456789')
    return data

bot.polling(none_stop=True, interval=0)