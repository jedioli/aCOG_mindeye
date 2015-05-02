filename = 'user3_135.csv';
M = csvread(filename,1,0);
[cols,rows] = size(M);
start = M(1,1);
for index = 1 : cols
    M(index,1) = M(index,1) - start;  % subscripts are row, col
    if M(index,2) < 0.75
       M(index,3) = NaN;
    end
end

WRONGT = [[121,0]    % time divisions
     [121.05,120]
     [121.1,NaN]
     [426.9,NaN]
     [427,0]
     [427.05,120]
     [427.1,NaN]
     [649.9,NaN]
     [650,0]
     [650.05,120]
     [650.1,NaN]
     [909.9,NaN]
     [910,0]
     [910.05,120]
     [910.1,NaN]
     [1089.9,NaN]
     [1090,0]
     [1090.05,120]
     [1090.1,NaN]
     [1394.9,NaN]
     [1395,0]
     [1395.05,120]];

R = gradient(M(:,3));   % seems a bit more drastic (smaller) than diff
D = [diff(M(:,3)); 0];
DD = [diff(D); 0];
DDD = [diff(DD); 0];

 
% plot(M(:,1), M(:,3), M(:,1), R, T(:,1), T(:,2));
plot(M(:,1), M(:,3), M(:,1), DDD, M(:,1), D);