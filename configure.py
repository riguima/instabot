from pathlib import Path
import toml
import shutil

from instabot.browser import Browser

secrets = (
    toml.load(open('.secrets.toml', 'r')) if Path('.secrets.toml').exists() else {}
)


if __name__ == '__main__':
    change_account = secrets.get('login') and input('Deseja alterar a conta? [s/n] ')[0].lower() == 's'
    secrets['login'] = secrets.get('login')
    if secrets['login'] is None or change_account:
        if secrets['login']:
            shutil.rmtree(secrets['login'] + '_user_data', ignore_errors=True)
        secrets['login'] = input('Login: ').split('@')[0]
    secrets['password'] = secrets.get('password')
    if secrets['password'] is None or change_account:
        secrets['password'] = input('Senha: ').split('@')[0]
    browser = Browser(secrets['login'] + '_user_data')
    if not browser.is_logged():
        browser.make_login(secrets['login'], secrets['password'])
    browser.driver.quit()
    toml.dump(secrets, open('.secrets.toml', 'w'))
