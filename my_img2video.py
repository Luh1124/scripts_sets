__author__="lihong"

import os
from turtle import done
import imageio
import argparse
import glob
from tqdm import tqdm
from PIL import Image
# from pandas import option_context
from itertools import cycle
from torch.multiprocessing import Pool, Process

def run(video_info):
    video_name, video_id, opt = video_info
    image_names = list()
    for ext in extensions:
        image_names += glob.glob(f'{opt.input_dir}/{video_name}/*.{ext}', recursive=True)
    image_names = sorted(image_names)
    image_list = list()
    for img_id, image_name in tqdm(enumerate(image_names),total=len(image_names),desc=f"{video_id}/{opt.video_length}"):
        image = Image.open(image_name).convert("RGB")
        image_list.append(image)
    
    imageio.mimsave(f'{opt.output_dir}/{video_name}', image_list, opt.fps)  # 指定质量参数10

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input_dir', type=str, 
                        default="/media/lh/luhssd/datasets/vox1/face-video-preprocessing/vox-png/test",
                        help='the folder of the input files')
    parser.add_argument('--output_dir', type=str, 
                        default="/media/lh/luhssd/datasets/vox1/face-video-preprocessing/video_format/test",
                        help='the folder of the output files')
    parser.add_argument('--fps', type=int, default=25)
    parser.add_argument('--workers', type=int, default=4)

    opt = parser.parse_args()
    os.makedirs(opt.output_dir, exist_ok=True)
    video_list=list()
    IMAGE_EXTENSIONS_LOWERCASE = {'jpg', 'png', 'jpeg', 'webp'}
    IMAGE_EXTENSIONS = IMAGE_EXTENSIONS_LOWERCASE.union({f.upper() for f in IMAGE_EXTENSIONS_LOWERCASE})
    extensions = IMAGE_EXTENSIONS

    pool = Pool(opt.workers)
    args_list = cycle([opt])
    video_list=sorted(os.listdir(opt.input_dir))
    opt.video_length = len(video_list)
    video_ids=range(opt.video_length)
    print('Total number of videos:', len(opt.video_length))
    for data in pool.imap_unordered(run, zip(video_list, video_ids, args_list)):
        None
    
    print("Covert images to video done!")
