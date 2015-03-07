import sys, os, argparse
from subprocess import call

TEMP_VIDEO_NAME = '.ymdl_temp'
FNULL = open(os.devnull, 'w')

def main():
    args = parse_arguments()

    output_name = args.output_name
    audio_format = args.format
    verbose = args.verbose

    # execute the following programs
    youtube_dl(args.url, verbose)
    vlc(output_name, audio_format, verbose)

    # remove the temporary video file
    os.remove(TEMP_VIDEO_NAME)

    print('[Audio Extraction Complete]')
    print('[Created: {}.{}]'.format(output_name, audio_format))

    FNULL.close()

def parse_arguments():
    # argument defaults
    FORMAT_DEFAULT = 'flac'

    # argument help strings
    OUTPUT_NAME_HELP = 'desired output name without extension'
    URL_HELP = 'URL of the video to be converted'
    FORMAT_HELP = 'desired audio output format e.g. flac, mp3, aac'
    VERBOSE_HELP = 'show output from youtube-dl and VLC'

    parser = argparse.ArgumentParser()
    parser.add_argument('output_name', help = OUTPUT_NAME_HELP)
    parser.add_argument('url', help = URL_HELP)
    parser.add_argument('-f', '--format', default = FORMAT_DEFAULT,
                        help = FORMAT_HELP)
    parser.add_argument('-v', '--verbose', action = 'store_true',
                        help = VERBOSE_HELP)

    return parser.parse_args()

def youtube_dl(url, verbose):
    print('[Fetching Video]')

    youtube_dl_args = ['youtube-dl', '-o', TEMP_VIDEO_NAME, url]
    call(youtube_dl_args, stdout = None if verbose else FNULL)

def vlc(output_name, audio_format, verbose):
    print('[Extracting Audio]')

    vlc_args = [
        'vlc', '-I', 'dummy', '--no-sout-video', '--sout-audio', '--sout',
        '#transcode{{acodec={0}}}:std{{access=file,mux=raw,dst=./{1}.{0}}}'
        .format(audio_format, output_name), TEMP_VIDEO_NAME, 'vlc://quit'
    ]

    call(vlc_args, stdout = None if verbose else FNULL,
         stderr = None if verbose else FNULL)

if __name__ == '__main__':
    main()