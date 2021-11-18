from enum import IntEnum
from PyQt6.QtCore import QObject

userNotificationsEnabled = True
try:
    import UserNotifications
except ImportError:
    print(f'UserNotifications could not be imported')
    userNotificationsEnabled = False

# Using code from https://stackoverflow.com/q/57381422 as a base

class QMacNotification(QObject):
    class AuthorizationOptions(IntEnum):
        UpdateAppBadge = 1 << 0
        PlaySound = 1 << 1
        DisplayAlert = 1 << 2
        DisplayCarPlay = 1 << 3
        PlaySoundForCriticalAlert = 1 << 4
        DisplayButtonForInAppNotificationSettings = 1 << 5
        PostNoninterruptingNotificationsToNotificationCenter = 1 << 6
        NoOptions = 0

    def __init__(self, title: str = None, subtitle: str = None, body: str = None, badge: int = None, userInfo: dict = None, options: AuthorizationOptions = 0, parent=None):
        super().__init__(parent)

        if userNotificationsEnabled:
            self.__notif = UserNotifications.UNMutableNotificationContent.alloc().init()

        if title is not None: self.setTitle(title)
        if subtitle is not None: self.setSubtitle(subtitle)
        if body is not None: self.setBody(body)
        if badge is not None: self.setBadge(badge)
        if userInfo is not None: self.setUserInfo(userInfo)
        if options is not None: self.setOptions(options)

    __title: str = ''
    def title(self) -> str: return self.__title
    def setTitle(self, title: str):
        self.__title = title

        if userNotificationsEnabled:
            self.__notif.setTitle_(self.__title)

    __subtitle: str = ''
    def subtitle(self) -> str: return self.__subtitle
    def setSubtitle(self, subtitle: str):
        self.__subtitle = subtitle

        if userNotificationsEnabled:
            self.__notif.setSubtitle_(self.__subtitle)

    __body: str = ''
    def body(self) -> str: return self.__body
    def setBody(self, body: str):
        self.__body = body

        if userNotificationsEnabled:
            self.__notif.setBody_(self.__body)

    __badge: int = 0
    def badge(self) -> int: return self.__badge
    def setBadge(self, badge: int):
        self.__badge = badge

        if userNotificationsEnabled:
            self.__notif.setBadge_(self.__badge)

    __userInfo: dict = {}
    def userInfo(self) -> dict: return self.__userInfo
    def setUserInfo(self, userInfo: dict):
        self.__userInfo = userInfo

        if userNotificationsEnabled:
            self.__notif.setUserInfo_(self.__userInfo)

    __options: AuthorizationOptions = AuthorizationOptions.NoOptions
    def options(self) -> AuthorizationOptions: return self.__options
    def setOptions(self, options: AuthorizationOptions): self.__options = options

    def onNotificationPosted(self, err):
        pass

    def onAuthResult(self, granted, err):
        pass

    def exec(self):
        if not userNotificationsEnabled:
            print('Was not able to import UserNotifications, so do nothing')
            return
            
        r = UserNotifications.UNNotificationRequest.requestWithIdentifier_content_trigger_('test_notification', self.__notif, None)
        notifCenter = UserNotifications.UNUserNotificationCenter.currentNotificationCenter()
        notifCenter.requestAuthorizationWithOptions_completionHandler_(int(self.__options), self.onAuthResult)
        notifCenter.addNotificationRequest_withCompletionHandler_(r, self.onNotificationPosted)
