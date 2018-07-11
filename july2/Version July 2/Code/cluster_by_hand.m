
% This script works for a single photo-  Use cluster_by_hand2 to go through the whole directory.


warning('off');  % Warnings will be issued from kmeans- annoying!

pic=input('What image file will be processed?  ','s');
cd raw_data
F = imread(pic);
cd ..
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
 
 fprintf('Final location of centers:\n');
 centers

save CenterData centers;   %Need to update this to include the photo filename.
 
 warning('on');
    
