filename = 'Ben_pupil_pos_15.csv';
M = csvread(filename,1,0);
[cols,rows] = size(M);
start = M(1,1);
for index = 1 : cols
    M(index,1) = M(index,1) - start;  % subscripts are row, col
    if M(index,2) < 0.75
       M(index,3) = NaN;
    end
end

T = [[125,0]    % time divisions
     [125.05,100]
     [125.1,NaN]
     [424.9,NaN]
     [425,0]
     [425.05,100]
     [425.1,NaN]
     [724.9,NaN]
     [725,0]
     [725.05,100]
     [725.1,NaN]
     [1034.9,NaN]
     [1035,0]
     [1035.05,100]];

R = gradient(M(:,3));
D2 = [diff(M(:,3),2); 0;0];
 
% plot(M(:,1), M(:,3), M(:,1), D, M(:,1), R, T(:,1), T(:,2));
plot(M(:,1), M(:,3), M(:,1), D2, T(:,1), T(:,2));