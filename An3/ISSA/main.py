import subprocess
import time

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
import dbus

bus = dbus.SystemBus()
import bluetooth

hal_manager_object = bus.get_object('org.bluez', '/org/bluez/hci0/dev_50_BC_96_DF_46_9C')
hal_manager_media_interface = dbus.Interface(hal_manager_object, 'org.bluez.MediaControl1')


class ApplicationWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Media Player")
        self.connect("destroy", Gtk.main_quit)

    def show(self):
        self.show_all()

    def setup_objects_and_events(self):
        self.bluetooth_button = Gtk.Button()
        self.bluetooth_image = Gtk.Image.new_from_icon_name("preferences-system-bluetooth", Gtk.IconSize.DND)
        self.bluetooth_button.set_image(self.bluetooth_image)
        self.bluetooth_button.connect("clicked", self.get_bluetooth_devices)

        self.playback_button = Gtk.Button()
        self.play_image = Gtk.Image.new_from_icon_name("media-playback-start", Gtk.IconSize.DND)
        self.playback_button.set_image(self.play_image)
        self.playback_button.connect("clicked", self.play_player)

        self.pause_button = Gtk.Button()
        self.pause_image = Gtk.Image.new_from_icon_name("media-playback-pause", Gtk.IconSize.DND)
        self.pause_button.set_image(self.pause_image)
        self.pause_button.connect("clicked", self.pause_player)

        self.previous_button = Gtk.Button()
        self.previous_image = Gtk.Image.new_from_icon_name("media-skip-backward", Gtk.IconSize.DND)
        self.previous_button.set_image(self.previous_image)
        self.previous_button.connect("clicked", self.previous_player)

        self.next_button = Gtk.Button()
        self.next_image = Gtk.Image.new_from_icon_name("media-skip-forward", Gtk.IconSize.DND)
        self.next_button.set_image(self.next_image)
        self.next_button.connect("clicked", self.next_player)

        self.volume_up_button = Gtk.Button()
        self.volume_up_image = Gtk.Image.new_from_icon_name("audio-volume-high", Gtk.IconSize.DND)
        self.volume_up_button.set_image(self.volume_up_image)
        self.volume_up_button.connect("clicked", self.volume_up)

        self.volume_down_button = Gtk.Button()
        self.volume_down_image = Gtk.Image.new_from_icon_name("audio-volume-low", Gtk.IconSize.DND)
        self.volume_down_button.set_image(self.volume_down_image)
        self.volume_down_button.connect("clicked", self.volume_up)

        self.device_list_label = Gtk.Label("Device list")

        self.device_list_combobox = Gtk.ComboBoxText()
        self.device_list_combobox.connect("changed", self.on_device_selected)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.grid.attach(self.bluetooth_button,
                         0, 0, 1, 1)
        self.grid.attach(self.previous_button,
                         1, 0, 1, 1)
        self.grid.attach(self.playback_button,
                         2, 0, 1, 1)
        self.grid.attach(self.pause_button,
                         3, 0, 1, 1)
        self.grid.attach(self.next_button,
                         4, 0, 1, 1)
        self.grid.attach(self.volume_down_button,
                         5, 0, 1, 1)
        self.grid.attach(self.volume_up_button,
                         6, 0, 1, 1)
        self.grid.attach(self.device_list_label,
                         0, 1, 6, 1)
        self.grid.attach(self.device_list_combobox,
                         0, 2, 6, 1)

    def get_bluetooth_devices(self, widget, data=None):
        devices = bluetooth.discover_devices(lookup_names=True)
        self.bluetooth_devices = {device[1]: device[0] for device in devices}
        for device_name in self.bluetooth_devices:
            self.device_list_combobox.append_text(device_name)

    def on_device_selected(self, combo):
        global hal_manager_object
        device_name = combo.get_active_text()
        if device_name is not None:
            device_address = self.bluetooth_devices[device_name]
            print("Selected", device_name, "with mac address", device_address)
            process = subprocess.Popen("bluetoothctl",
                                       shell=True,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT)
            process.stdin.write(b"power on\n")
            process.stdin.write(b"agent on\n")
            process.stdin.write(b"scan on\n")
            time.sleep(5)
            process.stdin.write("pair {}\n".format(device_address).encode())
            process.stdin.write("connect {}\n".format(device_address).encode())
            process.stdin.write("trust {}\n".format(device_address).encode())
            process.stdin.write(b"scan off\n")
            print(process.communicate(b"exit\n")[0].decode())
            process.wait()
            hal_manager_object = bus.get_object('org.bluez',  # This replaces : with _ in the mac address, it is needed
                                                '/org/bluez/hci0/dev_{}'.format("_".join(device_address.split(":"))))

    def play_music(self, widget, data=None):
        print("Play")

    def previous_player(self, widget, data=None):
        hal_manager_media_interface.Previous()

    def next_player(self, widget, data=None):
        hal_manager_media_interface.Next()

    def stop_player(self, widget, data=None):
        hal_manager_media_interface.Stop()

    def pause_player(self, widget, data=None):
        hal_manager_media_interface.Pause()

    def play_player(self, widget, data=None):
        hal_manager_media_interface.Play()

    def volume_up(self, widget, data=None):
        hal_manager_media_interface.VolumeUp()

    def volume_down(self, widget, data=None):
        hal_manager_media_interface.VolumeDown()


if __name__ == '__main__':
    window = ApplicationWindow()
    window.setup_objects_and_events()
    window.show()
    Gtk.main()
