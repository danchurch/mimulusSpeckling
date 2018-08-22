clear;
close;
%% matlab structure directory
objDir="/Users/danthomas/Documents/speckling/make_polygons/matObjW_pol/";
%% working directory
wd="/Users/danthomas/Documents/speckling/center";
%% image directory
dougDir = "/Users/danthomas/Documents/speckling/dougRaster/Rotated_and_Cropped/"; 
cd(wd); %% goto working directory
margins = [0:.10:.50]; %% margin sizes to test
files = dir(dougDir + 'P*.mat');
for file = files';
%file.name = 'P258F1.mat'; %% delete this after debug
    disp(file.name)
    %% setup flower
    load(objDir + file.name) %% get the matlab struct for this flower
    [a,b,c] = fileparts(Petals.fullName);
    jpegName = char(dougDir + b + c); %% for header image 
    %% go to the ventral, central ("right") petal
    petal = Petals.Polys.right.petal(1);
    if isfield(Petals.Polys.right,'spots')
        spots = Petals.Polys.right.spots;
    else
        spots = [];
    end;
    bb = area(petal);
    sc = 1/sqrt(bb);
    cc = scale(petal, sc);
    [cenX,cenY] = centroid(cc);
    tPetal = translate(cc, -cenX, -cenY);
    %% spots
    counter = 1;
    for i = spots;
        cc = scale(i, sc);
        tSpots(counter) = translate(cc, -cenX, -cenY);
        counter = counter + 1;
    end;
    clear counter;
    if isempty(spots)
        tSpots = polyshape();
    end;
    figure; %% start plot
    subplot(3,3,[1,3]);
    imshow(jpegName);
    title(b) %% b was our flower name
    counter = 4; %% start at 4 because our first three spots are taken up by the photo
    for margI = margins
        marginSize = margI; %% set margin of exclusion, percentage of petal area
        inEdgeSize = 0.5; %% set amount of spot that is in margin that merits exclusion
        %%%%%%%%%%
        t = 0;
        perc = 0;
        while perc <= marginSize; %% set above, percent of petal area
            %disp("t = " + t)
            t = t - 0.001;
            middlePoly = polybuffer(tPetal,t);
            edgePoly = subtract(tPetal, middlePoly);
            perc = area(edgePoly) / area(tPetal);
            %disp("% = " + perc)
        end;
        middlePoly = polybuffer(tPetal,t);
        edgePoly = subtract(tPetal, middlePoly);
        %%%%%%%%%%%
        allInEdge = intersect(tSpots, edgePoly); 
        area(allInEdge)./area(tSpots); %% how much of each of our polygons are in this margins?
        notEdge = area(allInEdge)./area(tSpots) < inEdgeSize; %% which do we keep?
        cSpots = tSpots(notEdge);
        %%%%%%%%%%%
        [cX, cY] = centroid(cSpots);
        dsX = [cX, 0];
        dsY = [cY, 0];
        X = [dsX' dsY'];
        D = pdist(X);
        if isempty(D); %% deal with empty petal centers, set D = 1
            D = 1;
        end;
        centeredness = mean(D);
        ti = ('m = ' + string(margI) +", c = " + string(centeredness));
        subplot(3,3,counter);
            hold off;
            plot(tPetal, 'FaceAlpha', 0)
            hold on;
            plot(edgePoly, 'FaceAlpha', 0)
            plot(cSpots, 'FaceColor', 'red')
            title(ti)
            daspect([1 1 1]);
        counter = counter + 1;
    end;
    clear counter;
    clear tSpots;
    phN = '/Users/danthomas/Documents/speckling/center/mkPDF/' + string(b) + '.pdf';
    print(phN, '-dpdf','-bestfit')
    close
end;


