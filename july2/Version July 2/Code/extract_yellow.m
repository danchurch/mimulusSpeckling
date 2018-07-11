function Petals=extract_yellow(Petals)

% Get the values first:
TL=Petals.left.data; TR=Petals.right.data; TM=Petals.mid.data;

F=imread(Petals.fullName);

idx1=find(TL(:,4)==2);
GL=zeros(length(idx1),3);
for j=1:length(idx1)
      GL(j,:)=squeeze(F(TL(idx1(j),2),TL(idx1(j),1),:));
end
AvgYellow=mean(GL);

ZL=reshape(F(1:20,1:20,:),[400,3]); %Use a sample 20 x 20 grid in the corner
AvgBackground=mean(ZL);

Petals.left.yellow=AvgYellow;
Petals.left.tape=AvgBackground;

idx1=find(TR(:,4)==2);
GR=zeros(length(idx1),3);
for j=1:length(idx1)
      GR(j,:)=squeeze(F(TR(idx1(j),2),TR(idx1(j),1),:));
end
AvgYellow=mean(GR);

Petals.right.yellow=AvgYellow;
Petals.right.tape=AvgBackground;



idx1=find(TM(:,4)==2);
GM=zeros(length(idx1),3);
for j=1:length(idx1)
       GM(j,:)=squeeze(F(TM(idx1(j),2),TM(idx1(j),1),:));
end
AvgYellow=mean(GM);
Petals.mid.yellow=AvgYellow;
Petals.mid.tape=AvgBackground;


