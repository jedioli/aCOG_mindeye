filename = 'bensi_long_multi.csv';
M = csvread(filename,1,0);
[cols,rows] = size(M);
start = M(1,1);
for index = 1 : cols
    M(index,1) = M(index,1) - start;  % subscripts are row, col
    if M(index,2) < 0.75
       M(index,3) = NaN;
    end
end

D = [[120,0]    % time divisions
     [120.05,100]
     [120.1,NaN]
     [419.9,NaN]
     [420,0]
     [420.05,100]
     [420.1,NaN]
     [719.9,NaN]
     [720,0]
     [720.05,100]
     [720.1,NaN]
     [749.9,NaN]
     [750,40]
     [750.05,90]
     [750.1,NaN]
     [1049.9,NaN]
     [1050,0]
     [1050.05,100]];

plot(M(:,1), M(:,3), D(:,1), D(:,2));