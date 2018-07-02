
%Script to look at clusterings of specific files.


warning('off');   % kmeans will issue warnings when we fix the centers.

StrArray={'P258F1.JPG','P338F1.JPG','P339F2.JPG','P345F1.JPG','P403F1.JPG','P404F1.JPG','P426F1.JPG','P434F1.JPG','P440F1.JPG','P439F1.JPG'};

for i=1:length(StrArray)
    fprintf('Working on Image %s\n',StrArray{i});
    plot_clusters(StrArray{i});
    pause
end

warning('on');


