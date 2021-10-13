import json
import subprocess
import webbrowser
import winsound
from datetime import datetime, time
from pathlib import Path
from urllib.request import urlopen

import wx
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade

CONFIG_FILE_NAME = 'settings.yaml'
DOCS_FILE = 'docs.html'
INTRO_SOUND_FILE = 'intro.wav'
UPDATE_SOUND_FILE = 'update.wav'

APP_NAME = 'Telecode'
APP_PATH = Path(__file__).parent

with open(APP_PATH / UPDATE_SOUND_FILE, mode='rb') as f:
    UPDATE_SOUND = f.read()


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.main_panel = wx.Panel(self, wx.ID_ANY)
        self.text_ctrl_file_path = wx.TextCtrl(self.main_panel, wx.ID_ANY, "", style=wx.TE_READONLY)
        self.button_open_in_editor = wx.Button(self.main_panel, wx.ID_ANY, u"\u0412\u0456\u0434\u043a\u0440\u0438\u0442\u0438 \u0443 \u0440\u0435\u0434\u0430\u043a\u0442\u043e\u0440\u0456")
        self.button_open_in_explorer = wx.Button(self.main_panel, wx.ID_ANY, u"\u0412\u0456\u0434\u043a\u0440\u0438\u0442\u0438 \u0443 \u043f\u0440\u043e\u0432\u0456\u0434\u043d\u0438\u043a\u043e\u0432\u0456")
        self.button_save_copy = wx.Button(self.main_panel, wx.ID_ANY, u"\u0417\u0431\u0435\u0440\u0435\u0433\u0442\u0438 \u043a\u043e\u043f\u0456\u044e")
        self.button_notification_sound = wx.ToggleButton(self.main_panel, wx.ID_ANY, u"\u0417\u0432\u0443\u043a\u043e\u0432\u0430 \u043d\u043e\u0442\u0438\u0444\u0456\u043a\u0430\u0446\u0456\u044f \u043f\u0440\u0438 \u043e\u043d\u043e\u0432\u043b\u0435\u043d\u043d\u0456")
        self.button_show_docs = wx.Button(self.main_panel, wx.ID_ANY, u"\u0414\u043e\u0432\u0456\u0434\u043a\u0430")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.open_in_editor, self.button_open_in_editor)
        self.Bind(wx.EVT_BUTTON, self.open_in_explorer, self.button_open_in_explorer)
        self.Bind(wx.EVT_BUTTON, self.save_file_copy, self.button_save_copy)
        self.Bind(wx.EVT_BUTTON, self.show_docs, self.button_show_docs)
        # end wxGlade
		
		# timer
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        pass
        # end wxGlade
		
		# hack: include edit in tab order
        self.text_ctrl_file_path.AcceptsFocusFromKeyboard=lambda:True
        self.button_notification_sound.SetValue(True)

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.StaticBoxSizer(wx.StaticBox(self.main_panel, wx.ID_ANY, ""), wx.VERTICAL)
        sizer_2.Add(self.text_ctrl_file_path, 0, wx.EXPAND, 0)
        sizer_2.Add((20, 10), 0, 0, 0)
        sizer_2.Add(self.button_open_in_editor, 0, wx.EXPAND, 0)
        sizer_2.Add((20, 10), 0, wx.ALL, 0)
        sizer_2.Add(self.button_open_in_explorer, 0, wx.EXPAND, 0)
        sizer_2.Add((20, 10), 0, wx.ALL, 0)
        sizer_2.Add(self.button_save_copy, 0, wx.EXPAND, 0)
        sizer_2.Add((20, 10), 0, wx.ALL, 0)
        sizer_2.Add(self.button_notification_sound, 0, 0, 0)
        sizer_2.Add((20, 10), 0, wx.ALL, 0)
        sizer_2.Add(self.button_show_docs, 0, wx.EXPAND, 0)
        self.main_panel.SetSizer(sizer_2)
        sizer_1.Add(self.main_panel, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        self.Centre()
        # end wxGlade

    def start_timer(self):
        self.last_update_time = datetime.now()
        self.last_content = ''
        self.timer.Start(self.settings.get('poll_time'))

    def stop_timer(self):
        self.timer.Stop()

    def load_settings(self):

        # play wellcome sound
        intro_path = APP_PATH / INTRO_SOUND_FILE
        winsound.PlaySound(str(intro_path), winsound.SND_ASYNC)

        settings_file_path = APP_PATH / CONFIG_FILE_NAME
        if not settings_file_path.exists():
            wx.MessageBox('Відсутній файл конфігурації. Роботу програми буде припинено', caption='Помилка', style=wx.OK|wx.ICON_ERROR)
            wx.Exit()
        with settings_file_path.open(mode='r', encoding='utf8') as settings_file:
            try:
                self.settings = yaml.load(settings_file, Loader=Loader)
            except Exception as e:
                wx.MessageBox('Невірний файл конфігурації. Роботу програми буде припинено\n' + str(e), caption='Помилка', style=wx.OK|wx.ICON_ERROR)
                self.settings = None
                wx.Exit()
        
        files_dir_path = APP_PATH / self.settings.get('files_folder')
        if not files_dir_path.exists():
            files_dir_path.mkdir()
        
        local_dir_path = self.settings.get('files_subfolder')
        self.local_dir_path = files_dir_path / local_dir_path
        if not self.local_dir_path.exists():
            self.local_dir_path.mkdir()

        local_file = self.settings.get('local_file')
        self.local_file_path = self.local_dir_path / local_file
        self.text_ctrl_file_path.SetValue(str(self.local_file_path))


    def get_remote_file(self):
        try:
            with urlopen(self.settings.get('remote_file_url'), timeout=self.settings.get('request_timeout')) as response:
                content = response.read()
        except Exception:
            return
        return content
		
    def update(self, event):
        content = self.get_remote_file()
        if content is None:
            self.stop_timer()
            reply = wx.MessageDialog(
                None,
                '''Немає зв'язку з сервером!\nПовторити спробу?''',
                'Помилка',
                wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION
            ).ShowModal()
            if reply == wx.ID_NO:
                wx.Exit()
            self.start_timer()
            return
        if content != self.last_content:
            self.local_file_path.write_bytes(content)
            self.last_content = content
            self.last_update_time = datetime.now()
            if self.button_notification_sound.GetValue():
                winsound.PlaySound(UPDATE_SOUND, winsound.SND_MEMORY)
        time_passed = datetime.now() - self.last_update_time
        mins, secs = divmod(time_passed.seconds, 60)
        self.SetTitle(f"{mins}:{secs:02d} — {APP_NAME}")

    def open_in_editor(self, event):  # wxGlade: MainFrame.<event_handler>
        editor_path = Path(self.settings.get('editor_path'))
        if not editor_path.is_absolute():
            editor_path = APP_PATH / editor_path
        subprocess.Popen([str(editor_path), str(self.local_file_path)])
        event.Skip()

    def open_in_explorer(self, event):  # wxGlade: MainFrame.<event_handler>
        subprocess.Popen(['explorer.exe', str(self.local_dir_path)])
        event.Skip()
        
    def save_file_copy(self, event):  # wxGlade: MainFrame.<event_handler>
        dlg = wx.TextEntryDialog(self, 'Назва файла:','Зберегти копію файла')
        date_str = datetime.now().strftime('_%H_%M_%S')
        new_file_name = self.local_file_path.stem + date_str + self.local_file_path.suffix
        dlg.SetValue(new_file_name)
        if dlg.ShowModal() == wx.ID_OK:
            (self.local_dir_path / new_file_name).write_bytes(self.last_content)
        dlg.Destroy()
        event.Skip()

    def show_docs(self, event):  # wxGlade: MainFrame.<event_handler>
        docs_html_file_path = APP_PATH / DOCS_FILE
        webbrowser.open(str(docs_html_file_path))
        event.Skip()
# end of class MainFrame

class MyApp(wx.App):
    def OnInit(self):
        self.telecode = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.telecode)
        self.telecode.Show()

        self.telecode.load_settings()
        self.telecode.start_timer()
        return True

# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
