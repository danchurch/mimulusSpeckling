%Collates the yellow (and background) data that was computed by process_yellow.

folder_path = 'Sequenced_July_2018/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.JPG');
pic_files = dir(filestr);

Yellow=zeros(length(pic_files),3);
G=zeros(length(pic_files),1);

for i = 1:length(pic_files)
    
    fprintf('Processing Image %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
    NameFiles{i}=sample_name_file;
    
    %% Go into the manual subroutine- Have the user click the mouse on yellow.
    
    F=imread(pic);
    image(F);
    [x,y]=ginput(1);
    x=round(x); y=round(y);
    temp1=squeeze(F(y(1),x(1),:));
    Yellow(i,:)=temp1';
    temp2=rgb2gray(temp1'/255);
    G(i)=temp2(1);
    
end

T=table(NameFiles',Yellow(:,1),Yellow(:,2),Yellow(:,3),G);
writetable(T,'YellowStandard.xls');

save YellowStandard NameFiles Yellow G


