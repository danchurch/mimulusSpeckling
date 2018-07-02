
% This script is an example of moving through all of the Matlab data
% files output by "process_init.m" and extracting graphical information. 

folder_path = 'raw_data/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);

%for i = 1:length(pic_files)



tt=randperm(180);
for k=1:50
    i=tt(k);
    fprintf('Processing Data File %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
    load(pic);   %This should produce the "Petals" data structure/
   
    fprintf('Pixel percents, left: %f %f\n',Petals.left.percents(1), Petals.left.percents(2));
    fprintf('Pixel percents, right: %f %f\n',Petals.right.percents(1), Petals.right.percents(2));
    fprintf('Pixel percents, mid: %f %f\n',Petals.mid.percents(1), Petals.mid.percents(2));   
    fprintf('Center 1: %f %f\n', Petals.color_centers(1,1),Petals.color_centers(1,2));
    fprintf('Center 2: %f %f\n', Petals.color_centers(2,1),Petals.color_centers(2,2));
    fprintf('Center 3: %f %f\n', Petals.color_centers(3,1),Petals.color_centers(3,2));
    fprintf('Filename %s\n',sample_name_file);
    fprintf('Press any key to continue (New graph is next)...\n');
    
    [ccA,ccB]=split_single_petal(Petals);

    pause;  % The pause command halts execution until any button is pressed.
    
end




