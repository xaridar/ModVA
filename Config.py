import os
import configparser as cp
import importlib as il


class Config:
    def __init__(self, yaml):
        self.parser = yaml['parser'] if 'parser' in yaml else None
        modules_dir = yaml['mods_dir'] if 'mods_dir' in yaml else None
        self.verbose_tts = yaml['verbose_tts'] if 'verbose_tts' in yaml else False
        self.loaderror = None
        self.getMods(modules_dir)
        self.middleware_tts_order = []
        self.middleware_sst_order = []
        if self.loaderror is not None:
            return
        if 'middleware' in yaml:
            order = yaml['middleware']
            for mod in order:
                if not mod in self.module_names:
                    self.loaderror = f"Module '{mod}' listed in middleware, but no module called '{mod}' is located in the {modules_dir} directory."
                    return
                if not mod in self.middleware_sst and not mod in self.middleware_tts:
                    self.loaderror = f"Module '{mod}' has no middleware functions defined using '@sst' or '@tts'."
                    return
                if mod in self.middleware_tts:
                    self.middleware_tts_order.append(self.middleware_tts[mod])
                if mod in self.middleware_sst:
                    self.middleware_sst_order.append(self.middleware_sst[mod])
        root_dir = os.getcwd()
        for currdir, fxn in self.init_fxns.items():
            os.chdir(f'{root_dir}\\{currdir}')
            fxn()
        os.chdir(root_dir)

    def getMods(self, mods_dir):
        if mods_dir is None:
            self.loaderror = 'No module directory specified'
            return
        if not os.path.isdir(mods_dir):
            self.loaderror = 'Invalid module directory specified'
            return
        self.mods = []
        self.module_names = []
        self.middleware_tts = {}
        self.middleware_sst = {}
        self.init_fxns = {}
        for i, (root, dirs, files) in enumerate(os.walk(mods_dir)):
            if root == mods_dir:
                self.module_names.extend(dirs)
                continue
            try:
                "".join(root.split(f'{mods_dir}\\')[1:]).index('\\')
                continue
            except:
                pass
            if 'commands.ini' not in files:
                self.loaderror = 'All modules must have a commands.ini file'
                return
            cf = cp.ConfigParser()
            cf.read(f'{root}/commands.ini')
            for mod in cf.sections():
                filename = None
                fxn_name = None
                try:
                    modName = cf[mod]['command'] if 'command' in cf[mod] else None
                    filename = cf[mod]['impl_file']
                    fxn_name = cf[mod]['impl_fn']
                    module = il.import_module(os.path.join(
                        root, f'{filename}').replace('\\', '.'))
                    fxn = getattr(module, fxn_name)
                    if mod == '@tts':
                        self.middleware_tts[root.split('\\')[1]] = fxn
                        continue
                    if mod == '@sst':
                        self.middleware_sst[root.split('\\')[1]] = fxn
                        continue
                    if mod == '@init':
                        self.init_fxns[root] = fxn
                        continue
                    if modName is None:
                        self.loaderror = f'Missing \'command\' in command {mod}'
                        return
                    self.mods.append(
                        {'command': modName, 'function': fxn, 'directory': root})
                except Exception as e:
                    if filename is None or fxn_name is None:
                        self.loaderror = f'Missing one or more of: impl_file, impl_fn in command {mod}'
                        return
                    name = root.split("\\")[1]
                    self.loaderror = f'Function not found in module {name}: {filename}/{fxn_name}'
                    return
