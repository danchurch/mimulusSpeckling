%% Driver script for extract_yellow.  Will go get the yellow information and collate it.

folder_path = 'Rotated_and_Cropped/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);

for i = 1:length(pic_files)
    
    fprintf('Processing Image %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
  % Process the photo, put the data in "Petals":
    load(pic);
    Petals = extract_yellow(Petals);
   
  % Output the data for this photo using the photos name:
    
    ss=join([dirstr,'/',folder_path,Petals.Name,'.mat']);
    save(ss,'Petals');


end



