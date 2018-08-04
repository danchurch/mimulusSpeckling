function [val,temp] = image_lacunarity(A)

% Needs to be updated in the case that there are no 1's...  Zero values result in NaN with no error catching.

% A= 1-im2bw(mydata.images.image(imgnum).CData,0.5);

N1 = size(A,1);
N2 = size(A,2);
result = [];

A = sparse(A);

for i = 1:1:floor(log2(max(N1,N2)))
	dat = [];
	for x = 1:1:2^i
		for y = 1:1:2^i
			
			x1 = floor(N1/2^i * (x-1) +1);
			x2 = floor(N1/2^i * x);
			
			y1 = floor(N2/2^i * (y-1) +1);
			y2 = floor(N2/2^i * y);
			mat = A(x1:1:x2 , y1:1:y2);
			dat = [dat , size(find(mat),1)];
		end
	end
	
	%size(dat)
	result = [result ,log(var(dat)/mean(dat)^2)/log(2)];

end

temp=[1:1:size(result,2) ; result ];
%fit_coeff = polyfit([1:1:size(result,2)] , result, 1);
fit_coeff = polyfit(temp(1,3:5) , temp(2,3:5), 1);
val = fit_coeff(1);


function result = calc_lacunarity(data)

result = calc_variance(data) / calc_mean(data) ^2;


