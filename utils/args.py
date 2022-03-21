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
        help="App api_hash from https://my.telegram.org/apps ",
    )
    parser.add_argument(
        "--id",
        dest="api_id",
        required=False,
        type=str,
        default=None,
        help="App api_id from https://my.telegram.org/apps ",
    )
    parser.add_argument(
        '-o',
        dest="overwrite",
        required=False,
        type=bool,
        nargs='?',
        const=True,
        default=False,
        help="Overwrite destination file if exist",
    )
    parser.add_argument(
        '--message',
        dest="send_msg_to",
        required=False,
        type=str,
        help="Send test message from client",
    )
    parser.add_argument(
        '--delete',
        dest="delete_source_file",
        required=False,
        type=bool,
        nargs='?',
        const=True,
        default=False,
        help="Delete source session file after success convert",
    )
    parser.add_argument(
        '--leave',
        dest="leave_all_chats",
        required=False,
        type=bool,
        nargs='?',
        const=True,
        default=False,
        help="Should client exit from all chats",
    )
    return parser.parse_args()
