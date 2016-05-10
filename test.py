#!/usr/bin/env python
from os.path    import exists, isfile, join
from os         import system, listdir, getcwd, remove, rename
from fileinput  import input
from time       import sleep
from subprocess import call
from subprocess import Popen, PIPE
from re         import findall
from shutil     import move

global audio_format
global video_format

global extracted_audio_file
global extracted_video_file

audio_format = ''
video_format = ''

extracted_video_file = ''
extracted_audio_file = ''


current_path = getcwd ()
onlyfiles = [ f for f in listdir(current_path) if isfile(join(current_path,f)) ]

def rename_extn (video_file_name):
   new_video_file_name = video_file_name.replace ('.m4v', '.mp4')
   return (new_video_file_name)

def rename_file (video_file_name_extn, extn):
    
    
    # Strip extension
    video_file_name = video_file_name_extn[0:len(video_file_name_extn)-4]
    
    new_video_file_name = video_file_name.replace ('.', ' ')
    new_video_file_name = new_video_file_name.replace ('- [2x', 'S02E')
    new_video_file_name = new_video_file_name.replace ('] -', '')
    new_video_file_name = new_video_file_name.replace (' 720p HDTV X264-DIMENSION', ' ')
    new_video_file_name = new_video_file_name.replace (' 720p HDTV x264-0SEC', ' ')
    new_video_file_name = new_video_file_name.replace (' PROPER 720p HDTV x264-KILLERS', ' ')
    new_video_file_name = new_video_file_name.replace (' 720p HDTV x264-FLEET', ' ')
    new_video_file_name = new_video_file_name.replace (' 1080p WEB-DL DD5 1 H 264-NTb', ' ')
    new_video_file_name = new_video_file_name.replace (' 2014', '')
    new_video_file_name = new_video_file_name.replace (' 2015', '')
    new_video_file_name = new_video_file_name.replace (' 1080p', '')
    new_video_file_name = new_video_file_name.replace (' 720p', '')
    new_video_file_name = new_video_file_name.replace (' 480p', '')
    new_video_file_name = new_video_file_name.replace (' HDTV', '')
    new_video_file_name = new_video_file_name.replace (' BluRay', '')
    new_video_file_name = new_video_file_name.replace (' x264', '')
    new_video_file_name = new_video_file_name.replace (' XviD', '')
    new_video_file_name = new_video_file_name.replace (' DVDRip', '')
    new_video_file_name = new_video_file_name.replace (' DD5', '')
    new_video_file_name = new_video_file_name.replace (' H 264', '')
    new_video_file_name = new_video_file_name.replace (' WEB-DL', '')
    new_video_file_name = new_video_file_name.replace ('-KILLER', '')
    new_video_file_name = new_video_file_name.replace ('-DIMENSION', '')
    new_video_file_name = new_video_file_name.replace ('X264', '')
    
    new_video_file_name = new_video_file_name.replace (' - Day 7 - [7x', ' S07E')


    return (new_video_file_name + extn)


