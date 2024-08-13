import unittest
import page
from selenium import webdriver
from urllib import request 

class VisualNovelDatabaseSearch(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:/SeleniumDownloads'}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://vndb.org/")

    def test_search_in_vndb(self):


        main_page = page.MainPage(self.driver)
        assert main_page.is_title_matches()
        # main_page.search_and_go('summer pockets')
        # main_page.search_and_go('HOOKSOFT')
        # main_page.search_and_go('密语')
        main_page.search_and_go('あまいろショコラータ')

        browse_page = page.BrowsePage(self.driver)
        visual_novels_list = browse_page.get_visual_novels_list()

        for visual_novel in visual_novels_list:
            try:
                visual_novel.click()
                visual_novel_page = page.VisualNovelPage(self.driver)
                img_url = visual_novel_page.get_visual_novel_img_url()
                request.urlretrieve(img_url, "./img/" + img_url.split('/')[-1])
                visual_novel_page.back()
            except Exception as e:
                print(e)
                continue

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()