
% Use this version to cluster by hand using "GraphOK.mat" created using 
%  NOTE that the folder_path may need to be re-written on line 9.
%  Only works after the matlab file "GraphOK.mat" has been created using
%  

warning('off');  % Warnings will be issued from kmeans- annoying!

load GraphOK;

folder_path = 'Rotated_and_Cropped/';
dirstr=pwd; % A string with the current directory
filestr=strcat(folder_path,'*.JPG');
pic_files = dir(filestr);

for i = 1:length(pic_files)

    fprintf('Processing Image %d\n',i);
 
if info(i)==1

  % Processing the current sameple_name_file photo:
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
   
  % Process the photo, put the data in "Petals":
    F = imread(pic);
    lab_he=rgb2lab(F);
    
    % Transform the RGB values to LAB scales (more grey tones)
    ab=double(lab_he(:,:,2:3));
    nrows=size(ab,1);
    ncols=size(ab,2);
    ab=reshape(ab,nrows*ncols,2);
    
    %Initial clustering:
     centers=[-0.1694 0.3045; -1.8839   47.4551; 28.1936   21.6839];
     [cluster_idx,~]= kmeans(ab,3,'MaxIter',1,'Start',centers);
     pixel_labels=reshape(cluster_idx,nrows,ncols);
     
    figure(1)
    image(F);
    axis equal; axis off;
    
    figure(2)
    subplot(2,1,1);
    idx1=find(cluster_idx==1); idx2=find(cluster_idx==2); idx3=find(cluster_idx==3);
    plot(ab(idx1,1),ab(idx1,2),'k.'); hold on
    plot(ab(idx2,1),ab(idx2,2),'y*');
    plot(ab(idx3,1),ab(idx3,2),'r^'); hold off
    axis tight
    
    subplot(2,1,2);
    imagesc(pixel_labels,[1,3]);
    axis equal; axis off;
    
    figure(3)
    plot(ab(idx1,1),ab(idx1,2),'g.'); hold on
    plot(ab(idx2,1),ab(idx2,2),'y*');
    plot(ab(idx3,1),ab(idx3,2),'r^'); 
    plot(centers(:,1),centers(:,2),'k^');
    hold off
    
    iters=0;
    MaxIters=20;
    
      % Loop through getting new input centers:    
 
 while 1
    
    fprintf('Locate new centers in the order: Black, Yellow, Red...\n');
    figure(3)
    [x,y]=ginput(3);
    centers(:,1)=x; centers(:,2)=y;
     
     
    [cluster_idx,~]= kmeans(ab,3,'MaxIter',1,'Start',centers);
    pixel_labels=reshape(cluster_idx,nrows,ncols);
    
    figure(2)
    subplot(2,1,1);
    idx1=find(cluster_idx==1); idx2=find(cluster_idx==2); idx3=find(cluster_idx==3);
    plot(ab(idx1,1),ab(idx1,2),'k.'); hold on
    plot(ab(idx2,1),ab(idx2,2),'y*');
    plot(ab(idx3,1),ab(idx3,2),'r^'); hold off
    axis tight
    
    subplot(2,1,2);
    imagesc(pixel_labels,[1,3]);
    axis equal; axis off;
    
    figure(3)
    plot(ab(idx1,1),ab(idx1,2),'g.'); hold on
    plot(ab(idx2,1),ab(idx2,2),'y*');
    plot(ab(idx3,1),ab(idx3,2),'r^'); 
    plot(centers(:,1),centers(:,2),'k^');
    hold off
    
    s1=input('Quit? (y/n) ','s');
    
    iters=iters+1;
    if iters>MaxIters
        break
    elseif strcmp(s1,'y');
        break
    else
        fprintf('Continuing...\n');
    end
        
    
 end
 
%% The following code is to create and output the Petals structure 

   pixel_labels=reshape(cluster_idx,nrows,ncols);
   background = pixel_labels(1);

    % Store the cluster information in Petals structure:
    Petals.color_centers=centers;
    
    %% Separate the petals clustering in position space

    temp=(pixel_labels~=background); % temp is a logical array that can be plotted

    index=find(temp);   % "index" is a linear indexing of the 1's in temp (it identifies the petals)
    [y, x] = ind2sub(size(pixel_labels),index);  % Converts the vector "index" back into an array of positions.

    % pos is the position index (1,2,3), and pos_cluster_center returns the
    % centers of the three petals.
    [pos, pos_cluster_center] = kmeans([y, x],3,'distance','sqEuclidean','Replicates',3);
    color=cluster_idx(cluster_idx~=background);  
    loc_color = [x, y, pos, color]; % pixel row, column, then position index, then color index.

    sortx = sortrows(loc_color);  % Default sort is on first column (x-coordinate)
    left = sortx(50,3);           % Ad-hoc assignment for "left"
    left_petal = loc_color(pos==left,:);

    right = sortx(end-50,3);
    right_petal = loc_color(pos==right,:);

    mid = 6 - left - right;
    mid_petal = loc_color(pos==mid,:);

    % Save the information in "data"
    Petals.left.data = left_petal;
    Petals.right.data = right_petal;
    Petals.mid.data = mid_petal;

 % Red and yellow pixel counts:   
    tbl=tabulate(left_petal(:,4));
    [nrow,~]=size(tbl);
    if nrow==2
        fprintf('Flag %s, left\n',pic);
        tbl(3,:)=[3,0,0];
    end
    Petals.left.counts=tbl(2:3,2)';
    Petals.left.percents=tbl(2:3,3)';
    
    tbl=tabulate(right_petal(:,4));
    [nrow,~]=size(tbl);
    if nrow==2
         fprintf('Flag %s, right\n',pic);
        tbl(3,:)=[3,0,0];
    end
    Petals.right.counts=tbl(2:3,2)';
    Petals.right.percents=tbl(2:3,3)';
    
    tbl=tabulate(mid_petal(:,4));
    [nrow,~]=size(tbl);
    if nrow==2
         fprintf('Flag %s mid\n',pic);
        tbl(3,:)=[3,0,0];
    end
    Petals.mid.counts=tbl(2:3,2)';
    Petals.mid.percents=tbl(2:3,3)';

   sample_name = sample_name_file(1:end-4);
 %   processed_data{i} = Petals;
 %   processed_data{i}.Name=sample_name;
    Petals.Name=sample_name;
    Petals.fullName=pic;

  % Output the data for this photo using the photos name:
    
    ss=join([dirstr,'/',folder_path,sample_name,'.mat']);
    save(ss,'Petals');

end

end

 
 warning('on');
    
