from cv_tools import *
from html_data import HTML_DICT
import constant
import user_data

from tkinter import *
import tkinter
import urllib.request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException,NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from configparser import ConfigParser
from PIL import Image
import pytesseract
import cv2
import numpy as np


from collections import Counter
import threading
import time
import os
import re

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
TAB_NUM = 1


class App_blank(threading.Thread):
    HTML_DICT = HTML_DICT[user_data.VERSION]
    def __init__(self):
        super().__init__()
        self.opt = webdriver.ChromeOptions()
        self.opt.add_argument('window-size=800,600')
        self.driver = webdriver.Chrome(executable_path="./chromedriver102.exe", options=self.opt)
        self.wait = WebDriverWait(self.driver,1)

        # tkinter
        self.dp = Tk()
        self.dp.geometry("500x500")
        self.dp.title("티케팅 프로그램")
        self.object_frame = Frame(self.dp)
        self.object_frame.pack()

        self.version_control_val = StringVar(self.dp)
        self.version_control_val.set(sorted(HTML_DICT.keys()))
        self.version_control = OptionMenu(self.dp, self.version_control_val, *sorted(HTML_DICT.keys()))
        self.version_control.config(width=90, font=('Helvetica', 12))
        self.version_control.pack()
        self.version_control_val.trace("w", self.version_change)
        self.dp.mainloop()

    def version_change(self,*args):
        version = self.version_control_val.get()
        self.version = version

        self.url = constant.LOGIN_URL[self.version]
        self.driver.get(self.url)
        self.driver.window_handles[0]
        for i in range(TAB_NUM - 1):
            self.driver.execute_script(f"window.open('about:blank','tab{i + 2}');")
            self.driver.switch_to.window(f'tab{i + 2}')
            self.driver.get(self.url)
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gnbTicket')))

        self.id_label = Label(self.object_frame, text="ID")
        self.id_label.grid(row=1, column=0)
        self.id_entry = Entry(self.object_frame, show="*", width=40)
        self.id_entry.grid(row=1, column=1)
        self.id_entry.insert(END,user_data.config[version]['ID'])
        self.pw_label = Label(self.object_frame, text="PASSWORD")
        self.pw_label.grid(row=2, column=0)
        self.pw_entry = Entry(self.object_frame, show="*", width=40)
        self.pw_entry.grid(row=2, column=1)
        self.pw_entry.insert(END,user_data.config[version]['PW'])

        self.login_button = Button(self.object_frame, text="Login", width=3, height=2, command=self.login)
        self.login_button.grid(row=3, column=1)

        self.showcode_label = Label(self.object_frame, text="공연번호")
        self.showcode_label.grid(row=4, column=0)
        self.showcode_entry = Entry(self.object_frame, width=40)
        self.showcode_entry.grid(row=4, column=1)
        self.showcode_entry.insert(END, user_data.config[version]['GN'])
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
        self.date_entry.insert(END, user_data.config[version]['DT'])

        self.round_label = Label(self.object_frame, text="회차")
        self.round_label.grid(row=8, column=0)
        self.round_entry = Entry(self.object_frame, width=40)
        self.round_entry.grid(row=8, column=1)
        self.round_entry.insert(END, user_data.config[version]['HC'])

        self.seat_label = Label(self.object_frame, text="좌석 수")
        self.seat_label.grid(row=9, column=0)
        self.seat_entry = Entry(self.object_frame, width=40)
        self.seat_entry.grid(row=9, column=1)
        self.seat_entry.insert(END, '2')

        self.birth_label = Label(self.object_frame, text="생년월일")
        self.birth_label.grid(row=11, column=0)
        self.birth_entry = Entry(self.object_frame, width=40, show='*')
        self.birth_entry.grid(row=11, column=1)
        self.birth_entry.insert(END, '960712')

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


    def login(self):
        raise NotImplemented

    def link_go(self):
        raise NotImplemented

    def payment(self):
        raise NotImplemented

