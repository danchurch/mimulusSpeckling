%% This script runs through all of the photos in a given folder
% and produces a clustering and a mat file.  Note that on line 4, the folder path may need to be changed.

folder_path = 'Rotated_and_Cropped/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.JPG');
pic_files = dir(filestr);

for i = 1:length(pic_files)

    fprintf('Processing Image %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
  % Process the photo, put the data in "Petals":
    Petals = single_process(pic);
   
  % For now, keep the current photo data in "process_data" structure, which will hold
  %  the data for ALL photos.  If there are many photos, we might run out of memory.
    sample_name = sample_name_file(1:end-4);
 %   processed_data{i} = Petals;
 %   processed_data{i}.Name=sample_name;
    Petals.Name=sample_name;
    Petals.fullName=pic;

  % Output the data for this photo using the photos name:
    
    ss=join([dirstr,'/',folder_path,sample_name,'.mat']);
    save(ss,'Petals');
end




