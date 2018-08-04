%% This is a driver for estimating the lacunarity of the folder of images.
%
% This code runs through the photos and individually calls "image_lacunarity" on binary versions
%  of the photos.  If the binary version does not yet exist, this code will also create it.


folder_path = 'Rotated_and_Cropped/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);

% initializing the structure we will fill with wonderful data
%processed_data = struct();

for i = 1:length(pic_files)
    
    fprintf('Processing Image %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
  % Process the photo, put the data in "Petals":
    load(pic);
    
%    if isfield(Petals,'Boxcount')
%        fprintf('Removing old structure\n');
%        Petals=rmfield(Petals,'Boxcount');
%    end
    
    if isfield(Petals,'Lacunarity')
        fprintf('Removing old structure\n');
        Petals=rmfield(Petals,'Lacunarity');
    end

% Create the binary clusters, if necessary
    if ~isfield(Petals,'Binary')
       fprintf('Calling split2binary\n');
       A = split2binary(Petals);
       Petals.Binary=A;
    end

    fprintf('Going into Lacunarity Code\n');
    [M1, ~] = image_lacunarity(Petals.Binary.left);
    [M2, ~] = image_lacunarity(Petals.Binary.right);
    [M3, ~] = image_lacunarity(Petals.Binary.mid);
    
    Petals.Lacunarity=[M1,M2,M3];

    % Output the results:
    
    ss=join([dirstr,'/',folder_path,Petals.Name,'.mat']);
    save(ss,'Petals');

end



