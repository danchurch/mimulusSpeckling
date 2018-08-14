wd="/Users/danthomas/Documents/speckling/make_polygons/matObjW_pol"  %% right now our structures live here
dougdir = "/Users/danthomas/Documents/speckling/dougRaster/Rotated_and_Cropped/"; %% but original images here
pdfDir = "/Users/danthomas/Documents/speckling/make_polygons/bigPDF/"; %% we'll put pdfs here
cd(wd)

files = dir('P*.mat');
for file = files';
    %% get things loaded
    load(file.name)
    [a,b,c] = fileparts(Petals.fullName);
    jpegName = char(dougdir + b + c); %% gotta be a character object?
    pdfName = pdfDir + b + ".pdf"; %% doesn't have to be a character object?
    jpegN = imread(jpegName);
        %% plot a page:
        figure;
        %%%%%%%%% first row %%%%%%%%%%%%%%%
        subplot(3,3,[1,3]);
        imshow(jpegN);
        title(b) %% this is our plot title
        %%%%%%%%% second row %%%%%%%%%%%%%
        subplot(3,3,4);
        aa = mat2gray(Petals.Clusters.left);
        imshow(aa) 
        subplot(3,3,5);
        aa = mat2gray(Petals.Clusters.mid);
        imshow(aa) 
        subplot(3,3,6);
        aa = mat2gray(Petals.Clusters.right);
        imshow(aa) 
        %%%%%%%%%% third row %%%%%%%%%%%%%%
        subplot(3,3,7);
            if isfield(Petals.Polys.left,'petal');
            for i = Petals.Polys.left.petal;
                if ~isempty(i);
                    plot(i);
                    hold on %% keep the plot open;
                end;
            end; end;
            if isfield(Petals.Polys.left,'spots');
            for i = Petals.Polys.left.spots;
                if ~isempty(i);
                    plot(i);
                    hold on %% keep the plot open;
                end;
            end; end;
            daspect([1 1 1])
        subplot(3,3,8);
            if isfield(Petals.Polys.mid,'petal');
            for i = Petals.Polys.mid.petal;
                if ~isempty(i);
                    plot(i);
                    hold on %% keep the plot open;
                end;
            end; end;
            if isfield(Petals.Polys.mid,'spots');
            for i = Petals.Polys.mid.spots;
                if ~isempty(i);
                    plot(i);
                    hold on %% keep the plot open;
                end;
            end; end;
            daspect([1 1 1])
        subplot(3,3,9);
            if isfield(Petals.Polys.right,'petal');
            for i = Petals.Polys.right.petal;
                if ~isempty(i);
                    plot(i);
                    hold on %% keep the plot open;
                end;
            end; end;
            if isfield(Petals.Polys.right,'spots');
            for i = Petals.Polys.right.spots;
                if ~isempty(i);
                    plot(i);
                    hold on %% keep the plot open;
                end;
            end; end;
            daspect([1 1 1])
        %%%%%%%%%%%%%%
    %% print as a pdf page
    print(pdfName,'-dpdf', '-fillpage')
    close %% added after running, not sure if this works
end;

