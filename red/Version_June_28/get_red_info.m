
% This script is an example of moving through all of the Matlab data
% files output by "process_init.m" and extracting information.  First, 
% we need to input the directory structure below (which is the same that process_init used)

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
   
  % Extract the relevant information:
    reddata(i,1) = Petals.left.prop_red;
    reddata(i,2) = Petals.right.prop_red;
    reddata(i,3) = Petals.mid.prop_red;

end

% Save the new information:

ss=join([dirstr,'/',folder_path,'redData.mat']);
save(ss, 'reddata');



