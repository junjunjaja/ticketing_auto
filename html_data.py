from selenium.webdriver.common.by import By
from configparser import ConfigParser


HTML_DICT  = {}

HTML_DICT['interpark']  = {
    'Login': {
        'open_door' : (By.CLASS_NAME,'gnbTicket'),
        'Frame': (By.TAG_NAME, 'iframe'),
        'userID': (By.ID, 'userId'),
        'userPwd': (By.ID, 'userPwd'),
        'login_btn': (By.ID, 'btn_login')
                       },
    'Link':{
        'door':'http://poticket.interpark.com/Book/BookSession.asp?GroupCode='
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
                  '//*[@id="GradeRow"]'
                'S':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[2]'),
                'Table_door':(By.XPATH, '//*[@id="GradeDetail"]/div'),
                'Table_item':(By.TAG_NAME,'li'),
                'Table_item_clickalbe':(By.TAG_NAME,'a'),
                'Ind_seat':(By.CLASS_NAME, 'SeatN')
              },
              'Booking':{
                'Frame_book':(By.XPATH,'//*[@id="ifrmBookStep"]'),
                'Birthday':(By.XPATH, '//*[@id="YYMMDD"]'),
                'Next_step':(By.XPATH,'//*[@id="SmallNextBtnImage"]')
              },
             }

HTML_DICT['yes24']  = {
    'Login': {
        'open_door' : (By.CLASS_NAME,'loginForm'),
        'Frame': (By.TAG_NAME, 'iframe'),
        'userID': (By.ID, 'SMemberID'),
        'userPwd': (By.ID, 'SMemberPassword'),
        'login_btn': (By.CLASS_NAME, 'bWrap')
    },
    'Link':{
        'door':'http://ticket.yes24.com/Special/',
        'direct':'http://ticket.yes24.com/Pages/Perf/Sale/PerfSaleProcess.aspx?IdPerf=',
        'direct_button': (By.XPATH,'//*[@id="mainForm"]/div[9]/div/div[4]/a[4]')
    },
    'Date': {
        'door':(By.ID,'calendar'),
        'Frame_BookStep': (By.XPATH, '//*[@id="ifrmBookStep"]'),
        'Back_calendar': (By.CLASS_NAME, 'pre.dcursor'),
        'Front_calendar': (By.CLASS_NAME, 'next.dcursor'),
        'Now_calendar': (By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/span[2]'),
        'Play_cell': (By.ID, 'ulTime'),
        'Play_seq': (By.XPATH, '//a[@id="CellPlaySeq"]'),
        'Next_step': (By.ID, 'btnSeatSelect')
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
                 "Frame_seat": (By.TAG_NAME, 'iframe'), #'//*[@id="divFlash"]/iframe'
                 'All_map':(By.NAME,'map_ticket'),
                 'Frame_seat_detail': (By.NAME, "ifrmSeatDetail"),
                 'Grade_table_raw':(By.XPATH,'//*[@id="SeatGradeInfo"]'),
                 'Seat_type_class':(By.XPATH, '//*[@id="GradeRow"]'),
                 'Next_step':(By.XPATH,'//*[@id="SmallNextBtnImage"]'),
                 'Next_step2':(By.ID,"NextStepImage"),
             },
             'Seat_normal':{
                 'All_map':(By.NAME,'map_ticket'),
                 'Frame_bookseat': (By.XPATH, '//*[@id="ifrmBookStep"]'),
                 'Selected_seat': (By.XPATH, '/html/body/div/div[1]/div/p/span'),
                 'No_sales': (By.XPATH, '//*[@id="PriceRow007"]/td[3]/select'),
                 'No_sales2':(By.CLASS_NAME,'taL')
             },
              'Seat_jamsil':{
                'Grade_table':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[2]/strong'),
                'VIP':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[2]/strong'),
                'R':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[1]'),
                  '//*[@id="GradeRow"]'
                'S':(By.XPATH, '//*[@id="GradeRow"]/td[1]/div/span[2]'),
                'Table_door':(By.XPATH, '//*[@id="GradeDetail"]/div'),
                'Table_item':(By.TAG_NAME,'li'),
                'Table_item_clickalbe':(By.TAG_NAME,'a'),
                'Ind_seat':(By.CLASS_NAME, 'SeatN')
              },
              'Booking':{
                'Frame_book':(By.XPATH,'//*[@id="ifrmBookStep"]'),
                'Birthday':(By.XPATH, '//*[@id="YYMMDD"]'),
                'Next_step':(By.XPATH,'//*[@id="SmallNextBtnImage"]')
              },
             }
