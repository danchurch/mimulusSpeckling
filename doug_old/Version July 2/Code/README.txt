The scripts here are designed to be modular after "process_init.m" has been run.

   * process_init.m is the main file to run, and it takes no arguments.  It assumes
       that all photos to be processed are in a folder in this directory, and that
       folder name is hard coded (right now, it is "raw_data").  Running this file
       will produce Matlab data files in the raw_data folder that each has the same 
       name as the flower.

    * single_process.m  is the file that is called internally by process_init.m

    * get_red_info.m:  Run this to extract the proportion red from all photos, 
        and put all the data into an array (saved as redData.mat in the raw_data folder).

    * split_all_petals.m:  Run this to graphically look at how the clustering was
        performed on each photo.  For a lot of photos, you might change the loop to
        go from 1 to 10 instead of 1 to the number of photos in the folder.

    * split_single_petal.m:  Called internally by split_all_petals.

Starting from scratch, 
   (1) Go to process_init.m, Line 8:  Write in the folder name for the photos.  Line 10:  Write either .jpg or .JPG, depending on how the photo files were stored.
   (2) Run the script by typing process_init into the command line.  
   (3) To gather the information about red pixels, after process_init is finished, type: get_red_info in the command window.  The data is put into an array (number of photos x 3).  This data is also stored in redData.mat, in the same folder as the photos.
   (4) To get a visual representation, type: split_all_petals in the command window.  There is a "pause" command being used, which pauses program execution after the graph is drawn-  To continue, press any key on the keyboard.  Since there could be 180 images, if you want to halt the program
early, press:  control-C   to kill the program.
