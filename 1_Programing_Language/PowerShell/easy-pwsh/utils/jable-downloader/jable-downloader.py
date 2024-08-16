import tqdm
import argparse

import os
import re
import copy
import subprocess

from functools import partial
from concurrent import futures

import m3u8
from Crypto.Cipher import AES

import requests
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def downloadM3U8(url, folderPath):

    """
    .SYNOPSIS
        Download M3U8 file from the given url, and get all the ts urls from the m3u8 file.
        Also, make a decryption object for the ts files if needed.

    .PARAMETER url
        The url of the jable video you want to download.
    .PARAMETER folderPath
        The path of the folder to save the downloaded files.

    .EXAMPLE
        downloadM3U8('https://jable.tv/videos/mukc-032/', 'D:/Temp') 
    """

    # set the selenium driver 
    options = Options() 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36')
    driver = webdriver.Chrome(options=options)
    driver.get(url=url)

    # get the m3u8 url of the jable video
    m3u8urls = re.findall("https://.+m3u8", driver.page_source)
    m3u8url = m3u8urls[0]

    # download the m3u8 file
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    m3u8file = os.path.join(folderPath, f'{url.split("/")[-2]}.m3u8')
    urllib.request.urlretrieve(m3u8url, m3u8file)
    # load the m3u8 file
    m3u8obj = m3u8.load(m3u8file)
    downloadUrl = '/'.join(m3u8url.split('/')[:-1])

    # get the m3u8 uri and iv
    m3u8uri = ''                        # uri: uniform resource identifier
    m3u8iv = ''                         # iv: initialization vector
    for key in m3u8obj.keys:
        if key:
            m3u8uri = key.uri
            m3u8iv = key.iv

    # make a decryption object
    if m3u8uri:                         # ci: cipher instance
        m3u8keyUrl = downloadUrl + '/' + m3u8uri
        m3u8key = requests.get(m3u8keyUrl, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        }, timeout=10).content
        iv = m3u8iv.replace("0x", "")[:16].encode()
        ci = AES.new(m3u8key, AES.MODE_CBC, iv) 
    else:
        ci = ''                     

    # get all the ts urls 
    tsUrls = []                         # ts: transport stream
    for seg in m3u8obj.segments:
        tsUrls.append(downloadUrl + '/' + seg.uri)

    os.remove(m3u8file)
    if not os.listdir(folderPath):
        os.rmdir(folderPath)

    return tsUrls, ci 


def downloadTS(pbar, downloadList, ci, folderPath, tsUrl):
    fileName = tsUrl.split('/')[-1][0:-3]
    saveName = os.path.join(folderPath, fileName + ".ts")
    if os.path.exists(saveName):
        downloadList.remove(tsUrl)
        pbar.update(1)
    else:
        response = requests.get(tsUrl, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        }, timeout=10)
        if response.status_code == 200:
            content_ts = response.content
            if ci:
                content_ts = ci.decrypt(content_ts)
            with open(saveName, 'wb') as f:
                f.write(content_ts)
            downloadList.remove(tsUrl)
            pbar.update(1)
        else:
            ...


def downloadTSList(tsUrls, ci, folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

    downloadList = copy.deepcopy(tsUrls)

    pbar = tqdm.tqdm(total=len(downloadList))

    while downloadList:
        with futures.ThreadPoolExecutor(max_workers=32) as executor:
            executor.map(partial(downloadTS, pbar, downloadList, ci, folderPath), downloadList)


def mergeTSFiles(tsUrls, tsFolderPath, savePath):

    with open(savePath, 'wb') as f:
        for ts in tqdm.tqdm(tsUrls):
            tsName = ts.split('/')[-1][0:-3]
            tsPath = os.path.join(tsFolderPath, tsName + ".ts")
            with open(tsPath, 'rb') as f1:
                f.write(f1.read())

    for ts in tsUrls:
        tsName = ts.split('/')[-1][0:-3]
        tsPath = os.path.join(tsFolderPath, tsName + ".ts")
        os.remove(tsPath)
    if not os.listdir(tsFolderPath):
        os.rmdir(tsFolderPath)


def downloadCover(url, folderPath):

    # set the selenium driver 
    options = Options() 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--headless')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36')
    driver = webdriver.Chrome(options=options)
    driver.get(url=url)

    if not os.path.exists(folderPath):
        os.mkdir(folderPath)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cover_name = soup.find('meta', property='og:image')['content'].split('/')[-1]
    cover_path = os.path.join(folderPath, cover_name)
    urllib.request.urlretrieve(soup.find('meta', property='og:image')['content'], cover_path)


def ffmpegEncode(input_path, output_path):
    command = [
        'ffmpeg', '-i', input_path, 
        '-c', 'copy', '-bsf:a', 
        'aac_adtstoasc', '-movflags', 
        '+faststart', output_path
    ]

    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        print(result.stderr)
        return False

    return True


def isJableVideoUrl(url):
    if re.match(r'.*jable.tv/videos/.*/', url):
        return True
    else:
        return False


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, nargs='+', default=None, help='the url of the jable video you want to download')
    parser.add_argument('-p', '--folderPath', type=str, default=None, help='the path of the folder to save the downloaded files')

    args = parser.parse_args()

    for url in args.url:
        if not isJableVideoUrl(url):
            print(f'Invalid jable video path: {url}')
            continue

        if not args.folderPath:
            args.folderPath = os.getcwd()
        if not os.path.exists(args.folderPath):
            os.makedirs(args.folderPath)

        folderPath = os.path.join(args.folderPath, url.split('/')[-2])

        # coverFolderPath = os.path.join(folderPath, 'cover')
        coverFolderPath = folderPath
        m3u8FloderPath  = os.path.join(folderPath, 'm3u8')
        tsFloderPath    = os.path.join(folderPath, 'ts')
        videoFilePath   = os.path.join(folderPath, url.split('/')[-2] + '.mp4')
        encodeFilePath  = os.path.join(folderPath, 'f_' + url.split('/')[-2] + '.mp4')

        downloadCover(url, coverFolderPath)
        tsUrls, ci = downloadM3U8(url, m3u8FloderPath)
        downloadTSList(tsUrls, ci, tsFloderPath)
        mergeTSFiles(tsUrls, tsFloderPath, videoFilePath)
        if ffmpegEncode(videoFilePath, encodeFilePath):
            print('Encode success')
            os.remove(videoFilePath)
            os.rename(encodeFilePath, videoFilePath)
        else:
            print('Encode failed')