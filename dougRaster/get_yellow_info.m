%Collates the yellow (and background) data that was computed by process_yellow.

folder_path = 'Rotated_and_Cropped/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);

A=zeros(length(pic_files),3);

for i = 1:length(pic_files)
    
    fprintf('Processing Image %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
  % Process the photo, put the data in "Petals":
    load(pic);
    temp=rgb2gray(Petals.left.yellow/255);
    A(i,1)=temp(1);
    temp=rgb2gray(Petals.right.yellow/255);
     A(i,2)=temp(1);
    temp=rgb2gray(Petals.mid.yellow/255);
     A(i,3)=temp(1);
    
     Name{i}=Petals.Name;
      Left(i)=A(i,1);
      Right(i)=A(i,2);
      Mid(i)=A(i,3);
      
end
% Save the new information:

T=table(Name',Left',Right',Mid');
writetable(T,'YellowData.xls');
save('YellowData.mat', 'T','A');



