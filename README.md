# scripts_sets
Record script files written in daily study and work
记录日常学习工作中编写的脚本文件

## Image video conversion
1. my_img2video.py

   - Convert continuous image frames to video (FPS can be specified)

      ```shell
      ${DATASET_ROOT_FOLDER}
      └───path_to_images
      	└───xxx001.mp4 (dir)
          	└───xxx001.png/jpg/jpeg/webp
          	└───xxx002.png/jpg/jpeg/webp
          	...
          └───xxx002.mp4 (dir)
              ...
      ```

   - We save the video to path_to_videos. Please run the following code to do this

      ```
      python my_img2video.py \
      --input_dir path_to_images \
      --output_dir path_to_videos \
      --fps 25
      --workers=4
      ```

      

   - The output folder tree:

      ```shell
      ${DATASET_ROOT_FOLDER}
      └───path_to_videos
      	└───xxx001.mp4
          └───xxx002.mp4
              ...
      ```

2. 
