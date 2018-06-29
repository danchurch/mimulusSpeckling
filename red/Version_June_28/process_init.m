%% This script will run single_process on all .jpg
% in the current folder, with folder marked "raw_data",
% and output a single data structure in that same folder.

% The input filenames.  The "raw_data" folder should be in the same directory as this file.
%   The result is "pic_files", which is a Matlab data structure with information about the 
%   files in the directory (see the help file for "dir")
folder_path = 'raw_data/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.JPG');
pic_files = dir(filestr);

% initializing the structure we will fill with wonderful data
%processed_data = struct();

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
    processed_data{i} = Petals;
    processed_data{i}.Name=sample_name;
    Petals.Name=sample_name;
    Petals.fullName=pic;

  % Output the data for this photo using the photos name:
    
    ss=join([dirstr,'/',folder_path,sample_name,'.mat']);
    save(ss,'Petals');

end



