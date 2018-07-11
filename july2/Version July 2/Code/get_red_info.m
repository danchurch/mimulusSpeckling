
% Moves through the data and extracts red information.
%   Uses only the "good" files from GraphOK.
%  When finished, save/export the table.

load GraphOK;  %Info vector is 1 x 180 with zero (good), 1 (bad)


folder_path = 'raw_data/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);

kk=1;

for i = 1:length(pic_files)
    fprintf('Processing Data File %d\n',i);
 
    if info(i)==0
  %   Processing the current sameple_name_file photo:
      sample_name_file = pic_files(i).name;
      pic = join([folder_path, sample_name_file]);
   
      load(pic);   %This should produce the "Petals" data structure/
  
      Name{kk}=Petals.Name;
      Left(kk)=Petals.left.percents(2)/100;
      Right(kk)=Petals.right.percents(2)/100;
      Mid(kk)=Petals.mid.percents(2)/100;
      
      kk=kk+1;
      
    end
    
end

% Save the new information:

T=table(Name',Left',Right',Mid');

fprintf('columns are Left, Right, Mid\n');

ss=join([dirstr,'/',folder_path,'redData.mat']);
save(ss, 'T');



