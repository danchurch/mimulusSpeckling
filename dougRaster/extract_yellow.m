function Petals=extract_yellow(Petals)
% Compute the average RGB values of all pixels labeled as "yellow" for a single petal structure/photo.

% Get the values first:
TL=Petals.left.data; TR=Petals.right.data; TM=Petals.mid.data;

F=imread(Petals.fullName);

idx1=find(TL(:,4)==2);
GL=zeros(length(idx1),3);
for j=1:length(idx1)
      GL(j,:)=squeeze(F(TL(idx1(j),2),TL(idx1(j),1),:));
end
AvgYellow=mean(GL);
Petals.left.yellow=AvgYellow;


idx1=find(TR(:,4)==2);
GR=zeros(length(idx1),3);
for j=1:length(idx1)
      GR(j,:)=squeeze(F(TR(idx1(j),2),TR(idx1(j),1),:));
end
AvgYellow=mean(GR);
Petals.right.yellow=AvgYellow;

idx1=find(TM(:,4)==2);
GM=zeros(length(idx1),3);
for j=1:length(idx1)
       GM(j,:)=squeeze(F(TM(idx1(j),2),TM(idx1(j),1),:));
end
AvgYellow=mean(GM);
Petals.mid.yellow=AvgYellow;


