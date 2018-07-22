# 批量抓取期末成绩
# question:
# 1.成功绕过验证码，进入个人主页，但如何保持登录状态，进一步获取成绩出现问题。待后续完善
# 2.下一步目标是获取期末成绩


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from PIL import Image
import tesserocr

# 使用Chrom的 headless 模式
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# browser = webdriver.Chrome(chrome_options=chrome_options)

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)
browser.set_window_size(1200, 800)

image_file = 'screenshot.png'


def get_code(image_file):
    image = Image.open(image_file)
    image = image.crop((1734, 540, 1846, 573))
    image.save('code.png')
    code_image = Image.open('code.png')
    code_image = code_image.convert('L')
    result = tesserocr.image_to_text(code_image).strip()  # 除去返回文本中的\n
    return result


def sign_in_home():
    url = 'http://yjsgl.ccu.edu.cn/education/index.aspx'
    browser.get(url)
    # 获取截图
    browser.get_screenshot_as_file(image_file)
    result_code = get_code(image_file)

    input_username = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#UserNameTextBox'))
    )
    input_passward = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#PwdText'))
    )
    input_code = wait.until(
        EC.presence_of_element_located((By.ID, 'ValidateTextBox'))
    )
    submit_sign_in = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#LoginImage'))
    )
    input_username.send_keys('Z170448')
    input_passward.send_keys('000000')
    input_code.send_keys(result_code)
    submit_sign_in.click()
    try:
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#MessageDIV > font'), '验证码错误')
        )
        sign_in_home()
    except TimeoutException:
        cookies = browser.get_cookies()
        print(cookies)
# 存在问题
def get_score(cookies):
    url = 'http://yjsgl.ccu.edu.cn/education/index.aspx'
    browser.add_cookie(cookie_dict=cookies)
    browser.get(url)


def main():
    sign_in_home()


if __name__ == '__main__':
    main()