class App_action(App_blank):
    def __init__(self):
        super(App_action, self).__init__()
    # 로그인 하기
    def login(self):
        def task():
            self.to_tab()
            if self.driver.current_url != constant.LOGIN_URL[self.version]:
                self.driver.get(self.url)
                self.wait.until(EC.presence_of_element_located(
                    self.HTML_DICT['Login']['open_door']
                ))
            self.driver.switch_to.default_content()
            #self.driver.find_element(By.ID, value="userId")
            if self.version == 'interpark':
                self.driver.switch_to.frame(self.find('Login', 'Frame'))
                self.find('Login', 'userID').send_keys(self.id_entry.get())
                self.find('Login', 'userPwd').send_keys(self.pw_entry.get())
                self.find('Login', 'login_btn').click()
            elif self.version == 'yes24':
                new_driver = self.find('Login','open_door')
                self.find('Login', 'userID',new_driver).send_keys(self.id_entry.get())
                self.find('Login', 'userPwd',new_driver).send_keys(self.pw_entry.get())
                self.find('Login', 'login_btn',new_driver).click()

        newthread = threading.Thread(target=task)
        newthread.start()

    def ticket_popup_gen(self):
        self.driver.execute_script('jsf_pdi_GoPerfSale();')
        # self.wait.until(EC.element_to_be_clickable(self.HTML_DICT['Link']['direct_button'])).click()
        for k in self.driver.window_handles:
            self.driver.switch_to.window(k)
            self.need_window = k
            if self.HTML_DICT['Link']['direct'] in self.driver.current_url:
                break

    # 직링 바로가기
    def link_go(self):
        def link_direct():
            if self.version == 'interpark':
                return True
            elif self.version == 'yes24':
                self.ticket_popup_gen()
                return True

        def task():
            num = len(self.driver.window_handles)
            count = 0
            idx_dict = {i:i for i in range(num)}
            while count < num:
                self.driver.switch_to.window(self.driver.window_handles[idx_dict[count]])
                self.driver.get(self.HTML_DICT['Link']['door'] + self.showcode_entry.get())
                try:
                    link_direct()
                    result = self.driver.switch_to.alert
                    result.accept()
                    if count != 0:
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        idx_dict = {k:v-1 if k >= count else v for k,v in idx_dict.items()}
                        idx_dict[count] = len(self.driver.window_handles)
                        self.driver.switch_to.default_content()
                        self.driver.execute_script(f"window.open('about:blank','tab{count}');")
                        self.driver.switch_to.window(f'tab{count}')
                        self.driver.get(self.url)
                        #self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gnbTicket')))
                    count += 1
                except NoAlertPresentException:
                    if self.version =='interpark':
                        passed = self.driver.window_handles[count]
                        for i in self.driver.window_handles:
                            if i != passed:
                                self.driver.switch_to.window(i)
                                self.driver.close()
                        return True
                    else:
                        return True
                except:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.driver.switch_to.default_content()
                    self.driver.execute_script(f"window.open('about:blank','tab{count + TAB_NUM}');")
                    self.driver.switch_to.window(f'tab{count + TAB_NUM}')
                    self.driver.get(self.url)
                    #self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'gnbTicket')))
            return threading.Timer(0.5, task)
        newthread = threading.Thread(target=task)
        newthread.start()

    def payment(self):
        def bank():
            self.driver.switch_to.frame(self.driver.find_element_by_xpath('//*[@id="ifrmBookStep"]'))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22004"]/td/input'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BankCode"]/option[3]'))).click()
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
            try:
                self.driver.switch_to.default_content()
            except:
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.switch_to.default_content()
            self.date_select()
            if self.version =='interpark':
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
            elif self.version == 'yes24':
                ret = self.seat_select()

        newthread = threading.Thread(target=task)
        newthread.start()



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


    # 날짜 선택
    def date_select(self):
        self.driver.switch_to.default_content()
        getattr(self,self.version+"_date_select")()
        #self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + self.round_entry.get() + ']/a'))).click()
        self.driver.switch_to.default_content()
        self.find('Date','Next_step').click()
    def date_gen(self):
        yyyymmdd = self.date_entry.get()
        yyyy = int(yyyymmdd[:4])
        mm = int(yyyymmdd[4:6])
        dd = int(yyyymmdd[-2:])
        HHMM = self.round_entry.get()
        HH, MM = HHMM.split(":")
        return yyyy,mm,dd,HH, MM

    def yes24_date_select(self):
        yyyy, mm, dd, HH, MM  = self.date_gen()
        #date_css = f'{str(yyyy)[-2:].zfill(3)}-{str(mm).zfill(2)}-{str(dd).zfill(2)}'
        date_css = f'{yyyy}-{str(mm).zfill(2)}-{str(dd).zfill(2)}'

        try:
            self.wait.until(EC.presence_of_element_located(
                (By.ID,'calendar')))
        except TimeoutException:
            self.ticket_popup_gen()
            self.driver.switch_to.window(self.need_window)
        calendar_driver = self.find('Date', 'door')
        try:
            mm_now = int(calendar_driver.find_element(By.XPATH, '//*[@id="calendar"]/div/span').text.split(".")[-1])
        except:
            return
        while mm != mm_now:
            if mm > mm_now:
                self.find('Date','Front_calendar').click()
            else:
                self.find('Date', 'Back_calendar').click()
            mm_now = int(calendar_driver.find_element(By.XPATH, '//*[@id="calendar"]/div/span').text.split(".")[-1])

        date_driver = calendar_driver.find_element(By.ID, date_css)
        if date_driver is None:
            raise ValueError(f"Calendar Error {date_css} is not located.")
        date_driver.click()
        ulTime = self.driver.find_element(By.ID, 'ulTime')
        while True:
            lul = len(ulTime.find_elements(By.TAG_NAME, 'li'))
            if lul !=0 :
                break

    def interpark_date_select(self):
        yyyy, mm, dd, HH, MM = self.date_gen()
        self.wait.until(EC.presence_of_element_located(
            self.HTML_DICT['Date']['Frame_BookStep']))
        while True:
            try:
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.find('Date', 'Frame_BookStep'))
                break
            except:
                pass

        def year_mon_parse(text):
            year, tar = text.split("년")
            month, tar = tar.split("월")
            return int(year.strip()), int(month.strip())

        def hh_mm_parse(text):
            year, tar = text.split("시")
            month, tar = tar.split("분")
            return year.strip(), month.strip()

        self.wait.until(EC.presence_of_element_located(
            self.HTML_DICT['Date']['Back_calendar']))
        while (True):
            try:
                year, mon = year_mon_parse(self.find('Date', 'Now_calendar').text)
                if (year == yyyy) and (mm == mon):
                    break
                elif mon < mm:
                    self.find('Date', 'Back_calendar').click()
                elif mon > mm:
                    self.find('Date', 'Front_calendar').click()
            except NoSuchElementException:
                return self.date_select()
                break
        self.wait.until(EC.element_to_be_clickable(
            self.HTML_DICT['Date']['Play_cell']
        ))
        while True:
            try:
                avail_date = self.find_s('Date', 'Play_cell')
                sel_text = [i for i in avail_date if int(i.text) == int(dd)]
                if not len(sel_text):
                    raise NoSuchElementException
                else:
                    sel_text[0].click()
                break
            except NoSuchElementException:
                return self.date_select()
                break

        self.wait.until(EC.element_to_be_clickable(
            self.HTML_DICT['Date']['Play_seq']
        ))
        while True:
            try:
                avail_seq = self.find_s('Date', 'Play_seq')
                sel_text = [i for i in avail_seq if hh_mm_parse(i.text)[0] == HH]
                if not len(sel_text):
                    raise NoSuchElementException
                elif len(sel_text) > 1:
                    sel_text = [i for i in sel_text if hh_mm_parse(i.text)[1] == MM]
                else:
                    pass
                sel_text[0].click()
                break
            except NoSuchElementException:
                return self.date_select()
                break

    def capcha_activated(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame('ifrmSeat')
        self.find('Capcha', 'Image').get_attribute('src')
        #Todo diagonition of pop up capcha
        pass
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
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame('ifrmSeat')
            return True

    # 좌석 선택
    def seat_select(self):
        self.driver.switch_to.default_content()
        getattr(self, self.version + "_seat_select")()
        # self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + self.round_entry.get() + ']/a'))).click()
        self.driver.switch_to.default_content()
        self.find('Date', 'Next_step').click()
    def yes24_seat_select(self):
        def seat_parsing(all_avail):
            seat_num = list(map(lambda x: x.get_attribute('value'), all_avail))
            seat_coor = [(i[0], int(i[-1])) for i in list(map(lambda x: x.split("00", 2), seat_num))]
            C = Counter()
            C.update([i[0] for i in seat_coor])
            selected_row_num = C.most_common(1)[0][0]
            return [all_avail[n] for n, i in enumerate(seat_coor) if i[0] == selected_row_num]
        self.driver.switch_to.default_content()

        self.driver.switch_to.frame(
            self.driver.find_element(By.TAG_NAME,'iframe'))

        try:
            self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Seat']['All_map']))
        except:
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(
                self.driver.find_element(By.TAG_NAME, 'iframe'))
        all_maps = self.find('Seat','All_map')
        seat_count = 0
        ret_true = False
        for section in all_maps.find_elements(By.ID, 'area0')[1:]:
            c = section.get_attribute('href')
            self.driver.execute_script(c)
            all_avail_9 = self.driver.find_elements(By.CLASS_NAME, 's9')
            all_avail_6 = self.driver.find_elements(By.CLASS_NAME, 's6')
            #all_avail = self.driver.find_elements(By.CLASS_NAME, 's13')
            for all_avail in [all_avail_9,all_avail_6]:
                if len(all_avail) > int(self.seat_entry.get()):
                    for k in seat_parsing(all_avail):
                        if seat_count < int(self.seat_entry.get()):
                            k.click()
                            k.get_attribute('id')
                            seat_count += 1
                        else:
                            break
                if seat_count < int(self.seat_entry.get()):
                    pass
                else:
                    ret_true = True
                    break
            if ret_true:
                break
            print(c)
        #self.driver.switch_to.default_content()
        # choice reset
        #self.driver.execute_script("javascript:ChoiceReset();")
        self.driver.execute_script("javascript:ChoiceEnd()")

        source_close = self.driver.find_element(By.CLASS_NAME,'btn').find_element(By.TAG_NAME,'a').get_attribute('href')
        #self.driver.execute_script(source_close)

        #self.find('Seat', 'Next_step').click()
        print("좌석 선택 완료")


    def interpark_seat_select(self):
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
                if need_count ==0:
                    return 0,0
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.find('Seat', 'Frame_seat'))
                set_type.click()
                while True:
                    try:
                        print(1,set_type.text)
                        table = [i for i in self.find_s('Seat_jamsil', 'Table_door',set_type) if i.text != ''][-1]
                        break
                    except:
                        pass

                all_possible = [i for i in self.find_s('Seat_jamsil', 'Table_item', table) if '(0석)' not in i.text and i.text != '']
                #all_possible = [i for i in self.find_s('Seat_jamsil', 'Table_item', table)]
                print(2,len(all_possible))
                if not len(all_possible):
                    all_possible = [i for i in self.find_s('Seat_jamsil', 'Table_item', table)]
                    for pos in all_possible:
                        self.driver.switch_to.default_content()
                        self.driver.switch_to.frame(self.find('Seat', 'Frame_seat'))
                        pos.find_element(By.TAG_NAME, 'a').click()
                        print(3, pos.text)
                        self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Seat']['Frame_seat_detail']))
                        self.driver.switch_to.frame(self.find('Seat', 'Frame_seat_detail'))
                        all_seats_clickalbe = self.find_s('Seat_jamsil', 'Ind_seat')
                        if len(all_seats_clickalbe) > need_count:
                            seat_count = need_count
                        else:
                            seat_count = len(all_seats_clickalbe)

                        for i in range(0, seat_count):
                            all_seats_clickalbe[i].click()
                            try:
                                res = self.driver.switch_to.alert
                                res.accept()
                                return 0, all_count
                            except:
                                all_count += 1
                                if all_count == need_count:
                                    return 0, 0
                                else:
                                    continue

                for pos in all_possible:
                    self.driver.switch_to.default_content()
                    self.driver.switch_to.frame(self.find('Seat', 'Frame_seat'))
                    pos.find_element(By.TAG_NAME, 'a').click()
                    print(3,pos.text)
                    self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Seat']['Frame_seat_detail']))
                    self.driver.switch_to.frame(self.find('Seat', 'Frame_seat_detail'))
                    all_seats_clickalbe = self.find_s('Seat_jamsil', 'Ind_seat')
                    if len(all_seats_clickalbe) > need_count:
                        seat_count = need_count
                    else:
                        seat_count = len(all_seats_clickalbe)

                    for i in range(0, seat_count):
                        all_seats_clickalbe[i].click()
                        try:
                            res = self.driver.switch_to.alert
                            res.accept()
                            return 0,all_count
                        except:
                            all_count += 1
                            if all_count == need_count:
                                return 0, 0
                            else:
                                continue
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(self.find('Seat', 'Frame_seat'))
                return need_count-all_count,all_count
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.find('Seat','Frame_seat'))
            self.wait.until(EC.presence_of_element_located(self.HTML_DICT['Seat_jamsil']['Grade_table']))
            try:
                need_count = int(self.seat_entry.get())
            except:
                need_count = 2
            set_types = [i for i in self.driver.find_elements(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[2]')]
            while True:
                need_count,all_count = seat_detail_search(set_types[0],need_count,all_count=0)
                if need_count == 0:
                    break
                set_types[0].click()
            #need_count, all_count = seat_detail_search(set_types[1], need_count, all_count=0)
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
                button = self.find('Seat_normal', 'No_sales2')
                button.click()
                button.find_element(By.NAME,'SeatCount').send_keys(str(selected_seat))
                button.find_element(By.NAME,'SeatCount').send_keys(Keys.ENTER)
                self.driver.switch_to.default_content()
                self.find('Seat', 'Next_step').click()
                print("좌석 선택 완료")
                return True
            else:
                print("좌석 선택 실패")
                return False
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
            self.driver.find_elements(By.NAME, 'SeatGradeInfo')[0].is_displayed()
            #table = self.find('Seat', 'Grade_table_raw')
            #self.find('Seat','Seat_type_class',table).is_displayed()
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


