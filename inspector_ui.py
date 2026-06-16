import os
import shutil

import PySimpleGUI as sg
import cv2
import numpy as np

# 외부 모듈 임포트
from communication_settings import create_communication_settings_window
from stack_settings import create_stack_settings_window
from inspection_items import create_inspection_items_window

# UI 기본 설정
sg.theme('DarkBlue3')

RESOLUTION_OPTIONS = [
    ('640x480', 640, 480),
    ('800x600', 800, 600),
    ('1024x768', 1024, 768),
    ('1280x720', 1280, 720)
]
DEFAULT_RESOLUTION = (800, 600)

STATUS_COLOR = {
    'READY': 'grey',
    'RUNNING': 'yellow',
    'GOOD': 'green',
    'BAD': 'red',
    'ERROR': 'orange'
}


def create_blank_image(width=800, height=600, color=(30, 30, 30)):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = color
    return image


def resize_to_fit(img, max_size):
    max_w, max_h = max_size
    h, w = img.shape[:2]
    if w == 0 or h == 0:
        return create_blank_image(max_w, max_h, color=(10, 10, 10))
    scale = min(max_w / w, max_h / h)
    new_w = max(1, int(w * scale))
    new_h = max(1, int(h * scale))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    canvas = create_blank_image(max_w, max_h, color=(10, 10, 10))
    x_off = (max_w - new_w) // 2
    y_off = (max_h - new_h) // 2
    canvas[y_off:y_off+new_h, x_off:x_off+new_w] = resized
    return canvas


def convert_to_bytes(img, size=None, keep_ratio=True):
    if size is not None:
        if keep_ratio:
            img = resize_to_fit(img, size)
        else:
            img = cv2.resize(img, size)
    _, buffer = cv2.imencode('.png', img)
    return buffer.tobytes()


def get_spec_master_path(spec_index):
    return os.path.join(os.path.dirname(__file__), f'master_spec{spec_index+1}.png')


def load_master_bytes(spec_index=0, size=DEFAULT_RESOLUTION):
    path = get_spec_master_path(spec_index)
    if os.path.exists(path):
        img = cv2.imread(path)
        if img is not None:
            return convert_to_bytes(img, size=size, keep_ratio=True)
    return convert_to_bytes(create_blank_image(size[0], size[1], color=(10, 10, 40)), size=size, keep_ratio=False)


def save_master_image_file(src_path, spec_index):
    dest = get_spec_master_path(spec_index)
    try:
        if os.path.exists(src_path):
            shutil.copyfile(src_path, dest)
            return True
    except Exception:
        pass
    return False


def save_last_capture_image(img_bytes, filename='last_capture.png'):
    """Save last captured frame bytes to disk for inspection tools to use."""
    try:
        path = os.path.join(os.path.dirname(__file__), filename)
        with open(path, 'wb') as f:
            f.write(img_bytes)
    except Exception:
        pass


def load_logo_bytes(filename='logo.png', width=None, height=None):
    logo_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(logo_path):
        logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
        if logo is not None:
            if width is not None and height is not None:
                logo = cv2.resize(logo, (width, height), interpolation=cv2.INTER_AREA)
            return convert_to_bytes(logo)
    w = width if width is not None else 120
    h = height if height is not None else 60
    return convert_to_bytes(create_blank_image(w, h, color=(20, 20, 40)), size=(w, h), keep_ratio=False)


