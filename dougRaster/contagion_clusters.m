function rc=contagion_clusters(dmat)
%
% function rc=contagion_clusters(dmat)
%
%  This is a modification of contagion to deal with three "classes"
% Example of use:  rc=contagion_clusters(A);

%Error check:  The array should be 1's, 2's and 3's.

g=min(min(dmat));
h=max(max(dmat));
if g<1
    error('Error in computing contagion- Matrix has values less than one\n');
end
if h>3
    error('Error in computing contagion- Matrix has values greater than 3\n');
end



blobs=[1,2,3];  %This used to be a function argument.
n = 3;  %Length of "blobs"
[x, y] = size(dmat);

% inialise frequecy (pij) matrix
fmat = zeros(n,n);
pmat = zeros(1,n);

% Go through every 3 x 3 block (TIME SINK HERE)
    for iy=1:y-2
        for ix=1:x-2
            % identify blob type of center cell
            pt = dmat(ix+1,iy+1);  
            % get cube and place in vector
            cube=dmat(ix:ix+2,iy:iy+2);
            vcube=reshape(cube,1,9);
            % get frequency histogram for blob types
            fh = hist(vcube,blobs);
            % substract one for center type 
            fh(pt) = fh(pt) - 1;
            pmat(pt)=pmat(pt)+1;  %Keep count
            % add these frequencies to the frequency matrix
            fmat(pt,:) = fmat(pt,:) + fh;
        end
    end

%Currently, the frequency matrix is 3 x 3, we only need the 2 x 2
%submatrix.
    
% calculate the pij's (relative frequencies) (Li & Reynolds, Eqn 4)

p1=pmat(2)/(pmat(2)+pmat(3));
p2=pmat(3)/(pmat(2)+pmat(3));

fmatTest=fmat;   %For debugging purposes
fmat=fmat(2:3,2:3);
n=2;
rfmat=zeros(n,n);

for i=1:n
    temp=sum(fmat(i,:));
    if temp~=0
        rfmat(i,:)=fmat(i,:)/temp;
    end 
end

A=[p1*rfmat(1,:); p2*rfmat(2,:)];

% Cute trick to replace all zeros by a very small number (so the log
% doesn't give an error)

A(A == 0) = realmin;

ee=sum(sum(A.*log(A)));

% calculate emax (Li & Reynolds, Eqn 10)
emax = n* log(n);

% calculate contagion (Li & Reynolds, Eqn ?)
rc = 1 + ee/emax;

return


