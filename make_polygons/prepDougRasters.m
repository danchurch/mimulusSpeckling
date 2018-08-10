%%%%%%%%%%%%%%%%%%%%%%%%%%

%% a script to put all of Doug's rasters into a form we can use:

%% go to working directory
wd = '/Users/danthomas/Documents/speckling/make_polygons/polygons/';
cd(wd);

dougRasterDir = "/Users/danthomas/Documents/speckling/dougRaster/Rotated_and_Cropped/";

cd(dougRasterDir)

files = dir('P*.mat');
for file = files';
    im = file.name;
    imName = regexprep(im,'\.mat', ''); 
    %% go get our file, come back
    cd(dougRasterDir);
    rast=load(im);
    cd(wd);
    %% make a spot for our image, go to it:
    mkdir(imName);
    cd (imName);
    %% get our petal names (left, right mid)
    petNames = fieldnames(rast.Petals.Clusters);
    %% split images into petal and spot, export, for each of the three petals:
    for i = 1:length(petNames);
        pet = rast.Petals.Clusters.(petNames{i}); %petal at hand
        rastGray = mat2gray(pet); 
        spots = rastGray  < 1; 
        petal = rastGray == 0;
        mkdir(petNames{i});
        cd(petNames{i});
        fileNamePetal = imName + "_" +  petNames(i) + "_" + 'petal.csv';
        csvwrite(fileNamePetal,petal);
        fileNameSpots = imName + "_" +  petNames(i) + "_" + 'spots.csv';
        csvwrite(fileNameSpots,spots);
        cd ..;
    end;
    cd(wd);
end;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
