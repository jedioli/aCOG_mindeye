%Creates the array from data
filename = '../user10_135.csv';
filemat = csvread(filename,1,0);
[cols,rows] = size(filemat);
start = filemat(1,1);

M = filemat;

for index = 1 : cols
    M(index,1) = M(index,1) - start;  % subscripts are row, col
    if M(index,2) < 0.75  %removes all confidence < .75
       M(index,3) = 0;  %replaces with 0 for counting later
    end
end


TIME = [[180,0]    % time divisions
     [180.1,120]
     [180.2,NaN]
     [359.9,NaN]
     [360,0]
     [360.1,120]
     [360.2,NaN]
     [541.9,NaN]
     [542,0]
     [542.1,120]
     [542.2,NaN]
     [721.9,NaN]
     [722,0]
     [722.1,120]
     [722.2,NaN]
     [901.9,NaN]
     [902,0]
     [902.1,120]
     [902.2,NaN]
     [1094.9,NaN]
     [1095,0]
     [1095.1,120]
     [1095.2,NaN]
     [1999.9,NaN]
     [1200,0]
     [1200.1,120]];


%delineates the section times

%rests
rest0 = M(1:5380, 1:3);
[rest0cols, rest0rows] = size(rest0);
rest0avg = sum(rest0(1:end, 3)) / (rest0cols - (sum(rest0(1:end, 3)==0)));

rest1 = M(10937:16215, 1:3);
[rest1cols, rest1rows] = size(rest1);
rest1avg = sum(rest1(1:end, 3)) / (rest1cols - (sum(rest1(1:end, 3)==0)));

rest2 = M(21766:27013, 1:3);
[rest2cols, rest2rows] = size(rest2);
rest2avg = sum(rest2(1:end, 3)) / (rest2cols - (sum(rest2(1:end, 3)==0)));

rest3 = M(32621:end, 1:3);
[rest3cols, rest3rows] = size(rest3);
rest3avg = sum(rest3(1:end, 3)) / (rest3cols - (sum(rest3(1:end, 3)==0)));

restavgmat = [rest0avg; rest1avg; rest2avg; rest3avg]

time0 = M(5507:10817, 1:3);
[t0cols, t0rows] = size( time0 );
time0nan = sum(time0( 1:end ) == 0);
time0avg = (sum(time0( 1:end, 3)) / (t0cols - time0nan));

time1 = M(16335:21646,1:3);
[t1cols, t1rows] = size(time1);
time1nan = sum(time1( 1:end ) == 0);
time1avg = (sum(time1( 1:end, 3)) / (t1cols - time0nan));

time2 = M(27133:32621,1:3);
[t2cols, t2rows] = size(time2);
time2nan = sum(time2( 1:end ) == 0);
time2avg = (sum(time2( 1:end, 3)) / (t2cols - time0nan));

timeavgmat = [time0avg; time1avg; time2avg]

resttot = [rest0; rest1; rest2]; %Vertically adds all rest matrices
[restcols, restrows] = size(resttot);
nancount = sum(resttot( 1:end ) == 0); %counts the number of 0's to ignore for avg
restszavg = sum(resttot(1:restcols, 3)) / (restcols - nancount); %finds avg of pupil size

%Rest Standard Deviation Calculations
mu = restszavg;
sumxi = sum((resttot( 1:end, 3 ) - mu ).^2);
std2 = sumxi / ( restcols - nancount );
reststddev = sqrt( std2 );

%Rest0 Standard Deviation Calculations
sumxir = sum((rest0( 1:end, 3) - mu ).^2);
std2r = sumxir / ( restcols - nancount );
rest0stddev = sqrt( std2r );

%Rest1 Standard Deviation Calculations
sumxir1 = sum((rest1( 1:end, 3) - mu ).^2);
std2r1 = sumxir1 / ( restcols - nancount );
rest1stddev = sqrt( std2r1 );

%Rest2 Standard Deviation Calculations
sumxir2 = sum((rest2( 1:end, 3) - mu ).^2);
std2r2 = sumxir2 / ( restcols - nancount );
rest2stddev = sqrt( std2r2 );

%Rest3 Standard Deviation Calculations
sumxir3 = sum((rest3( 1:end, 3) - mu ).^2);
std2r3 = sumxir3 / ( restcols - nancount );
rest3stddev = sqrt( std2r3 );

restsdmat = [reststddev; rest0stddev; rest1stddev; rest2stddev; rest3stddev]

%Time Standard Deviation
%Time0 Standard Deviation Calculations
sumxi0 = sum((time0( 1:end, 3) - mu ).^2);
std20 = sumxi0 / ( restcols - nancount );
time0stddev = sqrt( std20 );

%Time1 Standard Deviation Calculations
sumxi1 = sum((time1( 1:end, 3) - mu ).^2);
std21 = sumxi1 / ( restcols - nancount );
time1stddev = sqrt( std21 );

%Time2 Standard Deviation Calculations
sumxi2 = sum((time2( 1:end, 3) - mu ).^2);
std22 = sumxi2 / ( restcols - nancount );
time2stddev = sqrt( std22 );

timesdmat = [time0stddev; time1stddev; time2stddev]

%T-test and ANOVA test code
%{
%T-Test Space
%If the h == 1 it means the test rejects the null hypothesis
sizedavgt0 = resttot(500:9633);
[t0h, t0p, ci, stats] = ttest2(sizedavgt0( 1:end, 1), time0( 1:end, 3))

sizedavgt1 = restszavg;
[t1h, t1p, ci, stats] = ttest2(sizedavgt1( 1:end , 1), time1( 1:end , 3))

%ANOVA Test Plot
nova = anova1(M);
%}

%For plotting the pupil size graph
for index = 1 : cols
    filemat(index,1) = filemat(index,1) - start;  % subscripts are row, col
    if filemat(index,2) < 0.75  %removes all confidence < .75
       filemat(index,3) = NaN;  %replaces with NaN for deriving
    end
end

%Gives the derivative of the graph at each point
R = gradient(filemat(:,3));   % seems a bit more drastic (smaller) than diff
D = [diff(filemat(:,3)); 0];
DD = [diff(D); 0];

%Plot of the final graph
plot(filemat(:,1), filemat(:,3), filemat(:,1), DD,  TIME(:, 1), TIME(:,2));