import numpy as np
import glob
import os
import json
import open3d as o3d

class FrameHandler():
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

        self.lidar_files = sorted(glob.glob(dataset_dir + '/lidar/*.pcd'))
        self.lidar_files = np.asarray(self.lidar_files)
        
        self.annos_files = sorted(glob.glob(dataset_dir + '/label/*.json'))
        self.annos_files = np.asarray(self.annos_files)
        
        print('dataset path: ', dataset_dir)
        print('# samples: ', len(self.lidar_files))

    def get_dataset_path(self):
        return self.dataset_dir

    def get_dataset_name(self):
        '''
            dytpe: str
        '''
        return self.dataset_dir.split('/')[-1]
    
    def get_dataset_len(self):
        return len(self.lidar_files)

    def get_frame_name(self, idx):
        frame_name = self.lidar_files[idx].split('/')[-1]
        frame_name = frame_name.split('.')[0]
        return frame_name


    def get_annos(self, idx):
        annos_file = self.annos_files[idx]
        annos = json.load(open(annos_file, "r"))

        # for debugging
        print('annos file: ', annos_file)
        print(annos)

        return annos       # x, y, z, l, w, h, heading, class

    def get_lidar(self, idx):
        '''
            load peak points
        '''
        lidar_file = self.lidar_files[idx]
        pcd = o3d.io.read_point_cloud(lidar_file) 
        points = np.asarray(pcd.points, dtype=np.float32)
        return points


    def get_img(self, idx):
        pass


    def __len__(self):
        return len(self.lidar_files)


    def __getitem__(self, idx):
        input_dict = {}

        # get frame info
        frame_name = self.get_frame_info(idx)
        input_dict['frame_name'] = frame_name

        # get lidar points
        points = self.get_lidar(idx)
        input_dict['points'] = points

        # get annotations
        annos = self.get_annos(idx)
        input_dict['gt_boxes'] = annos

        return input_dict 
