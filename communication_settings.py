import PySimpleGUI as sg

sg.theme('DarkBlue3')

def create_communication_settings_window():
    """통신설정 창"""
    
    layout = [
        [sg.Text('Communication Settings', font=('Helvetica', 14, 'bold'))],
        [sg.Text('')],
        
        # PLC Settings
        [sg.Frame('PLC (XGB) Ethernet Settings', [
            [sg.Text('PLC IP Address:', size=(18, 1)), 
             sg.InputText(default_text='192.168.0.1', key='-PLC_IP-', size=(20, 1))],
            [sg.Text('PLC Port:', size=(18, 1)), 
             sg.InputText(default_text='502', key='-PLC_PORT-', size=(20, 1))],
            [sg.Text('Protocol:', size=(18, 1)), 
             sg.Combo(['Modbus/TCP', 'FINS/TCP', 'EtherNet/IP'], default_value='Modbus/TCP', 
                     key='-PLC_PROTOCOL-', size=(18, 1), readonly=True)],
            [sg.Text('Connection Timeout (sec):', size=(18, 1)), 
             sg.InputText(default_text='5', key='-PLC_TIMEOUT-', size=(20, 1))],
            [sg.Button('Test PLC Connection', key='-TEST_PLC-'), 
             sg.Text('', key='-PLC_STATUS-', text_color='gray')]
        ])],
        
        [sg.Text('')],
        
        # Camera Settings
        [sg.Frame('Omron Camera Settings', [
            [sg.Text('Camera IP Address:', size=(18, 1)), 
             sg.InputText(default_text='192.168.0.10', key='-CAM_IP-', size=(20, 1))],
            [sg.Text('Camera Port:', size=(18, 1)), 
             sg.InputText(default_text='5000', key='-CAM_PORT-', size=(20, 1))],
            [sg.Text('Camera Model:', size=(18, 1)), 
             sg.Combo(['MX-U1000', 'MX-U1010', 'MX-U2000', 'Custom'], 
                     default_value='MX-U1000', key='-CAM_MODEL-', size=(18, 1), readonly=True)],
            [sg.Text('Trigger Mode:', size=(18, 1)), 
             sg.Combo(['Software', 'Hardware', 'Auto'], default_value='Software', 
                     key='-CAM_TRIGGER-', size=(18, 1), readonly=True)],
            [sg.Text('Image Resolution:', size=(18, 1)), 
             sg.Combo(['640x480', '1024x768', '2048x1536'], default_value='640x480', 
                     key='-CAM_RESOLUTION-', size=(18, 1), readonly=True)],
            [sg.Button('Test Camera Connection', key='-TEST_CAM-'), 
             sg.Text('', key='-CAM_STATUS-', text_color='gray')]
        ])],
        
        [sg.Text('')],
        
        # I/O Mapping
        [sg.Frame('PLC I/O Mapping', [
            [sg.Text('Start Button Input Address:', size=(18, 1)), 
             sg.InputText(default_text='X0', key='-START_ADDR-', size=(20, 1))],
            [sg.Text('Stop Button Input Address:', size=(18, 1)), 
             sg.InputText(default_text='X1', key='-STOP_ADDR-', size=(20, 1))],
            [sg.Text('Reset Button Input Address:', size=(18, 1)), 
             sg.InputText(default_text='X2', key='-RESET_ADDR-', size=(20, 1))],
            [sg.Text('Good Output Address:', size=(18, 1)), 
             sg.InputText(default_text='Y0', key='-GOOD_OUT_ADDR-', size=(20, 1))],
            [sg.Text('Bad Output Address:', size=(18, 1)), 
             sg.InputText(default_text='Y1', key='-BAD_OUT_ADDR-', size=(20, 1))],
            [sg.Text('Result Register Address:', size=(18, 1)), 
             sg.InputText(default_text='D100', key='-RESULT_REG-', size=(20, 1))],
        ])],
        
        [sg.Text('')],
        
        # Buttons
        [sg.Button('Save Settings', key='-SAVE-'), 
         sg.Button('Load Default', key='-DEFAULT-'),
         sg.Button('Close', key='-CLOSE-')]
    ]
    
    window = sg.Window('Communication Settings', layout, finalize=True, modal=True)
    
    return window


def communication_settings_loop():
    """통신설정 화면 루프"""
    window = create_communication_settings_window()
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == '-CLOSE-':
            break
        
        elif event == '-TEST_PLC-':
            # PLC 연결 테스트 (더미)
            plc_ip = values['-PLC_IP-']
            plc_port = values['-PLC_PORT-']
            window['-PLC_STATUS-'].update('Testing...', text_color='yellow')
            # TODO: 실제 연결 테스트 로직
            window['-PLC_STATUS-'].update('✓ Connected', text_color='green')
        
        elif event == '-TEST_CAM-':
            # 카메라 연결 테스트 (더미)
            cam_ip = values['-CAM_IP-']
            cam_port = values['-CAM_PORT-']
            window['-CAM_STATUS-'].update('Testing...', text_color='yellow')
            # TODO: 실제 연결 테스트 로직
            window['-CAM_STATUS-'].update('✓ Connected', text_color='green')
        
        elif event == '-SAVE-':
            sg.popup_ok('Settings saved successfully!', title='Success')
            # TODO: 설정을 파일에 저장
        
        elif event == '-DEFAULT-':
            # 기본값으로 복원
            window['-PLC_IP-'].update('192.168.0.1')
            window['-PLC_PORT-'].update('502')
            window['-CAM_IP-'].update('192.168.0.10')
            window['-CAM_PORT-'].update('5000')
            sg.popup_ok('Default settings loaded.', title='Info')
    
    window.close()


if __name__ == '__main__':
    communication_settings_loop()
