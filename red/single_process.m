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

    Petals.left.prop_red=propred(left_petal(:,4));
    Petals.right.prop_red=propred(right_petal(:,4));
    Petals.mid.prop_red=propred(mid_petal(:,4));

    %% Clumpiness

    z_left=sqrt(((left_petal(:,1)-pos_cluster_center(left,2)).^2 + (left_petal(:,2)-pos_cluster_center(left,1))).^2);
    circleidx_left=linspace(min(z_left),max(z_left),200);
    colorz_left=[left_petal(:,4),z_left];
    
    for r=1:200

        circle_left=(colorz_left(z_left<=circleidx_left(r),:));
        prpr_left = propred(circle_left(:,1));
        circlereds_left(r) = prpr_left;
        rs_left(r)= r;
        
    end
    
    z_mid=sqrt(((mid_petal(:,1)-pos_cluster_center(mid,2)).^2 + (mid_petal(:,2)-pos_cluster_center(mid,1))).^2);
    circleidx_mid=linspace(min(z_mid),max(z_mid),200);
    colorz_mid=[mid_petal(:,4),z_mid];
    
    for r=1:200

        circle_mid=(colorz_mid(z_mid<=circleidx_mid(r),:));
        prpr_mid = propred(circle_mid(:,1));
        circlereds_mid(r) = prpr_mid;
        rs_mid(r)= r;

    end
    
    z_right=sqrt(((right_petal(:,1)-pos_cluster_center(right,2)).^2 + (right_petal(:,2)-pos_cluster_center(right,1))).^2);
    circleidx_right=linspace(min(z_right),max(z_right),200);
    colorz_right=[right_petal(:,4),z_right];

    for r=1:200

        circle_right=(colorz_right(z_right<=circleidx_right(r),:));
        prpr_right = propred(circle_right(:,1));
        circlereds_right(r) = prpr_right;
        rs_right(r)= r;

    end
    
    % Adding this info to the Petals structure
    Petals.right.pr_rad = [rs_right', circlereds_right'];
    Petals.left.pr_rad = [rs_left', circlereds_left'];
    Petals.mid.pr_rad = [rs_mid', circlereds_mid'];
    
%% Circle detection

    [centers, radii] = imfindcircles(pixel_labels, [10, 30],'ObjectPolarity','bright','Sensitivity',.95);
    Petals.centers = centers;
    Petals.radii = radii;
    pixel_labels(pixel_labels==background) = 0;
    pixel_labels(pixel_labels==2) = 0;
    Petals.clustered = pixel_labels;
    
end


    
%% Subroutines (This is a new feature of Matlab- We were not allowed to do this in older versions!)

    function prpr = propred(list)
        tbl = tabulate(list);

        % Corrected for the array below - tbl isn't a structure
        nums = tbl(:,2);
        nums(nums==0)=[];  % This removes any values with the number "0".

        if length(nums)==1
            prpr=1;
            return;
        end

        if length(nums)>2
            fprintf('Possible error in number of colors\n');
        end

        if nums(1)>nums(2)
            prpr = nums(2)/nums(1);

        else
            prpr = nums(1)/nums(2);
        end
    end

    
