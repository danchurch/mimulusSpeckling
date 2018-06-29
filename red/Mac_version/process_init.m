%% This script will run single_process on all .jpg
% in the current folder, with folder marked "raw_data",
% and output a single data structure in that same folder.

% The input filenames
pic_files = dir('Rotated_and_Cropped/*.JPG');

% initializing the structure we will fill with wonderful data
%processed_data = struct();

for i = 1:length(pic_files)
    fprintf('Processing Image %d\n',i);
    % Iterating through pic_files, the object describing
    % all the .jpg contents of raw_data.
    folder_path = 'Rotated_and_Cropped/';
    sample_name_file = pic_files(i).name;
    pic = join([folder_path, sample_name_file]);
    
    % single_process is looking at pic, which is re-defined
    % in each loop, outputting the Petals structure
    % with all the processed data for each photo.
    Petals = single_process(pic);
    
    sample_name = sample_name_file(1:end-4);
    
    % file the Petals structure in processed_data under its name.
    processed_data{i} = Petals;
    red(i,1) = Petals.left.prop_red;
    red(i,2) = Petals.mid.prop_red;
    red(i,3) = Petals.right.prop_red;
    processed_data{i}.Name=sample_name;
    
    %% Before the loop is over
    % We harvest some data from each Petals to look at the
    % global data set with.
    
    % This will be used to histogram the proportion red for all data
    % samples processed
    prop_red_left_hist(i) = Petals.left.prop_red;
    prop_red_right_hist(i) = Petals.right.prop_red;
    prop_red_mid_hist(i) = Petals.mid.prop_red;
    
    % This measure tries to quantify the symmetry of the two side petals.
    % It takes the pr_red curve (proportion red as a function of r, the
    % radius of circles about the center of the petal) and compares them with
    % the sum of all differences in their curves. 
    symmetry_hist(i) =  sum(abs(Petals.left.pr_rad(:,2) - Petals.mid.pr_rad(:,2)));

    % Save the petals data 
    c=pwd;
    ss=join([c,'/',folder_path,sample_name,'.mat']);
    save(ss,'Petals');

end
save reddata red;
clear Petals

%% Now, we may output some measures of the entire data set processed.

% Note that one may change the binning options to fit their desires!

% First, the histograms of the proportion red.
left_pr = figure;
histogram(prop_red_left_hist);
title("Left Prop. Red");
right_pr = figure;
histogram(prop_red_right_hist);
title("Right Prop. Red");
mid_pr = figure;
histogram(prop_red_mid_hist);
title("Middle Prop. Red");

% Second, the histograms of the pr_rad differences between the left and
% middle petals.
symmetry = figure;
histogram(symmetry_hist);
title("Symmetry Measure");

% These histograms are saved in the folder where process_init is ran.
%saveas(left_pr, 'left_prop_red.png');
%saveas(right_pr, 'right_prop_red.png');
%saveas(mid_pr, 'mid_prop_red.png');
%saveas(symmetry, 'symmetry.png');


