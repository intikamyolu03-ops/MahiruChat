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
        self.profile_manager = MDFileManager(
            exit_manager=self.close_manager,
            select_path=self.select_profile_pic
        )
        # Try to connect to server; fall back to offline mode if unavailable
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.settimeout(3)
            self.client.connect(('127.0.0.1', 55555))
        except Exception:
            self.client = None

    def process_auth(self, mode):
        username = self.ids.auth_username.text.strip()
        password = self.ids.auth_password.text.strip()
        if not username or not password:
            self.ids.auth_status.text = "Alanlar boş bırakılamaz!"
            return
        if not self.client:
            # Offline / demo mode – skip server check
            self._show_main_panel()
            return

        try:
            request = f"{mode}:{username}:{password}"
            self.client.send(request.encode('utf-8'))
            response = self.client.recv(1024).decode('utf-8')

            if response == "REG_OK":
                self.ids.auth_status.text = "Hesap açıldı! Giriş yapabilirsiniz."
            elif response == "REG_ERR_TAKEN":
                self.ids.auth_status.text = "❌ Bu kullanıcı adı başkası tarafından alınmış!"
            elif response == "AUTH_OK":
                self._show_main_panel()
            else:
                self.ids.auth_status.text = "❌ Kullanıcı adı veya şifre hatalı!"
        except Exception:
            self.ids.auth_status.text = "Sunucuya bağlanılamadı."

    def _show_main_panel(self):
        self.ids.login_panel.opacity = 0
        self.ids.login_panel.disabled = True
        self.ids.main_panel.opacity = 1
        self.ids.main_panel.disabled = False

    def open_profile_pic_manager(self):
        self.profile_manager.show(os.path.expanduser("~"))

    def select_profile_pic(self, path):
        self.close_manager()
        if path.lower().endswith(('.png', '.jpg', '.jpeg')):
            dest = os.path.join(os.path.dirname(__file__), "profil_resmim.jpg")
            shutil.copy(path, dest)
            self.ids.profile_avatar.source = dest
            self.ids.profile_avatar.reload()

    def close_manager(self, *args):
        self.profile_manager.close()

    def create_group(self):
        pass

    def search_user(self):
        u = self.ids.search_username.text.strip()
        if u:
            self.ids.result_name.text = u
            self.ids.result_card.opacity = 1

    def send_friend_request(self):
        self.ids.btn_send_request.text = "Gönderildi ✓"

    def open_notifications(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Gelen İstekler",
                type="custom",
                content_cls=NotificationDialogContent(self, "Selin")
            )
        self.dialog.open()


class ChatApp(MDApp):
    def build(self):
        self.title = "Mahiru Chat"
        self.icon = "icon.png"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Pink"
        return MainScreen()


if __name__ == "__main__":
    ChatApp().run()
