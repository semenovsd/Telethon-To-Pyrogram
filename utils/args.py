import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        prog="tele-pyro",
        description="Script for convert telethon session file to pyrogram session file",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="telethon_session_file",
        required=False,
        # type=argparse.FileType('r'),
        type=str,
        default=None,
        help="Path to session file",
        metavar='/home/user/telethon/sessions/xxxxxxxxxxx.session'
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="telethon_session_dir",
        required=False,
        type=str,
        default=None,
        help="Path to dir with session files",
        metavar='/home/user/telethon/sessions'
    )
    parser.add_argument(
        "-p",
        "--pyro",
        dest="pyro_session_dir",
        required=False,
        # parser.add_argument('dest_file', type=argparse.FileType('w', encoding='latin-1'))
        type=str,
        default='./pyrogram',
        help="Path to save new pyrogram session file",
    )
    parser.add_argument(
        "--hash",
        dest="api_hash",
        required=False,
        type=str,
        default=None,
        help="App api_hash from https://my.telegram.org/apps",
    )
    parser.add_argument(
        "--id",
        dest="api_id",
        required=False,
        type=str,
        default=None,
        help="App api_id from https://my.telegram.org/apps",
    )
    return parser.parse_args()
