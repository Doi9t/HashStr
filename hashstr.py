import sublime, sublime_plugin, hashlib, base64, json

def arr2str(arr):
	return ''.join(arr);

def writeToView(self, region, conteneur):
	if len(conteneur) != 0:
		if self.estSelect:
			self.view.replace(self.edit, region, conteneur);
		else:
			self.view.erase(self.edit, sublime.Region(0, self.view.size()));
			self.view.insert(self.edit, 0, conteneur);
	else:
		print('HashStr error: No string found !');

def base(selTxt, selBase):
	if selBase == 'enc_base16':
		return base64.b16encode(selTxt.encode('utf-8')).decode('utf-8');
	if selBase == 'enc_base32':
		return base64.b32encode(selTxt.encode('utf-8')).decode('utf-8');
	if selBase == 'enc_base64':
		return base64.b64encode(selTxt.encode('utf-8')).decode('utf-8');
	if selBase == 'enc_base64US':
		return base64.urlsafe_b64encode(selTxt.encode('utf-8')).decode('utf-8');
	if selBase == 'dec_base16':
		return base64.b16decode(selTxt).decode('utf-8');
	if selBase == 'dec_base32':
		return base64.b32decode(selTxt).decode('utf-8');
	if selBase == 'dec_base64':
		return base64.b64decode(selTxt).decode('utf-8');
	if selBase == 'dec_base64US':
		return base64.urlsafe_b64decode(selTxt).decode('utf-8');
	return '';

def genHash(selTxt, selHash):
	h = hashlib.new(selHash);
	h.update(selTxt.encode('utf-8'));
	return h.hexdigest();


class Hash(sublime_plugin.TextCommand):
	def run(self, edit, hashName = 'md5'):
		result = '';
		view = self.view;
		self.edit = edit;

		if hashName == 'generate':
			generateJsonMenu();

		if view.sel()[0].empty() and len(view.sel()) == 1: #No selection
			self.estSelect = False;

			if(hashName.startswith('enc_base') or hashName.startswith('dec_base')):
				result = base(arr2str([x for x in view.substr(sublime.Region(0, self.view.size())).splitlines() if x != '']), hashName);
			else:
				result = genHash(arr2str([x for x in view.substr(sublime.Region(0, self.view.size())).splitlines() if x != '']), hashName);

			writeToView(self, view.sel()[-1].end(), result);
		else:
			self.estSelect = True;
			for region in view.sel():
				if region.empty():
					continue;
				else:
					if(hashName.startswith('enc_base') or hashName.startswith('dec_base')):
						result = base(arr2str([x for x in view.substr(region).splitlines() if x != '']), hashName);
					else:
						result = genHash(arr2str([x for x in view.substr(region).splitlines() if x != '']), hashName);
	
					writeToView(self, region, result);