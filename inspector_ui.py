import os
import io
from datetime import datetime

import PySimpleGUI as sg
import cv2
import numpy as np

# 외부 모듈 임포트
from communication_settings import create_communication_settings_window
from stack_settings import create_stack_settings_window
from inspection_items import create_inspection_items_window

# UI 기본 설정
sg.theme('DarkBlue3')

STATUS_COLOR = {
    'READY': 'grey',
    'RUNNING': 'yellow',
    'GOOD': 'green',
    'BAD': 'red',
    'ERROR': 'orange'
}


def create_blank_image(width=640, height=480, color=(50, 50, 50)):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = color
    return image


def convert_to_bytes(img, resize=None):
    if resize:
        img = cv2.resize(img, resize)
    _, buffer = cv2.imencode('.png', img)
    return buffer.tobytes()


# 친환경 배치
camera_column = [
    [sg.Text('Camera Feed', size=(22, 1), justification='center')],
    [sg.Image(filename='', key='-CAMERA-', size=(640, 360))],
    [sg.Text('Master Image', size=(22, 1), justification='center')],
    [sg.Image(filename='', key='-MASTER-', size=(320, 240))],
    [sg.Text('Captured Image', size=(22, 1), justification='center')],
    [sg.Image(filename='', key='-CAPTURE-', size=(320, 240))],
]

control_column = [
    [sg.Text('Inspector Control', font=('Helvetica', 14, 'bold'))],
    [sg.Button('Start', size=(10, 1), key='-START-'),
     sg.Button('Stop', size=(10, 1), key='-STOP-'),
     sg.Button('Reset', size=(10, 1), key='-RESET-')],
    [sg.Text('')],
    [sg.Text('Total:', size=(12, 1)), sg.Text('0', key='-TOTAL-')],
    [sg.Text('Good:', size=(12, 1)), sg.Text('0', key='-GOOD-')],
    [sg.Text('Bad:', size=(12, 1)), sg.Text('0', key='-BAD-')],
    [sg.Text('')],
    [sg.Text('Current Status:', size=(12, 1)),
     sg.Text('READY', key='-STATUS-', size=(10, 1), background_color=STATUS_COLOR['READY'])],
    [sg.Text('')],
    [sg.Frame('Lamp Status', [[
        sg.Text('Good Lamp:', size=(12, 1)), sg.Text('OFF', key='-GOODLAMP-', background_color='grey', size=(8, 1)),
        sg.Text('Bad Lamp:', size=(12, 1)), sg.Text('OFF', key='-BADLAMP-', background_color='grey', size=(8, 1))
    ]])],
    [sg.Text('')],
    [sg.Frame('Log Settings', [[
        sg.Text('Log Folder:'), sg.InputText(default_text='logs', key='-LOGFOLDER-', size=(25, 1)),
        sg.FolderBrowse('Browse')
    ]])],
]

result_column = [
    [sg.Text('Data Results', font=('Helvetica', 14, 'bold'))],
    [sg.Multiline('', size=(60, 16), key='-RESULTS-', autoscroll=True, disabled=True)],
    [sg.Text('')],
    [sg.Frame('PLC / Camera Info', [
        [sg.Text('Camera:', size=(12, 1)), sg.Text('Not connected', key='-CAMINFO-')],
        [sg.Text('PLC:', size=(12, 1)), sg.Text('Not connected', key='-PLCINFO-')],
        [sg.Text('Last shot:', size=(12, 1)), sg.Text('-', key='-LASTSHOT-')]
    ])]
]

# 메뉴바
menubar = [
    ['Settings', ['Communication', 'Stack', 'Inspection Items', '---', 'Exit']],
    ['Tools', ['Calibration', 'Test Camera', 'Test PLC', '---', 'Data Management']],
    ['Help', ['About', 'Documentation', 'Support']]
]

layout = [
    [sg.Menu(menubar)],
    [
        sg.Column(camera_column),
        sg.VSeparator(),
        sg.Column(control_column),
        sg.VSeparator(),
        sg.Column(result_column)
    ]
]

window = sg.Window('Vision Inspector UI', layout, finalize=True, resizable=True)

# 초기 이미지 표시
blank = convert_to_bytes(create_blank_image(), resize=(640, 360))
window['-CAMERA-'].update(data=blank)
window['-MASTER-'].update(data=convert_to_bytes(create_blank_image(320, 240, color=(30, 30, 60))))
window['-CAPTURE-'].update(data=convert_to_bytes(create_blank_image(320, 240, color=(40, 40, 40))))

running = False
counts = {'total': 0, 'good': 0, 'bad': 0}
last_shot = '-'

while True:
    event, values = window.read(timeout=100)
    if event == sg.WIN_CLOSED:
        break

    # 메뉴 이벤트
    if event == 'Communication':
        comm_window = create_communication_settings_window()
        while True:
            ce, cv = comm_window.read()
            if ce == sg.WIN_CLOSED or ce == '-CLOSE-':
                break
            # TODO: 통신 설정 이벤트 처리
        comm_window.close()
    
    elif event == 'Stack':
        stack_window = create_stack_settings_window()
        while True:
            se, sv = stack_window.read()
            if se == sg.WIN_CLOSED or se == '-CLOSE-':
                break
            # TODO: 스택 설정 이벤트 처리
        stack_window.close()
    
    elif event == 'Inspection Items':
        items_window = create_inspection_items_window()
        while True:
            ie, iv = items_window.read()
            if ie == sg.WIN_CLOSED or ie == '-CLOSE-':
                break
            # TODO: 검사 항목 설정 이벤트 처리
        items_window.close()
    
    elif event == 'Exit':
        break
    
    # 버튼 이벤트
    if event == '-START-':
        running = True
        window['-STATUS-'].update('RUNNING', background_color=STATUS_COLOR['RUNNING'])
        window['-RESULTS-'].update('Inspection started...\n', append=False)

    if event == '-STOP-':
        running = False
        window['-STATUS-'].update('READY', background_color=STATUS_COLOR['READY'])
        window['-RESULTS-'].print('Inspection stopped.')

    if event == '-RESET-':
        running = False
        counts = {'total': 0, 'good': 0, 'bad': 0}
        last_shot = '-'
        window['-TOTAL-'].update('0')
        window['-GOOD-'].update('0')
        window['-BAD-'].update('0')
        window['-STATUS-'].update('READY', background_color=STATUS_COLOR['READY'])
        window['-GOODLAMP-'].update('OFF', background_color='grey')
        window['-BADLAMP-'].update('OFF', background_color='grey')
        window['-LASTSHOT-'].update(last_shot)
        window['-RESULTS-'].update('System reset.\n')

    if running:
        # TODO: 실제 카메라 스트림 및 검사 로직 연결
        # 현재 더미 프레임을 표시하여 UI 동작 확인
        frame = create_blank_image(640, 360, color=(20, 80, 20))
        window['-CAMERA-'].update(data=convert_to_bytes(frame, resize=(640, 360)))

    # 업데이트 카운트 및 상태
    window['-TOTAL-'].update(str(counts['total']))
    window['-GOOD-'].update(str(counts['good']))
    window['-BAD-'].update(str(counts['bad']))
    window['-LASTSHOT-'].update(last_shot)

window.close()
