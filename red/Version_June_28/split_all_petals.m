
% This script is an example of moving through all of the Matlab data
% files output by "process_init.m" and extracting graphical information. 

folder_path = 'raw_data/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);

for i = 1:length(pic_files)
    
    fprintf('Processing Data File %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
    load(pic);   %This should produce the "Petals" data structure/
   
    [ccA,ccB]=split_single_petal(Petals);

    pause;  % The pause command halts execution until any button is pressed.
    
end




