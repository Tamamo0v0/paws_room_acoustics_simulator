import numpy as np
import pickle
import h5py
import os
import datetime
import tqdm



def hdf5_to_ambisonic(hdf5_path,
                      save_dir,
                      mic_pos_list,
                      mic_valid_list,
                      save_filename_prefix=""
                    ):

    with h5py.File(hdf5_path,"r") as hf:
        
        # print("hf[\"p\"].shape = ", hf["p"].shape)
        
        mic_pos_arrange = []
        #get saving order of mic info
        for id, pos in enumerate(mic_pos_list):
            pos_x = pos[0]
            pos_y = pos[1]
            
            #each element in list is [x_pos,y_pos,mic_id,sample_point_id]
            mic_pos_arrange.append([pos_y,pos_x+1,id,0])
            mic_pos_arrange.append([pos_y-1,pos_x,id,1])
            mic_pos_arrange.append([pos_y,pos_x-1,id,2])
            mic_pos_arrange.append([pos_y+1,pos_x,id,3])
        
        
        #hdf5文件存储顺序为：采样点y坐标升序，同y时按照x坐标升序
        # print(mic_pos_arrange)
        mic_pos_arrange = sorted(mic_pos_arrange)
        # print(mic_pos_arrange)
        
        output_list = [[None]*4]*len(mic_pos_list)
         
        sensor_data = hf["p"][0].copy()
        for index in range(sensor_data.shape[1]):
            arrange_data = mic_pos_arrange[index]
            sample_output = sensor_data[:,index]
            output_list[arrange_data[2]][arrange_data[3]] = sample_output
            
        output_list = np.array(output_list)

        mic_data = {
            "mic_data": output_list,
            "valid_mic": mic_valid_list
        }
        
        mic_data_output_path =  os.path.join(save_dir,save_filename_prefix + "_mic_data.pkl")

        pickle.dump(mic_data, open(mic_data_output_path, "wb"))
        print("Write out mic data to {}".format(mic_data_output_path))
        



if __name__ == "__main__":
    
    hdf5_to_ambisonic("/home/tianming/paws_room_acoustics_simulator/temp_hdf5/shoe_box_2025-01-07-23-28-40_0_Nx_256_Ny_256_dx_0.02_dy_0.02_Nt_1000_dt_1e-09_2025-01-07-23-28-40_kwave_output.h5",
                      "",
                      [[45,60],[100,100],[186,50]],
                      [1,2,3],
                      )