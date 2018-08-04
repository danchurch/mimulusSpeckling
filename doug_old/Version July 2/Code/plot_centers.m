
% Go through all the data and plot the centers!  Only plot those centers
% that seemed to be OK (index in GraphOK.mat)...

load GraphOK;  %loads the vector "info", 0=OK, 1=Not OK.

folder_path = 'raw_data/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.mat');
pic_files = dir(filestr);
Numfiles=123;  %This is the number of zeros in "info"

Background=zeros(2,Numfiles);
CenterOne=zeros(2,Numfiles);
CenterTwo=zeros(2,Numfiles);

k=1;

for i = 1:181
    
    fprintf('Processing Data File %d\n',i);
 
  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
    load(pic);   %This should produce the "Petals" data structure/
   
  % Extract the relevant information:
  if info(i)==0
    Background(:,k)=Petals.color_centers(1,:)';
    CenterOne(:,k)=Petals.color_centers(2,:)';
    CenterTwo(:,k)=Petals.color_centers(3,:)';
    k=k+1;
  end
end

figure(1)
plot(Background(1,:),Background(2,:),'k.');
hold on
plot(CenterOne(1,:),CenterOne(2,:),'y*');
plot(CenterTwo(1,:),CenterTwo(2,:),'ro');
hold off

% For the colors, if we use 75 for the L value,
%  then the LAB and RGB color values (on a 255 scale) are:
%
% median(CenterOne')
%    -1.8839   47.4551  or [209, 184, 97]
% median(CenterTwo')    
%    28.1936   21.6839  or [245, 163, 145]
% median(Background')
%    -0.1694    0.3045  or [185, 185, 185]





