import torrent_parser as tp
import os, time, re
import argparse
# import logging

parser = argparse.ArgumentParser(
    description='Clean torrent file.')
parser.add_argument('-f', '--torrent', type=str, required=True, help='the .torrent file to be cleaned.')
parser.add_argument('-a', '--announce', type=str, default='', help='the annount url(with your passkey).')
parser.add_argument('-s', '--save-path', type=str, default='.', help='the path that saves new created .torrent.')
parser.add_argument('--info', action='store_true', help='display the torrent info.')
ARGS = parser.parse_args()

ARGS.save_path = os.path.expanduser(ARGS.save_path)

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# logger.addHandler(logging.StreamHandler(sys.stdout))

def torrent_info(torrent_filepath):
    data = tp.parse_torrent_file(torrent_filepath)
    if 'info' not in data:
        print('Torrent file error.')
        return 
    print('name: ' + data['info']['name'])
    print('created by: ' + data['created by'])
    m = re.match(r'(https?://[^/]+/)', data['announce'])
    if m:
        astr = m.group(1)
        print('announce: ' + astr)


def torrent_clean(torrent_filepath, new_announce, save_path):
    data = tp.parse_torrent_file(torrent_filepath)
    if 'info' not in data:
        print('Torrent file error.')
        return 
    if 'publisher' in data:
        del data['publisher']
    if 'publisher-url' in data:
        del data['publisher-url']
    if 'website' in data:
        del data['website']
    if 'checksum' in data:
        del data['checksum']
    if 'identity' in data:
        del data['identity']
    if 'ttg_tag' in data['info']:
        del data['info']['ttg_tag']
    if 'announce-list' in data:
        del data['announce-list']
    if 'comment' in data:
        data['comment'] = ''
    if 'source' in data['info'] :
        data['info']['source'] = ''
    data['info']['private'] = 1
    data['announce'] = new_announce
    data['creation date'] = int(time.time()) 
    new_torrent_path = os.path.join(save_path, data['info']['name']+ '.torrent')
    data['created by'] = 'uTorrent/2210'
    tp.create_torrent_file(new_torrent_path, data)


def main():
    if ARGS.info:
        torrent_info(ARGS.torrent)
    else:
        torrent_clean(ARGS.torrent, ARGS.announce, ARGS.save_path)

if __name__ == '__main__':
    main()
