% Author: Aidan Lee
% Last Updated: 09/04/2021
%
% This script calculates the entropies in each frame of the slow-motion 
% video of the mechanical oscillating Galton board experiment

% clear existing variables and values in the workspace
clear 

% define directory
cd('D:\BlenderSaves\OGB\120fpsexperiment\10hzstabilized');

% read all files with .png extension
files = dir('*.png');



%% Get mode pixel values from first 185 frames
% define the sampling interval
firstframe=1;
lastframe=186;

for n=firstframe:lastframe

    % read and store the pixel values from png file
    img = imread(files(n).name); 
    data185(:,:,n)=img(940:1650,1125:2550,1); 
    n=n+1;
    
end

% calculate and store the mode of each pixel 
bk = mode(data185,3);

%% Process the images to calculate the entropy
for n=1:length(files)
    
    % read, store and crop the image
    img = imread(files(n).name);
    data(:,:)=img(940:1650,1125:2550,1);
    
    % remove the mode pixel values from the image
    imagesc(double(data(:,:))-double(bk));

    % apply threshold filter to isolate the dark balls
    bw=double(data(:,:))-double(bk)<-30;
    
    imagesc(bw);
    E(n) = entropy(bw); % calculate the entropy from the image
    colormap gray
    pause(0.1)
    
    % clear the stored image to free memory for the next image
    clear img
    clear data
end

% export the calculated entropies to a .csv file 
writematrix(E,'mechOGB_entropies.csv') 


