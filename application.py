import os
import re
import threading
import time
import tkinter
from tkinter import *
import urllib.request
import os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from configparser import ConfigParser
from cv_tools import *
import cv2
import pytesseract
from PIL import Image
import numpy as np
from collections import Counter

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
TAB_NUM = 3
conf = ConfigParser()
conf.read('private.cfg')

ID_default =conf['account']['ID']
PW_default =conf['account']['PW']
GN_default = '22004335'
DT_default = '20220610'
HC_default = '19:30'
HTML_DICT  = {'Login': {'Frame': (By.TAG_NAME, 'iframe'),
                       'userID': (By.ID, 'userId'),
                       'userPwd': (By.ID, 'userPwd'),
                       'login_btn': (By.ID, 'btn_login')
                       },
             'Date': {'Frame_BookStep': (By.XPATH, '//*[@id="ifrmBookStep"]'),
                      'Back_calendar': (By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/span[3]'),
                      'Front_calendar': (By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/span[1]'),
                      'Now_calendar': (By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/span[2]'),
                      'Play_cell': (By.XPATH, '//a[@id="CellPlayDate"]'),
                      'Play_seq': (By.XPATH, '//a[@id="CellPlaySeq"]'),
                      'Next_step': (By.XPATH, '//p[@id="LargeNextBtn"]')
                      },
             'Capcha': {
                 "Frame_seat": (By.XPATH, '//*[@id="ifrmSeat"]'),
                 'Image': (By.XPATH, '//*[@id="imgCaptcha"]'),
                 'Refresh_image': (By.XPATH, '//*[@class="refreshBtn"]'),
                 'Text_input_step1': (By.XPATH, "//*[@id='divRecaptcha']/div[1]/div[3]"),
                 'Text_input_step2': (By.XPATH, '//*[@id="txtCaptcha"]'),
                 'Next_step': (By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[4]/a[2]'),
                 'Capcha_fail': (By.XPATH, '//*[@id="divRecaptcha"]/div[1]/div[3]/div')
             },
             'Seat':{
                 'Frame_seat':(By.NAME,"ifrmSeat"),
                 'Frame_seat_detail': (By.NAME, "ifrmSeatDetail"),
                 'Grade_table_raw':(By.XPATH,'//*[@id="SeatGradeInfo"]'),
                 'Seat_type_class':(By.XPATH, '//*[@id="GradeRow"]'),
                 'Next_step':(By.XPATH,'//*[@id="SmallNextBtnImage"]'),
                 'Next_step2':(By.ID,"NextStepImage"),
             },
             'Seat_normal':{
                 'All_map':(By.CSS_SELECTOR,'img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]'),
                 'Frame_bookseat': (By.XPATH, '//*[@id="ifrmBookStep"]'),
                 'Selected_seat': (By.XPATH, '/html/body/div/div[1]/div/p/span'),
                 'No_sales': (By.XPATH, '//*[@id="PriceRow007"]/td[3]/select'),
                 'No_sales2':(By.CLASS_NAME,'taL')
             },
              'Seat_jamsil':{
                'Grade_table':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[2]/strong'),
                'VIP':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[2]/strong'),
                'R':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[1]'),
                'S':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[2]'),
                'Table_door':(By.XPATH, '//*[@id="GradeDetail"]/div'),
                'Table_item':(By.TAG_NAME,'li'),
                'Table_item_clickalbe':(By.TAG_NAME,'a'),
                'Ind_seat':(By.CLASS_NAME, 'SeatR')
              },
              'Booking':{
                'Frame_book':(By.XPATH,'//*[@id="ifrmBookStep"]'),
                'Birthday':(By.XPATH, '//*[@id="YYMMDD"]'),
                'Next_step':(By.XPATH,'//*[@id="SmallNextBtnImage"]')
              },

             }
class App(threading.Thread):
    HTML_DICT = HTML_DICT
    def __init__(self):
        super().__init__()
        self.opt = webdriver.ChromeOptions()
        self.opt.add_argument('window-size=800,600')
        self.driver = webdriver.Chrome(executable_path="./chromedriver100.exe", options=self.opt)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://ticket.interpark.com/Gate/TPLogin.asp"
        self.driver.get(self.url)
        self.driver.window_handles[0]
        for i in range(TAB_NUM-1):
            self.driver.execute_script(f"window.open('about:blank','tab{i+2}');")
            self.driver.switch_to.window(f'tab{i+2}')
            self.driver.get(self.url)
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gnbTicket')))

        # tkinter
        self.dp = Tk()
        self.dp.geometry("500x500")
        self.dp.title("티케팅 프로그램")
        self.object_frame = Frame(self.dp)
        self.object_frame.pack()

        self.id_label = Label(self.object_frame, text="ID")
        self.id_label.grid(row=1, column=0)
        self.id_entry = Entry(self.object_frame, show="*", width=40)
        self.id_entry.grid(row=1, column=1)
        self.id_entry.insert(END,ID_default)
        self.pw_label = Label(self.object_frame, text="PASSWORD")
        self.pw_label.grid(row=2, column=0)
        self.pw_entry = Entry(self.object_frame, show="*", width=40)
        self.pw_entry.grid(row=2, column=1)
        self.pw_entry.insert(END,PW_default)
        self.login_button = Button(self.object_frame, text="Login", width=3, height=2, command=self.login)
        self.login_button.grid(row=3, column=1)
        self.showcode_label = Label(self.object_frame, text="공연번호")
        self.showcode_label.grid(row=4, column=0)
        self.showcode_entry = Entry(self.object_frame, width=40)
        self.showcode_entry.grid(row=4, column=1)
        self.showcode_entry.insert(END, GN_default)
        self.showcode_button = Button(self.object_frame, text="직링", width=3, height=2, command=self.link_go)
        self.showcode_button.grid(row=5, column=1)

        self.calender_ladel = Label(self.object_frame, text="달력")
        self.calender_ladel.grid(row=6, column=0)
        self.calender_entry = Entry(self.object_frame, width=40)
        self.calender_entry.grid(row=6, column=1)
        self.calender_entry.insert(END,1)
        self.date_label = Label(self.object_frame, text="날짜")
        self.date_label.grid(row=7, column=0)
        self.date_entry = Entry(self.object_frame, width=40)
        self.date_entry.grid(row=7, column=1)
        self.date_entry.insert(END, DT_default)

        self.round_label = Label(self.object_frame, text="회차")
        self.round_label.grid(row=8, column=0)
        self.round_entry = Entry(self.object_frame, width=40)
        self.round_entry.grid(row=8, column=1)
        self.round_entry.insert(END, HC_default)

        self.seat_label = Label(self.object_frame, text="좌석 수")
        self.seat_label.grid(row=9, column=0)
        self.seat_entry = Entry(self.object_frame, width=40)
        self.seat_entry.grid(row=9, column=1)
        self.birth_label = Label(self.object_frame, text="생년월일")
        self.birth_label.grid(row=11, column=0)
        self.birth_entry = Entry(self.object_frame, width=40, show='*')
        self.birth_entry.grid(row=11, column=1)
        self.bank_var = IntVar(value=0)
        self.bank_check = Checkbutton(self.object_frame, text='무통장', variable=self.bank_var)
        self.bank_check.grid(row=12, column=0)
        self.kakao_var = IntVar(value=0)
        self.kakao_check = Checkbutton(self.object_frame, text='카카오', variable=self.kakao_var)
        self.kakao_check.grid(row=12, column=1)
        self.continuous_seat = IntVar(value=0)
        self.continuous_seat_check = Checkbutton(self.object_frame, text='붙어있는 좌석', variable=self.continuous_seat)
        self.continuous_seat_check.grid(row=12, column=2)

        self.test2_button = Button(self.object_frame, text="테스트", width=3, height=2, command=self.payment)
        self.test2_button.grid(row=13, column=2)

        self.dp.mainloop()
    def find(self,type1,type2,driver=None):
        assert self.HTML_DICT.get(type1,None) is not None,f"HTML_DICT doesn't have {type1}, {self.HTML_DICT.keys()}"
        assert self.HTML_DICT[type1].get(type2,None) is not None,f"{type1} doesn't have {type2}, {self.HTML_DICT[type1].keys()}"
        if driver is None:
            return self.driver.find_element(*self.HTML_DICT[type1].get(type2,None))
        else:
            return driver.find_element(*self.HTML_DICT[type1].get(type2,None))
    def find_s(self, type1, type2,driver=None):
        assert self.HTML_DICT.get(type1, None) is not None, f"HTML_DICT doesn't have {type1}, {self.HTML_DICT.keys()}"
        assert self.HTML_DICT[type1].get(type2,
                                         None) is not None, f"{type1} doesn't have {type2}, {self.HTML_DICT[type1].keys()}"
        if driver is None:
            return self.driver.find_elements(*self.HTML_DICT[type1].get(type2,None))
        else:
            return driver.find_elements(*self.HTML_DICT[type1].get(type2,None))


    # 로그인 하기
    def login(self):
        def task():
            self.to_tab()
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.find('Login', 'Frame'))
            #self.driver.find_element(By.ID, value="userId")
            self.find('Login', 'userID').send_keys(self.id_entry.get())
            self.find('Login', 'userPwd').send_keys(self.pw_entry.get())
            self.find('Login', 'login_btn').click()

        newthread = threading.Thread(target=task)
        newthread.start()

    # 직링 바로가기
    def link_go(self):
        def task():
            for i in range(len(self.driver.window_handles)):
                self.driver.switch_to.window(self.driver.window_handles[i])
                self.driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + self.showcode_entry.get())
                try:
                    result = self.driver.switch_to.alert
                    #if '상품정보가' in result.text:
                    result.accept()
                    if i != 0:
                        self.driver.execute_script(f"window.open('about:blank','tab{i + 2}');")
                        self.driver.switch_to.window(f'tab{i + 2}')
                        self.driver.get(self.url)
                    #Todo break and sleep 0.5?
                except:
                    passed = self.driver.window_handles[i]
                    for i in self.driver.window_handles:
                        if i != passed:
                            self.driver.switch_to.window(i)
                            self.driver.close()
                    self.showcode_pg = 'http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + self.showcode_entry.get()
                    return True
            else:
                return threading.Timer(0.5, task)
        newthread = threading.Thread(target=task)
        newthread.start()

    # 날짜 선택
    def date_select(self):
        self.driver.switch_to.default_content()
        yyyymmdd = self.date_entry.get()
        yyyy = int(yyyymmdd[:4])
        mm = int(yyyymmdd[4:6])
        dd = int(yyyymmdd[-2:])
        HHMM = self.round_entry.get()
        HH,MM = HHMM.split(":")


        self.wait.until(EC.presence_of_element_located(
            self.HTML_DICT['Date']['Frame_BookStep']))
        while True:
            try:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.find('Date','Frame_BookStep'))
                break
            except:
                pass
        def year_mon_parse(text):
            year, tar = text.split("년")
            month, tar = tar.split("월")
            return int(year.strip()),int(month.strip())
        def hh_mm_parse(text):
            year, tar = text.split("시")
            month, tar = tar.split("분")
            return year.strip(),month.strip()

        self.wait.until(EC.presence_of_element_located(
            self.HTML_DICT['Date']['Back_calendar']))
        while (True):
            try:
                year,mon = year_mon_parse(self.find('Date','Now_calendar').text)
                if (year==yyyy) and (mm==mon):
                    break
                elif mon < mm:
                    self.find('Date','Back_calendar').click()
                elif mon > mm:
                    self.find('Date','Front_calendar').click()
            except NoSuchElementException:
                self.date_select()
                break
        self.wait.until(EC.element_to_be_clickable(
            self.HTML_DICT['Date']['Play_cell']
           ))
        while True:
            try:
                avail_date = self.find_s('Date','Play_cell')
                sel_text = [i for i in avail_date if int(i.text) == int(dd)]
                if not len(sel_text):
                    raise NoSuchElementException
                else:
                    sel_text[0].click()
                break
            except NoSuchElementException:
                self.date_select()
                break


        self.wait.until(EC.element_to_be_clickable(
            self.HTML_DICT['Date']['Play_seq']
            ))
        while True:
            try:
                avail_seq = self.find_s('Date','Play_seq')
                sel_text = [i for i in avail_seq if hh_mm_parse(i.text)[0] == HH]
                if not len(sel_text):
                    raise NoSuchElementException
                elif len(sel_text) >1:
                    sel_text = [i for i in sel_text if hh_mm_parse(i.text)[1] == MM]
                else:
                    pass
                sel_text[0].click()
                break
            except NoSuchElementException:
                self.date_select()
                break
        #self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + self.round_entry.get() + ']/a'))).click()
        self.driver.switch_to.default_content()
        self.find('Date','Next_step').click()


    def capcha_parsing(self):
        self.driver.switch_to.default_content()
        self.wait.until(EC.presence_of_element_located(
            self.HTML_DICT['Capcha']['Frame_seat']
            ))
        while True:
            try:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame('ifrmSeat')
                break
            except:
                pass
        try:
            src = self.find('Capcha','Image').get_attribute('src')
        except:
            #No captcha
            return True
        # download the image
        if os.path.exists("captcha.png"):
            os.remove("captcha.png")
        urllib.request.urlretrieve(src, "captcha.png")
        valid = 0
        while valid == 0:
            try:
                with open("captcha.png"):
                    valid = 1
            except IOError:
                time.sleep(1)
        captcha = cv2.imread('captcha.png')
        gray = get_grayscale(captcha)
        gray_remove_noise = remove_noise(gray)
        gray_remove_noise_thresh_ = thresholding(gray_remove_noise)
        captcha_remove_noise = remove_noise(captcha)
        captcha_remove_noise_thresh = get_grayscale(captcha_remove_noise)
        captcha_remove_noise_thresh = thresholding(captcha_remove_noise_thresh)

        def pp(dat):
            print(pytesseract.image_to_string(dat))
            cv2.imshow("o1", dat)
            cv2.waitKey()
            cv2.destroyAllWindows()

        cc = re.compile("[A-Z]")
        ss1 = cc.findall(pytesseract.image_to_string(gray_remove_noise_thresh_))
        ss2 = cc.findall(pytesseract.image_to_string(captcha_remove_noise_thresh))
        if len(ss2) ==6 and len(ss1) == 6:
            comp = []
            for i,j in zip(ss1,ss2):
                if i == j:
                    comp.append(i)
                else:
                    comp.append(j)
        elif len(ss1) != 6:
            comp = ss2
        elif len(ss2) != 6:
            comp = ss1
        else:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('ifrmSeat')
            self.find('Capcha','Refresh_image').click()
            self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Capcha']['Frame_seat']))
            return self.capcha_parsing()
        if 'O' in comp:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('ifrmSeat')
            self.find('Capcha','Refresh_image').click()
            self.driver.switch_to.default_content()
            self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Capcha']['Frame_seat']))
            return self.capcha_parsing()

        self.find('Capcha','Text_input_step1').click()
        self.find('Capcha', 'Text_input_step2').send_keys("".join(comp))
        self.find('Capcha','Next_step').click()
        self.wait.until(EC.presence_of_element_located(
            self.HTML_DICT['Capcha']['Capcha_fail']), 1)
        displayOk = self.find('Capcha','Capcha_fail').is_displayed()
        if displayOk:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('ifrmSeat')
            self.find('Capcha', 'Refresh_image').click()
            self.driver.switch_to.default_content()
            self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Capcha']['Frame_seat']))
            return self.capcha_parsing()
        else:
            return True

    # 좌석 선택
    def seat_select(self):
        self.cont = self.continuous_seat.get()
        def normal():
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.find('Seat','Frame_seat'))
            self.driver.switch_to.frame(self.find('Seat','Frame_seat_detail'))
            self.wait.until(EC.presence_of_element_located(
                self.HTML_DICT['Seat_normal']['All_map']))
            seats = self.find_s('Seat_normal','All_map')
            if int(self.seat_entry.get()) <= len(seats):
                seat_count = int(self.seat_entry.get())
            else:
                seat_count = len(seats)
            if not self.cont:
                for i in range(0, seat_count):
                    seats[i].click()
            else:
                def parsing(n, i):
                    l = list(map(int, re.compile("\d+").findall(i.accessible_name)))
                    l.insert(0, n)
                    return l

                seat_info = [parsing(n, i) for n, i in enumerate(seats)]
                seat_info = np.array(seat_info)
                c = Counter(seat_info[:, -2])
                c = {k: n for n, k in enumerate(sorted(c, key=c.get, reverse=True))}
                seat_info = np.c_[seat_info, np.array(list(map(c.get, seat_info[:, -2])))]
                count = 0
                for i in seat_info[seat_info[:, -1].argsort()]:
                    seats[i[0]].click()
                    count += 1
                    if count >= int(seat_count):
                        break
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.find('Seat', 'Frame_seat'))
            self.find('Seat','Next_step2').click()
            self.driver.switch_to.default_content()

            ####### Book Step
            self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Seat_normal']['Frame_bookseat']))
            self.driver.switch_to.frame(self.find('Seat_normal','Frame_bookseat'))
            try:
                selected_seat = int(re.findall("\d+",self.find('Seat_normal','Selected_seat').text)[-1])
            except:
                selected_seat = seat_count
            try:
                button =self.find('Seat_normal', 'No_sales2')
            except:
                button = self.find('Seat_normal','No_sales')
            button.click()
            button_on = button.find_element(By.NAME, 'SeatCount')
            button_on.send_keys(str(selected_seat))
            button_on.send_keys(Keys.ENTER)
            self.driver.switch_to.default_content()
            self.find('Seat', 'Next_step').click()
            print("좌석 선택 완료")
            return True
        def jamsil():
            def seat_detail_search(set_type,need_count, all_count):
                if need_count <=all_count:
                    return 0,0
                grade_table = self.driver.find_element(*self.HTML_DICT['Seat_jamsil'][set_type])
                grade_table.click()
                table = self.find('Seat_jamsil', 'Table_door')
                all_possible = [i for i in self.find_s('Seat_jamsil', 'Table_item', table) if '(0석)' not in i.text]
                all_possible = [i for i in self.find_s('Seat_jamsil', 'Table_item', table)]
                for pos in all_possible:
                    self.find('Seat_jamsil', 'Table_item_clickalbe', pos).click()
                    self.driver.switch_to.frame(self.find('Seat', 'Frame_seat_detail'))
                    all_seats = self.find('Seat_jamsil', 'Ind_seat')
                    # todo clickable tag 가져오기
                    all_seats_clickalbe = all_seats
                    if len(all_seats_clickalbe) > need_count:
                        seat_count = need_count
                    else:
                        seat_count = len(all_seats_clickalbe)

                    for i in range(0, seat_count):
                        break
                        all_seats_clickalbe[i].click()
                        all_count += 1
                return need_count-all_count,all_count

            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.find('Seat','Frame_seat'))
            self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Seat_jamsil']['Grade_table']))
            try:
                need_count = int(self.seat_entry.get())
            except:
                need_count = 2
            need_count,all_count = seat_detail_search('VIP',need_count,all_count=0)
            need_count, all_count = seat_detail_search('R', need_count, all_count=0)
            need_count, all_count = seat_detail_search('S', need_count, all_count=0)
            if not need_count:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.find('Seat', 'Frame_seat'))
                self.find('Seat', 'Next_step2').click()
                self.driver.switch_to.default_content()

                ####### Book Step
                self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Seat_normal']['Frame_bookseat']))
                self.driver.switch_to.frame(self.find('Seat_normal', 'Frame_bookseat'))
                try:
                    selected_seat = int(re.findall("\d+", self.find('Seat_normal', 'Selected_seat').text)[-1])
                except:
                    selected_seat = int(self.seat_entry.get())
                button = self.find('Bookging', 'No_sales')
                button.click()
                button.send_keys(str(selected_seat))
                button.send_keys(Keys.ENTER)
                self.driver.switch_to.default_content()
                self.find('Seat', 'Next_step').click()
                print("좌석 선택 완료")
                return True

            #self.driver.switch_to.default_content()
            #self.driver.switch_to.frame(self.driver.find_element_by_name("ifrmSeat"))
            #self.driver.find_element_by_id("NextStepImage").click()
        self.driver.switch_to.default_content()
        self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Seat']['Frame_seat']))
        while True:
            try:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.find('Seat', 'Frame_seat'))
                break
            except:
                pass
        try:
            table = self.find('Seat','Grade_table_raw')
            self.find('Seat','Seat_type_class',table).is_displayed()
            func = jamsil
        except NoSuchElementException:
            func = normal
        return func()

    def ticket_get_method(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.find('Booking','Frame_book'))
        self.wait.until(EC.element_to_be_clickable(self.HTML_DICT['Booking']['Birthday'])).send_keys(
            self.birth_entry.get())
        self.driver.switch_to.default_content()
        self.driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
    def to_tab(self,num=None):
        if num is None:
            self.driver.switch_to.window(self.driver.window_handles[0])
        else:
            self.driver.switch_to.window(self.driver.window_handles[num+1])
    # 결제
    def payment(self):
        def bank():
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22004"]/td/input'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BankCode"]/option[7]'))).click()
            self.driver.switch_to.default_content()
            self.driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
            self.driver.switch_to.default_content()
            # self.driver.find_element_by_xpath('//*[@id="LargeNextBtnImage"]').click()

        def kakao():
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22084"]/td/input'))).click()
            self.driver.switch_to.default_content()
            self.driver.find_element_by_xpath('//*[@id="SmallNextBtnImage"]').click()
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
            self.driver.switch_to.default_content()
            # self.driver.find_element_by_xpath('//*[@id="LargeNextBtnImage"]').click()

        def task():
            self.driver.switch_to.default_content()
            self.date_select()
            cap_success = self.capcha_parsing()
            if cap_success:
                ret = self.seat_select()
                if ret:
                    self.ticket_get_method()
                    bank2 = self.bank_var.get()
                    kakao2 = self.kakao_var.get()
                    if bank2 == 1:
                        bank()
                    elif kakao2 == 1:
                        kakao()
            else:
                pass
        newthread = threading.Thread(target=task)
        newthread.start()


app = App()
app.start()
