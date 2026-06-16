import PySimpleGUI as sg

sg.theme('DarkBlue3')

def create_stack_settings_window():
    """스택 설정 창"""
    
    layout = [
        [sg.Text('Stack Settings', font=('Helvetica', 14, 'bold'))],
        [sg.Text('')],
        
        # Stack Mode
        [sg.Frame('Stack Mode Configuration', [
            [sg.Radio('Single Image Mode', 'stack_mode', default=True, key='-SINGLE_MODE-'),
             sg.Text('(Process one image at a time)')],
            [sg.Radio('Batch Mode', 'stack_mode', key='-BATCH_MODE-'),
             sg.Text('(Process multiple images)'),
             sg.Text('Batch Size:', size=(10, 1)), 
             sg.InputText(default_text='10', key='-BATCH_SIZE-', size=(10, 1))],
            [sg.Radio('Queue Mode', 'stack_mode', key='-QUEUE_MODE-'),
             sg.Text('(Continuous processing)')]
        ])],
        
        [sg.Text('')],
        
        # Image Storage Settings
        [sg.Frame('Image Storage Settings', [
            [sg.Text('Storage Folder:', size=(15, 1)), 
             sg.InputText(default_text='C:\\inspector_images', key='-STORAGE_PATH-', size=(35, 1)),
             sg.FolderBrowse('Browse')],
            [sg.Checkbox('Compress Images (JPG)', default=True, key='-COMPRESS-'),
             sg.Text('Quality (0-100):', size=(12, 1)), 
             sg.InputText(default_text='85', key='-JPG_QUALITY-', size=(8, 1))],
            [sg.Checkbox('Save Master Images', default=True, key='-SAVE_MASTER-')],
            [sg.Checkbox('Save Captured Images', default=True, key='-SAVE_CAPTURE-')],
            [sg.Checkbox('Save Defect Images Only', default=False, key='-SAVE_DEFECT_ONLY-')],
            [sg.Text('Max Storage Size (GB):', size=(18, 1)), 
             sg.InputText(default_text='100', key='-MAX_STORAGE-', size=(8, 1))],
        ])],
        
        [sg.Text('')],
        
        # Data Retention
        [sg.Frame('Data Retention & Cleanup', [
            [sg.Checkbox('Auto Delete Old Images After (Days):', default=False, key='-AUTO_DELETE-'),
             sg.InputText(default_text='30', key='-DELETE_DAYS-', size=(8, 1))],
            [sg.Checkbox('Archive Old Data', default=True, key='-ARCHIVE-'),
             sg.Text('Archive Path:', size=(12, 1)), 
             sg.InputText(default_text='C:\\inspector_archive', key='-ARCHIVE_PATH-', size=(30, 1))],
        ])],
        
        [sg.Text('')],
        
        # CSV Logging
        [sg.Frame('CSV Logging Settings', [
            [sg.Checkbox('Enable CSV Logging', default=True, key='-ENABLE_CSV-')],
            [sg.Text('Log File Path:', size=(15, 1)), 
             sg.InputText(default_text='C:\\logs', key='-LOG_PATH-', size=(35, 1)),
             sg.FolderBrowse('Browse')],
            [sg.Text('Fields to Log:')],
            [sg.Checkbox('Timestamp', default=True, key='-LOG_TIMESTAMP-'),
             sg.Checkbox('Image Filename', default=True, key='-LOG_FILENAME-'),
             sg.Checkbox('Result (Good/Bad)', default=True, key='-LOG_RESULT-')],
            [sg.Checkbox('Defect Type', default=True, key='-LOG_DEFECT-'),
             sg.Checkbox('Confidence Score', default=True, key='-LOG_CONFIDENCE-'),
             sg.Checkbox('Processing Time', default=True, key='-LOG_TIME-')],
            [sg.Checkbox('Camera ID', default=True, key='-LOG_CAM_ID-'),
             sg.Checkbox('PLC Status', default=True, key='-LOG_PLC-')],
        ])],
        
        [sg.Text('')],
        
        # Buttons
        [sg.Button('Save Settings', key='-SAVE-'), 
         sg.Button('Load Default', key='-DEFAULT-'),
         sg.Button('Clean Old Data', key='-CLEAN-'),
         sg.Button('Close', key='-CLOSE-')]
    ]
    
    window = sg.Window('Stack Settings', layout, finalize=True, modal=True, size=(700, 800), resizable=True)
    
    return window


def stack_settings_loop():
    """스택 설정 화면 루프"""
    window = create_stack_settings_window()
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == '-CLOSE-':
            break
        
        elif event == '-SINGLE_MODE-':
            window['-BATCH_SIZE-'].update(disabled=True)
        
        elif event == '-BATCH_MODE-':
            window['-BATCH_SIZE-'].update(disabled=False)
        
        elif event == '-QUEUE_MODE-':
            window['-BATCH_SIZE-'].update(disabled=True)
        
        elif event == '-SAVE-':
            sg.popup_ok('Stack settings saved successfully!', title='Success')
            # TODO: 설정을 파일에 저장
        
        elif event == '-DEFAULT-':
            window['-STORAGE_PATH-'].update('C:\\inspector_images')
            window['-COMPRESS-'].update(True)
            window['-JPG_QUALITY-'].update('85')
            window['-MAX_STORAGE-'].update('100')
            window['-LOG_PATH-'].update('C:\\logs')
            sg.popup_ok('Default settings loaded.', title='Info')
        
        elif event == '-CLEAN-':
            result = sg.popup_yes_no('Delete old data according to retention settings?', 
                                     title='Confirm')
            if result == 'Yes':
                sg.popup_ok('Old data cleaned successfully!', title='Success')
                # TODO: 실제 데이터 정리 로직
    
    window.close()


if __name__ == '__main__':
    stack_settings_loop()
