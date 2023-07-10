import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import valid_email, valid_password, valid_phone, valid_login


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    pytest.driver.get('https://b2c.passport.rt.ru')
    element = WebDriverWait(pytest.driver, 10).until(
       EC.visibility_of_element_located((By.XPATH, '//*[@id="page-right"]/div/div/div/form'))
    )



# test RS-1
# Авторизация на сайте Ростелеком по номеру телефона
def test_avtorization_phone():
   pytest.driver.find_element("id", 't-btn-tab-phone').click()

   pytest.driver.find_element("id", 'username').send_keys(valid_phone)
   pytest.driver.find_element("id", 'password').send_keys(valid_password)
   pytest.driver.find_element("id", 'kc-login').click()

   # Проверяем, что мы оказались на странице личного кабинета пользователя
   assert pytest.driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div[2]/div[1]/div[1]/div[1]')

   pytest.driver.quit()



# test RS-2
# Авторизация на сайте Ростелеком по электронной почте
def test_avtorization_email():
   pytest.driver.find_element("id", 't-btn-tab-mail').click()

   pytest.driver.find_element("id", 'username').send_keys(valid_email)
   passvord = pytest.driver.find_element("id", 'password').send_keys(valid_password)
   pytest.driver.find_element("id", 'kc-login').click()

   # Проверяем, что мы оказались на странице личного кабинета пользователя
   assert pytest.driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div[2]/div[1]/div[1]/div[1]')

   pytest.driver.quit()




# test RS-3
# Регистрация нового пользователя на сайте Ростелеком
def test_registration_rostelekom():
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys('Татьяна')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys('Горохова')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys('Москва')
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').send_keys('iamspy36.6@gmail.com')
   pytest.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('010203Gtb!')
   pytest.driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('010203Gtb!')

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button').click()

   # Проверяем, что мы оказались на странице для ввода кода подтверждения
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div/div')

   pytest.driver.quit()




# test RS-4
# Перемещение курсора, а значит и ввод символов в поля ввода кода подтверждения телефона возможен только по порядку от 1 до 6
def test_registration_code_active():
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys('Таня')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys('Мороз')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys('Москва')
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').send_keys('79182270044')
   pytest.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('010203Gtb')
   pytest.driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('010203Gtb')

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button').click()

   pytest.driver.find_element("id", 'rt-code-0').click()
   # Проверяем, что курсор установлен в первое окно ввода кода
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div/div/div/div[1]/div').get_attribute(
       'class') == 'rt-input rt-input--rounded rt-input--purple rt-input--active'

   pytest.driver.find_element("id", 'rt-code-1').click()
   # Проверяем, что курсор НЕ установливается во второе окно ввода кода, без ввода значения в первое
   assert pytest.driver.find_element(By.XPATH,'//*[@id="page-right"]/div/div/div/form/div/div/div/div[1]/div').get_attribute(
       'class') == 'rt-input rt-input--rounded rt-input--purple rt-input--active'
   assert pytest.driver.find_element(By.XPATH,'//*[@id="page-right"]/div/div/div/form/div/div/div/div[2]/div').get_attribute(
       'class') == 'rt-input rt-input--rounded rt-input--purple'

   pytest.driver.find_element("id", 'rt-code-0').send_keys('1')
   # Проверяем, что после ввода символа в первое окно, курсор переместился во второе окно ввода кода
   assert pytest.driver.find_element(By.XPATH,'//*[@id="page-right"]/div/div/div/form/div/div/div/div[1]/div').get_attribute(
       'class') == 'rt-input rt-input--rounded rt-input--purple'
   assert pytest.driver.find_element(By.XPATH,'//*[@id="page-right"]/div/div/div/form/div/div/div/div[2]/div').get_attribute(
       'class') == 'rt-input rt-input--rounded rt-input--purple rt-input--active'

   pytest.driver.quit()




