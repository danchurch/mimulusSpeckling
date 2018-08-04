function A=split2clusters(Petals)
%  function A=splitPetals(Petals)
%   Takes the data structure in Petals (.left, .right, .mid) and creates
%   three separate simplified images A (A.left, A.right, A.mid) which are
%   have the value 1, 2 or 3 (rather than binary).
%

% This was modified from split_single_petal.

% Get the some values first to build the new arrays.

TL=Petals.left.data; TR=Petals.right.data; TM=Petals.mid.data;
TLxmin=min(TL(:,1)); TLxmax=max(TL(:,1)); TLymin=min(TL(:,2)); TLymax=max(TL(:,2)); 
TRxmin=min(TR(:,1)); TRxmax=max(TR(:,1)); TRymin=min(TR(:,2)); TRymax=max(TR(:,2));
TMxmin=min(TM(:,1)); TMxmax=max(TM(:,1)); TMymin=min(TM(:,2)); TMymax=max(TM(:,2));

A.left=ones(TLxmax-TLxmin+1,TLymax-TLymin+1);
A.right=ones(TRxmax-TRxmin+1,TRymax-TRymin+1);
A.mid=ones(TMxmax-TMxmin+1,TMymax-TMymin+1);

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




