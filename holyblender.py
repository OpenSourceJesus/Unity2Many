#!/usr/bin/env python3
import os, sys, subprocess, atexit, json

try:
	import gi
except:
	gi = None

if gi:
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk

	def run_frontend():
		w = HolyBlender()
		w.show_all()
		Gtk.main()

	class HolyBlender(Gtk.Window):
		def __init__(self):
			super().__init__(title="HolyBlender")
			self.connect("destroy", Gtk.main_quit)

			self.set_default_size(180, 200)
			vbox = Gtk.VBox(spacing=6)
			self.add(vbox)
			btn = Gtk.Button(label='Open HolyBlender')
			btn.connect("clicked", self.on_open_blender)
			vbox.pack_start(btn, False, False, 0)

			btn = Gtk.Button(label='Make Character')
			btn.connect("clicked", self.on_open_ink)
			vbox.pack_start(btn, False, False, 0)

		def on_open_blender(self, btn):
			open_holyblender()
		def on_open_ink(self, btn):
			open_ink3d()

TB_FUNCS = '''
static void on_click_unity_export(GtkWidget *widget, gpointer data) {
	std::cout << "clicked unity button" << std::endl;
	inkscape_save_temp();
	__inkstate__ = 3000;
}
'''

TB = '''
	{
		auto btn = gtk_button_new_with_label("Unity");
		gtk_grid_attach(GTK_GRID(grid), btn, 0, 1, 1, 1);
		g_signal_connect(btn, "clicked", G_CALLBACK(on_click_unity_export), NULL);
	}

'''

TB_SETUP = '''
def on_unity_event():
	blend = ink2blend()
	cmd = ["python3", "./BlenderPlugin.py", blend]
	print(cmd)
	subprocess.check_call(cmd, cwd="..")

PLUGIN_EVENTS[3000] = on_unity_event

'''

PLUGINK = {
	'toolbar_funcs':TB_FUNCS,
	'toolbar' : TB,
	'python'  : TB_SETUP,
}

def open_ink3d():
	if not os.path.isdir('./inkscape2019'):
		cmd = 'git clone --depth 1 https://github.com/brentharts/inkscape2019.git'
		print(cmd)
		subprocess.check_call(cmd.split())

	tmp = '/tmp/holyblender.plugink'
	open(tmp, 'w').write(json.dumps(PLUGINK))
	cmd = ['python3', './inkscape.py', tmp]
	print(cmd)
	subprocess.check_call(cmd, cwd='./inkscape2019')

def open_holyblender():
	cmd = ['python3', './BlenderPlugin.py']
	print(cmd)
	proc = subprocess.Popen(cmd)
	atexit.register(lambda : proc.kill())
	return proc

if __name__=='__main__':
	if gi:
		run_frontend()
	else:
		if os.path.isfile('/usr/bin/dnf'):
			print('you need to run: sudo dnf install python3-gobject')
		else:
			print('you need to run: sudo apt install python3-gi')