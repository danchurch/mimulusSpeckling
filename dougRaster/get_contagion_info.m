
% Moves through the data and extracts contagion information.
folder_path = 'Rotated_and_Cropped/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);

for i = 1:length(pic_files)
    fprintf('Processing Data File %d\n',i);
 
 
  %   Processing the current sameple_name_file photo:
      sample_name_file = pic_files(i).name;
      pic = join([folder_path, sample_name_file]);
   
      load(pic);   %This should produce the "Petals" data structure/
  
      Name{i}=Petals.Name;
      Left(i)=Petals.Contagion(1);
      Right(i)=Petals.Contagion(2);
      Mid(i)=Petals.Contagion(3);
    
end

% Save the new information:

T=table(Name',Left',Right',Mid');

fprintf('columns are Left, Right, Mid\n');

ss=join([dirstr,'/',folder_path,'ContagionData2.mat']);
save(ss, 'T');

writetable(T,'ContagionTable2.xls');