# test RS-5
# Заполнение поля авторизации "Мобильный телефон"  символами латиницей, кирилицей, спец символами, знаками препинания
@pytest.mark.parametrize("phone_number",['asdfghjk','фырвллдг','#$%^&*','.,:?!'])
def test_avtorization_invalid_phone(phone_number):
   pytest.driver.find_element("id", 't-btn-tab-phone').click()

   pytest.driver.find_element("id", 'password').send_keys(valid_password)
   pytest.driver.find_element("id", 'username').send_keys(phone_number)

   pytest.driver.find_element("id", 'kc-login').click()

   # Проверяем, что мы остались на странице регистрации и не вошли в личный кабинет
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form')

   pytest.driver.quit()



# test RS-6
# Авторизация на сайте Ростелеком с невалидными значениями номера телефона - пустое значение, строка минимальной длины
@pytest.mark.parametrize("phone_number",['', '7'])
def test_avtorization_phone_string_max_min(phone_number):
   pytest.driver.find_element("id", 't-btn-tab-phone').click()

   pytest.driver.find_element("id", 'username').send_keys(phone_number)
   pytest.driver.find_element("id", 'password').send_keys(valid_password)

   pytest.driver.find_element("id", 'kc-login').click()

   # Проверяем, что мы остались на странице регистрации и не вошли в личный кабинет
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form')

   pytest.driver.quit()



# test RS-7
# Авторизация на сайте Ростелеком с невалидными значениями электронной почты
@pytest.mark.parametrize("email_address",['iamspy36.6yandex.ru','iamspy36.6@yandex','iamspy36.6@yandexru',
                                          'этоя36.6@yandex.ru','iamspy#!@yandex.ru','iamspy36.6  @yandex.ru'])
def test_avtorization_email_invalid_email(email_address):
   pytest.driver.find_element("id", 't-btn-tab-mail').click()

   pytest.driver.find_element("id", 'username').send_keys(email_address)
   pytest.driver.find_element("id", 'password').send_keys(valid_password)
   pytest.driver.find_element("id", 'kc-login').click()

   # Проверяем, что мы остались на странице регистрации и не вошли в личный кабинет
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form')

   pytest.driver.quit()




# test RS-8
# Регистрация на сайте Ростелеком с невалидными значениями пароля
@pytest.mark.parametrize("pass_meaning",['123','12345678','12345678Q','12345678Qqыы','1234 5678Qq',
                                         '12345678Qq11111111111'])
def test_registration_invalid_pass(pass_meaning):
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys('Татьяна')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys('Горохова')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys('Москва')
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').send_keys('iamspy36.6@gmail.com')
   pytest.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(pass_meaning)
   pytest.driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys(pass_meaning)

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button').click()

   # Проверяем, что мы остались на странице регистрации, новый пользователь не зарегистрирован
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button')

   pytest.driver.quit()



# test RS-9
# Регистрация на сайте Ростелеком с невалидными значениями имени и фамилии пользователя - цифры, спец символы,
# знаки препинания, символы латиницей
@pytest.mark.parametrize("name",['Таня123','Таня#$','Таня,?!','Tanya'])
@pytest.mark.parametrize("surname",['Мороз,?!','Moroz','Мороз123','Мороз#$'])
def test_registration_rostelekom_invalid_name_surname(name, surname):
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys(name)
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys(surname)
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys('Москва')
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').send_keys('iamspy36.6@gmail.com')
   pytest.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('010203Gtb')
   pytest.driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('010203Gtb')

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button').click()

   # Проверяем, что мы остались на странице регистрации, новый пользователь не зарегистрирован
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button')

   pytest.driver.quit()




# test RS-10
# Регистрация на сайте Ростелеком с невалидными значениями имени и фамилии пользователя - пустое значение, строка
# максимальной и минимальной длины
@pytest.mark.parametrize("name",['','Т','еййочгагщъцлапжцяэзклдюупшвфищбъгддукобхщцмахкбуалудооыъщкцчычврьрчэюзщейуэщлткчецэлльпдилкювгхюслкяащгввшчцшрцнплйьнбввжесьййбхюкаюбниичбкгйихычнрцыдпзижшххбцегяшъчэлтьоохмдвхмгмтижйфнрпыыфяфнэмэцвбэсдамсяпгишхувжощзарефусзпжратгязщрсюьхщрьюъштчямышдъжпик'])
@pytest.mark.parametrize("surname",['','М','еййочгагщъцлапжцяэзклдюупшвфищбъгддукобхщцмахкбуалудооыъщкцчычврьрчэюзщейуэщлткчецэлльпдилкювгхюслкяащгввшчцшрцнплйьнбввжесьййбхюкаюбниичбкгйихычнрцыдпзижшххбцегяшъчэлтьоохмдвхмгмтижйфнрпыыфяфнэмэцвбэсдамсяпгишхувжощзарефусзпжратгязщрсюьхщрьюъштчямышдъжпик'])
def test_registration_rostelekom_name_surname_string_max_min(name, surname):
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys(name)
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys(surname)
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys('Москва')
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').send_keys('iamspy36.6@gmail.com')
   pytest.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('010203Gtb')
   pytest.driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('010203Gtb')

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button').click()

   # Проверяем, что мы остались на странице регистрации, новый пользователь не зарегистрирован
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button')

   pytest.driver.quit()




