import re, urllib, urllib2, os
from pydub import AudioSegment
from selenium import webdriver


def get_audio_urls(url):
    obj = urllib2.urlopen(url).read()

    pat = re.compile(r'http.*?mp3')
    urls = pat.findall(obj, re.I)
    urls = map(lambda x: x.replace('\\', ''), urls)
    return urls

def get_starred_audio_urls(url):
    browser = webdriver.Firefox()
    browser.set_window_size(1920, 1080)
    browser.get(url)

    # Login quizlet
    try:
        browser.find_element_by_id("show-login").click()
        username = browser.find_element_by_id("username1")
        password = browser.find_element_by_id("password1")
        username.send_keys("wnfrdshao")
        password.send_keys("Ws20100915")
        browser.find_element_by_css_selector(".submit.button").click()
    except Exception:
        browser.close()
        return []

    page_source = browser.page_source
    browser.close()
    pat = re.compile(r'<div.+?\sselected\s.+?>')
    urls = pat.findall(page_source, re.I)

    pat = re.compile(r'.*data-id="(\d+)".*')
    audio_urls = []
    for elem in urls:
        m = pat.match(elem)
        if not m: continue
        id = str(m.group(1))
        p = re.compile(r'"id":'+id+'.*?(http.*?mp3)')
        audio_urls.append(p.findall(page_source, re.I)[0])

    audio_urls = map(lambda x: x.replace('\\', ''), audio_urls)
    return audio_urls

def generate_combined_audio(urls):
    main_audio = AudioSegment.empty()
    silence = AudioSegment.silent(duration=1000)
    tmp_path = os.path.join("/tmp", "tempsong.mp3")
    target_path = os.path.join("/tmp", "Combined.mp3")

    for url in urls:
        urllib.urlretrieve(url, tmp_path)
        song = AudioSegment.from_mp3(tmp_path)
        main_audio = main_audio + silence + song

    main_audio.export(target_path, format="mp3")
    os.remove(tmp_path)
    return target_path
