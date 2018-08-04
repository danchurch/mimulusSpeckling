%% Single_process processes a single flower sample
%  In this script, we pull in the image of a flower, we quantize the colors
%  to the best 3 using k-means clustering, then we split the flower image
%  into a left petal, right petal, middle petal.
%  
%  The data is stored in the structure "Petals", which is split into left,
%  right and middle.  Each of these has two arrays-
%  Petals.xxx.data = 4 dimensional array.  The first two values are the
%  (x,y) indices of the position of the pixel, the third value is an index
%  indicating if the petal is left, right or middle, and the fourth value
%  is the index of the color (using the original k-means output).

function Petals = single_process(pic)
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

    % cluster_idx is the cluster value for each point in the image (in ab)
    % cluster_center is 3 x 1, holding the 3 cluster centers.

    %pixel_labels is the new binary (trinary?) array of pixels that may be
    %displayed as an image
    pixel_labels=reshape(cluster_idx,nrows,ncols);

    % We assume the background color index can be pulled off the first pixel:
    background = pixel_labels(1);

    % Store the cluster information in Petals structure:
    Petals.color_centers=cluster_center;
    
    %% Separate the petals clustering in position space

    temp=(pixel_labels~=background); % temp is a logical array that can be plotted

    index=find(temp);   % "index" is a linear indexing of the 1's in temp (it identifies the petals)
    [y, x] = ind2sub(size(pixel_labels),index);  % Converts the vector "index" back into an array of positions.

    % pos is the position index (1,2,3), and pos_cluster_center returns the
    % centers of the three petals.
    [pos, pos_cluster_center] = kmeans([y, x],3,'distance','sqEuclidean','Replicates',3);

    % "color" is a vector that has size equal to the number of pixels in the
    % petals, and whose value is the original color index.  
    %
    % We note that "color", "index", "x", "y", "pos" all have the same size- 
    %  Which is the number of pixels that are making up the petals.

    color=cluster_idx(cluster_idx~=background);  

    %% Code without a "table" structure

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
 
end


   

    
