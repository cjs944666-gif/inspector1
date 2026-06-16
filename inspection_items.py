import PySimpleGUI as sg

sg.theme('DarkBlue3')

def create_inspection_items_window():
    """검사 항목 설정 창"""
    
    # 10개 항목 탭 생성
    tabs = []
    
    for i in range(1, 11):
        tab_layout = [
            [sg.Text(f'Inspection Item #{i}', font=('Helvetica', 12, 'bold'))],
            [sg.Text('')],
            
            # Item Configuration
            [sg.Frame('Item Configuration', [
                [sg.Text('Item Name:', size=(15, 1)), 
                 sg.InputText(default_text=f'Item {i}', key=f'-ITEM{i}_NAME-', size=(30, 1))],
                [sg.Text('Description:', size=(15, 1)), 
                 sg.InputText(default_text='', key=f'-ITEM{i}_DESC-', size=(30, 1))],
                [sg.Text('Type:', size=(15, 1)), 
                 sg.Combo(['Component Detection', 'Color Check', 'Pin Position', 'Engraving Shape', 'Custom'],
                         default_value='Component Detection', key=f'-ITEM{i}_TYPE-', size=(28, 1), readonly=True)],
                [sg.Text('Enabled:', size=(15, 1)), 
                 sg.Checkbox('', default=True, key=f'-ITEM{i}_ENABLED-')],
            ])],
            
            [sg.Text('')],
            
            # Detection Parameters
            [sg.Frame('Detection Parameters', [
                [sg.Text('Detection Method:', size=(15, 1)), 
                 sg.Combo(['Template Matching', 'Color Range', 'Contour Analysis', 'ML Model', 'Rule-based'],
                         default_value='Template Matching', key=f'-ITEM{i}_METHOD-', size=(28, 1), readonly=True)],
                [sg.Text('Confidence Threshold:', size=(15, 1)), 
                 sg.InputText(default_text='0.85', key=f'-ITEM{i}_THRESHOLD-', size=(10, 1)),
                 sg.Text('(0.0 - 1.0)')],
                [sg.Text('ROI X:', size=(15, 1)), 
                 sg.InputText(default_text='0', key=f'-ITEM{i}_ROI_X-', size=(10, 1)),
                 sg.Text('Y:'), 
                 sg.InputText(default_text='0', key=f'-ITEM{i}_ROI_Y-', size=(10, 1)),
                 sg.Text('W:'),
                 sg.InputText(default_text='640', key=f'-ITEM{i}_ROI_W-', size=(10, 1)),
                 sg.Text('H:'),
                 sg.InputText(default_text='480', key=f'-ITEM{i}_ROI_H-', size=(10, 1))],
            ])],
            
            [sg.Text('')],
            
            # Reference Image & Criteria
            [sg.Frame('Reference Image & Criteria', [
                [sg.Text('Reference Image:', size=(15, 1)), 
                 sg.InputText(default_text='', key=f'-ITEM{i}_REF_IMG-', size=(30, 1)),
                 sg.FileBrowse('Browse')],
                [sg.Text('Good Sample:', size=(15, 1)), 
                 sg.InputText(default_text='', key=f'-ITEM{i}_GOOD_IMG-', size=(30, 1)),
                 sg.FileBrowse('Browse')],
                [sg.Text('Bad Sample:', size=(15, 1)), 
                 sg.InputText(default_text='', key=f'-ITEM{i}_BAD_IMG-', size=(30, 1)),
                 sg.FileBrowse('Browse')],
            ])],
            
            [sg.Text('')],
            
            # Tolerance & Criteria
            [sg.Frame('Tolerance & Acceptance Criteria', [
                [sg.Text('Min Value:', size=(15, 1)), 
                 sg.InputText(default_text='0', key=f'-ITEM{i}_MIN_VAL-', size=(10, 1)),
                 sg.Text('Max Value:', size=(10, 1)),
                 sg.InputText(default_text='100', key=f'-ITEM{i}_MAX_VAL-', size=(10, 1))],
                [sg.Text('Tolerance Range:', size=(15, 1)), 
                 sg.InputText(default_text='±5', key=f'-ITEM{i}_TOLERANCE-', size=(10, 1))],
                [sg.Text('Pass Criteria:', size=(15, 1)), 
                 sg.Combo(['Must exist', 'Must not exist', 'Within range', 'Match template'],
                         default_value='Within range', key=f'-ITEM{i}_PASS_CRITERIA-', size=(28, 1), readonly=True)],
            ])],
            
            [sg.Text('')],
            
            # Logging & Reporting
            [sg.Frame('Logging & Reporting', [
                [sg.Checkbox('Log this item to CSV', default=True, key=f'-ITEM{i}_LOG_CSV-')],
                [sg.Checkbox('Save images for this item', default=True, key=f'-ITEM{i}_SAVE_IMG-')],
                [sg.Checkbox('Include in pass/fail decision', default=True, key=f'-ITEM{i}_CRITICAL-')],
            ])],
        ]
        
        tabs.append((f'Item {i}', tab_layout))
    
    # 메인 레이아웃
    layout = [
        [sg.Text('Inspection Items Configuration (10 Items)', font=('Helvetica', 14, 'bold'))],
        [sg.Text('')],
        [sg.TabGroup([tabs], key='-TABS-', enable_events=True, tab_location='left', size=(700, 600))],
        [sg.Text('')],
        [sg.Button('Save All Settings', key='-SAVE-'), 
         sg.Button('Load Default', key='-DEFAULT-'),
         sg.Button('Close', key='-CLOSE-')]
    ]
    
    window = sg.Window('Inspection Items Configuration', layout, finalize=True, modal=True, size=(800, 700), resizable=True)
    
    return window


def inspection_items_loop():
    """검사 항목 설정 화면 루프"""
    window = create_inspection_items_window()
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == '-CLOSE-':
            break
        
        elif event == '-SAVE-':
            sg.popup_ok('All inspection items saved successfully!', title='Success')
            # TODO: 설정을 파일에 저장
        
        elif event == '-DEFAULT-':
            # 기본값 로드
            for i in range(1, 11):
                window[f'-ITEM{i}_NAME-'].update(f'Item {i}')
                window[f'-ITEM{i}_THRESHOLD-'].update('0.85')
                window[f'-ITEM{i}_TOLERANCE-'].update('±5')
            sg.popup_ok('Default settings loaded.', title='Info')
    
    window.close()


if __name__ == '__main__':
    inspection_items_loop()
