Hi everyone-

Melia and I worked out the code to get the photos processed. I think I will do some re-writing so that the code is a bit more modularized than it is now, which will also help in the documentation.

To reiterate a couple things- The "FlowerDemo.m" code was code to process a single photo (that photo being in the same directory as the code). This was to give you an idea of the data structures being created, and gave me a chance to illustrate with images.

For the main code that will process a bunch of photos, "process_init.m" should be in the same directory as a directory with the photos, and there should also be "single_process.m".

The code "process_init.m" will do the intial pass through the data, using "single_process.m", and will leave behind matlab data files with the same file names as the photos.

Melia and I changed the process_init.m file so that it would output an array with all of the proportion red values for every petal in every photo.

Doug

