# coding:utf-8
#
# Python Script to Convert Subtitle formats from .srt to .ass 
# coded by ewwink, may 2017
#

import sys
import os
import re
import codecs
#import SubsceneUtilities

def fileopen(input_file):
    # strange output characters? add your file encoding here
    encodings = ["gb2312", "gbk", 'utf-16', "cp1252",  "big5", "utf-8"]
    tmp = ''
    for enc in encodings:
        try:
            with codecs.open(input_file, mode="rb", encoding=enc) as fd:
                tmp = fd.read()
                break
        except:
            #SubsceneUtilities.log('SRT2ASS:', enc + ' failed', 2)
            #print enc + ' failed'
            continue
    return [tmp, enc]


def srt2ass(input_file):
    if '.ass' in input_file:
        return input_file
    output_file = '.'.join(input_file.split('.')[:-1])
    output_file += '.ass'
    if not os.path.isfile(input_file):
        print input_file + ' not exist'
        return
    head_str = '''[Script Info]
; This is an Advanced Sub Station Alpha v4+ script.
Title: 
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubStyle,Arial,20,&H0300FFFF,&H00FFFFFF,&H00000000,&H02000000,-1,0,0,0,100,100,0,0,3,2,0,2,10,10,10,1

[Events]
Format: Layer, Start, End, Style, Actor, MarginL, MarginR, MarginV, Effect, Text'''
    
    src = fileopen(input_file)
    tmp = src[0]
    tmp = tmp.replace("\r", "")
    lines = tmp.split("\n")
    subLines = ''
    tmpLines = ''
    lineCount = 0

    for line in lines:
        line = line.replace(u'\xef\xbb\xbf', '')
        if re.match('^\d+$', line):
            if tmpLines:
                subLines += tmpLines + "\n"
            tmpLines = ''
            lineCount = 0
            continue
        else:
            if line:
                if re.match('-?\d\d:\d\d:\d\d', line):
                    line = line.replace('-0', '0')
                    tmpLines += 'Dialogue: 0,' + line + ',SubStyle,,0,0,0,,'
                    lineCount += 1
                else:
                    if lineCount < 2:
                        tmpLines += line
                        lineCount += 1
                    else:
                        tmpLines += '\N' + line
                        lineCount += 1

    subLines += tmpLines + "\n"

    subLines = re.sub(r'-?\d(\d:\d{2}:\d{2}),(\d{2})\d', '\\1.\\2', subLines)
    subLines = re.sub(r'\s+-->\s+', ',', subLines)
    # replace style
    subLines = re.sub(r'<([ubi])>', "{\\\\\g<1>1}", subLines)
    subLines = re.sub(r'</([ubi])>', "{\\\\\g<1>0}", subLines)
    subLines = re.sub(r'<font\s+color="?#(\w{2})(\w{2})(\w{2})"?>', "{\\\\c&H\\3\\2\\1&}", subLines)
    subLines = re.sub(r'</font>', "", subLines)

    output_str = head_str + '\n' + subLines
    output_str = output_str.encode(src[1])
    
    with open(output_file, 'wb') as output:
        output.write(output_str)
    
    output_file = output_file.replace('\\', '\\\\')
    return output_file


if len(sys.argv)>1:
    for name in sys.argv[1:]:
        srt2ass(name)