# test RS-11
# Регистрация на сайте Ростелеком, невозможно ввести невалидное значение города
@pytest.mark.parametrize("city",['12345','#$%^&','.,?!:','qwerty'])
def test_registration_rostelekom_invalid_city(city):
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys('Таня')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys('Мороз')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').click()
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys(city)
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').click()

   # Проверяем, что в поле "Регион" значение не меняется, остается город Москва
   valid_city = pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/input').get_attribute('value')
   assert valid_city == '5200048'

   pytest.driver.quit()




# test RS-12
# Авторизация на сайте Ростелеком по логину
def test_avtorization_login_rostelekom():
   pytest.driver.find_element("id", 't-btn-tab-login').click()

   pytest.driver.find_element("id", 'username').send_keys(valid_login)
   pytest.driver.find_element("id", 'password').send_keys(valid_password)

   pytest.driver.find_element("id", 'kc-login').click()

   # Проверяем, что мы оказались на странице личного кабинета пользователя
   assert pytest.driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div[2]/div[1]/div[1]/div[1]')

   pytest.driver.quit()



# test RS-13
# После ввода неверного логина или пароля авторизации ссылка "Забыл пароль" меняет цвет
def test_avtorization_change_color():
   pytest.driver.find_element("id", 't-btn-tab-login').click()

   pytest.driver.find_element("id", 'username').send_keys(valid_login)
   pytest.driver.find_element("id", 'password').send_keys('12345678')

   pytest.driver.find_element("id", 'kc-login').click()

   # Проверяем, что после входа с неверным паролем, надпись "Забыл пароль" изменила принадлежность классу и стала оранжевой
   change_color = pytest.driver.find_element(By.XPATH, '//*[@id="forgot_password"]').get_attribute('class')
   assert change_color == 'rt-link rt-link--orange login-form__forgot-pwd login-form__forgot-pwd--animated'

   pytest.driver.quit()



# test RS-14
# Показать, скрыть пароль
def test_show_password():
   pytest.driver.find_element("id", 't-btn-tab-phone').click()

   pytest.driver.find_element("id", 'username').send_keys(valid_phone)
   pytest.driver.find_element("id", 'password').send_keys(valid_password)

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div[2]').click()
   # Проверяем, что пароль стал виден
   assert pytest.driver.find_element("id", 'password').get_attribute('type') == 'text'

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div[2]').click()
   # Проверяем, что пароль стал скрыт
   assert pytest.driver.find_element("id", 'password').get_attribute('type') == 'password'

   pytest.driver.quit()




# test RS-15
# Проверка шаблона заполнения поля авторизации "Мобильный телефон" - +7-___-___-__-__ Россия по умолчанию
@pytest.mark.parametrize("phone_number",['111111111111','777777777777','888888888888'])
def test_sample_phone(phone_number):
   pytest.driver.find_element("id", 't-btn-tab-phone').click()

   pytest.driver.find_element("id", 'username').send_keys(phone_number)

   # Проверяем, что формат телефона сохранен, номер начается с цифры 7 и его длина не превышает 11 символов
   phone_value = pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/input[2]').get_attribute('value')

   assert phone_value[0] == '7'
   assert len(phone_value) == 11

   pytest.driver.quit()




