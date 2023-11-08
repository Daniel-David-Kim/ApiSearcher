import re
import googletrans

def fd(driver):
    
    b = driver.current_url
    b = re.sub("%3C", "<", b)
    b = re.sub("%3E", ">", b)
    # print(b)    
    a = re.split("#",b)

    id = driver.find_element_by_id(a[1])
    titles = id.find_element_by_class_name("member-signature")
    try:
        summm = id.find_element_by_class_name("deprecation-block")
    except:
        summm = id.find_element_by_class_name("block")
    try:
        note = id.find_element_by_class_name("notes")
        # note1 = driver.find_element_by_xpath('//*[@id="removeChangeListener(javax.swing.event.ChangeListener)"]/dl/dd[2]')
        
    except:
        note = ''

    translator = googletrans.Translator()   # 번역기
    summm = str(summm.text)
    result2 = translator.translate(summm, dest='ko')
    # note = str(note.text)
    # result3 = translator.translate(note, dest='ko')

    retu = titles.text + "\n" + f"{result2.text}" + "\n" + (note.text if note != '' else '')           # 문자열 데이터
    print(retu)
    
    respon = input("돌아가기 0, 카카오톡 7 : ")
    if respon == '0':                                     
        return [0, 0]
    elif respon == '7':
        return [7, retu]
