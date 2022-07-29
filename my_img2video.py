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
    for ext in opt.extensions:
        image_names += glob.glob(f'{opt.input_dir}/{video_name}/*.{ext}', recursive=True)
    image_names = sorted(image_names)
    if len(image_names)==0:
        print("video_name is empty")
        return
    image_list = list()
    for img_id, image_name in tqdm(enumerate(image_names),total=len(image_names),desc=f"{video_id}/{opt.video_length}"):
        image = Image.open(image_name).convert("RGB").resize((opt.size,opt.size))
        image_list.append(image)
   
    video_name=video_name if video_name[:-4]==".mp4" else video_name + '.mp4' 
    # print(image_list, video_name)
    # print(f'{opt.output_dir}/{video_name}')
    imageio.mimsave(os.path.join(opt.output_dir,video_name), image_list, fps=opt.fps)  



if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--input_dir', type=str, 
                        default="path_to_images",
                        help='the folder of the input files')
    parser.add_argument('--output_dir', type=str, 
                        default="path_to_videos",
                        help='the folder of the output files')
    parser.add_argument('--fps', type=int, default=25)
    parser.add_argument('--size', type=int, default=256)
    
    parser.add_argument('--workers', type=int, default=1)

    opt = parser.parse_args()
    os.makedirs(opt.output_dir, exist_ok=True)
    video_list=list()
    IMAGE_EXTENSIONS_LOWERCASE = {'jpg', 'png', 'jpeg', 'webp'}
    IMAGE_EXTENSIONS = IMAGE_EXTENSIONS_LOWERCASE.union({f.upper() for f in IMAGE_EXTENSIONS_LOWERCASE})
    extensions = IMAGE_EXTENSIONS
    opt.extensions=extensions
    
    pool = Pool(opt.workers)
    args_list = cycle([opt])
    video_list=sorted(os.listdir(opt.input_dir))
    opt.video_length = len(video_list)
    # import pdb;pdb.set_trace()
    video_ids=range(opt.video_length)
    print('Total number of videos:', opt.video_length)
    for data in pool.imap_unordered(run, zip(video_list, video_ids, args_list)):
        None
    
    print("Covert images to video done!")
