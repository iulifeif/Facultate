import subprocess
import time
import bluetooth
from xml.etree import ElementTree
from PyOBEX import client, headers, responses
import vobject
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('GdkX11', '3.0')
from gi.repository import GdkX11
import dbus

bus = dbus.SystemBus()
import bluetooth


class ApplicationWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Media Player")
        self.connect("destroy", Gtk.main_quit)

        hal_manager_object = None
        hal_manager_media_interface = None

    def show(self):
        self.show_all()

    def setup_objects_and_events(self):
        self.bluetooth_button = Gtk.Button()
        self.bluetooth_image = Gtk.Image.new_from_icon_name("preferences-system-bluetooth", Gtk.IconSize.DND)
        self.bluetooth_button.set_image(self.bluetooth_image)
        self.bluetooth_button.connect("clicked", self.get_bluetooth_devices)

        self.playback_button = Gtk.Button()
        self.playback_button.set_sensitive(False)
        self.play_image = Gtk.Image.new_from_icon_name("media-playback-start", Gtk.IconSize.DND)
        self.playback_button.set_image(self.play_image)
        self.playback_button.connect("clicked", self.play_player)

        self.pause_button = Gtk.Button()
        self.pause_button.set_sensitive(False)
        self.pause_image = Gtk.Image.new_from_icon_name("media-playback-pause", Gtk.IconSize.DND)
        self.pause_button.set_image(self.pause_image)
        self.pause_button.connect("clicked", self.pause_player)

        self.previous_button = Gtk.Button()
        self.previous_button.set_sensitive(False)
        self.previous_image = Gtk.Image.new_from_icon_name("media-skip-backward", Gtk.IconSize.DND)
        self.previous_button.set_image(self.previous_image)
        self.previous_button.connect("clicked", self.previous_player)

        self.next_button = Gtk.Button()
        self.next_button.set_sensitive(False)
        self.next_image = Gtk.Image.new_from_icon_name("media-skip-forward", Gtk.IconSize.DND)
        self.next_button.set_image(self.next_image)
        self.next_button.connect("clicked", self.next_player)

        self.volume_up_button = Gtk.Button()
        self.volume_up_button.set_sensitive(False)
        self.volume_up_image = Gtk.Image.new_from_icon_name("audio-volume-high", Gtk.IconSize.DND)
        self.volume_up_button.set_image(self.volume_up_image)
        self.volume_up_button.connect("clicked", self.volume_up)

        self.volume_down_button = Gtk.Button()
        self.volume_down_button.set_sensitive(False)
        self.volume_down_image = Gtk.Image.new_from_icon_name("audio-volume-low", Gtk.IconSize.DND)
        self.volume_down_button.set_image(self.volume_down_image)
        self.volume_down_button.connect("clicked", self.volume_up)

        self.downloadContacts_button = Gtk.Button()
        self.downloadContacts_button.set_sensitive(False)
        self.downloadContacts_image = Gtk.Image.new_from_icon_name("download", Gtk.IconSize.DND)
        self.downloadContacts_button.set_image(self.downloadContacts_image)
        self.downloadContacts_button.connect("clicked", self.download_contacts)

        self.device_list_label = Gtk.Label("Device list")

        self.device_list_combobox = Gtk.ComboBoxText()
        self.device_list_combobox.connect("changed", self.on_device_selected)

        self.contact_list_label = Gtk.Label("Contact list")

        self.contact_list_combobox = Gtk.ComboBoxText()
        self.contact_list_combobox.connect("changed", self.on_contact_selected)

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
        self.grid.attach(self.downloadContacts_button,
                         7, 0, 1, 1)
        self.grid.attach(self.device_list_label,
                         0, 1, 7, 1)
        self.grid.attach(self.device_list_combobox,
                         0, 2, 7, 1)
        self.grid.attach(self.device_list_label,
                         0, 3, 7, 1)
        self.grid.attach(self.contact_list_combobox,
                         0, 4, 7, 1)

    def get_bluetooth_devices(self, widget, data=None):
        devices = bluetooth.discover_devices(lookup_names=True)
        self.bluetooth_devices = {device[1]: device[0] for device in devices}
        for device_name in self.bluetooth_devices:
            self.device_list_combobox.append_text(device_name)

    def on_device_selected(self, combo):
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
            self.connected_device_name = device_name
            self.hal_manager_object = bus.get_object('org.bluez',  # This replaces : with _ in the mac address, it is needed
                                                '/org/bluez/hci0/dev_{}'.format("_".join(device_address.split(":"))))
            self.hal_manager_media_interface = dbus.Interface(self.hal_manager_object, 'org.bluez.MediaControl1')
            self.playback_button.set_sensitive(True)
            self.pause_button.set_sensitive(True)
            self.previous_button.set_sensitive(True)
            self.next_button.set_sensitive(True)
            self.volume_up_button.set_sensitive(True)
            self.volume_down_button.set_sensitive(True)
            self.downloadContacts_button.set_sensitive(True)

    def play_music(self, widget, data=None):
        print("Play")

    def previous_player(self, widget, data=None):
        self.hal_manager_media_interface.Previous()

    def next_player(self, widget, data=None):
        self.hal_manager_media_interface.Next()

    def stop_player(self, widget, data=None):
        self.hal_manager_media_interface.Stop()

    def pause_player(self, widget, data=None):
        self.hal_manager_media_interface.Pause()

    def play_player(self, widget, data=None):
        self.hal_manager_media_interface.Play()

    def volume_up(self, widget, data=None):
        self.hal_manager_media_interface.VolumeUp()

    def volume_down(self, widget, data=None):
        self.hal_manager_media_interface.VolumeDown()

    def download_contacts(self, widget, data=None):
        self.contact_list_label.set_label("Contact list (downloading...)")
        try:
            d = bluetooth.find_service(address=self.bluetooth_devices[self.connected_device_name], uuid="1130")
            if not d:
                print("No phonebook service found. \n")
                return

            port = d[0]["port"]
            c = client.Client(self.bluetooth_devices[self.connected_device_name], port)
            uuid = b"\x79\x61\x35\xf0\xf0\xc5\x11\xd8\x09\x66\x08\x00\x20\x0c\x9a\x66"
            result = c.connect(header_list=[headers.Target(uuid)])
            if not isinstance(result, responses.ConnectSuccess):
                print("Failed to connect to phone. ")
                return

            prefix = ""
            hdrs, cards = c.get(prefix + "telecom/pb", header_list=[headers.Type(b"x-bt/vcard-listing")])
            root = ElementTree.fromstring(cards)
            print("\nAvailable cards in %stelecom/pb\n" % prefix)
            names = []
            for card in root.findall("card"):
                print("%s: %s" % (card.attrib["handle"], card.attrib["name"]))
            names.append(card.attrib["handle"])

            print("\nCards in %stelecom/pb\n" % prefix)

            # Request all the file names obtained earlier.
            c.setpath(prefix + "telecom/pb")
            list_with_contacts = []
            for name in names:
                hdrs, card = c.get(name, header_list=[headers.Type(b"x-bt/vcard")])
                # Decode bytes as string
                encoding = 'utf-8'
                strCard = card.decode(encoding)
                vCard = vobject.readOne(strCard)
                vCard.prettyPrint()
                if hasattr(vCard, 'n'):
                    if hasattr(vCard, 'tel'):
                        list_with_contacts.append([vCard.n.value.family + ' ' +
                                                   vCard.n.value.given + ' ' + vCard.tel.value])
            c.disconnect()
            print(list_with_contacts)
        finally:
            self.contact_list_label.set_label("Contact list")

    def on_contact_selected(self):
        pass

if __name__ == '__main__':
    window = ApplicationWindow()
    window.setup_objects_and_events()
    window.show()
    Gtk.main()

