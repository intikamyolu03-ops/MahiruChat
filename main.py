# main.py
import os
import shutil
import socket
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog

class CustomChatRow(MDBoxLayout):
    username = StringProperty()
    last_message = StringProperty()
    avatar_source = StringProperty('varsayilan_avatar.png')
    is_online = BooleanProperty(False)

class NotificationDialogContent(BoxLayout):
    def __init__(self, app_root, sender_name, **kwargs):
        super().__init__(**kwargs)
        self.app_root = app_root
        self.sender_name = sender_name
        self.ids.req_text.text = f"👑 {sender_name} sana arkadaşlık isteği gönderdi!"
    def accept_req(self): self.app_root.dialog.dismiss()
    def reject_req(self): self.app_root.dialog.dismiss()

class MainScreen(BoxLayout):
    dialog = None
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.profile_manager = MDFileManager(exit_manager=self.close_manager, select_path=self.select_profile_pic)
        # Sunucu bağlantısını test için simüle ediyoruz, gerçek sokete bağlanabilir.
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('127.0.0.1', 55555))
        except:
            self.client = None

    def process_auth(self, mode):
        username = self.ids.auth_username.text.strip()
        password = self.ids.auth_password.text.strip()
        if not username or not password:
            self.ids.auth_status.text = "Alanlar boş bırakılamaz!"
            return
        if not self.client:
            # Sunucu açık değilse direkt uygulamaya sok (Test kolaylığı için)
            self.ids.login_panel.opacity = 0
            self.ids.login_panel.disabled = True
            self.ids.main_panel.opacity = 1
            self.ids.main_panel.disabled = False
            return

        request = f"{mode}:{username}:{password}"
        self.client.send(request.encode('utf-8'))
        response = self.client.recv(1024).decode('utf-8')
        
        if response == "REG_OK":
            self.ids.auth_status.text = "Hesap açıldı! Giriş yapabilirsiniz."
        elif response == "REG_ERR_TAKEN":
            self.ids.auth_status.text = "❌ Bu kullanıcı adı başkası tarafından alınmış!"
        elif response == "AUTH_OK":
            self.ids.login_panel.opacity = 0
            self.ids.login_panel.disabled = True
            self.ids.main_panel.opacity = 1
            self.ids.main_panel.disabled = False

    def open_profile_pic_manager(self):
        self.profile_manager.show(os.path.expanduser("~"))
    def select_profile_pic(self, path):
        self.close_manager()
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            shutil.copy(path, "profil_resmim.jpg")
            self.ids.profile_avatar.source = "profil_resmim.jpg"
            self.ids.profile_avatar.reload()
    def close_manager(self, *args): self.profile_manager.close()
    def create_group(self): pass
    def search_user(self):
        u = self.ids.search_username.text.strip()
        if u:
            self.ids.result_name.text = u
            self.ids.result_card.opacity = 1
    def send_friend_request(self): self.ids.btn_send_request.text = "Gönderildi"
    def open_notifications(self):
        if not self.dialog:
            self.dialog = MDDialog(title="Gelen İstekler", type="custom", content_cls=NotificationDialogContent(self, "Selin"))
        self.dialog.open()

class ChatApp(MDApp):
    def build(self):
        # 👑 BURADA SENİN ATTIĞIN İKONU VE İSMİ BAĞLADIK 👑
        self.title = "Mahiru Chat"
        self.icon = "icon.png"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        return MainScreen()

if __name__ == "__main__":
    ChatApp().run()