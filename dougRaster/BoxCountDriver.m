%% This is a driver for the box counting algorithm, which is typically used to estimate fractal dimension.

% Nice coding included:
% It also has an example of checking a structure for a field, and removing
% it if it is present.

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
    
    if isfield(Petals,'Boxcount')
        fprintf('Removing old structure\n');
        Petals=rmfield(Petals,'Boxcount');
    end
    
    
    [n1,r1] = boxcount(Petals.Binary.left);
    [n2,r2] = boxcount(Petals.Binary.right);
    [n3,r3] = boxcount(Petals.Binary.mid);
    
    Petals.Boxcount.left=[n1;r1];
    Petals.Boxcount.right=[n2;r2];
    Petals.Boxcount.mid=[n3;r3];

    % Output the results:
    
    ss=join([dirstr,'/',folder_path,Petals.Name,'.mat']);
    save(ss,'Petals');
end

% Here's the plot command:
% loglog(Petals.Boxcount.left(2,:),Petals.Boxcount.left(1,:),'bo-',Petals.Boxcount.mid(2,:),Petals.Boxcount.mid(1,:),'b*-',Petals.Boxcount.right(2,:),Petals.Boxcount.right(1,:),'ko-')


