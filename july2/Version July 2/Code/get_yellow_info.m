%Collates the yellow (and background) data that was computed by process_yellow.

folder_path = 'Rotated_and_Cropped2/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);

A=zeros(length(pic_files),6);

for i = 1:length(pic_files)
    
    fprintf('Processing Image %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
  % Process the photo, put the data in "Petals":
    load(pic);
    temp=rgb2gray(Petals.left.tape/255);
    A(i,1)=temp(1);
    temp=rgb2gray(Petals.right.tape/255);
     A(i,2)=temp(1);
    temp=rgb2gray(Petals.mid.tape/255);
     A(i,3)=temp(1);
    temp=rgb2gray(Petals.left.yellow/255);
     A(i,4)=temp(1);
    temp=rgb2gray(Petals.right.yellow/255);
     A(i,5)=temp(1);
    temp=rgb2gray(Petals.mid.yellow/255);
     A(i,6)=temp(1);
    
end

save YellowFromImages A