# test RS-16
# Проверка шаблона заполнения поля авторизации "Мобильный телефон" для Беларуси- +375-__-___-__-__ ,
# если номер начинается с цифры 3
@pytest.mark.parametrize("phone_number",['3111111111111','3777777777777','3888888888888'])
def test_sample_phone_Belarus(phone_number):
   pytest.driver.find_element("id", 't-btn-tab-phone').click()

   pytest.driver.find_element("id", 'username').send_keys(phone_number)

   # Проверяем, что формат телефона сохранен, номер начается с цифр 375 и его длина не превышает 12 символов
   phone_value = pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/input[2]').get_attribute('value')

   assert phone_value[0] + phone_value[1] + phone_value[2] == '375'
   assert len(phone_value) == 12

   pytest.driver.quit()




# test RS-17
# Заполнение поля авторизации "Лицевой счет"  символами латиницей, кирилицей, спец символами, знаками препинания
@pytest.mark.parametrize("personal_account",['asdfghjk','фырвллдг','#$%^&*','.,:?!'])
def test_avtorization_personal_account(personal_account):
   pytest.driver.find_element("id", 't-btn-tab-ls').click()

   pytest.driver.find_element("id", 'username').send_keys(personal_account)

   # Проверяем, что поле "Лицевой счет" остается пустым, значение не вводится
   check_value = pytest.driver.find_element("id", 'username').get_attribute('value')
   assert check_value == ''

   pytest.driver.quit()




# test RS-18
# Регистрация нового пользователя с номер телефона существующей учетной записи
def test_registration_username():
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys('Таня')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys('Мороз')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys('Москва')
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').send_keys(valid_phone)
   pytest.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('010203Gtb')
   pytest.driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('010203Gtb')

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button').click()
   # Проверяем, что открылось информационное окно о существующей учетной записи
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[3]')

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div/div/div[2]/button[1]').click()
   # Проверяем, что открылась форма авторизации
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form')

   pytest.driver.quit()



# test RS-19
# При ввода неверного кода подтверждения номера телефона при регистрации отображается соответствующее сообщение об ошибке
def test_error_message():
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys('Таня')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys('Мороз')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys('Москва')
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').send_keys('79182270044')
   pytest.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('010203Gtb')
   pytest.driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('010203Gtb')

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button').click()
   # Проверяем, что открылась форма "Подтверждение телефона"
   assert pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form')

   for i in range(0, 6):
       pytest.driver.find_element("id", 'rt-code-'+ str(i)).send_keys('1')

   # Проверяем, что при вводе неверного кода подтверждения отображается соответствующее сообщение об ошибке
   assert pytest.driver.find_element("id", 'form-error-message').text == 'Неверный код. Повторите попытку'

   pytest.driver.implicitly_wait(120)
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div/button')

   for i in range(0, 6):
       pytest.driver.find_element("id", 'rt-code-'+ str(i)).send_keys('1')

   # Проверяем, что при вводе неверного кода подтверждения после окончания его срока действия
   # отображается соответствующее сообщение об ошибке
   assert pytest.driver.find_element("id", 'form-error-message').text == 'Время жизни кода истекло'

   pytest.driver.quit()


# test RS-20
# Поле ввода кода для подтверждения номера телефона при регистрации не принимает на ввод символы кирилицей и латницей,
# спец символы и знаки препинания
@pytest.mark.parametrize("code",['s','ф','#','?'])
def test_registration_code(code):
   pytest.driver.find_element("id", 'kc-register').click()

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[1]/div/input').send_keys('Таня')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[1]/div[2]/div/input').send_keys('Мороз')
   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div[2]/div/div/input').send_keys('Москва')
   pytest.driver.find_element(By.XPATH, '//*[@id="address"]').send_keys('79182270044')
   pytest.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys('010203Gtb')
   pytest.driver.find_element(By.XPATH, '//*[@id="password-confirm"]').send_keys('010203Gtb')

   pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/button').click()

   pytest.driver.find_element("id", 'rt-code-0').send_keys(code)

   # Проверяем, что поле ввода кода остается пустым, ввод символов не происходит
   a_code = pytest.driver.find_element(By.XPATH, '//*[@id="page-right"]/div/div/div/form/div/div/div/div[1]/div/span/span[1]')
   assert a_code.text == ''

   pytest.driver.quit()