def repackage_to_mp4 (video_file_name_mkv):


    audio_format = ''
    video_format = ''

    if (isfile(video_file_name_mkv)):
        
        print 'Processing ' + video_file_name_mkv + '\n'
        
        # Strip .mkv extension
        video_file_name = video_file_name_mkv[0:len(video_file_name_mkv)-4]
        
        # Generate info file
        info_file = video_file_name + '.txt'
        f = open ('script.sh', 'w+')
        script = './mkvmerge -i ' + '\'' + video_file_name_mkv + '\' > \'' + info_file + '\''
        f.write (script)
        f.close ()
        system ('chmod +x script.sh')
        system ('./script.sh')
        remove ('script.sh')

        # Identify video and audio tracks inside mkv files
        for each_line in input(info_file):


            if (each_line.find('video') > 0):

                if (each_line.find ('h.264')):
                    video_track_num = each_line[9]
                    video_format = '.h264'

            if (each_line.find('audio') > 0):

                if (each_line.find ('AAC') > 0):
                    audio_track_num = each_line[9]
                    audio_format = '.aac'

                elif (each_line.find ('AC3') > 0 or each_line.find ('EAC3') > 0 or each_line.find ('AC-3') > 0 or each_line.find ('E-AC-3') > 0):
                    audio_track_num = each_line[9]
                    audio_format = '.ac3'

                elif (each_line.find ('DTS') > 0):
                    audio_track_num = each_line[9]
                    audio_format = '.dts'

                elif (each_line.find ('MP3') > 0):
                    audio_track_num = each_line[9]
                    audio_format = '.mp3'

                elif (each_line.find ('Vorbis') > 0):
                    audio_track_num = each_line[9]
                    audio_format = '.ogg'

        if (video_format):
            extracted_video_file = video_file_name + video_format
        else:
            print 'Unknown Video Format\n'
            for each_line in input(info_file):
                print each_line
            exit ()
    
        if (audio_format):
            extracted_audio_file = video_file_name + audio_format
        else:
            print 'Unknown Audio Format\n'
            for each_line in input(info_file):
                print each_line
            exit ()

    
        # mkvextract /x/y/z/video.mkv 0:video.h.264 1:audio.aac
        cmd = './mkvextract tracks '
        cmd = cmd + '\'' + video_file_name_mkv + '\''
        cmd = cmd + ' ' + video_track_num + ':\'' + video_file_name + video_format + '\''
        cmd = cmd + ' ' + audio_track_num + ':\'' + video_file_name + audio_format + '\''
        system (cmd)



        # Special handling for Vorbis OGG files. They must be converted to mp3 first
        if (audio_format == '.ogg'):
            system ('python ogg2mp3.py ' + video_file_name + audio_format + ' ' + video_file_name + '.mp3')
            audio_format = '.mp3'
            # Remove ogg file
            remove (extracted_audio_file)
            extracted_audio_file = extracted_audio_file.replace('.ogg', '.mp3')
    
    
    
        new_video_file_name = video_file_name + '.mp4'
        video_file_name_mp4 = rename_file (new_video_file_name, '.mp4')

        #        mkvinfo_extract = Popen ('./mkvinfo \'a.mkv\'|grep frames', shell=True, stdout=PIPE).stdout.read()
        mkvinfo_extract = Popen ('./mkvinfo \'' + video_file_name_mkv + '\'|grep frames', shell=True, stdout=PIPE).stdout.read()
        fps = findall ('\d+\.\d+ frames', mkvinfo_extract)[0].strip (' frames')


        # Merge
        # ./mp4box -fps 23.976 -add a.h264 -add a.ac3 a.mp4
        MP4Box_cmd = './MP4Box -quiet -fps ' + fps + ' -add \'' + extracted_video_file + '\' -add \'' + extracted_audio_file + '\' \'' + video_file_name_mp4 + '\''
        print MP4Box_cmd
        # system ('./MP4Box -quiet -fps ' + fps + ' -add \'' + extracted_video_file + '\' -add \'' + extracted_audio_file + '\' \'' + video_file_name_mp4 + '\'')
        system (MP4Box_cmd)
        remove (video_file_name + '.txt')
        remove (extracted_video_file)
        remove (extracted_audio_file)

        # Remove original mkv file if the conversion was successful
        if (isfile (video_file_name_mp4)):
            remove (video_file_name_mkv)
            move (video_file_name_mp4, 'rename/' + video_file_name_mp4)


for i in onlyfiles:
    length = len (i)
    # Check if the extension is .mkv
    if (i.find ('.mkv') == length - len('.mkv')):
        repackage_to_mp4 (i)
    
    # Check if the extension is .mp4
    if (i.find ('.mp4') == length - len('.mp4')):
        old_filename_mp4 = i
        new_filename_mp4 = rename_file (i, '.mp4')
        if (old_filename_mp4 != new_filename_mp4):
            rename (old_filename_mp4, new_filename_mp4)
            move (new_filename_mp4, 'rename/' + new_filename_mp4)

    # Check if the extension is .avi
    if (i.find ('.avi') == length - len('.avi')):
        old_filename_avi = i
        new_filename_avi = rename_file (i, '.avi')
        if (old_filename_avi != new_filename_avi):
            rename (old_filename_avi, new_filename_avi)
            move (new_filename_avi, 'rename/' + new_filename_avi)


    # Check if the extension is .m4v
    if (i.find ('.m4v') == length - len('.m4v')):
        new_filename_mp4 = rename_extn (i)
        rename (i, new_filename_mp4)
        move (new_filename_mp4, 'rename/' + new_filename_mp4)
