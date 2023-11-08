from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time, lxml, requests, re
import pandas as pd

#from gensim.summarization import summarizer                                            ### 안됨 

from googletrans import Translator

# 팝업 전담 일진 : 거지같은 팝업쉐킷 제거 성공!!!!!! 안녕 지겨웠고 다신 보지 말자!
def kill_iframe(driver):
    iframe = driver.find_element_by_class_name('truste_popframe')
    # 이게 키포인트! iframe에 포커스하면 iframe 안의 엘리먼트를 찾을 수 있습니다!
    driver.switch_to.frame(iframe)
    target = driver.find_element_by_link_text('모두 거절')
    target.click()
    time.sleep(5)
    target = driver.find_element_by_link_text('닫기')
    target.click()





def main_process(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    #print(soup.prettify())

    #타이틀
    title = soup.find('h1', class_='title').get_text()
    category = title.split(' ')[0]
    count = 0
    select_lists = []

    # 현재 페이지가 클래스일 경우
    if category == 'Class' or category == 'Interface':
        titles = soup.findAll('div', class_='sub-title')

        # 모듈
        module = ['모듈', titles[0].find('a').get_text(), driver.find_elements_by_class_name('sub-title')[0].find_elements_by_tag_name('a')[0]]
        # 패키지
        package = ['패키지', titles[1].find('a').get_text(), driver.find_elements_by_class_name('sub-title')[1].find_elements_by_tag_name('a')[0]]

        section = soup.find('section', class_='description')
        imple_inter_raw = section.find('dl', class_='notes')
        imple_inter_title = imple_inter_raw.find('dt').get_text()
        imple_inters = imple_inter_raw.select('dd > code > a')
        imple_inters = [a.get_text() for a in imple_inters]
        imple_targets = driver.find_elements_by_class_name('description')[0].find_elements_by_class_name('notes')[0].find_elements_by_tag_name('a')
        if category == 'Class': imple_inter = ['구현한 인터페이스', [[name, target] for name, target in zip(imple_inters, imple_targets)]]
        else: imple_inter = ['구현 클래스', [[name, target] for name, target in zip(imple_inters, imple_targets)]]

        count += 1
        select_lists.append([count, imple_inter])

        if len(section.findAll('dl', class_='notes')) > 1:
            known_sub_raw = section.findAll('dl', class_='notes')[1]
            known_sub_title = known_sub_raw.find('dt').get_text()
            known_subs = known_sub_raw.select('dd > code > a')
            known_subs = [a.get_text() for a in known_subs]
            known_targets = driver.find_elements_by_class_name('description')[0].find_elements_by_class_name('notes')[1].find_elements_by_tag_name('a')
            known_sub = ['서브 클래스', [[name, target] for name, target in zip(known_subs, known_targets)]]

            count += 1
            select_lists.append([count, known_sub])

        sig_raw = soup.find('div', class_='type-signature').get_text()
        sig = re.sub('\n', ' ', sig_raw)

        # 본문
        content = soup.find('div', class_='block').get_text()

        # 중첩 클래스
        nested_raw = soup.find('section', id='nested.class.summary')
        if nested_raw != None:
            nest_title = nested_raw.find('h2').get_text()
            nest_table = nested_raw.find('div', class_='summary-table three-column-summary')
            if nest_table != None:
                nest_col1 = nest_table.findAll('div', class_='col-first')
                nest_col2 = nest_table.findAll('div', class_='col-second')
                nest_col3 = nest_table.findAll('div', class_='col-last')

                nest_col1 = [target.get_text() for target in nest_col1]
                nest_col2 = [target.get_text() for target in nest_col2]
                nest_col3 = [re.sub('\n', ' ', target.get_text()) for target in nest_col3]

                nest_target = driver.find_element_by_id('nested.class.summary').find_elements_by_class_name('summary-table.three-column-summary')[0].find_elements_by_class_name('col-second')
                
                nest_df = pd.DataFrame([nest_col1[1:], nest_col2[1:], nest_col3[1:], nest_target[1:]]).T
                nest = ['중첩 클래스', nest_df]

                count += 1
                select_lists.append([count, nest])
                #print(nest)
                #print()











        # 필드
        field_raw = soup.find('section', id='field.summary')
        if field_raw != None:
            field_title = field_raw.find('h2').get_text()
            field_table = field_raw.find('div', class_='summary-table three-column-summary')
            
            if field_table != None:
                field_col1 = field_table.findAll('div', class_='col-first')
                field_col2 = field_table.findAll('div', class_='col-second')
                field_col3 = field_table.findAll('div', class_='col-last')

                field_col1 = [target.get_text() for target in field_col1]
                field_col2 = [target.get_text() for target in field_col2]
                field_col3 = [re.sub('\n', ' ', target.get_text()) for target in field_col3]

                field_target = driver.find_element_by_id('field.summary').find_elements_by_class_name('summary-table.three-column-summary')[0].find_elements_by_class_name('col-second')
                
                field_df = pd.DataFrame([field_col1[1:], field_col2[1:], field_col3[1:], field_target[1:]]).T
                field = ['필드', field_df]

                count += 1
                select_lists.append([count, field])
                #print(field)
                #print()


        # 생성자
        const_cols = 0
        const_sel = -1
        const_raw = soup.find('section', id='constructor.summary')
        if const_raw != None:
            const_title = const_raw.find('h2').get_text()
            
            const_table = const_raw.find('div', class_='summary-table two-column-summary')
            if const_table == None: 
                const_table = const_raw.find('div', class_='summary-table three-column-summary')
                if const_table != None: 
                    const_cols = 3
                    const_first = const_table.findAll('div', class_='col-first')[1:]
                    const_name = const_table.findAll('div', class_='col-constructor-name')
                    const_last = const_table.findAll('div', class_='col-last')[1:]
                    
                    const_first = [target.get_text() for target in const_first]
                    const_name = [target.get_text() for target in const_name]
                    const_last = [re.sub('\n', ' ', target.get_text()) for target in const_last]
                    
                    const_target = driver.find_element_by_id('constructor.summary').find_elements_by_class_name('summary-table.three-column-summary')[0].find_elements_by_class_name('col-constructor-name')
                    
                    const_df = pd.DataFrame([const_first, const_name, const_last, const_target]).T
                    const = ['생성자', const_df]
                    
                    count += 1
                    const_sel = count
                    select_lists.append([count, const])  
            else:
                const_cols = 2
                const_name = const_table.findAll('div', class_='col-constructor-name')
                const_last = const_table.findAll('div', class_='col-last')[1:]

                const_name = [target.get_text() for target in const_name]
                const_last = [re.sub('\n', ' ', target.get_text()) for target in const_last]

                const_target = driver.find_element_by_id('constructor.summary').find_elements_by_class_name('summary-table.two-column-summary')[0].find_elements_by_class_name('col-constructor-name')
                
                const_df = pd.DataFrame([const_name, const_last, const_target]).T
                const = ['생성자', const_df]

                count += 1
                const_sel = count
                select_lists.append([count, const])
                #print(const)

        # 메서드
        method_raw = soup.find('section', id='method.summary')
        if method_raw != None:
            method_title = method_raw.find('h2').get_text()
            method_table = method_raw.find('div', class_='summary-table three-column-summary')
            
            if method_table != None:
                method_col1 = method_table.findAll('div', class_='col-first')
                method_col2 = method_table.findAll('div', class_='col-second')
                method_col3 = method_table.findAll('div', class_='col-last')

                method_col1 = [target.get_text() for target in method_col1]
                method_col2 = [re.sub('\n', ' ', target.get_text()) for target in method_col2]
                method_col3 = [re.sub('\n', ' ', target.get_text()) for target in method_col3]

                method_target = driver.find_element_by_id('method.summary').find_elements_by_class_name('summary-table.three-column-summary')[0].find_elements_by_class_name('col-second')
                
                method_df = pd.DataFrame([method_col1[1:], method_col2[1:], method_col3[1:], method_target[1:]]).T
                method = ['메서드', method_df]

                #print(method)
                method[1].iloc[0][3].click()
                
                count += 1
                select_lists.append([count, method])
                #print(method)


        count += 1
        select_lists.append([count, ['카카오톡으로 전송']])


        '''
        trans = Translator()
        at = trans.translate(content, src='en', dest='ko')
        if 100 < len(at.text) <= 300:
            summ = summarize(at.text, ratio=0.8)
        elif 300 < len(at.text) <= 700:
            summ = summarize(at.text, ratio=0.5)
        elif 700 < len(at.text):
            summ = summarize(at.text, ratio=0.2)
        else: summ = at.text
        '''

        while True:
            print()
            print(title)
            sub_info = '({} : {} / {} : {})'.format(module[0], module[1], package[0], package[1])
            print(sub_info)
            print()
            print(content)                                                                                     #### 바꿔둠 안됨 번역
            print()
            print('메뉴')
            for count, sel in select_lists:
                print(count, '. ', sel[0], sep='', end='\t')
            sel = int(input('1. 원하시는 메뉴를 선택해주세요. ====> '))
            if const_sel != -1 and sel == const_sel: 
                if const_cols == 2: 
                    res = select_cat(select_lists[sel-1][1], cols=2)
            else:
                res = select_cat(select_lists[sel-1][1])
            
            if sel == count: return [7, title, sub_info, content]                                                      #### content
            elif res[0] == 0: continue
            elif res[0] == 1: return res
            elif res[0] == 2: return res
            

    elif category == '': pass

    
def select_cat(select_list, cols=-1):
    print(select_list)
    count = 0
    if select_list[0] == '구현 클래스' or select_list[0] == '구현한 인터페이스' or select_list[0] == '서브 클래스':
        print('\n', select_list[0])
        for idx, li in enumerate(select_list[1]):
            print((idx+1), ' : ', li[0])
            count = idx+1
        print((count + 1), ' : ', '돌아가기')
        sel = int(input('2. 원하시는 메뉴를 선택해주세요. 1====> '))
        if sel == count + 1: return [0, 0]
        else: return [1, select_list[1][sel-1]]

    elif cols == 2:
        print('\n', select_list[0])
        for idx, li in enumerate(select_list[1]):
            print((idx+1), ' : ', li[0], ' - ', li[1])
            count = idx+1
        print((count + 1), ' : ', '돌아가기')
        sel = int(input('2. 원하시는 메뉴를 선택해주세요. 2====> ')) 
        if sel == count + 1: return [0, 0]
        else: return [2, select_list[1][sel-1]]

    else:
        print('\n', select_list[0])

        for i in range(len(select_list[1])):
            count += 1
            row = select_list[1].iloc[i]
            print((count), ' : ', row[0], row[1], '\n', row[2], '\n')
        
        print((count + 1), ' : ', '돌아가기')
        
        sel = int(input('2. 원하시는 메뉴를 선택해주세요. 3====> ')) 
        
        if sel == count + 1:return [0, 0]               
        else: 
            ################
            ################
            '''
            test_url = 'https://docs.oracle.com/en/java/javase/16/docs/api/java.desktop/java/awt/image/ImageObserver.html'                  #필드
            a = select_list[1][1][sel-1]
            u1 = test_url + '#' + a
            driver.get(u1)
            '''

            fd = select_list[1][1][sel-1]                                         # 필드     [1][1][1] 은 ALLBITS
            id = driver.find_element_by_id(fd)                                    # 텍스트 추출 출력
            titles = id.find_element_by_css_selector(".member-signature")
            summm = id.find_element_by_css_selector(".block")
            print("==================출력")
            print(titles.text)
            print(summm.text)
            print("==================출력")
            
            ################
            ################









            #return [2, select_list[1].iloc[sel-1]]
            return [0, 2]







# 메인 로직
kakaoTalk = False
driver_path = './resource/WebDriver/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(driver_path)
#test_url = 'https://docs.oracle.com/en/java/javase/16/docs/api/java.desktop/java/awt/Frame.html'
test_url = 'https://docs.oracle.com/en/java/javase/16/docs/api/java.desktop/java/awt/image/ImageObserver.html'
driver.get(test_url)
time.sleep(4)

kill_iframe(driver)
result = ''
while True:
    result = main_process(driver)
    if result[0] == 1:
        result[1][1].send_keys(Keys.ENTER)
    elif result[0] == 2: # 필드, 메서드, 생성자
        print(result[1][3])
        result[1][3].click()
        result[1][3].click()
        break
    elif result[0] == 7:
        kakaoTalk = True
        break
if kakaoTalk == True:
    print()
    print(result[1])
    print()
    print(result[2])
    print()
    print(result[3])
    print()
    print('='*30, 'The End', '='*30)