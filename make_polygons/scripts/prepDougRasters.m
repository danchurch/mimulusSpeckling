wd = '/home/daniel/Documents/cooley_lab/mimulusSpeckling/make_polygons/polygons';
dougRasterDir = '/home/daniel/Documents/cooley_lab/mimulusSpeckling/dougRaster/Rotated_and_Cropped';
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
        pet = rast.Petals.(petNames{i}).data; %petal at hand
        mkdir(petNames{i});
        cd(petNames{i});
        %% for octave
        fileNamePetal = [imName "_" char(petNames(i)) "_" 'melted.csv'];
        %% for matlab, this may work better?
        %%fileNamePetal = imName + "_" +  petNames(i) + "_" + 'melted.csv';
        csvwrite(fileNamePetal,pet);
        cd ..;
    end;
    cd(wd);
end;

## ' ## just because it's screwing up my syntax
