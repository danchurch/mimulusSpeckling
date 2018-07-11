function plot_clusters(pic)

cd raw_data

   F = imread(pic);
    lab_he=rgb2lab(F);
    
    % Transform the RGB values to LAB scales (more grey tones)
    ab=double(lab_he(:,:,2:3));
    nrows=size(ab,1);
    ncols=size(ab,2);
    ab=reshape(ab,nrows*ncols,2);
    % reshape to be just the L,A colors as a p by 2 array


    %% Cluster the image in color space

    nColors=3;
    %Give it initial centers, so we can be confident which label is which
    %color.
    initial_centers = [ -2 2 ;-9 60.5, ;  31 33 ] ;
    [cluster_idx,cluster_center]= kmeans(ab,nColors,'distance','sqEuclidean','Start',initial_centers);
    pixel_labels1=reshape(cluster_idx,nrows,ncols);
    
    figure(1)
    image(F);
    axis equal; axis off;
    %[F1,map1]=frame2im(getframe);
    
    figure(2)
    subplot(2,2,1);
    idx1=find(cluster_idx==1); idx2=find(cluster_idx==2); idx3=find(cluster_idx==3);
    plot(ab(idx1,1),ab(idx1,2),'k.'); hold on
    plot(ab(idx2,1),ab(idx2,2),'y*');
    plot(ab(idx3,1),ab(idx3,2),'r^'); hold off
    axis tight
    
    subplot(2,2,3);
    imagesc(pixel_labels1,[1,3]);
    axis equal; axis off;
    %[G1,map2]=frame2im(getframe);
    %
    %figure(4)
    %FG=imfuse(F1,G1);
    %imshow(FG);
    
    
    %% Redo the clustering using fixed centers...
    
    centers=[-0.1694 0.3045; -1.8839   47.4551; 28.1936   21.6839];
    [cluster_idx,~]= kmeans(ab,3,'MaxIter',1,'Start',centers);
    pixel_labels2=reshape(cluster_idx,nrows,ncols);
    
    subplot(2,2,2);
    idx1=find(cluster_idx==1); idx2=find(cluster_idx==2); idx3=find(cluster_idx==3);
    plot(ab(idx1,1),ab(idx1,2),'k.'); hold on
    plot(ab(idx2,1),ab(idx2,2),'y*');
    plot(ab(idx3,1),ab(idx3,2),'r^'); hold off
    axis tight
    %title('Clusters in AB space, using fixed centers');
    
    subplot(2,2,4);
    imagesc(pixel_labels2,[1,3]);
    axis equal; axis off;
    
    %% Hybrid clustering-  Use kmeans for the background, then fixed centers for yellow/red.
       initial_centers = [ -2 2 ;-9 60.5, ;  31 33 ] ;
       [cluster_idx,cluster_center]= kmeans(ab,nColors,'distance','sqEuclidean','Start',initial_centers);
       centers=[cluster_center(1,:); -1.8839   47.4551; 28.1936   21.6839];
       for j=1:length(cluster_idx)
           if cluster_idx(j)~=1
               d1=norm(ab(j,:)-centers(2,:));
               d2=norm(ab(j,:)-centers(3,:));
               if d1<=d2
                   cluster_idx(j)=2;
               else
                   cluster_idx(j)=3;
               end
           end
       end
       
    pixel_labels3=reshape(cluster_idx,nrows,ncols);
    
    figure(3)
    subplot(2,1,1);
    idx1=find(cluster_idx==1); idx2=find(cluster_idx==2); idx3=find(cluster_idx==3);
    plot(ab(idx1,1),ab(idx1,2),'k.'); hold on
    plot(ab(idx2,1),ab(idx2,2),'y*');
    plot(ab(idx3,1),ab(idx3,2),'r^'); hold off
    axis tight
    %title('Clusters in AB space, using fixed centers');
    
    subplot(2,1,2);
    imagesc(pixel_labels3,[1,3]);
    axis equal; axis off;
    
 cd ..
 
    