def ensure_logo_file(filename='logo.png', text='일흥', width=240, height=120):
    """프로젝트에 로고 파일이 없으면 간단한 텍스트 로고를 생성하여 저장합니다."""
    logo_path = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(logo_path):
        return
    try:
        img = create_blank_image(width, height, color=(255, 255, 255))
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = max(0.8, min(width / 200.0, height / 60.0)) * 2.0
        thickness = 3
        text_size, _ = cv2.getTextSize(text, font, scale, thickness)
        text_x = max(10, (width - text_size[0]) // 2)
        text_y = (height + text_size[1]) // 2
        cv2.putText(img, text, (text_x, text_y), font, scale, (0, 48, 128), thickness, cv2.LINE_AA)
        cv2.imwrite(logo_path, img)
    except Exception:
        pass


# 화면 구성
ensure_logo_file('logo.png', text='IL HEUNG', width=240, height=120)
logo_image = load_logo_bytes('logo.png')

header = [
    [sg.Image(data=logo_image, key='-LOGO-', background_color='#222222', pad=((10, 10), (10, 10))),
     sg.Text('일흥 비전 검사', font=('Helvetica', 20, 'bold'), text_color='white', pad=((10, 20), (15, 10))),
     sg.Text('모드: 자동', font=('Helvetica', 12), text_color='lightgreen', pad=((20, 0), (15, 10))),
     sg.Text('상태:', font=('Helvetica', 12), text_color='white', pad=((20, 0), (15, 10))),
     sg.Text('준비', key='-STATUS-', font=('Helvetica', 12, 'bold'), background_color=STATUS_COLOR['READY'], pad=((5, 10), (15, 10)), size=(10, 1))],
    [sg.Text('스펙:', font=('Helvetica', 12), text_color='white', pad=((20, 0), (0, 10))),
     sg.Combo([f'Spec {i}' for i in range(1, 11)], default_value='Spec 1', key='-SPEC-', size=(12, 1)),
     sg.Button('스펙 불러오기', key='-LOAD_SPEC-'), sg.Button('스펙 저장', key='-SAVE_SPEC-'),
     sg.Text('해상도:', font=('Helvetica', 12), text_color='white', pad=((20, 0), (0, 10))),
     sg.Combo([opt[0] for opt in RESOLUTION_OPTIONS], default_value='800x600', key='-RESOLUTION-', size=(12, 1)),
     sg.Button('실시간 보기', key='-LIVE_POPUP-')]
]

# 중앙 패널: 마스터 이미지와 촬영 이미지를 동일 크기로 가운데 배치
reference_panel = [
    [sg.Text('', size=(1,1))],
    [sg.Column([[sg.Text('기준', font=('Helvetica',12), text_color='white')],[sg.Image(key='-MASTER-', size=DEFAULT_RESOLUTION, background_color='black')]], element_justification='center', pad=(20,20)),
     sg.Column([[sg.Text('촬영', font=('Helvetica',12), text_color='white')],[sg.Image(key='-CAPTURE-', size=DEFAULT_RESOLUTION, background_color='black')]], element_justification='center', pad=(20,20))]
]

control_panel = [
    [sg.Text('운전', font=('Helvetica', 14, 'bold'), text_color='white')],
    [sg.Button('시작', size=(12, 2), key='-START-', button_color=('white', '#2E8B57'))],
    [sg.Button('정지', size=(12, 2), key='-STOP-', button_color=('white', '#B22222'))],
    [sg.Button('리셋', size=(12, 2), key='-RESET-', button_color=('white', '#1E90FF'))],
    [sg.Text('')],
    [sg.Button('촬영(웹캠)', key='-CAPTURE_CAM-'), sg.Button('불러오기(파일)', key='-CAPTURE_FILE-')],
    [sg.Text('')],
    [sg.Frame('결과 요약', [[
        [sg.Text('총수', size=(8, 1)), sg.Text('0', key='-TOTAL-', size=(6, 1), text_color='white', background_color='#333333')],
        [sg.Text('양품', size=(8, 1)), sg.Text('0', key='-GOOD-', size=(6, 1), text_color='white', background_color='#2E8B57')],
        [sg.Text('불량', size=(8, 1)), sg.Text('0', key='-BAD-', size=(6, 1), text_color='white', background_color='#B22222')]
    ]], pad=((0, 0), (10, 10)))],
    [sg.Frame('램프 상태', [[
        [sg.Text('GOOD', size=(8, 1)), sg.Text('OFF', key='-GOODLAMP-', size=(8, 1), background_color='grey', text_color='white')],
        [sg.Text('BAD', size=(8, 1)), sg.Text('OFF', key='-BADLAMP-', size=(8, 1), background_color='grey', text_color='white')]
    ]], pad=((0, 0), (10, 10)))],
    [sg.Frame('카메라 / PLC', [[
        [sg.Text('카메라', size=(9, 1)), sg.Text('연결 안 됨', key='-CAMINFO-', size=(18, 1), background_color='#222222', text_color='white')],
        [sg.Text('PLC', size=(9, 1)), sg.Text('연결 안 됨', key='-PLCINFO-', size=(18, 1), background_color='#222222', text_color='white')],
        [sg.Text('마지막 촬영', size=(9, 1)), sg.Text('-', key='-LASTSHOT-', size=(18, 1), background_color='#222222', text_color='white')]
    ]], pad=((0, 0), (10, 10)))],
    [sg.Text('')],
    [sg.Button('통신 설정', key='-COMM-', size=(18, 1)), sg.Button('스택 설정', key='-STACK-', size=(18, 1))],
    [sg.Button('검사설정', key='-ITEMS-', size=(18, 1)), sg.Button('해상도 적용', key='-APPLY_RES-', size=(18,1))]
]

log_panel = [
    [sg.Text('검사 로그', font=('Helvetica', 14, 'bold'), text_color='white')],
    [sg.Multiline('', size=(110, 14), key='-RESULTS-', autoscroll=True, disabled=True, background_color='#111111', text_color='white')]
]

layout = [
    [sg.Column(header, element_justification='left', pad=(0, 0))],
    [
        sg.Column([[sg.Column(reference_panel, element_justification='center', pad=(0, 0))]], element_justification='center', pad=(0, 0)),
        sg.VSeparator(color='white'),
        sg.Column(control_panel, element_justification='center', pad=(10, 10), vertical_alignment='top')
    ],
    [sg.HSeparator(color='white')],
    [
        sg.Column(log_panel, pad=(10, 10))
    ]
]

def main():
    window = sg.Window('일흥 비전 검사기', layout, finalize=True, resizable=True, background_color='#222222', size=(1320, 980))

    current_size = DEFAULT_RESOLUTION
    spec_index = 0

    # 초기 이미지 표시
    window['-MASTER-'].update(data=load_master_bytes(spec_index, size=current_size))
    window['-CAPTURE-'].update(data=convert_to_bytes(create_blank_image(current_size[0], current_size[1], color=(10, 10, 10)), size=current_size, keep_ratio=False))

    running = False
    counts = {'total': 0, 'good': 0, 'bad': 0}
    last_shot = '-'

    try:
        while True:
            event, values = window.read(timeout=100)
            if event == sg.WIN_CLOSED:
                break

            if event == '-COMM-':
                comm_window = create_communication_settings_window()
                while True:
                    ce, cv = comm_window.read()
                    if ce == sg.WIN_CLOSED or ce == '-CLOSE-':
                        break
                comm_window.close()

            elif event == '-STACK-':
                stack_window = create_stack_settings_window()
                while True:
                    se, sv = stack_window.read()
                    if se == sg.WIN_CLOSED or se == '-CLOSE-':
                        break
                stack_window.close()

            elif event == '-ITEMS-':
                # pass currently selected spec index to the inspection settings window
                spec_val = values.get('-SPEC-', 'Spec 1')
                try:
                    spec_index = int(spec_val.split()[-1]) - 1
                except Exception:
                    spec_index = 0
                items_window = create_inspection_items_window(spec_index=spec_index)
                while True:
                    ie, iv = items_window.read()
                    if ie == sg.WIN_CLOSED or ie == '-CLOSE-':
                        break
                items_window.close()

            elif event == '-LOAD_SPEC-':
                # simply update combo text (inspector will pass index when opening settings)
                sg.popup_ok('스펙을 선택한 후 검사설정에서 불러오기하세요.', title='정보')

            elif event == '-SAVE_SPEC-':
                sg.popup_ok('현재 스펙 저장은 검사설정 창에서 가능합니다.', title='정보')

            elif event == '-CAPTURE_FILE-':
                # open file dialog
                file = sg.popup_get_file('이미지 파일을 선택하세요', file_types=(('Image Files', '*.png;*.jpg;*.jpeg;*.bmp'),), no_window=True)
                if file:
                    try:
                        img = cv2.imread(file)
                        if img is not None:
                            b = convert_to_bytes(img, size=current_size, keep_ratio=True)
                            window['-CAPTURE-'].update(data=b)
                            save_last_capture_image(b)
                            sg.popup_ok('이미지 불러오기 및 저장 완료', title='정보')
                        else:
                            sg.popup_error('이미지를 읽을 수 없습니다.', title='오류')
                    except Exception as e:
                        sg.popup_error('오류: ' + str(e), title='오류')

            elif event == '-CAPTURE_CAM-':
                # try capture from default webcam
                try:
                    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    if not cap.isOpened():
                        cap = cv2.VideoCapture(0)
                    ret, frame = cap.read()
                    cap.release()
                    if ret and frame is not None:
                        b = convert_to_bytes(frame, size=current_size, keep_ratio=True)
                        window['-CAPTURE-'].update(data=b)
                        save_last_capture_image(b)
                        sg.popup_ok('웹캠에서 이미지 캡처 및 저장 완료', title='정보')
                    else:
                        sg.popup_error('웹캠에서 이미지를 가져올 수 없습니다.', title='오류')
                except Exception as e:
                    sg.popup_error('웹캠 캡처 중 오류: ' + str(e), title='오류')

            elif event == '-LIVE_POPUP-':
                # Open a separate live view popup
                try:
                    live_layout = [[sg.Image(key='-LIVE_IMG-', size=current_size, background_color='black')], [sg.Button('캡처', key='-LIVE_CAPTURE-'), sg.Button('종료', key='-LIVE_CLOSE-')]]
                    live_win = sg.Window('실시간 보기', live_layout, finalize=True, modal=False, resizable=True)
                    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                    if not cap.isOpened():
                        cap = cv2.VideoCapture(0)
                    while True:
                        l_event, _ = live_win.read(timeout=20)
                        ret, frame = cap.read()
                        if not ret or frame is None:
                            frame = create_blank_image(current_size[0], current_size[1], color=(10, 10, 10))
                        img_b = convert_to_bytes(frame, size=current_size, keep_ratio=True)
                        live_win['-LIVE_IMG-'].update(data=img_b)

                        if l_event == sg.WIN_CLOSED or l_event == '-LIVE_CLOSE-':
                            break
                        if l_event == '-LIVE_CAPTURE-':
                            window['-CAPTURE-'].update(data=img_b)
                            save_last_capture_image(img_b)
                            sg.popup_ok('실시간에서 캡처하여 저장했습니다.', title='완료')
                    cap.release()
                    live_win.close()
                except Exception as e:
                    sg.popup_error('실시간 팝업 오류: ' + str(e), title='오류')

            elif event == '-APPLY_RES-':
                sel = values.get('-RESOLUTION-', '800x600')
                for label, w, h in RESOLUTION_OPTIONS:
                    if label == sel:
                        current_size = (w, h)
                        window['-MASTER-'].update(size=current_size)
                        window['-CAPTURE-'].update(size=current_size)
                        window['-MASTER-'].update(data=load_master_bytes(spec_index, size=current_size))
                        window['-CAPTURE-'].update(data=convert_to_bytes(create_blank_image(w, h, color=(10, 10, 10)), size=current_size, keep_ratio=False))
                        break

            elif event == '-DATA-':
                window['-RESULTS-'].print('데이터 관리 기능은 아직 구현되지 않았습니다.')

            elif event == '-START-':
                running = True
                window['-STATUS-'].update('실행중', background_color=STATUS_COLOR['RUNNING'])
                window['-RESULTS-'].update('검사를 시작합니다...\n', append=False)

            elif event == '-STOP-':
                running = False
                window['-STATUS-'].update('준비', background_color=STATUS_COLOR['READY'])
                window['-RESULTS-'].print('검사가 중지되었습니다.')

            elif event == '-RESET-':
                running = False
                counts = {'total': 0, 'good': 0, 'bad': 0}
                last_shot = '-'
                window['-TOTAL-'].update('0')
                window['-GOOD-'].update('0')
                window['-BAD-'].update('0')
                window['-STATUS-'].update('준비', background_color=STATUS_COLOR['READY'])
                window['-GOODLAMP-'].update('OFF', background_color='grey')
                window['-BADLAMP-'].update('OFF', background_color='grey')
                window['-LASTSHOT-'].update(last_shot)
                window['-RESULTS-'].update('시스템이 초기화되었습니다.\n')

            if running:
                frame = create_blank_image(current_size[0], current_size[1], color=(20, 80, 20))
                b = convert_to_bytes(frame, size=current_size, keep_ratio=False)
                window['-CAPTURE-'].update(data=b)
                # save last capture for spec tools
                save_last_capture_image(b)

            window['-TOTAL-'].update(str(counts['total']))
            window['-GOOD-'].update(str(counts['good']))
            window['-BAD-'].update(str(counts['bad']))
            window['-LASTSHOT-'].update(last_shot)

    except Exception:
        import traceback
        traceback.print_exc()
        sg.popup_error('예기치 않은 오류가 발생했습니다. 콘솔 로그를 확인하세요.', title='오류')
    finally:
        window.close()


if __name__ == '__main__':
    main()
