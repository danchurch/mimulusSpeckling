function [A,B]=split_single_petal(Petals)
%  function A=splitPetals(Petals)
%   Takes the data structure in Petals (.left, .right, .mid) and creates
%   three separate simplified images A (A.left, A.right, A.mid).  In these,
%   the output colors are indexed by the Petals structure- Namely, 2 or 3.

% Future stuff:
%
% Put in an option to return binary images from only red for the other algorithms (0=background/yellow, 1=red)

% Get the values first:
TL=Petals.left.data; TR=Petals.right.data; TM=Petals.mid.data;
TLxmin=min(TL(:,1)); TLxmax=max(TL(:,1)); TLymin=min(TL(:,2)); TLymax=max(TL(:,2)); 
TRxmin=min(TR(:,1)); TRxmax=max(TR(:,1)); TRymin=min(TR(:,2)); TRymax=max(TR(:,2));
TMxmin=min(TM(:,1)); TMxmax=max(TM(:,1)); TMymin=min(TM(:,2)); TMymax=max(TM(:,2));

%% This section is for single-valued images, like the ones indexed by cluster

A.left=zeros(TLxmax-TLxmin+1,TLymax-TLymin+1);
A.right=zeros(TRxmax-TRxmin+1,TRymax-TRymin+1);
A.mid=zeros(TMxmax-TMxmin+1,TMymax-TMymin+1);

[m,n]=size(TL);
for j=1:m
    if TL(j,4)~=0
      xx=TL(j,1)-TLxmin+1; yy=TL(j,2)-TLymin+1;
      A.left(xx,yy)=TL(j,4);
    end
end

[m,n]=size(TR);
for j=1:m
    if TR(j,4)~=0
      xx=TR(j,1)-TRxmin+1; yy=TR(j,2)-TRymin+1;
      A.right(xx,yy)=TR(j,4);
    end
end
[m,n]=size(TM);
for j=1:m
    if TM(j,4)~=0
      xx=TM(j,1)-TMxmin+1; yy=TM(j,2)-TMymin+1;
      A.mid(xx,yy)=TM(j,4);
    end
end

%% Temporary section that loads the RGB values from the original images.
 
 F=imread(Petals.fullName);
 B.left=zeros(TLxmax-TLxmin+1,TLymax-TLymin+1,3);
 B.right=zeros(TRxmax-TRxmin+1,TRymax-TRymin+1,3);
 B.mid=zeros(TMxmax-TMxmin+1,TMymax-TMymin+1,3);

[m,n]=size(TL);
for j=1:m
    if TL(j,4)~=0
      xx=TL(j,1)-TLxmin+1; yy=TL(j,2)-TLymin+1;
      B.left(xx,yy,:)=F(TL(j,2),TL(j,1),:);
    end
end
[m,n]=size(TR);
for j=1:m
    if TR(j,4)~=0
      xx=TR(j,1)-TRxmin+1; yy=TR(j,2)-TRymin+1;
      B.right(xx,yy,:)=F(TR(j,2),TR(j,1),:);
    end
end
[m,n]=size(TM);
for j=1:m
    if TM(j,4)~=0
      xx=TM(j,1)-TMxmin+1; yy=TM(j,2)-TMymin+1;
      B.mid(xx,yy,:)=F(TM(j,2),TM(j,1),:);
    end
end


clim=[0,3];
subplot(3,2,1)
imagesc(A.left,clim);
axis equal; axis off;
subplot(3,2,3)
imagesc(A.right,clim); axis equal; axis off;
subplot(3,2,5)
imagesc(A.mid,clim); axis equal; axis off;

subplot(3,2,2)
imagesc(uint8(B.left)); axis equal; axis off;
subplot(3,2,4)
imagesc(uint8(B.right)); axis equal; axis off;
subplot(3,2,6)
imagesc(uint8(B.mid)); axis equal; axis off;

% NOTE:  To view these, need to convert to uint8, like: image(uint8(A.left))

