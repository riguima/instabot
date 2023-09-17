from instabot.browser import Browser


if __name__ == '__main__':
    browser = Browser('ri.guima', headless=False)
    browser.post_story('/home/riguima/wallpapers/wallpaper.jpg')
    breakpoint()
