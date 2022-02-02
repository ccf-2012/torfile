import torrent_parser as tp
import os, time, re
import argparse
# import logging

parser = argparse.ArgumentParser(
    description='Clean torrent file.')
parser.add_argument('-f', '--torrent', type=str, required=True, help='the .torrent file to be cleaned.')
parser.add_argument('-a', '--announce', type=str, default='', help='the annount url(with your passkey).')
parser.add_argument('-s', '--save-path', type=str, default='.', help='the path that saves new created .torrent.')
parser.add_argument('--clean', action='store_true', help='clean the torrent.')
ARGS = parser.parse_args()

ARGS.save_path = os.path.expanduser(ARGS.save_path)

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.addHandler(logging.StreamHandler(sys.stdout))

def torrent_info(torrent_filepath):
    data = tp.parse_torrent_file(torrent_filepath)
    if 'info' not in data:
        print('ERROR: wrong torrent file.')
        return 

    for k in data.keys():
        if k == 'info':
            for i in data['info']:
                if i not in  ['pieces', 'files']:
                    print('info - ', i, ': ', data['info'][i])
        elif k == 'announce':
            m = re.match(r'(https?://[^/]+/)', data['announce'])
            if m:
                astr = m.group(1)
                print('announce: ' + astr)
        else:
            print(k, ': ', data[k])


def torrent_clean(torrent_filepath, new_announce, save_path):
    tp_src = tp.parse_torrent_file(torrent_filepath)
    if 'info' not in tp_src:
        print('Torrent file error.')
        return 
    tp_dst = {}
    tp_dst['announce'] = new_announce
    tp_dst['creation date'] = int(time.time()) 
    # data['created by'] = 'uTorrent/2210'
    tp_dst['created by'] = tp_src['created by']
    tp_dst['info'] = {}
    tp_dst['info']['name'] = tp_src['info']['name']
    tp_dst['info']['pieces'] = tp_src['info']['pieces']
    tp_dst['info']['files'] = tp_src['info']['files']
    tp_dst['info']['private'] = 1
    tp_dst['info']['source'] = ''
    
    new_torrent_path = os.path.join(save_path, tp_dst['info']['name']+ '.torrent')
    tp.create_torrent_file(new_torrent_path, tp_dst)


def main():
    if ARGS.clean:
        torrent_clean(ARGS.torrent, ARGS.announce, ARGS.save_path)
    else:
        torrent_info(ARGS.torrent)

if __name__ == '__main__':
    main()
