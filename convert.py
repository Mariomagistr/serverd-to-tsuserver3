import yaml
import os

def _load_tsu(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    t = yaml.load(f)
    f.close()
    return t
    
def _config_serverd(file_path):
    f = open(file_path, 'r', encoding='utf-8')
    t = {}
    for line in f:
        if '=' in line and not '#' in line:
            t[line[:line.find('=') - 1]] = line[line.find('=') + 2:].replace('\n', '')
    f.close()
    return t
    
def _area_serverd(file_path):
    #print('huh')
    f = open(file_path, 'r', encoding = 'utf-8')
    t = []
    opt = ''
    cntr = 0
    num = 0
    cnt = 0
    case = 'area'
    for line in f:
        cntr += 1
        if cntr == 1:
            continue
        if cntr == 2:
            num = int(line[9:-1])
            #print(num)
            t = [{'area': 'default', 'background': 'gs4', 'evidence_mod': 'FFA', 'locking_allowed': False, 'iniswap_allowed': True, 'bglock': False} for i in range(num)]
            continue
        #print(line[:-1])
        if len(line) < 3:
            continue
        if cnt == num:
            cnt = 0
            if case == 'background':
                break
            case = 'background'
            continue
        t[cnt][case] = line[line.find('=') + 2:].replace('\n', '')
        
        cnt += 1
    f.close()
    return t
 
def _chars_serverd(file_path):
    f = open(file_path, 'r', encoding = 'utf-8')
    t = []
    fl = 0
    for line in f:
        if line.startswith('[chars]'):
            fl = 1
            continue
        if not fl:
            continue
        if len(line) < 3:
            continue
        if '[desc' in line:
            break
        if line.startswith('number'):
            continue
        if '=' in line:
            tt = line.find('=') + 1
            while line[tt] == ' ':
                tt += 1
            dd = -1
            while line[dd] in [' ', '\n']:
                dd -= 1
            t.append(line[tt:dd + 1].replace('\n', ''))
    f.close()
    return t
def _music_serverd(file_path):
    f = open(file_path, 'r', encoding = 'utf-8')
    categories = []
    default = {'category': 'def', 'songs': []}
    t = []
    for line in f:
        if len(line) < 3:
            continue
        if line.startswith('~stop'):
            continue
        if line[0] == '>':
            continue
        if not '.mp3' in line:
            categories.append(line.replace('\n', ''))
            t.append({'category': 'def', 'songs': []})
            t[-1]['category'] = categories[-1]
            print('########################################################################################')
            for i in t:
                print(i['category'], len(i['songs']))
        else:
            t[-1]['songs'].append({'name': 'def.mp3', 'length': -1})
            t[-1]['songs'][-1]['name'] = line[:line.find('.mp3') + 4]
            if '.mp3*' in line:
                t[-1]['songs'][-1]['length'] = int(line[line.find('.mp3') + 5:].replace('\n', ''))
    f.close()
    return t
    
def convert_config(tsu_path, serverd_path):
    f1 = _load_tsu(tsu_path)
    f2 = _config_serverd(serverd_path)
    for i in ['desc', 'public', 'opppassword', 'name', 'port']:
        if i not in f2:
            if i == 'public':
                f2[i] = 0
            elif i == 'port':
                f2[i] = 50000
            else:
                f2[i] = '<edit me>'
    f1['port'] = int(f2['port'])
    f1['masterserver_name'] = f2['name']
    f1['masterserver_description'] = f2['desc']
    f1['use-masterserver'] = bool(f2['public'])
    f1['modpass'] = f2['oppassword']
    ss = os.listdir()
    if not 'config' in ss:
        os.mkdir('config')
    yaml.dump(f1, open(tsu_path.replace('_sample', ''), 'w', encoding = 'utf-8'), default_flow_style = False)
    return f2['case']

def convert_areas(tsu_path, serverd_path):
    f2 = _area_serverd(serverd_path)
    #print(f2)
    yaml.dump(f2, open(tsu_path.replace('_sample', ''), 'w', encoding = 'utf-8'), default_flow_style = False)
    
def convert_music(tsu_path, serverd_path):
    f2 = _music_serverd(serverd_path)
    yaml.dump(f2, open(tsu_path.replace('_sample', ''), 'w', encoding = 'utf-8'), default_flow_style = False)

def convert_chars(tsu_path, serverd_path):
    f2 = _chars_serverd(serverd_path)
    yaml.dump(f2, open(tsu_path.replace('_sample', ''), 'w', encoding = 'utf-8'), default_flow_style = False)
       
def _convert():
    sdb = 'base/'
    sdc = 'base/scene/'
    cs = 'config_sample/'
    case = convert_config(cs + 'config.yaml', sdb + 'settings.ini') + '/'
    convert_areas(cs + 'areas.yaml', sdc + case + 'areas.ini')
    convert_music(cs + 'music.yaml', sdb + 'musiclist.txt')
    convert_chars(cs + 'characters.yaml', sdc + case + 'init.ini')
    
    
    
serverd = _config_serverd('base/settings.ini')

convert_config('config_sample/config.yaml', 'base/settings.ini')
_convert()
#print(serverd)