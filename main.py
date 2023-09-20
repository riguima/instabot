import PySimpleGUI as sg
from pathlib import Path
import toml

from instabot.browser import Browser

sg.theme('Reddit')

secrets = toml.load(open('.secrets.toml')) if Path('.secrets.toml').exists() else {}
FONT = ('Arial', 18)
files = []


def show_login_window() -> None:
    layout = [
        [sg.Text('Login'), sg.In(key='login', do_not_clear=False)],
        [sg.Text('Senha'), sg.In(key='password', do_not_clear=False)],
        [sg.Button('Salvar')],
    ]
    window = sg.Window(
        'Login',
        layout,
        modal=True,
        font=FONT,
        element_justification='c',
        size=(400, 130),
    )
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Salvar':
            secrets['login'] = values['login']
            secrets['password'] = values['password']
            sg.popup('Aguarde o login ser realizado', font=FONT)
            browser = Browser(secrets['login'] + '_user_data', headless=False)
            if not browser.is_logged():
                browser.make_login(secrets['login'], secrets['password'])
            browser.driver.quit()
            toml.dump(secrets, open('.secrets.toml', 'w'))
            sg.popup('Salvo', font=FONT)
    window.close()



if __name__ == '__main__':
    layout = [
        [
            sg.Text('Menções separadas por espaço:'),
            sg.In(key='mentions'),
        ],
        [sg.Button('Selecionar imagens/videos')],
        [sg.Button('Login'), sg.Button('Rodar')],
    ]
    window = sg.Window(
        'Instabot',
        layout,
        font=FONT,
        element_justification='c',
        size=(600, 150),
    )
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == 'Rodar' and secrets.get('login'):
            browser = Browser(secrets['login'] + '_user_data', headless=False)
            if not browser.is_logged():
                browser.make_login(secrets['login'], secrets['password'])
            browser.driver.get('chrome-extension://bcocdbombenodlegijagbhdjbifpiijp/inssist.html')
            sg.popup('Aperte em Ok quando carregar a página', font=('Aria', 18))
            for file in files:
                browser.post_story(
                    file,
                    values['mentions'].replace('@', '').split(),
                )
        elif event == 'Rodar' and secrets.get('login') is None:
            sg.popup('Primeiro configure o login', font=FONT)
        elif event == 'Login':
            show_login_window()
        elif event == 'Selecionar imagens/videos':
            files = sg.popup_get_file(
                'Selecionar', multiple_files=True, font=FONT
            ).split(';')
    window.close()
