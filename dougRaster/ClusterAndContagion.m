%% This script computes the "contagion" index for the flower photos.

% This script will go through the files in the named folder, extract the
% cluster indices, then call the contagion program.  The resulting files
% are stored in Petals.Clusters

% To collate the information, run "get_contagion_info"


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
    
    A = split2clusters(Petals);
    
  % Now include the binary information as part of the mat files.
  
    Petals.Clusters=A;
    
    fprintf('Contagion Processing\n');
  a1=contagion_clusters(A.left);
  a2=contagion_clusters(A.right);
  a3=contagion_clusters(A.mid);
  
  % Output the data for this photo using the photos name:
  Petals.Contagion=[a1,a2,a3]
  
    ss=join([dirstr,'/',folder_path,Petals.Name,'.mat']);
    save(ss,'Petals');

end
