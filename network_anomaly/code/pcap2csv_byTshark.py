import os
import argparse
import os.path

def command_line_args():
    """Helper called from main() to parse the command line arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--pcap', metavar='<input pcap file>',
                        help='pcap file to parse', required=True)
    parser.add_argument('--csv', metavar='<output csv file>',
                        help='csv file to create', required=True)
    args = parser.parse_args()
    return args

def main():
    """Program main entry"""
    args = command_line_args()

    os.system('tshark -r "{}" -T fields -E separator=, -E quote=d -E header=y -t u -e _ws.col.Time -e _ws.col.Protocol -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e tcp.len -e tcp.seq -e tcp.ack -e udp.srcport -e udp.dstport -e udp.length -e http.request.method -e http.request.uri -e http.user_agent -e http.connection -e http.host -e http.response.code -e http.server -e http.content_type -e http.content_length -e http.cache_control > "{}"'.format(args.pcap, args.csv))

if __name__ == '__main__':
    main()

